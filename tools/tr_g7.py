# -*- coding: utf-8 -*-
"""Türkiye 7.〜8. sınıf の共通部品：işaretli sayılar（−）、kesir、ondalık、ifade。tr_g の上に。"""
from fractions import Fraction as F
import tr_g as G
from tr_g import num, fr, NB

MINUS = "−"


def sn(x):
    """int / Fraction → '−3', '−3/4'（HTML kesir）"""
    x = F(x)
    s = MINUS if x < 0 else ""
    a = abs(x)
    if a.denominator == 1:
        return s + num(a.numerator)
    return s + fr(a.numerator, a.denominator)


def par(x):
    """negatifse parantez: (−3)"""
    return "(" + sn(x) + ")" if F(x) < 0 else sn(x)


def dq(x, k=None):
    """ondalık (işaretli): −2,5"""
    x = F(x)
    s = MINUS if x < 0 else ""
    v = float(abs(x))
    if k is None:
        t = ("%.4f" % v).rstrip("0").rstrip(".")
    else:
        t = ("%." + str(k) + "f") % v
    ip, _, fp = t.partition(".")
    return s + num(int(ip)) + ("," + fp if fp else "")


def dpar(x, k=None):
    return "(" + dq(x, k) + ")" if F(x) < 0 else dq(x, k)


def is_fin(x):
    """sonlu ondalık mı"""
    d = F(x).denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def ondalik(x):
    """Fraction → '0,25' ya da devirli '0,<ov>3</ov>'（işaretli）"""
    x = F(x)
    s = MINUS if x < 0 else ""
    a, b = abs(x.numerator), x.denominator
    q, r = divmod(a, b)
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // b))
        r %= b
    if not r:
        return s + num(q) + ("," + "".join(digits) if digits else "")
    i = seen[r]
    return s + num(q) + "," + "".join(digits[:i]) + "<span class='ov'>%s</span>" % "".join(digits[i:])


def lin(a, v, b=0):
    """a·v + b → '3x + 5', '−x − 2', 'x'"""
    if a == 0:
        return sn(b)
    t = (v if a == 1 else MINUS + v if a == -1 else sn(a) + v)
    if b > 0:
        t += " + " + sn(b)
    elif b < 0:
        t += " " + MINUS + " " + sn(-b)
    return t


def terms(cs):
    """[(katsayı, 'x'), (k, '')] → '3x − 2y + 5'"""
    out = ""
    for c, v in cs:
        if c == 0:
            continue
        a = abs(F(c))
        body = (v if a == 1 and v else sn(a) + v)
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" " + MINUS + " " if c < 0 else " + ") + body
    return out or "0"


def fig(svg, lab="şekil"):
    return "<div class='qfig'>" + G.lg(svg) + "</div>"


def gen(w):
    """iyelik (tamlayan) eki: Elif’in, Can’ın, Duru’nun, Ömer’in"""
    vs = [c for c in w.lower() if c in "aıoueiöü"]
    v = vs[-1] if vs else "e"
    s = {"a": "ın", "ı": "ın", "o": "un", "u": "un", "e": "in", "i": "in", "ö": "ün", "ü": "ün"}[v]
    if w[-1].lower() in "aıoueiöü":
        s = "n" + s
    return w + "’" + s
