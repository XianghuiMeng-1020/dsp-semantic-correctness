# PHASE 3A — Ambient dual derivation

This is the dual of the **implemented** primal, not a copied schematic.

## Primal

Decision variables \(c\in\mathbb R^d\), \(\gamma\in\mathbb R\).

\[
\max_{c,\gamma}\ \gamma
\]

subject to, for every frozen pair \(v\in V_t\), \(i\in I_t\),

\[
2c^\top(i-v)+\gamma
\le
\|i\|_2^2-\|v\|_2^2.
\]

No other constraints. If this program is unbounded above, the sets are spherically separable (`INF_SEPARABLE`).

A feasible pair with \(\gamma>0\) is a **strict** single-sphere separator. \(\gamma\le 0\) means no strict Euclidean single-center recovery on the frozen universe. This quantity is \(\Gamma_t^{\mathrm{amb}}\), the **ambient-center oracle margin**. It is not \(G_r\) and not \(G_{\mathrm{obs}}^\star\).

## Lagrangian and dual

Nonnegative multipliers \(\lambda_{vi}\) for each pair. Stationarity in \(\gamma\):

\[
\sum_{v,i}\lambda_{vi}=1.
\]

Stationarity in \(c\):

\[
\sum_{v,i}\lambda_{vi}(i-v)=0.
\]

The dual is therefore

\[
\min_{\lambda\ge 0}
\sum_{v,i}\lambda_{vi}\bigl(\|i\|_2^2-\|v\|_2^2\bigr)
\]

subject to those two equalities.

Strong duality holds when the primal is feasible and bounded (a convex LP). The common optimal value is \(\Gamma_t^{\mathrm{amb}}\).

## Certificates

- **No ambient center.** A dual-feasible \(\lambda\) with objective \(\le 0\) proves \(\Gamma_t^{\mathrm{amb}}\le 0\). If the weights can be reconstructed so the two equalities hold in exact binary64-rational arithmetic, the conclusion is `EXACT_RATIONAL_CERTIFICATE`.
- **Ambient center exists.** A primal \(c\) (itself a binary64 vector, hence a dyadic rational) whose exact pair-min slack is \(>0\) is an `EXACT_RATIONAL_CERTIFICATE` of separability for that \(c\).
- Numerical dual residuals without exact reconstruction are `HIGH_PRECISION_DUAL_CERTIFICATE` or `NUMERICAL_LP_ONLY` according to residual size.

The schematic “\(\sum\lambda(i-v)=0\), \(\sum\lambda=1\)” matches the implemented primal **including signs**. The dual objective uses \(\|i\|_2^2-\|v\|_2^2\), not the reverse.
