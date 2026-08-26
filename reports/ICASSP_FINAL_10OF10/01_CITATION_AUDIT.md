# 01 — Citation audit

**Verdict:** PASS

All `\cite{...}` keys in `manuscript/w4/paper.tex` resolve in `manuscript/w4/refs.bib`.
The compiled `paper.bbl` contains 19 items, all appearing as [1]–[19] on page 5.

| Use | Keys |
|---|---|
| Filter / mask theory | oppenheim2010dsp, proakis2007dsp, mitra2011dsp, rabiner1975theory, herrmann1973linear |
| FIR windows / sampling / equiripple | kaiser1974window, harris1978windows, rabiner1970freqsamp, parks1972chebyshev, mcclellan1973computer, rabiner1975fir |
| IIR | butterworth1930, constantinides1970, jackson1996filters, antoniou2006filters |
| Library occupant | virtanen2020scipy |
| Testing / generated-code protocol (scope only) | huuhtanen2015dsp, chen2021codex, liu2023evalplus |

No invented EDICS, no uncited claims that SciPy is a testing paper, no model-leaderboard citations used as primary evidence.
Vaidyanathan 1993 remains in the bib unused; it is not cited and does not appear on page 5.

Chen/Liu support only the sentence that unique-output unit tests do not score a non-unique mask. They are not used as an LLM benchmark cite.
