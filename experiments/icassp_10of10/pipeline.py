"""Run the 10/10 scientific stages and write JSON artifacts."""
from __future__ import annotations

import json
import os
import platform
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10.config import (  # noqa: E402
    BOOTSTRAP_B,
    BOUNDARY_DIR,
    DISCORD_TAU_DESCRIPTIVE,
    GENUINE_EPS,
    K_GRID,
    LIBRARY_ORDER_FIR,
    LIBRARY_ORDER_IIR,
    NEAR_SCALE_RESID,
    OUT_DIR,
    PROBE_CAND_DIR,
    SEED,
    VERIFIER_VERSION,
)
from src.suite_s_fixtures import ALTERNATE_VALID, CANONICAL, MUTANTS  # noqa: E402
from src.verification.boundary_invalids import construct_boundary_invalids  # noqa: E402
from src.verification.canonicalize import canonicalize_fir, unpack  # noqa: E402
from src.verification.distances import distance_bundle  # noqa: E402
from src.verification.feasible_set_probe import backoff_to_independent, run_probes_for_task  # noqa: E402
from src.verification.independent_spec_verifier import verify_specification  # noqa: E402
from src.verification.io_utils import dump_json, load_impl, sha256_file  # noqa: E402
from src.verification.registry_io import (  # noqa: E402
    LEGACY_TO_SUITE_N,
    get_task,
    is_fir,
    suite_n_tasks,
    suite_s_tasks,
)
from src.verification.search_checker import search_check  # noqa: E402

TAU_DESC = DISCORD_TAU_DESCRIPTIVE


def _scale_only(h, href) -> bool:
    a = np.asarray(unpack(h)[0], float).reshape(-1)
    b = np.asarray(unpack(href)[0], float).reshape(-1)
    n = min(len(a), len(b))
    if n == 0:
        return False
    aa, bb = a[:n], b[:n]
    den = float(np.dot(bb, bb))
    if den < 1e-18:
        return False
    alpha = float(np.dot(aa, bb) / den)
    resid = float(np.linalg.norm(aa - alpha * bb) / (np.linalg.norm(bb) + 1e-18))
    return resid <= NEAR_SCALE_RESID and abs(alpha - 1.0) > 1e-6


def _genuine_alt(dist: dict, impl, href, task) -> bool:
    if dist["d_coeff_mag_equiv"] <= GENUINE_EPS:
        return False
    if dist.get("zero_pad_artifact"):
        return False
    if dist.get("sign_flip_only"):
        return False
    if is_fir(task) and _scale_only(impl, href):
        return False
    return True


def load_base():
    canon_meta = json.loads((ROOT / "data" / "valid" / "canonical.json").read_text(encoding="utf-8"))
    valids = json.loads((ROOT / "data" / "valid" / "manifest.json").read_text(encoding="utf-8"))
    invalids = json.loads((ROOT / "data" / "invalid" / "manifest.json").read_text(encoding="utf-8"))
    hrefs = {tid: load_impl(m["path"]) for tid, m in canon_meta.items()}
    for row in valids:
        row["_impl"] = load_impl(row["path"])
        row["_href"] = hrefs[row["task_id"]]
        row["_task"] = get_task(row["task_id"])
        row["_cid"] = row["path"]
    for row in invalids:
        row["_impl"] = load_impl(row["path"])
        row["_href"] = hrefs[row["task_id"]]
        row["_task"] = get_task(row["task_id"])
        row["_cid"] = row["path"]
    return canon_meta, hrefs, valids, invalids


def recertify(rows, previous_valid: bool) -> list[dict]:
    out = []
    for r in rows:
        indep = verify_specification(r["task_id"], r["_impl"])
        search = search_check(r["task_id"], r["_impl"])
        prev = bool(r.get("S_t", previous_valid))
        new = bool(indep.ok)
        flip = prev != new
        reason = None
        if flip:
            if previous_valid and not new:
                if indep.numerical_failure:
                    reason = f"numerical_failure:{indep.numerical_failure}"
                elif indep.stability_error > 0:
                    reason = "stability"
                elif indep.passband_error > float(r["_task"]["residual_floor"]):
                    reason = f"passband_dense:{indep.passband_error:.3e}@f={indep.f_worst_pass}"
                elif indep.stopband_error > float(r["_task"]["residual_floor"]):
                    reason = f"stopband_dense:{indep.stopband_error:.3e}@f={indep.f_worst_stop}"
                else:
                    reason = "other_independent_fail"
            else:
                reason = "search_invalid_but_independent_valid"
        rec = {
            "id": r["_cid"],
            "task_id": r["task_id"],
            "source": r.get("source") or r.get("mechanism"),
            "method": r.get("method"),
            "previous_label": "VALID" if prev else "INVALID",
            "search_label": "VALID" if search["pass"] else "INVALID",
            "independent_label": "VALID" if new else "INVALID",
            "flip": flip,
            "flip_reason": reason,
            "near_boundary": indep.near_boundary,
            "numerical_failure": indep.numerical_failure,
            "independent": indep.as_dict(),
            "search": search,
            "family": "fir" if is_fir(r["_task"]) else "iir",
        }
        r["_indep"] = indep
        r["_indep_ok"] = new
        r["_search_ok"] = bool(search["pass"])
        r["_flip"] = flip
        r["_flip_reason"] = reason
        out.append(rec)
    return out


def attach_distances(rows):
    for r in rows:
        r["_db"] = distance_bundle(r["_impl"], r["_href"], r["_task"])


def _frr_far(valids, invalids, key, tau):
    nv = len(valids)
    ni = len(invalids)
    frr_n = sum(1 for r in valids if r["_db"][key] > tau)
    far_n = sum(1 for r in invalids if r["_db"][key] <= tau)
    return {
        "n_valid": nv,
        "n_invalid": ni,
        "frr_n": frr_n,
        "far_n": far_n,
        "frr": None if nv == 0 else frr_n / nv,
        "far": None if ni == 0 else far_n / ni,
    }


def separability(valids, invalids, key):
    if not valids or not invalids:
        return {
            "D_V": None,
            "D_I": None,
            "G_r": None,
            "exact_threshold_exists": False,
            "farthest_valid": None,
            "nearest_invalid": None,
            "inversion": None,
        }
    dv_row = max(valids, key=lambda r: r["_db"][key])
    di_row = min(invalids, key=lambda r: r["_db"][key])
    dv = float(dv_row["_db"][key])
    di = float(di_row["_db"][key])
    g = di - dv
    inv = None
    if di < dv:
        inv = {
            "valid_id": dv_row["_cid"],
            "invalid_id": di_row["_cid"],
            "d_valid": dv,
            "d_invalid": di,
        }
    return {
        "D_V": dv,
        "D_I": di,
        "G_r": g,
        "exact_threshold_exists": bool(g > 0),
        "farthest_valid": dv_row["_cid"],
        "nearest_invalid": di_row["_cid"],
        "inversion": inv,
    }


def threshold_sweep(valids, invalids, key):
    vd = [float(r["_db"][key]) for r in valids]
    id_ = [float(r["_db"][key]) for r in invalids]
    if not vd or not id_:
        return {"best_balanced_accuracy": None, "zero_frr_zero_far": False}
    cands = sorted(set(vd + id_))
    taus = [-1.0]
    for a, b in zip(cands, cands[1:] + [cands[-1] + 1.0]):
        taus.append(a)
        taus.append(0.5 * (a + b))
    best = None
    zero_both = False
    for tau in taus:
        rec = _frr_far(valids, invalids, key, tau)
        ba = None
        if rec["frr"] is not None and rec["far"] is not None:
            ba = 0.5 * ((1.0 - rec["frr"]) + (1.0 - rec["far"]))
            if rec["frr"] == 0.0 and rec["far"] == 0.0:
                zero_both = True
        if best is None or (ba is not None and ba > best["balanced_accuracy"]):
            best = {**rec, "tau": tau, "balanced_accuracy": ba}
    sep = separability(valids, invalids, key)
    return {
        "best": best,
        "zero_frr_zero_far": zero_both,
        **sep,
        "descriptive_tau": {
            "tau": TAU_DESC,
            **_frr_far(valids, invalids, key, TAU_DESC),
        },
    }


def bootstrap_macro(task_values: list[float], b: int = BOOTSTRAP_B, seed: int = SEED):
    rng = np.random.default_rng(seed)
    x = np.asarray(task_values, float)
    n = len(x)
    stats = []
    for _ in range(b):
        idx = rng.integers(0, n, n)
        stats.append(float(np.mean(x[idx])))
    lo, hi = np.quantile(stats, [0.025, 0.975])
    return {
        "n_tasks": n,
        "mean": float(np.mean(x)),
        "median": float(np.median(x)),
        "iqr": [float(np.quantile(x, 0.25)), float(np.quantile(x, 0.75))],
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "ci95": [float(lo), float(hi)],
        "B": b,
        "seed": seed,
    }


def library_refs_for_task(valids, tid):
    rows = [r for r in valids if r["task_id"] == tid and r.get("source") == "library" and r.get("_indep_ok")]
    fir = is_fir(get_task(tid))
    order = LIBRARY_ORDER_FIR if fir else LIBRARY_ORDER_IIR
    ranked = []
    seen = set()
    for meth in order:
        for r in rows:
            if r.get("method") == meth and r["_cid"] not in seen:
                ranked.append(r)
                seen.add(r["_cid"])
    for r in rows:
        if r["_cid"] not in seen:
            ranked.append(r)
            seen.add(r["_cid"])
    return ranked


def d_to(impl, href, task, key):
    return distance_bundle(impl, href, task)[key]


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


def _gen_worker(code, func_name, q):
    import contextlib
    import io

    from src.runtime import exec_function

    fn, err = exec_function(code, func_name)
    if fn is None:
        q.put(("exec_fail", err, None))
        return
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            y = fn()
        q.put(("ok", None, y))
    except Exception as exc:  # noqa: BLE001
        q.put(("call_fail", f"{type(exc).__name__}:{exc}", None))


def run_generated():
    from multiprocessing import Process, Queue

    gens = json.loads((ROOT / "data" / "arm_n_generations.json").read_text(encoding="utf-8"))
    rows = []

    for rec in gens:
        if rec.get("discarded_not_scored"):
            rows.append({**{k: rec[k] for k in rec if k != "code"}, "status": "discarded"})
            continue
        q: Queue = Queue()
        p = Process(target=_gen_worker, args=(rec.get("code") or "", rec["func_name"], q))
        p.start()
        p.join(15)
        if p.is_alive():
            p.terminate()
            p.join(3)
            rows.append({**{k: rec[k] for k in rec if k != "code"}, "status": "timeout"})
            continue
        if q.empty():
            rows.append({**{k: rec[k] for k in rec if k != "code"}, "status": "empty"})
            continue
        status, err, y = q.get()
        if status != "ok":
            rows.append({**{k: rec[k] for k in rec if k != "code"}, "status": status, "error": err})
            continue
        tid_legacy = rec["task"]
        tid = LEGACY_TO_SUITE_N.get(tid_legacy, tid_legacy)
        task = get_task(tid)
        href = load_impl(json.loads((ROOT / "data" / "valid" / "canonical.json").read_text(encoding="utf-8"))[tid]["path"])
        if isinstance(y, (tuple, list)) and len(y) == 2:
            impl = {"b": np.asarray(y[0], float), "a": np.asarray(y[1], float)}
        else:
            impl = np.asarray(y, float)
        try:
            indep = verify_specification(tid, impl)
            db = distance_bundle(impl, href, task)
        except Exception as exc:  # noqa: BLE001
            rows.append({**{k: rec[k] for k in rec if k != "code"}, "status": "verify_fail", "error": str(exc)})
            continue
        witness = bool(indep.ok and db["d_coeff_mag_equiv"] > TAU_DESC)
        rows.append(
            {
                "generation_id": rec["generation_id"],
                "legacy_task": tid_legacy,
                "task_id": tid,
                "model": rec.get("model"),
                "status": "executed",
                "independent_ok": bool(indep.ok),
                "near_boundary": indep.near_boundary,
                "distances": db,
                "S1_R0_witness": witness,
                "independent": indep.as_dict(),
            }
        )
    return rows


def run_all() -> dict:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_CAND_DIR.mkdir(parents=True, exist_ok=True)
    BOUNDARY_DIR.mkdir(parents=True, exist_ok=True)

    canon_meta, hrefs, valids, invalids = load_base()
    print(f"[1] recertify {len(valids)} valids + {len(invalids)} invalids")
    vcert = recertify(valids, True)
    icert = recertify(invalids, False)
    flips = [r for r in vcert + icert if r["flip"]]
    attach_distances(valids)
    attach_distances(invalids)

    v_ok = [r for r in valids if r["_indep_ok"]]
    i_ok = [r for r in invalids if not r["_indep_ok"]]
    # independently verified invalids = those the verifier says INVALID
    i_verified_invalid = [r for r in invalids if not r["_indep_ok"]]
    v_verified_valid = v_ok

    recert_summary = {
        "total_candidates": len(valids) + len(invalids),
        "previous_valid": len(valids),
        "previous_invalid": len(invalids),
        "independent_valid": sum(1 for r in valids if r["_indep_ok"]),
        "independent_invalid": sum(1 for r in invalids if not r["_indep_ok"]),
        "label_flips": len(flips),
        "flips": flips,
        "near_boundary": sum(1 for r in vcert + icert if r["near_boundary"]),
        "numerical_failures": [r for r in vcert + icert if r["numerical_failure"]],
        "fir_valid_indep": sum(1 for r in valids if r["_indep_ok"] and is_fir(r["_task"])),
        "iir_valid_indep": sum(1 for r in valids if r["_indep_ok"] and not is_fir(r["_task"])),
        "headline_374_of_416_survives": None,
    }

    # descriptive FRR on independently verified valids vs canonical, historical d
    frr_hist = sum(1 for r in v_verified_valid if r["_db"]["d_coeff_historical"] > TAU_DESC)
    recert_summary["descriptive_FRR_historical_indep"] = {
        "n": frr_hist,
        "den": len(v_verified_valid),
        "rate": None if not v_verified_valid else frr_hist / len(v_verified_valid),
    }
    recert_summary["headline_374_of_416_survives"] = (
        len(v_verified_valid) == 416
        and recert_summary["label_flips"] == 0
        and frr_hist == 374
    )

    dump_json(OUT_DIR / "recertify.json", {"summary": recert_summary, "valids": vcert, "invalids": icert})

    print("[2] canonicalization audit")
    canon_audit = []
    for r in valids + invalids:
        task = r["_task"]
        if is_fir(task):
            c = canonicalize_fir(r["_impl"])
            canon_audit.append(
                {
                    "id": r["_cid"],
                    "task_id": r["task_id"],
                    "kind": "fir",
                    "n_taps": c.n_taps,
                    "trimmed_trailing": c.trimmed_trailing,
                    "leading_zeros": c.n_leading_zeros,
                    "type1": c.type1,
                    "notes": c.notes,
                    "historical_vs_canonical": {
                        "historical": r["_db"]["d_coeff_historical"],
                        "canonical_mag": r["_db"]["d_coeff_mag_equiv"],
                        "sign_flip_only": r["_db"].get("sign_flip_only"),
                        "zero_pad_artifact": r["_db"].get("zero_pad_artifact"),
                    },
                }
            )
        else:
            from src.verification.canonicalize import canonicalize_iir

            c = canonicalize_iir(r["_impl"])
            canon_audit.append(
                {
                    "id": r["_cid"],
                    "task_id": r["task_id"],
                    "kind": "iir",
                    "n_b": int(len(c.b)),
                    "n_a": int(len(c.a)),
                    "a0_before": c.a0_before,
                    "notes": c.notes,
                    "historical_vs_canonical": {
                        "historical": r["_db"]["d_coeff_historical"],
                        "canonical": r["_db"]["d_coeff_canonical"],
                    },
                }
            )
    dump_json(OUT_DIR / "canonicalization.json", canon_audit)

    print("[3] same-order Type-I feasible-set probe")
    probe_rows = []
    n_tasks = suite_n_tasks()
    for task in n_tasks:
        tid = task["task_id"]
        href = hrefs[tid]
        lib = [r["_impl"] for r in v_verified_valid if r["task_id"] == tid and r.get("source") == "library"]
        raw = run_probes_for_task(task, href, lib)
        kept = []
        for rec in raw:
            if not rec.get("ok"):
                kept.append({k: rec[k] for k in rec if k != "h" and k != "theta"})
                continue
            h_star = rec["h"]
            href_h = canonicalize_fir(href).h
            h, alpha, how = backoff_to_independent(tid, href_h, h_star)
            if h is None:
                kept.append(
                    {
                        "task_id": tid,
                        "direction": rec["direction"],
                        "family": rec["family"],
                        "sense": rec["sense"],
                        "n_taps": rec.get("n_taps"),
                        "independent_ok": False,
                        "genuine_same_order": False,
                        "reference_discordant": False,
                        "backoff_alpha": alpha,
                        "backoff": how,
                        "reason": how,
                    }
                )
                continue
            indep = verify_specification(tid, h)
            db = distance_bundle(h, href, task)
            genuine = bool(indep.ok and db["same_order_canonical"] and _genuine_alt(db, h, href, task))
            discord = bool(genuine and db["d_coeff_mag_equiv"] > TAU_DESC)
            fname = f"{tid}__{rec['direction']}__{rec['sense']}.npy"
            rel = None
            if genuine:
                np.save(PROBE_CAND_DIR / fname, h)
                rel = str((PROBE_CAND_DIR / fname).relative_to(ROOT)).replace("\\", "/")
            kept.append(
                {
                    "task_id": tid,
                    "direction": rec["direction"],
                    "family": rec["family"],
                    "sense": rec["sense"],
                    "n_taps": rec.get("n_taps"),
                    "independent_ok": bool(indep.ok),
                    "genuine_same_order": genuine,
                    "reference_discordant": discord,
                    "backoff_alpha": alpha,
                    "backoff": how,
                    "d_coeff_mag_equiv": db["d_coeff_mag_equiv"],
                    "d_resp_band": db["d_resp_band"],
                    "passband_error": indep.passband_error,
                    "stopband_error": indep.stopband_error,
                    "near_boundary": indep.near_boundary,
                    "path": rel,
                    "reason": rec.get("reason"),
                }
            )
        probe_rows.extend(kept)
        print(f"    {tid}: probes={len(raw)} genuine={sum(1 for k in kept if k.get('genuine_same_order'))}")

    probe_by_task = defaultdict(list)
    for r in probe_rows:
        if r.get("task_id"):
            probe_by_task[r["task_id"]].append(r)
    existing_so = {}
    for t in n_tasks:
        tid = t["task_id"]
        href = hrefs[tid]
        rows = []
        for r in v_verified_valid:
            if r["task_id"] != tid:
                continue
            if not r["_db"].get("same_order_canonical"):
                continue
            if not _genuine_alt(r["_db"], r["_impl"], href, t):
                continue
            rows.append(r)
        existing_so[tid] = {
            "n": len(rows),
            "n_discord": sum(1 for r in rows if r["_db"]["d_coeff_mag_equiv"] > TAU_DESC),
        }

    probe_summary = {
        "n_fir_tasks": sum(1 for t in n_tasks if is_fir(t)),
        "n_all_tasks": len(n_tasks),
        "existing_same_order": existing_so,
        "tasks_with_existing_same_order_discord": sum(
            1 for t in n_tasks if existing_so[t["task_id"]]["n_discord"] > 0
        ),
        "tasks_with_same_order_alt": sum(
            1
            for t in n_tasks
            if is_fir(t)
            and (
                any(r.get("genuine_same_order") for r in probe_by_task[t["task_id"]])
                or existing_so[t["task_id"]]["n"] > 0
            )
        ),
        "tasks_with_discordant_alt": sum(
            1
            for t in n_tasks
            if is_fir(t)
            and (
                any(r.get("reference_discordant") for r in probe_by_task[t["task_id"]])
                or existing_so[t["task_id"]]["n_discord"] > 0
            )
        ),
        "tasks_with_probe_discordant_alt": sum(
            1
            for t in n_tasks
            if is_fir(t) and any(r.get("reference_discordant") for r in probe_by_task[t["task_id"]])
        ),
        "tight_discordant": sum(
            1
            for t in n_tasks
            if is_fir(t) and "tight" in t["task_id"] and any(r.get("reference_discordant") for r in probe_by_task[t["task_id"]])
        ),
        "loose_discordant": sum(
            1
            for t in n_tasks
            if is_fir(t) and "loose" in t["task_id"] and any(r.get("reference_discordant") for r in probe_by_task[t["task_id"]])
        ),
    }
    dump_json(OUT_DIR / "feasible_probe.json", {"summary": probe_summary, "rows": probe_rows})

    # attach probe valids into a confirmatory pool (not pooled into 416)
    probe_valids = []
    for r in probe_rows:
        if r.get("genuine_same_order") and r.get("path"):
            impl = np.load(r["path"])
            tid = r["task_id"]
            probe_valids.append(
                {
                    "task_id": tid,
                    "_impl": impl,
                    "_href": hrefs[tid],
                    "_task": get_task(tid),
                    "_cid": r["path"],
                    "_indep_ok": True,
                    "source": "feasible_set_probe",
                    "_db": distance_bundle(impl, hrefs[tid], get_task(tid)),
                }
            )

    print("[4] boundary invalids")
    boundary_rows = []
    for task in n_tasks:
        tid = task["task_id"]
        href = hrefs[tid]
        constructed = construct_boundary_invalids(href, task)
        for j, rec in enumerate(constructed):
            if not rec["construction_ok"]:
                boundary_rows.append({"task_id": tid, **{k: rec[k] for k in rec if k != "impl"}, "independent_invalid": False})
                continue
            impl = rec["impl"]
            indep = verify_specification(tid, impl)
            ok_invalid = not indep.ok
            fname = f"{tid}__{rec['mechanism']}__e{rec['epsilon']}"
            if isinstance(impl, dict):
                path = BOUNDARY_DIR / f"{fname}.npz"
                np.savez(path, b=impl["b"], a=impl["a"])
                loadp = impl
            else:
                path = BOUNDARY_DIR / f"{fname}.npy"
                np.save(path, impl)
                loadp = impl
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            db = distance_bundle(loadp, href, task) if ok_invalid or True else None
            boundary_rows.append(
                {
                    "task_id": tid,
                    "mechanism": rec["mechanism"],
                    "epsilon": rec["epsilon"],
                    "meta": rec["meta"],
                    "path": rel,
                    "independent_invalid": bool(ok_invalid),
                    "independent_ok": bool(indep.ok),
                    "near_boundary": indep.near_boundary,
                    "passband_error": indep.passband_error,
                    "stopband_error": indep.stopband_error,
                    "distances": db,
                    "cid": rel,
                }
            )
    dump_json(OUT_DIR / "boundary_invalids.json", boundary_rows)

    # verified boundary invalids as extra universe points
    b_invalids = []
    for r in boundary_rows:
        if not r.get("independent_invalid"):
            continue
        tid = r["task_id"]
        p = Path(r["path"])
        impl = load_impl(str(p.relative_to(ROOT)) if p.is_absolute() else r["path"])
        b_invalids.append(
            {
                "task_id": tid,
                "_impl": impl,
                "_href": hrefs[tid],
                "_task": get_task(tid),
                "_cid": r["cid"],
                "_indep_ok": False,
                "source": "boundary_invalid",
                "_db": distance_bundle(impl, hrefs[tid], get_task(tid)),
            }
        )

    print("[5] per-task separability + threshold sweep")
    task_metrics = []
    for task in n_tasks:
        tid = task["task_id"]
        vv = [r for r in v_verified_valid if r["task_id"] == tid]
        # universe invalids = independently verified original mutants + boundary
        ii = [r for r in i_verified_invalid if r["task_id"] == tid] + [r for r in b_invalids if r["task_id"] == tid]
        ii_mech = [r for r in i_verified_invalid if r["task_id"] == tid]
        ii_bound = [r for r in b_invalids if r["task_id"] == tid]
        # also include probe valids in U for D_V confirmatory
        vv_conf = vv + [r for r in probe_valids if r["task_id"] == tid]
        rec = {
            "task_id": tid,
            "family": "fir" if is_fir(task) else "iir",
            "tight": "tight" in tid,
            "n_valid_indep": len(vv),
            "n_valid_with_probe": len(vv_conf),
            "n_invalid_mech": len(ii_mech),
            "n_invalid_boundary": len(ii_bound),
            "coeff_constructed": threshold_sweep(vv, ii_mech, "d_coeff_mag_equiv"),
            "coeff_with_boundary": threshold_sweep(vv_conf, ii, "d_coeff_mag_equiv"),
            "resp_constructed": threshold_sweep(vv, ii_mech, "d_resp_band"),
            "resp_with_boundary": threshold_sweep(vv_conf, ii, "d_resp_band"),
            "historical_coeff": threshold_sweep(vv, ii_mech, "d_coeff_historical"),
            "descriptive_frr_tau05_hist": None
            if not vv
            else sum(1 for r in vv if r["_db"]["d_coeff_historical"] > TAU_DESC) / len(vv),
            "descriptive_frr_tau05_canon": None
            if not vv
            else sum(1 for r in vv if r["_db"]["d_coeff_mag_equiv"] > TAU_DESC) / len(vv),
            "has_discordant_valid": any(r["_db"]["d_coeff_mag_equiv"] > TAU_DESC for r in vv),
            "has_genuine_probe_discord": any(r.get("reference_discordant") for r in probe_by_task[tid]),
        }
        task_metrics.append(rec)
        print(
            f"    {tid}: G_coeff={rec['coeff_with_boundary']['G_r']} "
            f"G_resp={rec['resp_with_boundary']['G_r']}"
        )
    dump_json(OUT_DIR / "task_metrics.json", task_metrics)

    print("[6] reference-choice robustness")
    ref_choice = []
    for task in n_tasks:
        tid = task["task_id"]
        vv = [r for r in v_verified_valid if r["task_id"] == tid]
        ii = [r for r in i_verified_invalid if r["task_id"] == tid] + [r for r in b_invalids if r["task_id"] == tid]
        refs = library_refs_for_task(v_verified_valid, tid)
        per = []
        for ref in refs:
            # recompute distances to this reference
            vv2, ii2 = [], []
            for r in vv:
                db = distance_bundle(r["_impl"], ref["_impl"], task)
                vv2.append({**r, "_db": db, "_cid": r["_cid"]})
            for r in ii:
                db = distance_bundle(r["_impl"], ref["_impl"], task)
                ii2.append({**r, "_db": db, "_cid": r["_cid"]})
            per.append(
                {
                    "ref_id": ref["_cid"],
                    "method": ref.get("method"),
                    "coeff": threshold_sweep(vv2, ii2, "d_coeff_mag_equiv"),
                    "resp": threshold_sweep(vv2, ii2, "d_resp_band"),
                    "frr_tau05": None
                    if not vv2
                    else sum(1 for r in vv2 if r["_db"]["d_coeff_mag_equiv"] > TAU_DESC) / len(vv2),
                }
            )
        gs = [p["coeff"]["G_r"] for p in per if p["coeff"]["G_r"] is not None]
        ref_choice.append(
            {
                "task_id": tid,
                "n_refs": len(per),
                "any_ref_separable_coeff": any(p["coeff"]["exact_threshold_exists"] for p in per),
                "all_refs_nonseparable_coeff": all(not p["coeff"]["exact_threshold_exists"] for p in per) if per else None,
                "G_coeff_min": None if not gs else float(min(gs)),
                "G_coeff_median": None if not gs else float(np.median(gs)),
                "G_coeff_max": None if not gs else float(max(gs)),
                "per_reference": per,
            }
        )
    dump_json(OUT_DIR / "reference_choice.json", ref_choice)

    print("[7] multi-reference")
    multi = []
    for task in n_tasks:
        tid = task["task_id"]
        vv = [r for r in v_verified_valid if r["task_id"] == tid] + [r for r in probe_valids if r["task_id"] == tid]
        ii = [r for r in i_verified_invalid if r["task_id"] == tid] + [r for r in b_invalids if r["task_id"] == tid]
        refs = library_refs_for_task(v_verified_valid, tid)
        ks = []
        for k in list(K_GRID) + ["all"]:
            if k == "all":
                use = refs
                kn = len(use)
            else:
                kn = int(k)
                use = refs[:kn] if refs else []
            if not use:
                ks.append({"K": kn, "available": 0})
                continue

            def dmin(impl, key="d_coeff_mag_equiv"):
                return min(distance_bundle(impl, ref["_impl"], task)[key] for ref in use)

            vv2 = [{**r, "_db": {"d_coeff_mag_equiv": dmin(r["_impl"]), "d_resp_band": dmin(r["_impl"], "d_resp_band")}, "_cid": r["_cid"]} for r in vv]
            ii2 = [{**r, "_db": {"d_coeff_mag_equiv": dmin(r["_impl"]), "d_resp_band": dmin(r["_impl"], "d_resp_band")}, "_cid": r["_cid"]} for r in ii]
            ks.append(
                {
                    "K": kn if k != "all" else f"all:{len(use)}",
                    "available": len(use),
                    "methods": [u.get("method") for u in use],
                    "coeff": threshold_sweep(vv2, ii2, "d_coeff_mag_equiv"),
                    "resp": threshold_sweep(vv2, ii2, "d_resp_band"),
                }
            )
        multi.append({"task_id": tid, "k_sweep": ks})
    dump_json(OUT_DIR / "multi_reference.json", multi)

    print("[8] task-level statistics")
    frrs = [t["descriptive_frr_tau05_canon"] for t in task_metrics if t["descriptive_frr_tau05_canon"] is not None]
    disagree = sum(1 for t in task_metrics if t["has_discordant_valid"])
    pooled_n = sum(1 for r in v_verified_valid if r["_db"]["d_coeff_mag_equiv"] > TAU_DESC)
    by_src = defaultdict(lambda: {"n": 0, "discord": 0})
    for r in v_verified_valid:
        src = r.get("source") or "unknown"
        by_src[src]["n"] += 1
        if r["_db"]["d_coeff_mag_equiv"] > TAU_DESC:
            by_src[src]["discord"] += 1
    task_stats = {
        "n_tasks": len(task_metrics),
        "tasks_with_reference_disagreement": disagree,
        "macro": bootstrap_macro(frrs) if frrs else None,
        "pooled_descriptive_FRR": {
            "n": pooled_n,
            "den": len(v_verified_valid),
            "rate": None if not v_verified_valid else pooled_n / len(v_verified_valid),
        },
        "by_source": dict(by_src),
        "n_coeff_nonsep": sum(1 for t in task_metrics if not t["coeff_with_boundary"]["exact_threshold_exists"]),
        "n_resp_nonsep": sum(1 for t in task_metrics if not t["resp_with_boundary"]["exact_threshold_exists"]),
        "n_boundary_inversions": sum(1 for t in task_metrics if t["coeff_with_boundary"]["inversion"] is not None),
    }
    dump_json(OUT_DIR / "task_stats.json", task_stats)

    print("[9] singleton positive control")
    s_rows = []
    for task in suite_s_tasks():
        tid = task["task_id"]
        href_fn = CANONICAL[tid]
        items = [("canonical", href_fn)]
        if tid in ALTERNATE_VALID:
            items.append(("alternate", ALTERNATE_VALID[tid]))
        val_s, inv_s = [], []
        for kind, fn in items:
            indep = verify_specification(tid, fn)
            # Suite S distance: output disagreement vs canonical on the registered test vector
            d = 0.0 if kind == "canonical" else suite_s_disagreement(tid, fn, href_fn)
            rec = {
                "task_id": tid,
                "kind": kind,
                "_cid": f"suite_s/{tid}/{kind}",
                "_indep_ok": bool(indep.ok),
                "_db": {"d_coeff_mag_equiv": d, "d_resp_band": d, "d_coeff_historical": d},
            }
            s_rows.append({**rec, "independent": indep.as_dict(), "role": "valid"})
            if indep.ok:
                val_s.append(rec)
        for mech, fn in MUTANTS.get(tid, {}).items():
            indep = verify_specification(tid, fn)
            d = suite_s_disagreement(tid, fn, href_fn)
            rec = {
                "task_id": tid,
                "kind": mech,
                "_cid": f"suite_s/{tid}/{mech}",
                "_indep_ok": bool(indep.ok),
                "_db": {"d_coeff_mag_equiv": d, "d_resp_band": d, "d_coeff_historical": d},
            }
            s_rows.append({**rec, "independent": indep.as_dict(), "role": "invalid"})
            if not indep.ok:
                inv_s.append(rec)
        # per-task sep stored later
    # recompute per-task S
    s_metrics = []
    for task in suite_s_tasks():
        tid = task["task_id"]
        vv = [r for r in s_rows if r["task_id"] == tid and r["role"] == "valid" and r["_indep_ok"]]
        ii = [r for r in s_rows if r["task_id"] == tid and r["role"] == "invalid" and not r["_indep_ok"]]
        s_metrics.append(
            {
                "task_id": tid,
                "n_valid": len(vv),
                "n_invalid": len(ii),
                "coeff": threshold_sweep(vv, ii, "d_coeff_mag_equiv"),
            }
        )
    dump_json(OUT_DIR / "singleton.json", {"rows": s_rows, "metrics": s_metrics})

    print("[10] generated-code witness revalidation")
    gen_rows = run_generated()
    dump_json(OUT_DIR / "generated_witness.json", gen_rows)
    n_wit = sum(1 for r in gen_rows if r.get("S1_R0_witness"))
    print(f"    S=1,R=0 witnesses after independent verification: {n_wit}")

    env = {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "seed": SEED,
        "verifier": VERIFIER_VERSION,
        "elapsed_s": time.time() - t0,
        "cwd": str(Path.cwd()),
        "hashes": {
            "suite_n": sha256_file(ROOT / "registry" / "suite_n.json"),
            "suite_s": sha256_file(ROOT / "registry" / "suite_s.json"),
            "valid_manifest": sha256_file(ROOT / "data" / "valid" / "manifest.json"),
            "invalid_manifest": sha256_file(ROOT / "data" / "invalid" / "manifest.json"),
        },
    }
    dump_json(OUT_DIR / "environment.json", env)

    summary = {
        "recert": recert_summary,
        "probe": probe_summary,
        "task_stats": task_stats,
        "generated_witnesses": n_wit,
        "elapsed_s": env["elapsed_s"],
    }
    dump_json(OUT_DIR / "summary.json", summary)
    print(f"done in {env['elapsed_s']:.1f}s")
    return summary
