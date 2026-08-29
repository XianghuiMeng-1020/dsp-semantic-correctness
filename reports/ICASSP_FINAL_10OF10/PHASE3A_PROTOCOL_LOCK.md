# PHASE 3A — Protocol lock

Phase 3A tests a stronger oracle family over the frozen universe. No task, metric, implementation, validity label, or correctness specification may change after observing the result.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9` |
| git status at lock | clean |
| Phase-0 baseline | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| Phase-1 protocol lock | `33033e853acc7da8d9ffb71960a3ccbbbf4ef198` / `icassp-10of10-phase1-protocol-lock` |
| Phase-1 final | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` / `icassp-10of10-phase1-complete` |
| Phase-2A protocol lock | `2f475f69be23d3de49b90408f74e8ca6905a8f4d` / `icassp-10of10-phase2a-protocol-lock` |
| Phase-2A frozen-result | `10df2b3642e9f5ec9c8cdf8fe12fa0d4d69cff17` / `icassp-10of10-phase2a-complete` |
| Phase-2B protocol lock | `b5271454e1cb903cb130aaf8805e45c5542c6b4b` / `icassp-10of10-phase2b-protocol-lock` |
| Phase-2B final | `d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9` / `icassp-10of10-phase2b-complete` |
| Other tag (not moved) | `icassp-spec-final-10of10` → `905c53d1f340d7c24dfaaf5497981a4f5fd0ae02` |

Starting HEAD equals the Phase-2B complete tag. Existing tags must not be moved.

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
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | `bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49` |
| `results/icassp_10of10_hardening/phase1/fir_continuous_certification.json` | `263b69f0d444b7e5b5e9efb534730c85dfb85c2b636d30eac32a7865cffcdc17` |
| `results/icassp_10of10_hardening/phase2a/headline.json` | `85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b` |
| `results/icassp_10of10_hardening/phase2a/fir_power_polynomial_certification.json` | `f5de5ef06dae0118ddd4349fba35b9a2ed71dec65e72f2741ff3a8774d53f7ff` |
| `results/icassp_10of10_hardening/phase2a/denominator.json` | `6c4bda19e73e3ed8f1fbcf5e69a3bc4f7378271b7e493f133af3b1315fc9dce4` |
| `results/icassp_10of10_hardening/phase2b/headline.json` | `e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927` |
| `results/icassp_10of10_hardening/phase2b/iir_continuous_certification.json` | `7b172b1a7e47d734a4013f153f7633c60111d22aed93a29a59dc357fe68ccc22` |
| `results/icassp_10of10_hardening/phase2b/fir_remaining_resolution.json` | `c0e977755bb231073cdf9ebc0c001e0f137bfb53178e0a315a3df8bb0adcbec0` |
| `results/icassp_10of10_hardening/phase2b/population.json` | `68010979e87a1971953c932a0b9a08a4c6433c5717a00f699baca9a69245a15d` |

## Locks

- Do not edit the manuscript, PDF, title, abstract, frozen labels, tasks, masks, floors, or Phase-0 / Phase-1 / Phase-2A / Phase-2B frozen outputs.
- Do not move existing tags.
- Do not run \(K^*\), a mechanical metric sweep, a mask sweep, new tasks, LLM generations, or public-`main` sync.
- Do not invent a new favorable metric or change existing distance definitions.
- New outputs live only under `results/icassp_10of10_hardening/phase3a/` and `reports/ICASSP_FINAL_10OF10/PHASE3A_*`.

Phase 3A has three scientific arms only: (1) metric-geometry audit of the existing confirmatory distances; (2) prior-art boundary for test oracles, sphere separation, and DSP specification verification; (3) unrestricted single-center (ambient) separability under already existing Euclidean-equivalent metrics, with certificates and a three-level reference hierarchy.

The quantity \(\Gamma_t^{\mathrm{amb}}\) is not the manuscript fixed-reference \(G_r\) and is not Phase-1 \(G_{\mathrm{obs}}^\star\).
