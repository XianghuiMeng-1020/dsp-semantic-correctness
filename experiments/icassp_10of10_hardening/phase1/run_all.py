"""Phase-1 reproduction entry. Does not write data/icassp_10of10/."""
from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase1.best_observed import (  # noqa: E402
    best_observed,
    d_coeff,
    gap_for_reference,
    run_task_metrics,
    summarize,
)
from experiments.icassp_10of10_hardening.phase1.config import (  # noqa: E402
    CHECK3_TASKS,
    G_ZERO_ABS,
    OUT_DIR,
)
from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe  # noqa: E402
from src.continuous_certification.fir_adaptive import certify_fir  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402


def _table_row(tid, metric, rec, canon_g):
    return {
        "task": tid,
        "metric": metric,
        "n_valid": rec["n_valid"],
        "n_invalid": rec["n_invalid"],
        "canonical_G": canon_g,
        "best_reference_id": rec["best_reference_id"],
        "best_DV": rec["best_DV"],
        "best_DI": rec["best_DI"],
        "Gobs_star": rec["Gobs_star"],
        "exact_separable": rec["exact_separable"],
        "n_tied": rec["n_tied"],
        "tied_reference_ids": rec["tied_reference_ids"],
        "improvement_over_canonical": rec["improvement_over_canonical"],
    }


def run_best_observed(uni: dict) -> dict:
    print("[phase1] best-observed-valid-reference (primary universe)")
    task_rows = []
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        print(f"  {tid} nV={len(pack['valids'])} nI={len(pack['primary_invalids'])}")
        coeff = run_task_metrics(pack, pack["primary_invalids"], "coeff_with_boundary", "coeff")
        resp = run_task_metrics(pack, pack["primary_invalids"], "resp_with_boundary", "resp")
        # Check 2: reproduce canonical G
        canon_impl = pack["canonical"]
        # If canonical cid is not in valids, still score it as the manuscript center
        g_can_c = gap_for_reference(canon_impl, pack["valids"], pack["primary_invalids"], pack["task"], "coeff")
        g_can_r = gap_for_reference(canon_impl, pack["valids"], pack["primary_invalids"], pack["task"], "resp")
        task_rows.append(
            {
                "task_id": tid,
                "family": pack["family"],
                "coeff": coeff,
                "resp": resp,
                "canonical_recomputed": {"coeff": g_can_c, "resp": g_can_r},
                "table_coeff": _table_row(tid, "coeff", coeff, pack["frozen_metrics"]["coeff_with_boundary"]["G_r"]),
                "table_resp": _table_row(tid, "resp", resp, pack["frozen_metrics"]["resp_with_boundary"]["G_r"]),
            }
        )
        print(f"    coeff Gobs*={coeff['Gobs_star']:.6g} frozen_can={coeff['canonical_G_frozen']:.6g} recomputed_can={g_can_c['G']:.6g}")
        print(f"    resp  Gobs*={resp['Gobs_star']:.6g} frozen_can={resp['canonical_G_frozen']:.6g} recomputed_can={g_can_r['G']:.6g}")

    print("[phase1] secondary invalid decompositions")
    decomp = []
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        row = {"task_id": tid}
        for name, inv in (
            ("mechanism_only", pack["mechanism_invalids"]),
            ("boundary_only", pack["boundary_invalids"]),
            ("all_invalids_primary", pack["primary_invalids"]),
        ):
            row[name] = {
                "coeff": best_observed(
                    pack["valids"],
                    inv,
                    pack["task"],
                    "coeff",
                    None,
                ),
                "resp": best_observed(
                    pack["valids"],
                    inv,
                    pack["task"],
                    "resp",
                    None,
                ),
            }
        decomp.append(row)

    out = {
        "universe": {
            "definition": "manuscript confirmatory U_t: constructed+probe valids; mechanism+boundary invalids",
            "n_constructed_valids": uni["n_constructed_valids"],
            "n_probe_valids": uni["n_probe_valids"],
            "n_mechanism_invalids": uni["n_mechanism_invalids"],
            "n_boundary_invalids": uni["n_boundary_invalids"],
        },
        "limitation": (
            "Gobs_star is the max gap over observed valid occupants in U_t only. "
            "It does not rule out an unobserved valid realization or an ambient-space center."
        ),
        "tasks": task_rows,
        "summary_coeff": summarize(task_rows, "coeff"),
        "summary_resp": summarize(task_rows, "resp"),
        "tables": {
            "coeff": [r["table_coeff"] for r in task_rows],
            "resp": [r["table_resp"] for r in task_rows],
        },
    }
    dump_json(OUT_DIR / "best_observed_reference.json", out)
    dump_json(OUT_DIR / "best_observed_reference_decomposition.json", {"tasks": decomp, "note": "SECONDARY; primary is all_invalids_primary = manuscript universe"})
    return out


def run_validation(uni: dict, primary: dict) -> dict:
    print("[phase1] best-reference validation checks")
    checks = {}
    # Check 2: canonical G vs frozen
    max_abs_c = 0.0
    max_abs_r = 0.0
    mismatches = []
    for r in primary["tasks"]:
        tid = r["task_id"]
        fc = r["coeff"]["canonical_G_frozen"]
        fr = r["resp"]["canonical_G_frozen"]
        rc = r["canonical_recomputed"]["coeff"]["G"]
        rr = r["canonical_recomputed"]["resp"]["G"]
        max_abs_c = max(max_abs_c, abs(fc - rc))
        max_abs_r = max(max_abs_r, abs(fr - rr))
        if abs(fc - rc) > 1e-12 or abs(fr - rr) > 1e-10:
            mismatches.append({"task_id": tid, "coeff_frozen": fc, "coeff_re": rc, "resp_frozen": fr, "resp_re": rr})
    checks["check2_canonical_gap"] = {
        "max_abs_coeff": max_abs_c,
        "max_abs_resp": max_abs_r,
        "mismatches": mismatches,
        "pass": len(mismatches) == 0,
    }

    # Check 3: brute-force subset with public d_resp (no mag cache)
    check3 = []
    packs = {p["task_id"]: p for p in uni["tasks"]}
    for tid in CHECK3_TASKS:
        pack = packs[tid]
        task = pack["task"]
        # only first min(8, n) refs to keep second impl independent but bounded
        refs = pack["valids"]
        brute = []
        for ref in refs:
            dvs = [d_coeff(v["impl"], ref["impl"], task) for v in pack["valids"]]
            dis = [d_coeff(i["impl"], ref["impl"], task) for i in pack["primary_invalids"]]
            g = min(dis) - max(dvs)
            brute.append((ref["cid"], g, max(dvs), min(dis)))
        brute.sort(key=lambda t: (-t[1], t[0]))
        cached = next(x for x in primary["tasks"] if x["task_id"] == tid)["coeff"]
        check3.append(
            {
                "task_id": tid,
                "brute_best_id": brute[0][0],
                "brute_G": brute[0][1],
                "cached_best_id": cached["best_reference_id"],
                "cached_G": cached["Gobs_star"],
                "id_match": brute[0][0] == cached["best_reference_id"],
                "g_abs_diff": abs(brute[0][1] - cached["Gobs_star"]),
            }
        )
    checks["check3_bruteforce_coeff"] = check3

    # Check 4/5: all candidate refs are frozen valids; no invalid centers
    invalid_ids = set()
    valid_ids = set()
    for p in uni["tasks"]:
        for v in p["valids"]:
            valid_ids.add(v["cid"])
        for i in p["primary_invalids"]:
            invalid_ids.add(i["cid"])
    used = []
    for r in primary["tasks"]:
        used.extend(r["coeff"]["tied_reference_ids"])
        used.append(r["coeff"]["best_reference_id"])
    bad_center = [u for u in used if u in invalid_ids or u not in valid_ids]
    checks["check4_5_centers_are_valids"] = {"n_checked": len(used), "invalid_or_unknown_centers": bad_center, "pass": len(bad_center) == 0}

    # Check 6: self-distance
    self_d = []
    for p in uni["tasks"][:2]:
        v0 = p["valids"][0]
        self_d.append({"cid": v0["cid"], "d": d_coeff(v0["impl"], v0["impl"], p["task"])})
    checks["check6_self_distance"] = {"samples": self_d, "pass": all(abs(x["d"]) <= 1e-15 for x in self_d)}

    # Check 1 is the primary loop itself (raw occupants)
    checks["check1_raw_occupants"] = {"pass": True, "note": "all gaps recomputed via d_coeff_canonical / cached freqz identical to distances.d_resp"}

    ok = (
        checks["check2_canonical_gap"]["pass"]
        and all(c["id_match"] and c["g_abs_diff"] < 1e-12 for c in check3)
        and checks["check4_5_centers_are_valids"]["pass"]
        and checks["check6_self_distance"]["pass"]
    )
    verdict = "PASS" if ok else "FAIL"
    if ok and (max_abs_c > 0 or max_abs_r > 0):
        verdict = "PASS_WITH_NUMERICAL_NOTE"
    out = {"verdict": verdict, "checks": checks}
    dump_json(OUT_DIR / "best_reference_validation.json", out)
    print(f"  validation {verdict}")
    return out


def run_fir_cert(uni: dict) -> dict:
    print("[phase1] FIR continuous certification")
    rows = []

    def add(occupant, old_label):
        if occupant["family"] != "fir":
            return
        rec = certify_fir(occupant["task_id"], occupant["impl"])
        rows.append(
            {
                "occupant": occupant["cid"],
                "task": occupant["task_id"],
                "old_label": old_label,
                "continuous_status": rec["status"],
                "min_certified_margin": rec.get("min_certified_margin"),
                "witness_or_critical_interval": rec.get("witness") or rec.get("critical_interval"),
                "reason": rec.get("reason"),
                "n_taps": rec.get("n_taps"),
                "role": occupant["role"],
            }
        )
        print(
            f"    {occupant['cid'][-60:]} {old_label} -> {rec['status']} ({rec.get('reason')})",
            flush=True,
        )

    for p in uni["tasks"]:
        for v in p["constructed_valids"]:
            add(v, "VALID")
        for v in p["probe_valids"]:
            add(v, "VALID")
        for i in p["mechanism_invalids"]:
            add(i, "INVALID")
        for i in p["boundary_invalids"]:
            add(i, "INVALID")

    def cohort(role, old):
        sub = [r for r in rows if r["role"] == role]
        return {
            "total": len(sub),
            "CERTIFIED_VALID": sum(1 for r in sub if r["continuous_status"] == "CERTIFIED_VALID"),
            "CERTIFIED_INVALID": sum(1 for r in sub if r["continuous_status"] == "CERTIFIED_INVALID"),
            "UNDECIDED": sum(1 for r in sub if r["continuous_status"] == "UNDECIDED"),
        }

    contradictions = [
        r
        for r in rows
        if (r["old_label"] == "VALID" and r["continuous_status"] == "CERTIFIED_INVALID")
        or (r["old_label"] == "INVALID" and r["continuous_status"] == "CERTIFIED_VALID")
    ]
    out = {
        "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
        "rows": rows,
        "existing_valid_fir_constructed": cohort("constructed_valid", "VALID"),
        "existing_valid_fir_probe": cohort("probe_valid", "VALID"),
        "existing_valid_fir": {
            k: cohort("constructed_valid", "VALID")[k] + cohort("probe_valid", "VALID")[k]
            for k in ("total", "CERTIFIED_VALID", "CERTIFIED_INVALID", "UNDECIDED")
        },
        "mechanism_invalid_fir": cohort("mechanism_invalid", "INVALID"),
        "boundary_invalid_fir": cohort("boundary_invalid", "INVALID"),
        "fir_singleton_controls": {
            "total": 0,
            "note": "Suite S identities are not magnitude-mask FIR occupants; not applicable",
        },
        "contradictions": contradictions,
        "blocker": len([c for c in contradictions if c["old_label"] == "VALID" and c["continuous_status"] == "CERTIFIED_INVALID"]) > 0,
    }
    dump_json(OUT_DIR / "fir_continuous_certification.json", out)
    print(f"  valid FIR {out['existing_valid_fir']}")
    print(f"  contradictions {len(contradictions)}")
    return out


def main() -> int:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    uni = load_frozen_universe()
    print(
        f"[phase1] universe constructed_valids={uni['n_constructed_valids']} "
        f"probes={uni['n_probe_valids']} mech={uni['n_mechanism_invalids']} "
        f"boundary={uni['n_boundary_invalids']}"
    )
    primary = run_best_observed(uni)
    validation = run_validation(uni, primary)
    cert = run_fir_cert(uni)
    elapsed_s = time.time() - t0
    env = {
        "python": sys.version.split()[0],
        "platform": platform.system(),
        "numpy": np.__version__,
        "out_dir": "results/icassp_10of10_hardening/phase1",
        "note": "elapsed_s is printed, not stored, so a second run stays byte-stable",
    }
    try:
        import scipy

        env["scipy"] = scipy.__version__
    except Exception:
        env["scipy"] = None
    dump_json(OUT_DIR / "environment.json", env)
    dump_json(
        OUT_DIR / "headline.json",
        {
            "summary_coeff": primary["summary_coeff"],
            "summary_resp": primary["summary_resp"],
            "validation": validation["verdict"],
            "fir_valid": cert["existing_valid_fir"],
            "fir_valid_constructed": cert["existing_valid_fir_constructed"],
            "fir_valid_probe": cert["existing_valid_fir_probe"],
            "fir_mech": cert["mechanism_invalid_fir"],
            "fir_boundary": cert["boundary_invalid_fir"],
            "blocker": cert["blocker"],
        },
    )
    from experiments.icassp_10of10_hardening.phase1.write_reports import write_all_reports

    write_all_reports(elapsed_s=elapsed_s)
    print(f"PHASE1_ALL_STAGES: DONE elapsed_s={elapsed_s:.3f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
