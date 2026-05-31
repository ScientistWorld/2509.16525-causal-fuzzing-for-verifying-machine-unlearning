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
