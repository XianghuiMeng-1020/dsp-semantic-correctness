# 09 — ICASSP 4+1 page audit

Compiled from a clean auxiliary set (`pdflatex` + `bibtex` + `pdflatex` ×2) in `manuscript/w4/`.
Inspected the **rendered PDF**, not a TeX pagination guess.
Page images and extracted text: `reports/ICASSP_FINAL_10OF10/page_renders/`.

PDF: `manuscript/w4/paper.pdf` (letter, 612×792 pt, 5 pages, 268360 bytes).
No Overfull `\hbox` on the final compile. No `\tiny`, no negative `\vspace`.

Column fill (last text y / 792):

| Page | Left | Right | Role |
|---|---:|---:|---|
| 1 | 0.914 | 0.915 | technical |
| 2 | 0.915 | 0.914 | technical |
| 3 | 0.914 | 0.914 | technical |
| 4 | 0.914 | 0.879 | technical; small bottom margin after conclusion |
| 5 | 0.914 | 0.554 | compliance + references (right column ends with [19]) |

## Page-by-page (from rendered text)

```text
Page 1:
Title, authors, abstract, keywords.
§1 Introduction (when is a reference oracle exact).
Start of §2 (V_t, A_{τ,r}).

Page 2:
§2 continued: soundness/completeness/exactness, D_V, D_I, G_r,
Proposition 1, distances, d_K.
§3 Independent verification and protocol.
Start of §4 Results.

Page 3:
Fig. 1 (mask + reference ball).
Tables 1–3 (suites; separability; robustness).
§4 Results continued (task-level FRR, exact separation, same-order,
K-oracles, witness).
Start of §5 Discussion.

Page 4:
§5 Discussion continued (response gap, source-stratified FRR,
scope, canonicalization, operational Proposition 1, tight masks,
finite K, independent-verifier flips, frozen probe protocol,
Suite S control, empirical-certificate scope).
§6 Conclusion (complete; last sentence on this page).

Page 5:
Compliance with ethical standards.
§7 References [1]–[19] only.
```

Page 4 is occupied in both columns. The right column ends with the
conclusion at y=696 (fill 0.879), a normal leftover margin after a
short closing paragraph. It is not half-empty.
Page 5 begins with the compliance paragraph; no conclusion, table,
figure, theorem, method, or result sentence continues onto it.
References do not occupy technical pages.

```text
FINAL ICASSP PAGE AUDIT

Total PDF pages:
5

Technical pages:
4

Reference/compliance pages:
1

Technical content ends on:
Page 4

Page 4 substantive utilization:
PASS

Technical content spills onto page 5:
NO

Page 5 contains only permitted non-technical material:
YES

Tables readable:
PASS

Figures readable:
PASS

Template/font manipulation:
NONE

4+1 COMPLIANCE:
PASS
```
