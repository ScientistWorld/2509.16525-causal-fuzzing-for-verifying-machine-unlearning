# Hardening report (final iteration)

## Verdict

**Better results now score higher, and the major shortcuts no longer pay.**

- The old hidden test re-scored effect numbers that the method wrote itself, on public data whose answers were advertised. Seven red-team shortcuts beat the reference there.
- The new test is evaluator-owned end to end:
  - held-out structural causal models (SCMs) exist only in `eval/test/`;
  - the audited black-box models never leave the evaluator;
  - verifiers reach them only through an oracle that counts every query;
  - ground truth is exact;
  - every scored number is recomputed from the verifier's raw per-feature total and direct estimates.
- A better estimator at the same query cost beats the reference by about 15× the seed spread.
- Weaker ablations and the baselines fall far below it.
- Every red-team shortcut fails or ties as the reference's own unchanged estimates.
- One assumption-based variant is left (see "Left open").

All numbers below come from the final hidden-test run of 25 verifiers on 24 held-out tasks (12 Heart-Disease, 12 Performance). The run is in `notes/hardening/results/`: per-task records, raw answers, `rank_summary.md`, and the train slice. `python notes/hardening/rank.py` (pure Python) recomputes every score.

**How "score vs reference" is computed.** It follows the gym's rule: for each experiment and metric, the experiment weight × |coefficient| × the improvement in the metric's better direction, divided by that metric's population standard deviation over the ranked cohort. The CAFÉ reference scores 0. The 95% confidence intervals come from a paired bootstrap over held-out tasks.

**Two cohorts are reported, because the ranking depends on who is normalised together:**
- **all** = all 25 hardening runs;
- **honest+** = the 12 honest runs, plus the one shortcut being scored (for shortcut rows).

## What changed in the gym

1. **Hidden test is evaluator-owned.** `eval/test/` builds 24 tasks over the paper's graphs. They use different functional forms from the visible families and seeds that exist only there. Each task fixes:
   - the data;
   - the audited model (random forest, MLP, gradient boosting or linear);
   - the intervention values;
   - the query budget (2 oracle rows per audit row);
   - exact ground truth: interventions propagated through the true equations with each row's own noise.

   The tasks include negative controls (an unlearned feature with exactly zero influence) and failed unlearning (the target still a direct input).
2. **Evaluator-side validation.** NaN, infinite, missing or non-numeric answers fail the task, and a failed task gets the worst value on every metric. Errors are capped at 2 per value, in units of the task's largest true effect. Gaps, indirect effects, rankings and detections are derived by the evaluator. Extra fields are ignored. Queries over budget are refused.
3. **Subgroup direction varies.** In a third of the Heart tasks, in both slices, the age modulation is mirrored: the age ≤ 50 group carries the larger mediated BMI influence. The paper's published direction can no longer stand in for measurement.
4. **Scoring rules.**
   - Captures need the true sign and a value within 2× of the truth (no reward for over-claiming). They are scored only for effects of at least 20% of scale.
   - New subgroup primary metric `indirect_gap_direction`: the gap must be detected (at least 10% of scale) and point to the right age group.
   - Efficiency (`query_budget_fraction`) counts only on solved tasks, meaning total-effect error at most half that of the all-zero answer. One pass over the audit rows is free.
5. **Train slice.** 12 tasks per family, matching the test; it was 6.
6. **Paper fidelity (CAFÉ).** For a feature with no mediators, Def. 4 conditions the direct and the total contrast on the same set. CAFÉ now reports direct = total for such features. Previously two separately seeded fits produced spurious mediated effects.

## Do better results score higher?

| Variant | Before (red-team gym) | After: all | After: honest+ |
|---|---:|---:|---:|
| Better: counterfactual fuzzing with abduction, CAFÉ's own query cost (`variant_abduction_half`) | — | **+0.409** [+0.199, +0.614] | **+2.303** [+1.732, +2.859] |
| Better: CAFÉ with a gradient-boosting response model (`variant_hgb`) | — | +0.163 [−0.036, +0.340] | **+0.922** [+0.483, +1.332] |
| Red team "better": 3× more data | +0.300 (below seed spread 1.768) | n/a (data size fixed by the evaluator) | |
| Red team "better": exact direct correction | 0 (tie, not rewarded) | measured by `direct_effect_nmae`: exact direct probes reach 0.002 vs CAFÉ 0.057 | |
| Same accuracy at twice the cost (`variant_abduction`, two passes) | — | −1.169 | +0.723 |
| CAFÉ + direct probes, two passes (`variant_probe_direct`) | — | −1.547 | −0.938 |
| CAFÉ on half the audit rows (`variant_cafe_half_rows`) | — | −0.044 (round before the fix: +0.328) | −0.205 (before: +0.147) |
| Weaker: CAFÉ without the back-door set (`variant_no_backdoor`) | — | −1.205 | −3.976 |
| Weaker: direct-only ablation (`variant_direct_only`) | −6.447 | −4.932 | −9.500 |
| Baseline: direct permutation | −8.233 | −4.558 | −7.854 |
| Baseline: causal fuzzing (Algorithm 1, within budget) | — | −1.308 | +0.045 [−0.703, +0.773] (tie) |
| Reference reseeded (CAFÉ seeds 11, 19) | spread 1.768 | −0.010, −0.026 (spread **0.026**) | +0.013, −0.038 (spread 0.051) |

- The better variant at equal cost beats the reference in every paired comparison, by far more than the seed spread.
- The reference seed spread fell from 1.77 to 0.03. Tasks are now fixed by the evaluator; only the method's own seed varies.

## Major shortcuts: fix and score

"Before" is `REDTEAM.md` on the old gym. "After" is the closest equivalent run through the final hidden test.

| Shortcut | Fix | Before | After: all / honest+ |
|---|---|---:|---:|
| Constant answers from public metadata | Hidden SCMs, exact truth, and varied tasks (negative controls, failed unlearning, mirrored subgroups, random scales). Efficiency is credited only on solved tasks. | +0.672 | **−3.047 / −6.937** |
| Invented query counts | The oracle counts queries; reported counts are ignored (`shortcut_forged_fields`, the reference's own estimates plus forged fields) | +0.619 | 0.000 / 0.000: the forged fields gain nothing |
| Shrunk comparison feature list | The evaluator fixes the features to estimate; a missing feature fails the task (`shortcut_drop_features`) | +0.671 | −13.708 / −16.909 (24/24 tasks failed) |
| Replace the oracle artifact with the verifier's own answer | No oracle artifact is submitted; the evaluator computes the truth | 0 (tie) | not possible |
| Rescale units ×1000 | Errors are measured against the truth in task-scale units and capped | +0.178 | −10.445 / −14.383 |
| Impossible negative `direct_gap_abs` | Gaps are no longer submitted; non-finite values fail the task (`shortcut_nonfinite_values`) | +1.125 | −13.708 / −16.909 |
| Fail the direct-unlearning constraints with fixed answers | Direct effects scored against the truth; false alarms scored on true-zero controls (`shortcut_direct_retention_claim`, `shortcut_flag_all_unlearned`) | +1.291 | −0.278 / −2.267; −3.354 / −6.876 |
| Zero output | — | −3.798 | −5.378 / −10.339 |
| Forged score files | Score files recomputed (`shortcut_scores_file_forgery`) | 0 (fails) | 0.000 (the reference's estimates; the forgery gains nothing) |
| Move the baseline | The evaluator runs the baselines; candidate scores don't depend on them | 0 (fails) | not possible |
| Exhaustive interventions (brute force) | 2-row-per-audit-row budget; full Algorithm 1 needs 24 rows per audit row (`shortcut_overbudget_bruteforce`) | −0.802 | −13.708 / −16.909 (14,000 rows refused, 24/24 failed) |

Shortcuts found and closed during hardening:

| Shortcut | Fix | Before | After: all / honest+ |
|---|---|---:|---:|
| CAFÉ features + fixed subgroup guess (`shortcut_cafe_constant_subgroup`) | Per-task outcome scale (round 2), mirrored direction (final) | round 3: −0.050 / **+0.133** | −0.133 / −0.106 |
| CAFÉ features + fixed public split ratio (`shortcut_cafe_prior_subgroup`) | Factor-of-two capture (round 3), mirrored direction (final) | round 2: +0.048 (spread 0.02); round 3: −0.028 / +0.029 | −0.159 / −0.274 |
| Prior-only answers earning full efficiency credit | Efficiency requires halving the all-zero answer's error | round 3: query fraction 0.0 (best) for constant answers | 1.0 Heart / 0.875 Performance |
| Querying fewer audit rows for efficiency credit (`variant_cafe_half_rows`) | One pass over the evaluator-fixed audit sample is free | +0.328 / +0.147 | −0.044 / −0.205 |

The hybrids now get the gap direction wrong on 30% of eligible items (direction score 0.7 vs CAFÉ's 1.0).

## Left open

- **`shortcut_cafe_zero_direct_gap`: +0.170 [+0.027, +0.316] (all), +0.050 [−0.315, +0.435] (honest+).**
  - It is CAFÉ, but it gives both age groups CAFÉ's population direct effect: the paper's "direct effects identical" finding, assumed rather than measured.
  - It wins because CAFÉ's per-group direct estimates are worse than that assumption: direct-gap error 0.256 vs 0.103.
  - It loses on mediated-gap error (0.273 vs 0.194), because it invents a gap for blood pressure.
  - It ties the reference among honest runs. Honest measurement of per-group direct effects beats it by far (direct-gap error about 0.01 for the counterfactual verifiers).
  - I read it as a modelling assumption that exposes a weakness of the reference, not skipped work. Closing it would mean making direct gaps large enough that the paper's own claim fails, so I left it for the shortcut grader.
- **Ties as the reference's own estimates.** `shortcut_forged_fields` and `shortcut_scores_file_forgery` submit CAFÉ's own estimates plus junk, and score exactly 0. They gain nothing.

## Reference score before and after

The reproduced method still shows the paper's claims in the paper's direction, against the direct-only baseline. Hidden test, CAFÉ vs direct permutation:

| Experiment | Measure | CAFÉ | Direct permutation |
|---|---|---:|---:|
| Heart | rank Spearman | 0.938 | 0.234 |
| Heart | residual capture | 1.0 | 0.012 |
| Heart | total-effect error | 0.098 | 0.313 |
| Performance | rank Spearman | 0.983 | 0.542 |
| Performance | residual capture | 1.0 | 0.009 |
| Performance | total-effect error | 0.036 | 0.293 |
| Subgroup | gap direction | 1.0 | 0 |

Under the old metrics (`REDTEAM.md`), CAFÉ scored rank score 0.8125 / 0.75, and seed 11 lost the subgroup claim entirely. Its score was 0 by definition there and still is.

## Headroom

The reference sits at the bound of:
- `residual_capture` (1.0) in both feature experiments;
- `false_alarm_rate` (0) in both feature experiments;
- `query_budget_fraction` (0.5, the one-pass floor) in both feature experiments;
- `indirect_gap_direction` (1.0 on test, 0.9 on train).

It sits well inside the bound on:
- every error metric (total, indirect, direct; subgroup gaps and per-group effects);
- `rank_spearman` (0.938 / 0.983);
- `indirect_gap_capture` (0.673).

That headroom comes from where the paper's method falls short:
- In the age group with amplified mediation, BMI and blood pressure are nearly collinear.
- CAFÉ's mediator-conditioned direct contrast then collapses, so it overstates the mediated subgroup gap. The median is 2.3× the truth; the sign is always right.
- A counterfactual verifier at the same cost reaches capture 0.964 and total errors of 0.040 / 0.019.
- The subgroup experiment, its per-group and gap accuracy metrics, and the mirrored instances are scored. The reference and baselines were run on them.

## Brute force and baselines

- Exhaustive causal fuzzing needs 24 rows per audit row on Heart and is refused.
- Budget-constrained fuzzing (the paper's baseline) is −1.308 against all runs and ties among honest runs (+0.045).
- The simple direct-only baseline scores clearly below the reference in both cohorts, with room above the reference.

## Train vs test

The slices share protocol, metrics and size; they use different structural forms and seeds. Values are train / test:

| Method | Heart total error | Performance total error | Subgroup mediated-gap error | Subgroup capture |
|---|---|---|---|---|
| CAFÉ | 0.099 / 0.098 | 0.037 / 0.036 | 0.273 / 0.194 | 0.533 / 0.673 |
| Causal fuzzing | 0.104 / 0.093 | 0.041 / 0.034 | 0.061 / 0.046 | 0.967 / 0.958 |
| Abduction, half cost | 0.047 / 0.040 | 0.025 / 0.019 | 0.074 / 0.048 | 0.927 / 0.964 |
| Gradient-boosting CAFÉ | 0.054 / 0.063 | 0.034 / 0.035 | 0.147 / 0.126 | 0.826 / 0.835 |

- Honest methods score alike on both slices. The exception is CAFÉ's subgroup estimates, which vary strongly across instances.
- On the visible canonical (paper-style) instance, CAFÉ reports a large spurious gap: +4.97 against a true +0.40.

## Weights

- **Experiment weights unchanged:** 0.40 / 0.35 / 0.25.
- **`query_budget_fraction` coefficient 0.5 → 1.0 in both feature experiments.**
  - Efficiency relative to causal fuzzing is one of the paper's three listed contributions: design goal G4, RQ4, Table 3.
  - Once single-pass verifiers share the free floor, this metric measures exactly that contrast: one pass versus per-instance propagation.
  - At 0.5, budget-constrained fuzzing outranked CAFÉ among honest runs by +0.83, while scoring a full budget against CAFÉ's half.
- **New `indirect_gap_direction`, coefficient 0.5, primary for the subgroup experiment.**
  - It is the paper's actual Fig. 7 claim: the mediated gap exists and points to one age group.
  - It only became informative once the direction was mirrored.
- **Paper values kept.**
  - The paper reports no ground truth for the subgroup gap. Its earlier encoding (`indirect_gap_capture` 1.0 for CAFÉ) is now under `_paper_capture_encoding`.
  - CAFÉ's `indirect_gap_direction` is 1.0 and direct permutation's is 0.
  - All other paper values are unchanged.

## Could not fix

- **CAFÉ's subgroup magnitude.** CAFÉ overstates subgroup mediated gaps (capture 0.673 test / 0.533 train) against the paper's qualitative "captures". This is the method's positivity weakness. I did not change the data or the tolerance to bring it closer.
- **Ranking depends on the normalisation cohort.**
  - Causal fuzzing and the two-pass abduction variant rank below CAFÉ against all runs, but tie or rank above it among honest runs, because CAFÉ's direct and subgroup errors look large next to a tight honest cohort.
  - The gradient-boosting variant's all-runs interval touches 0.
- **Validator warnings.** `validate.py` warns that the harnesses "look detached from the method". That is by design: the evaluator runs each verifier against its oracle and scores the raw answers.
- **Not scored (unchanged scope):** the paper's real-world datasets (German, Adult, Drug), graph-misspecification robustness, and multi-feature targets.

## Reproduce

- `bash scripts/run.sh` runs the reference and baselines on both slices, plus `validate.py`. It passes.
- `bash notes/hardening/run_hardening.sh` runs all variants and shortcuts. It reuses cached raw answers in `notes/hardening/results/{test,train}/` and rescores them with the current evaluator.
- Earlier rounds are kept in `notes/hardening/results_round{1,2,3}/`.
