# Preregistration, Study 2

**Project:** Incentives or wording? An audit of LLM decision rules in the linear public goods game
**Authors:** José Pinto-Muñoz and Sofía Herrera-Henríquez, Universidad Técnica Federico Santa María, Chile
**Version:** 1.0, written 17 November 2026
**Repository:** https://github.com/Pepebeats-flp/llm-public-goods-audit
**Status:** to be posted on OSF before any confirmatory call of Study 2 is made. The launcher refuses to start Study 2 until the file `paper_ssc2027/OSF_REGISTRATION.txt`, containing the registration URL, exists.

Study 2 has two parts. Part A completes the reasoning arm of Study 1 with all prompt variants. Part B adds a repeated game with interacting agents.

## 1. What is known before this registration

- Study 1 is complete and its results are known to us (`paper_ssc2027/raw_materials/experimental_log.md`). In particular: without reasoning, wording explained more variance than the incentive in five of six models; with reasoning and the baseline prompt only, four of five models contributed nothing inside the dilemma.
- No data of Study 2 exist, with one exception: a technical test of the repeated-game runner (`techtest_repeated`, one model without reasoning, baseline wording, 2 groups, 80 calls). It was used to check that the code runs and that recorded payoffs equal the engine's payoffs. The contributions in it were not examined. It is excluded from all analyses.
- The analysis scripts were tested on Study 1 data (part A) and on synthetic games played by fixed rules (part B).

## 2. Research questions

- **RQ-A.** Does switching reasoning on remove the sensitivity of contributions to payoff-equivalent rewording and to framing, or does it only move the level of contributions?
- **RQ-B.** When agents interact repeatedly, does the difference in contributions produced by wording in the first round persist, and do contributions respond to what the other agents did?

## 3. Part A: reasoning on, all prompt variants (one-shot)

**Design.** Same game as Study 1 (N = 4, E = 20, integer contribution, one independent call per decision). Five models with `reasoning_effort: high`: claude-haiku-5-5, qwen3.8-flash, glm-5.3-flash, deepseek-v4.1-flash, hy3. Six values of the marginal per capita return m (0.2, 0.3, 0.4, 0.5, 0.75, 1.25) × eight prompt variants (P0, P1, P2, P4, P3, F1, F2, F3) × 50 decisions = 12,000 decisions. The baseline P0 is run again so that all variants share the same run dates. Temperature 1.0. Prompt texts are those of Study 1, unchanged (`pgg/prompts.py`).

**Comparison data.** Reasoning-off decisions of Study 1 for the same five models (collected 17 November 2026).

**Measures.**
- *Paraphrase range:* range (maximum minus minimum) of the mean contribution share across the four paraphrases P0, P1, P2, P4, inside the dilemma (m = 0.3 to 0.75 pooled), in percentage points.
- *Framing range:* the same across P0, F1, F2, F3.
- Eta-squared for m and for wording in the two balanced layouts, and the signal-to-noise ratio, when the total variance is above zero. When no decision varies they are reported as undefined.

**Hypotheses and tests.** Per model. Intervals are percentile bootstrap intervals with 10,000 resamples of decisions within cells, resampling the reasoning-on and reasoning-off data independently.

- **A1 (confirmatory).** The paraphrase range is smaller with reasoning on than with reasoning off. Supported for a model if the upper bound of the Bonferroni-adjusted interval (level 1 − 0.05/5) of the difference on minus off is below zero.
- **A2 (confirmatory).** The framing range is smaller with reasoning on than with reasoning off. Same test.
- **A3 (descriptive).** Controls with reasoning on, paraphrase set, with the thresholds of Study 1: pass if the 95% interval of the mean lies below 10% at m = 0.2, respectively above 90% at m = 1.25.
- **A4 (descriptive).** Slope of contribution on m inside the dilemma with reasoning on (OLS with paraphrase fixed effects, as in Study 1).
- **A5 (exploratory).** Named game F3 against baseline P0 with reasoning on, inside the dilemma and at m = 1.25.
- **A6 (stability check).** Baseline P0 with reasoning on in this run against the same cells of Study 1, per value of m. A difference whose 95% interval excludes zero is reported as instability between run dates and qualifies the comparison in A1 and A2.

**Interpretation fixed in advance.** If A1 holds because contributions are zero under every paraphrase, we will report that reasoning removes paraphrase sensitivity by driving behaviour to the floor, and say so in those words. A1 and A2 compare data collected on different dates; A6 is the check on that.

## 4. Part B: repeated game

**Design.** Groups of N = 4 agents play T = 10 rounds with a known horizon. E = 20 per round, m = 0.4 (r = 1.6). In each round every LLM agent receives one fresh call with the rules and its own history: for each past round, its own contribution, the mean contribution of the other three, and its payoff. Agents do not see individual contributions of others and there is no communication. All agents of a group use the same model and wording. Temperature 1.0. Prompt texts are in `pgg/prompts.py` (`repeated_prompt`).

| Condition | Models | Wordings | Groups per cell | Calls |
|---|---|---|---|---|
| B-off: homogeneous, reasoning off | all six models of Study 1 | P0, F2 ("Teamwork"), F3 (named game) | 15 | 10,800 |
| B-on: homogeneous, reasoning on | deepseek-v4.1-flash, glm-5.3-flash | P0, F2, F3 | 10 | 2,400 |
| B-mix: three LLM agents and one rule-based agent that always contributes 0, reasoning off | all six | P0 | 15 | 2,700 |

The two models of B-on were chosen because they were the fastest with reasoning on in Study 1, which keeps the run feasible. The choice was not based on their behaviour.

**Unit of analysis.** The group. Intervals are percentile bootstrap intervals with 10,000 resamples of groups. Outcomes are means of the LLM agents' contribution share per group and round.

**Hypotheses and tests.**

- **D1 (confirmatory).** In B-off, the gap between the "Teamwork" wording and the named game is still present in the last round: mean contribution in round 10 under F2 minus under F3 is above zero. Supported for a model if the lower bound of the Bonferroni-adjusted interval (level 1 − 0.05/6) is above zero. The same gap in round 1 is reported next to it.
- **D2 (confirmatory, descriptive of direction).** In B-off under P0, contributions decline over rounds: the mean per-group slope of contribution on round is below zero (95% interval).
- **D3 (confirmatory, descriptive of direction).** In B-off, an agent's contribution responds positively to the mean contribution of the others in the previous round, controlling for its own previous contribution. Estimated per group by OLS and averaged over groups (95% interval). Groups without variation in the regressors are left out and counted.
- **D4 (exploratory).** In B-mix, LLM agents contribute less in rounds 2 to 10 than in homogeneous groups under P0.
- **Exploratory.** Everything in B-on (two models, 10 groups per cell); end-game effect (round 10 minus the mean of rounds 7 to 9); Gini coefficient of cumulative payoffs; contrasts F2 − P0 and P0 − F3.

**Sample size rationale.** 15 groups per cell is set by the time and quota available, not by a power analysis. With nearly binary contributions, as in Study 1, a between-wording gap of 40 percentage points or more would be detected with 15 groups per cell; smaller gaps may not be. Null results in D1 will therefore be reported as inconclusive unless the interval excludes gaps of 20 points.

## 5. Data handling

- Part A: as in Study 1. An output without a valid action is recorded as invalid and the cell is queried once more; if the second output is invalid the cell is missing.
- Part B: in a round, an invalid output is queried once more. After a second invalid output the group is discarded; its rows are kept with status "discarded" and it is not replayed. Discarded groups are counted per cell and excluded from the analysis.
- Transport failures (HTTP 429 or 5xx, timeouts) are retried up to three times. In part B a game that cannot continue for this reason is abandoned without being recorded and played again.
- No decision is removed as an outlier and no output is repaired.
- The runs may take several days because of provider quotas. Runs that stop for quota reasons are resumed without change. Run dates are reported. Sample sizes are fixed; there is no optional stopping.
- If a model becomes unavailable before its cells are complete, it is reported with the data collected, flagged as incomplete, and left out of the tests that need complete cells.

## 6. Materials fixed by this registration

`pgg/prompts.py`, `pgg/game.py`, `pgg/llm.py`, `pgg/run_oneshot.py`, `pgg/run_repeated.py`, `pgg/analyze_study2.py`, `pgg/analyze_repeated.py`, and the 19 files `configs/study2_*.json`. Their SHA-256 hashes are in `preregistration_study2_manifest.txt`, committed to the public repository together with this document.

## 7. Limitations known in advance

- Models are accessed through one intermediary provider; the served model is recorded as the provider reports it.
- The models are of the fast, low-cost tier. Frontier models are not included.
- One group size, one endowment, one value of m in part B, one temperature, English prompts.
- Part A compares reasoning on and off across run dates.
- Agents in part B have no memory other than the history placed in the prompt.
- No counterfactual or policy conclusion will be drawn from the behaviour of LLM agents.

## 8. Deviations

Any deviation from this plan will be listed in the paper with its reason.
