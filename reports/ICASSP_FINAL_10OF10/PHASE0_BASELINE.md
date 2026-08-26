# PHASE 0 — Baseline freeze

Phase 0 only. No manuscript edit. No headline change. No new experiment design.

| Field | Value |
|---|---|
| Repo path | `F:/ICASSP/project_a_public_release` |
| Original branch | `research/icassp-spec-oracle-10of10` |
| Original HEAD | `41c8e69194ebabde3a68b1333df1beb3f2e01160` |
| Hardening branch | `research/icassp-final-10of10-scientific-hardening` (created from that HEAD; history not rewritten) |
| Baseline tag | `icassp-pre-10of10-hardening-baseline` → `41c8e69194ebabde3a68b1333df1beb3f2e01160` |
| Prior scientific tag | `icassp-spec-final-10of10` (annotated; peels to the same commit) |
| Dirty/clean before Phase 0 | **clean** |
| Authoritative remote | `origin` = `https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git` |
| Public default branch | `origin/main` = `a776d3c3f75f1343ed1769a444189f4a939f9a8f` (**older** Phase-2 / 374/416 package) |

## Authoritative current surfaces (this branch)

| Role | Path |
|---|---|
| Manuscript | `manuscript/w4/paper.tex` |
| PDF | `manuscript/w4/paper.pdf` |
| Submission copy | `manuscript/w4/submission/` |
| README | `README.md` |
| Experiment entry | `python -m experiments.icassp_10of10.run_all` |
| Task registry | `registry/suite_n.json`, `registry/suite_s.json` |
| Final verifier | `src/verification/independent_spec_verifier.py` |
| Construction checker | `src/spec_checker.py` via `src/verification/search_checker.py` |
| Headline source | `data/icassp_10of10/{summary,task_stats,recertify,reference_choice,multi_reference,feasible_probe,singleton,generated_witness,boundary_invalids}.json` |

Rejected as current: `manuscript/w1`, `w2`, `w3`, `reports/archive/**`, root Phase-2 reports (archived), `scripts/reproduce_*.py`.

## PDF (rendered, not inferred)

- Total pages: **5**
- Technical pages: **4** (1–4)
- References/compliance: **1** (page 5)

## SHA-256 manifest (pre-hardening)

```
69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c  manuscript/w4/paper.pdf
4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7  manuscript/w4/paper.tex
43d64e8c3ce9310772b100f2c2874dece42c19e4ff46cc8158818f4496f89d07  README.md
d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3  registry/suite_n.json
70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a  registry/suite_s.json
9f44b35a7b09bbffbaf8784dcec311a13266a9201040869736880bc0f2cf761e  src/verification/independent_spec_verifier.py
c1ad1cc913f6c4200e65e02da3c7af6eabcf4f63f20edcda32f87561dba6299a  src/verification/search_checker.py
753ffec3ae8be7d31b7670bbd1023e006ab9c509eb026495ec625d16ca8dc3da  src/spec_checker.py
37e4453543fd3c18f68dd97144bb02709f85328217d929fb2ae5187555382a82  src/verification/canonicalize.py
50b9baaa6518f3944b443e6fa4ee53679b7c41e504c6daa29f8c5d7f7b4c5d86  src/verification/distances.py
6ae4a73602fbe1cc2a5de290eaefe0caadbb24b473e2dafba42e76232c6a01f9  src/verification/feasible_set_probe.py
ff94c66f3f91e23c02df9509723aee490dec711b7ed476dd7a9cee31b3c5135f  src/verification/boundary_invalids.py
429644b5361978b09b847d199c30afe343b64e199f3bd6dd8731e463674a48a9  experiments/icassp_10of10/run_all.py
6e79846cf7facb7221f74b4d177a5938edf009f64c7c6fa8ffc0e014de264540  experiments/icassp_10of10/pipeline.py
f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b  data/icassp_10of10/summary.json
00f9d5f226c48b0e31b9c7bf58cc96535c2305e9db6eb2944e2ce6efe34ee884  data/icassp_10of10/task_stats.json
8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a  data/icassp_10of10/recertify.json
```

Submission `paper.tex` / `paper.pdf` hashes match the w4 sources.

No pre-existing uncommitted changes. Phase 0 commits are reports only.
