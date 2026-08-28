"""Frozen occupants. Labels are read, never recomputed."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase2b.config import FROZEN_DIR
from src.verification.registry_io import get_task, is_fir


def _rows(kind: str) -> list[dict]:
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    if kind == "valid":
        src = [r for r in recert["valids"] if r["independent_label"] == "VALID"]
        return [{"cid": r["id"], "task_id": r["task_id"], "family": r.get("family"), "old_label": "VALID"} for r in src]
    src = [r for r in recert["invalids"] if r["independent_label"] == "INVALID"]
    return [{"cid": r["id"], "task_id": r["task_id"], "family": r.get("family"), "old_label": "INVALID"} for r in src]


def constructed_valids(family: str) -> list[dict]:
    return [r for r in _rows("valid") if r.get("family") == family]


def mechanism_invalids(family: str) -> list[dict]:
    return [r for r in _rows("invalid") if r.get("family") == family]


def boundary_invalids(family: str) -> list[dict]:
    boundary = json.loads((FROZEN_DIR / "boundary_invalids.json").read_text(encoding="utf-8"))
    out = []
    for r in boundary:
        if r.get("independent_ok"):
            continue
        fir = is_fir(get_task(r["task_id"]))
        if (family == "fir") != fir:
            continue
        out.append(
            {
                "cid": r.get("path") or r.get("cid"),
                "task_id": r["task_id"],
                "family": family,
                "old_label": "INVALID",
            }
        )
    return out


def all_iir() -> dict:
    return {
        "valid": constructed_valids("iir"),
        "mechanism_invalid": mechanism_invalids("iir"),
        "boundary_invalid": boundary_invalids("iir"),
    }
