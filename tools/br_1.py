# -*- coding: utf-8 -*-
"""
Brasil Matemática 1º ano: partes comuns (figuras grandes com nomes em português).
Os geradores gen_br_matematica_1_*.py usam estas funções junto com br_common e br_2.
"""
import k_pics
from br_common import relabel, fig, coisas, COISAS, KINDS, num  # noqa: F401

EXTENSO = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
           "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte"]
ORD_M = ["", "primeiro", "segundo", "terceiro", "quarto", "quinto", "sexto", "sétimo", "oitavo", "nono", "décimo"]


def nome(kind, n=2):
    return COISAS[kind][0] if n == 1 else COISAS[kind][1]


def fem(kind):
    return COISAS[kind][2] == "f"


def quantos(kind):
    return "Quantas" if fem(kind) else "Quantos"


def art(kind):
    return ("a " if fem(kind) else "o ") + COISAS[kind][0]


def pic(svg, label, lg=False):
    svg = relabel(svg, label)
    if lg and "data-pf" not in svg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def fila(n, kind, per_row=10):
    return pic(k_pics.row_svg(n, kind, per_row), coisas(kind, n))


def espalhados(n, kind, seed):
    return pic(k_pics.scatter_svg(n, kind, seed), coisas(kind, n))


def quadro_dez(n, frames=None):
    return pic(k_pics.tenframe_svg(n, frames), "quadro de dez com %s" % ("%d bolinhas" % n if n != 1 else "1 bolinha"))


def dados(vals):
    return pic(k_pics.dice_svg(vals), "dados: " + ", ".join(map(str, vals)))


def dois_grupos(a, ka, b, kb=None, sinal="+"):
    kb = kb or ka
    return pic(k_pics.two_groups_svg(a, ka, b, kb, sinal), "%s %s %s" % (coisas(ka, a), {"+": "mais", "e": "e"}.get(sinal, sinal), coisas(kb, b)))


def riscados(n, kind, k, per_row=10):
    return pic(k_pics.crossed_row_svg(n, kind, k, per_row), "%s, %d riscad%ss" % (coisas(kind, n), k, "a" if fem(kind) else "o"))


def torres(hs):
    return pic(k_pics.towers_svg(hs), "torres de cubinhos " + ", ".join("%s com %d" % (l, h) for l, h in zip("ABCD", hs)))


def lapis(ls):
    return pic(k_pics.pencils_svg(ls), "lápis " + ", ".join("%s" % l for l in "ABCD"[:len(ls)]))


def ligacao(todo, a, b):
    return pic(k_pics.bond_svg(todo, a, b), "o todo %s e as partes %s e %s" % (todo, a, b))


def caixa(n, kind):
    return pic(k_pics.box_svg(n, kind), coisas(kind, n))
