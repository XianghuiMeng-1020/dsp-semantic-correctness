# PHASE 3D-B — Generator-family and DSP-structural transfer

Generator groups were frozen in Phase 3D-A. They were not inferred from rejection.

| generator | n | coeff transfer | response transfer |
| --------- | -: | -------------: | ----------------: |
| F1_remez | 152 | 0.138158 | 0.947368 |
| F2_firls | 146 | 0.130137 | 1 |
| F3_freqsamp | 104 | 0.115385 | 0.923077 |
| F4_window | 98 | 0.0510204 | 0.959184 |
| I1_butter | 22 | 0.181818 | 1 |
| I2_cheby1 | 28 | 0.0357143 | 1 |
| I3_cheby2 | 29 | 0.0689655 | 0.862069 |
| I4_ellip | 35 | 0.0571429 | 0.857143 |

Generator-effect verdict: `MIXED`

Order-bin definition: {'rule': 'descriptive tertiles of frozen H_VALID n_taps (FIR) or IIR order; not inferred from rejection', 'q33': 37, 'q67': 71, 'inferential': 0}

Structure (coeff): {'family': {'fir': 0.114, 'iir': 0.07894736842105263}, 'tightness': {'loose': 0.09832134292565947, 'tight': 0.12690355329949238}, 'filter_type': {'lp': 0.06532663316582915, 'hp': 0.14054054054054055, 'bp': 0.0967741935483871, 'bs': 0.14150943396226415}, 'order_bin': {'low_le_q33': 0.12962962962962962, 'mid_q33_q67': 0.13025210084033614, 'high_gt_q67': 0.04375}}

Structure (resp): {'family': {'fir': 0.96, 'iir': 0.9210526315789473}, 'tightness': {'loose': 0.9688249400479616, 'tight': 0.9187817258883249}, 'filter_type': {'lp': 0.9547738693467337, 'hp': 0.9621621621621622, 'bp': 0.9112903225806451, 'bs': 0.9811320754716981}, 'order_bin': {'low_le_q33': 0.9212962962962963, 'mid_q33_q67': 0.9621848739495799, 'high_gt_q67': 0.98125}}
