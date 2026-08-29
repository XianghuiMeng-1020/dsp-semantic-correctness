# PHASE 0 — Construction–verifier independence

## Dependency map

```text
registry/suite_{n,s}.json
        │
        ├── src/spec_checker.py          FREQZ_N=4096, no refine, tf freqz
        │         ▲
        │         └── search_checker.py  thin wrap (construction only)
        │                   ▲
        │                   ├── src/valid_designers.py
        │                   ├── src/valid_first_principles.py
        │                   ├── src/mutants.py
        │                   └── random-valid search (pipeline)
        │
        └── src/verification/registry_io.py   separate loader, same JSON
                  └── independent_spec_verifier.py
                            N_f=131072, extrema refine, IIR SOS
                            imports canonicalize, NOT spec_checker
```

Shared (not code-identical):

* Task JSON: bands, `residual_floor` (FIR \(10^{-6}\), IIR \(10^{-3}\)), pole 0.999
* Residual formula: \(\max(\mathrm{below},\mathrm{above})/(\mathrm{hi}-\mathrm{lo})\)
* SciPy `freqz` / `tf2zpk` / numpy
* Pass/stop role heuristic `lo >= 0.5`

Not shared:

* Import graph (verifier does not import `spec_checker`)
* Grid density; local `minimize_scalar` refinement; IIR `tf2sos`+`sosfreqz`
* Direct DFT `_mag_fir_scalar` at refined frequencies
* Suite S identities reimplemented in `_verify_singleton` (parallel code, same tests)

Construction of random-valids uses **only** the 4096 checker.
Final labels use **only** the independent verifier.

Four `firwin2` tight occupants: search residual 0, independent residual
\(7.8\times 10^{-3}\)–\(1.6\times 10^{-2}\). That disagreement is real.

### Q1 — Could one bug make both agree incorrectly?

**Yes.** A wrong band edge or floor in the registry, or a shared SciPy
`freqz` error on the same samples, could fool both. A bug only in
`spec_checker` is what the four flips already catch.

### Q2 — Same mask-evaluation function?

**No.** Separate functions. Same mathematical residual definition.

### Q3 — Identical grid points?

**No.** 4096 vs 131072. Construction has no refinement.

### Q4 — Same tolerance policy?

**Yes, by registry.** Same `residual_floor` and pole bound.

### Q5 — Does “independent” survive a strict reviewer?

**Partially.** Independent *implementation* of a *shared contract*.
Not an independently derived gold standard, not a second lab, not a
continuous proof. The paper already says this in Discussion.

### Q6 — Were the four flips from truly independent logic?

**Yes, as implementations.** They are exactly the cases the 4096-point
grid missed at a band edge. They are not evidence of independence from
the *registered floors*.

## Verdict

```text
PARTIAL_INDEPENDENCE
```

Not `STRONG`: shared contract, shared residual formula, shared SciPy.
Not `WEAK` / `NOT_INDEPENDENT`: no import of the construction checker;
different grid; documented label flips.
