## cohort all_hardening_runs: reference seed spread = 0.0188
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +0.3130 | [+0.191, +0.439] | 0 |
| variant_hgb | +0.1404 | [+0.017, +0.266] | 0 |
| cafe | +0.0000 | - | 0 |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] | 0 |
| cafe_seed11 | -0.0168 | [-0.038, +0.003] | 0 |
| cafe_seed19 | -0.0188 | [-0.039, -0.002] | 0 |
| shortcut_cafe_prior_subgroup | -0.0281 | [-0.213, +0.146] | 0 |
| shortcut_cafe_constant_subgroup | -0.0495 | [-0.223, +0.121] | 0 |
| shortcut_direct_retention_claim | -0.2640 | [-0.276, -0.253] | 0 |
| variant_abduction | -0.3648 | [-0.489, -0.236] | 0 |
| causal_fuzzing | -0.5260 | [-0.693, -0.355] | 0 |
| variant_no_backdoor | -0.6224 | [-0.780, -0.474] | 0 |
| variant_probe_direct | -0.6302 | [-0.675, -0.585] | 0 |
| shortcut_constant_answers | -0.8496 | [-1.105, -0.591] | 0 |
| shortcut_flag_all_unlearned | -2.6740 | [-2.780, -2.553] | 0 |
| variant_direct_only | -3.0064 | [-3.123, -2.879] | 0 |
| direct_permutation | -3.3233 | [-3.450, -3.189] | 0 |
| shortcut_zero_output | -4.1222 | [-4.235, -4.001] | 0 |
| shortcut_rescale_units | -9.9750 | [-10.089, -9.846] | 0 |
| shortcut_drop_features | -12.0564 | - | 24 |
| shortcut_nonfinite_values | -12.0564 | - | 24 |
| shortcut_overbudget_bruteforce | -12.0564 | - | 24 |

## cohort honest_runs: reference seed spread = 0.0412
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +2.2023 | [+1.655, +2.750] | 0 |
| variant_abduction | +1.4256 | [+0.875, +1.986] | 0 |
| variant_hgb | +0.9282 | [+0.503, +1.353] | 0 |
| causal_fuzzing | +0.6644 | [-0.078, +1.393] | 0 |
| cafe | +0.0000 | - | 0 |
| cafe_seed19 | -0.0265 | [-0.102, +0.062] | 0 |
| variant_probe_direct | -0.0279 | [-0.235, +0.198] | 0 |
| cafe_seed11 | -0.0412 | [-0.135, +0.056] | 0 |
| variant_no_backdoor | -3.4031 | [-3.911, -2.916] | 0 |
| direct_permutation | -6.6379 | [-7.125, -6.162] | 0 |
| variant_direct_only | -7.4769 | [-7.909, -7.055] | 0 |

## each shortcut ranked in a cohort of the honest runs plus that shortcut
| shortcut | rank score vs cafe | paired 95% CI |
|---|---:|---|
| shortcut_cafe_constant_subgroup | +0.1333 | [-0.391, +0.684] |
| shortcut_cafe_prior_subgroup | +0.0288 | [-0.683, +0.681] |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] |
| shortcut_direct_retention_claim | -2.2173 | [-2.312, -2.124] |
| shortcut_constant_answers | -4.5070 | [-5.294, -3.761] |
| shortcut_flag_all_unlearned | -6.1164 | [-6.353, -5.837] |
| shortcut_zero_output | -9.1564 | [-9.574, -8.735] |
| shortcut_rescale_units | -13.2913 | [-13.426, -13.140] |
| shortcut_drop_features | -15.3802 | - |
| shortcut_nonfinite_values | -15.3802 | - |
| shortcut_overbudget_bruteforce | -15.3802 | - |

## raw test metrics
### heart_disease_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0987 | 0.0897 | 0.0559 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0936 | 0.0861 | 0.0566 | 0.9048 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0981 | 0.0901 | 0.0559 | 0.9000 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0977 | 0.0976 | 0.0018 | 0.8048 | 1.0000 | 0.0000 | 0.9966 |
| direct_permutation | 0.3100 | 0.3096 | 0.0010 | 0.2558 | 0.0117 | 0.0000 | 0.9989 |
| shortcut_cafe_constant_subgroup | 0.0987 | 0.0897 | 0.0559 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0987 | 0.0897 | 0.0559 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_constant_answers | 0.3895 | 0.2561 | 0.1667 | 0.7888 | 0.3693 | 0.0000 | 0.0000 |
| shortcut_direct_retention_claim | 0.0987 | 0.2617 | 0.2294 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2377 | 0.2152 | 0.0413 | 0.3083 | 0.6968 | 1.0000 | 0.5000 |
| shortcut_forged_fields | 0.0987 | 0.0897 | 0.0559 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.9414 | 1.5937 | 0.9143 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0987 | 0.0897 | 0.0559 | 0.9143 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.4829 | 0.3096 | 0.1736 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0399 | 0.0399 | 0.0018 | 0.9524 | 1.0000 | 0.0000 | 0.9966 |
| variant_abduction_half | 0.0398 | 0.0392 | 0.0027 | 0.9667 | 1.0000 | 0.0000 | 0.4983 |
| variant_direct_only | 0.3367 | 0.3096 | 0.0559 | 0.0238 | 0.0000 | 0.0000 | 0.5000 |
| variant_hgb | 0.0665 | 0.0722 | 0.0373 | 0.9238 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2218 | 0.1477 | 0.1221 | 0.8810 | 1.0000 | 0.0000 | 0.5000 |
| variant_probe_direct | 0.0888 | 0.0878 | 0.0021 | 0.8952 | 1.0000 | 0.0000 | 0.9983 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae | direct_gap_nmae | subgroup_effect_nmae | indirect_gap_capture |
|---|---:|---:|---:|---:|
| cafe | 0.1733 | 0.2151 | 0.1956 | 0.8405 |
| cafe_seed11 | 0.1775 | 0.2350 | 0.2013 | 0.8193 |
| cafe_seed19 | 0.1708 | 0.2260 | 0.1972 | 0.8183 |
| causal_fuzzing | 0.0475 | 0.0074 | 0.0376 | 0.9538 |
| direct_permutation | 0.1720 | 0.0070 | 0.1031 | 0.0000 |
| shortcut_cafe_constant_subgroup | 0.1273 | 0.0922 | 0.3669 | 0.7304 |
| shortcut_cafe_prior_subgroup | 0.1911 | 0.0922 | 0.1945 | 0.7552 |
| shortcut_constant_answers | 0.1273 | 0.0922 | 0.3669 | 0.7304 |
| shortcut_direct_retention_claim | 0.1733 | 0.2151 | 0.1956 | 0.8405 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_flag_all_unlearned | 0.1733 | 0.2151 | 0.1956 | 0.8405 |
| shortcut_forged_fields | 0.1733 | 0.2151 | 0.1956 | 0.8405 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_rescale_units | 2.0000 | 1.9644 | 1.9851 | 0.0000 |
| shortcut_scores_file_forgery | 0.1733 | 0.2151 | 0.1956 | 0.8405 |
| shortcut_zero_output | 0.1720 | 0.0922 | 0.5519 | 0.0000 |
| variant_abduction | 0.0464 | 0.0074 | 0.0366 | 0.9630 |
| variant_abduction_half | 0.0523 | 0.0087 | 0.0401 | 0.9593 |
| variant_direct_only | 0.1720 | 0.2151 | 0.1843 | 0.0000 |
| variant_hgb | 0.1089 | 0.1268 | 0.1087 | 0.9349 |
| variant_no_backdoor | 0.1850 | 0.1955 | 0.4370 | 0.6618 |
| variant_probe_direct | 0.1609 | 0.0121 | 0.1238 | 0.8405 |

### performance_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0358 | 0.0509 | 0.0523 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0357 | 0.0507 | 0.0527 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0348 | 0.0506 | 0.0520 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0335 | 0.0333 | 0.0011 | 0.9667 | 1.0000 | 0.0000 | 1.0000 |
| direct_permutation | 0.2931 | 0.2930 | 0.0008 | 0.5420 | 0.0088 | 0.0000 | 1.0000 |
| shortcut_cafe_constant_subgroup | 0.0358 | 0.0509 | 0.0523 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0358 | 0.0509 | 0.0523 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_constant_answers | 0.3788 | 0.2243 | 0.1623 | 0.6895 | 0.5637 | 0.0000 | 0.0000 |
| shortcut_direct_retention_claim | 0.0358 | 0.2053 | 0.2146 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2537 | 0.2518 | 0.0307 | 0.3261 | 0.8571 | 1.0000 | 0.5000 |
| shortcut_forged_fields | 0.0358 | 0.0509 | 0.0523 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.8960 | 1.5816 | 0.9833 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0358 | 0.0509 | 0.0523 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.5494 | 0.2930 | 0.2563 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0182 | 0.0182 | 0.0011 | 0.9750 | 1.0000 | 0.0000 | 1.0000 |
| variant_abduction_half | 0.0187 | 0.0183 | 0.0013 | 0.9917 | 1.0000 | 0.0000 | 0.5000 |
| variant_direct_only | 0.3309 | 0.2930 | 0.0523 | 0.2750 | 0.0001 | 0.0000 | 0.5000 |
| variant_hgb | 0.0348 | 0.0469 | 0.0345 | 0.9667 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2564 | 0.1228 | 0.1895 | 0.5750 | 1.0000 | 0.0000 | 0.5000 |
| variant_probe_direct | 0.0501 | 0.0499 | 0.0010 | 0.9083 | 0.9965 | 0.0000 | 1.0000 |

## per-task paired comparison vs cafe (lower per-task error)
- cafe_seed11: heart total 8/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 3/12 better, 0 tied
- cafe_seed19: heart total 6/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied
- causal_fuzzing: heart total 5/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- direct_permutation: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- shortcut_cafe_constant_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 6/12 better, 0 tied
- shortcut_cafe_prior_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 6/12 better, 0 tied
- shortcut_constant_answers: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- shortcut_direct_retention_claim: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_flag_all_unlearned: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_forged_fields: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_rescale_units: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 0 tied
- shortcut_scores_file_forgery: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_zero_output: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- variant_abduction: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- variant_abduction_half: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- variant_direct_only: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- variant_hgb: heart total 12/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 9/12 better, 0 tied
- variant_no_backdoor: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied
- variant_probe_direct: heart total 7/12 better, 0 tied; perf total 4/12 better, 0 tied; subgroup indirect gap 12/12 better, 0 tied

## train vs test (honest runs)
### heart_disease_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.089/0.099 | 0.084/0.090 | 0.045/0.056 | 0.914/0.914 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.092/0.094 | 0.084/0.086 | 0.046/0.057 | 0.905/0.905 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.090/0.098 | 0.083/0.090 | 0.045/0.056 | 0.905/0.900 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.087/0.098 | 0.086/0.098 | 0.002/0.002 | 0.819/0.805 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| direct_permutation | 0.294/0.310 | 0.294/0.310 | 0.001/0.001 | 0.292/0.256 | 0.017/0.012 | 0.000/0.000 | 0.999/0.999 |
| variant_abduction | 0.051/0.040 | 0.049/0.040 | 0.002/0.002 | 0.962/0.952 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| variant_abduction_half | 0.055/0.040 | 0.054/0.039 | 0.004/0.003 | 0.962/0.967 | 1.000/1.000 | 0.000/0.000 | 0.498/0.498 |
| variant_direct_only | 0.312/0.337 | 0.294/0.310 | 0.045/0.056 | 0.057/0.024 | 0.001/0.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.046/0.067 | 0.053/0.072 | 0.036/0.037 | 0.924/0.924 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.185/0.222 | 0.127/0.148 | 0.098/0.122 | 0.905/0.881 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_probe_direct | 0.082/0.089 | 0.082/0.088 | 0.002/0.002 | 0.924/0.895 | 1.000/1.000 | 0.000/0.000 | 0.998/0.998 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae train/test | direct_gap_nmae train/test | subgroup_effect_nmae train/test | indirect_gap_capture train/test |
|---|---|---|---|---|
| cafe | 0.349/0.173 | 0.529/0.215 | 0.279/0.196 | 0.619/0.840 |
| cafe_seed11 | 0.343/0.178 | 0.529/0.235 | 0.274/0.201 | 0.656/0.819 |
| cafe_seed19 | 0.357/0.171 | 0.533/0.226 | 0.278/0.197 | 0.653/0.818 |
| causal_fuzzing | 0.062/0.047 | 0.008/0.007 | 0.070/0.038 | 0.722/0.954 |
| direct_permutation | 0.248/0.172 | 0.005/0.007 | 0.121/0.103 | 0.000/0.000 |
| variant_abduction | 0.063/0.046 | 0.008/0.007 | 0.066/0.037 | 0.781/0.963 |
| variant_abduction_half | 0.075/0.052 | 0.012/0.009 | 0.071/0.040 | 0.748/0.959 |
| variant_direct_only | 0.248/0.172 | 0.529/0.215 | 0.287/0.184 | 0.000/0.000 |
| variant_hgb | 0.144/0.109 | 0.252/0.127 | 0.103/0.109 | 0.833/0.935 |
| variant_no_backdoor | 0.379/0.185 | 0.354/0.195 | 0.431/0.437 | 0.630/0.662 |
| variant_probe_direct | 0.346/0.161 | 0.004/0.012 | 0.162/0.124 | 0.619/0.840 |

### performance_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.038/0.036 | 0.052/0.051 | 0.045/0.052 | 0.933/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.040/0.036 | 0.052/0.051 | 0.042/0.053 | 0.933/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.039/0.035 | 0.054/0.051 | 0.044/0.052 | 0.950/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.048/0.034 | 0.047/0.033 | 0.001/0.001 | 0.933/0.967 | 1.000/1.000 | 0.000/0.000 | 1.000/1.000 |
| direct_permutation | 0.338/0.293 | 0.338/0.293 | 0.001/0.001 | 0.288/0.542 | 0.005/0.009 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction | 0.026/0.018 | 0.025/0.018 | 0.001/0.001 | 0.933/0.975 | 1.000/1.000 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction_half | 0.027/0.019 | 0.027/0.018 | 0.002/0.001 | 0.933/0.992 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_direct_only | 0.379/0.331 | 0.338/0.293 | 0.045/0.052 | 0.000/0.275 | 0.000/0.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.034/0.035 | 0.045/0.047 | 0.033/0.035 | 0.917/0.967 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.252/0.256 | 0.129/0.123 | 0.165/0.189 | 0.567/0.575 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_probe_direct | 0.050/0.050 | 0.049/0.050 | 0.002/0.001 | 0.950/0.908 | 1.000/0.997 | 0.000/0.000 | 1.000/1.000 |

