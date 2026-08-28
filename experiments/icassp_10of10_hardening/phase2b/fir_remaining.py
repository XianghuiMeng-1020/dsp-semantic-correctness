"""Resolve the two Phase-2A UNDECIDED constructed FIRs by Sturm sign."""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase2b.config import PREVIOUSLY_UNDECIDED_FIR
from src.continuous_certification.mask_sign import certify_fir_sturm
from src.verification.io_utils import load_impl


def resolve() -> dict:
    rows = []
    for item in PREVIOUSLY_UNDECIDED_FIR:
        impl = load_impl(item["cid"])
        rec = certify_fir_sturm(item["task_id"], impl)
        status = rec["status"]
        if status == "CERTIFIED_VALID":
            verdict = "CERTIFIED_VALID"
        elif status == "CERTIFIED_INVALID":
            verdict = "CERTIFIED_INVALID"
        else:
            verdict = "STILL_UNDECIDED"
        rows.append(
            {
                "occupant": item["cid"],
                "task": item["task_id"],
                "phase2a_status": "UNDECIDED",
                "phase2b_status": verdict,
                "reason": rec.get("reason"),
                "n_taps": rec.get("n_taps"),
                "degree": rec.get("degree"),
                "method": rec.get("method"),
                "bands": rec.get("bands"),
            }
        )
        print(f"[phase2b] FIR remaining {item['cid'][-60:]} -> {verdict} ({rec.get('reason')})", flush=True)
    n_valid = sum(1 for r in rows if r["phase2b_status"] == "CERTIFIED_VALID")
    n_invalid = sum(1 for r in rows if r["phase2b_status"] == "CERTIFIED_INVALID")
    n_und = sum(1 for r in rows if r["phase2b_status"] == "STILL_UNDECIDED")
    return {
        "method": "exact rational P(x); primitive-integer Sturm sequence; sign on root-free intervals",
        "previously_undecided": 2,
        "CERTIFIED_VALID": n_valid,
        "CERTIFIED_INVALID": n_invalid,
        "STILL_UNDECIDED": n_und,
        "blocker": n_invalid > 0,
        "constructed_fir_valid_final": {
            "CERTIFIED_VALID": 334 + n_valid,
            "CERTIFIED_INVALID": n_invalid,
            "UNDECIDED": n_und,
            "total": 336,
            "coverage": (334 + n_valid) / 336,
        },
        "rows": rows,
    }
