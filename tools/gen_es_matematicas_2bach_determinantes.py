# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Determinantes (Sentido algebraico)
Determinantes de orden 2 y 3 (regla de Sarrus), propiedades, desarrollo por adjuntos, cálculo de la inversa con adjuntos, rango por menores, determinantes con parámetros.
Errores: |k·A| = k·|A| (es kⁿ·|A|), signos de los adjuntos, |A + B| = |A| + |B|.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, mat, det_h, nf, det2, det3, W, par, MINUS

R = random.Random(52002)


def rm(n, lo=-3, hi=4):
    return [[R.randint(lo, hi) for _ in range(n)] for _ in range(n)]


def minor(A, i, j):
    return [[A[r][c] for c in range(3) if c != j] for r in range(3) if r != i]


def s_orden2():
    A = rm(2, -6, 7)
    d = det2(A)
    t = R.choice(["calc", "calc", "param"])
    if t == "calc":
        return M("Calcula %s." % det_h(A), sg(d), W([sg(A[0][0] * A[1][1] + A[0][1] * A[1][0]), sg(A[0][1] * A[1][0] - A[0][0] * A[1][1]) if d else "1", sg(A[0][0] * A[0][1] - A[1][0] * A[1][1]), sg(d + 1)]),
                 "%s · %s − %s · %s = <b>%s</b>." % (sg(A[0][0]), par(A[1][1]), sg(A[0][1]), par(A[1][0]), sg(d)))
    a, b, c = R.randint(1, 5), R.randint(-4, 5), R.randint(-4, 5)
    v = R.randint(-10, 10)
    # det [[a, b], [c, k]] = a k − b c = v → k = (v + bc)/a
    k = F(v + b * c, a)
    return M("¿Qué valor de k cumple %s = %s?" % (det_h([[a, b], [c, "k"]]), sg(v)), "k = %s" % nf(k), W(["k = %s" % nf(F(v - b * c, a)), "k = %s" % nf(-k), "k = %s" % nf(F(v, a)), "k = %s" % nf(k + 1)]), "%sk − %s = %s → <b>k = %s</b>." % ("" if a == 1 else a, par(b * c), sg(v), nf(k)))


def s_sarrus():
    A = rm(3, -2, 3)
    d = det3(A)
    t = R.choice(["calc", "calc", "calc", "tri"])
    if t == "tri":
        A = [[R.randint(1, 4), R.randint(-3, 3), R.randint(-3, 3)], [0, R.randint(-3, 4) or 2, R.randint(-3, 3)], [0, 0, R.randint(-3, 4) or 1]]
        d = A[0][0] * A[1][1] * A[2][2]
        return M("Calcula %s." % det_h(A), sg(d), W([sg(A[0][0] + A[1][1] + A[2][2]), sg(det3(A) + A[0][1]), "0" if d else "1", sg(-d) if d else "2"]), "Es triangular: el determinante es el producto de la diagonal, <b>%s</b>." % sg(d))
    pos = A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] * A[2][0] + A[0][2] * A[1][0] * A[2][1]
    neg = A[0][2] * A[1][1] * A[2][0] + A[0][0] * A[1][2] * A[2][1] + A[0][1] * A[1][0] * A[2][2]
    return M("Calcula %s." % det_h(A), sg(d), W([sg(pos + neg), sg(neg - pos) if d else "1", sg(pos), sg(d + 2)]), "Sarrus: (%s) − (%s) = <b>%s</b>." % (sg(pos), sg(neg), sg(d)))


def s_propiedades():
    t = R.choice(["k", "k", "tras", "prod", "inv", "filas", "teo"])
    n = R.choice([2, 3])
    d = R.choice([2, 3, -2, 4, 5, -1])
    if t == "k":
        k = R.choice([2, 3, -1, -2])
        return M("Si A es una matriz %d × %d con |A| = %s, ¿cuánto vale |%sA|?" % (n, n, sg(d), sg(k) if k != -1 else MINUS), sg(k ** n * d), W([sg(k * d), sg(k + d), sg(k ** (n + 1) * d), sg(-k ** n * d)]), "|kA| = kⁿ · |A| = (%s)%s · %s = <b>%s</b>." % (sg(k), "²" if n == 2 else "³", sg(d), sg(k ** n * d)))
    if t == "tras":
        return M("Si |A| = %s, ¿cuánto vale |A<sup>t</sup>|?" % sg(d), sg(d), W([sg(-d), nf(F(1, d)), "0", sg(d * d)]), "El determinante de la traspuesta es el mismo: <b>%s</b>." % sg(d))
    if t == "prod":
        e = R.choice([2, -3, 4, 5])
        return M("Si |A| = %s y |B| = %s (matrices %d × %d), ¿cuánto vale |A · B|?" % (sg(d), sg(e), n, n), sg(d * e), W([sg(d + e), sg(d * e * n), "no se puede saber", sg(-d * e)]), "|A · B| = |A| · |B| = <b>%s</b>." % sg(d * e))
    if t == "inv":
        return M("Si |A| = %s, ¿cuánto vale |A⁻¹|?" % sg(d), nf(F(1, d)), W([sg(-d), sg(d), nf(F(-1, d)) if d != -1 else "0", "1"]), "|A⁻¹| = 1/|A| = <b>%s</b>." % nf(F(1, d)))
    if t == "filas":
        k = R.choice(["cambio", "cero", "iguales", "suma"])
        q, a, w = {"cambio": ("Si en A (|A| = %s) se intercambian dos filas, ¿cuánto vale el nuevo determinante?" % sg(d), sg(-d), [sg(d), "0", sg(2 * d)]),
                   "cero": ("Si una matriz tiene una fila de ceros, su determinante es…", "0", ["1", "no se puede calcular", "el producto de la diagonal"]),
                   "iguales": ("Si una matriz tiene dos filas iguales (o proporcionales), su determinante es…", "0", ["1", "el doble", "negativo"]),
                   "suma": ("Si a una fila se le suma otra multiplicada por un número, el determinante…", "no cambia", ["se multiplica por ese número", "cambia de signo", "se anula"])}[k]
        return M(q, a, w, "Propiedad de los determinantes: <b>%s</b>." % a)
    q, a, w = R.choice([("|A + B| es igual a…", "en general, no se puede calcular solo con |A| y |B|", ["|A| + |B|", "|A| · |B|", "0"]), ("Una matriz cuadrada tiene inversa si y solo si…", "|A| ≠ 0", ["|A| = 0", "|A| = 1", "es simétrica"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_adjuntos():
    A = rm(3, -3, 4)
    i, j = R.randint(0, 2), R.randint(0, 2)
    m = det2(minor(A, i, j))
    adj = (-1) ** (i + j) * m
    t = R.choice(["adj", "adj", "menor"])
    if t == "menor":
        return M("En A = %s, calcula el menor complementario α<sub>%d%d</sub>." % (mat(A), i + 1, j + 1), sg(m), W([sg(-m) if m else "1", sg(A[i][j]), sg(m + A[i][j]), sg(det3(A))]), "Tachamos la fila %d y la columna %d: %s = <b>%s</b>." % (i + 1, j + 1, det_h(minor(A, i, j)), sg(m)))
    return M("En A = %s, calcula el adjunto A<sub>%d%d</sub>." % (mat(A), i + 1, j + 1), sg(adj), W([sg(-adj) if adj else "1", sg(A[i][j] * adj) if A[i][j] not in (0, 1) else sg(adj + 2), sg(det3(A)) if det3(A) != adj else sg(adj - 1)]),
             "A<sub>ij</sub> = (−1)<sup>i+j</sup> · α<sub>ij</sub> = %s · %s = <b>%s</b>." % ("+1" if (i + j) % 2 == 0 else "−1", par(m), sg(adj)))


def s_inv3():
    t = R.choice(["existe", "existe", "elem", "rango"])
    if t == "existe":
        a, b = R.randint(1, 3), R.randint(-2, 3)
        # [[1, 0, a],[0, k, b],[1, 1, 1]] det = 1(k − b) − 0 + a(0 − k) = k − b − a k = k(1 − a) − b
        if a == 1:
            return None
        kk = F(b, 1 - a)
        return M("¿Para qué valor de k no tiene inversa A = %s?" % mat([[1, 0, a], [0, "k", b], [1, 1, 1]]), "k = %s" % nf(kk), W(["k = %s" % nf(-kk) if kk else "k = 1", "k = %s" % nf(F(b, a)), "k = %s" % nf(F(-b, 1 + a)), "k = 0" if kk else "k = 2"]),
                 "|A| = k − %s − %sk = 0 → <b>k = %s</b>." % (par(b), a, nf(kk)))
    if t == "elem":
        while True:
            A = rm(3, -2, 3)
            d = det3(A)
            if d in (1, -1, 2, -2):
                break
        i, j = R.randint(0, 2), R.randint(0, 2)
        # (A⁻¹)_ij = A_ji / |A|
        adj_ji = (-1) ** (i + j) * det2(minor(A, j, i))
        v = F(adj_ji, d)
        wrong = F((-1) ** (i + j) * det2(minor(A, i, j)), d)
        return M("Si A = %s, ¿cuánto vale el elemento (%d, %d) de A⁻¹?" % (mat(A), i + 1, j + 1), nf(v), W([nf(wrong) if wrong != v else nf(v + 1), nf(-v) if v else "1", nf(F(1, A[i][j])) if A[i][j] else "0", sg(adj_ji)]),
                 "A⁻¹ = (1/|A|) · Adj(A)<sup>t</sup>; |A| = %s y el adjunto que va en esa posición es A<sub>%d%d</sub> = %s: <b>%s</b>." % (sg(d), j + 1, i + 1, sg(adj_ji), nf(v)))
    a = R.randint(1, 4)
    k = R.choice([1, 2, 3])
    if k == 3:
        A = [[1, 0, 1], [0, 1, 2], [R.randint(1, 3), 1, R.randint(-2, 2)]]
        if det3(A) == 0:
            return None
    elif k == 2:
        A = [[1, a, 2], [0, 1, 1], [1, a + 1, 3]]
    else:
        A = [[1, a, 2], [2, 2 * a, 4], [-1, -a, -2]]
    return M("¿Cuál es el rango de A = %s?" % mat(A), str(k), [str(x) for x in (0, 1, 2, 3) if x != k], "%s: <b>%d</b>." % ("|A| ≠ 0" if k == 3 else "|A| = 0 y hay un menor de orden 2 no nulo" if k == 2 else "todas las filas son proporcionales", k))


seen = set()
sets = [("Determinantes de orden 2", mix(R, seen, [(s_orden2, 20)])), ("Regla de Sarrus", mix(R, seen, [(s_sarrus, 20)])), ("Propiedades", mix(R, seen, [(s_propiedades, 20)])),
        ("Menores y adjuntos", mix(R, seen, [(s_adjuntos, 20)])), ("Inversa y rango con determinantes", mix(R, seen, [(s_inv3, 20)]))]
think = ["<b>Orden 2</b>: |a b; c d| = ad − bc. <b>Orden 3</b>: regla de Sarrus (tres productos con +, tres con −) o desarrollo por una fila.",
         "<b>Adjunto</b>: A<sub>ij</sub> = (−1)<sup>i+j</sup> · α<sub>ij</sub>, donde α<sub>ij</sub> es el determinante que queda al tachar la fila i y la columna j.",
         "<b>Propiedades</b>: |A<sup>t</sup>| = |A|; |A · B| = |A| · |B|; |kA| = kⁿ|A|; si se cambian dos filas, cambia el signo; dos filas proporcionales → 0.",
         "A tiene inversa ⇔ |A| ≠ 0, y A⁻¹ = (1/|A|) · Adj(A)<sup>t</sup>."]
ex = [("|1 2 0; 3 1 2; 0 1 1|", ["(1 + 0 + 0) − (0 + 2 + 6)"], "−7")]
mist = [["|2A| = 2|A| en 3 × 3", "|2A| = 2³|A| = 8|A|."], ["Olvidar el signo del adjunto", "(−1)<sup>i+j</sup>: + − + en la primera fila."], ["|A + B| = |A| + |B|", "No es cierto en general."]]
body = L(think, ex, mist)
faq = [("¿Qué significa que el determinante sea 0?", "Que las filas (o columnas) son linealmente dependientes: la matriz no tiene inversa y su rango no es máximo."),
       ("¿Para qué se usan los determinantes?", "Para saber si una matriz tiene inversa, calcular rangos, resolver sistemas (Cramer) y calcular áreas y volúmenes.")]
unit(2, R, "determinantes", "A", "Determinantes: cálculo de orden 2 y 3, propiedades, adjuntos, cálculo de la matriz inversa y del rango",
     "Determinantes", "Determinantes", "Fichas de Matemáticas II (2.º de Bachillerato): determinantes de orden 2 y 3, Sarrus, propiedades, adjuntos, matriz inversa y rango. 100 ejercicios con soluciones.",
     "|A| ≠ 0 ⇔ A tiene inversa", "|kA| = kⁿ · |A|", body, faq, sets, 2)
