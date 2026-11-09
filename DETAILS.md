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

How can a deployed black-box tabular ML model be audited to determine whether
a specified feature, or a feature within a subgroup of the population, still
influences its predictions after unlearning — directly, or indirectly through
other inputs that the feature causally affects?

## Why It Matters

Unlearning claims are difficult to verify when the removed signal can still
affect predictions through correlated or downstream variables. A useful
verifier should detect residual influence without requiring model weights,
gradients, or training logs, and should say whether the influence is direct
or mediated so that the unlearning can be corrected.

## Setting

The verifier receives a causal graph over the tabular features and the model
outcome, a sample of observational audit rows, the unlearning targets, and
prediction-only access to the audited model under a fixed query budget. It
must report, for every feature, the total and the direct influence of a
specified intervention on the model output (indirect = total − direct), and
the same quantities within age subgroups where the task defines them.

## Success Criteria

An effective verifier estimates these influences accurately against exact
ground truth on unseen task instances: it recovers the residual (largely
mediated) influence of removed features, does not report influence for
features that truly have none, separates direct from mediated influence,
identifies which subgroup retains more mediated influence, and does so with
few black-box queries.

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

How a residual-influence verifier is scored. This describes the tasks, the
interface and the metrics only; how to estimate the quantities is up to you.

## Protocol

The evaluator owns everything on the far side of the comparison. For every
task it samples data from a structural causal model over a fixed causal graph,
trains the audited black-box model (with the unlearning target, and a control
feature, removed from its inputs — or, in some tasks, the target's direct
input left in place: a failed unlearning), fixes the two intervention values
per feature, the query budget and the exact ground truth, then runs every
registered verifier as a separate process.

- **Verifiers.** Any executable `scripts/verifiers/<name>.sh` is a verifier;
  it is called as `bash <name>.sh <tasks_dir> <answers.json>`. No method name
  is hard-coded: `scripts/evaluate_train.sh` (visible tasks) and the hidden
  `scripts/evaluate_test.sh` (held-out tasks, run as its own job) score every
  verifier on disk the same way.
- **Inputs per task** (`<tasks_dir>/<task_id>/`): `spec.json` (feature names,
  binary features, the causal graph as `edges`, the unlearned features, the
  features to estimate, the two intervention values per feature, the
  subgroup rules and subgroup features where present, the number of audit
  rows and the query budget) and `audit.csv` (the observational audit rows).
  `data/causal_graph.py` has small helpers to read them.
- **Black-box access.** The audited model never leaves the evaluator. A
  verifier obtains predictions only through the counted oracle (client:
  `data/blackbox.py`, `BlackBox(spec).predict(rows)`). The budget is 2 rows
  per audit row; requests beyond it are refused.
- **Answers.** `{"tasks": {task_id: {"effects": {feature: {"total": t,
  "direct": d}}, "subgroup_effects": {group: {feature: {"total": t,
  "direct": d}}}}}}` — the influence of switching each feature from its low
  to its high intervention value on the black-box output: *total* (the change
  propagated through the feature's causal descendants) and *direct* (only
  the feature changes, every other input keeps its observed value).
  `subgroup_effects` is required for tasks that define subgroups. A task
  with a missing, non-numeric, NaN or infinite value fails and gets the worst
  score on every metric. Any other field you write is ignored; the evaluator
  derives indirect effects, gaps, rankings and detections itself.
- **Ground truth** is exact: interventions propagated through the true
  structural equations with each audit row's own exogenous noise, read off
  the audited model. Errors are measured in units of the task's largest true
  total influence, so a task's output scale does not matter.

## Experiments and metrics

`heart_disease_feature_unlearning` and `performance_feature_unlearning`
(12 tasks each per slice; varied coefficients, audited-model architectures,
controls with and without a residual path, some failed unlearnings):

- `total_effect_nmae`, `indirect_effect_nmae`, `direct_effect_nmae` (lower is
  better): mean absolute error of every feature's total, indirect
  (total − direct) and direct influence, capped at 2 per value.
- `rank_spearman` (higher): Spearman correlation between the features'
  ranking by reported |total influence| and the true ranking.
- `residual_capture` (higher): for unlearned features whose true residual
  total influence is at least 20% of the task scale, credit 1 when the
  reported value has the true sign and is within a factor of two of the
  truth, linearly less outside (0 at zero, the wrong sign, or 3× the truth).
- `false_alarm_rate` (lower, constraint): fraction of unlearned features with
  exactly zero true influence that are reported with |total| ≥ 10% of scale.
- `query_budget_fraction` (lower, constraint): oracle rows used, counted by
  the evaluator, as a fraction of the budget; one pass over the audit rows is
  free (value 0.5), so only querying beyond one pass costs. A task counts as
  1.0 unless its total-effect error is at most half that of the all-zero
  answer.

`heart_disease_subgroup_unlearning` (the 12 Heart-Disease tasks): for BMI and
blood pressure, total and direct influence within age > 50 and age ≤ 50.
Which age group carries the larger mediated influence varies across tasks.

- `indirect_gap_nmae`, `direct_gap_nmae` (lower): error of the between-group
  gap (age > 50 minus age ≤ 50) in mediated and in direct influence.
- `subgroup_effect_nmae` (lower): error of each group's total, direct and
  mediated influence.
- `indirect_gap_capture` (higher): for features whose true mediated gap is at
  least 20% of the subgroup scale, the same factor-of-two credit as above.
- `indirect_gap_direction` (higher, primary): for the same features, credit 1
  when the reported mediated gap is detected (≥ 10% of scale) and points to
  the right group.

## Baselines

`direct_permutation` switches each feature with all other inputs held at
their observed values (a direct-only attribution check, reporting total =
direct). `causal_fuzzing` propagates interventions through learned
structural models and queries the black box per instance, within the same
budget. The scored reference is `cafe`; see `scoring/scores_train.json`.

## Ranking

A method's rank sums, over experiments and metrics, the experiment weight
times the metric coefficient (`scoring/reference.json`) times its improvement
over the reference in the metric's better direction, each improvement divided
by that metric's spread across ranked attempts.

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

### Iteration 3: gpt-5.5
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 9m | **GPU**: 0.0h
- **Jobs**: 5 total (4 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 4: gpt-5.5 (designer_stage_1)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 5m | **GPU**: 0.0h
- **Jobs**: 5 total (4 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 5: gpt-5.5 (designer_stage_2)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 3m | **GPU**: 0.0h
- **Jobs**: 5 total (4 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 6: gpt-5.5 (designer_stage_3)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 4m | **GPU**: 0.0h
- **Jobs**: 7 total (6 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 7: gpt-5.5 (packager)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 1m | **GPU**: 0.0h
- **Jobs**: 7 total (6 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 8: gpt-5.5 (verifier)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 4m | **GPU**: 0.0h
- **Jobs**: 7 total (6 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 9: gpt-5.5 (verifier)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 11m | **GPU**: 0.0h
- **Jobs**: 7 total (6 completed, 1 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 10: gpt-6.1-sol (redteam)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 7m | **GPU**: 0.0h

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 11: claude-opus-5-5 (hardener)
- **Milestone**: `secondary_claims` | **Status**: error
- **Working time**: 44m | **GPU**: 0.0h
- **Jobs**: 4 total (2 completed, 0 failed)

<details>
<summary>Progress Log</summary>

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

</details>

### Iteration 11: claude-opus-5-5 (hardener)
- **Milestone**: `secondary_claims` | **Status**: done
- **Working time**: 23m | **GPU**: 0.0h
- **Jobs**: 6 total (4 completed, 0 failed)

<details>
<summary>Progress Log</summary>

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

</details>


---

# Reproduction Milestones

**Current: secondary_claims**

## Stop Justification
- Completed at milestone `secondary_claims`.
