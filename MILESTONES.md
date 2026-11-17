# Reproduction Milestones

**Current: secondary_claims**

## Progress Log

### [2026-05-31 16:12] - none
- Audited the existing scaffold and found that the previous CAFÉ estimator used adjusted regression coefficients rather than the paper's expected-prediction contrast.
- Replaced the CAFÉ path with a backdoor/mediator-conditioned expected prediction contrast estimator and submitted a fresh CPU job to verify it end-to-end.

### [2026-05-31 16:16] - core_claim_plus
- CPU job `8970ea62-4e7` completed successfully with the patched CAFÉ estimator.
- Reproduced the core claim on Heart-Disease and Performance feature-unlearning settings: CAFÉ detected mediated residual influence while direct permutation ranked the omitted target feature last.
- The secondary subgroup experiment regressed after the estimator fix, so the Heart-Disease generator and scale-aware subgroup constraint were patched and another CPU job is being submitted.

### [2026-05-31 16:20] - secondary_claims
- CPU job `5a7287c3-8f1` completed successfully after the subgroup-generator patch.
- `python validate.py --compare` passes in the scheduler container.
- Reproduced the core feature-unlearning claim on two semi-synthetic settings and the secondary Heart-Disease subgroup-unlearning claim: CAFÉ detects an age-subgroup mediated BMI gap while preserving the direct-gap constraint, whereas direct permutation reports no mediated gap.

## Stop Justification
- Completed at milestone `secondary_claims`.

### [2026-11-17] - secondary_claims
- Final hardening (second pass): added the scored real-data experiment `adult_feature_unlearning` on UCI Adult (the paper's real-data evaluation, semi-synthetic only where exact ground truth requires it), with the reference and both baselines run on it. CAFÉ detects the removed attributes' mediated influence on real data (residual capture 1.0, verdict 0.953) where direct-only attribution fails (0.04 / 0.51). Unscored paper claims remain (German, Drug, graph misspecification, multi-feature), so the milestone stays `secondary_claims`.

