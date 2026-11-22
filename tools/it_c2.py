# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: disegni comuni (k_pics e de_k2 con etichette in italiano).
・COSE: nome singolare/plurale e genere degli oggetti di k_pics
・cose(kind, n) → «3 mele», un_(kind) → «una mela»
・it(svg, label, lg) : cambia l’aria-label
・riga(n, kind), gruppi(g, k, kind), tabella100(n), punti(r, c), retta100(lo, hi, marks)
"""
import re
import de_k2
import k_pics
from ws_common import fig, svg_wrap

COSE = {"apple": ("mela", "mele", "f"), "star": ("stella", "stelle", "f"), "ball": ("palla", "palle", "f"), "button": ("bottone", "bottoni", "m"),
        "fish": ("pesce", "pesci", "m"), "flower": ("fiore", "fiori", "m"), "heart": ("cuore", "cuori", "m"), "duck": ("papera", "papere", "f"),
        "cup": ("tazza", "tazze", "f"), "bug": ("coccinella", "coccinelle", "f")}
KINDS = list(COSE)


def cose(kind, n):
    s, p, _ = COSE[kind]
    return "%d %s" % (n, s if n == 1 else p)


def nome(kind, n=2):
    s, p, _ = COSE[kind]
    return s if n == 1 else p


def un_(kind):
    s, _, g = COSE[kind]
    return ("una " if g == "f" else "un ") + s


def quanti(kind):
    return "Quante" if COSE[kind][2] == "f" else "Quanti"


def it(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)
    if lg and "data-pf" not in svg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return svg if svg.startswith("<div") else fig(svg)


def riga(n, kind, per_row=10):
    return it(de_k2.reihe(n, kind, per_row), cose(kind, n))


def gruppi(g, k, kind):
    return it(de_k2.gruppen(g, k, kind), "%d gruppi, in ogni gruppo %s" % (g, cose(kind, k)))


def tabella100(n):
    return it(de_k2.hunderterfeld(n), "tabella del 100 con %d pallini colorati" % n)


def punti(rows, cols):
    return it(de_k2.punktfeld(rows, cols), "%d righe con %d pallini ciascuna" % (rows, cols))


def retta100(lo, hi, marks, step=1, every=10, width=440):
    return it(de_k2.zahlenstrahl100(lo, hi, marks, step, every, width), "retta dei numeri da %d a %d" % (lo, hi), lg=True)


def mucchio(n, kind, seed):
    return it(fig(k_pics.scatter_svg(n, kind, seed)), cose(kind, n))
