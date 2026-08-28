# PHASE 3D-B — Final targeted prior-art pass

Question:

> Is there close prior DSP work demonstrating, with prospectively generated and independently specification-certified FIR/IIR realizations, that exact realization-reference catalogs fitted on one implementation universe fail or require expansion on additional conforming implementations?

This is **not** a claim that prototype selection, train/test splits, set cover, or conformance testing are novel.

## Generic methods (explicitly known; disclaimed)

| Topic | Verdict | Evidence |
|---|---|---|
| Held-out prototype / nearest-neighbor evaluation | `KNOWN` | Hart condensed nearest neighbor (1968); standard prototype-set train/test evaluation. |
| Prototype maintenance under support expansion | `KNOWN` | Incremental CNN / prototype evolution (e.g. De Lange & Tuytelaars, CoPE, 2021); test-time prototype adaptation. Not a DSP filter result. |
| Set cover / minimum prototype catalog | `KNOWN` | Classical combinatorial optimization; Phase 3B already disclaimed this. |
| Specification / conformance testing | `KNOWN` | ISO/ITU conformance; NIST IR 6025 reference-implementation testing; software golden-master / pseudo-oracle testing. |
| DSP filter design plurality | `KNOWN` | Parks–McClellan, firls, window, Butterworth/Chebyshev/elliptic are textbook multiple *design methods* for the same mask (Oppenheim/Schafer; Rabiner–McClellan–Parks 1975; MATLAB `firpm`/`firls`). |

## DSP / implementation-verification neighbors (partial, not the same audit)

1. **DSVerifier** (Ismail, Bessa, et al.; digital-system BMC). Formal checks of overflow, stability, limit cycles, and FWL effects for a *given* \((b,a)\) under a chosen realization (DFI/DFII/TDFII). It does not fit an exact nearest-reference catalog on one valid universe and then score prospectively generated, independently \(S_t\)-certified alternate designs.

2. **UVM / MATLAB golden-model DSP filter verification** (e.g. DVCon “Flattening the UVM Learning Curve”). Bit-accurate comparison of RTL against one MATLAB/scipy reference for a programmed tap set. This is single-oracle conformance, not a finite-universe catalog-transfer audit across many spec-valid coefficient vectors.

3. **FPGA FIR cores vs `scipy.signal.lfilter`**. Bit-exact testing of an architecture against the *same* coefficients. Opposite scientific question: implementation fidelity for one \(h\), not whether a catalog of \(h\) values covers the specification-valid set.

4. **IEEE filter-design literature**. Compares Remez vs least-squares vs window *as design algorithms*. It does not treat those outputs as a holdout against an exact realization-reference oracle fitted on another library.

## Close-prior verdict

**`NO_CLOSE_PRIOR_FOUND`**

No located DSP paper performs the same prospective audit:

- catalogs fitted to exactness on a frozen finite valid/invalid universe;
- a later, catalog-blind, continuously certified FIR/IIR challenge;
- transfer reported without retuning \(\tau\) or \(R^\star\) on the challenge;
- maintenance \(\Delta K\) / unavoidable new references as the consequence of admitting those realizations.

Novelty boundary: **`CLEAR`** for this *audit and DSP interpretation*, **`WEAK`** for generic prototype/set-cover methodology (must remain disclaimed).
