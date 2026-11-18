# Study 2, part B: study2B

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
