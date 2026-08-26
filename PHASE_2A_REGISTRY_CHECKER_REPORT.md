# PHASE 2A — Registry and specification checker

Infrastructure validation only. No Suite N occupants generated. No LLM
draws. No manuscript edits. Thresholds not retuned.

## 1. Files created

| Path | Role |
|---|---|
| `registry/suite_s.json` | 8 singleton identity tasks |
| `registry/suite_n.json` | 20 magnitude-mask tasks |
| `src/mask_rules.py` | Mechanical tight + 16 kHz derivation |
| `src/spec_checker.py` | `check_specification(task_id, implementation)` |
| `src/suite_s_fixtures.py` | Suite S canonicals, alternate valids, mutants |
| `scripts/build_registry.py` | Writes both registries from frozen rules |
| `scripts/validate_phase2a.py` | Arm N + Suite S checker validation |

The checker evaluates specification membership only. It does not compute
coefficient distance, does not call a canonical designer, and does not
run Oracle A, Oracle B, or the tone battery \(T\).

## 2. Registry summary

**Suite S: 8 tasks**

| ID | Task | Residual floor |
|---|---|---|
| S1 | `crosscorrelation_integer_delay` | 0 |
| S2 | `circular_convolution_theorem` | \(10^{-6}\) |
| S3 | `linear_convolution_zero_padded_dft` | \(10^{-6}\) |
| S4 | `autocorrelation_lag0_energy` | \(10^{-4}\) |
| S5 | `decimation_alias_frequency` | \(10^{-8}\) |
| S6 | `digital_frequency_rescale` | \(10^{-8}\) |
| S7 | `nyquist_hz` | 0 |
| S8 | `integer_delay_impulse` | 0 |

No Suite S task was dropped. Alternate realizations of S1, S2, S3, and S8
all satisfy \(S_t=1\) and agree with the canonical (disagreement \(\le 6.4\times 10^{-16}\)).
None is an invalid singleton design.

**Suite N: 20 tasks**

- FIR: LP/HP/BP/BS \(\times\) \(\{8,16\}\,\mathrm{kHz}\) \(\times\) \(\{\mathrm{loose},\mathrm{tight}\}\) = 16
- IIR: LP/HP \(\times\) \(\{\mathrm{loose},\mathrm{tight}\}\) at \(8\,\mathrm{kHz}\) = 4

Tight masks are derived mechanically (pass ripple \(\times 1/5\) about 1;
stop ceiling \(\times 1/5\); stop edge moves halfway toward the facing pass).
16 kHz edges are the 8 kHz edges \(\times 2\).

Sanity: `fir_lp_tight_8k` equals the frozen P2C mask
(\(\lvert H\rvert\in[0.99,1.01]\) on \([0,800]\), \(\lvert H\rvert\le 0.01\) on
\([1400,4000]\)).

Legacy Arm N aliases: `fir_lowpass_spec` → `fir_lp_loose_8k`,
`fir_bandpass_spec` → `fir_bp_loose_8k`, `fir_bandstop_spec` →
`fir_bs_loose_8k`, `iir_lowpass_stable_spec` → `iir_lp_loose_8k`.

## 3. Checker validation

| Universe | Result |
|---|---|
| Existing Arm N valid controls | **12/12** \(S_t=1\) |
| Existing Arm N mutants | **12/12** \(S_t=0\) |
| Suite S canonicals | **8/8** \(S_t=1\) |
| Suite S predefined mutants | **16/16** \(S_t=0\) |

Arm N 12/12 was required before Suite S scoring. It passed. No threshold
was changed.

## 4. Failures

None.

No singleton task admitted two materially different valids
(\(d>0.05\)).

## 5. Recommendation

**READY_FOR_PHASE_2B**

Phase 2B may generate constructed Suite N valids and M1–M8 mutants.
Do not start LLM generations. Do not modify the manuscript.
