# Research Direction

## Research Problem
The research problem is black-box verification of machine unlearning for tabular models when a removed feature may still influence predictions indirectly through other variables.

## Core Contribution
The contribution area is causal residual-influence estimation with decomposition into direct and mediated effects. Improvements should make this kind of verifier more accurate, robust, interpretable, or efficient under the same black-box and causal-graph setting.

## Approach Scope
Work should remain within causal or intervention-aware verification of unlearning targets. A scientist may improve adjustment-set selection, effect estimation, subgroup handling, path-specific decomposition, or robustness to imperfect causal graphs.

## Out of Bounds
- Replacing the verifier with ordinary predictive accuracy, fairness-only, or attribution-only scoring that cannot distinguish direct from indirect influence.
- Changing the task into model retraining or unlearning itself rather than verification of a provided unlearned model.
- Using the removed feature inside the audited predictor to make the verification target easier.
