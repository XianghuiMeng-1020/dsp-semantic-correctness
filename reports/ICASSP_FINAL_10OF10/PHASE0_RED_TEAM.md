# PHASE 0 — Reviewer red team

Five attacks. Severity 1–10 is **current manuscript + current public
GitHub default**, not a hoped-for Phase 1.

### Attack A — “The theorem is obvious.”

Severity: **7**

Defense: Prop. 1 is labeled evaluation geometry; Suite S shows the
criterion is not vacuous; the result is the empirical \(G_r\le 0\)
pattern plus same-order probes.

Sufficient? **No** if novelty is sold as theory. **Partly** if sold
as DSP-evaluation measurement.

Smallest neutralization: one table of \(G^*\) (best evaluated
reference) plus a sentence that the contribution is the measured
geometry, not the iff.

Acceptance value: medium-high (novelty desk-reject risk).

### Attack B — “You chose a bad reference.”

Severity: **8**

Defense: every library designer and \(K\in\{1,3,5,\mathrm{all}\}\)
still 0/20. Discussion says a small catalog is still a catalog of
realizations.

Sufficient? **No.** The catalog is not \(\mathcal{V}_t\cap\mathcal{U}_t\).
A reviewer can demand the best occupant as \(h_r\).

Smallest neutralization: compute \(\mathrm{sign}(G_r)\) for every
independently valid library **and** every valid occupant as \(r\)
(\(G^*\)). No new generation.

Acceptance value: **highest** of the five.

### Attack C — “You chose a bad metric.”

Severity: **6**

Defense: response RMSE is already the stronger oracle and still
fails 19/20; the leftover gap is a \(10^{-6}\) near-tie. Canonical
\(\ell_2\) after Type-I rules, not raw tap padding.

Sufficient? **Partly.** No group-delay, no Sobolev, no weighted
Chebyshev residual as \(d\).

Smallest neutralization: pre-register **one** extra \(d\) (e.g.
max-band \(\lvert H-H_r\rvert\)) on the frozen corpus. Do not search
until a metric “works.”

Acceptance value: medium.

### Attack D — “The verifier is numerical and circular.”

Severity: **8**

Defense: no import of `spec_checker`; 131072 + refine; four flips;
explicit “not a continuous proof.”

Sufficient? **No** for a strict reviewer. Shared residual formula,
shared floors, 409/412 `near_boundary`, public `main` still showing
Oracle C = \(S_t\).

Smallest neutralization: (i) point GitHub default at the current
branch/paper; (ii) adaptive FIR remainder with UNDECIDED allowed.

Acceptance value: high (credibility).

### Attack E — “Only one DSP task family.”

Severity: **7**

Defense: Discussion lists beams/filter banks/phase as out of scope;
Suite S is the other family.

Sufficient? **For a specialized ICASSP paper, maybe.** For the
current title, no.

Smallest neutralization: retitle/abstract to magnitude-mask
evaluation **or** add one constrained-phase \(S_t\) on existing FIRs.

Acceptance value: medium (scope/fit, not a method bug).

## Expected value ranking (Phase 1)

1. \(G^*\) / best-reference (Attack B)
2. Public `main` sync (Attack D, non-scientific but blocker)
3. Continuous/adaptive cert or honest UNDECIDED (Attack D)
4. Title/abstract scope lock (Attack E)
5. One extra pre-registered \(d\) (Attack C)
