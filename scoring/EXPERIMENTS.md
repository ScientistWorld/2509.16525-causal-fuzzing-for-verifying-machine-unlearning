# Experiment Overview

All four experiments score a verifier's reported influences against exact
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

## adult_feature_unlearning
Establishes whether the audit works on real data: a census income classifier
(several model families) that must no longer use sex, race or national
origin. Built on the real UCI Adult rows, with the residual paths of the
prohibited attributes varied across instances — absent, close to a
regulator's decision threshold, or strong, sometimes partly cancelling.
Scored on the same influence accuracy, ranking, residual-recovery, false-alarm
and query-cost measures, plus the verification verdict itself: whether each
prohibited attribute's residual influence is correctly judged to be above or
below each of several thresholds.
