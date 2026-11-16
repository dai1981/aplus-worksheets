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


def qroots(a, b, c):
    """ax²＋bx＋c＝0 の解の文字列（「x ＝ …」）。D＜0 なら None"""
    from math import gcd, isqrt
    D = b * b - 4 * a * c
    if D < 0:
        return None
    r = isqrt(D)
    if r * r == D:
        x1, x2 = sorted([F(-b + r, 2 * a), F(-b - r, 2 * a)])
        return "x ＝ %s（重根）" % sn(x1) if x1 == x2 else "x ＝ %s 或 %s" % (sn(x1), sn(x2))
    k, m = simp(D)
    p, q, d = -b, k, 2 * a
    if d < 0:
        p, d = -p, -d
    g = gcd(gcd(abs(p), q), d)
    p, q, d = p // g, q // g, d // g
    rad = "√%d" % m if q == 1 else "%d√%d" % (q, m)
    top = ("±" + rad) if p == 0 else "%s ± %s" % (sn(p), rad)
    return "x ＝ " + (top if d == 1 else fr(top, d))
