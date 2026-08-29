"""Classify tasks into locked R1–R4 using Phase-3A ambient status and Phase-3B ρ."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3b.config import PHASE3A_DIR, RHO_LOW, RHO_MOD


def classify(coeff_bundle: dict, resp_bundle: dict | None) -> dict:
    amb = json.loads((PHASE3A_DIR / "coefficient_ambient.json").read_text(encoding="utf-8"))
    amb_c = {r["task"]: r["ambient_status"] for r in amb["tasks"]}
    amb_r = {}
    if (PHASE3A_DIR / "response_ambient.json").exists():
        ar = json.loads((PHASE3A_DIR / "response_ambient.json").read_text(encoding="utf-8"))
        amb_r = {r["task"]: r["ambient_status"] for r in ar["tasks"]}
    rows = []
    counts = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    for t in coeff_bundle["tasks"]:
        a = amb_c.get(t["task"])
        rho = t.get("rho")
        ambient_exists = a == "AMBIENT_SEPARABLE"
        if rho is None:
            lab = "R4"
        elif ambient_exists and rho <= RHO_LOW:
            lab = "R1"
        elif ambient_exists and rho > RHO_MOD:
            lab = "R2"
        elif (not ambient_exists) and rho > RHO_MOD:
            lab = "R3"
        else:
            lab = "R4"
        counts[lab] += 1
        rows.append(
            {
                "task": t["task"],
                "ambient": a,
                "K_obs_star": t["K_obs_star"],
                "rho": rho,
                "burden_band": t["burden_band"],
                "class": lab,
                "resp_ambient": amb_r.get(t["task"]),
                "resp_K": None
                if resp_bundle is None
                else next((x["K_obs_star"] for x in resp_bundle["tasks"] if x["task"] == t["task"]), None),
            }
        )
    return {"rows": rows, "counts": counts}
