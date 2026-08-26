# PHASE 0 — Experimental generalization

## Matrix (what was actually measured)

| Axis | Present? | Notes |
|---|---|---|
| FIR vs IIR | yes | 16 FIR, 4 IIR |
| Loose vs tight | yes | mechanical ×1/5; 8+8 FIR, 2+2 IIR |
| LP / HP / BP / BS | FIR yes; IIR only LP/HP | no IIR BP/BS |
| \(f_s\) 8 / 16 kHz | FIR yes; IIR 8 kHz only | |
| Order | free in \(S_t\); same-order **probe** on FIR | order is not part of \(S_t\) |
| Same-order alternatives | FIR Type-I LP; IIR library only | IIR weaker |
| Design families | firwin/remez/firls/firwin2; butter/cheby/ellip; sinc/freq-samp; random | |
| Magnitude constraints | **only** | free transition |
| Phase / group-delay | no | explicitly not in \(S_t\) |
| Coefficient identity | Suite S only | 8 tasks |
| Generated-code witnesses | 9 occupants, 4 loose 8 kHz masks | not a rate |

## What the evidence supports

**Strongest claim justified without new experiments:**

On this one family of independently labeled FIR/IIR **magnitude masks**
(20 instances) and this finite evaluated universe, a scalar
coefficient-distance threshold on a library reference does not recover
\(S_t\), nor does a finite library catalog, nor do same-order Type-I
FIR probes; a response-distance threshold fails on 19/20; the same
gap is positive on eight singleton identities. That is an evaluation
result about **mask-feasible sets vs realization balls**, not about
DSP correctness in general.

## Overclaim risk

Title and abstract say “DSP implementations.” Discussion correctly
narrows to one mask family. Reviewers who stop at the title will
read a broader claim than the design supports.

```text
GENERALIZATION BOUNDARY: OVERCLAIMED
```

(in title/abstract only; body is closer to CLEAR)

## Smallest new experiment that would help most

**Not** a new LLM arm. **Not** a 50-task mask sweep.

One of:

1. Per-task \(G^*\) over evaluated valids as candidate \(r\) (no new
   occupants; closes “bad reference”).
2. Adaptive FIR remainder on the 412 valids, reported as
   CERTIFIED / UNDECIDED / REFUTED (closes circular-grid attack).
3. **One** extra \(S_t\) variant on the existing 16 FIR masks:
   “Type-I + current length” as part of the spec — only if the PI
   wants to show the diagnostic still applies when the feasible set
   shrinks. Higher scope creep than (1)–(2).

Do not run these in Phase 0.
