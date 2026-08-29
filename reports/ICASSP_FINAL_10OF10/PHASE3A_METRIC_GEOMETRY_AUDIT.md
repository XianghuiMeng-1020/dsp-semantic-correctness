# PHASE 3A — Metric geometry audit

Inspected implementations: `src/verification/distances.py`, `src/verification/canonicalize.py`, `experiments/icassp_10of10_hardening/phase1/best_observed.py`. No metric was rewritten.

| metric | exact formula | embedding | Euclidean-ball equivalent? | unrestricted-center LP valid? |
| ------ | ------------- | --------- | -------------------------- | ----------------------------- |
| confirmatory coefficient (`d_coeff_canonical` / `d_coeff_mag_equiv`) | FIR: after canonicalize and zero-pad, \(\min(\|v-v_r\|_2,\|-v-v_r\|_2)/\|v_r\|_2\) (EPS \(10^{-18}\)). IIR: \(a_0=1\), pad \(b\) and \(a\), \(d=\|[b,a]-[b_r,a_r]\|_2/\|[b_r,a_r]\|_2\). | Canonical zero-padded coefficient vector. FIR oriented so the first nonzero tap is \(\ge 0\). IIR is \([b,a]\). | YES for the single-center threshold oracle: \(\{x:\|x-c\|_2/\|c\|_2\le\tau\}\) is a Euclidean ball (\(c\neq 0\)). | YES in that fixed embedding. Relative scale folds into \(\tau\). |
| historical coefficient (`d_coeff_historical`) | min-length relative \(\ell_2\) | pair-dependent truncation | NO (embedding depends on the pair) | NO (not confirmatory; arm not run) |
| confirmatory response (`d_resp_band`) | RMSE of \(\lvert H\rvert\) on the pass+stop mask, `FREQZ_N=131072` | band-masked magnitude vector in \(\mathbb R^m\) | YES: RMSE \(=\frac1{\sqrt m}\|x-y\|_2\) | YES; secondary because \(\lvert H\rvert\) is numerical |

## Coefficient verdict

The confirmatory coefficient distance is **reference-normalized relative L2**, not a \(c\)-independent Euclidean metric on a product space. That does **not** stop the ambient arm. The manuscript single-center oracle is a threshold on this distance. Those sublevel sets are Euclidean balls in the canonical padded embedding. Unrestricted-center exact recovery is therefore ordinary Euclidean sphere separation. The Phase-3A LP is the affine form of that question.

FIR magnitude-equivalence: Phase-1 takes \(\min(\|v-c\|,\|-v-c\|)\) against the reference. Phase-3A orients each occupant once (first nonzero \(\ge 0\)) and runs the LP in that **fixed** Euclidean section. This is not a new favorable metric. It is the magnitude-equivalence class already used for confirmatory coefficient scoring.

Historical min-length truncation is **not** Euclidean-equivalent in a fixed embedding and is not used.

## Response verdict

Band-masked RMSE is Euclidean up to the constant \(1/\sqrt{m}\) on the confirmatory masked-magnitude embedding. The ambient LP is valid. An arbitrary center in this space need not be a realizable filter response. Response results are secondary: they cannot receive `EXACT_RATIONAL_CERTIFICATE` for the freqz vectors themselves. Affine-span reduction of the frozen occupants is used only as a lossless isometry (no PCA truncation).

## Arms

- Coefficient ambient-center: **RUN**
- Response ambient-center: **RUN** (secondary / high-precision)
