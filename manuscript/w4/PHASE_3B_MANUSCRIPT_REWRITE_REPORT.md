# PHASE 3B — Manuscript Rewrite Report

**Status:** `READY_FOR_FINAL_REVIEW`

**Source of record:** `manuscript/w4/paper.tex`  
**Compiled PDF:** `manuscript/w4/paper.pdf`  
**Bibliography:** `manuscript/w4/refs.bib` (reused; no new entries)

No experiments were rerun. No frozen number, threshold, task definition, or label was changed.

---

## 1. Final title

**Beyond Reference Matching: Specification-Based Evaluation of Generated DSP Implementations**

Unchanged. Line-broken in `\title` for the SPS template only.

---

## 2. Abstract word count

| Count | Words |
|---|---:|
| Scientific abstract (excluding GitHub sentence) | **128** |
| Including the allowed GitHub sentence | **133** |

Target was 120–140. Structure matches the approved seven-part brief (problem → mask multiplicity → oracles → Suite N FRR → A/B/C → generated witness clause → realization-diagnostic close). Does not lead with 9/48, model names, or generated-code success rates.

---

## 3. Technical page count

**3.2 pages** (pages 1–3 plus the discussion/conclusion/ethics block at the top of page 4).

Safely under the 4-page technical target. Singleton contrast (RQ4) is present.

---

## 4. Total page count

**4 pages** (official `spconf` compile: `pdflatex` + `bibtex` + `pdflatex` ×2).

References occupy the remainder of page 4. A fifth references-only page is not required.

---

## 5. Figure count

**1** (`Fig. 1`, `figure*`).

Conceptual only: magnitude mask + realization space. Canonical \(h_r\), two valid occupants outside the \(\tau_R\)-ball, one invalid outside \(\mathcal{V}_t\). No LLM logos, pipeline, 416-dot swarm, or benchmark branding.

---

## 6. Table count

**4**

| Table | Content |
|---|---|
| 1 | Suite summary (S / N). Arm G listed as witness only; not pooled into constructed \(n\). |
| 2 | Reference rejection (S, N all / FIR / IIR / loose / tight), including \(\mathrm{FRR}_{\mathrm{ref}}^{\mathrm{any3}}\) and task-level 20/20. |
| 3 | Oracle A / B / C on Suite N; A / C on Suite S. No \(T\). |
| 4 | \(\tau_R\in\{0.01,0.05,0.10\}\) and canonical-order lock. No phase row. |

---

## 7. Old content removed

Deleted or demoted from the w3 existence-proof manuscript:

- Kendall \(\tau\) and coefficient–residual correlation claims
- Model-family comparison and model names in primary results
- Old occupancy Table I as the lead result
- Agreement-with-\((T)\) Table III
- 0/48 generated-code headline and success/failure framing
- Tone-probe result tables ( \(T\) retained as one sentence: same-mask check, not gold)
- Excessive chirp discussion
- Separate old RQ2 first-principles section
- Separate old one-mask tightening RQ
- Broad LLM survey / HumanEval-style background
- Generated-code occupancy as the paper’s scientific center

---

## 8. New content inserted

Full rewrite, not an incremental edit:

- Constructed-label evaluation-methodology narrative
- Formal \(R_{t,r}\) vs \(S_t\) / \(\mathcal{V}_t\) distinction
- Problem-formulation section (singleton vs non-unique)
- Oracle A / B / C definitions with checker independence
- Conceptual Figure 1
- Suite S (8 identities) vs Suite N (20 mask instances from one family)
- Construction protocol: library / first-principles / random-valid; admission \(S_t=1\); distance measured after admission
- Results organized as RQ1–RQ5
- Four new tables aligned to Phase 2C table-ready blocks
- Compact discussion (conditional argument; mask-family scope; Arm G as witness)
- One-paragraph conclusion with no new result

---

## 9. Headline numbers vs frozen Phase 2B / 2C

Checked against `project_a_public_release/PHASE_2B_VALID_GENERATION_REPORT.md` and `PHASE_2C_EVALUATION_REPORT.md`.

| Claim | Frozen | Manuscript | Match |
|---|---|---|---|
| Suite S instances / valids / invalids | 8 / 12 / 16 | 8 / 12 / 16 | yes |
| Suite S \(\mathrm{FRR}_{\mathrm{ref}}\) | 0/12 | 0/12 | yes |
| Suite S A, C FRR / FAR | 0 / 0 | 0 / 0 | yes |
| Suite N instances | 20 (16 FIR + 4 IIR) | 20 (16 FIR + 4 IIR) | yes |
| Constructed valids | 416 = 92 + 24 + 300 | 416 = 92 + 24 + 300 | yes |
| Constructed invalids | 144 | 144 | yes |
| \(\tau_R\) | 0.05 | 0.05 | yes |
| \(\mathrm{FRR}_{\mathrm{ref}}\) | 374/416 = 0.899 | 374/416 = 0.899 | yes |
| FIR | 302/340 = 0.888 | 302/340 = 0.888 | yes |
| IIR | 72/76 = 0.947 | 72/76 = 0.947 | yes |
| loose | 183/210 = 0.871 | 183/210 = 0.871 | yes |
| tight | 191/206 = 0.927 | 191/206 = 0.927 | yes |
| task-level | 20/20 | 20/20 | yes |
| any3 | 346/416 = 0.832 | 346/416 = 0.832 | yes |
| any3 FIR / IIR / loose / tight | 274/340, 72/76, 177/210, 169/206 | same | yes |
| Oracle A | FRR 0.899, FAR 0 | 0.899 / 0 | yes |
| Oracle B | FRR 0.067, FAR 0 | 0.067 / 0 | yes |
| Oracle C | FRR 0, FAR 0 | 0 / 0 | yes |
| \(\tau_R=0.01/0.05/0.10\) | 0.933 / 0.899 / 0.873 | same (388/416, 374/416, 363/416) | yes |
| order lock | 25/67 = 0.373 | 25/67 = 0.373 | yes |
| Oracle B fallback | 6 instances, all-library pairwise max | stated in Discussion | yes |
| All constructed FIR are Type I | 340/340 | stated; no phase ablation row | yes |
| Arm G | 4 tasks; 48 planned; 20 executed; 14 eligible; 9 with \(S_t=1\); all 9 have \(R_{t,r}=0\); 4/4 | same | yes |
| Diversity: every-task median \(d_{\mathrm{coeff}}\ge 1.0\); band RMSE \(\sim 10^{-3}\) FIR / \(10^{-2}\) IIR | Phase 2B/2C tables | RQ2 prose | yes |

---

## 10. Citation audit

No citations invented. All `\cite` keys exist in the inherited `refs.bib`.

| Cluster | Keys used | Verdict |
|---|---|---|
| Classical filter approximation / multiplicity | `oppenheim2010dsp`, `proakis2007dsp`, `mitra2011dsp`, `rabiner1975theory`, `kaiser1974window`, `harris1978windows`, `rabiner1970freqsamp`, `parks1972chebyshev`, `mcclellan1973computer`, `rabiner1975fir`, `butterworth1930`, `constantinides1970`, `jackson1996filters`, `antoniou2006filters`, `herrmann1973linear` | Support mask/feasible-set and classical designers. |
| Golden / reference evaluation | `huuhtanen2015dsp`, `virtanen2020scipy` | DSP/numerical reference comparison; SciPy as library occupant. |
| Generated-code evaluation | `chen2021codex`, `liu2023evalplus` | Framing only. No model leaderboard. |

Unused inherited entry (not cited, not fabricated): `vaidyanathan1993multirate`.

Claim control:

- No “first”, no literature-gap inflation.
- “EvalPlus-style suites do not address non-unique DSP specifications” is scoped to unique-output unit tests, not a survey claim.
- No “universal correctness criterion”.
- No “LLMs often…”.

`herrmann1973linear` is an inherited cite key; the bib year is 1971 (CT-18), which is the published year. Not altered.

---

## 11. Notation audit

| Symbol | Use | Consistent? |
|---|---|---|
| \(t\), \(h\) | task, implementation | yes |
| \(S_t(h)\), \(\mathcal{V}_t=\{h:S_t(h)=1\}\) | specification membership / feasible set | yes |
| \(h_r\in\mathcal{V}_t\) | canonical reference | yes |
| \(R_{t,r}(h)\), \(\tau_R=0.05\) | Oracle A / realization diagnostic | yes |
| \(\lvert\mathcal{V}_t\rvert=1\) vs \(>1\) | singleton vs non-unique | yes |
| Oracle B | spec-band \(\lvert H\rvert\) vs \(h_r\); not gold | yes |
| Oracle C | \(S_t\); FIR residual \(10^{-6}\); IIR residual \(10^{-3}\) + pole \(<0.999\) | yes |
| \(T\) | one sentence; not in FAR/FRR tables | yes |
| \(\mathrm{FRR}_{\mathrm{ref}}\), \(\mathrm{FRR}_{\mathrm{ref}}^{\mathrm{any3}}\) | defined in protocol | yes |

Suite N is called “20 specification instances from a common magnitude-mask family,” not 20 unrelated DSP tasks.

---

## 12. Overfull-box audit

Final `paper.log`:

- **Overfull `\hbox`:** none
- **Undefined references / citations:** none
- **Underfull `\hbox`:** one, GitHub URL in the abstract (typical URL break; not an overfull)

No manual negative `\vspace` compression. Ethics uses a 4 pt gap only.

---

## 13. Unsupported claims removed

Removed or never introduced:

- Prevalence of LLM DSP errors
- Model ranking / Kendall \(\tau\)
- \(T\) as gold
- Phase free vs Type-I as an independent ablation
- “90% of DSP implementations” / “90% of LLM outputs”
- “Universal correctness criterion”
- Random-valid search as disagreement maximization
- Pooling Arm G into constructed \(n\)
- Filter-design or verification-theory novelty

Oracle C is described as matching the admission rule against frozen constructed labels, not as an independently “validated” gold standard.

---

## 14. Strongest remaining scientific weakness

**Constructed labels make Oracle C’s FRR = FAR = 0 a consistency check, not an external validation.** The primary empirical result (reference FRR on a frozen valid set) is therefore only as strong as the claim that the constructed occupants are the right universe in which to measure realization disagreement. Random-valid occupants are 300/416 of that universe; Arm G remains an incomplete existence witness (20/48 executed). The paper states these limits, but a reviewer can still ask for an independently labeled or human-admitted valid set.

---

## 15. Submission readiness

**READY_FOR_FINAL_REVIEW**

Not BLOCKED: the rewrite matches the frozen Phase 3A architecture, the frozen Phase 2B/2C numbers, the citation whitelist, and the ICASSP 4-page compile.

Recommended final-review items (presentation only; no science change required):

- Table 1 currently interrupts a protocol sentence on page 2 (standard float).
- Page 4 mixes the tail of Discussion with the full reference list.
- Abstract GitHub URL produces an underfull line.

---

## Compile command

```
cd manuscript/w4
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Output: 4 pages, 1 figure, 4 tables, 19 cited works.
