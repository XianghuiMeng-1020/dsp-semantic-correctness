"""Phase-2A reproduction. Does not write data/icassp_10of10 or Phase-1 JSON."""
from __future__ import annotations

import json
import os
import platform
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.denominator import reconcile  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.extremum import audit_occupant  # noqa: E402
from experiments.icassp_10of10_hardening.phase2a.occupants import (  # noqa: E402
    load_manuscript_fir_occupants,
    load_phase1_status,
)
from src.continuous_certification.fir_power_polynomial import certify_fir  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402

PROBE_FULL_CERT_MAX_TAPS = 80
CHECKPOINT = OUT_DIR / "_checkpoint.jsonl"
LOCK = OUT_DIR / "_running.lock"
PROGRESS = OUT_DIR / "progress.json"


def _n_taps(impl) -> int:
    if isinstance(impl, dict):
        return int(np.asarray(impl.get("b", impl.get("h"))).size)
    return int(np.asarray(impl).size)


def _cohort_summary(rows: list[dict]) -> dict:
    c = Counter(r["phase2a_status"] for r in rows)
    return {
        "total_unique_occupants": len(rows),
        "unique_cids": len({r["occupant"] for r in rows}),
        "CERTIFIED_VALID": c.get("CERTIFIED_VALID", 0),
        "CERTIFIED_INVALID": c.get("CERTIFIED_INVALID", 0),
        "UNDECIDED": c.get("UNDECIDED", 0),
        "coverage": (c.get("CERTIFIED_VALID", 0) / len(rows)) if rows else None,
    }


def _ensure_impl(occ: dict) -> dict:
    if "impl" not in occ:
        from src.verification.io_utils import load_impl

        occ = dict(occ)
        occ["impl"] = load_impl(occ["cid"])
    return occ


def _run_one(occ: dict, phase1: dict, full_cert: bool) -> dict:
    occ = _ensure_impl(occ)
    cid, tid = occ["cid"], occ["task_id"]
    rec = certify_fir(tid, occ["impl"])
    return {
        "occupant": cid,
        "task": tid,
        "role": occ["role"],
        "old_label": occ["old_label"],
        "n_taps": rec.get("n_taps"),
        "phase1_status": phase1.get(cid),
        "phase2a_status": rec["status"],
        "reason": rec.get("reason"),
        "witness_or_critical": rec.get("witness") or rec.get("band"),
        "degree": rec.get("degree"),
        "method": rec.get("method"),
    }


def _run_one_maybe_capped(occ: dict, phase1: dict, max_taps: int | None) -> dict:
    occ = _ensure_impl(occ)
    n = _n_taps(occ["impl"])
    if max_taps is not None and n > max_taps:
        # still allow a witness-only path by calling certify_fir: it witnesses first.
        # For long probes, Bernstein after a clean witness is the cost. Use a
        # dedicated witness-only if we import... keep it simple: run full for
        # manuscript; cap probes by skipping Bernstein via a light wrapper.
        from src.continuous_certification.fir_power_polynomial import (
            _as_fir_taps,
            _eff_bounds,
            _load_task,
            _witness_invalid,
        )

        task = _load_task(occ["task_id"])
        h = _as_fir_taps(occ["impl"])
        fs = float(task["sampling_rate"])
        floor = float(task["residual_floor"])
        wit = None
        for band in list(task["pass_band"]) + list(task["stop_band"]):
            L, U = _eff_bounds(float(band["lo"]), float(band["hi"]), floor)
            from fractions import Fraction as _F

            w = _witness_invalid(h, float(band["f0"]), float(band["f1"]), fs, L if L > 0 else _F(0), U)
            if w is not None:
                wit = w
                break
        status = "CERTIFIED_INVALID" if wit else "UNDECIDED"
        reason = "witnessed_violation" if wit else "polynomial_arithmetic_resource_limit"
        return {
            "occupant": occ["cid"],
            "task": occ["task_id"],
            "role": occ["role"],
            "old_label": occ["old_label"],
            "n_taps": n,
            "phase1_status": phase1.get(occ["cid"]),
            "phase2a_status": status,
            "reason": reason,
            "witness_or_critical": wit,
            "degree": n - 1,
            "method": "witness_only_resource_cap",
        }
    return _run_one(occ, phase1, True)


def _worker(item: tuple) -> dict:
    cid, tid, role, old_label, cap, p1 = item
    occ = {"cid": cid, "task_id": tid, "role": role, "old_label": old_label}
    return _run_one_maybe_capped(occ, {cid: p1}, cap)


def _append_checkpoint(rec: dict) -> None:
    """Append one record and fsync so a power loss cannot lose completed occupants."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CHECKPOINT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=True) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def _load_checkpoint() -> dict:
    done = {}
    if not CHECKPOINT.exists():
        return done
    raw = CHECKPOINT.read_text(encoding="utf-8")
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue  # truncated last line after a crash
        if "occupant" in rec:
            done[rec["occupant"]] = rec
    return done


def _write_progress(done: dict) -> None:
    from collections import Counter

    roles = Counter(r.get("role") for r in done.values())
    status = Counter(r.get("phase2a_status") for r in done.values())
    payload = {
        "n_checkpoint": len(done),
        "roles": dict(roles),
        "status": dict(status),
        "complete": (OUT_DIR / "headline.json").exists(),
    }
    tmp = PROGRESS.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(tmp, PROGRESS)


def run_certification() -> dict:
    print("[phase2a] load occupants", flush=True)
    packs = load_manuscript_fir_occupants()
    phase1 = load_phase1_status()
    all_rows = []
    done = _load_checkpoint()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def go(name, items, cap=None):
        n_done = sum(1 for o in items if o["cid"] in done)
        pending = [o for o in items if o["cid"] not in done]
        print(f"[phase2a] certify {name} n={len(items)} resumed={n_done} pending={len(pending)}", flush=True)
        workers = max(1, min(6, (os.cpu_count() or 2)))
        if pending:
            jobs = [
                (o["cid"], o["task_id"], o["role"], o["old_label"], cap, phase1.get(o["cid"]))
                for o in pending
            ]
            finished = 0
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futs = [ex.submit(_worker, job) for job in jobs]
                for fut in as_completed(futs):
                    rec = fut.result()
                    _append_checkpoint(rec)
                    done[rec["occupant"]] = rec
                    finished += 1
                    if finished % 5 == 0:
                        _write_progress(done)
                    print(
                        f"    {name} {n_done+finished}/{len(items)} {rec['occupant'][-70:]} "
                        f"{rec['old_label']} P1={rec['phase1_status']} P2A={rec['phase2a_status']} ({rec['reason']})",
                        flush=True,
                    )
        rows = [done[o["cid"]] for o in items]
        all_rows.extend(rows)
        _write_progress(done)
        return rows

    constructed = go("constructed_valid_fir", packs["constructed_valid"])
    mech = go("mechanism_invalid_fir", packs["mechanism_invalid"])
    bound = go("boundary_invalid_fir", packs["boundary_invalid"])
    probes = go("probe_valid_confirmatory", packs["probe_valid_confirmatory"], PROBE_FULL_CERT_MAX_TAPS)

    contradictions = [
        r
        for r in constructed + probes
        if r["old_label"] == "VALID" and r["phase2a_status"] == "CERTIFIED_INVALID"
    ]
    xtab = {}
    for r in constructed:
        a, b = r["phase1_status"] or "ABSENT", r["phase2a_status"]
        xtab.setdefault(a, {"CERTIFIED_VALID": 0, "CERTIFIED_INVALID": 0, "UNDECIDED": 0})
        xtab[a][b] += 1

    # per-task coverage on constructed valids only
    tasks = {}
    for r in constructed:
        tasks.setdefault(r["task"], []).append(r)
    task_table = []
    for tid, rs in sorted(tasks.items()):
        n = len(rs)
        cv = sum(1 for x in rs if x["phase2a_status"] == "CERTIFIED_VALID")
        ci = sum(1 for x in rs if x["phase2a_status"] == "CERTIFIED_INVALID")
        ud = sum(1 for x in rs if x["phase2a_status"] == "UNDECIDED")
        task_table.append(
            {
                "task": tid,
                "frozen_valid_count": n,
                "certified_valid": cv,
                "contradicted": ci,
                "undecided": ud,
                "coverage": cv / n if n else None,
            }
        )

    out = {
        "method": "squared-magnitude Chebyshev polynomial; Bernstein sign on x=cos ω",
        "arithmetic": "exact IEEE-754 binary64 rationals for taps; JSON spec as binary64; Bernstein over Fraction",
        "certificate_type": "RIGOROUS_POLYNOMIAL_SIGN",
        "limitation": (
            "Frequency endpoints use an outward cosine enclosure. "
            "Probe occupants with n_taps>80 use witness-only (resource). "
            "Manuscript unique FIR valids are the 336 constructed FIR files."
        ),
        "existing_valid_fir_constructed": _cohort_summary(constructed),
        "existing_valid_fir_probe_confirmatory": _cohort_summary(probes),
        "mechanism_invalid_fir": _cohort_summary(mech),
        "boundary_invalid_fir": _cohort_summary(bound),
        "contradictions_valid_to_invalid": contradictions,
        "blocker": len(contradictions) > 0,
        "phase1_vs_phase2a_constructed": xtab,
        "task_coverage_constructed": task_table,
        "rows": all_rows,
    }
    dump_json(OUT_DIR / "fir_power_polynomial_certification.json", out)
    return out


def run_crosscheck(cert: dict) -> dict:
    print("[phase2a] extremum cross-check", flush=True)
    packs = load_manuscript_fir_occupants()
    by_cid = {o["cid"]: o for group in packs.values() for o in group}
    picks = []
    # prescribed kinds from constructed rows
    want = [
        ("fir_lp_loose_8k", "loose_lp"),
        ("fir_lp_tight_8k", "tight_lp"),
        ("fir_hp_loose_8k", "hp"),
        ("fir_bp_loose_8k", "bp"),
        ("fir_bs_loose_8k", "bs"),
    ]
    constructed = [r for r in cert["rows"] if r["role"] == "constructed_valid"]
    # shortest / longest
    constructed_sorted = sorted(constructed, key=lambda r: r.get("n_taps") or 0)
    selected = []
    if constructed_sorted:
        selected.append(("shortest", constructed_sorted[0]))
        selected.append(("longest", constructed_sorted[-1]))
    for tid, tag in want:
        hit = next((r for r in constructed if r["task"] == tid), None)
        if hit:
            selected.append((tag, hit))
    # Phase-1 UNDECIDED that Phase-2A resolved, and some remaining
    p1u = [r for r in constructed if r["phase1_status"] == "UNDECIDED"][:4]
    for r in p1u:
        selected.append(("phase1_undecided", r))
    bounds = [r for r in cert["rows"] if r["role"] == "boundary_invalid"][:3]
    for r in bounds:
        selected.append(("boundary_invalid", r))

    audits = []
    seen = set()
    for tag, r in selected:
        if r["occupant"] in seen:
            continue
        seen.add(r["occupant"])
        occ = by_cid.get(r["occupant"])
        if not occ:
            continue
        from src.verification.io_utils import load_impl

        rec = audit_occupant(r["task"], load_impl(r["occupant"]))
        rec["tag"] = tag
        rec["occupant"] = r["occupant"]
        rec["phase2a_status"] = r["phase2a_status"]
        audits.append(rec)
        print(f"    {tag} {r['occupant'][-50:]} viol={rec['n_violating_grid_or_stat']}", flush=True)
    out = {"audits": audits, "n": len(audits)}
    dump_json(OUT_DIR / "extremum_crosscheck.json", out)
    return out


def main() -> int:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    denom_path = OUT_DIR / "denominator.json"
    if denom_path.exists():
        denom = json.loads(denom_path.read_text(encoding="utf-8"))
        print("[phase2a] reuse existing denominator.json", flush=True)
    else:
        denom = reconcile()
        dump_json(denom_path, denom)
    print(f"[phase2a] denominator {denom['verdict']} blocker={denom['blocker']}", flush=True)
    if denom["blocker"]:
        print("PHASE2A_DENOMINATOR_BLOCKER", flush=True)
        return 2
    cert = run_certification()
    if cert["blocker"]:
        print("PHASE2A_VALIDITY_CONTRADICTION_BLOCKER", flush=True)
        dump_json(OUT_DIR / "headline.json", {"blocker": True, "contradictions": cert["contradictions_valid_to_invalid"]})
        from experiments.icassp_10of10_hardening.phase2a.write_reports import write_all_reports

        write_all_reports()
        return 3
    xcheck = run_crosscheck(cert)
    env = {
        "python": sys.version.split()[0],
        "platform": platform.system(),
        "numpy": np.__version__,
        "out_dir": "results/icassp_10of10_hardening/phase2a",
        "note": "elapsed_s printed only",
    }
    dump_json(OUT_DIR / "environment.json", env)
    dump_json(
        OUT_DIR / "headline.json",
        {
            "denominator": denom["verdict"],
            "constructed": cert["existing_valid_fir_constructed"],
            "probe": cert["existing_valid_fir_probe_confirmatory"],
            "mech": cert["mechanism_invalid_fir"],
            "boundary": cert["boundary_invalid_fir"],
            "blocker": cert["blocker"],
            "n_contradictions": len(cert["contradictions_valid_to_invalid"]),
            "xtab": cert["phase1_vs_phase2a_constructed"],
            "task_coverage": cert["task_coverage_constructed"],
            "crosscheck_n": xcheck["n"],
        },
    )
    from experiments.icassp_10of10_hardening.phase2a.write_reports import write_all_reports

    write_all_reports()
    if CHECKPOINT.exists():
        done_path = OUT_DIR / "_checkpoint.done.jsonl"
        if done_path.exists():
            done_path.unlink()
        CHECKPOINT.replace(done_path)
    if LOCK.exists():
        LOCK.unlink()
    print(f"PHASE2A_ALL_STAGES: DONE elapsed_s={time.time()-t0:.3f}", flush=True)
    return 0


def _acquire_lock() -> bool:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if LOCK.exists():
        try:
            old = json.loads(LOCK.read_text(encoding="utf-8"))
            pid = int(old.get("pid", -1))
            os.kill(pid, 0)
            print(f"[phase2a] another run is alive pid={pid}; exiting", flush=True)
            return False
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    LOCK.write_text(json.dumps({"pid": os.getpid()}), encoding="utf-8")
    return True


def verify_existing() -> int:
    """Reproduce summaries from frozen Phase-2A JSON without rewriting certificates."""
    from experiments.icassp_10of10_hardening.phase2a.console_report import print_console
    from experiments.icassp_10of10_hardening.phase2a.verify_frozen import verify_all
    from experiments.icassp_10of10_hardening.phase2a.write_reports import write_all_reports

    print("[phase2a] verify frozen original science + Phase-2A certificates", flush=True)
    result = verify_all(recertify_audit=True)
    write_all_reports()
    print(
        f"[phase2a] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase2a={result['phase2a_reproduction']}",
        flush=True,
    )
    if result["forbidden_imports"]:
        print(f"[phase2a] forbidden imports: {result['forbidden_imports']}", flush=True)
    if result["cert_consistency"]["problems"]:
        print(f"[phase2a] cert problems: {result['cert_consistency']['problems']}", flush=True)
    for a in result["audits"]:
        print(
            f"    audit {a['occupant'][-50:]} live={a['live']} frozen={a['frozen']} match={a['match']}",
            flush=True,
        )
    print_console(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    if (OUT_DIR / "headline.json").exists() and not CHECKPOINT.exists():
        raise SystemExit(verify_existing())
    if not _acquire_lock():
        raise SystemExit(0)
    try:
        code = main()
        if code == 0:
            raise SystemExit(verify_existing())
        raise SystemExit(code)
    finally:
        if LOCK.exists():
            try:
                meta = json.loads(LOCK.read_text(encoding="utf-8"))
                if meta.get("pid") == os.getpid():
                    LOCK.unlink()
            except Exception:
                pass
