# PHASE 3B — Prior art: prototype selection

Generic prototype / set-cover selection is **not** claimed as novel.

| Source | What is already known | What it does NOT establish | Relation |
| ------ | --------------------- | -------------------------- | -------- |
| Hart, *The Condensed Nearest Neighbor Rule*, IEEE Trans. Information Theory 1968 | Condensing a 1-NN training set | Not a DSP specification-oracle diagnostic | Ancestor of prototype reduction |
| Wilson, *Asymptotic Properties of Nearest Neighbor Rules Using Edited Data*, IEEE Trans. SMC 1972 | Editing neighbors | Same | Edition, not catalog burden for filter specs |
| García, Derrac, Cano, Herrera, *Prototype Selection for Nearest Neighbor Classification: Taxonomy and Empirical Study*, IEEE TPAMI 34(3):417–435, 2012 | Taxonomy of condensation / edition / hybrid prototype selection; large empirical NN study | Accuracy/reduction on UCI-style data, not exact recovery of a specification predicate on DSP masks | Standard survey. Do not claim to introduce prototype selection. |
| Pekalska & Duin, *The Dissimilarity Representation for Pattern Recognition* (World Scientific, 2005) | Representation sets / dissimilarity spaces | Not DSP verification | Related geometry of “which prototypes represent a class” |
| Bien & Tibshirani, *Prototype Selection for Interpretable Classification*, Ann. Appl. Stat. 2011 | Interpretable prototype classifiers | Not specification vs realization oracles | Different success criterion |
| Marchand & Shawe-Taylor, *The Set Covering Machine*, JMLR 2002 | Set-cover formulations for conjunction classifiers | Not filter-mask membership | Confirms set-cover as a known learning reduction |
| Class-cover catch-digit / Cannon–Cowen class-cover literature | Covering one class while excluding another | Pattern recognition, not DSP correctness evaluation | Same combinatorial shape; different scientific object |

## Known already

- Prototype selection and generation for nearest-neighbor classifiers.
- Set-cover / class-cover as a way to pick a small set of representatives.
- That adding more prototypes can improve a nearest-prototype rule.

## Not a defensible novelty claim

“We introduce set-cover selection of references.”

## Potentially manuscript-specific

Using the **exact minimal catalog size** of *observed specification-valid DSP realizations* as an adequacy/burden measure for whether the paper’s existing min-distance / common-threshold reference oracle can stand in for specification-defined FIR/IIR correctness on a frozen independently labeled universe.

No prior DSP verification paper was found that reports this same diagnostic (minimum valid prototype catalog required to reproduce a specification-oracle membership table on FIR/IIR masks). Absence of evidence is a boundary, not a priority claim.
