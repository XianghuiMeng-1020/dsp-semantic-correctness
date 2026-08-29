# PHASE 2A — Protocol lock

Phase 2A may create new certification evidence but may not alter any frozen scientific label or existing manuscript number without subsequent PI review.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting commit | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` |
| Phase-1 tag | `icassp-10of10-phase1-complete` → `54cdceb` |
| Phase-1 protocol lock | `icassp-10of10-phase1-protocol-lock` → `33033e8` |
| Baseline science | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| git status at lock | clean |

## Authoritative hashes at starting commit

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/summary.json` | `f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b` |
| `data/icassp_10of10/task_stats.json` | `00f9d5f226c48b0e31b9c7bf58cc96535c2305e9db6eb2944e2ce6efe34ee884` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |
| `results/icassp_10of10_hardening/phase1/headline.json` | `9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed` |
| `results/icassp_10of10_hardening/phase1/fir_continuous_certification.json` | `263b69f0d444b7e5b5e9efb534730c85dfb85c2b636d30eac32a7865cffcdc17` |
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | `bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49` |

## Existing certifier / checker paths (do not import for Phase-2A decisions)

| Role | Path |
|---|---|
| Phase-1 FIR certifier | `src/continuous_certification/fir_adaptive.py` |
| Construction checker | `src/spec_checker.py` via `src/verification/search_checker.py` |
| Old final verifier | `src/verification/independent_spec_verifier.py` |

## Locks

- Do not edit the manuscript, PDF, frozen labels, tasks, masks, floors, or Phase-0 / Phase-1 frozen JSON.
- Do not move existing tags.
- Do not run IIR certification, \(K^*\), metric robustness, mask sweeps, or public-`main` sync.
- New outputs live only under `results/icassp_10of10_hardening/phase2a/` and `reports/ICASSP_FINAL_10OF10/PHASE2A_*`.

The first scientific gate is denominator reconciliation (412 vs 1596). Certification proceeds only if that gate is not a material undocumented universe swap.
