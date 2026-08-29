"""Best-observed-valid-reference analysis using frozen distances.py definitions."""
from __future__ import annotations

import math
import numpy as np
from scipy import signal as sp_signal

from experiments.icassp_10of10_hardening.phase1.config import G_ZERO_ABS, TIE_ABS
from src.verification.canonicalize import unpack
from src.verification.distances import RESP_N, d_coeff_canonical


def _freqz_mag(impl, fs: float, n: int = RESP_N) -> tuple[np.ndarray, np.ndarray]:
    b, a = unpack(impl)
    if a is None:
        w, H = sp_signal.freqz(b, worN=n, fs=fs)
    else:
        try:
            sos = sp_signal.tf2sos(b, a)
            w, H = sp_signal.sosfreqz(sos, worN=n, fs=fs)
        except Exception:
            w, H = sp_signal.freqz(b, a, worN=n, fs=fs)
    return w, np.abs(H)


def _band_mask(w: np.ndarray, task: dict) -> np.ndarray:
    mask = np.zeros_like(w, dtype=bool)
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        mask |= (w >= float(band["f0"])) & (w <= float(band["f1"]))
    return mask


def d_coeff(h, href, task: dict) -> float:
    return float(d_coeff_canonical(h, href, task)["d_coeff_mag_equiv"])


def d_resp_from_mags(mag: np.ndarray, mag_r: np.ndarray, mask: np.ndarray) -> float:
    if not np.any(mask):
        return 1.0
    d = mag[mask] - mag_r[mask]
    return float(np.sqrt(np.mean(d**2)))


def cache_mags(occupants: list[dict], fs: float) -> None:
    for o in occupants:
        if "_mag" not in o:
            w, mag = _freqz_mag(o["impl"], fs)
            o["_w"] = w
            o["_mag"] = mag


def gap_for_reference(
    ref: dict,
    valids: list[dict],
    invalids: list[dict],
    task: dict,
    metric: str,
) -> dict:
    if metric == "coeff":
        dvs = [d_coeff(v["impl"], ref["impl"], task) for v in valids]
        dis = [d_coeff(i["impl"], ref["impl"], task) for i in invalids]
    elif metric == "resp":
        fs = float(task["sampling_rate"])
        cache_mags(valids + invalids + [ref], fs)
        mask = _band_mask(ref["_w"], task)
        dvs = [d_resp_from_mags(v["_mag"], ref["_mag"], mask) for v in valids]
        dis = [d_resp_from_mags(i["_mag"], ref["_mag"], mask) for i in invalids]
    else:
        raise ValueError(metric)
    if not dvs or not dis:
        return {"D_V": None, "D_I": None, "G": None, "farthest_valid": None, "nearest_invalid": None}
    i_dv = max(range(len(dvs)), key=lambda k: (dvs[k], valids[k]["cid"]))
    i_di = min(range(len(dis)), key=lambda k: (dis[k], invalids[k]["cid"]))
    dv, di = float(dvs[i_dv]), float(dis[i_di])
    return {
        "D_V": dv,
        "D_I": di,
        "G": di - dv,
        "farthest_valid": valids[i_dv]["cid"],
        "nearest_invalid": invalids[i_di]["cid"],
        "self_distance": dvs[[v["cid"] for v in valids].index(ref["cid"])] if ref["cid"] in {v["cid"] for v in valids} else d_coeff(ref["impl"], ref["impl"], task) if metric == "coeff" else 0.0,
    }


def best_observed(valids, invalids, task, metric: str, frozen_canonical_G: float | None) -> dict:
    rows = []
    for ref in valids:
        rec = gap_for_reference(ref, valids, invalids, task, metric)
        rec["ref_id"] = ref["cid"]
        rec["ref_role"] = ref["role"]
        rows.append(rec)
    if not rows:
        return {"error": "no_valids"}

    def key(r):
        g = r["G"]
        # maximize G; ties → lexicographic smallest ref_id
        return (-g, r["ref_id"])

    rows_sorted = sorted(rows, key=key)
    best = rows_sorted[0]
    gstar = best["G"]
    tied = [r["ref_id"] for r in rows if abs(r["G"] - gstar) <= TIE_ABS]
    canon_row = None
    return {
        "metric": metric,
        "n_valid": len(valids),
        "n_invalid": len(invalids),
        "Gobs_star": gstar,
        "best_reference_id": best["ref_id"],
        "best_DV": best["D_V"],
        "best_DI": best["D_I"],
        "exact_separable": bool(gstar > G_ZERO_ABS),
        "sign": "gt0" if gstar > G_ZERO_ABS else ("eq0" if abs(gstar) <= G_ZERO_ABS else "lt0"),
        "n_tied": len(tied),
        "tied_reference_ids": tied,
        "canonical_G_frozen": frozen_canonical_G,
        "improvement_over_canonical": None if frozen_canonical_G is None else gstar - frozen_canonical_G,
        "all_refs": rows,
    }


def summarize(task_rows: list[dict], metric: str) -> dict:
    gs = [r[metric]["Gobs_star"] for r in task_rows]
    n_gt = sum(1 for g in gs if g > G_ZERO_ABS)
    n_eq = sum(1 for g in gs if abs(g) <= G_ZERO_ABS)
    n_lt = sum(1 for g in gs if g < -G_ZERO_ABS)
    frozen_ns = sum(1 for r in task_rows if r[metric]["canonical_G_frozen"] is not None and r[metric]["canonical_G_frozen"] <= G_ZERO_ABS)
    best_ns = n_eq + n_lt
    status_change = 0
    largest_rescue = None
    for r in task_rows:
        cg = r[metric]["canonical_G_frozen"]
        bg = r[metric]["Gobs_star"]
        if cg is None:
            continue
        c_sep = cg > G_ZERO_ABS
        b_sep = bg > G_ZERO_ABS
        if c_sep != b_sep:
            status_change += 1
        imp = bg - cg
        if largest_rescue is None or imp > largest_rescue["improvement"]:
            largest_rescue = {"task_id": r["task_id"], "improvement": imp, "canonical_G": cg, "Gobs_star": bg}
    arr = np.asarray(gs, float)
    return {
        "n_tasks": len(gs),
        "n_gt0": n_gt,
        "n_eq0": n_eq,
        "n_lt0": n_lt,
        "median": float(np.median(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "canonical_nonseparable": frozen_ns,
        "best_observed_nonseparable": best_ns,
        "n_separability_status_change": status_change,
        "largest_rescue": largest_rescue,
    }


def run_task_metrics(pack: dict, invalids: list, metric_frozen_key: str, metric: str) -> dict:
    frozen = pack["frozen_metrics"][metric_frozen_key]
    return best_observed(
        pack["valids"],
        invalids,
        pack["task"],
        metric,
        float(frozen["G_r"]) if frozen.get("G_r") is not None else None,
    )
