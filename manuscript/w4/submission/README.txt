ICASSP 2027 submission package
==============================

Title:
Beyond Reference Matching: Specification-Based Correctness
Evaluation for DSP Implementations

Authors (single-anonymous; names required on the PDF):
Xianghui Meng (The University of Hong Kong)
Jionghao Lin (The University of Hong Kong / Carnegie Mellon University, corresponding)

Recommended primary track (official CFP wording):
Signal Processing Theory & Methods

Recommended secondary track:
Applied Signal Processing Systems

Avoid:
Machine Learning and Generative AI

This folder contains only the files needed to compile or upload the paper.
It does not contain experimental data, phase reports, or obsolete manuscript variants.

Compile:
  pdflatex paper.tex
  bibtex paper
  pdflatex paper.tex
  pdflatex paper.tex

CMS upload: paper.pdf
Source upload if requested: paper.tex, refs.bib, paper.bbl, spconf.sty, IEEEbib.bst
The figure is TikZ-inline; there is no separate image asset.
