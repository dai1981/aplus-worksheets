# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: gemeinsame Teile
  mcq   wie de_k6.mcq, negative Zahlen erlaubt
  eur   Geldbetrag 12,50 € (kaufmännisch gerundet)
  pz    Prozent mit Leerzeichen: 12,5 %
  rd    kaufmännisch runden auf k Stellen (als Fraction)
"""
from fractions import Fraction as Fr
from de_common import NB
from de_k6 import bh, dz, endlich, mcq as _mcq

P = NB + "%"


def mcq(q, a, cands, e):
    return _mcq(q, a, cands, e, neg=True)


def rd(v, k=2):
    v = Fr(v)
    f = 10 ** k
    s = -1 if v < 0 else 1
    return s * Fr(int(abs(v) * f + Fr(1, 2)), f)


def eur(v):
    v = rd(v, 2)
    c = int(abs(v) * 100)
    if c % 100 == 0:
        return ("−" if v < 0 else "") + dz(c // 100) + NB + "€"
    return ("−" if v < 0 else "") + "%s,%02d" % (dz(c // 100), c % 100) + NB + "€"


def pz(v):
    return dz(Fr(v)) + P


def zk(v, k=2):
    """gerundete Dezimalzahl mit Komma"""
    return dz(rd(v, k))
