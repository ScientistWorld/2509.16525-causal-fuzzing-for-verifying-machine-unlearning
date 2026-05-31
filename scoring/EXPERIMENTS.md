# Experiment Overview

## heart_disease_feature_unlearning
Tests whether an audit can identify that a removed health-behavior feature still affects model predictions through other observed health variables. This is the paper's clearest semi-synthetic demonstration that direct-only verification can give false confidence.

## performance_feature_unlearning
Tests whether residual influence of a removed protected attribute is detectable in a second tabular setting where downstream socioeconomic variables carry mediated signal. This checks that the effect is not specific to one synthetic causal graph.
