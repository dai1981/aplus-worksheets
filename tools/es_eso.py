# -*- coding: utf-8 -*-
"""
España, ESO (Real Decreto 217/2022): partes comunes de los generadores gen_es_matematicas_{1,2,3,4}eso_*.
Sobre es_c3 (fq, d, sg, W, M, mcq, mix, lesson, num, eur, Kids, fr…):
  E(*términos) / expr([(coef, "x"), (c, "")]) → 3x − 5         poly([a_n, …, a_0]) → 2x³ − x + 4
  P2(a, b, c) → ax² + bx + c     par(x) → (−3) si es negativo     sup(3) → ³
  rq(n) → (k, m) con √n = k√m    raiz(n) → «2√3»                  sol([..]) → «x₁ = −2, x₂ = 3»
  kosy(...) plano cartesiano (de_k8), kurve(...) gráfica (de_k10), figure(...) figura con vértices (fr_c4): etiquetas en español
  nz(R, lo, hi) entero no nulo; uniq(): filtro de repetidos por valor
  unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort) → grade «lv-eso»
  L(think, ejemplos, errores, pic="") → body_html (Cómo se hace → Ejemplo → Errores frecuentes)
"""
import math
import re
from fractions import Fraction as F
from es_c3 import (fq, d, sg, W, M, MINUS, mcq, mix, lesson, make_unit, num, dz, eur, Kids, ao, bank, fr, POR, DIV, NB,  # noqa: F401
                   recta, grafico, cuerpo_svg, relabel, fig, table, tira, circulo)

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUB = "₀₁₂₃₄₅₆₇₈₉"
PI = "π"


def sup(n):
    return "" if n == 1 else ("⁻" if n < 0 else "") + "".join(SUP[int(c)] for c in str(abs(n)))


def nz(R, lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def nums(x):
    """número (Fraction/int) en texto: entero, decimal exacto o fracción"""
    x = F(x)
    if x.denominator == 1:
        return sg(int(x))
    try:
        return d(x)
    except ValueError:
        return fq(x)


def coef(k, var, first):
    k = F(k)
    a = abs(k)
    body = ("" if (a == 1 and var) else fq(a)) + var
    if first:
        return (MINUS if k < 0 else "") + body
    return " %s %s" % (MINUS if k < 0 else "+", body)


def expr(terms):
    out = ""
    for k, v in terms:
        if F(k) == 0:
            continue
        out += coef(k, v, out == "")
    return out or "0"


def E(*t):
    return expr(list(t))


def poly(cs, v="x"):
    n = len(cs) - 1
    return expr([(c, v + sup(n - i) if n - i >= 1 else "") for i, c in enumerate(cs)])


def P2(a, b, c, v="x"):
    return expr([(a, v + "²"), (b, v), (c, "")])


def par(x):
    x = F(x)
    return "(%s)" % fq(x) if x < 0 else fq(x)


def rq(n):
    k, m = 1, n
    f = 2
    while f * f <= m:
        while m % (f * f) == 0:
            m //= f * f
            k *= f
        f += 1
    return k, m


def raiz(n, k=1):
    """k·√n simplificado"""
    a, b = rq(n)
    a *= k
    if b == 1:
        return num(a)
    return ("" if a == 1 else num(a)) + "√" + str(b)


def sol(xs, v="x"):
    xs = sorted(set(F(x) for x in xs))
    if len(xs) == 1:
        return "%s = %s" % (v, fq(xs[0]))
    return ", ".join("%s%s = %s" % (v, SUB[i + 1], fq(x)) for i, x in enumerate(xs))


def kosy(*a, **k):
    from de_k8 import kosy as _k
    k.setdefault("label", "plano cartesiano")
    return relabel(_k(*a, **k), k["label"])


def kurve(*a, **k):
    from de_k10 import kurve as _k
    k.setdefault("label", "gráfica de una función")
    return relabel(_k(*a, **k), k["label"])


def figure(*a, **k):
    from fr_c4 import figure as _f
    k.setdefault("label", "figura geométrica")
    return _f(*a, **k)


def L(think, ex, mist, pic=""):
    return lesson(think, ex, mist, pic)


def unit(lv, R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort):
    make_unit(R, slug, dom, std, title, short, meta, key_big, key_sub, body, faq, sets, sort, grade="%d-eso" % lv)


def tabla(head, rows):
    """tabla pequeña dentro de una pregunta"""
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def use_(modname, seed, *names, preds=()):
    """generadores de otro curso de España (cambia su R)"""
    from es_common import use
    out = use(modname, seed, *names, preds=preds)

    def wrap(mk):
        def f():
            it = mk()
            if it:
                for k in ("q", "e"):
                    it[k] = it[k].replace(" × ", " · ")
                it["c"] = [c.replace(" × ", " · ") for c in it["c"]]
            return it
        f.__name__ = mk.__name__
        return f
    return [wrap(m) for m in out] if isinstance(out, list) else wrap(out)
