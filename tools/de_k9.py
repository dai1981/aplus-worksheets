# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: gemeinsame Teile
  qf(a, b, c)         quadratischer Term: x² − 4x + 3, −2x² + 1
  sform(a, d, e)      Scheitelpunktform: y = 2(x − 3)² + 1
  zr(v, k=1)          gerundete Dezimalzahl mit Komma, immer k Nachkommastellen (12,0)
  parabel(...)        Koordinatensystem mit Parabeln (SVG, lg)
  rdreieck(...)       rechtwinkliges Dreieck mit Beschriftung (SVG, lg)
"""
import math
from fractions import Fraction as Fr
from de_common import wrap, line, text, INK, BLUE, RED, GREEN, FILL, MAL, NB
from de_k6 import bh, dz
from de_k8 import mcq, expr, gl, par, kosy, eur, GRID  # noqa: F401

MINUS = "−"


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def zr(v, k=1):
    v = float(v)
    n = int(abs(v) * 10 ** k + 0.5)
    ip, fp = divmod(n, 10 ** k)
    s = dz(ip) + ("," + str(fp).rjust(k, "0") if k else "")
    return (MINUS + s) if v < 0 and n else s


def qf(a, b, c, v="x"):
    return expr([(a, v + "²"), (b, v), (c, "")])


def sform(a, d, e, y="y"):
    """y = a(x − d)² + e"""
    a, d, e = Fr(a), Fr(d), Fr(e)
    if d == 0:
        inner = "x²"
    else:
        inner = "(x%s%s%s%s)²" % (NB, "−" if d > 0 else "+", NB, zahl(abs(d)))
    pre = "" if a == 1 else (MINUS if a == -1 else (zahl(a) if a.denominator == 1 else (MINUS if a < 0 else "") + bh(abs(a))))
    rest = "" if e == 0 else (" + %s" % zahl(e) if e > 0 else " − %s" % zahl(-e))
    return "%s = %s%s%s" % (y, pre, inner, rest)


def parabel(curves=(), pts=(), lo=-5, hi=5, u=24, label="Parabel im Koordinatensystem"):
    """curves: [(a, d, e, farbe, name)] für y = a(x − d)² + e"""
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
    for a, d, e, col, nm in curves:
        a, d, e = float(a), float(d), float(e)
        pts_ = []
        seg = []
        steps = 200
        for k in range(steps + 1):
            x = lo + (hi - lo) * k / steps
            y = a * (x - d) ** 2 + e
            if lo - 0.01 <= y <= hi + 0.01:
                seg.append("%.1f,%.1f" % (X(x), Y(y)))
            else:
                if len(seg) > 1:
                    pts_.append(seg)
                seg = []
        if len(seg) > 1:
            pts_.append(seg)
        for sg in pts_:
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3.2'/>" % (" ".join(sg), col))
        if nm:
            s.append(text(X(d) + 16, Y(e) + (22 if a > 0 else -12), nm, 17, col=col, italic=True))
    for x, y, nm in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='6' fill='%s'/>" % (X(x), Y(y), RED))
        if nm:
            s.append(text(X(x) + 13, Y(y) - 9, nm, 17, col=RED))
    return wrap(W, H, "".join(s), label, lg=True)


def rdreieck(lab_a, lab_b, lab_c, ang=None, ang_txt="", w=4, h=3, names=("A", "B", "C"), label="rechtwinkliges Dreieck"):
    """rechter Winkel bei C (unten links). a = senkrechte Kathete (BC), b = waagrechte Kathete (AC), c = Hypotenuse.
    A rechts unten, B oben links. ang: 'A' oder 'B' für einen markierten Winkel."""
    sc = min(220.0 / w, 120.0 / h)
    W, H = w * sc + 180, h * sc + 60
    C = (120, 20 + h * sc)
    A = (120 + w * sc, 20 + h * sc)
    B = (120, 20)
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.6'/>" % (A + B + C + (FILL, GREEN))]
    q = 14
    s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.8'/>" % (C[0] + q, C[1], C[0] + q, C[1] - q, C[0], C[1] - q, INK))
    s.append(text(A[0] + 12, A[1] + 18, names[0], 17) + text(B[0] - 4, B[1] - 4, names[1], 17, anchor="end") + text(C[0] - 12, C[1] + 18, names[2], 17))
    if lab_b:
        s.append(text((A[0] + C[0]) / 2, C[1] + 26, lab_b, 17, col=BLUE))
    if lab_a:
        s.append(text(C[0] - 10, (B[1] + C[1]) / 2 + 6, lab_a, 17, col=BLUE, anchor="end"))
    if lab_c:
        s.append(text((A[0] + B[0]) / 2 + 14, (A[1] + B[1]) / 2 - 8, lab_c, 17, col=BLUE, anchor="start"))
    if ang == "A":
        s.append(text(A[0] - 44, A[1] - 8, ang_txt, 16, col=RED))
    elif ang == "B":
        s.append(text(B[0] + 16, B[1] + 44, ang_txt, 16, col=RED, anchor="start"))
    return wrap(W, H, "".join(s), label, lg=True)
