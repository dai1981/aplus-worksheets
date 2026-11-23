# -*- coding: utf-8 -*-
"""España, primer ciclo (1.º y 2.º) y 3.º de Primaria: dibujos de k_pics con nombres en español."""
import k_pics
from es_common import relabel, fig, num

# kind: (singular, plural, género)
COSAS = {"apple": ("manzana", "manzanas", "f"), "star": ("estrella", "estrellas", "f"), "ball": ("pelota", "pelotas", "f"), "button": ("botón", "botones", "m"),
         "fish": ("pez", "peces", "m"), "flower": ("flor", "flores", "f"), "heart": ("corazón", "corazones", "m"), "duck": ("pato", "patos", "m"),
         "cup": ("taza", "tazas", "f"), "bug": ("mariquita", "mariquitas", "f")}
KINDS = list(COSAS)
NUM = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
       "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte"]


def nombre(kind, n=2):
    return COSAS[kind][0] if n == 1 else COSAS[kind][1]


def fem(kind):
    return COSAS[kind][2] == "f"


def cuantos(kind):
    return "¿Cuántas" if fem(kind) else "¿Cuántos"


def cosas(kind, n):
    return "%d %s" % (n, nombre(kind, n))


def pic(svg, label, lg=False):
    svg = relabel(svg, label)
    if lg and "data-pf" not in svg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def fila(n, kind, per_row=10):
    return pic(k_pics.row_svg(n, kind, per_row), cosas(kind, n))


def disperso(n, kind, seed):
    return pic(k_pics.scatter_svg(n, kind, seed), cosas(kind, n))


def marco10(n, frames=None):
    return pic(k_pics.tenframe_svg(n, frames), "marco de diez con %d %s" % (n, "punto" if n == 1 else "puntos"))


def dados(vals):
    return pic(k_pics.dice_svg(vals), "dados: " + ", ".join(map(str, vals)))


def dos_grupos(a, ka, b, kb=None, signo="+"):
    kb = kb or ka
    s = k_pics.two_groups_svg(a, ka, b, kb, signo)
    return pic(s, "%s %s %s" % (cosas(ka, a), "más" if signo == "+" else signo, cosas(kb, b)))


def tachados(n, kind, k, per_row=10):
    return pic(k_pics.crossed_row_svg(n, kind, k, per_row), "%s, %d %s" % (cosas(kind, n), k, "tachadas" if fem(kind) else "tachados"))


def torres(hs):
    return pic(k_pics.towers_svg(hs), "torres de cubos: " + ", ".join("%s con %d" % (l, h) for l, h in zip("ABCD", hs)))


def lapices(ls):
    return pic(k_pics.pencils_svg(ls), "lápices " + ", ".join("ABCD"[:len(ls)]))


def caja(n, kind):
    return pic(k_pics.box_svg(n, kind), cosas(kind, n))


def regletas(t, o):
    return pic(k_pics.rods_svg(t, o), "%d decenas y %d unidades" % (t, o))


def salto(start, hops, lo=0, hi=10):
    return pic(k_pics.hop_line_svg(start, hops, lo, hi), "recta con saltos")


def grupos(g, k, kind):
    """g grupos iguales de k objetos"""
    return pic(k_pics.groups_svg([(k, kind)] * g), "%d grupos de %s" % (g, cosas(kind, k)))


def matriz(rows, cols, kind):
    """filas y columnas: rows filas de cols objetos"""
    return pic(k_pics.array_svg(rows, cols, kind), "%d filas de %s" % (rows, cosas(kind, cols)))


def plato(n, kind, per_row=5):
    return pic(k_pics.plate_svg(n, kind, per_row), "plato con %s" % cosas(kind, n))
