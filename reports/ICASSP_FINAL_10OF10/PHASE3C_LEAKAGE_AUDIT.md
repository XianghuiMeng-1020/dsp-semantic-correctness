# PHASE 3C — Leakage audit

Corpus: `type_i_feasible_probes_1260`

Verdict: `MATERIAL_LEAKAGE`

Blocker: `PHASE3C_HOLDOUT_LEAKAGE_BLOCKER`

Primary transfer is valid only if the first five relevant leakage checks are clean.

| question | answer |
| -------- | ------ |
| Was it part of base V? | 1 |
| Was it part of base I? | 0 |
| Was it a candidate reference in Phase 3B? | 1 |
| Did its distances affect Phase-3B K*? | 1 |
| Did its labels affect threshold selection? | 1 |
| Was any catalog changed after its score was observed? | 0 |
| Is it coefficient-identical to any selected reference? | 1 |
| Is it response-identical to any selected reference? | not_scored_after_blocker |

First five relevant checks clean: `0`

## Evidence

- Phase-3B $V_t$ includes probes: 1
- Probe n: 1260; constructed n: 412
- Exact CID overlap constructed vs probes: 0
- Probe paths among coefficient catalog members: 467 / 825
- FIR tasks with at least one selected probe reference: 16
- FIR Phase-3B n_valid equals constructed + probes. 467 of 825 coefficient catalog members are probe_candidates paths.

Do not score this corpus as `H_TYPEI` external validity.
