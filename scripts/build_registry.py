#!/usr/bin/env python3
"""Write registry/suite_s.json and registry/suite_n.json from frozen rules."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.mask_rules import (  # noqa: E402
    CANONICAL,
    LEGACY_ARM_N,
    LOOSE_8K,
    scale_mask,
    tighten_mask,
)

OUT = ROOT / "registry"


def _task_n(kind: str, tightness: str, fs: float) -> dict:
    proto = LOOSE_8K[kind]
    passes, stops = deepcopy(proto["pass"]), deepcopy(proto["stop"])
    if tightness == "tight":
        passes, stops = tighten_mask(passes, stops)
    if abs(fs - 16000.0) < 1e-9:
        passes, stops = scale_mask(passes, stops, 2.0)
    family = "fir" if kind.startswith("fir") else "iir"
    rtype = kind.split("_")[1]
    tid = f"{kind}_{tightness}_{int(fs // 1000)}k"
    floor = 1e-6 if family == "fir" else 1e-3
    rec = {
        "task_id": tid,
        "family": "filter_specification",
        "type": f"{family}_{rtype}",
        "sampling_rate": fs,
        "pass_band": passes,
        "stop_band": stops,
        "constraints": {
            "pole_radius_max": 0.999 if family == "iir" else None,
            "freqz_points": 4096,
        },
        "phase_requirement": "none",
        "order_constraint": "free",
        "canonical_designer": CANONICAL[family],
        "residual_floor": floor,
        "notes": (
            "loose 8 kHz prototype"
            + ("; tightness derived mechanically" if tightness == "tight" else "")
            + ("; edges scaled x2 for 16 kHz" if fs > 9000 else "")
        ),
        "legacy_arm_n_id": LEGACY_ARM_N.get(tid),
    }
    return rec


def suite_n() -> dict:
    tasks = []
    for kind in ("fir_lp", "fir_hp", "fir_bp", "fir_bs"):
        for fs in (8000.0, 16000.0):
            for tightness in ("loose", "tight"):
                tasks.append(_task_n(kind, tightness, fs))
    for kind in ("iir_lp", "iir_hp"):
        for tightness in ("loose", "tight"):
            tasks.append(_task_n(kind, tightness, 8000.0))
    return {
        "suite": "N",
        "purpose": "non-unique magnitude-mask filter specifications",
        "n_tasks": len(tasks),
        "derivation": {
            "tight": "pass ripple x1/5 about 1; stop ceiling x1/5; stop edge moves halfway toward facing pass",
            "fs_16k": "all band edges x2",
        },
        "tasks": tasks,
    }


def suite_s() -> dict:
    tasks = [
        {
            "task_id": "crosscorrelation_integer_delay",
            "family": "singleton_identity",
            "type": "integer_lag",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "argmax of circular cross-correlation equals the circular delay L",
                "output": "integer L in 0..N-1",
                "test_vector": {"N": 128, "L": 17, "seed": 19},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "fft_circular_xcorr_argmax",
            "residual_floor": 0.0,
            "notes": "Unique integer. Mutants: off-by-one; sign-flipped lag.",
            "invalid_mechanisms": ["off_by_one_lag", "sign_flipped_lag"],
        },
        {
            "task_id": "circular_convolution_theorem",
            "family": "singleton_identity",
            "type": "circular_convolution",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "y = Re IFFT(FFT(x) * FFT(h)) for equal-length real x,h",
                "test_vector": {"N": 128, "seed": 20270823},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "dft_product_ifft",
            "residual_floor": 1e-6,
            "notes": "Unique given DFT convention. Mutants: linear conv; conjugate product.",
            "invalid_mechanisms": ["linear_not_circular", "conjugate_product"],
        },
        {
            "task_id": "linear_convolution_zero_padded_dft",
            "family": "singleton_identity",
            "type": "linear_convolution",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "zero-padded circular convolution equals linear convolution",
                "length": "len(x)+len(h)-1",
                "test_vector": {"Nx": 32, "Nh": 9, "seed": 3},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "zero_padded_fft_product",
            "residual_floor": 1e-6,
            "notes": "Unique given declared length. Mutants: missing pad; circular wrap.",
            "invalid_mechanisms": ["missing_pad", "circular_wrap"],
        },
        {
            "task_id": "autocorrelation_lag0_energy",
            "family": "singleton_identity",
            "type": "energy_identity",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "R_xx[0] = sum(x**2) on lags -(N-1)..+(N-1)",
                "test_vector": {"N": 64, "seed": 7},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "np_correlate_full",
            "residual_floor": 1e-4,
            "notes": "Unique lag-0 identity. Mutants: mean at lag 0; omit energy.",
            "invalid_mechanisms": ["lag0_is_mean", "lag0_is_zero"],
        },
        {
            "task_id": "decimation_alias_frequency",
            "family": "singleton_identity",
            "type": "alias_map",
            "sampling_rate": 1000.0,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "f_alias = |mod(f + fs_out/2, fs_out) - fs_out/2|, fs_out=fs/M, one-sided",
                "test_vector": {"f": 350.0, "fs": 1000.0, "M": 4},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "fold_alias_hz",
            "residual_floor": 1e-8,
            "notes": "Unique folding map. Mutants: no fold; fold about old Nyquist.",
            "invalid_mechanisms": ["no_fold", "fold_old_nyquist"],
        },
        {
            "task_id": "digital_frequency_rescale",
            "family": "singleton_identity",
            "type": "frequency_rescale",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "f_hat_out = f_hat_in * fs_in / fs_out (physical Hz invariant; no alias)",
                "test_vector": {"f_hat": 0.125, "fs_in": 8000.0, "fs_out": 16000.0},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "physical_hz_invariant_rescale",
            "residual_floor": 1e-8,
            "notes": "Unique map. Mutants: forget rescale; invert ratio.",
            "invalid_mechanisms": ["forget_rescale", "inverted_ratio"],
        },
        {
            "task_id": "nyquist_hz",
            "family": "singleton_identity",
            "type": "scalar_nyquist",
            "sampling_rate": 8000.0,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "Nyquist frequency is fs/2",
                "test_vector": {"fs": 8000.0},
            },
            "phase_requirement": "none",
            "order_constraint": "none",
            "canonical_designer": "fs_over_2",
            "residual_floor": 0.0,
            "notes": "Unique scalar. Mutants: return 1; return fs.",
            "invalid_mechanisms": ["return_one_hz", "return_fs"],
        },
        {
            "task_id": "integer_delay_impulse",
            "family": "singleton_identity",
            "type": "unique_fir",
            "sampling_rate": None,
            "pass_band": None,
            "stop_band": None,
            "constraints": {
                "identity": "unique FIR of delay D is delta[n-D]",
                "test_vector": {"N": 32, "D": 7},
            },
            "phase_requirement": "none",
            "order_constraint": "N=32",
            "canonical_designer": "unit_impulse_at_D",
            "residual_floor": 0.0,
            "notes": "Unique coefficient vector. Mutants: impulse at 0; impulse at D+1.",
            "invalid_mechanisms": ["impulse_at_zero", "impulse_at_D_plus_1"],
        },
    ]
    return {
        "suite": "S",
        "purpose": "singleton identities where reference matching must coincide with S_t",
        "n_tasks": len(tasks),
        "tasks": tasks,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    s = suite_s()
    n = suite_n()
    (OUT / "suite_s.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    (OUT / "suite_n.json").write_text(json.dumps(n, indent=2), encoding="utf-8")
    print(f"wrote {OUT / 'suite_s.json'} n={s['n_tasks']}")
    print(f"wrote {OUT / 'suite_n.json'} n={n['n_tasks']}")
    assert s["n_tasks"] == 8
    assert n["n_tasks"] == 20


if __name__ == "__main__":
    main()
