#!/usr/bin/env python3
"""Phase 2B: constructed valid occupants for Suite N.

Admission: S_t(h)=1 only. Distance to the canonical reference is measured
after admission. No mutant generation. No FRR/FAR evaluation tables.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.filter_geom import is_fir  # noqa: E402
from src.first_principles_fir import assert_no_scipy_design_in  # noqa: E402
from src.spec_checker import check_specification, get_task  # noqa: E402
from src.valid_designers import (  # noqa: E402
    design_canonical,
    generate_library,
    random_attempt,
)
from src.valid_first_principles import generate_first_principles  # noqa: E402
from src.valid_metrics import (  # noqa: E402
    TAU_R,
    d_coeff,
    distance_to_reference,
    is_near_duplicate,
    unpack,
)

SEED = 20260826
RANDOM_TARGET = 15
RANDOM_CAP = 400
LOW_OCCUPANCY = 8
OUT = ROOT / "data" / "valid"
TAU_R_DEFAULT = TAU_R


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [float(v) for v in np.asarray(x, float).reshape(-1)]
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return None if not math.isfinite(v) else v
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    return x


def _load_suite_n():
    payload = json.loads((ROOT / "registry" / "suite_n.json").read_text(encoding="utf-8"))
    return payload["tasks"]


def _save_impl(path: Path, impl):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(impl, dict) and "b" in impl:
        np.savez(path.with_suffix(".npz"), b=np.asarray(impl["b"], float), a=np.asarray(impl["a"], float))
        return path.with_suffix(".npz")
    np.save(path.with_suffix(".npy"), np.asarray(impl, float))
    return path.with_suffix(".npy")


def _stem(rec: dict, serial: int) -> str:
    tid = rec["task_id"]
    src = rec["source"]
    method = rec["method"]
    if src == "random":
        return f"{tid}__r{serial:03d}"
    if src == "first_principles":
        variant = rec["parameters"].get("variant", "shortest")
        return f"{tid}__{method}__{variant}"
    if src == "canonical":
        return f"{tid}__canonical"
    return f"{tid}__{method}"


def _subdir(source: str) -> Path:
    return OUT / source


def _checker_impl(impl):
    return impl


def _dedup_keep(rec, accepted: list[dict], fs: float) -> bool:
    for prev in accepted:
        if is_near_duplicate(rec["impl"], prev["impl"], fs):
            return False
    return True


def _manifest_row(rec: dict, path: Path, href, task: dict) -> dict:
    chk = check_specification(task["task_id"], rec["impl"])
    dist = distance_to_reference(rec["impl"], href, task)
    row = {
        "task_id": rec["task_id"],
        "source": rec["source"],
        "method": rec["method"],
        "parameters": _jsonable(rec["parameters"]),
        "S_t": bool(chk["pass"]),
        "label": "valid-by-construction",
        "distance_to_reference": dist,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "residuals": chk["residuals"],
    }
    b, a = unpack(rec["impl"])
    if a is None:
        row["n_taps"] = int(len(b))
    else:
        row["n_b"] = int(len(b))
        row["n_a"] = int(len(a))
    return row


def generate_random(task: dict, rng: np.random.Generator, accepted: list[dict]) -> tuple[list[dict], dict]:
    rows = []
    attempts = 0
    n_dup = 0
    while len(rows) < RANDOM_TARGET and attempts < RANDOM_CAP:
        attempts += 1
        impl, params = random_attempt(rng, task)
        if impl is None:
            continue
        rec = {
            "task_id": task["task_id"],
            "source": "random",
            "method": params.get("method", "random"),
            "parameters": params,
            "impl": impl,
            "label": "valid-by-construction",
        }
        if not _dedup_keep(rec, accepted + rows, float(task["sampling_rate"])):
            n_dup += 1
            continue
        rows.append(rec)
    log = {
        "attempts": attempts,
        "accepted": len(rows),
        "duplicates_skipped": n_dup,
        "low_occupancy": len(rows) < LOW_OCCUPANCY,
    }
    return rows, log


def _task_stats(rows: list[dict]) -> dict:
    if not rows:
        return {
            "n": 0,
            "median_d_coeff": None,
            "max_d_coeff": None,
            "frac_d_coeff_gt_tau_R": None,
            "median_mag_rmse_band": None,
            "median_mag_rmse_full": None,
            "max_mag_rmse_band": None,
            "max_mag_rmse_full": None,
        }
    dc = np.array([r["distance_to_reference"]["d_coeff"] for r in rows], float)
    rb = np.array([r["distance_to_reference"]["mag_rmse_band"] for r in rows], float)
    rf = np.array([r["distance_to_reference"]["mag_rmse_full"] for r in rows], float)
    return {
        "n": int(len(rows)),
        "median_d_coeff": float(np.median(dc)),
        "max_d_coeff": float(np.max(dc)),
        "frac_d_coeff_gt_tau_R": float(np.mean(dc > TAU_R_DEFAULT)),
        "median_mag_rmse_band": float(np.median(rb)),
        "median_mag_rmse_full": float(np.median(rf)),
        "max_mag_rmse_band": float(np.max(rb)),
        "max_mag_rmse_full": float(np.max(rf)),
    }


def main() -> int:
    assert_no_scipy_design_in(ROOT / "src" / "first_principles_fir.py")
    tasks = _load_suite_n()
    assert len(tasks) == 20
    rng = np.random.default_rng(SEED)

    for sub in ("canonical", "library", "first_principles", "random"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    canon = {}
    all_rows = []
    logs = {}
    infeasible_canon = []

    for task in tasks:
        tid = task["task_id"]
        print(f"== {tid} ==", flush=True)
        crec = design_canonical(task)
        if not crec.get("ok"):
            infeasible_canon.append(tid)
            print(f"  CANONICAL INFEASIBLE {crec}", flush=True)
            logs[tid] = {"canonical": crec, "blocked": True}
            continue
        href = crec["impl"]
        cpath = _save_impl(OUT / "canonical" / f"{tid}__canonical", href)
        canon[tid] = {
            "method": crec["method"],
            "parameters": _jsonable(crec["parameters"]),
            "path": str(cpath.relative_to(ROOT)).replace("\\", "/"),
            "S_t": True,
        }
        print(f"  canonical {crec['method']} {crec['parameters']}", flush=True)

        accepted = []
        lib_rows, lib_log = generate_library(task)
        print(f"  library accepted={lib_log['accepted']} infeasible={lib_log['infeasible']}", flush=True)
        kept_lib = []
        for rec in lib_rows:
            if _dedup_keep(rec, accepted, float(task["sampling_rate"])):
                accepted.append(rec)
                kept_lib.append(rec)
        canon_n = None
        if is_fir(task):
            canon_n = int(len(np.asarray(href, float)))

        fp_rows, fp_log = generate_first_principles(task, canon_n)
        print(f"  first_principles accepted={fp_log['accepted']} infeasible={fp_log['infeasible']}", flush=True)
        kept_fp = []
        for rec in fp_rows:
            if _dedup_keep(rec, accepted, float(task["sampling_rate"])):
                accepted.append(rec)
                kept_fp.append(rec)

        rnd_rows, rnd_log = generate_random(task, rng, accepted)
        print(
            f"  random accepted={rnd_log['accepted']}/{rnd_log['attempts']} "
            f"dup_skip={rnd_log['duplicates_skipped']} low={rnd_log['low_occupancy']}",
            flush=True,
        )
        kept_rnd = rnd_rows
        accepted.extend(kept_rnd)

        serial = 0
        written = []
        for rec in kept_lib + kept_fp + kept_rnd:
            serial += 1
            stem = _stem(rec, serial)
            path = _save_impl(_subdir(rec["source"]) / stem, rec["impl"])
            row = _manifest_row(rec, path, href, task)
            (path.with_suffix(".json")).write_text(json.dumps(row, indent=2), encoding="utf-8")
            written.append(row)
            all_rows.append(row)

        logs[tid] = {
            "library": lib_log,
            "first_principles": fp_log,
            "random": rnd_log,
            "n_kept": len(written),
            "n_after_dedup": len(accepted),
        }

    fail_st = [r for r in all_rows if not r["S_t"]]
    per_task = {}
    for r in all_rows:
        per_task.setdefault(r["task_id"], []).append(r)

    low = []
    loose_fir_short = []
    for task in tasks:
        tid = task["task_id"]
        rows = per_task.get(tid, [])
        n = len(rows)
        if logs.get(tid, {}).get("random", {}).get("low_occupancy"):
            low.append(tid)
        if is_fir(task) and "loose" in tid and n < LOW_OCCUPANCY:
            loose_fir_short.append(tid)

    by_source = {}
    for r in all_rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1

    lib_att = sum(v.get("library", {}).get("attempts", 0) for v in logs.values())
    lib_acc = sum(v.get("library", {}).get("accepted", 0) for v in logs.values())
    rnd_att = sum(v.get("random", {}).get("attempts", 0) for v in logs.values())
    rnd_acc = sum(v.get("random", {}).get("accepted", 0) for v in logs.values())

    frr_ref = None
    if all_rows:
        frr_ref = float(np.mean([r["distance_to_reference"]["d_coeff"] > TAU_R_DEFAULT for r in all_rows]))

    diversity = {tid: _task_stats(rows) for tid, rows in per_task.items()}
    ready = not fail_st and not infeasible_canon and not loose_fir_short
    payload = {
        "seed": SEED,
        "n_tasks": len(tasks),
        "n_valid": len(all_rows),
        "n_S_t_fail": len(fail_st),
        "by_source": by_source,
        "per_task_n": {tid: len(per_task.get(tid, [])) for tid, _t in ((t["task_id"], t) for t in tasks)},
        "library_attempts": lib_att,
        "library_accepted_pre_dedup": lib_acc,
        "library_acceptance_rate": None if lib_att == 0 else lib_acc / lib_att,
        "random_attempts": rnd_att,
        "random_accepted": rnd_acc,
        "random_acceptance_rate": None if rnd_att == 0 else rnd_acc / rnd_att,
        "low_occupancy_tasks": low,
        "loose_fir_below_8": loose_fir_short,
        "canonical_infeasible": infeasible_canon,
        "FRR_reference_descriptive": frr_ref,
        "tau_R": TAU_R_DEFAULT,
        "diversity": diversity,
        "logs": logs,
        "recommendation": "READY_FOR_PHASE_2C" if ready else "BLOCKED",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(all_rows, indent=2), encoding="utf-8")
    (OUT / "canonical.json").write_text(json.dumps(canon, indent=2), encoding="utf-8")
    (OUT / "stats.json").write_text(json.dumps(_jsonable(payload), indent=2), encoding="utf-8")
    print(f"n_valid={len(all_rows)} S_t_fail={len(fail_st)} FRR_ref={frr_ref}")
    print("recommendation", payload["recommendation"])
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
