"""Non-mutating checks of frozen original science and Phase-2A certificates."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR, PHASE1_DIR, ROOT
from experiments.icassp_10of10_hardening.phase2a.denominator import reconcile
from src.continuous_certification.fir_power_polynomial import certify_fir
from src.verification.io_utils import load_impl, sha256_file

# Authoritative hashes recorded in PHASE2A_PROTOCOL_LOCK.md at starting commit 54cdceb.
LOCKED_HASHES = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/summary.json": "f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b",
    "data/icassp_10of10/task_stats.json": "00f9d5f226c48b0e31b9c7bf58cc96535c2305e9db6eb2944e2ce6efe34ee884",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase1/fir_continuous_certification.json": "263b69f0d444b7e5b5e9efb534730c85dfb85c2b636d30eac32a7865cffcdc17",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json": "bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49",
}

FORBIDDEN_IMPORT_ROOTS = {
    "src.spec_checker",
    "src.verification.search_checker",
    "src.verification.independent_spec_verifier",
    "src.continuous_certification.fir_adaptive",
}

AUDIT_CASES = [
    ("fir_lp_loose_8k", "data/valid/library/fir_lp_loose_8k__firwin.npy", "CERTIFIED_VALID"),
    ("fir_lp_loose_8k", "data/icassp_10of10/boundary_invalids/fir_lp_loose_8k__PASS_DROP__e0.002.npy", "CERTIFIED_INVALID"),
]


def _hash_rows() -> list[dict]:
    rows = []
    for rel, exp in LOCKED_HASHES.items():
        got = sha256_file(ROOT / rel)
        rows.append({"path": rel, "expected": exp, "got": got, "match": got == exp})
    return rows


def _imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _original_headline_from_frozen() -> dict:
    summary = json.loads((ROOT / "data" / "icassp_10of10" / "summary.json").read_text(encoding="utf-8"))
    recert = summary["recert"]
    p1 = json.loads((PHASE1_DIR / "headline.json").read_text(encoding="utf-8"))
    ok = (
        recert["independent_valid"] == 412
        and recert["independent_invalid"] == 144
        and recert["label_flips"] == 4
        and p1["summary_coeff"]["best_observed_nonseparable"] == 20
        and p1["summary_resp"]["best_observed_nonseparable"] == 18
        and p1["fir_valid"]["total"] == 1596
        and p1["fir_valid"]["CERTIFIED_VALID"] == 78
        and p1["fir_valid"]["UNDECIDED"] == 1518
        and p1["fir_valid"]["CERTIFIED_INVALID"] == 0
    )
    return {
        "independent_valid": recert["independent_valid"],
        "independent_invalid": recert["independent_invalid"],
        "label_flips": recert["label_flips"],
        "coeff_best_observed_nonseparable": p1["summary_coeff"]["best_observed_nonseparable"],
        "resp_best_observed_nonseparable": p1["summary_resp"]["best_observed_nonseparable"],
        "pass_exact": ok,
    }


def _cert_internal_consistency(cert: dict) -> dict:
    rows = cert["rows"]
    by_role = {}
    for r in rows:
        by_role.setdefault(r["role"], []).append(r)
    problems = []
    ev = cert["existing_valid_fir_constructed"]
    constructed = by_role.get("constructed_valid", [])
    if ev["total_unique_occupants"] != len(constructed):
        problems.append("constructed count mismatch")
    if ev["CERTIFIED_VALID"] != sum(1 for r in constructed if r["phase2a_status"] == "CERTIFIED_VALID"):
        problems.append("constructed CERTIFIED_VALID mismatch")
    probe = by_role.get("probe_valid", [])
    pr = cert["existing_valid_fir_probe_confirmatory"]
    if pr["total_unique_occupants"] != len(probe):
        problems.append("probe count mismatch")
    if any(r.get("method") != "power_polynomial_bernstein" for r in rows):
        problems.append("non-Bernstein method present in frozen rows")
    if any(r["phase2a_status"] == "CERTIFIED_VALID" and r.get("reason") != "all_bands_polynomial_sign" for r in rows):
        problems.append("CERTIFIED_VALID without polynomial-sign reason")
    if cert["contradictions_valid_to_invalid"]:
        problems.append("valid→invalid contradictions present")
    return {"ok": not problems, "problems": problems, "n_rows": len(rows)}


def verify_all(recertify_audit: bool = True) -> dict:
    hashes = _hash_rows()
    hash_ok = all(r["match"] for r in hashes)
    headline = _original_headline_from_frozen()
    denom = reconcile()
    stored_denom = json.loads((OUT_DIR / "denominator.json").read_text(encoding="utf-8"))
    denom_ok = (
        denom["verdict"] == stored_denom["verdict"]
        and denom["blocker"] == stored_denom["blocker"]
        and denom["phase1_1596_value"] == stored_denom["phase1_1596_value"]
        and denom["manuscript_valid_implementations"] == stored_denom["manuscript_valid_implementations"]
    )
    cert = json.loads((OUT_DIR / "fir_power_polynomial_certification.json").read_text(encoding="utf-8"))
    cons = _cert_internal_consistency(cert)

    src = ROOT / "src" / "continuous_certification" / "fir_power_polynomial.py"
    imported = _imports_of(src)
    forbidden_hit = sorted(n for n in imported if any(n == f or n.startswith(f + ".") for f in FORBIDDEN_IMPORT_ROOTS))

    audits = []
    audit_ok = True
    if recertify_audit:
        frozen_by = {(r["task"], r["occupant"]): r["phase2a_status"] for r in cert["rows"]}
        extra = []
        mech = next(
            r
            for r in cert["rows"]
            if r["role"] == "mechanism_invalid" and r["task"] == "fir_lp_loose_8k"
        )
        extra.append((mech["task"], mech["occupant"], "CERTIFIED_INVALID"))
        probe = next(r for r in cert["rows"] if r["role"] == "probe_valid" and r["task"] == "fir_lp_loose_8k")
        extra.append((probe["task"], probe["occupant"], "CERTIFIED_VALID"))
        for tid, cid, expect in AUDIT_CASES + extra:
            live = certify_fir(tid, load_impl(cid))
            frozen = frozen_by.get((tid, cid), expect)
            match = live["status"] == frozen == expect
            audits.append(
                {
                    "task": tid,
                    "occupant": cid,
                    "expected": expect,
                    "live": live["status"],
                    "frozen": frozen,
                    "match": match,
                    "reason": live.get("reason"),
                }
            )
            audit_ok = audit_ok and match

    ok = hash_ok and headline["pass_exact"] and denom_ok and cons["ok"] and not forbidden_hit and audit_ok
    return {
        "ok": ok,
        "hashes": hashes,
        "hash_ok": hash_ok,
        "original_headline": headline,
        "denominator_ok": denom_ok,
        "denominator_verdict": denom["verdict"],
        "cert_consistency": cons,
        "forbidden_imports": forbidden_hit,
        "audits": audits,
        "audit_ok": audit_ok,
        "original_reproduction": "PASS_EXACT" if hash_ok and headline["pass_exact"] else "FAIL",
        "phase2a_reproduction": "PASS_EXACT" if ok else "FAIL",
    }
