# -*- coding: utf-8 -*-
"""
Italia Matematica, scuola secondaria di primo grado (prima, seconda, terza media): parti comuni.
・d(x): Fraction/int/float → numero con la virgola (2,5), num() all’italiana (4 cifre senza spazio, 12 000); ValueError se non è decimale
・fq(x): Fraction → HTML (frazione o intero), negativi con «−»; par(x): (−3) se negativo
・expr([(coeff, "x"), …]) → 3x − 5 ; mono(k, "a²b")
・M(q, a, w, e): mcq con negativi, toglie i distrattori con lo stesso valore della risposta
・unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort)
・L(think, ex, mist): lezione (Come si fa → Esempio → Errori frequenti)
・figure(...) (fr_c4), kosy(...) (de_k8, piano cartesiano), kurve(...) (de_k10)
・dom: N Numeri, S Spazio e figure, F Relazioni e funzioni, D Dati e previsioni, P Problemi
"""
import os
import re
from fractions import Fraction as Fr
from it_common import mcq, num, lesson, make_unit, mix, table, example, Kids, fr, NB, FOIS, DIV, eur, relabel  # noqa: F401
import it_common
import fr_c4
import de_k8
import de_k10

MINUS = "−"
it_common.GRADE_NAME.update({"prima-media": "Prima media", "seconda-media": "Seconda media", "terza-media": "Terza media"})
it_common.DOMAIN.update({"F": "Relazioni e funzioni", "Q": "Dati e previsioni"})


def d(x):
    x = Fr(x).limit_denominator(10 ** 6) if isinstance(x, float) else Fr(x)
    t = x.denominator
    for p in (2, 5):
        while t % p == 0:
            t //= p
    if t != 1:
        raise ValueError("non decimale")
    k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1
    n = int(abs(x) * 10 ** k)
    ip, fp_ = divmod(n, 10 ** k)
    return (MINUS if x < 0 else "") + num(ip) + ("," + str(fp_).rjust(k, "0") if k else "")


def dk(x, k):
    x = Fr(x)
    n = int(abs(x) * 10 ** k + Fr(1, 2))
    ip, fp_ = divmod(n, 10 ** k)
    return (MINUS if x < 0 else "") + num(ip) + ("," + str(fp_).rjust(k, "0") if k else "")


def fq(x):
    x = Fr(x)
    if x.denominator == 1:
        return d(x)
    a = abs(x)
    return (MINUS if x < 0 else "") + fr(a.numerator, a.denominator)


def par(x):
    return "(%s)" % fq(x) if Fr(x) < 0 else fq(x)


def sgn(x):
    """+3 / −3 (numeri relativi con il segno)"""
    x = Fr(x)
    return ("+" if x > 0 else "") + fq(x)


def coef(k, var, first):
    k = Fr(k)
    a = abs(k)
    body = ("" if (a == 1 and var) else fq(a)) + var
    if first:
        return (MINUS if k < 0 else "") + body
    return " %s %s" % (MINUS if k < 0 else "+", body)


def expr(terms):
    out = ""
    for k, v in terms:
        if Fr(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def val(t):
    t = re.sub(r"<span class='fn'>([^<]*)</span><span class='fd'>([^<]*)</span>", r"\1/\2", str(t))
    t = re.sub(r"<[^>]+>", "", t).replace(NB, "").replace(" ", "").replace(MINUS, "-")
    m = re.match(r"^([-+]?)(\d+(?:,\d+)?)(?:/(\d+))?([a-zA-Z€%²³°]*)$", t)
    if not m:
        return None
    v = Fr(m.group(2).replace(",", "."))
    if m.group(3):
        v /= int(m.group(3))
    return (-v if m.group(1) == "-" else v, m.group(4))


def M(q, a, w, e):
    va = val(a)
    ws = []
    for x in w:
        if x is None or str(x) == str(a) or str(x) in ws or (va is not None and val(x) == va):
            continue
        ws.append(str(x))
    if len(ws) < 3 and os.environ.get("IT_WARN"):
        print("FILL:", re.sub(r"<[^>]+>", " ", q)[-90:], "|", a)
    return mcq(q, a, ws, e, neg=True)


def L(think, ex, mist, extra=""):
    return lesson(think, ex, mist, extra)


def unit(grade, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    make_unit(R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort, grade=grade)


def figure(pts, segs, sides=(), right=(), W=340, H=230, label="figura geometrica", ticks=(), dashed=()):
    return fr_c4.figure(pts, segs, sides, right, W, H, label, ticks, dashed)


def kosy(lines=(), pts=(), lo=-5, hi=5, u=24, label="piano cartesiano", names=None):
    return de_k8.kosy(lines, pts, lo, hi, u, label, names)


def kurve(fs, xr, yr, pts=(), W=330, H=250, label="grafico", xlab=None):
    return de_k10.kurve(fs, xr, yr, pts, W, H, label, xlab)


def W(*xs):
    """lista di distrattori senza None e senza doppioni (come stringhe)"""
    out = []
    for x in xs:
        if x is not None and not (isinstance(x, (int, Fr)) and x < 0) and str(x) not in out:
            out.append(str(x))
    return out
