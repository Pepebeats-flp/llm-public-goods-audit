"""Aggregates of Study 2 quoted in experimental_log.md that the two analysis scripts do not print.

  python3 -m pgg.extra_aggregates_study2
"""
import glob
import json
import os
import time

import pandas as pd

from .summarize import final_rows

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ORDER = ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"]


def load(pattern):
    return [json.loads(line) for f in sorted(glob.glob(os.path.join(ROOT, pattern))) for line in open(f)]


def hm(ts):
    return time.strftime("%d %b %H:%M", time.gmtime(ts)) + " UTC"


def main():
    # ---- part A -----------------------------------------------------------------------------
    raw = load("data/raw/study2_on_*.jsonl")
    on = pd.DataFrame([r for r in final_rows(raw) if r["kind"] == "decision" and r["valid"]])
    on["s"] = 100 * on.contribution / on.endowment
    print("== Part A ==")
    print(f"calls {len(raw)} | cells {on.key.nunique()} | invalid first attempts {sum(1 for r in raw if r['ok'] and not r['valid'])}"
          f" | failed calls {sum(1 for r in raw if not r['ok'])} | calls needing a transport retry {sum(1 for r in raw if r.get('transport_retries'))}")
    print("window:", hm(min(r["ts"] for r in raw)), "to", hm(max(r["ts"] for r in raw)))
    allow = sum((((r.get("usage") or {}).get("opencode") or {}).get("allowance") or 0) for r in raw)
    print(f"allowance {allow:.2f} USD")
    hi = on[on.mpcr == 1.25].groupby(["model", "variant"]).s.mean().unstack()[ORDER]
    print("\nReasoning on, m = 1.25: lowest and highest variant mean, and range")
    for m in hi.index:
        print(f"  {m:22} min {hi.loc[m].min():5.1f} ({hi.loc[m].idxmin()})  max {hi.loc[m].max():5.1f} ({hi.loc[m].idxmax()})  range {hi.loc[m].max() - hi.loc[m].min():5.1f}")
    dil = on[on.mpcr.between(0.26, 0.99)].groupby(["model", "variant"]).s.mean().unstack()[ORDER]
    print("\nReasoning on, dilemma: share of the 32 (MPCR x variant) cells per model in which every decision is zero")
    z = on[on.mpcr.between(0.26, 0.99)].groupby(["model", "mpcr", "variant"]).s.max().eq(0).groupby("model").mean() * 100
    print("  ", z.round(1).to_dict())
    print("Reasoning on, dilemma, pooled over the five models, by variant:", dil.mean().round(1).to_dict())
    tok = pd.Series([(r.get("usage") or {}).get("completion_tokens") for r in raw], index=[r["label"] for r in raw])
    print("median completion tokens per call:", tok.groupby(level=0).median().to_dict())

    # ---- part B -----------------------------------------------------------------------------
    rep = load("data/raw/study2_rep_*.jsonl")
    d = pd.DataFrame([r for r in rep if r["agent_type"] == "llm" and r["valid"] and r["game_status"] == "complete"])
    d["s"] = 100 * d.contribution / d.endowment
    print("\n== Part B ==")
    llm = [r for r in rep if r["agent_type"] == "llm"]
    print(f"LLM calls {len(llm)} | completed games {d.key.nunique()} | invalid outputs {sum(1 for r in llm if not r['valid'])}"
          f" | discarded games {len({r['key'] for r in rep if r['game_status'] == 'discarded'})}"
          f" | calls needing a transport retry {sum(1 for r in llm if r.get('transport_retries'))}")
    print("window:", hm(min(r["ts"] for r in llm)), "to", hm(max(r["ts"] for r in llm)))
    games = d.groupby(["label", "composition", "variant"]).key.nunique().unstack(fill_value=0)
    print("completed games per cell:\n", games.to_string())

    print("\nFirst decision under the baseline wording, reasoning off: one-shot (Study 1, m = 0.4) against round 1 of the repeated game")
    s1 = pd.DataFrame([r for r in final_rows(load("data/raw/final_off_*.jsonl")) if r["kind"] == "decision" and r["valid"]])
    s1["s"] = 100 * s1.contribution / s1.endowment
    one = s1[(s1.variant == "P0") & (s1.mpcr == 0.4)].groupby("model").s.mean()
    r1 = d[(d["round"] == 1) & (d.variant == "P0") & (d.composition == "homogeneous") & (d.effort == "none")].groupby("model").s.mean()
    for m in one.index:
        print(f"  {m:22} one-shot {one[m]:5.1f}   repeated, round 1 {r1.get(m, float('nan')):5.1f}")

    print("\nSame prompt, same settings, two batches: round 1 under P0 in the mixed-composition runs and in the homogeneous runs")
    for (model), part in d[(d["round"] == 1) & (d.variant == "P0") & (d.effort == "none")].groupby("model"):
        out = []
        for comp in ("one_selfish", "homogeneous"):
            p = part[part.composition == comp]
            share20 = 100 * (p.contribution == 20).mean()
            out.append(f"{comp}: n={len(p)} mean {p.s.mean():5.1f} answers of 20: {share20:5.1f}% ({hm(p.ts.min())} to {hm(p.ts.max())})")
        print(f"  {model:22} " + " | ".join(out), "| prompt hashes:", sorted(part.prompt_sha.unique()))

    print("\nMean contribution by round, reasoning off, homogeneous groups")
    t = d[(d.effort == "none") & (d.composition == "homogeneous")].groupby(["model", "variant", "round"]).s.mean().unstack().round(1)
    print(t.to_string())


if __name__ == "__main__":
    main()
