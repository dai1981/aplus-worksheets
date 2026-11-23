# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º de Primaria: Repartos (Sentido numérico)
Repartir en partes iguales con dibujos, hacer grupos iguales, reparto y multiplicación, ¿sobra alguno?, problemas.
Sin el signo de dividir (se introduce en 3.º).
Errores: repartir sin que todos tengan lo mismo, confundir el número de grupos con lo que hay en cada grupo.
"""
import random
from es_common import mcq, num
from es_low import unit
import es_pics as P

R = random.Random(32006)
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]


def cuant(kind):
    return "¿Cuántas" if P.fem(kind) else "¿Cuántos"


def s_dibujo():
    g, k = R.randint(2, 5), R.randint(2, 5)
    kind = R.choice(P.KINDS)
    n = g * k
    return mcq(P.fila(n, kind, 10) + "Repartimos %s en %d grupos iguales. %s van en cada grupo?" % (P.cosas(kind, n), g, cuant(kind)), str(k), [str(g) if g != k else str(k + 2), str(k + 1), str(n - g)],
               "%d grupos de %d son %d: van <b>%d</b> en cada grupo." % (g, k, n, k))


def s_grupos():
    g, k = R.randint(2, 5), R.choice([2, 3, 4, 5])
    kind = R.choice(P.KINDS)
    n = g * k
    return mcq(P.fila(n, kind, 10) + "Hacemos grupos de %d con %s. ¿Cuántos grupos salen?" % (k, P.cosas(kind, n)), str(g), [str(k) if g != k else str(g + 2), str(g + 1), str(n - k)],
               "%d + %s = %d: salen <b>%d</b> grupos." % (k, " + ".join([str(k)] * (g - 1)), n, g))


def s_ver():
    g, k = R.randint(2, 4), R.randint(2, 5)
    kind = R.choice(P.KINDS)
    t = R.choice(["cada", "grupos", "total"])
    pic = P.grupos(g, k, kind)
    if t == "cada":
        return mcq(pic + "Hemos repartido %s en %d grupos iguales. %s hay en cada grupo?" % (P.cosas(kind, g * k), g, cuant(kind)), str(k), [str(g) if g != k else str(k + 2), str(k + 1), str(g * k)], "En cada grupo hay <b>%d</b>." % k)
    if t == "grupos":
        return mcq(pic + "Hemos hecho grupos de %d. ¿Cuántos grupos hay?" % k, str(g), [str(k) if g != k else str(g + 2), str(g + 1), str(g * k)], "Contamos los grupos: <b>%d</b>." % g)
    return mcq(pic + "¿Qué multiplicación cuenta todos?", "%d × %d = %d" % (g, k, g * k), ["%d + %d = %d" % (g, k, g + k), "%d × %d = %d" % (g, k + 1, g * (k + 1)), "%d × %d = %d" % (g + 1, k, (g + 1) * k)],
               "%d grupos de %d: <b>%d × %d = %d</b>." % (g, k, g, k, g * k))


def s_sobra():
    g = R.randint(2, 4)
    k = R.randint(2, 5)
    r = R.randint(1, g - 1) if R.random() < 0.6 else 0
    n = g * k + r
    kind = R.choice(P.KINDS)
    ok = "sí, sobra%s %d" % ("n" if r > 1 else "", r) if r else "no sobra ninguno"
    return mcq(P.fila(n, kind, 10) + "Repartimos %s entre %d niños, lo mismo a cada uno. ¿Sobra alguno?" % (P.cosas(kind, n), g),
               ok, ["no sobra ninguno" if r else "sí, sobra 1", "sí, sobra%s %d" % ("n" if r + 1 > 1 else "", r + 1) if r + 1 < g else "sí, sobran %d" % g, "sí, sobran %d" % (k + r)] + (["sí, sobran 2"] if r != 2 else []),
               "%d niños × %d = %d. %s" % (g, k, g * k, "Sobra%s <b>%d</b>." % ("n" if r > 1 else "", r) if r else "<b>No sobra ninguno</b>."))


def s_tabla():
    g = R.choice([2, 3, 4, 5, 10])
    k = R.randint(2, 10)
    n = g * k
    return mcq("Si %d × %d = %d, al repartir %d entre %d, ¿cuántos le tocan a cada uno?" % (g, k, n, n, g), str(k), [str(g) if g != k else str(k + 2), str(n - g), str(k + 1)],
               "%d × %d = %d: a cada uno le tocan <b>%d</b>." % (g, k, n, k))


# (cosas, femenino, «en/entre X», ¿cada qué?)
COSAS = [("caramelos", False, "en %d bolsas", "cada bolsa"), ("cromos", False, "entre %d amigos", "cada amigo"), ("galletas", True, "en %d platos", "cada plato"),
         ("lápices", False, "en %d estuches", "cada estuche"), ("niños", False, "en %d equipos", "cada equipo"), ("flores", True, "en %d jarrones", "cada jarrón"),
         ("libros", False, "en %d estanterías", "cada estantería"), ("huevos", False, "en %d cajas", "cada caja"), ("canicas", True, "entre %d amigas", "cada amiga")]


def s_problema():
    what, fem, among, each = R.choice(COSAS)
    g = R.choice([2, 3, 4, 5, 10])
    k = R.randint(2, 10)
    n = g * k
    p = R.choice(NOMBRES)
    cu = "¿Cuántas" if fem else "¿Cuántos"
    if R.random() < 0.6:
        q = "%s reparte %d %s %s por igual. %s %s hay en %s?" % (p, n, what, among % g, cu, what, each)
        if among.startswith("entre"):
            q = "%s reparte %d %s %s por igual. %s le tocan a %s?" % (p, n, what, among % g, cu, each)
        return mcq(q, str(k), [str(n - g), str(g) if g != k else str(k + 2), str(k + 1)], "%d × %d = %d: <b>%d</b> en cada uno." % (g, k, n, k))
    if what in ("niños", "flores", "libros", "huevos"):
        return None
    return mcq("%s tiene %d %s y quiere hacer montones de %d. ¿Cuántos montones hace?" % (p, n, what, k), str(g), [str(n - k), str(k) if g != k else str(g + 2), str(g + 1)], "%d × %d = %d: hace <b>%d</b> montones." % (g, k, n, g))


unit(2, "repartos", 6, "N", "Repartos en partes iguales y agrupamientos con material y dibujos; relación del reparto con la multiplicación",
     "Repartos en partes iguales", "Repartos",
     "Fichas de matemáticas de 2.º de Primaria: repartir en partes iguales, hacer grupos, ver si sobra alguno y problemas de reparto. 100 ejercicios con soluciones.",
     "Repartir: todos reciben lo mismo", "Lo que no se puede repartir, sobra.",
     ["<b>Repartir</b> en partes iguales es dar a cada uno lo mismo.", "Puedes repartir de uno en uno, como en un juego de cartas, hasta que se acaben.",
      "Si sabes 3 × 4 = 12, sabes que 12 repartido entre 3 da 4 a cada uno.", "A veces sobra alguno que no se puede repartir."],
     [("12 caramelos entre 3 niños", ["3 × 4 = 12"], "4 a cada uno"), ("13 cromos entre 2 amigos", ["2 × 6 = 12", "13 − 12 = 1"], "6 a cada uno y sobra 1")],
     [["Dar más a uno que a otro", "Al final, todos deben tener lo mismo."], ["Confundir grupos y lo que hay en cada grupo", "Pregunta: ¿cuántos grupos? ¿cuántos en cada uno?"], ["Olvidar lo que sobra", "Cuenta lo que queda sin repartir."]],
     [("¿Qué es repartir en partes iguales?", "Dar a cada uno la misma cantidad. Por ejemplo, 10 caramelos entre 2 niños: 5 para cada uno."), ("¿Qué relación hay entre repartir y multiplicar?", "Son contrarios: si 2 × 5 = 10, al repartir 10 entre 2 le tocan 5 a cada uno.")],
     [("Repartir con dibujos", [(s_dibujo, 20)]), ("Hacer grupos iguales", [(s_grupos, 20)]), ("Grupos y multiplicación", [(s_ver, 14), (s_tabla, 6)]), ("¿Sobra alguno?", [(s_sobra, 20)]), ("Problemas", [(s_problema, 20)])],
     32006, P.grupos(3, 4, "apple"))
