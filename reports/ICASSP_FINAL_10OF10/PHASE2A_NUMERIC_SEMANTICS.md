# PHASE 2A — Numeric semantics

## Stored FIR coefficients

Each tap is an IEEE-754 binary64 value on disk. Phase 2A treats that bit pattern as
the **exact rational** `float.as_integer_ratio()`. Taps are never rounded to a
shorter decimal before the autocorrelation / Chebyshev expansion.

## Specification constants

`registry/suite_n.json` is parsed by `json.loads`. Numbers become Python `float`
(binary64). Phase 2A treats those binary64 values as the frozen specification,
matching the existing pipeline. They are **not** re-interpreted as exact decimal
rationals (so `1e-6` is the binary64 nearest to \(10^{-6}\), not \(10^{-6}\) itself).

Floor expansion copies the old verifier:

`span = max(hi - lo, 1e-6)`, `L = lo - floor*span`, `U = hi + floor*span`.

If `L <= 0`, the lower magnitude constraint is vacuous (`|H| >= L` holds for all
real \(H\)). Phase 2A does **not** impose \(P \ge L^2\) in that case.

## Frequency endpoints

\(\omega = 2\pi f / f_s\). If \(f=0\) then \(\cos\omega=1\) exactly. If
\(2f=f_s\) exactly as binary64 rationals, then \(\cos\omega=-1\) exactly.
Otherwise \(\cos\omega\) is enclosed by an outward `mpmath` bound converted to
`Fraction`. The inner \(x\)-interval is certified first; leftover endpoint slivers
must also certify or the occupant is `UNDECIDED` (`endpoint_enclosure_limitation`).

## Equality

Frozen \(S_t\) permits equality (`|H|` on the expanded wall). Bernstein
`nonpos` / `nonneg` includes zeros. Tangential contact is valid. Unresolved
proximity is `UNDECIDED`, not a fabricated positive margin.
