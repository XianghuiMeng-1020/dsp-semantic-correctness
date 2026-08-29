# PHASE 4B — Submission / public-release protocol lock

Phase 4B may modify only manuscript wording/metadata, public-facing reproduction structure, documentation, release packaging, and submission compliance. Scientific definitions and results are immutable.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting HEAD | `912817a60270b563904c169bf27fe86b9c0859c2` |
| Working tree at lock | clean |
| `manuscript/final/paper.tex` SHA-256 | `e95e303c17930b13a70e6796d68627d9cfd784d059143b1b1f2bbe1e0e88cc42` |
| `manuscript/final/paper.pdf` SHA-256 | `c29f87e97e99f139c979acfdcbf4ae7429dbd9093b4f78f4075f65b6e76d7759` |
| Public remote | `https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git` |
| Public default (`origin/main`) at lock | `a776d3c` (old paper story; MATERIAL_MISMATCH vs final manuscript) |

## Immutable scientific tags (do not move)

| Tag | Commit |
|---|---|
| `icassp-10of10-phase3d-a-challenge-frozen` | `8ccb7f18f1b9f48ce8c4f40ff6df202bdec6862e` |
| `icassp-10of10-phase3d-b-primary-transfer-frozen` | `4fd880b9ad8cf0e2b46677db1b3fae57b765a831` |
| `icassp-10of10-phase3d-b-complete` | `639632f7cb6e2826c594396d2470503652791405` |
| `icassp-10of10-phase4a-manuscript-final` | `912817a60270b563904c169bf27fe86b9c0859c2` |

This protocol lock tag: `icassp-10of10-phase4b-protocol-lock` (created at the commit of this file).

## Forbidden

No new experiment, filter, task, metric, \(S_t\), catalog, threshold, challenge membership, or headline-number change.
Do not move older scientific tags.
Do not invent authors, affiliations, emails, grants, or DOIs.

## Required Phase-4B outcomes

1. Official-rules audit (this file's companion).
2. Single-anonymous author-mode compliance.
3. Writing micro-hardening only.
4. Public README + `python -m experiments.icassp_final.run_all` as the user-facing entry.
5. Clean-room reproduction.
6. Submission package + SHA-256 manifest.
7. Public `main` sync if credentials permit; otherwise report `PUBLIC_PUSH_REQUIRES_USER_CREDENTIALS`.
8. Immutable tag `icassp-2027-submission-frozen` on the exact release commit.
