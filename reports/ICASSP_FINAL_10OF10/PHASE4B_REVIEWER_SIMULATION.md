# PHASE 4B — Reviewer simulation (final PDF only)

Read from `manuscript/final/paper.pdf` after the writing pass. No new science.

## Reviewer 1 — Signal Processing Theory & Methods

**Summary.** Audits whether coefficient or magnitude-response reference catalogs recover a magnitude-mask specification, then tests transfer to 614 catalog-blind certified FIR/IIR designs.

**Strengths.** DSP-native (masks, Remez/window/Butterworth/elliptic, Schur, Bernstein/Sturm). Representation contrast is mechanistically explained. Ambient-center sentence blocks a geometric overclaim.

**Weaknesses.** 20 tasks; eight designer families; response is not exact.

**Score.** 4/5. **Accept.**

## Reviewer 2 — Applied DSP

**Summary.** Golden coefficient vectors and even exact finite coefficient catalogs fail as correctness oracles for later valid designs (66/614); response catalogs usually transfer (585/614).

**Strengths.** Freeze-then-generate protocol; continuous certification 412/412; figure makes the contrast obvious; public reproduction command.

**Weaknesses.** Invalid holdout is incomplete and omitted from the core table (correctly). Catalog maintenance is a diagnostic, not a product procedure.

**Score.** 4/5. **Accept.**

## Reviewer 3 — Skeptical cross-domain

**Summary.** Oracle problem and set cover are known; the paper disclaims both and reports a FIR/IIR transfer measurement.

**Strengths.** Explicit novelty boundary. Finite-universe language. No impossibility claim.

**Weaknesses.** A reader who stops at “coefficients differ” will underrate the paper; the intro now says that fact is classical. Finite suite remains.

**Score.** 3.5/5. **Weak accept / accept.**

## Meta-review

**Decision: ACCEPT.**

Is there a credible rejection argument based on a *correct* reading rather than an acknowledged limitation? **NO.**

A reject that says “coefficients of Remez and window filters differ” misreads the intro. A reject that says “oracle problem is old” misreads the disclaimer. Remaining limits (20 masks, eight families, incomplete invalids) are stated and are inherent, not packaging defects.
