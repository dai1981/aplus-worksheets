# -*- coding: utf-8 -*-
"""
Brasil Matemática, Ensino Médio (1ª a 3ª série): partes comuns.
Tudo de br_9 (d, fq, expr, P2, par, sq, M, kosy, tab, ntab, bank, figure, formas, tri_pts, _svg, _t, _ln) e de br_common
(mix, lesson, use, num, reais, Kids), mais:
  curva   gráfico de funções (de_k10.kurve) com números brasileiros
  R2      Fraction → «R$ 1.234,56»
  pc      Fraction → «12,5%»
  sg      número com sinal para somar: «+ 3», «− 3»
  unit    make_unit com grade (1-serie, 2-serie, 3-serie)
"""
import re
from fractions import Fraction as F
from br_9 import (M, d, fq, expr, P2, par, sq, kosy, tab, ntab, bank, figure, formas, tri_pts, circulo,  # noqa: F401
                  _svg, _t, _ln, _arc, INK, BLUE, RED, GRN, make_unit, NB, MINUS)
from br_common import mix, lesson, use, num, reais, Kids, o, do, keep  # noqa: F401
import de_k10

COLS = ["#1f5fbf", "#c0392b", "#2e7d32", "#8e44ad"]


def _txt(t):
    t = re.sub("(\\d)[\u00a0\u202f ](\\d{3})(?!\\d)", r"\1\2", t)
    return re.sub(r"(?<![\d,.])(\d{4,})(?!\d)", lambda m: num(int(m.group(1))), t)


def _br(svg):
    """só nos textos (entre > e <): «1 000» e «1000» → «1.000»"""
    return re.sub(r">([^<]*)<", lambda m: ">" + _txt(m.group(1)) + "<", svg)


def curva(fs, xr, yr, pts=(), label="gráfico", xlab=None, W=330, H=250):
    """fs = [(f, nome)] ou [(f, cor, nome)]; xr, yr = (início, fim, passo)"""
    ff = []
    for i, t in enumerate(fs):
        if len(t) == 2:
            ff.append((t[0], COLS[i % len(COLS)], t[1]))
        else:
            ff.append(t)
    return _br(de_k10.kurve(ff, xr, yr, pts=pts, W=W, H=H, label=label, xlab=xlab))


def R2(x):
    """valor em reais (Fraction) → «R$ 1.234,56»"""
    x = F(x)
    neg = x < 0
    s = "R$" + NB + d(abs(x), 2, keep=True)
    return (MINUS if neg else "") + s


def pc(x, places=None):
    """Fraction (já em %) → «12,5%»"""
    return d(x, places) + "%"


def sg(x):
    """« + 3» / « − 3» para escrever depois de outro termo"""
    x = F(x)
    return (" %s %s" % (MINUS, d(-x))) if x < 0 else (" + %s" % d(x))


def unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort, grade):
    make_unit(R, slug, dom, codes, std, title, short, meta, kb, ks, body, faq, sets, sort, grade=grade)


def tri_ret(cb, ca, sides=(), ang=None, label="triângulo retângulo", W=340, H=220):
    """triângulo ABC com ângulo reto em C (C embaixo à esquerda, B à direita, A em cima).
    cb, ca: comprimentos (só para a forma); sides: [(P, Q, texto)]; ang: texto do ângulo em B"""
    sc = min((W - 140) / float(cb), (H - 70) / float(ca))
    x0, y0 = 60 + (W - 140 - cb * sc) / 2.0, H - 34
    P = {"C": (x0, y0), "B": (x0 + cb * sc, y0), "A": (x0, y0 - ca * sc)}
    sh = {"pts": P, "poly": "ABC", "sides": list(sides), "right": [("C", "A", "B")]}
    if ang:
        sh["angles"] = [("B", "A", "C", ang)]
    return formas([sh], W, H, label)


def tri(a, b, c, sides=(), angles=(), label="triângulo ABC", W=360, H=230):
    """triângulo com BC = a, CA = b, AB = c (números, só para a forma); sides [(P, Q, texto)], angles [(V, texto)]"""
    import math as _mm
    xa = (a * a + c * c - b * b) / (2.0 * a)
    ya = _mm.sqrt(max(c * c - xa * xa, 0))
    xs = [0, a, xa]
    sc = min((W - 120) / float(max(xs) - min(xs)), (H - 70) / float(ya or 1))
    x0 = 60 - min(xs) * sc + ((W - 120) - (max(xs) - min(xs)) * sc) / 2.0
    y0 = H - 34
    P = tri_pts(a, b, c, x0, y0, sc)
    other = {"A": ("B", "C"), "B": ("A", "C"), "C": ("A", "B")}
    sh = {"pts": P, "poly": "ABC", "sides": list(sides), "angles": [(v, other[v][0], other[v][1], t) for v, t in angles]}
    return formas([sh], W, H, label)


def pit(v):
    """múltiplo de π (Fraction) → «3π/4», «−π/2», «2π»"""
    v = F(v)
    if v == 0:
        return "0"
    s = MINUS if v < 0 else ""
    v = abs(v)
    z = ("" if v.numerator == 1 else str(v.numerator)) + "π"
    return s + (z if v.denominator == 1 else "%s/%d" % (z, v.denominator))


def trig(deg, fn):
    """valor exato de sen/cos/tg de um ângulo notável em graus → texto («√3/2», «−1/2»); None se não existir"""
    import math as _mm
    r = _mm.radians(deg)
    if fn == "tg":
        if abs(_mm.cos(r)) < 1e-9:
            return None
        v = _mm.tan(r)
        tab_ = [(0, "0"), (1, "1"), (-1, MINUS + "1"), (_mm.sqrt(3), "√3"), (-_mm.sqrt(3), MINUS + "√3"), (_mm.sqrt(3) / 3, "√3/3"), (-_mm.sqrt(3) / 3, MINUS + "√3/3")]
    else:
        v = (_mm.sin if fn == "sen" else _mm.cos)(r)
        tab_ = [(0, "0"), (1, "1"), (-1, MINUS + "1"), (0.5, "1/2"), (-0.5, MINUS + "1/2"), (_mm.sqrt(2) / 2, "√2/2"), (-_mm.sqrt(2) / 2, MINUS + "√2/2"),
                (_mm.sqrt(3) / 2, "√3/2"), (-_mm.sqrt(3) / 2, MINUS + "√3/2")]
    for x, s in tab_:
        if abs(v - x) < 1e-9:
            return s
    return None


def code(*lines):
    """código ou algoritmo em bloco (recuo com espaços)"""
    out = []
    for ln in lines:
        ind = len(ln) - len(ln.lstrip(" "))
        out.append(NB * ind + ln.lstrip(" ").replace("<", "&lt;").replace(">", "&gt;"))
    return "<span class='code'>%s</span>" % "<br>".join(out)


def fluxo(nodes, label="fluxograma"):
    """nodes: [(tipo, texto)] com tipo 'ini' (oval), 'proc' (retângulo), 'dec' (losango), 'es' (paralelogramo); em coluna"""
    W, bh, gap = 340, 40, 22
    H = 20 + len(nodes) * (bh + gap)
    s = []
    cx = W / 2
    for i, (tp, txt) in enumerate(nodes):
        y = 14 + i * (bh + gap)
        txt = txt.replace("<", "&lt;").replace(">", "&gt;")
        if tp == "ini":
            s.append("<rect x='%d' y='%d' width='160' height='%d' rx='20' fill='#e8f3e8' stroke='%s' stroke-width='2'/>" % (cx - 80, y, bh, INK))
        elif tp == "dec":
            s.append("<polygon points='%.1f,%d %.1f,%.1f %.1f,%d %.1f,%.1f' fill='#fff4d6' stroke='%s' stroke-width='2'/>" % (cx, y - 4, cx + 120, y + bh / 2.0, cx, y + bh + 4, cx - 120, y + bh / 2.0, INK))
        elif tp == "es":
            s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d %.1f,%d' fill='#eef4fb' stroke='%s' stroke-width='2'/>" % (cx - 100, y + bh, cx - 80, y, cx + 100, y, cx + 80, y + bh, INK))
        else:
            s.append("<rect x='%d' y='%d' width='220' height='%d' fill='#eef4fb' stroke='%s' stroke-width='2'/>" % (cx - 110, y, bh, INK))
        s.append(_t(cx, y + bh / 2.0 + 5, txt, 13, INK, bold=False))
        if i + 1 < len(nodes):
            y2 = y + bh + gap
            s.append(_ln(cx, y + bh + (4 if tp == "dec" else 0), cx, y2 - 2, INK, 1.6))
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (cx - 4, y2 - 8, cx + 4, y2 - 8, cx, y2 - 1, INK))
    return _svg(W, H, "".join(s), label)
