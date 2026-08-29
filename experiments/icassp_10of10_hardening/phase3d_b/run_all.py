"""Phase-3D-B reproduction. Consumes the frozen Phase-3D-A challenge; does not regenerate it."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase3d_b.console_report import print_console  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.freeze import write_frozen_package  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.hierarchy import score_hierarchy  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.invalid import score_invalid  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.maintenance import run_all_maintenance  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.margin import diagnose  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.strata import generator_and_structure  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.transfer import run_primary  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.verify_frozen import verify_all  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.headline import write_headline  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.write_primary import write_primary_report  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.write_reports import write_remaining_reports  # noqa: E402
from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR  # noqa: E402


def run_science() -> None:
    print("[phase3d_b] freeze catalogs/thresholds from Phase-3B only", flush=True)
    write_frozen_package()
    print("[phase3d_b] margin-zero diagnosis (no catalog distances)", flush=True)
    diagnose()
    if (OUT_DIR / "transfer_coeff.json").exists() and (OUT_DIR / "transfer_resp.json").exists():
        print("[phase3d_b] primary transfer artifacts present; rewrite reports only", flush=True)
    else:
        print("[phase3d_b] primary H_VALID transfer", flush=True)
        run_primary()
    write_primary_report()
    generator_and_structure()
    if (OUT_DIR / "hierarchy_transfer.json").exists():
        print("[phase3d_b] hierarchy artifacts present", flush=True)
    else:
        print("[phase3d_b] hierarchy transfer", flush=True)
        score_hierarchy()
    if (OUT_DIR / "invalid_secondary.json").exists():
        print("[phase3d_b] H_INVALID artifacts present", flush=True)
    else:
        print("[phase3d_b] secondary H_INVALID", flush=True)
        score_invalid()
    if (OUT_DIR / "maintenance.json").exists():
        print("[phase3d_b] maintenance artifacts present", flush=True)
    else:
        print("[phase3d_b] catalog maintenance", flush=True)
        run_all_maintenance()
    write_headline()
    write_remaining_reports()


def main() -> int:
    run_science()
    result = verify_all()
    print(
        f"[phase3d_b] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase3d_b={result['phase3d_b_reproduction']} tree={result['working_tree']}",
        flush=True,
    )
    print_console(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
