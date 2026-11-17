## cohort all_hardening_runs: reference seed spread = 0.0360
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +0.2743 | [+0.100, +0.437] | 0 |
| variant_hgb | +0.1398 | [-0.028, +0.292] | 0 |
| shortcut_cafe_zero_direct_gap | +0.1357 | [+0.019, +0.255] | 0 |
| variant_full_adjust | +0.0188 | [-0.023, +0.062] | 0 |
| cafe | +0.0000 | - | 0 |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] | 0 |
| cafe_seed11 | -0.0079 | [-0.026, +0.007] | 0 |
| shortcut_cafe_shrink_unlearned | -0.0226 | [-0.062, +0.007] | 0 |
| cafe_seed19 | -0.0360 | [-0.077, -0.006] | 0 |
| shortcut_cafe_constant_subgroup | -0.1046 | [-0.304, +0.089] | 0 |
| variant_cafe_half_rows | -0.1237 | [-0.271, +0.007] | 0 |
| shortcut_cafe_prior_subgroup | -0.1248 | [-0.346, +0.082] | 0 |
| shortcut_direct_retention_claim | -0.2686 | [-0.280, -0.257] | 0 |
| shortcut_cafe_assume_unlearned | -0.6896 | [-0.812, -0.538] | 0 |
| variant_abduction | -1.4015 | [-1.572, -1.231] | 0 |
| variant_no_backdoor | -1.5673 | [-1.911, -1.242] | 0 |
| causal_fuzzing | -1.6001 | [-1.818, -1.401] | 0 |
| variant_probe_direct | -1.6773 | [-1.717, -1.641] | 0 |
| shortcut_constant_answers | -4.3387 | [-4.645, -4.008] | 0 |
| shortcut_flag_all_unlearned | -4.5053 | [-4.735, -4.251] | 0 |
| variant_direct_only | -4.8230 | [-4.957, -4.681] | 0 |
| direct_permutation | -5.0173 | [-5.168, -4.861] | 0 |
| shortcut_zero_output | -6.0483 | [-6.180, -5.906] | 0 |
| shortcut_rescale_units | -11.6746 | [-11.804, -11.539] | 0 |
| shortcut_drop_features | -15.3974 | - | 48 |
| shortcut_nonfinite_values | -15.3974 | - | 48 |
| shortcut_overbudget_bruteforce | -15.3974 | - | 48 |

## cohort honest_runs: reference seed spread = 0.0700
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +1.6524 | [+1.196, +2.106] | 0 |
| variant_hgb | +0.8365 | [+0.490, +1.179] | 0 |
| variant_full_adjust | +0.3031 | [+0.161, +0.450] | 0 |
| variant_abduction | +0.0347 | [-0.423, +0.483] | 0 |
| cafe_seed11 | +0.0152 | [-0.050, +0.074] | 0 |
| cafe | +0.0000 | - | 0 |
| cafe_seed19 | -0.0547 | [-0.152, +0.023] | 0 |
| causal_fuzzing | -1.1344 | [-1.806, -0.502] | 0 |
| variant_cafe_half_rows | -1.1523 | [-2.803, -0.144] | 0 |
| variant_probe_direct | -1.1900 | [-1.355, -1.017] | 0 |
| variant_no_backdoor | -5.3569 | [-6.021, -4.738] | 0 |
| direct_permutation | -9.4151 | [-9.864, -8.928] | 0 |
| variant_direct_only | -10.2542 | [-10.688, -9.810] | 0 |

## each shortcut ranked in a cohort of the honest runs plus that shortcut
| shortcut | rank score vs cafe | paired 95% CI |
|---|---:|---|
| shortcut_cafe_zero_direct_gap | +0.0390 | [-0.269, +0.349] |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] |
| shortcut_cafe_shrink_unlearned | -0.0252 | [-0.131, +0.061] |
| shortcut_cafe_constant_subgroup | -0.0868 | [-0.512, +0.379] |
| shortcut_cafe_prior_subgroup | -0.2160 | [-0.820, +0.369] |
| shortcut_cafe_assume_unlearned | -1.3426 | [-1.618, -1.029] |
| shortcut_direct_retention_claim | -2.4612 | [-2.580, -2.338] |
| shortcut_flag_all_unlearned | -9.6161 | [-10.041, -9.143] |
| shortcut_constant_answers | -9.6484 | [-10.355, -8.921] |
| shortcut_zero_output | -12.2150 | [-12.589, -11.812] |
| shortcut_rescale_units | -15.9694 | [-16.137, -15.799] |
| shortcut_drop_features | -18.9324 | - |
| shortcut_nonfinite_values | -18.9324 | - |
| shortcut_overbudget_bruteforce | -18.9324 | - |

## raw test metrics
### adult_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | verdict_accuracy | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| cafe_seed11 | 0.0369 | 0.0349 | 0.0292 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| cafe_seed19 | 0.0365 | 0.0356 | 0.0294 | 0.9783 | 1.0000 | 0.0000 | 0.9792 | 0.5000 |
| causal_fuzzing | 0.0991 | 0.0966 | 0.0125 | 0.9436 | 0.9738 | 0.0000 | 0.9375 | 0.9978 |
| direct_permutation | 0.1644 | 0.1609 | 0.0079 | 0.6664 | 0.0361 | 0.0000 | 0.5222 | 0.9977 |
| shortcut_cafe_assume_unlearned | 0.0673 | 0.0656 | 0.0289 | 0.8806 | 0.5854 | 0.0000 | 0.7667 | 0.5000 |
| shortcut_cafe_constant_subgroup | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_cafe_shrink_unlearned | 0.0377 | 0.0360 | 0.0291 | 0.9800 | 1.0000 | 0.0000 | 0.9667 | 0.5000 |
| shortcut_cafe_zero_direct_gap | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_constant_answers | 1.1500 | 0.3213 | 0.9543 | 0.4539 | 0.0000 | 0.0000 | 0.7667 | 1.0000 |
| shortcut_direct_retention_claim | 0.0373 | 0.1236 | 0.1282 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2723 | 0.2717 | 0.0283 | 0.3348 | 0.6313 | 1.0000 | 0.5000 | 0.9375 |
| shortcut_forged_fields | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_rescale_units | 1.9923 | 1.7339 | 1.7548 | 0.9762 | 0.0000 | 1.0000 | 0.5000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0373 | 0.0356 | 0.0294 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_zero_output | 0.4184 | 0.1609 | 0.2632 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 1.0000 |
| variant_abduction | 0.0376 | 0.0335 | 0.0125 | 0.9752 | 1.0000 | 0.0000 | 0.9889 | 0.9977 |
| variant_abduction_half | 0.0440 | 0.0348 | 0.0180 | 0.9689 | 1.0000 | 0.0000 | 0.9583 | 0.5000 |
| variant_cafe_half_rows | 0.0498 | 0.0488 | 0.0373 | 0.9505 | 1.0000 | 0.0714 | 0.9583 | 0.5000 |
| variant_direct_only | 0.1723 | 0.1609 | 0.0294 | 0.6925 | 0.0085 | 0.0000 | 0.5000 | 0.5000 |
| variant_full_adjust | 0.0341 | 0.0326 | 0.0280 | 0.9731 | 1.0000 | 0.0000 | 0.9778 | 0.5000 |
| variant_hgb | 0.0305 | 0.0284 | 0.0130 | 0.9818 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| variant_no_backdoor | 0.2388 | 0.0645 | 0.1875 | 0.6674 | 1.0000 | 0.0000 | 1.0000 | 0.9167 |
| variant_probe_direct | 0.0394 | 0.0356 | 0.0132 | 0.9710 | 1.0000 | 0.0000 | 1.0000 | 0.9989 |

### heart_disease_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0930 | 0.0849 | 0.0554 | 0.9286 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0977 | 0.0895 | 0.0556 | 0.9238 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0927 | 0.0924 | 0.0016 | 0.8429 | 1.0000 | 0.0000 | 0.9966 |
| direct_permutation | 0.3129 | 0.3124 | 0.0011 | 0.2340 | 0.0117 | 0.0000 | 1.0000 |
| shortcut_cafe_assume_unlearned | 0.1205 | 0.0963 | 0.0405 | 0.9238 | 0.6667 | 0.0000 | 0.5000 |
| shortcut_cafe_constant_subgroup | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0979 | 0.0883 | 0.0568 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_shrink_unlearned | 0.0969 | 0.0875 | 0.0565 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
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
| variant_abduction | 0.0477 | 0.0476 | 0.0016 | 0.9238 | 1.0000 | 0.0000 | 0.9966 |
| variant_abduction_half | 0.0487 | 0.0483 | 0.0027 | 0.9429 | 1.0000 | 0.0000 | 0.5000 |
| variant_cafe_half_rows | 0.0926 | 0.0791 | 0.0622 | 0.9571 | 1.0000 | 0.0000 | 0.5000 |
| variant_direct_only | 0.3411 | 0.3124 | 0.0568 | -0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_full_adjust | 0.0862 | 0.0628 | 0.0406 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| variant_hgb | 0.0633 | 0.0714 | 0.0377 | 0.9381 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2304 | 0.1490 | 0.1291 | 0.8571 | 1.0000 | 0.0000 | 0.6250 |
| variant_probe_direct | 0.0892 | 0.0883 | 0.0021 | 0.8810 | 1.0000 | 0.0000 | 0.9983 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae | direct_gap_nmae | subgroup_effect_nmae | indirect_gap_capture | indirect_gap_direction |
|---|---:|---:|---:|---:|---:|
| cafe | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| cafe_seed11 | 0.1919 | 0.2687 | 0.2126 | 0.6583 | 1.0000 |
| cafe_seed19 | 0.1947 | 0.2629 | 0.2093 | 0.6419 | 1.0000 |
| causal_fuzzing | 0.0461 | 0.0077 | 0.0381 | 0.9585 | 0.9000 |
| direct_permutation | 0.1695 | 0.0049 | 0.1029 | 0.0000 | 0.0000 |
| shortcut_cafe_assume_unlearned | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_cafe_constant_subgroup | 0.1762 | 0.1028 | 0.3823 | 0.6003 | 0.7000 |
| shortcut_cafe_prior_subgroup | 0.2595 | 0.1028 | 0.2036 | 0.5552 | 0.7000 |
| shortcut_cafe_shrink_unlearned | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_cafe_zero_direct_gap | 0.2730 | 0.1028 | 0.2157 | 0.9785 | 1.0000 |
| shortcut_constant_answers | 0.1762 | 0.1028 | 0.3823 | 0.6003 | 0.7000 |
| shortcut_direct_retention_claim | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | 0.0000 | 0.0000 |
| shortcut_flag_all_unlearned | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_forged_fields | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | 0.0000 | 0.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | 0.0000 | 0.0000 |
| shortcut_rescale_units | 1.0000 | 1.9644 | 1.6667 | 0.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.1944 | 0.2557 | 0.2056 | 0.6729 | 1.0000 |
| shortcut_zero_output | 0.1695 | 0.1028 | 0.5625 | 0.0000 | 0.0000 |
| variant_abduction | 0.0469 | 0.0077 | 0.0375 | 0.9642 | 0.9000 |
| variant_abduction_half | 0.0479 | 0.0095 | 0.0388 | 0.9637 | 0.9000 |
| variant_cafe_half_rows | 0.2120 | 0.3350 | 0.2338 | 0.6302 | 1.0000 |
| variant_direct_only | 0.1695 | 0.2557 | 0.1955 | 0.0000 | 0.0000 |
| variant_full_adjust | 0.1955 | 0.2558 | 0.2055 | 0.6731 | 1.0000 |
| variant_hgb | 0.1263 | 0.1531 | 0.1163 | 0.8349 | 0.9000 |
| variant_no_backdoor | 0.1698 | 0.2339 | 0.4477 | 0.6227 | 0.9000 |
| variant_probe_direct | 0.1944 | 0.0129 | 0.1315 | 0.6729 | 1.0000 |

### performance_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0357 | 0.0496 | 0.0527 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0348 | 0.0493 | 0.0517 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0335 | 0.0333 | 0.0011 | 0.9667 | 1.0000 | 0.0000 | 1.0000 |
| direct_permutation | 0.2931 | 0.2930 | 0.0008 | 0.5420 | 0.0088 | 0.0000 | 1.0000 |
| shortcut_cafe_assume_unlearned | 0.0474 | 0.0438 | 0.0308 | 0.9833 | 0.8571 | 0.0000 | 0.5000 |
| shortcut_cafe_constant_subgroup | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_shrink_unlearned | 0.0367 | 0.0489 | 0.0471 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_cafe_zero_direct_gap | 0.0358 | 0.0499 | 0.0524 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| shortcut_constant_answers | 0.3788 | 0.2243 | 0.1623 | 0.6895 | 0.5637 | 0.0000 | 0.8750 |
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
| variant_cafe_half_rows | 0.0424 | 0.0500 | 0.0574 | 0.9750 | 1.0000 | 0.0000 | 0.5000 |
| variant_direct_only | 0.3310 | 0.2930 | 0.0524 | 0.2750 | 0.0001 | 0.0000 | 1.0000 |
| variant_full_adjust | 0.0338 | 0.0297 | 0.0308 | 0.9833 | 1.0000 | 0.0000 | 0.5000 |
| variant_hgb | 0.0348 | 0.0469 | 0.0345 | 0.9667 | 1.0000 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2564 | 0.1169 | 0.1925 | 0.5750 | 1.0000 | 0.0000 | 0.7500 |
| variant_probe_direct | 0.0501 | 0.0499 | 0.0010 | 0.9083 | 0.9965 | 0.0000 | 1.0000 |

## per-task paired comparison vs cafe (lower per-task error)
- cafe_seed11: heart total 9/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied; adult total 11/24 better, 0 tied
- cafe_seed19: heart total 6/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 15/24 better, 0 tied
- causal_fuzzing: heart total 5/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 5/24 better, 0 tied
- direct_permutation: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_cafe_assume_unlearned: heart total 6/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 4/24 better, 0 tied
- shortcut_cafe_constant_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_cafe_prior_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_cafe_shrink_unlearned: heart total 6/12 better, 6 tied; perf total 6/12 better, 4 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 13/24 better, 2 tied
- shortcut_cafe_zero_direct_gap: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 3/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_constant_answers: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_direct_retention_claim: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_flag_all_unlearned: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 0 tied
- shortcut_forged_fields: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_rescale_units: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_scores_file_forgery: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_zero_output: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_abduction: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 16/24 better, 0 tied
- variant_abduction_half: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 9/24 better, 0 tied
- variant_cafe_half_rows: heart total 8/12 better, 0 tied; perf total 3/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied; adult total 7/24 better, 0 tied
- variant_direct_only: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_full_adjust: heart total 9/12 better, 0 tied; perf total 9/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied; adult total 18/24 better, 0 tied
- variant_hgb: heart total 12/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 20/24 better, 0 tied
- variant_no_backdoor: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_probe_direct: heart total 6/12 better, 0 tied; perf total 4/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 10/24 better, 0 tied

## train vs test (honest runs)
### adult_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | verdict_accuracy train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|---|
| cafe | 0.034/0.037 | 0.033/0.036 | 0.026/0.029 | 0.972/0.976 | 1.000/1.000 | 0.000/0.000 | 0.859/1.000 | 0.500/0.500 |
| cafe_seed11 | 0.035/0.037 | 0.033/0.035 | 0.026/0.029 | 0.973/0.976 | 1.000/1.000 | 0.000/0.000 | 0.870/1.000 | 0.500/0.500 |
| cafe_seed19 | 0.035/0.037 | 0.034/0.036 | 0.026/0.029 | 0.970/0.978 | 1.000/1.000 | 0.000/0.000 | 0.859/0.979 | 0.500/0.500 |
| causal_fuzzing | 0.090/0.099 | 0.090/0.097 | 0.012/0.013 | 0.953/0.944 | 0.983/0.974 | 0.083/0.000 | 0.870/0.938 | 0.998/0.998 |
| direct_permutation | 0.171/0.164 | 0.169/0.161 | 0.008/0.008 | 0.704/0.666 | 0.034/0.036 | 0.000/0.000 | 0.533/0.522 | 0.998/0.998 |
| variant_abduction | 0.036/0.038 | 0.029/0.034 | 0.012/0.013 | 0.974/0.975 | 1.000/1.000 | 0.000/0.000 | 0.946/0.989 | 0.998/0.998 |
| variant_abduction_half | 0.040/0.044 | 0.031/0.035 | 0.019/0.018 | 0.962/0.969 | 1.000/1.000 | 0.000/0.000 | 0.902/0.958 | 0.500/0.500 |
| variant_cafe_half_rows | 0.052/0.050 | 0.048/0.049 | 0.033/0.037 | 0.959/0.950 | 1.000/1.000 | 0.000/0.071 | 0.859/0.958 | 0.500/0.500 |
| variant_direct_only | 0.174/0.172 | 0.169/0.161 | 0.026/0.029 | 0.747/0.692 | 0.011/0.009 | 0.000/0.000 | 0.500/0.500 | 0.500/0.500 |
| variant_full_adjust | 0.030/0.034 | 0.031/0.033 | 0.025/0.028 | 0.971/0.973 | 1.000/1.000 | 0.000/0.000 | 0.913/0.978 | 0.500/0.500 |
| variant_hgb | 0.027/0.030 | 0.026/0.028 | 0.012/0.013 | 0.974/0.982 | 1.000/1.000 | 0.000/0.000 | 0.859/1.000 | 0.500/0.500 |
| variant_no_backdoor | 0.233/0.239 | 0.063/0.065 | 0.184/0.187 | 0.645/0.667 | 1.000/1.000 | 0.000/0.000 | 0.859/1.000 | 0.854/0.917 |
| variant_probe_direct | 0.037/0.039 | 0.033/0.036 | 0.011/0.013 | 0.968/0.971 | 1.000/1.000 | 0.000/0.000 | 0.880/1.000 | 0.999/0.999 |

### heart_disease_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.099/0.098 | 0.089/0.088 | 0.051/0.057 | 0.910/0.938 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.099/0.093 | 0.089/0.085 | 0.050/0.055 | 0.900/0.929 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.100/0.098 | 0.089/0.090 | 0.052/0.056 | 0.910/0.924 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.104/0.093 | 0.104/0.092 | 0.002/0.002 | 0.795/0.843 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| direct_permutation | 0.280/0.313 | 0.280/0.312 | 0.001/0.001 | 0.285/0.234 | 0.011/0.012 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction | 0.057/0.048 | 0.058/0.048 | 0.002/0.002 | 0.948/0.924 | 1.000/1.000 | 0.000/0.000 | 0.997/0.997 |
| variant_abduction_half | 0.061/0.049 | 0.059/0.048 | 0.004/0.003 | 0.943/0.943 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_cafe_half_rows | 0.091/0.093 | 0.074/0.079 | 0.055/0.062 | 0.933/0.957 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_direct_only | 0.302/0.341 | 0.280/0.312 | 0.051/0.057 | 0.090/-0.000 | 0.004/0.000 | 0.000/0.000 | 1.000/1.000 |
| variant_full_adjust | 0.090/0.086 | 0.067/0.063 | 0.036/0.041 | 0.938/0.938 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.054/0.063 | 0.065/0.071 | 0.039/0.038 | 0.924/0.938 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.207/0.230 | 0.134/0.149 | 0.112/0.129 | 0.886/0.857 | 1.000/1.000 | 0.000/0.000 | 0.708/0.625 |
| variant_probe_direct | 0.089/0.089 | 0.089/0.088 | 0.002/0.002 | 0.919/0.881 | 1.000/1.000 | 0.000/0.000 | 0.998/0.998 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae train/test | direct_gap_nmae train/test | subgroup_effect_nmae train/test | indirect_gap_capture train/test | indirect_gap_direction train/test |
|---|---|---|---|---|---|
| cafe | 0.273/0.194 | 0.394/0.256 | 0.249/0.206 | 0.533/0.673 | 0.900/1.000 |
| cafe_seed11 | 0.268/0.192 | 0.389/0.269 | 0.246/0.213 | 0.603/0.658 | 1.000/1.000 |
| cafe_seed19 | 0.264/0.195 | 0.390/0.263 | 0.248/0.209 | 0.613/0.642 | 1.000/1.000 |
| causal_fuzzing | 0.061/0.046 | 0.006/0.008 | 0.063/0.038 | 0.967/0.958 | 1.000/0.900 |
| direct_permutation | 0.182/0.169 | 0.006/0.005 | 0.094/0.103 | 0.000/0.000 | 0.000/0.000 |
| variant_abduction | 0.065/0.047 | 0.006/0.008 | 0.060/0.037 | 0.952/0.964 | 1.000/0.900 |
| variant_abduction_half | 0.074/0.048 | 0.011/0.009 | 0.063/0.039 | 0.927/0.964 | 1.000/0.900 |
| variant_cafe_half_rows | 0.285/0.212 | 0.458/0.335 | 0.264/0.234 | 0.545/0.630 | 0.900/1.000 |
| variant_direct_only | 0.182/0.169 | 0.394/0.256 | 0.228/0.195 | 0.000/0.000 | 0.000/0.000 |
| variant_full_adjust | 0.275/0.196 | 0.394/0.256 | 0.250/0.205 | 0.532/0.673 | 0.900/1.000 |
| variant_hgb | 0.147/0.126 | 0.210/0.153 | 0.112/0.116 | 0.826/0.835 | 0.900/0.900 |
| variant_no_backdoor | 0.298/0.170 | 0.308/0.234 | 0.457/0.448 | 0.520/0.623 | 1.000/0.900 |
| variant_probe_direct | 0.273/0.194 | 0.006/0.013 | 0.135/0.132 | 0.533/0.673 | 0.900/1.000 |

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
| variant_cafe_half_rows | 0.050/0.042 | 0.058/0.050 | 0.064/0.057 | 0.967/0.975 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_direct_only | 0.372/0.331 | 0.328/0.293 | 0.051/0.052 | 0.042/0.275 | 0.000/0.000 | 0.000/0.000 | 1.000/1.000 |
| variant_full_adjust | 0.039/0.034 | 0.033/0.030 | 0.030/0.031 | 0.967/0.983 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.034/0.035 | 0.048/0.047 | 0.035/0.035 | 0.933/0.967 | 1.000/1.000 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.264/0.256 | 0.120/0.117 | 0.191/0.192 | 0.508/0.575 | 1.000/1.000 | 0.000/0.000 | 0.667/0.750 |
| variant_probe_direct | 0.050/0.050 | 0.050/0.050 | 0.002/0.001 | 0.958/0.908 | 0.987/0.997 | 0.000/0.000 | 1.000/1.000 |

