"""Honest verifier variants used to check that the hidden test rewards better
(and penalises worse) residual-influence estimation. Hardening evidence only;
the scored reference is method/cafe.py.

  probe_direct  CAFÉ, plus the unused half of the query budget spent on direct
                black-box probes (swap only f, hold everything else): direct :=
                probe mean; total := probe direct + CAFÉ's indirect (total -
                direct) estimate, or the probe alone when f has no mediators.
  hgb           CAFÉ with a gradient-boosting response model.
  hgb_probe     both of the above.
  abduction     counterfactual fuzzing: learned structural models with
                additive-noise abduction (cross-fitted residuals) propagate
                f <- theta for subsampled rows; direct by probes.
  direct_only   weaker ablation: report CAFÉ's direct effect as the total
                (ignores mediated influence).
  no_backdoor   weaker ablation: CAFÉ without the back-door adjustment set.
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import KFold

from baseline.direct_permutation import direct_contrasts, row_allocation
from data.blackbox import BlackBox
from data.causal_graph import descendants, load_tasks, parents, subgroup_mask, topological_order, write_answers
from method import cafe


def hgb_response(seed: int):
    return HistGradientBoostingRegressor(
        max_iter=300, learning_rate=0.05, min_samples_leaf=20, early_stopping=False, random_state=seed
    )


def _has_mediators(spec, feature):
    return any(d in spec["features"] for d in descendants(spec["edges"], feature))


def _probe_all(spec, audit, blackbox, seed):
    rng = np.random.default_rng(seed + 303)
    allocation = row_allocation(spec, 2, blackbox.remaining)
    probes = {}
    for feature in spec["estimate_features"]:
        rows = np.sort(rng.choice(len(audit), size=allocation[feature], replace=False))
        probes[feature] = (rows, direct_contrasts(spec, audit, blackbox, feature, rows))
    return probes


def _combine(spec, cafe_effects, probes, mask=None):
    out = {}
    for feature, values in cafe_effects.items():
        rows, contrast = probes[feature]
        inside = np.ones(len(rows), bool) if mask is None else mask[rows]
        if not inside.any():
            out[feature] = values
            continue
        direct = float(contrast[inside].mean())
        if _has_mediators(spec, feature):
            total = direct + (values["total"] - values["direct"])
        else:
            total = direct
        out[feature] = {"total": total, "direct": direct}
    return out


def cafe_probe(spec, audit, blackbox, seed, response=cafe.random_forest_response):
    answer = cafe.estimate_task(spec, audit, blackbox, seed=seed, response_model=response)
    probes = _probe_all(spec, audit, blackbox, seed)
    result = {"effects": _combine(spec, answer["effects"], probes)}
    if spec.get("subgroups"):
        result["subgroup_effects"] = {
            name: _combine(spec, answer["subgroup_effects"][name], probes, subgroup_mask(audit, rule))
            for name, rule in spec["subgroups"].items()
        }
    return result


def _crossfit_models(audit, spec, seed):
    models = {}
    for node in spec["features"]:
        node_parents = [p for p in parents(spec["edges"], node) if p in spec["features"]]
        if not node_parents:
            continue
        x = audit[node_parents].to_numpy(float)
        y = audit[node].to_numpy(float)
        oof = np.zeros(len(y))
        for train, held in KFold(5, shuffle=True, random_state=seed).split(x):
            model = RandomForestRegressor(n_estimators=60, min_samples_leaf=10, random_state=seed, n_jobs=1)
            model.fit(x[train], y[train])
            oof[held] = model.predict(x[held])
        final = RandomForestRegressor(n_estimators=80, min_samples_leaf=10, random_state=seed, n_jobs=1)
        final.fit(x, y)
        models[node] = (node_parents, final, y - oof)
    return models


def _abduct(sample, rows, spec, models, feature, value):
    out = sample.copy()
    out[feature] = value
    changed = {feature}
    downstream = descendants(spec["edges"], feature)
    for node in topological_order(spec["features"], spec["edges"]):
        if node == feature or node not in downstream or node not in models:
            continue
        node_parents, model, residual = models[node]
        if changed.intersection(node_parents):
            out[node] = model.predict(out[node_parents].to_numpy(float)) + residual[rows]
            changed.add(node)
    return out


def abduction(spec, audit, blackbox, seed):
    rng = np.random.default_rng(seed)
    models = _crossfit_models(audit, spec, seed + 5)
    allocation = row_allocation(spec, 4, blackbox.remaining)
    effects, per_row = {}, {}
    for feature in spec["estimate_features"]:
        lo, hi = spec["interventions"][feature]
        rows = np.sort(rng.choice(len(audit), size=allocation[feature], replace=False))
        sample = audit.iloc[rows].reset_index(drop=True)
        d_lo, d_hi = sample.copy(), sample.copy()
        d_lo[feature], d_hi[feature] = lo, hi
        batch = pd.concat(
            [_abduct(sample, rows, spec, models, feature, lo), _abduct(sample, rows, spec, models, feature, hi), d_lo, d_hi],
            ignore_index=True,
        )
        preds = blackbox.predict(batch).reshape(4, len(rows))
        total, direct = preds[1] - preds[0], preds[3] - preds[2]
        per_row[feature] = (rows, total, direct)
        effects[feature] = {"total": float(total.mean()), "direct": float(direct.mean())}
    answer = {"effects": effects}
    if spec.get("subgroups"):
        answer["subgroup_effects"] = {}
        for name, rule in spec["subgroups"].items():
            mask = subgroup_mask(audit, rule)
            group = {}
            for feature in spec["subgroup_features"]:
                rows, total, direct = per_row[feature]
                inside = mask[rows]
                group[feature] = {
                    "total": float(total[inside].mean()) if inside.any() else 0.0,
                    "direct": float(direct[inside].mean()) if inside.any() else 0.0,
                }
            answer["subgroup_effects"][name] = group
    return answer


def _map_effects(answer, fn):
    out = {"effects": {f: fn(f, v) for f, v in answer["effects"].items()}}
    if "subgroup_effects" in answer:
        out["subgroup_effects"] = {
            g: {f: fn(f, v) for f, v in entries.items()} for g, entries in answer["subgroup_effects"].items()
        }
    return out


def direct_only(spec, audit, blackbox, seed):
    answer = cafe.estimate_task(spec, audit, blackbox, seed=seed)
    return _map_effects(answer, lambda f, v: {"total": v["direct"], "direct": v["direct"]})


def no_backdoor(spec, audit, blackbox, seed):
    frame = audit.copy()
    frame[cafe.PREDICTION] = blackbox.predict(audit)

    def effects(rows, features):
        out = {}
        for feature in features:
            lo, hi = spec["interventions"][feature]
            _, mediators = cafe.adjustment_sets(spec, feature)
            out[feature] = {
                "total": cafe.adjusted_contrast(rows, feature, [], lo, hi, seed),
                "direct": cafe.adjusted_contrast(rows, feature, mediators, lo, hi, seed + 101),
            }
        return out

    answer = {"effects": effects(frame, spec["estimate_features"])}
    if spec.get("subgroups"):
        answer["subgroup_effects"] = {
            name: effects(frame[subgroup_mask(audit, rule)], spec["subgroup_features"])
            for name, rule in spec["subgroups"].items()
        }
    return answer


VARIANTS = {
    "probe_direct": lambda s, a, b, seed: cafe_probe(s, a, b, seed),
    "hgb": lambda s, a, b, seed: cafe.estimate_task(s, a, b, seed=seed, response_model=hgb_response),
    "hgb_probe": lambda s, a, b, seed: cafe_probe(s, a, b, seed, response=hgb_response),
    "abduction": abduction,
    "direct_only": direct_only,
    "no_backdoor": no_backdoor,
}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", required=True, choices=sorted(VARIANTS))
    parser.add_argument("--tasks-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args(argv)
    answers = {}
    for spec, audit in load_tasks(args.tasks_dir):
        answers[spec["task_id"]] = VARIANTS[args.variant](spec, audit, BlackBox(spec), args.seed)
    write_answers(args.output, answers)


if __name__ == "__main__":
    main()
