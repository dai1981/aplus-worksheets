# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: disegni comuni (k_pics con etichette in italiano) e piccoli aiuti.
・I nomi degli oggetti vengono da it_c2.COSE (singolare/plurale/genere)
・dieci(n): schema del dieci (1 o 2 telai); dado(vals); due(a, ka, b, kb, segno); barrati(n, kind, k);
  scatola(n, kind); salti(start, hops, lo, hi); coppia(tutto, a, b); regoli(d, u); carte(items); retta(lo, hi, marks)
・Le parole: num_parola(n) (0–20), Q(kind) «Quante mele», un_(kind)
"""
import k_pics
import f_common
from it_c2 import COSE, KINDS, cose, nome, un_, quanti, it, riga, mucchio  # noqa: F401
from it_common import lettere

PAROLE = [lettere(n) for n in range(0, 21)]


def num_parola(n):
    return PAROLE[n]


def Q(kind):
    return "%s %s" % (quanti(kind), nome(kind))


def dieci(n, frames=None, kind="dot"):
    return it(k_pics.tenframe_svg(n, frames, kind), "schema del dieci con %d pallini" % n)


def dado(vals):
    return it(k_pics.dice_svg(vals), "dadi: " + ", ".join(str(v) for v in vals))


def due(a, ka, b, kb=None, segno="e"):
    kb = kb or ka
    return it(k_pics.two_groups_svg(a, ka, b, kb, segno), "%s %s %s" % (cose(ka, a), segno, cose(kb, b)))


def barrati(n, kind, k):
    return it(k_pics.crossed_row_svg(n, kind, k), "%s, %d barrat%s" % (cose(kind, n), k, "e" if COSE[kind][2] == "f" else "i"))


def scatola(n, kind):
    return it(k_pics.box_svg(n, kind), "%s e una scatola chiusa" % cose(kind, n))


def salti(start, hops, lo=0, hi=10):
    return it(k_pics.hop_line_svg(start, hops, lo, hi, sp=40 if hi - lo <= 12 else 30), "retta dei numeri da %d a %d con i salti" % (lo, hi), lg=True)


def coppia(tutto, a, b):
    return it(k_pics.bond_svg(tutto, a, b), "il numero %s diviso in due parti" % tutto)


def regoli(d, u):
    return it(k_pics.rods_svg(d, u), "%d decin%s e %d unità" % (d, "a" if d == 1 else "e", u))


def carte(items):
    return it(k_pics.cards_svg(items), "cartellini con i numeri")


def retta(lo, hi, marks=None):
    return it(k_pics.number_line_svg(lo, hi, marks, sp=40 if hi - lo <= 12 else 28), "retta dei numeri da %d a %d" % (lo, hi), lg=True)


def piatto(n, kind):
    return it(k_pics.plate_svg(n, kind), "un piatto con %s" % (cose(kind, n) if n else "niente"))


def fila(kinds):
    return it(k_pics.kinds_row_svg(kinds), "oggetti in fila")


def ritmo(items, blanks=0):
    return it(f_common.pattern_svg(items, blanks), "un ritmo")
