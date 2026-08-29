# PHASE 3D-B — Valid margin-zero diagnosis

This audit inspects the Phase-3D-A `spec_margin_grid` field and the frozen
specification checker. It does **not** compute any Phase-3B catalog distance.
The challenge is not filtered or modified.

Classification: `MIXED`

- H_VALID n: 614
- Stored residual identically 0: 611 / 614 (the other 3 are IIR stopband residuals of order 1e-15, i.e. binary64 contact with an inclusive mask; still <= 1e-4)
- Stored continuously certified valid: 614 / 614
- True 4096-point min interior slack: min=-1.8041124150158794e-16, median=7.462357560743306e-09, max=0.024815282142678342
- Members with non-positive interior slack: 24
- Numerical fragility: `False`
- Challenge filtered after diagnosis: `False`
- Catalog distances computed: `False`

## Q1

YES — stored spec_margin_grid is check_specification violation residual; 0 means the 4096-point grid is inside an inclusive mask, not a geometric distance to the edge.

## Q2

YES — Phase-3D-A took max residual over pass/stop/stability/other keys. Passing residuals are identically 0.0, so min=median=0 and near-boundary (residual<=1e-4) is 614/614 by definition of a grid pass.

## Q3

PARTIALLY — the locked schedule does not target residual=0; Remez/elliptic families are equiripple and often have small true slack. Window/Butterworth typically retain slack.

## Q4

NO — a reporting residual of 0 is the pass convention, not a continuous-certification interval failure.

## Q5

YES — all 614 stored members have continuous_status=CERTIFIED_VALID and undecided_included=0.

## Q6

NO — members were not selected or filtered by margin; the challenge is not an intentional boundary-stress set, though some families sit nearer the mask.

## Slack by generator (specification geometry only)

| generator | n | min slack | median slack | max slack | n ≤ 0 |
| --------- | -: | --------: | -----------: | --------: | ----: |
| F1_remez | 152 | 1.6401643046719713e-15 | 4.1432525448223116e-08 | 5.382078670140688e-06 | 0 |
| F2_firls | 146 | 3.799039786457122e-14 | 3.0372435687374686e-09 | 9.98101357921229e-07 | 0 |
| F3_freqsamp | 104 | 0.0 | 2.3520582133223618e-09 | 3.212285366125938e-05 | 12 |
| F4_window | 98 | 0.0 | 2.6164424292506905e-08 | 1.4643801352815806e-06 | 6 |
| I1_butter | 22 | 0.0 | 2.3093322906925364e-18 | 2.3054321873151048e-08 | 1 |
| I2_cheby1 | 28 | 3.568310145831224e-24 | 7.807209997982101e-20 | 5.819241383968219e-12 | 0 |
| I3_cheby2 | 29 | -5.551115123125783e-17 | 5.984465233026584e-06 | 0.024815282142678342 | 2 |
| I4_ellip | 35 | -1.8041124150158794e-16 | 4.734285556213174e-06 | 0.023484572527378823 | 3 |

STOP condition: `NUMERICAL_FRAGILITY` was **not** found.
Continue to primary transfer.
