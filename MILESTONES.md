# Reproduction Milestones

**Current: none**

## Progress Log

### [2026-05-31 00:00] - none
- Read the paper markdown and identified CAFÉ as the core algorithm: black-box causal effect estimation with total/direct/indirect decomposition.
- Implemented the initial semi-synthetic data generators, CAFÉ estimator, direct permutation baseline, and artifact-only evaluator.

### [2026-05-31 00:00] - none
- Audited the existing workspace: implementation contains the CAFÉ computational steps, evaluation is separated from `method/`, and `validate.py --reference-only` passes.
- No official `scoring/scores.json` exists yet, so the next step is a CPU test job running `scripts/reproduce.sh` and `validate.py --compare`.

## Stop Justification
