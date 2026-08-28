"""Catalog-blind generation / certification / mutation pipeline."""
from __future__ import annotations

import json

import numpy as np

from experiments.icassp_10of10_hardening.phase3d_a.blinding import forbid_catalog_io
from experiments.icassp_10of10_hardening.phase3d_a.certify import certify_candidate, grid_screen
from experiments.icassp_10of10_hardening.phase3d_a.config import (
    ATTEMPTS_PER_FAMILY,
    FIR_FAMILIES,
    IIR_FAMILIES,
    MUTATION_LADDER,
    OUT_DIR,
    ROOT,
)
from experiments.icassp_10of10_hardening.phase3d_a.generators import generate_one
from experiments.icassp_10of10_hardening.phase3d_a.io_impl import rel_path, save_impl
from experiments.icassp_10of10_hardening.phase3d_a.mutate import mutate_fir, mutate_iir
from experiments.icassp_10of10_hardening.phase3d_a.prior import fir_dup_of, iir_dup_of, load_prior, spec_margin_grid
from experiments.icassp_10of10_hardening.phase3d_a.seeds import seed_record
from src.verification.io_utils import dump_json
from src.verification.registry_io import is_fir, suite_n_tasks


def _jsonable_impl_meta(family: str, impl) -> dict:
    if family == "fir":
        h = np.asarray(impl, float).reshape(-1)
        return {"n_taps": int(h.size), "l2": float(np.linalg.norm(h))}
    b = np.asarray(impl["b"], float).reshape(-1)
    a = np.asarray(impl["a"], float).reshape(-1)
    return {"n_b": int(b.size), "n_a": int(a.size), "l2": float(np.linalg.norm(np.concatenate([b, a])))}


def generate_attempts() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    with forbid_catalog_io():
        for task in suite_n_tasks():
            tid = task["task_id"]
            fams = FIR_FAMILIES if is_fir(task) else IIR_FAMILIES
            family = "fir" if is_fir(task) else "iir"
            for gid in fams:
                for a in range(ATTEMPTS_PER_FAMILY):
                    seed = seed_record(tid, gid, a)
                    print(f"[phase3d_a] generate {tid} {gid} a={a}", flush=True)
                    rec = {
                        "task_id": tid,
                        "family": family,
                        "generator_id": gid,
                        "attempt_index": a,
                        "seed_u64": seed["seed_u64"],
                        "seed_sha256": seed["sha256"],
                        "label": "CANDIDATE_UNCERTIFIED",
                    }
                    gen = generate_one(task, gid, a)
                    rec["params"] = gen.get("params")
                    if not gen.get("ok"):
                        rec["generation_ok"] = False
                        rec["generation_reason"] = gen.get("reason")
                        rec["grid_pass"] = False
                        rows.append(rec)
                        continue
                    rec["generation_ok"] = True
                    rec["generation_reason"] = None
                    impl = gen["impl"]
                    rel = rel_path(tid, f"{gid}__a{a:02d}", family)
                    rec["impl_rel"] = rel
                    rec["impl_sha256"] = save_impl(rel, family, impl)
                    rec["impl_meta"] = _jsonable_impl_meta(family, impl)
                    scr = grid_screen(tid, impl)
                    rec["grid_pass"] = bool(scr.get("pass"))
                    rec["grid_residuals"] = scr.get("residuals")
                    rec["grid_reason"] = None if scr.get("pass") else (scr.get("reason") or "GRID_SCREEN_FAIL")
                    rows.append(rec)
    bundle = {"n": len(rows), "attempts": rows, "blinding": "forbid_catalog_io"}
    dump_json(OUT_DIR / "all_attempts.json", bundle)
    return bundle


def certify_and_admit() -> dict:
    attempts = json.loads((OUT_DIR / "all_attempts.json").read_text(encoding="utf-8"))
    prior = load_prior()
    tasks = {t["task_id"]: t for t in suite_n_tasks()}
    h_valid = []
    admitted_fir = []
    admitted_iir = []
    n_dup_prior = 0
    n_dup_within = 0
    with forbid_catalog_io():
        for rec in attempts["attempts"]:
            if not rec.get("generation_ok") or not rec.get("grid_pass"):
                rec["continuous_status"] = None
                continue
            task = tasks[rec["task_id"]]
            from src.verification.io_utils import load_impl

            impl = load_impl(rec["impl_rel"])
            print(f"[phase3d_a] certify {rec['task_id']} {rec['generator_id']} a={rec['attempt_index']}", flush=True)
            cert = certify_candidate(task, impl)
            rec["continuous_status"] = cert.get("status")
            rec["continuous"] = cert
            if cert.get("status") != "CERTIFIED_VALID":
                continue
            family = rec["family"]
            if family == "fir":
                d0 = fir_dup_of(impl, prior["fir"])
                d1 = fir_dup_of(impl, admitted_fir)
            else:
                d0 = iir_dup_of(impl, prior["iir"])
                d1 = iir_dup_of(impl, admitted_iir)
            if d0:
                rec["exact_duplicate"] = {"against": "prior_science", "cid": d0}
                n_dup_prior += 1
                continue
            if d1:
                rec["exact_duplicate"] = {"against": "holdout", "cid": d1}
                n_dup_within += 1
                continue
            rec["exact_duplicate"] = None
            rec["label"] = "H_VALID"
            member = {
                "id": rec["impl_rel"],
                "task_id": rec["task_id"],
                "family": family,
                "generator_id": rec["generator_id"],
                "attempt_index": rec["attempt_index"],
                "seed_u64": rec["seed_u64"],
                "seed_sha256": rec["seed_sha256"],
                "impl_sha256": rec["impl_sha256"],
                "params": rec["params"],
                "continuous_status": "CERTIFIED_VALID",
                "grid_residuals": rec.get("grid_residuals"),
                "spec_margin_grid": spec_margin_grid(rec["task_id"], impl),
                "impl_meta": rec.get("impl_meta"),
            }
            h_valid.append(member)
            slot = {"cid": rec["impl_rel"], "impl": impl}
            if family == "fir":
                admitted_fir.append(slot)
            else:
                admitted_iir.append(slot)
    dump_json(OUT_DIR / "all_attempts.json", attempts)
    hv = {
        "n": len(h_valid),
        "members": h_valid,
        "exact_duplicates_vs_prior": n_dup_prior,
        "exact_duplicates_within": n_dup_within,
        "undecided_included": 0,
    }
    dump_json(OUT_DIR / "H_VALID.json", hv)
    return hv


def generate_invalids() -> dict:
    hv = json.loads((OUT_DIR / "H_VALID.json").read_text(encoding="utf-8"))
    prior = load_prior()
    tasks = {t["task_id"]: t for t in suite_n_tasks()}
    from src.verification.io_utils import load_impl

    h_inv = []
    mutation_log = []
    admitted = []
    with forbid_catalog_io():
        for mem in hv["members"]:
            task = tasks[mem["task_id"]]
            family = mem["family"]
            impl0 = load_impl(mem["id"])
            for kind in ("M1", "M2"):
                chosen = None
                ladder_rows = []
                for eps in MUTATION_LADDER:
                    if family == "fir":
                        mut = mutate_fir(impl0, kind, mem["seed_u64"], mem["seed_sha256"], eps)
                    else:
                        mut = mutate_iir(impl0, kind, mem["seed_u64"], mem["seed_sha256"], eps)
                    tag = f"{mem['generator_id']}__a{mem['attempt_index']:02d}__{kind}__e{eps:.0e}"
                    rel = rel_path(mem["task_id"], tag, family)
                    sha = save_impl(rel, family, mut)
                    cert = certify_candidate(task, mut)
                    row = {
                        "progenitor": mem["id"],
                        "task_id": mem["task_id"],
                        "mutation": kind,
                        "eps": eps,
                        "impl_rel": rel,
                        "impl_sha256": sha,
                        "continuous_status": cert.get("status"),
                    }
                    ladder_rows.append(row)
                    if cert.get("status") == "CERTIFIED_INVALID" and chosen is None:
                        if family == "fir":
                            d0 = fir_dup_of(mut, prior["fir"])
                            d1 = fir_dup_of(mut, admitted)
                        else:
                            d0 = iir_dup_of(mut, prior["iir"])
                            d1 = iir_dup_of(mut, admitted)
                        if d0 or d1:
                            row["exact_duplicate"] = d0 or d1
                            continue
                        chosen = {
                            "id": rel,
                            "task_id": mem["task_id"],
                            "family": family,
                            "mutation": kind,
                            "eps": eps,
                            "progenitor": mem["id"],
                            "impl_sha256": sha,
                            "continuous_status": "CERTIFIED_INVALID",
                            "seed_sha256": mem["seed_sha256"],
                        }
                        h_inv.append(chosen)
                        admitted.append({"cid": rel, "impl": mut})
                mutation_log.append(
                    {
                        "progenitor": mem["id"],
                        "task_id": mem["task_id"],
                        "mutation": kind,
                        "ladder": ladder_rows,
                        "admitted": chosen["id"] if chosen else None,
                        "outcome": "ADMITTED" if chosen else "NO_CERTIFIED_INVALID_FROM_MUTATION",
                    }
                )
                print(
                    f"[phase3d_a] mutate {mem['task_id']} {kind} -> {('ADMITTED' if chosen else 'NONE')}",
                    flush=True,
                )
    bundle = {"n": len(h_inv), "members": h_inv, "undecided_included": 0, "log": mutation_log}
    dump_json(OUT_DIR / "H_INVALID.json", bundle)
    return bundle
