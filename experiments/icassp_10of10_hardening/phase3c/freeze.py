"""Freeze Phase-3B optimal catalogs before any holdout scoring."""
from __future__ import annotations

import json
import math

from experiments.icassp_10of10_hardening.phase3c.config import G_ZERO_ABS, PHASE3B_DIR
from src.verification.io_utils import sha256_file


def _tau_safe(d_v: float | None, d_i: float | None) -> dict:
    if d_v is None or d_i is None:
        return {"tau_safe": None, "ok": False, "reason": "missing_D"}
    if not (d_v < d_i and (d_i - d_v) > G_ZERO_ABS):
        return {"tau_safe": None, "ok": False, "reason": "nonpositive_gap"}
    tau = math.nextafter(float(d_i), 0.0)
    if tau < d_v:
        return {"tau_safe": None, "ok": False, "reason": "nextafter_below_DV"}
    return {
        "tau_safe": tau,
        "ok": True,
        "convention": "largest IEEE-754 binary64 strictly less than D_I",
        "covers_base_valids": tau >= d_v,
        "rejects_base_invalids": tau < d_i,
    }


def freeze_base_catalogs() -> dict:
    src = PHASE3B_DIR / "reference_catalog_complexity.json"
    rcc = json.loads(src.read_text(encoding="utf-8"))
    src_hash = sha256_file(src)
    tasks = []
    for metric in ("coeff", "resp"):
        bundle = rcc[metric]
        for t in bundle["tasks"]:
            p = t["primary"]
            ts = _tau_safe(p.get("D_V"), p.get("D_I"))
            tasks.append(
                {
                    "task": t["task"],
                    "family": t.get("family"),
                    "metric": metric,
                    "n_valid_phase3b": t["n_valid"],
                    "n_invalid_phase3b": t["n_invalid"],
                    "status": p.get("status"),
                    "K_obs_star": p.get("K_obs_star"),
                    "catalog_ids": list(p.get("catalog_ids") or []),
                    "catalog_indices": list(p.get("catalog_indices") or []),
                    "stored_tau": p.get("tau"),
                    "D_V": p.get("D_V"),
                    "D_I": p.get("D_I"),
                    "G_R": p.get("G_R"),
                    "tau_safe": ts,
                    "existing_hierarchy_exact": t.get("existing"),
                    "phase1": t.get("phase1"),
                }
            )
    return {
        "source": "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json",
        "source_sha256": src_hash,
        "derived_only_from_phase3b": True,
        "holdout_used_in_derivation": False,
        "tau_safe_rule": "math.nextafter(D_I, 0.0); not retuned on any external set",
        "tasks": tasks,
    }
