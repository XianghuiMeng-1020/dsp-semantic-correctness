# PHASE 0 — Headline claim provenance

Source manuscript: `manuscript/w4/paper.tex` (SHA-256 `4750d393…`).
Computation: `experiments/icassp_10of10/pipeline.py` → `data/icassp_10of10/*.json`.
“Recomputed?” means the number was re-derived from the frozen artifacts
and/or the live `run_all` invocation in this phase, **not** that a JSON
was merely read and believed.

| Claim | Manuscript location | Source file/script | Frozen input | Recomputed? | Exact match? | Notes |
|---|---|---|---|---|---|---|
| 20 non-unique mask tasks | Abstract; §3; Table 1 | `registry/suite_n.json` | 20 `task_id`s | YES (count tasks) | YES | 16 FIR + 4 IIR |
| 8 singleton controls | Abstract; Table 1; §4 | `registry/suite_s.json` | 8 tasks | YES | YES | unique-map identities |
| Suite S valid 12 / invalid 16 | Table 1 | `singleton.json` rows | Suite S occupants | YES (`_indep_ok` 12/28) | YES | 28 rows = 12+16 |
| Independent valids 412 | §3; Table 1 | `pipeline.recertify` / `recertify.json` | 416 constructed valids | YES | YES | 416−4 flips |
| Mechanism invalids 144 | §3; Table 1 | `data/invalid/` + recertify | 144 mutants | YES | YES | all independently INVALID |
| Boundary invalids 160/160 | §3; Discussion | `boundary_invalids.py` / `boundary_invalids.json` | 20×2×4 ε | YES (`independent_ok` all 0) | YES | PASS_DROP / STOP_LIFT |
| 4 construction→verifier flips | §3; Discussion | `recertify.json` flips[] | 4 tight `firwin2` | YES | YES | LP/HP 8k+16k |
| 88 / 24 / 300 source split | §3; Discussion | `task_stats.json` by_source | verified valids | YES | YES | 58/14/298 discord at τ=0.05 |
| Coeff. \(G_r\le 0\) on 20/20 | Abstract; Table 2; §4 | `pipeline` task metrics | U_t = valids+probes+invalids+boundary | YES (`n_coeff_nonsep=20`) | YES | finite U_t |
| Resp. \(G_r\le 0\) on 19/20 | Table 2; §4 | same | same | YES (`n_resp_nonsep=19`) | YES | one IIR HP tight ~3.8e-6 |
| Inversions 20/20 | Table 2; §4 | same | boundary invalids in U_t | YES | YES | near-boundary |
| Suite S \(G_r>0\) 8/8 | Table 2; §4 | `singleton.json` metrics | 8 tasks | YES (8/8 `exact_threshold_exists`) | YES | not a uniqueness proof |
| Task-macro FRR 0.900 | §4; Table 2 | `task_stats.macro.mean` | 20 task FRRs | YES (0.900144… → 0.900) | YES (rounding) | τ_R=0.05 descriptive |
| Median 0.907; IQR [0.893,0.947]; range [0.727,0.950] | §4 | `task_stats.macro` | same | YES | YES (rounding) | |
| 95% CI [0.871, 0.925] | §4; Table 2 | bootstrap B=10^4 seed 20260826 | task FRRs | YES ([0.871253…, 0.924536…]) | YES (rounding) | task-cluster |
| Pooled 370/412=0.898 | §4; Table 2 | historical \(d\) > 0.05 | 412 valids | YES (370, rate 0.898058…) | YES | secondary |
| 20/20 tasks have a valid with \(d_{\mathrm{coeff}}>\tau_R\) | §4 | `tasks_with_reference_disagreement` | 20 | YES | YES | not the gap claim |
| FIR Type-I probe 16/16 discordant | Table 3; §4 | `feasible_probe.json` | seed 20260826, 512-pt LP | YES | YES | independently re-verified |
| IIR equal-length library 4/4 | Table 3; §4 | `existing_same_order` IIR | library occupants | YES | YES | no pole/zero LP |
| Same-order/same-structure 20/20 | Abstract; Table 3 | 16+4 | above | YES | YES | IIR weaker by design |
| Any library reference exact 0/20 | Abstract; Table 3 | `reference_choice.json` | all library \(h_r\) | YES (`any_ref_separable_coeff` sum 0) | YES | coeff. only |
| \(K=1,3,5,\mathrm{all}\) exact 0/20 | Abstract; Table 3 | `multi_reference.json` | deterministic method order | YES (0 exact_threshold hits) | YES | |
| Generated witnesses 9 on 4/4 original masks | §4 | `generated_witness.json` | frozen Arm G occupants | YES | YES | not pooled into n |
| “No scalar threshold separates…” | Abstract; Prop. 1 | \(G_r\le 0\) on U_t | 20 tasks | YES | YES **on U_t** | not a global theorem |
| “All alternative references fail” | Abstract / Table 3 | library catalog only | finite library | YES | YES **for that catalog** | not all possible \(r\in\mathcal{V}_t\) |
| Dense grid is not a continuous proof | §3; Discussion | verifier docstring | — | N/A | N/A | correctly scoped |
| \(N_f=131072\); floors \(10^{-6}/10^{-3}\); pole 0.999 | §3 | verifier + registry | registry | YES | YES | |
| Flip residual up to \(1.6\times 10^{-2}\) | §3 | flip_reason / residuals | 4 flips | YES (max 0.01594) | YES | |

## Issues recorded (not repaired)

1. Abstract “every library choice of reference” is true for the **independently verified library catalog**, not for an optimized \(r\in\mathcal{V}_t\cap\mathcal{U}_t\).
2. Exactness in §2 is defined as \(\mathcal{A}=\mathcal{V}_t\) over all \(h\); Proposition 1 is only on finite \(\mathcal{U}_t\). The paper usually says so; the title/abstract are broader.
3. `near_boundary=1` on 409/412 valids is a loose heuristic (`NEAR_ABS=1e-5`), not a published headline.

**Headline provenance verdict:** PASS (numbers match frozen computation). Scope caveats are recorded, not hidden.
