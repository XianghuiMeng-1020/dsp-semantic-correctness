# PHASE 4A — Manuscript reconstruction protocol

The scientific program is **closed**. Phase 4A may only rewrite the manuscript from locked evidence.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `639632f7cb6e2826c594396d2470503652791405` |
| Phase-3D-B tag | `icassp-10of10-phase3d-b-complete` (do not move) |
| git status at lock | clean |

## Locked science (do not alter)

No new experiment, filter, task, metric, label, \(S_t\), catalog, threshold, or holdout.
Do not hide Phase-3A ambient centers or Phase-3C leakage.
H_INVALID remains secondary / incomplete (12/20 tasks).
Do not claim infinite-universe impossibility, set-cover novelty, or generic oracle-problem novelty.

Authoritative numbers come from:

- Phase 1: `results/icassp_10of10_hardening/phase1/headline.json`
- Phase 2A/2B: 412/412 continuous certification
- Phase 3A: ambient 19/20 coeff, 20/20 resp
- Phase 3B: `phase3b/headline.json` (median \(K^\star=23\))
- Phase 3D-A: frozen challenge 614 / 310
- Phase 3D-B: `phase3d_b/transfer_*.json`, `maintenance.json`, `headline.json`

## Framing (locked)

**E — hybrid concise ICASSP story.** Three contributions. Three RQs. RQ3 is the climax.

**Title candidate (selected):** A —
*When Does Reference Matching Transfer? Specification-Certified Audits of FIR/IIR Realizations*

| Candidate | ICASSP | Specificity | Novelty signal | Overclaim | Readability | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| A | 9 | 9 | 9 | 8 | 8 | 9 |
| B | 8 | 8 | 7 | 8 | 8 | 8 |
| C | 9 | 9 | 9 | 8 | 7 | 9 |
| D (old) | 7 | 5 | 6 | 6 | 8 | 5 |

A is preferred: FIR/IIR-specific, question form matches the representation-dependent transfer result, does not say “all DSP implementations.”

## Submission mode

ICASSP 2027 is **single-anonymous** (reviewers see authors; reviewers are anonymous).
Author names and affiliations are retained.
Public `main` / GitHub URL is **not** synchronized in Phase 4A.
The camera-ready sentence will point to a reproduction repository after Phase 4B.

## Historical manuscript

The pre-4A source is preserved as `manuscript/w4/paper_pre4a.tex` (copy of the frozen w4 paper).
New source of record: `manuscript/final/paper.tex` (also compiled from that tree).
Working `manuscript/w4/paper.tex` is updated to match `manuscript/final/`.

## Forbidden claims (quote-audit)

No “no possible reference exists,” “fundamentally impossible,” “all DSP implementations,” “response matching solves the problem,” or unscoped “reference matching is unsound.”

## Reproduction wrapper (design only)

Eventual public command: `python -m experiments.icassp_final.run_all`.
May be sketched locally; do not switch public `main`.
