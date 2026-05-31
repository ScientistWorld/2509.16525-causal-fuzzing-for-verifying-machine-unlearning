# Evaluation Targets

## Primary: heart_disease_feature_unlearning
Tests whether a verifier identifies the removed target feature as influential when its effect remains through mediators.
- **Metric**: `rank_score` (higher is better)
- **Constraint metrics**: `direct_unlearned` must stay high, and `indirect_detected` must be high.
- **Run**: `bash scripts/reproduce.sh && bash scripts/evaluate.sh outputs`

## Primary: performance_feature_unlearning
Tests whether the same residual-influence finding appears in a second semi-synthetic feature-unlearning setting.
- **Metric**: `rank_score` (higher is better)
- **Constraint metrics**: `direct_unlearned` must stay high, and `indirect_detected` must be high.
- **Run**: `bash scripts/reproduce.sh && bash scripts/evaluate.sh outputs`
