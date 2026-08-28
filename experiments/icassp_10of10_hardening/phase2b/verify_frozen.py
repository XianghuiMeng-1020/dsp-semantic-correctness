"""Non-mutating checks of frozen original science and Phase-2B certificates."""
from __future__ import annotations

import ast
import json

from experiments.icassp_10of10_hardening.phase2b.config import OUT_DIR, PHASE1_DIR, PHASE2A_DIR, ROOT
from experiments.icassp_10of10_hardening.phase2b.population import audit
from src.continuous_certification.iir_schur import certify_stability
from src.continuous_certification.mask_sign import certify_fir_sturm, certify_iir_magnitude, load_task
from src.verification.io_utils import load_impl, sha256_file

LOCKED = {
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
    "results/icassp_10of10_hardening/phase2a/headline.json": "85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b",
    "results/icassp_10of10_hardening/phase2a/fir_power_polynomial_certification.json": "f5de5ef06dae0118ddd4349fba35b9a2ed71dec65e72f2741ff3a8774d53f7ff",
    "results/icassp_10of10_hardening/phase2a/denominator.json": "6c4bda19e73e3ed8f1fbcf5e69a3bc4f7378271b7e493f133af3b1315fc9dce4",
}

FORBIDDEN = {
    "src.spec_checker",
    "src.verification.search_checker",
    "src.verification.independent_spec_verifier",
    "src.continuous_certification.fir_adaptive",
    "src.continuous_certification.fir_power_polynomial",
}


def _imports(path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "match": match})
        hash_ok = hash_ok and match
    pop = audit()
    stored = json.loads((OUT_DIR / "population.json").read_text(encoding="utf-8"))
    pop_ok = pop["verdict"] == stored["verdict"] and not pop["blocker"]
    fir = json.loads((OUT_DIR / "fir_remaining_resolution.json").read_text(encoding="utf-8"))
    iir = json.loads((OUT_DIR / "iir_continuous_certification.json").read_text(encoding="utf-8"))
    forbidden = []
    for rel in (
        "src/continuous_certification/poly_sturm.py",
        "src/continuous_certification/mask_sign.py",
        "src/continuous_certification/iir_schur.py",
    ):
        hit = [n for n in _imports(ROOT / rel) if n in FORBIDDEN or any(n.startswith(f + ".") for f in FORBIDDEN)]
        forbidden.extend(hit)
    # live recertify of cheap occupants
    fir_live = certify_fir_sturm("fir_lp_loose_8k", load_impl("data/valid/library/fir_lp_loose_8k__firwin.npy"))
    impl = load_impl("data/valid/library/iir_lp_loose_8k__butter.npz")
    task = load_task("iir_lp_loose_8k")
    stab = certify_stability(impl["a"], float(task["constraints"]["pole_radius_max"]))
    mag = certify_iir_magnitude("iir_lp_loose_8k", impl["b"], impl["a"])
    audit_ok = (
        fir_live["status"] == "CERTIFIED_VALID"
        and stab["status"] == "CERTIFIED_STABLE"
        and mag["status"] == "CERTIFIED_VALID"
        and fir.get("CERTIFIED_INVALID", 0) == 0
        and not iir.get("blocker")
    )
    ok = hash_ok and pop_ok and not forbidden and audit_ok
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "hashes": hashes,
        "pop_ok": pop_ok,
        "forbidden_imports": forbidden,
        "audit_ok": audit_ok,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase2b_reproduction": "PASS_EXACT" if ok else "FAIL",
    }
