# PHASE 1 — Verifier independence reaudit

## Dependency table

| Asset | Candidate construction | Old final verifier | New continuous FIR certifier |
|---|---|---|---|
| Code path | `src/spec_checker.py` via `search_checker.py` | `src/verification/independent_spec_verifier.py` | `src/continuous_certification/fir_adaptive.py` |
| Imports the others? | no | no | **no** |
| Frequency grid | SciPy `freqz` $N=4096$ | SciPy `freqz`/`sosfreqz` $N=131072$ + extrema refine | own DFT sum; witness grid length **10007** (prime); adaptive midpoints |
| Residual / floor | residual vs `residual_floor` | same residual formula vs `residual_floor` | floor-expanded $L,U$ from the same registered floor (the $S_t$ contract) |
| Pass/fail function | `check_specification` | `verify_specification` | `certify_fir` (derivative-bound adaptive) |
| Response routine | SciPy `freqz` | SciPy `freqz` / `sosfreqz` / scalar DFT at refined $\omega$ | numpy complex exponential sum; **not** SciPy `freqz` |
| Tolerance constants | registry floors | registry floors + `NEAR_ABS` | registry floors + float64 rounding envelope |
| Numerical libraries | numpy, scipy | numpy, scipy | numpy only |
| Spec parsing | `src` registry helpers | `registry_io.get_task` | local JSON read of `registry/suite_*.json` |
| Raw coefficients | occupant files | occupant files | occupant files (acceptable share) |

Sharing raw coefficients and specification JSON is required and permitted.
Sharing pass/fail logic is not: the new certifier does not call either existing verdict.

## Classification of the NEW FIR verifier

```text
PARTIAL_INDEPENDENCE
```

**Why not STRONG:** the certificate target is the same registered $S_t$ (band edges + `residual_floor`).
A corrupted registry would still mislead all three procedures.

**Why not WEAK / NOT_INDEPENDENT:** no import of construction or old-final pass/fail;
no reuse of 4096 or 131072 grids; no reuse of residual-check helpers; different decision
procedure (analytic $M$ + adaptive bisection + independent witness grid).

Phase-0 classification of construction vs old final verifier remains `PARTIAL_INDEPENDENCE`.
