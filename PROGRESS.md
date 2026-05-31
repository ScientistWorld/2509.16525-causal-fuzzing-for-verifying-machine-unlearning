# Progress

## What Works

- Implemented the paper's CAFÉ-style adjusted causal effect estimator for total, direct, and indirect residual influence.
- Implemented two semi-synthetic tabular settings modeled after the paper's Heart-Disease and Performance experiments.
- Implemented a direct permutation baseline that fails to detect influence from omitted target features.
- Implemented `scripts/reproduce.sh` and `scripts/evaluate.sh`; evaluation reads artifacts only and does not import from `method/`.

## Results

- Local smoke test on 1,000 samples: Heart-Disease target smoking ranked 1st by CAFÉ and last by direct permutation.
- Local smoke test on 1,000 samples: Performance target gender ranked 2nd by CAFÉ and last by direct permutation, with indirect influence detected and near-zero direct influence.
- Full-size 10,000-sample run is queued via `scripts/run.sh`.

## Remaining

- Run the containerized job to produce official `scoring/scores.json`.
- If the job passes, update milestone to `core_claim`; if it fails, fix and resubmit.

## Issues

- The paper markdown does not include concrete training hyperparameters or a repository URL despite mentioning an open-sourced prototype.
- Most reported values for the core ranking experiments are qualitative or figure-based; `reference.json` encodes the paper-supported rank/detection claims rather than copying unreported bar heights.

## Deviations from Paper

- The paper's exact semi-synthetic structural equations were not provided. I recreated semi-synthetic datasets with the same causal roles and evaluation phenomenon: the target feature is omitted from the audited model but retains mediated influence through downstream variables.
- The paper evaluates additional real-world datasets and architectures. This first reproduction focuses on the two semi-synthetic settings needed for the core claim.
