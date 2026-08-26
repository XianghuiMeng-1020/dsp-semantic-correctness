"""First-principles FIR occupants. Numpy design only."""
from __future__ import annotations

import numpy as np

from src.filter_geom import cutoff_grid, default_cutoffs, estimate_fir_n, response_type
from src.first_principles_fir import (
    frequency_sampling,
    mag_bandpass,
    mag_bandstop,
    mag_highpass,
    mag_lowpass,
    windowed_sinc_bandpass,
    windowed_sinc_bandstop,
    windowed_sinc_highpass,
    windowed_sinc_lowpass,
)
from src.spec_checker import check_specification

N_MAX = 401


def _norm_dc(h):
    s = float(np.sum(h))
    return h / s if abs(s) > 1e-18 else h


def _norm_nyq(h, fs):
    n = np.arange(len(h), dtype=float)
    g = float(np.abs(np.dot(h, np.exp(-1j * np.pi * n))))
    return h / g if g > 1e-12 else h


def _norm_at(h, f_hz, fs):
    n = np.arange(len(h), dtype=float)
    g = float(np.abs(np.dot(h, np.exp(-1j * 2.0 * np.pi * f_hz * n / fs))))
    return h / g if g > 1e-12 else h


def _edges(task):
    p = sorted(task["pass_band"], key=lambda b: b["f0"])
    s = sorted(task["stop_band"], key=lambda b: b["f0"])
    return p, s


def windowed_at(task: dict, n: int, cut: list[float]):
    fs = float(task["sampling_rate"])
    r = response_type(task)
    p, s = _edges(task)
    if r == "lp":
        return windowed_sinc_lowpass(n, float(cut[0]), fs)
    if r == "hp":
        return windowed_sinc_highpass(n, float(cut[0]), fs)
    if r == "bp":
        fmid = 0.5 * (float(p[0]["f0"]) + float(p[0]["f1"]))
        return windowed_sinc_bandpass(n, float(cut[0]), float(cut[1]), fs, fmid)
    if r == "bs":
        return windowed_sinc_bandstop(n, float(cut[0]), float(cut[1]), fs)
    raise KeyError(r)


def freqsamp_at(task: dict, n: int, cut=None):
    fs = float(task["sampling_rate"])
    r = response_type(task)
    p, s = _edges(task)
    if r == "lp":
        fp, fst = float(p[0]["f1"]), float(s[0]["f0"])
        if cut is not None and len(cut) >= 1:
            # keep pass/stop edges; cut is unused except as transition probe
            pass
        h = frequency_sampling(n, lambda f, a=fp, b=fst: mag_lowpass(f, a, b), fs)
        return _norm_dc(h)
    if r == "hp":
        fst, fp = float(s[0]["f1"]), float(p[0]["f0"])
        h = frequency_sampling(n, lambda f, a=fst, b=fp: mag_highpass(f, a, b), fs)
        return _norm_nyq(h, fs)
    if r == "bp":
        f_s1, f_p1, f_p2, f_s2 = (
            float(s[0]["f1"]),
            float(p[0]["f0"]),
            float(p[0]["f1"]),
            float(s[1]["f0"]),
        )
        h = frequency_sampling(
            n, lambda f: mag_bandpass(f, f_s1, f_p1, f_p2, f_s2), fs
        )
        fmid = 0.5 * (f_p1 + f_p2)
        return _norm_at(h, fmid, fs)
    if r == "bs":
        f_p1, f_s1, f_s2, f_p2 = (
            float(p[0]["f1"]),
            float(s[0]["f0"]),
            float(s[0]["f1"]),
            float(p[1]["f0"]),
        )
        h = frequency_sampling(
            n, lambda f: mag_bandstop(f, f_p1, f_s1, f_s2, f_p2), fs
        )
        return _norm_dc(h)
    raise KeyError(r)


def _pass(task, h) -> bool:
    if h is None or not np.all(np.isfinite(h)):
        return False
    return bool(check_specification(task["task_id"], h)["pass"])


def _search_windowed(task, n_fixed=None):
    grids = cutoff_grid(task, n_pts=7)
    mid = default_cutoffs(task)
    cuts = [mid] + [g for g in grids if g != mid]
    if n_fixed is not None:
        for cut in cuts:
            try:
                h = windowed_at(task, int(n_fixed), cut)
            except Exception:
                continue
            if _pass(task, h):
                return np.asarray(h, float), {"n": int(n_fixed), "cutoff": [float(x) for x in cut]}
        return None, {"n": int(n_fixed), "infeasible": True}
    n0 = estimate_fir_n(task)
    ns = list(range(n0 if n0 % 2 else n0 + 1, N_MAX + 1, 2)) + list(range(21, n0, 2))
    for n in ns:
        for cut in cuts:
            try:
                h = windowed_at(task, int(n), cut)
            except Exception:
                continue
            if _pass(task, h):
                # walk down for shortest
                best_h, best_p = np.asarray(h, float), {"n": int(n), "cutoff": [float(x) for x in cut]}
                for n2 in range(n - 2, 20, -2):
                    hit = False
                    for cut2 in cuts:
                        try:
                            h2 = windowed_at(task, int(n2), cut2)
                        except Exception:
                            continue
                        if _pass(task, h2):
                            best_h, best_p = np.asarray(h2, float), {
                                "n": int(n2),
                                "cutoff": [float(x) for x in cut2],
                            }
                            hit = True
                            break
                    if not hit:
                        break
                return best_h, best_p
    return None, {"infeasible": True}


def _search_freqsamp(task, n_fixed=None):
    if n_fixed is not None:
        try:
            h = freqsamp_at(task, int(n_fixed))
        except Exception:
            return None, {"n": int(n_fixed), "infeasible": True}
        if _pass(task, h):
            return np.asarray(h, float), {"n": int(n_fixed)}
        return None, {"n": int(n_fixed), "infeasible": True}
    n0 = estimate_fir_n(task)
    ns = list(range(n0 if n0 % 2 else n0 + 1, N_MAX + 1, 2)) + list(range(21, n0, 2))
    for n in ns:
        try:
            h = freqsamp_at(task, int(n))
        except Exception:
            continue
        if _pass(task, h):
            best_h, best_n = np.asarray(h, float), int(n)
            for n2 in range(n - 2, 20, -2):
                try:
                    h2 = freqsamp_at(task, int(n2))
                except Exception:
                    break
                if _pass(task, h2):
                    best_h, best_n = np.asarray(h2, float), int(n2)
                else:
                    break
            return best_h, {"n": best_n}
    return None, {"infeasible": True}


def generate_first_principles(task: dict, canonical_n: int | None) -> tuple[list[dict], dict]:
    rows = []
    log = {"attempts": 0, "accepted": 0, "infeasible": []}
    if not str(task["type"]).startswith("fir_"):
        return rows, log
    searches = (
        ("windowed_sinc", _search_windowed),
        ("frequency_sampling", _search_freqsamp),
    )
    for method, fn in searches:
        for variant, n_lock in (("shortest", None), ("sameorder", canonical_n)):
            if variant == "sameorder" and canonical_n is None:
                log["infeasible"].append(f"{method}/sameorder")
                continue
            log["attempts"] += 1
            h, params = fn(task, n_fixed=n_lock)
            if h is None:
                log["infeasible"].append(f"{method}/{variant}")
                continue
            log["accepted"] += 1
            params = dict(params)
            params["variant"] = variant
            rows.append(
                {
                    "task_id": task["task_id"],
                    "source": "first_principles",
                    "method": method,
                    "parameters": params,
                    "impl": h,
                    "label": "valid-by-construction",
                }
            )
    return rows, log
