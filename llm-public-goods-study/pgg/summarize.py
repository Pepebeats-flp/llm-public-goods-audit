"""Descriptive summary of a one-shot run. Usage: python3 -m pgg.summarize data/raw/<run>.jsonl

Standard library only. Prints tables; inferential analysis (intervals, variance
decomposition) belongs to the analysis stage of the final run.
"""
import json
import statistics as st
import sys
from collections import defaultdict


def load(path):
    rows = [json.loads(line) for line in open(path)]
    return rows


def final_rows(rows):
    """One row per cell: the valid attempt if any, else the last attempt."""
    by_key = {}
    for r in rows:
        if r["key"] not in by_key or r["valid"] or not by_key[r["key"]]["valid"]:
            if not (by_key.get(r["key"], {}).get("valid") and not r["valid"]):
                by_key[r["key"]] = r
    return list(by_key.values())


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def slope(xs, ys):
    if len(set(xs)) < 2:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def fmt(x, w=6, d=1):
    return f"{x:{w}.{d}f}" if x == x else " " * (w - 1) + "-"


def main(path):
    rows = load(path)
    cells = final_rows(rows)
    dec = [r for r in cells if r["kind"] == "decision"]
    comp = [r for r in cells if r["kind"] == "comprehension"]
    labels = sorted({r["label"] for r in cells})
    mpcrs = sorted({r["mpcr"] for r in dec})
    variants = [v for v in ["P0", "P1", "P2", "P4", "P3", "F1", "F2", "F3"] if any(r["variant"] == v for r in dec)]
    E = dec[0]["endowment"] if dec else 20

    def share(r):
        return 100.0 * r["contribution"] / r["endowment"]

    print(f"file: {path}")
    print(f"rows: {len(rows)}  cells: {len(cells)}  decisions: {len(dec)}  comprehension probes: {len(comp)}")
    allowance = sum((((r.get('usage') or {}).get('opencode') or {}).get('allowance') or 0) for r in rows)
    print(f"allowance used (USD, as reported by provider): {allowance:.4f}")

    print("\n== Mean contribution, % of endowment, by MPCR (all prompt variants pooled) ==")
    print(f"{'model':28}" + "".join(f"{m:>7}" for m in mpcrs) + "   n/cell")
    for lab in labels:
        line, ns = f"{lab:28}", []
        for m in mpcrs:
            xs = [share(r) for r in dec if r["label"] == lab and r["mpcr"] == m and r["valid"]]
            ns.append(len(xs))
            line += fmt(mean(xs), 7)
        print(line + f"   {min(ns)}-{max(ns)}")

    print("\n== Same, baseline prompt P0 only ==")
    for lab in labels:
        line = f"{lab:28}"
        for m in mpcrs:
            xs = [share(r) for r in dec if r["label"] == lab and r["mpcr"] == m and r["variant"] == "P0" and r["valid"]]
            line += fmt(mean(xs), 7)
        print(line)

    print("\n== Incentive response (all variants pooled) ==")
    print(f"{'model':28} slope_in_dilemma(pp per unit m)  err_ctrl_r<1(pp)  err_ctrl_m>1(pp)  invalid%  latency_s")
    for lab in labels:
        d = [r for r in dec if r["label"] == lab]
        v = [r for r in d if r["valid"]]
        ins = [r for r in v if r["regime"] == "dilemma"]
        lo = [share(r) for r in v if r["regime"] == "control_inefficient"]
        hi = [100 - share(r) for r in v if r["regime"] == "control_dominant"]
        inv = 100.0 * sum(1 for r in d if not r["valid"]) / len(d) if d else float("nan")
        lat = st.median([r["latency_s"] for r in d if r.get("latency_s") is not None]) if d else float("nan")
        print(f"{lab:28} {fmt(slope([r['mpcr'] for r in ins], [share(r) for r in ins]), 12)}"
              f"{'':20}{fmt(mean(lo), 8)}{'':10}{fmt(mean(hi), 8)}{'':6}{fmt(inv, 6)}   {fmt(lat, 6, 2)}")

    print("\n== Mean contribution by prompt variant, dilemma range only ==")
    print(f"{'model':28}" + "".join(f"{v:>7}" for v in variants) + "   sd_paraphrase  sd_framing")
    for lab in labels:
        line, means = f"{lab:28}", {}
        for v in variants:
            xs = [share(r) for r in dec if r["label"] == lab and r["variant"] == v and r["regime"] == "dilemma" and r["valid"]]
            means[v] = mean(xs)
            line += fmt(means[v], 7)
        para = [means[v] for v in variants if v in ("P0", "P1", "P2", "P4") and means[v] == means[v]]
        fram = [means[v] for v in variants if v in ("P0", "F1", "F2", "F3") and means[v] == means[v]]
        sdp = st.pstdev(para) if len(para) > 1 else float("nan")
        sdf = st.pstdev(fram) if len(fram) > 1 else float("nan")
        print(line + f"   {fmt(sdp, 10)}   {fmt(sdf, 8)}")

    print("\n== Distribution of contributions (share of valid decisions at focal values) ==")
    print(f"{'model':28}   at 0   at E/2   at E   other")
    for lab in labels:
        v = [r["contribution"] for r in dec if r["label"] == lab and r["valid"]]
        if not v:
            continue
        c0, ch, ce = (sum(1 for x in v if x == k) for k in (0, E // 2, E))
        print(f"{lab:28} {fmt(100 * c0 / len(v), 6)} {fmt(100 * ch / len(v), 7)} {fmt(100 * ce / len(v), 7)} {fmt(100 * (len(v) - c0 - ch - ce) / len(v), 7)}")

    if comp:
        print("\n== Comprehension probes: % correct ==")
        items = sorted({r["item"] for r in comp})
        print(f"{'model':28}" + "".join(f"{i:>24}" for i in items) + "   n")
        for lab in labels:
            line = f"{lab:28}"
            for i in items:
                xs = [r for r in comp if r["label"] == lab and r["item"] == i]
                line += fmt(100.0 * sum(r["correct"] for r in xs) / len(xs) if xs else float("nan"), 24)
            print(line + f"   {len([r for r in comp if r['label'] == lab])}")

    fails = [r for r in rows if not r["ok"]]
    if fails:
        print(f"\n== Transport failures: {len(fails)} ==")
        by = defaultdict(int)
        for r in fails:
            by[(r["label"], r.get("http_status"))] += 1
        for k, n in sorted(by.items(), key=str):
            print("  ", k, n)


if __name__ == "__main__":
    main(sys.argv[1])
