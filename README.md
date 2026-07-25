# Systematic Trading Research Platform

**A solo-built platform for running quantitative research the way a regulated data function should — engineered so that bad ideas die fast, cheap, and on the record.**

This repository documents a **method and its engineering discipline**, not a strategy. It is the public, sanitized face of a private systematic-trading research programme: what you can see is *how* the research is run — the data architecture, the quality gates, the decision governance, and the validation standard — never *what* is traded.

> **What you will not find here.** The programme's strategies, hypotheses, parameters, data, results, and infrastructure are private and appear nowhere in this repository — not in files, not in commit history, not in examples.

---

## Why it's rigorous

Most exciting backtests are false discoveries: test enough variations and something will look brilliant by luck alone. The whole platform is engineered against that single failure mode — **make it structurally difficult to fool yourself** — enforced through architecture, tests, and documentation rather than good intentions.

## What this demonstrates

Engineering and data-governance discipline, mapped to the competencies it exercises:

| Competency | How it shows up here |
|---|---|
| **Data architecture & pipelines** | Versioned SQLite store, exchange-API ingestion (`ccxt`), idempotent (re-runnable) migrations, checksum-verified transfers between machines. |
| **Testing & data QA** | 1,294+ automated tests as a reliability system: point-in-time (as-of-t) no-look-ahead guards, regression over frozen surfaces, hash-chain / fingerprint integrity checks, planted-bug self-tests. |
| **Documentation-as-governance** | 45+ Architecture Decision Records, 30+ strategy memos, a living decision register, and 17 incident post-mortems — the auditable "decision papers" that make every call traceable. Frozen text is never edited; corrections are declared and labelled. |
| **KPI / metric definition** | Success is a *pre-registered, falsifiable* rule with explicit PASS/REFUTE thresholds and no third outcome; headline metrics are **deflated for the number of trials** (multiple-testing correction). |
| **Hypothesis → validation** | Books-first, mechanism-first; a pre-registration frozen to version control *before* any data contact; honest verdicts, where a refutation is a success. |
| **Monitoring & reproducibility** | Long jobs run as monitored `systemd` services with health gates and structured logs; expensive runs are checkpointed and resumable; a documentation-freshness assertion fails loudly on drift. |

## The method

The full pipeline —

```
mechanism → literature → frozen pre-registration → cheapest decisive test
          → counted ledger → honest verdict → (survivors only) held-out → forward
```

— is documented in **[docs/METHOD.md](docs/METHOD.md)**, written for a mixed audience: plain-language explanations for data/product readers, page-cited primary sources for quants (López de Prado, Harvey–Liu–Zhu, Ioannidis, Carver).

## How it's built

Two roles, by design. A chat-based co-designer writes specifications, defines success criteria, and reviews output; a coding agent implements — under a **written permission fence**: explicit allowed write-scopes, denied paths, a pre-execution guard hook, and **no git rights** (a human makes every commit, every time). This is AI-assisted development with the governance made explicit and enforced, not assumed.

## Scope & honesty

Independent research project on **paper trading**. No live-performance or profit claims are made — the value on display is method and engineering discipline, not returns.

---

*Full method: [docs/METHOD.md](docs/METHOD.md) · License: MIT*
