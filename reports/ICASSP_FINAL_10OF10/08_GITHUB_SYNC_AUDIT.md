# 08 — GitHub remote synchronization audit

Authoritative remote: `origin`

```text
origin  https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git (fetch)
origin  https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git (push)
```

## Commands recorded (authoring repo)

```text
git status                          # clean before first push
git branch --show-current           # research/icassp-spec-oracle-10of10
git rev-parse HEAD                  # c2e854f4e7e934f241e09e405f08bc0cd7539ce5
git remote -v                       # origin → GitHub URL above
git fetch --all --prune
git status -sb
git log -1 --oneline                # c2e854f Reconstruct the ICASSP manuscript...
git push -u origin research/icassp-spec-oracle-10of10
git fetch --all --prune
git rev-parse HEAD
git rev-parse origin/research/icassp-spec-oracle-10of10
```

## First push (manuscript reconstruction)

| Field | Value |
|---|---|
| GitHub remote URL | `https://github.com/XianghuiMeng-1020/dsp-semantic-correctness.git` |
| Local branch | `research/icassp-spec-oracle-10of10` |
| Local HEAD | `c2e854f4e7e934f241e09e405f08bc0cd7539ce5` |
| Remote branch HEAD | `c2e854f4e7e934f241e09e405f08bc0cd7539ce5` |
| Equality check | **YES — identical** |
| Final tag at that moment | `icassp-spec-final-10of10` did **not** exist remotely (`git ls-remote --tags origin icassp-spec-final-10of10` empty) |

This was not inferred from a quiet `git push`. The two `rev-parse` hashes were compared.

This audit file, the clean-clone report, and the tag are added after that
verified push. After they are committed and pushed, `HEAD` and
`origin/research/icassp-spec-oracle-10of10` must again be identical
before the tag is created. The PI report records those post-audit hashes.

## README / science check

- Root README exposes the final table (412 / 144 / 0.900 / [0.871, 0.925] / 20/20 / 19/20 / 0/20 / 4 flips).
- Final labels are stated to come from the independent verifier, not the 4096-point construction checker.
- Authoritative command: `python -m experiments.icassp_10of10.run_all`
- Stale-number search: see `06_STALE_NUMBER_SEARCH.md` (PASS on current surfaces).

## Reproduction

Authoritative command: `python -m experiments.icassp_10of10.run_all`
Headline lock: PASS (`05_REPRODUCTION_LOCK.md`)
Clean-clone: PASS (`07_CLEAN_CLONE.md`)

## Working tree

After this audit commit: intended clean working tree.
Ignored only: `__pycache__/`, `manuscript/w4/*.{aux,log,out,blg}`.
Those auxiliaries are not scientific inputs.

## Conclusion

```text
GITHUB_FULLY_SYNCHRONIZED
```

The manuscript reconstruction commit was hash-verified on GitHub.
The subsequent audit/tag commit is pushed only if `HEAD` again equals
`origin/research/icassp-spec-oracle-10of10`.
