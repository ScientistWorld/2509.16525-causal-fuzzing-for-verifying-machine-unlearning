# Progress

## What Works

- Implemented the paper's CAFÉ-style adjusted expected-prediction contrast estimator for total, direct, and indirect residual influence. The estimator identifies backdoor controls and mediators from the causal DAG, estimates conditional expected black-box predictions under two intervention values, and averages the contrast over the observed control distribution.
- Added an Algorithm 1-style causal fuzzing oracle that learns structural equations for descendants, propagates interventions through the DAG, and records query-count artifacts for fidelity/efficiency scoring.
- Implemented two semi-synthetic tabular settings modeled after the paper's Heart-Disease and Performance experiments.
- Added a Heart-Disease subgroup-unlearning setting that tests whether mediated BMI influence differs for age > 50 versus age <= 50 while direct-only subgroup effects remain small.
- Implemented a direct permutation baseline that fails to detect influence from omitted target features.
- Implemented `scripts/reproduce.sh` and `scripts/evaluate.sh`; evaluation reads artifacts only and does not import from `method/`.
- Removed automatic evaluation from `scripts/method.sh` so fresh method artifacts are not mixed with stale baseline artifacts.

## Results

- Current generated scores are stale after replacing the CAFÉ estimator on 2026-05-31 16:12. A clean CPU test job is being submitted to regenerate `outputs/` and `scoring/scores.json`.
- Completed containerized CPU reproduction job `ae348bd1-9a4` with exit code 0.
- `python validate.py --compare` passes: `reference.json` and `scores.json` validate, evaluation remains separated from `method/`, and no committed code references `shared/`.
- Heart-Disease feature-unlearning: CAFÉ ranked the omitted target feature `smoking` 1st with `rank_score=1.0`, `indirect_detected=1.0`, and `direct_unlearned=1.0`; direct permutation ranked it 5th with `rank_score=0.0`.
- Performance feature-unlearning: CAFÉ ranked the omitted target feature `gender` 2nd with `rank_score=0.6666666667`, `indirect_detected=1.0`, and `direct_unlearned=1.0`; direct permutation ranked it 4th with `rank_score=0.0`.
- Job `d51d701a-975` regenerated all artifacts but failed final validation because `scores.json` included two diagnostic fields not declared in `reference.json`. The evaluator now omits those diagnostics from the scoring contract while keeping the underlying method artifacts in `outputs/`.
- Re-running `scripts/evaluate.sh outputs && python validate.py --compare` on the generated artifacts passes locally after the schema fix. A CPU test job is being resubmitted to verify the full clean reproduction path in the scheduler container.
- CPU test job `416d8c69-a53` completed with exit code 0. The scheduler-provided absolute log paths were not visible inside this shell, but the regenerated artifacts are present and `python validate.py --compare` passes on the final workspace.
- Heart-Disease subgroup-unlearning: CAFÉ detects a mediated subgroup gap (`indirect_gap_detected=1.0`, `indirect_gap=0.2205`) while the direct-only baseline reports no mediated gap (`indirect_gap_detected=0.0`); the direct-gap constraint remains satisfied for both methods.

## Remaining

- Verify the patched expected-contrast CAFÉ estimator in the scheduler container and inspect the regenerated scores.
- No further job is pending. The packaged environment now covers the core claim on two semi-synthetic settings and one secondary subgroup-unlearning setting.
- Higher milestones would require expanding beyond the accessible semi-synthetic reproduction, for example by reconstructing additional paper datasets, adding graph-misspecification sensitivity runs, or recovering the paper's open-source prototype if it becomes available.
- Current audit found no reason to rewrite the environment; the existing `setup.sh` installs only Python dependencies and `container.def` is a reasonable CPU base.

## Issues

- A code audit found that the previous CAFÉ path was too close to coefficient attribution. This has been replaced, and the milestone is temporarily downgraded pending a fresh end-to-end job.
- The paper markdown does not include concrete training hyperparameters or a repository URL despite mentioning an open-sourced prototype.
- Most reported values for the core ranking experiments are qualitative or figure-based; `reference.json` encodes the paper-supported rank/detection claims rather than copying unreported bar heights.
- The scheduler-provided absolute stdout/stderr paths for jobs `ae348bd1-9a4` and `416d8c69-a53` were not visible inside this container, but both reported exit code 0 and the expected output artifacts were present in the workspace.
- Local login-node smoke execution could not run because the host Python environment lacks `numpy`; dependency installation remains in `environment/setup.sh`, and execution is being tested through the scheduler container.

## Deviations from Paper

- The paper's exact semi-synthetic structural equations were not provided. I recreated semi-synthetic datasets with the same causal roles and evaluation phenomenon: the target feature is omitted from the audited model but retains mediated influence through downstream variables.
- The paper evaluates additional real-world datasets and architectures. This first reproduction focuses on the two semi-synthetic settings needed for the core claim.
