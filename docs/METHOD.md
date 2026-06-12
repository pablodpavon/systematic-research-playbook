# The Method

This is the research pipeline I run, written for a mixed audience: if you work in data, product, or analysis, every statistical term gets a plain-language explanation the first time it appears; if you're a quant, the citations point at the primary sources.

The design goal is simple to state and hard to live by: **make it structurally difficult to fool yourself.**

## The problem this method solves

Two distinct failures kill quantitative research, and they need different defenses (the framing follows López de Prado, *Causal Factor Investing*, 2023):

**Failure A — you tested too many things.** Try enough parameter combinations and one will look spectacular by pure luck. The fix is mechanical: *count every attempt* and discount the best result accordingly. This is what the Deflated Sharpe Ratio does (Bailey & López de Prado 2014) — in plain language: the more lottery tickets you bought, the less impressed anyone should be that one of them won.

**Failure B — you found a real pattern with no real cause.** Correlation that held historically but isn't anchored in an economic reason can vanish the day you trade it. More data does not fix this; out-of-sample testing does not fix this. Only a causal story does: *who is paying, and why does the opportunity persist instead of being competed away?*

Everything below exists to defend against one of these two.

## The pipeline

```
mechanism → literature → frozen pre-registration → cheapest decisive test
          → counted ledger → honest verdict → (survivors only) held-out → forward
```

### 1. Mechanism first

No hypothesis enters the pipeline without an economic mechanism: who pays, why the payment persists, and why it hasn't already been arbitraged away. "The chart looks like it mean-reverts" is not a mechanism. This step is the Failure-B screen, and it is deliberately placed *before* any data is touched — a mechanism invented after seeing the data is a rationalization, not a screen.

### 2. Literature first

Before designing any test, read the canonical sources — actually read them, with page-cited notes, not summaries from memory. If the literature already prescribes the standard test of a mechanism, run the literature's test before your clever variation. Design decisions cite pages. This sounds bureaucratic; in practice it has repeatedly replaced a weak home-grown design with a stronger published one before any compute was spent.

### 3. Frozen pre-registration — committed before any data contact

A pre-registration is a short document that fixes, in advance: the hypothesis as a falsifiable sentence; the exact test design; the *complete* parameter grid (set a priori, from the literature — never extended after peeking); the cost model; the random seeds; and the verdict rule — explicit PASS/REFUTE thresholds with **no third outcome** ("almost passed" is not a verdict).

Two hard rules make the freeze real rather than asserted:

- **Freeze-commit rule.** The pre-registration is committed to git *alone*, at the moment of freezing, before the run. The freeze must be provable from commit history — not claimed in a document written afterward.
- **Lock-before-look rule.** If a held-out data partition will ever judge this family of hypotheses, freeze that partition's cutoff *before* the first selection-bearing run on the data. A hold-out carved out after you've already selected a candidate on the full sample is not out-of-sample for that candidate — it just looks like one.

If a defect is found after the freeze, the fix is a *declared, labelled correction* appended to the record. Frozen text is never silently edited; history is never rewritten.

### 4. The cheapest decisive test

The smallest, cheapest experiment that can falsify the hypothesis runs first. Free data before paid data. Before any long run: a scale probe (measure time and memory at realistic size — a self-test on toy data tells you nothing about a multi-gigabyte panel), and a self-test of the harness on synthetic fixtures with planted, known answers. A test harness that has never caught a planted bug has proven nothing about itself.

### 5. Count every trial

Every configuration evaluated — not just the interesting ones — becomes one row in an append-only, hash-chained ledger. Append-only means rows can never be edited or deleted; hash-chained means any tampering breaks a cryptographic chain and is detectable. The ledger's row count then *deflates* every reported result: the headline number is not "the best Sharpe ratio found" but "the best Sharpe ratio found, discounted for how many things were tried" (Bailey & López de Prado 2014). Because trials are often near-duplicates of each other, the effective number of independent attempts is estimated by clustering correlated trials (López de Prado & Lewis 2019) rather than naively counting rows.

The uncomfortable, load-bearing property: **the ledger makes your own search history evidence against you.** That is the point.

### 6. Honest verdict

The verdict is read against the frozen rule — nothing else. A refutation is a *success*: it is information about where the edge isn't, bought at the lowest available price. Incidentally positive cells inside the grid are reported but never selected ("this corner happened to look good" is exactly the Failure-A trap). If a related mechanism deserves a new attempt, its grid is set a priori from the literature — never from the cell that looked good.

### 7. Three-tier validation, for survivors only

1. **In-sample** — exploration, fully counted.
2. **Frozen held-out** — a locked partition, evaluated *once, ever*, under a pre-registered verdict rule. Spent is spent: a failed look burns the partition for that hypothesis family, and the next test requires genuinely new data.
3. **Forward / paper trading** — the only judge that cannot be fooled by construction.

A profitable backtest, by itself, proves almost nothing. The only evidence that accumulates is performance on data the process *provably* never saw.

## Working rules (the condensed list)

- No mechanism story, no test.
- Read the source; design from pages, not from memory.
- Pre-registration committed alone, before the run (freeze-commit).
- Hold-out cutoff frozen before any selection-bearing run (lock-before-look).
- Complete grid a priori; the grid never grows after first contact with data.
- Scale-probe and self-test before every long run.
- Every evaluated configuration is a counted ledger row; report deflated numbers only.
- Refutation is success; "almost passed" does not exist.
- Deviations are declared, labelled corrections; frozen text and history are never rewritten.
- Assert absence only as "not found by <the specific check you ran>" — never as "does not exist".
- Every artifact transferred between machines is verified by checksum before use.
- An AI agent's permission fence is policy, not trust: deny by default, verify in review.

## References

- Bailey, D. H., & López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality." *The Journal of Portfolio Management*, 40(5), 94–107.
- Carver, R. (2015). *Systematic Trading: A Unique New Method for Designing Trading and Investing Systems.* Harriman House.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). "…and the Cross-Section of Expected Returns." *The Review of Financial Studies*, 29(1), 5–68.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine*, 2(8), e124.
- López de Prado, M. (2018). *Advances in Financial Machine Learning.* Wiley.
- López de Prado, M. (2023). *Causal Factor Investing: Can Factor Investing Become Scientific?* Cambridge University Press.
- López de Prado, M., & Lewis, M. J. (2019). "Detection of False Investment Strategies Using Unsupervised Learning Methods." *Quantitative Finance*, 19(9), 1555–1565.
