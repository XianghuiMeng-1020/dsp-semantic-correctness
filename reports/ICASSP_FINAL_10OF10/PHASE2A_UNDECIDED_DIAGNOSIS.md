# PHASE 2A — UNDECIDED diagnosis (constructed FIR valids)

Total constructed FIR valids UNDECIDED: 2 / 336

## Reason counts

- `polynomial_arithmetic_resource_limit`: 2
  - `data/valid/first_principles/fir_bs_tight_8k__frequency_sampling__shortest.npy` (n_taps=267)
  - `data/valid/first_principles/fir_bs_tight_16k__frequency_sampling__shortest.npy` (n_taps=267)

Occupants:

- `data/valid/first_principles/fir_bs_tight_8k__frequency_sampling__shortest.npy` n_taps=267 reason=`polynomial_arithmetic_resource_limit`
- `data/valid/first_principles/fir_bs_tight_16k__frequency_sampling__shortest.npy` n_taps=267 reason=`polynomial_arithmetic_resource_limit`

Categories:

* `endpoint_enclosure_limitation`: cosine endpoint sliver not certified;
* `polynomial_arithmetic_resource_limit`: Bernstein node/depth budget;
* `root_isolation_or_depth_limit`: mixed Bernstein coefficients at max depth;
* `exact_equality_ambiguity`: not used as a dump category in this run;
* `implementation_bug`: none identified unless a VALID→INVALID appears.

Implication for the finite-universe gap: Phase-2A does not relabel occupants.
A certified-valid *subset* must not silently replace \(\mathcal{U}_t\).

The two UNDECIDED constructed occupants are the longest frequency-sampling
tight bandstops (`n_taps=267`). Bernstein subdivision hit the node/time budget.
They remain frozen VALID. They are not the farthest valids in the frozen
reference-choice tables. Each of `fir_bs_tight_8k` and `fir_bs_tight_16k`
still has 20/21 constructed occupants with Bernstein `CERTIFIED_VALID`.
This does not materially threaten the existing finite-universe gap, but it
also does not license replacing those tasks' \(\mathcal{U}_t\) by the certified subset.

