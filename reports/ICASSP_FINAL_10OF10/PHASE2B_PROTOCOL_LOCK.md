# PHASE 2B — Protocol lock

Phase 2B evaluates the already frozen implementations and specifications. It cannot change the scientific universe, validity definitions, or original labels in response to certification outcomes.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD / current HEAD | `0e743b8e87e813f0c8ddddcbaa059b6e59aff52b` |
| git status at lock | clean |
| Phase-0 baseline | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| Phase-1 protocol lock | `33033e853acc7da8d9ffb71960a3ccbbbf4ef198` / `icassp-10of10-phase1-protocol-lock` |
| Phase-1 final | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` / `icassp-10of10-phase1-complete` |
| Phase-2A protocol lock | `2f475f69be23d3de49b90408f74e8ca6905a8f4d` / `icassp-10of10-phase2a-protocol-lock` |
| Phase-2A frozen-result | `10df2b3642e9f5ec9c8cdf8fe12fa0d4d69cff17` / `icassp-10of10-phase2a-complete` |
| Other tag (not moved) | `icassp-spec-final-10of10` → `905c53d1f340d7c24dfaaf5497981a4f5fd0ae02` |

The Phase-2A frozen-result tag remains at `10df2b3`. It must not be moved. HEAD `0e743b8` is the Phase-2A audit/verify extension after that tag.

## Authoritative hashes at lock

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
| `results/icassp_10of10_hardening/phase2a/headline.json` | `85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b` |
| `results/icassp_10of10_hardening/phase2a/fir_power_polynomial_certification.json` | `f5de5ef06dae0118ddd4349fba35b9a2ed71dec65e72f2741ff3a8774d53f7ff` |
| `results/icassp_10of10_hardening/phase2a/denominator.json` | `6c4bda19e73e3ed8f1fbcf5e69a3bc4f7378271b7e493f133af3b1315fc9dce4` |

## Locks

- Do not edit the manuscript, PDF, frozen labels, tasks, masks, floors, or Phase-0 / Phase-1 / Phase-2A frozen JSON.
- Do not move existing tags.
- Do not run \(K^*\), metric robustness, mask sweeps, novelty experiments, or public-`main` sync.
- New outputs live only under `results/icassp_10of10_hardening/phase2b/` and `reports/ICASSP_FINAL_10OF10/PHASE2B_*`.

Phase 2B has two scientific arms only: (1) resolve the two remaining constructed-FIR `UNDECIDED` occupants by a root/sign method distinct from Phase-2A Bernstein; (2) continuously certify the frozen IIR corpus (strict stability + magnitude polynomial sign).
