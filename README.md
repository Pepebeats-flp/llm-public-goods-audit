# Incentives or Wording? Auditing LLM Decision Rules in a Public Goods Game

Code, data, preregistration and manuscript source for a study of six large language models used as decision rules in a one-shot linear public goods game.

Two studies, run on 17 and 18 November 2026.

- **Study 1.** One-shot decisions: six models, six values of the marginal per capita return, eight payoff-equivalent or reframed descriptions of the same game, 50 decisions per cell without reasoning, plus a reasoning arm on the baseline prompt and comprehension probes. 17,940 cells.
- **Study 2.** Part A repeats the one-shot design with reasoning on for five models and all eight descriptions (12,000 decisions). Part B is a ten-round game in groups of four agents with feedback (410 games, 15,503 calls).

## Main results

- Without reasoning, rewording the same game explains 3 to 21 times more variance in contributions than the incentive, in the five models where the ratio is defined. Two of six models respond to the incentive and none chooses the dominant action in both controls.
- With reasoning on, three of five models contribute nothing under every wording inside the dilemma. Where contributing is dominant, two models still range over 70 and 82 percentage points across wordings.
- In the repeated game, the gap between a "Teamwork" label and the named game is still present in round 10 in three of six models and vanishes in the other three.
- One model answered an identical prompt with the full endowment in 91% of decisions in one batch and in 10% in a batch that began 22 minutes later.

## Layout

| Path | Content |
|---|---|
| `llm-public-goods-study/pgg/` | Game engine, prompt variants, API client, runner, supervisor, analysis and figures |
| `llm-public-goods-study/tests/` | Environment validation (19 tests) |
| `llm-public-goods-study/configs/` | One configuration per model and reasoning setting; snapshot of model metadata |
| `llm-public-goods-study/data/raw/` | One JSON line per API call: parsed action, returned text, reasoning trace, usage, timing |
| `llm-public-goods-study/data/processed/` | Tables and the analysis report |
| `llm-public-goods-study/docs/ODD.md` | Full model description (ODD protocol) |
| `paper_ssc2027/preregistration.md`, `preregistration_study2.md` | Analysis plans of the two studies, with file hashes in the manifests |
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
python3 -m pgg.analyze_study2                                        # Study 2, part A
python3 -m pgg.analyze_repeated                                      # Study 2, part B
python3 -m pgg.extra_aggregates_study2
python3 -m pgg.figures --tag final                                   # figures
```

Collecting new data requires an OpenAI-compatible endpoint and key; see `llm-public-goods-study/README.md` (in Spanish) and `pgg/llm.py`.

## Things to know before reusing the data

- The pilot run (`pilot_20261117`) was inspected before the analysis plan was fixed. It is kept for transparency and is excluded from every reported result.
- The preregistration was not posted to a public registry before the run; the hash manifest was generated before the first confirmatory call.
- Models were accessed through an intermediary provider (OpenCode Go). The served model identifier is recorded as reported by the provider.
- The plan of Study 2 (`paper_ssc2027/preregistration_study2.md`) was pushed to this repository before its run (commit 28b8b11) but was not registered on OSF. Deviations are listed in `paper_ssc2027/deviations_study2.md`.
- One cell of Study 2 is missing: deepseek-v4.1-flash with reasoning in the repeated game under the "Teamwork" wording.
- `techtest_repeated` is a technical test of the repeated-game runner and is excluded from every result.

## Authors

José Pinto-Muñoz and Sofía Herrera-Henríquez, Universidad Técnica Federico Santa María, Chile.

## Use of AI tools

An AI coding assistant (Claude, Anthropic) was used to write the code, run the analysis, and draft and revise the text. The authors take full responsibility for the content.

## License

Code: MIT (see `LICENSE`). Data, documentation and manuscript text: CC BY 4.0. The files `llncs.cls` and `splncs04.bst` are distributed by Springer under their own terms.
