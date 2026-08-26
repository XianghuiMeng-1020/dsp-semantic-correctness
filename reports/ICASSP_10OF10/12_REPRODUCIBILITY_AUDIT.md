# 12 — Reproducibility audit

Entry point:

```text
python -m experiments.icassp_10of10.run_all
```

## Environment recorded at this run

- Python: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- Platform: Windows-11-10.0.26200-SP0
- numpy: 2.3.5
- scipy: 1.15.3
- seed: 20260826
- verifier: independent_spec_verifier/1.0
- elapsed_s: 944.9154484272003

## Dataset hashes

{
  "suite_n": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
  "suite_s": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
  "valid_manifest": "5ba9b66db22f784a7f677aa988fdeb922ca2245f568d6805d84a03b01ae02933",
  "invalid_manifest": "bfd8e5137c8475b5b4175f1c35756b9677e49ca2f94de19f9be21be4ff890e97"
}

## Regenerated artifacts

All under `data/icassp_10of10/`:
`recertify.json`, `canonicalization.json`, `feasible_probe.json`,
`boundary_invalids.json`, `task_metrics.json`, `reference_choice.json`,
`multi_reference.json`, `task_stats.json`, `singleton.json`,
`generated_witness.json`, `environment.json`, `summary.json`,
plus `probe_candidates/` and `boundary_invalids/`.

README is **not** rewritten in this scientific pass.
