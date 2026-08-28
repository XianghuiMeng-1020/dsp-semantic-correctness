"""Phase-2A reproduction. Does not write data/icassp_10of10 or Phase-1 JSON."""
from __future__ import annotations

import json
import platform
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.denominator import reconcile  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.extremum import audit_occupant  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.occupants import (  # noqa: E402
    load_manuscript_fir_occupants,
    load_phase1_status,
)
from src.continuous_certification.fir_power_polynomial import certify_fir  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402

PROBE_FULL_CERT_MAX_TAPS = 80
CROSSCHECK_CIDS = []


def _n_taps(impl) -> int:
    if isinstance(impl, dict):
        return int(np.asarray(impl.get("b", impl.get("h"))).size)
    return int(np.asarray(impl).size)


def _cohort_summary(rows: list[dict]) -> dict:
    c = Counter(r["phase2a_status"] for r in rows)
    return {
        "total_unique_occupants": len(rows),
        "unique_cids": len({r["occupant"] for r in rows}),
        "CERTIFIED_VALID": c.get("CERTIFIED_VALID", 0),
        "CERTIFIED_INVALID": c.get("CERTIFIED_INVALID", 0),
        "UNDECIDED": c.get("UNDECIDED", 0),
        "coverage": (c.get("CERTIFIED_VALID", 0) / len(rows)) if rows else None,
    }


def _run_one(occ: dict, phase1: dict, full_cert: bool) -> dict:
    cid, tid = occ["cid"], occ["task_id"]
    if not full_cert:
        rec = certify_fir(tid, occ["impl"])
        # certify_fir always does full Bernstein; skip by wrapping below
    rec = certify_fir(tid, occ["impl"])
    return {
        "occupant": cid,
        "task": tid,
        "role": occ["role"],
        "old_label": occ["old_label"],
        "n_taps": rec.get("n_taps"),
        "phase1_status": phase1.get(cid),
        "phase2a_status": rec["status"],
        "reason": rec.get("reason"),
        "witness_or_critical": rec.get("witness") or rec.get("band"),
        "degree": rec.get("degree"),
        "method": rec.get("method"),
    }


def _run_one_maybe_capped(occ: dict, phase1: dict, max_taps: int | None) -> dict:
    n = _n_taps(occ["impl"])
    if max_taps is not None and n > max_taps:
        # still allow a witness-only path by calling certify_fir: it witnesses first.
        # For long probes, Bernstein after a clean witness is the cost. Use a
        # dedicated witness-only if we import... keep it simple: run full for
        # manuscript; cap probes by skipping Bernstein via a light wrapper.
        from src.continuous_certification.fir_power_polynomial import (
            _as_fir_taps,
            _eff_bounds,
            _load_task,
            _witness_invalid,
        )

        task = _load_task(occ["task_id"])
        h = _as_fir_taps(occ["impl"])
        fs = float(task["sampling_rate"])
        floor = float(task["residual_floor"])
        wit = None
        for band in list(task["pass_band"]) + list(task["stop_band"]):
            L, U = _eff_bounds(float(band["lo"]), float(band["hi"]), floor)
            from fractions import Fraction as _F

            w = _witness_invalid(h, float(band["f0"]), float(band["f1"]), fs, L if L > 0 else _F(0), U)
            if w is not None:
                wit = w
                break
        status = "CERTIFIED_INVALID" if wit else "UNDECIDED"
        reason = "witnessed_violation" if wit else "polynomial_arithmetic_resource_limit"
        return {
            "occupant": occ["cid"],
            "task": occ["task_id"],
            "role": occ["role"],
            "old_label": occ["old_label"],
            "n_taps": n,
            "phase1_status": phase1.get(occ["cid"]),
            "phase2a_status": status,
            "reason": reason,
            "witness_or_critical": wit,
            "degree": n - 1,
            "method": "witness_only_resource_cap",
        }
    return _run_one(occ, phase1, True)


def run_certification() -> dict:
    print("[phase2a] load occupants", flush=True)
    packs = load_manuscript_fir_occupants()
    phase1 = load_phase1_status()
    all_rows = []

    def go(name, items, cap=None):
        print(f"[phase2a] certify {name} n={len(items)}", flush=True)
        rows = []
        for i, occ in enumerate(items, 1):
            rec = _run_one_maybe_capped(occ, phase1, cap)
            rows.append(rec)
            all_rows.append(rec)
            print(
                f"    {i}/{len(items)} {occ['cid'][-70:]} {rec['old_label']} "
                f"P1={rec['phase1_status']} P2A={rec['phase2a_status']} ({rec['reason']})",
                flush=True,
            )
        return rows

    constructed = go("constructed_valid_fir", packs["constructed_valid"])
    mech = go("mechanism_invalid_fir", packs["mechanism_invalid"])
    bound = go("boundary_invalid_fir", packs["boundary_invalid"])
    probes = go("probe_valid_confirmatory", packs["probe_valid_confirmatory"], PROBE_FULL_CERT_MAX_TAPS)

    contradictions = [
        r
        for r in constructed + probes
        if r["old_label"] == "VALID" and r["phase2a_status"] == "CERTIFIED_INVALID"
    ]
    xtab = {}
    for r in constructed:
        a, b = r["phase1_status"] or "ABSENT", r["phase2a_status"]
        xtab.setdefault(a, {"CERTIFIED_VALID": 0, "CERTIFIED_INVALID": 0, "UNDECIDED": 0})
        xtab[a][b] += 1

    # per-task coverage on constructed valids only
    tasks = {}
    for r in constructed:
        tasks.setdefault(r["task"], []).append(r)
    task_table = []
    for tid, rs in sorted(tasks.items()):
        n = len(rs)
        cv = sum(1 for x in rs if x["phase2a_status"] == "CERTIFIED_VALID")
        ci = sum(1 for x in rs if x["phase2a_status"] == "CERTIFIED_INVALID")
        ud = sum(1 for x in rs if x["phase2a_status"] == "UNDECIDED")
        task_table.append(
            {
                "task": tid,
                "frozen_valid_count": n,
                "certified_valid": cv,
                "contradicted": ci,
                "undecided": ud,
                "coverage": cv / n if n else None,
            }
        )

    out = {
        "method": "squared-magnitude Chebyshev polynomial; Bernstein sign on x=cos ω",
        "arithmetic": "exact IEEE-754 binary64 rationals for taps; JSON spec as binary64; Bernstein over Fraction",
        "certificate_type": "RIGOROUS_POLYNOMIAL_SIGN",
        "limitation": (
            "Frequency endpoints use an outward cosine enclosure. "
            "Probe occupants with n_taps>80 use witness-only (resource). "
            "Manuscript unique FIR valids are the 336 constructed FIR files."
        ),
        "existing_valid_fir_constructed": _cohort_summary(constructed),
        "existing_valid_fir_probe_confirmatory": _cohort_summary(probes),
        "mechanism_invalid_fir": _cohort_summary(mech),
        "boundary_invalid_fir": _cohort_summary(bound),
        "contradictions_valid_to_invalid": contradictions,
        "blocker": len(contradictions) > 0,
        "phase1_vs_phase2a_constructed": xtab,
        "task_coverage_constructed": task_table,
        "rows": all_rows,
    }
    dump_json(OUT_DIR / "fir_power_polynomial_certification.json", out)
    return out


def run_crosscheck(cert: dict) -> dict:
    print("[phase2a] extremum cross-check", flush=True)
    packs = load_manuscript_fir_occupants()
    by_cid = {o["cid"]: o for group in packs.values() for o in group}
    picks = []
    # prescribed kinds from constructed rows
    want = [
        ("fir_lp_loose_8k", "loose_lp"),
        ("fir_lp_tight_8k", "tight_lp"),
        ("fir_hp_loose_8k", "hp"),
        ("fir_bp_loose_8k", "bp"),
        ("fir_bs_loose_8k", "bs"),
    ]
    constructed = [r for r in cert["rows"] if r["role"] == "constructed_valid"]
    # shortest / longest
    constructed_sorted = sorted(constructed, key=lambda r: r.get("n_taps") or 0)
    selected = []
    if constructed_sorted:
        selected.append(("shortest", constructed_sorted[0]))
        selected.append(("longest", constructed_sorted[-1]))
    for tid, tag in want:
        hit = next((r for r in constructed if r["task"] == tid), None)
        if hit:
            selected.append((tag, hit))
    # Phase-1 UNDECIDED that Phase-2A resolved, and some remaining
    p1u = [r for r in constructed if r["phase1_status"] == "UNDECIDED"][:4]
    for r in p1u:
        selected.append(("phase1_undecided", r))
    bounds = [r for r in cert["rows"] if r["role"] == "boundary_invalid"][:3]
    for r in bounds:
        selected.append(("boundary_invalid", r))

    audits = []
    seen = set()
    for tag, r in selected:
        if r["occupant"] in seen:
            continue
        seen.add(r["occupant"])
        occ = by_cid.get(r["occupant"])
        if not occ:
            continue
        rec = audit_occupant(r["task"], occ["impl"])
        rec["tag"] = tag
        rec["occupant"] = r["occupant"]
        rec["phase2a_status"] = r["phase2a_status"]
        audits.append(rec)
        print(f"    {tag} {r['occupant'][-50:]} viol={rec['n_violating_grid_or_stat']}", flush=True)
    out = {"audits": audits, "n": len(audits)}
    dump_json(OUT_DIR / "extremum_crosscheck.json", out)
    return out


def main() -> int:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    denom = reconcile()
    dump_json(OUT_DIR / "denominator.json", denom)
    print(f"[phase2a] denominator {denom['verdict']} blocker={denom['blocker']}", flush=True)
    if denom["blocker"]:
        print("PHASE2A_DENOMINATOR_BLOCKER", flush=True)
        return 2
    cert = run_certification()
    if cert["blocker"]:
        print("PHASE2A_VALIDITY_CONTRADICTION_BLOCKER", flush=True)
        dump_json(OUT_DIR / "headline.json", {"blocker": True, "contradictions": cert["contradictions_valid_to_invalid"]})
        from experiments.icassp_10of10_hardening.phase2a.write_reports import write_all_reports

        write_all_reports()
        return 3
    xcheck = run_crosscheck(cert)
    env = {
        "python": sys.version.split()[0],
        "platform": platform.system(),
        "numpy": np.__version__,
        "out_dir": "results/icassp_10of10_hardening/phase2a",
        "note": "elapsed_s printed only",
    }
    dump_json(OUT_DIR / "environment.json", env)
    dump_json(
        OUT_DIR / "headline.json",
        {
            "denominator": denom["verdict"],
            "constructed": cert["existing_valid_fir_constructed"],
            "probe": cert["existing_valid_fir_probe_confirmatory"],
            "mech": cert["mechanism_invalid_fir"],
            "boundary": cert["boundary_invalid_fir"],
            "blocker": cert["blocker"],
            "n_contradictions": len(cert["contradictions_valid_to_invalid"]),
            "xtab": cert["phase1_vs_phase2a_constructed"],
            "task_coverage": cert["task_coverage_constructed"],
            "crosscheck_n": xcheck["n"],
        },
    )
    from experiments.icassp_10of10_hardening.phase2a.write_reports import write_all_reports

    write_all_reports()
    print(f"PHASE2A_ALL_STAGES: DONE elapsed_s={time.time()-t0:.3f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
