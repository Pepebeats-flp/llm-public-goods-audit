# Incentives or Wording? Auditing LLM Decision Rules in a Public Goods Game

Code, data, preregistration and manuscript source for a study of six large language models used as decision rules in a one-shot linear public goods game.

Each model was asked 2,640 times (reasoning off) how much of an endowment of 20 it places in a shared account, under six values of the marginal per capita return and eight payoff-equivalent or reframed descriptions of the same game. Five models were asked again with reasoning switched on. In total: 17,940 preregistered decisions and comprehension probes, run on 17 November 2026.

## Main results

- Without reasoning, rewording the same game explains 3 to 21 times more variance in contributions than the incentive, in the five models where the ratio is defined.
- Two of six models respond to the incentive; no model chooses the dominant action in both control conditions.
- Naming the game lowers contributions, including where contributing everything maximises the agent's own payoff.
- With reasoning on, four of five models contribute nothing at every value inside the social dilemma.

## Layout

| Path | Content |
|---|---|
| `llm-public-goods-study/pgg/` | Game engine, prompt variants, API client, runner, supervisor, analysis and figures |
| `llm-public-goods-study/tests/` | Environment validation (14 tests) |
| `llm-public-goods-study/configs/` | One configuration per model and reasoning setting; snapshot of model metadata |
| `llm-public-goods-study/data/raw/` | One JSON line per API call: parsed action, returned text, reasoning trace, usage, timing |
| `llm-public-goods-study/data/processed/` | Tables and the analysis report |
| `llm-public-goods-study/docs/ODD.md` | Full model description (ODD protocol) |
| `paper_ssc2027/preregistration.md` | Analysis plan fixed before the confirmatory run, with file hashes in `preregistration_manifest.txt` |
| `paper_ssc2027/raw_materials/experimental_log.md` | Every number used in the manuscript |
| `paper_ssc2027/latex_writeup/` | Manuscript source (Springer LNCS) and figures |
| `paper_ssc2027/review/` | Internal review rounds |
| `guia_paper_ssc2027_llm_public_goods.md` | Working notes and literature review (in Spanish) |

## Reproducing the analysis

The raw responses are in the repository, so no API access is needed.

```bash
pip install -r requirements.txt
cd llm-public-goods-study
python3 -m unittest discover -s tests                                # environment validation
python3 -m pgg.analyze --glob 'data/raw/final_*.jsonl' --tag final   # tables and report (seeded bootstrap)
python3 -m pgg.extra_aggregates                                      # aggregates quoted in the log
python3 -m pgg.figures --tag final                                   # figures
```

Collecting new data requires an OpenAI-compatible endpoint and key; see `llm-public-goods-study/README.md` (in Spanish) and `pgg/llm.py`.

## Things to know before reusing the data

- The pilot run (`pilot_20261117`) was inspected before the analysis plan was fixed. It is kept for transparency and is excluded from every reported result.
- The preregistration was not posted to a public registry before the run; the hash manifest was generated before the first confirmatory call.
- Models were accessed through an intermediary provider (OpenCode Go). The served model identifier is recorded as reported by the provider.
- The reasoning arm used the baseline prompt only.

## Authors

José Pinto-Muñoz and Sofía Herrera-Henríquez, Universidad Técnica Federico Santa María, Chile.

## Use of AI tools

An AI coding assistant (Claude, Anthropic) was used to write the code, run the analysis, and draft and revise the text. The authors take full responsibility for the content.

## License

Code: MIT (see `LICENSE`). Data, documentation and manuscript text: CC BY 4.0. The files `llncs.cls` and `splncs04.bst` are distributed by Springer under their own terms.
