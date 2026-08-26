# PHASE 3D — Final Submission Package Audit

**Recommendation:** `SUBMIT`

Scientific experiments remain frozen. No numbers, thresholds, tasks, or generated examples were changed.

---

## 1. Final title

**Beyond Reference Matching: Specification-Based Correctness Evaluation for DSP Implementations**

Title B selected.

| Criterion | Title A (Generated DSP Implementations) | Title B (Correctness Evaluation for DSP Implementations) |
|---|---|---|
| Scientific accuracy | Over-weights the 9-occupant witness | Matches the constructed-label study |
| Reviewer expectation | LLM / code-generation reviewers | Filter / SPTM methodology reviewers |
| ICASSP fit | Sideways into ML-for-SP | Theory & Methods |
| Wrong-pool risk | High | Lower |
| Abstract/contribution consistency | Title promised generation quality | Title matches scoring-rule contribution |

Abstract opening changed from “generated DSP code” to “DSP implementations.” The generated-code sentence remains a witness. Keywords: `correctness evaluation` replaces `generated implementations`.

---

## 2. Final author block status

**Complete. Not blocked.**

- Xianghui Meng\(^1\)
- Jionghao Lin\(^{1,2,*}\) (corresponding: `jionghao@hku.hk`)
- \(^1\) The University of Hong Kong
- \(^2\) Carnegie Mellon University
- Contact email: `margretmeng1020@gmail.com`

No “Anonymous Author,” no TODO, no double-blind leftover. Matches single-anonymous ICASSP 2027 policy (reviewers know authors). Metadata was not invented.

---

## 3. Final technical page count

**4** (title through Conclusion and the ethics statement).

---

## 4. Total page count

**5** (letter, 612 × 792 pt).

---

## 5. Page-5 compliance

**PASS.**

Page 5 contains only bibliography entries [17]–[19]. No results, equations, figures, tables, or methods.

Official template (`official_template/Template.tex`): “An additional final page … must contain only references.” Ethics/compliance sits on page 4, before References.

Residual cosmetic: page 5 is short (three leftover refs). `flushend` was added to balance last-page columns; overflow is still left-column-first. Not a compliance fail.

---

## 6. Figure count and visual verdict

**1 figure. PASS after font bump.**

TikZ labels raised from `\scriptsize` to `\footnotesize` (≥ 9 pt, official minimum). Caption states two spaces; panel (b) is labeled schematic; \(\mathcal{V}_t\) is not claimed as a Euclidean ball. Invalid occupant is a distinct red marker. No clipped labels at 100%. Figure first mentioned on p. 2, placed as `figure*` on p. 3 (standard).

---

## 7. Table count and visual verdict

**4 tables. PASS.**

All use `\footnotesize` (9 pt), not `\tiny`. Denominators explicit. Arm G not pooled into constructed \(n\).

- Table 3 caption: C zeros = label consistency, not independent validation.
- Table 4 caption: \(\tau_R\) rows use 416; order-lock uses 67.

---

## 8. Citation audit

**PASS for the compiled PDF.**

- 19 cited works; all exist in `refs.bib`.
- Compiled `.bbl` contains only cited entries.
- Inherited unused key `vaidyanathan1993multirate` remains in `refs.bib` but is **not** in the PDF bibliography.
- Classic DSP cites support mask/designer claims only.
- Huuhtanen supports golden-reference testing; SciPy supports the library occupant; Chen/Liu support generated-code protocol only.
- No placeholder DOI, no malformed URL, no duplicates.
- `herrmann1973linear` is a cite key; published year in the bib is 1971 (CT-18). Not altered.
- Liu et al. (NeurIPS 2023) has no page range in the inherited bib; not invented.

---

## 9. Notation / number audit

**PASS. All frozen.**

| Quantity | Manuscript |
|---|---|
| N \(\mathrm{FRR}_{\mathrm{ref}}\) | 374/416 = 0.899 |
| FIR / IIR | 302/340 = 0.888 / 72/76 = 0.947 |
| Loose / tight | 183/210 = 0.871 / 191/206 = 0.927 |
| any3 | 346/416 = 0.832 |
| S | 0/12 |
| Oracle B FRR | 0.067 |
| Order lock | 25/67 = 0.373 |
| Witness | 9 occupants, 4/4 original instances |

---

## 10. Final recommended ICASSP category

Official CFP terminology only (no invented EDICS code; the April 2026 Unified EDICS spreadsheet is not in this repo).

- **Primary:** Signal Processing Theory & Methods  
  (CFP topic; SPTM TC). The object of study is a correctness criterion for filter-mask specifications.
- **Secondary:** Applied Signal Processing Systems  
  if a second track is required (implementation / checker, not a new filter algorithm).
- **Avoid:** Machine Learning and Generative AI  
  That track would send the paper to the wrong reviewer pool.

---

## 11. Final PDF path

`manuscript/w4/paper.pdf`  
(also copied to `manuscript/w4/submission/paper.pdf`)

---

## 12. Final submission-directory path

`manuscript/w4/submission/`

| File | Role |
|---|---|
| `paper.pdf` | CMS upload |
| `paper.tex` | Source |
| `refs.bib` | Bibliography |
| `paper.bbl` | Compiled refs |
| `spconf.sty` | Official SPS style |
| `IEEEbib.bst` | Official IEEE bib style |
| `README.txt` | Compile + track note |

No experimental data, no Phase 3A–3C reports, no `w1`/`w3`/`final_polished_submission` variants. Those remain in the research tree and were not deleted.

Figure asset: none (TikZ inline).

---

## 13. Strongest remaining scientific weakness

Constructed labels make Oracle C’s zeros a consistency check. The primary FRR is a property of this frozen constructed universe.

---

## 14. Strongest remaining reviewer risk

A traditional DSP reviewer can still say the paper measures a classical feasible-set fact. Title B reduces the ML-reviewer mismatch; it does not remove the “textbook DSP” attack.

---

## 15. Final recommendation

**SUBMIT**

Not `BLOCKED`. Author metadata is complete. Format matches the in-repo SPS template: letter paper, two-column `spconf`, 4 technical pages, page 5 references only, named authors, no overfull boxes.

### Format notes (non-blocking)

| Item | Status |
|---|---|
| Template | `article` + `spconf.sty` (same as `official_template/`) |
| Paper size | letter 8.5 × 11 in |
| Negative vspace | only `4pt` before ethics |
| `\resizebox` | none |
| `\tiny` tables | none |
| Altered margins / line spacing | none |
| Extra packages | `tikz`, `amssymb`, `hyperref` (template also uses hyperref), `flushend` (last-page balance) |
| Underfull hbox | GitHub URL in abstract |

### PDF forensic summary

| Page | Verdict |
|---|---|
| 1 | Title B; authors present; abstract/keywords aligned; intro starts cleanly |
| 2 | Eq. (2) in column; Table 1 at column top; no overflow |
| 3 | Fig. 1 + Tables 2–3 readable; RQ2–RQ5 complete |
| 4 | Table 4 + discussion + conclusion + ethics; refs begin |
| 5 | References only |

### Reviewer simulation (final PDF)

**R1 Traditional DSP** — score 3/5. Positive: conditional Suite S argument. Weakness: “textbook multiplicity.” Title B sets a methods expectation, not a new design claim.

**R2 SP methodology** — score 4/5. Positive: circularity of C is explicit; A/B are the informative contrast. Weakness: constructed universe. Title B matches this reviewer.

**R3 Generated-code / ML** — score 3/5. Positive: witness, not a leaderboard. Weakness: almost all \(n\) is constructed. Title B now tells this reviewer they are not the primary audience.

**PI:** Submit under **Signal Processing Theory & Methods**. Do not run new experiments.
