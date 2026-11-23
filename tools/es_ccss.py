# -*- coding: utf-8 -*-
"""Matemáticas Aplicadas a las Ciencias Sociales I y II (Real Decreto 243/2022): piezas comunes sobre es_bach.
grade «1-bachillerato-ccss» / «2-bachillerato-ccss». Los generadores de Matemáticas I y II se reutilizan con use_ (otra semilla)."""
import math
from es_bach import *  # noqa
from es_bach import M, mix, sg, num, L, nf, fq, d, r2, tabla, kurve, kosy, W, MINUS, E, make_unit, mat, det_h, BLUE, RED, GREEN, NB, use_  # noqa: F401


def unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    make_unit(R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort, grade="%d-bachillerato-ccss" % lv)


def eu(x, k=2):
    """euros con separador de miles y coma: 12345.6 → 12 345,60 €; k = 0 → sin decimales"""
    m = 10 ** k
    v = int(math.floor(abs(x) * m + 0.5))
    ent, dec = divmod(v, m)
    s = num(ent) + ("," + str(dec).rjust(k, "0") if k else "")
    return (MINUS if x < 0 and v else "") + s + NB + "€"


def pc(x, k=2):
    """porcentaje: 3.5 → 3,5 %; quita ceros finales"""
    s = r2(x, k)
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s + NB + "%"


def dd(x, k=4):
    """decimal sin ceros finales: 0.2500 → 0,25"""
    s = r2(x, k)
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


Z_CRIT = {"90": 1.645, "95": 1.96, "99": 2.575}
