"""Exact rational Sturm / real-root isolation for polynomial sign.

Does not import spec checkers or the Phase-2A Bernstein engine.
Polynomials are low-degree-first lists of Fraction or int.
"""
from __future__ import annotations

import math
from fractions import Fraction


def _trim(p: list) -> list:
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q or [0]


def deg(p: list) -> int:
    p = _trim(p)
    return 0 if (len(p) == 1 and p[0] == 0) else len(p) - 1


def _content_int(p: list[int]) -> int:
    g = 0
    for c in p:
        g = math.gcd(g, abs(int(c)))
    return g or 1


def primitive_int(p: list[int]) -> list[int]:
    p = [int(c) for c in _trim(p)]
    c = _content_int(p)
    if c == 1:
        return p
    return [x // c for x in p]


def to_int_poly(p: list[Fraction]) -> list[int]:
    fr = [Fraction(c) for c in _trim(p)]
    lcm = 1
    for c in fr:
        lcm = lcm * c.denominator // math.gcd(lcm, c.denominator)
    return primitive_int([int(c.numerator * (lcm // c.denominator)) for c in fr])


def deriv_int(p: list[int]) -> list[int]:
    if len(p) <= 1:
        return [0]
    return primitive_int([i * p[i] for i in range(1, len(p))])


def poly_eval_frac(p: list, x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(_trim(p)):
        acc = acc * x + Fraction(c)
    return acc


def prem_int(u: list[int], v: list[int]) -> list[int]:
    """Integer pseudo-remainder of u by v (low-degree first)."""
    u = _trim([int(c) for c in u])
    v = _trim([int(c) for c in v])
    if v == [0]:
        raise ZeroDivisionError("poly div by zero")
    dv = deg(v)
    if deg(u) < dv:
        return u
    lc_v = v[dv]
    a = list(u)
    guard = deg(u) - dv + 2
    for _ in range(guard):
        da = deg(a)
        if a == [0] or da < dv:
            break
        lc_a = a[da]
        shift = da - dv
        na = [lc_v * c for c in a]
        need = shift + len(v)
        if len(na) < need:
            na.extend([0] * (need - len(na)))
        for i, c in enumerate(v):
            na[i + shift] -= lc_a * c
        a = primitive_int(na)
    return a if a != [0] else [0]


def _divmod_int(u: list[int], v: list[int]) -> tuple[list[int], list[int]]:
    """Return (dummy_quot, remainder) with the same sign as the remainder over Q."""
    u = _trim([int(c) for c in u])
    v = _trim([int(c) for c in v])
    rem = prem_int(u, v)
    if rem == [0]:
        return [0], [0]
    dv = deg(v)
    du = deg(u)
    delta = max(0, du - dv)
    lc_v = v[dv]
    # prem = lc(v)^{delta+1} * rem_Q  (up to a positive integer)
    if lc_v < 0 and ((delta + 1) % 2 == 1):
        rem = [-c for c in rem]
    return [0], primitive_int(rem)


def sturm_sequence(p: list[Fraction] | list[int]) -> list[list[int]]:
    """Primitive integer Sturm sequence of p (p, p', -rem, ...)."""
    if p and isinstance(p[0], Fraction):
        p0 = to_int_poly([Fraction(c) for c in p])
    else:
        p0 = primitive_int([int(c) for c in p])
    if p0 == [0]:
        return [[0]]
    p1 = deriv_int(p0)
    seq = [p0]
    if p1 != [0]:
        seq.append(p1)
    while True:
        prev, cur = seq[-2], seq[-1]
        if cur == [0] or (len(cur) == 1 and cur[0] == 0):
            break
        if deg(cur) == 0:
            break
        _q, rem = _divmod_int(prev, cur)
        if rem == [0]:
            break
        nxt = primitive_int([-c for c in rem])
        if nxt == [0]:
            break
        seq.append(nxt)
        if deg(nxt) == 0:
            break
        if len(seq) > deg(p0) + 3:
            break
    return seq


def _sign_int(v) -> int:
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def _eval_sign_at(p: list[int], x: Fraction) -> int:
    return _sign_int(poly_eval_frac(p, x))


def sign_variations(seq: list[list[int]], x: Fraction) -> int:
    signs = []
    for p in seq:
        s = _eval_sign_at(p, x)
        if s != 0:
            signs.append(s)
    v = 0
    for a, b in zip(signs, signs[1:]):
        if a != b:
            v += 1
    return v


def distinct_real_root_count(p: list[Fraction] | list[int], a: Fraction, b: Fraction) -> int:
    """Number of distinct real roots in (a, b], Sturm count var(a)-var(b).

    Roots exactly at a are excluded; roots at b are included. Callers that need
    a closed interval should also test Q(a)==0 separately.
    """
    if b < a:
        a, b = b, a
    if a == b:
        return 0
    seq = sturm_sequence(p)
    return max(0, sign_variations(seq, a) - sign_variations(seq, b))


def isolate_distinct_roots(
    p: list[Fraction] | list[int],
    a: Fraction,
    b: Fraction,
    max_bisect: int = 80,
) -> dict:
    """Isolate distinct real roots of p in (a, b] as disjoint rational intervals."""
    if b < a:
        a, b = b, a
    seq = sturm_sequence(p)
    isolated: list[tuple[Fraction, Fraction]] = []
    stack = [(a, b, 0)]
    undecided = False
    while stack:
        lo, hi, depth = stack.pop()
        if hi <= lo:
            continue
        n = max(0, sign_variations(seq, lo) - sign_variations(seq, hi))
        if n == 0:
            continue
        if n == 1:
            isolated.append((lo, hi))
            continue
        if depth >= max_bisect:
            undecided = True
            isolated.append((lo, hi))
            continue
        mid = (lo + hi) / 2
        stack.append((lo, mid, depth + 1))
        stack.append((mid, hi, depth + 1))
    isolated.sort(key=lambda t: t[0])
    return {"intervals": isolated, "undecided": undecided, "sturm_len": len(seq)}


def _gcd_int(u: list[int], v: list[int]) -> list[int]:
    u, v = primitive_int(u), primitive_int(v)
    while v != [0]:
        _q, r = _divmod_int(u, v)
        u, v = v, (r if r != [0] else [0])
    return primitive_int(u)


def square_free_part(p: list[Fraction] | list[int]) -> list[int]:
    if p and isinstance(p[0], Fraction):
        pint = to_int_poly([Fraction(c) for c in p])
    else:
        pint = primitive_int([int(c) for c in p])
    if pint == [0]:
        return [0]
    g = _gcd_int(pint, deriv_int(pint))
    if deg(g) == 0:
        return pint
    q, r = _divmod_int(pint, g)
    if r != [0]:
        return pint
    # _divmod currently discards quotient; recompute over Q
    uf = [Fraction(c) for c in pint]
    vf = [Fraction(c) for c in g]
    dv = deg(vf)
    lv = vf[-1]
    qf = [Fraction(0)] * max(1, deg(uf) - dv + 1)
    rf = list(uf)
    while deg(rf) >= dv and not (len(_trim(rf)) == 1 and rf[0] == 0):
        dr = deg(rf)
        c = rf[dr] / lv
        shift = dr - dv
        if shift >= len(qf):
            qf.extend([Fraction(0)] * (shift - len(qf) + 1))
        qf[shift] += c
        for i, a in enumerate(vf):
            j = i + shift
            if j >= len(rf):
                rf.extend([Fraction(0)] * (j - len(rf) + 1))
            rf[j] -= c * a
        rf = _trim(rf)
    return to_int_poly(qf)


def certify_sign_on_interval(
    p: list[Fraction],
    a: Fraction,
    b: Fraction,
    want: str,
) -> dict:
    """Certify p<=0 (want='nonpos') or p>=0 (want='nonneg') on closed [a,b].

    Tangent / even-multiplicity roots are allowed. A true odd-multiplicity
    crossing into the forbidden half-line is REFUTED.
    """
    if b < a:
        a, b = b, a
    pf = [Fraction(c) for c in _trim(p)]
    if all(c == 0 for c in pf):
        return {"status": "CERTIFIED", "reason": "identically_zero", "n_roots": 0}

    def ok(val: Fraction) -> bool:
        if want == "nonpos":
            return val <= 0
        return val >= 0

    def forbidden(val: Fraction) -> bool:
        if want == "nonpos":
            return val > 0
        return val < 0

    va, vb = poly_eval_frac(pf, a), poly_eval_frac(pf, b)
    if forbidden(va) or forbidden(vb):
        return {
            "status": "REFUTED",
            "reason": "endpoint_forbidden_sign",
            "n_roots": None,
        }

    n0 = distinct_real_root_count(pf, a, b)
    if n0 == 0:
        mid = (a + b) / 2
        vm = poly_eval_frac(pf, mid)
        if forbidden(vm):
            return {"status": "REFUTED", "reason": "constant_forbidden_sign", "n_roots": 0}
        if ok(vm) or vm == 0:
            return {"status": "CERTIFIED", "reason": "sturm_zero_roots_constant_sign", "n_roots": 0}
        return {"status": "UNDECIDED", "reason": "sample_ambiguous", "n_roots": 0}

    sf = square_free_part(pf)
    if sf == [0]:
        return {"status": "UNDECIDED", "reason": "square_free_failed", "n_roots": None}

    iso = isolate_distinct_roots(sf, a, b)
    if iso["undecided"]:
        return {"status": "UNDECIDED", "reason": "root_isolation_depth_limit", "n_roots": len(iso["intervals"])}

    # Build complementary test points: endpoints plus midpoints of root-free gaps.
    cuts = [a]
    for lo, hi in iso["intervals"]:
        cuts.append(lo)
        cuts.append(hi)
    cuts.append(b)
    cuts = sorted(set(cuts))
    samples = [a, b]
    for x, y in zip(cuts, cuts[1:]):
        if y > x:
            samples.append((x + y) / 2)
    for x in samples:
        val = poly_eval_frac(pf, x)
        if forbidden(val):
            return {
                "status": "REFUTED",
                "reason": "sign_crossing_or_forbidden_sample",
                "n_roots": len(iso["intervals"]),
                "x": str(x),
            }
        if not ok(val) and val != 0:
            return {"status": "UNDECIDED", "reason": "sample_ambiguous", "n_roots": len(iso["intervals"])}
    return {
        "status": "CERTIFIED",
        "reason": "sturm_sign_no_forbidden_region",
        "n_roots": len(iso["intervals"]),
        "sturm_len": iso["sturm_len"],
    }
