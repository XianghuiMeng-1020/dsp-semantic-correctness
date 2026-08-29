"""Dumbbell plot of frozen Phase-3D-B per-task transfer. Not a new experiment."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

LABEL = {
    "fir_lp_loose_8k": "FIR LP L 8k",
    "fir_lp_loose_16k": "FIR LP L 16k",
    "fir_lp_tight_8k": "FIR LP T 8k",
    "fir_lp_tight_16k": "FIR LP T 16k",
    "fir_hp_loose_8k": "FIR HP L 8k",
    "fir_hp_loose_16k": "FIR HP L 16k",
    "fir_hp_tight_8k": "FIR HP T 8k",
    "fir_hp_tight_16k": "FIR HP T 16k",
    "fir_bp_loose_8k": "FIR BP L 8k",
    "fir_bp_loose_16k": "FIR BP L 16k",
    "fir_bp_tight_8k": "FIR BP T 8k",
    "fir_bp_tight_16k": "FIR BP T 16k",
    "fir_bs_loose_8k": "FIR BS L 8k",
    "fir_bs_loose_16k": "FIR BS L 16k",
    "fir_bs_tight_8k": "FIR BS T 8k",
    "fir_bs_tight_16k": "FIR BS T 16k",
    "iir_lp_loose_8k": "IIR LP L 8k",
    "iir_lp_tight_8k": "IIR LP T 8k",
    "iir_hp_loose_8k": "IIR HP L 8k",
    "iir_hp_tight_8k": "IIR HP T 8k",
}
ORDER = list(LABEL)


def main() -> None:
    coeff = json.loads((ROOT / "results/icassp_10of10_hardening/phase3d_b/transfer_coeff.json").read_text(encoding="utf-8"))
    resp = json.loads((ROOT / "results/icassp_10of10_hardening/phase3d_b/transfer_resp.json").read_text(encoding="utf-8"))
    c = {r["task"]: r["transfer"] for r in coeff["rows"]}
    r = {r["task"]: r["transfer"] for r in resp["rows"]}
    ys = np.arange(len(ORDER))
    xc = np.array([c[t] for t in ORDER])
    xr = np.array([r[t] for t in ORDER])

    fig, ax = plt.subplots(figsize=(7.16, 3.12), dpi=200)
    for y, a, b in zip(ys, xc, xr):
        ax.plot([a, b], [y, y], color="#7a8188", lw=1.05, zorder=1)
    ax.scatter(
        xc, ys, s=30, c="#b23a48", marker="o", zorder=2,
        label="Coefficient", edgecolors="k", linewidths=0.35,
    )
    ax.scatter(
        xr, ys, s=28, c="#2c6e8a", marker="s", zorder=2,
        label="Magnitude response", edgecolors="k", linewidths=0.35,
    )
    ax.axvline(0.75, color="#b0b0b0", ls=":", lw=0.7)
    ax.axvline(0.95, color="#b0b0b0", ls="--", lw=0.7)
    ax.set_yticks(ys)
    ax.set_yticklabels([LABEL[t] for t in ORDER], fontsize=7.4)
    ax.set_xlabel("Prospective valid-realization transfer", fontsize=8)
    ax.set_xlim(-0.03, 1.05)
    ax.set_ylim(-0.75, len(ORDER) - 0.25)
    ax.tick_params(axis="x", labelsize=7.4)
    ax.legend(loc="lower right", fontsize=7.2, frameon=False, handletextpad=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout(pad=0.25)
    fig.savefig(OUT / "fig_transfer.pdf")
    fig.savefig(ROOT / "manuscript/w4/fig_transfer.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
