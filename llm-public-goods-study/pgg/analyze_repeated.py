"""Study 2, part B: repeated game.

  python3 -m pgg.analyze_repeated                                  # study2_rep_*.jsonl
  python3 -m pgg.analyze_repeated --glob 'data/raw/x.jsonl' --tag x

Follows paper_ssc2027/preregistration_study2.md, part B. The group (one game) is the unit
of analysis: every interval is a percentile bootstrap over groups. Only completed games
are analysed; discarded games are counted and reported.
"""
import argparse
import glob
import json
import os

import numpy as np
import pandas as pd

from .analyze import ci, md
from .game import gini

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load(pattern):
    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        with open(path) as f:
            rows += [json.loads(line) for line in f if line.strip()]
    return pd.DataFrame(rows)


def boot_mean_diff(a, b, n_boot, rng):
    """Bootstrap of mean(a) - mean(b) for two independent sets of group-level values."""
    da = a[rng.integers(0, len(a), (n_boot, len(a)))].mean(1)
    db = b[rng.integers(0, len(b), (n_boot, len(b)))].mean(1)
    return da - db


def group_slopes(mat):
    """OLS slope of contribution on round for each group (rows = groups, columns = rounds)."""
    t = np.arange(1, mat.shape[1] + 1)
    tc = t - t.mean()
    return (mat - mat.mean(1, keepdims=True)) @ tc / (tc ** 2).sum()


def reciprocity(d):
    """Per group: slope of an agent's contribution on the others' mean in the previous round,
    with the agent's own previous contribution as a covariate. Returns one coefficient per group."""
    out = []
    for _, g in d.groupby("key"):
        g = g.sort_values(["seat", "round"])
        g["lag_others"] = g.groupby("seat").others_mean.shift(1)
        g["lag_own"] = g.groupby("seat").contribution.shift(1)
        g = g.dropna(subset=["lag_others", "lag_own"])
        X = np.column_stack([np.ones(len(g)), g.lag_others, g.lag_own]).astype(float)
        y = g.contribution.to_numpy(float)
        if np.linalg.matrix_rank(X) < 3:
            out.append(np.nan)      # no variation to identify the response in this group
            continue
        out.append(np.linalg.lstsq(X, y, rcond=None)[0][1])
    return np.array(out, float)


def analyse(pattern, tag, n_boot, seed):
    raw = load(pattern)
    if raw.empty:
        raise SystemExit("no repeated-game data for " + pattern)
    rng = np.random.default_rng(seed)
    out = os.path.join(ROOT, "data", "processed")
    rep = [f"# Study 2, part B: {tag}\n"]
    P = rep.append

    games = raw.groupby("key").agg(status=("game_status", "first"), label=("label", "first"),
                                   composition=("composition", "first"), variant=("variant", "first"))
    q = games.groupby(["label", "composition", "variant"]).status.value_counts().unstack(fill_value=0)
    q.to_csv(os.path.join(out, f"{tag}_games.csv"))
    P("## Games by status\n\n" + md(q) + "\n")

    d = raw[(raw.game_status == "complete") & (raw.agent_type == "llm") & raw.valid.astype(bool)].copy()
    E, T = int(d.endowment.iloc[0]), int(d.rounds.iloc[0])
    d["s"] = 100.0 * d.contribution / E
    calls = len(raw[raw.agent_type == "llm"])
    allowance = sum((((u or {}).get("opencode") or {}).get("allowance") or 0) for u in raw["usage"] if isinstance(u, dict))
    P(f"LLM calls: {calls} | completed games: {int((games.status == 'complete').sum())} | discarded: "
      f"{int((games.status == 'discarded').sum())} | rounds: {T} | allowance: {allowance:.4f} USD | bootstrap: {n_boot}\n")

    # group x round matrix of the mean contribution of the LLM seats
    cells = {}
    for (label, comp, variant), part in d.groupby(["label", "composition", "variant"]):
        mat = part.groupby(["key", "round"]).s.mean().unstack().to_numpy(float)
        cells[(label, comp, variant)] = (mat, part)

    rows, traj = [], []
    for (label, comp, variant), (mat, part) in cells.items():
        g = mat.shape[0]
        idx = rng.integers(0, g, (n_boot, g))
        sl = group_slopes(mat)
        end = mat[:, -1] - mat[:, -4:-1].mean(1)
        rec = reciprocity(part)
        rec_ok = rec[np.isfinite(rec)]
        pay = part.groupby(["key", "seat"]).payoff.sum().groupby("key").apply(lambda x: gini(list(x))).to_numpy(float)

        def b(v):
            return ci(v[idx].mean(1))

        row = dict(label=label, composition=comp, variant=variant, groups=g,
                   round1=mat[:, 0].mean(), round1_lo=b(mat[:, 0])[0], round1_hi=b(mat[:, 0])[1],
                   roundT=mat[:, -1].mean(), roundT_lo=b(mat[:, -1])[0], roundT_hi=b(mat[:, -1])[1],
                   all_rounds=mat.mean(), all_lo=b(mat.mean(1))[0], all_hi=b(mat.mean(1))[1],
                   slope_per_round=sl.mean(), slope_lo=b(sl)[0], slope_hi=b(sl)[1],
                   endgame=end.mean(), endgame_lo=b(end)[0], endgame_hi=b(end)[1],
                   gini_payoffs=pay.mean(), reciprocity_groups=len(rec_ok))
        if len(rec_ok) >= 2:
            ridx = rng.integers(0, len(rec_ok), (n_boot, len(rec_ok)))
            lo, hi = ci(rec_ok[ridx].mean(1))
            row.update(reciprocity=rec_ok.mean(), reciprocity_lo=lo, reciprocity_hi=hi)
        rows.append(row)
        for t in range(T):
            lo, hi = b(mat[:, t])
            traj.append(dict(label=label, composition=comp, variant=variant, round=t + 1, mean=mat[:, t].mean(), ci_lo=lo, ci_hi=hi))
    summ = pd.DataFrame(rows)
    summ.to_csv(os.path.join(out, f"{tag}_summary.csv"), index=False)
    pd.DataFrame(traj).to_csv(os.path.join(out, f"{tag}_trajectories.csv"), index=False)
    P("## Contribution of the LLM agents (% of endowment), by condition\n")
    show = ["label", "composition", "variant", "groups", "round1", "roundT", "all_rounds", "slope_per_round", "slope_lo", "slope_hi",
            "endgame", "reciprocity", "reciprocity_lo", "reciprocity_hi", "reciprocity_groups", "gini_payoffs"]
    P(md(summ[[c for c in show if c in summ]].round(3), index=False) + "\n")

    # D1: wording gap in round 1 and in the last round (homogeneous groups)
    rows = []
    pairs = [("F2", "F3"), ("F2", "P0"), ("P0", "F3")]
    family = len({k[0] for k in cells if k[0].endswith("@none") and k[1] == "homogeneous"}) or 1
    level_fw = 100 * (1 - 0.05 / family)                        # Bonferroni across reasoning-off models
    for label in sorted({k[0] for k in cells}):
        for hi_v, lo_v in pairs:
            ka, kb = (label, "homogeneous", hi_v), (label, "homogeneous", lo_v)
            if ka not in cells or kb not in cells:
                continue
            A, B = cells[ka][0], cells[kb][0]
            row = dict(label=label, contrast=f"{hi_v} - {lo_v}")
            for name, col in (("round1", 0), ("roundT", -1)):
                diff = boot_mean_diff(A[:, col], B[:, col], n_boot, rng)
                lo, hi = ci(diff)
                lo_f, hi_f = ci(diff, level_fw)
                row.update({f"gap_{name}": A[:, col].mean() - B[:, col].mean(), f"{name}_lo": lo, f"{name}_hi": hi,
                            f"{name}_lo_fw": lo_f, f"{name}_hi_fw": hi_f, f"{name}_nonzero": bool(lo_f > 0 or hi_f < 0)})
            rows.append(row)
    d1 = pd.DataFrame(rows)
    d1.to_csv(os.path.join(out, f"{tag}_D1_wording_gap.csv"), index=False)
    P("## D1: gap between wordings in round 1 and in the last round (percentage points)\n")
    P(md(d1.round(1), index=False) + "\n")

    # D4: one selfish rule agent in the group, baseline wording
    rows = []
    for label in sorted({k[0] for k in cells}):
        ka, kb = (label, "one_selfish", "P0"), (label, "homogeneous", "P0")
        if ka not in cells or kb not in cells:
            continue
        A, B = cells[ka][0], cells[kb][0]
        for name, sl in (("round1", slice(0, 1)), ("rounds2toT", slice(1, None))):
            a, b_ = A[:, sl].mean(1), B[:, sl].mean(1)
            lo, hi = ci(boot_mean_diff(a, b_, n_boot, rng))
            rows.append(dict(label=label, rounds=name, with_selfish=a.mean(), homogeneous=b_.mean(), diff_pp=a.mean() - b_.mean(), ci_lo=lo, ci_hi=hi))
    if rows:
        d4 = pd.DataFrame(rows)
        d4.to_csv(os.path.join(out, f"{tag}_D4_one_selfish.csv"), index=False)
        P("## D4 (exploratory): LLM agents with one selfish rule agent in the group, against homogeneous groups, wording P0\n")
        P(md(d4.round(1), index=False) + "\n")

    path = os.path.join(out, f"{tag}_analysis.md")
    open(path, "w").write("\n".join(rep))
    print("report:", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="data/raw/study2_rep_*.jsonl")
    ap.add_argument("--tag", default="study2B")
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20270403)
    a = ap.parse_args()
    analyse(a.glob, a.tag, a.boot, a.seed)
