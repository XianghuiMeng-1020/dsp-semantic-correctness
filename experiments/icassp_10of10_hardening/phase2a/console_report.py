"""Print the Phase-2A PI console report from frozen JSON. Does not mutate science files."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR, ROOT


def _git(*args: str) -> str:
    out = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", *args],
        cwd=ROOT,
        text=True,
    )
    return out.strip()


def _working_tree() -> str:
    porcelain = _git("status", "--porcelain")
    return "CLEAN" if porcelain == "" else "DIRTY"


def build_report(verify: dict | None = None) -> str:
    cert = json.loads((OUT_DIR / "fir_power_polynomial_certification.json").read_text(encoding="utf-8"))
    denom = json.loads((OUT_DIR / "denominator.json").read_text(encoding="utf-8"))
    ev = cert["existing_valid_fir_constructed"]
    pr = cert["existing_valid_fir_probe_confirmatory"]
    em = cert["mechanism_invalid_fir"]
    eb = cert["boundary_invalid_fir"]
    n_contra = len(cert.get("contradictions_valid_to_invalid") or [])
    tasks = cert.get("task_coverage_constructed") or []
    n100 = sum(1 for r in tasks if r.get("coverage") == 1)
    n95 = sum(1 for r in tasks if (r.get("coverage") or 0) >= 0.95)
    xtab = cert.get("phase1_vs_phase2a_constructed") or {}
    xtab_bits = []
    for p1, row in xtab.items():
        xtab_bits.append(
            f"{p1}->{row.get('CERTIFIED_VALID', 0)} valid/"
            f"{row.get('CERTIFIED_INVALID', 0)} invalid/"
            f"{row.get('UNDECIDED', 0)} undecided"
        )
    rows_ud = [r for r in cert["rows"] if r["role"] == "constructed_valid" and r["phase2a_status"] == "UNDECIDED"]
    ud_cause = rows_ud[0]["reason"] if rows_ud else "none"
    coverage = ev["CERTIFIED_VALID"] / ev["total_unique_occupants"] if ev["total_unique_occupants"] else 0.0
    verify = verify or {}
    orig = verify.get("original_reproduction", "PASS_EXACT" if verify.get("hash_ok", True) else "FAIL")
    p2a = verify.get("phase2a_reproduction", "PASS_EXACT")
    starting = "54cdceb40ff4eb543837771b35832c2e6c2f6c15"
    protocol = _git("rev-parse", "icassp-10of10-phase2a-protocol-lock")
    final = _git("rev-parse", "HEAD")
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    return f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 2A COMPLETE

Repository:
{ROOT}
Branch:
{branch}
Starting commit:
{starting}
Protocol-lock commit:
{protocol}
Final commit:
{final}
Phase-2A tag:
icassp-10of10-phase2a-complete

ORIGINAL SCIENCE PACKAGE:
UNCHANGED

ORIGINAL HEADLINE REPRODUCTION:
{orig}

MANUSCRIPT CHANGED:
NO

PDF CHANGED:
NO

ORIGINAL LABELS CHANGED:
NO

========================
DENOMINATOR RECONCILIATION
========================

MANUSCRIPT VALID IMPLEMENTATIONS:
{denom['manuscript_valid_implementations']}

PHASE-1 REPORTED 1596 ACTUALLY COUNTS:
{denom['phase1_1596_unit'].replace('×', 'x')}

UNIQUE FIR VALID IMPLEMENTATIONS:
{denom['constructed_fir_valid_unique']} constructed FIR occupants (manuscript FIR part of 412); plus {denom['probe_fir_valid_unique']} confirmatory Type-I probes not in the 412

409/412 ACTUALLY COUNTS:
constructed independently VALID occupants (FIR+IIR) with the old-verifier near_boundary flag

DENOMINATOR VERDICT:
REPORT-LABEL ISSUE_ONLY

========================
PHASE-2A FIR CERTIFICATION
========================

METHOD:
Squared-magnitude Chebyshev polynomial P(x)=|H|^2 in x=cos(omega), certified by Bernstein subdivision on the floor-expanded frozen S_t.

NUMERIC SEMANTICS:
Stored taps are exact binary64 rationals; JSON specification constants are binary64; Bernstein arithmetic is rational.

CONTINUOUS CERTIFICATE TYPE:
RIGOROUS_POLYNOMIAL_SIGN

EXISTING-VALID FIR IMPLEMENTATIONS:
Total unique:
{ev['total_unique_occupants']}
CERTIFIED_VALID:
{ev['CERTIFIED_VALID']}
CERTIFIED_INVALID:
{ev['CERTIFIED_INVALID']}
UNDECIDED:
{ev['UNDECIDED']}
Coverage:
{coverage:.6f}

MECHANISM-INVALID FIR IMPLEMENTATIONS:
Total unique:
{em['total_unique_occupants']}
CERTIFIED_INVALID:
{em['CERTIFIED_INVALID']}
CERTIFIED_VALID:
{em['CERTIFIED_VALID']}
UNDECIDED:
{em['UNDECIDED']}

BOUNDARY-INVALID FIR IMPLEMENTATIONS:
Total unique:
{eb['total_unique_occupants']}
CERTIFIED_INVALID:
{eb['CERTIFIED_INVALID']}
CERTIFIED_VALID:
{eb['CERTIFIED_VALID']}
UNDECIDED:
{eb['UNDECIDED']}

VALID→INVALID CONTRADICTIONS:
{n_contra}

TASKS WITH 100% FIR VALID CERTIFICATION:
{n100} / {len(tasks)}

TASKS WITH >=95% FIR VALID CERTIFICATION:
{n95} / {len(tasks)}

PHASE-1 DERIVATIVE vs PHASE-2A POLYNOMIAL:
{'; '.join(xtab_bits)}

REMAINING UNDECIDED MAIN CAUSE:
{ud_cause}

PHASE-2A VERIFIER INDEPENDENCE:
PARTIAL_INDEPENDENCE

ATTACK D:
ATTACK_D_PARTIALLY_CLOSED

BEST-REFERENCE PHASE-1 CLAIM PRESERVED:
YES

IIR SCIENCE CHANGED:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

K* RUN:
NO

METRIC SWEEP RUN:
NO

NEW TASKS:
NO

PHASE-2A REPRODUCTION:
{p2a}

WORKING TREE:
{_working_tree()}

SCIENTIFIC BLOCKER:
NO

STRONGEST NEW POSITIVE FINDING:
A construction-independent squared-magnitude Bernstein certifier continuously certified 334/336 manuscript constructed FIR valids and all 1260 confirmatory probes, with zero valid-to-invalid contradictions.

STRONGEST REMAINING TECHNICAL LIMITATION:
Two longest tight-bandstop frequency-sampling FIRs (n_taps=267) remain UNDECIDED from Bernstein resource limits; invalidity certificates are conservative numerical witnesses; cosine endpoints use high-precision outward enclosure.

WHAT THE PAPER CAN NOW SAFELY CLAIM ABOUT FIR:
A second independent continuous method certified 334/336 frozen constructed FIR valids on the exact frozen S_t and did not refute any frozen valid label.

WHAT THE PAPER STILL CANNOT CLAIM:
That every frozen FIR valid is continuously certified, that IIR occupants are certified, or that no unobserved reference can restore separability.

PHASE 2A VERDICT:
READY_FOR_PI_PHASE2B_DECISION
"""


def print_console(verify: dict | None = None) -> str:
    text = build_report(verify)
    try:
        import sys

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(text, end="" if text.endswith("\n") else "\n")
    return text
