# PHASE 4A — Claim red-team

No new science. Each attack is answered by a sentence, table, or figure already in `manuscript/final/paper.tex`.

Submission mode (authoritative ICASSP 2027 CFP): **single-anonymous**.
Reviewers see authors; authors do not see reviewers.
Author names and affiliations are retained.
The public GitHub URL is **not** printed (Phase 4B owns release wording).

---

## Reviewer A — signal-processing theorist

### A1. “Why aren't coefficient vectors expected to differ?”

**Manuscript answer (Discussion, first paragraph):**
> That Remez, window, and elliptic designs can meet one mask with different coefficients is classical filter theory; the audit is whether a catalog of those realizations remains an adequate correctness proxy for later valid designs.

The paper does not sell coefficient disagreement as a discovery.

### A2. “What does this tell me beyond basic filter-design theory?”

**Answers:**
- Fig.~1 / Table II: catalogs *exact on one finite universe* still accept only 66/614 later certified-valid designs in coefficient space, versus 585/614 in magnitude-response space.
- Sec.~4.2 hierarchy: enlarging the *base* coefficient catalog to exact \(K^\star_{\mathrm{obs}}\) still yields only 10.7% prospective transfer (canonical / \(K\in\{3,5\}\) / library: 0/614).
- Sec.~4.3: every expanded exact coefficient catalog requires newly admitted realizations (\(M^\star>0\) on 20/20; median \(K^\star\) 23→55).

That is a transfer/adequacy result, not a restatement of Parks–McClellan vs window design.

### A3. “Response matching just *is* the specification.”

**Answers:**
- Discussion: response matching “failed on one task in Fig.~1, and it is not a proof of mask satisfaction.”
- Limitations: secondary invalid FAR 96/310 on a 12-task subset; “not asserted to be sound or complete in general.”
- Correctness definition remains \(S_t\) (eq.~(1)).

---

## Reviewer B — software-testing expert

### B1. “The oracle problem is old.”

**Introduction, paragraph 3:**
> The general test-oracle problem, specification-based conformance, and prototype or reference-set selection are established ideas [14, 15, 16, 17, 18]. We do not propose a new set-cover algorithm or a new theory of oracles. The unresolved signal-processing question is narrower: whether realization-based coefficient or magnitude-response references fitted on one FIR/IIR implementation universe remain adequate for later implementations certified against the same mask.

### B2. “Set cover / prototypes are old.”

**Sec.~2:**
> Computing that finite-universe diagnostic reduces to a standard set-cover optimization [18, 17]; the optimization itself is not our contribution. \(K^\star_{\mathrm{obs}}\) measures realizable reference burden, not algorithmic novelty.

### B3. “This is just conformance testing.”

Conformance supplies the *definition* \(S_t\). The contribution is the certified FIR/IIR audit plus the *representation-dependent transfer* measurement (Contribution 3 / RQ3 / Fig.~1).

---

## Reviewer C — skeptical empiricist

### C1. “The challenge is generated.”

**Sec.~3:** eight ordinary designer families; 960 scheduled attempts; catalog-blind sequence (1)–(8); “they are not all possible filters.”
Limitations repeat the eight-family scope.

### C2. “The universe is finite.”

Observation 1 is labeled evaluation geometry, “not a theorem over all filters.”
Limitations: “No infinite-universe claim is made.”
Single-reference results are stated as finite-universe non-separability, never “no possible reference exists.”

### C3. “Why trust \(S_t\)?”

**Sec.~3:** 412/412 continuous certification (FIR Bernstein/Sturm on \(P(x)=\lvert H\rvert^2\); IIR Schur + \(P_B-CP_A\)); no valid→invalid contradiction.
Cosine endpoints are *not* claimed as a machine-checked continuous proof.

### C4. “Why only magnitude masks?”

Limitations: “We evaluate 20 magnitude-mask tasks, not general DSP software.”
Title and abstract say FIR/IIR realizations / magnitude masks.

### C5. “Response matching works, so why is this paper needed?”

Because the *evaluation practice* under audit is often a golden *coefficient* vector or a small coefficient catalog.
Fig.~1 is the reason the paper exists: that practice does not transfer, while a response catalog is a better but imperfect surrogate.
If the community already scored \(S_t\), there would be no proxy to audit.
Response transfer is 95.3%, not 100%, and one task is at 70%.

### C6. “Maybe you just needed more references.”

Sec.~4.2: exact base \(K^\star_{\mathrm{obs}}\) still 10.7% coefficient transfer; \(K\in\{1,3,5\}\) and all-library accept 0/614.

### C7. “Maybe the point sets are just not one-ball separable.”

Sec.~4.1 ambient-center sentence: arbitrary Euclidean centers separate 19/20 coefficient and 20/20 response universes.

---

## Quote-audit of forbidden claims

Searched the reconstructed manuscript for:
impossible / cannot recover / no reference can / all DSP / fundamentally / unsound / theorem proves.

None of those unscoped claims appear.
Scoped language used instead: finite universe, representation-dependent, not universally sound, not all possible filters.

---

## Unanswered attacks

None that writing can close without new science.
Remaining empirical limits (8 families; 20 masks; incomplete H_INVALID) are stated in the limitations paragraph.

---

## Internal review scores (writing only; science closed)

| Dimension | Score /10 | reason |
|---|---:|---|
| ICASSP scope fit | 9.6 | FIR/IIR magnitude masks, classical designers, ICASSP template |
| Technical correctness | 9.6 | All headlines traced to frozen artifacts |
| Experimental validation | 9.3 | Prospective protocol is strong; 8 families and 12/20 H_INVALID remain |
| Novelty | 9.3 | Matches Phase-3D-B framing E; oracle/set-cover novelty disclaimed |
| Presentation / clarity | 9.2 | Fig.~1 carries the result; page-3 float gap is residual |
| Reproducibility as represented | 9.2 | Frozen artifacts + local `python -m experiments.icassp_final.run_all`; public URL not synced |
| Claim calibration | 9.5 | Finite-universe, representation-dependent, response not gold |
| Overall | 9.4 | Ready for PI reading; no further science authorized |

Presentation 9.2 is not fixable by shrinking the whole document. Further figure compression would hurt readability. Stop.
