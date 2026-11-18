# Study 2, part A: study2A

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
