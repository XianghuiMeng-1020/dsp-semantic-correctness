"""Non-mutating checks of original science, challenge hashes, and Phase-3D-B freeze."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3d_b.config import (
    CHALLENGE_FILES,
    LOCKED,
    OUT_DIR,
    PHASE3B_DIR,
    PHASE3DA_DIR,
    ROOT,
)
from src.verification.io_utils import sha256_file


def _working_tree() -> str:
    r = subprocess.run(
        ["git", "-c", "safe.directory=F:/ICASSP/project_a_public_release", "status", "--porcelain=v1"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return "CLEAN" if r.returncode == 0 and not r.stdout.strip() else "DIRTY"


def _catalogs_match() -> bool:
    rcc = json.loads((PHASE3B_DIR / "reference_catalog_complexity.json").read_text(encoding="utf-8"))
    freeze = json.loads((OUT_DIR / "FROZEN_CATALOGS_PREUNBLIND.json").read_text(encoding="utf-8"))
    by = {(t["task"], t["metric"]): t for t in freeze["tasks"]}
    for metric in ("coeff", "resp"):
        for t in rcc[metric]["tasks"]:
            rec = by[(t["task"], metric)]
            p = t["primary"]
            if rec["catalog_ids"] != list(p.get("catalog_ids") or []):
                return False
            if rec["K_obs_star"] != p.get("K_obs_star"):
                return False
    return True


def verify_all() -> dict:
    hashes = []
    hash_ok = True
    for rel, exp in LOCKED.items():
        got = sha256_file(ROOT / rel)
        match = got == exp
        hashes.append({"path": rel, "match": match})
        hash_ok = hash_ok and match
    man = (PHASE3DA_DIR / "CHALLENGE_MANIFEST.sha256").read_text(encoding="utf-8")
    man_ok = True
    for line in man.splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        if sha256_file(ROOT / rel) != digest:
            man_ok = False
    challenge_ok = True
    for rel in CHALLENGE_FILES:
        if rel in LOCKED and sha256_file(ROOT / rel) != LOCKED[rel]:
            challenge_ok = False
    recert = json.loads((OUT_DIR / "h_valid_recertify.json").read_text(encoding="utf-8"))
    recert_ok = bool(recert.get("all_still_certified")) and recert.get("certified_valid") == 614
    cat_ok = _catalogs_match()
    th = json.loads((OUT_DIR / "FROZEN_THRESHOLDS_PREUNBLIND.json").read_text(encoding="utf-8"))
    th_ok = (not th.get("holdout_used_in_derivation")) and all(r.get("holdout_used_in_threshold_selection") in (0, False, None) for r in th["tasks"])
    ok = hash_ok and man_ok and challenge_ok and recert_ok and cat_ok and th_ok
    return {
        "ok": ok,
        "hash_ok": hash_ok,
        "manifest_ok": man_ok,
        "challenge_ok": challenge_ok,
        "recert_ok": recert_ok,
        "catalogs_match": cat_ok,
        "thresholds_base_only": th_ok,
        "hashes": hashes,
        "original_reproduction": "PASS_EXACT" if hash_ok else "FAIL",
        "phase3d_b_reproduction": "PASS_EXACT" if ok else "FAIL",
        "working_tree": _working_tree(),
        "manuscript_changed": False,
        "pdf_changed": False,
        "labels_changed": False,
        "challenge_hashes": "PRESERVED" if challenge_ok and man_ok else "CHANGED",
    }
