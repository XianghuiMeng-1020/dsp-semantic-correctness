ICASSP 2027 final manuscript package (Phase 4A).

Authoritative source: paper.tex
Authoritative PDF:    paper.pdf
Bibliography:         refs.bib
Style:                spconf.sty + IEEEbib.bst
Main figure:          fig_transfer.pdf  (built from frozen Phase-3D-B transfer JSON)

The pre-reconstruction manuscript is preserved at
  manuscript/w4/paper_pre4a.tex

Build:
  pdflatex paper
  bibtex paper
  pdflatex paper
  pdflatex paper

Do not treat this directory as a public-main sync. Phase 4B owns release.
