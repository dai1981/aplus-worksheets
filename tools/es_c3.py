# -*- coding: utf-8 -*-
"""España, tercer ciclo de Primaria (5.º y 6.º): partes comunes.
Todo de es_common, más:
  fq     Fraction → fracción HTML (mixto=True → número mixto)
  d      Fraction → decimal con coma exacto (ValueError si no es exacto)
  M      mcq con negativos, sin opciones repetidas por valor
  sg     número con signo «−3», «+3»
  W      quita None y repetidos
"""
from fractions import Fraction as F
from es_common import (mcq, mix, lesson, make_unit, num, dz, eur, Kids, ao, bank, fr, POR, DIV, NB, letra, letra_big,  # noqa: F401
                       recta, tira, circulo, grafico, cuerpo_svg, relabel, fig, table, keep)

MINUS = "−"


def fq(x, mixto=False):
    x = F(x)
    s = MINUS if x < 0 else ""
    x = abs(x)
    if x.denominator == 1:
        return s + num(x.numerator)
    if mixto and x > 1:
        e = x.numerator // x.denominator
        r = x - e
        return s + "%s%s%s" % (num(e), NB, fr(r.numerator, r.denominator))
    return s + fr(x.numerator, x.denominator)


def d(x, places=None):
    x = F(x)
    neg = x < 0
    x = abs(x)
    for k in range(0, 7):
        if (x * 10 ** k).denominator == 1:
            break
    else:
        raise ValueError("no exacto")
    if places is not None and k > places:
        raise ValueError("demasiadas cifras")
    n = int(x * 10 ** k)
    return (MINUS if neg else "") + dz(n, k)


def sg(x):
    return (MINUS + num(-x)) if x < 0 else num(x)


def W(xs, ok=None):
    out = []
    for x in xs:
        if x is None or x in out or x == ok:
            continue
        out.append(x)
    return out


def M(q, ok, cands, e):
    return mcq(q, ok, W(cands, ok), e, neg=True)
