# Pre-registration — "Lunar-phase momentum" (frozen)

**Status:** FROZEN before any result was observed. This document is the contract.
The test below is run exactly once, with the seeds named here, and the verdict is whatever
the frozen rule yields. This is a *worked example on synthetic data*: the thesis is
deliberately absurd and the dataset contains no lunar effect by construction. Its purpose is
pedagogical — to show the full pre-registration → test → verdict machinery behaving honestly
on a hypothesis that should be refuted.

---

## 1. Hypothesis (one falsifiable sentence)

Assets bought while the moon is in its **waxing** phase outperform assets bought while the
moon is in its **waning** phase over the holding horizon.

This is falsifiable: it predicts a positive, statistically distinguishable mean return for a
long-waxing / short-waning basket, net of cost. If that quantity is not distinguishable from
zero under the frozen rule, the hypothesis is refuted.

## 2. Economic mechanism (played honest)

There is no credible mechanism. For a return premium to persist, someone must systematically
pay for it — a hedger offloading risk, a constrained holder forced to sell, a structural payer.
No one systematically loses money to the lunar calendar; the moon's phase is common knowledge,
costless to observe, and connected to no cash flow, funding obligation, or risk transfer in the
assets traded here. There is therefore no payer and no persistence mechanism.

The thesis is admitted into the pipeline precisely *because* it has no mechanism: it is the
control case for the mechanism screen. A screen that cannot reject this should not be trusted to
pass anything. We expect refutation, and we want the machinery — not our prior — to deliver it.

## 3. Literature grounding

No supporting literature exists; folklore only. There is no peer-reviewed finding of a tradeable
lunar-phase return premium in the asset class modeled here. The absence of literature is itself a
recorded input to the verdict, not an oversight.

## 4. Frozen test design

- **Data:** `synthetic_prices.csv`, produced by `generate_data.py` with seed **20260612**.
  12 assets (`SYN01`..`SYN12`), 2,520 daily bars (~10 trading years), prices starting at 100.0,
  i.i.d. lognormal daily returns with zero drift and per-asset annualized volatility drawn once
  from U[0.15, 0.35]. There is **zero cross-asset lunar structure by construction** — returns do
  not depend on the calendar in any way.
- **Lunar phase:** computed by synodic approximation. Synodic period **29.530588 days**;
  new-moon epoch **2000-01-06** (phase 0 at the epoch). Phase fraction for a date `d` is
  `((d − epoch) / 29.530588) mod 1`. **Waxing** = phase fraction in [0, 0.5) (new → full);
  **waning** = [0.5, 1.0) (full → new).
- **Signal:** each day, go long an equal-weighted basket of assets designated "waxing" and short
  an equal-weighted basket designated "waning", rebalanced daily, held for the configuration's
  horizon. The portfolio return series is the daily long-short return net of the configured cost.
  (Because the phase is a single global calendar value, the waxing/waning designation is varied
  across assets by the phase-split rule below so that both baskets are populated each day.)

## 5. Complete a-priori grid (every cell ledgered)

The grid is fixed at **8 configurations** and never grows:

| Factor          | Levels                                  |
|-----------------|-----------------------------------------|
| Phase split     | {half-cycle, quartile-extremes}         |
| Holding horizon | {1 day, 5 days}                         |
| Cost            | {0 bps, 10 bps round-trip}              |

2 × 2 × 2 = **8** cells. Every cell is computed and written to the hash-chained trial ledger,
including dominated ones. No cell is added, dropped, or silently skipped after freezing.

- *half-cycle*: waxing = phase in [0, 0.5), waning = [0.5, 1.0).
- *quartile-extremes*: waxing = phase in [0, 0.25) (around new moon), waning = [0.5, 0.75)
  (just past full); the mid-quartiles are excluded, sharpening the contrast the folklore claims.

## 6. Power-feasibility (mandatory — arithmetic shown)

We must confirm the test can detect an effect worth caring about before running it. Invert the
PSR lower bound. The Probabilistic Sharpe Ratio reaches 95% one-sided confidence that the true
Sharpe exceeds 0 when

    T ≥ 1 + (z / SR_period)²,   z = Φ⁻¹(0.95) = 1.645

Solving for the minimum detectable per-period (daily) Sharpe at T = 2,520:

    SR_daily,min = 1.645 / √(2,520 − 1)
                 = 1.645 / √2,519
                 = 1.645 / 50.1896
                 = 0.032776   (per day)

Annualizing at 252 trading days (SR scales with √periods):

    SR_ann,min = 0.032776 × √252 = 0.032776 × 15.8745 = 0.5203

**Minimum detectable Sharpe ≈ 0.52 annualized-equivalent** at 95% one-sided over 2,520 daily
returns. Any lunar effect large enough to matter economically would exceed this comfortably, so
the test is **adequately powered**: a failure to detect is evidence of absence, not of weak power.

## 7. Verdict rule (numeric — exactly two outcomes)

Let the **best net-of-cost configuration** be the grid cell with the highest net daily Sharpe.

**PASS** iff *both* hold for that best cell:

1. **Deflated Sharpe Ratio > 0.95.** The DSR deflates the observed Sharpe against the
   expected maximum Sharpe from N = 8 independent trials (Bailey & López de Prado, 2014),
   using the expected-max-SR benchmark
   `SR* = √Var[SR] · ((1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e)))`, γ = Euler–Mascheroni ≈ 0.5772,
   then PSR evaluated at `SR*` with the series' skewness and kurtosis terms; **and**
2. **Bootstrap CI excludes 0.** A 1,000-draw stationary block bootstrap (mean block length
   21 days, seed **20260613**) of the best cell's mean daily return yields a 90% confidence
   interval that does **not** contain 0.

**REFUTE** otherwise. There is no third outcome and no discretionary override.

## 8. Seeds and scope

- Data generation seed: **20260612**.
- Bootstrap seed: **20260613**.
- **Out of scope:** anything not in the 8-cell grid — other phase definitions, other horizons,
  other assets, other cost models, regime conditioning, parameter search of any kind. Exploring
  out-of-scope variants after seeing the result would void this pre-registration.

## 9. Corrections

None yet.
