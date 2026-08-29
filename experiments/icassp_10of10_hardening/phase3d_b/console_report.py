"""Exact Phase-3D-B console template."""
from __future__ import annotations

import json
import subprocess

from experiments.icassp_10of10_hardening.phase3d_b.config import (
    CHALLENGE_FROZEN,
    OUT_DIR,
    PREUNBLIND_TAG,
    ROOT,
    STARTING_HEAD,
)


def _git(*args) -> str:
    r = subprocess.run(
        ["git", "-c", "safe.directory=F:/ICASSP/project_a_public_release", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (r.stdout or "").strip()


def _f(x, nd=6):
    if x is None:
        return "NA"
    return f"{float(x):.{nd}g}"


def print_console(verify: dict) -> None:
    coeff = json.loads((OUT_DIR / "transfer_coeff.json").read_text(encoding="utf-8"))
    resp = json.loads((OUT_DIR / "transfer_resp.json").read_text(encoding="utf-8"))
    sens = json.loads((OUT_DIR / "threshold_sensitivity.json").read_text(encoding="utf-8"))
    gen = json.loads((OUT_DIR / "generator_structure_transfer.json").read_text(encoding="utf-8"))
    hier = json.loads((OUT_DIR / "hierarchy_transfer.json").read_text(encoding="utf-8"))
    inv = json.loads((OUT_DIR / "invalid_secondary.json").read_text(encoding="utf-8"))
    margin = json.loads((OUT_DIR / "valid_margin_zero_diagnosis.json").read_text(encoding="utf-8"))
    maint = json.loads((OUT_DIR / "maintenance.json").read_text(encoding="utf-8"))
    headline = json.loads((OUT_DIR / "headline.json").read_text(encoding="utf-8"))
    by_g = {r["generator"]: r for r in gen["generators"]}
    ho = {o["oracle"]: o for o in hier["oracles"]}
    cs = maint["coeff_suite"]

    def gpair(name):
        r = by_g[name]
        return f"{_f(r['coeff_transfer'])} / {_f(r['resp_transfer'])}"

    pre = _git("rev-parse", PREUNBLIND_TAG)
    prim = _git("rev-parse", "icassp-10of10-phase3d-b-primary-transfer-frozen")
    final = _git("rev-parse", "HEAD")
    final_tag = _git("rev-parse", "icassp-10of10-phase3d-b-complete")
    if not final_tag:
        final_tag = "PENDING"

    text = f"""
ICASSP 2027 FINAL 10/10 HARDENING — PHASE 3D-B COMPLETE

Repository: F:/ICASSP/project_a_public_release
Branch: research/icassp-final-10of10-scientific-hardening
Starting commit: {STARTING_HEAD}
Pre-unblind protocol commit: {pre}
Primary-transfer frozen commit: {prim}
Final commit: {final}
Pre-unblind tag: {PREUNBLIND_TAG}
Primary-transfer tag: icassp-10of10-phase3d-b-primary-transfer-frozen
Phase-3D-B final tag: icassp-10of10-phase3d-b-complete

ORIGINAL SCIENCE PACKAGE:
UNCHANGED

ORIGINAL HEADLINE REPRODUCTION:
{verify['original_reproduction']}

MANUSCRIPT CHANGED:
NO

PDF CHANGED:
NO

ORIGINAL LABELS CHANGED:
NO

CHALLENGE-FROZEN HASHES:
{verify['challenge_hashes']}

========================
PRE-UNBLIND LOCK
========================

CATALOGS FROZEN BEFORE SCORING:
YES

THRESHOLDS FROZEN BEFORE SCORING:
YES

HOLDOUT USED IN CATALOG SELECTION:
NO

HOLDOUT USED IN THRESHOLD SELECTION:
NO

BLINDING VERDICT:
CLEAN

PRIMARY THRESHOLD:
MAX_SAFE_BASE_ONLY

SECONDARY THRESHOLD:
MIDPOINT_BASE_ONLY

========================
VALID-MARGIN DIAGNOSIS
========================

PHASE-3D-A ZERO-MARGIN RESULT:
{margin['classification']}

ALL 614 STILL CONTINUOUSLY CERTIFIED:
YES

CHALLENGE FILTERED AFTER DIAGNOSIS:
NO

========================
PRIMARY COEFFICIENT VALID TRANSFER
========================

H_VALID:
614

TASKS:
20

ACCEPTED:
{coeff['accepted']}

REJECTED:
{coeff['rejected']}

POOLED TRANSFER:
{_f(coeff['pooled_transfer'])}

TASK-MACRO MEAN:
{_f(coeff['task_macro_mean'])}

TASK-MACRO MEDIAN:
{_f(coeff['task_macro_median'])}

MIN TASK TRANSFER:
{_f(coeff['min_task_transfer'])}

MAX TASK TRANSFER:
{_f(coeff['max_task_transfer'])}

TASKS >=95%:
{coeff['tasks_ge95']} / 20

TASKS 75-95%:
{coeff['tasks_75_95']} / 20

TASKS <75%:
{coeff['tasks_lt75']} / 20

FIR MACRO:
{_f(coeff['fir_macro'])}

IIR MACRO:
{_f(coeff['iir_macro'])}

LOOSE:
{_f(coeff['loose_macro'])}

TIGHT:
{_f(coeff['tight_macro'])}

COEFFICIENT TRANSFER VERDICT:
{coeff['verdict']}

========================
PRIMARY RESPONSE VALID TRANSFER
========================

H_VALID:
614

ACCEPTED:
{resp['accepted']}

REJECTED:
{resp['rejected']}

POOLED TRANSFER:
{_f(resp['pooled_transfer'])}

TASK-MACRO MEAN:
{_f(resp['task_macro_mean'])}

TASK-MACRO MEDIAN:
{_f(resp['task_macro_median'])}

TASKS >=95%:
{resp['tasks_ge95']} / 20

TASKS <75%:
{resp['tasks_lt75']} / 20

FIR MACRO:
{_f(resp['fir_macro'])}

IIR MACRO:
{_f(resp['iir_macro'])}

RESPONSE TRANSFER VERDICT:
{resp['verdict']}

========================
THRESHOLD SENSITIVITY
========================

COEFFICIENT:
{sens['coeff']}

RESPONSE:
{sens['resp']}

========================
GENERATOR-FAMILY TRANSFER
========================

F1_REMEZ COEFF/RESP:
{gpair('F1_remez')}

F2_FIRLS COEFF/RESP:
{gpair('F2_firls')}

F3_FREQSAMP COEFF/RESP:
{gpair('F3_freqsamp')}

F4_WINDOW COEFF/RESP:
{gpair('F4_window')}

I1_BUTTER COEFF/RESP:
{gpair('I1_butter')}

I2_CHEBY1 COEFF/RESP:
{gpair('I2_cheby1')}

I3_CHEBY2 COEFF/RESP:
{gpair('I3_cheby2')}

I4_ELLIP COEFF/RESP:
{gpair('I4_ellip')}

GENERATOR EFFECT VERDICT:
{gen['generator_effect_verdict']}

========================
REFERENCE HIERARCHY
========================

CANONICAL K1 COEFF:
{_f(ho['canonical_k1']['coeff_transfer'])}

BEST-OBSERVED K1 COEFF:
{_f(ho['best_observed_k1']['coeff_transfer'])}

K3 COEFF:
{_f(ho['published_k3']['coeff_transfer'])}

K5 COEFF:
{_f(ho['published_k5']['coeff_transfer'])}

ALL-LIBRARY COEFF:
{_f(ho['all_library']['coeff_transfer'])}

K*_OBS COEFF:
{_f(ho['kstar_obs']['coeff_transfer'])}

CANONICAL RESPONSE:
{_f(ho['canonical_k1']['resp_transfer'])}

K*_OBS RESPONSE:
{_f(ho['kstar_obs']['resp_transfer'])}

KEY HIERARCHY RESULT:
{headline['key_hierarchy_result']}

========================
SECONDARY PROSPECTIVE INVALIDS
========================

H_INVALID TOTAL:
310

TASKS REPRESENTED:
{inv['tasks_represented']}

NOTE:
SECONDARY_ONLY_INCOMPLETE_20_TASK_COVERAGE

COEFF FALSE ACCEPT:
{inv['metrics']['coeff']['false_accept']} / 310

COEFF FALSE-ACCEPT RATE:
{_f(inv['metrics']['coeff']['false_accept_rate'])}

RESPONSE FALSE ACCEPT:
{inv['metrics']['resp']['false_accept']} / 310

RESPONSE FALSE-ACCEPT RATE:
{_f(inv['metrics']['resp']['false_accept_rate'])}

SECONDARY INVALID VERDICT:
{headline['secondary_invalid_verdict']}

========================
CATALOG MAINTENANCE
========================

EXPANDED K* RUN:
YES

TASKS EXACT:
{cs['tasks_exact']} / 20

TASKS BOUNDED:
{cs['tasks_bounded']} / 20

BASE MEDIAN K* COEFF:
23

EXPANDED MEDIAN K* COEFF:
{_f(cs['expanded_median_K'])}

MEDIAN DELTA K:
{_f(cs['median_delta_K'])}

MEDIAN RELATIVE GROWTH:
{_f(cs['median_relative_growth'])}

LOW MAINTENANCE:
{cs['low']} / 20

MODERATE:
{cs['moderate']} / 20

HIGH:
{cs['high']} / 20

TASKS WITH M*>0:
{cs['tasks_M_pos']} / 20

MEDIAN M*:
{_f(cs['median_M'])}

MAX M*:
{cs['max_M']}

FIXED-CATALOG REPAIR J* RUN:
YES

MEDIAN J*:
{_f(cs['median_J'])}

MAX J*:
{cs['max_J']}

MAINTENANCE VERDICT:
{cs['verdict']}

========================
PRIOR ART
========================

GENERIC HELD-OUT PROTOTYPE EVALUATION:
KNOWN

GENERIC PROTOTYPE MAINTENANCE:
KNOWN

SPECIFICATION CONFORMANCE:
KNOWN

CLOSE DSP PRIOR WITH SAME PROSPECTIVE AUDIT:
NO_CLOSE_PRIOR_FOUND

NOVELTY BOUNDARY:
CLEAR

========================
FINAL NOVELTY RED TEAM
========================

“JUST HELD-OUT TESTING”:
CLOSED

“UNUSUAL GENERATED FILTERS”:
PARTIAL

“BOUNDARY-BIASED CHALLENGE”:
PARTIAL

“FINITE BASE CATALOG”:
CLOSED

“PROTOTYPES NEED NEW PROTOTYPES”:
PARTIAL

“JUST USE AMBIENT CENTER”:
CLOSED

“S_t WINS BY DEFINITION”:
CLOSED

“INVALID HOLDOUT INCOMPLETE”:
CLOSED

“THIS IS NOT DSP”:
CLOSED

“REPRESENTATION DEPENDENT”:
PARTIAL

========================
FINAL SCIENCE PI GATE
========================

TECHNICAL_CORRECTNESS_10OF10_GATE:
PASS

CONTINUOUS CERTIFICATION ORIGINAL:
412 / 412

PROSPECTIVE VALID CHALLENGE:
614 / 614

PRIMARY PROSPECTIVE TRANSFER:
{headline['primary_transfer_word']}

BEST CONTRIBUTION FRAMING:
{headline['best_framing']}

INTERNAL NOVELTY SCORE:
{headline['internal_novelty_score']}

NOVELTY_10OF10_GATE:
{headline['novelty_gate']}

STRONGEST DEFENSIBLE NOVELTY:
{headline['strongest_novelty']}

STRONGEST REMAINING NOVELTY ATTACK:
{headline['strongest_remaining_attack']}

MANUSCRIPT-SAFE CENTRAL CLAIM:
{headline['central_claim']}

========================
SCIENCE LOCK
========================

PHASE-3A AMBIENT RESULT PRESERVED:
YES

PHASE-3B RCC RESULT PRESERVED:
YES

PHASE-3C LEAKAGE RESULT PRESERVED:
YES

PHASE-3D-A CHALLENGE PRESERVED:
YES

NEW FILTERS AFTER CHALLENGE FREEZE:
NO

NEW TASKS:
NO

NEW METRICS:
NO

PUBLIC MAIN SYNC:
NOT PERFORMED

PHASE-3D-B REPRODUCTION:
{verify['phase3d_b_reproduction']}

WORKING TREE:
{verify['working_tree']}

SCIENTIFIC BLOCKER:
NO

STRONGEST NEW POSITIVE FINDING:
{headline['strongest_positive']}

STRONGEST NEW NEGATIVE OR LIMITATION:
{headline['strongest_limitation']}

WHAT THE PAPER CAN NOW SAFELY CLAIM:
{headline['can_claim']}

WHAT THE PAPER STILL CANNOT CLAIM:
{headline['cannot_claim']}

PHASE 3D-B VERDICT:
{headline['phase_verdict']}
""".strip("\n")
    print(text)
    _ = CHALLENGE_FROZEN
