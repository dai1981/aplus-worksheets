# -*- coding: utf-8 -*-
"""
France cycle 2 (CP・CE1, programmes 2024) の生成スクリプト共通部品。fr_common の上に:
・G(lv) → "cp"/"ce1"、GN(lv) → "CP"/"CE1"（lv = 0 は CP、1 は CE1）
・CHOSE：k_pics の絵の種類 → フランス語（単数・複数・女性名詞か）。ch(kind, n) → « 3 pommes »
・pic(svg, label, lg)：k_pics の SVG に フランス語の aria-label を付けて qfig にする
・unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort)：seo_title を自動
・各 CE1 の生成スクリプトは CP の生成スクリプトの build(1) を呼ぶ（gen_fr_maths_cp_* に build(lv)）
"""
import re
from fr_common import (mcq, num, dec, eur, hm, dur, fp, Kids, Il, mix, table, example, lesson, make_unit,  # noqa: F401
                       wrap, text, line, INK, FILL, GREEN, RED, BLUE, NB, FOIS, DIV, fr, bande, disque, droite_frac, droite, barres,
                       posee, horloge, solide_svg, lettres, blocs, numeration, argent_svg)
from ws_common import fig
import k_pics as KP

CHOSE = {"apple": ("pomme", "pommes", True), "star": ("étoile", "étoiles", True), "ball": ("ballon", "ballons", False),
         "button": ("bouton", "boutons", False), "fish": ("poisson", "poissons", False), "flower": ("fleur", "fleurs", True),
         "heart": ("cœur", "cœurs", False), "duck": ("canard", "canards", False), "cup": ("tasse", "tasses", True),
         "bug": ("coccinelle", "coccinelles", True)}
KINDS = list(CHOSE)


def G(lv):
    return ["cp", "ce1"][lv]


def GN(lv):
    return ["CP", "CE1"][lv]


def ch(kind, n):
    s, p, _ = CHOSE[kind]
    return "%d %s" % (n, s if n == 1 else p)


def nom(kind, n=2):
    s, p, _ = CHOSE[kind]
    return s if n == 1 else p


def un(kind):
    return ("une " if CHOSE[kind][2] else "un ") + CHOSE[kind][0]


def de(kind):
    """de pommes / d’étoiles"""
    p = CHOSE[kind][1]
    return ("d’" if p[0] in "aeiouéœ" else "de ") + p


def pic(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def C2(t):
    return t + " (résumé du programme 2024 du cycle 2)"


def unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    seo = "%s %s : fiches et exercices avec corrigé" % (short, GN(lv))
    make_unit(R, slug, dom, C2(std), title, seo, short, meta, key_big, key_sub, body, faq, sets, sort, grade=G(lv))


def re_mcq(it):
    """réutiliser un exercice d’un autre générateur (déjà en français)"""
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def pl(n, s, p=None):
    """pl(1, "dizaine") → 1 dizaine ; pl(3, "dizaine") → 3 dizaines（0 と 1 は単数）"""
    return "%s %s" % (num(n), s if n <= 1 else (p or s + "s"))


def le(kind):
    """le ballon / la pomme / l’étoile"""
    s, _, f = CHOSE[kind]
    return ("l’" if s[0] in "aeiouéœ" else "la " if f else "le ") + s


def que(n):
    """que Léo / qu’Ambre"""
    return ("qu’" if n[0] in "AEIOUÉaeiouéH" else "que ") + n


def de_n(n):
    """de Léo / d’Ambre"""
    return ("d’" if n[0] in "AEIOUÉaeiouéH" else "de ") + n
