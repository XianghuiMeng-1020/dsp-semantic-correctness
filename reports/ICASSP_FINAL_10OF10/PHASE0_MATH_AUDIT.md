# PHASE 0 — Mathematical claims

No manuscript edits.

## Definitions (as written)

- \(\mathcal{V}_t=\{h:S_t(h)=1\}\)
- \(\mathcal{A}_{\tau,r}=\{h:d(h,h_r)\le\tau\}\) (closed ball)
- Soundness / completeness / exactness over **all** \(h\)
- Measurements restricted to finite \(\mathcal{U}_t\)
- \(D_V=\sup_{\mathcal{V}_t\cap\mathcal{U}_t}d\), \(D_I=\inf_{\mathcal{U}_t\setminus\mathcal{V}_t}d\)
- Gap \(G_r=D_I-D_V\)
- Exact threshold on \(\mathcal{U}_t\) iff \(\exists\tau:\ D_V\le\tau<D_I\)
- \(d_K=\min_{r\in R_K}d(\cdot,h_r)\); same gap

## Checks

| Issue | Class | Comment |
|---|---|---|
| Closed ball vs `≤ τ < D_I` | NONE | Correct for \(d\le\tau\). If \(D_V<D_I\), any \(\tau\in[D_V,D_I)\) works. |
| Equality \(D_V=D_I\) | NONE | \(G_r=0\) correctly forbids a separating \(\tau\). |
| Finite vs infinite | WORDING_ONLY | Exactness defined globally; Prop. 1 is finite. Body is usually careful. Conclusion states “evaluated universe.” |
| Empty \(\mathcal{V}\) or complement in \(\mathcal{U}\) | MINOR_TECHNICAL | `sup`/`inf` of empty set not defined in the text. Does not arise in the 20+8 tasks. |
| Ties / equal-length padding | NONE | Canonicalization + exclusion of trivial encodings is stated. |
| Unequal-order historical \(d\) | NONE | Historical min-length \(d\) is secondary; confirmatory \(d\) is canonical. |
| Multi-reference | NONE | Gap on \(d_K\) is the correct analogue. |
| “iff \(G_r>0\)” | NONE | Equivalent to existence of \(\tau\) on a finite nonempty pair of sets. |
| Abstract “no coefficient-distance threshold” | WORDING_ONLY | True on the stated \(\mathcal{U}_t\) and stated \(d\), not over all DSP. |
| “every library reference” | WORDING_ONLY | Library catalog, not \(\arg\max_r G_r\). |
| Inversion \(\Rightarrow G_r\le 0\) | NONE | Correct. |
| Response near-tie \(3.8\times 10^{-6}\) | NONE | Correctly not sold as exactness. |

Global exactness \(\mathcal{A}_{\tau,r}=\mathcal{V}_t\) is **not**
proved and is **not** claimed as a theorem over filters.

**Worst class present:** `MINOR_TECHNICAL` (empty-set `sup`/`inf`).
**Overall:** `WORDING_ONLY` for reviewer-facing overbreadth in the
title/abstract; the formal Prop. 1 is sound.

```text
MATHEMATICAL AUDIT: WORDING_ONLY
```
