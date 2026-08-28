# PHASE 3D-A — Protocol lock

Phase 3D-A creates a **catalog-blind** prospective FIR/IIR challenge set. It does **not** score reference-catalog transfer. Phase 3D-B is not authorized by this lock.

> From this commit until `icassp-10of10-phase3d-a-challenge-frozen`, generation and holdout inclusion may depend only on frozen \(S_t\), task metadata, this locked schedule, generation success/failure, continuous certification, and exact duplicate detection. No candidate may be accepted or rejected using a reference distance.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `4f6d498ad26065962ebba80e8aa019dfbe8ec1c2` |
| git status at lock | clean |
| Phase-0 baseline | `icassp-pre-10of10-hardening-baseline` |
| Phase-1 complete | `icassp-10of10-phase1-complete` |
| Phase-2A complete | `icassp-10of10-phase2a-complete` |
| Phase-2B complete | `icassp-10of10-phase2b-complete` |
| Phase-3A complete | `icassp-10of10-phase3a-complete` |
| Phase-3B complete | `icassp-10of10-phase3b-complete` |
| Phase-3C complete | `icassp-10of10-phase3c-complete` / `4f6d498ad26065962ebba80e8aa019dfbe8ec1c2` |

Existing tags must not be moved.

## Authoritative hashes at lock

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |
| `data/icassp_10of10/feasible_probe.json` | `bad0223edec5b62ef72e05dd17c2a8eb135f1f0831d10b0dfdf4da314e0a6b10` |
| `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json` | `92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061` |
| `results/icassp_10of10_hardening/phase3b/headline.json` | `fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0` |
| `results/icassp_10of10_hardening/phase3c/leakage.json` | `d02fb07b073ed6f1fd6648fb0f57d130e6b29ebee286cca02fc5488f0c2f962f` |
| `reports/ICASSP_FINAL_10OF10/PHASE3C_LEAKAGE_AUDIT.md` | `8af8d2aae8dbca0e4dc0bed9fd97ca460fe95c93179551249d2a591ca92154ed` |

## Locks

- Do not edit the manuscript, PDF, title, abstract, frozen labels, tasks, masks, metrics, or Phase-0/1/2/3A/3B/3C outputs.
- Do not move existing tags.
- Do not compute distances to Phase-3B selected references, ambient centers, or canonical/best-observed identities for candidate selection.
- Do not run transfer, FRR/FAR, expanded \(K^\star\), or catalog maintenance.
- Do not increase the 48-attempt budget after seeing yields.
- Do not replace seeds.
- Do not synchronize public `main`.
- New outputs live only under `results/icassp_10of10_hardening/phase3d_a/` and `reports/ICASSP_FINAL_10OF10/PHASE3D_A_*`.

## Tasks

All 20 Suite N filter tasks. No new task.

FIR (16): `fir_{lp,hp,bp,bs}_{loose,tight}_{8k,16k}`.

IIR (4): `iir_{lp,hp}_{loose,tight}_8k`.

\(S_t\) has `order_constraint=free`. Existing scientific search ranges are odd FIR length \(\in[21,401]\) and IIR order \(\in[2,12]\). This protocol uses a **non-extreme** subset: FIR \(n\in\{21,25,31,37,43,49,55,61,71,81,91,101\}\); IIR order \(\in\{2,\ldots,10\}\) as listed below.

## Budget

Exactly 48 valid-candidate **attempts** per task, 12 per family.

Total attempts: \(20\times 48=960\) (FIR 768, IIR 192).

Every attempt is logged. Failed seeds are not rerun. The valid challenge size is the number of those 960 attempts that are continuously certified valid after exact deduplication.

## Seeds

For task \(t\), generator \(g\), attempt index \(a\in\{0,\ldots,11\}\):

```
material = PHASE3D_A|{task_id}|{generator_id}|{attempt_index}
digest   = SHA-256(material UTF-8)
seed_u64 = integer of digest[0:16] hex
```

Stored in `results/icassp_10of10_hardening/phase3d_a/seed_manifest.json` **before** candidate generation. No seed replacement.

## Generator families (locked)

### FIR — all four apply to all 16 FIR tasks

| ID | Route | Attempts |
|---|---|---|
| `F1_remez` | Parks–McClellan via `scipy.signal.remez` / `src.valid_designers.design_remez` | 12 |
| `F2_firls` | least-squares via `scipy.signal.firls` / `design_firls` | 12 |
| `F3_freqsamp` | independent frequency-sampling (`src.first_principles_fir.frequency_sampling`) | 12 |
| `F4_window` | even \(a\): `firwin2`; odd \(a\): Hamming windowed-sinc (`valid_first_principles.windowed_at`) | 12 |

No FIR family is `NOT_APPLICABLE` on Suite N. Fallback order if a future task were inapplicable (not used): F1→F2→F3→F4, redistribute that family's 12 slots in attempt-index order onto the next applicable family. Redistribution is **not** based on yield.

### IIR — all four apply to all 4 IIR (lp/hp) tasks

| ID | Route | Attempts |
|---|---|---|
| `I1_butter` | Butterworth `scipy.signal.butter` | 12 |
| `I2_cheby1` | Chebyshev I | 12 |
| `I3_cheby2` | Chebyshev II | 12 |
| `I4_ellip` | elliptic | 12 |

IIR band-pass/stop tasks do not exist in Suite N. Fallback order if needed: I1→I2→I3→I4.

## FIR parameter schedule (attempt \(a=0\ldots11\))

`FIR_N_GRID[a]` as above.

**F1.** `n = FIR_N_GRID[a]`. Weights `REMEZ_W2[a]` for lp/hp; `REMEZ_W3[a]` for bp/bs. Bands from frozen `remez_bands(S_t)`. `maxiter=100`.

**F2.** `n = FIR_N_GRID[a]`. `firls` bands/desired from frozen `firwin2_spec` / `firls_desired`. No weight tuning.

**F3.** `n = FIR_N_GRID[a]`. Designed (not \(S_t\)) transition inset: \(\alpha=\) `F3_EDGE_ALPHA[a]`. For each free transition \((L,R)\) between a pass edge and a stop edge, the designed interface is moved inward by \(\alpha\cdot(R-L)/2\) from each side, then passed to the existing `mag_*` masks. If the inset collapses the transition, fall back to the raw \(S_t\) edges. DC/Nyquist/mid-band normalization as in `freqsamp_at`.

**F4.** `n = FIR_N_GRID[a]`. If \(a\) even: `design_firwin2(task, n)`. If \(a\) odd: `windowed_at(task, n, default_cutoffs(task))` (Hamming sinc).

No parameter is a function of a catalog distance.

## IIR parameter schedule (attempt \(a=0\ldots11\))

`order = IIR_ORDER_GRID[a]`.

Designed cutoff: the single free-transition midpoint family is replaced by
\(\mathrm{fc}=L+\mathrm{IIR\_FC\_FRAC}[a]\cdot(R-L)\)
for the unique lp/hp free transition \((L,R)\).

Ripple (used only by I2/I4): `rp = IIR_RP_FRAC[a] * pass_rp_db(task)` with `pass_rp_db` the existing textbook helper (0.5 dB loose / 0.1 dB tight). This stays inside the allowed passband tolerance by construction of that helper.

Stop attenuation (used only by I3/I4): `rs = IIR_RS_FRAC[a] * stop_atten_db(task)` (at least the mask-implied attenuation; fractions \(\ge 1\) go beyond the required attenuation).

I1 ignores `rp`/`rs`. I2 ignores `rs`. I3 ignores `rp`.

## Labels

Every generator output starts as `CANDIDATE_UNCERTIFIED`.

Cheap 4096-point `check_specification` may **reject** obvious invalids (`GRID_SCREEN_FAIL`). It may **not** assign `VALID`.

Final `H_VALID` requires continuous certification:

- FIR: `src.continuous_certification.fir_power_polynomial.certify_fir` (Bernstein / rational squared-magnitude). If `UNDECIDED`, resolve with `certify_fir_sturm`. Still-undecided does **not** enter `H_VALID`.
- IIR: `certify_stability` with frozen `pole_radius_max=0.999`, then `certify_iir_magnitude` (\(P_B-C P_A\) Sturm). Both must be certified. `UNDECIDED` excluded.

## Exact duplicate rule

Remove exact duplicates only.

- FIR: `fir_sign_equivalent` after frozen canonicalize (magnitude-only sign flip is the same realization).
- IIR: `iir_same_tf` after `a0=1` canonicalize.

Compare against: original 412 valids; original mechanism invalids; Type-I probes; other prospective `H_VALID` / `H_INVALID` members.

Do **not** use a distance threshold. Near-duplicates remain.

Prior-science coefficient files may be loaded for identity only. Phase-3B `catalog_ids` / \(K^\star\) JSON must not be opened by generation.

## Invalid challenge

Do not dump all failed valid-design attempts into `H_INVALID`.

For each admitted `H_VALID` progenitor, exactly two mutations:

**M1 — coefficient perturbation.** Coefficient index \(i=\mathrm{seed\_u64}\bmod n_{\mathrm{coeff}}\) (FIR taps, or concatenated IIR `(b,a)` excluding `a[0]`). Sign \(s=+1\) if bit 16 of the SHA-256 digest is 0 else \(-1\). Scale \(\sigma=\|h\|_2\) (FIR) or \(\|(b,a)\|_2\) (IIR). Try ladder \(\varepsilon\in\{10^{-5},10^{-4},10^{-3},10^{-2}\}\) in that order: add \(s\cdot\varepsilon\cdot\sigma\) to coefficient \(i\). First continuously certified invalid/unstable wins. If none, `NO_CERTIFIED_INVALID_FROM_MUTATION`.

**M2 — structured DSP perturbation.** Same ladder.

- FIR: perturb the symmetric pair \((i, n-1-i)\) equally (Type-I-preserving if the progenitor is Type I); if \(i=n-1-i\), perturb the center tap only.
- IIR: scale every denominator coefficient except `a[0]` by \(1+s\cdot\varepsilon\) (pole-radius-directed).

Mutation uses progenitor coefficients, the locked seed/hash, and \(S_t\) certification only.

`H_INVALID` requires: progenitor in `H_VALID`; locked mutation; continuously certified invalid or strictly unstable; not an exact duplicate of any existing invalid.

Do not balance class sizes post hoc.

## Adequacy gate (descriptive; no top-up)

`ADEQUATE` only if: every task has \(\ge 5\) new continuous nonduplicate valids; \(|H_{\mathrm{VALID}}|\ge 200\); FIR valids \(\ge 160\); IIR valids \(\ge 20\); at least two families contribute valids on \(\ge 15/20\) tasks where two families apply; every task has \(\ge 5\) prospective invalids; \(|H_{\mathrm{INVALID}}|\ge 200\).

If any fail: freeze and report `PROSPECTIVE_CHALLENGE_INADEQUATE`. Do not add attempts.

## Forbidden opens during generation

Generation/certify/dedup/mutate modules must not open:

- `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json`
- other Phase-3B selected-catalog artifacts
- `phase3a/coefficient_ambient.json`, `response_ambient.json`, `hierarchy.json`
- `phase1/best_observed_reference.json`

An automated guard fails the run if those paths are opened.

## Reproduction

`python -m experiments.icassp_10of10_hardening.phase3d_a.run_all`

Deterministic from this lock + seed manifest. No timestamps in hash-critical artifacts.

## What this phase does not establish

Reference-oracle transfer has not been evaluated.
