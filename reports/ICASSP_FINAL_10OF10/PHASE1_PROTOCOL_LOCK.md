# PHASE 1 — Protocol lock

Phase 1 is confirmatory with respect to the frozen Phase-0 scientific corpus. No occupant, task, specification, distance metric, or original label may be changed in response to Phase-1 results.

| Field | Value |
|---|---|
| Repository | `F:/ICASSP/project_a_public_release` |
| Branch | `research/icassp-final-10of10-scientific-hardening` |
| Starting commit | `8767aa4033a55af2405cad06e87ded8ce205f9e8` |
| Baseline science | `41c8e69194ebabde3a68b1333df1beb3f2e01160` / `icassp-pre-10of10-hardening-baseline` |
| git status at lock | clean (CRLF working-tree copies of a few text files are Git `autocrlf` only; blob-identical to HEAD) |

## Authoritative hashes (git blobs / files at starting commit)

| Artifact | SHA-256 |
|---|---|
| `manuscript/w4/paper.tex` | `4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7` |
| `manuscript/w4/paper.pdf` | `69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c` |
| `README.md` (HEAD blob) | `43d64e8c3ce9310772b100f2c2874dece42c19e4ff46cc8158818f4496f89d07` |
| `registry/suite_n.json` | `d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3` |
| `registry/suite_s.json` | `70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a` |
| `data/icassp_10of10/summary.json` | `f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b` |
| `data/icassp_10of10/task_stats.json` | `00f9d5f226c48b0e31b9c7bf58cc96535c2305e9db6eb2944e2ce6efe34ee884` |
| `data/icassp_10of10/recertify.json` | `8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a` |

## Frozen metric and universe definitions (not to be altered)

**Coefficient distance (confirmatory):** `d_coeff_mag_equiv` from `src/verification/distances.py` — relative \(\ell_2\) after `canonicalize_fir` / `canonicalize_iir`, FIR magnitude-equivalent (min of signed and global sign-flip). Unequal lengths zero-padded. Historical min-length \(d\) is **not** used for \(G_{\mathrm{obs}}^\star\).

**Response distance:** `d_resp_band` — RMSE of \(\lvert H\rvert\) on pass∪stop bands, `RESP_N = 131072` via the same `freqz`/`sosfreqz` path as `distance_bundle`.

**Canonical reference:** shortest-odd Hamming `firwin` (FIR) or lowest-order `butter` (IIR) recorded in `data/valid/canonical.json`.

**Primary manuscript universe \(\mathcal{U}_t\)** (`pipeline.py` confirmatory gap `coeff_with_boundary` / `resp_with_boundary`):

- Valids: independently verified constructed occupants (`independent_label=VALID` in `recertify.json`) **plus** Type-I probe occupants with `genuine_same_order` in `feasible_probe.json`.
- Invalids: independently verified mechanism invalids **plus** independently verified boundary invalids.

**Labels** used in Phase 1 are the frozen `independent_label` / `independent_ok` fields. Phase 1 does not re-vote them.

**Outputs** live only under `results/icassp_10of10_hardening/phase1/` and `reports/ICASSP_FINAL_10OF10/PHASE1_*`. Frozen `data/icassp_10of10/*.json` (except those new paths) must remain byte-identical.

**Not in Phase 1:** manuscript edit, `main` sync, \(K^*\), IIR continuous certification, new tasks/metrics, label changes.
