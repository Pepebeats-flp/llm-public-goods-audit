# Analysis plan, Study 3: the prisoner's dilemma

**Project:** Incentives or wording? An audit of LLM decision rules in social dilemma games
**Authors:** José Pinto-Muñoz and Sofía Herrera-Henríquez, Universidad Técnica Federico Santa María, Chile
**Version:** 1.0, written 18 November 2026
**Repository:** https://github.com/Pepebeats-flp/llm-public-goods-audit
**Status:** committed and pushed to the public repository before any model call of Study 3. The launcher does not start Study 3 until the file `paper_ssc2027/STUDY3_GO.txt` exists, and that file is created only after this plan is public. The plan is not registered on a third-party registry. The public commit is the record.

Study 3 repeats the audit of Studies 1 and 2 in a second game, the two-player prisoner's dilemma, with the same six models and the same three blocks of evidence: one-shot decisions without reasoning, one-shot decisions with reasoning, and a repeated game.

## 1. What is known before this plan

- Studies 1 and 2 (linear public goods game) are complete and their results are known to us (`paper_ssc2027/raw_materials/experimental_log.md`). Without reasoning, wording explained more variance than the incentive in five of six models. With reasoning, most models contributed nothing inside the dilemma and two of them failed the control where contributing is dominant. In the repeated game the gap between wordings was still present in the last round for three models. One model changed its behaviour between two batches collected 22 minutes apart.
- No model has been called with any prisoner's dilemma prompt. The code was checked with unit tests (`tests/test_environment.py`, 27 tests) and with a dry run in which a fake offline client returned random outputs. The dry run confirmed that the 29 configurations produce the planned cells, that the label of the cooperative option is balanced in every cell, that recorded payoffs equal the engine's payoffs, and that the three analysis scripts run. Its output was deleted.
- Before the launch we will run a technical test with real calls: `configs/techtest_pd_oneshot.json` (12 calls) and `configs/techtest_pd_repeated.json` (20 calls), one model without reasoning. It checks output format and recorded payoffs. It is excluded from all analyses.

## 2. Research questions

- **RQ1.** Do the findings of Studies 1 and 2 hold in a second social dilemma with a different action space (binary) and a different presentation (a table of four outcomes)?
- **RQ2.** Are the differences between models stable across the two games?

## 3. Game

Two players choose at the same time between two options. With endowment E = 20 and marginal return m, the payoffs are R = 2mE when both cooperate, T = E + mE for defecting against a cooperator, P = E when both defect, and S = mE for cooperating against a defector. These are the payoffs of the linear public goods game of Study 1 with N = 2, r = 2m and the contribution restricted to 0 or E. The game is a prisoner's dilemma (T > R > P > S) when 0.5 < m < 1.

| Condition | m | R, T, P, S | Dominant action | Efficient profile |
|---|---|---|---|---|
| Control | 0.4 | 16, 28, 20, 8 | defect | both defect |
| Dilemma | 0.6 | 24, 32, 20, 12 | defect | both cooperate |
| Dilemma | 0.7 | 28, 34, 20, 14 | defect | both cooperate |
| Dilemma | 0.8 | 32, 36, 20, 16 | defect | both cooperate |
| Dilemma | 0.9 | 36, 38, 20, 18 | defect | both cooperate |
| Control | 1.25 | 50, 45, 20, 25 | cooperate | both cooperate |

The cooperation index of Rapoport and Chammah, K = (R − P)/(T − S), equals 2m − 1 in this family: 0.2, 0.4, 0.6 and 0.8 in the four dilemma conditions.

**Presentation.** The baseline describes the four outcomes with options labelled "A" and "B". The label that stands for cooperation alternates with the replicate, so that it is A in half of the decisions of every cell and B in the other half. The outcomes are always listed in the order AA, BB, AB, BA.

**Eight wordings, parallel to Study 1** (`pgg/pd.py`). P0 neutral baseline. P1, P2 and P4 paraphrases (P1 reorders the sentences and uses the unit "tokens", P2 lists the outcomes as pairs and uses "coins", P4 uses an itemised layout). P3 is the baseline plus the joint total of the two symmetric outcomes as worked examples. F1 take frame: both start with R and an option adds T − R to oneself and removes R − S from the other. F2 the baseline preceded by "This task is called the Teamwork task." F3 names the prisoner's dilemma and uses its vocabulary (players, cooperate, defect, payoff). The unit tests check that the text of every wording implies the engine's payoffs for the six values of m and under both label assignments. The paraphrase set is P0, P1, P2, P4 and the framing set is P0, F1, F2, F3, as in Study 1.

## 4. Design

Temperature 1.0. One independent call per decision. Same six models and same provider as Studies 1 and 2.

| Block | Levels | Calls |
|---|---|---|
| A-off: one-shot, reasoning off | 6 models × 6 values of m × 8 wordings × 50 | 14,400 |
| Comprehension, reasoning off | 6 models × 6 values of m × 2 questions × 20 | 1,440 |
| A-on: one-shot, reasoning `high` | 5 models (gpt-5.6-luna does not offer the setting) × 6 × 8 × 50 | 12,000 |
| B-off: repeated game, 10 rounds, known horizon, m = 0.7, reasoning off | 6 models × 3 wordings (P0, F2, F3) × 15 pairs × 20 calls | 5,400 |
| B-mix: one LLM agent against a rule-based agent that always defects, P0, reasoning off | 6 models × 15 pairs × 10 calls | 900 |

Total: 34,140 calls. There is no repeated game with reasoning on.

In the repeated game each agent receives in every round one fresh call with the rules and the history of the pair: for each past round its own choice, the choice of the other participant and its own points. Both agents of a pair use the same model and wording. The cooperative label alternates across pairs.

The outcome is the cooperation rate, coded as a contribution of E (cooperate) or 0 (defect) so that the measures of Studies 1 and 2 apply without change.

## 5. Hypotheses and tests

All tests are per model. Intervals are percentile bootstrap intervals with 10,000 resamples (decisions within cells in the one-shot blocks, pairs in the repeated game). The scripts are those of Studies 1 and 2 with the incentive values of this game (`--game pd`).

**One-shot, reasoning off (as Study 1).**

- **S3-H1a (confirmatory).** Cooperation increases with m inside the dilemma. OLS of the cooperation share on m with paraphrase fixed effects and HC3 errors, paraphrase set, m in 0.6 to 0.9. One-sided test, Holm correction across the six models.
- **S3-H1b (confirmatory).** Controls, paraphrase set. A model passes the control at m = 0.4 if the 95% interval of its cooperation rate lies at or below 10%, and the control at m = 1.25 if it lies at or above 90%.
- **S3-H2 (confirmatory).** Eta-squared of m and of wording in the two balanced layouts (m × paraphrase set, m × framing set) inside the dilemma. The signal-to-noise ratio is eta-squared of m divided by eta-squared of wording in the paraphrase layout. It is reported with its bootstrap interval, or as undefined when no decision varies.
- **S3-H6 (confirmatory).** Named game F3 against baseline P0, inside the dilemma and at m = 1.25. Welch test, Holm correction across models within each region. Direction expected from Study 1: naming the game lowers cooperation.
- **Descriptive.** Cooperation by wording and m, comprehension probes (share correct), and the effect of the label: cooperation when the cooperative option is A minus when it is B, and the share of decisions that choose A.

**One-shot, reasoning on against off (as Study 2, part A).**

- **S3-A1 (confirmatory).** The paraphrase range (maximum minus minimum of the mean cooperation rate across P0, P1, P2, P4 inside the dilemma) is smaller with reasoning on. Supported for a model if the upper bound of the Bonferroni-adjusted interval (level 1 − 0.05/5) of the difference on minus off is below zero.
- **S3-A2 (confirmatory).** The same for the framing range.
- **S3-A3 and S3-A4 (descriptive).** Controls and slope with reasoning on, with the thresholds above.
- **S3-A5 (exploratory).** F3 against P0 with reasoning on.

**Repeated game (as Study 2, part B).** Unit of analysis: the pair.

- **S3-D1 (confirmatory).** The gap between "Teamwork" and the named game is present in the last round: cooperation in round 10 under F2 minus under F3 is above zero. Supported for a model if the lower bound of the Bonferroni-adjusted interval (level 1 − 0.05/6) is above zero. The gap in round 1 is reported next to it.
- **S3-D2 (confirmatory, direction).** Under P0 cooperation declines over rounds: the mean per-pair slope on round is below zero (95% interval).
- **S3-D3 (confirmatory, direction).** An agent's choice responds positively to the other's choice in the previous round, controlling for its own previous choice. Estimated per pair and averaged. Pairs without variation in the regressors are left out and counted.
- **S3-D4 (exploratory).** Against the agent that always defects, cooperation in rounds 2 to 10 is lower than in pairs of two LLM agents under P0.
- **Exploratory.** End-game effect, contrasts F2 − P0 and P0 − F3.

**Comparison between the two games (descriptive, no test).** For the quantities that exist in both games (mean in the dilemma range, slope on m, both control verdicts, paraphrase range, framing range, signal-to-noise ratio, F3 − P0, reasoning-on paraphrase range, last-round gap F2 − F3) we will report the values side by side, the number of models with the same verdict or the same sign in both games, and the Spearman rank correlation across the six models. With six models the correlation is a description, not a test.

## 6. Interpretation fixed in advance

- The two games differ in the number of players, the action space (binary against 0 to 20) and the presentation, and their data come from different dates. Differences between games are therefore not attributed to any single one of these features.
- The prisoner's dilemma is the best known game in the literature the models were trained on. If cooperation under F3 differs from the neutral wordings, we will report it as an effect of naming the game, and the controls will be used to separate recitation of the textbook answer from application of the payoff rule.
- If a range shrinks with reasoning because cooperation is zero under every wording, we will say that reasoning removes the sensitivity by driving behaviour to the floor.
- A result of Studies 1 and 2 that does not appear in Study 3 will be reported as specific to the public goods game in our data, in the abstract and in the discussion.

## 7. Sample size

50 decisions per cell and 15 pairs per cell, the sizes of Studies 1 and 2, set by the time and quota available and not by a power analysis. With 15 pairs per cell a between-wording gap of 40 percentage points or more would be detected. Null results in S3-D1 will be reported as inconclusive unless the interval excludes gaps of 20 points.

## 8. Data handling

As in Studies 1 and 2.

- An output without a valid choice is recorded as invalid and the cell is asked once more. If the second output is invalid the cell is missing. In the repeated game a second invalid output discards the pair, which is kept with status "discarded", counted and not replayed.
- Transport failures are retried up to three times. A repeated game that cannot continue is abandoned without being recorded and played again. The client timeout is 600 seconds in the reasoning-on runs.
- No decision is removed as an outlier and no output is repaired.
- Cells are executed in a seeded random order. The reasoning-on runs of the two slowest models are split into four processes that take every fourth cell of that order.
- Runs that stop for quota reasons are resumed without change. Run dates are reported. Sample sizes are fixed and there is no optional stopping.
- If a model becomes unavailable before its cells are complete, it is reported with the data collected, flagged as incomplete, and left out of the tests that need complete cells.

## 9. Materials fixed by this plan

`pgg/pd.py`, `pgg/game.py`, `pgg/prompts.py`, `pgg/llm.py`, `pgg/run_oneshot.py`, `pgg/run_repeated.py`, `pgg/analyze.py`, `pgg/analyze_study2.py`, `pgg/analyze_repeated.py`, `tests/test_environment.py` and the 29 files `configs/study3_*.json`. Their SHA-256 hashes are in `preregistration_study3_manifest.txt`, committed together with this document.

## 10. Limitations known in advance

- One intermediary provider. The served model is recorded as the provider reports it.
- Fast, low-cost models. Frontier models are not included.
- One endowment, one family of payoff matrices, one temperature, English prompts, one value of m in the repeated game.
- Reasoning on and off are collected in the same days in this study, but the two games are not.
- Agents in the repeated game have no memory other than the history placed in the prompt.
- No counterfactual or policy conclusion will be drawn from the behaviour of LLM agents.

## 11. Deviations

Any deviation from this plan will be listed in the paper with its reason.
