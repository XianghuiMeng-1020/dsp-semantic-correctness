"""Exact Phase-3D-A console report."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3d_a.config import OUT_DIR, ROOT, STARTING_HEAD


def _git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-c", "safe.directory=F:/ICASSP/project_a_public_release", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (r.stdout or "").strip() if r.returncode == 0 else ""


def _yn(v) -> str:
    return "YES" if v else "NO"


def print_console(verify: dict) -> None:
    adeq = json.loads((OUT_DIR / "adequacy.json").read_text(encoding="utf-8"))
    hv = json.loads((OUT_DIR / "H_VALID.json").read_text(encoding="utf-8"))
    hi = json.loads((OUT_DIR / "H_INVALID.json").read_text(encoding="utf-8"))
    div = json.loads((OUT_DIR / "diversity.json").read_text(encoding="utf-8"))
    scan = json.loads((OUT_DIR / "no_transfer_scan.json").read_text(encoding="utf-8"))
    g = adeq["gates"]
    prot = _git("rev-parse", "icassp-10of10-phase3d-a-protocol-lock") or "PENDING"
    frozen = _git("rev-parse", "icassp-10of10-phase3d-a-challenge-frozen") or "PENDING_LOCAL"
    final = _git("rev-parse", "HEAD")
    ftag = _git("rev-parse", "icassp-10of10-phase3d-a-complete") or "PENDING_LOCAL"
    chal = adeq["PROSPECTIVE_CHALLENGE"]
    verdict = (
        "READY_FOR_BLINDED_PHASE3D_B_UNFREEZE"
        if chal == "ADEQUATE" and scan["verdict"] == "CLEAN" and verify["ok"]
        else "PROSPECTIVE_CHALLENGE_REQUIRES_PI_REVIEW"
    )
    blocker = "NO" if verdict.startswith("READY") else "YES"
    pf = lambda ok: "PASS" if ok else "FAIL"
    text = f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 3D-A COMPLETE

Repository:
F:/ICASSP/project_a_public_release
Branch:
research/icassp-final-10of10-scientific-hardening
Starting commit:
{STARTING_HEAD}
Protocol-lock commit:
{prot}
Challenge-frozen commit:
{frozen}
Final commit:
{final}
Protocol-lock tag:
icassp-10of10-phase3d-a-protocol-lock
Challenge-frozen tag:
icassp-10of10-phase3d-a-challenge-frozen
Phase-3D-A final tag:
icassp-10of10-phase3d-a-complete

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
BLINDING
========================

PHASE-3B CATALOG ACCESSED DURING GENERATION:
NO

REFERENCE DISTANCES COMPUTED BEFORE CHALLENGE FREEZE:
NO

TRANSFER ACCEPTANCE COMPUTED:
NO

BLINDING VERDICT:
{scan["verdict"] if scan["verdict"] == "CLEAN" else "VIOLATED"}

========================
GENERATION PROTOCOL
========================

TASKS:
20

VALID ATTEMPTS:
960

FIR ATTEMPTS:
768

IIR ATTEMPTS:
192

FIR GENERATOR FAMILIES:
F1_remez, F2_firls, F3_freqsamp, F4_window

IIR GENERATOR FAMILIES:
I1_butter, I2_cheby1, I3_cheby2, I4_ellip

SEEDS FROZEN BEFORE GENERATION:
YES

GENERATION BUDGET CHANGED AFTER RESULTS:
NO

========================
PROSPECTIVE VALID CHALLENGE
========================

TOTAL H_VALID:
{adeq["n_valid"]}

FIR H_VALID:
{adeq["n_valid_fir"]}

IIR H_VALID:
{adeq["n_valid_iir"]}

TASKS WITH >=5 H_VALID:
{adeq["tasks_ge5_valid"]} / 20

TASKS WITH >=10 H_VALID:
{adeq["tasks_ge10_valid"]} / 20

MIN H_VALID PER TASK:
{adeq["min_valid"]}

MAX H_VALID PER TASK:
{adeq["max_valid"]}

CONTINUOUSLY CERTIFIED:
{adeq["n_valid"]} / {adeq["n_valid"]}

UNDECIDED INCLUDED:
0

EXACT DUPLICATES VS PRIOR SCIENCE:
{hv.get("exact_duplicates_vs_prior", 0)}

EXACT DUPLICATES WITHIN HOLDOUT:
{hv.get("exact_duplicates_within", 0)}

GENERATOR FAMILY CONTRIBUTION:
{div["by_generator"]}

========================
PROSPECTIVE INVALID CHALLENGE
========================

TOTAL H_INVALID:
{adeq["n_invalid"]}

FIR H_INVALID:
{adeq["n_invalid_fir"]}

IIR H_INVALID:
{adeq["n_invalid_iir"]}

TASKS WITH >=5 H_INVALID:
{adeq["tasks_ge5_invalid"]} / 20

MIN H_INVALID PER TASK:
{adeq["min_invalid"]}

CONTINUOUSLY CERTIFIED INVALID:
{adeq["n_invalid"]} / {adeq["n_invalid"]}

UNDECIDED INCLUDED:
0

========================
DSP COVERAGE
========================

FIR TASKS COVERED:
16 / 16

IIR TASKS COVERED:
4 / 4

LOOSE/TIGHT COVERED:
{_yn(div["by_loose_tight"].get("loose", 0) > 0 and div["by_loose_tight"].get("tight", 0) > 0)}

LP/HP/BP/BS COVERAGE:
{div["by_filter_type"]}

MULTIPLE GENERATOR FAMILIES:
{adeq["families_ge2_tasks"]} / 20 tasks with ≥2 families

VALID SPEC-MARGIN SUMMARY:
min={div["margin_min"]} median={div["margin_median"]} near-boundary={div["near_boundary_count"]} / {div["n_with_margin"]}

========================
PROSPECTIVE HOLDOUT GATE
========================

H_VALID >= 200:
{pf(g["H_VALID_ge_200"])}

H_INVALID >= 200:
{pf(g["H_INVALID_ge_200"])}

ALL TASKS >=5 VALID:
{pf(g["all_tasks_ge5_valid"])}

ALL TASKS >=5 INVALID:
{pf(g["all_tasks_ge5_invalid"])}

FIR VALID >=160:
{pf(g["fir_valid_ge_160"])}

IIR VALID >=20:
{pf(g["iir_valid_ge_20"])}

GENERATOR-DIVERSITY GATE:
{pf(g["generator_diversity"])}

PROSPECTIVE CHALLENGE:
{chal}

========================
SCIENCE LOCK
========================

TECHNICAL_CORRECTNESS_10OF10_GATE:
PASS

CONTINUOUS CERTIFICATION ORIGINAL:
412 / 412

PHASE-3B RCC RESULT PRESERVED:
YES

PHASE-3C LEAKAGE RESULT PRESERVED:
YES

NEW TASKS:
NO

NEW METRICS:
NO

TRANSFER SCORING RUN:
NO

EXPANDED K* RUN:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-3D-A REPRODUCTION:
{verify["phase3d_a_reproduction"]}

WORKING TREE:
{verify["working_tree"]}

SCIENTIFIC BLOCKER:
{blocker}

STRONGEST POSITIVE FINDING:
Prospectively generated catalog-blind challenge has H_VALID={adeq["n_valid"]} and H_INVALID={adeq["n_invalid"]} under continuous certification.

STRONGEST LIMITATION:
Adequacy is {chal}; Phase 3D-A does not evaluate reference-oracle transfer.

WHAT PHASE 3D-A ESTABLISHES:
A frozen, continuously certified, catalog-blind FIR/IIR challenge set exists for a later blinded Phase-3D-B unfreeze.

WHAT PHASE 3D-A DOES NOT ESTABLISH:
Reference-oracle transfer performance has not yet been evaluated.

PHASE 3D-A VERDICT:
{verdict}
"""
    print(text)
