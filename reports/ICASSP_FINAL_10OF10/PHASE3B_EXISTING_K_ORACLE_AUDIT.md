# PHASE 3B — Existing multi-reference oracle audit

Inspected: `manuscript/w4/paper.tex` eqs. (dK), (A), (Gr); `experiments/icassp_10of10/pipeline.py` (`multi-reference` stage, `library_refs_for_task`, `threshold_sweep`, `separability`); `experiments/icassp_10of10/config.py` (`K_GRID=(1,3,5)`); `src/verification/distances.py`; frozen `data/icassp_10of10/multi_reference.json`.

### Q1

Yes. Manuscript and code both use

\[
d_K(h)=\min_{r\in\mathcal{R}_K}d(h,h_r).
\]

Code: `dmin(impl) = min(distance_bundle(impl, ref, task)[key] for ref in use)`.

### Q2

Yes. One common scalar \(\tau\) is applied to \(d_K\). Exact recovery is the same gap as \(K=1\): \(D_V\le\tau<D_I\) iff \(G=D_I-D_V>0\).

### Q3

No. Thresholds are not per-reference radii.

### Q4

Yes for the published \(K\) table: centers are independently verified **library** realizations (`source=="library"`). They are specification-valid implementations. Phase 3B keeps that eligibility class (valid realizations) and enlarges the *candidate pool* to every observed valid in \(V_t\cap U_t\), without changing the oracle family.

### Q5

Confirmatory coefficient distance is `d_coeff_mag_equiv` via `distance_bundle` / `d_coeff_canonical`:

- FIR: canonicalize (trim unpaired trailing zeros; keep leading zeros/scale); zero-pad; \(d=\min(\|v-v_r\|_2,\|-v-v_r\|_2)/\|v_r\|_2\).
- IIR: \(a_0=1\), trim, pad \(b\) and \(a\), concatenate, relative \(\ell_2\).

The score \(d(x,r)\) is **reference-normalized** and therefore not assumed symmetric. Set cover uses \(d(x,r)\) with \(r\) as the selected reference.

### Q6

Response: band-masked RMSE of \(|H|\) on pass+stop bands, `FREQZ_N=131072` (`d_resp_band`).

### Q7

The published multi-reference stage scores constructed+probe valids against mechanism+boundary invalids — the same confirmatory \(\mathcal{U}_t\) as Phase 1.

### Q8

Deterministic **library prefixes** in `LIBRARY_ORDER_FIR` / `LIBRARY_ORDER_IIR` (`firwin`, `remez`, `firls`, … / `butter`, `cheby1`, …). Not the best combination of size \(K\).

## Verdict

The existing family **is** min-distance with a common scalar threshold. Phase-3B \(K^\star_{\mathrm{obs}}\) reproduces that family. No PI stop on oracle definition.

`PHASE3B_ORACLE_DEFINITION_REQUIRES_PI_REVIEW` is **not** raised.
