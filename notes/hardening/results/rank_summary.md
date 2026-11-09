## cohort all_hardening_runs: reference seed spread = 0.0186
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +0.1574 | [+0.054, +0.252] | 0 |
| variant_hgb | +0.1084 | [+0.047, +0.163] | 0 |
| cafe_seed19 | +0.0186 | [-0.009, +0.059] | 0 |
| cafe_seed11 | +0.0015 | [-0.020, +0.026] | 0 |
| cafe | +0.0000 | - | 0 |
| shortcut_forged_fields | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_scores_file_forgery | +0.0000 | [+0.000, +0.000] | 0 |
| shortcut_direct_retention_claim | -0.2543 | [-0.266, -0.243] | 0 |
| variant_no_backdoor | -0.4577 | [-0.574, -0.342] | 0 |
| variant_abduction | -0.4890 | [-0.589, -0.395] | 0 |
| variant_probe_direct | -0.6335 | [-0.672, -0.597] | 0 |
| causal_fuzzing | -0.6638 | [-0.805, -0.533] | 0 |
| shortcut_constant_answers | -1.2422 | [-1.353, -1.124] | 0 |
| shortcut_flag_all_unlearned | -2.2759 | [-2.344, -2.204] | 0 |
| variant_direct_only | -3.0304 | [-3.117, -2.912] | 0 |
| direct_permutation | -3.3097 | [-3.397, -3.209] | 0 |
| shortcut_zero_output | -3.9997 | [-4.073, -3.907] | 0 |
| shortcut_rescale_units | -7.9140 | [-8.012, -7.811] | 0 |
| shortcut_drop_features | -11.7312 | - | 24 |
| shortcut_nonfinite_values | -11.7312 | - | 24 |
| shortcut_overbudget_bruteforce | -11.7312 | - | 24 |

## cohort honest_runs: reference seed spread = 0.0885
| method | rank score vs cafe | paired 95% CI | failed tasks |
|---|---:|---|---:|
| variant_abduction_half | +1.9823 | [+1.458, +2.517] | 0 |
| variant_abduction | +1.2400 | [+0.697, +1.792] | 0 |
| variant_hgb | +0.9855 | [+0.623, +1.369] | 0 |
| causal_fuzzing | +0.4435 | [-0.206, +1.083] | 0 |
| cafe_seed19 | +0.0354 | [-0.110, +0.194] | 0 |
| cafe | +0.0000 | - | 0 |
| cafe_seed11 | -0.0531 | [-0.163, +0.049] | 0 |
| variant_probe_direct | -0.2137 | [-0.370, -0.049] | 0 |
| variant_no_backdoor | -2.9691 | [-3.515, -2.478] | 0 |
| direct_permutation | -6.6842 | [-7.142, -6.243] | 0 |
| variant_direct_only | -7.7695 | [-8.125, -7.407] | 0 |

## raw test metrics
### heart_disease_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0813 | 0.0849 | 0.0542 | 0.9524 | 0.9774 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0814 | 0.0828 | 0.0530 | 0.9619 | 0.9781 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0809 | 0.0818 | 0.0532 | 0.9619 | 0.9762 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0977 | 0.0971 | 0.0025 | 0.8238 | 0.9949 | 0.0000 | 0.9966 |
| direct_permutation | 0.3082 | 0.3079 | 0.0010 | 0.2326 | 0.0041 | 0.0000 | 0.9989 |
| shortcut_constant_answers | 0.4057 | 0.2690 | 0.1635 | 0.7888 | 0.1555 | 0.0000 | 0.0000 |
| shortcut_direct_retention_claim | 0.0813 | 0.2571 | 0.2295 | 0.9524 | 0.9774 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2189 | 0.2106 | 0.0394 | 0.3285 | 0.9955 | 1.0000 | 0.5000 |
| shortcut_forged_fields | 0.0813 | 0.0849 | 0.0542 | 0.9524 | 0.9774 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.9730 | 1.5548 | 0.9524 | 1.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0813 | 0.0849 | 0.0542 | 0.9524 | 0.9774 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.4821 | 0.3079 | 0.1744 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0374 | 0.0371 | 0.0025 | 0.9714 | 0.9869 | 0.0000 | 0.9966 |
| variant_abduction_half | 0.0386 | 0.0380 | 0.0027 | 0.9714 | 0.9839 | 0.0000 | 0.4983 |
| variant_direct_only | 0.3425 | 0.3079 | 0.0542 | 0.0095 | 0.0000 | 0.0000 | 0.5000 |
| variant_hgb | 0.0541 | 0.0625 | 0.0319 | 0.9667 | 0.9787 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2285 | 0.1603 | 0.1229 | 0.8571 | 0.9816 | 0.0000 | 0.5000 |
| variant_probe_direct | 0.0840 | 0.0831 | 0.0019 | 0.8810 | 0.9959 | 0.0000 | 0.9983 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae | total_gap_nmae | direct_gap_nmae | indirect_gap_capture |
|---|---:|---:|---:|---:|
| cafe | 0.1807 | 0.1713 | 0.2637 | 0.9158 |
| cafe_seed11 | 0.1921 | 0.1752 | 0.2754 | 0.9334 |
| cafe_seed19 | 0.1828 | 0.1772 | 0.2537 | 0.9457 |
| causal_fuzzing | 0.0427 | 0.0488 | 0.0070 | 0.7860 |
| direct_permutation | 0.1570 | 0.1591 | 0.0063 | 0.0000 |
| shortcut_constant_answers | 0.0904 | 0.1639 | 0.1039 | 0.5265 |
| shortcut_direct_retention_claim | 0.1807 | 0.1713 | 0.2637 | 0.9158 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_flag_all_unlearned | 0.1807 | 0.1713 | 0.2637 | 0.9158 |
| shortcut_forged_fields | 0.1807 | 0.1713 | 0.2637 | 0.9158 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | 0.0000 |
| shortcut_rescale_units | 1.9733 | 2.0000 | 2.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.1807 | 0.1713 | 0.2637 | 0.9158 |
| shortcut_zero_output | 0.1570 | 0.2529 | 0.1039 | 0.0000 |
| variant_abduction | 0.0458 | 0.0516 | 0.0070 | 0.7705 |
| variant_abduction_half | 0.0490 | 0.0539 | 0.0077 | 0.7718 |
| variant_direct_only | 0.1570 | 0.4075 | 0.2637 | 0.0000 |
| variant_hgb | 0.1075 | 0.0911 | 0.1356 | 0.9166 |
| variant_no_backdoor | 0.1594 | 0.1299 | 0.2362 | 0.9826 |
| variant_probe_direct | 0.1745 | 0.1754 | 0.0107 | 0.9158 |

### performance_feature_unlearning
| method | total_effect_nmae | indirect_effect_nmae | direct_effect_nmae | rank_spearman | residual_capture | false_alarm_rate | query_budget_fraction |
|---|---:|---:|---:|---:|---:|---:|---:|
| cafe | 0.0452 | 0.0636 | 0.0567 | 0.9667 | 0.9856 | 0.0000 | 0.5000 |
| cafe_seed11 | 0.0444 | 0.0658 | 0.0555 | 0.9500 | 0.9863 | 0.0000 | 0.5000 |
| cafe_seed19 | 0.0441 | 0.0639 | 0.0563 | 0.9583 | 0.9873 | 0.0000 | 0.5000 |
| causal_fuzzing | 0.0456 | 0.0450 | 0.0012 | 0.9667 | 0.9288 | 0.0000 | 1.0000 |
| direct_permutation | 0.2920 | 0.2916 | 0.0006 | 0.5253 | 0.0042 | 0.0000 | 1.0000 |
| shortcut_constant_answers | 0.3930 | 0.2295 | 0.1649 | 0.6895 | 0.3244 | 0.0000 | 0.0000 |
| shortcut_direct_retention_claim | 0.0452 | 0.2140 | 0.2205 | 0.9667 | 0.9856 | 0.0000 | 0.5000 |
| shortcut_drop_features | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_flag_all_unlearned | 0.2522 | 0.2510 | 0.0351 | 0.3024 | 0.9964 | 1.0000 | 0.5000 |
| shortcut_forged_fields | 0.0452 | 0.0636 | 0.0567 | 0.9667 | 0.9856 | 0.0000 | 0.5000 |
| shortcut_nonfinite_values | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_overbudget_bruteforce | 2.0000 | 2.0000 | 2.0000 | -1.0000 | 0.0000 | 1.0000 | 1.0000 |
| shortcut_rescale_units | 2.0000 | 1.9296 | 1.6129 | 0.9667 | 1.0000 | 1.0000 | 1.0000 |
| shortcut_scores_file_forgery | 0.0452 | 0.0636 | 0.0567 | 0.9667 | 0.9856 | 0.0000 | 0.5000 |
| shortcut_zero_output | 0.5483 | 0.2916 | 0.2567 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| variant_abduction | 0.0254 | 0.0249 | 0.0012 | 0.9833 | 0.9745 | 0.0000 | 1.0000 |
| variant_abduction_half | 0.0267 | 0.0265 | 0.0010 | 0.9833 | 0.9763 | 0.0000 | 0.5000 |
| variant_direct_only | 0.3319 | 0.2916 | 0.0567 | 0.2583 | 0.0001 | 0.0000 | 0.5000 |
| variant_hgb | 0.0418 | 0.0588 | 0.0365 | 0.9583 | 0.9871 | 0.0000 | 0.5000 |
| variant_no_backdoor | 0.2636 | 0.1330 | 0.1934 | 0.5833 | 0.9856 | 0.0000 | 0.5000 |
| variant_probe_direct | 0.0630 | 0.0628 | 0.0010 | 0.9000 | 0.9875 | 0.0000 | 1.0000 |

## per-task paired comparison vs cafe (lower per-task error)
- cafe_seed11: heart total 7/12 better, 0 tied; perf total 7/12 better, 0 tied; subgroup indirect gap 4/12 better, 0 tied
- cafe_seed19: heart total 8/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 5/12 better, 0 tied
- causal_fuzzing: heart total 6/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 10/12 better, 0 tied
- direct_permutation: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied
- shortcut_constant_answers: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 9/12 better, 0 tied
- shortcut_direct_retention_claim: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_flag_all_unlearned: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_forged_fields: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_rescale_units: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 0/12 better, 0 tied
- shortcut_scores_file_forgery: heart total 0/12 better, 12 tied; perf total 0/12 better, 12 tied; subgroup indirect gap 0/12 better, 12 tied
- shortcut_zero_output: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied
- variant_abduction: heart total 11/12 better, 0 tied; perf total 12/12 better, 0 tied; subgroup indirect gap 11/12 better, 0 tied
- variant_abduction_half: heart total 11/12 better, 0 tied; perf total 11/12 better, 0 tied; subgroup indirect gap 11/12 better, 0 tied
- variant_direct_only: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 7/12 better, 0 tied
- variant_hgb: heart total 11/12 better, 0 tied; perf total 8/12 better, 0 tied; subgroup indirect gap 9/12 better, 0 tied
- variant_no_backdoor: heart total 0/12 better, 0 tied; perf total 0/12 better, 0 tied; subgroup indirect gap 8/12 better, 0 tied
- variant_probe_direct: heart total 6/12 better, 0 tied; perf total 3/12 better, 0 tied; subgroup indirect gap 12/12 better, 0 tied

## train vs test (honest runs)
### heart_disease_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.089/0.081 | 0.087/0.085 | 0.048/0.054 | 0.971/0.952 | 0.986/0.977 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.090/0.081 | 0.088/0.083 | 0.047/0.053 | 0.981/0.962 | 0.988/0.978 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.087/0.081 | 0.086/0.082 | 0.047/0.053 | 0.981/0.962 | 0.988/0.976 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.106/0.098 | 0.106/0.097 | 0.002/0.003 | 0.800/0.824 | 0.986/0.995 | 0.000/0.000 | 0.997/0.997 |
| direct_permutation | 0.293/0.308 | 0.293/0.308 | 0.001/0.001 | 0.292/0.233 | 0.011/0.004 | 0.000/0.000 | 0.999/0.999 |
| variant_abduction | 0.043/0.037 | 0.042/0.037 | 0.002/0.003 | 0.971/0.971 | 0.977/0.987 | 0.000/0.000 | 0.997/0.997 |
| variant_abduction_half | 0.045/0.039 | 0.044/0.038 | 0.004/0.003 | 0.971/0.971 | 0.976/0.984 | 0.000/0.000 | 0.498/0.498 |
| variant_direct_only | 0.319/0.343 | 0.293/0.308 | 0.048/0.054 | 0.095/0.010 | 0.001/0.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.047/0.054 | 0.055/0.063 | 0.039/0.032 | 0.981/0.967 | 0.986/0.979 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.175/0.229 | 0.122/0.160 | 0.094/0.123 | 0.943/0.857 | 0.978/0.982 | 0.000/0.000 | 0.500/0.500 |
| variant_probe_direct | 0.085/0.084 | 0.085/0.083 | 0.001/0.002 | 0.962/0.881 | 0.999/0.996 | 0.000/0.000 | 0.998/0.998 |

### heart_disease_subgroup_unlearning
| method | indirect_gap_nmae train/test | total_gap_nmae train/test | direct_gap_nmae train/test | indirect_gap_capture train/test |
|---|---|---|---|---|
| cafe | 0.323/0.181 | 0.262/0.171 | 0.446/0.264 | 1.000/0.916 |
| cafe_seed11 | 0.323/0.192 | 0.261/0.175 | 0.442/0.275 | 0.969/0.933 |
| cafe_seed19 | 0.316/0.183 | 0.252/0.177 | 0.441/0.254 | 0.958/0.946 |
| causal_fuzzing | 0.063/0.043 | 0.068/0.049 | 0.005/0.007 | 0.642/0.786 |
| direct_permutation | 0.256/0.157 | 0.256/0.159 | 0.003/0.006 | 0.000/0.000 |
| variant_abduction | 0.050/0.046 | 0.056/0.052 | 0.005/0.007 | 0.698/0.771 |
| variant_abduction_half | 0.054/0.049 | 0.066/0.054 | 0.014/0.008 | 0.686/0.772 |
| variant_direct_only | 0.256/0.157 | 0.681/0.408 | 0.446/0.264 | 0.000/0.000 |
| variant_hgb | 0.196/0.108 | 0.207/0.091 | 0.215/0.136 | 0.919/0.917 |
| variant_no_backdoor | 0.289/0.159 | 0.201/0.130 | 0.334/0.236 | 1.000/0.983 |
| variant_probe_direct | 0.314/0.175 | 0.317/0.175 | 0.004/0.011 | 1.000/0.916 |

### performance_feature_unlearning
| method | total_effect_nmae train/test | indirect_effect_nmae train/test | direct_effect_nmae train/test | rank_spearman train/test | residual_capture train/test | false_alarm_rate train/test | query_budget_fraction train/test |
|---|---|---|---|---|---|---|---|
| cafe | 0.045/0.045 | 0.052/0.064 | 0.051/0.057 | 0.933/0.967 | 0.993/0.986 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed11 | 0.047/0.044 | 0.056/0.066 | 0.052/0.056 | 0.933/0.950 | 0.993/0.986 | 0.000/0.000 | 0.500/0.500 |
| cafe_seed19 | 0.045/0.044 | 0.053/0.064 | 0.051/0.056 | 0.933/0.958 | 0.993/0.987 | 0.000/0.000 | 0.500/0.500 |
| causal_fuzzing | 0.036/0.046 | 0.036/0.045 | 0.001/0.001 | 0.933/0.967 | 0.937/0.929 | 0.000/0.000 | 1.000/1.000 |
| direct_permutation | 0.335/0.292 | 0.335/0.292 | 0.001/0.001 | 0.305/0.525 | 0.003/0.004 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction | 0.025/0.025 | 0.024/0.025 | 0.001/0.001 | 0.967/0.983 | 0.978/0.975 | 0.000/0.000 | 1.000/1.000 |
| variant_abduction_half | 0.025/0.027 | 0.025/0.026 | 0.002/0.001 | 0.950/0.983 | 0.977/0.976 | 0.000/0.000 | 0.500/0.500 |
| variant_direct_only | 0.385/0.332 | 0.335/0.292 | 0.051/0.057 | -0.067/0.258 | 0.000/0.000 | 0.000/0.000 | 0.500/0.500 |
| variant_hgb | 0.033/0.042 | 0.040/0.059 | 0.037/0.036 | 0.933/0.958 | 0.993/0.987 | 0.000/0.000 | 0.500/0.500 |
| variant_no_backdoor | 0.282/0.264 | 0.152/0.133 | 0.184/0.193 | 0.367/0.583 | 0.993/0.986 | 0.000/0.000 | 0.500/0.500 |
| variant_probe_direct | 0.051/0.063 | 0.051/0.063 | 0.001/0.001 | 0.917/0.900 | 0.994/0.988 | 0.000/0.000 | 1.000/1.000 |

