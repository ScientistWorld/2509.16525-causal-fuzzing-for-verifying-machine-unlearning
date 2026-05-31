# Reproduction Milestones

**Current: core_claim_plus**

## Progress Log

### [2026-05-31 00:00] - none
- Read the paper markdown and identified CAFÉ as the core algorithm: black-box causal effect estimation with total/direct/indirect decomposition.
- Implemented the initial semi-synthetic data generators, CAFÉ estimator, direct permutation baseline, and artifact-only evaluator.

### [2026-05-31 00:00] - none
- Audited the existing workspace: implementation contains the CAFÉ computational steps, evaluation is separated from `method/`, and `validate.py --reference-only` passes.
- No official `scoring/scores.json` exists yet, so the next step is a CPU test job running `scripts/reproduce.sh` and `validate.py --compare`.

### [2026-05-31 15:52] - method_runs
- Completed job `ae348bd1-9a4` with exit code 0.
- `scripts/reproduce.sh` ran the direct-permutation baseline, CAFÉ estimator, artifact-only evaluator, and `validate.py --compare` without errors.

### [2026-05-31 15:52] - core_claim
- On the semi-synthetic Heart-Disease setting, CAFÉ ranked the omitted target feature first by indirect residual influence while the direct-permutation baseline ranked it last.
- The run measured both benefit and constraint sides of the claim: indirect influence was detected, and the direct effect remained near zero after feature removal.

### [2026-05-31 15:52] - core_claim_plus
- The same feature-unlearning verification behavior was reproduced on the additional Performance setting.
- Both reproduced experiments match the reference rank and detection claims encoded from the paper.

## Stop Justification
- Stopped at `core_claim_plus`: the core CAFÉ claim is reproduced on two accessible semi-synthetic settings and the reusable environment is packaged. Higher milestones would require reconstructing additional paper experiments whose exact data-generating equations and prototype repository were not available in the paper artifact.
