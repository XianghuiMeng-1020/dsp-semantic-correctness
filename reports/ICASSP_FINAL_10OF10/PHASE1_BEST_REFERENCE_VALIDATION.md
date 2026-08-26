# PHASE 1 — Best-reference validation

**Verdict:** `PASS`

## Check 1 — raw occupants

all gaps recomputed via d_coeff_canonical / cached freqz identical to distances.d_resp

Every $D_V$, $D_I$, $G$ was recomputed from frozen coefficient files. Cached $|H|$ is the same `freqz`/`sosfreqz` path and $N=131072$ as `distances.d_resp_band`.

## Check 2 — canonical $G$ reproduction

- max |Δ| coefficient: 0.0
- max |Δ| response: 0.0
- mismatches: []
- pass: True

The new implementation reproduces the frozen manuscript `G_r` values **exactly** (absolute difference 0.0 on both metrics).

## Check 3 — independent brute-force coefficient loop

Recomputed with a second loop over all observed valids as centres for `fir_lp_loose_8k`, `fir_lp_tight_8k`, `iir_lp_loose_8k`, `iir_hp_tight_8k` (one FIR loose, one FIR tight, one IIR loose, one IIR tight) using `d_coeff` only.

- `fir_lp_loose_8k`: brute `data/icassp_10of10/probe_candidates/fir_lp_loose_8k__alternating__max.npy` $G=-0.50108825$; cached match=True |ΔG|=0.0
- `fir_lp_tight_8k`: brute `data/valid/random/fir_lp_tight_8k__r017.npy` $G=-0.42495196$; cached match=True |ΔG|=0.0
- `iir_lp_loose_8k`: brute `data/valid/random/iir_lp_loose_8k__r017.npz` $G=-0.042232562$; cached match=True |ΔG|=0.0
- `iir_hp_tight_8k`: brute `data/valid/random/iir_hp_tight_8k__r007.npz` $G=-0.28093865$; cached match=True |ΔG|=0.0

Response $G$ was not re-bruteforced without the magnitude cache (that would re-run `freqz` tens of thousands of times). Check 2 already matches frozen response $G$ exactly.

## Check 4 / 5 — centres are frozen valids

{'n_checked': 88, 'invalid_or_unknown_centers': [], 'pass': 1}

No invalid occupant was used as a candidate centre.

## Check 6 — self-distance

{'samples': [{'cid': 'data/valid/library/fir_lp_loose_8k__firwin.npy', 'd': 0.0}, {'cid': 'data/valid/library/fir_lp_tight_8k__firwin.npy', 'd': 0.0}], 'pass': 1}

$D_V$ is a max, so a zero self-distance cannot inflate $D_V$. Tie-breaking on `ref_id` is independent of the self term.

