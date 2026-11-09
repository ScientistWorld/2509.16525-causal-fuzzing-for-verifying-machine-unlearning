"""Small causal-graph and task-input helpers shared by verifiers.

Nothing here knows the data-generating process of any scored task; it only
reads what the evaluator hands to a verifier (``spec.json`` + ``audit.csv``).
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd


def parents(edges: list[list[str]] | list[tuple[str, str]], node: str) -> list[str]:
    return [src for src, dst in edges if dst == node]


def children_map(edges) -> dict[str, list[str]]:
    children: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        children[src].append(dst)
    return children


def descendants(edges, node: str) -> set[str]:
    children = children_map(edges)
    seen: set[str] = set()
    queue: deque[str] = deque(children[node])
    while queue:
        cur = queue.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        queue.extend(children[cur])
    return seen


def topological_order(nodes: list[str], edges) -> list[str]:
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        if src in indegree and dst in indegree:
            children[src].append(dst)
            indegree[dst] += 1
    queue = deque([node for node in nodes if indegree[node] == 0])
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        raise ValueError("Causal graph must be acyclic")
    return order


_OPS = {
    ">": np.greater,
    ">=": np.greater_equal,
    "<": np.less,
    "<=": np.less_equal,
}


def subgroup_mask(frame: pd.DataFrame, rule: dict) -> np.ndarray:
    """Boolean row mask for a subgroup rule ``{feature, op, threshold}``."""

    values = frame[rule["feature"]].to_numpy(dtype=float)
    return _OPS[rule["op"]](values, float(rule["threshold"]))


def load_tasks(tasks_dir: str | Path) -> list[tuple[dict, pd.DataFrame]]:
    """Read every task the evaluator wrote: ``[(spec, audit_frame), ...]``."""

    root = Path(tasks_dir)
    index = json.loads((root / "index.json").read_text())
    tasks = []
    for task_id in index["tasks"]:
        spec = json.loads((root / task_id / "spec.json").read_text())
        audit = pd.read_csv(root / task_id / "audit.csv")[spec["features"]]
        tasks.append((spec, audit.astype(float)))
    return tasks


def write_answers(path: str | Path, answers: dict) -> None:
    """Write ``{"tasks": {task_id: answer}}``; refuses NaN/inf values."""

    Path(path).write_text(json.dumps({"tasks": answers}, indent=1, allow_nan=False))
