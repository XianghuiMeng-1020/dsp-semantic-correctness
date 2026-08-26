# PHASE 0 — Novelty boundary

## Not sufficient novelty (and the paper mostly does not sell these as the contribution)

- References differ from other valid filters
- Golden outputs can be incomplete
- Software testing has an oracle problem (Weyuker; Chen/Liu are cited only for unique-output unit tests)
- Multiple numerical implementations may exist
- LLM code may differ from a canonical call

Included test-oracle / testing cites: Huuhtanen 2015 (golden DSP tests),
Chen 2021, Liu 2023 (EvalPlus). Missing (not added): Weyuker oracle
problem, Barr et al. metamorphic testing, IEEE 829/29119, filter-design
feasibility literature beyond the classical DSP books already cited.

## What the manuscript actually claims as new

Best characterization (ranked):

1. **Finite-universe exactness criterion** for a scalar
   reference-distance oracle vs \(S_t\) (\(G_r\), Prop. 1).
2. **Empirical geometry** on 20 independently labeled magnitude-mask
   tasks: coeff. non-separable 20/20; response 19/20; inversions 20/20.
3. **Protocol split**: construction checker ≠ final verifier, with
   four documented flips.
4. **Same-order / same-structure** alternatives still reference-discordant
   (16/16 Type-I probe + 4/4 IIR library).
5. **Finite multi-reference catalogs** \(K\in\{1,3,5,\mathrm{all}\}\)
   still 0/20 exact.
6. **Positive control**: Suite S \(G_r>0\) on 8/8.

(1) is mathematically thin if sold as a theorem (it is threshold
separability). It becomes ICASSP-relevant only when tied to (2)–(6)
on DSP masks. (3) is necessary hygiene, not a standalone theory result.

### Strongest defensible novelty statement

On specification-defined FIR/IIR magnitude masks, a scalar (or finite
catalog) reference-distance test is exactly the wrong object for
correctness once labels are assigned by an independent specification
predicate: the valid set and the invalid set interleave in coefficient
space on every evaluated task, including same-order Type-I alternatives,
and the same geometry is absent on singleton identities. The paper’s
contribution is that **evaluation geometry**, not a new designer and
not an LLM benchmark.

### Strongest reviewer novelty attack

“Proposition 1 is the definition of a separating threshold. That
valid Parks–McClellan and Hamming designs differ is textbook. You
measured that a Hamming ball does not recover a mask. Where is the
signal-processing result that is not software-testing folklore plus
a filter-design truism?”

### What would neutralize that attack

1. Show that **no occupant of \(\mathcal{V}_t\cap\mathcal{U}_t\)**
   (not merely no library designer) restores \(G_r>0\) — i.e. compute
   or bound \(G^*\). That kills “you chose a bad golden `firwin`.”
2. A **continuous-frequency** (or adaptive-certified) label, so the
   geometry is not an artifact of a 4096/131072 grid.
3. One **additional specification family** (linear-phase + max-order,
   or group-delay) where the same \(G_r\) diagnostic is applied.
4. Explicit contrast to metamorphic / oracle-problem papers: the
   *DSP-specific* object is the mask-feasible set vs a realization ball.
5. Keep Suite S as the control that shows the criterion is not
   “reference matching always fails.”

## \(G^*=\sup_r[\min_{h\notin V}d(h,r)-\max_{h\in V}d(h,r)]\)

On finite \(\mathcal{U}_t\), if \(r\) is restricted to
\(\mathcal{V}_t\cap\mathcal{U}_t\), this is **exactly computable**
by enumerating candidate references (the 412 valids, per task
typically ~20). It is the “best possible single evaluated reference.”
Mathematically correct; nontrivial as a **robustness diagnostic**,
not as a new theorem. Relevant to Attack B. Risk of a second paper:
low if reported as one table row (20 tasks, \(\mathrm{sign}(G^*)\)).
**ICASSP novelty value: HIGH** as a Phase 1 test, not as new theory.

Note the written formula used \(\min_{U\setminus V}\) which is \(D_I(r)\);
the displayed fraction bar in the PI prompt is \(D_I/D_V\) if parsed
as a ratio. The **gap** form \(D_I-D_V\) (already in the paper) is
the right object; a ratio is optional and can be infinite if \(D_V=0\).
Phase 1 should optimize **\(G_r\)**, not invent a second primary metric.

## \(K_t^*=\min |R|\) s.t. some \(\tau\) makes \(\bigcup_r A_{\tau,r}\) recover \(V\cap U\)

Finite-universe **exact cover** of valids without covering a nearer
invalid. Computable by set-cover style search on small per-task \(n\).
If \(K_t^*\) is huge (near \(n_{\mathrm{valid}}\)), the finding is
“you need \(S_t\).” If small, Attack B gains force. Relevant; can
become a catalog-complexity paper if over-emphasized.

**ICASSP novelty value: MEDIUM** — run as a bound or greedy upper
bound, not as the new title claim.

## Novelty boundary verdict

```text
PARTIAL
```

Clear as an empirical DSP-evaluation result; weak if Prop. 1 is
sold as theory-first novelty.
