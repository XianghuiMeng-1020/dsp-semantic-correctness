#!/usr/bin/env python3
"""Phase 2C Stage 5: evaluation after labels are frozen."""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.filter_geom import is_fir  # noqa: E402
from src.oracles import oracle_a, oracle_b, oracle_b_threshold  # noqa: E402
from src.spec_checker import check_specification, get_task  # noqa: E402
from src.suite_s_fixtures import ALTERNATE_VALID, CANONICAL, MUTANTS  # noqa: E402
from src.valid_metrics import (  # noqa: E402
    d_coeff,
    distance_to_reference,
    is_type1_linear_phase,
    mag_rmse,
    same_order,
    unpack,
)

TAU_GRID = (0.01, 0.05, 0.10)
TAU_DEFAULT = 0.05
ANY3_METHODS = ("firwin", "remez", "firls")


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
    if x is None:
        return None
    return x


def load_impl(rel: str):
    p = ROOT / rel
    if p.suffix == ".npy":
        return np.load(p)
    z = np.load(p)
    return {"b": z["b"], "a": z["a"]}


def _rate(num, den):
    if den == 0:
        return None
    return float(num) / float(den)


def suite_s_disagreement(tid: str, fn_a, fn_b) -> float:
    task = get_task(tid)
    tv = task["constraints"]["test_vector"]
    if tid == "integer_delay_impulse":
        a, b = np.asarray(fn_a(), float), np.asarray(fn_b(), float)
        n = min(len(a), len(b))
        return float(np.linalg.norm(a[:n] - b[:n]) / max(np.linalg.norm(b[:n]), 1e-18))
    if tid == "crosscorrelation_integer_delay":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        y = np.roll(x, int(tv["L"]))
        return 0.0 if int(fn_a(x, y)) == int(fn_b(x, y)) else 1.0
    if tid == "circular_convolution_theorem":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        h = rng.standard_normal(int(tv["N"]))
        ya, yb = np.asarray(fn_a(x, h), float), np.asarray(fn_b(x, h), float)
        if ya.shape != yb.shape:
            return 1.0
        return float(np.linalg.norm(ya - yb) / max(np.linalg.norm(yb), 1e-18))
    if tid == "linear_convolution_zero_padded_dft":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["Nx"]))
        h = rng.standard_normal(int(tv["Nh"]))
        ya, yb = np.asarray(fn_a(x, h), float), np.asarray(fn_b(x, h), float)
        if ya.shape != yb.shape:
            return 1.0
        return float(np.linalg.norm(ya - yb) / max(np.linalg.norm(yb), 1e-18))
    if tid == "autocorrelation_lag0_energy":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        ra, rb = np.asarray(fn_a(x), float), np.asarray(fn_b(x), float)
        if ra.shape != rb.shape:
            return 1.0
        return float(np.linalg.norm(ra - rb) / max(np.linalg.norm(rb), 1e-18))
    if tid == "decimation_alias_frequency":
        ya = float(np.asarray(fn_a(tv["f"], tv["fs"], tv["M"])).reshape(()))
        yb = float(np.asarray(fn_b(tv["f"], tv["fs"], tv["M"])).reshape(()))
        return abs(ya - yb) / max(abs(yb), 1e-18)
    if tid == "digital_frequency_rescale":
        ya = float(np.asarray(fn_a(tv["f_hat"], tv["fs_in"], tv["fs_out"])).reshape(()))
        yb = float(np.asarray(fn_b(tv["f_hat"], tv["fs_in"], tv["fs_out"])).reshape(()))
        return abs(ya - yb) / max(abs(yb), 1e-18)
    if tid == "nyquist_hz":
        ya = float(np.asarray(fn_a(tv["fs"])).reshape(()))
        yb = float(np.asarray(fn_b(tv["fs"])).reshape(()))
        return 0.0 if abs(ya - yb) <= 1e-15 else 1.0
    return 0.0


def load_suite_n():
    tasks = json.loads((ROOT / "registry" / "suite_n.json").read_text(encoding="utf-8"))["tasks"]
    task_map = {t["task_id"]: t for t in tasks}
    canon_meta = json.loads((ROOT / "data" / "valid" / "canonical.json").read_text(encoding="utf-8"))
    valids = json.loads((ROOT / "data" / "valid" / "manifest.json").read_text(encoding="utf-8"))
    invalids = json.loads((ROOT / "data" / "invalid" / "manifest.json").read_text(encoding="utf-8"))
    hrefs = {tid: load_impl(m["path"]) for tid, m in canon_meta.items()}
    for row in valids:
        row["_impl"] = load_impl(row["path"])
        row["_href"] = hrefs[row["task_id"]]
        row["_task"] = task_map[row["task_id"]]
    for row in invalids:
        row["_impl"] = load_impl(row["path"])
        row["_href"] = hrefs[row["task_id"]]
        row["_task"] = task_map[row["task_id"]]
    return task_map, hrefs, valids, invalids


def audit_labels(valids, invalids):
    v_fail = []
    i_fail = []
    for r in valids:
        chk = check_specification(r["task_id"], r["_impl"])
        r["_S"] = bool(chk["pass"])
        if not chk["pass"]:
            v_fail.append(r["path"])
    for r in invalids:
        chk = check_specification(r["task_id"], r["_impl"])
        r["_S"] = bool(chk["pass"])
        r["residuals"] = chk["residuals"]
        if chk["pass"]:
            i_fail.append(r["path"])
    return {
        "valid_n": len(valids),
        "invalid_n": len(invalids),
        "valid_S1": sum(1 for r in valids if r["_S"]),
        "invalid_S0": sum(1 for r in invalids if not r["_S"]),
        "valid_label_errors": v_fail,
        "invalid_label_errors": i_fail,
        "FRR_S": _rate(sum(1 for r in valids if not r["_S"]), len(valids)),
        "FAR_S": _rate(sum(1 for r in invalids if r["_S"]), len(invalids)),
    }


def attach_distances(rows):
    for r in rows:
        r["_dist"] = distance_to_reference(r["_impl"], r["_href"], r["_task"])
        r["_lp"] = is_type1_linear_phase(r["_impl"])
        r["_same_order"] = bool(r["_dist"]["same_order"])


def frr_ref(rows, tau=TAU_DEFAULT):
    if not rows:
        return None
    return _rate(sum(1 for r in rows if r["_dist"]["d_coeff"] > tau), len(rows))


def frr_any3(valids, tau=TAU_DEFAULT):
    by = defaultdict(list)
    for r in valids:
        if r["source"] == "library" and r["method"] in ANY3_METHODS:
            by[r["task_id"]].append(r)
    n_rej = 0
    for r in valids:
        refs = by.get(r["task_id"], [])
        if not refs:
            if r["_dist"]["d_coeff"] > tau:
                n_rej += 1
            continue
        if all(d_coeff(r["_impl"], ref["_impl"]) > tau for ref in refs):
            n_rej += 1
    return _rate(n_rej, len(valids))


def task_level_disagreement(valids, tau=TAU_DEFAULT):
    tasks = sorted({r["task_id"] for r in valids})
    hit = 0
    for tid in tasks:
        rows = [r for r in valids if r["task_id"] == tid]
        if any(r["_S"] and r["_dist"]["d_coeff"] > tau for r in rows):
            hit += 1
    return {"n_tasks": len(tasks), "n_disagree": hit, "fraction": _rate(hit, len(tasks))}


def diversity(valids):
    out = {}
    for tid in sorted({r["task_id"] for r in valids}):
        rows = [r for r in valids if r["task_id"] == tid]
        dc = np.array([r["_dist"]["d_coeff"] for r in rows], float)
        rb = np.array([r["_dist"]["mag_rmse_band"] for r in rows], float)
        rf = np.array([r["_dist"]["mag_rmse_full"] for r in rows], float)
        pair_c, pair_b, pair_f = [], [], []
        for i, a in enumerate(rows):
            for b in rows[i + 1 :]:
                pair_c.append(d_coeff(a["_impl"], b["_impl"]))
                fs = float(a["_task"]["sampling_rate"])
                bands = list(a["_task"]["pass_band"]) + list(a["_task"]["stop_band"])
                pair_b.append(mag_rmse(a["_impl"], b["_impl"], fs, bands))
                pair_f.append(mag_rmse(a["_impl"], b["_impl"], fs, None))
        out[tid] = {
            "n": len(rows),
            "median_d_coeff": float(np.median(dc)),
            "max_d_coeff": float(np.max(dc)),
            "frac_d_coeff_gt_tau_R": float(np.mean(dc > TAU_DEFAULT)),
            "median_mag_rmse_band": float(np.median(rb)),
            "median_mag_rmse_full": float(np.median(rf)),
            "pairwise_median_d_coeff": float(np.median(pair_c)) if pair_c else None,
            "pairwise_frac_gt_tau_R": float(np.mean(np.array(pair_c) > TAU_DEFAULT)) if pair_c else None,
        }
    return out


def slice_rows(valids, kind):
    if kind == "all":
        return valids
    if kind == "fir":
        return [r for r in valids if is_fir(r["_task"])]
    if kind == "iir":
        return [r for r in valids if not is_fir(r["_task"])]
    if kind == "loose":
        return [r for r in valids if "loose" in r["task_id"]]
    if kind == "tight":
        return [r for r in valids if "tight" in r["task_id"]]
    raise KeyError(kind)


def table2(valids):
    tld = task_level_disagreement(valids)
    rows = {}
    for name in ("all", "fir", "iir", "loose", "tight"):
        sl = slice_rows(valids, name)
        rows[f"N_{name}"] = {
            "n": len(sl),
            "FRR_ref": frr_ref(sl),
            "FRR_ref_any3": frr_any3(sl),
            "P_d_gt_tau_R": frr_ref(sl),
        }
    rows["N_all"]["task_level_disagreement"] = tld
    return rows


def oracle_tables(valids, invalids, hrefs, tau=TAU_DEFAULT):
    lib = defaultdict(list)
    for r in valids:
        if r["source"] == "library":
            lib[r["task_id"]].append(r["_impl"])
    bcal = {}
    for tid, impls in lib.items():
        task = get_task(tid)
        bands = list(task["pass_band"]) + list(task["stop_band"])
        bcal[tid] = oracle_b_threshold(impls, float(task["sampling_rate"]), bands, hrefs[tid])

    def score(rows, label_valid: bool):
        a_pos = b_pos = 0
        for r in rows:
            tid = r["task_id"]
            fs = float(r["_task"]["sampling_rate"])
            bands = list(r["_task"]["pass_band"]) + list(r["_task"]["stop_band"])
            a_ok = oracle_a(r["_impl"], r["_href"], tau)
            b_ok = oracle_b(r["_impl"], r["_href"], fs, bands, bcal[tid]["threshold"])
            r["_A"] = bool(a_ok)
            r["_B"] = bool(b_ok)
            a_pos += int(a_ok)
            b_pos += int(b_ok)
        n = len(rows)
        if label_valid:
            return {"FRR_A": _rate(n - a_pos, n), "FRR_B": _rate(n - b_pos, n), "n": n}
        return {"FAR_A": _rate(a_pos, n), "FAR_B": _rate(b_pos, n), "n": n}

    v = score(valids, True)
    inv = score(invalids, False)
    return {
        "oracle_b_calibration": bcal,
        "A": {"FRR": v["FRR_A"], "FAR": inv["FAR_A"]},
        "B": {"FRR": v["FRR_B"], "FAR": inv["FAR_B"]},
        "C": {
            "FRR": _rate(sum(1 for r in valids if not r["_S"]), len(valids)),
            "FAR": _rate(sum(1 for r in invalids if r["_S"]), len(invalids)),
        },
    }


def ablations(valids):
    out = {"tau_R": {}, "phase": {}, "order": {}}
    for tau in TAU_GRID:
        out["tau_R"][str(tau)] = {"n": len(valids), "FRR_ref": frr_ref(valids, tau)}
    out["phase"]["free"] = {"n": len(valids), "FRR_ref": frr_ref(valids)}
    lp = [r for r in valids if r["_lp"]]
    out["phase"]["linear_type1"] = {"n": len(lp), "FRR_ref": frr_ref(lp)}
    out["order"]["free"] = {"n": len(valids), "FRR_ref": frr_ref(valids)}
    so = [r for r in valids if r["_same_order"]]
    out["order"]["canonical_order"] = {"n": len(so), "FRR_ref": frr_ref(so)}
    return out


def evaluate_suite_s():
    valids = []
    invalids = []
    for tid, fn in CANONICAL.items():
        chk = check_specification(tid, fn)
        d = suite_s_disagreement(tid, fn, CANONICAL[tid])
        valids.append({"task_id": tid, "kind": "canonical", "S": chk["pass"], "d_ref": d})
        if tid in ALTERNATE_VALID:
            alt = ALTERNATE_VALID[tid]
            chk_a = check_specification(tid, alt)
            d_a = suite_s_disagreement(tid, alt, CANONICAL[tid])
            valids.append({"task_id": tid, "kind": "alternate", "S": chk_a["pass"], "d_ref": d_a})
    for tid, muts in MUTANTS.items():
        for name, fn in muts.items():
            chk = check_specification(tid, fn)
            d = suite_s_disagreement(tid, fn, CANONICAL[tid])
            invalids.append({"task_id": tid, "mechanism": name, "S": chk["pass"], "d_ref": d})
    frr_s = _rate(sum(1 for r in valids if not r["S"]), len(valids))
    far_s = _rate(sum(1 for r in invalids if r["S"]), len(invalids))
    frr_ref_s = _rate(sum(1 for r in valids if r["d_ref"] > TAU_DEFAULT), len(valids))
    far_a_s = _rate(sum(1 for r in invalids if r["d_ref"] <= TAU_DEFAULT), len(invalids))
    return {
        "n_valid": len(valids),
        "n_invalid": len(invalids),
        "FRR_ref": frr_ref_s,
        "FRR_S": frr_s,
        "FAR_S": far_s,
        "FRR_A": frr_ref_s,
        "FAR_A": far_a_s,
        "valids": valids,
        "invalids": invalids,
    }


def main() -> int:
    task_map, hrefs, valids, invalids = load_suite_n()
    audit = audit_labels(valids, invalids)
    attach_distances(valids)
    attach_distances(invalids)
    t2 = table2(valids)
    orc = oracle_tables(valids, invalids, hrefs)
    abl = ablations(valids)
    s = evaluate_suite_s()
    by_mech = defaultdict(int)
    for r in invalids:
        by_mech[r["mechanism"]] += 1
    payload = {
        "label_audit": audit,
        "invalid_by_mechanism": dict(by_mech),
        "table2_reference_rejection": t2,
        "diversity": diversity(valids),
        "table3_verification": orc,
        "table4_ablations": abl,
        "suite_s": {k: v for k, v in s.items() if k not in {"valids", "invalids"}},
        "suite_s_detail": s,
    }
    out = ROOT / "data" / "phase2c"
    out.mkdir(parents=True, exist_ok=True)
    (out / "evaluation.json").write_text(json.dumps(_jsonable(payload), indent=2), encoding="utf-8")
    print("valids", audit["valid_n"], "invalids", audit["invalid_n"])
    print("FRR_S", audit["FRR_S"], "FAR_S", audit["FAR_S"])
    print("FRR_ref N", t2["N_all"]["FRR_ref"])
    print("Oracle A", orc["A"], "B", orc["B"], "C", orc["C"])
    print("Suite S FRR_ref", s["FRR_ref"], "FRR_S", s["FRR_S"])
    print("wrote", out / "evaluation.json")
    return 0 if not audit["valid_label_errors"] and not audit["invalid_label_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
