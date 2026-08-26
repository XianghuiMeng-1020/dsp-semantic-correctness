# 02 — Independent verification

Verifier: `independent_spec_verifier/1.0`  
Grid: \(N_f=131072\) plus local extremum refinement.  
Construction labels come from `search_checker` (4096-point). Final labels come only from the independent verifier.

## Counts

| Quantity | Value |
|---|---:|
| Total constructed candidates | 560 |
| Previous VALID | 416 |
| Previous INVALID | 144 |
| Independent VALID (from previous-valid set) | 412 |
| Independent INVALID (from previous-invalid set) | 144 |
| Label flips | 4 |
| Near-boundary flags | 557 |
| Numerical failures | 0 |
| Independent FIR valids | 336 |
| Independent IIR valids | 76 |

Headline 374/416 at \(\tau_R=0.05\) (historical \(d\)) survives unchanged: **0**

Descriptive historical FRR on independently verified valids: {'n': 370, 'den': 412, 'rate': 0.8980582524271845}

## Label flips

- `data/valid/library/fir_lp_tight_8k__firwin2.npy` VALID → INVALID: passband_dense:7.765e-03@f=799.987770595171
- `data/valid/library/fir_lp_tight_16k__firwin2.npy` VALID → INVALID: passband_dense:7.765e-03@f=1599.975541190342
- `data/valid/library/fir_hp_tight_8k__firwin2.npy` VALID → INVALID: stopband_dense:1.594e-02@f=1399.9938602831642
- `data/valid/library/fir_hp_tight_16k__firwin2.npy` VALID → INVALID: stopband_dense:1.594e-02@f=2799.9877205663283

If flips occurred, corrected independent labels are authoritative. Old numbers are not preserved for narrative convenience.

Dense sampling plus refinement is a numerical certificate, not a continuous-frequency proof.
