# Evaluation Targets

## Primary: heart_disease_feature_unlearning
Tests whether a verifier identifies the removed target feature as influential when its effect remains through mediators.
- **Metric**: `rank_score` (higher is better)
- **Constraint metrics**: `direct_unlearned` must stay high, `indirect_detected` must be high, `fuzzing_agreement` must show the fast estimator agrees with causal fuzzing on residual mediated influence, and `query_ratio_vs_fuzzing` should remain above 1.
- **Run**: `bash scripts/reproduce.sh && bash scripts/evaluate.sh outputs`

## Primary: performance_feature_unlearning
Tests whether the same residual-influence finding appears in a second semi-synthetic feature-unlearning setting.
- **Metric**: `rank_score` (higher is better)
- **Constraint metrics**: `direct_unlearned` must stay high, `indirect_detected` must be high, `fuzzing_agreement` must show the fast estimator agrees with causal fuzzing on residual mediated influence, and `query_ratio_vs_fuzzing` should remain above 1.
- **Run**: `bash scripts/reproduce.sh && bash scripts/evaluate.sh outputs`

## Secondary: heart_disease_subgroup_unlearning
Tests whether a verifier catches subgroup-specific mediated influence for the BMI target in older versus younger Heart-Disease samples.
- **Metric**: `subgroup_residual_score` (higher is better)
- **Constraint metrics**: `direct_gap_small` must stay high so the effect is not explained by a large direct-only subgroup gap relative to the direct-effect scale; `indirect_gap_detected` and `total_gap_detected` should also be high.
- **Run**: `bash scripts/reproduce.sh && bash scripts/evaluate.sh outputs`
