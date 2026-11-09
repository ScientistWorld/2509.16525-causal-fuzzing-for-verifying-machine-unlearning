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
