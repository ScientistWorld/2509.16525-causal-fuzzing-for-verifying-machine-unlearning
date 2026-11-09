# Experiment Overview

All three experiments score a verifier's reported influences against exact
ground truth on task instances it has not seen (the hidden test draws its own
structural equations, coefficients, audited models and seeds), through a
counted prediction-only oracle with a fixed query budget.

## heart_disease_feature_unlearning
Establishes whether an audit can see that a removed health-behaviour feature
still drives the model's predictions through other observed health variables,
where checks that only look at the model's direct reliance give false
confidence. Accuracy of every feature's total, direct and mediated influence
and of the influence ranking is the benefit side; the constraint side is not
raising alarms for removed features that truly have no influence, not
mis-assigning influence to the direct pathway, and query cost.

## performance_feature_unlearning
The same question for a removed protected attribute whose signal reaches the
model through downstream socioeconomic variables: shows the finding is not
specific to one causal graph. Same benefit and constraint metrics.

## heart_disease_subgroup_unlearning
Establishes whether an audit can tell that the mediated influence of a health
feature differs between older and younger people — and in which direction,
which varies across instances — while not attributing the difference to the
direct pathway. Scored on the between-group gaps, each group's influences,
and whether the gap is detected in the right direction.
