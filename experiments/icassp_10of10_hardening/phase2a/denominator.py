"""Reconcile 412 vs 1596. Labels are read, never recomputed."""
from __future__ import annotations

import hashlib
import json
import numpy as np

from experiments.icassp_10of10_hardening.phase2a.config import FROZEN_DIR, PHASE1_DIR, ROOT
from src.verification.io_utils import load_impl
from src.verification.registry_io import get_task, is_fir


def _sha_taps(impl) -> str:
    if isinstance(impl, dict):
        arr = np.asarray(impl.get("b", impl.get("h")), dtype=np.float64).reshape(-1)
    else:
        arr = np.asarray(impl, dtype=np.float64).reshape(-1)
    return hashlib.sha256(arr.tobytes()).hexdigest()


def reconcile() -> dict:
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    probe = json.loads((FROZEN_DIR / "feasible_probe.json").read_text(encoding="utf-8"))
    boundary = json.loads((FROZEN_DIR / "boundary_invalids.json").read_text(encoding="utf-8"))
    p1 = json.loads((PHASE1_DIR / "fir_continuous_certification.json").read_text(encoding="utf-8"))
    headline = json.loads((PHASE1_DIR / "headline.json").read_text(encoding="utf-8"))

    constructed_valid = [r for r in recert["valids"] if r["independent_label"] == "VALID"]
    constructed_valid_fir = [r for r in constructed_valid if r.get("family") == "fir"]
    constructed_valid_iir = [r for r in constructed_valid if r.get("family") == "iir"]
    near = [r for r in constructed_valid if r.get("near_boundary")]
    mech_inv = [r for r in recert["invalids"] if r["independent_label"] == "INVALID"]
    mech_inv_fir = [r for r in mech_inv if r.get("family") == "fir"]
    bound_inv = [r for r in boundary if not r.get("independent_ok")]
    bound_inv_fir = [r for r in bound_inv if is_fir(get_task(r["task_id"]))]
    probes = [
        r
        for r in probe["rows"]
        if r.get("genuine_same_order") and r.get("path") and r.get("independent_ok")
    ]

    def unique_ids(rows, key):
        ids = [r[key] for r in rows]
        return len(ids), len(set(ids))

    def unique_hashes(rows, key):
        hs = []
        for r in rows:
            hs.append(_sha_taps(load_impl(r[key])))
        return len(hs), len(set(hs))

    n_cv, u_cv = unique_ids(constructed_valid, "id")
    n_cv_fir, u_cv_fir = unique_ids(constructed_valid_fir, "id")
    n_pr, u_pr = unique_ids(probes, "path")
    n_mi_fir, u_mi_fir = unique_ids(mech_inv_fir, "id")
    bound_paths = [{"id": r.get("path") or r.get("cid")} for r in bound_inv_fir]
    n_bi_fir, u_bi_fir = unique_ids(bound_paths, "id")

    _, h_cv_fir = unique_hashes(constructed_valid_fir, "id")
    _, h_pr = unique_hashes(probes, "path")
    _, h_mi = unique_hashes(mech_inv_fir, "id")
    _, h_bi = unique_hashes(bound_paths, "id")

    p1_rows = p1["rows"]
    p1_valid = [r for r in p1_rows if r["old_label"] == "VALID"]
    p1_cv = [r for r in p1_rows if r.get("role") == "constructed_valid"]
    p1_pr = [r for r in p1_rows if r.get("role") == "probe_valid"]
    p1_cert = [r for r in p1_valid if r["continuous_status"] == "CERTIFIED_VALID"]
    p1_und = [r for r in p1_valid if r["continuous_status"] == "UNDECIDED"]

    # occupant id uniqueness in Phase-1 rows
    p1_valid_ids = [r["occupant"] for r in p1_valid]
    verdict = "REPORT_LABEL_ISSUE_ONLY"
    # 1596 is documented constructed+probe FIR occupants, not manuscript 412
    if headline["fir_valid"]["total"] != len(p1_valid):
        verdict = "MATERIAL_INCONSISTENCY"
    if n_cv != 412:
        verdict = "MATERIAL_INCONSISTENCY"

    rows = [
        {
            "quantity": "412 manuscript independent valids",
            "value": n_cv,
            "unit": "constructed occupant (task × stored file); FIR+IIR",
            "unique_implementation_count": u_cv,
            "unique_coefficient_hash_count": None,
            "source": "recertify.json independent_label=VALID",
        },
        {
            "quantity": "409/412 near-boundary",
            "value": f"{len(near)}/{n_cv}",
            "unit": "constructed independently VALID occupants with near_boundary=1",
            "unique_implementation_count": len(near),
            "unique_coefficient_hash_count": None,
            "source": "recertify.json valids[*].near_boundary",
        },
        {
            "quantity": "constructed FIR valids (subset of 412)",
            "value": n_cv_fir,
            "unit": "constructed FIR occupant (task × stored file)",
            "unique_implementation_count": u_cv_fir,
            "unique_coefficient_hash_count": h_cv_fir,
            "source": "recertify.json family=fir and independent_label=VALID",
        },
        {
            "quantity": "constructed IIR valids (subset of 412)",
            "value": len(constructed_valid_iir),
            "unit": "constructed IIR occupant (task × stored file)",
            "unique_implementation_count": len({r["id"] for r in constructed_valid_iir}),
            "unique_coefficient_hash_count": None,
            "source": "recertify.json family=iir and independent_label=VALID",
        },
        {
            "quantity": "Type-I probe valids (confirmatory U_t, not in 412)",
            "value": n_pr,
            "unit": "probe occupant (task × stored file); all FIR",
            "unique_implementation_count": u_pr,
            "unique_coefficient_hash_count": h_pr,
            "source": "feasible_probe.json genuine_same_order and independent_ok",
        },
        {
            "quantity": "1596 Phase-1 EXISTING-VALID FIR",
            "value": len(p1_valid),
            "unit": "Phase-1 FIR certification record = constructed FIR valid + probe valid",
            "unique_implementation_count": len(set(p1_valid_ids)),
            "unique_coefficient_hash_count": None,
            "source": "phase1/fir_continuous_certification.json rows with old_label=VALID",
        },
        {
            "quantity": "78 Phase-1 CERTIFIED_VALID",
            "value": len(p1_cert),
            "unit": "Phase-1 FIR certification record (constructed+probe)",
            "unique_implementation_count": len({r["occupant"] for r in p1_cert}),
            "unique_coefficient_hash_count": None,
            "source": "phase1 fir rows continuous_status=CERTIFIED_VALID and old_label=VALID",
        },
        {
            "quantity": "1518 Phase-1 UNDECIDED among valids",
            "value": len(p1_und),
            "unit": "Phase-1 FIR certification record (constructed+probe)",
            "unique_implementation_count": len({r["occupant"] for r in p1_und}),
            "unique_coefficient_hash_count": None,
            "source": "phase1 fir rows continuous_status=UNDECIDED and old_label=VALID",
        },
        {
            "quantity": "112 mechanism-invalid FIR",
            "value": n_mi_fir,
            "unit": "constructed mechanism-invalid FIR occupant (task × stored file)",
            "unique_implementation_count": u_mi_fir,
            "unique_coefficient_hash_count": h_mi,
            "source": "recertify.json family=fir and independent_label=INVALID",
        },
        {
            "quantity": "128 boundary-invalid FIR",
            "value": n_bi_fir,
            "unit": "boundary-invalid FIR occupant (task × stored file)",
            "unique_implementation_count": u_bi_fir,
            "unique_coefficient_hash_count": h_bi,
            "source": "boundary_invalids.json independent_ok=false and FIR task",
        },
    ]

    identity = {
        "manuscript_412": "constructed independently VALID occupants (FIR+IIR). Identity: recertify.valids with independent_label=VALID.",
        "manuscript_412_fir": f"{n_cv_fir} of 412 are FIR; {len(constructed_valid_iir)} are IIR.",
        "near_409_412": "409 of those 412 constructed valids carry the old verifier near_boundary flag. Not a count of Phase-1 FIR records.",
        "phase1_1596": (
            f"{len(p1_cv)} constructed FIR valids + {len(p1_pr)} Type-I probe valids = {len(p1_valid)}. "
            "Each record is one stored file evaluated on its registered task. "
            "This is the confirmatory FIR-valid occupant pool used for Phase-1 certification, "
            "not the manuscript headline 412."
        ),
        "preexisting_documentation": (
            "PHASE1_PROTOCOL_LOCK.md and PHASE1_FIR_CONTINUOUS_CERTIFICATION.md already split "
            "constructed vs probe. The Phase-1 console label EXISTING-VALID FIR=1596 omitted that split."
        ),
    }

    # blocker only if 1596 is an undocumented different universe
    blocker = False
    reason = None
    if n_cv != 412:
        blocker = True
        reason = "recertify independent VALID count is not 412"
    elif headline["fir_valid"]["total"] != 336 + 1260 and headline["fir_valid"]["total"] != len(p1_valid):
        blocker = True
        reason = "Phase-1 headline 1596 does not match constructed+probe FIR rows"

    return {
        "verdict": "PHASE2A_DENOMINATOR_BLOCKER" if blocker else verdict,
        "blocker": blocker,
        "blocker_reason": reason,
        "identity": identity,
        "table": rows,
        "manuscript_valid_implementations": n_cv,
        "manuscript_valid_fir_unique": u_cv_fir,
        "phase1_1596_unit": "FIR occupant record (constructed valid + Type-I probe valid); task × stored file",
        "phase1_1596_value": len(p1_valid),
        "constructed_fir_valid_unique": u_cv_fir,
        "probe_fir_valid_unique": u_pr,
        "near_boundary": f"{len(near)}/{n_cv}",
        "p1_constructed_valid_fir": len(p1_cv),
        "p1_probe_valid_fir": len(p1_pr),
        "p1_certified_valid": len(p1_cert),
        "p1_undecided_valid": len(p1_und),
        "mech_invalid_fir_unique": u_mi_fir,
        "boundary_invalid_fir_unique": u_bi_fir,
        "unique_coeff_hashes": {
            "constructed_fir_valid": h_cv_fir,
            "probe_valid": h_pr,
            "mechanism_invalid_fir": h_mi,
            "boundary_invalid_fir": h_bi,
        },
    }
