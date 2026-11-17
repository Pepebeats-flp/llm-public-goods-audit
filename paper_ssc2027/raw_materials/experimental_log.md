# experimental_log.md

**STATUS: CONFIRMATORY RUN COMPLETE.** All numbers below come from `llm-public-goods-study/data/raw/final_*.jsonl`, analysed with `python3 -m pgg.analyze --glob 'data/raw/final_*.jsonl' --tag final` (10,000 bootstrap resamples, seed 20270401). The pilot (`pilot_20261117`) is not included anywhere in this file. Sections 2 onward are the analysis report copied verbatim; tables as CSV are in `llm-public-goods-study/data/processed/final_*.csv`.

Scope: one-shot linear public goods game only (experiments E0, E1, E2 and the reasoning arm). Mixed populations, the repeated game and the strategy method were not run.

## 0. Run registry

| Field | Value |
|---|---|
| Date of run | 17 November 2026, 18:37 to 21:00 UTC |
| Access | OpenCode Go inference API, OpenAI-compatible chat completions |
| Planned cells | 17,940 (14,400 decisions reasoning off; 1,500 decisions reasoning on; 2,040 comprehension probes) |
| Completed cells | 17,940 (100%) |
| API calls logged | 17,945 (4 repeat queries after an invalid output, 1 call that failed after transport retries and was completed on restart) |
| Missing cells | 0 |
| Provider allowance used | 1.85 USD |
| Temperature | 1.0 for every call (no model rejected the parameter) |
| Game | N = 4, E = 20, integer contribution; MPCR 0.2, 0.3, 0.4, 0.5, 0.75, 1.25 |
| Decisions per cell | 50 |
| Preregistration | `paper_ssc2027/preregistration.md`, hashes in `preregistration_manifest.txt` generated 17 November 2026 before the first confirmatory call; not posted to a public registry before the run |

### Models

| Label in paper | Canonical identifier (provider snapshot) | Open weights | Released | Reasoning off | Reasoning on |
|---|---|---|---|---|---|
| gpt-5.6-luna | openai/gpt-5.6-luna | no | 2026-07-09 | yes | not available through this API |
| claude-haiku-5-5 | anthropic/claude-haiku-5-5 | no | 2026-10-07 | yes | yes |
| qwen3.8-flash | alibaba/qwen3.8-flash | no | 2026-08-26 | yes | yes |
| glm-5.3-flash | zhipuai/glm-5.3-flash | yes | 2026-08-26 | yes | yes |
| deepseek-v4.1-flash | deepseek/deepseek-v4.1-flash-1017 | yes | 2026-10-17 | yes | yes |
| hy3 | tencent/hy3 | yes | 2026-07-06 | yes | yes |

Reasoning off is `reasoning_effort: none`; reasoning on is `reasoning_effort: high`. With reasoning off no call returned reasoning text; with reasoning on 99.8% did. Median completion tokens per call: off 7 to 10; on 48 (glm-5.3-flash), 170 (deepseek-v4.1-flash), 238 (claude-haiku-5-5, qwen3.8-flash), 722 (hy3).

### E0 environment validation

14 unit tests pass (`python3 -m unittest discover -s tests`): reference payoffs, welfare identity, regimes and dominant actions by enumeration, regret identity, input validation, efficiency and Gini, payoff equivalence of all 8 prompt variants across the 6 MPCR values, parameters present in every prompt text, absence of loaded vocabulary in the neutral variants, comprehension answer keys, output parsing, rule-agent trajectories and seed reproducibility.

### Deviations from the preregistration

1. The preregistration was not posted to a public registry before the run; only local SHA-256 hashes exist.
2. For claude-haiku-5-5 without reasoning, every one of the 800 decisions in the paraphrase layout is zero, so eta-squared and the signal-to-noise ratio are undefined. The preregistration only specified the case of a denominator below 0.001. It is reported as "undefined (no variation)".
3. No other deviation. Runs were executed in parallel, one process per model and reasoning setting, as stated in the preregistration.

## 0b. Human reference values (checked 17 November 2026)

| Source | Version read | Value | Slope in pp per unit of MPCR |
|---|---|---|---|
| Isaac and Walker (1988), QJE 103(1), p. 190 | Published article (scan) | Period-10 contributions of 3.65% at MPCR 0.3 and 26.35% at MPCR 0.75, experienced subjects | (26.35 - 3.65) / 0.45 = 50.4 |
| Gächter and Marino Fages (2023), IZA DP 16605, Table 3, column 2 | Discussion paper (the published JEBO 2026 version could not be retrieved) | One-shot game, endowment 10, n = 936; coefficient of high MPCR (0.8 versus 0.4) on contributions 0.987 (robust SE 0.293), constant 4.026 | 9.87 / 0.4 = 24.7 (groups of 3) |
| Zelmer (2003), Experimental Economics 6(3) | Published abstract only | MPCR has a positive, significant effect across 27 studies and 711 groups | Not used as a number. The working-paper coefficient (39.5, 28 studies) is not quoted in the paper |

## 1. Additional aggregates (computed from the same data)

Baseline prompt P0 only, mean contribution in % of endowment:

| Model | Dilemma (4 MPCR values), off | Dilemma, on | m = 1.25, off | m = 1.25, on | m = 0.2, off | m = 0.2, on |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0.0 | 0.0 | 0.0 | 46.0 | 0.0 | 0.0 |
| deepseek-v4.1-flash | 10.5 | 0.0 | 30.0 | 100.0 | 0.0 | 0.0 |
| glm-5.3-flash | 28.0 | 7.8 | 66.5 | 48.0 | 0.0 | 0.0 |
| gpt-5.6-luna | 39.5 | n/a | 90.0 | n/a | 2.0 | n/a |
| hy3 | 68.1 | 0.0 | 88.0 | 98.0 | 0.0 | 0.0 |
| qwen3.8-flash | 37.3 | 0.0 | 56.0 | 84.0 | 2.0 | 0.0 |

Paraphrase set (P0, P1, P2, P4), dilemma range, reasoning off, mean contribution: claude-haiku-5-5 0.0; deepseek-v4.1-flash 29.9; glm-5.3-flash 39.8; gpt-5.6-luna 64.2; hy3 79.9; qwen3.8-flash 35.6.

Lowest and highest variant mean inside the dilemma, reasoning off: claude-haiku-5-5 0.0 (F3 and all neutral variants) to 94.0 (F1); deepseek-v4.1-flash 2.0 (F3) to 80.0 (P3); glm-5.3-flash 18.0 (P2) to 88.0 (F2); gpt-5.6-luna 0.0 (F3) to 91.0 (P4); hy3 4.2 (F3) to 100.0 (F2); qwen3.8-flash 7.5 (P2) to 78.4 (F2).

claude-haiku-5-5, reasoning off, share of decisions (all six MPCR values, 300 per variant) in which the stated integer is 0: P0 100.0%; F1 take frame 96.0% (the other 4.0% state 20); F2 55.3%; F3 100.0%. Under F1 the stated integer is a withdrawal, so 0 means full contribution.

Range of the mean contribution across the four paraphrases inside the dilemma, reasoning off, in percentage points: gpt-5.6-luna 51.5; deepseek-v4.1-flash 37.8; qwen3.8-flash 54.5; glm-5.3-flash 40.0; hy3 32.7; claude-haiku-5-5 0.

Pooled over the six models, reasoning off, dilemma range, mean contribution by variant: P0 30.6; P1 51.9; P2 33.9; P4 49.9; P3 58.8; F1 53.2; F2 73.7; F3 9.8.

Variant F3 at m = 1.25, reasoning off, mean contribution per model: claude-haiku-5-5 0.0; deepseek-v4.1-flash 2.0; glm-5.3-flash 28.5; gpt-5.6-luna 0.0; hy3 1.0; qwen3.8-flash 27.1; unweighted mean of the six 9.8. Take frame F1, claude-haiku-5-5, mean contribution by MPCR (0.2, 0.3, 0.4, 0.5, 0.75, 1.25): 100, 100, 76, 100, 100, 100; dilemma mean 94.0.

All aggregates of this section are reproduced by `python3 -m pgg.extra_aggregates`.

Game-theory vocabulary in the returned text (answer plus reasoning trace) of decisions under variants other than F3, matched with the pattern `public good|prisoner|nash|free.rid|social dilemma`: reasoning off 0.0% to 0.6% of decisions per model; reasoning on 90.0% (claude-haiku-5-5), 97.7% (qwen3.8-flash), 98.3% (glm-5.3-flash), 99.0% (deepseek-v4.1-flash), 100% (hy3). This is a text-level observation; it is not evidence about how the action was produced.

In the table "Mean contribution by MPCR, paraphrase set pooled" below, rows labelled `@high` contain the baseline prompt P0 only, because the reasoning arm used only P0.

## 2. Analysis report (verbatim)


Files: 11 | raw rows: 17945 | decision cells: 15900 (valid 15900) | comprehension probes: 2040
Provider allowance used: 1.8547 USD | bootstrap resamples: 10000 | seed: 20270401
Paraphrase set: ['P0', 'P1', 'P2', 'P4'] | framing set: ['P0', 'F1', 'F2', 'F3']
Run window (UTC): 2026-11-17 18:37:27.463840008 to 2026-11-17 21:00:41.736785412

## Data quality

| label | rows | failed | retried | invalid_first_attempt | missing_cells | temperature_default | served_models |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5@high | 420 | 0 | 0 | 0 | 0 | 0 | claude-haiku-5-5 |
| claude-haiku-5-5@none | 2640 | 0 | 0 | 0 | 0 | 0 | claude-haiku-5-5 |
| deepseek-v4.1-flash@high | 420 | 0 | 0 | 0 | 0 | 0 | deepseek-v4.1-flash |
| deepseek-v4.1-flash@none | 2640 | 0 | 0 | 0 | 0 | 0 | deepseek-v4.1-flash |
| glm-5.3-flash@high | 420 | 0 | 0 | 0 | 0 | 0 | glm-5.3-flash |
| glm-5.3-flash@none | 2640 | 0 | 0 | 0 | 0 | 0 | glm-5.3-flash |
| gpt-5.6-luna@none | 2640 | 0 | 0 | 0 | 0 | 0 | gpt-5.6-luna |
| hy3@high | 420 | 0 | 0 | 0 | 0 | 0 | hy3 |
| hy3@none | 2640 | 0 | 0 | 0 | 0 | 0 | hy3 |
| qwen3.8-flash@high | 421 | 0 | 2 | 1 | 0 | 0 | qwen3.8-flash |
| qwen3.8-flash@none | 2644 | 1 | 2 | 3 | 0 | 0 | qwen3.8-flash |

## Mean contribution (% of endowment) by MPCR, paraphrase set pooled

| label | 0.2 | 0.3 | 0.4 | 0.5 | 0.75 | 1.25 |
|---|---|---|---|---|---|---|
| claude-haiku-5-5@high | 0 | 0 | 0 | 0 | 0 | 46 |
| claude-haiku-5-5@none | 0 | 0 | 0 | 0 | 0 | 0 |
| deepseek-v4.1-flash@high | 0 | 0 | 0 | 0 | 0 | 100 |
| deepseek-v4.1-flash@none | 11.3 | 24.7 | 28.2 | 29.5 | 37 | 47.5 |
| glm-5.3-flash@high | 0 | 4 | 4 | 6 | 17 | 48 |
| glm-5.3-flash@none | 1 | 37.5 | 44.7 | 35 | 42 | 76.6 |
| gpt-5.6-luna@none | 21 | 58.2 | 56.2 | 64 | 78.5 | 97 |
| hy3@high | 0 | 0 | 0 | 0 | 0 | 98 |
| hy3@none | 34.4 | 78.4 | 88.8 | 68.2 | 84.2 | 89.3 |
| qwen3.8-flash@high | 0 | 0 | 0 | 0 | 0 | 84 |
| qwen3.8-flash@none | 3 | 28.6 | 36.9 | 42 | 34.6 | 49.9 |

## H1a: slope of contribution on MPCR inside the dilemma (paraphrase set, variant fixed effects)

| model | n | slope_pp_per_unit | ci_lo | ci_hi | p_one_sided | spearman_rho | logit_coef_full | p_holm | supported |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 800 | 0 | 0 | 0 | 1 |  |  | 1 | False |
| deepseek-v4.1-flash | 800 | 26.6173 | 8.824 | 44.0791 | 0.0022 | 0.0875 | 1.5591 | 0.0109 | True |
| glm-5.3-flash | 800 | 4.648 | -12.3911 | 21.3525 | 0.3138 | 0.0085 | 0.2284 | 0.7399 | False |
| gpt-5.6-luna | 800 | 49.7207 | 33.1557 | 65.8387 | 0 | 0.1636 | 2.8895 | 0 | True |
| hy3 | 800 | 4.2263 | -7.4975 | 16.0765 | 0.2466 | -0.0345 | -0.9256 | 0.7399 | False |
| qwen3.8-flash | 800 | 9.1397 | -7.2126 | 26.0003 | 0.1464 | 0.0627 | 0.18 | 0.5854 | False |

## H1b: out-of-dilemma controls (paraphrase set)

| model | mpcr | dominant_action_pct | n | mean_pct | ci_lo | ci_hi | threshold | verdict |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0.2 | 0 | 200 | 0 | 0 | 0 | <= 10 | pass |
| claude-haiku-5-5 | 1.25 | 100 | 200 | 0 | 0 | 0 | >= 90 | fail |
| deepseek-v4.1-flash | 0.2 | 0 | 200 | 11.3 | 7.1 | 15.7 | <= 10 | inconclusive |
| deepseek-v4.1-flash | 1.25 | 100 | 200 | 47.5 | 40.5 | 54.5 | >= 90 | fail |
| glm-5.3-flash | 0.2 | 0 | 200 | 1 | 0 | 2.5 | <= 10 | pass |
| glm-5.3-flash | 1.25 | 100 | 200 | 76.6 | 70.8 | 82.3 | >= 90 | fail |
| gpt-5.6-luna | 0.2 | 0 | 200 | 21 | 15.5 | 27 | <= 10 | fail |
| gpt-5.6-luna | 1.25 | 100 | 200 | 97 | 94.5 | 99 | >= 90 | pass |
| hy3 | 0.2 | 0 | 200 | 34.4 | 28.4 | 40.6 | <= 10 | fail |
| hy3 | 1.25 | 100 | 200 | 89.3 | 86.1 | 92.1 | >= 90 | inconclusive |
| qwen3.8-flash | 0.2 | 0 | 200 | 3 | 1 | 5.5 | <= 10 | pass |
| qwen3.8-flash | 1.25 | 100 | 200 | 49.9 | 43.3 | 56.6 | >= 90 | fail |

## H2: variance decomposition inside the dilemma (eta-squared)

| model | eta_mpcr_para | eta_wording_para | eta_inter_para | eta_resid_para | p_wording_para_holm | eta_mpcr_fram | eta_wording_fram | diff_fram_minus_para | diff_lo | diff_hi | snr_reported | snr_lo | snr_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 |  |  |  |  |  | 0.055 | 0.711 |  |  |  | undefined (no variation) |  |  |
| deepseek-v4.1-flash | 0.01 | 0.136 | 0.11 | 0.744 | 0 | 0.014 | 0.28 | 0.144 | 0.085 | 0.202 | 0.07 | 0.014 | 0.22 |
| glm-5.3-flash | 0.006 | 0.124 | 0.123 | 0.747 | 0 | 0.006 | 0.296 | 0.172 | 0.108 | 0.232 | 0.05 | 0.01 | 0.186 |
| gpt-5.6-luna | 0.034 | 0.187 | 0.087 | 0.693 | 0 | 0.019 | 0.471 | 0.285 | 0.219 | 0.348 | 0.18 | 0.089 | 0.341 |
| hy3 | 0.058 | 0.179 | 0.127 | 0.636 | 0 | 0.011 | 0.672 | 0.493 | 0.44 | 0.543 | 0.33 | 0.219 | 0.482 |
| qwen3.8-flash | 0.011 | 0.174 | 0.018 | 0.797 | 0 | 0.035 | 0.165 | -0.01 | -0.072 | 0.051 | 0.06 | 0.016 | 0.189 |

## H6 (formed after the pilot): named game F3 against baseline P0

| model | region | variant | p0_mean_pct | mean_pct | diff_pp | ci_lo | ci_hi | p_welch | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | dilemma | F3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| claude-haiku-5-5 | control_m>1 | F3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| deepseek-v4.1-flash | dilemma | F3 | 10.5 | 2 | -8.5 | -13.5 | -4 | 0.0004 | 0.0018 |
| deepseek-v4.1-flash | control_m>1 | F3 | 30 | 2 | -28 | -42 | -15.95 | 0.0001 | 0.0004 |
| glm-5.3-flash | dilemma | F3 | 28 | 21.625 | -6.375 | -14.75 | 2.125 | 0.1402 | 0.3499 |
| glm-5.3-flash | control_m>1 | F3 | 66.5 | 28.5 | -38 | -55.5 | -20 | 0.0001 | 0.0003 |
| gpt-5.6-luna | dilemma | F3 | 39.5 | 0 | -39.5 | -46.25 | -32.75 | 0 | 0 |
| gpt-5.6-luna | control_m>1 | F3 | 90 | 0 | -90 | -98 | -82 | 0 | 0 |
| hy3 | dilemma | F3 | 68.075 | 4.25 | -63.825 | -70.325 | -57.225 | 0 | 0 |
| hy3 | control_m>1 | F3 | 88 | 1 | -87 | -95 | -77 | 0 | 0 |
| qwen3.8-flash | dilemma | F3 | 37.275 | 30.625 | -6.65 | -14.825 | 1.55 | 0.1166 | 0.3499 |
| qwen3.8-flash | control_m>1 | F3 | 56 | 27.1 | -28.9 | -45.5 | -11.8975 | 0.0013 | 0.0026 |

## Mean contribution (%) by variant, dilemma range

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0 | 0 | 0 | 0 | 94 | 65 | 0 |
| deepseek-v4.1-flash | 10.5 | 44.8 | 15.9 | 48.3 | 80 | 59.8 | 33.1 | 2 |
| glm-5.3-flash | 28 | 55.2 | 18 | 58 | 70.5 | 63.9 | 88 | 21.6 |
| gpt-5.6-luna | 39.5 | 50 | 76.5 | 91 | 38 | 7 | 77.8 | 0 |
| hy3 | 68.1 | 99.5 | 85.3 | 66.8 | 99.6 | 45.7 | 100 | 4.2 |
| qwen3.8-flash | 37.3 | 62 | 7.5 | 35.4 | 64.5 | 48.8 | 78.4 | 30.6 |

## Mean contribution (%) by variant, control m > 1 (dominant action: 100)

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0 | 0 | 0 | 0 | 100 | 0 | 0 |
| deepseek-v4.1-flash | 30 | 52 | 28 | 80 | 100 | 83.2 | 68 | 2 |
| glm-5.3-flash | 66.5 | 76 | 96 | 68 | 92 | 87.5 | 96 | 28.5 |
| gpt-5.6-luna | 90 | 98 | 100 | 100 | 100 | 2 | 97 | 0 |
| hy3 | 88 | 96 | 91.2 | 82 | 100 | 45.2 | 100 | 1 |
| qwen3.8-flash | 56 | 59.6 | 38 | 46 | 79.1 | 54.2 | 81.3 | 27.1 |

## Mean contribution (%) by variant, control r < 1 (dominant action: 0)

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0 | 0 | 0 | 0 | 100 | 0 | 0 |
| deepseek-v4.1-flash | 0 | 8 | 26 | 11.2 | 0 | 48.1 | 2 | 2 |
| glm-5.3-flash | 0 | 2 | 2 | 0 | 6 | 29.2 | 20 | 4 |
| gpt-5.6-luna | 2 | 2 | 76 | 4 | 0 | 0 | 5 | 0 |
| hy3 | 0 | 6 | 99.2 | 32.2 | 1 | 38.9 | 15 | 0 |
| qwen3.8-flash | 2 | 0 | 10 | 0 | 2 | 32.5 | 14 | 1 |

## H5 (exploratory): reasoning on minus off, baseline prompt P0

| model | mpcr | off_pct | on_pct | diff_pp | ci_lo | ci_hi | n_on | n_off |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0.2 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| claude-haiku-5-5 | 0.3 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| claude-haiku-5-5 | 0.4 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| claude-haiku-5-5 | 0.5 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| claude-haiku-5-5 | 0.75 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| claude-haiku-5-5 | 1.25 | 0 | 46 | 46 | 32 | 60 | 50 | 50 |
| deepseek-v4.1-flash | 0.2 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| deepseek-v4.1-flash | 0.3 | 8 | 0 | -8 | -16 | -2 | 50 | 50 |
| deepseek-v4.1-flash | 0.4 | 2 | 0 | -2 | -6 | 0 | 50 | 50 |
| deepseek-v4.1-flash | 0.5 | 6 | 0 | -6 | -14 | 0 | 50 | 50 |
| deepseek-v4.1-flash | 0.75 | 26 | 0 | -26 | -38 | -14 | 50 | 50 |
| deepseek-v4.1-flash | 1.25 | 30 | 100 | 70 | 56 | 82 | 50 | 50 |
| glm-5.3-flash | 0.2 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| glm-5.3-flash | 0.3 | 26 | 4 | -22 | -36 | -8 | 50 | 50 |
| glm-5.3-flash | 0.4 | 18 | 4 | -14 | -26 | -3 | 50 | 50 |
| glm-5.3-flash | 0.5 | 26 | 6 | -20 | -34 | -6 | 50 | 50 |
| glm-5.3-flash | 0.75 | 42 | 17 | -25 | -42 | -8 | 50 | 50 |
| glm-5.3-flash | 1.25 | 66.5 | 48 | -18.5 | -36.5 | 1 | 50 | 50 |
| hy3 | 0.2 | 0 | 0 | 0 | 0 | 0 | 50 | 50 |
| hy3 | 0.3 | 76 | 0 | -76 | -88 | -64 | 50 | 50 |
| hy3 | 0.4 | 96.3 | 0 | -96.3 | -100 | -91.2 | 50 | 50 |
| hy3 | 0.5 | 29 | 0 | -29 | -42 | -17 | 50 | 50 |
| hy3 | 0.75 | 71 | 0 | -71 | -83 | -58 | 50 | 50 |
| hy3 | 1.25 | 88 | 98 | 10 | 0 | 20 | 50 | 50 |
| qwen3.8-flash | 0.2 | 2 | 0 | -2 | -6 | 0 | 50 | 50 |
| qwen3.8-flash | 0.3 | 24.5 | 0 | -24.5 | -36 | -14 | 50 | 50 |
| qwen3.8-flash | 0.4 | 38.6 | 0 | -38.6 | -51.5 | -26.3 | 50 | 50 |
| qwen3.8-flash | 0.5 | 47 | 0 | -47 | -60 | -35 | 50 | 50 |
| qwen3.8-flash | 0.75 | 39 | 0 | -39 | -51 | -27 | 50 | 50 |
| qwen3.8-flash | 1.25 | 56 | 84 | 28 | 12 | 43 | 50 | 50 |

## Distribution of contributions (% of valid decisions)

| label | at_zero | at_half | at_full | n | other |
|---|---|---|---|---|---|
| claude-haiku-5-5@high | 92.3 | 0 | 7.7 | 300 | 0 |
| claude-haiku-5-5@none | 82.4 | 0.3 | 17.2 | 2400 | -0 |
| deepseek-v4.1-flash@high | 83.3 | 0 | 16.7 | 300 | -0 |
| deepseek-v4.1-flash@none | 62.5 | 1.5 | 34.5 | 2400 | 1.5 |
| glm-5.3-flash@high | 86.3 | 1 | 12.7 | 300 | 0 |
| glm-5.3-flash@none | 51.8 | 0.2 | 47.3 | 2400 | 0.7 |
| gpt-5.6-luna@none | 53.1 | 2.4 | 44.5 | 2400 | -0 |
| hy3@high | 83.7 | 0 | 16.3 | 300 | -0 |
| hy3@none | 24.2 | 7.9 | 49.5 | 2400 | 18.3 |
| qwen3.8-flash@high | 86 | 0 | 14 | 300 | -0 |
| qwen3.8-flash@none | 53.3 | 9.7 | 34.7 | 2400 | 2.4 |

## Comprehension probes (% correct)

| label | own_full_others_zero | own_zero_others_full | n_per_item |
|---|---|---|---|
| claude-haiku-5-5@high | 100 | 100 | 60 |
| claude-haiku-5-5@none | 100 | 100 | 120 |
| deepseek-v4.1-flash@high | 100 | 100 | 60 |
| deepseek-v4.1-flash@none | 82.5 | 40 | 120 |
| glm-5.3-flash@high | 100 | 60 | 60 |
| glm-5.3-flash@none | 81.7 | 3.3 | 120 |
| gpt-5.6-luna@none | 85.8 | 0 | 120 |
| hy3@high | 100 | 100 | 60 |
| hy3@none | 88.3 | 17.5 | 120 |
| qwen3.8-flash@high | 100 | 100 | 60 |
| qwen3.8-flash@none | 88.3 | 6.7 | 120 |

### By MPCR, both items pooled

| label | 0.2 | 0.3 | 0.4 | 0.5 | 0.75 | 1.25 |
|---|---|---|---|---|---|---|
| claude-haiku-5-5@high | 100 | 100 | 100 | 100 | 100 | 100 |
| claude-haiku-5-5@none | 100 | 100 | 100 | 100 | 100 | 100 |
| deepseek-v4.1-flash@high | 100 | 100 | 100 | 100 | 100 | 100 |
| deepseek-v4.1-flash@none | 92.5 | 72.5 | 57.5 | 42.5 | 52.5 | 50 |
| glm-5.3-flash@high | 90 | 85 | 75 | 85 | 75 | 70 |
| glm-5.3-flash@none | 10 | 50 | 47.5 | 50 | 50 | 47.5 |
| gpt-5.6-luna@none | 7.5 | 50 | 50 | 50 | 50 | 50 |
| hy3@high | 100 | 100 | 100 | 100 | 100 | 100 |
| hy3@none | 15 | 65 | 70 | 67.5 | 50 | 50 |
| qwen3.8-flash@high | 100 | 100 | 100 | 100 | 100 | 100 |
| qwen3.8-flash@none | 42.5 | 50 | 45 | 40 | 57.5 | 50 |
