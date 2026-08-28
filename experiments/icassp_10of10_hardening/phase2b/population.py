"""Manuscript 412 population audit. Labels are read, never recomputed."""
from __future__ import annotations

import json
from collections import Counter

from experiments.icassp_10of10_hardening.phase2b.config import FROZEN_DIR
from src.verification.registry_io import get_task, is_fir


def audit() -> dict:
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    boundary = json.loads((FROZEN_DIR / "boundary_invalids.json").read_text(encoding="utf-8"))
    probe = json.loads((FROZEN_DIR / "feasible_probe.json").read_text(encoding="utf-8"))

    valids = [r for r in recert["valids"] if r["independent_label"] == "VALID"]
    mechs = [r for r in recert["invalids"] if r["independent_label"] == "INVALID"]
    bounds = [r for r in boundary if not r.get("independent_ok")]

    def split(rows, key_family=True):
        fir, iir = [], []
        for r in rows:
            if key_family and r.get("family") in ("fir", "iir"):
                (fir if r["family"] == "fir" else iir).append(r)
                continue
            tid = r["task_id"]
            (fir if is_fir(get_task(tid)) else iir).append(r)
        return fir, iir

    v_fir, v_iir = split(valids)
    m_fir, m_iir = split(mechs)
    b_fir, b_iir = split(bounds, key_family=False)

    def tasks(rows):
        return sorted({r["task_id"] for r in rows})

    probes_ok = [
        r
        for r in probe["rows"]
        if r.get("genuine_same_order") and r.get("path") and r.get("independent_ok")
    ]
    p_fir, p_iir = [], []
    for r in probes_ok:
        (p_fir if is_fir(get_task(r["task_id"])) else p_iir).append(r)

    table = [
        {
            "family": "FIR",
            "unique_valid": len(v_fir),
            "mechanism_invalid": len(m_fir),
            "boundary_invalid": len(b_fir),
            "tasks": len(tasks(v_fir)),
            "source": "recertify.json family=fir; boundary_invalids.json FIR tasks",
        },
        {
            "family": "IIR",
            "unique_valid": len(v_iir),
            "mechanism_invalid": len(m_iir),
            "boundary_invalid": len(b_iir),
            "tasks": len(tasks(v_iir)),
            "source": "recertify.json family=iir; boundary_invalids.json IIR tasks",
        },
        {
            "family": "Total",
            "unique_valid": len(valids),
            "mechanism_invalid": len(mechs),
            "boundary_invalid": len(bounds),
            "tasks": len(tasks(valids)),
            "source": "constructed independently labeled occupants",
        },
    ]
    blocker = len(valids) != 412 or len(v_fir) + len(v_iir) != 412
    return {
        "blocker": blocker,
        "verdict": "PHASE2B_POPULATION_BLOCKER" if blocker else "RECONCILES_TO_412",
        "table": table,
        "fir_valid": len(v_fir),
        "iir_valid": len(v_iir),
        "fir_mech": len(m_fir),
        "iir_mech": len(m_iir),
        "fir_boundary": len(b_fir),
        "iir_boundary": len(b_iir),
        "fir_tasks": tasks(v_fir),
        "iir_tasks": tasks(v_iir),
        "probe_fir_valid": len(p_fir),
        "probe_iir_valid": len(p_iir),
        "valid_task_counts": dict(Counter(r["task_id"] for r in valids)),
    }
