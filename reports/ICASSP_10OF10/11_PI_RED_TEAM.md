# 11 — PI red team (three hostile reviewers)

Attacks are judged against the **new scientific thesis** (when a reference-distance oracle can be a correct oracle for a specification-defined task) and the independently verified evidence in reports 02–10.  
RESOLVED is used only when the evidence actually answers the attack.

---

## Reviewer A — expert digital-filter designer

| Attack | Verdict | Evidence |
|---|---|---|
| Multiple valid filters are obvious; the paper has no result | **PARTLY VALID** | Multiplicity of mask-feasible FIRs is classical. The new result is the **finite-universe exact-threshold criterion** and the measured **reference-separability gap**, not the observation that Remez ≠ Hamming. |
| Coefficient matching is a straw man | **PARTLY VALID** | Coefficient \(d\) is the community default for “same implementation.” Response-space \(d\) was also swept: **19/20** tasks remain empirically non-separable. The paper must lead with \(G_r\), not \(\tau_R=0.05\). |
| Different orders explain everything | **RESOLVED** | Type-I same-order / same-length / same-structure probes found independently verified reference-discordant alternatives on **16/16** FIR tasks, including all tight masks. Trivial padding / sign / scale were excluded. IIR: **4/4** tasks have same-order library alternatives that remain discordant. |
| The reference was badly selected | **RESOLVED** | Every independently verified library realization was used as \(h_r\). **0/20** tasks become exactly separable for any library reference. Min/median/max \(G_r\) are all negative. |
| The feasible-set construction is artificial | **PARTLY VALID** | The LP is a predetermined Type-I amplitude program with frozen directions, not a random search tuned for FRR. It is still a **numerical** interior of a discretized mask, not the full analytic feasible set. Report that limit. |
| Discretized frequency checking is insufficient | **PARTLY VALID** | Construction used 4096-point `freqz`. Final labels use \(N_f=131072\) plus local refinement. Four `firwin2` occupants flipped. This is a stronger numerical certificate, **not** a continuous-frequency proof. |

---

## Reviewer B — signal-processing theory reviewer

| Attack | Verdict | Evidence |
|---|---|---|
| There is no new SP methodology | **RESOLVED** | Reusable pieces: (i) soundness/completeness/exactness of reference balls vs \(\mathcal{V}_t\); (ii) \(D_V,D_I,G_r\); (iii) Type-I feasible-set probing with frozen directions; (iv) boundary-invalid inversion witnesses. |
| The theorem is trivial | **PARTLY VALID** | The finite-set threshold criterion is elementary once stated. Its value is that it **replaces an arbitrary \(\tau\)** and forbids overclaiming impossibility over all filters. The manuscript must keep that distinction. |
| The claimed impossibility is only finite-set empirical | **RESOLVED** | Claim registry forbids a global impossibility theorem. All \(G_r\le 0\) results are **empirical non-separability certificates on the evaluated universe**. |
| Numerical experiments do not justify the formal language | **PARTLY VALID** | Formal statements in `01_THEORY_AND_CLAIM_REGISTRY.md` are proved for finite \(\mathcal{U}_t\). Experiments instantiate \(\mathcal{U}_t\). The manuscript must not write “theorem: no threshold exists for FIR masks” without the universe qualifier. |
| Response-distance oracle could solve the problem | **PARTLY VALID** | Band \(\lvert H\rvert\) RMSE still has \(G_r\le 0\) on **19/20** tasks. One tight IIR task (`iir_hp_tight_8k`) has a tiny positive response gap (\(\approx 3.8\times 10^{-6}\)). Response matching is better than coefficients but is **not** an exact specification oracle on this universe. |

---

## Reviewer C — evaluation / verification reviewer

| Attack | Verdict | Evidence |
|---|---|---|
| Gold labels are circular | **RESOLVED** | Construction/`search_checker` is Stage A only. Final VALID/INVALID comes from `independent_spec_verifier` (no wrap of `spec_checker`). **4** previous valids flipped and were dropped. |
| Invalid examples are too easy | **RESOLVED** | A second invalid set of near-boundary `PASS_DROP` / `STOP_LIFT` mutants (fixed \(\varepsilon\in\{0.002,0.005,0.010,0.020\}\)) was independently verified (**160/160**). Inversion witnesses exist on **20/20** tasks. |
| Thresholds are arbitrary | **RESOLVED** | The scientific claim is the sign of \(G_r\), not \(\tau_R=0.05\). Full threshold sweeps; zero-FRR and zero-FAR cannot coexist when \(G_r\le 0\). |
| Candidate generation induces the result | **PARTLY VALID** | Pooled FRR is still dominated by 298/300 random-valids. The **task-level** and **probe** results do not depend on how many random samples were kept: 20/20 tasks disagree; 16/16 FIR probes produce same-order discordant valids. |
| Observations are clustered by task | **RESOLVED** | Primary unit is the specification. Macro-FRR, median, IQR, min/max, and task-cluster bootstrap (\(B=10000\), seed `20260826`) are reported. Occupant 370/412 is secondary. |
| Reference matching is not representative of real evaluation | **PARTLY VALID** | Arm G remains an existence witness (9 independently valid, all 9 reference-discordant, 4/4 original masks). It is not a field sample of industrial test benches. |

---

## Attacks that remain open (must stay visible)

1. Suite N is **one magnitude-mask family**, not DSP evaluation in general.
2. Dense-grid + refinement is **not** continuous-band certification.
3. IIR confirmatory same-order evidence is **library**, not a pole/zero feasible-set probe.
4. The “near-boundary” flag in the verifier is conservative (557 flags) and must not be narrated as “almost all occupants sit on the mask edge.”
5. Generated-code coverage is still 20 executed of 48 planned.

None of these reopen the central finite-universe claim if the manuscript stays inside the claim registry.
