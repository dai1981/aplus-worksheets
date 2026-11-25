# -*- coding: utf-8 -*-
"""Sverige årskurs 4–6: gemensamma delar för se_m_*.py（単元関数は lv = 4, 5, 6 を受け取る）。"""
import math
import re
from fractions import Fraction as F
import se_common as C
from se_common import (num, kr, NB, Kids, hon, Hon, wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE)  # noqa: F401

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    R.shuffle(xs)
    return xs


def cap(s):
    return s[0].upper() + s[1:]


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def fq(x, mixed=False):
    """Fraction → HTML（heltal som tal, mixed=True → blandad form 2 3/4）"""
    x = F(x)
    if x.denominator == 1:
        return sn(x.numerator)
    if mixed and abs(x) > 1:
        w = int(abs(x)) * (1 if x > 0 else -1)
        r = abs(x - w)
        return ("−" if x < 0 else "") + num(abs(w)) + fr(r.numerator, r.denominator)
    return ("−" if x < 0 else "") + fr(abs(x.numerator), x.denominator)


def sn(n):
    """heltal med minustecken −"""
    return num(n)


def d(x, places=None):
    """Fraction/int → decimaltal med komma: 2,35 / 1 250,5（måste gå jämnt ut）"""
    x = F(x)
    neg = x < 0
    x = abs(x)
    k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1
        if k > 6:
            raise ValueError("inte ändligt decimaltal")
    if places is not None:
        if k > places:
            raise ValueError("för många decimaler")
        k = places
    n = int(x * 10 ** k)
    ip, fp = divmod(n, 10 ** k)
    s = num(ip) + ("," + str(fp).rjust(k, "0") if k else "")
    return ("−" if neg and n else "") + s


_FR = re.compile(r"^(\d*)<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")


def fval(s):
    m = _FR.match(s)
    if not m:
        return None
    return int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3)))


def M(q, correct, cands, e, fill=False):
    """4 alternativ; negativa tal är tillåtna. Räcker inte felsvaren → None (görs om).
    Ett bråk med samma värde som svaret (5/10 och 1/2) räknas inte som felsvar."""
    correct = str(correct)
    seen = {correct}
    cv = fval(correct)
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "":
            continue
        if cv is not None and fval(c) == cv:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        if fill:
            return C.mcq(q, correct, pick, e)
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def unit(slug, dom, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, dom=dom, title=title, short=short, std=std, meta=meta, kb=kb, ks=ks,
                sets=sets, think=think, ex=ex, mist=mist, faq=faq)


def tab(head, rows):
    return ("<table class='sn-table' style='width:auto'><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head), "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)))


PLATS = ["ental", "tiotal", "hundratal", "tusental", "tiotusental", "hundratusental", "miljontal"]
DEC = ["tiondelar", "hundradelar", "tusendelar"]
MAXN = {4: 99999, 5: 999999, 6: 9999999}
