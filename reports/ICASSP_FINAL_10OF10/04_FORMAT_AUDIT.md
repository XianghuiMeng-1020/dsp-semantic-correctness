# 04 — Format audit

**Verdict:** PASS

| Check | Result |
|---|---|
| Template | official `spconf.sty` / `IEEEbib.bst` |
| Class | `article` + `spconf` (ICASSP conference) |
| Title / authors | Title B; Meng + Lin (HKU / CMU); corresponding `jionghao@hku.hk` |
| Single-anonymous | names on PDF |
| Keywords | Filter design, specification testing, correctness evaluation, FIR, IIR |
| Figure | 1 TikZ `figure*`; `\footnotesize` labels |
| Tables | 3; `\footnotesize`; denominators explicit |
| Font games / negative vspace | none |
| Overfull `\hbox` on final compile | none |
| GitHub URL | abstract only |
| Track recommendation (not printed) | Signal Processing Theory & Methods |

No `\tiny` tables. No leaderboard formatting. Compliance sits on page 5 with references, as permitted.
