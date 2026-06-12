# RESULTS — "Lunar-phase momentum" (frozen run, single execution)

## Run metadata

| Field | Value |
|---|---|
| Pre-registration | `SPEC_preregistration.md` (frozen before execution) |
| Data | `synthetic_prices.csv` — 2,520 daily rows × 12 assets (`SYN01`..`SYN12`), null by construction |
| Data seed | 20260612 |
| Bootstrap seed | 20260613 |
| Trial ledger | `trial_ledger.jsonl` — 8 rows, seq 0–7, hash chain verified (`verify_chain` → ok) |
| Test suite | `pytest example/test_example.py` → 9 passed (incl. planted-answer detector validation) |
| Agent tool | `claude --version` → 2.1.175 (Claude Code) |
| Model | `claude-fable-5` (Fable 5) — switched to via `/model` before the frozen run; session began on `claude-opus-4-8[1m]` (self-reported; no `model` field in settings) |
| Stack | Python 3.12.3, numpy 2.4.6, pandas 3.0.3 |
| Executions of the frozen test | **1** (no reruns, no seed changes) |

## Headline vs frozen rule

| Frozen criterion | Threshold | Observed | Met? |
|---|---|---|---|
| Deflated Sharpe Ratio (best net cell, N=8 benchmark) | > 0.95 | **0.1530** | No |
| Stationary block-bootstrap 90% CI for mean daily return excludes 0 | excludes 0 | **[−1.134e−04, +1.189e−04]** — contains 0 | No |

**VERDICT: REFUTED** (rule requires both; neither held).

## Trial accounting

All 8 pre-registered grid cells were run and ledgered — none added, none dropped
(ledger seq 0–7, chain intact):

| seq | split | horizon | cost | SR gross (daily) | SR net (daily) | SR net (ann.) | mean net (daily) |
|---|---|---|---|---|---|---|---|
| 0 | half-cycle | 1 | 0 bps | −0.00505 | −0.00505 | −0.080 | −2.300e−05 |
| 1 | half-cycle | 1 | 10 bps | −0.00505 | −0.02587 | −0.411 | −1.181e−04 |
| 2 | half-cycle | 5 | 0 bps | −0.00091 | −0.00091 | −0.014 | −3.433e−06 |
| 3 | half-cycle | 5 | 10 bps | −0.00091 | −0.02591 | −0.411 | −9.819e−05 |
| 4 | quartile-extremes | 1 | 0 bps | 0.00181 | 0.00181 | 0.029 | +5.873e−06 |
| 5 | quartile-extremes | 1 | 10 bps | 0.00181 | −0.02745 | −0.436 | −8.920e−05 |
| 6 | quartile-extremes | 5 | 0 bps | 0.00152 | 0.00152 | 0.024 | +4.014e−06 |
| 7 | quartile-extremes | 5 | 10 bps | 0.00152 | −0.03445 | −0.547 | −9.075e−05 |

- Best net cell: **seq 4** (quartile-extremes, 1-day horizon, 0 bps) — daily SR 0.00181
  (≈ 0.029 annualized).
- Expected-max-SR benchmark across the 8 trials (Bailey–LdP): SR* = 0.02221 daily — i.e. the
  *luckiest* of 8 null trials is expected to look ~12× better than this best cell actually does.
- **Deflated Sharpe Ratio = 0.1530.**

## Per-hypothesis disposition

| Hypothesis | Disposition |
|---|---|
| H1: waxing-phase basket outperforms waning-phase basket over the holding horizon | **REFUTED.** Best of 8 pre-registered configurations is statistically indistinguishable from luck (DSR 0.153 vs required 0.95) and its mean daily return CI straddles 0. Every cost-bearing cell is outright negative. |

## The honest verdict

The data contained no lunar effect by construction, and the pipeline said so. The detector is
not toothless: the planted-answer test shows that injecting a +30 bps/day waxing effect into a
control dataset flips the same machinery to PASS, and removing it flips it back. The pipeline
refuted the thesis because the thesis is false, not because the test was weak — the
pre-registered power line shows any Sharpe above ≈ 0.52 annualized was detectable.

## Corrections

None.

## What would reopen it

Nothing — the mechanism section already told us the answer; the pipeline merely confirmed it
cheaply.
