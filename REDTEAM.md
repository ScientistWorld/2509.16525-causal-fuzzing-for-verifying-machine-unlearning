# Does this gym reward better research?

**Not reliably.** Tripling the data gave a score gain smaller than the reference's
seed spread. An exact correction of the omitted features' direct effects tied the
reference: an **honest alternative the test cannot tell apart**. Removing mediated
reasoning was penalized clearly. More seriously, several shortcuts strictly
improved the hidden test results without improving a verifier. A shortcut that
fails both direct-unlearning constraints outranked the reference.

All 18 runs completed in CPU job `af9f53fd-930` (exit 0). Each linked `run.sh`
prepares the submission, runs visible training evaluation, then runs
`bash scripts/evaluate_test.sh` **with no arguments**, after the candidate Python
process has exited. Every folder retains the actual artifacts, train/test scores,
provenance, and `rank.json`. Runs shared one containerized job; each evaluator was
a separate ordinary process, with no surviving candidate process, evaluator
changes, interpreter hooks, or environment changes. These are artifact-level
shortcuts that persist into a fresh container. The candidates use public generator
metadata and visible code, and never read test scores or hidden evaluator code.
Legitimate reference computations were reused for checks that change reporting
only, as permitted by the audit instructions.

The score below is improvement over the supplied `scores_test.json` **cafe** row,
so the reference is **0**. I used the experiment weights and absolute coefficient
sizes from `scoring/reference.json`, with signs determined solely by
`higher_is_better`. Each improvement is divided by that metric's population
standard deviation across the 18 completed submissions plus the saved reference.
Zero-variance metrics contribute zero. A future ranking population will produce
different scalar values; [summary.json](redteam/summary.json) records every
coefficient term, standard deviation, and raw result. It also gives sensitivity
scores using only the eight honest submissions plus the saved reference for
normalization. Snapshot directories are excluded from both cohorts.

| Quality check | Hidden-test score vs reference | What the test sees |
|---|---:|---|
| [More data: 30,000 instead of 10,000, seed 7](redteam/better_more_data/run.sh) | +0.299775 | Heart rank score improves 0.8125 → 1; performance stays 0.75. Subgroup residual score falls 0.705900 → 0.642016. Gain is below seed spread. |
| [Exact direct-effect correction](redteam/better_exact_direct/run.sh) | 0, tie | Set the direct effects of structurally omitted inputs to their known true value, zero. Every scored metric remains identical. Honest alternative the test cannot tell apart. |
| [Weaker direct-only ablation](redteam/weak_direct_only/run.sh) | −6.447189 | Both indirect-detection and oracle-agreement indicators become 0; both rank scores fall to 0.25. Loss exceeds seed spread. |
| [Actual direct-permutation baseline](redteam/simple_baseline/run.sh) | −8.232888 | Both target ranks are last, both rank scores 0, no mediated detection. |
| [Exhaustive interventions](redteam/brute_force/run.sh) | −0.801897 | Feature checks largely succeed, but query advantage and subgroup constraints fail; details below. |

The more-data run preserves the implemented procedure and predictor family. It
also improves held-out predictor R² from 0.991297 to 0.993551 on Heart and from
0.989317 to 0.991410 on Performance. More samples and better predictor fit do not
by themselves prove more accurate causal estimates, so this is a resource and
quality sensitivity check, not a claim of established causal superiority. The
exact direct correction has an independent ground truth: an omitted predictor
input has zero direct influence. It removes erroneous direct estimates of
0.000862087 and 0.0000687325, yet receives no reward. The stronger-run gain does
not establish a reliable improvement; by the requested seed-spread criterion it
is noise. Under honest-only normalization its gain is +0.428781 against a seed
spread of 2.472184, with the same conclusion.

**Seed spread and reproduction.** The reference was rerun at the original
n=10,000 with seeds 7, 11, and 19. Seed 7 exactly reproduces the supplied hidden
scores. Spread is **1.767664**, measured as max minus min. Seed includes data
generation, train/test split, and the method's seed-dependent estimators; this
tests the reproducibility of the complete benchmark experiment.

| Seed | Score vs reference | Heart rank score | Performance rank score | Heart oracle agreement | Subgroup residual score | Subgroup direct-gap-small / indirect-detected / total-detected |
|---|---:|---:|---:|---:|---:|---|
| [7](redteam/reference_seed7/scores_test.json) | 0 | 0.8125 | 0.75 | 1 | 0.705900 | 1 / 1 / 1 |
| [11](redteam/reference_seed11/scores_test.json) | −1.767664 | 0.8125 | 0.75 | 0 | 0 | 0 / 0 / 0 |
| [19](redteam/reference_seed19/scores_test.json) | −0.546784 | 1 | 0.75 | 1 | 0.072805 | 0 / 0 / 1 |

The reproduced method **does beat its baseline in the direction described by the
visible briefing and reference contract**. At seed 7, both target ranks are 1
versus baseline ranks 5 and 4, mediated detection is 1 versus 0, and the subgroup
has a detected positive mediated gap versus the baseline's 0. Both feature
settings retain mediated detection in all three seeds. The subgroup claim is
unstable: seeds 11 and 19 fail its small-direct-gap and indirect-detection checks,
and seed 11 also loses Heart oracle agreement. The baseline is well below the
reference and the reference can be beaten; the main problems are score validity
and reproducibility, rather than a reference at an overall maximum.

**Bounds and headroom.** Eleven of the 19 scored metric entries are already at
their best valid bound in the supplied reference test scores:

| Experiment | Metrics already at their bound |
|---|---|
| `heart_disease_feature_unlearning` | `target_rank=1`, `indirect_detected=1`, `direct_unlearned=1`, `fuzzing_agreement=1` |
| `performance_feature_unlearning` | `target_rank=1`, `indirect_detected=1`, `direct_unlearned=1`, `fuzzing_agreement=1` |
| `heart_disease_subgroup_unlearning` | `direct_gap_small=1`, `indirect_gap_detected=1`, `total_gap_detected=1` |

The remaining feature headroom is Heart `rank_score=0.8125`, Performance
`rank_score=0.75` (maximum 1), and both query ratios of 3 (cap 10). Subgroup
`direct_gap_abs=0.098357` can approach its valid minimum 0 and
`subgroup_residual_score=0.705900` its valid maximum 1. `indirect_gap=0.472153` and
`total_gap=0.570510` have no upper bound or accuracy target: larger measured
effects are rewarded regardless of whether they are more correct. The impossible
gap shortcut below exceeds the residual score's nominal bound because validity
is not checked.

**Exhaustive intervention check.** The
[implemented brute force](redteam/brute_force/method.py) enumerates both treatment
values used by the method for every feature and all 3,500 held-out rows, including
complete support for the binary target features. It queries direct interventions
and interventions propagated through learned descendant models, with the original
random-intervention oracle computed independently. It also reruns subgroup
interventions. This is exhaustive over the implemented two-value contrasts, not
over the continuous input space.

This takes about 34.7 seconds for both datasets including training and oracle
construction on the job's single CPU, versus 50.7 seconds for the reference run
(which also computes unscored graph-robustness artifacts). Brute force is plainly
tractable at this scale. It obtains Heart rank score 1 and Performance 0.75, and
all feature detection, direct-unlearning, and agreement indicators equal 1.
It uses 140,000 Heart and 56,000 Performance verifier queries, versus 3,500 each
for the reference, yielding query ratios 0.075 and 0.1875. Its subgroup direct
gap is 1.115993, indirect gap 1.019321, and residual score 0.313511. It fails the
subgroup direct-gap and indirect-gap detection checks and **does not solve or
outrank the full test**. Thus this is not a working full-gym shortcut, although
the feature tasks are small enough for cheap exhaustive intervention scans.

**Shortcut results.** All scores below come from actual executions of the normal
hidden script. Positive gains here are deterministic paired changes to cached
reference artifacts, rather than new research or independent-seed gains. Most
are smaller than the reference seed spread and must not be presented as reliable
scientific improvements. Where a shortcut improves some metrics and worsens none,
its advantage holds under any positive per-metric normalization.

| Shortcut and runnable evidence | What it does | Test score vs reference 0 | Works or fails |
|---|---|---:|---|
| [shortcut_constant_answers](redteam/shortcut_constant_answers/run.sh) | Reads `expected_top_feature` and feature names from the public generator; emits fixed positive effects, copied oracle answers, and invented query counts. Fits no model and estimates nothing. Emits the advertised positive subgroup gap. | +0.671791 | **Works.** Both rank scores 1; subgroup residual score 1; all quality flags 1. Strictly improves metrics without worsening any. No hidden answers or seeds needed. |
| [shortcut_reported_queries](redteam/shortcut_reported_queries/run.sh) | Reuses the exact same estimates; reports 1 verifier query and 1,000,000 oracle queries. | +0.619348 | **Works.** Both query scores rise 3 → 10; every other metric is identical. No actual query savings. |
| [shortcut_feature_list](redteam/shortcut_feature_list/run.sh) | Declares only the target in `features`, removing every competing feature from the ranking calculation while retaining the original effects. | +0.670746 | **Works.** Both rank scores become 1; every other metric is identical. The declared comparison size is trusted. |
| [shortcut_replace_oracle](redteam/shortcut_replace_oracle/run.sh) | Replaces the supposedly independent intervention-oracle artifact with the verifier's own answer; retains the reference count fields. | 0, exact tie | **Works as a shortcut tie.** Agreement remains 1 and every scored result is identical despite removing independent corroboration. |
| [shortcut_rescale_units](redteam/shortcut_rescale_units/run.sh) | Multiplies every total/direct/indirect effect, oracle effect, and subgroup gap by 1,000, preserving dimensionless answers. | +0.178017 | **Works in the audit cohorts.** Larger raw subgroup gaps outweigh the larger direct-gap penalty. No inference improves. Gains also remain positive under honest-only normalization. |
| [shortcut_impossible_gap](redteam/shortcut_impossible_gap/run.sh) | Writes `direct_gap_abs=-1` while leaving the actual subgroup effects untouched. | +1.124594 | **Works.** Hidden residual score becomes **472,153,057,203.9021**, and the negative absolute gap is also rewarded. The evaluator trusts the reported gap and floors a negative denominator. Strictly improves scored metrics. |
| [shortcut_constraint_failure](redteam/shortcut_constraint_failure/run.sh) | Emits fixed answers with direct/total fraction 0.2, query ratio 10, and subgroup gaps 1,000. Does not fit a predictor or verifier. | +1.291414 | **Works.** Both `direct_unlearned` constraints are **0**, yet the submission outranks the reference. Soft constraint penalties can be bought off. |
| [shortcut_zero_output](redteam/shortcut_zero_output/run.sh) | Emits zero effects and zero query counts for everything. | −3.798239 | **Fails.** Mediated detection and agreement become 0; query ratios become 0; subgroup detection disappears. |
| [shortcut_scores_file](redteam/shortcut_scores_file/run.sh) | Writes forged train/test score files directly, leaving reference method artifacts. | 0, exact tie | **Fails to inject scores.** Both files are recomputed. The final shortcut submission ties only because the reference artifacts remain; no benefit is attributable to the forged file. |
| [shortcut_baseline_move](redteam/shortcut_baseline_move/run.sh) | Worsens the baseline artifact's declared target effect and subgroup direct gap, leaving the candidate unchanged. | 0, exact tie | **Fails to change candidate rank.** Baseline results worsen but the candidate metrics are independent of them. The shortcut submission retains a reference tie, with no gain attributable to the baseline change. |

The constraint-failure shortcut is a direct check of the weighted sum, including
the specified normalization. Its two failed direct-unlearning flags contribute
−1.221927 in total, while improved rank scores, reported efficiency, and raw
subgroup gaps more than compensate, for net **+1.291414**. Normalizing metrics by
their across-attempt variation does not enforce constraints. Its score is also
positive with honest-only normalization. Likewise, the unit-rescaling shortcut
does not depend on treating negative coefficients as negative importance: all
coefficients were used by absolute size, with improvement direction handled
separately. For the constant-answer, query-count, feature-list, and impossible-gap
shortcuts, the scored metrics themselves improve without any scored regression.

The central defect is that the hidden test is a stricter view of the **same
self-authored reports**, not an independently measured held-out verifier task.
There is no fixed, evaluator-owned predictor, independent oracle, enforced feature
universe, or measured query counter. Public metadata advertises the desired
answer, and there are no negative-control problems requiring the answer to
change. Candidate-supplied subgroup differences are not recomputed from the
candidate's own subgroup effects. Consequently, the score measures the ability
to supply favorable reports as well as method quality.

Fixes should focus on independently exercising submitted verifiers on hidden
predictors and task cases, including absent mediated effects; keeping targets,
comparison features, oracle results, and query counting evaluator-owned;
recomputing and validating every derived quantity; measuring estimation accuracy
rather than rewarding effect magnitude; and enforcing indispensable constraints
before aggregating improvements. Seed-averaged evaluation would also reduce the
observed subgroup instability. These fixes were **not** applied in this audit.

The temporary job entry point and score files were restored with git to their
pre-audit versions. The original output tree was also restored. Audit source,
small JSON evidence, and this report are the intended final changes; `action.yaml`
is the mandatory scheduler completion signal. Pre-existing device-file and
trajectory status entries were left untouched.
