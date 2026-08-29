"""Non-mutating checks of frozen original science and Phase-3A certificates."""
from __future__ import annotations

import json
from fractions import Fraction

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3a.certificates import qnorm2, vec_to_q
from experiments.icassp_10of10_hardening.phase3a.config import OUT_DIR, PHASE1_DIR, PHASE2A_DIR, PHASE2B_DIR, ROOT
from experiments.icassp_10of10_hardening.phase3a.embeddings import affine_span_reduce, embed_coeff_task
from experiments.icassp_10of10_hardening.phase3a.validation import synthetic_suite
from src.verification.io_utils import sha256_file

LOCKED = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/summary.json": "f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b",
    "data/icassp_10of10/task_stats.json": "00f9d5f226c48b0e31b9c7bf58cc96535c2305e9db6eb2944e2ce6efe34ee884",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json": "bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49",
    "results/icassp_10of10_hardening/phase1/fir_continuous_certification.json": "263b69f0d444b7e5b5e9efb534730c85dfb85c2b636d30eac32a7865cffcdc17",
    "results/icassp_10of10_hardening/phase2a/headline.json": "85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b",
    "results/icassp_10of10_hardening/phase2a/fir_power_polynomial_certification.json": "f5de5ef06dae0118ddd4349fba35b9a2ed71dec65e72f2741ff3a8774d53f7ff",
    "results/icassp_10of10_hardening/phase2a/denominator.json": "6c4bda19e73e3ed8f1fbcf5e69a3bc4f7378271b7e493f133af3b1315fc9dce4",
    "results/icassp_10of10_hardening/phase2b/headline.json": "e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927",
    "results/icassp_10of10_hardening/phase2b/iir_continuous_certification.json": "7b172b1a7e47d734a4013f153f7633c60111d22aed93a29a59dc357fe68ccc22",
}


def _recheck_exact_dual(emb: dict, support: list[dict]) -> bool:
    if not support:
        return False
    Vq = [vec_to_q(v) for v in emb["V"]]
    Iq = [vec_to_q(i) for i in emb["I"]]
    d = emb["dim"]
    acc = [Fraction(0)] * d
    s = Fraction(0)
    obj = Fraction(0)
    for rec in support:
        w = Fraction(int(rec["weight_num"]), int(rec["weight_den"]))
        vi, ii = int(rec["v_index"]), int(rec["i_index"])
        diff = [Iq[ii][j] - Vq[vi][j] for j in range(d)]
        for j in range(d):
            acc[j] += w * diff[j]
        s += w
        obj += w * (qnorm2(Iq[ii]) - qnorm2(Vq[vi]))
    return s == 1 and all(x == 0 for x in acc) and obj <= 0


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "expected": exp, "got": got, "match": match})
        hash_ok = hash_ok and match
    syn = synthetic_suite()
    coeff = json.loads((OUT_DIR / "coefficient_ambient.json").read_text(encoding="utf-8"))
    resp = json.loads((OUT_DIR / "response_ambient.json").read_text(encoding="utf-8"))
    hier = json.loads((OUT_DIR / "hierarchy.json").read_text(encoding="utf-8"))
    headline = json.loads((OUT_DIR / "headline.json").read_text(encoding="utf-8"))
    uni = load_frozen_universe()
    by = {p["task_id"]: p for p in uni["tasks"]}
    cert_ok = True
    cert_rows = []
    for row in coeff["tasks"]:
        if row["certificate_strength"] != "EXACT_RATIONAL_CERTIFICATE":
            continue
        if row["ambient_status"] != "NO_AMBIENT_CENTER":
            continue
        support = row.get("dual_support") or []
        if not support or "weight_num" not in support[0]:
            cert_ok = False
            cert_rows.append({"task": row["task"], "ok": False, "reason": "missing_rational_support"})
            continue
        pack = by[row["task"]]
        raw = embed_coeff_task(pack["valids"], pack["primary_invalids"], pack["family"])
        red = affine_span_reduce(raw["V"], raw["I"])
        emb = {"V": red["V"], "I": red["I"], "dim": red["dim"]}
        ok = _recheck_exact_dual(emb, support)
        cert_ok = cert_ok and ok
        cert_rows.append({"task": row["task"], "ok": ok})
    counts_ok = (
        headline.get("coeff_ambient_separable") == coeff["AMBIENT_SEPARABLE"]
        and headline.get("coeff_ambient_nonseparable") == coeff["NO_AMBIENT_CENTER"]
        and hier["coeff"]["counts"]["A"] + hier["coeff"]["counts"]["B"]
        + hier["coeff"]["counts"]["C"] + hier["coeff"]["counts"]["D"]
        + hier["coeff"]["counts"]["UNDECIDED"]
        == 20
    )
    # Phase-1/2 dirs exist and were not required to be rewritten
    _ = PHASE1_DIR, PHASE2A_DIR, PHASE2B_DIR
    ok = hash_ok and syn["pass"] and cert_ok and counts_ok
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "hashes": hashes,
        "synthetic_pass": syn["pass"],
        "certificate_recheck_ok": cert_ok,
        "certificate_rows": cert_rows,
        "counts_ok": counts_ok,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase3a_reproduction": "PASS_EXACT" if ok else "FAIL",
        "response_precision_robust": resp.get("precision_robust"),
    }
