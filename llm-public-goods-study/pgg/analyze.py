"""Confirmatory analysis, following paper_ssc2027/preregistration.md section 5.

  python3 -m pgg.analyze --glob 'data/raw/final_*.jsonl' --tag final
  python3 -m pgg.analyze --glob 'data/raw/pilot_*.jsonl' --tag pilotdev --boot 500   # code test only

Writes CSV tables and a Markdown report to data/processed/<tag>_*.
Pilot files must never be passed together with final files.
"""
import argparse
import glob
import json
import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests

from .prompts import FRAMING_SET, PARAPHRASE_SET
from .summarize import final_rows

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DILEMMA = [0.3, 0.4, 0.5, 0.75]
CTRL_LOW, CTRL_HIGH = 0.2, 1.25
ALPHA = 0.05


def load(pattern):
    rows = []
    files = sorted(glob.glob(os.path.join(ROOT, pattern)))
    for path in files:
        with open(path) as f:
            rows += [json.loads(line) for line in f if line.strip()]
    cells = final_rows(rows)
    dec = pd.DataFrame([r for r in cells if r["kind"] == "decision"])
    comp = pd.DataFrame([r for r in cells if r["kind"] == "comprehension"])
    raw = pd.DataFrame(rows)
    return files, raw, dec, comp


def md(df, index=True):
    """Markdown table without external dependencies."""
    d = df.reset_index() if index else df
    def cell(v):
        if isinstance(v, float):
            return "" if v != v else f"{v:g}"
        return str(v)
    head = "| " + " | ".join(str(c) for c in d.columns) + " |"
    sep = "|" + "|".join("---" for _ in d.columns) + "|"
    body = ["| " + " | ".join(cell(v) for v in row) + " |" for row in d.itertuples(index=False, name=None)]
    return "\n".join([head, sep] + body)


def pct(x):
    return 100.0 * x


def boot_cells(groups, n_boot, rng):
    """groups: list of 1-D arrays (one per cell). Returns (means, within_ss), each (n_boot, n_cells)."""
    means = np.empty((n_boot, len(groups)))
    wss = np.empty((n_boot, len(groups)))
    for j, y in enumerate(groups):
        n = len(y)
        idx = rng.integers(0, n, size=(n_boot, n))
        yb = y[idx]
        means[:, j] = yb.mean(axis=1)
        wss[:, j] = (yb ** 2).sum(axis=1) - n * means[:, j] ** 2
    return means, wss


def two_way_eta(means, wss, ns, a_idx, b_idx):
    """Eta-squared of factor A, factor B, interaction and residual from cell statistics.

    means, wss: (..., n_cells); ns, a_idx, b_idx: (n_cells,). Exact for balanced layouts;
    with a few missing observations the interaction is the remainder of the between-cell SS.
    """
    ns = np.asarray(ns, float)
    N = ns.sum()
    grand = (means * ns).sum(axis=-1, keepdims=True) / N
    ss_cells = (ns * (means - grand) ** 2).sum(axis=-1)

    def marginal(idx):
        ss = 0.0
        for lev in np.unique(idx):
            mask = idx == lev
            n_l = ns[mask].sum()
            mean_l = (means[..., mask] * ns[mask]).sum(axis=-1) / n_l
            ss = ss + n_l * (mean_l - grand[..., 0]) ** 2
        return ss

    ss_a, ss_b = marginal(a_idx), marginal(b_idx)
    ss_res = wss.sum(axis=-1)
    ss_tot = ss_cells + ss_res
    with np.errstate(divide="ignore", invalid="ignore"):
        return {"A": ss_a / ss_tot, "B": ss_b / ss_tot, "AB": (ss_cells - ss_a - ss_b) / ss_tot, "res": ss_res / ss_tot}


def fe_slope(means, ns, m_vals, b_idx):
    """Slope of y on m with fixed effects for the wording, from cell means (weighted)."""
    ns = np.asarray(ns, float)
    m_c = np.asarray(m_vals, float).copy()
    y_c = means.copy()
    for lev in np.unique(b_idx):
        mask = b_idx == lev
        w = ns[mask] / ns[mask].sum()
        m_c[mask] = m_c[mask] - (m_c[mask] * w).sum()
        y_c[..., mask] = y_c[..., mask] - (y_c[..., mask] * w).sum(axis=-1, keepdims=True)
    return (ns * m_c * y_c).sum(axis=-1) / (ns * m_c ** 2).sum()


def ci(x, level=95):
    lo = (100 - level) / 2
    return np.nanpercentile(x, lo), np.nanpercentile(x, 100 - lo)


def layout(d, variants, mpcrs):
    """Cells of a two-way layout MPCR x variant, as arrays. Returns None if a cell is empty."""
    groups, ns, a_idx, b_idx, m_vals = [], [], [], [], []
    for i, m in enumerate(mpcrs):
        for j, v in enumerate(variants):
            y = d[(d.mpcr == m) & (d.variant == v)]["s"].to_numpy(float)
            if len(y) == 0:
                return None
            groups.append(y); ns.append(len(y)); a_idx.append(i); b_idx.append(j); m_vals.append(m)
    return groups, np.array(ns), np.array(a_idx), np.array(b_idx), np.array(m_vals)


def analyse(pattern, tag, n_boot, seed, paraphrases, framings):
    files, raw, dec, comp = load(pattern)
    if dec.empty:
        raise SystemExit("no decisions found for " + pattern)
    rng = np.random.default_rng(seed)
    out = os.path.join(ROOT, "data", "processed")
    os.makedirs(out, exist_ok=True)
    rep = []
    P = rep.append

    dec["valid"] = dec["valid"].astype(bool)
    ok = dec[dec.valid].copy()
    ok["s"] = ok["contribution"] / ok["endowment"]
    ok["full"] = (ok["contribution"] == ok["endowment"]).astype(int)
    off = ok[ok.effort == "none"]
    on = ok[ok.effort != "none"]
    models = sorted(off.model.unique())

    P(f"# Analysis report: {tag}\n")
    P(f"Files: {len(files)} | raw rows: {len(raw)} | decision cells: {len(dec)} (valid {len(ok)}) | comprehension probes: {len(comp)}")
    allowance = sum((((u or {}).get('opencode') or {}).get('allowance') or 0) for u in raw["usage"] if isinstance(u, dict))
    P(f"Provider allowance used: {allowance:.4f} USD | bootstrap resamples: {n_boot} | seed: {seed}")
    P(f"Paraphrase set: {paraphrases} | framing set: {framings}")
    P(f"Run window (UTC): {pd.to_datetime(raw.ts.min(), unit='s')} to {pd.to_datetime(raw.ts.max(), unit='s')}\n")

    # ---- data quality -------------------------------------------------------------------
    q = raw.groupby("label").agg(rows=("key", "size"), failed=("ok", lambda x: int((~x.astype(bool)).sum())),
                                 retried=("transport_retries", lambda x: int((x.fillna(0) > 0).sum())))
    q["invalid_first_attempt"] = raw[(raw.ok.astype(bool)) & (~raw.valid.astype(bool)) & (raw.attempt == 1)].groupby("label").size()
    q["missing_cells"] = dec[~dec.valid].groupby("label").size()
    q["temperature_default"] = raw[raw.temperature.isna()].groupby("label").size()
    q["served_models"] = raw.groupby("label")["served_model"].agg(lambda x: ",".join(sorted({str(v) for v in x.dropna()})))
    q = q.fillna(0)
    q.to_csv(os.path.join(out, f"{tag}_quality.csv"))
    P("## Data quality\n\n" + md(q) + "\n")

    # ---- descriptive: mean share by model and MPCR, paraphrase set ---------------------------
    rows = []
    for (label, m), g in ok[ok.variant.isin(paraphrases)].groupby(["label", "mpcr"]):
        y = g.s.to_numpy(float)
        b = y[rng.integers(0, len(y), size=(n_boot, len(y)))].mean(axis=1)
        lo, hi = ci(b)
        rows.append(dict(label=label, mpcr=m, n=len(y), mean_pct=pct(y.mean()), ci_lo=pct(lo), ci_hi=pct(hi),
                         at_zero_pct=pct((g.contribution == 0).mean()), at_full_pct=pct(g.full.mean())))
    curve = pd.DataFrame(rows)
    curve.to_csv(os.path.join(out, f"{tag}_curve_paraphrase_set.csv"), index=False)
    P("## Mean contribution (% of endowment) by MPCR, paraphrase set pooled\n")
    P(md(curve.pivot(index="label", columns="mpcr", values="mean_pct").round(1)) + "\n")

    rows = []
    for (label, v, m), g in ok.groupby(["label", "variant", "mpcr"]):
        rows.append(dict(label=label, variant=v, mpcr=m, n=len(g), mean_pct=pct(g.s.mean())))
    cellmeans = pd.DataFrame(rows)
    cellmeans.to_csv(os.path.join(out, f"{tag}_cell_means.csv"), index=False)

    # ---- H1a ---------------------------------------------------------------------------------
    rows = []
    for model in models:
        d = off[(off.model == model) & off.mpcr.isin(DILEMMA) & off.variant.isin(paraphrases)]
        lay = layout(d, paraphrases, DILEMMA)
        if lay is None:
            rows.append(dict(model=model, note="incomplete layout")); continue
        groups, ns, a_idx, b_idx, m_vals = lay
        fit = smf.ols("s ~ mpcr + C(variant)", data=d).fit(cov_type="HC3")
        slope, se = fit.params["mpcr"], fit.bse["mpcr"]
        p_one = 1 - stats.norm.cdf(slope / se) if se > 0 else (0.0 if slope > 0 else 1.0)
        means, _ = boot_cells(groups, n_boot, rng)
        lo, hi = ci(fe_slope(means, ns, m_vals, b_idx))
        rho, _ = stats.spearmanr(d.mpcr, d.s) if d.s.nunique() > 1 else (np.nan, np.nan)
        logit_b = np.nan
        if 0 < d.full.mean() < 1:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    logit_b = smf.logit("full ~ mpcr + C(variant)", data=d).fit(disp=0).params["mpcr"]
            except Exception:
                logit_b = np.nan
        rows.append(dict(model=model, n=len(d), slope_pp_per_unit=pct(slope), ci_lo=pct(lo), ci_hi=pct(hi),
                         p_one_sided=p_one, spearman_rho=rho, logit_coef_full=logit_b))
    h1a = pd.DataFrame(rows)
    if "p_one_sided" in h1a:
        mask = h1a.p_one_sided.notna()
        h1a.loc[mask, "p_holm"] = multipletests(h1a.loc[mask, "p_one_sided"], method="holm")[1]
        h1a["supported"] = h1a.p_holm < ALPHA
    h1a.to_csv(os.path.join(out, f"{tag}_H1a.csv"), index=False)
    P("## H1a: slope of contribution on MPCR inside the dilemma (paraphrase set, variant fixed effects)\n")
    P(md(h1a.round(4), index=False) + "\n")

    # ---- H1b ---------------------------------------------------------------------------------
    rows = []
    for model in models:
        for m, thr, direction in ((CTRL_LOW, 0.10, "<="), (CTRL_HIGH, 0.90, ">=")):
            y = off[(off.model == model) & (off.mpcr == m) & off.variant.isin(paraphrases)].s.to_numpy(float)
            if len(y) == 0:
                continue
            lo, hi = ci(y[rng.integers(0, len(y), size=(n_boot, len(y)))].mean(axis=1))
            if direction == "<=":
                verdict = "pass" if hi <= thr else ("fail" if lo > thr else "inconclusive")
            else:
                verdict = "pass" if lo >= thr else ("fail" if hi < thr else "inconclusive")
            rows.append(dict(model=model, mpcr=str(m), dominant_action_pct=0 if direction == "<=" else 100, n=len(y),
                             mean_pct=pct(y.mean()), ci_lo=pct(lo), ci_hi=pct(hi), threshold=f"{direction} {int(pct(thr))}", verdict=verdict))
    h1b = pd.DataFrame(rows)
    h1b.to_csv(os.path.join(out, f"{tag}_H1b.csv"), index=False)
    P("## H1b: out-of-dilemma controls (paraphrase set)\n")
    P(md(h1b.round(1), index=False) + "\n")

    # ---- H2 ----------------------------------------------------------------------------------
    union = list(dict.fromkeys(paraphrases + framings))
    rows = []
    for model in models:
        d = off[(off.model == model) & off.mpcr.isin(DILEMMA) & off.variant.isin(union)]
        lay = layout(d, union, DILEMMA)
        if lay is None:
            rows.append(dict(model=model, note="incomplete layout")); continue
        groups, ns, a_idx, b_idx, _ = lay
        obs_means = np.array([g.mean() for g in groups])
        obs_wss = np.array([((g - g.mean()) ** 2).sum() for g in groups])
        b_means, b_wss = boot_cells(groups, n_boot, rng)   # one resample per cell, shared by both layouts

        def sub(variants, means, wss):
            keep = np.isin(b_idx, [union.index(v) for v in variants])
            return two_way_eta(means[..., keep], wss[..., keep], ns[keep], a_idx[keep], b_idx[keep])

        ep, ef = sub(paraphrases, obs_means, obs_wss), sub(framings, obs_means, obs_wss)
        bp, bf = sub(paraphrases, b_means, b_wss), sub(framings, b_means, b_wss)
        dp = d[d.variant.isin(paraphrases)]
        try:
            aov = anova_lm(smf.ols("s ~ C(mpcr) * C(variant)", data=dp).fit(), typ=2)
            f_word, p_word = aov.loc["C(variant)", "F"], aov.loc["C(variant)", "PR(>F)"]
        except Exception:
            f_word, p_word = np.nan, np.nan
        diff = bf["B"] - bp["B"]
        with np.errstate(divide="ignore", invalid="ignore"):
            snr_b = np.where(bp["B"] > 0, bp["A"] / bp["B"], np.inf)
        snr = ep["A"] / ep["B"] if np.isfinite(ep["B"]) and ep["B"] >= 0.001 else np.nan
        lo_d, hi_d = ci(diff)
        rows.append(dict(
            model=model,
            eta_mpcr_para=ep["A"], eta_wording_para=ep["B"], eta_inter_para=ep["AB"], eta_resid_para=ep["res"],
            eta_mpcr_para_lo=ci(bp["A"])[0], eta_mpcr_para_hi=ci(bp["A"])[1],
            eta_wording_para_lo=ci(bp["B"])[0], eta_wording_para_hi=ci(bp["B"])[1],
            F_wording_para=f_word, p_wording_para=p_word,
            eta_mpcr_fram=ef["A"], eta_wording_fram=ef["B"], eta_inter_fram=ef["AB"], eta_resid_fram=ef["res"],
            eta_wording_fram_lo=ci(bf["B"])[0], eta_wording_fram_hi=ci(bf["B"])[1],
            diff_fram_minus_para=ef["B"] - ep["B"], diff_lo=lo_d, diff_hi=hi_d, framing_exceeds_paraphrase=bool(lo_d > 0),
            snr=snr, snr_lo=np.nanpercentile(snr_b, 2.5) if np.isfinite(snr_b).any() else np.nan,
            snr_hi=np.nanpercentile(snr_b, 97.5) if np.isfinite(snr_b).any() else np.nan,
            snr_reported=("undefined (no variation)" if not np.isfinite(ep["B"]) else
                          (">100" if ep["B"] < 0.001 else f"{snr:.2f}")),
        ))
    h2 = pd.DataFrame(rows)
    if "p_wording_para" in h2:
        mask = h2.p_wording_para.notna()
        h2.loc[mask, "p_wording_para_holm"] = multipletests(h2.loc[mask, "p_wording_para"], method="holm")[1]
    h2.to_csv(os.path.join(out, f"{tag}_H2.csv"), index=False)
    P("## H2: variance decomposition inside the dilemma (eta-squared)\n")
    show = ["model", "eta_mpcr_para", "eta_wording_para", "eta_inter_para", "eta_resid_para", "p_wording_para_holm",
            "eta_mpcr_fram", "eta_wording_fram", "diff_fram_minus_para", "diff_lo", "diff_hi", "snr_reported", "snr_lo", "snr_hi"]
    P(md(h2[[c for c in show if c in h2]].round(3), index=False) + "\n")

    # ---- H6 and other variant contrasts against P0 -------------------------------------------
    rows = []
    for model in models:
        for region, ms in (("dilemma", DILEMMA), ("control_m>1", [CTRL_HIGH]), ("control_r<1", [CTRL_LOW])):
            base = off[(off.model == model) & off.mpcr.isin(ms) & (off.variant == "P0")].s.to_numpy(float)
            for v in sorted(set(off.variant) - {"P0"}):
                y = off[(off.model == model) & off.mpcr.isin(ms) & (off.variant == v)].s.to_numpy(float)
                if len(y) < 2 or len(base) < 2:
                    continue
                d_b = y[rng.integers(0, len(y), (n_boot, len(y)))].mean(1) - base[rng.integers(0, len(base), (n_boot, len(base)))].mean(1)
                lo, hi = ci(d_b)
                p = stats.ttest_ind(y, base, equal_var=False).pvalue if (y.std() + base.std()) > 0 else (1.0 if y.mean() == base.mean() else 0.0)
                rows.append(dict(model=model, region=region, variant=v, p0_mean_pct=pct(base.mean()), mean_pct=pct(y.mean()),
                                 diff_pp=pct(y.mean() - base.mean()), ci_lo=pct(lo), ci_hi=pct(hi), p_welch=p))
    contrasts = pd.DataFrame(rows)
    if not contrasts.empty:
        h6 = contrasts[(contrasts.variant == "F3") & contrasts.region.isin(["dilemma", "control_m>1"])].copy()
        for region in h6.region.unique():
            mk = h6.region == region
            h6.loc[mk, "p_holm"] = multipletests(h6.loc[mk, "p_welch"], method="holm")[1]
        contrasts.to_csv(os.path.join(out, f"{tag}_variant_contrasts_vs_P0.csv"), index=False)
        h6.to_csv(os.path.join(out, f"{tag}_H6.csv"), index=False)
        P("## H6 (formed after the pilot): named game F3 against baseline P0\n")
        P(md(h6.round(4), index=False) + "\n")
        P("## Mean contribution (%) by variant, dilemma range\n")
        byv = off[off.mpcr.isin(DILEMMA)].groupby(["model", "variant"]).s.mean().mul(100).unstack().round(1)
        P(md(byv[[v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if v in byv]]) + "\n")
        P("## Mean contribution (%) by variant, control m > 1 (dominant action: 100)\n")
        byv = off[off.mpcr == CTRL_HIGH].groupby(["model", "variant"]).s.mean().mul(100).unstack().round(1)
        P(md(byv[[v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if v in byv]]) + "\n")
        P("## Mean contribution (%) by variant, control r < 1 (dominant action: 0)\n")
        byv = off[off.mpcr == CTRL_LOW].groupby(["model", "variant"]).s.mean().mul(100).unstack().round(1)
        P(md(byv[[v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if v in byv]]) + "\n")

    # ---- H5 (exploratory): reasoning on versus off at P0 ---------------------------------------
    rows = []
    for model in sorted(on.model.unique()):
        for m in sorted(on.mpcr.unique()):
            a = on[(on.model == model) & (on.mpcr == m) & (on.variant == "P0")].s.to_numpy(float)
            b = off[(off.model == model) & (off.mpcr == m) & (off.variant == "P0")].s.to_numpy(float)
            if len(a) < 2 or len(b) < 2:
                continue
            d_b = a[rng.integers(0, len(a), (n_boot, len(a)))].mean(1) - b[rng.integers(0, len(b), (n_boot, len(b)))].mean(1)
            lo, hi = ci(d_b)
            rows.append(dict(model=model, mpcr=str(m), off_pct=pct(b.mean()), on_pct=pct(a.mean()), diff_pp=pct(a.mean() - b.mean()),
                             ci_lo=pct(lo), ci_hi=pct(hi), n_on=len(a), n_off=len(b)))
    h5 = pd.DataFrame(rows)
    if not h5.empty:
        h5.to_csv(os.path.join(out, f"{tag}_H5_reasoning.csv"), index=False)
        P("## H5 (exploratory): reasoning on minus off, baseline prompt P0\n")
        P(md(h5.round(1), index=False) + "\n")

    # ---- distribution and comprehension --------------------------------------------------------
    E = int(ok.endowment.iloc[0])
    dist = ok.groupby("label").contribution.agg(
        at_zero=lambda x: pct((x == 0).mean()), at_half=lambda x: pct((x == E // 2).mean()),
        at_full=lambda x: pct((x == E).mean()), n="size")
    dist["other"] = 100 - dist.at_zero - dist.at_half - dist.at_full
    dist.to_csv(os.path.join(out, f"{tag}_distribution.csv"))
    P("## Distribution of contributions (% of valid decisions)\n\n" + md(dist.round(1)) + "\n")

    if not comp.empty:
        comp["correct"] = comp["correct"].astype(bool)
        c1 = comp.groupby(["label", "item"]).correct.mean().mul(100).unstack().round(1)
        c1["n_per_item"] = comp.groupby("label").size() // 2
        c1.to_csv(os.path.join(out, f"{tag}_comprehension.csv"))
        P("## Comprehension probes (% correct)\n\n" + md(c1) + "\n")
        c2 = comp.groupby(["label", "mpcr"]).correct.mean().mul(100).unstack().round(1)
        P("### By MPCR, both items pooled\n\n" + md(c2) + "\n")

    path = os.path.join(out, f"{tag}_analysis.md")
    with open(path, "w") as f:
        f.write("\n".join(rep))
    print("report:", path)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--boot", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20270401)
    ap.add_argument("--paraphrases", default=",".join(PARAPHRASE_SET))
    ap.add_argument("--framings", default=",".join(FRAMING_SET))
    a = ap.parse_args()
    analyse(a.glob, a.tag, a.boot, a.seed, a.paraphrases.split(","), a.framings.split(","))
