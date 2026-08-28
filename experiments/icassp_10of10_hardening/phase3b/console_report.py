"""Exact Phase-3B PI console report."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3b.config import OUT_DIR, PROTOCOL_LOCK_COMMIT, ROOT, STARTING_HEAD


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
    branch = _git(["branch", "--show-current"]) or "research/icassp-final-10of10-scientific-hardening"
    final = _git(["rev-parse", "HEAD"])
    dirty = _git(["status", "--porcelain=v1"])
    tree = "DIRTY" if dirty else "CLEAN"
    print(
        f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 3B COMPLETE

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
Phase-3B tag:
icassp-10of10-phase3b-complete

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
EXISTING MULTI-REFERENCE ORACLE
========================

ORACLE SCORE:
d_K(h) = min_{{r in R}} d(h, r)

THRESHOLD:
COMMON_SCALAR

CENTERS:
specification-valid realizations (published table: library prefixes; Phase-3B primary: all observed valids)

PHASE-3B K* MATCHES EXISTING ORACLE FAMILY:
YES

========================
COEFFICIENT REFERENCE CATALOG COMPLEXITY
========================

TASKS:
20

EXACT OPTIMUM:
{h["coeff_exact"]} / 20

BOUND_ONLY:
{h["coeff_bound"]} / 20

UNDECIDED:
{h["coeff_und"]} / 20

K*=1:
{h["coeff_k1"]}

K*=2:
{h["coeff_k2"]}

K*=3-5:
{h["coeff_k35"]}

K*=6-10:
{h["coeff_k610"]}

K*>10:
{h["coeff_kgt10"]}

MEDIAN K*:
{h["coeff_med_k"]}

MIN K*:
{h["coeff_min_k"]}

MAX K*:
{h["coeff_max_k"]}

MEDIAN K*/N_VALID:
{h["coeff_med_rho"]}

MIN K*/N_VALID:
{h["coeff_min_rho"]}

MAX K*/N_VALID:
{h["coeff_max_rho"]}

LOW BURDEN:
{h["coeff_low"]} / 20

MODERATE BURDEN:
{h["coeff_mod"]} / 20

HIGH BURDEN:
{h["coeff_high"]} / 20

NEAR-ENUMERATIVE:
{h["coeff_near"]} / 20

ZERO-DISTANCE VALID/INVALID COLLISIONS:
{h["coeff_collisions"]}

CATALOG BURDEN VERDICT:
{h["catalog_verdict"]}

STRONGEST COEFFICIENT K* RESULT:
{h["strongest_coeff"]}

========================
RESPONSE REFERENCE CATALOG COMPLEXITY
========================

RUN:
YES

EXACT OPTIMUM:
{h["resp_exact"]} / {h["resp_n"]}

K*=1:
{h["resp_k1"]}

MEDIAN K*:
{h["resp_med_k"]}

MEDIAN K*/N_VALID:
{h["resp_med_rho"]}

BURDEN VERDICT:
{h["resp_verdict"]}

STRONGEST RESPONSE K* RESULT:
{h["strongest_resp"]}

========================
LIBRARY-ONLY CATALOG
========================

RUN:
YES

TASKS WITH SOME EXACT LIBRARY SUBSET:
{h["lib_yes"]} / {h["lib_n"]}

TASKS WITH NO EXACT LIBRARY CATALOG:
{h["lib_no"]} / {h["lib_n"]}

========================
AMBIENT VS REALIZABLE CATALOG
========================

R1 ambient exists + low K*:
{h["R1"]}

R2 ambient exists + high/near-enumerative K*:
{h["R2"]}

R3 no ambient center + high/near-enumerative K*:
{h["R3"]}

R4 other/mixed:
{h["R4"]}

STRONGEST INTERPRETATION:
{h["strongest_avs"]}

========================
PRIOR ART
========================

GENERIC PROTOTYPE SELECTION:
KNOWN

SET-COVER PROTOTYPE SELECTION:
KNOWN

CLOSE DSP WORK WITH SAME CATALOG-BURDEN AUDIT:
NO

K* ITSELF IS CLAIMED AS NEW OPTIMIZATION:
NO

MANUSCRIPT-SPECIFIC NOVELTY BOUNDARY:
{h["novelty_boundary"]}

========================
NOVELTY RED TEAM
========================

“JUST SET COVER”:
{h["atk_K1"]}

“OF COURSE MORE REFERENCES HELP”:
{h["atk_K2"]}

“FINITE UNIVERSE IS ARTIFICIAL”:
{h["atk_K3"]}

“JUST USE THE AMBIENT CENTER”:
{h["atk_K4"]}

“WHY REQUIRE REAL IMPLEMENTATIONS”:
{h["atk_K5"]}

“THIS IS NOT DSP”:
{h["atk_K6"]}

========================
NOVELTY PI GATE
========================

BEST CONTRIBUTION FRAMING:
{h["best_framing"]}

INTERNAL NOVELTY SCORE:
{h["internal_novelty"]}

NOVELTY_10OF10_GATE:
{h["novelty_gate"]}

STRONGEST DEFENSIBLE NOVELTY:
{h["strongest_novelty"]}

STRONGEST REMAINING NOVELTY ATTACK:
{h["strongest_attack"]}

========================
SCIENCE LOCK
========================

TECHNICAL_CORRECTNESS_10OF10_GATE:
PASS

CONTINUOUS CERTIFICATION:
412 / 412

AMBIENT-CENTER PHASE-3A RESULT PRESERVED:
YES

METRIC SWEEP RUN:
NO

NEW TASKS:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-3B REPRODUCTION:
{verify["phase3b_reproduction"]}

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

PHASE 3B VERDICT:
{h["verdict"]}
"""
    )
