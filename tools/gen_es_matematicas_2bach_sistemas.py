# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Sistemas de ecuaciones lineales (Sentido algebraico)
Expresión matricial, teorema de Rouché-Frobenius, regla de Cramer, discusión de sistemas con un parámetro, sistemas homogéneos, problemas.
Errores: comparar el rango con el número de ecuaciones en lugar de con el de incógnitas, olvidar que Cramer exige |A| ≠ 0, perder el caso del parámetro que anula |A|.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, mat, det_h, nf, det2, det3, W, par, MINUS

R = random.Random(52003)
VARS = ("x", "y", "z")


def eq(cs, rhs):
    return "%s = %s" % (E(*[(c, v) for c, v in zip(cs, VARS)]), rhs if isinstance(rhs, str) else sg(rhs))


def sys_(rows):
    return "<span class='sys'>%s</span>" % "<br>".join(eq(cs, r) for cs, r in rows)


def T(*v):
    return "(%s)" % ", ".join(nf(x) for x in v)


def s_matricial():
    t = R.choice(["A", "amp", "escribe"])
    rows = [([R.randint(-3, 4) for _ in range(3)], R.randint(-6, 8)) for _ in range(3)]
    if any(all(c == 0 for c in cs) for cs, _ in rows):
        return None
    A = [cs for cs, _ in rows]
    if t == "A":
        return M("¿Cuál es la matriz de coeficientes del sistema? %s" % sys_(rows), mat(A), W([mat([cs + [r] for cs, r in rows]), mat([list(c) for c in zip(*A)]), mat([[r] for _, r in rows])]), "Se escriben los coeficientes de x, y, z por filas: <b>%s</b>." % mat(A))
    if t == "amp":
        return M("¿Cuál es la matriz ampliada del sistema? %s" % sys_(rows), mat([cs + [r] for cs, r in rows]), W([mat(A), mat([[r] + cs for cs, r in rows]), mat([cs + [-r] for cs, r in rows])]), "Se añade la columna de términos independientes: <b>%s</b>." % mat([cs + [r] for cs, r in rows]))
    A2 = [[R.randint(-3, 4) for _ in range(2)] for _ in range(2)]
    b = [R.randint(-6, 6) for _ in range(2)]
    rows2 = [(A2[i] + [0], b[i]) for i in range(2)]
    s = "<span class='sys'>%s</span>" % "<br>".join("%s = %s" % (E((A2[i][0], "x"), (A2[i][1], "y")), sg(b[i])) for i in range(2))
    ok = "%s · %s = %s" % (mat(A2), mat([["x"], ["y"]]), mat([[b[0]], [b[1]]]))
    return M("¿Cómo se escribe en forma matricial el sistema? %s" % s, ok, W(["%s · %s = %s" % (mat([list(c) for c in zip(*A2)]), mat([["x"], ["y"]]), mat([[b[0]], [b[1]]])), "%s · %s = %s" % (mat([["x"], ["y"]]), mat(A2), mat([[b[0]], [b[1]]])), "%s · %s = %s" % (mat(A2), mat([[b[0]], [b[1]]]), mat([["x"], ["y"]]))]), "A · X = B: <b>%s</b>." % ok)


def s_rouche():
    t = R.choice(["rangos", "rangos", "rangos", "teo"])
    if t == "rangos":
        n = R.choice([2, 3, 4])
        m = R.choice([2, 3, 4])
        rA = R.randint(1, min(m, n))
        rB = R.choice([rA, rA, rA + 1]) if rA < m else rA
        ok = "compatible determinado" if rA == rB == n else "compatible indeterminado" if rA == rB else "incompatible"
        par_ = n - rA
        extra = " (con %d parámetro%s)" % (par_, "s" if par_ > 1 else "") if ok == "compatible indeterminado" else ""
        return M("Un sistema de %d ecuaciones con %d incógnitas tiene rango(A) = %d y rango(A*) = %d. ¿Cómo es?" % (m, n, rA, rB), ok + extra, [o for o in ["compatible determinado", "compatible indeterminado", "incompatible", "no se puede saber"] if o != ok],
                 "Rouché-Frobenius: %s → <b>%s</b>%s." % ("rangos iguales al número de incógnitas" if ok == "compatible determinado" else "rangos iguales, menores que el número de incógnitas" if ok == "compatible indeterminado" else "rangos distintos", ok, extra))
    q, a, w = R.choice([("Según Rouché-Frobenius, un sistema es compatible si…", "rango(A) = rango(A*)", ["rango(A) = 3", "|A| = 0", "rango(A*) &gt; rango(A)"]),
                        ("Si rango(A) = rango(A*) = 2 y hay 3 incógnitas, la solución depende de…", "1 parámetro", ["2 parámetros", "ningún parámetro", "3 parámetros"]),
                        ("Un sistema homogéneo (términos independientes 0) siempre es…", "compatible", ["incompatible", "compatible determinado", "indeterminado"]),
                        ("Si |A| ≠ 0 en un sistema de 3 × 3, el sistema es…", "compatible determinado", ["incompatible", "compatible indeterminado", "no se puede saber"]),
                        ("Si |A| = 0 en un sistema homogéneo de 3 × 3, entonces…", "tiene infinitas soluciones", ["solo tiene la solución (0, 0, 0)", "es incompatible", "no tiene solución"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_cramer():
    t = R.choice(["2", "2", "3", "3", "x3"])
    if t == "2":
        while True:
            A = [[R.randint(-4, 5) for _ in range(2)] for _ in range(2)]
            if det2(A) not in (0,):
                break
        x, y = R.randint(-5, 6), R.randint(-5, 6)
        b = [A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y]
        s = "<span class='sys'>%s<br>%s</span>" % ("%s = %s" % (E((A[0][0], "x"), (A[0][1], "y")), sg(b[0])), "%s = %s" % (E((A[1][0], "x"), (A[1][1], "y")), sg(b[1])))
        d = det2(A)
        dx = det2([[b[0], A[0][1]], [b[1], A[1][1]]])
        return M("Resuelve por Cramer: %s" % s, "x = %s, y = %s" % (sg(x), sg(y)), W(["x = %s, y = %s" % (sg(y), sg(x)), "x = %s, y = %s" % (sg(-x), sg(y)), "x = %s, y = %s" % (sg(x), sg(-y)), "x = %s, y = %s" % (sg(x + 1), sg(y))]),
                 "|A| = %s; x = |A<sub>x</sub>|/|A| = %s/%s = %s; y análogamente. <b>x = %s, y = %s</b>." % (sg(d), sg(dx), par(d), sg(x), sg(x), sg(y)))
    while True:
        A = [[R.randint(-2, 3) for _ in range(3)] for _ in range(3)]
        d = det3(A)
        if d not in (0,) and abs(d) <= 12:
            break
    sol = [R.randint(-4, 5) for _ in range(3)]
    b = [sum(c * v for c, v in zip(r, sol)) for r in A]
    rows = [(A[i], b[i]) for i in range(3)]
    if t == "x3":
        k = R.randint(0, 2)
        Ak = [[b[i] if j == k else A[i][j] for j in range(3)] for i in range(3)]
        return M("En el sistema %s ¿cuánto vale %s por Cramer?" % (sys_(rows), VARS[k]), "%s = %s" % (VARS[k], sg(sol[k])), W(["%s = %s" % (VARS[k], sg(sol[(k + 1) % 3])) if sol[(k + 1) % 3] != sol[k] else "%s = %s" % (VARS[k], sg(sol[k] + 2)), "%s = %s" % (VARS[k], sg(-sol[k])) if sol[k] else "%s = 1" % VARS[k], "%s = %s" % (VARS[k], sg(det3(Ak))) if det3(Ak) != sol[k] else "%s = %s" % (VARS[k], sg(sol[k] - 1))]),
                 "|A| = %s y |A<sub>%s</sub>| = %s: %s = %s/%s = <b>%s</b>." % (sg(d), VARS[k], sg(det3(Ak)), VARS[k], sg(det3(Ak)), par(d), sg(sol[k])))
    return M("Resuelve el sistema: %s" % sys_(rows), T(*sol), W([T(sol[1], sol[0], sol[2]), T(-sol[0], sol[1], sol[2]), T(sol[0], sol[1], -sol[2]) if sol[2] else T(sol[0], sol[1], 1), T(sol[2], sol[1], sol[0])]), "|A| = %s ≠ 0: es compatible determinado; por Cramer o Gauss, <b>%s</b>." % (sg(d), T(*sol)))


def s_discutir():
    t = R.choice(["d1", "d1", "d2", "homog"])
    if t == "d1":
        a = R.randint(1, 4)
        b = R.randint(1, 6)
        c = R.choice([x for x in range(-5, 7) if x != a * b])
        # x + a y = b ; m x + ... ; sistema 2x2: x + a y = b ; 2x + 2a y = m? (parámetro en el término)
        k = R.choice(["coef", "term"])
        if k == "term":
            s = "<span class='sys'>%s = %d<br>%s = m</span>" % (E((1, "x"), (a, "y")), b, E((2, "x"), (2 * a, "y")))
            return M("Discute el sistema según m: %s" % s, "m = %d: compatible indeterminado; m ≠ %d: incompatible" % (2 * b, 2 * b),
                     ["m = %d: compatible determinado; m ≠ %d: incompatible" % (2 * b, 2 * b), "siempre compatible determinado", "m = %d: incompatible; m ≠ %d: compatible indeterminado" % (2 * b, 2 * b)],
                     "rango(A) = 1. Si m = %d, rango(A*) = 1 (infinitas soluciones); si no, rango(A*) = 2 (sin solución)." % (2 * b))
        s = "<span class='sys'>%s = %d<br>%s = %d</span>" % (E((1, "x"), (a, "y")), b, "2x + my", c)
        return M("Discute el sistema según m: %s" % s, "m ≠ %d: compatible determinado; m = %d: incompatible" % (2 * a, 2 * a), ["m ≠ %d: compatible determinado; m = %d: compatible indeterminado" % (2 * a, 2 * a), "siempre compatible determinado", "m = %d: compatible determinado" % (2 * a)],
                 "|A| = m − %d. Si m ≠ %d, |A| ≠ 0 → compatible determinado. Si m = %d, las ecuaciones son incompatibles (%d ≠ %d). " % (2 * a, 2 * a, 2 * a, c, 2 * b))
    if t == "d2":
        a = R.randint(1, 3)
        # [[1,1,1],[1,m,1],[1,1,m]] det = (m−1)²
        b = R.randint(1, 5)
        s = sys_([([1, 1, 1], b), ([1, "m", 1], b), ([1, 1, "m"], b)]) if False else "<span class='sys'>x + y + z = %d<br>x + my + z = %d<br>x + y + mz = %d</span>" % (b, b, b)
        return M("¿Para qué valores de m es compatible determinado el sistema? %s" % s, "m ≠ 1", ["m = 1", "m ≠ 0", "para todo m"], "|A| = (m − 1)²: se anula solo en m = 1. <b>m ≠ 1</b> (para m = 1 es compatible indeterminado).")
    a, b = R.randint(1, 4), R.randint(-3, 4)
    s = "<span class='sys'>x + %sy = 0<br>%sx + my = 0</span>" % ("" if a == 1 else a, sg(b) if b != 1 else "") if b else None
    if not s:
        return None
    return M("¿Para qué valor de m tiene el sistema homogéneo soluciones distintas de (0, 0)? %s" % s, "m = %s" % sg(a * b), W(["m = %s" % sg(-a * b), "m = 0", "m = %s" % nf(F(b, a)), "m = %s" % sg(a * b + 1)]), "Hace falta |A| = 0: m − %s = 0 → <b>m = %s</b>." % (par(a * b), sg(a * b)))


def s_problema():
    t = R.choice(["compra", "edades", "mezcla", "inversion"])
    a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    if t == "compra":
        r1, r2, r3 = a + b + c, 2 * a + b, b + 2 * c
        return M("Un café, un zumo y un bocadillo cuestan %d €. Dos cafés y un zumo, %d €. Un zumo y dos bocadillos, %d €. ¿Cuánto cuesta cada cosa (café, zumo, bocadillo)?" % (r1, r2, r3), "%d €, %d € y %d €" % (a, b, c), W(["%d €, %d € y %d €" % v for v in ((b, a, c), (a, c, b), (c, b, a), (a + 1, b - 1, c))]), "x + y + z = %d; 2x + y = %d; y + 2z = %d → <b>%d €, %d € y %d €</b>." % (r1, r2, r3, a, b, c))
    if t == "edades":
        a, b = R.randint(5, 15), R.randint(30, 45)
        k = R.randint(3, 10)
        return M("La edad de una madre es ahora %s veces la de su hijo... Si la madre tiene %d años y el hijo %d, ¿cuántos años faltan para que la suma de sus edades sea %d?" % ("varias", b, a, a + b + 2 * k), "%d" % k, W(["%d" % (2 * k), "%d" % (k + 1), "%d" % (a + b)]), "%d + x + %d + x = %d → <b>x = %d</b>." % (a, b, a + b + 2 * k, k)) if False else None
    if t == "mezcla":
        x, y, z = R.randint(1, 6) * 10, R.randint(1, 6) * 10, R.randint(1, 6) * 10
        p = (3, 5, 8)
        tot = x + y + z
        coste = 3 * x + 5 * y + 8 * z
        return M("Se mezclan tres tipos de café de 3 €, 5 € y 8 € el kilo para obtener %d kg que cuestan %d €. Del tercer tipo hay %d kg más que del primero. ¿Cuántos kg hay de cada tipo?" % (tot, coste, z - x) if z > x else None,
                 "%d, %d y %d kg" % (x, y, z), W(["%d, %d y %d kg" % v for v in ((y, x, z), (z, y, x), (x + 10, y - 10, z), (x, y + 10, z - 10))]), "x + y + z = %d; 3x + 5y + 8z = %d; z = x + %d → <b>%d, %d y %d kg</b>." % (tot, coste, z - x, x, y, z)) if z > x else None
    c1, c2 = R.sample([1000, 2000, 3000, 4000], 2)
    c3 = c1 + c2
    I = c1 * 2 + c2 * 3 + c3 * 5
    return M("Se invierten %s € en tres fondos al 2 %%, 3 %% y 5 %% anual y se obtienen %s € de intereses. En el tercero se invierte lo mismo que en los otros dos juntos%s. ¿Cuánto se invierte en cada fondo?" % (num(c1 + c2 + c3), num(I // 100), "") if c3 == c1 + c2 else None,
             "%s €, %s € y %s €" % (num(c1), num(c2), num(c3)), W(["%s €, %s € y %s €" % (num(c2), num(c1), num(c3)), "%s €, %s € y %s €" % (num(c3), num(c2), num(c1)), "%s €, %s € y %s €" % (num(c1), num(c3), num(c2)), "%s €, %s € y %s €" % (num(c1 + 500), num(c2 - 500), num(c3))]),
             "x + y + z = %s; 0,02x + 0,03y + 0,05z = %s; z = x + y → <b>%s €, %s € y %s €</b>." % (num(c1 + c2 + c3), num(I // 100), num(c1), num(c2), num(c3))) if c3 == c1 + c2 else None


seen = set()
sets = [("Expresión matricial", mix(R, seen, [(s_matricial, 20)])), ("Teorema de Rouché-Frobenius", mix(R, seen, [(s_rouche, 20)])), ("Regla de Cramer", mix(R, seen, [(s_cramer, 20)])),
        ("Discusión con parámetros", mix(R, seen, [(s_discutir, 12), (s_rouche, 8)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["Un sistema se escribe A · X = B. A es la matriz de coeficientes y A* (ampliada) añade la columna B.",
         "<b>Rouché-Frobenius</b>: si rango(A) = rango(A*) = n.º de incógnitas, compatible determinado; si rango(A) = rango(A*) &lt; n.º de incógnitas, compatible indeterminado; si rango(A) ≠ rango(A*), incompatible.",
         "<b>Cramer</b> (si |A| ≠ 0): cada incógnita es |A<sub>i</sub>|/|A|, donde A<sub>i</sub> cambia la columna i por los términos independientes.",
         "Para <b>discutir</b> con un parámetro, se buscan los valores que anulan |A| y se estudia cada caso aparte."]
ex = [("x + y = 3; 2x − y = 0", ["|A| = −3", "x = |3 1; 0 −1| / (−3) = 1"], "x = 1, y = 2")]
mist = [["Comparar el rango con el n.º de ecuaciones", "Se compara con el número de incógnitas."], ["Usar Cramer con |A| = 0", "Cramer solo vale si |A| ≠ 0."], ["Olvidar el caso especial", "Estudia aparte el valor del parámetro que anula |A|."]]
body = L(think, ex, mist)
faq = [("¿Qué método es mejor, Gauss o Cramer?", "Gauss sirve siempre y es más rápido con muchas incógnitas; Cramer da fórmulas directas cuando |A| ≠ 0."),
       ("¿Qué es discutir un sistema?", "Decir, según el valor de un parámetro, si tiene una solución, infinitas o ninguna.")]
unit(2, R, "sistemas-de-ecuaciones-lineales", "A", "Sistemas de ecuaciones lineales: expresión matricial, teorema de Rouché-Frobenius, regla de Cramer, discusión con parámetros y resolución de problemas",
     "Sistemas de ecuaciones lineales", "Sistemas lineales", "Fichas de Matemáticas II (2.º de Bachillerato): forma matricial, Rouché-Frobenius, regla de Cramer, discusión con parámetros y problemas. 100 ejercicios con soluciones.",
     "Compatible ⇔ rango(A) = rango(A*)", "Cramer: x = |Aₓ| / |A| (si |A| ≠ 0)", body, faq, sets, 3)
