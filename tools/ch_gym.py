# -*- coding: utf-8 -*-
"""
Schweiz / Mathematik Gymnasium（Rahmenlehrplan Gymnasiale Maturitätsschulen, EDK 2024）: gemeinsame Teile
  build(spec)   spec(R) → dict(title, short, meta, kb, ks, think, ex, mist, faq, sets=[(Titel, [(maker, n)])])
                → Funktion (seed, slug, grade, sort, codes, dom) für ch_run
  mcq           4 Antworten, negative Zahlen erlaubt, None bei zu wenig Ablenkern
  z(v)          Zahl (Fraction) → 3 / −2,5 / Bruch
  poly(c, v)    {Exponent: Koeffizient} → 3x³ − 2x + 5
  vec(*k)       Spaltenvektor (.mx m1), pt(*k) Punkt (2 | −1 | 3)
Text in deutscher Schreibweise (Komma); ch_common.ch_text stellt auf Schweizer Schreibweise um (Punkt, ’).
"""
import random
from fractions import Fraction as Fr
import ch_common as C
import de_common as D
from de_k6 import bh, dz, endlich  # noqa: F401
from de_k10 import kurve, pi_txt  # noqa: F401

NB = D.NB
MI = "−"
SUPS = {2: "²", 3: "³", 4: "⁴"}


def mcq(q, a, cands, e):
    try:
        return D.mcq(q, a, cands, e, neg=True)
    except AssertionError:
        return None


def z(v):
    v = Fr(v)
    if v.denominator == 1:
        return (MI if v < 0 else "") + D.num(abs(v.numerator))
    if endlich(v) and v.denominator <= 20:
        return dz(v)
    return bh(v)


def fz(v):
    """Bruch immer als Bruch (nicht als Dezimalzahl)"""
    v = Fr(v)
    return z(v) if v.denominator == 1 else bh(v)


def par(v):
    v = Fr(v)
    return "(%s)" % z(v) if v < 0 else z(v)


def sup(e):
    if e in SUPS:
        return SUPS[e]
    return "<sup>%s</sup>" % ((MI + str(-e)) if e < 0 else str(e))


def poly(c, v="x", frac=True):
    """c: {Exponent: Koeffizient}; Exponent kann auch ein Text sein (dann als Faktor angehängt)"""
    out = []
    keys = [k for k in c if isinstance(k, str)] + sorted([k for k in c if not isinstance(k, str)], reverse=True)
    for e in keys:
        k = Fr(c[e])
        if k == 0:
            continue
        a = abs(k)
        cs = fz(a) if frac else z(a)
        if isinstance(e, str):
            body = ("" if a == 1 else cs) + e
        elif e == 0:
            body = cs
        else:
            body = ("" if a == 1 else cs) + v + ("" if e == 1 else sup(e))
        out.append((k < 0, body))
    if not out:
        return "0"
    s = (MI if out[0][0] else "") + out[0][1]
    for neg, b in out[1:]:
        s += (" − " if neg else " + ") + b
    return s


def lin(a, b, v="x"):
    return poly({1: a, 0: b}, v)


def vec(*k):
    return "<span class='mx m1'>%s</span>" % "".join("<span>%s</span>" % (x if isinstance(x, str) else z(x)) for x in k)


def pt(name, *k):
    return "%s(%s)" % (name, (NB + "|" + NB).join(z(x) for x in k))


def ri(R, lo, hi, no=()):
    while True:
        v = R.randint(lo, hi)
        if v not in no:
            return v


def build(spec):
    def src(seed, slug, grade, sort, codes, dom):
        R = random.Random(seed)
        u = spec(R)
        seen = set()
        sets = [(t, D.mix(R, seen, parts)) for t, parts in u["sets"]]
        body = D.lesson(u["think"], [D.example(*x) for x in u["ex"]], u["mist"])
        C.write(slug, grade, sort, codes, dom, u["title"], u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"],
                sets, random.Random(seed + 7))
    return src


import re as _re
_GYM = [(r"\bfür (die )?(Klasse 10|10\. Klasse)\b", "für das Gymnasium"), (r"\b[Ii]n (der )?(Klasse 10|10\. Klasse)\b", "am Gymnasium"),
        (r"\b(Klasse 10|10\. Klasse)\b", "Gymnasium"), (r"Sek(undarstufe)? I\b", "Gymnasium")]


def gymfix(got):
    """Texte aus Deutschland Klasse 10 auf das Gymnasium umstellen"""
    def f(s):
        for a, b in _GYM:
            s = _re.sub(a, b, s)
        return s
    for k in ("title", "short", "meta", "kb", "ks", "body"):
        got[k] = f(got[k])
    got["faq"] = [{"q": f(x["q"]), "a": f(x["a"])} for x in got["faq"]]
