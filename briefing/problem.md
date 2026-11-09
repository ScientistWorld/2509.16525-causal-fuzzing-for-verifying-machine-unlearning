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
