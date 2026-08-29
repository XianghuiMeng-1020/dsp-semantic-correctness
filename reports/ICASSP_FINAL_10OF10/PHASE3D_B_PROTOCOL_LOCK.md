# PHASE 3D-B — Pre-unblind protocol lock

Phase 3D-B is the first phase authorized to score the Phase-3D-A frozen prospective challenge against already-fitted Phase-3B realization-reference catalogs.

This report freezes catalogs, thresholds, endpoints, bands, ties, aggregation, and maintenance rules **before** any Phase-3D challenge-to-reference distance is computed.

> No H_VALID or H_INVALID coefficient or response distance to a Phase-3B catalog, hierarchy oracle, ambient center, or canonical/best-observed identity may be computed until tag `icassp-10of10-phase3d-b-preunblind-lock` exists.

PI override (Phase-3D-A ADEQUATE gate failed on invalid-side balance): H_VALID is the **primary** scientific endpoint; H_INVALID is a **secondary diagnostic** only. No additional generation is authorized. No claim of complete 20-task prospective invalid validation is permitted.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `8ae58fd14aca92b236a920a1678f5de396e2a5f5` |
| git status at lock | clean |
| Phase-3D-A final | `8ae58fd14aca92b236a920a1678f5de396e2a5f5` / `icassp-10of10-phase3d-a-complete` |
| Challenge-frozen commit | `8ccb7f18f1b9f48ce8c4f40ff6df202bdec6862e` |
| Challenge-frozen tag | `icassp-10of10-phase3d-a-challenge-frozen` (**do not move**) |

## Previous phase tag targets (do not move)

| Tag | Commit |
|---|---|
| `icassp-pre-10of10-hardening-baseline` | `41c8e69194ebabde3a68b1333df1beb3f2e01160` |
| `icassp-10of10-phase1-protocol-lock` | `33033e853acc7da8d9ffb71960a3ccbbbf4ef198` |
| `icassp-10of10-phase1-complete` | `54cdceb40ff4eb543837771b35832c2e6c2f6c15` |
| `icassp-10of10-phase2a-protocol-lock` | `2f475f69be23d3de49b90408f74e8ca6905a8f4d` |
| `icassp-10of10-phase2a-complete` | `10df2b3642e9f5ec9c8cdf8fe12fa0d4d69cff17` |
| `icassp-10of10-phase2b-protocol-lock` | `b5271454e1cb903cb130aaf8805e45c5542c6b4b` |
| `icassp-10of10-phase2b-complete` | `d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9` |
| `icassp-10of10-phase3a-protocol-lock` | `171703da17a81b4c8dfb73ed465912264bdd85e5` |
| `icassp-10of10-phase3a-complete` | `be675b8f2d319f999ca9b1f9515f09dc2f3aef6d` |
| `icassp-10of10-phase3b-protocol-lock` | `714a8ee78b71f42e1f6914303444b06b51917f1c` |
| `icassp-10of10-phase3b-complete` | `7a0c670a5273f34aff1a3fb00842ddf1ea01aa85` |
| `icassp-10of10-phase3c-protocol-lock` | `5de9d2c582893252e0370d145b958cb2803396a2` |
| `icassp-10of10-phase3c-complete` | `4f6d498ad26065962ebba80e8aa019dfbe8ec1c2` |
| `icassp-10of10-phase3d-a-protocol-lock` | `8bad1dbcb699a5e1f694a78053ec061bc81ac324` |
| `icassp-10of10-phase3d-a-challenge-frozen` | `8ccb7f18f1b9f48ce8c4f40ff6df202bdec6862e` |
| `icassp-10of10-phase3d-a-complete` | `8ae58fd14aca92b236a920a1678f5de396e2a5f5` |
| `icassp-spec-final-10of10` | `905c53d1f340d7c24dfaaf5497981a4f5fd0ae02` |

## Authoritative hashes at lock

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |
| `data/icassp_10of10/feasible_probe.json` | `bad0223edec5b62ef72e05dd17c2a8eb135f1f0831d10b0dfdf4da314e0a6b10` |
| `data/icassp_10of10/multi_reference.json` | `44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67` |
| `results/icassp_10of10_hardening/phase1/headline.json` | `9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed` |
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | `bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49` |
| `results/icassp_10of10_hardening/phase2a/headline.json` | `85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b` |
| `results/icassp_10of10_hardening/phase2b/headline.json` | `e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927` |
| `results/icassp_10of10_hardening/phase3a/headline.json` | `a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f` |
| `results/icassp_10of10_hardening/phase3b/headline.json` | `fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0` |
| `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json` | `92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061` |
| `results/icassp_10of10_hardening/phase3c/leakage.json` | `d02fb07b073ed6f1fd6648fb0f57d130e6b29ebee286cca02fc5488f0c2f962f` |
| `results/icassp_10of10_hardening/phase3c/frozen_base_catalogs.json` | `06f1a97d1ff4633cf167b47c8bb2fc69e5c24784a360c3e0532c3190d69e69a6` |
| `results/icassp_10of10_hardening/phase3d_a/H_VALID.json` | `8e02b28762ed28bccf0c6e8dec8c7ad28c021eb7ee791d13cbf2ec3f9de5dac1` |
| `results/icassp_10of10_hardening/phase3d_a/H_INVALID.json` | `61b37f89cca8941f1d9d3c30ecf08d6308e2e721adf7a200f5e158daa55d48fa` |
| `results/icassp_10of10_hardening/phase3d_a/CHALLENGE_MANIFEST.sha256` | `e104433f4b0721682034c8f4f08c04e5356feae8ee4bfe14518a0602d24f0498` |

Challenge identity hashes (H_VALID, H_INVALID, manifest) are recorded for integrity only. They are **not** reference distances.

## 1. Exact catalogs to be scored

Primary catalogs are the Phase-3B **stored** observed-valid optima. Do **not** re-optimize. Do **not** substitute another tied optimum after seeing holdout scores.

Source: `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json`.

For each task \(t\) and metric \(\in\{\mathrm{coeff},\mathrm{resp}\}\):

\[
R_{t,\mathrm{metric}}^\star
=
\texttt{primary.catalog\_ids}
\]

exactly as stored, including order.

If a future reconstruction ever encountered multiple stored tied optima (Phase 3B stored one witness per task/metric), the deterministic tie-break, using **only** Phase-3B information, is:

1. lexicographically smallest sorted reference-ID tuple;
2. then the Phase-3B stored \(\tau\) (smaller first);
3. then the Phase-3B stored catalog-index tuple.

The selected identity is written to `results/icassp_10of10_hardening/phase3d_b/FROZEN_CATALOGS_PREUNBLIND.json` **before** H_VALID scoring.

Hierarchy oracles (scored after primary \(R^\star\) transfer is frozen, still with base-only thresholds):

| Oracle | Identity source (frozen; not retuned on H_VALID) |
|---|---|
| canonical \(K=1\) | `data/valid/canonical.json` path |
| best-observed-valid \(K=1\) | Phase-1 `best_reference_id` (stored winner; not a retie) |
| published \(K=3\) | `multi_reference.json` `k_sweep` methods at \(K=3\) mapped to `data/valid/library/{task}__{method}.{npy\|npz}` |
| published \(K=5\) | same at \(K=5\) |
| all-library | every library occupant already in the Phase-3B base valid universe for that task |
| Phase-3B optimal \(K^\star_{\mathrm{obs}}\) | the primary frozen catalog above |

Missing library files are recorded as `oracle_undefined` for that task; they are not replaced by another method.

## 2. Exact thresholds

Thresholds depend **only** on the original Phase-3B base universe. H_VALID is not inspected when fixing \(\tau\).

For catalog \(R\) on the base occupants:

\[
D_V^{\mathrm{base}}(R)=\max_{v\in V_{\mathrm{base}}} d_R(v),\qquad
D_I^{\mathrm{base}}(R)=\min_{i\in I_{\mathrm{base}}} d_R(i).
\]

Phase-3B exactness: \(D_V^{\mathrm{base}}<D_I^{\mathrm{base}}\) (gap test \(G>10^{-15}\)).

**Primary** (IEEE-754 binary64):

\[
\tau_{\mathrm{maxsafe}}=\mathrm{nextafter}(D_I^{\mathrm{base}},-\infty)
\]

i.e. the predecessor of \(D_I\): the largest representable threshold strictly below \(D_I\). For \(D_I>0\) this coincides with Phase-3C `math.nextafter(D_I, 0.0)`.

Must satisfy \(\tau_{\mathrm{maxsafe}}\ge D_V^{\mathrm{base}}\) and \(\tau_{\mathrm{maxsafe}}<D_I^{\mathrm{base}}\).

**Secondary** (predeclared; one only):

\[
\tau_{\mathrm{mid}}=\frac{D_V^{\mathrm{base}}+D_I^{\mathrm{base}}}{2}.
\]

No additional thresholds may be added after observing transfer. Primary interpretation uses \(\tau_{\mathrm{maxsafe}}\).

Acceptance: \(d_R(h)\le\tau\) (closed at the frozen threshold). Because \(\tau_{\mathrm{maxsafe}}<D_I\), every frozen base invalid remains strictly rejected.

Written to `results/icassp_10of10_hardening/phase3d_b/FROZEN_THRESHOLDS_PREUNBLIND.json` **before** unblinding.

Metrics remain Phase-1 confirmatory: `d_coeff` = `d_coeff_canonical` magnitude-equivalent; `d_resp` = band-masked RMSE on the frozen \(N=131072\) grid. \(S_t\), masks, and residual floors are unchanged.

## 3. Primary / secondary endpoints

**Primary:** prospective valid-realization transfer of the 614 continuously certified H_VALID members (catalog-excluded realization transfer). Coefficient and response are reported separately and never combined into one score.

Per task:

\[
\mathrm{TransferAccept}_t
=
\frac{|\{h\in H_{t,\mathrm{VALID}}:d_{R_t^\star}(h)\le\tau_{t,\mathrm{maxsafe}}\}|}{|H_{t,\mathrm{VALID}}|},
\qquad
\mathrm{ExternalFRR}_t=1-\mathrm{TransferAccept}_t.
\]

This is an exact count on the frozen prospective challenge. It is **not** an estimate of all possible DSP implementations.

Preferred wording: **prospective valid-realization transfer** or **catalog-excluded realization transfer**.

Primary aggregate for interpretation: **task-macro median + full per-task distribution**. Pooled counts are reported but must not hide heterogeneous tasks.

**Secondary:** H_INVALID (310). Incomplete 20-task coverage. Aggregate only over tasks with \(n>0\). Do not compute a 20-task macro FAR by treating missing tasks as zero. Do not use H_INVALID to establish the central novelty result.

## 4. Descriptive interpretation bands (do not modify)

Valid transfer:

| Band | Rule |
|---|---|
| ROBUST | \(\mathrm{TransferAccept}\ge 0.95\) |
| PARTIAL | \(0.75\le\mathrm{TransferAccept}<0.95\) |
| FRAGILE | \(\mathrm{TransferAccept}<0.75\) |

Catalog relative growth \(g=\Delta K/K^\star_{\mathrm{base}}\):

| Band | Rule |
|---|---|
| LOW | \(g\le 0.10\) |
| MODERATE | \(0.10<g\le 0.30\) |
| HIGH | \(g>0.30\) |

Threshold-sensitivity (after primary freeze):

| Class | Rule |
|---|---|
| `ROBUST_TO_THRESHOLD_CHOICE` | no task changes ROBUST/PARTIAL/FRAGILE band vs \(\tau_{\mathrm{mid}}\) |
| `SOMEWHAT_SENSITIVE` | some tasks change band, but the suite-level verdict is unchanged |
| `MATERIALLY_SENSITIVE` | the suite-level transfer verdict changes |

Transfer verdicts (coefficient and response separately):

- `PROSPECTIVE_TRANSFER_STRONG_FAILURE` — multiple FRAGILE tasks, substantial task-macro failure, spanning more than one generator family / DSP regime
- `PROSPECTIVE_TRANSFER_MIXED` — some tasks/families transfer well and others poorly
- `PROSPECTIVE_TRANSFER_ROBUST` — nearly all tasks have \(\ge 95\%\) transfer
- `PROSPECTIVE_TRANSFER_INCONCLUSIVE` — scoring/provenance compromised

Do not force a failure classification. Do not select the threshold that makes a stronger paper.

## 5. Tie handling

Catalog identity: Phase-3B stored witness; if multiple, lex-smallest sorted ID tuple, then stored \(\tau\), then stored index tuple. No holdout-based tie.

Best-observed \(K=1\): use Phase-1 stored `best_reference_id`, not a retie on H_VALID.

Rejected-valid nearest-reference reporting: among catalog members, smallest distance, then lexicographically smallest reference ID.

## 6. Aggregation rules

- Coefficient and response never pooled into one transfer number.
- Primary interpretation: task-macro **median** plus the 20-task distribution.
- Also report: pooled transfer; task-macro mean; min/max; counts in \(\ge 95\%\), \([75,95)\), \(<75\%\); FIR/IIR macros; loose/tight; LP/HP/BP/BS; generator families.
- FIR/IIR/loose/tight/type macros are unweighted means of the per-task transfer rates in that stratum.
- Generator-family transfer uses the prospectively frozen `generator_id` field. Do not infer groups from results.
- Order/tap bins, if used, are fixed descriptive quantiles of the frozen H_VALID metadata (`n_taps` / IIR order). They are not inferential clusters and are not defined from rejection.
- H_INVALID: pooled over the 310 members; task-specific only where \(n>0\); FIR/IIR among represented tasks. **No 20-task macro FAR.**

## 7. Maintenance-analysis rules

Maintenance runs **only after** primary H_VALID transfer is irreversibly frozen and tagged `icassp-10of10-phase3d-b-primary-transfer-frozen`.

- \(V_t^+=V_t^{\mathrm{base}}\cup H_{t,\mathrm{VALID}}\). Invalid universe remains the frozen Phase-3B base invalids.
- Candidate references may come from \(V_t^+\).
- Use the **exact same** Phase-3B `solve_task` / set-cover/MILP family. Do not report a greedy catalog as \(K^\star\).
- Do **not** alter the already frozen Phase-3B \(K^\star\).
- Classify each expanded solve as `EXACT_OPTIMUM`, `CERTIFIED_BOUNDS`, or `UNDECIDED`.
- Suite-level median \(K^\star_+\) is reported only over tasks with exact optima, or clearly labeled if bounds are mixed.
- Growth: \(\Delta K_t=K_{t,+}^\star-K_{t,\mathrm{base}}^\star\), \(g_t=\Delta K_t/K_{t,\mathrm{base}}^\star\), \(\rho_t^+=K_{t,+}^\star/|V_t^+|\).
- Unavoidable prospective references: fix \(|R|=K_{t,+}^\star\), then \(M_t^\star=\min|R\cap H_{t,\mathrm{VALID}}|\). \(M^*=0\) means an optimal expanded catalog can still be built entirely from base valids; \(M^*>0\) means every minimum-size exact catalog needs at least \(M^*\) newly admitted realizations.
- Optional fixed-catalog repair: keep \(R_t^\star\) and find smallest \(A_t\subseteq H_{t,\mathrm{VALID}}\) such that \(R_t^\star\cup A_t\) exactly covers \(V_t^+\) while rejecting the frozen base invalids under one common threshold. \(J_t^\star=\min|A_t|\).
- Maintenance is a diagnostic, **not** a novel optimization method.

## Absolute locks

- Do not modify H_VALID, H_INVALID, challenge labels, original labels, tasks, \(S_t\), metrics, or Phase-3B catalogs.
- Do not generate additional implementations.
- Do not remove difficult cases or add new challenge cases.
- Do not retune thresholds on H_VALID or H_INVALID.
- Do not choose a different Phase-3B catalog after observing transfer.
- Do not add a new metric.
- Do not edit the manuscript or PDF.
- Do not synchronize public `main`.
- Do not move any existing tag.
- Reference rejection of an H_VALID member is **not** evidence of invalidity.

## Freeze order

1. This protocol + tag `icassp-10of10-phase3d-b-preunblind-lock`.
2. Frozen catalog identities.
3. Frozen thresholds.
4. Margin-zero diagnosis (no catalog distances).
5. Coefficient then response H_VALID transfer.
6. Tag `icassp-10of10-phase3d-b-primary-transfer-frozen`.
7. Only then H_INVALID, hierarchy (base-thresholded), generators, maintenance, novelty.

## Reproduction

`python -m experiments.icassp_10of10_hardening.phase3d_b.run_all`

Consumes the frozen Phase-3D-A challenge. Does not regenerate it. Does not overwrite this protocol lock.
