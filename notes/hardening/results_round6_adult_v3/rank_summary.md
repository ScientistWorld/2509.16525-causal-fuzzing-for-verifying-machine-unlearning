## cohort all_hardening_runs: reference seed spread = 0.0213
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +0.2021 | [-0.028, +0.392] | 0 |
| variant_hgb | +0.1392 | [-0.030, +0.291] | 0 |
| shortcut_cafe_zero_direct_gap | +0.1357 | [+0.019, +0.255] | 0 |
| variant_full_adjust | +0.0383 | [+0.002, +0.077] | 0 |
| shortcut_cafe_shrink_unlearned | +0.0020 | [-0.004, +0.007] | 0 |
| cafe | +0.0000 | - | 0 |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] | 0 |
| cafe_seed11 | -0.0088 | [-0.026, +0.006] | 0 |
| cafe_seed19 | -0.0213 | [-0.042, -0.003] | 0 |
| shortcut_cafe_constant_subgroup | -0.1046 | [-0.304, +0.089] | 0 |
| variant_cafe_half_rows | -0.1121 | [-0.262, +0.017] | 0 |
| shortcut_cafe_prior_subgroup | -0.1248 | [-0.346, +0.082] | 0 |
| shortcut_direct_retention_claim | -0.2702 | [-0.281, -0.258] | 0 |
| shortcut_cafe_assume_unlearned | -0.6957 | [-0.818, -0.544] | 0 |
| variant_abduction | -1.3957 | [-1.570, -1.231] | 0 |
| variant_no_backdoor | -1.5228 | [-1.879, -1.191] | 0 |
| causal_fuzzing | -1.5806 | [-1.795, -1.386] | 0 |
| variant_probe_direct | -1.6804 | [-1.720, -1.644] | 0 |
| shortcut_constant_answers | -4.3420 | [-4.654, -4.011] | 0 |
| shortcut_flag_all_unlearned | -4.4609 | [-4.697, -4.198] | 0 |
| variant_direct_only | -4.8227 | [-4.955, -4.682] | 0 |
| direct_permutation | -5.0247 | [-5.180, -4.869] | 0 |
| shortcut_zero_output | -6.0534 | [-6.185, -5.912] | 0 |
| shortcut_rescale_units | -11.6893 | [-11.816, -11.556] | 0 |
| shortcut_drop_features | -15.3963 | - | 48 |
| shortcut_nonfinite_values | -15.3963 | - | 48 |
| shortcut_overbudget_bruteforce | -15.3963 | - | 48 |

## cohort honest_runs: reference seed spread = 0.0408
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +1.0187 | [-0.556, +1.907] | 0 |
| variant_hgb | +0.8249 | [+0.477, +1.166] | 0 |
| variant_full_adjust | +0.3477 | [+0.207, +0.490] | 0 |
| variant_abduction | +0.0528 | [-0.406, +0.494] | 0 |
| cafe_seed11 | +0.0097 | [-0.056, +0.071] | 0 |
| cafe | +0.0000 | - | 0 |
| cafe_seed19 | -0.0311 | [-0.095, +0.030] | 0 |
| variant_cafe_half_rows | -0.9335 | [-2.205, -0.131] | 0 |
| causal_fuzzing | -1.1099 | [-1.786, -0.489] | 0 |
| variant_probe_direct | -1.1844 | [-1.351, -1.011] | 0 |
| variant_no_backdoor | -5.2861 | [-5.942, -4.669] | 0 |
| direct_permutation | -9.4297 | [-9.876, -8.945] | 0 |
| variant_direct_only | -10.2553 | [-10.683, -9.815] | 0 |

## each shortcut ranked in a cohort of the honest runs plus that shortcut
| shortcut | rank score vs cafe | paired 95% CI |
|---|---:|---|
| shortcut_cafe_zero_direct_gap | +0.0390 | [-0.269, +0.349] |
| shortcut_cafe_shrink_unlearned | +0.0235 | [-0.022, +0.064] |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] |
| shortcut_cafe_constant_subgroup | -0.0868 | [-0.512, +0.379] |
| shortcut_cafe_prior_subgroup | -0.2160 | [-0.820, +0.369] |
| shortcut_cafe_assume_unlearned | -1.3604 | [-1.637, -1.044] |
| shortcut_direct_retention_claim | -2.4673 | [-2.585, -2.344] |
| shortcut_flag_all_unlearned | -9.5528 | [-9.986, -9.061] |
| shortcut_constant_answers | -9.6474 | [-10.362, -8.927] |
| shortcut_zero_output | -12.2151 | [-12.595, -11.812] |
| shortcut_rescale_units | -15.9682 | [-16.136, -15.795] |
| shortcut_drop_features | -18.9325 | - |
| shortcut_nonfinite_values | -18.9325 | - |
| shortcut_overbudget_bruteforce | -18.9325 | - |

## raw test metrics
### adult_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | verdict_accuracy | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| cafe_seed11 | 0.0367 | 0.0331 | 0.0289 | 0.9672 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| cafe_seed19 | 0.0367 | 0.0336 | 0.0292 | 0.9686 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| causal_fuzzing | 0.1015 | 0.0997 | 0.0125 | 0.9380 | 0.9706 | 0.0000 | 0.9750 | 0.9978 |
| direct_permutation | 0.1673 | 0.1638 | 0.0079 | 0.6608 | 0.0316 | 0.0000 | 0.5222 | 0.9977 |
| shortcut_cafe_assume_unlearned | 0.0699 | 0.0663 | 0.0285 | 0.8771 | 0.5714 | 0.0000 | 0.7667 | 0.5000 |
| shortcut_cafe_constant_subgroup | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_cafe_prior_subgroup | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_cafe_shrink_unlearned | 0.0370 | 0.0334 | 0.0287 | 0.9696 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_cafe_zero_direct_gap | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_constant_answers | 1.1476 | 0.3242 | 0.9492 | 0.4502 | 0.0000 | 0.0000 | 0.7667 | 1.0000 |
| shortcut_direct_retention_claim | 0.0372 | 0.1247 | 0.1311 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2683 | 0.2659 | 0.0279 | 0.3460 | 0.6221 | 1.0000 | 0.5000 | 0.8958 |
| shortcut_forged_fields | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| shortcut_rescale_units | 1.9962 | 1.7663 | 1.7506 | 0.9699 | 0.0000 | 1.0000 | 0.5000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0372 | 0.0335 | 0.0290 | 0.9699 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| shortcut_zero_output | 0.4230 | 0.1638 | 0.2650 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 1.0000 |
| variant_abduction | 0.0370 | 0.0328 | 0.0125 | 0.9779 | 1.0000 | 0.0000 | 1.0000 | 0.9977 |
| variant_abduction_half | 0.0445 | 0.0358 | 0.0172 | 0.9633 | 1.0000 | 0.0714 | 0.9139 | 0.5000 |
| variant_cafe_half_rows | 0.0495 | 0.0463 | 0.0372 | 0.9401 | 1.0000 | 0.0714 | 0.9750 | 0.5000 |
| variant_direct_only | 0.1747 | 0.1638 | 0.0290 | 0.6869 | 0.0084 | 0.0000 | 0.5000 | 0.5000 |
| variant_full_adjust | 0.0335 | 0.0306 | 0.0276 | 0.9738 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| variant_hgb | 0.0305 | 0.0279 | 0.0135 | 0.9762 | 1.0000 | 0.0000 | 1.0000 | 0.5000 |
| variant_no_backdoor | 0.2383 | 0.0631 | 0.1878 | 0.6792 | 1.0000 | 0.0000 | 1.0000 | 0.8750 |
| variant_probe_direct | 0.0380 | 0.0335 | 0.0135 | 0.9703 | 1.0000 | 0.0000 | 1.0000 | 0.9989 |

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
- cafe_seed11: heart total 9/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied; adult total 12/24 better, 0 tied
- cafe_seed19: heart total 6/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 15/24 better, 0 tied
- causal_fuzzing: heart total 5/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 5/24 better, 0 tied
- direct_permutation: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_cafe_assume_unlearned: heart total 6/12 better, 0 tied; perf total 6/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 4/24 better, 0 tied
- shortcut_cafe_constant_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_cafe_prior_subgroup: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_cafe_shrink_unlearned: heart total 6/12 better, 6 tied; perf total 6/12 better, 4 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 13/24 better, 3 tied
- shortcut_cafe_zero_direct_gap: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 3/12 better, 0 tied; adult total 0/24 better, 24 tied
- shortcut_constant_answers: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_direct_retention_claim: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_flag_all_unlearned: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 0 tied
- shortcut_forged_fields: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_rescale_units: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 0 tied; adult total 0/24 better, 0 tied
- shortcut_scores_file_forgery: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 0/24 better, 24 tied
- shortcut_zero_output: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_abduction: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 13/24 better, 0 tied
- variant_abduction_half: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 11/24 better, 0 tied
- variant_cafe_half_rows: heart total 8/12 better, 0 tied; perf total 3/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied; adult total 6/24 better, 0 tied
- variant_direct_only: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 6/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_full_adjust: heart total 9/12 better, 0 tied; perf total 9/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied; adult total 18/24 better, 0 tied
- variant_hgb: heart total 12/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied; adult total 21/24 better, 0 tied
- variant_no_backdoor: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied; adult total 0/24 better, 0 tied
- variant_probe_direct: heart total 6/12 better, 0 tied; perf total 4/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied; adult total 13/24 better, 0 tied
