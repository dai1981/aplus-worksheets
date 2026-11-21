# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: gemeinsame Teile
  expr([(k, "x²"), (k, "x"), (k, "")])  Term als Text: 2x² − 3x + 5
  gl(m, b)        Geradengleichung: y = 2x − 3, y = −½x + 1 (Brüche als HTML)
  kosy(...)       Koordinatensystem mit Geraden und Punkten (SVG, lg)
"""
from fractions import Fraction as Fr
from de_common import wrap, line, text, INK, BLUE, RED, GREEN
from de_k6 import bh, dz
from de_k7 import mcq, eur, pz, rd, zk  # noqa: F401

MINUS = "−"
GRID = "#d5dfec"


def coef(k, var, first):
    """ein Summand mit Vorzeichen"""
    k = Fr(k)
    sgn = MINUS if k < 0 else "+"
    a = abs(k)
    if var:
        body = ("" if a == 1 else (bh(a) if a.denominator != 1 else dz(a))) + var
    else:
        body = bh(a) if a.denominator != 1 else dz(a)
    if first:
        return (MINUS if k < 0 else "") + body
    return " %s %s" % (sgn, body)


def expr(terms):
    out = ""
    for k, v in terms:
        if Fr(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def gl(m, b, y="y"):
    return "%s = %s" % (y, expr([(m, "x"), (b, "")]))


def par(v):
    """negative Zahl in Klammern"""
    v = Fr(v)
    s = bh(v) if v.denominator != 1 else dz(v)
    return "(%s)" % s if v < 0 else s


def kosy(lines=(), pts=(), lo=-5, hi=5, u=24, label="Koordinatensystem", names=None):
    """lines: [(m, b, farbe, name)], pts: [(x, y, name)]"""
    n = hi - lo
    W = H = n * u + 40
    x0 = 20 - lo * u
    y0 = 20 + hi * u
    X = lambda x: x0 + float(x) * u
    Y = lambda y: y0 - float(y) * u
    s = []
    for i in range(lo, hi + 1):
        s.append(line(X(i), Y(lo), X(i), Y(hi), GRID, 1) + line(X(lo), Y(i), X(hi), Y(i), GRID, 1))
    s.append(line(X(lo), Y(0), X(hi) + 8, Y(0), INK, 2.2) + line(X(0), Y(lo), X(0), Y(hi) - 8, INK, 2.2))
    for i in range(lo, hi + 1):
        if i and i % 2 == 0:
            s.append(text(X(i), Y(0) + 19, dz(i), 16, weight=600) + text(X(0) - 13, Y(i) + 6, dz(i), 16, weight=600))
    s.append(text(X(hi) + 6, Y(0) - 8, "x", 17, italic=True) + text(X(0) + 12, Y(hi) - 2, "y", 17, italic=True))
    for m, b, col, nm in lines:
        m, b = Fr(m), Fr(b)
        # Schnitt mit dem Rahmen
        cand = []
        for x in (lo, hi):
            y = m * x + b
            if lo <= y <= hi:
                cand.append((Fr(x), y))
        if m:
            for y in (lo, hi):
                x = (y - b) / m
                if lo <= x <= hi:
                    cand.append((x, Fr(y)))
        cand = sorted(set(cand))
        if len(cand) < 2:
            continue
        (xa, ya), (xb, yb) = cand[0], cand[-1]
        s.append(line(X(xa), Y(ya), X(xb), Y(yb), col, 3.4))
        if nm:
            # Name nahe am rechten Ende
            s.append(text(X(xb) - 14 if xb > lo + 1 else X(xb) + 14, Y(yb) + (18 if yb >= hi else -8), nm, 18, col=col, italic=True))
    for x, y, nm in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (X(x), Y(y), RED))
        if nm:
            s.append(text(X(x) + 13, Y(y) - 9, nm, 17, col=RED))
    return wrap(W, H, "".join(s), label, lg=True)
