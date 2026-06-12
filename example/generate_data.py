#!/usr/bin/env python3
"""Generate the synthetic price panel for the lunar-phase worked example.

NULL BY CONSTRUCTION. Each asset's daily returns are i.i.d. lognormal with zero
drift and a per-asset volatility drawn once from U[0.15, 0.35]. Returns depend on
nothing but the RNG -- there is no calendar term, no lunar term, no cross-asset
structure of any kind. Any apparent lunar-phase effect found downstream is, by the
design of this file, a statistical artifact and not a property of the data.

Deterministic: a given --seed always produces a byte-identical CSV. Default seed is
20260612 (the frozen data seed named in the pre-registration).

Usage:
    python generate_data.py [--seed 20260612] [--out synthetic_prices.csv]
"""
from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd

N_ASSETS = 12
N_DAYS = 2520           # ~10 trading years
TRADING_DAYS = 252
START_PRICE = 100.0
VOL_LOW, VOL_HIGH = 0.15, 0.35
CALENDAR_START = "2010-01-04"   # synthetic business-day calendar (fiction; not a real programme)
DEFAULT_SEED = 20260612


def generate(seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """Return a (N_DAYS x N_ASSETS) price DataFrame indexed by business date."""
    rng = np.random.default_rng(seed)
    assets = [f"SYN{i:02d}" for i in range(1, N_ASSETS + 1)]

    # One volatility per asset, drawn once (annualized -> daily).
    ann_vol = rng.uniform(VOL_LOW, VOL_HIGH, size=N_ASSETS)
    daily_vol = ann_vol / np.sqrt(TRADING_DAYS)

    # Zero-drift lognormal daily gross returns: log-return ~ Normal(0, daily_vol).
    log_ret = rng.normal(loc=0.0, scale=daily_vol, size=(N_DAYS, N_ASSETS))
    gross = np.exp(log_ret)

    prices = np.empty((N_DAYS, N_ASSETS))
    prices[0] = START_PRICE
    for t in range(1, N_DAYS):
        prices[t] = prices[t - 1] * gross[t]

    dates = pd.bdate_range(start=CALENDAR_START, periods=N_DAYS)
    return pd.DataFrame(prices, index=dates, columns=assets)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate synthetic_prices.csv (null by construction).")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "synthetic_prices.csv"))
    args = ap.parse_args()

    df = generate(args.seed)
    df.to_csv(args.out, index_label="date", float_format="%.10f")
    print(f"wrote {args.out}: {df.shape[0]} rows x {df.shape[1]} cols, seed={args.seed}")


if __name__ == "__main__":
    main()
