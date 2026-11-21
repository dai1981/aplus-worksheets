# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: gemeinsame Teile
  kurve(fs, xr, yr, ...)  Graphen beliebiger Funktionen im Koordinatensystem (SVG, lg)
                          fs: [(f, farbe, name)], xr = (lo, hi, schritt, beschriftung), yr ebenso
  pi_lab(k)               Beschriftung k · π/2 → „π“, „3π/2“, „2π“
"""
import math
from fractions import Fraction as Fr
from de_common import wrap, line, text, INK, BLUE, RED, GREEN, MAL, NB
from de_k6 import bh, dz
from de_k9 import mcq, zahl, zr, qf, par, eur, expr  # noqa: F401
from de_k8 import GRID

MINUS = "−"


def pi_txt(v):
    """v = Vielfaches von π als Fraction → Text"""
    v = Fr(v)
    if v == 0:
        return "0"
    s = MINUS if v < 0 else ""
    v = abs(v)
    n, d = v.numerator, v.denominator
    z = ("" if n == 1 else str(n)) + "π"
    return s + (z if d == 1 else "%s/%d" % (z, d))


def kurve(fs, xr, yr, pts=(), W=330, H=250, label="Graph", xlab=None):
    xlo, xhi, xs = xr
    ylo, yhi, ys = yr
    m = 34
    X = lambda x: m + (float(x) - xlo) / (xhi - xlo) * (W - 2 * m)
    Y = lambda y: H - m + 6 - (float(y) - ylo) / (yhi - ylo) * (H - 2 * m)
    s = []
    k = xlo
    i = 0
    while k <= xhi + 1e-9:
        s.append(line(X(k), Y(ylo), X(k), Y(yhi), GRID, 1))
        if abs(k) > 1e-9:
            lab = xlab(k) if xlab else dz(Fr(k).limit_denominator(100))
            s.append(text(X(k), Y(0) + 20 if ylo < 0 <= yhi else Y(ylo) + 20, lab, 15, weight=600))
        k += xs
    k = ylo
    while k <= yhi + 1e-9:
        s.append(line(X(xlo), Y(k), X(xhi), Y(k), GRID, 1))
        if abs(k) > 1e-9:
            s.append(text((X(0) if xlo <= 0 <= xhi else X(xlo)) - 8, Y(k) + 5, dz(Fr(k).limit_denominator(100)), 15, anchor="end", weight=600))
        k += ys
    if ylo <= 0 <= yhi:
        s.append(line(X(xlo), Y(0), X(xhi) + 8, Y(0), INK, 2.2) + text(X(xhi) + 6, Y(0) - 8, "x", 17, italic=True))
    if xlo <= 0 <= xhi:
        s.append(line(X(0), Y(ylo), X(0), Y(yhi) - 8, INK, 2.2) + text(X(0) + 12, Y(yhi) - 4, "y", 17, italic=True))
    for f, col, nm in fs:
        seg, segs = [], []
        N = 300
        for j in range(N + 1):
            x = xlo + (xhi - xlo) * j / N
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError, OverflowError):
                y = None
            if y is not None and ylo - 0.05 <= y <= yhi + 0.05:
                seg.append("%.1f,%.1f" % (X(x), Y(y)))
            else:
                if len(seg) > 1:
                    segs.append(seg)
                seg = []
        if len(seg) > 1:
            segs.append(seg)
        for sg in segs:
            s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join(sg), col))
        if nm and segs:
            lx, ly = segs[-1][-1].split(",")
            s.append(text(float(lx) - 6, float(ly) - 8, nm, 16, col=col, italic=True, anchor="end"))
    for x, y, nm in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s'/>" % (X(x), Y(y), RED))
        if nm:
            s.append(text(X(x) + 12, Y(y) - 8, nm, 16, col=RED))
    return wrap(W, H, "".join(s), label, lg=True)
