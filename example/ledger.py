#!/usr/bin/env python3
"""Append-only, hash-chained trial ledger over JSONL.

Each appended row is

    {seq, utc_ts, params, metrics, prev_sha256, sha256}

where `sha256` is the SHA-256 of the row's canonical JSON *including* `prev_sha256`
(but excluding `sha256` itself). Each row's `prev_sha256` is the previous row's
`sha256`, so any edit to any past row breaks every hash from that row onward.

The ledger is append-only by contract: there is no update or delete API, and
`verify_chain` recomputes every hash and checks the linkage, returning
(ok, first_bad_seq). The point is that every trial ever run is permanently visible
-- the multiple-testing denominator cannot quietly shrink after the fact.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

GENESIS = "0" * 64
_BODY_KEYS = ("seq", "utc_ts", "params", "metrics", "prev_sha256")


def _canonical(body: dict) -> bytes:
    """Deterministic JSON encoding used as the hash preimage."""
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _row_hash(body: dict) -> str:
    return hashlib.sha256(_canonical(body)).hexdigest()


def _read_rows(path: str) -> list[dict]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
    except FileNotFoundError:
        return []


def append(path: str, params: dict, metrics: dict) -> dict:
    """Append one trial row to the JSONL ledger at `path` and return the row."""
    rows = _read_rows(path)
    seq = len(rows)
    prev_sha256 = rows[-1]["sha256"] if rows else GENESIS

    body = {
        "seq": seq,
        "utc_ts": datetime.now(timezone.utc).isoformat(),
        "params": params,
        "metrics": metrics,
        "prev_sha256": prev_sha256,
    }
    row = dict(body)
    row["sha256"] = _row_hash(body)

    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def verify_chain(path: str) -> tuple[bool, int | None]:
    """Walk the ledger; return (ok, first_bad_seq). first_bad_seq is None when ok."""
    rows = _read_rows(path)
    prev = GENESIS
    for i, row in enumerate(rows):
        try:
            body = {k: row[k] for k in _BODY_KEYS}
        except (KeyError, TypeError):
            return False, i
        if row.get("seq") != i:
            return False, i
        if row.get("prev_sha256") != prev:
            return False, i
        if _row_hash(body) != row.get("sha256"):
            return False, i
        prev = row["sha256"]
    return True, None
