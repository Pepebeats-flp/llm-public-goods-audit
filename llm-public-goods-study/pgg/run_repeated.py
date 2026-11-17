"""Runner for the repeated game (Study 2, part B).

Usage: python3 -m pgg.run_repeated configs/<name>.json

Config keys:
  run_id, group, runner ("repeated")
  n, endowment, mpcr, rounds
  models            list with one {"model": id, "effort": ...}
  variants          prompt variants (subset of pgg.prompts.REPEATED_VARIANTS)
  groups            number of games per (model, variant)
  composition       "homogeneous" (n LLM agents) or "one_selfish" (n-1 LLM agents and one
                    rule-based agent that always contributes 0, in the last seat)
  temperature, min_interval, max_allowance_usd, seed

A game is atomic. Its rows are written only when the game ends, so resuming never
leaves half games in the data.

Rules fixed before running:
  * In every round each LLM agent gets a fresh single-message call with the rules and its
    own history (own contribution, mean of the others, own payoff per past round).
  * Transport failures are retried up to 3 times (see run_oneshot._call). If a call still
    fails, the game is abandoned without being recorded and is played again on resume.
  * An output with no valid action is asked once more. If the second output is also
    invalid the group is discarded: its rows are written with game_status "discarded"
    and it is not replayed.
"""
import hashlib
import json
import os
import random
import sys
import time

from .agents import Selfish
from .game import Game
from .llm import Client, parse_amount
from .prompts import repeated_prompt
from .run_oneshot import _allowance, _call


def _finished_games(path):
    keys = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("game_status") in ("complete", "discarded"):
                    keys.add(row["key"])
    return keys


def play_game(game, rounds, seats, variant, decide):
    """Play one game.

    seats: list of "llm" or "selfish", one per player.
    decide(seat_index, prompt): returns (contribution or None, list of attempt records).
        None with a non-empty list means two invalid outputs; None with records flagged
        transport_failed means the call could not be completed.
    Returns (status, rows) with status in {"complete", "discarded", "transport_failed"}.
    """
    histories = [[] for _ in seats]
    rows = []
    rule = Selfish()
    for t in range(1, rounds + 1):
        contributions = []
        round_rows = []
        for i, kind in enumerate(seats):
            if kind == "selfish":
                c = rule.act(game, histories[i])
                round_rows.append({"round": t, "seat": i, "agent_type": "selfish", "attempt": 1, "valid": True,
                                   "amount": c, "contribution": c})
                contributions.append(c)
                continue
            prompt, conv = repeated_prompt(variant, game, rounds, t, histories[i])
            c, attempts = decide(i, prompt)
            for a in attempts:
                a.update(round=t, seat=i, agent_type="llm",
                         prompt_sha=hashlib.sha256(prompt.encode()).hexdigest()[:12])
                round_rows.append(a)
            if c is None:
                rows += round_rows
                failed = any(a.get("transport_failed") for a in attempts)
                return ("transport_failed" if failed else "discarded"), rows
            contributions.append(conv(c))
        payoffs = game.payoffs(contributions)
        for i in range(len(seats)):
            others = [c for j, c in enumerate(contributions) if j != i]
            histories[i].append({"round": t, "own": contributions[i], "payoff": payoffs[i],
                                 "others_mean": sum(others) / len(others)})
        for r in round_rows:
            if r["valid"]:
                i = r["seat"]
                r.update(payoff=payoffs[i], others_mean=histories[i][-1]["others_mean"],
                         round_total=sum(contributions))
        rows += round_rows
    return "complete", rows


def main(config_path):
    cfg = json.load(open(config_path))
    out_path = os.path.join("data", "raw", cfg["run_id"] + ".jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    done = _finished_games(out_path)
    client = Client("pgg-" + cfg["run_id"], min_interval=cfg.get("min_interval", 1.5))
    mc = cfg["models"][0]
    label = mc.get("label") or f"{mc['model']}@{mc.get('effort')}"
    game = Game(cfg["n"], cfg["endowment"], round(cfg["mpcr"] * cfg["n"], 6))
    composition = cfg.get("composition", "homogeneous")
    seats = ["llm"] * cfg["n"] if composition == "homogeneous" else ["llm"] * (cfg["n"] - 1) + ["selfish"]

    tasks = [(v, gi) for v in cfg["variants"] for gi in range(cfg["groups"])]
    random.Random(cfg.get("seed", 0)).shuffle(tasks)

    spent = [0.0]
    cap = cfg.get("max_allowance_usd", 1.0)

    def decide(seat, prompt):
        attempts = []
        for attempt in (1, 2):
            resp, retries, temp_used = _call(client, mc["model"], prompt, cfg.get("temperature"), mc.get("effort"))
            spent[0] += _allowance(resp)
            amount = parse_amount(resp.get("text"), game.endowment) if resp["ok"] else None
            attempts.append({
                "ts": time.time(), "attempt": attempt, "ok": resp["ok"], "transport_retries": retries,
                "temperature": temp_used, "text": resp.get("text"), "reasoning_text": resp.get("reasoning_text"),
                "finish_reason": resp.get("finish_reason"), "served_model": resp.get("served_model"),
                "usage": resp.get("usage"), "latency_s": resp.get("latency_s"), "error": resp.get("error"),
                "http_status": resp.get("http_status"), "amount": amount, "contribution": amount,
                "valid": amount is not None, "transport_failed": not resp["ok"],
            })
            if not resp["ok"]:
                return None, attempts
            if amount is not None:
                return amount, attempts
        return None, attempts

    n_games = 0
    with open(out_path, "a") as out:
        for variant, gi in tasks:
            key = f"game|{label}|{composition}|{variant}|{gi}"
            if key in done:
                continue
            if spent[0] >= cap:
                print(f"allowance cap reached ({spent[0]:.4f} >= {cap}); stopping", flush=True)
                break
            status, rows = play_game(game, cfg["rounds"], seats, variant, decide)
            if status == "transport_failed":
                err = next((r.get("error") for r in rows if r.get("transport_failed")), "")
                http = next((r.get("http_status") for r in rows if r.get("transport_failed")), None)
                if http in (401, 402, 403):
                    print("authorisation or quota error; stopping:", err, flush=True)
                    break
                print(f"game {key} abandoned after a transport failure; it will be replayed", flush=True)
                continue
            for r in rows:
                r.update(key=key, run_id=cfg["run_id"], kind="repeated_decision", label=label, model=mc["model"],
                         effort=mc.get("effort"), variant=variant, composition=composition, game_index=gi,
                         n=game.n, endowment=game.endowment, mpcr=cfg["mpcr"], r=game.r, rounds=cfg["rounds"],
                         game_status=status)
                out.write(json.dumps(r) + "\n")
            out.flush()
            n_games += 1
            print(f"{n_games} games written ({status}), allowance used {spent[0]:.4f} USD", flush=True)
    print(f"finished: {n_games} new games, allowance used this session {spent[0]:.4f} USD, file {out_path}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
