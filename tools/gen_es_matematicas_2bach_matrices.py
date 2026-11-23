# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Matrices (Sentido algebraico)
Tipos y dimensión, suma y producto por un número, producto de matrices, traspuesta, potencias, matriz inversa (2×2 y por Gauss), ecuaciones matriciales, rango.
Errores: A · B = B · A, multiplicar elemento a elemento, (A · B)⁻¹ = A⁻¹ · B⁻¹, despejar X «dividiendo» entre una matriz.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, mat, nf, det2, mmul, tr, W, MINUS, par

R = random.Random(52001)


def rm(r, c, lo=-4, hi=5):
    return [[R.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def add(a, b, k=1):
    return [[x + k * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scal(k, a):
    return [[k * x for x in r] for r in a]


def s_basico():
    t = R.choice(["dim", "elem", "suma", "comb", "tras"])
    if t == "dim":
        r, c = R.randint(1, 4), R.randint(1, 4)
        A = rm(r, c)
        return M("¿Qué dimensión tiene la matriz A = %s?" % mat(A), "%d × %d" % (r, c), W(["%d × %d" % (c, r) if r != c else "%d × %d" % (r, c + 1), "%d" % (r * c), "%d × %d" % (r + 1, c)]), "Filas × columnas: <b>%d × %d</b>." % (r, c))
    if t == "elem":
        A = rm(3, 3)
        i, j = R.randint(1, 3), R.randint(1, 3)
        if i == j:
            return None
        return M("En A = %s, ¿cuánto vale a<sub>%d%d</sub>?" % (mat(A), i, j), sg(A[i - 1][j - 1]), W([sg(A[j - 1][i - 1]), sg(A[i - 1][i - 1]), sg(A[j - 1][j - 1]), sg(A[i - 1][j - 1] + 1)]), "a<sub>%d%d</sub> está en la fila %d, columna %d: <b>%s</b>." % (i, j, i, j, sg(A[i - 1][j - 1])))
    A, B = rm(2, 2), rm(2, 2)
    if t == "suma":
        return M("Calcula A + B con A = %s y B = %s." % (mat(A), mat(B)), mat(add(A, B)), W([mat(add(A, B, -1)), mat([[a * b for a, b in zip(x, y)] for x, y in zip(A, B)]), mat(tr(add(A, B)))]), "Sumamos elemento a elemento: <b>%s</b>." % mat(add(A, B)))
    if t == "comb":
        k = R.choice([2, 3, -2])
        res = add(scal(k, A), B, -1)
        return M("Calcula %sA − B con A = %s y B = %s." % (sg(k), mat(A), mat(B)), mat(res), W([mat(add(scal(k, A), B)), mat(scal(k, add(A, B, -1))), mat(add(A, scal(k, B), -1))]), "Multiplicamos A por %s y restamos B: <b>%s</b>." % (sg(k), mat(res)))
    A = rm(2, 3)
    return M("¿Cuál es la traspuesta de A = %s?" % mat(A), mat(tr(A)), W([mat([r[::-1] for r in A]), mat([list(reversed(c)) for c in tr(A)]), mat(scal(-1, A))]), "Las filas pasan a ser columnas: <b>%s</b>." % mat(tr(A)))


def s_producto():
    t = R.choice(["22", "22", "23", "dim", "conm"])
    if t == "22":
        A, B = rm(2, 2, -3, 4), rm(2, 2, -3, 4)
        P = mmul(A, B)
        return M("Calcula A · B con A = %s y B = %s." % (mat(A), mat(B)), mat(P), W([mat(mmul(B, A)), mat([[a * b for a, b in zip(x, y)] for x, y in zip(A, B)]), mat(tr(P))]), "Fila por columna: c<sub>11</sub> = %s · %s + %s · %s = %s, … <b>%s</b>." % (sg(A[0][0]), par(B[0][0]), par(A[0][1]), par(B[1][0]), sg(P[0][0]), mat(P)))
    if t == "23":
        A, B = rm(2, 3, -2, 3), rm(3, 1, -2, 3)
        P = mmul(A, B)
        return M("Calcula A · B con A = %s y B = %s." % (mat(A), mat(B)), mat(P), W([mat([[P[1][0]], [P[0][0]]]) if P[0][0] != P[1][0] else mat([[P[0][0] + 1], [P[1][0]]]), mat([[sum(A[0])], [sum(A[1])]]), "no se puede multiplicar"]), "(2 × 3) · (3 × 1) = 2 × 1: <b>%s</b>." % mat(P))
    if t == "dim":
        m, n, p = R.randint(1, 4), R.randint(1, 4), R.randint(1, 4)
        q = R.choice([n, n, R.randint(1, 4)])
        ok = "%d × %d" % (m, p) if q == n else "no se pueden multiplicar"
        return M("Si A es %d × %d y B es %d × %d, ¿qué dimensión tiene A · B?" % (m, n, q, p), ok, W(["%d × %d" % (n, q), "%d × %d" % (p, m) if p != m else "%d × %d" % (m, n), "no se pueden multiplicar" if q == n else "%d × %d" % (m, p), "%d × %d" % (m * n, q * p)]),
                 "Las columnas de A deben coincidir con las filas de B: <b>%s</b>." % ok)
    q, a, w = R.choice([("En general, ¿A · B = B · A?", "no, el producto de matrices no es conmutativo", ["sí, siempre", "solo si son 2 × 2", "solo si son simétricas"]),
                        ("¿Qué matriz es el elemento neutro del producto?", "la identidad I", ["la matriz nula", "la traspuesta", "la inversa"]),
                        ("(A · B)<sup>t</sup> es igual a…", "B<sup>t</sup> · A<sup>t</sup>", ["A<sup>t</sup> · B<sup>t</sup>", "A · B", "B · A"]),
                        ("(A · B)⁻¹ es igual a…", "B⁻¹ · A⁻¹", ["A⁻¹ · B⁻¹", "A · B", "(B · A)<sup>t</sup>"]),
                        ("Una matriz es simétrica si…", "A<sup>t</sup> = A", ["A⁻¹ = A", "A² = A", "A<sup>t</sup> = −A"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_potencias():
    t = R.choice(["cuad", "cuad", "patron", "patron"])
    if t == "cuad":
        A = rm(2, 2, -3, 3)
        return M("Calcula A² con A = %s." % mat(A), mat(mmul(A, A)), W([mat([[x * x for x in r] for r in A]), mat(scal(2, A)), mat(tr(mmul(A, A)))]), "A² = A · A (no se elevan los elementos): <b>%s</b>." % mat(mmul(A, A)))
    k = R.choice(["tri", "rot", "nil"])
    n = R.randint(3, 12)
    if k == "tri":
        a = R.randint(1, 4)
        A = [[1, a], [0, 1]]
        ok = mat([[1, n * a], [0, 1]])
        return M("Calcula A<sup>%d</sup> con A = %s." % (n, mat(A)), ok, W([mat([[1, a ** n], [0, 1]]), mat([[n, n * a], [0, n]]), mat([[1, a + n], [0, 1]])]), "A² = %s, A³ = %s… → A<sup>n</sup> = %s: <b>%s</b>." % (mat([[1, 2 * a], [0, 1]]), mat([[1, 3 * a], [0, 1]]), mat([[1, "%dn" % a if a > 1 else "n"], [0, 1]]), ok))
    if k == "rot":
        A = [[0, -1], [1, 0]]
        P = [[1, 0], [0, 1]]
        for _ in range(n):
            P = mmul(P, A)
        return M("Calcula A<sup>%d</sup> con A = %s." % (n, mat(A)), mat(P), W([mat(A), mat(scal(-1, P)), mat(tr(P)) if tr(P) != P else mat([[0, 1], [1, 0]])]), "A⁴ = I; %d = 4 · %d + %d → A<sup>%d</sup> = A<sup>%d</sup>: <b>%s</b>." % (n, n // 4, n % 4, n, n % 4, mat(P)))
    a = R.randint(1, 5)
    A = [[0, a], [0, 0]]
    return M("Calcula A<sup>%d</sup> con A = %s." % (n, mat(A)), mat([[0, 0], [0, 0]]), [mat(A), mat([[0, a ** n], [0, 0]]), mat([[0, n * a], [0, 0]])], "A² = 0 (matriz nula), así que todas las potencias siguientes también: <b>la matriz nula</b>.")


def s_inversa():
    t = R.choice(["22", "22", "22", "exist", "comprobar"])
    while True:
        A = rm(2, 2, -4, 5)
        d = det2(A)
        if d in (1, -1, 2, -2, 3, -3) or (t == "exist" and d == 0):
            break
    if t == "exist":
        k = R.randint(-4, 5)
        a, b, c = R.randint(1, 4), R.randint(1, 4), R.randint(1, 4)
        # det [[a, b],[c, k]] = a k − b c = 0 → k = bc/a
        kk = F(b * c, a)
        return M("¿Para qué valor de k no tiene inversa A = %s?" % mat([[a, b], [c, "k"]]), "k = %s" % nf(kk), W(["k = %s" % nf(-kk), "k = %s" % nf(F(a * c, b)) if F(a * c, b) != kk else "k = %s" % nf(kk + 1), "k = 0", "k = %s" % nf(F(a, b * c))]), "|A| = %dk − %d = 0 → <b>k = %s</b>." % (a, b * c, nf(kk)))
    inv = [[F(A[1][1], d), F(-A[0][1], d)], [F(-A[1][0], d), F(A[0][0], d)]]
    if t == "comprobar":
        B = scal(d, inv)
        B = [[int(x) for x in r] for r in B]
        return M("Si A = %s, ¿cuál es A⁻¹?" % mat(A), mat(inv), W([mat(B), mat(tr(inv)), mat([[F(A[0][0], d), F(A[0][1], d)], [F(A[1][0], d), F(A[1][1], d)]]), mat(scal(-1, inv)), mat(A)]), "A⁻¹ = (1/|A|) · Adj(A)<sup>t</sup> con |A| = %s: <b>%s</b>." % (sg(d), mat(inv)))
    return M("Calcula la inversa de A = %s." % mat(A), mat(inv), W([mat([[F(1, x) if x else 0 for x in r] for r in A]) if all(A[0]) and all(A[1]) else mat(tr(inv)), mat(scal(-1, inv)), mat([[F(A[1][1], d), F(A[0][1], d)], [F(A[1][0], d), F(A[0][0], d)]])]),
             "|A| = %s. Se cambian los elementos de la diagonal, se cambia el signo de los otros dos y se divide entre |A|: <b>%s</b>." % (sg(d), mat(inv)))


def s_ecuaciones():
    t = R.choice(["ax", "xa", "suma", "rango", "rango"])
    if t in ("ax", "xa"):
        while True:
            A = rm(2, 2, -3, 4)
            if det2(A) in (1, -1):
                break
        X = rm(2, 2, -3, 3)
        B = mmul(A, X) if t == "ax" else mmul(X, A)
        alt = mmul(X, A) if t == "ax" else mmul(A, X)
        return M("Resuelve %s con A = %s y B = %s." % ("A · X = B" if t == "ax" else "X · A = B", mat(A), mat(B)), "X = " + mat(X), W(["X = " + mat(mmul(B, [[A[1][1] * det2(A), -A[0][1] * det2(A)], [-A[1][0] * det2(A), A[0][0] * det2(A)]]) if t == "ax" else mmul([[A[1][1] * det2(A), -A[0][1] * det2(A)], [-A[1][0] * det2(A), A[0][0] * det2(A)]], B)),
                                                                                                                                       "X = " + mat(add(B, A, -1)), "X = " + mat(tr(X)), "X = " + mat(scal(-1, X)), "X = " + mat(alt) if alt != B else "X = " + mat(B)]),
                 "%s: <b>X = %s</b>." % ("X = A⁻¹ · B (A⁻¹ por la izquierda)" if t == "ax" else "X = B · A⁻¹ (A⁻¹ por la derecha)", mat(X)))
    if t == "suma":
        A, B = rm(2, 2), rm(2, 2)
        k = R.choice([2, 3])
        C = add(scal(k, add(A, A, 0)), B) if False else add(scal(k, A), B)
        return M("Resuelve %dX + B = C con B = %s y C = %s." % (k, mat(B), mat(C)), "X = " + mat(A), W(["X = " + mat(add(C, B)), "X = " + mat(add(C, B, -1)), "X = " + mat(scal(k, A)), "X = " + mat(tr(A)) if tr(A) != A else "X = " + mat(scal(-1, A))]), "X = (C − B)/%d = <b>%s</b>." % (k, mat(A)))
    k = R.choice([1, 2, 3])
    if k == 1:
        a, b, c = R.randint(1, 4), R.randint(-3, 3), R.randint(-3, 3)
        m1, m2 = R.choice([2, -1, 3]), R.choice([-2, 1, 4])
        A = [[a, b, c], [m1 * a, m1 * b, m1 * c], [m2 * a, m2 * b, m2 * c]]
    elif k == 2:
        r1, r2_ = [1, R.randint(-3, 3), R.randint(-3, 3)], [0, 1, R.randint(-3, 3)]
        p, q = R.choice([1, 2, -1]), R.choice([1, -2, 3])
        A = [r1, r2_, [p * x + q * y for x, y in zip(r1, r2_)]]
    else:
        A = [[1, R.randint(-3, 3), R.randint(-3, 3)], [0, 1, R.randint(-3, 3)], [0, 0, R.choice([1, 2, -1, 3])]]
        # mezclar filas
        a2 = R.randint(1, 3)
        A = [A[0], [x + a2 * y for x, y in zip(A[1], A[0])], A[2]]
    return M("¿Cuál es el rango de A = %s?" % mat(A), str(k), [str(x) for x in (1, 2, 3, 0) if x != k], "Número de filas linealmente independientes (por Gauss o con menores): <b>%d</b>." % k)


seen = set()
sets = [("Tipos y operaciones", mix(R, seen, [(s_basico, 20)])), ("Producto de matrices", mix(R, seen, [(s_producto, 20)])), ("Potencias", mix(R, seen, [(s_potencias, 20)])),
        ("Matriz inversa", mix(R, seen, [(s_inversa, 20)])), ("Ecuaciones matriciales y rango", mix(R, seen, [(s_ecuaciones, 20)]))]
think = ["Una <b>matriz</b> m × n tiene m filas y n columnas. Se suman elemento a elemento si tienen la misma dimensión.",
         "<b>Producto</b> A · B: fila de A por columna de B. Solo existe si las columnas de A coinciden con las filas de B. En general A · B ≠ B · A.",
         "<b>Inversa</b> de una matriz 2 × 2: A⁻¹ = (1/|A|) · [[d, −b], [−c, a]]. Existe solo si |A| ≠ 0.",
         "<b>Ecuaciones</b>: de A · X = B sale X = A⁻¹ · B (por la izquierda); de X · A = B, X = B · A⁻¹."]
ex = [("A = [[2, 1], [5, 3]]", ["|A| = 6 − 5 = 1"], "A⁻¹ = [[3, −1], [−5, 2]]")]
mist = [["A · B = B · A", "El producto no es conmutativo."], ["Multiplicar elemento a elemento", "Es fila por columna."], ["X = B / A", "No se divide: se multiplica por A⁻¹ en el lado correcto."]]
body = L(think, ex, mist)
faq = [("¿Para qué sirven las matrices?", "Para organizar datos, resolver sistemas de ecuaciones, describir transformaciones geométricas y en informática y economía."),
       ("¿Cuándo tiene inversa una matriz?", "Cuando es cuadrada y su determinante es distinto de 0 (rango máximo).")]
unit(2, R, "matrices", "A", "Matrices: operaciones, producto, potencias, matriz inversa, ecuaciones matriciales y rango",
     "Matrices", "Matrices", "Fichas de Matemáticas II (2.º de Bachillerato): operaciones con matrices, producto, traspuesta, potencias, inversa, ecuaciones matriciales y rango. 100 ejercicios.",
     "A · B ≠ B · A", "A · X = B → X = A⁻¹ · B", body, faq, sets, 1)
