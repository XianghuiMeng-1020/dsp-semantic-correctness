#!/usr/bin/env python3
"""Authoritative reproduction entry point.

    python -m experiments.icassp_10of10.run_all

Regenerates verified labels, task-level metrics, separability,
same-order probes, reference-choice, multi-reference, boundary invalids,
and manuscript-ready number tables under data/icassp_10of10/.
"""
from __future__ import annotations

from multiprocessing import freeze_support

from experiments.icassp_10of10.pipeline import run_all
from experiments.icassp_10of10.write_reports import write_reports


def main() -> int:
    summary = run_all()
    write_reports(summary)
    print("ALL_10OF10_STAGES: DONE")
    return 0


if __name__ == "__main__":
    freeze_support()
    raise SystemExit(main())
