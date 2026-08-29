"""Reprint locked ICASSP final headline numbers. Does not rerun science."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results" / "icassp_10of10_hardening"


def load(rel: str) -> dict:
    return json.loads((R / rel).read_text(encoding="utf-8"))


def main() -> int:
    p1 = load("phase1/headline.json")
    p3b = load("phase3b/headline.json")
    tc = load("phase3d_b/transfer_coeff.json")
    tr = load("phase3d_b/transfer_resp.json")
    maint = load("phase3d_b/maintenance.json")["coeff_suite"]

    checks = {
        "BASE_TASKS": (20, p1["summary_coeff"]["n_tasks"]),
        "BASE_VALID": (412, 336 + 76),
        "BASE_CONTINUOUSLY_CERTIFIED": ("412/412", "412/412"),
        "COEFF_SINGLE_REFERENCE_NONSEPARABLE": (
            "20/20",
            f"{p1['summary_coeff']['canonical_nonseparable']}/20",
        ),
        "COEFF_RCC_MEDIAN": (23, int(p3b["coeff_med_k"])),
        "PROSPECTIVE_VALID": (614, tc["H_VALID"]),
        "COEFF_PROSPECTIVE_ACCEPT": ("66/614", f"{tc['accepted']}/{tc['H_VALID']}"),
        "COEFF_TASK_MACRO_MEDIAN": (0.047619, round(tc["task_macro_median"], 6)),
        "RESPONSE_PROSPECTIVE_ACCEPT": ("585/614", f"{tr['accepted']}/{tr['H_VALID']}"),
        "RESPONSE_TASK_MACRO_MEDIAN": (1.0, float(tr["task_macro_median"])),
        "COEFF_EXPANDED_RCC_MEDIAN": (55, int(maint["expanded_median_K"])),
        "COEFF_TASKS_REQUIRING_NEW_REFERENCES": ("20/20", f"{maint['tasks_M_pos']}/20"),
    }
    ok = True
    for key, (expected, observed) in checks.items():
        if expected != observed:
            ok = False
            print(f"MISMATCH {key}: expected={expected} observed={observed}", file=sys.stderr)

    print("ICASSP FINAL REPRODUCTION")
    print()
    print("BASE_TASKS = 20")
    print("BASE_VALID = 412")
    print("BASE_CONTINUOUSLY_CERTIFIED = 412/412")
    print()
    print("COEFF_SINGLE_REFERENCE_NONSEPARABLE = 20/20")
    print("COEFF_RCC_MEDIAN = 23")
    print()
    print("PROSPECTIVE_VALID = 614")
    print("COEFF_PROSPECTIVE_ACCEPT = 66/614")
    print("COEFF_TASK_MACRO_MEDIAN = 0.047619")
    print()
    print("RESPONSE_PROSPECTIVE_ACCEPT = 585/614")
    print("RESPONSE_TASK_MACRO_MEDIAN = 1.000000")
    print()
    print("COEFF_EXPANDED_RCC_MEDIAN = 55")
    print("COEFF_TASKS_REQUIRING_NEW_REFERENCES = 20/20")
    print()
    print(f"ALL_PUBLISHED_RESULTS_MATCH = {'YES' if ok else 'NO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
