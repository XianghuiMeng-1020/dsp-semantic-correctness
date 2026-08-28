# PHASE 2A — Denominator reconciliation (412 vs 1596)

Phase 2A may create new certification evidence but may not alter any frozen scientific label or existing manuscript number without subsequent PI review.

This gate was run **before** the power-polynomial certifier was applied to the corpus.

## Verdict

```text
REPORT_LABEL_ISSUE_ONLY
```

Not `MATERIAL_INCONSISTENCY` and not `PHASE2A_DENOMINATOR_BLOCKER`.

`1596` is a different, already documented occupant pool from the manuscript `412`. Phase-1 reports already split constructed vs probe; the Phase-1 console headline `EXISTING-VALID FIR Total: 1596` omitted that split. Old Phase-1 frozen reports are not edited.

## Identities

| Quantity | Identity |
|---|---|
| **412** | Constructed occupants with `independent_label=VALID` in `recertify.json`. Unit: **task × stored file**. FIR+IIR. Unique file paths: 412. |
| **336 / 76** | Of those 412: 336 FIR, 76 IIR. |
| **409/412** | Of those 412 constructed valids, 409 have the old-verifier `near_boundary` flag. Same unit (constructed occupant). Not a Phase-1 FIR-record count. |
| **1260** | Type-I probe occupants with `genuine_same_order` and `independent_ok` in `feasible_probe.json`. All FIR. In confirmatory \(\mathcal{U}_t\) for \(G_r\), **not** in the 412 headline. |
| **1596** | Phase-1 FIR certification **records**: 336 constructed FIR valids + 1260 probe valids. Unique occupant paths: 1596. |
| **78 / 1518** | Phase-1 `CERTIFIED_VALID` / `UNDECIDED` among those 1596 records. |
| **112** | Mechanism-invalid FIR occupants (`recertify` `family=fir`, `independent_label=INVALID`). Unique paths: 112. |
| **128** | Boundary-invalid FIR occupants (`independent_ok=false`). Unique paths: 128. |

Coefficient-vector hashes (binary64 tap bytes) are **fewer** than file counts because some 8 kHz / 16 kHz files store identical taps. Certification remains **per (task, file)** because \(S_t\) is task-specific.

| Cohort | Occupant files | Unique tap hashes |
|---|---:|---:|
| Constructed FIR valid | 336 | 288 |
| Probe valid | 1260 | 515 |
| Mechanism-invalid FIR | 112 | 64 |
| Boundary-invalid FIR | 128 | 64 |

## Required table

| Quantity | Value | Unit actually counted | Unique implementation count | Source |
| -------- | ----: | --------------------- | --------------------------: | ------ |
| 412 | 412 | constructed occupant (task × stored file), FIR+IIR | 412 | `recertify.json` `independent_label=VALID` |
| 409/412 | 409/412 | constructed VALID occupants with `near_boundary=1` | 409 | `recertify.json` `near_boundary` |
| constructed FIR valids (subset of 412) | 336 | constructed FIR occupant (task × stored file) | 336 | `recertify.json` `family=fir` |
| 1596 | 1596 | Phase-1 FIR **record** = constructed FIR valid + probe valid | 1596 | `phase1/fir_continuous_certification.json` |
| 78 Phase-1 CERTIFIED_VALID | 78 | Phase-1 FIR record (constructed+probe) | 78 | Phase-1 `continuous_status` |
| 1518 Phase-1 UNDECIDED | 1518 | Phase-1 FIR record (constructed+probe) | 1518 | Phase-1 `continuous_status` |
| 112 mechanism-invalid FIR | 112 | mechanism-invalid FIR occupant (task × stored file) | 112 | `recertify.json` |
| 128 boundary-invalid FIR | 128 | boundary-invalid FIR occupant (task × stored file) | 128 | `boundary_invalids.json` |

## What Phase 2A will certify

Manuscript-used **unique FIR implementations** for the 412 headline (FIR part):

* 336 constructed FIR valids.

Confirmatory extras (not in 412; already in Phase-1 1596):

* 1260 probe valids, reported **separately**.

Invalids:

* 112 mechanism-invalid FIR;
* 128 boundary-invalid FIR.

Do not treat 1596 as the manuscript valid count. Do not treat unique tap hashes as the implementation count when the same taps are bound to two tasks.
