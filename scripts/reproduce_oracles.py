#!/usr/bin/env python3
"""Reproduce Table III: Oracles A/B/C versus tone consistency check T.

Frozen Arm N artifacts only. No new models or generations.

Oracle A: coefficient concordance with the canonical occupant (tau_R=0.05).
Oracle B: spec-band |H| RMSE versus that occupant, no larger than the
          same-order control-pair maximum on the task.
Oracle C: specification membership S_t.

T applies the same magnitude mask to steady-state Hilbert envelopes of
constrained real cosines (lfilter). T is a consistency probe of that mask,
not an independent gold / correctness oracle.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts_arm_n import (  # noqa: E402
    FIR_BANDPASS_BANDS,
    FIR_BANDSTOP_BANDS,
    FIR_LOWPASS_BANDS,
    FS,
    IIR_LOWPASS_BANDS,
    TASK_FACTORIES,
    spec_residual,
)
from src.runtime import exec_function, score_task  # noqa: E402

WORN = 4096
TAU_R = 0.05
CALL_TIMEOUT_SEC = 15
N_TONE = 8192
TRANSIENT_DROP = 1024
CANONICAL = {
    "fir_lowpass_spec": "firwin",
    "fir_bandpass_spec": "firwin",
    "fir_bandstop_spec": "firwin",
    "iir_lowpass_stable_spec": "butter",
}
BANDS = {
    "fir_lowpass_spec": FIR_LOWPASS_BANDS,
    "fir_bandpass_spec": FIR_BANDPASS_BANDS,
    "fir_bandstop_spec": FIR_BANDSTOP_BANDS,
    "iir_lowpass_stable_spec": IIR_LOWPASS_BANDS,
}
# Constrained-band edges and midpoints. Transition tones are generated but
# not scored (unconstrained).
PROBES = {
    "fir_lowpass_spec": {
        "pass": [50.0, 400.0, 800.0],
        "transition": [1400.0],
        "stop": [2000.0, 3000.0, 3900.0],
    },
    "fir_bandpass_spec": {
        "stop": [50.0, 250.0, 500.0, 3200.0, 3600.0, 3900.0],
        "pass": [1500.0, 1850.0, 2200.0],
        "transition": [1000.0],
    },
    "fir_bandstop_spec": {
        "pass": [50.0, 300.0, 600.0, 3000.0, 3500.0, 3900.0],
        "stop": [1400.0, 1800.0, 2200.0],
        "transition": [1000.0],
    },
    "iir_lowpass_stable_spec": {
        "pass": [50.0, 300.0, 600.0],
        "transition": [1500.0],
        "stop": [2400.0, 3200.0, 3900.0],
    },
}
PUBLISHED_BAND_MAX = {
    "fir_lowpass_spec": 8.6e-4,
    "fir_bandpass_spec": 1.0e-3,
    "fir_bandstop_spec": 7.4e-4,
    "iir_lowpass_stable_spec": 1.9e-2,
}


def _arm_n_worker(code, func_name, q):
    import contextlib
    import io

    fn, err = exec_function(code, func_name)
    if fn is None:
        q.put(("exec_fail", err, None))
        return
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            y = fn()
        q.put(("ok", None, y))
    except Exception as exc:  # noqa: BLE001
        q.put(("call_fail", f"CALL_ERROR: {exc}", None))


def exec_with_timeout(code: str, func_name: str):
    from multiprocessing import Process, Queue

    q: Queue = Queue()
    p = Process(target=_arm_n_worker, args=(code, func_name, q))
    p.start()
    p.join(CALL_TIMEOUT_SEC)
    if p.is_alive():
        p.terminate()
        p.join(3)
        return None, f"EXEC_TIMEOUT:{CALL_TIMEOUT_SEC}s"
    if q.empty():
        return None, "EXEC_ERROR: empty worker result"
    status, err, y = q.get()
    if status != "ok":
        return None, err
    return y, None


def load_controls():
    out = {}
    for p in (ROOT / "data/arm_n_valid_controls").glob("*"):
        tid = p.name.split("__")[0]
        impl = p.stem.split("__", 1)[1]
        out.setdefault(tid, {})
        if p.suffix == ".npy":
            h = np.asarray(np.load(p), float).reshape(-1)
            out[tid][impl] = (h, np.array([1.0]))
        else:
            z = np.load(p)
            out[tid][impl] = (
                np.asarray(z["b"], float).reshape(-1),
                np.asarray(z["a"], float).reshape(-1),
            )
    return out


def pack_from_y(tid, y):
    if tid.startswith("iir"):
        return np.asarray(y[0], float).reshape(-1), np.asarray(y[1], float).reshape(-1)
    return np.asarray(y, float).reshape(-1), np.array([1.0])


def coeff_rel_l2(b, a, rb, ra, tid):
    if tid.startswith("iir"):
        v = np.concatenate([b, a])
        vr = np.concatenate([rb, ra])
    else:
        v, vr = b, rb
    n = min(len(v), len(vr))
    return float(np.linalg.norm(v[:n] - vr[:n]) / max(np.linalg.norm(vr[:n]), 1e-18))


def band_mag_rmse(b, a, rb, ra, bands):
    w, H = sp_signal.freqz(b, a, worN=WORN, fs=FS)
    _, Hr = sp_signal.freqz(rb, ra, worN=WORN, fs=FS)
    d = np.abs(H) - np.abs(Hr)
    mask = np.zeros_like(w, dtype=bool)
    for band in bands:
        mask |= (w >= band["f0"]) & (w <= band["f1"])
    return float(np.sqrt(np.mean(d[mask] ** 2)))


def tone_gain(b, a, f0):
    t = np.arange(N_TONE) / FS
    x = np.cos(2 * np.pi * f0 * t)
    y = sp_signal.lfilter(b, a, x)
    ax = float(np.mean(np.abs(sp_signal.hilbert(x[TRANSIENT_DROP:]))))
    ay = float(np.mean(np.abs(sp_signal.hilbert(y[TRANSIENT_DROP:]))))
    return ay / max(ax, 1e-18)


def tone_consistency(b, a, tid):
    bands = BANDS[tid]
    n_ok = n_con = 0
    for role, freqs in PROBES[tid].items():
        if role == "transition":
            continue
        for f0 in freqs:
            g = tone_gain(b, a, f0)
            for band in bands:
                if band["f0"] <= f0 <= band["f1"]:
                    n_con += 1
                    n_ok += int(band["lo"] <= g <= band["hi"])
                    break
    return n_ok == n_con, f"{n_ok}/{n_con}"


def control_band_maxima(controls):
    maxima = {}
    for tid, impls in controls.items():
        names = sorted(impls)
        vals = []
        for i, ni in enumerate(names):
            for nj in names[i + 1 :]:
                bi, ai = impls[ni]
                bj, aj = impls[nj]
                vals.append(band_mag_rmse(bi, ai, bj, aj, BANDS[tid]))
        maxima[tid] = max(vals)
    return maxima


def check(cond, label, failures):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def rates(rows, key):
    agree = sum(1 for r in rows if r[key] == r["T"])
    tp_of = sum(1 for r in rows if (not r[key]) and r["T"])
    tn_op = sum(1 for r in rows if r[key] and (not r["T"]))
    n_t1 = sum(1 for r in rows if r["T"])
    n_t0 = sum(1 for r in rows if not r["T"])
    return {
        "agree": agree,
        "tp_of": tp_of,
        "tn_op": tn_op,
        "frr": 0.0 if n_t1 == 0 else tp_of / n_t1,
        "far": 0.0 if n_t0 == 0 else tn_op / n_t0,
    }


def main() -> int:
    from multiprocessing import freeze_support

    freeze_support()
    failures: list[str] = []
    print("RQ4 — Oracles A/B/C vs tone consistency check T")
    print("T is a consistency probe of the same mask, not an independent gold oracle.")

    tasks = {f()["id"]: f() for f in TASK_FACTORIES}
    controls = load_controls()
    band_max = control_band_maxima(controls)
    frozen_a = json.loads((ROOT / "data/arm_n_oracle_a_frozen.json").read_text(encoding="utf-8"))
    frozen_r = frozen_a["rows"]
    rows_json = json.loads((ROOT / "data/arm_n_generations.json").read_text(encoding="utf-8"))

    eligible = []
    for rec in rows_json:
        if rec.get("discarded_not_scored"):
            continue
        y, err = exec_with_timeout(rec.get("code") or "", rec["func_name"])
        if err is not None:
            continue
        tid = rec["task"]
        task = tasks[tid]
        fn = lambda y=y: y  # noqa: E731
        base = score_task(task, fn)
        if not base["unit_test_pass"]:
            continue
        b, a = pack_from_y(tid, y)
        rb, ra = controls[tid][CANONICAL[tid]]
        live_coeff = coeff_rel_l2(b, a, rb, ra, tid)
        gid = rec["generation_id"]
        if gid not in frozen_r:
            continue
        coeff = float(frozen_r[gid])
        rmse_b = band_mag_rmse(b, a, rb, ra, BANDS[tid])
        t_pass, tstr = tone_consistency(b, a, tid)
        a_pass = coeff <= TAU_R
        b_pass = rmse_b <= band_max[tid] + 1e-8
        c_pass = bool(base["unit_test_pass"] and not base["semantic_fail"])
        eligible.append(
            {
                "id": gid,
                "task": tid,
                "A": a_pass,
                "B": b_pass,
                "C": c_pass,
                "T": t_pass,
                "tones": tstr,
                "coeff": coeff,
                "live_coeff": live_coeff,
                "rmse_band": rmse_b,
            }
        )

    print(f"  eligible n={len(eligible)}")
    check(len(eligible) == 14, "eligible 14", failures)

    print("  Oracle | Agree with T | T+ and orc- | T- and orc+")
    summary = {}
    for name in ("A", "B", "C"):
        d = rates(eligible, name)
        summary[name] = d
        print(
            f"  {name}     {d['agree']}/14          "
            f"{d['frr']:.2f}         {d['far']:.2f}"
        )

    check(summary["A"]["agree"] == 5, "A agree 5/14", failures)
    check(abs(summary["A"]["frr"] - 1.00) < 1e-9, "A T+ and orc- = 1.00", failures)
    check(summary["A"]["far"] == 0.0, "A T- and orc+ = 0", failures)
    check(summary["B"]["agree"] == 8, "B agree 8/14", failures)
    check(abs(summary["B"]["frr"] - 6 / 9) < 1e-9, "B T+ and orc- = 0.67", failures)
    check(summary["B"]["far"] == 0.0, "B T- and orc+ = 0", failures)
    check(summary["C"]["agree"] == 14, "C agree 14/14", failures)
    check(summary["C"]["frr"] == 0.0, "C T+ and orc- = 0", failures)
    check(summary["C"]["far"] == 0.0, "C T- and orc+ = 0", failures)

    for tid, published in PUBLISHED_BAND_MAX.items():
        got = band_max[tid]
        print(f"  B calibration max {tid}: {got:.4g} (paper {published:.4g})")
        check(abs(got - published) / published < 0.08, f"B max {tid} matches paper", failures)

    if failures:
        print(f"ORACLE_TABLE_MATCH: NO ({len(failures)} failed checks)")
        return 1
    print("ORACLE_TABLE_MATCH: YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
