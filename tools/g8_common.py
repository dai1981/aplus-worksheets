# -*- coding: utf-8 -*-
"""Shared helpers for the US Grade 8 generators (gen_us_math_g8_*.py)."""
from fractions import Fraction as F
from ws_common import num, par, svg_wrap, text, line, INK, RED, BLUE, GREEN, GRAY, MINUS, X

PURPLE = "#7d3c98"


def term(a, var=X, st="d"):
    """a·x with 1 and −1 written as x and −x (no leading sign handling for 0)."""
    a = F(a)
    if a == 1:
        return var
    if a == -1:
        return MINUS + var
    return num(a, st) + var


def lin(a, b, var=X, st="d"):
    """a x + b written nicely: 3x − 4, −x + 2, 5, x."""
    a, b = F(a), F(b)
    if a == 0:
        return num(b, st)
    s = term(a, var, st)
    if b > 0:
        s += " + " + num(b, st)
    elif b < 0:
        s += " − " + num(-b, st)
    return s


def plus(b, st="d"):
    b = F(b)
    return (" + " + num(b, st)) if b >= 0 else (" − " + num(-b, st))


def grid_svg(lo=-6, hi=6, points=(), lines=(), segs=(), polys=(), unit=24, label="coordinate plane",
             ylo=None, yhi=None, tick_every=1, axis_names=("x", "y")):
    """A coordinate plane. points: (x, y, label, colour); lines: (m, b, colour) or ('v', x, colour);
    segs: (x1, y1, x2, y2, colour); polys: ([(x, y)...], fill, stroke)."""
    ylo = lo if ylo is None else ylo
    yhi = hi if yhi is None else yhi
    m = 22
    W = (hi - lo) * unit + 2 * m
    H = (yhi - ylo) * unit + 2 * m
    X_ = lambda x: m + (x - lo) * unit
    Y_ = lambda y: m + (yhi - y) * unit
    s = []
    for v in range(lo, hi + 1):
        s.append(line(X_(v), Y_(ylo), X_(v), Y_(yhi), "#dddddd", 1))
    for v in range(ylo, yhi + 1):
        s.append(line(X_(lo), Y_(v), X_(hi), Y_(v), "#dddddd", 1))
    if lo <= 0 <= hi:
        s.append(line(X_(0), Y_(ylo), X_(0), Y_(yhi), INK, 1.8))
    if ylo <= 0 <= yhi:
        s.append(line(X_(lo), Y_(0), X_(hi), Y_(0), INK, 1.8))
    for v in range(lo, hi + 1):
        if v != 0 and v % tick_every == 0 and ylo <= 0 <= yhi:
            s.append(text(X_(v), Y_(0) + 14, num(v), 10, weight=400))
    for v in range(ylo, yhi + 1):
        if v != 0 and v % tick_every == 0 and lo <= 0 <= hi:
            s.append(text(X_(0) - 5, Y_(v) + 4, num(v), 10, anchor="end", weight=400))
    if ylo <= 0 <= yhi:
        s.append(text(X_(hi) - 4, Y_(0) - 6, "<tspan font-style='italic'>%s</tspan>" % axis_names[0], 13))
    if lo <= 0 <= hi:
        s.append(text(X_(0) + 8, Y_(yhi) + 12, "<tspan font-style='italic'>%s</tspan>" % axis_names[1], 13, anchor="start"))
    for pts, fill, stroke in polys:
        s.append("<polygon points='%s' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2.2'/>"
                 % (" ".join("%.1f,%.1f" % (X_(x), Y_(y)) for x, y in pts), fill, stroke))
    for ln in lines:
        if ln[0] == "v":
            s.append(line(X_(ln[1]), Y_(ylo), X_(ln[1]), Y_(yhi), ln[2], 2.5))
            continue
        mm, b, col = ln
        mm, b = F(mm), F(b)
        # clip to the box
        cand = []
        for x in (lo, hi):
            y = mm * x + b
            if ylo <= y <= yhi:
                cand.append((F(x), y))
        if mm != 0:
            for y in (ylo, yhi):
                x = (y - b) / mm
                if lo <= x <= hi:
                    cand.append((x, F(y)))
        cand = sorted(set(cand))
        if len(cand) >= 2:
            (x1, y1), (x2, y2) = cand[0], cand[-1]
            s.append(line(X_(x1), Y_(y1), X_(x2), Y_(y2), col, 2.5))
    for x1, y1, x2, y2, col in segs:
        s.append(line(X_(x1), Y_(y1), X_(x2), Y_(y2), col, 2.5))
    for x, y, lab, col in points:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X_(x), Y_(y), col))
        if lab:
            s.append(text(X_(x) + 7, Y_(y) - 7, lab, 13, anchor="start", col=col))
    return svg_wrap(int(W), int(H), "".join(s), label)


def xy_table(xs, ys, xname="x", yname="y"):
    """A small horizontal input-output table (HTML)."""
    h = "<tr><th><i>%s</i></th>%s</tr>" % (xname, "".join("<td>%s</td>" % x for x in xs))
    b = "<tr><th><i>%s</i></th>%s</tr>" % (yname, "".join("<td>%s</td>" % y for y in ys))
    return "<div class='sn-tw'><table class='sn-table'><tbody>%s%s</tbody></table></div>" % (h, b)
