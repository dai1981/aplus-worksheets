# -*- coding: utf-8 -*-
"""Sverige gymnasiet（Gy25 Matematik nivå 1c–5）: gemensamma delar för se_g1〜se_g5（単元関数は引数なし）。
se_h の上に take()（åk 7–9 の単元から問題関数を取り出す）、pol()（多項式）、ang()、frac()。"""
import math
from fractions import Fraction as F
from se_h import (gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin, expr, lin,  # noqa: F401
                  kosy, kurve, figure, wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE)


def take(fn, lv, name):
    dd = fn(lv)
    for _, parts in dd["sets"]:
        for mk, _n in parts:
            if mk.__name__ == name:
                return mk
    raise KeyError(name)


def nz(a, b):
    while True:
        v = ri(a, b)
        if v:
            return v


SUPS = {2: "²", 3: "³", 4: "⁴", 5: "⁵"}


def xp(n, v="x"):
    if n == 0:
        return ""
    if n == 1:
        return v
    return v + SUPS.get(n, sup(n))


def pol(cs, v="x"):
    """cs = {exponent: koefficient} → 3x² − 2x + 5（högsta grad först）"""
    return expr([(cs[e], xp(e, v)) for e in sorted(cs, reverse=True)])


def deriv(cs):
    return {e - 1: c * e for e, c in cs.items() if e != 0}


def ev(cs, x):
    return sum(F(c) * F(x) ** e for e, c in cs.items())


def integ(cs):
    return {e + 1: F(c, e + 1) for e, c in cs.items()}


def U(slug, dom, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return unit(slug, dom, title, short, std, meta, kb, ks, sets, think, ex, mist, faq)


def graf(f, xr, yr, pts=(), label="graf", W=330, H=250):
    return kurve([(f, BLUE, "")], xr, yr, pts, W, H, label)
