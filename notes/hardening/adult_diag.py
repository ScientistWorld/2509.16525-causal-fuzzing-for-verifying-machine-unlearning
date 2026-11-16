"""Calibration check for the Adult-Income experiment (hardening evidence only).

Builds the Adult tasks of one slice, prints the generated data against the
real rows, the audited models' held-out quality and each task's exact truth
(total / direct influence per feature, scale, verdict items), then scores a
subset of the hardening registry on those tasks only.

Usage: python notes/hardening/adult_diag.py {test,train} OUT_DIR [verifier ...]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> None:
    slice_name, out_dir, names = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
    out_dir.mkdir(parents=True, exist_ok=True)
    start = time.time()
    if slice_name == "test":
        from eval.test import harness
        from eval.test import tasks as plan_module
        from eval.test.adult import HeldOutAdult as family
        from eval.test.adult import load_real_rows

        real = load_real_rows()
        plan = [p for p in plan_module._plan(False) if p[1] is family]
        items = [
            dict(task_id=t, family=f, seed=s, architecture=a, control_active=c, target_retained=r, params=None)
            for t, f, s, a, c, r in plan
        ]
    else:
        from data.adult_semisynthetic import AdultIncomeSCM as family
        from data.adult_semisynthetic import load_adult
        from eval.train import harness
        from eval.train import tasks as plan_module

        real = load_adult()
        items = [p for p in plan_module._plan(False) if p["family"] is family]
    tasks, report = {}, []
    for item in items:
        t0 = time.time()
        task = harness.build_task(
            item["task_id"], item["family"], item["seed"], item["architecture"], item["control_active"],
            item["target_retained"], n_total=plan_module.ADULT_TOTAL, n_audit=plan_module.N_AUDIT,
            params=item.get("params"),
        )
        tasks[task.task_id] = task
        truth = task.truth
        audit = task.audit
        preds = task.predict(audit.to_numpy(dtype=float))
        row = {
            "task_id": task.task_id,
            "architecture": item["architecture"],
            "control_active": item["control_active"],
            "target_retained": item["target_retained"],
            "build_s": round(time.time() - t0, 1),
            "scale": round(truth["scale"], 4),
            "pred_mean": round(float(preds.mean()), 3),
            "pred_sd": round(float(preds.std()), 3),
            "rel_total": {f: round(v / truth["scale"], 3) for f, v in truth["total"].items()},
            "rel_direct": {f: round(v / truth["scale"], 3) for f, v in truth["direct"].items()},
            "positives": truth["positives"],
            "negatives": truth["negatives"],
            "verdict_residual": truth["verdict_residual"],
            "verdict_clear": truth["verdict_clear"],
            "interventions": task.spec["interventions"],
            "audit_means": {f: round(float(audit[f].mean()), 3) for f in audit.columns},
        }
        report.append(row)
        print(json.dumps(row), flush=True)
    print("real means:", {f: round(float(real[f].mean()), 3) for f in real.columns}, flush=True)
    unlearned = [(r["task_id"], f, r["rel_total"][f]) for r in report for f in ("sex", "race", "native_country")]
    print("unlearned |rel total| sorted:", sorted(round(abs(v), 3) for _, _, v in unlearned), flush=True)
    print(
        "verdict items: residual", sum(len(r["verdict_residual"]) for r in report),
        "clear", sum(len(r["verdict_clear"]) for r in report),
        "exact zero", sum(len(r["negatives"]) for r in report),
        "capture positives", sum(len(r["positives"]) for r in report),
        flush=True,
    )
    print(f"built {len(tasks)} adult tasks in {time.time() - start:.1f}s", flush=True)
    (out_dir / f"truth_{slice_name}.json").write_text(json.dumps(report, indent=1))
    if not names:
        return
    verifiers = harness.discover_verifiers(ROOT / "notes" / "hardening" / "registry", names)
    scores = harness.evaluate(
        tasks, verifiers, slice_name, per_method_dir=out_dir / slice_name,
        details_path=out_dir / f"details_{slice_name}.json",
    )
    (out_dir / f"scores_{slice_name}.json").write_text(json.dumps(scores, indent=1, sort_keys=True))
    print(f"done in {time.time() - start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
