# -*- coding: utf-8 -*-
"""Türkiye lise（10.〜12. sınıf）の共通部品。tr_s9a の部品の上に、三角比・多項式・メタ文の自動化。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, M
from tr_g7 import sn, par, dq, lin, MINUS
from tr_common import low
from tr_s9a import ri, ch, sh, nz, named, kosy, kurve, reuse, cap, iv, rts, rt, pw, _figure  # noqa: F401


def figure(pts, segs, sides=(), right=(), label="geometrik şekil", ticks=()):
    return _figure(pts, segs, sides=sides, right=right, label=label, ticks=ticks)


def frs(a, b):
    """'√3', 2 → HTML kesir"""
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


# 特別角の値（文字列）
TRIG = {
    ("sin", 30): frs(1, 2), ("sin", 45): frs("√2", 2), ("sin", 60): frs("√3", 2), ("sin", 0): "0", ("sin", 90): "1",
    ("cos", 30): frs("√3", 2), ("cos", 45): frs("√2", 2), ("cos", 60): frs(1, 2), ("cos", 0): "1", ("cos", 90): "0",
    ("tan", 30): frs("√3", 3), ("tan", 45): "1", ("tan", 60): "√3", ("tan", 0): "0",
    ("cot", 30): "√3", ("cot", 45): "1", ("cot", 60): frs("√3", 3), ("cot", 90): "0",
}
TVAL = {("sin", 30): 0.5, ("sin", 45): 2 ** .5 / 2, ("sin", 60): 3 ** .5 / 2, ("cos", 30): 3 ** .5 / 2, ("cos", 45): 2 ** .5 / 2, ("cos", 60): 0.5,
        ("tan", 30): 3 ** .5 / 3, ("tan", 45): 1.0, ("tan", 60): 3 ** .5, ("cot", 30): 3 ** .5, ("cot", 45): 1.0, ("cot", 60): 3 ** .5 / 3,
        ("sin", 0): 0.0, ("sin", 90): 1.0, ("cos", 0): 1.0, ("cos", 90): 0.0, ("tan", 0): 0.0, ("cot", 90): 0.0}
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def poly(cs, v="x"):
    """[a_n, …, a_0] → '2x³ − x + 5'"""
    n = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        c = F(c)
        if c == 0:
            continue
        p = n - i
        a = abs(c)
        body = ("" if (a == 1 and p > 0) else (num(a) if a.denominator == 1 else frs(a.numerator, a.denominator))) + (v if p >= 1 else "") + (str(p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")) if p >= 2 else "")
        if out == "":
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"


def peval(cs, x):
    v = F(0)
    for c in cs:
        v = v * x + c
    return v


def nCr(n, r):
    return math.comb(n, r)


def nPr(n, r):
    return math.perm(n, r)


def U(grade, slug, dom, code, sort, title, short, std, topics, kb, ks, sets, think, ex, mist, faq):
    meta = "%d. sınıf %s çalışma kâğıdı: %s. 100 soru ve cevap anahtarı." % (grade, low(short), topics)
    return unit(slug, dom, code, sort, title, short, std, meta, kb, ks, sets, think, ex, mist, faq)


def W3(ws, g):
    """重複・正解と同じ誤答を落とす"""
    out = []
    for w in ws:
        if w is None or w == g or w in out:
            continue
        out.append(w)
    return out
