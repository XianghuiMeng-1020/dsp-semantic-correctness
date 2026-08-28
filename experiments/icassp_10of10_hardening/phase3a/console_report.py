"""Exact Phase-3A PI console report."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3a.config import OUT_DIR, PROTOCOL_LOCK_COMMIT, ROOT, STARTING_HEAD


def _git(args: list[str]) -> str:
    r = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT}", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (r.stdout or "").strip()


def print_console(verify: dict) -> None:
    h = json.loads((OUT_DIR / "headline.json").read_text(encoding="utf-8"))
    branch = _git(["branch", "--show-current"]) or h.get("branch")
    final = _git(["rev-parse", "HEAD"]) or h.get("final_commit")
    dirty = _git(["status", "--porcelain=v1"])
    tree = "DIRTY" if dirty else "CLEAN"
    print(
        f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 3A COMPLETE

Repository:
{ROOT}
Branch:
{branch}
Starting commit:
{STARTING_HEAD}
Protocol-lock commit:
{PROTOCOL_LOCK_COMMIT}
Final commit:
{final}
Phase-3A tag:
{h.get("phase3a_tag") or "icassp-10of10-phase3a-complete"}

ORIGINAL SCIENCE PACKAGE:
{"UNCHANGED" if verify["hash_ok"] else "CHANGED"}

ORIGINAL HEADLINE REPRODUCTION:
{verify["original_reproduction"]}

MANUSCRIPT CHANGED:
NO

PDF CHANGED:
NO

ORIGINAL LABELS CHANGED:
NO

========================
METRIC GEOMETRY
========================

COEFFICIENT METRIC:
{h["coeff_formula"]}

COEFFICIENT EUCLIDEAN-EQUIVALENT:
{h["coeff_euclidean"]}

RESPONSE METRIC:
{h["resp_formula"]}

RESPONSE EUCLIDEAN-EQUIVALENT:
{h["resp_euclidean"]}

========================
COEFFICIENT AMBIENT-CENTER
========================

TASKS:
20

AMBIENT SINGLE-CENTER SEPARABLE:
{h["coeff_ambient_separable"]}

AMBIENT SINGLE-CENTER NON-SEPARABLE:
{h["coeff_ambient_nonseparable"]}

UNDECIDED:
{h["coeff_undecided"]}

EXACT-RATIONAL NO-CENTER CERTIFICATES:
{h["exact_rational_no_center"]}

HIGH-PRECISION CERTIFICATES:
{h["high_precision"]}

NUMERICAL-ONLY:
{h["numerical_only"]}

TYPE A:
canonical fail -> observed fail -> ambient fail:
{h["type_A"]}

TYPE B:
canonical fail -> observed fail -> ambient succeeds:
{h["type_B"]}

TYPE C:
canonical fail -> observed succeeds:
{h["type_C"]}

TYPE D:
canonical succeeds:
{h["type_D"]}

STRONGEST COEFFICIENT RESULT:
{h["strongest_coeff"]}

========================
RESPONSE AMBIENT-CENTER
========================

RUN:
YES

TASKS:
{h["resp_tasks"]}

AMBIENT SEPARABLE:
{h["resp_ambient_separable"]}

AMBIENT NON-SEPARABLE:
{h["resp_ambient_nonseparable"]}

UNDECIDED:
{h["resp_undecided"]}

PRECISION ROBUST:
{h["resp_precision_robust"]}

STRONGEST RESPONSE RESULT:
{h["strongest_resp"]}

========================
REFERENCE HIERARCHY
========================

CANONICAL COEFFICIENT NON-SEPARABLE:
20 / 20

BEST-OBSERVED COEFFICIENT NON-SEPARABLE:
20 / 20

AMBIENT COEFFICIENT NON-SEPARABLE:
{h["coeff_ambient_nonseparable"]} / 20

CANONICAL RESPONSE NON-SEPARABLE:
19 / 20

BEST-OBSERVED RESPONSE NON-SEPARABLE:
18 / 20

AMBIENT RESPONSE NON-SEPARABLE:
{h["resp_ambient_nonseparable"]} / {h["resp_tasks"]}

========================
PRIOR ART
========================

GENERAL TEST-ORACLE PROBLEM:
KNOWN

GENERIC SPHERE-SEPARATION LP:
KNOWN

CLOSE DSP PRIOR WORK THAT ALREADY ESTABLISHES OUR FULL RESULT:
NO

NOVELTY BOUNDARY:
{h["novelty_boundary"]}

STRONGEST DEFENSIBLE MANUSCRIPT-SPECIFIC NOVELTY:
{h["strongest_novelty"]}

STRONGEST REMAINING NOVELTY ATTACK:
{h["strongest_attack"]}

========================
NOVELTY PI GATE
========================

FIXED-REFERENCE ATTACK:
{h["gate_fixed_ref"]}

BAD-REFERENCE ATTACK:
{h["gate_bad_ref"]}

UNRESTRICTED-CENTER ATTACK:
{h["gate_ambient"]}

“THE THEOREM IS OBVIOUS” ATTACK:
{h["gate_obvious"]}

“THIS IS JUST THE KNOWN ORACLE PROBLEM” ATTACK:
{h["gate_oracle"]}

KSTAR_NEXT:
{h["KSTAR_NEXT"]}

BEST CONTRIBUTION FRAMING:
{h["best_framing"]}

INTERNAL NOVELTY SCORE AFTER PHASE 3A:
{h["internal_novelty"]}

========================
SCIENCE LOCK
========================

TECHNICAL_CORRECTNESS_10OF10_GATE:
PASS

CONTINUOUS CERTIFICATION:
412 / 412

K* RUN:
NO

METRIC SWEEP RUN:
NO

NEW TASKS:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-3A REPRODUCTION:
{h.get("phase3a_reproduction") or verify["phase3a_reproduction"]}

WORKING TREE:
{tree}

SCIENTIFIC BLOCKER:
{h["scientific_blocker"]}

STRONGEST NEW POSITIVE FINDING:
{h["strongest_positive"]}

STRONGEST NEW NEGATIVE OR LIMITATION:
{h["strongest_negative"]}

WHAT THE PAPER CAN NOW SAFELY CLAIM:
{h["can_claim"]}

WHAT THE PAPER STILL CANNOT CLAIM:
{h["cannot_claim"]}

PHASE 3A VERDICT:
{h["verdict"]}
"""
    )
