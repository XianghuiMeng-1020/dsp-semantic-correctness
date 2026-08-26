# 05 — Final reproduction after manuscript freeze

**Verdict:** PASS

Command:

```bash
python -m experiments.icassp_10of10.run_all
```

Completed with `ALL_10OF10_STAGES: DONE` in 1015.2 s.
Manuscript was then rebuilt from a clean auxiliary set
(`pdflatex` + `bibtex` + `pdflatex` ×2). Headline numbers did not move.

| Locked headline | Regenerated value | Match |
|---|---|---|
| Independent valid | 412 | yes |
| Invalid | 144 | yes |
| Label flips | 4 | yes |
| Pooled FRR | 370/412 = 0.898058… → 0.898 | yes |
| Task-macro FRR | 0.900144… → 0.900 | yes |
| 95% CI | [0.871253…, 0.924536…] → [0.871, 0.925] | yes |
| Same-order discordant | 16/16 FIR probe + 4/4 IIR library = 20/20 | yes |
| Coefficient non-separable | 20/20 | yes |
| Response non-separable | 19/20 | yes |
| Boundary inversion | 20/20 | yes |
| Reference-choice exact | 0/20 (`any_ref_separable_coeff` sum = 0) | yes |
| Multi-ref exact | 0/20 (`exact_threshold_exists` hits = 0) | yes |
| Suite S $G_r>0$ | 8/8 | yes |

`headline_374_of_416_survives` = 0 (expected).
The final tag is allowed to proceed on this lock.
