"""Study 2, part A: reasoning on, all eight prompt variants (one-shot).

  python3 -m pgg.analyze_study2                  # Study 2 reasoning-on data against Study 1
  python3 -m pgg.analyze_study2 --selftest       # code check on Study 1 reasoning-off data only

Follows paper_ssc2027/preregistration_study2.md, part A. Writes data/processed/study2A_*.
The primary measure of wording sensitivity is the range of variant means, which exists
even when every decision is identical; eta-squared is reported when it is defined.
"""
import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests

from . import analyze as A
from .analyze import ALPHA, DILEMMA, boot_cells, ci, fe_slope, layout, md, pct, two_way_eta
from .prompts import FRAMING_SET, PARAPHRASE_SET
from .summarize import final_rows

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def decisions(pattern):
    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        with open(path) as f:
            rows += [json.loads(line) for line in f if line.strip()]
    d = pd.DataFrame([r for r in final_rows(rows) if r["kind"] == "decision"])
    if d.empty:
        return d, len(rows)
    d = d[d.valid.astype(bool)].copy()
    d["s"] = d.contribution / d.endowment
    d["full"] = (d.contribution == d.endowment).astype(int)
    return d, len(rows)


def variant_means_boot(d, variants, n_boot, rng):
    """Bootstrap of the mean share per variant inside the dilemma (cells = MPCR x variant)."""
    lay = layout(d, variants, DILEMMA)
    if lay is None:
        return None
    groups, ns, a_idx, b_idx, _ = lay
    means, wss = boot_cells(groups, n_boot, rng)
    obs = np.array([g.mean() for g in groups])
    obs_wss = np.array([((g - g.mean()) ** 2).sum() for g in groups])

    def by_variant(m):
        return np.stack([(m[..., b_idx == j] * ns[b_idx == j]).sum(-1) / ns[b_idx == j].sum() for j in range(len(variants))], -1)

    return dict(obs=by_variant(obs), boot=by_variant(means), eta=two_way_eta(obs, obs_wss, ns, a_idx, b_idx),
                eta_boot=two_way_eta(means, wss, ns, a_idx, b_idx), groups=groups, ns=ns, a_idx=a_idx, b_idx=b_idx)


def rng_range(x):
    return x.max(axis=-1) - x.min(axis=-1)


def sensitivity(d, n_boot, rng):
    """Range of variant means (pp) in the paraphrase and framing sets, with bootstrap draws."""
    out = {}
    for name, variants in (("paraphrase", PARAPHRASE_SET), ("framing", FRAMING_SET)):
        vm = variant_means_boot(d, variants, n_boot, rng)
        if vm is None:
            return None
        out[name] = dict(range=pct(rng_range(vm["obs"])), boot=pct(rng_range(vm["boot"])), means=pct(vm["obs"]),
                         eta_m=vm["eta"]["A"], eta_w=vm["eta"]["B"], eta_boot=vm["eta_boot"])
    return out


def analyse(on, off, on_old, tag, n_boot, seed, title="Study 2, part A"):
    rng = np.random.default_rng(seed)
    out = os.path.join(ROOT, "data", "processed")
    rep = [f"# {title}: {tag}\n"]
    P = rep.append
    models = sorted(on.model.unique())
    P(f"Reasoning-on decisions: {len(on)} | models: {', '.join(models)} | bootstrap: {n_boot} | seed: {seed}\n")

    P("## Mean contribution (%) by variant, reasoning on, dilemma range\n")
    t = on[on.mpcr.isin(DILEMMA)].groupby(["model", "variant"]).s.mean().mul(100).unstack().round(1)
    P(md(t[[v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if v in t]]) + "\n")
    for m, title in ((A.CTRL_HIGH, f"control m = {A.CTRL_HIGH:g} (dominant action 100)"), (A.CTRL_LOW, f"control m = {A.CTRL_LOW:g} (dominant action 0)")):
        t = on[on.mpcr == m].groupby(["model", "variant"]).s.mean().mul(100).unstack().round(1)
        P(f"## Mean contribution (%) by variant, reasoning on, {title}\n")
        P(md(t[[v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if v in t]]) + "\n")

    # ---- A1: wording sensitivity with reasoning on, and against reasoning off -----------------
    rows = []
    for model in models:
        s_on = sensitivity(on[on.model == model], n_boot, rng)
        s_off = sensitivity(off[off.model == model], n_boot, rng) if len(off) else None
        if s_on is None:
            rows.append(dict(model=model, note="incomplete layout")); continue
        row = dict(model=model)
        for name in ("paraphrase", "framing"):
            lo, hi = ci(s_on[name]["boot"])
            row.update({f"{name}_range_on": s_on[name]["range"], f"{name}_on_lo": lo, f"{name}_on_hi": hi,
                        f"eta_wording_{name}_on": s_on[name]["eta_w"], f"eta_mpcr_{name}_on": s_on[name]["eta_m"]})
            if s_off is not None:
                d_b = s_on[name]["boot"] - s_off[name]["boot"]
                lo_d, hi_d = ci(d_b)
                lo_f, hi_f = ci(d_b, 100 * (1 - ALPHA / len(models)))   # Bonferroni across models
                row.update({f"{name}_range_off": s_off[name]["range"], f"{name}_diff_on_minus_off": s_on[name]["range"] - s_off[name]["range"],
                            f"{name}_diff_lo": lo_d, f"{name}_diff_hi": hi_d, f"{name}_diff_lo_fw": lo_f, f"{name}_diff_hi_fw": hi_f,
                            f"{name}_reduced": bool(hi_f < 0)})
        e = s_on["paraphrase"]
        defined = np.isfinite(e["eta_w"]) and e["eta_w"] >= 0.001
        row["snr_on"] = e["eta_m"] / e["eta_w"] if defined else np.nan
        row["snr_on_reported"] = (f"{row['snr_on']:.2f}" if defined else
                                  ("undefined (no variation)" if not np.isfinite(e["eta_w"]) else ">100"))
        rows.append(row)
    a1 = pd.DataFrame(rows)
    a1.to_csv(os.path.join(out, f"{tag}_A1_wording_sensitivity.csv"), index=False)
    P("## A1: range of variant means (percentage points) inside the dilemma, reasoning on versus off\n")
    P(md(a1.round(3), index=False) + "\n")

    # ---- A2: incentive response and controls with reasoning on (paraphrase set) ------------------
    rows = []
    for model in models:
        d = on[(on.model == model) & on.mpcr.isin(DILEMMA) & on.variant.isin(PARAPHRASE_SET)]
        lay = layout(d, PARAPHRASE_SET, DILEMMA)
        row = dict(model=model)
        if lay is not None:
            groups, ns, a_idx, b_idx, m_vals = lay
            fit = smf.ols("s ~ mpcr + C(variant)", data=d).fit(cov_type="HC3")
            slope, se = fit.params["mpcr"], fit.bse["mpcr"]
            row.update(slope_pp=pct(slope), p_one_sided=(1 - stats.norm.cdf(slope / se)) if se > 0 else (0.0 if slope > 0 else 1.0))
            lo, hi = ci(fe_slope(boot_cells(groups, n_boot, rng)[0], ns, m_vals, b_idx))
            row.update(slope_lo=pct(lo), slope_hi=pct(hi), dilemma_mean_pct=pct(d.s.mean()))
        for m, thr, direction, name in ((A.CTRL_LOW, 0.10, "<=", "ctrl_low"), (A.CTRL_HIGH, 0.90, ">=", "ctrl_high")):
            y = on[(on.model == model) & (on.mpcr == m) & on.variant.isin(PARAPHRASE_SET)].s.to_numpy(float)
            if len(y) == 0:
                continue
            lo, hi = ci(y[rng.integers(0, len(y), size=(n_boot, len(y)))].mean(axis=1))
            verdict = ("pass" if hi <= thr else "fail" if lo > thr else "inconclusive") if direction == "<=" else \
                      ("pass" if lo >= thr else "fail" if hi < thr else "inconclusive")
            row.update({f"{name}_mean_pct": pct(y.mean()), f"{name}_lo": pct(lo), f"{name}_hi": pct(hi), f"{name}_verdict": verdict})
        rows.append(row)
    a2 = pd.DataFrame(rows)
    if "p_one_sided" in a2:
        mask = a2.p_one_sided.notna()
        a2.loc[mask, "p_holm"] = multipletests(a2.loc[mask, "p_one_sided"], method="holm")[1]
    a2.to_csv(os.path.join(out, f"{tag}_A2_incentives_controls.csv"), index=False)
    P("## A2: slope inside the dilemma and controls, reasoning on, paraphrase set\n")
    P(md(a2.round(3), index=False) + "\n")

    # ---- A3: named game against baseline with reasoning on -----------------------------------------
    rows = []
    for model in models:
        for region, ms in (("dilemma", DILEMMA), ("control_m>1", [A.CTRL_HIGH])):
            base = on[(on.model == model) & on.mpcr.isin(ms) & (on.variant == "P0")].s.to_numpy(float)
            y = on[(on.model == model) & on.mpcr.isin(ms) & (on.variant == "F3")].s.to_numpy(float)
            if len(y) < 2 or len(base) < 2:
                continue
            d_b = y[rng.integers(0, len(y), (n_boot, len(y)))].mean(1) - base[rng.integers(0, len(base), (n_boot, len(base)))].mean(1)
            lo, hi = ci(d_b)
            rows.append(dict(model=model, region=region, p0_pct=pct(base.mean()), f3_pct=pct(y.mean()),
                             diff_pp=pct(y.mean() - base.mean()), ci_lo=pct(lo), ci_hi=pct(hi)))
    a3 = pd.DataFrame(rows)
    a3.to_csv(os.path.join(out, f"{tag}_A3_named_game.csv"), index=False)
    P("## A3: named game F3 minus baseline P0, reasoning on\n")
    P(md(a3.round(1), index=False) + "\n")

    # ---- A4: stability of the baseline between the two run dates --------------------------------------
    if len(on_old):
        rows = []
        for model in models:
            for m in sorted(on.mpcr.unique()):
                a = on[(on.model == model) & (on.mpcr == m) & (on.variant == "P0")].s.to_numpy(float)
                b = on_old[(on_old.model == model) & (on_old.mpcr == m) & (on_old.variant == "P0")].s.to_numpy(float)
                if len(a) < 2 or len(b) < 2:
                    continue
                d_b = a[rng.integers(0, len(a), (n_boot, len(a)))].mean(1) - b[rng.integers(0, len(b), (n_boot, len(b)))].mean(1)
                lo, hi = ci(d_b)
                rows.append(dict(model=model, mpcr=str(m), study1_pct=pct(b.mean()), study2_pct=pct(a.mean()),
                                 diff_pp=pct(a.mean() - b.mean()), ci_lo=pct(lo), ci_hi=pct(hi), differs=bool(lo > 0 or hi < 0)))
        a4 = pd.DataFrame(rows)
        a4.to_csv(os.path.join(out, f"{tag}_A4_stability.csv"), index=False)
        P("## A4: baseline prompt with reasoning on, Study 2 run against Study 1 run\n")
        P(md(a4.round(1), index=False) + "\n")

    path = os.path.join(out, f"{tag}_analysis.md")
    open(path, "w").write("\n".join(rep))
    print("report:", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20270402)
    ap.add_argument("--selftest", action="store_true", help="run the code on Study 1 reasoning-off data only")
    ap.add_argument("--game", default="pgg", choices=sorted(A.DESIGNS),
                    help="pd: Study 3, prisoner's dilemma (reasoning on against reasoning off, same study)")
    a = ap.parse_args()
    if a.game == "pd":
        A.use_game("pd")
        off, _ = decisions("data/raw/study3_off_*.jsonl")
        on, _ = decisions("data/raw/study3_on_*.jsonl")
        if on.empty or off.empty:
            raise SystemExit("no Study 3 data yet")
        analyse(on, off, on.iloc[0:0], "study3A", a.boot, a.seed, title="Study 3, reasoning on against off")
        raise SystemExit(0)
    off, _ = decisions("data/raw/final_off_*.jsonl")
    if a.selftest:
        analyse(off, off.iloc[0:0], off.iloc[0:0], "selftest_study2A", a.boot, a.seed)
    else:
        on, n_rows = decisions("data/raw/study2_on_*.jsonl")
        if on.empty:
            raise SystemExit("no Study 2 reasoning-on data yet")
        on_old, _ = decisions("data/raw/final_on_*.jsonl")
        analyse(on, off, on_old, "study2A", a.boot, a.seed)
