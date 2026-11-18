# -*- coding: utf-8 -*-
"""Small helpers shared by the US Algebra 2 generators (gen_us_math_a2_*.py)."""
from fractions import Fraction as F
from us_hs import num, fr, MINUS, expr

X = "<i>x</i>"
SUP = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}


def xp(k, var=X):
    if k == 0:
        return ""
    if k == 1:
        return var
    return var + SUP.get(k, "<sup>%d</sup>" % k)


def poly(cs, var=X):
    """coefficients from the highest power down to the constant"""
    n = len(cs) - 1
    return expr([(c, xp(n - i, var)) for i, c in enumerate(cs)])


def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def ps(v):
    """number in parentheses if negative"""
    return "(%s)" % sf(v) if F(v) < 0 else sf(v)


def lin(a, var=X):
    """x − a"""
    if a == 0:
        return var
    return "%s %s %s" % (var, MINUS if a > 0 else "+", num(abs(a)))


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def peval(p, x):
    v = 0
    for c in p:
        v = v * x + c
    return v


def synth(p, a):
    """divide p by (x − a): quotient list and remainder"""
    q = []
    acc = 0
    for c in p:
        acc = acc * a + c
        q.append(acc)
    return q[:-1], q[-1]
