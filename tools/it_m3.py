# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: monomi e polinomi (parti comuni).
・mono(c, {"a": 2, "b": 1}) → «−3a²b»; poly([(c, {..}), …]) → «2x² − 3x + 1» (ordinato per grado decrescente)
・padd / pmul (polinomi come dict {tuple(sorted exps): coeff}); grado
"""
from fractions import Fraction as Fr
from it_media import fq

MINUS = "−"
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def sup(n):
    return "" if n == 1 else "".join(SUP[int(c)] for c in str(n))


def lett(ex):
    return "".join(v + sup(e) for v, e in sorted(ex.items()) if e)


def mono(c, ex, first=True):
    c = Fr(c)
    L_ = lett(ex)
    a = abs(c)
    body = ("" if a == 1 and L_ else fq(a)) + L_
    if first:
        return (MINUS if c < 0 else "") + body
    return " %s %s" % (MINUS if c < 0 else "+", body)


def key(ex):
    return tuple(sorted((v, e) for v, e in ex.items() if e))


def P(terms):
    """lista [(c, ex)] → dict"""
    out = {}
    for c, ex in terms:
        k = key(ex)
        out[k] = out.get(k, 0) + Fr(c)
    return {k: v for k, v in out.items() if v}


def deg(k):
    return sum(e for _, e in k)


def show(p):
    if not p:
        return "0"
    ks = sorted(p, key=lambda k: (-deg(k), [(-e if v == "x" else 0) for v, e in k], k))
    s = ""
    for k in ks:
        s += mono(p[k], dict(k), s == "")
    return s


def mul(p, q):
    out = {}
    for k1, c1 in p.items():
        for k2, c2 in q.items():
            ex = dict(k1)
            for v, e in k2:
                ex[v] = ex.get(v, 0) + e
            k = key(ex)
            out[k] = out.get(k, 0) + c1 * c2
    return {k: v for k, v in out.items() if v}


def add(p, q, s=1):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, 0) + s * c
    return {k: v for k, v in out.items() if v}


def evalp(p, vals):
    tot = Fr(0)
    for k, c in p.items():
        t = Fr(c)
        for v, e in k:
            t *= Fr(vals[v]) ** e
        tot += t
    return tot
