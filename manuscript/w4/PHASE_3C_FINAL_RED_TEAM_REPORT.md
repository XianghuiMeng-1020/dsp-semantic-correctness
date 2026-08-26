# PHASE 3C — Final Scientific Red-Team and Claim Audit

**Manuscript:** `manuscript/w4/paper.tex`  
**Compiled PDF:** `manuscript/w4/paper.pdf`  
**Recommendation:** `SUBMISSION_READY`

No experiments were rerun. No frozen number, threshold, task, or label was changed.

---

## 1. Scientific corrections made

Text-only repairs. All headline quantities unchanged.

| Location | Repair |
|---|---|
| Abstract | “often treated” → “commonly used”; C’s zeros now “restate the admission rule”; “these non-unique specifications”; generated event “among existing” occupants. |
| Intro, related work | Dropped “typically” + SciPy-as-testing-cite. “Inherited… those suites do not address” → “A standard generated-code protocol uses unique-output unit tests; that protocol does not score a non-unique DSP mask.” |
| Intro, contributions | “We formalize” → “We distinguish … as scoring rules.” Consequence scoped to the constructed suites. |
| Intro, singleton | \(\lvert\mathcal{V}_t\rvert=1\) → “effectively a singleton under the declared scoring tolerance.” |
| Formulation | Singleton / non-unique defined operationally, not as a literal cardinality of a continuum. |
| Method | Oracle C “implements the same predicate \(S_t\) used to admit constructed labels; it is the membership checker, not an external labeler.” |
| Fig. 1 caption / panel (b) | Two spaces stated; \(\mathcal{V}_t\) region declared schematic, not a Euclidean ball in the \(\tau_R\) metric. |
| Protocol | Near-\(h_r\) valids retained; dedup does not maximize distance; mutants are mechanism-based contract violations, not a natural-error sample; constructed occupants score oracles, Arm G is only a witness. |
| Table 2 caption | Universe = constructed-valid occupants; task disagreement uses contract membership, not “C accepts” as gold. |
| Table 3 caption | Contract-defined universe; C zeros = label consistency, not independent validation; informative contrast is A and B. |
| Table 4 caption | \(\tau_R\) rows = all 416; order-lock = 67-occupant subset. |
| RQ2 | Order result reported on the restricted \(n=67\) subset, not as a drop on the same population. |
| RQ3 | C = implementation consistency; informative comparison is A/B on the same contract-valid set; B can agree with C while asking a different question. |
| RQ5 | Removed 20/14 counts that invited a 9/14 rate. Existence wording only. |
| Discussion | Tight-mask wording = “did not eliminate the disagreement”; order subset qualified; C consistency restated; A/B are the substantive comparison. |

---

## 2. Claims removed or weakened

| Removed / weakened | Why |
|---|---|
| “DSP and numerical testing typically compare … golden reference” + SciPy cite | Two-cite “typically” overclaimed; SciPy is a library paper, not a testing-practice paper. |
| “Generated-code evaluation inherited unique-output unit tests; those suites do not address non-unique DSP specifications” | Field-wide inheritance / gap claim not supported by one paper. |
| “We formalize …” as a theory-style contribution | Risked sounding like DSP-theory novelty. |
| Literal \(\lvert\mathcal{V}_t\rvert=1\) | Over-literal for numerical equivalence classes. |
| Abstract C FRR/FAR = 0 as if validated | Circularity. |
| “drops FRR from 0.899 to 0.373” without subset \(n\) | Unequal populations. |
| “Tightening the masks does not remove that multiplicity” | Multiplicity is classical; the datum is disagreement on these frozen masks. |
| RQ5 “20 executed, 14 software-eligible” | Invites 9/14 prevalence. |
| “Oracle C accepts” in Table 2 caption | Implied C is an independent gold. |

No Category E claims remain in the final text.

---

## 3. Circularity audit verdict

**PASS after repair.**

Allowed argument, now stated in Method, Table 3, RQ3, and Discussion:

> The constructed universe is defined by the frozen contract. Oracle C implements \(S_t\). Its zero FRR/FAR is implementation consistency, not external validation. The informative comparison is that A and B reject subsets of the same contract-valid set.

Forbidden argument is not present:

> Labels are defined by \(S_t\); C computes \(S_t\); therefore C is validated.

Table 3 is retained with an explicit epistemic caption.

---

## 4. Selection-bias audit verdict

**PASS after repair.**

The manuscript now states all required facts:

- admission by \(S_t=1\) only
- distance to \(h_r\) measured after admission
- random-valid search does not maximize disagreement
- near-\(h_r\) valids retained
- deduplication does not maximize distance
- library and first-principles sources independently occupy \(\mathcal{V}_t\)

Remaining reviewer residual (not a wording defect): 300/416 occupants are random-valid, so the FRR is still a property of this constructed universe.

---

## 5. Generated-witness audit verdict

**PASS after repair.**

RQ5 reports nine existing eligible occupants with \(S_t=1\) and \(R_{t,r}=0\) on 4/4 original masks. No model names, no Kendall \(\tau\), no ranking, no 9/14 or 64%. Protocol keeps “48 planned draws” as scope only. Arm G is excluded from constructed \(n\).

---

## 6. Citation audit verdict

**PASS after repair.**

| Cluster | Support |
|---|---|
| Classical mask / multiplicity | Oppenheim, Proakis, Mitra, Rabiner/Gold, Kaiser, Harris, Rabiner freq.-samp., Parks–McClellan, Rabiner FIR, Butterworth, Constantinides, Jackson, Antoniou, Herrmann. Used only for feasible-set / designer facts. |
| Golden-reference testing | Huuhtanen et al. (ICST 2015) only, after removing SciPy from that sentence. |
| Generated-code protocol | Chen et al. (code-eval framing); Liu et al. (EvalPlus unique-output tests). Not used as DSP-practice evidence. |
| SciPy | Library occupant (`firwin` / `butter`) only. |

No invented references. No dangling cites. Unused inherited entry `vaidyanathan1993multirate` remains uncited. No “we are the first / no prior work” sentence.

---

## 7. Figure audit verdict

**PASS after repair.**

Two panels, now captioned as different spaces. Panel (b) labeled “Schematic realization space.” \(\mathcal{V}_t\) is declared schematic and not a Euclidean ball in the \(\tau_R\) metric. The intended message is intact: same contract → multiple realizations → some valid occupants fall outside reference proximity. Oracle B is not drawn as identical to C.

Residual: the \(\mathcal{V}_t\) blob is still a drawn disk. The caption is the control; a reviewer can still misread the drawing if they ignore the caption.

---

## 8. Notation audit verdict

**PASS after repair.**

| Symbol | Meaning | Drift? |
|---|---|---|
| \(t,h,h_r\) | task, implementation, canonical occupant | no |
| \(S_t\) | frozen contract predicate | no; C implements \(S_t\) |
| \(\mathcal{V}_t=\{h:S_t(h)=1\}\) | feasible set | no |
| \(R_{t,r}\), \(\tau_R=0.05\) | Oracle A | no |
| FRR / FAR | vs constructed labels | no |
| A / B / C | realization / response-to-\(h_r\) / membership | no |
| \(T\) | one sentence; not gold | no |

Singleton wording is now “effectively singleton under the declared scoring tolerance,” not literal \(\lvert\mathcal{V}_t\rvert=1\).

---

## 9. Page / format audit

Compile: `pdflatex` + `bibtex` + `pdflatex` ×2.

| Item | Result |
|---|---|
| Technical pages | 4 (through Conclusion + ethics) |
| Total pages | 5 (references continue; page 5 is refs only) |
| Figures | 1 |
| Tables | 4 |
| Overfull `\hbox` | none |
| Undefined cites / refs | none |
| Underfull | GitHub URL in abstract only |
| Negative vspace abuse | none (4 pt ethics gap only) |
| Abstract words | **134** excluding URL (139 with URL) |

Tables remain `\footnotesize`. Captions are longer by design (Table 3 especially). No unreadably small body font.

---

## 10. Reviewer simulation

### Reviewer A — Traditional DSP

- **Likely score:** 3 / 5 (borderline).
- **Strongest positive:** Suite S makes the claim conditional; the paper no longer pretends non-uniqueness is a discovery.
- **Strongest remaining weakness:** “This is textbook approximation theory plus a counting exercise on constructed filters.”
- **Likely rejection sentence:** “The authors measure a classical fact and call it an evaluation contribution.”
- **Does the manuscript answer it?** Partially. Intro now separates classical feasible-set fact from the scoring-rule consequence, and FRR is framed as decision error of reference matching. A DSP reviewer who wants an algorithm will still not be persuaded.

### Reviewer B — Empirical methodology

- **Likely score:** 4 / 5 (accept with comments).
- **Strongest positive:** Circularity of C is now explicit; A/B are named as the informative contrast; \(\tau_R\) grid and order-subset \(n=67\) are qualified.
- **Strongest remaining weakness:** Labels and C share \(S_t\); invalids are easy mechanism mutants; 300/416 valids are random-valid.
- **Likely rejection sentence:** “C is perfect because you defined the labels with C, and the valid set was built to be diverse.”
- **Does the manuscript answer it?** Yes, in wording. The residual is scientific, not rhetorical: there is still no independently labeled external gold.

### Reviewer C — Generated-code / ML

- **Likely score:** 3 / 5 (borderline).
- **Strongest positive:** Title/application are scoped; Arm G is an existence witness; no model ranking.
- **Strongest remaining weakness:** Almost all \(n\) is constructed; the title still leads with “Generated DSP Implementations.”
- **Likely rejection sentence:** “If this is about generated code, show generated-code rates; if it is about oracles, do not advertise generated implementations.”
- **Does the manuscript answer it?** Yes as a positioning argument (criterion first, witness second). A reviewer who wanted an LLM benchmark will still reject.

### PI estimate

- **Current accept probability:** **0.35–0.40.**  
  Experiments are internally consistent, but ICASSP can treat this as a methods-on-constructed-labels paper in a DSP venue. Do not inflate because the tables are clean.
- **Strongest remaining scientific weakness:** Constructed labels make C’s zeros a consistency check; the primary FRR is a property of this frozen constructed universe, not of independently admitted implementations.
- **Strongest remaining writing/positioning weakness:** The title still promises generated implementations while the evidence is overwhelmingly constructed. That mismatch is now explained, but it remains the first thing a hostile ML reviewer will quote.

---

## 11. Final strongest weakness

Oracle C cannot be externally validated inside this design, and 416/144 constructed labels are the only universe on which A/B FRR–FAR are estimated. The paper now says so. The weakness is the design, not a hidden claim.

---

## 12. Final recommendation

**SUBMISSION_READY**

Not `REVISION_REQUIRED`: every Category E wording risk identified in this audit was repaired; circularity, selection, order-subset, tight-mask, Suite S, and Arm G are now reviewer-safe; the compile meets the 4-technical + refs-on-5 constraint.

Further improvement would require new evidence (independent labels, more generated occupants, or a title change). That is outside Phase 3C authorization.
