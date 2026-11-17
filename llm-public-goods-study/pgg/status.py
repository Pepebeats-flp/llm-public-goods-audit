"""Console status of the experiment runs.

  python3 -m pgg.status            # one snapshot
  python3 -m pgg.status --watch    # refresh every 5 s (Ctrl+C to leave; the runs keep going)
  python3 -m pgg.status --watch 2  # refresh every 2 s

Reads configs/*.json and data/raw/. It never touches the runs.
"""
import glob
import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAW = os.path.join(ROOT, "data", "raw")
BAR = 20


def alive_runs():
    """{config file name: pid} for live run_oneshot processes."""
    try:
        out = subprocess.run(["pgrep", "-af", "pgg.run_"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return {}
    procs = {}
    for line in out.splitlines():
        parts = line.split()
        if "pgrep" in line or len(parts) < 2:
            continue
        cfgs = [p for p in parts if p.endswith(".json")]
        if cfgs:
            procs[os.path.basename(cfgs[-1])] = parts[0]
    return procs


def supervisor():
    try:
        pid = int(open(os.path.join(RAW, "supervisor.pid")).read().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def is_repeated(cfg):
    return cfg.get("runner") == "repeated"


def calls_per_cell(cfg):
    """A cell is one decision (one-shot runs) or one game (repeated runs)."""
    if not is_repeated(cfg):
        return 1
    n_llm = cfg["n"] if cfg.get("composition", "homogeneous") == "homogeneous" else cfg["n"] - 1
    return n_llm * cfg["rounds"]


def total_cells(cfg):
    if is_repeated(cfg):
        return len(cfg["variants"]) * cfg["groups"] * len(cfg["models"])
    per_model = len(cfg["mpcrs"]) * len(cfg["variants"]) * cfg["reps"] + len(cfg["mpcrs"]) * cfg.get("comprehension_reps", 0) * 2
    return per_model * len(cfg["models"])


def gate_missing(cfg):
    """Path of the registration file a run waits for, if it is required and absent."""
    gate = cfg.get("gate_file")
    if not gate:
        return None
    path = os.path.normpath(os.path.join(ROOT, gate))
    return None if os.path.exists(path) else path


def bar(done, total):
    frac = done / total if total else 0
    full = int(round(BAR * min(frac, 1)))
    return "[" + "#" * full + "." * (BAR - full) + f"]{100 * frac:6.1f}%"


def hms(seconds):
    if seconds is None or seconds != seconds or seconds < 0:
        return "--"
    s = int(seconds)
    return f"{s // 3600}h{(s % 3600) // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def read_run(cfg):
    path = os.path.join(RAW, cfg["run_id"] + ".jsonl")
    d = {"rows": 0, "invalid": 0, "fails": 0, "retried": 0, "allowance": 0.0, "ts": [], "done": set(), "last": None,
         "discarded": set()}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue  # line still being written
                if "game_status" in r:               # repeated game: a cell is a finished game
                    d["done"].add(r["key"])
                    if r.get("game_status") == "discarded":
                        d["discarded"].add(r["key"])
                    if r.get("agent_type") != "llm":
                        continue
                    d["rows"] += 1
                    d["allowance"] += (((r.get("usage") or {}).get("opencode") or {}).get("allowance") or 0)
                    d["ts"].append(r["ts"])
                    d["last"] = r
                    if r.get("transport_retries"):
                        d["retried"] += 1
                    if not r.get("valid"):
                        d["invalid"] += 1
                    continue
                d["rows"] += 1
                d["allowance"] += (((r.get("usage") or {}).get("opencode") or {}).get("allowance") or 0)
                d["ts"].append(r["ts"])
                d["last"] = r
                if r.get("transport_retries"):
                    d["retried"] += 1
                if not r.get("ok"):
                    d["fails"] += 1
                elif not r.get("valid"):
                    d["invalid"] += 1
                if r.get("valid") or r.get("attempt", 1) >= 2:
                    d["done"].add(r["key"])
    return d


def log_tail(run_id, n=1):
    path = os.path.join(RAW, run_id + ".log")
    if not os.path.exists(path):
        return []
    with open(path, errors="replace") as f:
        return [x.rstrip() for x in f.readlines()[-n:]]


def snapshot():
    now = time.time()
    alive = alive_runs()
    runs = []
    for path in sorted(glob.glob(os.path.join(ROOT, "configs", "*.json"))):
        try:
            cfg = json.load(open(path))
        except Exception:
            continue
        if isinstance(cfg, dict) and "run_id" in cfg and "models" in cfg:
            runs.append((os.path.basename(path), cfg, read_run(cfg)))

    sup = supervisor()
    lines = [f"Estado de las corridas   {time.strftime('%Y-%m-%d %H:%M:%S')}",
             f"Supervisor: {'activo (pid %d), reinicia corridas caídas' % sup if sup else 'no activo'}", ""]

    names = {"final": "ESTUDIO 1 (final)", "study2": "ESTUDIO 2"}
    for grp in [g for g in ("final", "study2") if any(c.get("group") == g for _, c, _ in runs)]:
        part = [(n, c, d) for n, c, d in runs if c.get("group") == grp]
        tot = sum(total_cells(c) * calls_per_cell(c) for _, c, _ in part)
        done = sum(len(d["done"]) * calls_per_cell(c) for _, c, d in part)
        recent = sum(1 for _, _, d in part for t in d["ts"] if now - t <= 120)
        spent = sum(d["allowance"] for _, _, d in part)
        n_alive = sum(1 for n, _, _ in part if n in alive)
        lines.append(f"{names[grp]:18} {bar(done, tot)}  {done}/{tot} llamadas   {n_alive} de {len(part)} procesos activos")
        lines.append(f"  ritmo total {recent / 2:.0f} llamadas/min (últimos 2 min)   cuota usada {spent:.4f} USD")
        lines.append("")

    lines.append(f"{'corrida':34} {'estado':10} {'avance':28} {'celdas*':>11} {'/min':>5} {'falta':>7} {'inv':>4} {'reint':>5} {'fallos':>6}  última fila")
    warnings, etas = [], []
    for name, cfg, d in runs:
        tot, done, pid = total_cells(cfg), len(d["done"]), alive.get(name)
        recent = d["ts"][-30:]
        rate = (len(recent) - 1) / (recent[-1] - recent[0]) if len(recent) > 1 and recent[-1] > recent[0] else None
        eta = (tot - done) * calls_per_cell(cfg) / rate if rate and pid else None
        idle = now - d["ts"][-1] if d["ts"] else None
        if pid:
            state = "corriendo"
            if eta:
                etas.append(eta)
        elif tot and done >= tot:
            state = "terminada"
        elif d["rows"]:
            state = "DETENIDA"
            tail = " | ".join(log_tail(cfg["run_id"]))
            warnings.append(f"{cfg['run_id']}: detenida en {done}/{tot}. Último mensaje: {tail[:150]}")
        elif gate_missing(cfg):
            state = "bloqueada"
        else:
            state = "pendiente"
        if d["discarded"]:
            warnings.append(f"{cfg['run_id']}: {len(d['discarded'])} grupos descartados por dos respuestas inválidas")
        if pid and idle and idle > 300:
            warnings.append(f"{cfg['run_id']}: {hms(idle)} sin filas nuevas (reintentos o llamada colgada)")
        if d["fails"]:
            warnings.append(f"{cfg['run_id']}: {d['fails']} llamadas fallaron tras los reintentos")
        lines.append(f"{cfg['run_id']:34} {state:10} {bar(done, tot):28} {str(done) + '/' + str(tot):>11} "
                     f"{(60 * rate if rate and pid else 0):5.1f} {hms(eta):>7} {d['invalid']:4d} {d['retried']:5d} {d['fails']:6d}  "
                     f"{('hace ' + hms(idle)) if idle is not None else '-'}")
    if etas:
        lines += ["", f"Tiempo estimado hasta que termine la más lenta: {hms(max(etas))}"]

    sup_log = os.path.join(RAW, "supervisor.log")
    if os.path.exists(sup_log):
        with open(sup_log, errors="replace") as f:
            tail = [x.rstrip() for x in f.readlines()[-4:]]
        lines += ["", "Supervisor, últimos eventos:"] + ["  " + x for x in tail]
    if warnings:
        lines += ["", "AVISOS:"] + ["  " + w for w in warnings]
    if any(gate_missing(c) for _, c, _ in runs):
        lines += ["", "Las corridas 'bloqueada' esperan el registro público del plan de análisis:",
                  "  " + next(gate_missing(c) for _, c, _ in runs if gate_missing(c))]
    lines += ["", "* celda = una decisión (una ronda) o un juego completo (juego repetido)"]
    if not runs:
        lines.append("No hay configuraciones de corrida en configs/.")
    return "\n".join(lines)


def main(argv):
    if "--watch" in argv:
        i = argv.index("--watch")
        every = float(argv[i + 1]) if len(argv) > i + 1 else 5.0
        try:
            while True:
                text = snapshot()
                sys.stdout.write("\033[2J\033[H" + text + f"\n\n(se actualiza cada {every:g} s; Ctrl+C cierra esta vista, las corridas siguen)\n")
                sys.stdout.flush()
                time.sleep(every)
        except KeyboardInterrupt:
            print()
    else:
        print(snapshot())


if __name__ == "__main__":
    main(sys.argv[1:])
