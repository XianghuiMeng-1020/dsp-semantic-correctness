# 03 — Canonicalization audit

Rules are listed in `src/verification/canonicalize.py`. Confirmatory distances use those rules. Historical min-length truncation is retained only as `d_coeff_historical`.

## Observed artifacts on constructed occupants

| Artifact | Count |
|---|---:|
| Occupants inspected | 560 |
| FIR trailing-zero trims | 0 |
| IIR \(a_0\neq 1\) rescales | 0 |
| Pure sign-flip vs canonical | 0 |

Scale is **not** removed: Suite N masks constrain absolute \(\lvert H\rvert\).

Unequal-order truncation is **not** used as a confirmatory metric.

Every confirmatory “distinct realization” excludes zero-padding artifacts, pure sign flips (magnitude-only), and pure global rescaling.
