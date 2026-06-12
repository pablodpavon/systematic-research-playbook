#!/usr/bin/env python3
"""Tests for the lunar-phase worked example. All must pass before the frozen run.

The planted-answer test (c) deliberately uses its OWN seed (777), not the frozen
data seed: the detector must be validated on data whose truth we control, without
peeking at the frozen dataset's outcome before the single official run.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd
import pytest

import generate_data
import ledger
import run_test


def _csv_hash(df: pd.DataFrame) -> str:
    return hashlib.sha256(df.to_csv(float_format="%.10f").encode()).hexdigest()


# (a) generator determinism ----------------------------------------------------

def test_generator_same_seed_identical():
    a = generate_data.generate(20260612)
    b = generate_data.generate(20260612)
    assert _csv_hash(a) == _csv_hash(b)


def test_generator_different_seed_differs():
    a = generate_data.generate(20260612)
    c = generate_data.generate(99)
    assert _csv_hash(a) != _csv_hash(c)


# (b) ledger chain integrity + tamper detection --------------------------------

def test_ledger_chain_ok(tmp_path):
    path = str(tmp_path / "ledger.jsonl")
    for i in range(5):
        ledger.append(path, {"trial": i}, {"sr": 0.1 * i})
    ok, bad = ledger.verify_chain(path)
    assert ok and bad is None


def test_ledger_tamper_detected(tmp_path):
    path = str(tmp_path / "ledger.jsonl")
    for i in range(5):
        ledger.append(path, {"trial": i}, {"sr": 0.1 * i})
    rows = [json.loads(l) for l in open(path)]
    rows[2]["metrics"]["sr"] = 9.99            # doctor one past result on a copy
    tampered = str(tmp_path / "tampered.jsonl")
    with open(tampered, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    ok, bad = ledger.verify_chain(tampered)
    assert not ok and bad == 2


# (c) planted-answer test -------------------------------------------------------

PLANT_BPS_DAILY = 0.0030    # +30 bps/day to waxing days
TEST_SEED = 777


def _prices_with_plant(plant: bool) -> pd.DataFrame:
    base = generate_data.generate(TEST_SEED)
    px = base.to_numpy()
    rets = px[1:] / px[:-1] - 1.0
    if plant:
        waxing = run_test.lunar_phase(base.index[1:]) < 0.5
        rets = rets + np.where(waxing, PLANT_BPS_DAILY, 0.0)[:, None]
    out = np.empty_like(px)
    out[0] = px[0]
    out[1:] = px[0] * np.cumprod(1.0 + rets, axis=0)
    return pd.DataFrame(out, index=base.index, columns=base.columns)


def test_planted_effect_detected(tmp_path):
    res = run_test.run(_prices_with_plant(True), str(tmp_path / "ledger.jsonl"))
    best = res["best"]["metrics"]
    ci_lo, ci_hi = res["ci"]
    assert best["mean_net_daily"] > 0.0010          # strongly positive
    assert ci_lo > 0.0                              # CI excludes 0 from above
    assert res["verdict"] == "PASS"                 # full frozen rule fires on planted truth


def test_no_plant_no_detection(tmp_path):
    res = run_test.run(_prices_with_plant(False), str(tmp_path / "ledger.jsonl"))
    best = res["best"]["metrics"]
    strongly_positive = best["mean_net_daily"] > 0.0010 and res["ci"][0] > 0.0
    assert not strongly_positive


# (d) phase function sanity ------------------------------------------------------

def test_phase_epoch_is_zero():
    phase = run_test.lunar_phase(pd.DatetimeIndex([run_test.EPOCH]))
    assert phase[0] == pytest.approx(0.0, abs=1e-12)


def test_phase_period():
    one_cycle = run_test.EPOCH + pd.Timedelta(days=run_test.SYNODIC_DAYS)
    phase = run_test.lunar_phase(pd.DatetimeIndex([one_cycle]))
    assert min(phase[0], 1.0 - phase[0]) == pytest.approx(0.0, abs=1e-9)
    daily = run_test.lunar_phase(pd.DatetimeIndex([run_test.EPOCH + pd.Timedelta(days=1)]))
    assert daily[0] == pytest.approx(1.0 / 29.530588, rel=1e-9)


def test_phase_monotone_within_cycle():
    days = pd.DatetimeIndex([run_test.EPOCH + pd.Timedelta(days=d) for d in range(29)])
    phase = run_test.lunar_phase(days)
    assert np.all(np.diff(phase) > 0)               # strictly increasing inside one cycle
