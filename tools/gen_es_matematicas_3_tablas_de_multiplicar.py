# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º y 3.º de Primaria: la multiplicación y las tablas (Sentido numérico)
build(lv): lv = 2 → «la-multiplicacion»: sumas repetidas, filas y columnas, tablas del 2, 3, 4, 5 y 10;
lv = 3 → «tablas-de-multiplicar»: tablas del 2 al 10, el factor que falta, el orden de los factores.
Errores: sumar en lugar de multiplicar (3 × 4 = 7), confundir grupos y elementos, saltarse un número de la tabla.
"""
import random
from es_common import mcq, mix, make_unit, lesson
import es_pics as P

R = None
LV = 3
TAB = {2: [2, 3, 4, 5, 10], 3: [2, 3, 4, 5, 6, 7, 8, 9, 10]}
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario", "Daniela", "Álvaro"]


def W(a, b):
    p = a * b
    return [str(a + b), str(p + a), str(p - b) if p - b > 0 else str(p + b + 1), str(p + b)]


def s_sumas():
    g = R.randint(2, 5)
    k = R.choice([2, 3, 4, 5, 10])
    kind = R.choice(P.KINDS)
    t = R.choice(["suma", "mult", "total"])
    pic = P.grupos(g, k, kind)
    if t == "suma":
        ok = " + ".join([str(k)] * g)
        return mcq(pic + "¿Qué suma corresponde al dibujo?", ok, [" + ".join([str(g)] * k), "%d + %d" % (g, k), " + ".join([str(k)] * (g + 1))], "Hay %d grupos de %d: <b>%s</b>." % (g, k, ok))
    if t == "mult":
        ok = "%d × %d" % (g, k)
        return mcq(pic + "¿Qué multiplicación corresponde al dibujo?", ok, ["%d + %d" % (g, k), "%d × %d" % (g, k + 1), "%d × %d" % (g + 1, k)] if g != k else ["%d + %d" % (g, k), "%d × %d" % (g, k + 1), "%d × %d" % (g + 1, k)],
                   "%d grupos de %d: <b>%s</b> = %d." % (g, k, ok, g * k))
    return mcq(pic + "%s hay en total?" % P.cuantos(kind), str(g * k), W(g, k), "%s = %d × %d = <b>%d</b>." % (" + ".join([str(k)] * g), g, k, g * k))


def s_filas():
    r, c = R.randint(2, 5), R.choice([2, 3, 4, 5])
    kind = R.choice(P.KINDS)
    t = R.choice(["total", "mult", "filas"])
    pic = P.matriz(r, c, kind)
    if t == "total":
        return mcq(pic + "%s hay?" % P.cuantos(kind), str(r * c), W(r, c), "%d filas de %d: %d × %d = <b>%d</b>." % (r, c, r, c, r * c))
    if t == "filas":
        return mcq(pic + "¿Cuántas filas hay? ¿Y cuántos en cada fila?", "%d filas de %d" % (r, c), ["%d filas de %d" % (c, r) if r != c else "%d filas de %d" % (r, c + 1), "%d filas de %d" % (r + 1, c), "%d filas de %d" % (r, c * r)], "Las filas van de izquierda a derecha: <b>%d filas de %d</b>." % (r, c))
    return mcq(pic + "¿Qué multiplicación da el total?", "%d × %d" % (r, c), ["%d + %d" % (r, c), "%d × %d" % (r, r * c), "%d × %d" % (r + 1, c)], "<b>%d × %d</b> = %d." % (r, c, r * c))


def s_tabla(tabs):
    def mk():
        a = R.choice(tabs)
        b = R.randint(1, 10)
        if R.random() < 0.5:
            a, b = b, a
        return mcq("Calcula: %d × %d" % (a, b), str(a * b), W(a, b), "%d × %d = <b>%d</b>." % (a, b, a * b))
    mk.__name__ = "tabla_%s" % tabs
    return mk


def s_serie():
    a = R.choice(TAB[LV])
    s = R.randint(0, 6)
    xs = [a * (s + i) for i in range(4)]
    hole = R.randint(1, 3)
    ok = xs[hole]
    shown = ", ".join("___" if i == hole else str(x) for i, x in enumerate(xs))
    return mcq("Tabla del %d. ¿Qué número falta? %s" % (a, shown), str(ok), [str(ok + 1), str(ok - 1), str(ok + 2) if a != 2 else str(ok + 10)], "Cada número es %d más que el anterior: <b>%d</b>." % (a, ok))


def s_falta():
    a = R.choice(TAB[LV])
    b = R.randint(2, 10)
    t = R.choice(["izq", "der", "conm", "doble"])
    if t == "izq":
        return mcq("¿Qué número falta? ___ × %d = %d" % (a, a * b), str(b), [str(a * b - a), str(b + 1), str(b - 1)], "%d × %d = %d: falta el <b>%d</b>." % (b, a, a * b, b))
    if t == "der":
        return mcq("¿Qué número falta? %d × ___ = %d" % (a, a * b), str(b), [str(a * b - a), str(b + 1), str(b - 1)], "%d × %d = %d: falta el <b>%d</b>." % (a, b, a * b, b))
    if t == "conm":
        return mcq("Si %d × %d = %d, ¿cuánto es %d × %d?" % (a, b, a * b, b, a), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)], "El orden de los factores no cambia el producto: <b>%d</b>." % (a * b))
    if LV == 2:
        return None
    if a not in (2, 3, 4, 5):
        return None
    return mcq("Si %d × %d = %d, ¿cuánto es %d × %d?" % (a, b, a * b, 2 * a, b), str(2 * a * b), [str(a * b + 2), str(a * b + b), str(a * b * 4)], "La tabla del %d es el doble de la del %d: %d × 2 = <b>%d</b>." % (2 * a, a, a * b, 2 * a * b))


COSAS = [("ruedas", "bicicleta", "bicicletas", 2), ("patas", "perro", "perros", 4), ("ruedas", "triciclo", "triciclos", 3), ("dedos", "mano", "manos", 5), ("ruedas", "coche", "coches", 4),
         ("lados", "triángulo", "triángulos", 3), ("patas", "araña", "arañas", 8), ("días", "semana", "semanas", 7), ("lápices", "caja", "cajas", 6), ("huevos", "cartón", "cartones", 10),
         ("cromos", "sobre", "sobres", 5), ("yogures", "paquete", "paquetes", 4), ("patas", "mesa", "mesas", 4), ("galletas", "bolsa", "bolsas", 9)]


def s_problema():
    what, one, many, k = R.choice(COSAS)
    if k not in TAB[LV] and LV == 2:
        return None
    n = R.randint(2, 9 if LV == 3 else 5)
    p = R.choice(NOMBRES)
    t = R.choice(["cuantos", "cuantos", "mas"])
    if t == "cuantos":
        q = "Cada %s tiene %d %s. ¿Cuántos %s hay en %d %s?" % (one, k, what, what, n, many) if not what.endswith("as") else "Cada %s tiene %d %s. ¿Cuántas %s hay en %d %s?" % (one, k, what, what, n, many)
        return mcq(q, str(n * k), W(n, k), "%d × %d = <b>%d</b>." % (n, k, n * k))
    m = R.randint(1, 3)
    if what != "cromos":
        return None
    return mcq("%s compra %d sobres de %d cromos y ya tenía %d cromos sueltos. ¿Cuántos cromos tiene ahora?" % (p, n, k, m), str(n * k + m), [str(n * k), str(n + k + m), str((n + m) * k)], "%d × %d = %d; %d + %d = <b>%d</b>." % (n, k, n * k, n * k, m, n * k + m))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30005 + lv * 1000)
    seen = set()
    if lv == 2:
        sets = [("Sumas repetidas", mix(R, seen, [(s_sumas, 20)])), ("Filas y columnas", mix(R, seen, [(s_filas, 20)])),
                ("Tablas del 2, del 5 y del 10", mix(R, seen, [(s_tabla([2, 5, 10]), 16), (s_serie, 4)])), ("Tablas del 3 y del 4", mix(R, seen, [(s_tabla([3, 4]), 14), (s_falta, 6)])),
                ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["<b>Multiplicar</b> es sumar varias veces el mismo número: 4 + 4 + 4 = 3 × 4 = 12.", "3 × 4 se lee «tres por cuatro»: 3 grupos de 4.", "En filas y columnas: 3 filas de 4 son 3 × 4."]
        ex = [("5 + 5 + 5 + 5", ["Hay 4 veces el 5", "4 × 5"], "20"), ("3 filas de 6 sillas", ["3 × 6"], "18 sillas")]
        mist = [["Sumar los dos números", "3 × 4 no es 3 + 4: son 3 grupos de 4."], ["Contar mal los grupos", "Cuenta primero los grupos y después cuántos hay en cada uno."], ["Saltarse un número de la tabla", "Di la tabla de 2 en 2: 2, 4, 6, 8…"]]
        pic = P.grupos(3, 4, "apple")
        slug, title, short = "la-multiplicacion", "La multiplicación", "La multiplicación"
        meta = "Fichas de matemáticas de 2.º de Primaria: la multiplicación como suma repetida, filas y columnas, tablas del 2, 3, 4, 5 y 10 y problemas. 100 ejercicios con soluciones."
        kb, ks = "Multiplicar es sumar el mismo número", "3 × 4 = 4 + 4 + 4 = 12."
        std = "La multiplicación como suma repetida y en disposiciones rectangulares; tablas del 2, 3, 4, 5 y 10"
    else:
        sets = [("Tablas del 2, 5 y 10", mix(R, seen, [(s_tabla([2, 5, 10]), 20)])), ("Tablas del 3, 4 y 6", mix(R, seen, [(s_tabla([3, 4, 6]), 20)])),
                ("Tablas del 7, 8 y 9", mix(R, seen, [(s_tabla([7, 8, 9]), 20)])), ("El factor que falta y el orden", mix(R, seen, [(s_falta, 14), (s_serie, 6)])),
                ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["En 6 × 4 = 24, 6 y 4 son los <b>factores</b> y 24 es el <b>producto</b>.", "El orden no importa: 6 × 4 = 4 × 6. Si sabes una, sabes la otra.",
                 "Trucos: la tabla del 4 es el doble de la del 2; la del 6, el doble de la del 3; la del 8, el doble de la del 4."]
        ex = [("7 × 8", ["7 × 4 = 28", "El doble: 28 + 28"], "56"), ("___ × 6 = 42", ["¿Qué número por 6 da 42?", "7 × 6 = 42"], "7")]
        mist = [["Sumar en vez de multiplicar", "6 × 4 no es 10: son 6 grupos de 4."], ["Confundir dos productos cercanos", "7 × 8 = 56, 6 × 9 = 54. Repasa las difíciles."], ["Olvidar el orden de los factores", "Si no sabes 9 × 3, piensa 3 × 9."]]
        pic = P.matriz(4, 6, "star")
        slug, title, short = "tablas-de-multiplicar", "Tablas de multiplicar", "Tablas de multiplicar"
        meta = "Fichas de matemáticas de 3.º de Primaria: tablas de multiplicar del 2 al 10, el factor que falta, el orden de los factores y problemas. 100 ejercicios con soluciones."
        kb, ks = "6 × 4 = 4 × 6 = 24", "Si sabes una, sabes la otra."
        std = "Tablas de multiplicar; propiedad conmutativa; relación entre tablas (dobles)"
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué tablas son las más difíciles?", "Suelen ser la del 7, la del 8 y la del 9. Ayuda pensar en dobles y en el orden: 8 × 7 = 7 × 8 = 56."),
           ("¿Qué es un producto?", "Es el resultado de una multiplicación. En 3 × 5 = 15, el producto es 15.")]
    make_unit(R, slug, "N", std, title, short, meta, kb, ks, body, faq, sets, 5, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(3)
