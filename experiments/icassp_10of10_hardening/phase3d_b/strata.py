"""Generator-family and DSP-structural transfer. Groups are frozen, not inferred."""
from __future__ import annotations

import json
from statistics import mean

from experiments.icassp_10of10_hardening.phase3d_b.config import FIR_FAMILIES, IIR_FAMILIES, OUT_DIR
from experiments.icassp_10of10_hardening.phase3d_b.score import load_challenge, task_factors
from src.verification.io_utils import dump_json


def _rate(rows: list[dict]) -> float | None:
    if not rows:
        return None
    acc = sum(1 for r in rows if r["accepted"])
    return acc / len(rows)


def generator_and_structure() -> dict:
    hv = load_challenge("H_VALID.json")
    coeff = json.loads((OUT_DIR / "transfer_details_coeff.json").read_text(encoding="utf-8"))
    resp = json.loads((OUT_DIR / "transfer_details_resp.json").read_text(encoding="utf-8"))
    meta = {m["id"]: m for m in hv["members"]}

    def enrich(details):
        out = []
        for r in details:
            m = meta[r["id"]]
            fac = task_factors(r["task"])
            order = None
            im = m.get("impl_meta") or {}
            if "n_taps" in im:
                order = int(im["n_taps"])
            elif "n_a" in im:
                order = max(0, int(im["n_a"]) - 1)
            out.append({**r, "generator_id": m["generator_id"], "order": order, **fac})
        return out

    c = enrich(coeff)
    r = enrich(resp)
    families = list(FIR_FAMILIES) + list(IIR_FAMILIES)
    gen_rows = []
    for g in families:
        gc = [x for x in c if x["generator_id"] == g]
        gr = [x for x in r if x["generator_id"] == g]
        gen_rows.append(
            {
                "generator": g,
                "n": len(gc),
                "coeff_transfer": _rate(gc),
                "resp_transfer": _rate(gr),
            }
        )

    def struct(rows, key, values):
        return {v: _rate([x for x in rows if x[key] == v]) for v in values}

    # Fixed descriptive order bins from frozen metadata quantiles (FIR taps / IIR order).
    orders = sorted(x["order"] for x in c if x["order"] is not None)
    q = lambda p: orders[int(round(p * (len(orders) - 1)))] if orders else None
    cuts = {"q33": q(1 / 3), "q67": q(2 / 3)}

    def order_bin(o):
        if o is None or cuts["q33"] is None:
            return "unknown"
        if o <= cuts["q33"]:
            return "low_le_q33"
        if o <= cuts["q67"]:
            return "mid_q33_q67"
        return "high_gt_q67"

    for x in c:
        x["order_bin"] = order_bin(x["order"])
    for x in r:
        x["order_bin"] = order_bin(x["order"])

    coeff_rates = [row["coeff_transfer"] for row in gen_rows if row["coeff_transfer"] is not None]
    spread = (max(coeff_rates) - min(coeff_rates)) if coeff_rates else 0.0
    if spread >= 0.25:
        gen_verdict = "CLEAR"
    elif spread >= 0.10:
        gen_verdict = "MIXED"
    else:
        gen_verdict = "WEAK"

    out = {
        "generator_groups_frozen_before_transfer": True,
        "inferred_from_failure": False,
        "generators": gen_rows,
        "generator_effect_verdict": gen_verdict,
        "structure": {
            "coeff": {
                "family": struct(c, "family", ("fir", "iir")),
                "tightness": struct(c, "tightness", ("loose", "tight")),
                "filter_type": struct(c, "filter_type", ("lp", "hp", "bp", "bs")),
                "order_bin": struct(c, "order_bin", ("low_le_q33", "mid_q33_q67", "high_gt_q67")),
            },
            "resp": {
                "family": struct(r, "family", ("fir", "iir")),
                "tightness": struct(r, "tightness", ("loose", "tight")),
                "filter_type": struct(r, "filter_type", ("lp", "hp", "bp", "bs")),
                "order_bin": struct(r, "order_bin", ("low_le_q33", "mid_q33_q67", "high_gt_q67")),
            },
        },
        "order_bin_definition": {
            "rule": "descriptive tertiles of frozen H_VALID n_taps (FIR) or IIR order; not inferred from rejection",
            "q33": cuts["q33"],
            "q67": cuts["q67"],
            "inferential": False,
        },
        "task_macros_from_primary": {
            "note": "FIR/IIR/loose/tight/type macros in transfer_*.json are unweighted task means",
        },
    }
    dump_json(OUT_DIR / "generator_structure_transfer.json", out)
    return out


if __name__ == "__main__":
    generator_and_structure()
