# PHASE 2A — Crash / power-loss recovery

Unexpected shutdown must not lose completed occupant certificates.

## Durability

* Each finished occupant is appended to `results/icassp_10of10_hardening/phase2a/_checkpoint.jsonl` and **fsync'd**.
* A truncated last line after a crash is skipped on resume.
* `progress.json` is rewritten atomically every 5 new records and after each cohort.
* `denominator.json` is reused on resume (not recomputed).
* A `_running.lock` prevents two overlapping `run_all` processes.
* On success the checkpoint is renamed to `_checkpoint.done.jsonl` (not deleted until you choose).

## Resume command

```bat
cd /d F:\ICASSP\project_a_public_release
python -m experiments.icassp_10of10_hardening.phase2a.run_all
```

If `headline.json` exists and the live checkpoint is gone, the command exits immediately.

## Auto-resume after reboot

`scripts/phase2a_autoresume.cmd` is copied into the current Windows Startup folder so a login after a crash continues the run. Remove that shortcut after Phase 2A completes if you do not want it to fire again.

Log: `results/icassp_10of10_hardening/phase2a/autoresume.log`
