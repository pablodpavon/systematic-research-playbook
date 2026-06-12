# AI Orchestration: governing agents that do research

This is the part of the playbook I haven't seen written down elsewhere. Anyone can have an AI write code in 2026. The hard part — the part that decides whether you can *trust* what came back — is governance: who decides, who implements, who verifies, and what stops an agent from quietly doing the wrong thing. This document is the doctrine I run, generic enough to copy.

A note on my position: I'm not a professional programmer. That constraint designed this architecture. I can't review every line of code for correctness, so the system is built so I don't have to — roles are split, permissions are explicit, every transfer is checksummed, and a human (me) sits at every irreversible step.

## The two-role architecture

**Role 1 — the co-designer (chat-based agent).** Writes specifications, makes judgment calls, reviews outputs, drafts documents. Has no hands: it cannot touch the codebase, run jobs, or commit. Its product is *decisions and text*.

**Role 2 — the implementer (coding agent).** Executes specifications inside a permission fence on a real machine. Has hands but no authority: it cannot commit, cannot push, cannot touch protected paths, and never decides *what* should be built.

The split is the point. A single agent that designs, implements, and evaluates its own work will grade itself generously — same failure mode as a human, faster. Splitting roles means every artifact crosses at least one boundary where a different party (the other role, or me) looks at it cold.

**Role 0 — the human.** I own every commit, every merge, every purchase, every irreversible action. Both agents produce; I ratify. This is not ceremony — it is the single control that makes the rest recoverable.

## The fence: deny by default

The coding agent runs inside three independent layers. Any one of them failing still leaves two.

1. **Workspace isolation.** The agent works in a dedicated workspace (a separate clone or worktree), never in the production tree. Worst case, the blast radius is a disposable directory.
2. **Permission configuration.** An explicit allow/deny policy file: denied paths (protected source, system commands, anything destructive), allowed write-scopes (the research workspace only), and **no git mutations** — the agent can read history but never write it. Deny rules win over allow rules.
3. **A pre-execution guard.** A hook that inspects each shell command before it runs and blocks pattern-matches against a denylist. Crude and occasionally overcautious — mine has blocked legitimate commands, and the agent simply rerouted — which is exactly the right failure direction.

Config syntax varies by tool and version; the example files in this repo (`.claude/settings.example.json`, `.claude/CLAUDE.example.md`) show the *shape* with placeholder paths. Verify field names against your tool's current documentation before relying on them.

The principle underneath: **the fence is policy, not trust.** You don't fence an agent because you expect malice; you fence it because "it probably won't" is not an engineering control.

## Doc-driven execution

Work is delegated to the coding agent through a **versioned brief file on disk**, not through a chat conversation. The brief is the complete session contract: role and hard boundaries, what to read first, exact deliverables, what must NOT be touched, and a terminal-summary format. The launch is one line: *"Read `<brief>` and execute it exactly. That document is your complete brief for this session."*

Why a file and not a conversation:

- **Reviewable before execution.** The brief is re-read and corrected as a document, with a checksum, before the agent ever sees it.
- **Reproducible.** The brief is committed next to its output as one logical unit; six months later, the instruction set that produced an artifact is in the same commit as the artifact.
- **Interruption-safe by contract.** The brief requires *incremental output*: the agent writes its output file as it goes, ending every write with a `STATUS:` line listing which sections are COMPLETE and which are PENDING. A crashed or interrupted session loses minutes, not hours — and the status line tells you exactly where to resume.

## Two-instance audits: facts and judgment never share a brain

When the work is an *audit* — reviewing past research, verifying integrity, checking claims — I split it across two separate agent instances:

- **The extraction instance** gathers facts only: file-cited, line-cited, verbatim where it matters. Its brief forbids conclusions, severities, and anything supplied from memory ("never supply a prescription from memory" is a literal line in the brief). Where something is absent, it must record the *specific check that established absence* — "not found by `<command>`" — never "does not exist".
- **The judgment instance** reads the extraction cold and issues verdicts — and it independently re-reads a sample of the load-bearing citations before trusting any of them. Spot-check results are recorded in the judgment document itself.

This mirrors how serious human audits work: the evidence gatherer and the opinion writer are different people. With agents it costs almost nothing to enforce, and it caught real issues in my programme that a single self-reviewing pass would have sailed past.

## Transfer integrity: checksums on everything

Every artifact that moves between machines — my laptop, the chat environment, the server — is verified by SHA-256 before use. The producing side publishes the hash; the receiving side recomputes it; nothing proceeds on a mismatch. This sounds paranoid until the first time a file arrives subtly different from what was reviewed — a truncated download, an editor's silent reformat, the wrong version of a similarly-named file. The gate has caught both real corruption and false alarms (a viewer rendering a file as blank that was byte-perfect); in both cases the hash settled the question in seconds, in the right direction.

Two companion habits: **never reuse a filename across iterations** (version-suffix everything: `_v1`, `_v2` — stale-file bugs are transfer bugs), and **record run metadata** (agent tool version, model identifier, date) inside every produced artifact, read from the machine, not assumed.

## What the agent must never do

A short list, absolute, enforced by the fence and re-stated in every brief:

- Never commit or push. A human makes every commit.
- Never touch protected paths (production source, system configuration).
- Never act on credentials, secrets, or payment-capable surfaces.
- Never assert absence without naming the check that established it.
- Never silently edit frozen documents — corrections are declared, appended, dated.

## Failure modes, honestly

- **Fences over-block.** Pattern guards stop legitimate commands; agents reroute or you whitelist deliberately. Annoying, and the correct trade.
- **Semantic search lies by omission.** Indexes lag fresh commits; exact-path reads beat search for recent files. Treat "search found nothing" as "this search found nothing".
- **Agents fill gaps confidently.** The single highest-value line in any brief is the one that forbids answering from memory and requires a citation or a named check.
- **Long sessions drift.** The incremental-output contract and the terminal-summary contract exist because the failure you must design for is the session that dies at 90%.

## Why this matters beyond trading

Nothing above is specific to markets. It is a governance pattern for *any* AI-assisted knowledge work where being wrong is expensive: split design from implementation, fence the hands, gate the irreversible steps on a human, checksum the transfers, and never let the same instance gather the evidence and write the verdict.
