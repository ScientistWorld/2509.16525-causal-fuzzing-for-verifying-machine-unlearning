# Progress

## What Works

- Implemented the paper's CAFÉ-style adjusted causal effect estimator for total, direct, and indirect residual influence.
- Implemented two semi-synthetic tabular settings modeled after the paper's Heart-Disease and Performance experiments.
- Implemented a direct permutation baseline that fails to detect influence from omitted target features.
- Implemented `scripts/reproduce.sh` and `scripts/evaluate.sh`; evaluation reads artifacts only and does not import from `method/`.

## Results

- Completed containerized CPU reproduction job `ae348bd1-9a4` with exit code 0.
- `python validate.py --compare` passes: `reference.json` and `scores.json` validate, evaluation remains separated from `method/`, and no committed code references `shared/`.
- Heart-Disease feature-unlearning: CAFÉ ranked the omitted target feature `smoking` 1st with `rank_score=1.0`, `indirect_detected=1.0`, and `direct_unlearned=1.0`; direct permutation ranked it 5th with `rank_score=0.0`.
- Performance feature-unlearning: CAFÉ ranked the omitted target feature `gender` 2nd with `rank_score=0.6666666667`, `indirect_detected=1.0`, and `direct_unlearned=1.0`; direct permutation ranked it 4th with `rank_score=0.0`.

## Remaining

- The environment is usable as a research gym at `core_claim_plus`.
- Higher milestones would require expanding beyond the accessible semi-synthetic reproduction, for example by reconstructing additional paper datasets, adding graph-misspecification sensitivity runs, or recovering the paper's open-source prototype if it becomes available.
- Current audit found no reason to rewrite the environment; the existing `setup.sh` installs only Python dependencies and `container.def` is a reasonable CPU base.

## Issues

- The paper markdown does not include concrete training hyperparameters or a repository URL despite mentioning an open-sourced prototype.
- Most reported values for the core ranking experiments are qualitative or figure-based; `reference.json` encodes the paper-supported rank/detection claims rather than copying unreported bar heights.
- The scheduler-provided absolute stdout/stderr paths for job `ae348bd1-9a4` were not visible inside this container, but the job exit code was 0 and the expected output artifacts were present in the workspace.

## Deviations from Paper

- The paper's exact semi-synthetic structural equations were not provided. I recreated semi-synthetic datasets with the same causal roles and evaluation phenomenon: the target feature is omitted from the audited model but retains mediated influence through downstream variables.
- The paper evaluates additional real-world datasets and architectures. This first reproduction focuses on the two semi-synthetic settings needed for the core claim.
