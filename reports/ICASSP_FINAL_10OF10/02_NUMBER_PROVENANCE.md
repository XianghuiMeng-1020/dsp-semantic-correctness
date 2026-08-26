# 02 — Number provenance

**Verdict:** PASS

Every manuscript headline traces to `data/icassp_10of10/` after independent verification.

| Manuscript number | Source | Notes |
|---|---|---|
| 412 independent valids | `recertify.json` / `summary.json` | 416−4 flips |
| 144 mechanism invalids | `recertify.json` | unchanged |
| 4 label flips | `recertify.json` flips[] | tight firwin2 LP/HP |
| 370/412 = 0.898 | `task_stats.json` pooled_descriptive_FRR | secondary |
| task-macro FRR 0.900 | `task_stats.json` macro.mean | rounded from 0.900144… |
| 95% CI [0.871, 0.925] | `task_stats.json` macro.ci95 | rounded |
| median 0.907, IQR [0.893, 0.947], range [0.727, 0.950] | `task_stats.json` | rounded |
| 20/20 task disagreement | `task_stats.json` | descriptive τ=0.05 |
| 20/20 coeff. \(G_r\le 0\) | `task_stats.json` n_coeff_nonsep | |
| 19/20 resp. \(G_r\le 0\) | `task_stats.json` n_resp_nonsep | |
| 20/20 inversions | `task_stats.json` n_boundary_inversions | |
| 16/16 FIR Type-I probe | `feasible_probe.json` | independently verified |
| 4/4 IIR same-order library | `feasible_probe.json` existing_same_order | |
| 20/20 same-order discordant | probe + IIR library | |
| 0/20 reference-choice exact | `reference_choice.json` | |
| 0/20 multi-ref \(K=1,3,5,all\) | `multi_reference.json` | |
| 8/8 Suite S \(G_r>0\) | `singleton.json` | |
| 9 generated witnesses | `generated_witness.json` | 4/4 original masks |
| 88/24/300 source split; 58/14/298 discord | `task_stats.json` by_source | |
| 160/160 boundary invalids | `boundary_invalids.json` | |
| \(N_f=131072\), floors \(10^{-6}/10^{-3}\), pole 0.999 | verifier + registries | |
| seed 20260826, \(B=10^4\) | `environment.json` / config | |

Not used as current headlines: 374/416, 0.899, 346/416 any3, 25/67 order-lock, Oracle C FRR=FAR=0 as validation.
