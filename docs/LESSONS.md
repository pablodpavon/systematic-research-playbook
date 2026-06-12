# Lessons

Every rule below was paid for. The research rules come from running a private systematic-trading research programme; they are published as generic rules only — the originating incidents stay private. The agent-governance rules come from building this repository's own worked example, where the isolation fence failed twice before it held. That story is told here because telling it is the honest version of this document.

## Research discipline

1. **Lock the hold-out before any selection-bearing look.** The cutoff that separates in-sample from held-out data must be frozen — committed, hash-fixed — before the first run that could influence a selection. A partition locked after you've already chosen among candidates on the full panel is not a hold-out; it's a formality.

2. **Commit the frozen pre-registration alone, before the run.** One commit containing only the SPEC, timestamped before any result exists, makes the freeze *provable from git history* rather than asserted. SPEC and results landing in the same commit proves nothing about ordering.

3. **Write the power-feasibility line before the run.** Compute the minimum effect your sample size can detect at your significance bar. If the effect you're hunting is below that line, the test cannot refute anything and a "positive" means little — and you should know that before spending the run, not after.

4. **Count every trial in an append-only ledger.** Exploratory or judged, every evaluated configuration is a draw from the multiple-testing lottery. Deflate reported performance by what you actually searched, not by what you chose to remember searching.

5. **Assert absence only as "not found by `<named check>`".** "It doesn't exist" is a claim about the world; "this grep over these paths returned nothing" is a claim about a check. Only the second one is verifiable, and only the second one tells a future reader what to re-run.

6. **The frozen rule decides the verdict — including the boring one.** A marginal positive indistinguishable from zero is a null, not a lead. Post-hoc investigation of cells the pre-registration didn't name is how dead hypotheses come back as false discoveries.

7. **Verify that every frozen section is consumed.** When a spec freezes an input that the test it governs never reads, that dead text becomes a drift seed — someone will later "fix" the test to match it, silently changing what was tested. Check consumption at freeze time.

## Agent governance

8. **A fence you haven't mechanically tested at its real layer is a hypothesis, not a control.** While building this repository's worked example, two consecutive configuration-layer fences (a permission file, then a pre-execution hook) looked correct, passed isolated tests — and never bound in the real session. The fence that held was operating-system isolation: a separate user the kernel refuses. Test the denial in the exact context that will run, at the layer that enforces it.

9. **Make the fence self-test the first step of the brief.** The worked example's brief opens by ordering the agent to probe the fence and halt on any success. That self-test caught both broken fences before a single deliverable line existed — at zero contamination cost, twice. Cheap, decisive, first.

10. **Filesystem fences do not cover network channels.** An OS-level fence can be kernel-tight while account-level connectors — which ride along with the agent's *login*, not the machine user — still reach the protected resource over the network. Enumerate every channel an agent has (filesystem, network/connectors, environment) and fence each at its own layer; doctrine covers whatever the mechanics miss, but doctrine alone is the last layer, not the first.

11. **Hook commands need absolute paths, and fail-closed is the correct failure direction.** A guard hook invoked by relative path, combined with a session-wide shared working directory, deadlocked an entire session: one `cd` into a subdirectory and every guarded tool failed before running — including the command that would have fixed it. Annoying, and exactly right: the fence failed *closed*. Use absolute paths in hook commands; accept that a good fence will occasionally lock you out too.

12. **When instructions conflict, the stricter rule wins — write your briefs knowing this.** Given a doctrine file forbidding any reference to protected paths and a brief instructing a probe of those same paths, the agent refused the probe, held the boundary at the stricter layer, and recorded the conflict instead of resolving it quietly. That is the resolution you want — so when a brief genuinely needs an exception to standing doctrine, declare the exception in the doctrine itself, not in the brief.
