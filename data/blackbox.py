"""Client for the evaluator-owned black-box model oracle.

During evaluation every task's audited model lives inside the evaluator
process. A verifier can only obtain predictions by sending feature rows over
the connection advertised in the ``UNLEARN_ORACLE_ADDRESS`` /
``UNLEARN_ORACLE_AUTHKEY`` environment variables. The evaluator counts every
row it scores and refuses requests beyond the task's ``query_budget``.

Wire format (both directions, one message each):
    uint32 little-endian header length | UTF-8 JSON header | raw payload
Request header: ``{"task_id": str, "n_rows": int, "n_cols": int}``, payload is
``n_rows * n_cols`` little-endian float64 values in ``spec["features"]`` order.
Reply header: ``{"ok": true, "n_rows": int}`` with ``n_rows`` float64
predictions, or ``{"ok": false, "error": str}``.
"""

from __future__ import annotations

import json
import os
import struct
from multiprocessing.connection import Client

import numpy as np
import pandas as pd

ADDRESS_ENV = "UNLEARN_ORACLE_ADDRESS"
AUTHKEY_ENV = "UNLEARN_ORACLE_AUTHKEY"
CHUNK_ROWS = 50_000


class OracleError(RuntimeError):
    """The oracle rejected a request."""


class BudgetExceeded(OracleError):
    """The request would exceed the task's query budget."""


_CONNECTION = None


def _connection():
    global _CONNECTION
    if _CONNECTION is None:
        address = os.environ.get(ADDRESS_ENV)
        key = os.environ.get(AUTHKEY_ENV)
        if not address or not key:
            raise OracleError(
                "No black-box oracle available: run verifiers through "
                "scripts/evaluate_train.sh (or the eval harness)."
            )
        authkey = bytes.fromhex(key)
        if address.startswith("unix:"):
            _CONNECTION = Client(address[len("unix:"):], family="AF_UNIX", authkey=authkey)
        elif address.startswith("tcp:"):
            host, port = address[len("tcp:"):].rsplit(":", 1)
            _CONNECTION = Client((host, int(port)), family="AF_INET", authkey=authkey)
        else:
            raise OracleError(f"Unknown oracle address {address!r}")
    return _CONNECTION


def _pack(header: dict, payload: bytes) -> bytes:
    raw = json.dumps(header).encode()
    return struct.pack("<I", len(raw)) + raw + payload


def _unpack(blob: bytes) -> tuple[dict, bytes]:
    (size,) = struct.unpack("<I", blob[:4])
    header = json.loads(blob[4 : 4 + size].decode())
    return header, blob[4 + size :]


class BlackBox:
    """Prediction-only access to one task's audited model."""

    def __init__(self, spec: dict):
        self.task_id = spec["task_id"]
        self.features = list(spec["features"])
        self.budget = int(spec["query_budget"])
        self.used = 0

    @property
    def remaining(self) -> int:
        return self.budget - self.used

    def predict(self, rows) -> np.ndarray:
        if isinstance(rows, pd.DataFrame):
            array = rows[self.features].to_numpy(dtype=float)
        else:
            array = np.asarray(rows, dtype=float)
            if array.ndim != 2 or array.shape[1] != len(self.features):
                raise ValueError(
                    f"Expected rows with {len(self.features)} columns ordered as {self.features}"
                )
        array = np.ascontiguousarray(array, dtype="<f8")
        if len(array) == 0:
            return np.zeros(0)
        conn = _connection()
        outputs = []
        for start in range(0, len(array), CHUNK_ROWS):
            chunk = array[start : start + CHUNK_ROWS]
            header = {"task_id": self.task_id, "n_rows": int(len(chunk)), "n_cols": int(chunk.shape[1])}
            conn.send_bytes(_pack(header, chunk.tobytes()))
            reply, payload = _unpack(conn.recv_bytes())
            if not reply.get("ok"):
                error = str(reply.get("error", "unknown error"))
                if error.startswith("budget_exceeded"):
                    raise BudgetExceeded(f"{self.task_id}: {error}")
                raise OracleError(f"{self.task_id}: {error}")
            outputs.append(np.frombuffer(payload, dtype="<f8").copy())
            self.used += len(chunk)
        return np.concatenate(outputs)
