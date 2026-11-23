# -*- coding: utf-8 -*-
"""
Italia Matematica, liceo (Indicazioni nazionali per i licei, DM 211/2010, liceo scientifico): parti comuni.
Sopra it_media (M, W, d, dk, fq, sgn, par, expr, L, figure, kosy, kurve) e it_m3 (P, show, mul, add, evalp, mono).
・grade: prima-liceo … quinta-liceo; dom: A Aritmetica e algebra, G Geometria, F Relazioni e funzioni, Q Dati e previsioni
・nz(R, lo, hi) intero non nullo; sq(n) → 2√3; pit / pif (multipli di π); FR(n, d) frazione HTML; trig_val(t, fn)
・P2(a, b, c) → 2x² − 3x + 5; poly([a_n, …, a_0]) → polinomio in x
・vtab (tabella di variazione), arbre (diagramma ad albero), code (Python) con etichette italiane
・ex(x) → «x = 3»; sol([..]) → «x = −2 ∨ x = 3»
"""
import math
import re
from fractions import Fraction as Fr
from it_media import M, L, mix, table, W, d, dk, fq, sgn, par, expr, val, Kids, NB, fr, figure, kosy, kurve, relabel, num  # noqa: F401
from it_m3 import P, show, mul, add, evalp, mono, sup, deg  # noqa: F401
import it_common
import it_media
import fr_ly1

MINUS = "−"
it_common.UPDATED = "2026-11-23"
it_common.GRADE_NAME.update({"prima-liceo": "Prima liceo", "seconda-liceo": "Seconda liceo", "terza-liceo": "Terza liceo",
                             "quarta-liceo": "Quarta liceo", "quinta-liceo": "Quinta liceo"})
it_common.DOMAIN.update({"A": "Aritmetica e algebra", "G": "Geometria", "F": "Relazioni e funzioni", "Q": "Dati e previsioni"})

sq = fr_ly1.sq
pit = fr_ly1.pit
pif = fr_ly1.pif
FR = fr_ly1.FR
trig_val = fr_ly1.trig_val


def nz(R, lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def P2(a, b, c, v="x"):
    return expr([(a, v + "²"), (b, v), (c, "")])


def poly(cs, v="x"):
    """[a_n, …, a_0] → polinomio"""
    n = len(cs) - 1
    t = []
    for i, c in enumerate(cs):
        e = n - i
        t.append((c, v + sup(e) if e >= 1 else ""))
    return expr(t)


def ex(x, v="x"):
    return "%s = %s" % (v, fq(x))


def sol(xs, v="x"):
    xs = sorted(set(Fr(x) for x in xs))
    return " ∨ ".join("%s = %s" % (v, fq(x)) for x in xs)


def unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    it_media.unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort)


def vtab(xs, ys, dsig=None, fname="f"):
    return relabel(fr_ly1.vtab(xs, ys, dsig, fname), "tabella di variazione")


def albero(pa, pba, pbna, A="A", B="B", fmt=None):
    return relabel(fr_ly1.arbre(pa, pba, pbna, A, B, fmt or fq), "diagramma ad albero")


code = fr_ly1.code


def uniq(seq):
    out = []
    for x in seq:
        if x is not None and x not in out:
            out.append(x)
    return out


def isq(n):
    r = math.isqrt(n)
    return r if r * r == n else None


def surd(a, b, c=1):
    """(a + b√c) testo, c senza fattori quadrati"""
    if b == 0 or c == 1:
        return fq(Fr(a) + Fr(b) * (1 if c == 1 else 0))
    rb = ("" if abs(b) == 1 else fq(abs(b))) + "√%d" % c
    if a == 0:
        return (MINUS if b < 0 else "") + rb
    return "%s %s %s" % (fq(a), "+" if b > 0 else MINUS, rb)


def simp_root(n):
    """n = k²·m → (k, m)"""
    k, m = 1, n
    for p in range(2, int(math.isqrt(n)) + 1):
        while m % (p * p) == 0:
            m //= p * p
            k *= p
    return k, m


def strip(t):
    return re.sub(r"<[^>]+>", "", t)


def show(p, main="x"):
    """polinomio ordinato: grado decrescente, poi la lettera principale (x, altrimenti la prima in ordine alfabetico) con esponente decrescente"""
    if not p:
        return "0"
    vs = sorted(set(v for k in p for v, _ in k))
    if main in vs:
        vs.remove(main)
        vs.insert(0, main)
    ks = sorted(p, key=lambda k: (-deg(k), [-dict(k).get(v, 0) for v in vs]))
    s = ""
    for k in ks:
        s += mono(p[k], dict(k), s == "")
    return s
