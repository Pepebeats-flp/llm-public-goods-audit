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


---

# STUDY 2

**STATUS: COMPLETE EXCEPT ONE CELL.** All numbers below come from `llm-public-goods-study/data/raw/study2_*.jsonl`, analysed with `python3 -m pgg.analyze_study2`, `python3 -m pgg.analyze_repeated` and `python3 -m pgg.extra_aggregates_study2` (10,000 bootstrap resamples, seeds 20270402 and 20270403). The technical test `techtest_repeated` is not included. The analysis plan is `paper_ssc2027/preregistration_study2.md`.

## S2.0 Run registry

| Field | Value |
|---|---|
| Dates | 17 November 2026 23:23 UTC to 18 November 2026 07:56 UTC |
| Access, models, temperature | As in Study 1 |
| Part A (one-shot, reasoning on, 8 variants) | 12,000 cells planned and completed; 12,004 calls; 4 invalid first outputs, all valid when asked again; no failed call; 133 calls needed a transport retry |
| Part B (repeated game) | 420 games planned; 410 completed; 0 discarded; 15,503 LLM calls; 3 invalid outputs, all valid when asked again |
| Part B, missing cell | deepseek-v4.1-flash with reasoning on, wording F2: 0 of 10 games. See deviation 3 |
| Provider allowance used | Part A 6.02 USD; part B 2.10 USD |

Completed games per cell of part B: reasoning off, homogeneous, 15 per model and wording (P0, F2, F3) for the six models (270 games); reasoning off, one selfish rule agent, P0, 15 per model (90 games); reasoning on, homogeneous, glm-5.3-flash 10 per wording (30 games), deepseek-v4.1-flash 10 for P0 and 10 for F3 (20 games).

### Deviations from the Study 2 plan

1. The plan was not registered on OSF. The public record of the plan before data collection is commit 28b8b11 of the repository (`paper_ssc2027/OSF_REGISTRATION.txt`).
2. About 40 minutes into the run, the reasoning-on runs of hy3 and qwen3.8-flash in part A were split across four processes each, to shorten a projected 13 hours. Cells, prompts, settings, seed and sample size did not change; up to four calls per model were in flight at once. The decision used call rates only (`paper_ssc2027/deviations_study2.md`).
3. Part B, reasoning on, deepseek-v4.1-flash, wording F2: none of the 10 games could be completed. Every game was abandoned after a transport failure in four successive attempts over six hours (first run and three automatic restarts). A diagnostic call on 18 November with the round-1 prompt of that cell returned a valid answer after 90 seconds and 5,137 completion tokens, against a median of about 200 tokens and 5 seconds for the same model in the completed cells, so calls in this cell were probably exceeding the 180-second client timeout. Following the plan, the model is reported with the data collected and flagged as incomplete. Part B with reasoning on was registered as exploratory.
4. Instability between batches for hy3 (not a deviation of ours, but it qualifies comparisons): see S2.1.

## S2.1 Additional aggregates

Output of `python3 -m pgg.extra_aggregates_study2`:

```text
== Part A ==
calls 12004 | cells 12000 | invalid first attempts 4 | failed calls 0 | calls needing a transport retry 133
window: 17 Nov 23:23 UTC to 18 Nov 05:45 UTC
allowance 6.02 USD

Reasoning on, m = 1.25: lowest and highest variant mean, and range
  claude-haiku-5-5       min  16.0 (P3)  max  98.0 (F1)  range  82.0
  deepseek-v4.1-flash    min  98.0 (P1)  max 100.0 (P0)  range   2.0
  glm-5.3-flash          min  14.0 (F3)  max  84.0 (F2)  range  70.0
  hy3                    min  98.0 (P0)  max 100.0 (P1)  range   2.0
  qwen3.8-flash          min  90.0 (P4)  max  98.0 (P2)  range   8.0

Reasoning on, dilemma: share of the 32 (MPCR x variant) cells per model in which every decision is zero
   {'claude-haiku-5-5': 81.2, 'deepseek-v4.1-flash': 100.0, 'glm-5.3-flash': 3.1, 'hy3': 100.0, 'qwen3.8-flash': 87.5}
Reasoning on, dilemma, pooled over the five models, by variant: {'P0': 1.6, 'P1': 1.4, 'P2': 4.9, 'P4': 2.1, 'P3': 5.8, 'F1': 3.2, 'F2': 13.2, 'F3': 1.2}
median completion tokens per call: {'claude-haiku-5-5@high': 271.0, 'deepseek-v4.1-flash@high': 202.0, 'glm-5.3-flash@high': 97.5, 'hy3@high': 1254.0, 'qwen3.8-flash@high': 337.0}

== Part B ==
LLM calls 15503 | completed games 410 | invalid outputs 3 | discarded games 0 | calls needing a transport retry 38
window: 17 Nov 23:23 UTC to 18 Nov 07:56 UTC
completed games per cell:
 variant                               F2  F3  P0
label                    composition            
claude-haiku-5-5@none    homogeneous  15  15  15
                         one_selfish   0   0  15
deepseek-v4.1-flash@high homogeneous   0  10  10
deepseek-v4.1-flash@none homogeneous  15  15  15
                         one_selfish   0   0  15
glm-5.3-flash@high       homogeneous  10  10  10
glm-5.3-flash@none       homogeneous  15  15  15
                         one_selfish   0   0  15
gpt-5.6-luna@none        homogeneous  15  15  15
                         one_selfish   0   0  15
hy3@none                 homogeneous  15  15  15
                         one_selfish   0   0  15
qwen3.8-flash@none       homogeneous  15  15  15
                         one_selfish   0   0  15

First decision under the baseline wording, reasoning off: one-shot (Study 1, m = 0.4) against round 1 of the repeated game
  claude-haiku-5-5       one-shot   0.0   repeated, round 1  50.0
  deepseek-v4.1-flash    one-shot   2.0   repeated, round 1   0.8
  glm-5.3-flash          one-shot  18.0   repeated, round 1  80.8
  gpt-5.6-luna           one-shot  10.0   repeated, round 1  35.8
  hy3                    one-shot  96.3   repeated, round 1  55.0
  qwen3.8-flash          one-shot  38.6   repeated, round 1  66.2

Same prompt, same settings, two batches: round 1 under P0 in the mixed-composition runs and in the homogeneous runs
  claude-haiku-5-5       one_selfish: n=45 mean  50.0 answers of 20:   0.0% (17 Nov 23:23 UTC to 17 Nov 23:40 UTC) | homogeneous: n=60 mean  50.0 answers of 20:   0.0% (17 Nov 23:42 UTC to 18 Nov 00:53 UTC) | prompt hashes: ['1cbb7ea7f1b2']
  deepseek-v4.1-flash    one_selfish: n=45 mean   3.1 answers of 20:   2.2% (17 Nov 23:23 UTC to 17 Nov 23:43 UTC) | homogeneous: n=60 mean   0.8 answers of 20:   0.0% (17 Nov 23:46 UTC to 18 Nov 01:08 UTC) | prompt hashes: ['1cbb7ea7f1b2']
  glm-5.3-flash          one_selfish: n=45 mean  78.6 answers of 20:  55.6% (17 Nov 23:23 UTC to 17 Nov 23:40 UTC) | homogeneous: n=60 mean  80.8 answers of 20:  61.7% (17 Nov 23:45 UTC to 18 Nov 00:58 UTC) | prompt hashes: ['1cbb7ea7f1b2']
  gpt-5.6-luna           one_selfish: n=45 mean  41.1 answers of 20:  15.6% (17 Nov 23:23 UTC to 17 Nov 23:41 UTC) | homogeneous: n=60 mean  35.8 answers of 20:  18.3% (17 Nov 23:50 UTC to 18 Nov 00:57 UTC) | prompt hashes: ['1cbb7ea7f1b2']
  hy3                    one_selfish: n=45 mean  96.2 answers of 20:  91.1% (17 Nov 23:23 UTC to 17 Nov 23:47 UTC) | homogeneous: n=60 mean  55.0 answers of 20:  10.0% (18 Nov 00:09 UTC to 18 Nov 01:41 UTC) | prompt hashes: ['1cbb7ea7f1b2']
  qwen3.8-flash          one_selfish: n=45 mean  63.3 answers of 20:  28.9% (17 Nov 23:41 UTC to 18 Nov 00:01 UTC) | homogeneous: n=60 mean  66.2 answers of 20:  38.3% (18 Nov 00:06 UTC to 18 Nov 01:21 UTC) | prompt hashes: ['1cbb7ea7f1b2']

Mean contribution by round, reasoning off, homogeneous groups
round                          1      2      3      4      5      6      7      8      9      10
model               variant                                                                     
claude-haiku-5-5    F2       50.0   50.0   50.0   50.0   50.0   50.0   50.0   50.0   50.0    0.0
                    F3       50.0   49.7   49.7   49.7   49.2   48.1   47.7   46.2   40.2    0.0
                    P0       50.0   50.0   50.0   50.0   45.0   42.6   29.2   15.5    0.8    0.0
deepseek-v4.1-flash F2       20.0   19.2   15.8   10.0   11.7    6.0    3.3    3.3    3.3    1.7
                    F3       24.6    0.5    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
                    P0        0.8    6.7    5.0    3.3    6.7    6.7    0.0    1.7    5.0    0.0
glm-5.3-flash       F2       88.5   98.8  100.0  100.0  100.0  100.0  100.0  100.0  100.0  100.0
                    F3       71.7   76.2   78.9   80.8   81.5   81.8   81.8   82.0   81.6   68.4
                    P0       80.8   91.9   95.1   95.8   95.9   96.0   96.4   96.6   96.7   94.2
gpt-5.6-luna        F2       71.7   51.7   32.4   25.8   19.7   16.8   15.7   15.0   13.9   11.3
                    F3       25.0   27.1   29.8   29.9   30.0   30.2   30.2   30.2   29.7   10.7
                    P0       35.8    6.0    2.5    0.2    0.0    0.0    0.0    0.0    0.0    0.0
hy3                 F2       98.1  100.0  100.0  100.0  100.0  100.0  100.0  100.0  100.0  100.0
                    F3       50.0   50.0   50.0   50.0   50.0   50.0   50.0   50.0   50.0   13.3
                    P0       55.0   53.7   51.9   51.9   51.9   51.9   51.9   51.9   51.9   84.4
qwen3.8-flash       F2       84.6   90.9   90.3   91.2   91.5   87.2   80.1   77.2   78.8   70.5
                    F3       69.2   74.7   72.8   67.8   62.9   58.9   55.9   53.3   43.6   13.7
                    P0       66.2   67.0   61.2   59.6   58.3   49.5   40.8   47.9   36.0   29.2
```

Reading notes for the block above.

- **Instability of hy3 between batches.** The round-1 prompt under P0 is identical in the mixed-composition runs and in the homogeneous runs (same hash, same settings, reasoning off). For hy3 the answer was 20 in 91.1% of 45 decisions in the first batch (17 Nov 23:23 to 23:47 UTC) and in 10.0% of 60 decisions in the second (18 Nov 00:09 to 01:41 UTC); means 96.2% and 55.0%. The other five models differ by at most 5.3 points between the two batches. Consequences: the comparison D4 is confounded for hy3, and the one-shot versus round-1 comparison is uninformative for hy3. Comparisons between wordings inside the homogeneous run of hy3 are not affected, because the three wordings were interleaved in one process.
- **Announcing repetition.** Under the baseline wording and without reasoning, the first decision of the repeated game differs from the one-shot decision at the same return (m = 0.4): claude-haiku-5-5 0.0 against 50.0; glm-5.3-flash 18.0 against 80.8; gpt-5.6-luna 10.0 against 35.8; qwen3.8-flash 38.6 against 66.2; deepseek-v4.1-flash 2.0 against 0.8. The two prompts differ in more than the mention of repetition and the data were collected on different days, so this is descriptive.

## S2.2 Part A report (verbatim)


Reasoning-on decisions: 12000 | models: claude-haiku-5-5, deepseek-v4.1-flash, glm-5.3-flash, hy3, qwen3.8-flash | bootstrap: 10000 | seed: 20270402

## Mean contribution (%) by variant, reasoning on, dilemma range

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0.5 | 0 | 0 | 0 | 1 | 4 | 0 |
| deepseek-v4.1-flash | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glm-5.3-flash | 8 | 6.8 | 24.5 | 10.5 | 29 | 15.1 | 41.2 | 6 |
| hy3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3.8-flash | 0 | 0 | 0 | 0 | 0 | 0 | 20.8 | 0 |

## Mean contribution (%) by variant, reasoning on, control m = 1.25 (dominant action 100)

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 54 | 36 | 68 | 58 | 16 | 98 | 54 | 30 |
| deepseek-v4.1-flash | 100 | 98 | 100 | 100 | 100 | 100 | 100 | 100 |
| glm-5.3-flash | 66 | 74 | 73 | 80 | 62 | 68 | 84 | 14 |
| hy3 | 98 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| qwen3.8-flash | 92 | 92 | 98 | 90 | 94 | 98 | 98 | 90 |

## Mean contribution (%) by variant, reasoning on, control m = 0.2 (dominant action 0)

| model | P0 | P1 | P2 | P4 | P3 | F1 | F2 | F3 |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deepseek-v4.1-flash | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| glm-5.3-flash | 0 | 0 | 5 | 4 | 0 | 0 | 13 | 0 |
| hy3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3.8-flash | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## A1: range of variant means (percentage points) inside the dilemma, reasoning on versus off

| model | paraphrase_range_on | paraphrase_on_lo | paraphrase_on_hi | eta_wording_paraphrase_on | eta_mpcr_paraphrase_on | paraphrase_range_off | paraphrase_diff_on_minus_off | paraphrase_diff_lo | paraphrase_diff_hi | paraphrase_diff_lo_fw | paraphrase_diff_hi_fw | paraphrase_reduced | framing_range_on | framing_on_lo | framing_on_hi | eta_wording_framing_on | eta_mpcr_framing_on | framing_range_off | framing_diff_on_minus_off | framing_diff_lo | framing_diff_hi | framing_diff_lo_fw | framing_diff_hi_fw | framing_reduced | snr_on | snr_on_reported |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0.5 | 0 | 1.5 | 0.004 | 0.004 | 0 | 0.5 | 0 | 1.5 | 0 | 2 | False | 4 | 1.5 | 7 | 0.022 | 0.006 | 94 | -90 | -94 | -86 | -95 | -84.5 | True | 1 | 1.00 |
| deepseek-v4.1-flash | 0 | 0 | 0 |  |  | 37.775 | -37.775 | -45.25 | -32 | -47.301 | -30 | True | 0 | 0 | 0 |  |  | 57.85 | -57.85 | -63.925 | -51.725 | -65.725 | -49.75 | True |  | undefined (no variation) |
| glm-5.3-flash | 17.75 | 12 | 25 | 0.047 | 0.002 | 40 | -22.25 | -32 | -12.7 | -35.5 | -9.5 | True | 35.25 | 28.5 | 42.75 | 0.144 | 0.012 | 66.375 | -31.125 | -40.625 | -21.125 | -43.75 | -17.75 | True | 0.049 | 0.05 |
| hy3 | 0 | 0 | 0 |  |  | 32.725 | -32.725 | -36.901 | -31.075 | -38.625 | -30.475 | True | 0 | 0 | 0 |  |  | 95.75 | -95.75 | -97.5 | -93.75 | -98 | -93 | True |  | undefined (no variation) |
| qwen3.8-flash | 0 | 0 | 0 |  |  | 54.475 | -54.475 | -61.725 | -47.45 | -63.501 | -44.75 | True | 20.75 | 15.5 | 26.5 | 0.165 | 0.009 | 47.725 | -26.975 | -35.725 | -18.05 | -38.125 | -15.425 | True |  | undefined (no variation) |

## A2: slope inside the dilemma and controls, reasoning on, paraphrase set

| model | slope_pp | p_one_sided | slope_lo | slope_hi | dilemma_mean_pct | ctrl_low_mean_pct | ctrl_low_lo | ctrl_low_hi | ctrl_low_verdict | ctrl_high_mean_pct | ctrl_high_lo | ctrl_high_hi | ctrl_high_verdict | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 1.173 | 0.159 | 0 | 3.52 | 0.125 | 0 | 0 | 0 | pass | 54 | 47 | 61 | fail | 0.637 |
| deepseek-v4.1-flash | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | pass | 99.5 | 98.5 | 100 | pass | 1 |
| glm-5.3-flash | 9.134 | 0.097 | -4.302 | 22.571 | 12.438 | 2.25 | 0.5 | 4.5 | pass | 73.25 | 67 | 79.25 | fail | 0.487 |
| hy3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | pass | 99.5 | 98.5 | 100 | pass | 1 |
| qwen3.8-flash | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | pass | 93 | 89 | 96.5 | inconclusive | 1 |

## A3: named game F3 minus baseline P0, reasoning on

| model | region | p0_pct | f3_pct | diff_pp | ci_lo | ci_hi |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | dilemma | 0 | 0 | 0 | 0 | 0 |
| claude-haiku-5-5 | control_m>1 | 54 | 30 | -24 | -42 | -6 |
| deepseek-v4.1-flash | dilemma | 0 | 0 | 0 | 0 | 0 |
| deepseek-v4.1-flash | control_m>1 | 100 | 100 | 0 | 0 | 0 |
| glm-5.3-flash | dilemma | 8 | 6 | -2 | -6.8 | 2.7 |
| glm-5.3-flash | control_m>1 | 66 | 14 | -52 | -68 | -36 |
| hy3 | dilemma | 0 | 0 | 0 | 0 | 0 |
| hy3 | control_m>1 | 98 | 100 | 2 | 0 | 6 |
| qwen3.8-flash | dilemma | 0 | 0 | 0 | 0 | 0 |
| qwen3.8-flash | control_m>1 | 92 | 90 | -2 | -14 | 10 |

## A4: baseline prompt with reasoning on, Study 2 run against Study 1 run

| model | mpcr | study1_pct | study2_pct | diff_pp | ci_lo | ci_hi | differs |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0.2 | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5 | 0.3 | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5 | 0.4 | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5 | 0.5 | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5 | 0.75 | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5 | 1.25 | 46 | 54 | 8 | -12 | 28 | False |
| deepseek-v4.1-flash | 0.2 | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash | 0.3 | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash | 0.4 | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash | 0.5 | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash | 0.75 | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash | 1.25 | 100 | 100 | 0 | 0 | 0 | False |
| glm-5.3-flash | 0.2 | 0 | 0 | 0 | 0 | 0 | False |
| glm-5.3-flash | 0.3 | 4 | 3 | -1 | -8 | 6 | False |
| glm-5.3-flash | 0.4 | 4 | 8 | 4 | -4 | 13 | False |
| glm-5.3-flash | 0.5 | 6 | 8 | 2 | -8 | 11 | False |
| glm-5.3-flash | 0.75 | 17 | 13 | -4 | -18 | 10 | False |
| glm-5.3-flash | 1.25 | 48 | 66 | 18 | -2 | 36 | False |
| hy3 | 0.2 | 0 | 0 | 0 | 0 | 0 | False |
| hy3 | 0.3 | 0 | 0 | 0 | 0 | 0 | False |
| hy3 | 0.4 | 0 | 0 | 0 | 0 | 0 | False |
| hy3 | 0.5 | 0 | 0 | 0 | 0 | 0 | False |
| hy3 | 0.75 | 0 | 0 | 0 | 0 | 0 | False |
| hy3 | 1.25 | 98 | 98 | 0 | -6 | 6 | False |
| qwen3.8-flash | 0.2 | 0 | 0 | 0 | 0 | 0 | False |
| qwen3.8-flash | 0.3 | 0 | 0 | 0 | 0 | 0 | False |
| qwen3.8-flash | 0.4 | 0 | 0 | 0 | 0 | 0 | False |
| qwen3.8-flash | 0.5 | 0 | 0 | 0 | 0 | 0 | False |
| qwen3.8-flash | 0.75 | 0 | 0 | 0 | 0 | 0 | False |
| qwen3.8-flash | 1.25 | 84 | 92 | 8 | -4 | 20 | False |


## S2.3 Part B report (verbatim)


## Games by status

| label | composition | variant | complete |
|---|---|---|---|
| claude-haiku-5-5@none | homogeneous | F2 | 15 |
| claude-haiku-5-5@none | homogeneous | F3 | 15 |
| claude-haiku-5-5@none | homogeneous | P0 | 15 |
| claude-haiku-5-5@none | one_selfish | P0 | 15 |
| deepseek-v4.1-flash@high | homogeneous | F3 | 10 |
| deepseek-v4.1-flash@high | homogeneous | P0 | 10 |
| deepseek-v4.1-flash@none | homogeneous | F2 | 15 |
| deepseek-v4.1-flash@none | homogeneous | F3 | 15 |
| deepseek-v4.1-flash@none | homogeneous | P0 | 15 |
| deepseek-v4.1-flash@none | one_selfish | P0 | 15 |
| glm-5.3-flash@high | homogeneous | F2 | 10 |
| glm-5.3-flash@high | homogeneous | F3 | 10 |
| glm-5.3-flash@high | homogeneous | P0 | 10 |
| glm-5.3-flash@none | homogeneous | F2 | 15 |
| glm-5.3-flash@none | homogeneous | F3 | 15 |
| glm-5.3-flash@none | homogeneous | P0 | 15 |
| glm-5.3-flash@none | one_selfish | P0 | 15 |
| gpt-5.6-luna@none | homogeneous | F2 | 15 |
| gpt-5.6-luna@none | homogeneous | F3 | 15 |
| gpt-5.6-luna@none | homogeneous | P0 | 15 |
| gpt-5.6-luna@none | one_selfish | P0 | 15 |
| hy3@none | homogeneous | F2 | 15 |
| hy3@none | homogeneous | F3 | 15 |
| hy3@none | homogeneous | P0 | 15 |
| hy3@none | one_selfish | P0 | 15 |
| qwen3.8-flash@none | homogeneous | F2 | 15 |
| qwen3.8-flash@none | homogeneous | F3 | 15 |
| qwen3.8-flash@none | homogeneous | P0 | 15 |
| qwen3.8-flash@none | one_selfish | P0 | 15 |

LLM calls: 15503 | completed games: 410 | discarded: 0 | rounds: 10 | allowance: 2.1005 USD | bootstrap: 10000

## Contribution of the LLM agents (% of endowment), by condition

| label | composition | variant | groups | round1 | roundT | all_rounds | slope_per_round | slope_lo | slope_hi | endgame | reciprocity | reciprocity_lo | reciprocity_hi | reciprocity_groups | gini_payoffs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5@none | homogeneous | F2 | 15 | 50 | 0 | 45 | -2.727 | -2.727 | -2.727 | -50 |  |  |  | 0 | 0 |
| claude-haiku-5-5@none | homogeneous | F3 | 15 | 50 | 0 | 43.05 | -3.274 | -3.746 | -2.904 | -44.722 | 2.353 | 1.534 | 2.906 | 8 | 0.004 |
| claude-haiku-5-5@none | homogeneous | P0 | 15 | 50 | 0 | 33.317 | -6.251 | -6.707 | -5.745 | -15.194 | 0.557 | 0.455 | 0.654 | 13 | 0.013 |
| claude-haiku-5-5@none | one_selfish | P0 | 15 | 50 | 0 | 15 | -5.481 | -5.598 | -5.347 | -0.63 | 0.526 | 0.398 | 0.659 | 15 | 0.003 |
| deepseek-v4.1-flash@high | homogeneous | F3 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  | 0 | 0 |
| deepseek-v4.1-flash@high | homogeneous | P0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  | 0 | 0 |
| deepseek-v4.1-flash@none | homogeneous | F2 | 15 | 20 | 1.667 | 9.433 | -2.206 | -3.157 | -1.309 | -1.667 | 0.086 | 0.003 | 0.185 | 15 | 0.031 |
| deepseek-v4.1-flash@none | homogeneous | F3 | 15 | 24.583 | 0 | 2.508 | -1.362 | -1.836 | -0.909 | 0 | 0.001 | 0 | 0.002 | 12 | 0.016 |
| deepseek-v4.1-flash@none | homogeneous | P0 | 15 | 0.833 | 0 | 3.583 | -0.278 | -0.616 | 0.025 | -2.222 | -0.033 | -0.111 | 0.063 | 13 | 0.02 |
| deepseek-v4.1-flash@none | one_selfish | P0 | 15 | 3.111 | 2.222 | 4.756 | -0.385 | -0.808 | 0.005 | 0.741 | -0.065 | -0.174 | 0.104 | 13 | 0.018 |
| glm-5.3-flash@high | homogeneous | F2 | 10 | 78.75 | 32.5 | 71.325 | -4.718 | -7.981 | -1.45 | -30.75 | 0.475 | 0.1 | 1.06 | 8 | 0.041 |
| glm-5.3-flash@high | homogeneous | F3 | 10 | 59 | 1.875 | 43.762 | -5.101 | -6.037 | -4.17 | -34.417 | 0.244 | -0.792 | 1.046 | 10 | 0.011 |
| glm-5.3-flash@high | homogeneous | P0 | 10 | 74.375 | 11.875 | 62.65 | -6.779 | -8.723 | -4.812 | -37.792 | 0.474 | 0.313 | 0.642 | 9 | 0.046 |
| glm-5.3-flash@none | homogeneous | F2 | 15 | 88.5 | 100 | 98.725 | 0.68 | 0.425 | 0.947 | 0 | 0.004 | 0.001 | 0.008 | 11 | 0.005 |
| glm-5.3-flash@none | homogeneous | F3 | 15 | 71.667 | 68.417 | 78.45 | 0.166 | -1.166 | 1.384 | -13.361 | 0.587 | 0.086 | 1.284 | 15 | 0.017 |
| glm-5.3-flash@none | homogeneous | P0 | 15 | 80.833 | 94.167 | 93.933 | 0.987 | 0.375 | 1.576 | -2.389 | 0.01 | 0.005 | 0.016 | 13 | 0.009 |
| glm-5.3-flash@none | one_selfish | P0 | 15 | 78.556 | 54.556 | 63.6 | -2.877 | -4.835 | -1.107 | -2 | 0.046 | -0.391 | 0.448 | 11 | 0.033 |
| gpt-5.6-luna@none | homogeneous | F2 | 15 | 71.667 | 11.333 | 27.4 | -5.622 | -6.738 | -4.394 | -3.528 | 0.246 | 0.147 | 0.355 | 15 | 0.026 |
| gpt-5.6-luna@none | homogeneous | F3 | 15 | 25 | 10.667 | 27.267 | -0.657 | -1.079 | -0.236 | -19.333 | 0.002 | -0.226 | 0.222 | 13 | 0.017 |
| gpt-5.6-luna@none | homogeneous | P0 | 15 | 35.833 | 0 | 4.458 | -2.289 | -2.977 | -1.663 | 0 | 0.094 | 0.024 | 0.18 | 15 | 0.018 |
| gpt-5.6-luna@none | one_selfish | P0 | 15 | 41.111 | 0 | 4.622 | -2.432 | -3.131 | -1.833 | 0 | 0.074 | -0.003 | 0.181 | 14 | 0.013 |
| hy3@none | homogeneous | F2 | 15 | 98.083 | 100 | 99.808 | 0.105 | 0 | 0.227 | 0 | 0 | -0 | 0 | 3 | 0.001 |
| hy3@none | homogeneous | F3 | 15 | 50 | 13.333 | 46.333 | -2 | -2.364 | -1.636 | -36.667 |  |  |  | 0 | 0.005 |
| hy3@none | homogeneous | P0 | 15 | 55 | 84.417 | 55.65 | 1.53 | 0.879 | 2.084 | 32.5 | -0.274 | -0.643 | 0.097 | 5 | 0.021 |
| hy3@none | one_selfish | P0 | 15 | 96.222 | 80 | 83.267 | -1.475 | -3.305 | 0 | 0 | 0.656 | 0.345 | 0.899 | 3 | 0.004 |
| qwen3.8-flash@none | homogeneous | F2 | 15 | 84.583 | 70.5 | 84.233 | -1.909 | -4.568 | 0.446 | -8.194 | 0.256 | 0.066 | 0.428 | 12 | 0.03 |
| qwen3.8-flash@none | homogeneous | F3 | 15 | 69.167 | 13.667 | 57.283 | -5.178 | -7.073 | -3.274 | -37.278 | 0.446 | 0.053 | 0.784 | 13 | 0.028 |
| qwen3.8-flash@none | homogeneous | P0 | 15 | 66.25 | 29.167 | 51.575 | -4.134 | -5.882 | -2.264 | -12.417 | 0.217 | 0.012 | 0.448 | 15 | 0.046 |
| qwen3.8-flash@none | one_selfish | P0 | 15 | 63.333 | 2.222 | 22.4 | -7.04 | -8.024 | -5.91 | -2.222 | 0.57 | 0.41 | 0.723 | 15 | 0.018 |

## D1: gap between wordings in round 1 and in the last round (percentage points)

| label | contrast | gap_round1 | round1_lo | round1_hi | round1_lo_fw | round1_hi_fw | round1_nonzero | gap_roundT | roundT_lo | roundT_hi | roundT_lo_fw | roundT_hi_fw | roundT_nonzero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5@none | F2 - F3 | 0 | 0 | 0 | 0 | 0 | False | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5@none | F2 - P0 | 0 | 0 | 0 | 0 | 0 | False | 0 | 0 | 0 | 0 | 0 | False |
| claude-haiku-5-5@none | P0 - F3 | 0 | 0 | 0 | 0 | 0 | False | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash@high | P0 - F3 | 0 | 0 | 0 | 0 | 0 | False | 0 | 0 | 0 | 0 | 0 | False |
| deepseek-v4.1-flash@none | F2 - F3 | -4.6 | -18.3 | 10 | -23.3 | 15 | False | 1.7 | 0 | 5 | 0 | 6.7 | False |
| deepseek-v4.1-flash@none | F2 - P0 | 19.2 | 7.5 | 30.8 | 4.2 | 35.8 | True | 1.7 | 0 | 5 | 0 | 6.7 | False |
| deepseek-v4.1-flash@none | P0 - F3 | -23.8 | -32.1 | -15 | -34.6 | -12.5 | True | 0 | 0 | 0 | 0 | 0 | False |
| glm-5.3-flash@high | F2 - F3 | 19.8 | 10.6 | 29.5 | 7.9 | 32.6 | True | 30.6 | 8.1 | 53.1 | 3.1 | 60.6 | True |
| glm-5.3-flash@high | F2 - P0 | 4.4 | -6.2 | 15 | -10 | 19 | False | 20.6 | -2.5 | 45.6 | -11.5 | 53.1 | False |
| glm-5.3-flash@high | P0 - F3 | 15.4 | 7.5 | 23.5 | 4.4 | 26.8 | True | 10 | 0 | 21.9 | -3.1 | 25.6 | False |
| glm-5.3-flash@none | F2 - F3 | 16.8 | 10.4 | 23.1 | 8.2 | 25.2 | True | 31.6 | 13.1 | 51.7 | 7.9 | 58.3 | True |
| glm-5.3-flash@none | F2 - P0 | 7.7 | 0.5 | 15.2 | -1.7 | 18.7 | False | 5.8 | 0 | 17.5 | 0 | 23.3 | False |
| glm-5.3-flash@none | P0 - F3 | 9.2 | 1.2 | 16.2 | -1.7 | 18.8 | False | 25.8 | 3.3 | 48.3 | -4.8 | 55.8 | False |
| gpt-5.6-luna@none | F2 - F3 | 46.7 | 36.7 | 55.8 | 33.3 | 58.3 | True | 0.7 | -11 | 13.6 | -14.6 | 18.2 | False |
| gpt-5.6-luna@none | F2 - P0 | 35.8 | 25 | 45.8 | 20.8 | 49.2 | True | 11.3 | 1.8 | 22.1 | 0.4 | 27.2 | True |
| gpt-5.6-luna@none | P0 - F3 | 10.8 | 0 | 21.7 | -3.3 | 25.8 | False | -10.7 | -17.8 | -4.4 | -19.9 | -2.7 | True |
| hy3@none | F2 - F3 | 48.1 | 45.8 | 50 | 44.9 | 50 | True | 86.7 | 80 | 93.3 | 77.5 | 95 | True |
| hy3@none | F2 - P0 | 43.1 | 38.4 | 47.1 | 36.8 | 48.3 | True | 15.6 | 8.1 | 23.9 | 5.8 | 27.2 | True |
| hy3@none | P0 - F3 | 5 | 1.7 | 9.2 | 0.8 | 10.8 | True | 71.1 | 60.8 | 81.1 | 56.7 | 84.2 | True |
| qwen3.8-flash@none | F2 - F3 | 15.4 | 7.9 | 23.3 | 5.4 | 25.8 | True | 56.8 | 31.8 | 79.3 | 21.7 | 86 | True |
| qwen3.8-flash@none | F2 - P0 | 18.3 | 9.6 | 27.1 | 6.7 | 30 | True | 41.3 | 11.7 | 68.5 | -0.7 | 75.3 | False |
| qwen3.8-flash@none | P0 - F3 | -2.9 | -11.7 | 5.4 | -14.6 | 8.3 | False | 15.5 | -7.8 | 40 | -15.9 | 48 | False |

## D4 (exploratory): LLM agents with one selfish rule agent in the group, against homogeneous groups, wording P0

| label | rounds | with_selfish | homogeneous | diff_pp | ci_lo | ci_hi |
|---|---|---|---|---|---|---|
| claude-haiku-5-5@none | round1 | 50 | 50 | 0 | 0 | 0 |
| claude-haiku-5-5@none | rounds2toT | 11.1 | 31.5 | -20.4 | -23.1 | -17.7 |
| deepseek-v4.1-flash@none | round1 | 3.1 | 0.8 | 2.3 | -1.7 | 7.6 |
| deepseek-v4.1-flash@none | rounds2toT | 4.9 | 3.9 | 1 | -1.4 | 3.5 |
| glm-5.3-flash@none | round1 | 78.6 | 80.8 | -2.3 | -11.7 | 7.4 |
| glm-5.3-flash@none | rounds2toT | 61.9 | 95.4 | -33.5 | -53.7 | -13.3 |
| gpt-5.6-luna@none | round1 | 41.1 | 35.8 | 5.3 | -7.2 | 18.1 |
| gpt-5.6-luna@none | rounds2toT | 0.6 | 1 | -0.4 | -1.3 | 0.5 |
| hy3@none | round1 | 96.2 | 55 | 41.2 | 35.2 | 46.6 |
| hy3@none | rounds2toT | 81.8 | 55.7 | 26.1 | 4.9 | 43.8 |
| qwen3.8-flash@none | round1 | 63.3 | 66.2 | -2.9 | -13.9 | 7.8 |
| qwen3.8-flash@none | rounds2toT | 17.9 | 49.9 | -32.1 | -49.3 | -15.1 |

