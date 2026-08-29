# PHASE 0 — Existing reproduction only

No new experiment design. No headline retune.
After the live run, timestamp-only overwrites (`elapsed_s`) were
**reverted** so frozen artifacts stay at the baseline commit.

## Command

```bash
python -m experiments.icassp_10of10.run_all
```

This is the currently intended entry point (`experiments/icassp_10of10/run_all.py`).

## Environment (this machine)

| Item | Value |
|---|---|
| OS | Windows-11-10.0.26200 |
| Python | 3.12.10 |
| NumPy | 2.3.5 |
| SciPy | 1.15.3 |
| Seed | 20260826 |
| Runtime | 979.1 s |
| Warnings | SciPy `BadCoefficients` on some IIR numerators (same as prior runs); `write_reports.py` `SyntaxWarning` on `\(` in f-strings |
| Errors | none |
| Exit | `ALL_10OF10_STAGES: DONE` (exit 0) |

## Headline recompute vs manuscript

| Quantity | Manuscript | Live recompute | Match |
|---|---|---|---|
| Independent valid | 412 | 412 | YES |
| Mechanism invalid | 144 | 144 | YES |
| Flips | 4 | 4 | YES |
| Pooled FRR | 370/412 = 0.898 | 370/412 = 0.898058… | YES |
| Task-macro FRR | 0.900 | 0.900144… | YES |
| 95% CI | [0.871, 0.925] | [0.871253…, 0.924536…] | YES |
| Coeff. non-sep | 20/20 | 20 | YES |
| Resp. non-sep | 19/20 | 19 | YES |
| Inversions | 20/20 | 20 | YES |
| FIR probe discord | 16/16 | 16/16 (same probe counts) | YES |
| Generated witnesses | 9 | 9 | YES |
| `iir_hp_tight_8k` \(G_{\mathrm{resp}}\) | order \(10^{-6}\) | \(+3.804604682714971\times 10^{-6}\) | YES |

`task_stats.json` and `recertify.json` SHA-256 **unchanged**.
`summary.json` differed only in `elapsed_s` (1015.17 → 979.14) and
was restored to the baseline file.

Per-task \(G_{\mathrm{coeff}}\) printed values matched the previous
run to the printed precision (same 20-task table).

## Verdict

```text
PASS_EXACT
```

Rounding in the PDF (0.900, [0.871, 0.925], 0.898) is documented
display rounding of the same floats. No scientific mismatch.
