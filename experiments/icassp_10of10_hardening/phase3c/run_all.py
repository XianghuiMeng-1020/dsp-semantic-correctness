"""Phase-3C reproduction. Does not write Phase-0/1/2/3A/3B artifacts or score a leaked holdout."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase3c.analysis import (  # noqa: E402
    blocked_maintenance,
    blocked_transfer,
    dsp_mechanism,
    secondary_holdouts,
)
from experiments.icassp_10of10_hardening.phase3c.optional_invalid import (  # noqa: E402
    score_optional_invalids,
)
from experiments.icassp_10of10_hardening.phase3c.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.console_report import print_console  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.freeze import freeze_base_catalogs  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.inventory import build_inventory  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.leakage import audit_leakage  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.novelty import decide  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.verify_frozen import verify_all  # noqa: E402
from experiments.icassp_10of10_hardening.phase3c.write_reports import write_all_reports  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402


def _headline(inv: dict, leak: dict, nov: dict) -> dict:
    cat = inv["catalog_probe_stats"]
    return {
        "blocker": inv["blocker"],
        "leakage_verdict": leak["verdict"],
        "external_transfer": nov["EXTERNAL_TRANSFER"],
        "best_framing": nov["best_framing"],
        "internal_novelty": f"{nov['internal_novelty']:.1f}",
        "novelty_gate": nov["NOVELTY_10OF10_GATE"],
        "strongest_novelty": nov["strongest_novelty"],
        "strongest_attack": nov["strongest_attack"],
        "manuscript_safe_claim": nov["manuscript_safe_claim"],
        "scientific_blocker": nov["scientific_blocker"],
        "strongest_positive": (
            f"Inventory+leakage established that {cat['probe_catalog_refs']}/"
            f"{cat['total_catalog_refs']} Phase-3B coefficient catalog members are Type-I probe paths."
        ),
        "strongest_negative": (
            "The intended 1260 Type-I probes leaked into Phase-3B catalog selection; "
            "external-validity transfer was not scored."
        ),
        "can_claim": (
            "Exact realization-reference scoring on the frozen confirmatory universe requires "
            "a measured observed-valid catalog (Phase-3B). Type-I probes are confirmatory "
            "occupants of that universe, not a catalog-excluded holdout."
        ),
        "cannot_claim": (
            "The paper cannot claim out-of-catalog transfer, catalog-maintenance growth after "
            "admitting new realizations, ambient-center impossibility, or novelty of generic "
            "prototype selection / test-set evaluation."
        ),
        "verdict": "NOVELTY_BLOCKER_REQUIRES_PI_REVIEW",
        "probe_n": inv["probe_n"],
        "constructed_n": inv["constructed_n"],
        "probe_catalog_refs": cat["probe_catalog_refs"],
        "total_catalog_refs": cat["total_catalog_refs"],
        "final_commit": None,
        "phase3c_tag": None,
    }


def run_science() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("[phase3c] inventory", flush=True)
    inv = build_inventory()
    dump_json(OUT_DIR / "inventory.json", inv)
    print("[phase3c] leakage", flush=True)
    leak = audit_leakage(inv)
    dump_json(OUT_DIR / "leakage.json", leak)
    print("[phase3c] freeze Phase-3B catalogs (no holdout scoring)", flush=True)
    freeze = freeze_base_catalogs()
    dump_json(OUT_DIR / "frozen_base_catalogs.json", freeze)
    print(f"[phase3c] {inv['blocker']}: not scoring H_TYPEI", flush=True)
    transfer = blocked_transfer(leak)
    maint = blocked_maintenance()
    secondary = secondary_holdouts(inv)
    print("[phase3c] optional external-invalid label-flips (not a valid holdout)", flush=True)
    invalid = score_optional_invalids(inv, freeze)
    mech = dsp_mechanism()
    nov = decide(inv, leak)
    dump_json(OUT_DIR / "transfer.json", transfer)
    dump_json(OUT_DIR / "maintenance.json", maint)
    dump_json(OUT_DIR / "secondary.json", secondary)
    dump_json(OUT_DIR / "external_invalid.json", invalid)
    dump_json(OUT_DIR / "dsp_mechanism.json", mech)
    dump_json(OUT_DIR / "novelty.json", nov)
    dump_json(OUT_DIR / "headline.json", _headline(inv, leak, nov))


def verify_existing() -> int:
    print("[phase3c] verify frozen original science + Phase-3B + Phase-3C freeze", flush=True)
    result = verify_all()
    write_all_reports()
    print(
        f"[phase3c] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase3c={result['phase3c_reproduction']} tree={result['working_tree']}",
        flush=True,
    )
    print_console(result)
    return 0 if result["ok"] else 1


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_science()
    return verify_existing()


if __name__ == "__main__":
    raise SystemExit(main())
