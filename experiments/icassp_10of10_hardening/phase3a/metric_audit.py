"""Machine-readable metric-geometry audit. Formulas match distances.py / Phase-1."""
from __future__ import annotations


def audit() -> dict:
    return {
        "coefficient": {
            "name": "d_coeff_canonical / d_coeff_mag_equiv",
            "source": "src/verification/distances.py::d_coeff_canonical; Phase-1 d_coeff",
            "exact_formula": (
                "FIR: canonicalize (trim unpaired trailing zeros; keep leading zeros/scale); "
                "zero-pad to equal length; d = min(||v-vr||_2, ||-v-vr||_2) / ||vr||_2, EPS=1e-18. "
                "IIR: a0=1, trim, pad b and a independently, concatenate; "
                "d = ||[b,a]-[br,ar]||_2 / ||[br,ar]||_2."
            ),
            "embedding": (
                "Canonical zero-padded coefficient vector. FIR occupants are oriented so the first "
                "nonzero tap is nonnegative (magnitude-equivalence section). IIR embedding is [b,a]."
            ),
            "class": "reference-normalized relative L2 (FIR: also occupant sign-min)",
            "euclidean_ball_equivalent": True,
            "unrestricted_center_lp_valid": True,
            "justification": (
                "For c≠0, {x : ||x-c||_2/||c||_2 ≤ τ} is a Euclidean ball. Relative scaling changes "
                "the numerical threshold, not membership. Unrestricted (c,τ) separability is therefore "
                "Euclidean sphere separation in the stated embedding. The implemented LP uses "
                "unnormalized ||x-c||_2 on oriented padded vectors. FIR pairwise mag-equiv uses "
                "min(||v-c||,||-v-c||); the LP orients each occupant once (first nonzero ≥ 0) rather "
                "than taking a c-dependent min. That is a fixed Euclidean embedding of the "
                "magnitude-equivalence class, not a new metric."
            ),
            "stop_arm": False,
        },
        "coefficient_historical": {
            "name": "d_coeff_historical",
            "exact_formula": "min-length relative L2 (Phase-2 frozen baseline; not confirmatory)",
            "embedding": "truncate both vectors to min length (pair-dependent)",
            "euclidean_ball_equivalent": False,
            "unrestricted_center_lp_valid": False,
            "stop_arm": True,
            "note": "Not used for Phase-3A ambient analysis.",
        },
        "response": {
            "name": "d_resp_band",
            "source": "src/verification/distances.py::d_resp; Phase-1 d_resp_from_mags",
            "exact_formula": (
                "d = sqrt(mean_j ( |H|(ω_j) - |H_r|(ω_j) )^2 ) over the confirmatory "
                "pass+stop mask on FREQZ_N=131072."
            ),
            "embedding": "band-masked magnitude vector in R^m, m = # masked grid points",
            "class": "RMSE = (1/sqrt(m)) * Euclidean L2 on the masked magnitude embedding",
            "euclidean_ball_equivalent": True,
            "unrestricted_center_lp_valid": True,
            "justification": (
                "RMSE is a positive constant times Euclidean distance in a fixed grid embedding. "
                "Sphere separation is invariant to that constant. Response vectors are numerical "
                "(freqz), not exact rationals. Affine-span reduction of the frozen occupants is "
                "isometric on pairwise distances and preserves the squared-distance differences "
                "that define Γ^amb."
            ),
            "stop_arm": False,
        },
    }
