"""Runner for one-shot decisions (experiments E1 and E2) and comprehension probes.

Usage: python3 -m pgg.run_oneshot configs/<name>.json

Config keys:
  run_id            label; output goes to data/raw/<run_id>.jsonl (appended, resumable)
  n, endowment      game size
  mpcrs             list of marginal per capita returns
  models            list of {"model": id, "effort": "none"|"low"|"high"|..., "label": str}
  variants          list of prompt variant names (see pgg.prompts.VARIANTS)
  reps              decisions per (model, mpcr, variant) cell
  temperature       number or null (provider default)
  comprehension_reps  probes per (model, mpcr, item); 0 to skip
  max_allowance_usd stop when the cumulative allowance reported by the provider reaches this
  min_interval      seconds between requests
  seed              shuffles the order of cells so that time is not confounded with condition

Rules fixed before running:
  * Transport failures (HTTP 429/5xx, timeouts) are retried up to 3 times with backoff and
    logged; they are not model outputs.
  * An output with no valid action is recorded as invalid and the cell is asked once more
    (attempt 2). Both rows are kept. Nothing is repaired.
"""
import hashlib
import json
import os
import random
import sys
import time

from .game import Game
from .llm import Client, parse_amount, parse_json_field
from .prompts import KIND, VARIANTS, comprehension_items


def _done_keys(path):
    keys = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                row = json.loads(line)
                if row.get("valid") or row.get("attempt", 1) >= 2:
                    keys.add(row["key"])
    return keys


def _allowance(resp):
    return (((resp.get("usage") or {}).get("opencode") or {}).get("allowance")) or 0.0


def _call(client, model, prompt, temperature, effort):
    """Call with transport retries. Returns (response, transport_retries, temperature_used)."""
    retries, temp = 0, temperature
    while True:
        resp = client.chat(model, prompt, temperature=temp, reasoning_effort=effort)
        if resp["ok"]:
            return resp, retries, temp
        status, err = resp.get("http_status"), resp.get("error", "")
        if status == 400 and temp is not None and "temperature" in err.lower():
            temp = None  # model does not accept the parameter: use provider default, and record it
            continue
        if status in (401, 402, 403):
            return resp, retries, temp
        retries += 1
        if retries > 3:
            return resp, retries, temp
        time.sleep(10 * retries)


def main(config_path):
    cfg = json.load(open(config_path))
    out_path = os.path.join("data", "raw", cfg["run_id"] + ".jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    done = _done_keys(out_path)
    client = Client("pgg-" + cfg["run_id"], min_interval=cfg.get("min_interval", 1.5))

    tasks = []
    for mc in cfg["models"]:
        label = mc.get("label") or f"{mc['model']}@{mc.get('effort')}"
        for m in cfg["mpcrs"]:
            for v in cfg["variants"]:
                for rep in range(cfg["reps"]):
                    tasks.append(("decision", mc, label, m, v, rep))
            for rep in range(cfg.get("comprehension_reps", 0)):
                for item in (0, 1):
                    tasks.append(("comprehension", mc, label, m, f"Q{item + 1}", rep))
    random.Random(cfg.get("seed", 0)).shuffle(tasks)

    spent = 0.0
    cap = cfg.get("max_allowance_usd", 1.0)
    n_new = 0
    with open(out_path, "a") as out:
        for kind, mc, label, m, v, rep in tasks:
            key = f"{kind}|{label}|{m}|{v}|{rep}"
            if key in done:
                continue
            if spent >= cap:
                print(f"allowance cap reached ({spent:.4f} >= {cap}); stopping", flush=True)
                break
            game = Game(cfg["n"], cfg["endowment"], round(m * cfg["n"], 6))
            if kind == "decision":
                prompt, conv = VARIANTS[v](game)
            else:
                item_name, prompt, correct = comprehension_items(game)[int(v[1]) - 1]
            for attempt in (1, 2):
                resp, retries, temp_used = _call(client, mc["model"], prompt, cfg.get("temperature"), mc.get("effort"))
                spent += _allowance(resp)
                row = {
                    "key": key, "run_id": cfg["run_id"], "ts": time.time(), "kind": kind,
                    "label": label, "model": mc["model"], "effort": mc.get("effort"),
                    "temperature": temp_used, "n": game.n, "endowment": game.endowment,
                    "mpcr": m, "r": game.r, "regime": game.regime,
                    "variant": v, "rep": rep, "attempt": attempt,
                    "prompt_sha": hashlib.sha256(prompt.encode()).hexdigest()[:12],
                    "ok": resp["ok"], "transport_retries": retries,
                    "text": resp.get("text"), "reasoning_text": resp.get("reasoning_text"),
                    "finish_reason": resp.get("finish_reason"), "served_model": resp.get("served_model"),
                    "usage": resp.get("usage"), "latency_s": resp.get("latency_s"),
                    "error": resp.get("error"), "http_status": resp.get("http_status"),
                }
                if kind == "decision":
                    amount = parse_amount(resp.get("text"), game.endowment) if resp["ok"] else None
                    row.update(variant_kind=KIND[v], amount=amount, valid=amount is not None,
                               contribution=conv(amount) if amount is not None else None)
                else:
                    ans = parse_json_field(resp.get("text"), "answer") if resp["ok"] else None
                    numeric = isinstance(ans, (int, float)) and not isinstance(ans, bool)
                    row.update(item=item_name, answer=ans, correct_answer=correct, valid=numeric,
                               correct=bool(numeric and abs(ans - correct) < 1e-6))
                out.write(json.dumps(row) + "\n")
                out.flush()
                n_new += 1
                if row["valid"] or not resp["ok"]:
                    break
            if not resp["ok"] and resp.get("http_status") in (401, 402, 403):
                print("authorisation or quota error; stopping:", resp.get("error"), flush=True)
                break
            if n_new % 25 == 0:
                print(f"{n_new} rows written, allowance used {spent:.4f} USD", flush=True)
    print(f"finished: {n_new} new rows, allowance used this session {spent:.4f} USD, file {out_path}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
