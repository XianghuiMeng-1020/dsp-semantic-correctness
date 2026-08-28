# PHASE 2A — UNDECIDED diagnosis (constructed FIR valids)

Total constructed FIR valids UNDECIDED: 2 / 336

## Reason counts

- `polynomial_arithmetic_resource_limit`: 2

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

