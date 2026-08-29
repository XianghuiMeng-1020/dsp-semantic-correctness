# PHASE 2A — Constraint transformation

Frozen Suite N FIR tasks are magnitude-mask specifications.
`phase_requirement` is `none` and `order_constraint` is `free` on every FIR
task, so Phase 2A adds no extra polynomial conditions beyond the registered
pass and stop bands.

## Frozen \(S_t\) (exact existing semantics)

Each registered band is a closed frequency interval \([f_0,f_1]\) with a
closed magnitude interval \([\mathrm{lo},\mathrm{hi}]\). The old verifier
and the construction checker both use inclusive endpoints
(`w >= f0` and `w <= f1`). Phase 2A uses the same closed interval.

Floor expansion is copied from the frozen residual contract:

\[
\mathrm{span}=\max(\mathrm{hi}-\mathrm{lo},10^{-6}),\quad
L=\mathrm{lo}-\mathrm{floor}\cdot\mathrm{span},\quad
U=\mathrm{hi}+\mathrm{floor}\cdot\mathrm{span}.
\]

The constants `1e-6` and `residual_floor` are the JSON/binary64 values, not
re-parsed decimal rationals. Equality on the expanded wall remains valid
(`residual <= floor`).

Transition bands (frequencies listed in neither pass nor stop) are
unconstrained and are not certified.

## Polynomial-sign form

Let \(P(x)=|H(e^{j\omega})|^2\) with \(x=\cos\omega\).

| Frozen condition | After floor | Polynomial-sign condition | Vacuous case |
|---|---|---|---|
| \(|H|\le \mathrm{hi}\) | \(|H|\le U\) | \(Q_U(x)=P(x)-U^2\le 0\) on the \(x\)-image of the band | never (\(U>0\) on all Suite N FIR bands) |
| \(|H|\ge \mathrm{lo}\) | \(|H|\ge L\) | \(Q_L(x)=P(x)-L^2\ge 0\) | if \(L\le 0\), omit \(Q_L\) (true for every real \(H\)) |

Stop bands have `lo=0`, so after a non-negative floor expansion \(L\le 0\)
and the lower constraint is vacuous. Pass bands have `lo` near 1, so both
\(Q_U\le 0\) and \(Q_L\ge 0\) are enforced.

The map \(x=\cos\omega\) is monotonic on \(\omega\in[0,\pi]\). The
continuous band in \(\omega\) becomes a continuous interval in \(x\),
enclosed conservatively when \(\cos(2\pi f/f_s)\) is not a dyadic rational.

Tangential roots of \(Q_U=0\) or \(Q_L=0\) with no sign change into the
forbidden half-line remain valid. A true crossing is `CERTIFIED_INVALID`.
Unresolved mixed Bernstein coefficients are `UNDECIDED`.
