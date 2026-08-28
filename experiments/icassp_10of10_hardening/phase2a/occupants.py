"""Frozen unique FIR occupants. Labels are read, never recomputed."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase2a.config import FROZEN_DIR, PHASE1_DIR
from src.verification.io_utils import load_impl
from src.verification.registry_io import get_task, is_fir


def load_phase1_status() -> dict[str, str]:
    payload = json.loads((PHASE1_DIR / "fir_continuous_certification.json").read_text(encoding="utf-8"))
    return {r["occupant"]: r["continuous_status"] for r in payload["rows"]}


def _fir_constructed_valids():
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    out = []
    for r in recert["valids"]:
        if r["independent_label"] != "VALID" or r.get("family") != "fir":
            continue
        out.append(
            {
                "cid": r["id"],
                "task_id": r["task_id"],
                "role": "constructed_valid",
                "old_label": "VALID",
                "impl": load_impl(r["id"]),
            }
        )
    return out


def _fir_mechanism_invalids():
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    out = []
    for r in recert["invalids"]:
        if r["independent_label"] != "INVALID" or r.get("family") != "fir":
            continue
        out.append(
            {
                "cid": r["id"],
                "task_id": r["task_id"],
                "role": "mechanism_invalid",
                "old_label": "INVALID",
                "impl": load_impl(r["id"]),
            }
        )
    return out


def _fir_boundary_invalids():
    boundary = json.loads((FROZEN_DIR / "boundary_invalids.json").read_text(encoding="utf-8"))
    out = []
    for r in boundary:
        if r.get("independent_ok"):
            continue
        if not is_fir(get_task(r["task_id"])):
            continue
        path = r.get("path") or r.get("cid")
        out.append(
            {
                "cid": path,
                "task_id": r["task_id"],
                "role": "boundary_invalid",
                "old_label": "INVALID",
                "impl": load_impl(path),
            }
        )
    return out


def _fir_probes():
    probe = json.loads((FROZEN_DIR / "feasible_probe.json").read_text(encoding="utf-8"))
    out = []
    for r in probe["rows"]:
        if not r.get("genuine_same_order") or not r.get("path") or not r.get("independent_ok"):
            continue
        out.append(
            {
                "cid": r["path"],
                "task_id": r["task_id"],
                "role": "probe_valid",
                "old_label": "VALID",
                "impl": load_impl(r["path"]),
            }
        )
    return out


def load_manuscript_fir_occupants() -> dict:
    """Unique FIR files used by the manuscript 412 (FIR part) plus FIR invalids."""
    return {
        "constructed_valid": _fir_constructed_valids(),
        "mechanism_invalid": _fir_mechanism_invalids(),
        "boundary_invalid": _fir_boundary_invalids(),
        "probe_valid_confirmatory": _fir_probes(),
    }
