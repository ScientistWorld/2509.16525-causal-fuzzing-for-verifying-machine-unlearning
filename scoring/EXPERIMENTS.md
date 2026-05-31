# Experiment Overview

## heart_disease_feature_unlearning
Tests whether an audit can identify that a removed health-behavior feature still affects model predictions through other observed health variables. This setting checks whether direct-only verification can give false confidence.
The score also checks agreement with an intervention-oracle artifact while rewarding lower model-query use.

## performance_feature_unlearning
Tests whether residual influence of a removed protected attribute is detectable in a second tabular setting where downstream socioeconomic variables carry mediated signal. This checks that the effect is not specific to one synthetic causal graph.
The score also checks agreement with an intervention-oracle artifact while rewarding lower model-query use.

## heart_disease_subgroup_unlearning
Tests whether an audit can surface that the same health feature has different mediated residual influence in older and younger subgroups even when direct-only subgroup effects remain small.

## graph_misspecification_robustness
Tests whether an audit remains useful when the supplied causal graph is moderately imperfect. The score averages rank-change measurements across the two semi-synthetic datasets and distinguishes mild graph perturbations from severe graph distortion.
