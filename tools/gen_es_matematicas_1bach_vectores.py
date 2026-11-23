# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Vectores en el plano (Sentido espacial)
Coordenadas y operaciones, módulo y vector unitario, combinación lineal y bases, producto escalar, ángulo entre vectores, perpendicularidad y proyección.
Errores: confundir producto escalar (un número) con vector, olvidar dividir entre los módulos en el ángulo, u · v = 0 significa perpendiculares, no paralelos.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, raiz, nf, r2, V, kosy, BLUE, RED, W, MINUS

R = random.Random(51007)


def rv(lo=-6, hi=6):
    while True:
        a, b = R.randint(lo, hi), R.randint(lo, hi)
        if a or b:
            return a, b


def s_operaciones():
    u, v = rv(), rv()
    t = R.choice(["comb", "comb", "ab", "medio", "extremo"])
    if t == "comb":
        k, m = R.choice([2, 3, -2, -1]), R.choice([1, 2, -3, -1])
        r = (k * u[0] + m * v[0], k * u[1] + m * v[1])
        name = "%su %s %sv" % ("" if k == 1 else MINUS if k == -1 else sg(k), "+" if m > 0 else "−", "" if abs(m) == 1 else abs(m))
        return M("Si u = %s y v = %s, calcula %s." % (V(*u), V(*v), name), V(*r), W([V(k * u[0] - m * v[0], k * u[1] - m * v[1]), V(k * u[0] + v[0], k * u[1] + v[1]), V(u[0] + m * v[0], u[1] + m * v[1]), V(r[1], r[0])]), "Operamos coordenada a coordenada: <b>%s</b>." % V(*r))
    A, B = rv(-8, 8), rv(-8, 8)
    if t == "ab":
        return M("Halla las coordenadas del vector AB con A%s y B%s." % (V(*A), V(*B)), V(B[0] - A[0], B[1] - A[1]), W([V(A[0] - B[0], A[1] - B[1]), V(A[0] + B[0], A[1] + B[1]), V(B[1] - A[1], B[0] - A[0])]), "AB = B − A = <b>%s</b>." % V(B[0] - A[0], B[1] - A[1]))
    if t == "medio":
        m = (F(A[0] + B[0], 2), F(A[1] + B[1], 2))
        return M("Halla el punto medio de A%s y B%s." % (V(*A), V(*B)), V(*m), W([V(B[0] - A[0], B[1] - A[1]), V(F(B[0] - A[0], 2), F(B[1] - A[1], 2)), V(A[0] + B[0], A[1] + B[1])]), "M = (A + B)/2 = <b>%s</b>." % V(*m))
    w = rv()
    return M("Si A%s y AB = %s, ¿cuál es el punto B?" % (V(*A), V(*w)), V(A[0] + w[0], A[1] + w[1]), W([V(A[0] - w[0], A[1] - w[1]), V(w[0] - A[0], w[1] - A[1]), V(A[0] + w[1], A[1] + w[0])]), "B = A + AB = <b>%s</b>." % V(A[0] + w[0], A[1] + w[1]))


def s_modulo():
    t = R.choice(["mod", "mod", "unit", "dist", "k"])
    if t in ("mod", "unit"):
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (8, 15), (1, 1), (1, 2), (2, 3), (1, 3), (4, 4), (7, 24)])
        a, b = a * R.choice([1, -1]), b * R.choice([1, -1])
        n = a * a + b * b
        if t == "mod":
            return M("Calcula el módulo de u = %s." % V(a, b), raiz(n), W([num(abs(a) + abs(b)), num(n), raiz(abs(a * a - b * b)) if a * a != b * b else "0"]), "|u| = √(%d + %d) = <b>%s</b>." % (a * a, b * b, raiz(n)))
        m = int(math.isqrt(n))
        if m * m != n:
            return None
        return M("¿Cuál es el vector unitario con la misma dirección y sentido que u = %s?" % V(a, b), V(F(a, m), F(b, m)), W([V(F(m, a), F(m, b)), V(F(-a, m), F(-b, m)), V(F(a, n), F(b, n))]), "Dividimos entre |u| = %d: <b>%s</b>." % (m, V(F(a, m), F(b, m))))
    if t == "dist":
        A = rv(-6, 6)
        a, b = R.choice([(3, 4), (5, 12), (6, 8), (1, 2), (2, 2), (1, 4)])
        B = (A[0] + a * R.choice([1, -1]), A[1] + b * R.choice([1, -1]))
        n = a * a + b * b
        return M("¿Cuál es la distancia entre A%s y B%s?" % (V(*A), V(*B)), raiz(n), W([num(a + b), num(n), raiz(abs(a * a - b * b)) if a != b else raiz(2 * n)]), "d = |AB| = √(%d² + %d²) = <b>%s</b>." % (a, b, raiz(n)))
    a, m = R.choice([(3, 5), (4, 5), (5, 13), (12, 13), (6, 10), (8, 10), (8, 17)])
    b = int(math.isqrt(m * m - a * a))
    return M("¿Qué valores de k hacen que u = (%d, k) tenga módulo %d?" % (a, m), "k = ±%d" % b, ["k = %d" % b, "k = ±%d" % (m - a), "k = ±%d" % (m * m - a * a)], "%d² + k² = %d² → k² = %d → <b>k = ±%d</b>." % (a, m, b * b, b))


def s_escalar():
    u, v = rv(), rv()
    t = R.choice(["prod", "prod", "perp", "k", "paral"])
    p = u[0] * v[0] + u[1] * v[1]
    if t == "prod":
        return M("Calcula el producto escalar u · v, con u = %s y v = %s." % (V(*u), V(*v)), sg(p), W([V(u[0] * v[0], u[1] * v[1]), sg(u[0] * v[1] - u[1] * v[0]) if u[0] * v[1] - u[1] * v[0] != p else sg(p + 1), sg(u[0] * v[0] - u[1] * v[1]) if u[0] * v[0] - u[1] * v[1] != p else sg(p - 2)]),
                 "u · v = %s · %s + %s · %s = <b>%s</b> (es un número, no un vector)." % (sg(u[0]), "(%s)" % sg(v[0]) if v[0] < 0 else sg(v[0]), sg(u[1]), "(%s)" % sg(v[1]) if v[1] < 0 else sg(v[1]), sg(p)))
    if t == "perp":
        k = R.choice([1, 2, -1, -2, 3])
        a, b = u
        return M("¿Qué vector es perpendicular a u = %s?" % V(a, b), V(-b * k, a * k), W([V(b * k, a * k) if b * k * a + a * k * b != 0 else V(a * k, b * k), V(a * k, b * k), V(-a * k, -b * k), V(b, -a + 1)]), "Dos vectores son perpendiculares si u · v = 0; (a, b) ⊥ (−b, a): <b>%s</b>." % V(-b * k, a * k))
    if t == "k":
        a, b = u
        c = R.randint(-6, 6)
        if b == 0 or c == 0:
            return None
        k = F(-a * c, b)
        return M("¿Para qué valor de k son perpendiculares u = %s y v = (%s, k)?" % (V(a, b), sg(c)), "k = %s" % nf(k), W(["k = %s" % nf(-k), "k = %s" % nf(F(a * c, 1) if True else 0), "k = %s" % nf(F(b * c, a)) if a else "k = 0", "k = %s" % nf(F(c * b, a)) if a else "k = %s" % nf(k + 1)]),
                 "u · v = %s + %sk = 0 → <b>k = %s</b>." % (sg(a * c), sg(b), nf(k)))
    a, b = u
    m = R.choice([2, 3, -2])
    c = R.randint(1, 5) * (1 if a else 1)
    if a == 0:
        return None
    k = F(b * c * m, a * m) if False else F(b * c, a)
    return M("¿Para qué valor de k son paralelos u = %s y v = (%d, k)?" % (V(a, b), c), "k = %s" % nf(k), W(["k = %s" % nf(F(-a * c, b)) if b else "k = 1", "k = %s" % nf(F(a * c, b)) if b else "k = 2", "k = %s" % nf(k + 1)]),
             "Coordenadas proporcionales: %d/%s = k/%s → <b>k = %s</b>." % (c, sg(a), sg(b), nf(k)))


def s_angulo():
    t = R.choice(["ang", "ang", "ang", "tipo", "proy"])
    pairs = [((1, 0), (1, 1), "45°"), ((1, 0), (0, 3), "90°"), ((2, 0), (-3, 0), "180°"), ((1, 1), (-1, 1), "90°"), ((1, 0), (1, 0), "0°"), ((3, 4), (4, 3), None), ((1, 2), (3, 1), "45°"), ((2, 1), (1, 3), "45°"), ((1, 0), (-1, 1), "135°"), ((1, 1), (0, -2), "135°"), ((3, 0), (1, 1), "45°")]
    if t == "ang":
        u = rv(-5, 5)
        v = rv(-5, 5)
        c = (u[0] * v[0] + u[1] * v[1]) / math.sqrt((u[0] ** 2 + u[1] ** 2) * (v[0] ** 2 + v[1] ** 2))
        A = math.degrees(math.acos(max(-1, min(1, c))))
        if A < 5 or abs(A - 180) < 5:
            return None
        ok = "%s°" % r2(A, 1)
        return M("Calcula el ángulo que forman u = %s y v = %s (a las décimas de grado)." % (V(*u), V(*v)), ok, W(["%s°" % r2(180 - A, 1), "%s°" % r2(90 - A, 1) if A < 90 else "%s°" % r2(A - 90, 1), "%s°" % r2(A / 2, 1)]),
                 "cos α = u · v / (|u| · |v|) = %s / (√%d · √%d) → α ≈ <b>%s</b>." % (sg(u[0] * v[0] + u[1] * v[1]), u[0] ** 2 + u[1] ** 2, v[0] ** 2 + v[1] ** 2, ok))
    if t == "tipo":
        u, v = rv(), rv()
        p = u[0] * v[0] + u[1] * v[1]
        ok = "agudo" if p > 0 else "obtuso" if p < 0 else "recto"
        return M("Si u = %s y v = %s, ¿cómo es el ángulo que forman?" % (V(*u), V(*v)), ok, [x for x in ["agudo", "recto", "obtuso", "llano"] if x != ok], "u · v = %s: %s → <b>%s</b>." % (sg(p), "positivo" if p > 0 else "negativo" if p < 0 else "cero", ok))
    u = R.choice([(3, 4), (6, 8), (0, 2), (5, 12), (1, 0)])
    v = rv()
    n = math.sqrt(u[0] ** 2 + u[1] ** 2)
    pr = (u[0] * v[0] + u[1] * v[1]) / n
    return M("Calcula la proyección del vector v = %s sobre u = %s." % (V(*v), V(*u)), r2(pr) if pr != int(pr) else sg(int(pr)), W([sg(u[0] * v[0] + u[1] * v[1]), r2(pr * 2) if pr else "1", r2((u[0] * v[0] + u[1] * v[1]) / n ** 2) if pr else "2", r2(-pr) if pr else "3"]),
             "proy = u · v / |u| = %s / %s = <b>%s</b>." % (sg(u[0] * v[0] + u[1] * v[1]), num(int(n)), r2(pr) if pr != int(pr) else sg(int(pr))))


def s_base():
    t = R.choice(["comb", "comb", "base", "teo"])
    if t == "teo":
        q, a, w = R.choice([("¿Qué es u · v si u y v son perpendiculares?", "0", ["1", "|u| · |v|", "−1"]), ("¿Cuánto vale u · u?", "|u|²", ["|u|", "0", "1"]),
                            ("Dos vectores forman una base del plano si…", "no son paralelos", ["son perpendiculares", "tienen el mismo módulo", "son unitarios"]),
                            ("¿Qué es una base ortonormal?", "dos vectores perpendiculares de módulo 1", ["dos vectores paralelos", "dos vectores cualesquiera", "tres vectores del plano"]),
                            ("Si u · v &lt; 0, el ángulo entre u y v es…", "obtuso", ["agudo", "recto", "nulo"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    if t == "base":
        a, b = rv(-4, 4)
        k = R.choice([2, 3, -1, -2])
        if R.random() < 0.5:
            v = (k * a, k * b)
            ok = "no, porque son paralelos"
        else:
            v = rv(-4, 4)
            if a * v[1] - b * v[0] == 0:
                return None
            ok = "sí, porque no son paralelos"
        return M("¿Forman una base u = %s y v = %s?" % (V(a, b), V(*v)), ok, [x for x in ["sí, porque no son paralelos", "no, porque son paralelos", "sí, porque son perpendiculares", "no, porque no son unitarios"] if x != ok], "Comprobamos si las coordenadas son proporcionales: <b>%s</b>." % ok)
    x, y = R.randint(-4, 4), R.randint(-4, 4)
    if x == 0 or y == 0:
        return None
    u, v = (1, 2), (3, -1)
    u = R.choice([(1, 2), (2, 1), (1, -1), (1, 1)])
    v = R.choice([(3, -1), (0, 1), (2, 3), (1, 0)])
    if u[0] * v[1] - u[1] * v[0] == 0:
        return None
    w = (x * u[0] + y * v[0], x * u[1] + y * v[1])
    def cl(p, q):
        c1 = {1: "", -1: MINUS}.get(p, sg(p))
        c2 = "" if abs(q) == 1 else str(abs(q))
        return "w = %su %s %sv" % (c1, "+" if q > 0 else "−", c2)
    ok = cl(x, y)
    return M("Expresa w = %s como combinación lineal de u = %s y v = %s." % (V(*w), V(*u), V(*v)), ok, W([cl(y, x), cl(-x, y), cl(x, -y), cl(-x, -y)]),
             "w = a·u + b·v → resolvemos el sistema: a = %s, b = %s. <b>%s</b>." % (sg(x), sg(y), ok))


seen = set()
sets = [("Coordenadas y operaciones", mix(R, seen, [(s_operaciones, 20)])), ("Módulo y vector unitario", mix(R, seen, [(s_modulo, 20)])), ("Producto escalar", mix(R, seen, [(s_escalar, 20)])),
        ("Ángulo y proyección", mix(R, seen, [(s_angulo, 20)])), ("Bases y combinación lineal", mix(R, seen, [(s_base, 20)]))]
think = ["Un vector libre tiene <b>módulo</b> (longitud), <b>dirección</b> y <b>sentido</b>. Con coordenadas: AB = B − A y |u| = √(a² + b²).",
         "<b>Producto escalar</b>: u · v = u₁v₁ + u₂v₂ = |u| · |v| · cos α. Es un número.",
         "u · v = 0 ⇔ u y v son <b>perpendiculares</b>. Son <b>paralelos</b> si sus coordenadas son proporcionales.",
         "Dos vectores no paralelos forman una <b>base</b>: cualquier vector es combinación lineal de ellos."]
ex = [("u = (3, 4), v = (4, −3)", ["u · v = 12 − 12 = 0"], "perpendiculares"), ("u = (1, 2), v = (3, 1)", ["cos α = 5 / (√5 · √10)"], "α = 45°")]
mist = [["Dar u · v como vector", "El producto escalar es un número."], ["Olvidar dividir entre los módulos", "cos α = u · v / (|u| |v|)."], ["Confundir paralelo y perpendicular", "u · v = 0: perpendiculares."]]
body = L(think, ex, mist, kosy(vecs=[(0, 0, 3, 2, BLUE, "u"), (0, 0, -2, 3, RED, "v")], lo=-4, hi=4) if False else "")
faq = [("¿Para qué sirve el producto escalar?", "Para calcular ángulos, comprobar si dos vectores son perpendiculares y hallar proyecciones (en física, el trabajo de una fuerza)."),
       ("¿Qué diferencia hay entre vector fijo y vector libre?", "El fijo tiene un origen concreto; el libre representa a todos los vectores con el mismo módulo, dirección y sentido.")]
unit(1, R, "vectores-en-el-plano", "E", "Vectores en el plano: operaciones, módulo, bases, producto escalar, ángulo entre vectores y proyecciones",
     "Vectores en el plano", "Vectores", "Fichas de Matemáticas I (1.º de Bachillerato): coordenadas, operaciones, módulo, bases, producto escalar, ángulo, perpendicularidad y proyección. 100 ejercicios.",
     "u · v = |u| · |v| · cos α", "u · v = 0: vectores perpendiculares.", body, faq, sets, 7)
