#!/usr/bin/env python3
"""Run the frozen lunar-phase test exactly as pre-registered.

Loads synthetic_prices.csv, evaluates all 8 pre-registered grid cells (each one
ledgered), computes the Deflated Sharpe Ratio of the best net-of-cost cell against
the expected-max-SR benchmark for N=8 trials (Bailey & Lopez de Prado 2014), runs
the 1,000-path stationary block bootstrap for that cell's mean daily return, and
prints the verdict strictly per the frozen rule. No discretionary inputs.
"""
from __future__ import annotations

import math
import os

import numpy as np
import pandas as pd

import ledger

SYNODIC_DAYS = 29.530588
EPOCH = pd.Timestamp("2000-01-06")          # new-moon epoch: phase 0
TRADING_DAYS = 252
DATA_SEED = 20260612
BOOT_SEED = 20260613
N_TRIALS = 8
EULER_GAMMA = 0.5772156649015329

GRID = [
    {"split": split, "horizon": h, "cost_bps": c}
    for split in ("half-cycle", "quartile-extremes")
    for h in (1, 5)
    for c in (0, 10)
]


def lunar_phase(dates: pd.DatetimeIndex) -> np.ndarray:
    """Phase fraction in [0, 1): 0 = new moon, 0.5 = full, by synodic approximation."""
    days = (dates - EPOCH).total_seconds() / 86400.0
    return np.mod(days / SYNODIC_DAYS, 1.0)


def base_signal(phase: np.ndarray, split: str) -> np.ndarray:
    """Daily directional signal: +1 long (waxing), -1 short (waning), 0 flat."""
    if split == "half-cycle":
        return np.where(phase < 0.5, 1.0, -1.0)
    if split == "quartile-extremes":
        sig = np.zeros_like(phase)
        sig[phase < 0.25] = 1.0
        sig[(phase >= 0.5) & (phase < 0.75)] = -1.0
        return sig
    raise ValueError(f"unknown split: {split}")


def portfolio_returns(prices: pd.DataFrame, split: str, horizon: int,
                      cost_bps: float) -> tuple[np.ndarray, np.ndarray]:
    """(gross, net) daily long-short return series for one grid cell.

    Market leg = equal-weighted mean of the 12 assets' simple daily returns.
    Position on day t = mean of the base signals over the last `horizon` days
    (overlapping holding). The lunar phase is astronomically deterministic, so
    using day t's phase for day t's position involves no information leakage.
    Cost: half the round-trip rate per unit of position traded.
    """
    px = prices.to_numpy()
    rets = px[1:] / px[:-1] - 1.0                     # (T-1, n_assets)
    mkt = rets.mean(axis=1)
    phase = lunar_phase(prices.index[1:])
    sig = base_signal(phase, split)
    if horizon > 1:
        kernel = np.ones(horizon) / horizon
        pos = np.convolve(sig, kernel)[: len(sig)]    # mean of last `horizon` signals
    else:
        pos = sig
    gross = pos * mkt
    per_side = (cost_bps / 1e4) / 2.0
    turnover = np.abs(np.diff(pos, prepend=0.0))
    net = gross - per_side * turnover
    return gross, net


def sharpe_daily(returns: np.ndarray) -> float:
    sd = returns.std(ddof=1)
    return float(returns.mean() / sd) if sd > 0 else 0.0


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(q: float) -> float:
    """Inverse standard normal CDF by bisection on erf (deterministic, ample precision)."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def expected_max_sr(trial_srs: list[float]) -> float:
    """Bailey-LdP expected maximum daily SR among N independent trials under the null."""
    n = len(trial_srs)
    var_sr = float(np.var(trial_srs, ddof=1))
    return math.sqrt(var_sr) * ((1.0 - EULER_GAMMA) * norm_ppf(1.0 - 1.0 / n)
                                + EULER_GAMMA * norm_ppf(1.0 - 1.0 / (n * math.e)))


def deflated_sharpe(sr_hat: float, sr_star: float, returns: np.ndarray) -> float:
    """DSR = PSR evaluated at the expected-max-SR benchmark, with skew/kurtosis terms."""
    t = len(returns)
    mu, sd = returns.mean(), returns.std(ddof=1)
    z = (returns - mu) / sd
    skew = float(np.mean(z ** 3))
    kurt = float(np.mean(z ** 4))                     # Pearson (normal = 3), per Bailey-LdP
    denom = math.sqrt(1.0 - skew * sr_hat + ((kurt - 1.0) / 4.0) * sr_hat ** 2)
    return norm_cdf((sr_hat - sr_star) * math.sqrt(t - 1) / denom)


def stationary_bootstrap_ci(returns: np.ndarray, n_draws: int = 1000,
                            mean_block: float = 21.0, seed: int = BOOT_SEED,
                            ci: float = 0.90) -> tuple[float, float]:
    """Politis-Romano stationary block bootstrap CI for the mean daily return."""
    rng = np.random.default_rng(seed)
    t = len(returns)
    p = 1.0 / mean_block
    means = np.empty(n_draws)
    for d in range(n_draws):
        idx = np.empty(t, dtype=np.int64)
        idx[0] = rng.integers(t)
        new_block = rng.random(t) < p
        for i in range(1, t):
            idx[i] = rng.integers(t) if new_block[i] else (idx[i - 1] + 1) % t
        means[d] = returns[idx].mean()
    alpha = (1.0 - ci) / 2.0
    return (float(np.quantile(means, alpha)), float(np.quantile(means, 1.0 - alpha)))


def evaluate_grid(prices: pd.DataFrame, ledger_path: str) -> list[dict]:
    """Evaluate every pre-registered cell, ledger each one, return the cell records."""
    cells = []
    for cfg in GRID:
        gross, net = portfolio_returns(prices, cfg["split"], cfg["horizon"], cfg["cost_bps"])
        metrics = {
            "sharpe_gross_daily": sharpe_daily(gross),
            "sharpe_net_daily": sharpe_daily(net),
            "sharpe_net_annualized": sharpe_daily(net) * math.sqrt(TRADING_DAYS),
            "mean_net_daily": float(net.mean()),
            "T": int(len(net)),
        }
        row = ledger.append(ledger_path, {**cfg, "data_seed": DATA_SEED}, metrics)
        cells.append({"cfg": cfg, "metrics": metrics, "net": net, "seq": row["seq"]})
    return cells


def run(prices: pd.DataFrame, ledger_path: str, boot_seed: int = BOOT_SEED) -> dict:
    """Full frozen procedure on a price panel; returns the verdict record."""
    cells = evaluate_grid(prices, ledger_path)
    best = max(cells, key=lambda c: c["metrics"]["sharpe_net_daily"])
    trial_srs = [c["metrics"]["sharpe_net_daily"] for c in cells]
    sr_star = expected_max_sr(trial_srs)
    dsr = deflated_sharpe(best["metrics"]["sharpe_net_daily"], sr_star, best["net"])
    ci_lo, ci_hi = stationary_bootstrap_ci(best["net"], seed=boot_seed)
    ci_excludes_zero = (ci_lo > 0.0) or (ci_hi < 0.0)
    verdict = "PASS" if (dsr > 0.95 and ci_excludes_zero) else "REFUTED"
    return {"cells": cells, "best": best, "sr_star": sr_star, "dsr": dsr,
            "ci": (ci_lo, ci_hi), "ci_excludes_zero": ci_excludes_zero, "verdict": verdict}


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    prices = pd.read_csv(os.path.join(here, "synthetic_prices.csv"),
                         index_col="date", parse_dates=True)
    ledger_path = os.path.join(here, "trial_ledger.jsonl")
    res = run(prices, ledger_path)

    print(f"{'seq':>3} {'split':<19} {'h':>2} {'cost':>5} "
          f"{'SR_gross(d)':>12} {'SR_net(d)':>10} {'SR_net(ann)':>12} {'mean_net(d)':>12}")
    for c in res["cells"]:
        m, g = c["metrics"], c["cfg"]
        print(f"{c['seq']:>3} {g['split']:<19} {g['horizon']:>2} {g['cost_bps']:>4}b "
              f"{m['sharpe_gross_daily']:>12.5f} {m['sharpe_net_daily']:>10.5f} "
              f"{m['sharpe_net_annualized']:>12.4f} {m['mean_net_daily']:>12.3e}")

    b = res["best"]
    print(f"\nbest net cell: seq {b['seq']} {b['cfg']}")
    print(f"expected-max SR* (N={N_TRIALS}, daily): {res['sr_star']:.5f}")
    print(f"Deflated Sharpe Ratio: {res['dsr']:.4f}  (rule: > 0.95)")
    print(f"bootstrap 90% CI for mean daily return: [{res['ci'][0]:.3e}, {res['ci'][1]:.3e}]"
          f"  (rule: excludes 0 -> {res['ci_excludes_zero']})")
    ok, bad = ledger.verify_chain(ledger_path)
    print(f"ledger chain verified: {ok} (rows 0..{len(res['cells']) - 1})")
    print(f"\nVERDICT: {res['verdict']}")


if __name__ == "__main__":
    main()
