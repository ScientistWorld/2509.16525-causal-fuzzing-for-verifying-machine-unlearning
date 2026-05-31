# Overview

- **Paper ID:** 2509.16525
- **Title:** Causal Fuzzing for Verifying Machine Unlearning
- **Domain:** Machine unlearning verification / causal inference / tabular ML
- **TL;DR:** The paper verifies whether black-box models still use supposedly unlearned features by measuring direct and mediated causal influence.

## Short Summary

The paper argues that conventional feature-attribution and fairness tests can miss residual influence after unlearning because they focus on direct or associational effects. CAFÉ uses a supplied causal graph to estimate total, direct, and indirect influence of unlearning targets from black-box model predictions. The evaluation spans semi-synthetic and real-world tabular datasets and shows that mediated effects can remain even when the target feature is omitted from the audited model.

## Key Results

- On the Heart-Disease semi-synthetic setting, the paper reports that smoking is the most influential feature under ground truth and CAFÉ, while conventional baselines rank it near the bottom.
- On the Performance setting, standard fairness metrics and direct checks miss substantial mediated influence for gender after direct unlearning.
- Table 3 reports CAFÉ running in roughly 0.026-0.030 seconds across LR, RF, and NN settings, much faster than causal fuzzing and most attribution baselines.

---

# Problem Definition

## Research Question

How can a deployed black-box tabular ML model be audited to determine whether a specified feature or feature-subgroup target still influences predictions after unlearning?

## Why It Matters

Unlearning claims are difficult to verify when the removed signal can still affect predictions through correlated or downstream variables. A useful verifier should detect residual influence without requiring model weights, gradients, or training logs.

## Success Criteria

An effective verifier should identify target features with residual influence, separate direct influence from mediated influence, work with prediction-only access, and expose cases where direct-only attribution methods incorrectly conclude that unlearning succeeded.

---

# Paper's Method

How the paper approaches the problem, i.e. the paper's core contributions.

## Key Contribution

The paper introduces CAFÉ, a black-box unlearning verifier that estimates whether an unlearning target retains direct or indirect causal influence on model predictions.

## Approach

CAFÉ takes a causal graph over tabular features and the model outcome, a target feature or target feature-subgroup set, and black-box predictions from the audited model. For each target feature, it identifies a backdoor adjustment set and the mediators on directed paths to the outcome. It estimates total influence by comparing adjusted expected predictions across target-feature values, estimates direct influence by additionally conditioning on mediators, and reports indirect influence as total minus direct.

The paper also presents a causal-fuzzing oracle that intervenes on target features and propagates changes through structural equations. CAFÉ is the fast estimator that replaces exhaustive intervention propagation with adjusted aggregate effect estimates.

## Main Claims

- Primary: indirect residual influence can remain after direct feature unlearning, and CAFÉ detects it where direct-only attribution methods fail.
- Secondary: direct and indirect decomposition gives actionable information for feature, datapoint, subgroup, and multi-feature unlearning targets.
- Secondary: the approach works across several tabular datasets and model architectures and is much faster than exhaustive causal fuzzing.

---

# Evaluation

How success is measured. Describe only the metrics, targets, and evaluation procedure — do NOT describe the paper's method or how they achieved these results. Think of this as a general evaluation protocol for other scientists trying to solve the same problem, where they should not see this paper's solution.

## Metrics

- `target_rank`: rank of the unlearned target feature by residual influence; lower is better.
- `rank_score`: normalized rank quality, where 1 means the target is ranked first and 0 means last; higher is better.
- `indirect_detected`: binary indicator that the verifier found substantial mediated residual influence; higher is better.
- `direct_unlearned`: binary indicator that the direct effect is near zero after direct feature removal; higher is better.
- `fuzzing_agreement`: binary indicator that the fast verifier and a slower intervention oracle agree that mediated influence remains; higher is better.
- `query_ratio_vs_fuzzing`: model-query ratio of the intervention oracle over the fast verifier; higher is better.
- `indirect_gap_detected`: binary indicator that subgroup-specific mediated influence differs across target subpopulations; higher is better.
- `direct_gap_small`: binary indicator that a subgroup result is not explained by a large direct-only subgroup difference; higher is better.

## Baselines and Targets

The main baseline is direct permutation importance, representative of direct-only attribution checks. The target behavior is that direct-only checks rank the removed feature last or near-last, while a successful verifier still detects residual mediated influence. The paper reports this most explicitly for the semi-synthetic Heart-Disease setting: smoking is ranked first by the proposed verifier and ground truth, while conventional methods rank it second-last or lower.

## Evaluation Protocol

Run `scripts/reproduce.sh` to generate the semi-synthetic tabular datasets, train black-box random-forest predictors with the target feature omitted, run the direct-only baseline and verifier, and write comparable artifacts under `outputs/`. Then run `scripts/evaluate.sh outputs`; evaluation reads only those artifacts and writes `scoring/scores.json`.

---

# Reproduction Log

### Iteration 1: gpt-5.5
- **Milestone**: `none` | **Status**: error
- **Working time**: 15m | **GPU**: 0.0h

<details>
<summary>Progress Log</summary>

<!-- Write your progress here -->

</details>

### Iteration 1: gpt-5.5
- **Milestone**: `none` | **Status**: error
- **Working time**: 30m | **GPU**: 0.0h

### Iteration 1: gpt-5.5
- **Milestone**: `none` | **Status**: error
- **Working time**: 30m | **GPU**: 0.0h

### Iteration 1: gpt-5.5
- **Milestone**: `none` | **Status**: error
- **Working time**: 30m | **GPU**: 0.0h

### Iteration 1: gpt-5.5
- **Milestone**: `core_claim_plus` | **Status**: done
- **Working time**: 8m | **GPU**: 0.0h
- **Jobs**: 1 total (1 completed, 0 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 2: gpt-5.5
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 9m | **GPU**: 0.0h
- **Jobs**: 3 total (2 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>


---

# Reproduction Milestones

**Current: secondary_claims**
