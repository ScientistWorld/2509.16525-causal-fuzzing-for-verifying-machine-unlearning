"""Evaluator harness for residual-influence verification.

The evaluator owns everything on the far side of the comparison: the
data-generating process, the audited black-box models, the intervention
contrasts, the query budget, the ground truth and the thresholds. A verifier
is any executable ``<verifiers_dir>/<name>.sh``; it is run as a separate
process as ``bash <name>.sh <tasks_dir> <answers.json>`` and can reach the
audited models only through a counted prediction oracle. Every scored number
is recomputed here from the verifier's raw per-feature effect estimates.
This module never imports method code.
"""

from __future__ import annotations

import json
import math
import os
import re
import secrets
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass, field
from multiprocessing.connection import Client, Listener
from pathlib import Path

# One thread for OpenMP/BLAS in the evaluator and (inherited) in every verifier:
# keeps the audited models deterministic and avoids oversubscribing small CPU
# allocations. Must be set before numpy / scikit-learn load their runtimes.
for _variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_variable] = "1"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

try:  # also cap pools that were already initialised
    from threadpoolctl import threadpool_limits

    threadpool_limits(1)
except Exception:  # pragma: no cover
    pass

WORKSPACE = Path(__file__).resolve().parents[2]
DEFAULT_VERIFIERS_DIR = WORKSPACE / "scripts" / "verifiers"
ADDRESS_ENV = "UNLEARN_ORACLE_ADDRESS"
AUTHKEY_ENV = "UNLEARN_ORACLE_AUTHKEY"

QUERY_BUDGET_PER_ROW = 2          # oracle rows allowed per audit row
MAX_ROWS_PER_REQUEST = 100_000
MAX_COLS = 64
ERROR_CAP = 2.0                   # per-quantity normalized error cap (failed tasks get it)
DETECT_FRACTION = 0.10            # |estimate| >= 0.10 * scale counts as "influence found"
POSITIVE_FRACTION = 0.20          # unlearned features with |truth| >= 0.20 * scale are positives
GAP_FRACTION = 0.20               # subgroup indirect gaps >= 0.20 * subgroup scale are scored for capture
SOLVED_FRACTION = 0.5             # efficiency credit needs total error <= 0.5 * the all-zero answer's
VERDICT_CLEAR_FRACTION = 0.09     # verdict items: unlearned features with |truth| <= 9% of scale must pass ...
VERDICT_RESIDUAL_FRACTION = 0.11  # ... and those with |truth| >= 11% must be flagged (flag: |estimate| >= 10%)
# Verifier limits. CPU seconds per process (independent of machine load) is the
# binding limit; the wall-clock backstop only ends verifiers that hang idle and
# is ~50x the slowest registered verifier's run time.
VERIFIER_CPU_LIMIT_S = 3 * 3600
VERIFIER_TIMEOUT_S = 5 * 3600
_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")

FEATURE_EXPERIMENTS = {
    "heart_disease": "heart_disease_feature_unlearning",
    "performance": "performance_feature_unlearning",
    "adult_income": "adult_feature_unlearning",
}
SUBGROUP_EXPERIMENT = "heart_disease_subgroup_unlearning"
VERDICT_EXPERIMENTS = {"adult_feature_unlearning"}
EXPERIMENTS = (
    "heart_disease_feature_unlearning",
    "performance_feature_unlearning",
    SUBGROUP_EXPERIMENT,
    "adult_feature_unlearning",
)


# ── tasks and ground truth ───────────────────────────────────────────────────


@dataclass
class Task:
    task_id: str
    spec: dict
    audit: pd.DataFrame
    model: object
    model_columns: list[int]
    truth: dict = field(default_factory=dict)

    @property
    def family(self) -> str:
        return self.spec["family"]

    def predict(self, rows: np.ndarray) -> np.ndarray:
        rows = np.asarray(rows, dtype=float)
        return np.asarray(self.model.predict(rows[:, self.model_columns]), dtype=float).reshape(-1)


_OPS = {">": np.greater, ">=": np.greater_equal, "<": np.less, "<=": np.less_equal}


def subgroup_mask(frame: pd.DataFrame, rule: dict) -> np.ndarray:
    return _OPS[rule["op"]](frame[rule["feature"]].to_numpy(dtype=float), float(rule["threshold"]))


def intervention_values(audit: pd.DataFrame, features: list[str], binary: list[str]) -> dict:
    values = {}
    for feature in features:
        if feature in binary:
            values[feature] = [0.0, 1.0]
        else:
            column = audit[feature].to_numpy(dtype=float)
            for q_lo, q_hi in ((0.25, 0.75), (0.1, 0.9), (0.0, 1.0)):
                lo, hi = float(np.quantile(column, q_lo)), float(np.quantile(column, q_hi))
                if hi > lo:
                    break
            values[feature] = [lo, hi]
    return values


def compute_truth(spec: dict, audit: pd.DataFrame, noise_audit: dict, scm, predict) -> dict:
    """Exact per-task effects of each feature on the audited model's output.

    total(f):  mean over audit rows of M(x[f<-hi] with every causal descendant
               recomputed from the row's own exogenous noise) - same with f<-lo.
    direct(f): mean over audit rows of M(x with only f set to hi) - M(x with
               only f set to lo); all other inputs keep their observed values.
    indirect(f) = total(f) - direct(f).
    """

    features = spec["features"]
    observed = audit[features].to_numpy(dtype=float)
    regenerated = scm.features_frame(noise_audit)[features].to_numpy(dtype=float)
    if np.max(np.abs(regenerated - observed)) > 1e-8:
        raise RuntimeError(f"{spec['task_id']}: structural equations do not reproduce the audit rows")

    row_total: dict[str, np.ndarray] = {}
    row_direct: dict[str, np.ndarray] = {}
    for feature in spec["estimate_features"]:
        lo, hi = spec["interventions"][feature]
        j = features.index(feature)
        cf_lo = scm.features_frame(noise_audit, do={feature: lo})[features].to_numpy(dtype=float)
        cf_hi = scm.features_frame(noise_audit, do={feature: hi})[features].to_numpy(dtype=float)
        row_total[feature] = predict(cf_hi) - predict(cf_lo)
        d_lo = observed.copy()
        d_hi = observed.copy()
        d_lo[:, j] = lo
        d_hi[:, j] = hi
        row_direct[feature] = predict(d_hi) - predict(d_lo)

    total = {f: float(np.mean(v)) for f, v in row_total.items()}
    direct = {f: float(np.mean(v)) for f, v in row_direct.items()}
    scale = max(abs(v) for v in total.values())
    if not scale > 0:
        raise RuntimeError(f"{spec['task_id']}: degenerate task with no feature influence")
    positives = [f for f in spec["unlearned_features"] if abs(total[f]) >= POSITIVE_FRACTION * scale]
    negatives = [f for f in spec["unlearned_features"] if abs(total[f]) <= 1e-12 * scale]
    verdict_residual = [f for f in spec["unlearned_features"] if abs(total[f]) >= VERDICT_RESIDUAL_FRACTION * scale]
    verdict_clear = [f for f in spec["unlearned_features"] if abs(total[f]) <= VERDICT_CLEAR_FRACTION * scale]

    subgroup_scale = max([abs(total[f]) for f in spec.get("subgroup_features", [])] or [scale])
    subgroups = {}
    for name, rule in spec.get("subgroups", {}).items():
        mask = subgroup_mask(audit, rule)
        if mask.sum() < 50:
            raise RuntimeError(f"{spec['task_id']}: subgroup {name} too small")
        subgroups[name] = {
            f: {"total": float(np.mean(row_total[f][mask])), "direct": float(np.mean(row_direct[f][mask]))}
            for f in spec.get("subgroup_features", [])
        }
    return {
        "total": total,
        "direct": direct,
        "scale": float(scale),
        "positives": positives,
        "negatives": negatives,
        "verdict_residual": verdict_residual,
        "verdict_clear": verdict_clear,
        "subgroups": subgroups,
        "subgroup_scale": float(subgroup_scale if subgroup_scale > 0 else scale),
    }


def write_task_inputs(tasks: dict[str, Task], root: Path) -> None:
    root.mkdir(parents=True, exist_ok=False)
    for task_id, task in tasks.items():
        task_dir = root / task_id
        task_dir.mkdir()
        (task_dir / "spec.json").write_text(json.dumps(task.spec, indent=1))
        task.audit.to_csv(task_dir / "audit.csv", index=False, float_format="%.17g")
    (root / "index.json").write_text(json.dumps({"protocol": 1, "tasks": list(tasks)}, indent=1))


# ── black-box oracle ─────────────────────────────────────────────────────────


def _pack(header: dict, payload: bytes = b"") -> bytes:
    raw = json.dumps(header).encode()
    return struct.pack("<I", len(raw)) + raw + payload


class OracleServer:
    """Serves predictions of the evaluator-held models; counts and caps rows."""

    def __init__(self, tasks: dict[str, Task]):
        self.tasks = tasks
        self.used = {task_id: 0 for task_id in tasks}
        self.refused = {task_id: 0 for task_id in tasks}
        self.authkey = secrets.token_bytes(32)
        self._lock = threading.Lock()
        self._stopping = False
        self._dir = None
        try:
            base = "/tmp" if os.path.isdir("/tmp") and os.access("/tmp", os.W_OK) else None
            self._dir = tempfile.mkdtemp(prefix="ulo_", dir=base)
            path = os.path.join(self._dir, "s")
            self._listener = Listener(path, family="AF_UNIX", authkey=self.authkey)
            self.address = f"unix:{path}"
            self._client_address = (path, "AF_UNIX")
        except OSError:
            self._listener = Listener(("127.0.0.1", 0), family="AF_INET", authkey=self.authkey)
            host, port = self._listener.address
            self.address = f"tcp:{host}:{port}"
            self._client_address = ((host, port), "AF_INET")
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def _serve(self) -> None:
        while not self._stopping:
            try:
                conn = self._listener.accept()
            except Exception:
                if self._stopping:
                    return
                continue
            if self._stopping:
                conn.close()
                return
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn) -> None:
        limit = MAX_ROWS_PER_REQUEST * MAX_COLS * 8 + 65_536
        try:
            while True:
                try:
                    blob = conn.recv_bytes(maxlength=limit)
                except (EOFError, OSError):
                    return
                try:
                    reply = self._answer(blob)
                except Exception as exc:  # malformed request: answer, never crash
                    reply = _pack({"ok": False, "error": f"bad_request: {type(exc).__name__}"})
                conn.send_bytes(reply)
        finally:
            conn.close()

    def _answer(self, blob: bytes) -> bytes:
        (size,) = struct.unpack("<I", blob[:4])
        header = json.loads(blob[4 : 4 + size].decode())
        payload = blob[4 + size :]
        task = self.tasks.get(header.get("task_id")) if isinstance(header.get("task_id"), str) else None
        if task is None:
            return _pack({"ok": False, "error": "unknown_task"})
        n_rows, n_cols = header.get("n_rows"), header.get("n_cols")
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in (n_rows, n_cols)):
            return _pack({"ok": False, "error": "bad_shape"})
        if n_cols != len(task.spec["features"]) or not 0 <= n_rows <= MAX_ROWS_PER_REQUEST:
            return _pack({"ok": False, "error": "bad_shape"})
        if len(payload) != n_rows * n_cols * 8:
            return _pack({"ok": False, "error": "bad_payload"})
        rows = np.frombuffer(payload, dtype="<f8").reshape(n_rows, n_cols)
        if not np.isfinite(rows).all():
            return _pack({"ok": False, "error": "non_finite_rows"})
        budget = int(task.spec["query_budget"])
        with self._lock:
            if self.used[task.task_id] + n_rows > budget:
                self.refused[task.task_id] += n_rows
                left = budget - self.used[task.task_id]
                return _pack({"ok": False, "error": f"budget_exceeded (remaining {left} rows)"})
            self.used[task.task_id] += n_rows
            predictions = task.predict(rows) if n_rows else np.zeros(0)
        return _pack({"ok": True, "n_rows": n_rows}, np.ascontiguousarray(predictions, dtype="<f8").tobytes())

    def stop(self) -> None:
        self._stopping = True

        def wake() -> None:  # unblock accept(); bounded so a stray client cannot hang us
            try:
                address, family = self._client_address
                Client(address, family=family, authkey=self.authkey).close()
            except Exception:
                pass

        waker = threading.Thread(target=wake, daemon=True)
        waker.start()
        waker.join(timeout=5)
        try:
            self._listener.close()
        except Exception:
            pass
        self._thread.join(timeout=5)
        if self._dir:
            shutil.rmtree(self._dir, ignore_errors=True)


# ── running verifiers ────────────────────────────────────────────────────────


def discover_verifiers(verifiers_dir: Path, only: list[str] | None = None) -> dict[str, Path]:
    found = {
        path.stem: path
        for path in sorted(Path(verifiers_dir).glob("*.sh"))
        if path.is_file() and _NAME_RE.match(path.stem)
    }
    if only:
        missing = [name for name in only if name not in found]
        if missing:
            raise FileNotFoundError(f"No verifier script for {missing} in {verifiers_dir}")
        found = {name: found[name] for name in only}
    return found


def _kill_group(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        pass


def _tail(path: Path, lines: int = 25) -> str:
    try:
        return "\n".join(path.read_text(errors="replace").splitlines()[-lines:])
    except OSError:
        return ""


def run_verifier(name: str, script: Path, tasks: dict[str, Task], timeout: int = VERIFIER_TIMEOUT_S) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix="ulv_"))
    task_dir = workdir / "tasks"
    out_path = workdir / "answers.json"
    log_path = workdir / "verifier.log"
    write_task_inputs(tasks, task_dir)
    server = OracleServer(tasks)
    env = dict(os.environ)
    env[ADDRESS_ENV] = server.address
    env[AUTHKEY_ENV] = server.authkey.hex()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(WORKSPACE)] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    )
    status = "ok"
    limit = int(VERIFIER_CPU_LIMIT_S)
    with open(log_path, "wb") as log:
        proc = subprocess.Popen(
            ["bash", "-c", f'ulimit -t {limit} 2>/dev/null; exec bash "$0" "$@"', str(script), str(task_dir), str(out_path)],
            cwd=str(WORKSPACE),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            returncode = proc.wait(timeout=timeout)
            if returncode != 0:
                status = f"exit_code_{returncode}"
        except subprocess.TimeoutExpired:
            status = "timeout"
    _kill_group(proc)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        pass
    server.stop()
    answers = None
    if status == "ok":
        try:
            answers = _load_answers(out_path)
        except Exception as exc:
            status = f"unreadable_answers: {type(exc).__name__}: {exc}"[:300]
    run = {
        "status": status,
        "answers": answers,
        "used": dict(server.used),
        "refused": dict(server.refused),
        "log_tail": _tail(log_path) if status != "ok" else "",
    }
    shutil.rmtree(workdir, ignore_errors=True)
    return run


def _load_answers(path: Path) -> dict:
    if path.stat().st_size > 200_000_000:
        raise ValueError("answers file too large")
    obj = json.loads(path.read_text(), parse_constant=lambda _token: float("nan"))
    tasks = obj.get("tasks") if isinstance(obj, dict) else None
    if not isinstance(tasks, dict):
        raise ValueError("answers must be {'tasks': {task_id: ...}}")
    return tasks


# ── validation and scoring ───────────────────────────────────────────────────


def _number(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def _pair(entry) -> tuple[float, float] | None:
    if not isinstance(entry, dict):
        return None
    total, direct = _number(entry.get("total")), _number(entry.get("direct"))
    if total is None or direct is None:
        return None
    return total, direct


def parse_task_answer(task: Task, answer) -> dict | None:
    """Validated ``{effects: {f: (total, direct)}, subgroups: {g: {f: (...)}}}`` or None."""

    spec = task.spec
    if not isinstance(answer, dict) or not isinstance(answer.get("effects"), dict):
        return None
    parsed = {"effects": {}, "subgroups": {}}
    for feature in spec["estimate_features"]:
        pair = _pair(answer["effects"].get(feature))
        if pair is None:
            return None
        parsed["effects"][feature] = pair
    if spec.get("subgroups"):
        groups = answer.get("subgroup_effects")
        if not isinstance(groups, dict):
            return None
        for group in spec["subgroups"]:
            entries = groups.get(group)
            if not isinstance(entries, dict):
                return None
            parsed["subgroups"][group] = {}
            for feature in spec["subgroup_features"]:
                pair = _pair(entries.get(feature))
                if pair is None:
                    return None
                parsed["subgroups"][group][feature] = pair
    return parsed


def _err(estimate: float, truth: float, scale: float) -> float:
    return float(min(abs(estimate - truth) / scale, ERROR_CAP))


def _capture(estimate: float, truth: float) -> float:
    """Credit for recovering a nonzero true effect: 1 when the estimate has the
    true sign and lies within a factor of two of it; linearly less outside
    (0 at zero or the wrong sign, 0 at three times the truth)."""
    ratio = estimate / truth
    if ratio <= 0:
        return 0.0
    if ratio < 0.5:
        return float(ratio / 0.5)
    if ratio <= 2.0:
        return 1.0
    return float(max(0.0, 3.0 - ratio))


def _spearman(a: list[float], b: list[float]) -> float:
    ra = pd.Series(a).rank(method="average").to_numpy()
    rb = pd.Series(b).rank(method="average").to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])


def feature_record(task: Task, parsed: dict | None, used_rows: int = 0) -> dict:
    truth, spec = task.truth, task.spec
    features = spec["estimate_features"]
    scale = truth["scale"]
    record = {"task_id": task.task_id, "failed": parsed is None}
    if parsed is None:
        record.update(
            total_err=[ERROR_CAP] * len(features),
            direct_err=[ERROR_CAP] * len(features),
            indirect_err=[ERROR_CAP] * len(features),
            spearman=-1.0,
            capture=[0.0] * len(truth["positives"]),
            false_alarms=[1.0] * len(truth["negatives"]),
            verdict_residual=[0.0] * len(truth.get("verdict_residual", [])),
            verdict_clear=[0.0] * len(truth.get("verdict_clear", [])),
            query_fraction=1.0,
        )
        return record
    est = parsed["effects"]
    record["total_err"] = [_err(est[f][0], truth["total"][f], scale) for f in features]
    record["direct_err"] = [_err(est[f][1], truth["direct"][f], scale) for f in features]
    record["indirect_err"] = [
        _err(est[f][0] - est[f][1], truth["total"][f] - truth["direct"][f], scale) for f in features
    ]
    record["spearman"] = _spearman([abs(est[f][0]) for f in features], [abs(truth["total"][f]) for f in features])
    record["capture"] = [_capture(est[f][0], truth["total"][f]) for f in truth["positives"]]
    record["false_alarms"] = [
        1.0 if abs(est[f][0]) >= DETECT_FRACTION * scale else 0.0 for f in truth["negatives"]
    ]
    # Verification verdict (paper Def. 4 / Problem 1): an unlearned feature is
    # flagged as retaining influence when |reported total| >= 10% of scale.
    # Correct when flagged for a true residual influence >= 11% of scale and
    # not flagged for one <= 9% (only the razor-edge band in between is not
    # scored, so influences near the threshold count).
    flagged = {f: abs(est[f][0]) >= DETECT_FRACTION * scale for f in spec["unlearned_features"]}
    record["verdict_residual"] = [1.0 if flagged[f] else 0.0 for f in truth.get("verdict_residual", [])]
    record["verdict_clear"] = [0.0 if flagged[f] else 1.0 for f in truth.get("verdict_clear", [])]
    # Efficiency counts only on solved tasks: the total-effect error must be at
    # most half that of the trivial all-zero answer. One pass over the audit
    # rows is free (the audit sample size is fixed by the evaluator; querying
    # fewer rows only shrinks it), so only querying beyond one pass is charged.
    trivial = float(np.mean([min(abs(truth["total"][f]) / scale, ERROR_CAP) for f in features]))
    solved = float(np.mean(record["total_err"])) <= SOLVED_FRACTION * trivial
    charged = max(int(used_rows), int(spec["n_rows"]))
    record["query_fraction"] = float(charged / spec["query_budget"]) if solved else 1.0
    return record


def _gaps(groups: dict, feature: str, first: str, second: str) -> tuple[float, float, float]:
    t1, d1 = groups[first][feature]
    t2, d2 = groups[second][feature]
    return (t1 - d1) - (t2 - d2), t1 - t2, d1 - d2


def subgroup_record(task: Task, parsed: dict | None) -> dict:
    truth, spec = task.truth, task.spec
    scale = truth["subgroup_scale"]
    first, second = spec["subgroup_gap"]
    true_groups = {
        g: {f: (v["total"], v["direct"]) for f, v in entries.items()} for g, entries in truth["subgroups"].items()
    }
    features = spec["subgroup_features"]
    true_gaps = {f: _gaps(true_groups, f, first, second) for f in features}
    eligible = [f for f in features if abs(true_gaps[f][0]) >= GAP_FRACTION * scale]
    record = {"task_id": task.task_id, "failed": parsed is None}
    if parsed is None:
        record.update(
            indirect_gap_err=[ERROR_CAP] * len(features),
            total_gap_err=[ERROR_CAP] * len(features),
            direct_gap_err=[ERROR_CAP] * len(features),
            effect_err=[ERROR_CAP] * (3 * len(features) * len(true_groups)),
            gap_capture=[0.0] * len(eligible),
            gap_direction=[0.0] * len(eligible),
        )
        return record
    record["effect_err"] = []
    for group, entries in true_groups.items():
        for f in features:
            (t, d), (te, de) = entries[f], parsed["subgroups"][group][f]
            record["effect_err"] += [_err(te, t, scale), _err(de, d, scale), _err(te - de, t - d, scale)]
    est_gaps = {f: _gaps(parsed["subgroups"], f, first, second) for f in features}
    record["indirect_gap_err"] = [_err(est_gaps[f][0], true_gaps[f][0], scale) for f in features]
    record["total_gap_err"] = [_err(est_gaps[f][1], true_gaps[f][1], scale) for f in features]
    record["direct_gap_err"] = [_err(est_gaps[f][2], true_gaps[f][2], scale) for f in features]
    record["gap_capture"] = [_capture(est_gaps[f][0], true_gaps[f][0]) for f in eligible]
    # Direction: the reported mediated-influence gap is detected (at least the
    # detection fraction of the scale) and points to the right subgroup.
    record["gap_direction"] = [
        1.0 if (est_gaps[f][0] * true_gaps[f][0] > 0 and abs(est_gaps[f][0]) >= DETECT_FRACTION * scale) else 0.0
        for f in eligible
    ]
    return record


def _pooled(records: list[dict], key: str, empty: float = 0.0) -> float:
    values = [v for record in records for v in record[key]]
    return float(np.mean(values)) if values else empty


def verdict_balanced_accuracy(records: list[dict]) -> float:
    """Mean of the pooled hit rate on residual items and the pooled pass rate on clear items."""

    parts = []
    for key in ("verdict_residual", "verdict_clear"):
        values = [v for record in records for v in record.get(key, [])]
        if values:
            parts.append(float(np.mean(values)))
    return float(np.mean(parts)) if parts else 0.0


def aggregate_feature(records: list[dict], verdict: bool = False) -> dict:
    metrics = {
        "total_effect_nmae": _pooled(records, "total_err", ERROR_CAP),
        "indirect_effect_nmae": _pooled(records, "indirect_err", ERROR_CAP),
        "direct_effect_nmae": _pooled(records, "direct_err", ERROR_CAP),
        "rank_spearman": float(np.mean([r["spearman"] for r in records])) if records else -1.0,
        "residual_capture": _pooled(records, "capture"),
        "false_alarm_rate": _pooled(records, "false_alarms"),
        "query_budget_fraction": float(np.mean([r["query_fraction"] for r in records])) if records else 1.0,
    }
    if verdict:
        metrics["verdict_accuracy"] = verdict_balanced_accuracy(records)
    return metrics


def aggregate_subgroup(records: list[dict]) -> dict:
    return {
        "indirect_gap_nmae": _pooled(records, "indirect_gap_err", ERROR_CAP),
        "direct_gap_nmae": _pooled(records, "direct_gap_err", ERROR_CAP),
        "subgroup_effect_nmae": _pooled(records, "effect_err", ERROR_CAP),
        "indirect_gap_capture": _pooled(records, "gap_capture"),
        "indirect_gap_direction": _pooled(records, "gap_direction"),
    }


def score_run(tasks: dict[str, Task], run: dict) -> dict:
    answers = run["answers"]
    records = {experiment: [] for experiment in EXPERIMENTS}
    failed = 0
    for task_id, task in tasks.items():
        parsed = parse_task_answer(task, answers.get(task_id)) if answers is not None else None
        failed += parsed is None
        records[FEATURE_EXPERIMENTS[task.family]].append(feature_record(task, parsed, run["used"][task_id]))
        if task.spec.get("subgroups"):
            records[SUBGROUP_EXPERIMENT].append(subgroup_record(task, parsed))
    metrics = {}
    for experiment in EXPERIMENTS:
        if not records[experiment]:
            continue
        if experiment == SUBGROUP_EXPERIMENT:
            metrics[experiment] = aggregate_subgroup(records[experiment])
        else:
            metrics[experiment] = aggregate_feature(records[experiment], verdict=experiment in VERDICT_EXPERIMENTS)
    fractions = [run["used"][t] / tasks[t].spec["query_budget"] for t in tasks]
    diagnostics = {
        "status": run["status"],
        "tasks": len(tasks),
        "failed_tasks": int(failed),
        "mean_query_budget_fraction": float(np.mean(fractions)) if fractions else 0.0,
        "refused_rows": int(sum(run["refused"].values())),
    }
    if run.get("log_tail"):
        diagnostics["log_tail"] = run["log_tail"]
    return {"metrics": metrics, "diagnostics": diagnostics, "records": records, "run": run}


def evaluate(
    tasks: dict[str, Task],
    verifiers: dict[str, Path],
    slice_name: str,
    per_method_dir: Path | None = None,
    details_path: Path | None = None,
) -> dict:
    scores = {"_slice": slice_name, "_diagnostics": {}, "experiments": {}}
    present = {experiment for task in tasks.values() for experiment in _task_experiments(task)}
    for experiment in EXPERIMENTS:
        if experiment in present:
            scores["experiments"][experiment] = {"results": {}}
    details = {}
    for name, script in verifiers.items():
        cache = per_method_dir / f"{name}.json" if per_method_dir is not None else None
        if cache is not None and cache.is_file() and "run" in json.loads(cache.read_text()):
            # Audit runs only: rescore the cached raw answers with the current scoring code.
            entry = score_run(tasks, json.loads(cache.read_text())["run"])
            print(f"[{slice_name}] {name}: rescored cached answers from {cache}", flush=True)
        else:
            print(f"[{slice_name}] running verifier {name} on {len(tasks)} tasks", flush=True)
            entry = score_run(tasks, run_verifier(name, script, tasks))
            if cache is not None:
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(entry, indent=1, sort_keys=True))
        for experiment, metrics in entry["metrics"].items():
            scores["experiments"][experiment]["results"][name] = metrics
        scores["_diagnostics"][name] = entry["diagnostics"]
        details[name] = entry["records"]
        print(f"[{slice_name}] {name}: {json.dumps(entry['diagnostics'])}", flush=True)
        for experiment, metrics in entry["metrics"].items():
            print(f"    {experiment}: " + ", ".join(f"{k}={v:.4f}" for k, v in metrics.items()), flush=True)
    if details_path is not None:
        details_path.parent.mkdir(parents=True, exist_ok=True)
        details_path.write_text(json.dumps(details, indent=1, sort_keys=True))
    return scores


def _task_experiments(task: Task) -> list[str]:
    experiments = [FEATURE_EXPERIMENTS[task.family]]
    if task.spec.get("subgroups"):
        experiments.append(SUBGROUP_EXPERIMENT)
    return experiments


# ── audited black-box models ─────────────────────────────────────────────────


class ProbabilityModel:
    """Audited classifier whose black-box output is P(positive class)."""

    def __init__(self, classifier):
        self.classifier = classifier

    def fit(self, x, y):
        self.classifier.fit(x, np.asarray(y).astype(int))
        return self

    def predict(self, x):
        return self.classifier.predict_proba(x)[:, 1]


def make_classifier(architecture: str, seed: int) -> ProbabilityModel:
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    if architecture == "random_forest":
        model = RandomForestClassifier(n_estimators=160, min_samples_leaf=12, random_state=seed, n_jobs=1)
    elif architecture == "gradient_boosting":
        model = HistGradientBoostingClassifier(
            max_iter=250, learning_rate=0.06, max_leaf_nodes=31, early_stopping=False, random_state=seed
        )
    elif architecture == "mlp":
        model = make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(64, 32),
                alpha=1e-3,
                learning_rate_init=1e-3,
                max_iter=300,
                early_stopping=True,
                random_state=seed,
            ),
        )
    elif architecture == "linear":
        model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000))
    else:
        raise ValueError(f"Unknown architecture {architecture}")
    return ProbabilityModel(model)


def make_model(architecture: str, seed: int, kind: str = "regression"):
    from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.neural_network import MLPRegressor
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    if kind == "classification":
        return make_classifier(architecture, seed)
    if architecture == "random_forest":
        return RandomForestRegressor(n_estimators=160, min_samples_leaf=12, random_state=seed, n_jobs=1)
    if architecture == "gradient_boosting":
        return HistGradientBoostingRegressor(
            max_iter=250, learning_rate=0.06, max_leaf_nodes=31, early_stopping=False, random_state=seed
        )
    if architecture == "mlp":
        return make_pipeline(
            StandardScaler(),
            MLPRegressor(
                hidden_layer_sizes=(64, 32),
                alpha=1e-3,
                learning_rate_init=1e-3,
                max_iter=300,
                early_stopping=True,
                random_state=seed,
            ),
        )
    if architecture == "linear":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    raise ValueError(f"Unknown architecture {architecture}")


def build_task(
    task_id: str,
    scm_cls,
    seed: int,
    architecture: str,
    control_active: bool,
    target_retained: bool,
    n_total: int,
    n_audit: int,
    params: dict | None = None,
) -> Task:
    """Sample one task: data, audited model, contrasts, budget and exact truth."""

    import warnings

    rng = np.random.default_rng(seed)
    scm = scm_cls(params if params is not None else scm_cls.draw_params(rng, control_active))
    noise = scm_cls.draw_noise(rng, n_total)
    frame = scm.features_frame(noise)
    outcome = scm.outcome_values(frame, noise)
    order = rng.permutation(n_total)
    audit_idx, train_idx = np.sort(order[:n_audit]), np.sort(order[n_audit:])
    features = list(scm_cls.features)
    removed = [f for f in scm.unlearned if not (target_retained and f == scm_cls.target)]
    model_columns = [i for i, f in enumerate(features) if f not in removed]
    matrix = frame[features].to_numpy(dtype=float)
    model = make_model(architecture, seed % (2**31), getattr(scm_cls, "task_kind", "regression"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(matrix[train_idx][:, model_columns], outcome[train_idx])
    audit = frame.iloc[audit_idx][features].reset_index(drop=True)
    noise_audit = {key: value[audit_idx] for key, value in noise.items()}
    spec = {
        "task_id": task_id,
        "family": scm_cls.name,
        "features": features,
        "binary_features": list(scm_cls.binary_features),
        "outcome": scm_cls.outcome,
        "edges": [list(edge) for edge in scm_cls.edges],
        "unlearned_features": list(scm.unlearned),
        "estimate_features": features,
        "interventions": intervention_values(audit, features, scm_cls.binary_features),
        "subgroups": dict(scm_cls.subgroups),
        "subgroup_gap": list(scm_cls.subgroups)[:2] if scm_cls.subgroups else [],
        "subgroup_features": list(scm_cls.subgroup_features),
        "n_rows": int(n_audit),
        "query_budget": int(QUERY_BUDGET_PER_ROW * n_audit),
    }
    task = Task(task_id=task_id, spec=spec, audit=audit, model=model, model_columns=model_columns)
    task.truth = compute_truth(spec, audit, noise_audit, scm, task.predict)
    return task


def run_cli(slice_name: str, build_tasks, default_scores: str, argv: list[str] | None = None) -> None:
    import argparse
    import time

    parser = argparse.ArgumentParser(description=f"Score every registered verifier on the {slice_name} tasks.")
    parser.add_argument("--verifiers-dir", default=str(DEFAULT_VERIFIERS_DIR))
    parser.add_argument("--methods", nargs="*", default=None, help="optional subset of verifier names")
    parser.add_argument("--scores", default=default_scores)
    parser.add_argument("--per-method-dir", default=None, help="cache per-verifier results (audit runs only)")
    parser.add_argument("--details", default=None, help="write per-task records for paired analysis")
    parser.add_argument("--smoke", action="store_true", help="tiny task set for pipeline checks")
    args = parser.parse_args(argv)

    verifiers = discover_verifiers(Path(args.verifiers_dir), args.methods)
    if not verifiers:
        raise SystemExit(f"No verifier scripts found in {args.verifiers_dir}")
    start = time.time()
    tasks = build_tasks(smoke=args.smoke, log=lambda msg: print(f"[{slice_name}] {msg} ({time.time() - start:.1f}s)", flush=True))
    print(f"[{slice_name}] built {len(tasks)} tasks in {time.time() - start:.1f}s", flush=True)
    scores = evaluate(
        tasks,
        verifiers,
        slice_name,
        per_method_dir=Path(args.per_method_dir) if args.per_method_dir else None,
        details_path=Path(args.details) if args.details else None,
    )
    path = Path(args.scores)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scores, indent=2, sort_keys=True))
    print(f"[{slice_name}] wrote {path} in {time.time() - start:.1f}s", flush=True)
