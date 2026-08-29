"""Non-mutating checks of original science and Phase-3D-A challenge hashes."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3d_a.config import OUT_DIR, ROOT
from src.verification.io_utils import sha256_file

LOCKED = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase2a/headline.json": "85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b",
    "results/icassp_10of10_hardening/phase2b/headline.json": "e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927",
    "results/icassp_10of10_hardening/phase3a/headline.json": "a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f",
    "results/icassp_10of10_hardening/phase3b/headline.json": "fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0",
    "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json": "92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061",
    "results/icassp_10of10_hardening/phase3c/leakage.json": "d02fb07b073ed6f1fd6648fb0f57d130e6b29ebee286cca02fc5488f0c2f962f",
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


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "match": match})
        hash_ok = hash_ok and match
    man = (OUT_DIR / "CHALLENGE_MANIFEST.sha256").read_text(encoding="utf-8")
    man_ok = True
    for line in man.splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        got = sha256_file(ROOT / rel)
        if got != digest:
            man_ok = False
    hv = json.loads((OUT_DIR / "H_VALID.json").read_text(encoding="utf-8"))
    hi = json.loads((OUT_DIR / "H_INVALID.json").read_text(encoding="utf-8"))
    att = json.loads((OUT_DIR / "all_attempts.json").read_text(encoding="utf-8"))
    count_ok = att["n"] == 960 and hv.get("undecided_included") == 0 and hi.get("undecided_included") == 0
    scan = json.loads((OUT_DIR / "no_transfer_scan.json").read_text(encoding="utf-8"))
    blind_ok = scan.get("verdict") == "CLEAN"
    ok = hash_ok and man_ok and count_ok and blind_ok
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "manifest_ok": man_ok,
        "count_ok": count_ok,
        "blind_ok": blind_ok,
        "hashes": hashes,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase3d_a_reproduction": "PASS_EXACT" if ok else "FAIL",
        "working_tree": _working_tree(),
    }
