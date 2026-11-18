"""Launch the final runs and keep them going.

  python3 -m pgg.launch             # start everything that is pending, then show the live status
  python3 -m pgg.launch --no-watch  # start and return
  python3 -m pgg.launch --stop      # stop the supervisor and all runs (they can be resumed later)

One detached process per study config in configs/ (group "final", "study2" or "study3"), plus a detached supervisor that
checks every 30 s and restarts a run that died before finishing. Runs are resumable, so a
restart never repeats a completed cell. Closing the terminal or pressing Ctrl+C in the
status view does not stop anything. Running this command again is safe: it starts only
what is not already running or finished.

The supervisor does not restart a run that stopped for a reason a person must look at:
authorisation or quota errors, or the allowance cap of the config. A config with a
"gate_file" is not started until that file exists. Study 3 uses this: nothing starts until
paper_ssc2027/STUDY3_GO.txt exists, which is created after the analysis plan is public.
"""
import glob
import json
import os
import signal
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAW = os.path.join(ROOT, "data", "raw")
SUP_PID = os.path.join(RAW, "supervisor.pid")
SUP_LOG = os.path.join(RAW, "supervisor.log")
MAX_RESTARTS = 5
MAX_PARALLEL = 18   # runs alive at the same time
BLOCKERS = ("authorisation or quota error", "allowance cap reached")


from .status import gate_missing, read_run, total_cells  # noqa: E402

GROUPS = ("final", "study2", "study3")


def configs():
    """Configs that belong to a study (pilot and technical tests are run by hand)."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "configs", "*.json"))):
        cfg = json.load(open(path))
        if isinstance(cfg, dict) and "run_id" in cfg and "models" in cfg and cfg.get("group") in GROUPS:
            out.append((path, cfg))
    return out


def done_cells(cfg):
    return len(read_run(cfg)["done"])


def run_pid(path):
    """PID of the live runner for this config, or None."""
    out = subprocess.run(["pgrep", "-af", "pgg.run_"], capture_output=True, text=True).stdout
    name = os.path.basename(path)
    for line in out.splitlines():
        parts = line.split()
        if len(parts) > 1 and parts[-1].endswith(name) and "pgrep" not in line:
            return int(parts[0])
    return None


def blocker(cfg):
    """Reason the run must not be restarted automatically, or None."""
    log = os.path.join(RAW, cfg["run_id"] + ".log")
    if not os.path.exists(log):
        return None
    with open(log, errors="replace") as f:
        tail = f.readlines()[-5:]
    for line in tail:
        for b in BLOCKERS:
            if b in line:
                return line.strip()[:160]
    return None


def start_run(path, cfg):
    log = open(os.path.join(RAW, cfg["run_id"] + ".log"), "a")
    subprocess.Popen(
        [sys.executable, "-m", "pgg.run_repeated" if cfg.get("runner") == "repeated" else "pgg.run_oneshot",
         os.path.relpath(path, ROOT)],
        cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True,
    )


def note(msg):
    with open(SUP_LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def supervisor_pid():
    try:
        pid = int(open(SUP_PID).read().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def supervise():
    """Runs detached. Starts pending runs, restarts dead ones, exits when nothing is left to do."""
    with open(SUP_PID, "w") as f:
        f.write(str(os.getpid()))
    note(f"supervisor started (pid {os.getpid()})")
    restarts = {}
    try:
        while True:
            pending = 0
            running = sum(1 for path, _ in configs() if run_pid(path))
            for path, cfg in configs():
                rid = cfg["run_id"]
                if done_cells(cfg) >= total_cells(cfg):
                    continue
                if run_pid(path):
                    pending += 1
                    continue
                if gate_missing(cfg):
                    if restarts.get(rid) != "gated":
                        note(f"{rid}: waiting for the gate file {gate_missing(cfg)}")
                        restarts[rid] = "gated"
                    continue
                if restarts.get(rid) == "gated":
                    restarts.pop(rid)
                why = blocker(cfg)
                if why:
                    if restarts.get(rid) != "blocked":
                        note(f"{rid}: NOT restarted, needs attention: {why}")
                        restarts[rid] = "blocked"
                    continue
                if running >= MAX_PARALLEL:
                    pending += 1
                    continue
                n = restarts.get(rid, 0)
                if n > MAX_RESTARTS:
                    if restarts.get(rid) != "given_up":
                        note(f"{rid}: gave up after {MAX_RESTARTS} restarts")
                        restarts[rid] = "given_up"
                    continue
                start_run(path, cfg)
                note(f"{rid}: {'started' if n == 0 else f'restarted ({n})'} at {done_cells(cfg)}/{total_cells(cfg)} cells")
                restarts[rid] = n + 1
                running += 1
                pending += 1
                time.sleep(2)  # stagger the starts
            if pending == 0:
                note("nothing left to run; supervisor exiting")
                return
            time.sleep(30)
    finally:
        try:
            os.remove(SUP_PID)
        except OSError:
            pass


def stop_all():
    pid = supervisor_pid()
    if pid:
        os.kill(pid, signal.SIGTERM)
        print(f"supervisor detenido (pid {pid})")
    for path, cfg in configs():
        p = run_pid(path)
        if p:
            os.kill(p, signal.SIGTERM)
            print(f"detenida {cfg['run_id']} (pid {p})")
    note("stopped by user")


def main(argv):
    os.makedirs(RAW, exist_ok=True)
    if "--supervise" in argv:
        supervise()
        return
    if "--stop" in argv:
        stop_all()
        return
    if not configs():
        print("No hay configuraciones de estudio en configs/")
        return
    if supervisor_pid():
        print(f"El supervisor ya está activo (pid {supervisor_pid()}).")
    else:
        log = open(SUP_LOG, "a")
        subprocess.Popen([sys.executable, "-m", "pgg.launch", "--supervise"], cwd=ROOT,
                         stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        print("Supervisor iniciado. Arranca una corrida cada 2 segundos.")
        time.sleep(3)
    if "--no-watch" not in argv:
        from . import status
        status.main(["--watch"])


if __name__ == "__main__":
    main(sys.argv[1:])
