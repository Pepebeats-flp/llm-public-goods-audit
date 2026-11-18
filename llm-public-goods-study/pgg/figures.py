"""Figures for the paper, drawn from the tables written by pgg.analyze.

  python3 -m pgg.figures --tag final --out ../paper_ssc2027/latex_writeup/figures

Static print figures for Springer LNCS (text width about 12.2 cm). Each is written as PDF
(for LaTeX) and PNG (for checking). Identity is never carried by colour alone: Figure 1
uses small multiples with one series per panel, Figure 2 uses a different marker per series.
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"   # validated: scripts/validate_palette.js, light mode
WIDTH = 4.8  # inches, LNCS text width

plt.rcParams.update({
    "font.size": 7, "font.family": "DejaVu Sans", "axes.edgecolor": AXIS, "axes.linewidth": 0.6,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "savefig.dpi": 300,
})


def save(fig, out, name):
    os.makedirs(out, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"{name}.{ext}"), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("written:", os.path.join(out, name + ".pdf"))


def short(label):
    return label.split("@")[0]


def fig_incentive(tag, out, n=4):
    """Small multiples: mean contribution against MPCR, one panel per model."""
    d = pd.read_csv(os.path.join(ROOT, "data", "processed", f"{tag}_curve_paraphrase_set.csv"))
    on = d[~d.label.str.endswith("@none")]          # reasoning on: baseline prompt only
    d = d[d.label.str.endswith("@none")]
    labels = sorted(d.label.unique())
    ncol = 3
    nrow = -(-len(labels) // ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(WIDTH, 1.55 * nrow), sharex=True, sharey=True, squeeze=False)
    lo_edge, hi_edge = 1.0 / n, 1.0
    for ax, lab in zip(axes.flat, labels):
        g = d[d.label == lab].sort_values("mpcr")
        # out-of-dilemma regions and the payoff-maximising action
        ax.axvspan(0.1, lo_edge, color="#f0efec", lw=0)
        ax.axvspan(hi_edge, 1.35, color="#f0efec", lw=0)
        ax.plot([0.1, hi_edge, hi_edge, 1.35], [0, 0, 100, 100], color=MUTED, lw=0.9, ls=(0, (3, 2)), zorder=2)
        ax.fill_between(g.mpcr, g.ci_lo, g.ci_hi, color=BLUE, alpha=0.18, lw=0, zorder=3)
        ax.plot(g.mpcr, g.mean_pct, color=BLUE, lw=1.4, marker="o", ms=3.2, mec="white", mew=0.5, zorder=4,
                label="reasoning off, four paraphrases")
        h = on[on.label.map(short) == short(lab)].sort_values("mpcr")
        if len(h):
            ax.plot(h.mpcr, h.mean_pct, color=ORANGE, lw=1.0, ls=(0, (1, 1)), marker="s", ms=3.0, mec="white", mew=0.5,
                    zorder=5, label="reasoning on, baseline prompt")
        ax.set_title(short(lab), fontsize=7, color=INK, pad=3, loc="left")
        ax.set_xlim(0.1, 1.35)
        ax.set_ylim(-4, 104)
        ax.set_yticks([0, 50, 100])
        ax.set_xticks([0.2, 0.5, 0.75, 1.25])
        ax.set_xticklabels(["0.2", "0.5", "0.75", "1.25"])
        ax.grid(axis="y", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
    for ax in axes.flat[len(labels):]:
        ax.set_visible(False)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=BLUE, lw=1.4, marker="o", ms=3.2, mec="white", mew=0.5),
               Line2D([], [], color=ORANGE, lw=1.0, ls=(0, (1, 1)), marker="s", ms=3.0, mec="white", mew=0.5),
               Line2D([], [], color=MUTED, lw=0.9, ls=(0, (3, 2)))]
    fig.legend(handles, ["reasoning off, four paraphrases", "reasoning on, baseline prompt", "payoff-maximising action"],
               loc="upper center", ncol=3, frameon=False, fontsize=6.2, handlelength=2.4, columnspacing=1.2,
               bbox_to_anchor=(0.53, 1.0))
    fig.supxlabel("marginal per capita return $m$", fontsize=7, color=INK2, y=0.045)
    fig.supylabel("contribution (% of endowment)", fontsize=7, color=INK2, x=0.02)
    fig.tight_layout(w_pad=0.8, h_pad=0.9, rect=(0.02, 0.02, 1, 0.95))
    save(fig, out, "fig_incentive_response_curves")


def fig_variance(tag, out):
    """Dot plot: share of variance explained by the incentive, by paraphrase and by framing."""
    d = pd.read_csv(os.path.join(ROOT, "data", "processed", f"{tag}_H2.csv"))
    d = d.sort_values("eta_mpcr_para", na_position="first").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(WIDTH, 0.34 * len(d) + 0.95))
    series = [
        ("eta_mpcr_para", "eta_mpcr_para_lo", "eta_mpcr_para_hi", "incentive ($m$)", BLUE, "o", +0.22),
        ("eta_wording_para", "eta_wording_para_lo", "eta_wording_para_hi", "paraphrase", ORANGE, "s", 0.0),
        ("eta_wording_fram", "eta_wording_fram_lo", "eta_wording_fram_hi", "framing", AQUA, "^", -0.22),
    ]
    for col, lo, hi, name, color, marker, dy in series:
        y = d.index + dy
        ax.hlines(y, d[lo], d[hi], color=color, lw=1.0, alpha=0.6, zorder=3)
        ax.plot(d[col], y, ls="", marker=marker, ms=4.5, color=color, mec="white", mew=0.6, label=name, zorder=4)
    ax.set_yticks(d.index)
    ax.set_yticklabels(d.model)
    ax.set_ylim(-0.6, len(d) - 0.4)
    ax.set_xlim(-0.02, 1.0)
    ax.set_xlabel("share of contribution variance ($\\eta^2$), dilemma range")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for i, row in d.iterrows():
        if pd.isna(row.eta_wording_para):
            ax.text(0.01, i + 0.1, "no variation across the paraphrase set", fontsize=6, color=MUTED, va="center")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False, fontsize=6.5,
              handletextpad=0.2, columnspacing=1.2, borderaxespad=0.1)
    fig.tight_layout()
    save(fig, out, "fig_variance_decomposition")


def fig_variants(tag, out):
    """Dot plot: mean contribution by prompt variant inside the dilemma, one row per model."""
    d = pd.read_csv(os.path.join(ROOT, "data", "processed", f"{tag}_cell_means.csv"))
    d = d[d.label.str.endswith("@none") & d.mpcr.between(0.26, 0.99)]
    g = d.groupby(["label", "variant"]).mean_pct.mean().unstack()
    kinds = [("P0", "baseline", INK, "o"), ("P1", "paraphrase", ORANGE, "s"), ("P2", "paraphrase", ORANGE, "s"),
             ("P4", "paraphrase", ORANGE, "s"), ("P3", "worked examples", MUTED, "D"), ("F1", "take frame", AQUA, "v"),
             ("F2", "\"Teamwork\"", AQUA, "^"), ("F3", "named game", AQUA, "X")]
    g = g.loc[g.mean(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(WIDTH, 0.34 * len(g) + 0.95))
    seen = set()
    for i, lab in enumerate(g.index):
        ax.hlines(i, g.loc[lab].min(), g.loc[lab].max(), color=GRID, lw=1.2, zorder=2)
        for v, name, color, marker in kinds:
            if v not in g.columns:
                continue
            ax.plot(g.loc[lab, v], i, ls="", marker=marker, ms=4.8, color=color, mec="white", mew=0.6,
                    label=None if name in seen else name, zorder=6 if v == "P0" else 4)
            seen.add(name)
    ax.set_yticks(range(len(g)))
    ax.set_yticklabels([short(x) for x in g.index])
    ax.set_ylim(-0.6, len(g) - 0.4)
    ax.set_xlim(-3, 103)
    ax.set_xlabel("mean contribution (% of endowment), dilemma range")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=6, frameon=False,
              fontsize=6, handletextpad=0.1, columnspacing=0.8, borderaxespad=0.1)
    fig.tight_layout()
    save(fig, out, "fig_prompt_variants")


def fig_trajectories(out, tag="study2B"):
    """Small multiples: mean contribution by round in the repeated game, one line per wording."""
    d = pd.read_csv(os.path.join(ROOT, "data", "processed", f"{tag}_trajectories.csv"))
    d = d[d.label.str.endswith("@none") & (d.composition == "homogeneous")]
    labels = sorted(d.label.unique())
    series = [("P0", "baseline", BLUE, "o", "-"), ("F2", "\"Teamwork\"", AQUA, "^", (0, (4, 1.5))), ("F3", "named game", ORANGE, "s", (0, (1, 1)))]
    ncol = 3
    nrow = -(-len(labels) // ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(WIDTH, 1.5 * nrow), sharex=True, sharey=True, squeeze=False)
    for ax, lab in zip(axes.flat, labels):
        for v, name, color, marker, ls in series:
            g = d[(d.label == lab) & (d.variant == v)].sort_values("round")
            if g.empty:
                continue
            ax.fill_between(g["round"], g.ci_lo, g.ci_hi, color=color, alpha=0.13, lw=0, zorder=2)
            ax.plot(g["round"], g["mean"], color=color, lw=1.2, ls=ls, marker=marker, ms=2.6, mec="white", mew=0.4, zorder=4)
        ax.set_title(short(lab), fontsize=7, color=INK, pad=3, loc="left")
        ax.set_ylim(-4, 104)
        ax.set_yticks([0, 50, 100])
        ax.set_xticks([1, 4, 7, 10])
        ax.grid(axis="y", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
    for ax in axes.flat[len(labels):]:
        ax.set_visible(False)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=c, lw=1.2, ls=ls, marker=m, ms=2.8, mec="white", mew=0.4) for _, _, c, m, ls in series]
    fig.legend(handles, [n for _, n, _, _, _ in series], loc="upper center", ncol=3, frameon=False, fontsize=6.2,
               handlelength=2.6, columnspacing=1.4, bbox_to_anchor=(0.53, 1.0))
    fig.supxlabel("round", fontsize=7, color=INK2, y=0.045)
    fig.supylabel("contribution (% of endowment)", fontsize=7, color=INK2, x=0.02)
    fig.tight_layout(w_pad=0.8, h_pad=0.9, rect=(0.02, 0.02, 1, 0.95))
    save(fig, out, "fig_repeated_trajectories")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", default=os.path.join(ROOT, "..", "paper_ssc2027", "latex_writeup", "figures"))
    a = ap.parse_args()
    fig_incentive(a.tag, a.out)
    fig_variance(a.tag, a.out)
    fig_variants(a.tag, a.out)
    if os.path.exists(os.path.join(ROOT, "data", "processed", "study2B_trajectories.csv")):
        fig_trajectories(a.out)
