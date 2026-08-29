# PHASE 3C — Prior art: transfer and conformance

This audit does **not** re-litigate generic set-cover. The question is whether prior work already uses a minimum catalog of conforming reference implementations, selected on one certified universe, then audits transfer and maintenance when additional conforming DSP realizations are admitted.

## Generic prototype transfer

**KNOWN.**

Condensed nearest neighbor (Hart 1968), edited neighbors (Wilson 1972), and the prototype-selection taxonomy (García et al., IEEE TPAMI 2012) already evaluate selected prototypes on held-out labeled samples. Train/test evaluation of prototypes is not novel.

## Conformance-testing preference for specifications

**KNOWN.**

Software-engineering conformance testing compares implementations to a specification rather than to a single reference binary. Wikipedia's reference-implementation discussion and NIST-style conformance suites treat a reference as an interpretation aid, not as the definition of correctness. Independent reimplementation work (e.g. SPE11B specification-conformance studies) shows that tests sharing a code's reading of a specification cannot detect that shared misreading.

## DSP / filter implementation verification

Hardware DSP verification commonly uses a MATLAB/Simulink model as a **golden reference** and checks RTL bit/cycle accuracy (DVCon UVM+dpigen flows; HDL Coder reference RTL; HLS C-vs-MATLAB testbenches). That is the opposite scientific object: one golden realization, not a specification-oracle catalog-burden plus catalog-excluded transfer audit.

## Close DSP work with the same external-validity reference-catalog audit

**NO.**

No DSP/filter paper was found that (i) selects a minimum catalog of specification-valid reference realizations on one frozen certified universe, (ii) freezes that catalog, then (iii) asks whether independently certified additional realizations excluded from selection are accepted, and (iv) measures how much the catalog must grow if they are admitted. Absence of evidence is a boundary, not a priority claim.

## Defensible novelty boundary

Generic prototype transfer and specification-based conformance are known. Close DSP hardware verification uses golden MATLAB references rather than specification-membership catalogs. Phase 3C does **not** convert that literature gap into a transfer result, because the intended Type-I holdout leaked into Phase-3B catalog selection. The remaining manuscript-specific object is still the finite-universe RCC / reference-hierarchy diagnostic, not a new algorithm and not an external-validity theorem.

### Required conclusions

| item | verdict |
| ---- | ------- |
| Generic prototype transfer | KNOWN |
| Conformance-testing preference for specifications | KNOWN |
| Close DSP work with the same external-validity reference-catalog audit | NO |
| Defensible novelty boundary | PARTIAL |
