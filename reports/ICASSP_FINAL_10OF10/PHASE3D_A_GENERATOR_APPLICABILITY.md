# PHASE 3D-A — Generator applicability

Inspected frozen Suite N tasks and public design APIs only. Phase-3B catalog geometry was not inspected.

## Task facts used

- All 20 tasks: `order_constraint=free`, magnitude mask \(S_t\).
- IIR additionally: `pole_radius_max=0.999`.
- Existing scientific search ranges: odd FIR \(n\in[21,401]\), IIR order \(\in[2,12]\).
- This protocol uses a non-extreme locked subset (see protocol lock).

## FIR families vs 16 FIR tasks

| Family | lp/hp loose | lp/hp tight | bp/bs loose | bp/bs tight | verdict |
|---|---|---|---|---|---|
| F1 Remez | applicable | applicable | applicable | applicable | used 12/task |
| F2 firls | applicable | applicable | applicable | applicable | used 12/task |
| F3 frequency-sampling | applicable | applicable | applicable | applicable | used 12/task |
| F4 firwin2 / windowed-sinc | applicable | applicable | applicable | applicable | used 12/task |

No FIR family is `NOT_APPLICABLE`. Historical occupant yields (e.g. some `firwin2` tight bp/bs library occupants failed independent certification) are **not** used to drop a family. Failed attempts stay in the log.

IIR design routes are `NOT_APPLICABLE` on FIR tasks.

## IIR families vs 4 IIR tasks

All four Suite N IIR tasks are lp/hp. `filter_geom.iir_btype` supports those only.

| Family | iir_lp_loose_8k | iir_lp_tight_8k | iir_hp_loose_8k | iir_hp_tight_8k |
|---|---|---|---|---|
| I1 Butterworth | applicable | applicable | applicable | applicable |
| I2 Chebyshev I | applicable | applicable | applicable | applicable |
| I3 Chebyshev II | applicable | applicable | applicable | applicable |
| I4 elliptic | applicable | applicable | applicable | applicable |

No redistribution. FIR families are `NOT_APPLICABLE` on IIR tasks.

## First-principles frequency-sampling

`src/first_principles_fir.py` and `freqsamp_at` read registry band edges only. They do not load catalog IDs.
