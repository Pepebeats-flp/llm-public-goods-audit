"""Aggregates quoted in section 1 of experimental_log.md that pgg.analyze does not print.

  python3 -m pgg.extra_aggregates            # final data
"""
import glob
import json
import os
import sys

import pandas as pd

from .prompts import PARAPHRASE_SET
from .summarize import final_rows

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DILEMMA = [0.3, 0.4, 0.5, 0.75]
VOCAB = r"public good|prisoner|nash|free.rid|social dilemma"


def main(pattern="data/raw/final_*.jsonl"):
    rows = [json.loads(line) for f in sorted(glob.glob(os.path.join(ROOT, pattern))) for line in open(f)]
    raw = pd.DataFrame(rows)
    d = pd.DataFrame([r for r in final_rows(rows) if r["kind"] == "decision"])
    d["s"] = 100 * d.contribution / d.endowment
    off, on = d[d.effort == "none"], d[d.effort != "none"]

    print("== Baseline prompt P0, mean contribution (%), reasoning off / on ==")
    for m in sorted(d.model.unique()):
        def f(part, ms):
            x = part[(part.model == m) & (part.variant == "P0") & part.mpcr.isin(ms)].s
            return f"{x.mean():5.1f}" if len(x) else "  n/a"
        print(f"{m:22} dilemma {f(off, DILEMMA)} / {f(on, DILEMMA)} | m=1.25 {f(off, [1.25])} / {f(on, [1.25])} | m=0.2 {f(off, [0.2])} / {f(on, [0.2])}")

    in_d = off[off.mpcr.isin(DILEMMA)]
    g = in_d.groupby(["model", "variant"]).s.mean().unstack()
    print("\n== Reasoning off, dilemma: paraphrase-set mean; range across paraphrases; lowest and highest variant ==")
    para = in_d[in_d.variant.isin(PARAPHRASE_SET)].groupby("model").s.mean()
    for m in g.index:
        p = g.loc[m, PARAPHRASE_SET]
        print(f"{m:22} mean {para[m]:5.1f} | paraphrase range {p.max() - p.min():5.1f} | min {g.loc[m].min():5.1f} ({g.loc[m].idxmin()}) max {g.loc[m].max():5.1f} ({g.loc[m].idxmax()})")
    print("\n== Reasoning off, dilemma, pooled over models, by variant ==")
    print(in_d.groupby("variant").s.mean().round(1).to_dict())

    f3 = off[(off.variant == "F3") & (off.mpcr == 1.25)].groupby("model").s.mean()
    print("\n== F3 at m=1.25, reasoning off ==")
    print(f3.round(1).to_dict(), "| unweighted mean", round(f3.mean(), 1))

    h = off[off.model == "claude-haiku-5-5"]
    print("\n== claude-haiku-5-5, reasoning off: share of decisions stating the integer 0, by variant ==")
    print((h.assign(z=h.amount == 0).groupby("variant").z.mean() * 100).round(1).to_dict())
    print("take frame F1, mean contribution by MPCR:", h[h.variant == "F1"].groupby("mpcr").s.mean().round(1).to_dict())

    dec = raw[(raw.kind == "decision") & (raw.variant != "F3")].copy()
    text = (dec.text.fillna("") + " " + dec.reasoning_text.fillna("")).str.lower()
    dec["vocab"] = text.str.contains(VOCAB)
    print("\n== Game-theory vocabulary in answer plus reasoning trace, variants other than F3 (% of calls) ==")
    print((dec.groupby("label").vocab.mean() * 100).round(1).to_dict())

    tok = raw.usage.apply(lambda u: (u or {}).get("completion_tokens") if isinstance(u, dict) else None)
    print("\n== Median completion tokens per call ==")
    print(raw.assign(t=tok).groupby("label").t.median().to_dict())
    print("\nraw rows:", len(raw), "| cells:", raw.key.nunique(),
          "| failed calls:", int((~raw.ok.astype(bool)).sum()),
          "| invalid outputs:", int((raw.ok.astype(bool) & ~raw.valid.astype(bool)).sum()))


if __name__ == "__main__":
    main(*sys.argv[1:])
