# -*- coding: utf-8 -*-
"""
France cycle 3 (CM1・CM2, programmes 2025) の生成スクリプト共通部品。fr_common の上に:
・G(L) → "cm1"/"cm2"、GN(L) → "CM1"/"CM2"
・dz(n, k)：整数 n を 10^k で割った小数をコンマで（dz(2345, 2) → 23,45）。末尾の 0 は消す（keep=True で残す）
・frh(a, b)：分数の HTML、mixed(q, r, b)：帯分数ではなく「q + r/b」の和の形
・droite_dec(lo, hi, k, marks)：小数のドロワット（lo・hi は 10^k 倍した整数）
・unit(L, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort)：seo_title を自動で作る
・「各 CM2 の生成スクリプトは CM1 の生成スクリプトの build(2) を呼ぶ」形にする
"""
import math
from fr_common import (mcq, num, dec, eur, unit as funit, hm, dur, fp, Kids, Il, mix, table, example, lesson, make_unit,  # noqa: F401
                       wrap, text, line, INK, FILL, GREEN, RED, BLUE, NB, FOIS, DIV, fr, bande, disque, droite_frac, droite, barres,
                       posee, horloge, solide_svg, lettres)


def G(L):
    return "cm%d" % L


def GN(L):
    return "CM%d" % L


def dz(n, k, keep=False):
    """dz(2345, 2) → 23,45 ; dz(2300, 2) → 23 ; dz(2300, 2, keep=True) → 23,00"""
    neg = n < 0
    n = abs(int(n))
    if k == 0:
        return ("−" if neg else "") + num(n)
    ip, fpart = divmod(n, 10 ** k)
    f = str(fpart).rjust(k, "0")
    if not keep:
        f = f.rstrip("0")
    return ("−" if neg else "") + num(ip) + ("," + f if f else "")


def frh(a, b):
    return fr(a, b)


def C3(t):
    return t + " (résumé du programme 2025 du cycle 3)"


def unit(L, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    seo = "%s %s : fiches et exercices avec corrigé" % (short, GN(L))
    make_unit(R, slug, dom, C3(std), title, seo, short, meta, key_big, key_sub, body, faq, sets, sort, grade=G(L))


def droite_dec(lo, hi, step, marks=(), k=1, every=None, width=460, label="droite graduée"):
    """lo, hi, step : entiers en 10^-k ; marks : [(valeur, lettre)] ; graduations étiquetées tous les every"""
    n = (hi - lo) // step
    u = width / float(n)
    x0, y = 34, 58
    X = lambda v: x0 + (v - lo) / float(step) * u
    every = every or step * (10 if n >= 20 else 5 if n >= 10 else 1)
    s = [line(x0 - 8, y, x0 + n * u + 12, y, INK, 2), "<path d='M%.1f %.1f l-9 -6 v12 Z' fill='%s'/>" % (x0 + n * u + 20, y, INK)]
    for i in range(n + 1):
        v = lo + i * step
        big = (v - lo) % every == 0
        s.append(line(X(v), y - (10 if big else 6), X(v), y + (10 if big else 6), INK, 2 if big else 1.3))
        if big:
            s.append(text(X(v), y + 30, dz(v, k), 14, weight=600))
    for v, ch in marks:
        s.append("<path d='M%.1f %.1f l-7 -12 h14 Z' fill='%s'/>" % (X(v), y - 12, RED))
        s.append(text(X(v), y - 28, ch, 16, col=RED))
    return wrap(x0 * 2 + n * u + 4, y + 42, "".join(s), label, lg=True)


def plural(n, w, ws=None):
    return "%s %s" % (num(n), w if n == 1 else (ws or w + "s"))


def lettres_big(n):
    """jusqu’à 999 999 999 : 2 300 080 → deux millions trois cent mille quatre-vingts"""
    from fr_common import _w999
    if n == 0:
        return "zéro"
    mi, r = divmod(n, 1000000)
    th, u = divmod(r, 1000)
    s = []
    if mi:
        s.append(("un million" if mi == 1 else _w999(mi, final=True) + " millions"))
    if th:
        s.append("mille" if th == 1 else _w999(th, final=False) + " mille")
    if u:
        s.append(_w999(u))
    return " ".join(s)


RANGS = ["unités", "dizaines", "centaines", "unités de mille", "dizaines de mille", "centaines de mille",
         "unités de millions", "dizaines de millions", "centaines de millions"]
RANG1 = ["unité", "dizaine", "centaine", "millier", "dizaine de mille", "centaine de mille", "million", "dizaine de millions", "centaine de millions"]
RANGP = ["unités", "dizaines", "centaines", "milliers", "dizaines de mille", "centaines de mille", "millions", "dizaines de millions", "centaines de millions"]


def de(w):
    return ("d’" if w[0] in "aeiouéèhAEIOUÉ" else "de ") + w


def un_zero_de_moins(n):
    s = str(n)
    i = s.find("0")
    return int(s[:i] + s[i + 1:]) if i > 0 else n // 10


NOMF = {2: ("demi", "demis"), 3: ("tiers", "tiers"), 4: ("quart", "quarts")}
NUMW = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
        "dix-sept", "dix-huit", "dix-neuf", "vingt"]


def nomfrac(n, d):
    """3/4 → trois quarts ; 7/12 → sept douzièmes ; 16/31 → seize trente et unièmes"""
    if d in NOMF:
        w = NOMF[d][0 if n == 1 else 1]
    else:
        base = lettres_big(d).replace("quatre-vingts", "quatre-vingt").replace("cents", "cent")
        if base.endswith("cinq"):
            base += "u"
        elif base.endswith("neuf"):
            base = base[:-1] + "v"
        elif base.endswith("e"):
            base = base[:-1]
        if base == "un":
            base = "un"
        w = base.replace("mille", "mill") + "ième" + ("s" if n > 1 else "")
    return ("un" if n == 1 else lettres_big(n)) + " " + w
