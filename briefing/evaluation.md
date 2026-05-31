# Evaluation

This file defines how a residual-influence verifier is scored. It describes
only the target behavior and metrics; implementation details belong outside the
problem definition.

## Metrics

- `target_rank`: rank of the unlearned target feature by residual influence; lower is better.
- `rank_score`: normalized rank quality, where 1 means the target is ranked first and 0 means last; higher is better.
- `indirect_detected`: binary indicator that the verifier found substantial mediated residual influence; higher is better.
- `direct_unlearned`: binary indicator that the direct effect is near zero after direct feature removal; higher is better.
- `fuzzing_agreement`: binary indicator that the submitted verifier and an intervention-oracle artifact agree that mediated influence remains; higher is better.
- `query_ratio_vs_fuzzing`: model-query ratio of the intervention oracle over the submitted verifier artifact; higher is better.
- `indirect_gap_detected`: binary indicator that subgroup-specific mediated influence differs across target subpopulations; higher is better.
- `direct_gap_small`: binary indicator that a subgroup result is not explained by a large direct-only subgroup difference; higher is better.

## Baseline And Targets

The main baseline is direct permutation importance, representative of direct-only attribution checks. The target behavior is that direct-only checks rank the removed feature last or near-last, while a successful verifier still detects residual mediated influence. In the Heart-Disease setting, the ground-truth target is that `smoking` retains mediated residual influence even though it is omitted from the audited predictor.

## Evaluation Protocol

Run `scripts/reproduce.sh` to generate the semi-synthetic tabular datasets, train the fixed black-box audited predictors with the target feature omitted, run the direct-only baseline and submitted verifier, and write comparable artifacts under `outputs/`. Then run `scripts/evaluate.sh outputs`; evaluation reads only those artifacts and writes `scoring/scores.json`.
