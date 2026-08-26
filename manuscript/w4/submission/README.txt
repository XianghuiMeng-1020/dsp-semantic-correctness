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

Scientific headlines in this PDF (independently verified labels):
  412 valid, 144 invalid, 4 label flips
  task-macro FRR 0.900, 95% CI [0.871, 0.925]
  pooled descriptive FRR 370/412 = 0.898
  same-order 20/20; coeff. non-separable 20/20; resp. non-separable 19/20
  boundary inversion 20/20; reference-choice exact recovery 0/20
Final labels come from the independent verifier, not the 4096-point
construction checker. Authoritative reproduction:
  python -m experiments.icassp_10of10.run_all

Compile:
  pdflatex paper.tex
  bibtex paper
  pdflatex paper.tex
  pdflatex paper.tex

CMS upload: paper.pdf
Source upload if requested: paper.tex, refs.bib, paper.bbl, spconf.sty, IEEEbib.bst
The figure is TikZ-inline; there is no separate image asset.
