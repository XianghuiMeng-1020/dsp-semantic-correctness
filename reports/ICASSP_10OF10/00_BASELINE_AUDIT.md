# 00 — Scientific baseline audit (frozen)

**Status:** FROZEN before any scientific-code change.  
**Purpose:** Record the exact pre-strengthening state of the authoritative repository.  
**Rule:** Later work must not silently rewrite this baseline. New numbers belong in later reports.

This audit does **not** authorize a manuscript rewrite.

---

## 1. Repository identity

| Field | Value |
|---|---|
| Authoritative repository | `F:\ICASSP\project_a_public_release` |
| Public remote | `https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git` |
| Current commit | `a776d3c3f75f1343ed1769a444189f4a939f9a8f` |
| Current commit (short) | `a776d3c` |
| Commit message | `Add frozen Phase 2 suites and the final ICASSP manuscript package.` |
| Current branch | `main` |
| Working-tree state | clean (`git status --short` empty) |
| Tags | none |
| Local branches besides `main` | none |
| Remote branches | `origin/main` only |
| Strengthening branch (this pass) | **not created at freeze time** |

Non-authoritative workspaces exist (`A_dsp_code_semantic_testing`, `A_dsp_code_semantic_testing_r9`) and are **not** the scientific source of truth for this pass.

---

## 2. Manuscript and PDF

| Field | Path / value |
|---|---|
| Authoritative manuscript | `manuscript/w4/paper.tex` |
| Bibliography | `manuscript/w4/refs.bib` |
| Compiled PDF | `manuscript/w4/paper.pdf` |
| Submission bundle | `manuscript/w4/submission/` |
| PDF page count | **5** (4 technical pages + page 5 references only) |
| Title | Beyond Reference Matching: Specification-Based Correctness Evaluation for DSP Implementations |
| Current story center | specification-set membership vs reference matching when \(\lvert\mathcal{V}_t\rvert>1\) |
| Manuscript rewrite in this pass | **forbidden** until `13_SCIENTIFIC_GATE_DECISION.md` is `STRONG_GO_FOR_MANUSCRIPT_REWRITE` |

`manuscript/w3` is historical. Do not treat it as current.

---

## 3. Experiment entry points (baseline)

### Phase 2 constructed-label study (current paper evidence)

| Role | Path |
|---|---|
| Suite S registry | `registry/suite_s.json` |
| Suite N registry | `registry/suite_n.json` |
| Construction / admission checker (Oracle C) | `src/spec_checker.py` |
| Oracle A / B | `src/oracles.py` |
| Distances | `src/valid_metrics.py` |
| Library / random designers | `src/valid_designers.py` |
| First-principles FIR | `src/first_principles_fir.py`, `src/valid_first_principles.py` |
| Mutants | `src/mutants.py` |
| Mask geometry | `src/filter_geom.py`, `src/mask_rules.py` |
| Suite S fixtures | `src/suite_s_fixtures.py` |
| Valid generation | `scripts/generate_valid_occupants.py` |
| Invalid generation | `scripts/generate_invalids.py` |
| Evaluation (Tables I–IV numbers) | `scripts/evaluate_phase2c.py` |
| Numeric source of headline tables | `data/phase2c/evaluation.json` |
| Phase reports | `PHASE_2A_REGISTRY_CHECKER_REPORT.md`, `PHASE_2B_VALID_GENERATION_REPORT.md`, `PHASE_2C_EVALUATION_REPORT.md` |

### Historical / generated-code arm (witness only)

| Role | Path |
|---|---|
| Frozen generated implementations | `data/arm_n_generations.json` |
| Frozen Oracle A distances | `data/arm_n_oracle_a_frozen.json` |
| Historical floors | `data/arm_n_thresholds.json` |
| Historical contracts | `src/contracts_arm_n.py` |
| Reproduction | `scripts/reproduce_all.py`, `scripts/reproduce_oracles.py` |

README still documents the **old** Arm-N generated-code framing (48/20/14/9). The current manuscript treats that arm as a witness only. This mismatch is a baseline limitation, not a number change.

---

## 4. Constructed data inventory

### Specifications / tasks

| Quantity | Count | Notes |
|---|---:|---|
| Total registered specifications | 28 | 8 Suite S + 20 Suite N |
| Singleton / unique-map tasks (Suite S) | 8 | identity maps; reference matching is expected to coincide with \(S_t\) |
| Non-unique magnitude-mask tasks (Suite N) | 20 | one filter-mask family, not 20 unrelated DSP domains |
| Suite N FIR | 16 | LP/HP/BP/BS × {8,16} kHz × {loose,tight} |
| Suite N IIR | 4 | LP/HP × {loose,tight} at 8 kHz only |

Tight masks are mechanical: pass ripple ×1/5 about 1; stop ceiling ×1/5; stop edge moved halfway toward the facing pass. 16 kHz edges = 8 kHz × 2.

### Constructed occupants

| Set | Count | Admission rule |
|---|---:|---|
| Suite N valid-by-construction | **416** | construction checker \(S_t=1\) |
| Suite N invalid-by-construction | **144** | construction checker \(S_t=0\) |
| Suite S valids (canonical + alternate) | **12** | identity fixtures |
| Suite S mutants | **16** | predefined identity mutants |

### Suite N valid breakdown

| Source | Count |
|---|---:|
| library | 92 |
| first-principles | 24 |
| random-valid | 300 |
| FIR valids | 340 |
| IIR valids | 76 |
| loose valids | 210 |
| tight valids | 206 |

Random-valid seed: `20260826`. Search objective was \(S_t=1\) only. Distance to \(h_r\) was measured **after** admission.

### Suite N invalid breakdown (mechanism mutants)

| Mechanism | n |
|---|---:|
| M1 band swap | 20 |
| M2 cutoff into constrained band | 20 |
| M3 order too short | 20 |
| M4 unstable pole (IIR only) | 4 |
| M5 Nyquist as 1 Hz | 20 |
| M6 pass gain collapse | 20 |
| M7 wrong sampling rate | 20 |
| M8 type mismatch | 20 |
| **Total** | **144** |

### Same-order baseline (existing ablation, not a confirmatory study)

| Quantity | Value |
|---|---|
| Occupants with length/order equal to canonical \(h_r\) | 67 |
| \(\mathrm{FRR}_{\mathrm{ref}}\) on that subset at \(\tau_R=0.05\) | 25/67 = 0.373 |
| Scientific limit | this is whichever existing occupants happened to match order; not a same-structure probe |

All 340 constructed FIR occupants are Type I. The “phase Type-I” ablation is therefore identical to the FIR slice.

---

## 5. Current Oracle A / B / C definitions

### Oracle A — coefficient reference match

\[
R_{t,r}(h)=1 \iff d_{\mathrm{coeff}}(h,h_r)\le \tau_R
\]

- \(d_{\mathrm{coeff}}\): **min-length relative \(\ell_2\)** on truncated coefficient vectors (`src/valid_metrics.py::d_coeff`).
- FIR: compare `h[:n]` vs `h_r[:n]` with `n=min(len(h),len(h_r))`.
- IIR: concatenate `(b,a)` and truncate to the shorter concatenated length.
- Default operating point: \(\tau_R=0.05\).
- Sensitivity grid (not a sweep): \(\tau_R\in\{0.01,0.05,0.10\}\).
- Canonical \(h_r\): shortest-odd Hamming `firwin` (FIR) or lowest-order `butter` (IIR) that meets construction \(S_t\).

This truncation is a representation artifact. It is **not** a confirmatory metric for the strengthening pass.

### Oracle B — spec-band magnitude RMSE vs \(h_r\)

- Distance: RMSE of \(\lvert H\rvert-\lvert H_r\rvert\) on the constrained pass+stop bands, 4096-point `freqz`.
- Threshold: max same-order **library-pair** band RMSE \(+10^{-8}\).
- Fallback: if a task has no same-order library pair, use the all-library pairwise max \(+10^{-8}\).
- Six Suite N tasks used the fallback.

Oracle B is a response-space reference oracle, still relative to one (or pairwise library) realization, not specification membership.

### Oracle C — specification membership

- Implementation: `src/spec_checker.py::check_specification`.
- Rule: \(C(h)=1\) iff the construction checker returns `pass`.
- On constructed labels this is **circular**: occupants were admitted by the same predicate.

### Tone battery \(T\)

Historical Arm N only. Same-mask consistency probe. **Not gold.**

---

## 6. Current thresholds and numerical floors

| Quantity | Value | Role |
|---|---|---|
| \(\tau_R\) default | 0.05 | Oracle A / \(\mathrm{FRR}_{\mathrm{ref}}\) headline |
| \(\tau_R\) grid | 0.01, 0.05, 0.10 | sensitivity only |
| FIR residual floor | \(10^{-6}\) | construction \(S_t\) |
| IIR residual floor | \(10^{-3}\) | construction \(S_t\) |
| Pole-radius max | 0.999 | IIR stability in construction checker |
| Construction `freqz` points | **4096** | `FREQZ_N` in `spec_checker.py` and `valid_metrics.py` |
| Near-duplicate filter | \(d_{\mathrm{coeff}}\le 0.01\) and full-grid RMSE \(\le 10^{-3}\) | valid-set dedup, not an oracle |
| Oracle B additive | \(10^{-8}\) | pairwise-max offset |

Band residual in the construction checker is a **normalized** violation: `max(below, above) / max(hi-lo, 1e-6)`, then compared to the residual floor. Pass vs stop is classified by `lo >= 0.5`.

---

## 7. Exact 4096-point validity mechanism (construction checker)

File: `src/spec_checker.py`.

1. Unpack `b` (and `a` if IIR).
2. `scipy.signal.freqz(b[, a], worN=4096, fs=fs)`.
3. Magnitude `abs(H)` on that discrete grid only.
4. For each registered pass/stop interval, restrict to grid bins with `f0 <= w <= f1`.
5. If a band contains no grid bin, both pass and stop errors are set to 1.0 (fail).
6. Per-bin violation = amount outside `[lo, hi]`, divided by `max(hi-lo, 1e-6)`.
7. Band error = max normalized violation on that band; aggregated into passband vs stopband by `lo >= 0.5`.
8. Non-finite coefficients force pass/stop errors to at least 1.0.
9. IIR stability: `pollz` via `tf2zpk`; fail if any `|p| >= pole_radius_max` (default 0.999).
10. Accept iff `pass_err <= floor` and `stop_err <= floor` and `stab == 0`.

**Not certified:** continuous-frequency extrema, transition-band exclusions beyond “not scored”, SOS evaluation, order/length/normalization as hard constraints (Suite N `order_constraint` is `free`; `phase_requirement` is `none`).

This checker is both the **search/admission oracle** and **Oracle C**. That identity is the circularity to be removed.

---

## 8. All current headline results (do not preserve for narrative convenience)

Source: `data/phase2c/evaluation.json` and `PHASE_2C_EVALUATION_REPORT.md`.

### Reference rejection at \(\tau_R=0.05\)

| Slice | n | \(\mathrm{FRR}_{\mathrm{ref}}\) | any3 |
|---|---:|---|---|
| Suite S | 12 | 0/12 = 0.000 | — |
| Suite N all | 416 | **374/416 = 0.899** | **346/416 = 0.832** |
| N FIR | 340 | 302/340 = 0.888 | 274/340 = 0.806 |
| N IIR | 76 | 72/76 = 0.947 | 72/76 = 0.947 |
| N loose | 210 | 183/210 = 0.871 | 177/210 = 0.843 |
| N tight | 206 | 191/206 = 0.927 | 169/206 = 0.820 |
| Task-level disagreement | 20 | **20/20** | — |

\(\mathrm{FRR}_{\mathrm{ref}}^{\mathrm{any3}}\): rejected only if \(d_{\mathrm{coeff}}>\tau_R\) versus every available library occupant among `firwin` / `remez` / `firls` (FIR) or the IIR library set. This is the current **best-of-three / multi-library** number.

### Oracle table vs constructed labels (Suite N: 416 valid + 144 invalid)

| Oracle | FRR | FAR |
|---|---|---|
| A | 374/416 = 0.899 | 0/144 = 0.000 |
| B | 28/416 = 0.067 | 0/144 = 0.000 |
| C | 0/416 = 0.000 | 0/144 = 0.000 |

Suite S (12 valid + 16 invalid): Oracle A and C both FRR = FAR = 0. Oracle B is undefined (not a filter mask).

### Threshold sensitivity (Oracle A FRR on 416 valids)

| \(\tau_R\) | FRR |
|---|---|
| 0.01 | 388/416 = 0.933 |
| 0.05 | 374/416 = 0.899 |
| 0.10 | 363/416 = 0.873 |

### Canonical-order lock

25/67 = 0.373 at \(\tau_R=0.05\).

### Generated-code witness (Arm G / historical Arm N)

Manuscript / Phase 3 reports (not recomputed in this freeze):

| Quantity | Value |
|---|---|
| Tasks | 4 original loose 8 kHz masks |
| Planned draws | 48 |
| Executed | 20 |
| Eligible | 14 |
| Specification-valid | 9 |
| Those 9 with \(R_{t,r}=0\) | **9** |
| Tasks with such a witness | 4/4 |

This is an existence witness, not a model benchmark. Frozen code lives in `data/arm_n_generations.json`. Model generation is not shipped.

---

## 9. Current known limitations (baseline)

1. **Oracle C circularity.** Constructed labels are defined by the same 4096-point checker later scored as Oracle C. C’s zeros are consistency, not external validation.
2. **Discrete-frequency certification only.** 4096-point `freqz` does not certify continuous-band extrema.
3. **Min-length coefficient truncation.** Unequal-order FIR/IIR comparisons are not transfer-function canonical.
4. **No IIR \(a_0=1\) canonicalization** before coefficient distance.
5. **Same-order result is an opportunistic subset** (67 occupants), not a same-structure feasible-set study.
6. **Invalids are easy mechanism mutants**, not near-boundary specification violations.
7. **Headline FRR depends on \(\tau_R=0.05\)** (sensitivity exists but is not a full separability analysis).
8. **Single canonical reference** per task (`firwin_hamming` or `butter`). any3 is a limited robustness check, not a full reference-choice or \(K\)-reference study.
9. **Statistical unit is mostly occupant-pooled** (374/416). Task-level 20/20 is reported, but there is no task-cluster bootstrap, macro-FRR, or IQR.
10. **Random-valid occupants are 300/416.** The pooled rate is sensitive to how many random samples were kept.
11. **Suite N is one magnitude-mask family**, not a broad DSP-domain sample.
12. **All constructed FIR are Type I.** Phase-free vs Type-I is not an independent ablation.
13. **Oracle B FAR = 0** may reflect easy invalids rather than a strong response-space oracle.
14. **No independent verifier, no separability gap \(G_r\), no \(D_V/D_I\).**
15. **Generated witness is incomplete** (20/48 executed) and uses the old checker / old task IDs.
16. **README still leads with the old generated-code RQ framing.**
17. **The observation “different filters can satisfy the same mask” is too weak** as a scientific thesis for an expert filter-design reviewer.

---

## 10. What this freeze does *not* change

- No scientific source file was edited before this document was written.
- No occupant label was changed.
- No threshold was retuned.
- No manuscript text was rewritten.
- No previous tag or branch was deleted (none existed to delete).

The strengthening branch `research/icassp-spec-oracle-10of10` is created **after** this file is recorded.
