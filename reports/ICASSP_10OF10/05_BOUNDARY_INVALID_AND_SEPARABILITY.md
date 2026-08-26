# 05 — Boundary invalids and reference-separability

Severity levels frozen: \(0.002, 0.005, 0.010, 0.020\).
Mechanisms frozen: `PASS_DROP`, `STOP_LIFT`. Not tuned per candidate.

Independently verified invalids: **160/160** constructed boundary mutants.

A failed construction that remains VALID is not relabeled invalid.

## Per-task coefficient-space diagnostics (constructed valids + probe valids vs mechanism+boundary invalids)

| Task | \(D_V\) | \(D_I\) | \(G_r\) | exact \(\tau\) exists | inversion |
|---|---:|---:|---:|---|---|
| `fir_lp_loose_8k` | 1.5296633602348348 | 0.02168165085348744 | -1.5079817093813475 | 0 | True |
| `fir_lp_tight_8k` | 1.462869824131724 | 0.0025435791230293088 | -1.4603262450086947 | 0 | True |
| `fir_lp_loose_16k` | 1.50652262139156 | 0.02168165085348744 | -1.4848409705380725 | 0 | True |
| `fir_lp_tight_16k` | 1.4831312161774854 | 0.0025435791230293088 | -1.4805876370544562 | 0 | True |
| `fir_hp_loose_8k` | 1.491109505650585 | 0.015574532504233877 | -1.4755349731463512 | 0 | True |
| `fir_hp_tight_8k` | 1.4487696011267879 | 0.0018592573077666436 | -1.4469103438190212 | 0 | True |
| `fir_hp_loose_16k` | 1.5114901132055634 | 0.015574532504233877 | -1.4959155807013296 | 0 | True |
| `fir_hp_tight_16k` | 1.4483623582957637 | 0.0018592573077666436 | -1.446503100987997 | 0 | True |
| `fir_bp_loose_8k` | 1.6113564569583456 | 0.014027038395885285 | -1.5973294185624602 | 0 | True |
| `fir_bp_tight_8k` | 1.4959743766332323 | 0.0008910303705835882 | -1.4950833462626487 | 0 | True |
| `fir_bp_loose_16k` | 1.6260656067817938 | 0.014027038395885285 | -1.6120385683859084 | 0 | True |
| `fir_bp_tight_16k` | 1.5156523808273898 | 0.0008910303705835882 | -1.5147613504568063 | 0 | True |
| `fir_bs_loose_8k` | 1.4863701715922524 | 0.007709746893285618 | -1.4786604246989667 | 0 | True |
| `fir_bs_tight_8k` | 1.4220747566719805 | 0.0012403449239797078 | -1.4208344117480007 | 0 | True |
| `fir_bs_loose_16k` | 1.542462750278764 | 0.007709746893285618 | -1.5347530033854784 | 0 | True |
| `fir_bs_tight_16k` | 1.4490410342947244 | 0.0012403449239797078 | -1.4478006893707447 | 0 | True |
| `iir_lp_loose_8k` | 66.53489102197732 | 0.001633148480278999 | -66.53325787349704 | 0 | True |
| `iir_lp_tight_8k` | 11.304952430775337 | 1.801617926262515e-05 | -11.304934414596074 | 0 | True |
| `iir_hp_loose_8k` | 22.0569624795322 | 0.02169923263777779 | -22.03526324689442 | 0 | True |
| `iir_hp_tight_8k` | 11.881945643086732 | 0.005810055962046768 | -11.876135587124686 | 0 | True |

Tasks with empirical coefficient non-separability: **20/20**  
Tasks with empirical response non-separability: **19/20**  
Coefficient inversion witnesses: **20**

\(\tau_R=0.05\) is an illustrative operating point only. The scientific statement is the sign of \(G_r\).
