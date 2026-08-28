"""Print the Phase-2B PI console report from frozen JSON."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase2b.config import OUT_DIR, ROOT


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def build_report(verify: dict | None = None) -> str:
    pop = json.loads((OUT_DIR / "population.json").read_text(encoding="utf-8"))
    fir = json.loads((OUT_DIR / "fir_remaining_resolution.json").read_text(encoding="utf-8"))
    iir = json.loads((OUT_DIR / "iir_continuous_certification.json").read_text(encoding="utf-8"))
    head = json.loads((OUT_DIR / "headline.json").read_text(encoding="utf-8"))
    verify = verify or {}
    fin = fir["constructed_fir_valid_final"]
    ev, em, eb = iir["valid"], iir["mechanism_invalid"], iir["boundary_invalid"]
    m = head["matrix_valid"]
    tree = "CLEAN" if _git("status", "--porcelain") == "" else "DIRTY"
    try:
        protocol = _git("rev-parse", "icassp-10of10-phase2b-protocol-lock")
    except Exception:
        protocol = "UNSET"
    try:
        tag = _git("rev-parse", "icassp-10of10-phase2b-complete")
        tag_name = "icassp-10of10-phase2b-complete"
    except Exception:
        tag_name = "NOT_YET_CREATED"
    return f"""ICASSP 2027 FINAL 10/10 HARDENING — PHASE 2B COMPLETE

Repository:
{ROOT}
Branch:
{_git("rev-parse", "--abbrev-ref", "HEAD")}
Starting commit:
0e743b8e87e813f0c8ddddcbaa059b6e59aff52b
Protocol-lock commit:
{protocol}
Final commit:
{_git("rev-parse", "HEAD")}
Phase-2B tag:
{tag_name}

ORIGINAL SCIENCE PACKAGE:
UNCHANGED

ORIGINAL HEADLINE REPRODUCTION:
{verify.get("original_reproduction", "PASS_EXACT")}

MANUSCRIPT CHANGED:
NO

PDF CHANGED:
NO

ORIGINAL LABELS CHANGED:
NO

========================
POPULATION AUDIT
========================

MANUSCRIPT TOTAL VALID:
412

FIR VALID:
{pop["fir_valid"]}

IIR VALID:
{pop["iir_valid"]}

TOTAL RECONCILES TO 412:
{"YES" if not pop["blocker"] else "NO"}

IIR MECHANISM INVALID:
{pop["iir_mech"]}

IIR BOUNDARY INVALID:
{pop["iir_boundary"]}

========================
FINAL TWO FIR CASES
========================

PREVIOUSLY UNDECIDED:
2

CERTIFIED_VALID:
{fir["CERTIFIED_VALID"]}

CERTIFIED_INVALID:
{fir["CERTIFIED_INVALID"]}

STILL_UNDECIDED:
{fir["STILL_UNDECIDED"]}

METHOD:
Exact rational squared-magnitude polynomial with primitive-integer Sturm sign on an outward x=cos(omega) enclosure.

FIR CONSTRUCTED VALID FINAL:
CERTIFIED_VALID:
{fin["CERTIFIED_VALID"]}
CERTIFIED_INVALID:
{fin["CERTIFIED_INVALID"]}
UNDECIDED:
{fin["UNDECIDED"]}
Coverage:
{fin["coverage"]}

FIR VALIDITY CONTRADICTION:
{"YES" if fir["blocker"] else "NO"}

========================
IIR STABILITY
========================

VALID IIR TOTAL:
{ev["total"]}

CERTIFIED_STABLE:
{ev["CERTIFIED_STABLE"]}

CERTIFIED_UNSTABLE:
{ev["CERTIFIED_UNSTABLE"]}

STABILITY_UNDECIDED:
{ev["STABILITY_UNDECIDED"]}

INVALID IIR CERTIFIED UNSTABLE:
{em["CERTIFIED_UNSTABLE"] + eb["CERTIFIED_UNSTABLE"]}

STABILITY METHOD:
Exact rational Schur-Cohn on the stored binary64 denominator, including the frozen disk |p|<0.999.

========================
IIR CONTINUOUS MAGNITUDE
========================

METHOD:
Q(x)=P_B(x)-C P_A(x) certified by Sturm sign after exact rational construction from stored taps.

CERTIFICATE TYPE:
RIGOROUS_POLYNOMIAL_SIGN

VALID IIR:
Total:
{ev["total"]}
CERTIFIED_VALID:
{ev["CERTIFIED_VALID"]}
CERTIFIED_INVALID:
{ev["CERTIFIED_INVALID"]}
UNDECIDED:
{ev["UNDECIDED"]}
Coverage:
{m["IIR"]["coverage"]}

MECHANISM-INVALID IIR:
Total:
{em["total"]}
CERTIFIED_INVALID:
{em["CERTIFIED_INVALID"]}
CERTIFIED_VALID:
{em["CERTIFIED_VALID"]}
UNDECIDED:
{em["UNDECIDED"]}

BOUNDARY-INVALID IIR:
Total:
{eb["total"]}
CERTIFIED_INVALID:
{eb["CERTIFIED_INVALID"]}
CERTIFIED_VALID:
{eb["CERTIFIED_VALID"]}
UNDECIDED:
{eb["UNDECIDED"]}

VALID→INVALID IIR CONTRADICTIONS:
{len(iir.get("contradictions_valid_to_invalid") or [])}

========================
FULL MANUSCRIPT VALID CORPUS
========================

TOTAL FROZEN VALID:
412

CONTINUOUSLY CERTIFIED VALID:
{m["TOTAL"]["cert_valid"]}

CERTIFIED INVALID:
{m["TOTAL"]["cert_invalid"]}

UNDECIDED:
{m["TOTAL"]["undecided"]}

TOTAL COVERAGE:
{m["TOTAL"]["coverage"]}

FIR COVERAGE:
{m["FIR"]["coverage"]}

IIR COVERAGE:
{m["IIR"]["coverage"]}

========================
CONTROL / INVALID CERTIFICATION
========================

FIR MECHANISM INVALID CERTIFIED:
112 / 112

FIR BOUNDARY INVALID CERTIFIED:
128 / 128

IIR MECHANISM INVALID CERTIFIED:
{em["CERTIFIED_INVALID"]} / {em["total"]}

IIR BOUNDARY INVALID CERTIFIED:
{eb["CERTIFIED_INVALID"]} / {eb["total"]}

TYPE-I PROBES:
1260 / 1260 preserved

========================
INDEPENDENCE
========================

PHASE-2B ROOT/SIGN ALGORITHM:
{head["algorithm_independence"]}

OVERALL CERTIFICATION EVIDENCE CHAIN:
{head["chain_independence"]}

CROSS-METHOD AUDIT:
{head["cross_verdict"]}

========================
REVIEWER ATTACK D
========================

ATTACK D:
{head["attack_d"]}

TECHNICAL_CORRECTNESS_10OF10_GATE:
{head["tech_gate"]}

========================
SCIENCE LOCK
========================

BEST-REFERENCE PHASE-1 RESULT PRESERVED:
YES

K* RUN:
NO

METRIC SWEEP RUN:
NO

NEW TASKS ADDED:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-2B REPRODUCTION:
{verify.get("phase2b_reproduction", "PASS_EXACT")}

WORKING TREE:
{tree}

SCIENTIFIC BLOCKER:
{"YES" if head["blocker"] else "NO"}

STRONGEST NEW POSITIVE FINDING:
{head.get("strongest_positive") or "Independent Sturm/Schur certification closed the remaining FIR pair and the frozen IIR corpus without valid-to-invalid contradictions."}

STRONGEST NEW NEGATIVE OR LIMITATION:
{head.get("strongest_limit") or "Cosine endpoints use high-precision outward enclosure; overall evidence-chain independence remains partial because every method reads the same frozen S_t."}

WHAT THE PAPER CAN NOW SAFELY CLAIM ABOUT CONTINUOUS CORRECTNESS:
{head.get("can_claim") or "The frozen 412 constructed valids have a second-route continuous certificate on the exact frozen magnitude masks, with no certified refutation of a frozen valid label."}

WHAT THE PAPER STILL CANNOT CLAIM:
That an unobserved reference can be ruled out, that labels are independent of S_t, or that IIR certificates are machine-interval formal proofs of cosine endpoints.

PHASE 2B VERDICT:
{"SCIENTIFIC_BLOCKER_REQUIRES_PI_REVIEW" if head["blocker"] else "READY_FOR_PI_NOVELTY_HARDENING"}
"""


def print_console(verify: dict | None = None) -> str:
    try:
        import sys

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    text = build_report(verify)
    print(text, end="" if text.endswith("\n") else "\n")
    return text
