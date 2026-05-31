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
