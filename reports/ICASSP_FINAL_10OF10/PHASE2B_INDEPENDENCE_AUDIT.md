# PHASE 2B — Independence audit

Compared procedures:

1. construction checker (`src/spec_checker.py`);
2. original final verifier (`src/verification/independent_spec_verifier.py`);
3. Phase-1 derivative verifier (`src/continuous_certification/fir_adaptive.py`);
4. Phase-2A FIR Bernstein verifier (`src/continuous_certification/fir_power_polynomial.py`);
5. Phase-2B root/sign verifier (`src/continuous_certification/poly_sturm.py`, `mask_sign.py`);
6. Phase-2B stability verifier (`src/continuous_certification/iir_schur.py`).

| Pair | Shared correctness logic? | Shared assets |
|---|---|---|
| Construction vs Phase-2B root/sign | No | registry JSON, residual_floor contract |
| Old final vs Phase-2B root/sign | No | registry JSON, residual_floor contract |
| Phase-1 vs Phase-2B root/sign | No | registry JSON |
| Phase-2A Bernstein vs Phase-2B Sturm | No pass/fail import | same P(x) mathematics, independently reimplemented; different algorithm |
| Phase-2B Sturm vs Phase-2B Schur | No | Fraction / stored coefficients only |
| Old final vs Phase-2B Schur | No | stored `a`; old final uses `tf2zpk` |

Phase-2B does not import `spec_checker`, `search_checker`,
`independent_spec_verifier`, `fir_adaptive`, or `fir_power_polynomial`.
It does not call their residual, grid, or Bernstein functions.

High-precision `mpmath.polyroots` is a stability *cross-check* only.

## Phase-2B algorithm independence

```text
STRONG_INDEPENDENCE
```

The decision objects are a Sturm sequence / real-root sign analysis and an
exact rational Schur-Cohn recursion. Those are not wrappers around an
existing pass/fail routine.

## Overall evidence-chain independence

```text
PARTIAL_INDEPENDENCE
```

Every method still reads the same frozen `S_t` and the same `residual_floor`
contract. A corrupted registry would mislead the whole chain. That is why
the *chain* is not classified STRONG even though the Phase-2B algorithm is.
