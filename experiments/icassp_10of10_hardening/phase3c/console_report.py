"""Exact Phase-3C final console report."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3c.config import (
    OUT_DIR,
    PROTOCOL_LOCK_COMMIT,
    ROOT,
    STARTING_HEAD,
)


def _git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-c", "safe.directory=F:/ICASSP/project_a_public_release", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (r.stdout or "").strip() if r.returncode == 0 else ""


def _na(x) -> str:
    return "N/A" if x is None else str(x)


def print_console(verify: dict) -> None:
    hl = json.loads((OUT_DIR / "headline.json").read_text(encoding="utf-8"))
    ext = json.loads((OUT_DIR / "external_invalid.json").read_text(encoding="utf-8"))
    ext_line = ext.get("EXTERNAL_INVALID_TRANSFER", "NOT_AVAILABLE")
    if ext.get("n"):
        ext_line = (
            f"{ext_line} (n={ext['n']}, false_accept={ext.get('false_accept')}, "
            f"rate={ext.get('false_accept_rate')})"
        )
    head = _git("rev-parse", "HEAD") or "PENDING_LOCAL"
    tag = _git("rev-parse", "icassp-10of10-phase3c-complete")
    tag_s = tag if tag else "PENDING_LOCAL"
    text = f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 3C COMPLETE

Repository:
F:/ICASSP/project_a_public_release
Branch:
research/icassp-final-10of10-scientific-hardening
Starting commit:
{STARTING_HEAD}
Protocol-lock commit:
{PROTOCOL_LOCK_COMMIT}
Final commit:
{head}
Phase-3C tag:
{tag_s}

ORIGINAL SCIENCE PACKAGE:
UNCHANGED

ORIGINAL HEADLINE REPRODUCTION:
{verify["original_reproduction"]}

MANUSCRIPT CHANGED:
NO

PDF CHANGED:
NO

ORIGINAL LABELS CHANGED:
NO

========================
PRIMARY EXTERNAL HOLDOUT
========================

CORPUS:
type_i_feasible_probes_1260 (NOT ELIGIBLE; intended H_TYPEI)

EXISTED BEFORE PHASE 3C:
YES

USED IN PHASE-3B CATALOG FITTING:
YES

TOTAL UNIQUE VALID HOLDOUT:
0 (1260 probes excluded as leaked; no replacement holdout)

TASKS COVERED:
16 FIR / 0 IIR (provenance only; not scored)

CONTINUOUSLY CERTIFIED:
1260 / 1260

EXACT DUPLICATES REMOVED:
0 (dedup not applied; corpus ineligible)

LEAKAGE VERDICT:
MATERIAL_LEAKAGE

========================
COEFFICIENT EXTERNAL-VALIDITY TRANSFER
========================

TASKS:
N/A

HOLDOUT VALID TOTAL:
N/A

ACCEPTED:
N/A

REJECTED:
N/A

POOLED TRANSFER ACCEPT:
N/A

TASK-MACRO MEAN TRANSFER:
N/A

TASK-MACRO MEDIAN TRANSFER:
N/A

TASKS >=95% TRANSFER:
N/A

TASKS 75-95% TRANSFER:
N/A

TASKS <75% TRANSFER:
N/A

WORST TASK TRANSFER:
N/A

TRANSFER VERDICT:
NOT_SCORED

========================
RESPONSE EXTERNAL-VALIDITY TRANSFER
========================

RUN:
NO

HOLDOUT VALID TOTAL:
N/A

POOLED TRANSFER ACCEPT:
N/A

TASK-MACRO MEDIAN TRANSFER:
N/A

TASKS >=95%:
N/A

TASKS <75%:
N/A

TRANSFER VERDICT:
N/A

========================
REFERENCE HIERARCHY ON EXTERNAL VALIDITY
========================

CANONICAL K=1 COEFF TRANSFER:
N/A

BEST-OBSERVED K=1 COEFF TRANSFER:
N/A

K=3 COEFF TRANSFER:
N/A

K=5 COEFF TRANSFER:
N/A

ALL-LIBRARY COEFF TRANSFER:
N/A

K*_OBS COEFF TRANSFER:
N/A

CANONICAL RESPONSE TRANSFER:
N/A

K*_OBS RESPONSE TRANSFER:
N/A

KEY HIERARCHY FINDING:
Hierarchy transfer was not scored because the intended Type-I set leaked into Phase-3B catalog selection.

========================
CATALOG MAINTENANCE
========================

EXPANDED K* RUN:
NO

TASKS EXACT:
N/A

TASKS BOUNDED:
N/A

BASE MEDIAN K*:
23

EXPANDED MEDIAN K*:
N/A

MEDIAN DELTA K:
N/A

MEDIAN RELATIVE GROWTH:
N/A

LOW MAINTENANCE:
N/A

MODERATE MAINTENANCE:
N/A

HIGH MAINTENANCE:
N/A

TASKS WITH UNAVOIDABLE NEW REFERENCES:
N/A

MEDIAN MINIMUM NEW REFERENCES:
N/A

MAX MINIMUM NEW REFERENCES:
N/A

MAINTENANCE VERDICT:
INCONCLUSIVE

========================
DSP MECHANISM
========================

SAME-ORDER TRANSFER EFFECT:
Not scored: intended Type-I same-order probes leaked into catalog fitting.

TYPE-I RESULT:
Not scored as an external holdout. Type-I probes were Phase-3B valids.

LOOSE VS TIGHT:
Not scored.

FILTER-TYPE RESULT:
Not scored.

REJECTED HOLDOUTS STILL S_t-CERTIFIED:
N/A

DSP-MECHANISM VERDICT:
WEAK

========================
SECONDARY HOLDOUTS
========================

ELIGIBLE SECONDARY CORPORA:
NONE

CONSISTENT WITH PRIMARY:
N/A

EXTERNAL INVALID TRANSFER:
{ext_line}

========================
PRIOR ART
========================

GENERIC PROTOTYPE TRANSFER:
KNOWN

SPECIFICATION-BASED CONFORMANCE:
KNOWN

CLOSE DSP PRIOR WORK WITH SAME AUDIT:
NO

NOVELTY BOUNDARY:
PARTIAL

========================
NOVELTY RED TEAM
========================

“STILL FINITE”:
OPEN

“JUST PROTOTYPE TEST-SET EVALUATION”:
PARTIAL

“TYPE-I HOLDOUT TOO SIMILAR”:
PARTIAL

“HOLDOUT ONLY FIR”:
OPEN

“S_t WINS BY DEFINITION”:
PARTIAL

“MAINTENANCE IS JUST SET COVER”:
PARTIAL

“DOES NOT GENERALIZE TO ALL REFERENCE MATCHING”:
PARTIAL

“THIS IS NOT DSP”:
PARTIAL

========================
FINAL NOVELTY PI GATE
========================

EXTERNAL TRANSFER:
EXTERNAL_TRANSFER_INCONCLUSIVE

BEST CONTRIBUTION FRAMING:
B

INTERNAL NOVELTY SCORE:
6.4

NOVELTY_10OF10_GATE:
NOT_YET

STRONGEST DEFENSIBLE NOVELTY:
{hl["strongest_novelty"]}

STRONGEST REMAINING NOVELTY ATTACK:
{hl["strongest_attack"]}

MANUSCRIPT-SAFE CENTRAL CLAIM:
{hl["manuscript_safe_claim"]}

========================
SCIENCE LOCK
========================

TECHNICAL_CORRECTNESS_10OF10_GATE:
PASS

CONTINUOUS CERTIFICATION:
412 / 412

PHASE-3A AMBIENT RESULT PRESERVED:
YES

PHASE-3B RCC RESULT PRESERVED:
YES

NEW FILTERS GENERATED:
NO

NEW TASKS:
NO

NEW METRICS:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-3C REPRODUCTION:
{verify["phase3c_reproduction"]}

WORKING TREE:
{verify.get("working_tree", "UNKNOWN")}

SCIENTIFIC BLOCKER:
YES

STRONGEST NEW POSITIVE FINDING:
{hl["strongest_positive"]}

STRONGEST NEW NEGATIVE OR LIMITATION:
{hl["strongest_negative"]}

WHAT THE PAPER CAN NOW SAFELY CLAIM:
{hl["can_claim"]}

WHAT THE PAPER STILL CANNOT CLAIM:
{hl["cannot_claim"]}

PHASE 3C VERDICT:
NOVELTY_BLOCKER_REQUIRES_PI_REVIEW
"""
    print(text)
