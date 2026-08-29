"""Three-level reference-oracle hierarchy. Does not mutate Phase-1 numbers."""
from __future__ import annotations

G_ZERO = 1e-15


def _pos(g) -> bool:
    return g is not None and g != "+INF" and float(g) > G_ZERO


def classify_task(canon_g: float, gobs: float, ambient_kind: str) -> str:
    if _pos(canon_g):
        return "D"
    if _pos(gobs):
        return "C"
    if ambient_kind == "AMBIENT_SEPARABLE":
        return "B"
    if ambient_kind == "NO_AMBIENT_CENTER":
        return "A"
    return "UNDECIDED"


def build_hierarchy(coeff: dict, resp: dict | None) -> dict:
    coeff_rows = []
    for r in coeff["tasks"]:
        typ = classify_task(r["canonical_G"], r["best_observed_valid_reference"], r["ambient_status"])
        coeff_rows.append(
            {
                "task": r["task"],
                "canonical_G": r["canonical_G"],
                "best_observed_valid_reference": r["best_observed_valid_reference"],
                "ambient_status": r["ambient_status"],
                "ambient_margin": r["ambient_margin"],
                "type": typ,
            }
        )
    resp_rows = []
    if resp:
        for r in resp["tasks"]:
            typ = classify_task(r["canonical_G"], r["best_observed_valid_reference"], r["ambient_status"])
            resp_rows.append(
                {
                    "task": r["task"],
                    "canonical_G": r["canonical_G"],
                    "best_observed_valid_reference": r["best_observed_valid_reference"],
                    "ambient_status": r["ambient_status"],
                    "ambient_margin": r["ambient_margin"],
                    "type": typ,
                    "precision_stability": r.get("precision_stability"),
                }
            )

    def counts(rows):
        c = {"A": 0, "B": 0, "C": 0, "D": 0, "UNDECIDED": 0}
        for r in rows:
            c[r["type"]] = c.get(r["type"], 0) + 1
        return c

    cc, rc = counts(coeff_rows), counts(resp_rows)
    return {
        "coeff": {
            "rows": coeff_rows,
            "counts": cc,
            "canonical_nonseparable": sum(1 for r in coeff_rows if not _pos(r["canonical_G"])),
            "best_observed_nonseparable": sum(1 for r in coeff_rows if not _pos(r["best_observed_valid_reference"])),
            "ambient_nonseparable": sum(1 for r in coeff_rows if r["ambient_status"] == "NO_AMBIENT_CENTER"),
        },
        "resp": {
            "rows": resp_rows,
            "counts": rc,
            "canonical_nonseparable": sum(1 for r in resp_rows if not _pos(r["canonical_G"])),
            "best_observed_nonseparable": sum(1 for r in resp_rows if not _pos(r["best_observed_valid_reference"])),
            "ambient_nonseparable": sum(1 for r in resp_rows if r["ambient_status"] == "NO_AMBIENT_CENTER"),
        }
        if resp
        else None,
    }
