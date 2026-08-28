# PHASE 2A — Attack D reaudit

Attack D is the claim that frozen FIR valid/invalid labels are only
grid-local and might flip under a continuous-band certificate.

## Facts after Phase 2A

* Valid→invalid contradictions: 0
* Manuscript constructed FIR valids: 336 unique occupants;
  334 `CERTIFIED_VALID`; 2 `UNDECIDED`;
  0 `CERTIFIED_INVALID`
* FIR headline tasks with 100% constructed-valid certification: 14/16
* FIR headline tasks with ≥95%: 16/16
* Mechanism-invalid FIR: all tested `CERTIFIED_INVALID`
* Boundary-invalid FIR: all tested `CERTIFIED_INVALID`
* Phase-2A certifier independence: `PARTIAL_INDEPENDENCE`
* Remaining UNDECIDED cause: Bernstein resource limit on two \(n=267\) tight bandstops

## Classification

```text
ATTACK_D_PARTIALLY_CLOSED
```

`ATTACK_D_STRONGLY_CLOSED` is not used.

Reasons to close partially rather than claim a full close:

1. Independence is `PARTIAL_INDEPENDENCE` because every method reads the same
   registered \(S_t\) and the same `residual_floor` contract.
2. Two manuscript constructed FIR valids remain `UNDECIDED`. The cause is
   a resource limit, not a suspected violation, but they are not certified.
3. `CERTIFIED_INVALID` on mechanism/boundary FIR uses a conservative
   prime-grid witness. That is a valid invalidity certificate, not the
   Bernstein sign certificate used for validity.
4. Cosine band endpoints use a high-precision outward enclosure, not a
   formal machine-interval cosine.

Reasons it is not left `ATTACK_D_OPEN`:

* Zero valid→invalid contradictions after an independent polynomial-sign method.
* 334/336 constructed FIR valids, and all 16 FIR headline tasks at ≥95%,
  now have continuous Bernstein certificates on the frozen \(S_t\).
* The two UNDECIDED occupants have a specific, non-threatening explanation
  and are not the farthest valids supporting the frozen gap tables.

Phase 2A does not edit the manuscript. IIR certification was not run.
