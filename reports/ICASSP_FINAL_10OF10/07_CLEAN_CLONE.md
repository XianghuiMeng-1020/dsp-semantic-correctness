# 07 — Clean-clone reproducibility

**Verdict:** PASS

Clone:

```text
git clone --branch research/icassp-spec-oracle-10of10 \
  https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git
```

Temporary directory: `C:\Users\User\AppData\Local\Temp\icassp-clean-clone-10of10`

Cloned HEAD: `c2e854f4e7e934f241e09e405f08bc0cd7539ce5`
identical to `origin/research/icassp-spec-oracle-10of10` at clone time.

## Required inputs are tracked

`git status --short --ignored` in the authoring repo showed only
`__pycache__/` and LaTeX auxiliaries as ignored. No scientific input
was untracked.

Tracked required paths include
`registry/suite_{n,s}.json`, `requirements.txt`,
`experiments/icassp_10of10/run_all.py`,
`src/verification/independent_spec_verifier.py`,
`manuscript/w4/{paper.tex,refs.bib,spconf.sty,IEEEbib.bst}`,
855 `data/valid` files, and 290 `data/invalid` files.

## Manuscript compile from the clone

From `manuscript/w4` with clean auxiliaries:

```text
pdflatex + bibtex + pdflatex x2
Output written on paper.pdf (5 pages, 268360 bytes)
Page 5 starts: Compliance with ethical standards.
```

## Experiment rerun from the clone

Fresh venv (`numpy 2.5.2`, `scipy 1.18.1` — newer than the authoring
machine, still inside `requirements.txt` lower bounds):

```bash
python -m venv .venv
pip install -r requirements.txt
python -m experiments.icassp_10of10.run_all
```

`ALL_10OF10_STAGES: DONE` in 988.8 s.

| Headline | Clean-clone value |
|---|---|
| Independent valid | 412 |
| Invalid | 144 |
| Label flips | 4 |
| Pooled FRR | 370/412 = 0.898058… |
| Task-macro FRR | 0.900144… |
| 95% CI | [0.871253…, 0.924536…] |
| Coeff. non-separable | 20/20 |
| Resp. non-separable | 19/20 |
| Boundary inversion | 20/20 |
| Same-order FIR probe discord | 16/16 |
| Reference-choice exact | 0/20 |
| Multi-ref exact | 0/20 |
| Suite S exact | 8/8 |
| Generated witnesses | 9 |

No manuscript headline moved.
