"""Stage A — search / construction checker.

Approximate 4096-point admission checker used during candidate generation.
This is the ONLY module allowed to wrap ``src.spec_checker``.

The independent verifier must not import this module.
"""
from __future__ import annotations

from src.spec_checker import check_specification as _construction_check

SEARCH_CHECKER_NAME = "search_checker"
SEARCH_FREQZ_N = 4096


def search_check(task_id: str, implementation) -> dict:
    """Return the construction-time membership result."""
    out = _construction_check(task_id, implementation)
    return {
        "pass": bool(out["pass"]),
        "residuals": dict(out["residuals"]),
        "checker": SEARCH_CHECKER_NAME,
        "freqz_n": SEARCH_FREQZ_N,
    }
