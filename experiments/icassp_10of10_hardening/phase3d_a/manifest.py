"""SHA-256 challenge manifest. No timestamps."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3d_a.config import OUT_DIR, ROOT
from src.verification.io_utils import sha256_file


def write_challenge_manifest() -> dict:
    hv = json.loads((OUT_DIR / "H_VALID.json").read_text(encoding="utf-8"))
    hi = json.loads((OUT_DIR / "H_INVALID.json").read_text(encoding="utf-8"))
    lines = []
    rows = []
    for mem in hv["members"] + hi["members"]:
        rel = mem["id"]
        digest = sha256_file(ROOT / rel)
        lines.append(f"{digest}  {rel}")
        rows.append({"rel": rel, "sha256": digest, "task_id": mem["task_id"]})
    for name in ("H_VALID.json", "H_INVALID.json", "all_attempts.json", "seed_manifest.json"):
        p = OUT_DIR / name
        digest = sha256_file(p)
        rel = f"results/icassp_10of10_hardening/phase3d_a/{name}"
        lines.append(f"{digest}  {rel}")
        rows.append({"rel": rel, "sha256": digest})
    text = "\n".join(sorted(lines)) + "\n"
    (OUT_DIR / "CHALLENGE_MANIFEST.sha256").write_text(text, encoding="utf-8")
    return {"n": len(rows), "rows": rows}
