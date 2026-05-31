# Reproduction Milestones

**Current: core_claim_plus**

## Progress Log

### [2026-05-31 16:12] - none
- Audited the existing scaffold and found that the previous CAFÉ estimator used adjusted regression coefficients rather than the paper's expected-prediction contrast.
- Replaced the CAFÉ path with a backdoor/mediator-conditioned expected prediction contrast estimator and submitted a fresh CPU job to verify it end-to-end.

### [2026-05-31 16:16] - core_claim_plus
- CPU job `8970ea62-4e7` completed successfully with the patched CAFÉ estimator.
- Reproduced the core claim on Heart-Disease and Performance feature-unlearning settings: CAFÉ detected mediated residual influence while direct permutation ranked the omitted target feature last.
- The secondary subgroup experiment regressed after the estimator fix, so the Heart-Disease generator and scale-aware subgroup constraint were patched and another CPU job is being submitted.

## Stop Justification
- Not stopped; secondary subgroup verification is pending after a generator fix.
