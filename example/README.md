# Worked example: a deliberately absurd thesis, run honestly

**What this is.** A complete, self-contained demonstration of a pre-registration research
pipeline applied to a thesis chosen *because* it is absurd: that assets bought during the
waxing lunar phase outperform those bought during the waning phase. The machinery is real —
frozen hypothesis grid, hash-chained trial ledger, Deflated Sharpe Ratio against an
expected-max benchmark, stationary block bootstrap — and the verdict is whatever the frozen
rule yields. (It yielded REFUTED. See `RESULTS.md`.)

**What this is not.** Nothing here relates to any real strategy, market, venue, or dataset.
The 12 assets (`SYN01`..`SYN12`) are synthetic: seeded i.i.d. lognormal daily returns with
zero drift and no calendar structure of any kind (`generate_data.py` is null by construction).
Every parameter is arbitrary by design. No real market data was used or consulted.

**Why it exists.** Pipelines are easy to trust when they confirm what you hoped. The honest
test of one is whether it refutes a hypothesis with no mechanism — and whether it would have
*detected* the effect had it been real. Both are demonstrated here: the null run refutes, and
the planted-answer test (`test_example.py`) shows the same machinery fires correctly when a
+30 bps/day effect is injected into a control dataset.

**Reproducibility.** Built by a coding agent (Claude Code) in an isolated session under a
documented access fence. Every number is reproducible from two seeds: data 20260612,
bootstrap 20260613. Pipeline: `generate_data.py` → `run_test.py`; integrity: `ledger.py`
(`verify_chain`); tests: `pytest test_example.py` (9 tests, all required green before the
single frozen run). The frozen test was executed exactly once.
