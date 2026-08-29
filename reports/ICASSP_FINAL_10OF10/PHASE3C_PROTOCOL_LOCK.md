# PHASE 3C — Protocol lock

Phase 3C audits whether a **frozen** Phase-3B observed-valid reference catalog, selected on the confirmatory valid universe used to compute \(K^\star_{\mathrm{obs}}\), transfers to additional independently certified specification-valid realizations that were **not** used to select that catalog. If no such catalog-excluded holdout exists, the audit must stop rather than invent one.

> No external-validity artifact may be used to alter catalog selection, task definitions, thresholds, metrics, or frozen base-universe labels. Primary catalogs must be frozen before external-validity scores are inspected.

This is **not** a new prototype-selection algorithm. Set-cover / prototype selection remain known prior art. Ambient-center impossibility is **not** the paper's story.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `7a0c670a5273f34aff1a3fb00842ddf1ea01aa85` |
| git status at lock | clean |
| Phase-0 baseline | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| Phase-1 complete | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` / `icassp-10of10-phase1-complete` |
| Phase-2A complete | `10df2b3642e9f5ec9c8cdf8fe12fa0d4d69cff17` / `icassp-10of10-phase2a-complete` |
| Phase-2B complete | `d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9` / `icassp-10of10-phase2b-complete` |
| Phase-3A complete | `be675b8f2d319f999ca9b1f9515f09dc2f3aef6d` / `icassp-10of10-phase3a-complete` |
| Phase-3B protocol lock | `714a8ee78b71f42e1f6914303444b06b51917f1c` / `icassp-10of10-phase3b-protocol-lock` |
| Phase-3B complete | `7a0c670a5273f34aff1a3fb00842ddf1ea01aa85` / `icassp-10of10-phase3b-complete` |
| Other tag (not moved) | `icassp-spec-final-10of10` → `905c53d1f340d7c24dfaaf5497981a4f5fd0ae02` |

Starting HEAD equals the Phase-3B complete tag. Existing tags must not be moved.

## Authoritative hashes at lock

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/summary.json` | `f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |
| `data/icassp_10of10/feasible_probe.json` | `bad0223edec5b62ef72e05dd17c2a8eb135f1f0831d10b0dfdf4da314e0a6b10` |
| `data/icassp_10of10/multi_reference.json` | `44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67` |
| `results/icassp_10of10_hardening/phase1/headline.json` | `9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed` |
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | `bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49` |
| `results/icassp_10of10_hardening/phase2a/headline.json` | `85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b` |
| `results/icassp_10of10_hardening/phase2a/fir_power_polynomial_certification.json` | `f5de5ef06dae0118ddd4349fba35b9a2ed71dec65e72f2741ff3a8774d53f7ff` |
| `results/icassp_10of10_hardening/phase2b/headline.json` | `e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927` |
| `results/icassp_10of10_hardening/phase3a/headline.json` | `a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f` |
| `results/icassp_10of10_hardening/phase3b/headline.json` | `fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0` |
| `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json` | `92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061` |

## Exact Phase-3B optimal catalog witnesses (coefficient \(K^\star_{\mathrm{obs}}\))

These catalogs are frozen inputs. They must not be reselected after any holdout inspection.

| task | n_valid (Phase-3B \(V_t\)) | K* | D_V | D_I | status |
| --- | ---: | ---: | ---: | ---: | --- |
| fir_lp_loose_8k | 89 | 42 | (from Phase-3B JSON) | (from Phase-3B JSON) | EXACT_OPTIMUM |
| fir_lp_tight_8k | 104 | 84 | | | EXACT_OPTIMUM |
| fir_lp_loose_16k | 89 | 41 | | | EXACT_OPTIMUM |
| fir_lp_tight_16k | 104 | 84 | | | EXACT_OPTIMUM |
| fir_hp_loose_8k | 90 | 38 | | | EXACT_OPTIMUM |
| fir_hp_tight_8k | 104 | 20 | | | EXACT_OPTIMUM |
| fir_hp_loose_16k | 90 | 23 | | | EXACT_OPTIMUM |
| fir_hp_tight_16k | 104 | 17 | | | EXACT_OPTIMUM |
| fir_bp_loose_8k | 87 | 48 | | | EXACT_OPTIMUM |
| fir_bp_tight_8k | 111 | 23 | | | EXACT_OPTIMUM |
| fir_bp_loose_16k | 87 | 49 | | | EXACT_OPTIMUM |
| fir_bp_tight_16k | 111 | 21 | | | EXACT_OPTIMUM |
| fir_bs_loose_8k | 90 | 19 | | | EXACT_OPTIMUM |
| fir_bs_tight_8k | 123 | 113 | | | EXACT_OPTIMUM |
| fir_bs_loose_16k | 90 | 21 | | | EXACT_OPTIMUM |
| fir_bs_tight_16k | 123 | 112 | | | EXACT_OPTIMUM |
| iir_lp_loose_8k | 19 | 15 | | | EXACT_OPTIMUM |
| iir_lp_tight_8k | 19 | 19 | | | EXACT_OPTIMUM |
| iir_hp_loose_8k | 19 | 17 | | | EXACT_OPTIMUM |
| iir_hp_tight_8k | 19 | 19 | | | EXACT_OPTIMUM |

Exact IDs, stored \(\tau\), \(D_V\), \(D_I\), and gap live in `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json`. The Phase-3C freeze file must copy those witnesses without re-solving.

Phase-3B \(V_t=\mathrm{constructed}+\mathrm{Type\text{-}I~probes}\). FIR `n_valid` is therefore **not** the manuscript 412-only constructed count.

## Locks

- Do not edit the manuscript, PDF, title, abstract, frozen labels, tasks, masks, floors, distances, or Phase-0/1/2/3A/3B outputs.
- Do not move existing tags.
- Do not add metrics, tasks, filters, Type-I probes, or LLM generations.
- Do not reselect Phase-3B catalogs after observing holdout performance.
- Do not use holdout validity to choose a better Phase-3B catalog or to increase \(\tau\).
- Do not synchronize public `main`.
- New outputs live only under `results/icassp_10of10_hardening/phase3c/` and `reports/ICASSP_FINAL_10OF10/PHASE3C_*`.

## Transfer threshold convention (base-universe only)

For a frozen catalog \(R^\star\) with confirmatory distances \(D_V(R^\star)<D_I(R^\star)\),

\[
\tau_{\mathrm{safe}}
=
\mathrm{nextafter}(D_I(R^\star),0)
\]

the largest IEEE-754 binary64 value strictly less than \(D_I(R^\star)\). This is the strongest still-safe threshold that rejects every frozen base invalid while preserving all base valid coverage whenever \(D_V\le\tau_{\mathrm{safe}}\). Do **not** use the midpoint \((D_V+D_I)/2\) if a larger still-safe value exists. Do **not** retune \(\tau\) on any external set.

Numerical constants: `G_ZERO_ABS = 1e-15` (Phase-3B exactness). Representation: IEEE-754 binary64 via Python `math.nextafter`.

## Frozen descriptive transfer bands (locked before holdout scoring)

These cutoffs are descriptive only. They will not be moved after seeing results.

| Band | TransferAccept |
|---|---|
| Robust | \(\mathrm{TransferAccept}\ge 0.95\) |
| Partial | \(0.75\le\mathrm{TransferAccept}<0.95\) |
| Fragile | \(\mathrm{TransferAccept}<0.75\) |

Suite wording: **external-validity transfer** / **out-of-catalog valid-realization transfer**. Not a population generalization estimate.

## Frozen descriptive maintenance bands (locked before expanded-\(K^\star\) inspection)

| Band | Relative growth \(\Delta K/K^\star_{\mathrm{base}}\) |
|---|---|
| Low | \(\le 0.10\) |
| Moderate | \(0.10 < \cdot \le 0.30\) |
| High | \(> 0.30\) |

## Holdout eligibility (locked before scoring)

A corpus is eligible as **PRIMARY** external validity only if all of the following hold:

1. it existed before Phase 3C;
2. it was not used to fit Phase-3B catalog selection (not a member of Phase-3B \(V_t\), not a candidate reference, and it did not affect \(D_V\), \(D_I\), or \(\tau\));
3. its task membership is frozen;
4. its specification-valid status is independently established;
5. after a protocol-defined exact-duplicate rule, remaining occupants are not coefficient-identical (and, for response scoring, not response-identical under the frozen representation) to a base occupant.

If the intended Type-I probe corpus fails (2), the required stop is:

`PHASE3C_HOLDOUT_LEAKAGE_BLOCKER`

Do not proceed with a false holdout claim. Do not re-fit \(K^\star\) on the constructed-only 412 after the fact in order to manufacture independence.

### Deduplication rule (locked)

If a candidate holdout occupant is retained, remove it from the holdout **only** when its frozen coefficient vector is exactly equal (IEEE-754 identity after the Phase-1 coefficient canonicalize used by `d_coeff`) to some Phase-3B base valid. Do not remove difficult non-duplicate cases.

## First scientific gate after this lock

1. Inventory every pre-existing valid/invalid corpus.
2. Test Type-I leakage into Phase-3B catalog selection.
3. Freeze `results/icassp_10of10_hardening/phase3c/frozen_base_catalogs.json` from Phase-3B witnesses only.
4. Score a holdout **only if** leakage is clean. Otherwise stop.

## PI novelty-gate note (locked)

Phase 3B printed `NOVELTY_10OF10_GATE = PASS`. The PI rejected that gate. Phase 3C reopens novelty. A numeric internal score is not the PI gate.
