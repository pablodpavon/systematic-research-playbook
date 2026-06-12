# systematic-research-playbook

**How I run a systematic-trading research programme with AI agents — built so that bad ideas die fast, cheap, and on the record.**

This repository documents a *method*, not a strategy. It covers two things: the research discipline (economic-mechanism-first hypotheses, frozen pre-registrations, a counted trial ledger, honest verdicts) and the AI-orchestration architecture (a permission-fenced coding agent, doc-driven execution briefs, two-instance audits, human-gated git) that I use to run a private systematic-trading research programme.

**What you will not find here.** The real programme's strategies, hypotheses, parameters, data, results, and infrastructure are private and never appear in this repository — not in files, not in commit history, not in examples. The worked example uses a deliberately absurd synthetic thesis on generated data. If you came to copy an edge, there isn't one here. If you came to copy a *way of working*, take all of it.

## Why this exists

Most exciting backtests are false discoveries. Test enough variations and something will look brilliant by luck alone — finance research has documented this at scale (Harvey, Liu & Zhu 2016; Bailey & López de Prado 2014), and it is the same multiple-testing failure that plagues published science generally (Ioannidis 2005). The method documented here is engineered against that failure — and against the subtler one of fooling yourself with your own tools.

The second reason: in 2026 anyone can have an AI write code. Almost nobody documents how to *govern* AI agents doing research — permission fences, audit splits, provable pre-registrations, human-gated commits. That governance layer is the part of this repository I have not seen written down elsewhere, so I wrote it down.

## The method in one paragraph

Every hypothesis starts as an economic mechanism (who pays, and why does the opportunity persist?), gets grounded in published literature before any data is touched, is frozen as a pre-registration committed to git *before* the first run, is tested with the cheapest test that can falsify it, with every evaluated configuration counted in an append-only ledger that deflates reported performance for multiple testing — and ends in an honest verdict, where refutation is a success, not a failure. The full pipeline, with the statistics explained in plain language: [docs/METHOD.md](docs/METHOD.md).

## The AI architecture in one paragraph

Two roles. A chat-based co-designer writes specifications, makes judgment calls, and reviews output. A coding agent implements — under a written permission fence: explicit allowed write-scopes, denied paths, a pre-execution guard hook, and **no git rights** (a human makes every commit, every time). Work is delegated through versioned brief files on disk and launched with one line; outputs are written incrementally with status lines so an interrupted session loses nothing; audits split fact-extraction from judgment across *separate* agent instances so the agent never grades its own work; and every artifact that moves between machines is gated by a checksum. Full doctrine and example configs: `docs/AI_ORCHESTRATION.md` (next on the roadmap).

## Repository map

```
README.md                    you are here
LICENSE                      MIT
docs/
  METHOD.md                  the research pipeline, step by step
  AI_ORCHESTRATION.md        agent governance doctrine          (planned)
  LESSONS.md                 hard-won rules, in generic form    (planned)
example/                     a synthetic thesis run end-to-end  (planned)
templates/                   empty pre-registration / results / incident templates (planned)
```

## Roadmap

1. ✅ Method documentation (this commit)
2. Agent-governance doctrine, scrubbed fence configs, document templates
3. The worked example: a deliberately false thesis ("lunar-phase momentum") on seeded synthetic data, carried through the entire pipeline to its honest refutation — implemented by the coding agent itself, in an isolated session, under the documented fence

## About

I'm a senior business and data analyst, not a professional programmer — which is precisely why the orchestration layer exists, and why it is documented to be reproducible by other non-programmers in the same position. I design, specify, and audit; AI agents implement under fences I control. The research programme itself is private; this playbook is the part worth sharing.

## License

MIT — see [LICENSE](LICENSE).
