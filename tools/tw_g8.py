# -*- coding: utf-8 -*-
"""國中八年級の共通部品：多項式・根式"""
from fractions import Fraction as F
from tw_common import num, fr
from tw_g7 import sn, par, opv, tidy_sets, term, const, lin

SUP = {2: "<sup>2</sup>", 3: "<sup>3</sup>"}


def poly(cs, v="x"):
    """cs = [a_n, ..., a_0]（降冪）→ 3x<sup>2</sup> － 2x ＋ 1"""
    n = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        c = F(c)
        if c == 0:
            continue
        d = n - i
        var = "" if d == 0 else (v + SUP.get(d, "" if d == 1 else "<sup>%d</sup>" % d))
        a = abs(c)
        if d == 0:
            body = num(a.numerator) if a.denominator == 1 else fr(a.numerator, a.denominator)
        else:
            body = ("" if a == 1 else (num(a.numerator) if a.denominator == 1 else fr(a.numerator, a.denominator))) + var
        if not out:
            out = ("－" if c < 0 else "") + body
        else:
            out += (" － " if c < 0 else " ＋ ") + body
    return out or "0"


def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def padd(a, b, s=1):
    n = max(len(a), len(b))
    a = [0] * (n - len(a)) + list(a)
    b = [0] * (n - len(b)) + list(b)
    r = [x + s * y for x, y in zip(a, b)]
    while len(r) > 1 and r[0] == 0:
        r = r[1:]
    return r


def rt(k, n):
    """k√n（n=1 なら k）"""
    if n == 1:
        return sn(k)
    if k == 1:
        return "√%d" % n
    if k == -1:
        return "－√%d" % n
    return "%s√%d" % (sn(k), n)


def simp(n):
    """√n → (k, m)"""
    k, m = 1, n
    d = 2
    while d * d <= m:
        while m % (d * d) == 0:
            m //= d * d
            k *= d
        d += 1
    return k, m


def pq(a, b, v="x"):
    """（ax ＋ b）"""
    return "（%s）" % lin(a, b, v)
