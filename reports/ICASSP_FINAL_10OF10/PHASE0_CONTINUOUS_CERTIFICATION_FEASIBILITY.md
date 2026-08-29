# PHASE 0 — Continuous-frequency certification feasibility

No certification was implemented.

## Current status

| Family | Support for a published label |
|---|---|
| FIR | (2) dense grid \(N_f=131072\) **plus** local extremum refinement around the **grid-global** min and max per band |
| IIR | (2) same, plus SOS evaluation and pole-radius check; not interval arithmetic |

Not used: analytic Parks–McClellan extrema, Lipschitz remainder, interval/adaptive subdivision, symbolic identities (except Suite S exact maps).

The manuscript already states this is not a continuous-frequency proof.

## FIR

Proposed bound \(\lvert dH/d\omega\rvert \le \sum_n n\lvert h_n\rvert\) is
**mathematically valid** for \(H(e^{j\omega})=\sum h_n e^{-jn\omega}\)
(and likewise for \(\lvert H\rvert\) almost everywhere except at zeros,
where \(\lvert H\rvert'\) can be unbounded in the derivative of the
modulus — use \(\lvert \lvert H\rvert(a)-\lvert H\rvert(b)\rvert\le
\sup\lvert H'\rvert\cdot\lvert a-b\rvert\) via \(\lvert H'\rvert\le\lvert H'\rvert_{\mathbb{C}}\)
i.e. the same \(\sum n\lvert h_n\rvert\) on the complex derivative).

**Too loose in practice** for the long library FIRs (hundreds of taps).
If \(\sum n\lvert h_n\rvert \approx 10^2\)–\(10^3\) and grid \(\Delta\omega
\sim 2\pi/131072\), the remainder can exceed the FIR floor
(\(\lvert H\rvert\) slack corresponding to residual \(10^{-6}\times\)
band span \(\sim 10^{-8}\)). A single-interval remainder will **not**
certify most long FIRs.

**Adaptive subdivision** (bisect until remainder \(<\) unused slack)
is the feasible design:

* Upper-bound (stop): certify \(\sup_I \lvert H\rvert \le hi\) by
  midpoint +\(\lvert H'\rvert\) remainder, or interval eval of the
  trigonometric polynomial.
* Lower-bound (pass): certify \(\inf_I \lvert H\rvert \ge lo\).
  Harder at near-zeros; for passbands near 1 this is routine.
* Equality/edge: treat \(S_t\) as closed (\(\le hi\), \(\ge lo\))
  consistent with the current residual \(\le\) floor.

Type-I cosine polynomial form already in the paper is the right
object for a Chebyshev-proxy or Clenshaw evaluation.

**Could alter labels?** Yes, for occupants with unused slack
smaller than the uncertified remainder. The verifier’s own
`near_boundary` flag is true for **409/412** independently valid
occupants (`NEAR_ABS=1e-5`). Those are the risk set.
The four already-flipped `firwin2` show band-edge misses are not
hypothetical.

**Complexity:** medium (adaptive FIR evaluator + remainder). Days, not weeks,
if scoped to the 412+144+160 corpus and allowed to return
`CERTIFIED` / `UNDECIDED` / `REFUTED`.

**Headline dependence on uncertified boundary cases:** **yes**.
Same-order probes and library occupants include long Type-I FIRs.
If a currently VALID occupant is REFUTED, 412 and possibly some
20/20 counts move. If only UNDECIDED, headlines can stay with a
sharper caveat.

## IIR

Rational \(\lvert B(z)/A(z)\rvert\) on the unit circle. Poles inside
0.999 are already checked (not a continuous-mask proof).

Defensible route: high-precision SOS eval + adaptive subdivision
with a derivative bound from \(\lvert H'/H\rvert\) or interval
arithmetic on the bilinear frequency variable. Remainder constants
are messier than FIR; tightness of the mask (and the 4 IIR tasks)
makes **UNDECIDED** likely for some tight IIR occupants.

The one **positive response gap** (\(\sim 3.8\times 10^{-6}\) on
`iir_hp_tight_8k`) is already a numerical near-tie. Continuous
re-labeling of that task’s occupants could flip 19/20 → 20/20 or
the reverse.

**Complexity:** high. **Could alter labels:** yes, especially tight IIR.

## FIR / IIR summary

| | FIR | IIR |
|---|---|---|
| Current status | FEASIBLE_NOT_IMPLEMENTED | FEASIBLE_NOT_IMPLEMENTED |
| Mathematical risk | missed inter-sample peaks on long taps | rational peaks; pole/zero sensitivity |
| Feasible design | adaptive FIR + \(\sum n\lvert h_n\rvert\) remainder | adaptive SOS + interval/deriv bound |
| Implementation complexity | medium | high |
| Could alter existing labels | yes (near-edge FIR) | yes (tight IIR) |
| Headlines depend on uncertified cases | yes | yes |

Neither family is `CURRENTLY_CERTIFIED`. Neither is a
`MATERIAL_PROBLEM` in the sense of a known wrong theorem; the
problem is **unclosed numerical risk**, already disclosed.
