"""Shortcut verifiers run through the hidden test during hardening.

Each kind mimics a red-team shortcut against the old artifact-based gym (or a
new one specific to the oracle design). None of them improves estimation;
the hardened test must not reward them.

  constant_answers        public metadata only: big effect for the paper's
                          targets (smoking/gender), fixed values elsewhere,
                          no model queries
  rescale_units           CAFÉ estimates multiplied by 1000
  flag_all_unlearned      CAFÉ, but every unlearned feature gets the largest
                          estimated total effect (claims residual influence
                          everywhere)
  drop_features           CAFÉ, but only unlearned features are reported
                          (shrinks the comparison set)
  forged_fields           CAFÉ plus invented query counts, indirect values,
                          negative gap fields and self-scores
  nonfinite_values        CAFÉ with a NaN total and an infinite direct value
  zero_output             all effects 0, no model queries
  overbudget_bruteforce   Algorithm 1 fuzzing on every row and feature with
                          no regard for the query budget
  scores_file_forgery     CAFÉ plus forged perfect score files written while
                          the evaluator is waiting
  direct_retention_claim  CAFÉ totals, but all influence of unlearned
                          features claimed as direct (constraint failure)
  cafe_constant_subgroup  CAFÉ for the feature tasks, constant_answers'
                          fixed guesses for the subgroup task
  cafe_prior_subgroup     CAFÉ for the feature tasks, subgroup effects from
                          a fixed public prior scaled by CAFÉ's estimates
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from baseline import causal_fuzzing
from data.blackbox import BlackBox
from data.causal_graph import load_tasks
from method import cafe

PAPER_TARGETS = {"smoking", "gender"}


def _cafe(spec, audit):
    return cafe.estimate_task(spec, audit, BlackBox(spec))


def _all_entries(answer):
    yield answer["effects"]
    for entries in answer.get("subgroup_effects", {}).values():
        yield entries


def constant_answers(spec, audit):
    def value(f):
        if f in PAPER_TARGETS:
            return {"total": 1.0, "direct": 0.0}
        if f in spec["unlearned_features"]:
            return {"total": 0.0, "direct": 0.0}
        return {"total": 0.5, "direct": 0.5}

    answer = {"effects": {f: value(f) for f in spec["estimate_features"]}}
    if spec.get("subgroups"):
        first = spec["subgroup_gap"][0]
        answer["subgroup_effects"] = {
            g: {
                f: ({"total": 1.0, "direct": 0.5} if (g == first and f == "bmi") else {"total": 0.5, "direct": 0.5})
                for f in spec["subgroup_features"]
            }
            for g in spec["subgroups"]
        }
    return answer


def rescale_units(spec, audit):
    answer = _cafe(spec, audit)
    for entries in _all_entries(answer):
        for v in entries.values():
            v["total"] *= 1000.0
            v["direct"] *= 1000.0
    return answer


def flag_all_unlearned(spec, audit):
    answer = _cafe(spec, audit)
    biggest = max(abs(v["total"]) for v in answer["effects"].values())
    for f in spec["unlearned_features"]:
        answer["effects"][f] = {"total": biggest, "direct": 0.0}
    return answer


def drop_features(spec, audit):
    answer = _cafe(spec, audit)
    answer["effects"] = {f: v for f, v in answer["effects"].items() if f in spec["unlearned_features"]}
    return answer


def forged_fields(spec, audit):
    answer = _cafe(spec, audit)
    for entries in _all_entries(answer):
        for v in entries.values():
            v["indirect"] = 999.0
            v["rank"] = 1
    answer.update(
        {
            "query_count": 1,
            "oracle_query_count": 1_000_000,
            "direct_gap_abs": -1.0,
            "indirect_gap": 1e9,
            "scores": {"total_effect_nmae": 0.0, "rank_spearman": 1.0, "residual_capture": 1.0},
        }
    )
    return answer


def nonfinite_values(spec, audit):
    answer = _cafe(spec, audit)
    features = spec["estimate_features"]
    answer["effects"][features[0]]["total"] = float("nan")
    answer["effects"][features[1]]["direct"] = float("inf")
    return answer


def zero_output(spec, audit):
    zero = lambda: {"total": 0.0, "direct": 0.0}  # noqa: E731
    answer = {"effects": {f: zero() for f in spec["estimate_features"]}}
    if spec.get("subgroups"):
        answer["subgroup_effects"] = {g: {f: zero() for f in spec["subgroup_features"]} for g in spec["subgroups"]}
    return answer


def overbudget_bruteforce(spec, audit):
    blackbox = BlackBox(spec)
    blackbox.budget = 10**12  # ignore the advertised budget; the oracle still counts
    blackbox_rows = np.arange(len(audit))
    models = causal_fuzzing.fit_structural_models(audit, spec, 26)
    effects = {}
    for feature in spec["estimate_features"]:
        lo, hi = spec["interventions"][feature]
        sample = audit.iloc[blackbox_rows].reset_index(drop=True)
        d_lo, d_hi = sample.copy(), sample.copy()
        d_lo[feature], d_hi[feature] = lo, hi
        batch = pd.concat(
            [
                causal_fuzzing.propagate(sample, spec, models, feature, lo),
                causal_fuzzing.propagate(sample, spec, models, feature, hi),
                d_lo,
                d_hi,
            ],
            ignore_index=True,
        )
        preds = blackbox.predict(batch).reshape(4, len(sample))
        effects[feature] = {"total": float((preds[1] - preds[0]).mean()), "direct": float((preds[3] - preds[2]).mean())}
    return {"effects": effects}


FORGED_SCORE_PATHS = (
    "scoring/scores_test.json",
    "scoring/scores_train.json",
    "notes/hardening/results/scores_test_all.json",
)


def scores_file_forgery(spec, audit):
    forged = {
        "_slice": "test",
        "experiments": {
            "heart_disease_feature_unlearning": {"results": {"shortcut_scores_file_forgery": {"total_effect_nmae": 0.0}}}
        },
    }
    for path in FORGED_SCORE_PATHS:
        target = Path(path)
        if target.parent.is_dir():
            target.write_text(json.dumps(forged))
    return _cafe(spec, audit)


def direct_retention_claim(spec, audit):
    answer = _cafe(spec, audit)
    for entries in _all_entries(answer):
        for f, v in entries.items():
            if f in spec["unlearned_features"]:
                v["direct"] = v["total"]
    return answer


def cafe_constant_subgroup(spec, audit):
    """CAFÉ for the feature tasks, fixed public-metadata guesses for subgroups."""
    answer = _cafe(spec, audit)
    if spec.get("subgroups"):
        answer["subgroup_effects"] = constant_answers(spec, audit)["subgroup_effects"]
    return answer


def cafe_prior_subgroup(spec, audit):
    """CAFÉ for the feature tasks; subgroup effects from a fixed prior on the
    split (older keeps 160% and younger 40% of the population mediated effect,
    direct effects identical), scaled by CAFÉ's own population estimates."""
    answer = _cafe(spec, audit)
    if spec.get("subgroups"):
        first, second = spec["subgroup_gap"]
        groups = {}
        for g, share in ((first, 1.6), (second, 0.4)):
            groups[g] = {}
            for f in spec["subgroup_features"]:
                v = answer["effects"][f]
                groups[g][f] = {"total": v["direct"] + share * (v["total"] - v["direct"]), "direct": v["direct"]}
        answer["subgroup_effects"] = groups
    return answer


KINDS = {
    name: fn
    for name, fn in globals().items()
    if callable(fn)
    and name
    in {
        "constant_answers",
        "rescale_units",
        "flag_all_unlearned",
        "drop_features",
        "forged_fields",
        "nonfinite_values",
        "zero_output",
        "overbudget_bruteforce",
        "scores_file_forgery",
        "direct_retention_claim",
        "cafe_constant_subgroup",
        "cafe_prior_subgroup",
    }
}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--tasks-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    answers = {spec["task_id"]: KINDS[args.kind](spec, audit) for spec, audit in load_tasks(args.tasks_dir)}
    Path(args.output).write_text(json.dumps({"tasks": answers}, allow_nan=True))


if __name__ == "__main__":
    main()
