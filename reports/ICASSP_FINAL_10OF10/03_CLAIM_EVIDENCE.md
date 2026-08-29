# 03 — Claim–evidence audit

**Verdict:** PASS

Checked against `reports/ICASSP_10OF10/01_THEORY_AND_CLAIM_REGISTRY.md`.

| Claim in manuscript | Allowed? | Evidence |
|---|---|---|
| Finite-universe exactness iff \(D_V\le\tau<D_I\) | yes (proved for finite \(\mathcal{U}_t\)) | Proposition 1 |
| \(G_r\le 0\) is an empirical certificate, not a global theorem | yes | theory + discussion |
| Independent verifier, not 4096 search, assigns final labels | yes | 4 flips |
| Coeff. non-separable 20/20 | yes | task_stats |
| Resp. non-separable 19/20 | yes | one near-tie disclosed |
| Same-order 20/20 | yes | 16/16 probe + 4/4 IIR library |
| Reference-choice 0/20; multi-ref 0/20 | yes | reports 06–07 |
| Suite S 8/8 positive control; “effectively singleton” | yes | singleton.json |
| Generated arm is a witness only | yes | 9 occupants, 4 tasks |
| Macro FRR 0.900 [0.871, 0.925]; pooled 370/412 secondary | yes | task-level unit |
| One mask family; no continuous-frequency proof | yes | discussion |

Forbidden claims were not made: global impossibility, \(\tau_R=0.05\) as the claim, 370/412 as a field rate, 20 tasks as DSP-in-general, uniqueness of Suite S maps, \(K\) recovers \(\mathcal{V}_t\).
