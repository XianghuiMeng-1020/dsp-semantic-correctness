# PHASE 1 — IIR continuous-certification design (not executed)

Phase 1 ran FIR only. This is a design plan for a possible Phase-2 IIR certifier.

## Target

For $H(z)=B(z)/A(z)$, certify $|H(e^{j\omega})|$ on each frozen constrained band
against the same $S_t$ (floor-expanded $L,U$), plus pole/stability as in the paper
(pole radius $< 0.999$).

## Proposed route

1. **Poles / stability.** High-precision roots of $A$, or a Schur/Jury enclosure.
   A pole with $|p|\ge 0.999$ is `CERTIFIED_INVALID` with an explicit witness.
2. **Rational evaluation.** Evaluate $B(e^{j\omega})/A(e^{j\omega})$ in high precision
   (`mpmath`) or interval arithmetic. Do not inherit SOS/`sosfreqz` from the old verifier.
3. **Lower bound on $|A(e^{j\omega})|$.** Needed to bound $|H|$ and $|H'|$.
   If an interval cannot prove $|A|\ge a_{\min}>0$, subdivide or return `UNDECIDED`.
   Near-unit-circle poles make this the main incompleteness source.
4. **Derivative bound.** $H'= (B'A-BA')/A^2$. Bound $|H'|$ from enclosures of
   $B,A,B',A'$ and $a_{\min}$. Then reuse the FIR adaptive test
   $|H(c)|+M\delta < U$, $|H(c)|-M\delta > L$.
5. **Adaptive subdivision.** Same three-way status: `CERTIFIED_VALID` /
   `CERTIFIED_INVALID` / `UNDECIDED`. Never coerce `UNDECIDED`.
6. **Violation witnesses.** A midpoint (or independent grid point) with
   $|H|$ outside $[L,U]$ after a rounding/enclosure guard is `CERTIFIED_INVALID`.

## Feasibility after the FIR experiment

FIR already showed that a conservative $M$ leaves many long filters `UNDECIDED`
even when the old grid label is VALID and no contradiction appears.
IIR will be **strictly harder**: $|A|$ can be small, $M$ can explode, and
float64 `freqz` is not a certificate.

Phase 2 can implement a **defensible** IIR verifier if it:

* keeps the three-way status;
* treats pole-near-unit-circle cases as `UNDECIDED` rather than guessed valid;
* classifies arithmetic honestly (`HIGH_PRECISION_NOT_FORMAL_INTERVAL` unless
  a real interval library is used);
* lives in `src/continuous_certification/` and does not import the old verdict.

## Phase-2 recommendation

```text
FEASIBLE_WITH_LIMITATIONS
```

Not a material blocker for *attempting* IIR certification. Expect many `UNDECIDED`
IIR valids and reliable `CERTIFIED_INVALID` only when a witness is far from $S_t$.
Do not run that experiment until the PI opens Phase 2.
