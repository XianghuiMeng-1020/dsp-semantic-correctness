# PHASE 2A — Independence audit

| Pair | Shared correctness logic? | Shared assets |
|---|---|---|
| Construction vs old final verifier | No pass/fail import | registry JSON, residual_floor contract, numpy/scipy |
| Construction vs Phase-1 derivative | No | registry JSON, residual_floor, numpy |
| Construction vs Phase-2A polynomial | No | registry JSON, residual_floor, numpy |
| Old final vs Phase-1 | No | registry, residual formula, scipy freqz family |
| Old final vs Phase-2A | No | registry, residual_floor *contract* only |
| Phase-1 vs Phase-2A | No | registry, residual_floor contract, numpy (not the same H routine) |

Phase-2A (`fir_power_polynomial.py`) does not import `spec_checker`,
`search_checker`, `independent_spec_verifier`, or `fir_adaptive`.
It does not call their residual or grid functions.
It builds \(P(x)=|H|^2\) from exact binary64 autocorrelations and certifies
polynomial sign by Bernstein subdivision.

Witness grid length is 1021 (prime), not 4096 / 131072 / 10007.

## Classification of the Phase-2A certifier

```text
PARTIAL_INDEPENDENCE
```

**Why not STRONG:** the target is still the registered \(S_t\) (bands + `residual_floor`).
A corrupted registry would mislead every procedure.

**Why not WEAK:** decision procedure is a different mathematical object
(polynomial sign on \(x=\cos\omega\)), different arithmetic (exact rationals),
and a different implementation file with no shared pass/fail function.
