# PHASE 3A — Prior-art boundary

Sources below are peer-reviewed articles, textbooks, or archival surveys. Blogs are not used. The generic sphere-separation LP is treated as **known mathematics**. No citation is fabricated.

| Source | What is already known | What it does NOT establish | Relation to our manuscript |
| ------ | --------------------- | -------------------------- | -------------------------- |
| Weyuker, *On Testing Non-testable Programs*, Comput. J. 25(4):465–470, 1982; Davis & Weyuker, *Pseudo-oracles for non-testable programs*, ACM 1981 | The test-oracle problem; numerical/scientific programs often lack a unique correct output; pseudo-oracles compare independent implementations | Does not study FIR/IIR magnitude-mask membership, nor whether a distance-to-reference threshold recovers a specification set | Frames why a golden filter is an attractive but incomplete oracle. Not a DSP correctness theorem. |
| Barr, Harman, McMinn, Shahbaz, Yoo, *The Oracle Problem in Software Testing: A Survey*, IEEE TSE 41(5):507–525, 2015 | Taxonomy of specified, derived, implicit, and human oracles; metamorphic and specification-based oracles | Does not give a finite-universe exactness criterion for reference-distance scoring of DSP masks | The paper is an instance of specification vs derived (golden) oracles. The survey does not contain our geometry diagnostic. |
| Chen, Tse, Zhou and later metamorphic-testing literature (e.g. Chen et al., IST 2003) | Relations among inputs/outputs can test programs without a full oracle | Does not address single-center Euclidean recovery of a filter mask | Complementary testing style. Not used as a substitute for \(S_t\) membership and not claimed as our method. |
| Kanewala & Bieman, *Techniques for Testing Scientific Programs Without an Oracle*, SE-CSE 2013 | Scientific software often lacks oracles; ad-hoc expert inspection is common | No DSP mask geometry; no ambient-center certificates | Motivates specification predicates for numerical DSP, not our LP. |
| Huuhtanen, *Testing digital signal processing software* (cited in the manuscript) | Golden-output testing is used in DSP software practice | Does not prove reference balls fail on independently labeled mask occupants | Closest DSP-testing cite already in the paper. Practice, not a separability audit. |
| Chen 2021 / Liu 2023 (EvalPlus; manuscript cites) | Unique-output unit tests miss non-unique correct programs | Not a filter-specification result | Already scoped in the manuscript to that sentence only. |
| Parks & McClellan, IEEE Trans. Circuit Theory 1972; McClellan, Parks, Rabiner 1973; Herrmann 1973; Oppenheim & Schafer; Proakis & Manolakis; Rabiner & Gold | A magnitude mask can admit many designs; equiripple linear-phase FIR of fixed order/weight is unique; windows, least-squares, IIR classical designs differ | Does not ask whether *distance to one realization* recovers *specification membership*, nor whether any ambient Euclidean center does | Explains why valid occupants are not a singleton. Necessary background, not the oracle-adequacy theorem. |
| SciPy `signal` (Virtanen et al. 2020; manuscript library occupant) | Concrete library realizations | Not a verification methodology | Occupant source, not prior art for the claim. |
| Elzinga–Hearn / smallest enclosing ball; Gärtner | Computing a minimum-radius ball through a point set | Enclosing one class, not excluding a second labeled class as a *correctness oracle* | Related convex geometry. Different objective (volume vs exact two-set recovery). |
| Tax & Duin, *Support Vector Data Description*, Machine Learning 54:45–66, 2004; Tax & Duin, PRL 1999 | One-class hypersphere; optional negative examples; kernels | Soft-margin description / novelty detection, not an auditable finite-universe exactness certificate for a DSP spec | Same geometric object (a sphere), different scientific question and success criterion. |
| Astorino & Gaudioso, *A fixed-center spherical separation algorithm...*, Comput. Manag. Sci. 2009; Astorino, Fuduli, Gaudioso, *DC models for spherical separation*, J. Global Optim. 48:657–669, 2010; Astorino, Fuduli, Gaudioso, *Margin maximization in spherical separation*, Comput. Optim. Appl. 53:301–322, 2012; Le Thi et al., J. Global Optim. 2013 | Spherical separation of two finite point sets; fixed or free center; LP / DC algorithms | Pattern-classification accuracy, not specification-defined DSP correctness, not frozen-universe certificates tied to \(G_r\) / \(G_{\mathrm{obs}}^\star\) | The **LP transformation we use is in this family**. We do not claim the transformation is new. |
| Mangasarian, *Linear and Nonlinear Separation of Patterns by Linear Programming*, Operations Research 13:444–452, 1965 | LP formulations for pattern separation | Not spheres-as-oracles for filters | Ancestor of linear-separability LPs. |
| Boyd & Vandenberghe, *Convex Optimization* | QCQP / SOC representability of Euclidean-ball constraints | Textbook, not a DSP result | Confirms that the ambient program is standard convex optimization. |

## Definitely not novel

- The test-oracle problem, golden/pseudo-oracles, and specification-based testing.
- The existence of multiple valid FIR/IIR designs for one magnitude mask.
- Separating two finite point sets by a sphere, and rewriting \(\|i-c\|_2^2-\|v-c\|_2^2>0\) as an affine inequality in \(c\).
- One-class / SVDD hyperspheres and spherical classifiers.
- The statement “a Hamming ball around one library call is not the mask.”

The ambient-center criterion, **as a generic geometric program**, is standard mathematical knowledge.

## Potentially manuscript-specific contribution

What is not established by the sources above, taken together, is this **applied diagnostic on a frozen, independently labeled DSP universe**:

1. Specification membership \(S_t\) is the correctness predicate (continuously certified in Phases 2A/2B), not agreement with a realization.
2. Level-1 fixed canonical \(G_r\) and Level-2 best **observed valid** \(G_{\mathrm{obs}}^\star\) already fail on the confirmatory coefficient metric (20/20).
3. Level-3 asks whether **any** point in the confirmatory Euclidean embedding — not necessarily a filter — can serve as a single-center threshold oracle, with stored dual/primal certificates.
4. The scientific claim, if Level 3 also fails, is **not** “sphere LP is new.” It is: *on this frozen finite universe, specification-defined valid membership is not a Euclidean ball in the paper’s coefficient representation.* That closes the “you picked a bad reference” attack without claiming a new theorem of convex geometry.

That package is a **reference-oracle adequacy audit** for DSP implementations. It is a methodological contribution to how filter correctness is evaluated, not a new separator algorithm.

## Claims we must never make

- That the generic test-oracle problem was introduced here.
- That sphere-separation LP, \(\Gamma^{\mathrm{amb}}\), or the affine expansion is a new optimization result.
- That “no metric works,” “no multi-reference oracle can work,” or “no nonlinear boundary could recover validity.”
- That an ambient center, when it exists, is a realizable DSP filter.
- That specification-based verification is universally necessary for all DSP software.
- That closely matching prior DSP work already performed this three-level audit with certificates on an independently labeled mask corpus. **We found no such paper.** Absence of evidence is not a proof of absence; it is a boundary, not a priority claim.

## Prior-art claim gate (preview)

These answers are literature answers. They do not depend on the numerical ambient margins.

- **Q1.** Is the generic test-oracle problem novel here? **NO.**
- **Q2.** Is generic sphere separation / LP novel here? **NO.**
- **Q5 (partial).** A signal-processing reviewer can still see a DSP-methodological contribution: the object being audited is *mask membership vs realization balls*, which is a filter-evaluation question, not a tutorial on Weyuker. Whether that survives the ambient numbers is decided after the LP, not here.
