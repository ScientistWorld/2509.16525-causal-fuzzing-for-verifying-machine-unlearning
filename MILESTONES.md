# Reproduction Milestones

**Current: secondary_claims**

## Progress Log

### [2026-05-31 00:00] - core_claim
- Existing reproduction implements CAFÉ-style causal residual influence scoring on two semi-synthetic feature-unlearning settings.
- Audit found stale scores for newly added fidelity metrics and limited coverage of subgroup-unlearning claims.
- Added a Heart-Disease subgroup-unlearning experiment for age-stratified mediated influence; pending containerized CPU validation before raising the milestone.

### [2026-05-31 00:00] - core_claim
- Job `d51d701a-975` ran the method and baseline artifacts but failed validation due to undeclared diagnostic score fields.
- Fixed the evaluator to keep `scores.json` aligned with `reference.json`; local validation of the generated artifacts now passes.
- Resubmitting a CPU test job to validate the full reproduction script after the fix.

### [2026-05-31 00:00] - secondary_claims
- CPU test job `416d8c69-a53` completed with exit code 0, regenerating method, baseline, and evaluation artifacts.
- Final `python validate.py --compare` passes for the two feature-unlearning experiments and the Heart-Disease subgroup-unlearning experiment.
- The reproduction now supports the core residual-influence claim and a secondary subgroup-unlearning claim; remaining paper coverage would require additional datasets and paper-specific implementation details that were not available in the markdown.
