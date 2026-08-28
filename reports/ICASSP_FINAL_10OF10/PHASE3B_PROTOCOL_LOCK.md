# PHASE 3B — Protocol lock

Phase 3B measures the minimum catalog size required by the existing reference-oracle family. It may not modify the oracle family, metric, task universe, labels, or candidate realization corpus after observing results.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `be675b8f2d319f999ca9b1f9515f09dc2f3aef6d` |
| git status at lock | clean |
| Phase-0 baseline | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| Phase-1 complete | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` / `icassp-10of10-phase1-complete` |
| Phase-2A complete | `10df2b3642e9f5ec9c8cdf8fe12fa0d4d69cff17` / `icassp-10of10-phase2a-complete` |
| Phase-2B complete | `d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9` / `icassp-10of10-phase2b-complete` |
| Phase-3A protocol lock | `171703da17a81b4c8dfb73ed465912264bdd85e5` / `icassp-10of10-phase3a-protocol-lock` |
| Phase-3A complete | `be675b8f2d319f999ca9b1f9515f09dc2f3aef6d` / `icassp-10of10-phase3a-complete` |
| Other tag (not moved) | `icassp-spec-final-10of10` → `905c53d1f340d7c24dfaaf5497981a4f5fd0ae02` |

Starting HEAD equals the Phase-3A complete tag. Existing tags must not be moved.

## Authoritative hashes at lock

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/summary.json` | `f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |
| `data/icassp_10of10/multi_reference.json` | `44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67` |
| `results/icassp_10of10_hardening/phase1/headline.json` | `9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed` |
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | `bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49` |
| `results/icassp_10of10_hardening/phase2b/headline.json` | `e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927` |
| `results/icassp_10of10_hardening/phase2b/iir_continuous_certification.json` | `7b172b1a7e47d734a4013f153f7633c60111d22aed93a29a59dc357fe68ccc22` |
| `results/icassp_10of10_hardening/phase3a/headline.json` | `a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f` |
| `results/icassp_10of10_hardening/phase3a/coefficient_ambient.json` | `7160bf5cb68fc101bf636f5020f3746c50e7d0dc6cb7e2d66070f45e880f59a0` |
| `results/icassp_10of10_hardening/phase3a/response_ambient.json` | `9389b2ee7fe85c61e98b97a75c6a4d33e10c6df1afcc2e5cc997be97a05fdb16` |
| `results/icassp_10of10_hardening/phase3a/hierarchy.json` | `5b1d0b28d9d4d99c98ebe2fd337d83971fbb739dce73df92fe029d8b2b3c4af9` |

## Locks

- Do not edit the manuscript, PDF, title, abstract, frozen labels, tasks, masks, floors, distances, or Phase-0/1/2/3A outputs.
- Do not move existing tags.
- Do not add metrics, tasks, filters, or LLM generations.
- Do not synchronize public `main`.
- New outputs live only under `results/icassp_10of10_hardening/phase3b/` and `reports/ICASSP_FINAL_10OF10/PHASE3B_*`.

The Phase-3B quantity is **Observed-valid Reference Catalog Complexity** \(K_{t,\mathrm{obs}}^\star\): the minimum number of observed specification-valid realizations such that the existing min-distance / common-threshold oracle exactly recovers frozen membership on \(\mathcal{U}_t\). It is a finite-universe diagnostic, not a new classifier, and not unrestricted \(K^*\) over all DSP implementations.

## Frozen descriptive burden bands (locked before K* inspection)

These cutoffs are descriptive only. They will not be moved after seeing results.

| Band | Burden ratio \(\rho=K^\star_{\mathrm{obs}}/\|V_t\|\) |
|---|---|
| Low | \(\rho\le 0.10\) |
| Moderate | \(0.10<\rho\le 0.30\) |
| High | \(0.30<\rho\le 0.70\) |
| Near-enumerative | \(\rho>0.70\) |

Ambient-vs-catalog classes (also locked now):

- **R1**: Phase-3A ambient center exists and \(\rho\le 0.10\).
- **R2**: ambient exists and \(\rho>0.30\).
- **R3**: no ambient center and \(\rho>0.30\).
- **R4**: any other combination (including moderate \(\rho\), or no ambient with low/moderate \(\rho\)).

Suite-level catalog-burden verdict (locked now):

- `CATALOG_BURDEN_STRONG`: at least 15/20 coefficient tasks are High or Near-enumerative.
- `CATALOG_BURDEN_WEAK`: at least 15/20 coefficient tasks have \(K^\star\le 3\) or Low burden.
- `CATALOG_BURDEN_MIXED`: neither STRONG nor WEAK, and exact optima exist for all 20.
- `CATALOG_ANALYSIS_INCONCLUSIVE`: exact optimization is missing on enough tasks to block a suite conclusion.
