## cohort all_hardening_runs: reference seed spread = 0.0264
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +0.4409 | [+0.266, +0.624] | 0 |
| variant_cafe_half_rows | +0.3284 | [+0.220, +0.440] | 0 |
| variant_hgb | +0.1936 | [+0.040, +0.343] | 0 |
| shortcut_cafe_zero_direct_gap | +0.1703 | [+0.027, +0.316] | 0 |
| cafe | +0.0000 | - | 0 |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] | 0 |
| cafe_seed11 | -0.0104 | [-0.031, +0.007] | 0 |
| cafe_seed19 | -0.0264 | [-0.052, -0.004] | 0 |
| shortcut_cafe_constant_subgroup | -0.0409 | [-0.233, +0.138] | 0 |
| shortcut_cafe_prior_subgroup | -0.0662 | [-0.277, +0.135] | 0 |
| shortcut_direct_retention_claim | -0.2777 | [-0.290, -0.266] | 0 |
| variant_abduction | -0.3123 | [-0.489, -0.130] | 0 |
| causal_fuzzing | -0.4516 | [-0.665, -0.248] | 0 |
| variant_probe_direct | -0.7194 | [-0.768, -0.671] | 0 |
| variant_no_backdoor | -0.8699 | [-1.132, -0.617] | 0 |
| shortcut_constant_answers | -2.1353 | [-2.486, -1.755] | 0 |
| shortcut_flag_all_unlearned | -3.0364 | [-3.181, -2.864] | 0 |
| direct_permutation | -3.4218 | [-3.607, -3.225] | 0 |
| variant_direct_only | -3.7963 | [-3.954, -3.624] | 0 |
| shortcut_zero_output | -4.2422 | [-4.407, -4.063] | 0 |
| shortcut_rescale_units | -9.6159 | [-9.781, -9.448] | 0 |
| shortcut_drop_features | -12.5723 | - | 24 |
| shortcut_nonfinite_values | -12.5723 | - | 24 |
| shortcut_overbudget_bruteforce | -12.5723 | - | 24 |

## cohort honest_runs: reference seed spread = 0.0509
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +2.3392 | [+1.794, +2.879] | 0 |
| variant_abduction | +1.6223 | [+1.077, +2.166] | 0 |
| variant_hgb | +0.9565 | [+0.569, +1.340] | 0 |
| causal_fuzzing | +0.9443 | [+0.231, +1.648] | 0 |
| variant_cafe_half_rows | +0.1469 | [-0.134, +0.425] | 0 |
| cafe_seed11 | +0.0126 | [-0.066, +0.091] | 0 |
| cafe | +0.0000 | - | 0 |
| cafe_seed19 | -0.0382 | [-0.114, +0.037] | 0 |
| variant_probe_direct | -0.0720 | [-0.270, +0.152] | 0 |
| variant_no_backdoor | -3.6225 | [-4.244, -3.012] | 0 |
| direct_permutation | -6.6369 | [-7.184, -6.101] | 0 |
| variant_direct_only | -8.2822 | [-8.752, -7.789] | 0 |

## each shortcut ranked in a cohort of the honest runs plus that shortcut
| shortcut | rank score vs cafe | paired 95% CI |
|---|---:|---|
| shortcut_cafe_zero_direct_gap | +0.0503 | [-0.315, +0.435] |
| shortcut_cafe_constant_subgroup | +0.0031 | [-0.497, +0.500] |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] |
| shortcut_cafe_prior_subgroup | -0.1652 | [-0.901, +0.502] |
| shortcut_direct_retention_claim | -2.2674 | [-2.366, -2.171] |
| shortcut_constant_answers | -5.9788 | [-6.808, -5.118] |
| shortcut_flag_all_unlearned | -6.5310 | [-6.881, -6.139] |
| shortcut_zero_output | -9.1718 | [-9.643, -8.695] |
| shortcut_rescale_units | -13.5264 | [-13.743, -13.314] |
| shortcut_drop_features | -15.7421 | - |
| shortcut_nonfinite_values | -15.7421 | - |
| shortcut_overbudget_bruteforce | -15.7421 | - |

## raw test metrics
### heart_disease_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0930 | 0.0849 | 0.0554 | 0.9286 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0977 | 0.0895 | 0.0556 | 0.9238 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0927 | 0.0924 | 0.0016 | 0.8429 | 1.0000 | 0.0000 | 0.9966 |
| direct_permutation | 0.3129 | 0.3124 | 0.0011 | 0.2340 | 0.0117 | 0.0000 | 1.0000 |
| shortcut_cafe_constant_subgroup | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_zero_direct_gap | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_constant_answers | 0.3942 | 0.2586 | 0.1697 | 0.7888 | 0.3771 | 0.0000 | 1.0000 |
| shortcut_direct_retention_claim | 0.0979 | 0.2592 | 0.2288 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2360 | 0.2118 | 0.0405 | 0.3324 | 0.6968 | 1.0000 | 0.7500 |
| shortcut_forged_fields | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.6552 | 1.6244 | 0.9381 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.4889 | 0.3124 | 0.1765 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0398 | 0.0399 | 0.0016 | 0.9524 | 1.0000 | 0.0000 | 0.9966 |
| variant_abduction_half | 0.0402 | 0.0392 | 0.0027 | 0.9619 | 1.0000 | 0.0000 | 0.4983 |
| variant_cafe_half_rows | 0.0926 | 0.0791 | 0.0622 | 0.9571 | 1.0000 | 0.0000 | 0.2500 |
| variant_direct_only | 0.3411 | 0.3124 | 0.0568 | -0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_hgb | 0.0633 | 0.0714 | 0.0377 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2304 | 0.1490 | 0.1291 | 0.8571 | 1.0000 | 0.0000 | 0.6250 |
| variant_probe_direct | 0.0892 | 0.0883 | 0.0021 | 0.8810 | 1.0000 | 0.0000 | 0.9983 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae | direct_gap_nmae | subgroup_effect_nmae | indirect_gap_capture |
|---|---:|---:|---:|---:|
| cafe | 0.1944 | 0.2557 | 0.2056 | 0.6729 |
| cafe_seed11 | 0.1919 | 0.2687 | 0.2126 | 0.6583 |
| cafe_seed19 | 0.1947 | 0.2629 | 0.2093 | 0.6419 |
| causal_fuzzing | 0.0461 | 0.0077 | 0.0381 | 0.9585 |
| direct_permutation | 0.1695 | 0.0049 | 0.1029 | 0.0000 |
| shortcut_cafe_constant_subgroup | 0.1762 | 0.1028 | 0.3823 | 0.6003 |
| shortcut_cafe_prior_subgroup | 0.2595 | 0.1028 | 0.2036 | 0.5552 |
| shortcut_cafe_zero_direct_gap | 0.2730 | 0.1028 | 0.2157 | 0.9785 |
| shortcut_constant_answers | 0.1762 | 0.1028 | 0.3823 | 0.6003 |
| shortcut_direct_retention_claim | 0.1944 | 0.2557 | 0.2056 | 0.6729 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_flag_all_unlearned | 0.1944 | 0.2557 | 0.2056 | 0.6729 |
| shortcut_forged_fields | 0.1944 | 0.2557 | 0.2056 | 0.6729 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_rescale_units | 1.0000 | 1.9644 | 1.6667 | 0.0000 |
| shortcut_scores_file_forgery | 0.1944 | 0.2557 | 0.2056 | 0.6729 |
| shortcut_zero_output | 0.1695 | 0.1028 | 0.5625 | 0.0000 |
| variant_abduction | 0.0469 | 0.0077 | 0.0375 | 0.9642 |
| variant_abduction_half | 0.0479 | 0.0095 | 0.0388 | 0.9637 |
| variant_cafe_half_rows | 0.2120 | 0.3350 | 0.2338 | 0.6302 |
| variant_direct_only | 0.1695 | 0.2557 | 0.1955 | 0.0000 |
| variant_hgb | 0.1263 | 0.1531 | 0.1163 | 0.8349 |
| variant_no_backdoor | 0.1698 | 0.2339 | 0.4477 | 0.6227 |
| variant_probe_direct | 0.1944 | 0.0129 | 0.1315 | 0.6729 |

### performance_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0357 | 0.0496 | 0.0527 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0348 | 0.0493 | 0.0517 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0335 | 0.0333 | 0.0011 | 0.9667 | 1.0000 | 0.0000 | 1.0000 |
| direct_permutation | 0.2931 | 0.2930 | 0.0008 | 0.5420 | 0.0088 | 0.0000 | 1.0000 |
| shortcut_cafe_constant_subgroup | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_zero_direct_gap | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_constant_answers | 0.3788 | 0.2243 | 0.1623 | 0.6895 | 0.5637 | 0.0000 | 0.7500 |
| shortcut_direct_retention_claim | 0.0358 | 0.2043 | 0.2147 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2537 | 0.2508 | 0.0308 | 0.3261 | 0.8571 | 1.0000 | 0.6250 |
| shortcut_forged_fields | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.5681 | 1.5816 | 0.9833 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.5494 | 0.2930 | 0.2563 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0182 | 0.0182 | 0.0011 | 0.9750 | 1.0000 | 0.0000 | 1.0000 |
| variant_abduction_half | 0.0187 | 0.0183 | 0.0013 | 0.9917 | 1.0000 | 0.0000 | 0.5000 |
| variant_cafe_half_rows | 0.0424 | 0.0500 | 0.0574 | 0.9750 | 1.0000 | 0.0000 | 0.2500 |
| variant_direct_only | 0.3310 | 0.2930 | 0.0524 | 0.2750 | 0.0001 | 0.0000 | 1.0000 |
| variant_hgb | 0.0348 | 0.0469 | 0.0345 | 0.9667 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2564 | 0.1169 | 0.1925 | 0.5750 | 1.0000 | 0.0000 | 0.7500 |
| variant_probe_direct | 0.0501 | 0.0499 | 0.0010 | 0.9083 | 0.9965 | 0.0000 | 1.0000 |

## per-task paired comparison vs cafe (lower per-task error)
- cafe_seed11: heart total 9/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied
- cafe_seed19: heart total 6/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied
- causal_fuzzing: heart total 5/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- direct_permutation: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- shortcut_cafe_constant_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied
- shortcut_cafe_prior_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied
- shortcut_cafe_zero_direct_gap: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 3/12 better, 0 tied
- shortcut_constant_answers: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied
- shortcut_direct_retention_claim: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_flag_all_unlearned: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_forged_fields: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_rescale_units: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 0 tied
- shortcut_scores_file_forgery: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_zero_output: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- variant_abduction: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- variant_abduction_half: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- variant_cafe_half_rows: heart total 8/12 better, 0 tied; perf total 3/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied
- variant_direct_only: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied
- variant_hgb: heart total 12/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- variant_no_backdoor: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied
- variant_probe_direct: heart total 6/12 better, 0 tied; perf total 4/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied

## train vs test (honest runs)
### heart_disease_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.099/0.098 | 0.089/0.088 | 0.051/0.057 | 0.910/0.938 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.099/0.093 | 0.089/0.085 | 0.050/0.055 | 0.900/0.929 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.100/0.098 | 0.089/0.090 | 0.052/0.056 | 0.910/0.924 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.104/0.093 | 0.104/0.092 | 0.002/0.002 | 0.795/0.843 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| direct_permutation | 0.280/0.313 | 0.280/0.312 | 0.001/0.001 | 0.285/0.234 | 0.011/0.012 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction | 0.042/0.040 | 0.042/0.040 | 0.002/0.002 | 0.981/0.952 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| variant_abduction_half | 0.047/0.040 | 0.045/0.039 | 0.004/0.003 | 0.976/0.962 | 1.000/1.000 | 0.000/0.000 | 0.498/0.498 |
| variant_cafe_half_rows | 0.091/0.093 | 0.074/0.079 | 0.055/0.062 | 0.933/0.957 | 1.000/1.000 | 0.000/0.000 | 0.250/0.250 |
| variant_direct_only | 0.302/0.341 | 0.280/0.312 | 0.051/0.057 | 0.090/-0.000 | 0.004/0.000 | 0.000/0.000 | 1.000/1.000 |
| variant_hgb | 0.054/0.063 | 0.065/0.071 | 0.039/0.038 | 0.924/0.938 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.207/0.230 | 0.134/0.149 | 0.112/0.129 | 0.886/0.857 | 1.000/1.000 | 0.000/0.000 | 0.708/0.625 |
| variant_probe_direct | 0.089/0.089 | 0.089/0.088 | 0.002/0.002 | 0.919/0.881 | 1.000/1.000 | 0.000/0.000 | 0.998/0.998 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae train/test | direct_gap_nmae train/test | subgroup_effect_nmae train/test | indirect_gap_capture train/test |
|---|---|---|---|---|
| cafe | 0.273/0.194 | 0.394/0.256 | 0.249/0.206 | 0.533/0.673 |
| cafe_seed11 | 0.268/0.192 | 0.389/0.269 | 0.246/0.213 | 0.603/0.658 |
| cafe_seed19 | 0.264/0.195 | 0.390/0.263 | 0.248/0.209 | 0.613/0.642 |
| causal_fuzzing | 0.061/0.046 | 0.006/0.008 | 0.063/0.038 | 0.967/0.958 |
| direct_permutation | 0.182/0.169 | 0.006/0.005 | 0.094/0.103 | 0.000/0.000 |
| variant_abduction | 0.065/0.047 | 0.006/0.008 | 0.060/0.037 | 0.952/0.964 |
| variant_abduction_half | 0.074/0.048 | 0.011/0.009 | 0.063/0.039 | 0.927/0.964 |
| variant_cafe_half_rows | 0.285/0.212 | 0.458/0.335 | 0.264/0.234 | 0.545/0.630 |
| variant_direct_only | 0.182/0.169 | 0.394/0.256 | 0.228/0.195 | 0.000/0.000 |
| variant_hgb | 0.147/0.126 | 0.210/0.153 | 0.112/0.116 | 0.826/0.835 |
| variant_no_backdoor | 0.298/0.170 | 0.308/0.234 | 0.457/0.448 | 0.520/0.623 |
| variant_probe_direct | 0.273/0.194 | 0.006/0.013 | 0.135/0.132 | 0.533/0.673 |

### performance_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.037/0.036 | 0.050/0.050 | 0.051/0.052 | 0.958/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.038/0.036 | 0.049/0.050 | 0.051/0.053 | 0.958/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.037/0.035 | 0.050/0.049 | 0.051/0.052 | 0.967/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.041/0.034 | 0.040/0.033 | 0.001/0.001 | 0.942/0.967 | 1.000/1.000 | 0.000/0.000 | 1.000/1.000 |
| direct_permutation | 0.328/0.293 | 0.328/0.293 | 0.001/0.001 | 0.321/0.542 | 0.005/0.009 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction | 0.022/0.018 | 0.022/0.018 | 0.001/0.001 | 0.967/0.975 | 1.000/1.000 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction_half | 0.025/0.019 | 0.024/0.018 | 0.002/0.001 | 0.967/0.992 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_cafe_half_rows | 0.050/0.042 | 0.058/0.050 | 0.064/0.057 | 0.967/0.975 | 1.000/1.000 | 0.000/0.000 | 0.250/0.250 |
| variant_direct_only | 0.372/0.331 | 0.328/0.293 | 0.051/0.052 | 0.042/0.275 | 0.000/0.000 | 0.000/0.000 | 1.000/1.000 |
| variant_hgb | 0.034/0.035 | 0.048/0.047 | 0.035/0.035 | 0.933/0.967 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.264/0.256 | 0.120/0.117 | 0.191/0.192 | 0.508/0.575 | 1.000/1.000 | 0.000/0.000 | 0.667/0.750 |
| variant_probe_direct | 0.050/0.050 | 0.050/0.050 | 0.002/0.001 | 0.958/0.908 | 0.987/0.997 | 0.000/0.000 | 1.000/1.000 |

