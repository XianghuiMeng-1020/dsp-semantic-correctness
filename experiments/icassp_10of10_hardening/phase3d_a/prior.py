"""Load prior-science coefficients for exact-duplicate checks only. No Phase-3B catalogs."""
from __future__ import annotations

import json

import numpy as np

from experiments.icassp_10of10_hardening.phase3d_a.config import FROZEN_DIR
from src.verification.canonicalize import fir_sign_equivalent, iir_same_tf, unpack
from src.verification.io_utils import load_impl


def _norm(rel: str) -> str:
    return str(rel).replace("\\", "/")


def load_prior() -> dict:
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    probe = json.loads((FROZEN_DIR / "feasible_probe.json").read_text(encoding="utf-8"))
    fir = []
    iir = []
    meta = []
    for r in recert["valids"]:
        if r.get("independent_label") != "VALID":
            continue
        impl = load_impl(r["id"])
        rec = {"cid": _norm(r["id"]), "task_id": r["task_id"], "role": "constructed_valid", "impl": impl}
        meta.append(rec)
        if r.get("family") == "iir" or (isinstance(impl, dict) and impl.get("a") is not None and np.asarray(impl["a"]).size > 1):
            iir.append(rec)
        else:
            fir.append(rec)
    for r in recert["invalids"]:
        if r.get("independent_label") != "INVALID":
            continue
        impl = load_impl(r["id"])
        rec = {"cid": _norm(r["id"]), "task_id": r["task_id"], "role": "mechanism_invalid", "impl": impl}
        meta.append(rec)
        if r.get("family") == "iir" or (isinstance(impl, dict) and impl.get("a") is not None and np.asarray(impl["a"]).size > 1):
            iir.append(rec)
        else:
            fir.append(rec)
    for r in probe["rows"]:
        if not r.get("genuine_same_order") or not r.get("path") or not r.get("independent_ok"):
            continue
        impl = load_impl(r["path"])
        rec = {"cid": _norm(r["path"]), "task_id": r["task_id"], "role": "probe_valid", "impl": impl}
        meta.append(rec)
        fir.append(rec)
    return {"fir": fir, "iir": iir, "n": len(meta)}


def fir_dup_of(h, pool: list[dict]) -> str | None:
    for rec in pool:
        other = rec["impl"]
        ho = other if not isinstance(other, dict) else other.get("b", other)
        if fir_sign_equivalent(h, ho):
            return rec["cid"]
    return None


def iir_dup_of(impl, pool: list[dict]) -> str | None:
    b, a = unpack(impl)
    for rec in pool:
        b2, a2 = unpack(rec["impl"])
        if iir_same_tf(b, a, b2, a2):
            return rec["cid"]
    return None


def spec_margin_grid(task_id: str, impl) -> dict | None:
    """Intrinsic grid residuals; not a reference distance."""
    from src.spec_checker import check_specification

    try:
        rec = check_specification(task_id, impl)
    except Exception:
        return None
    res = rec.get("residuals") or {}
    return {k: res.get(k) for k in ("passband_error", "stopband_error", "stability_error", "other_constraints")}
