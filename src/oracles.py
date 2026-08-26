"""Oracle A (coefficient) and Oracle B (spec-band |H| RMSE).

Thresholds are frozen: tau_R grid for A; same-order library pairwise
max + 1e-8 for B. Not fit to invalid residuals.
"""
from __future__ import annotations

from src.valid_metrics import d_coeff, mag_rmse, same_order, unpack


def oracle_a(h, href, tau_r: float) -> bool:
    return d_coeff(h, href) <= float(tau_r)


def oracle_b_threshold(library_impls: list, fs: float, bands: list, href) -> dict:
    """Max same-order library pairwise band RMSE, else all-library pairwise."""
    same_pairs = []
    all_pairs = []
    for i, a in enumerate(library_impls):
        for b in library_impls[i + 1 :]:
            d = mag_rmse(a, b, fs, bands)
            all_pairs.append(d)
            if same_order(a, b):
                same_pairs.append(d)
    used = same_pairs if same_pairs else all_pairs
    fallback = not bool(same_pairs)
    if not used:
        thr = 1e-8
    else:
        thr = float(max(used)) + 1e-8
    return {
        "threshold": thr,
        "n_same_order_pairs": len(same_pairs),
        "n_all_pairs": len(all_pairs),
        "fallback_all_library": fallback,
    }


def oracle_b(h, href, fs: float, bands: list, threshold: float) -> bool:
    return mag_rmse(h, href, fs, bands) <= float(threshold)
