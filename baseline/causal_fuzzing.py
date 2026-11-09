"""Causal fuzzing oracle (paper Algorithm 1) under the task's query budget.

For each feature f, structural models H_v (lightweight regressions of every
node on its graph parents, trained on the observational audit rows) propagate
an intervention f <- theta through f's descendants in topological order; the
black box is queried on the propagated rows (total influence) and on rows
where only f changed (direct influence, propagation skipped). Algorithm 1
evaluates every row; here rows are subsampled so the four model queries per
row and feature fit the same oracle budget every verifier gets.

Run as a verifier:  python -m baseline.causal_fuzzing --tasks-dir DIR --output answers.json
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from baseline.direct_permutation import row_allocation
from data.blackbox import BlackBox
from data.causal_graph import descendants, load_tasks, parents, subgroup_mask, topological_order, write_answers


def fit_structural_models(audit: pd.DataFrame, spec: dict, seed: int) -> dict:
    models = {}
    for node in spec["features"]:
        node_parents = [p for p in parents(spec["edges"], node) if p in spec["features"]]
        if not node_parents:
            continue
        model = RandomForestRegressor(n_estimators=80, min_samples_leaf=10, random_state=seed, n_jobs=1)
        model.fit(audit[node_parents].to_numpy(dtype=float), audit[node].to_numpy(dtype=float))
        models[node] = (node_parents, model)
    return models


def propagate(sample: pd.DataFrame, spec: dict, models: dict, feature: str, value: float) -> pd.DataFrame:
    rows = sample.copy()
    rows[feature] = value
    changed = {feature}
    downstream = descendants(spec["edges"], feature)
    for node in topological_order(spec["features"], spec["edges"]):
        if node == feature or node not in downstream or node not in models:
            continue
        node_parents, model = models[node]
        if changed.intersection(node_parents):
            rows[node] = model.predict(rows[node_parents].to_numpy(dtype=float))
            changed.add(node)
    return rows


def estimate_task(spec: dict, audit: pd.DataFrame, blackbox: BlackBox, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    models = fit_structural_models(audit, spec, seed + 19)
    allocation = row_allocation(spec, 4, blackbox.remaining)
    effects, per_row = {}, {}
    for feature in spec["estimate_features"]:
        lo, hi = spec["interventions"][feature]
        rows = np.sort(rng.choice(len(audit), size=allocation[feature], replace=False))
        sample = audit.iloc[rows].reset_index(drop=True)
        direct_lo, direct_hi = sample.copy(), sample.copy()
        direct_lo[feature] = lo
        direct_hi[feature] = hi
        batch = pd.concat(
            [
                propagate(sample, spec, models, feature, lo),
                propagate(sample, spec, models, feature, hi),
                direct_lo,
                direct_hi,
            ],
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


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tasks-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args(argv)
    answers = {}
    for spec, audit in load_tasks(args.tasks_dir):
        answers[spec["task_id"]] = estimate_task(spec, audit, BlackBox(spec), seed=args.seed)
    write_answers(args.output, answers)


if __name__ == "__main__":
    main()
