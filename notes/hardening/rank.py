"""Rank hardening runs with the gym's rule and check noise with paired bootstraps.

rank(m) = sum_experiments weight * sum_metrics |coefficient| * direction *
          (value_m - value_reference) / sigma_metric
direction comes from higher_is_better, sigma is the population std of the
metric over the ranked cohort (zero-variance metrics contribute 0). The
reference is the ``cafe`` entry. Paired bootstraps resample held-out tasks
(the same tasks for both methods) to put an interval on rank differences.

Cohorts: all hardening runs; honest runs only; and, per shortcut, the honest
runs plus that one shortcut (the shortcut's score there is reported in
``shortcut_vs_honest``). Pure Python (no numpy), so it can be rerun anywhere.

Usage: python notes/hardening/rank.py [results_dir]   (default notes/hardening/results/)
"""

from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "notes" / "hardening" / "results"
REFERENCE = "cafe"
SEEDS = ("cafe", "cafe_seed11", "cafe_seed19")
CAP = 2.0
POOLED = {
    "total_effect_nmae": ("total_err", CAP),
    "indirect_effect_nmae": ("indirect_err", CAP),
    "direct_effect_nmae": ("direct_err", CAP),
    "residual_capture": ("capture", 0.0),
    "false_alarm_rate": ("false_alarms", 0.0),
    "indirect_gap_nmae": ("indirect_gap_err", CAP),
    "total_gap_nmae": ("total_gap_err", CAP),
    "direct_gap_nmae": ("direct_gap_err", CAP),
    "subgroup_effect_nmae": ("effect_err", CAP),
    "indirect_gap_capture": ("gap_capture", 0.0),
}


def metric_specs(reference: dict) -> list[tuple]:
    return [
        (exp, metric, body["weight"], abs(spec["coefficient"]), 1.0 if spec["higher_is_better"] else -1.0)
        for exp, body in reference["experiments"].items()
        for metric, spec in body["metrics"].items()
    ]


def rank_cohort(table: dict, members: list[str], specs: list[tuple]) -> tuple[dict, dict]:
    sigma = {
        (exp, metric): statistics.pstdev([table[exp][m][metric] for m in members])
        for exp, metric, *_ in specs
    }
    scores = {}
    for m in members:
        terms = {}
        for exp, metric, weight, coef, direction in specs:
            s = sigma[(exp, metric)]
            delta = direction * (table[exp][m][metric] - table[exp][REFERENCE][metric])
            terms[f"{exp}/{metric}"] = weight * coef * delta / s if s > 0 else 0.0
        scores[m] = {"score": float(sum(terms.values())), "terms": terms}
    return scores, sigma


def _mean(values) -> float:
    values = list(values)
    return float(sum(values) / len(values))


def _percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q / 100.0
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    return float(ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo))


def aggregate(records: list[dict], idx: list[int], metric: str) -> float:
    if metric == "rank_spearman":
        return _mean(records[i]["spearman"] for i in idx)
    if metric == "query_budget_fraction":
        return _mean(records[i]["query_fraction"] for i in idx)
    key, empty = POOLED[metric]
    values = [v for i in idx for v in records[i][key]]
    return _mean(values) if values else empty


def paired_bootstrap(details, method, specs, sigma, n_boot=2000, seed=0) -> dict:
    rng = random.Random(seed)
    experiments = sorted({exp for exp, *_ in specs})
    sizes = {exp: len(details[REFERENCE][exp]) for exp in experiments}

    def score_difference(index):
        total = 0.0
        for exp, metric, weight, coef, direction in specs:
            s = sigma[(exp, metric)]
            if s <= 0:
                continue
            a = aggregate(details[method][exp], index[exp], metric)
            b = aggregate(details[REFERENCE][exp], index[exp], metric)
            total += weight * coef * direction * (a - b) / s
        return total

    point = score_difference({exp: list(range(n)) for exp, n in sizes.items()})
    draws = [
        score_difference({exp: [rng.randrange(n) for _ in range(n)] for exp, n in sizes.items()})
        for _ in range(n_boot)
    ]
    lo, hi = _percentile(draws, 2.5), _percentile(draws, 97.5)
    return {"point": float(point), "ci95": [lo, hi], "p_not_better": float(_mean(d <= 0 for d in draws))}


def task_wins(details, method, exp, key) -> str:
    wins = ties = 0
    pairs = list(zip(details[method][exp], details[REFERENCE][exp]))
    for mine, ref in pairs:
        a, b = _mean(mine[key]), _mean(ref[key])
        wins += a < b - 1e-12
        ties += abs(a - b) <= 1e-12
    return f"{wins}/{len(pairs)} better, {ties} tied"


def main() -> None:
    global RESULTS
    if len(sys.argv) > 1:
        RESULTS = Path(sys.argv[1]).resolve()
    reference = json.loads((ROOT / "scoring" / "reference.json").read_text())
    specs = metric_specs(reference)
    test = json.loads((RESULTS / "scores_test_all.json").read_text())
    details = json.loads((RESULTS / "details_test.json").read_text())
    table = {exp: body["results"] for exp, body in test["experiments"].items()}
    methods = sorted(table[specs[0][0]])
    cohorts = {
        "all_hardening_runs": methods,
        "honest_runs": [m for m in methods if not m.startswith("shortcut_")],
    }
    summary = {"rule": __doc__.split("\n\n")[1], "cohorts": {}, "diagnostics": test.get("_diagnostics", {})}
    lines = []
    for label, members in cohorts.items():
        scores, sigma = rank_cohort(table, members, specs)
        seed_scores = [scores[s]["score"] for s in SEEDS if s in scores]
        spread = max(seed_scores) - min(seed_scores) if seed_scores else None
        boots = {
            m: paired_bootstrap(details, m, specs, sigma)
            for m in members
            if m != REFERENCE and m in details and not test["_diagnostics"][m].get("failed_tasks")
        }
        summary["cohorts"][label] = {
            "members": members,
            "scores": scores,
            "sigma": {f"{e}/{k}": v for (e, k), v in sigma.items()},
            "reference_seed_spread": spread,
            "paired_bootstrap_vs_reference": boots,
        }
        lines.append(f"## cohort {label}: reference seed spread = {spread:.4f}")
        lines.append("| method | rank score vs cafe | paired 95% CI | failed tasks |")
        lines.append("|---|---:|---|---:|")
        for m, body in sorted(scores.items(), key=lambda kv: -kv[1]["score"]):
            ci = boots.get(m, {}).get("ci95")
            ci_text = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "-"
            failed = test["_diagnostics"][m]["failed_tasks"]
            lines.append(f"| {m} | {body['score']:+.4f} | {ci_text} | {failed} |")
        lines.append("")
    honest = cohorts["honest_runs"]
    shortcut_rows = {}
    for m in methods:
        if not m.startswith("shortcut_"):
            continue
        scores, sigma = rank_cohort(table, honest + [m], specs)
        boot = None
        if m in details and not test["_diagnostics"][m].get("failed_tasks"):
            boot = paired_bootstrap(details, m, specs, sigma)
        shortcut_rows[m] = {"score": scores[m]["score"], "bootstrap": boot, "terms": scores[m]["terms"]}
    summary["shortcut_vs_honest"] = shortcut_rows
    lines.append("## each shortcut ranked in a cohort of the honest runs plus that shortcut")
    lines.append("| shortcut | rank score vs cafe | paired 95% CI |")
    lines.append("|---|---:|---|")
    for m, body in sorted(shortcut_rows.items(), key=lambda kv: -kv[1]["score"]):
        ci = (body["bootstrap"] or {}).get("ci95")
        ci_text = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci else "-"
        lines.append(f"| {m} | {body['score']:+.4f} | {ci_text} |")
    lines.append("")
    lines.append("## raw test metrics")
    for exp, results in table.items():
        metrics = list(reference["experiments"][exp]["metrics"])
        lines.append(f"### {exp}")
        lines.append("| method | " + " | ".join(metrics) + " |")
        lines.append("|---|" + "---:|" * len(metrics))
        for m in methods:
            lines.append(f"| {m} | " + " | ".join(f"{results[m][k]:.4f}" for k in metrics) + " |")
        lines.append("")
    lines.append("## per-task paired comparison vs cafe (lower per-task error)")
    for m in methods:
        if m == REFERENCE or test["_diagnostics"][m].get("failed_tasks"):
            continue
        parts = [
            f"heart total {task_wins(details, m, 'heart_disease_feature_unlearning', 'total_err')}",
            f"perf total {task_wins(details, m, 'performance_feature_unlearning', 'total_err')}",
            f"subgroup indirect gap {task_wins(details, m, 'heart_disease_subgroup_unlearning', 'indirect_gap_err')}",
        ]
        lines.append(f"- {m}: " + "; ".join(parts))
    train_path = RESULTS / "scores_train_all.json"
    if train_path.is_file():
        train = json.loads(train_path.read_text())
        lines.append("")
        lines.append("## train vs test (honest runs)")
        for exp, body in train["experiments"].items():
            metrics = list(reference["experiments"][exp]["metrics"])
            lines.append(f"### {exp}")
            lines.append("| method | " + " | ".join(f"{k} train/test" for k in metrics) + " |")
            lines.append("|---|" + "---|" * len(metrics))
            for m, values in sorted(body["results"].items()):
                if m in table[exp]:
                    cells = [f"{values[k]:.3f}/{table[exp][m][k]:.3f}" for k in metrics]
                    lines.append(f"| {m} | " + " | ".join(cells) + " |")
            lines.append("")
    (RESULTS / "rank_summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True))
    (RESULTS / "rank_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
