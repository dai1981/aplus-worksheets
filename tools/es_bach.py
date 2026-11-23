# -*- coding: utf-8 -*-
"""Bachillerato (Matemáticas I y II, Real Decreto 243/2022): piezas comunes sobre es_eso."""
import math
from fractions import Fraction as F
from es_eso import *  # noqa
from es_eso import fq, sg, d, M, mix, num, L, E, P2, poly, sol, raiz, kosy, kurve, figure, tabla, MINUS, make_unit, sup, par

BLUE, RED, GREEN = "#1565c0", "#c62828", "#2e7d32"


def unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    make_unit(R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort, grade="%d-bachillerato" % lv)


def r2(x, k=2):
    """redondeo (no al par) con coma decimal"""
    m = 10 ** k
    v = int(math.floor(abs(x) * m + 0.5))
    s = d(F(v, m))
    return (MINUS + s) if x < 0 and v else s


def nf(x):
    """Fraction/int → texto (fracción en HTML)"""
    x = F(x)
    return sg(int(x)) if x.denominator == 1 else fq(x)


def mat(rows):
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else nf(c)) for row in rows for c in row)
    return "<span class='mx m%d'>%s</span>" % (n, cells)


def det_h(rows):
    n = len(rows[0])
    cells = "".join("<span>%s</span>" % (c if isinstance(c, str) else nf(c)) for row in rows for c in row)
    return "<span class='mx det m%d'>%s</span>" % (n, cells)


def V(*cs):
    return "(%s)" % ", ".join(c if isinstance(c, str) else nf(c) for c in cs)


def pi_txt(f):
    """múltiplo de π: 3/2 → 3π/2"""
    f = F(f)
    if f == 0:
        return "0"
    s = MINUS if f < 0 else ""
    f = abs(f)
    n, dd = f.numerator, f.denominator
    t = ("" if n == 1 else str(n)) + "π"
    return s + (t if dd == 1 else t + "/" + str(dd))


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(r) for r in zip(*a)]


def W(xs):
    """quita duplicados conservando el orden"""
    out = []
    for x in xs:
        if x is not None and x not in out:
            out.append(x)
    return out
