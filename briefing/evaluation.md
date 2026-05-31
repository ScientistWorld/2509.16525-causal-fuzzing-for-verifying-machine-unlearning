# Evaluation

How success is measured. Describe only the metrics, targets, and evaluation procedure — do NOT describe the paper's method or how they achieved these results. Think of this as a general evaluation protocal for other scientists trying to solve the same problem, where they should not see this paper's solution.

## Metrics

- `target_rank`: rank of the unlearned target feature by residual influence; lower is better.
- `rank_score`: normalized rank quality, where 1 means the target is ranked first and 0 means last; higher is better.
- `indirect_detected`: binary indicator that the verifier found substantial mediated residual influence; higher is better.
- `direct_unlearned`: binary indicator that the direct effect is near zero after direct feature removal; higher is better.

## Baselines and Targets

The main baseline is direct permutation importance, representative of direct-only attribution checks. The target behavior is that direct-only checks rank the removed feature last or near-last, while a successful verifier still detects residual mediated influence. The paper reports this most explicitly for the semi-synthetic Heart-Disease setting: smoking is ranked first by the proposed verifier and ground truth, while conventional methods rank it second-last or lower.

## Evaluation Protocol

Run `scripts/reproduce.sh` to generate the semi-synthetic tabular datasets, train black-box random-forest predictors with the target feature omitted, run the direct-only baseline and proposed verifier, and write comparable artifacts under `outputs/`. Then run `scripts/evaluate.sh outputs`; evaluation reads only those artifacts and writes `scoring/scores.json`.
