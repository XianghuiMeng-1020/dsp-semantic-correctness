# PHASE 1 — Why 409/412 were “near boundary”

Phase 0 reported `near_boundary=1` on 409/412 independently VALID occupants.

## What the old margin measures

In `independent_spec_verifier.py`, `near_boundary` is a **heuristic**: linear $|H|$ within $\max(10\cdot\mathrm{slack},10^{-5})$ of an active mask wall. The stored residual-to-floor margin on FIR valids is typically exactly the FIR floor $10^{-6}$ because the **measured residual is 0** on the refined 131072-point grid. That quantity is distance to the *decision threshold*, not evidence of an unstable label.

Equiripple / window designers sit on the specification frontier by construction. The flag therefore fires on almost every FIR valid **by design**.

## Phase-1 continuous comparison (constructed FIR valids)

- constructed FIR valids certified here: 336
- of which frozen `near_boundary` true (matched by occupant id): 336
- CERTIFIED_VALID: 68
- CERTIFIED_INVALID: 0
- UNDECIDED: 268

## Does “409/412 near-boundary” mean the current valid labels are numerically fragile?

**NO** for label instability: zero constructed FIR valids were `CERTIFIED_INVALID`. The 409/412 flag is a **margin-definition / construction-frontier artifact** (residual-to-floor plus `NEAR_ABS=1e-5`).

**MIXED only as certification completeness:** many long FIRs remain `UNDECIDED` under a conservative derivative bound. That is a limitation of $M_1/M_{\mathrm{local}}$, not a demonstration that the frozen VALID labels flip under a witnessed violation.

Console classification: `MARGIN_DEFINITION_ARTIFACT`

