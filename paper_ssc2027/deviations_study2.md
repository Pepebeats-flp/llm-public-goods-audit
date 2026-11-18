# Study 2: deviations from the registered plan

Recorded as they happen. To be reported in the paper.

1. **No OSF registration (17 November 2026).** The plan announced an OSF registration. The authors decided not to make one. The public record of the plan before data collection is commit 28b8b11 of this repository. See `OSF_REGISTRATION.txt`.

2. **Two slow runs were split across processes (17 November 2026, about 40 minutes into the run).** With reasoning on, `hy3` and `qwen3.8-flash` were answering about 3 calls per minute, which projected 13 hours each. Their runs (`study2_on_hy3`, `study2_on_qwen3_8-flash`) were stopped after 94 and 154 completed cells and the remaining cells were divided among four processes per model (`*_s0` to `*_s3`), each taking every fourth cell of the same seeded order and skipping cells already collected.
   - What did not change: the set of cells, the prompts, the models, the settings, the seed and the sample size.
   - What changed: up to four calls to the same model are in flight at once, the order in which cells are collected, and the files `pgg/run_oneshot.py` (new options `shard` and `also_done_from`) and the two configurations, whose hashes no longer match `preregistration_study2_manifest.txt`. Eight configuration files were added.
   - The number of runs the supervisor keeps alive at once was raised from 10 to 18.
   - Outcomes were not examined before or when making this change. The decision was based on call rate only.
