# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Matrices (Sentido algebraico)
Tipos de matrices y operaciones, producto, potencias, matriz inversa, ecuaciones matriciales; matrices para organizar datos (ventas, precios, producción).
Reutiliza los generadores de Matemáticas II con otra semilla.
Errores: multiplicar elemento a elemento, creer que AB = BA, multiplicar matrices de dimensiones que no encajan.
"""
import random
from es_ccss import M, mix, num, unit, L, W, eu, use_, mat, tabla

R = random.Random(54001)
s_basico, s_producto, s_potencias, s_inversa, s_ecuaciones = use_("gen_es_matematicas_2bach_matrices", 54101, "s_basico", "s_producto", "s_potencias", "s_inversa", "s_ecuaciones")

TIENDAS = [("la tienda del centro", "la tienda de las afueras"), ("el local de Valencia", "el local de Sevilla"), ("el puesto del mercado", "la tienda online")]
PROD = [((("camisetas", "las"), ("pantalones", "los"), ("chaquetas", "las")), (8, 25, 40)), ((("cafés", "los"), ("bocadillos", "los"), ("zumos", "los")), (2, 4, 3)),
        ((("libros", "los"), ("cuadernos", "los"), ("mochilas", "las")), (15, 3, 30))]


def de(t):
    return "del " + t[3:] if t.startswith("el ") else "de " + t


def en(t):
    return "en " + t


def s_datos():
    t = R.choice(["ingreso", "ingreso", "total", "dim", "elem"])
    (pr, precios), (t1, t2) = R.choice(PROD), R.choice(TIENDAS)
    A = [[R.randint(5, 60) for _ in range(3)] for _ in range(2)]
    P = [p + R.choice([0, 1, 2]) for p in precios]
    T = tabla(["", pr[0][0], pr[1][0], pr[2][0]], [[t1, str(A[0][0]), str(A[0][1]), str(A[0][2])], [t2, str(A[1][0]), str(A[1][1]), str(A[1][2])]])
    intro = T + "La matriz A recoge las unidades vendidas en una semana y el vector P = %s los precios (en euros) de %s, %s y %s. " % (mat([[P[0]], [P[1]], [P[2]]]), pr[0][0], pr[1][0], pr[2][0])
    ing = [sum(a * p for a, p in zip(row, P)) for row in A]
    if t == "ingreso":
        i = R.randrange(2)
        tn = (t1, t2)[i]
        return M(intro + "Con A · P, ¿cuánto se ingresó %s?" % en(tn), eu(ing[i], 0),
                 W([eu(ing[1 - i], 0), eu(sum(A[i]) * sum(P), 0), eu(sum(A[i]) + sum(P), 0), eu(A[i][0] * P[0], 0)]),
                 "Fila %s por P: %s = <b>%s</b>." % (de(tn), " + ".join("%d · %d" % (a, p) for a, p in zip(A[i], P)), eu(ing[i], 0)))
    if t == "total":
        return M(intro + "¿Cuánto se ingresó en total entre los dos sitios?", eu(sum(ing), 0), W([eu(ing[0], 0), eu(sum(map(sum, A)) * sum(P), 0), eu(sum(map(sum, A)), 0), eu(ing[0] * 2, 0) if ing[0] != ing[1] else eu(sum(ing) + 10, 0)]),
                 "A · P = %s; total: %s + %s = <b>%s</b>." % (mat([[ing[0]], [ing[1]]]), num(ing[0]), num(ing[1]), eu(sum(ing), 0)))
    if t == "dim":
        return M(intro + "¿Qué dimensión tiene A · P?", "2 × 1", ["3 × 1", "2 × 3", "1 × 2", "no se puede multiplicar"], "A es 2 × 3 y P es 3 × 1: el producto es <b>2 × 1</b> (un ingreso por fila).")
    j = R.randrange(3)
    nm, ar = pr[j]
    vend = "vendidos" if ar == "los" else "vendidas"
    ok = "el número de %s %s %s" % (nm, vend, en(t2))
    return M(intro + "¿Qué significa el elemento a<sub>2%d</sub> de A?" % (j + 1), ok,
             W(["el número de %s %s %s" % (nm, vend, en(t1)), "el precio de %s %s" % (ar, nm), "el número de %s %s en total" % (nm, vend), "el ingreso por %s %s" % (ar, nm)]),
             "a<sub>ij</sub>: fila i (sitio de venta), columna j (producto). a<sub>2%d</sub> = %d: <b>%s</b>." % (j + 1, A[1][j], ok))


seen = set()
sets = [("Tipos y operaciones", mix(R, seen, [(s_basico, 20)])), ("Producto de matrices", mix(R, seen, [(s_producto, 20)])), ("Matrices con datos", mix(R, seen, [(s_datos, 20)])),
        ("Matriz inversa", mix(R, seen, [(s_inversa, 20)])), ("Potencias y ecuaciones matriciales", mix(R, seen, [(s_potencias, 8), (s_ecuaciones, 12)]))]
think = ["Una <b>matriz</b> m × n es una tabla de números con m filas y n columnas. Sirve para organizar datos: ventas por tienda y producto, precios, producción…",
         "Se suman (y se restan) elemento a elemento si tienen la misma dimensión. Para multiplicar A · B, las columnas de A deben ser tantas como las filas de B: fila por columna.",
         "El producto <b>no es conmutativo</b>: en general AB ≠ BA.",
         "La <b>inversa</b> A<sup>−1</sup> cumple A · A<sup>−1</sup> = I. Para resolver AX = B, se multiplica por la izquierda: X = A<sup>−1</sup>B."]
ex = [("Ventas (2 tiendas × 3 productos) por precios (3 × 1)", ["fila 1: 10 · 8 + 20 · 25 + 5 · 40"], "780 € en la tienda 1")]
mist = [["Multiplicar elemento a elemento", "Es fila por columna."], ["Creer que AB = BA", "El orden importa."], ["X = BA<sup>−1</sup> en AX = B", "Se multiplica por la izquierda: X = A<sup>−1</sup>B."]]
body = L(think, ex, mist)
faq = [("¿Para qué sirven las matrices en ciencias sociales?", "Para manejar tablas de datos: ventas, costes, flujos de población entre ciudades o relaciones entre sectores de la economía."),
       ("¿Cuándo tiene inversa una matriz?", "Cuando es cuadrada y su determinante no es 0.")]
unit(2, R, "matrices", "A", "Matrices: tipos, operaciones, producto, potencias, matriz inversa y ecuaciones matriciales; matrices para organizar y calcular con datos",
     "Matrices", "Matrices", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: operaciones con matrices, producto, inversa, ecuaciones matriciales y tablas de datos. 100 ejercicios.",
     "Producto: fila por columna", "En general, AB ≠ BA.", body, faq, sets, 1)
