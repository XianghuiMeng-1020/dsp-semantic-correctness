# PHASE 0 — Margin audit

Labels were **not** changed. Occupant files were **not** rewritten.
All figures below are computed from **already stored** independent-verifier
fields in `data/icassp_10of10/recertify.json` and
`boundary_invalids.json`, plus the registered `residual_floor`.

Interior unused slack (how far a VALID occupant sits *inside* the
mask) is **not stored** except via the boolean `near_boundary`.
Recomputing a new slack field would be a Phase 1 measurement; it
was not run.

## Residual-to-floor signed margin

Valid: \(\mathrm{margin}= \mathrm{floor}-\max(\mathrm{pass},\mathrm{stop},\mathrm{stab},\mathrm{other})\).
Invalid: \(\mathrm{violation}= \max(\cdot)-\mathrm{floor}\).

| Cohort | n | min | p1 | p5 | median | \(\lvert\cdot\rvert<10^{-4}\) | \(<10^{-6}\) | \(<10^{-8}\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Independently VALID constructed | 412 | \(10^{-6}\) | \(10^{-6}\) | \(10^{-6}\) | \(10^{-6}\) | 336 | 0 | 0 |
| Mechanism INVALID (violation) | 144 | 0.999 | 2.04 | 4.40 | 19.3 | 0 | 0 | 0 |
| Boundary INVALID (violation) | 160 | \(\approx 0.009\) (IIR) / \(0.020\) (FIR) | — | — | — | 0 | 0 | 0 |
| Label flips (violation) | 4 | \(7.76\times 10^{-3}\) | same | same | \(1.18\times 10^{-2}\) | 0 | 0 | 0 |

FIR floor is \(10^{-6}\); IIR floor is \(10^{-3}\). 336/412 valids are
FIR with **zero** measured residual, so margin equals the FIR floor.
That is distance to the **decision threshold**, not to the mask wall.

Linear \(|H|\) violation stored as `worst_*_abs` on the 412 valids:
max \(9.4\times 10^{-17}\) (4 IIR numerical crumbs). None within
\(10^{-8}\) of a **violating** wall on the refined grid.

## Verifier `near_boundary` flag (existing)

Defined in `independent_spec_verifier.py` as closeness to a wall
within \(\max(10\cdot\mathrm{slack}, 10^{-5})\).

| Cohort | near_boundary |
|---|---|
| Independently VALID | **409 / 412** |
| Mechanism invalid | (flag used; not the headline) |
| Boundary invalid | **160 / 160** (by construction) |

409/412 valids are therefore flagged as living within about \(10^{-5}\)
in linear \(|H|\) of some active constraint, even though their
**normalized residual is 0**. Continuous certification is more likely
to return `UNDECIDED` or a rare `REFUTED` on this majority than to
rubber-stamp them.

## Mechanism vs boundary invalids

Mechanism mutants are far from the floor (median violation \(\sim 19\)).
Re-label risk: **negligible**.

Boundary mutants are independently INVALID with minimum residual
0.010 (IIR, floor 0.001) or 0.020 (FIR, floor \(10^{-6}\)).
Re-label risk: **low**. They exist to make \(D_I\) small, not to sit
on the knife-edge of \(S_t\).

## Singleton controls

`singleton.json`: 12 independently OK, 16 not. Residuals are 0 or 1
on exact identities. Boundary-margin language does not apply.

## Risk verdict

```text
MODERATE
```

Invalids (mechanism + boundary + flips) are not ambiguous under the
current residual. Valids have zero refined-grid residual but
**almost all** carry `near_boundary=1`. A Lipschitz/adaptive cert
is therefore likely to **confirm invalids** and to **leave many
valids uncertified or occasionally refuted**, which is exactly the
Phase 1 question. Headlines are not currently known to be wrong;
they are **uncertified at the mask wall**.
