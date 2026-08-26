# PHASE 1 — FIR continuous-band certification

New implementation: `src/continuous_certification/fir_adaptive.py`.
It does **not** import `spec_checker`, `search_checker`, or `independent_spec_verifier`.

Arithmetic class: `CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL`

## Bound

$H(\omega)=\sum_n h_n e^{-jn\omega}$, $M_1=\sum n|h_n|$, optional $M_{\mathrm{local}}=|H'(c)|+M_2\delta$ with $M_2=\sum n^2|h_n|$. Certificate: $|H(c)|+M\delta < U_{\mathrm{eff}}$ and $|H(c)|-M\delta > L_{\mathrm{eff}}$.

Band-edge semantics and `residual_floor` follow the frozen task JSON ($L_{\mathrm{eff}}=L-\mathrm{floor}\cdot\mathrm{span}$, $U_{\mathrm{eff}}=U+\mathrm{floor}\cdot\mathrm{span}$), i.e. the paper $S_t$, not a stricter raw mask.

Evaluation uses float64 DFT sums plus a documented rounding envelope. This is **not** formal interval arithmetic. `UNDECIDED` is never coerced to valid and never resolved by the old label.

## Existing-valid FIR (constructed + Type-I probe)

- total: 1596
- CERTIFIED_VALID: 78
- CERTIFIED_INVALID: 0
- UNDECIDED: 1518

Constructed only: {'total': 336, 'CERTIFIED_VALID': 68, 'CERTIFIED_INVALID': 0, 'UNDECIDED': 268}

Probe only: {'total': 1260, 'CERTIFIED_VALID': 10, 'CERTIFIED_INVALID': 0, 'UNDECIDED': 1250}

## Mechanism-invalid FIR

- total: 112
- CERTIFIED_INVALID: 112
- CERTIFIED_VALID: 0
- UNDECIDED: 0

## Boundary-invalid FIR

- total: 128
- CERTIFIED_INVALID: 128
- CERTIFIED_VALID: 0
- UNDECIDED: 0

## FIR singleton controls

{'total': 0, 'note': 'Suite S identities are not magnitude-mask FIR occupants; not applicable'}

## Contradictions

Count: 0

Blocker (old VALID → CERTIFIED_INVALID): False

No contradictory certifications.

A compact occupant table is stored in `results/icassp_10of10_hardening/phase1/fir_continuous_certification.json` (full `rows` array). Rendering thousands of rows here would hide the counts.

## Interpretation

Mechanism invalids were witnessed on an independent prime-length grid or at adaptive midpoints. Many long constructed / probe FIRs remain `UNDECIDED` because the analytic $M$ bound is conservative, not because the old label was used. That incompleteness is reported, not repaired.

