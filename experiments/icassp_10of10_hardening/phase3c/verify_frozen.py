"""Non-mutating checks of frozen original science, Phase-3B catalogs, and Phase-3C freeze."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3c.config import OUT_DIR, PHASE3B_DIR, ROOT
from src.verification.io_utils import sha256_file

LOCKED = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/summary.json": "f27fa024aaf355b803e27292aa6e3f2ddcb68ea183d7defb50bec8a124880a1b",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "data/icassp_10of10/feasible_probe.json": "bad0223edec5b62ef72e05dd17c2a8eb135f1f0831d10b0dfdf4da314e0a6b10",
    "data/icassp_10of10/multi_reference.json": "44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json": "bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49",
    "results/icassp_10of10_hardening/phase2a/headline.json": "85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b",
    "results/icassp_10of10_hardening/phase2b/headline.json": "e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927",
    "results/icassp_10of10_hardening/phase3a/headline.json": "a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f",
    "results/icassp_10of10_hardening/phase3b/headline.json": "fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0",
    "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json": "92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061",
}


def _working_tree() -> str:
    r = subprocess.run(
        ["git", "-c", "safe.directory=F:/ICASSP/project_a_public_release", "status", "--porcelain=v1"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return "CLEAN" if r.returncode == 0 and not r.stdout.strip() else "DIRTY"


def _catalogs_match_phase3b(freeze: dict) -> bool:
    rcc = json.loads((PHASE3B_DIR / "reference_catalog_complexity.json").read_text(encoding="utf-8"))
    by = {(t["task"], t["metric"]): t for t in freeze["tasks"]}
    for metric in ("coeff", "resp"):
        for t in rcc[metric]["tasks"]:
            rec = by[(t["task"], metric)]
            p = t["primary"]
            if rec["catalog_ids"] != list(p.get("catalog_ids") or []):
                return False
            if rec["K_obs_star"] != p.get("K_obs_star"):
                return False
            if rec["D_V"] != p.get("D_V") or rec["D_I"] != p.get("D_I"):
                return False
    return True


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "match": match, "got": got})
        hash_ok = hash_ok and match
    freeze = json.loads((OUT_DIR / "frozen_base_catalogs.json").read_text(encoding="utf-8"))
    leak = json.loads((OUT_DIR / "leakage.json").read_text(encoding="utf-8"))
    inv = json.loads((OUT_DIR / "inventory.json").read_text(encoding="utf-8"))
    freeze_ok = (
        freeze.get("derived_only_from_phase3b")
        and freeze.get("source_sha256") == LOCKED["results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json"]
        and _catalogs_match_phase3b(freeze)
    )
    leak_ok = leak.get("verdict") == "MATERIAL_LEAKAGE" and bool(leak.get("do_not_score_as_holdout"))
    inv_ok = inv.get("blocker") == "PHASE3C_HOLDOUT_LEAKAGE_BLOCKER" and not inv.get("eligible_primary")
    transfer = json.loads((OUT_DIR / "transfer.json").read_text(encoding="utf-8"))
    no_false_holdout = not bool(transfer.get("run"))
    ok = hash_ok and freeze_ok and leak_ok and inv_ok and no_false_holdout
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "hashes": hashes,
        "freeze_ok": freeze_ok,
        "leak_ok": leak_ok,
        "inv_ok": inv_ok,
        "no_false_holdout": no_false_holdout,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase3c_reproduction": "PASS_EXACT" if ok else "FAIL",
        "working_tree": _working_tree(),
    }
