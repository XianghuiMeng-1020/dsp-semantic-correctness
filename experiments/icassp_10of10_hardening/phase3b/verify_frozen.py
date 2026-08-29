"""Non-mutating checks of frozen original science and Phase-3B catalogs."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3b.config import G_ZERO_ABS, OUT_DIR, ROOT
from experiments.icassp_10of10_hardening.phase3b.pairwise import coeff_matrices, gap_of_catalog
from src.verification.io_utils import sha256_file

LOCKED = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/summary.json": "f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "data/icassp_10of10/multi_reference.json": "44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json": "bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49",
    "results/icassp_10of10_hardening/phase2b/headline.json": "e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927",
    "results/icassp_10of10_hardening/phase3a/headline.json": "a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f",
    "results/icassp_10of10_hardening/phase3a/coefficient_ambient.json": "7160bf5cb68fc101bf636f5020f3746c50e7d0dc6cb7e2d66070f45e880f59a0",
    "results/icassp_10of10_hardening/phase3a/hierarchy.json": "5b1d0b28d9d4d99c98ebe2fd337d83971fbb739dce73df92fe029d8b2b3c4af9",
}


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "match": match})
        hash_ok = hash_ok and match
    rcc = json.loads((OUT_DIR / "reference_catalog_complexity.json").read_text(encoding="utf-8"))
    uni = {p["task_id"]: p for p in load_frozen_universe()["tasks"]}
    wit_ok = True
    wits = []
    for t in rcc["coeff"]["tasks"]:
        idx = t["primary"].get("catalog_indices") or []
        if t["K_obs_star"] is None or not idx:
            wit_ok = False
            wits.append({"task": t["task"], "ok": False})
            continue
        pack = uni[t["task"]]
        vv, iv = coeff_matrices(pack["valids"], pack["primary_invalids"], pack["task"])
        gap = gap_of_catalog(vv, iv, idx)
        ok = gap["G_R"] is not None and gap["G_R"] > G_ZERO_ABS and len(idx) == t["K_obs_star"]
        wit_ok = wit_ok and ok
        wits.append({"task": t["task"], "ok": ok, "G_R": gap["G_R"]})
    ok = hash_ok and wit_ok
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "hashes": hashes,
        "witness_ok": wit_ok,
        "witnesses": wits,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase3b_reproduction": "PASS_EXACT" if ok else "FAIL",
    }
