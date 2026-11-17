# Evaluation Targets

Reference values are the scored reference verifier (`cafe`) on the hidden
test slice (`scoring/scores_test.json`); visible-slice values are in
`scoring/scores_train.json`. Run all of them with
`bash scripts/evaluate_train.sh` (visible) — the hidden slice is scored by
`bash scripts/evaluate_test.sh` with no arguments.

## Primary: heart_disease_feature_unlearning (weight 0.30)
Recover the residual influence of the unlearned `smoking` target (and of the
family-history control where it has a residual path) and every feature's
total / direct / mediated influence.
- **Metric**: `rank_spearman` (higher; reference 0.938, direct-only baseline 0.234)
- **Accuracy**: `total_effect_nmae` 0.098, `indirect_effect_nmae` 0.088,
  `direct_effect_nmae` 0.057 (lower; direct-only baseline 0.313 / 0.312 / 0.001)
- **Residual influence**: `residual_capture` 1.0 (baseline 0.012)
- **Constraint metrics**: `false_alarm_rate` must stay 0; `query_budget_fraction`
  0.5 (single pass; per-instance propagation costs up to 1.0).

## Primary: performance_feature_unlearning (weight 0.26)
The same for the unlearned `gender` target (and the region control).
- **Metric**: `rank_spearman` (higher; reference 0.983, baseline 0.542)
- **Accuracy**: `total_effect_nmae` 0.036, `indirect_effect_nmae` 0.050,
  `direct_effect_nmae` 0.052 (baseline 0.293 / 0.293 / 0.001)
- **Residual influence**: `residual_capture` 1.0 (baseline 0.009)
- **Constraint metrics**: `false_alarm_rate` 0; `query_budget_fraction` 0.5.

## Primary: adult_feature_unlearning (weight 0.25)
Real UCI Adult data: verify that an income classifier no longer uses sex,
race and native country; every feature's influence and the verdict per
prohibited attribute.
- **Metric**: `verdict_accuracy` (higher; reference 0.953, direct-only
  baseline 0.515; bound 1.0)
- **Ranking / accuracy**: `rank_spearman` 0.976 (baseline 0.666);
  `total_effect_nmae` 0.037, `indirect_effect_nmae` 0.036,
  `direct_effect_nmae` 0.029 (baseline 0.164 / 0.161 / 0.008)
- **Residual influence**: `residual_capture` 1.0 (baseline 0.036)
- **Constraint metrics**: `false_alarm_rate` 0; `query_budget_fraction` 0.5.

## Secondary: heart_disease_subgroup_unlearning (weight 0.19)
Between-group (age > 50 vs age ≤ 50) differences in the mediated and direct
influence of BMI and blood pressure.
- **Metric**: `indirect_gap_direction` (higher; reference 1.0, baseline 0.0)
- **Accuracy**: `indirect_gap_nmae` 0.194, `subgroup_effect_nmae` 0.206 (lower;
  baseline 0.169 / 0.103), `indirect_gap_capture` 0.673 (higher; baseline 0.0)
- **Constraint metric**: `direct_gap_nmae` 0.256 (lower; baseline 0.005) — the
  disparity must not be attributed to the wrong pathway.

The reference is below the bound on every error metric, on the rank
correlations, on subgroup capture and on the Adult verdict: verifiers at the
same query cost reach total-effect errors of 0.049 / 0.019 (Heart /
Performance), subgroup capture 0.96, an Adult verdict accuracy of 0.972 and
an Adult rank correlation of 0.982.
