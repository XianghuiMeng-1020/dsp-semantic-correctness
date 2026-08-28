# PHASE 3A — Ambient validation

Verdict: `PASS`

## Synthetic

- A (separated clusters): AMBIENT_SEPARABLE pass=1
- B (nested square): NO_AMBIENT_CENTER pass=1
- C (canonical fails, ambient succeeds): AMBIENT_SEPARABLE pass=1

## Check D

If a frozen canonical Euclidean gap is already positive, the ambient solver must not report `NO_AMBIENT_CENTER`.

- coefficient check D: `1`
- response check D: `1`

## Check E — second optimizer / independent dual

- `fir_lp_loose_8k`: kind_agree=1 gamma_close=1 strong_duality=None pass=1
- `iir_hp_tight_8k`: kind_agree=1 gamma_close=1 strong_duality=1 pass=1

## Engine

The optimizer is `scipy.optimize.linprog` on the ambient primal/dual. It does not call Phase-1 `gap_for_reference`.
