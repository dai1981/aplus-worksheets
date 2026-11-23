# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio (1ª a 3ª série): partes comuns.
Tudo de br_9 (d, fq, expr, P2, par, sq, M, kosy, tab, ntab, bank, figure, formas, tri_pts, _svg, _t, _ln) e de br_common
(mix, lesson, use, num, reais, Kids), mais:
  curva   gráfico de funções (de_k10.kurve) com números brasileiros
  R2      Fraction → «R$ 1.234,56»
  pc      Fraction → «12,5%»
  sg      número com sinal para somar: «+ 3», «− 3»
  unit    make_unit com grade (1-serie, 2-serie, 3-serie)
"""
import re
from fractions import Fraction as F
from br_9 import (M, d, fq, expr, P2, par, sq, kosy, tab, ntab, bank, figure, formas, tri_pts, circulo,  # noqa: F401
                  _svg, _t, _ln, _arc, INK, BLUE, RED, GRN, make_unit, NB, MINUS)
from br_common import mix, lesson, use, num, reais, Kids, o, do, keep  # noqa: F401
import de_k10

COLS = ["#1f5fbf", "#c0392b", "#2e7d32", "#8e44ad"]


def _txt(t):
    t = re.sub("(\\d)[\u00a0\u202f ](\\d{3})(?!\\d)", r"\1\2", t)
    return re.sub(r"(?<![\d,.])(\d{4,})(?!\d)", lambda m: num(int(m.group(1))), t)


def _br(svg):
    """só nos textos (entre > e <): «1 000» e «1000» → «1.000»"""
    return re.sub(r">([^<]*)<", lambda m: ">" + _txt(m.group(1)) + "<", svg)


def curva(fs, xr, yr, pts=(), label="gráfico", xlab=None, W=330, H=250):
    """fs = [(f, nome)] ou [(f, cor, nome)]; xr, yr = (início, fim, passo)"""
    ff = []
    for i, t in enumerate(fs):
        if len(t) == 2:
            ff.append((t[0], COLS[i % len(COLS)], t[1]))
        else:
            ff.append(t)
    return _br(de_k10.kurve(ff, xr, yr, pts=pts, W=W, H=H, label=label, xlab=xlab))


def R2(x):
    """valor em reais (Fraction) → «R$ 1.234,56»"""
    x = F(x)
    neg = x < 0
    s = "R$" + NB + d(abs(x), 2, keep=True)
    return (MINUS if neg else "") + s


def pc(x, places=None):
    """Fraction (já em %) → «12,5%»"""
    return d(x, places) + "%"


def sg(x):
    """« + 3» / « − 3» para escrever depois de outro termo"""
    x = F(x)
    return (" %s %s" % (MINUS, d(-x))) if x < 0 else (" + %s" % d(x))


def unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort, grade):
    make_unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort, grade=grade)
