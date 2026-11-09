# Research Direction

## Research Problem
Black-box verification of machine unlearning for tabular models: deciding
whether a removed feature, globally or within a subgroup, still influences a
deployed model's predictions, directly or through other inputs it causally
affects, using only predictions and a causal graph.

## Core Contribution
Causal residual-influence estimation with a decomposition into direct and
mediated effects. Improvements should make such a verifier more accurate
(total, direct and mediated influence, subgroup differences), more robust
across audited-model architectures and causal mechanisms, or cheaper in
black-box queries at the same accuracy.

## Approach Scope
Work within causal or intervention-aware verification under the given graph
and query budget: better adjustment and mediator handling, better effect or
response estimation, handling of weak overlap between correlated inputs,
subgroup-specific estimation, counterfactual propagation, or more
query-efficient designs.

## Out of Bounds
- Attribution-only or fairness-metric scoring that cannot separate direct
  from mediated influence.
- Retraining or unlearning the model instead of verifying the given one.
- Using knowledge of the task generators, fixed priors or published answer
  patterns in place of measurement.
