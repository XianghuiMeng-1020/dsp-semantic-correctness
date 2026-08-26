# 08 — Task-level statistics

Primary unit: specification/task (\(n=20\)). Occupant-pooled rates are secondary.

| Statistic | Value |
|---|---|
| Tasks with reference disagreement (descriptive \(\tau=0.05\), canonical \(d\)) | 20/20 |
| Task-macro FRR | 0.9001446798815218 |
| Median task FRR | 0.9069264069264069 |
| IQR | [0.8928571428571428, 0.9473684210526315] |
| Min / max | 0.7272727272727273 / 0.95 |
| Task-cluster bootstrap 95% CI | [0.8712536597174755, 0.924536910457963] |
| Bootstrap B / seed | 10000 / 20260826 |
| Pooled descriptive FRR | {'n': 370, 'den': 412, 'rate': 0.8980582524271845} |

By generation source (independently verified valids, descriptive \(\tau=0.05\)): `{'library': {'n': 88, 'discord': 58}, 'first_principles': {'n': 24, 'discord': 14}, 'random': {'n': 300, 'discord': 298}}`

The central conclusion must not depend on how many random-valid occupants were drawn.
