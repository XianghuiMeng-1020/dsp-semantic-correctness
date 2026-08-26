ICASSP 2027 SPECIFICATION-BASED CORRECTNESS
10/10 SCIENTIFIC STRENGTHENING — FINAL GATE

Baseline commit: a776d3c3f75f1343ed1769a444189f4a939f9a8f
Strengthening branch: research/icassp-spec-oracle-10of10
Final scientific commit: (set after this commit)

G1 Independent validity:
PASS

G2 Canonicalization:
PASS

G3 Same-order robustness:
PASS

G4 Threshold robustness:
PASS

G5 Boundary-invalid robustness:
PASS

G6 Reference-choice robustness:
PASS

G7 Multi-reference robustness:
PASS

G8 Task-level statistics:
PASS

G9 Signal-processing methodology:
PASS

G10 Reproducibility:
PASS

Independent-verifier label flips:
4

Non-unique specifications analyzed:
20

Specifications with independently verified valid/reference-discordant alternatives:
20/20

Same-order specifications with independently verified valid/reference-discordant alternatives:
20/20
(16/16 FIR Type-I same-structure probes + 4/4 IIR same-order library)

Specifications with empirical coefficient-distance non-separability:
20/20

Specifications with empirical response-distance non-separability:
19/20

Singleton-control exact-separation result:
8/8 Suite S tasks have G_r>0 (effectively singleton over the evaluated universe)

Reference-choice robustness:
0/20 tasks become exactly coefficient-separable under any independently verified library reference; all-library G_r min/median/max remain negative

Multi-reference robustness:
K=1,3,5, and all-library: 0/20 tasks exactly separable in coefficient space on the evaluated universe

Boundary-invalid inversion witnesses:
20

Task-macro FRR:
0.900 (task-cluster bootstrap 95% CI [0.871, 0.925]; median 0.907; IQR [0.893, 0.947]; min 0.727; max 0.950)

Pooled descriptive FRR:
370/412 = 0.898 at the illustrative operating point tau=0.05 (canonical magnitude-equivalent coefficient distance; independently verified valids only)

Generated authentic witness survives independent verification:
YES
(9 independently valid generated implementations; all 9 remain S=1, R=0; 4/4 original loose 8 kHz masks)

Scientific status:
STRONG_GO_FOR_MANUSCRIPT_REWRITE

Strongest remaining scientific weakness:
Suite N is still one magnitude-mask family, and all G_r statements remain empirical certificates on a finite independently verified universe rather than continuous-frequency global extrema.

Claims that must NOT be made:
- A global impossibility theorem that no reference-distance oracle can ever evaluate a filter specification
- That 4096- or 131072-point checking certifies the continuous mask
- That tau_R=0.05 is the scientifically distinguished threshold
- That 370/412 is a rate over real-world or generated DSP code
- That 20 tasks represent DSP evaluation in general
- That Suite S proves mathematical uniqueness of the identity maps
- That Oracle C / the independent verifier is an external gold standard beyond the registered numerical contract
- That adding K library references recovers the feasible set (it does not, on this universe)
- That old 374/416 remains the authoritative occupant count (4 firwin2 labels flipped)

Claims now supported:
- A scalar reference-distance threshold classifies a finite evaluated universe exactly iff D_V <= tau < D_I
- On this independently verified universe, G_r <= 0 in coefficient space for 20/20 Suite N tasks, including every library choice of reference and K=1,3,5,all
- Response-space distance fails exact separation on 19/20 tasks
- Same-order / same-structure Type-I probing produces independently verified reference-discordant valids on 16/16 FIR tasks, including tight masks
- Near-boundary independently verified invalids invert the reference-distance order on 20/20 tasks
- Suite S is a positive control: 8/8 tasks are exactly separable when the specification is effectively singleton on the evaluated universe
- The generated-code arm remains an existence witness (9 occupants, 4/4 original masks) after independent revalidation
