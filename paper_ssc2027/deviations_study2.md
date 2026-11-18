# Study 2: deviations from the registered plan

Recorded as they happen. To be reported in the paper.

1. **No OSF registration (17 November 2026).** The plan announced an OSF registration. The authors decided not to make one. The public record of the plan before data collection is commit 28b8b11 of this repository. See `OSF_REGISTRATION.txt`.

2. **Two slow runs were split across processes (17 November 2026, about 40 minutes into the run).** With reasoning on, `hy3` and `qwen3.8-flash` were answering about 3 calls per minute, which projected 13 hours each. Their runs (`study2_on_hy3`, `study2_on_qwen3_8-flash`) were stopped after 94 and 154 completed cells and the remaining cells were divided among four processes per model (`*_s0` to `*_s3`), each taking every fourth cell of the same seeded order and skipping cells already collected.
   - What did not change: the set of cells, the prompts, the models, the settings, the seed and the sample size.
   - What changed: up to four calls to the same model are in flight at once, the order in which cells are collected, and the files `pgg/run_oneshot.py` (new options `shard` and `also_done_from`) and the two configurations, whose hashes no longer match `preregistration_study2_manifest.txt`. Eight configuration files were added.
   - The number of runs the supervisor keeps alive at once was raised from 10 to 18.
   - Outcomes were not examined before or when making this change. The decision was based on call rate only.

3. **One cell not collected (18 November 2026).** Part B, reasoning on, `deepseek-v4.1-flash`, wording F2: none of the 10 games could be completed. Every game was abandoned after a transport failure in four successive attempts over about six hours. A diagnostic call with the round-1 prompt of that cell returned a valid answer after 90 seconds and 5,137 completion tokens, against a median near 200 tokens and 5 seconds for the same model in the completed cells, so calls were probably exceeding the 180-second client timeout. The run was stopped. Following section 5 of the plan, the model is reported with the data collected and flagged as incomplete. This arm was registered as exploratory.

4. **Instability of one model between batches (observation, not a change of ours).** The round-1 prompt under the baseline wording is identical in the mixed-composition runs and in the homogeneous runs. For `hy3` the answer was the full endowment in 91.1% of 45 decisions in the first batch and in 10.0% of 60 decisions in the second, which began 22 minutes after the first ended. Comparison D4 is therefore uninformative for that model.
