"""Phase-3D-A reproduction. Catalog-blind generation and certification only."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase3d_a.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_a.console_report import print_console  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_a.manifest import write_challenge_manifest  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_a.pipeline import (  # noqa: E402
    certify_and_admit,
    generate_attempts,
    generate_invalids,
)
from experiments.icassp_10of10_hardening.phase3d_a.summarize import (  # noqa: E402
    adequacy,
    attrition,
    diversity,
    invalid_attrition,
    no_transfer_scan,
)
from experiments.icassp_10of10_hardening.phase3d_a.verify_frozen import verify_all  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_a.write_reports import write_all_reports  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402
import json  # noqa: E402


def run_science() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frozen = (OUT_DIR / "CHALLENGE_MANIFEST.sha256").exists() and (OUT_DIR / "H_VALID.json").exists()
    if frozen:
        print("[phase3d_a] challenge already frozen; rewrite summaries from frozen artifacts", flush=True)
        hv = json.loads((OUT_DIR / "H_VALID.json").read_text(encoding="utf-8"))
        hi = json.loads((OUT_DIR / "H_INVALID.json").read_text(encoding="utf-8"))
    else:
        print("[phase3d_a] generate 960 attempts", flush=True)
        generate_attempts()
        print("[phase3d_a] continuous certify + dedup", flush=True)
        hv = certify_and_admit()
        print("[phase3d_a] invalid mutations", flush=True)
        hi = generate_invalids()
    attempts = json.loads((OUT_DIR / "all_attempts.json").read_text(encoding="utf-8"))
    attr = {"valid": attrition(attempts), "invalid": invalid_attrition(hi)}
    adeq = adequacy(hv, hi)
    div = diversity(hv)
    dump_json(OUT_DIR / "attrition.json", attr)
    dump_json(OUT_DIR / "adequacy.json", adeq)
    dump_json(OUT_DIR / "diversity.json", div)
    write_challenge_manifest()
    scan = no_transfer_scan()
    dump_json(OUT_DIR / "no_transfer_scan.json", scan)
    write_all_reports()
    dump_json(
        OUT_DIR / "headline.json",
        {
            "n_valid": adeq["n_valid"],
            "n_invalid": adeq["n_invalid"],
            "challenge": adeq["PROSPECTIVE_CHALLENGE"],
            "blinding": scan["verdict"],
        },
    )


def main() -> int:
    run_science()
    result = verify_all()
    print(
        f"[phase3d_a] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase3d_a={result['phase3d_a_reproduction']} tree={result['working_tree']}",
        flush=True,
    )
    print_console(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
