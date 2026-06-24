# Lessons

Every rule below was paid for. The research and execution-discipline rules come from running a private systematic-trading research programme; they are published as generic rules only — the originating incidents stay private. The agent-governance rules come from building this repository's own worked example, where the isolation fence failed twice before it held. That story is told here because telling it is the honest version of this document.

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

## More research discipline

These were added as the programme continued past the founding batch — generic form, originating incidents private.

13. **Cost is a first-class risk, not a post-filter.** A mechanism can be real and the edge still die: turnover-scaled cost — fees, slippage, and any financing leg — can swamp a genuine gross premium entirely. Model cost from the first run, not as a final adjustment; the only number a verdict reads is net-of-cost; and a configuration that is gross-positive but net-negative is a refutation, not a "close call". The most expensive way to learn this is to find a real signal and then watch trading frequency eat all of it.

14. **A new signal must be *stably* distinct from the ones you already have, not just distinct.** Before a feature earns a place in a model, show that it adds information beyond your existing inputs — and that the (non-)redundancy holds across time, not only in aggregate. A signal that looks independent in one period and collapses into an existing one in another doesn't sharpen the model; it manufactures false structure, and a coarse input you can trust beats a rich one that drifts.

15. **Quarry your dead hypotheses; a refuted thesis still pays.** A stopped or refuted hypothesis leaves byproducts — a mechanism you now understand, an instrument you built, a dataset you cleaned, a method fix, a negative result that rules out a whole neighbourhood. At every closure, inventory what was *produced*, not just the verdict; the next hypothesis is often assembled from what the last one left behind.

## Execution and process discipline

16. **Self-audit every deliverable before it ships — hardest on the ones nothing else checks.** Code has tests; a number has a recomputation; a design document has nothing but your own re-reading. Re-read each artifact critically against the standard before handing it over, and treat un-executed prose as the highest-risk case: it is the one place where a load-bearing omission has no automated gate to catch it except your own attention.

17. **Confirm the code path and the data exist before you build on them.** "The function is probably there, the column is probably named that" is how an implementation cycle gets spent on a wrong assumption. Read the API, read the schema, confirm the path — *before* writing the code that depends on it. Verification before construction is far cheaper than debugging a build founded on a guess.

18. **An assumed platform limit is a defect waiting to ship.** A constraint you remember, or copy from your own old notes, is not a measured constraint. Character caps, rate limits, payload sizes, API shapes — measure the real limit against the live target before you rely on it, because the version in your head is exactly the kind of thing that has quietly changed since you wrote it down.

19. **An automated edit verifies it parses and that its anchor is unique — before it touches anything.** A script that rewrites files is a loaded tool: it must confirm the new content compiles, and that the text it keys off matches *exactly once*, before applying a single change. An anchor that matches twice silently edits the wrong place; one that matches zero times silently does nothing while reporting success. Pre-flight both.

20. **A close-out is exhaustive or it rots.** When a unit of work finishes, every document that records its state updates in the same pass — the status handoff, the running log, the changelog, the cross-references that point at it. A half-updated record is worse than none: it carries the authority of being written down while being wrong, and the next reader trusts it.

21. **A check is only as good as the layer it actually exercises.** A verification that passes by touching a different path than the one you care about proves nothing about the path you care about — a check that cannot fail is not a check. Pair every automated check with a probe that exercises the real path, and confirm the check would actually go red if the thing it guards were broken.

22. **Mutate live state atomically, and make rollback match how the running system holds the resource.** When you change something a running system is reading, the change must be atomic to readers — they see the old state or the new one, never a half-built intermediate (one transaction, or build-aside-then-swap). And a rollback only counts if it respects how the process actually holds the resource: a process holding a file open will not see a file swapped underneath it, so restore in place.
