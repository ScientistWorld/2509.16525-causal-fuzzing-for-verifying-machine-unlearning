# Problem Definition

## Research Question

How can a deployed black-box tabular ML model be audited to determine whether a specified feature or feature-subgroup target still influences predictions after unlearning?

## Why It Matters

Unlearning claims are difficult to verify when the removed signal can still affect predictions through correlated or downstream variables. A useful verifier should detect residual influence without requiring model weights, gradients, or training logs.

## Success Criteria

An effective verifier should identify target features with residual influence, separate direct influence from mediated influence, work with prediction-only access, and expose cases where direct-only attribution methods incorrectly conclude that unlearning succeeded.
