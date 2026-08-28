"""Catalog-oracle distances. Metrics are the frozen Phase-1 confirmatory pair."""
from __future__ import annotations

import json
from collections import defaultdict

from experiments.icassp_10of10_hardening.phase1.best_observed import cache_mags, d_coeff, d_resp_from_mags, _band_mask
from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR, PHASE3DA_DIR, ROOT
from src.verification.io_utils import load_impl
from src.verification.registry_io import get_task


def task_factors(tid: str) -> dict:
    parts = tid.split("_")
    family = parts[0]
    ftype = parts[1]
    tightness = parts[2]
    return {
        "family": family,
        "filter_type": ftype,
        "tightness": tightness,
        "fir": family == "fir",
        "iir": family == "iir",
        "loose": tightness == "loose",
        "tight": tightness == "tight",
    }


def load_frozen_maps() -> tuple[dict, dict]:
    catalogs = json.loads((OUT_DIR / "FROZEN_CATALOGS_PREUNBLIND.json").read_text(encoding="utf-8"))
    thresholds = json.loads((OUT_DIR / "FROZEN_THRESHOLDS_PREUNBLIND.json").read_text(encoding="utf-8"))
    cat = {(r["task"], r["metric"]): r for r in catalogs["tasks"]}
    th = {(r["task"], r["metric"]): r for r in thresholds["tasks"]}
    return cat, th


def load_challenge(name: str) -> dict:
    return json.loads((PHASE3DA_DIR / name).read_text(encoding="utf-8"))


def members_by_task(bundle: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for m in bundle["members"]:
        out[m["task_id"]].append(m)
    return dict(out)


def load_occ(rel: str, extra: dict | None = None) -> dict:
    rec = {"cid": rel, "impl": load_impl(rel)}
    if extra:
        rec.update(extra)
    return rec


def catalog_min_distance(occ: dict, refs: list[dict], task: dict, metric: str) -> dict:
    if not refs:
        return {"d": None, "nearest_id": None}
    if metric == "coeff":
        ds = [(d_coeff(occ["impl"], r["impl"], task), r["cid"]) for r in refs]
    else:
        mask = _band_mask(refs[0]["_w"], task)
        ds = [(d_resp_from_mags(occ["_mag"], r["_mag"], mask), r["cid"]) for r in refs]
    ds.sort(key=lambda x: (x[0], x[1]))
    d, rid = ds[0]
    return {"d": float(d), "nearest_id": rid}


def prepare_refs(ids: list[str], task: dict, metric: str) -> list[dict]:
    refs = [load_occ(i) for i in ids]
    if metric == "resp":
        cache_mags(refs, float(task["sampling_rate"]))
    return refs


def prepare_occs(members: list[dict], task: dict, metric: str) -> list[dict]:
    occs = []
    for m in members:
        rec = load_occ(m["id"], {"member": m})
        occs.append(rec)
    if metric == "resp":
        cache_mags(occs, float(task["sampling_rate"]))
    return occs


def get_task_rec(tid: str) -> dict:
    return get_task(tid)


def root() -> type:
    return ROOT
