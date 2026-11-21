# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: gemeinsame Teile（Brüche, Dezimalzahlen）
  bh(v)   Bruch als HTML (gekürzt), ganze Zahl ohne Bruch, gemischt=True → 2 ¾
  dz(v)   exakte Dezimalzahl mit Komma: 2,75 / −0,4 / 12 500,5
  fq(...) mcq mit Brüchen als Fraction-Werten (Text wird gebaut, Doppelte fallen weg)
"""
from fractions import Fraction as Fr
from de_common import mcq as _mcq, num, fr, NB

MINUS = "−"


def mcq(q, a, cands, e, neg=False):
    """wie de_common.mcq, aber None statt Fehler, wenn zu wenig Ablenker da sind (dann neuer Versuch)"""
    try:
        return _mcq(q, a, cands, e, neg=neg)
    except AssertionError:
        return None


def bh(v, gemischt=False, roh=None):
    """roh=(z, n): ungekürzt anzeigen"""
    if roh is not None:
        z, n = roh
        return (MINUS if z * n < 0 else "") + fr(abs(z), abs(n))
    v = Fr(v)
    s = MINUS if v < 0 else ""
    v = abs(v)
    if v.denominator == 1:
        return s + num(v.numerator)
    if gemischt and v > 1:
        w, r = divmod(v.numerator, v.denominator)
        return s + "%s%s%s" % (num(w), NB, fr(r, v.denominator))
    return s + fr(v.numerator, v.denominator)


def endlich(v):
    d = Fr(v).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dz(v):
    v = Fr(v)
    if not endlich(v):
        raise ValueError("nicht abbrechend: %s" % v)
    s = MINUS if v < 0 else ""
    v = abs(v)
    k = 0
    while (10 ** k) % v.denominator:
        k += 1
    n = v.numerator * 10 ** k // v.denominator
    ip, fp = divmod(n, 10 ** k)
    return s + num(ip) + ("," + str(fp).rjust(k, "0") if k else "")


def fq(q, ans, wrong, e, gemischt=False, neg=False, fmt=None):
    f = fmt or (lambda v: bh(v, gemischt))
    a = f(ans)
    ws = []
    for w in wrong:
        if w is None:
            continue
        if not isinstance(w, str):
            w = Fr(w)
            if w == Fr(ans) or (w <= 0 and not neg):
                continue
            w = f(w)
        ws.append(w)
    return mcq(q, a, ws, e, neg=neg)
