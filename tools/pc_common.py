# -*- coding: utf-8 -*-
"""Helpers shared by the US Precalculus generators (gen_us_math_pc_*.py).
Exact trig values, multiples of π, matrices and vectors, on top of us_hs and a2_common."""
import math
from fractions import Fraction as F
from us_hs import num, fr, MINUS
from a2_common import sf, ps, poly, xp, lin, X

GRADE = "precalculus"


def pis(f):
    """f·π as html, e.g. 3π/4"""
    f = F(f)
    if f == 0:
        return "0"
    top = ("" if abs(f.numerator) == 1 else str(abs(f.numerator))) + "π"
    s = top if f.denominator == 1 else fr(top, f.denominator)
    return (MINUS if f < 0 else "") + s


def pis_t(f):
    """f·π as plain text, e.g. 3π/4 (for FAQ and titles)"""
    f = F(f)
    if f == 0:
        return "0"
    top = ("" if abs(f.numerator) == 1 else str(abs(f.numerator))) + "π"
    s = top if f.denominator == 1 else "%s/%d" % (top, f.denominator)
    return ("−" if f < 0 else "") + s


# exact values: key -> html. Keys: "0", "1/2", "r2/2", "r3/2", "1", "r3/3", "r3", "2", "2r3/3", "r2"
VAL = {"0": "0", "1/2": fr(1, 2), "r2/2": fr("√2", 2), "r3/2": fr("√3", 2), "1": "1",
       "r3/3": fr("√3", 3), "r3": "√3", "2": "2", "2r3/3": fr("2√3", 3), "r2": "√2", "und": "undefined"}
FLOAT = {"0": 0, "1/2": .5, "r2/2": math.sqrt(2) / 2, "r3/2": math.sqrt(3) / 2, "1": 1, "r3/3": math.sqrt(3) / 3,
         "r3": math.sqrt(3), "2": 2, "2r3/3": 2 / math.sqrt(3), "r2": math.sqrt(2)}


def key_of(x):
    """float -> (sign, key) or None for undefined"""
    if x is None:
        return None
    for k, v in FLOAT.items():
        if abs(abs(x) - v) < 1e-9:
            return (-1 if x < -1e-12 else 1, k)
    raise AssertionError(x)


def vhtml(sk):
    if sk is None:
        return "undefined"
    s, k = sk
    return (MINUS if s < 0 and k != "0" else "") + VAL[k]


def trig(fn, deg):
    """exact value of fn(deg) as (sign, key) or None (undefined); deg a multiple of 30 or 45"""
    r = math.radians(deg)
    s, c = math.sin(r), math.cos(r)
    s = 0.0 if abs(s) < 1e-12 else s
    c = 0.0 if abs(c) < 1e-12 else c
    val = {"sin": s, "cos": c,
           "tan": None if c == 0 else s / c, "cot": None if s == 0 else c / s,
           "sec": None if c == 0 else 1 / c, "csc": None if s == 0 else 1 / s}[fn]
    return key_of(val)


def trig_h(fn, deg):
    return vhtml(trig(fn, deg))


def rad(deg):
    return F(deg, 180)


def mat(rows):
    """matrix in brackets; rows of numbers or html strings"""
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else sf(c)) for row in rows for c in row)
    return "<span class='mx m%d'>%s</span>" % (n, cells)


def det_h(rows):
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else sf(c)) for row in rows for c in row)
    return "<span class='mx det m%d'>%s</span>" % (n, cells)


def vec(*cs):
    return "⟨%s⟩" % ", ".join(c if isinstance(c, str) else sf(c) for c in cs)


def rt(n):
    """simplified √n as html, e.g. 2√3; n a positive integer"""
    n = int(n)
    out, inside = 1, n
    k = 2
    while k * k <= inside:
        while inside % (k * k) == 0:
            out *= k
            inside //= k * k
        k += 1
    if inside == 1:
        return str(out)
    return ("" if out == 1 else str(out)) + "√%d" % inside


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def C(n, k):
    return math.comb(n, k)


def P(n, k):
    return math.perm(n, k)


def curve_svg(fn, lo=-6, hi=6, ylo=None, yhi=None, unit=22, vasym=(), hasym=(), slant=(), holes=(), label="graph", col="#1f6fd1", step=0.02):
    """grid with the graph of fn (returns None where undefined) and dashed asymptotes"""
    from g8_common import grid_svg
    ylo = lo if ylo is None else ylo
    yhi = hi if yhi is None else yhi
    base = grid_svg(lo, hi, unit=unit, label=label, ylo=ylo, yhi=yhi)
    m = 22
    X_ = lambda x: m + (x - lo) * unit
    Y_ = lambda y: m + (yhi - y) * unit
    add = []
    dash = "stroke-dasharray='6 5'"
    for a in vasym:
        add.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#c0392b' stroke-width='1.8' %s/>" % (X_(a), Y_(ylo), X_(a), Y_(yhi), dash))
    for b in hasym:
        add.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#c0392b' stroke-width='1.8' %s/>" % (X_(lo), Y_(b), X_(hi), Y_(b), dash))
    for mm, b in slant:
        add.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#c0392b' stroke-width='1.8' %s/>" % (X_(lo), Y_(mm * lo + b), X_(hi), Y_(mm * hi + b), dash))
    pieces, cur = [], []
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        x = lo + i * step
        try:
            y = fn(x)
        except (ZeroDivisionError, ValueError):
            y = None
        if y is None or y != y or y < ylo - 0.3 or y > yhi + 0.3:
            if len(cur) > 1:
                pieces.append(cur)
            cur = []
            continue
        cur.append((X_(x), Y_(y)))
    if len(cur) > 1:
        pieces.append(cur)
    for pc in pieces:
        add.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.6'/>" % (" ".join("%.1f,%.1f" % p for p in pc[::2] + [pc[-1]]), col))
    for x, y in holes:
        add.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='#fff' stroke='%s' stroke-width='2.2'/>" % (X_(x), Y_(y), col))
    return base.replace("</g></svg>", "".join(add) + "</g></svg>")
