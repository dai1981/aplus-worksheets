# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité, programme 2026) : outils communs au-dessus de fr_c4.
・E(*termes) = expr, nz(R, lo, hi) entier non nul
・P2(a, b, c) → 2x² − 3x + 5 ; sq(n) → √n simplifié (3√2) ; pit(Fraction) → 3π/4
・vtab(xs, ys, dsig=None) : tableau de variations (option : ligne du signe de f′(x))
・arbre(pA, pBA, pBnA, labels) : arbre pondéré à deux niveaux
・code(*lignes) : bloc Python
・loi(xs, ps) : tableau de loi d’une variable aléatoire
・grille / kurve / kosy : graphiques (de_k10.kurve, de_k8.kosy)
"""
import math
from fractions import Fraction as Fr
from fr_c4 import *  # noqa: F401,F403
from fr_c4 import d, fq, expr, MINUS, wrap, text, line, INK, BLUE, NB, table
import de_k10
import de_k8

GREEN2 = "#15803d"


def E(*t):
    return expr(list(t))


def nz(R, lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def P2(a, b, c, v="x"):
    return expr([(a, v + "²"), (b, v), (c, "")])


def sq(n):
    """√n simplifié : 12 → 2√3, 9 → 3"""
    k = 1
    m = n
    for p in range(2, int(math.isqrt(n)) + 1):
        while m % (p * p) == 0:
            m //= p * p
            k *= p
    if m == 1:
        return str(k)
    return ("" if k == 1 else str(k)) + "√" + str(m)


def pit(v):
    """multiple de π (Fraction) → texte"""
    v = Fr(v)
    if v == 0:
        return "0"
    s = MINUS if v < 0 else ""
    v = abs(v)
    z = ("" if v.numerator == 1 else str(v.numerator)) + "π"
    return s + (z if v.denominator == 1 else "%s/%d" % (z, v.denominator))


def ival(a, b, ca="[", cb="]"):
    return "%s%s ; %s%s" % (ca, a, b, cb)


def vtab(xs, ys, dsig=None, fname="f"):
    """xs : textes ; ys : nombres (ou textes) ; dsig : liste de '+'/'−' entre les xs (ligne f′(x))"""
    n = len(xs)
    W = 130 + 100 * (n - 1) + 40
    top = 38
    rows = 1 + (1 if dsig else 0)
    H = top + (42 if dsig else 0) + 92
    X = lambda i: 120 + 100 * i
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, INK),
         line(2, top, W - 2, top, INK, 1.2), line(76, 2, 76, H - 2, INK, 1.2), text(39, 26, "x", 15, weight=700)]
    y0 = top
    if dsig:
        s.append(line(2, top + 42, W - 2, top + 42, INK, 1.2))
        s.append(text(39, top + 27, fname + "′(x)", 14, weight=700))
        for i, sg in enumerate(dsig):
            s.append(text((X(i) + X(i + 1)) / 2, top + 28, sg, 17, weight=700))
        for i in range(1, n - 1):
            s.append(text(X(i), top + 27, "0", 14))
        y0 = top + 42
    s.append(text(39, y0 + 52, fname + "(x)", 14, weight=700))
    for i, x in enumerate(xs):
        s.append(text(X(i), 26, x, 14))
    num = [isinstance(y, (int, Fr)) for y in ys]
    vals = [y if num[i] else None for i, y in enumerate(ys)]
    hi_ = []
    for i in range(n):
        if vals[i] is None:
            hi_.append(i % 2 == 0)
            continue
        h = (i > 0 and vals[i - 1] is not None and vals[i] > vals[i - 1]) or (i < n - 1 and vals[i + 1] is not None and vals[i] > vals[i + 1])
        hi_.append(h)
    for i in range(n):
        yy = y0 + 22 if hi_[i] else y0 + 82
        s.append(text(X(i), yy, d(ys[i]) if num[i] else ys[i], 14, weight=600))
    for i in range(n - 1):
        up = hi_[i + 1] and not hi_[i]
        x1, x2 = X(i) + 22, X(i + 1) - 22
        y1, y2 = (y0 + 74, y0 + 20) if up else (y0 + 20, y0 + 74)
        s.append(line(x1, y1, x2, y2, BLUE, 1.8))
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (x2, y2, BLUE))
    return wrap(W, H, "".join(s), "tableau de variations", lg=True)


def arbre(pa, pba, pbna, A="A", B="B", fmt=d):
    """arbre pondéré : A / Ā puis B / B̄ ; probabilités en Fraction"""
    W, H = 440, 220
    s = []
    O = (24, 110)
    nA, nAb = (170, 55), (170, 165)
    leaves = [(360, 25, nA, B, pba), (360, 85, nA, B + "̄", 1 - pba), (360, 135, nAb, B, pbna), (360, 195, nAb, B + "̄", 1 - pbna)]
    for (x, y), lab, p in ((nA, A, pa), (nAb, A + "̄", 1 - pa)):
        s.append(line(O[0], O[1], x - 14, y, INK, 1.6))
        s.append(text((O[0] + x) / 2 - 4, (O[1] + y) / 2 + (-8 if y < O[1] else 20), fmt(p), 14, col=BLUE, weight=600))
        s.append(text(x, y + 6, lab, 17, weight=700))
    for x, y, (px, py), lab, p in leaves:
        s.append(line(px + 14, py, x - 14, y, INK, 1.6))
        s.append(text((px + x) / 2 + 6, (py + y) / 2 + (-6 if y < py else 18), fmt(p), 14, col=BLUE, weight=600))
        s.append(text(x, y + 6, lab, 17, weight=700))
    return wrap(W, H, "".join(s), "arbre pondéré", lg=True)


def code(*lines):
    out = []
    for ln in lines:
        ind = len(ln) - len(ln.lstrip(" "))
        out.append(NB * ind + ln.lstrip(" ").replace("<", "&lt;").replace(">", "&gt;"))
    return "<span class='code'>%s</span>" % "<br>".join(out)


def loi(xs, ps, var="X"):
    """tableau de loi : xs textes ou nombres, ps Fractions ou textes"""
    return table(["%s = x<sub>i</sub>" % var] + [x if isinstance(x, str) else d(x) for x in xs],
                 [["P(%s = x<sub>i</sub>)" % var] + [p if isinstance(p, str) else d(p) for p in ps]])


def kurve(*a, **k):
    return de_k10.kurve(*a, **k)


def kosy(*a, **k):
    return de_k8.kosy(*a, **k)


_M = M


def M(q, a, w, e):
    """comme fr_c4.M, mais signale (variable FRLY_WARN) quand il manque des distracteurs et que mcq complète au hasard"""
    import os
    from fr_c4 import val
    va = val(a)
    ws = []
    for x in w:
        if x is None or str(x) == str(a) or str(x) in ws or (va is not None and val(x) == va):
            continue
        ws.append(str(x))
    if len(ws) < 3 and os.environ.get("FRLY_WARN"):
        print("FILL:", q[-90:], "|", a)
    import re as _re
    m_ = _re.match(r"Voici la loi de X :(<div class='sn-tw'>.*?</div>) (.*)$", q, _re.S)
    if m_:
        q = m_.group(2) + " Loi de X :" + m_.group(1)
    fx = lambda t: t if t is None else str(t).replace("(x)(", "x(")
    return _M(fx(q), fx(a), [fx(x) for x in w], fx(e))


def U(i, v="u"):
    return "%s<sub>%s</sub>" % (v, i)


def FR(n, dd):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (n, dd)


def trig_val(t, fn):
    """t : multiple de π (Fraction) ; fn 'cos' ou 'sin' → texte exact"""
    v = (math.cos if fn == "cos" else math.sin)(float(t) * math.pi)
    for val_, s in ((0, "0"), (1, "1"), (-1, MINUS + "1"), (0.5, FR(1, 2)), (-0.5, MINUS + FR(1, 2)),
                    (math.sqrt(2) / 2, FR("√2", 2)), (-math.sqrt(2) / 2, MINUS + FR("√2", 2)), (math.sqrt(3) / 2, FR("√3", 2)), (-math.sqrt(3) / 2, MINUS + FR("√3", 2))):
        if abs(v - val_) < 1e-9:
            return s
    raise ValueError("pas remarquable")


def pif(t):
    """multiple de π → texte avec fraction HTML (π/3 → π/3 en fraction)"""
    t = Fr(t)
    if t == 0:
        return "0"
    s = MINUS if t < 0 else ""
    a = abs(t)
    num_ = ("" if a.numerator == 1 else str(a.numerator)) + "π"
    return s + (num_ if a.denominator == 1 else FR(num_, a.denominator))
