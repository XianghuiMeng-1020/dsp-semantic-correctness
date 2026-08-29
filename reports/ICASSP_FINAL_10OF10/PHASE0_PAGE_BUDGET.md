# PHASE 0 — Presentation / page budget

Inspected `manuscript/w4/paper.pdf` (5 pages, SHA-256 `69890c7a…`)
and prior page renders under `page_renders/`. No edits.

| Check | Result |
|---|---|
| Pages 1–4 technical | YES |
| Page 5 compliance + refs only | YES |
| Accidental page 6 | NO |
| Figure text | TikZ `\footnotesize`; readable |
| Table overflow | none on last compile |
| Overfull boxes | none on last compile |
| Broken refs | no |
| Missing cites | all `\cite` keys in `refs.bib` |

Page 4 right-column fill ≈ 0.88 after conclusion (small leftover).
Not half-empty.

## Recoverable 0.25–0.50 page (if Phase 1 needs a table)

In order of scientific cost (lowest first):

1. **Discussion repeats** (label-flip paragraph + firwin2 edge
   sentence; Suite S restated; finite \(K\) restated after Results).
   ~0.20–0.30 page.
2. Move seed / \(B=10^4\) / method list (`firwin`/`remez`/…) to
   repository Methods supplement. ~0.08 page.
3. Collapse source-stratified 58/88, 14/24, 298/300 into Table 2
   footnote. ~0.05 page.

Do **not** cut Prop. 1, the four flips, or the 19/20 near-tie.

## Geometry figure vs tables

Fig. 1 already states the inversion cartoon. An empirical
\(D_V\) vs \(D_I\) scatter (20 tasks, coeff + resp) would make
\(G_r\le 0\) visible in one glance and could **replace** part of
Table 2, not add a sixth display. Higher value than another
robustness table. Not drawn in Phase 0.

```text
PAGE / FORMAT AUDIT: PASS
```
