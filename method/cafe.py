"""CAFÉ: Causal-Aware Fast Estimator (paper Algorithm 2, Definition 4).

For every feature f the verifier must report:
  * total influence  - Def. 4 with Z_f = a valid back-door set (parents of f):
        sum_z P(z) [ E[M'(X) | Z=z, X_f=theta_hi] - E[M'(X) | Z=z, X_f=theta_lo] ]
  * direct influence - the same contrast after also conditioning on the
        mediators (descendants of f), i.e. with every other path blocked;
  * indirect influence is total - direct (computed by the evaluator).

E[M'(X) | f, Z] is estimated with a lightweight regression model fitted on the
black-box predictions of the audit rows (one oracle query per audit row), and
the adjusted contrast is averaged over the empirical distribution of Z
(back-door formula, Eq. 3). Subgroup targets use the rows of the subgroup.

Run as a verifier:  python -m method.cafe --tasks-dir DIR --output answers.json
"""

from __future__ import annotations

import argparse
from typing import Callable

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from data.blackbox import BlackBox
from data.causal_graph import descendants, load_tasks, parents, subgroup_mask, write_answers

PREDICTION = "__prediction__"


def random_forest_response(seed: int):
    return RandomForestRegressor(n_estimators=80, min_samples_leaf=12, random_state=seed, n_jobs=1)


def adjusted_contrast(
    frame: pd.DataFrame,
    feature: str,
    controls: list[str],
    theta_lo: float,
    theta_hi: float,
    seed: int,
    response_model: Callable[[int], object] = random_forest_response,
) -> float:
    """Back-door adjusted expected-prediction contrast for ``feature``."""

    controls = [c for c in controls if c != feature]
    target = frame[PREDICTION].to_numpy(dtype=float)
    if abs(theta_hi - theta_lo) < 1e-12 or len(frame) < 2 or target.std() < 1e-12:
        return 0.0
    columns = [feature] + controls
    design = frame[columns].to_numpy(dtype=float)
    model = response_model(seed)
    model.fit(design, target)
    low, high = design.copy(), design.copy()
    low[:, 0] = theta_lo
    high[:, 0] = theta_hi
    return float(np.mean(model.predict(high) - model.predict(low)))


def adjustment_sets(spec: dict, feature: str) -> tuple[list[str], list[str]]:
    """(back-door set Z_f, mediators M_f) read off the supplied causal graph."""

    features = set(spec["features"])
    backdoor = [p for p in parents(spec["edges"], feature) if p in features]
    mediators = sorted(d for d in descendants(spec["edges"], feature) if d in features)
    return backdoor, mediators


def cafe_effects(
    frame: pd.DataFrame,
    spec: dict,
    features: list[str],
    seed: int,
    response_model: Callable[[int], object] = random_forest_response,
) -> dict[str, dict[str, float]]:
    effects = {}
    for feature in features:
        theta_lo, theta_hi = spec["interventions"][feature]
        backdoor, mediators = adjustment_sets(spec, feature)
        total = adjusted_contrast(frame, feature, backdoor, theta_lo, theta_hi, seed, response_model)
        direct = adjusted_contrast(
            frame, feature, backdoor + mediators, theta_lo, theta_hi, seed + 101, response_model
        )
        effects[feature] = {"total": total, "direct": direct}
    return effects


def estimate_task(
    spec: dict,
    audit: pd.DataFrame,
    blackbox: BlackBox,
    seed: int = 7,
    response_model: Callable[[int], object] = random_forest_response,
) -> dict:
    frame = audit.copy()
    frame[PREDICTION] = blackbox.predict(audit)
    answer = {"effects": cafe_effects(frame, spec, spec["estimate_features"], seed, response_model)}
    if spec.get("subgroups"):
        answer["subgroup_effects"] = {
            name: cafe_effects(
                frame[subgroup_mask(audit, rule)], spec, spec["subgroup_features"], seed, response_model
            )
            for name, rule in spec["subgroups"].items()
        }
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
        print(f"cafe: {spec['task_id']} done", flush=True)
    write_answers(args.output, answers)


if __name__ == "__main__":
    main()
