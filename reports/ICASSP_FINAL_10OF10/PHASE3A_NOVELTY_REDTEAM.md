# PHASE 3A — Novelty red-team

Attacks assume a knowledgeable reviewer. Phase 3A does not make the sphere LP novel.

## N1. The general oracle problem was known decades ago.

- Severity before Phase 3A: HIGH
- Evidence after Phase 3A: Confirmed. Weyuker 1982; Barr et al. TSE 2015. Q1=NO.
- Residual severity: LOW as a novelty claim; HIGH if the paper were sold as introducing oracles.
- Manuscript-safe defense: Cite the oracle problem as background. Claim only the DSP reference-adequacy audit.
- Additional science needed: NO

## N2. Sphere separability by LP is textbook convex optimization.

- Severity before Phase 3A: HIGH
- Evidence after Phase 3A: Confirmed. Astorino–Gaudioso; Tax–Duin SVDD; Boyd–Vandenberghe. Q2=NO.
- Residual severity: LOW if named as a diagnostic; FATAL if named as a new theorem.
- Manuscript-safe defense: Call Γ^amb an unrestricted-center adequacy diagnostic, not a new separator.
- Additional science needed: NO

## N3. The finite-set geometry is mathematically elementary.

- Severity before Phase 3A: HIGH
- Evidence after Phase 3A: Coefficient ambient: separable=19 non-separable=1; Type A/B/C/D = 1/19/0/0; exact-rational=3.
- Residual severity: MEDIUM. Elementary does not mean the DSP measurement was already done.
- Manuscript-safe defense: Sell the hierarchy + certificates on S_t, not the expansion of ||i-c||^2.
- Additional science needed: NO unless certificates are only NUMERICAL_LP_ONLY.

## N4. The paper merely applies software-testing ideas to filters.

- Severity before Phase 3A: HIGH
- Evidence after Phase 3A: No matching DSP paper found that runs this three-level audit on independently labeled masks.
- Residual severity: MEDIUM. A reviewer can still call it 'testing applied to DSP'.
- Manuscript-safe defense: The scientific object is mask-feasible sets vs realization balls — a filter-evaluation result.
- Additional science needed: Optional later: one more specification family. Not required to finish Phase 3A.

## N5. The result depends on one magnitude-mask task family.

- Severity before Phase 3A: MEDIUM
- Evidence after Phase 3A: Still 20 magnitude-mask tasks. Phase 3A did not add families.
- Residual severity: MEDIUM (scope, not a contradiction).
- Manuscript-safe defense: State the universe explicitly. Do not claim all DSP correctness.
- Additional science needed: A second family would help a journal version; not Phase 3A.

## N6. The unrestricted center is not itself a realizable DSP implementation.

- Severity before Phase 3A: MEDIUM
- Evidence after Phase 3A: Asymmetry is explicit: no ambient center ⇒ no realizable reference rescues a single-center Euclidean oracle; an ambient center ≠ a realizable filter.
- Residual severity: LOW if Type A; HIGH if Type B is sold as 'a better filter exists'.
- Manuscript-safe defense: Keep the asymmetry in any future sentence. Never infer realizability from a center.
- Additional science needed: NO

## K* decision (not run)

`KSTAR_NEXT = HIGH_VALUE`

Type B is the dominant coefficient outcome: an unrestricted Euclidean center (often a halfspace / center at infinity) recovers the frozen labels, but no observed valid realization does. The remaining reference-oracle question is exactly catalog complexity K* over observed valids. Phase 3A does not run K*.

## Claim gates

- Q1 generic oracle novel? NO
- Q2 generic sphere LP novel? NO
- Q3 manuscript-specific: The manuscript-specific object is a certified three-level adequacy audit of realization-reference scoring against specification-defined FIR/IIR mask membership on a frozen independently labeled finite universe — not the oracle problem and not sphere LP.
- Q4 testing reviewer 'already known'? NO — a testing reviewer can correctly say the oracle problem and sphere LP are known, but cannot correctly say that this frozen DSP universe was already shown to be non-spherically-separable under the paper's confirmatory embedding with certificates.
- Q5 SP reviewer sees a DSP contribution? PARTIAL — ambient rescue would re-open 'a better geometric center exists' and weaken the claim that specification predicates are needed to represent validity.
