# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Rectas y planos en el espacio (Sentido espacial)
Ecuaciones de la recta (vectorial, paramétricas, continua, implícita), ecuaciones del plano (vectorial, general, por tres puntos), vector normal,
puntos que pertenecen a una recta o a un plano, recta como intersección de dos planos.
Errores: confundir vector director de la recta y vector normal del plano, signos en la ecuación continua, tres puntos alineados no determinan un plano.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, nf, det3, W, MINUS, par
from es_espacio import V, add, esc, cruz, plano, param, continua, simp

R = random.Random(52005)


def rv(lo=-4, hi=5, nz=False):
    while True:
        v = tuple(R.randint(lo, hi) for _ in range(3))
        if any(v) and (not nz or all(v)):
            return v


def s_recta():
    P, v = rv(-5, 5), rv(-3, 4, nz=True)
    t = R.choice(["param", "cont", "dos", "dir", "punto"])
    if t == "param":
        return M("¿Cuáles son las ecuaciones paramétricas de la recta que pasa por P%s con vector director v = %s?" % (V(*P), V(*v)), param(P, v), W([param(v, P), param(P, tuple(-x for x in v[::-1])), param(tuple(-x for x in P), v)]), "x = p₁ + λv₁, y = p₂ + λv₂, z = p₃ + λv₃.")
    if t == "cont":
        return M("¿Cuál es la ecuación continua de la recta que pasa por P%s con vector director %s?" % (V(*P), V(*v)), continua(P, v), W([continua(tuple(-x for x in P), v), continua(v, P) if all(P) else continua(P, v[::-1]), continua(P, tuple(-x for x in v))]) if continua(P, tuple(-x for x in v)) != continua(P, v) else None, "(x − p₁)/v₁ = (y − p₂)/v₂ = (z − p₃)/v₃: <b>%s</b>." % continua(P, v))
    if t == "dos":
        Q = add(P, v)
        return M("¿Qué vector director tiene la recta que pasa por A%s y B%s?" % (V(*P), V(*Q)), V(*v), W([V(*add(P, Q)), V(*tuple(-x for x in Q)), V(*Q)]), "AB = B − A = <b>%s</b> (o cualquier múltiplo).".replace("<b>%s</b>", "<b>%s</b>") % V(*v))
    if t == "dir":
        n1, n2 = rv(-3, 3), rv(-3, 3)
        d = cruz(n1, n2)
        if not any(d):
            return None
        s_ = "<span class='sys'>%s<br>%s</span>" % (plano(n1, R.randint(-5, 5)), plano(n2, R.randint(-5, 5)))
        return M("¿Cuál es un vector director de la recta %s?" % s_, V(*d), W([V(*add(n1, n2)), V(*n1), V(*(a * b for a, b in zip(n1, n2)))]), "Es perpendicular a los dos vectores normales: n₁ × n₂ = <b>%s</b>." % V(*d))
    lam = R.randint(-3, 3)
    Q = add(P, tuple(lam * x for x in v))
    others = [add(Q, (1, 0, 0)), add(Q, (0, -1, 1)), add(P, tuple((lam + 1) * x for x in v[::-1])) if v[::-1] != v else add(Q, (0, 0, 2))]
    return M("¿Qué punto pertenece a la recta (x, y, z) = %s + λ%s?" % (V(*P), V(*v)), V(*Q), W([V(*o) for o in others]), "Con λ = %s se obtiene <b>%s</b>." % (sg(lam), V(*Q)))


def s_plano():
    t = R.choice(["normal", "normal", "pn", "pn", "tres", "pertenece"])
    n = rv(-4, 5)
    P = rv(-4, 4)
    d = -esc(n, P)
    if t == "normal":
        return M("¿Cuál es un vector normal al plano %s?" % plano(n, d), V(*n), W([V(*n[::-1]) if n[::-1] != n else V(n[0], -n[1], n[2]), V(n[0], n[1], d), V(*tuple(-x for x in n[:2])) if False else V(-n[0], n[1], n[2]) if n[0] else V(n[0], n[1] + 1, n[2])]), "En ax + by + cz + d = 0, el normal es (a, b, c): <b>%s</b>." % V(*n))
    if t == "pn":
        return M("Halla el plano que pasa por P%s y tiene vector normal n = %s." % (V(*P), V(*n)), plano(n, d), W([plano(n, -d) if d else plano(n, 1), plano(P, -esc(P, n)) if any(P) and P != n else plano(n, d + 1), plano(n[::-1], d) if n[::-1] != n else plano(n, d - 2)]),
                 "%s(x − p₁) + … = 0 → d = −n · P = %s: <b>%s</b>." % ("n", sg(d), plano(n, d)))
    if t == "tres":
        A = rv(-3, 3)
        u, v = rv(-2, 3), rv(-2, 3)
        nn = cruz(u, v)
        if not any(nn):
            return None
        nn = simp(nn)
        B, C = add(A, u), add(A, v)
        dd = -esc(nn, A)
        return M("Halla el plano que pasa por A%s, B%s y C%s." % (V(*A), V(*B), V(*C)), plano(nn, dd), W([plano(nn, -dd) if dd else plano(nn, 2), plano(simp(add(u, v)) if any(add(u, v)) else (1, 1, 1), dd), plano((nn[0], -nn[1], nn[2]), dd) if nn[1] else plano((nn[0] + 1, nn[1], nn[2]), dd)]),
                 "n = AB × AC = %s; sustituimos A: <b>%s</b>." % (V(*nn), plano(nn, dd)))
    pts = [P, add(P, (1, 0, 0)), add(P, (0, 1, -1)), add(P, (1, 1, 1))]
    ok = pts[0]
    alts = [q for q in pts[1:] if esc(n, q) + d != 0]
    if len(alts) < 3:
        return None
    return M("¿Qué punto pertenece al plano %s?" % plano(n, d), V(*ok), [V(*q) for q in alts], "Sustituimos: %s cumple la ecuación. <b>%s</b>." % (V(*ok), V(*ok)))


def s_conceptos():
    q, a, w = R.choice([("¿Cuántos puntos no alineados determinan un plano?", "tres", ["dos", "cuatro", "uno"]), ("¿Qué determina una recta en el espacio?", "un punto y un vector director", ["un punto y un vector normal", "tres puntos", "un solo vector"]),
                        ("¿Qué es el vector normal de un plano?", "un vector perpendicular al plano", ["un vector contenido en el plano", "un vector de módulo 1", "el vector de posición"]),
                        ("¿Cuántas ecuaciones implícitas (cartesianas) tiene una recta en el espacio?", "dos (es la intersección de dos planos)", ["una", "tres", "ninguna"]),
                        ("Si tres puntos están alineados, ¿cuántos planos pasan por ellos?", "infinitos", ["uno", "ninguno", "tres"]), ("¿Cuántos parámetros tiene la ecuación paramétrica de un plano?", "dos (λ y μ)", ["uno", "tres", "ninguno"]),
                        ("El plano z = 0 es…", "el plano XY", ["el eje Z", "el plano XZ", "el plano YZ"]), ("¿Qué ecuación tiene el plano paralelo a XY que pasa por (1, 2, 5)?", "z = 5", ["x = 1", "y = 2", "x + y + z = 8"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_parametros():
    t = R.choice(["vecplano", "ejes", "coplanar"])
    if t == "vecplano":
        P = rv(-3, 3)
        u, v = rv(-2, 3), rv(-2, 3)
        nn = cruz(u, v)
        if not any(nn):
            return None
        nn = simp(nn)
        dd = -esc(nn, P)
        return M("Halla la ecuación general del plano (x, y, z) = %s + λ%s + μ%s." % (V(*P), V(*u), V(*v)), plano(nn, dd), W([plano(nn, -dd) if dd else plano(nn, 3), plano(simp(add(u, v)), dd) if any(add(u, v)) else plano((1, 1, 1), dd), plano(u, -esc(u, P))]), "n = u × v = %s y pasa por P: <b>%s</b>." % (V(*nn), plano(nn, dd)))
    if t == "ejes":
        a, b, c = R.choice([2, 3, 4, 6, -2]), R.choice([2, 3, 4, -3]), R.choice([2, 4, 6, 12])
        L_ = abs(a * b * c)
        n = (L_ // a, L_ // b, L_ // c)
        g = 0
        import math
        for x in n:
            g = math.gcd(g, x)
        n = tuple(x // g for x in n)
        dd = -L_ // g
        return M("¿Qué plano corta a los ejes en (%s, 0, 0), (0, %s, 0) y (0, 0, %s)?" % (sg(a), sg(b), sg(c)), plano(n, dd), W([plano((a, b, c), -1), plano(n, -dd), plano(n[::-1], dd) if n[::-1] != n else plano(n, dd + 1)]), "Ecuación segmentaria x/%s + y/%s + z/%s = 1 → <b>%s</b>." % (par(a), par(b), par(c), plano(n, dd)))
    A, B, C = rv(-3, 3), rv(-3, 3), rv(-3, 3)
    D0 = (0, 0, 0)
    u, v = add(B, A, -1), add(C, A, -1)
    nn = cruz(u, v)
    if not any(nn):
        return None
    w0 = (1, 1, 0)
    # D = A + (1, 1, k): coplanar si (D − A)·nn = 0 → nn0 + nn1 + k nn2 = 0
    if nn[2] == 0:
        return None
    k = F(-(nn[0] + nn[1]), nn[2])
    D = (A[0] + 1, A[1] + 1, "%s + k" % nf(A[2]) if A[2] else "k")
    return M("¿Para qué k son coplanarios A%s, B%s, C%s y D(%s, %s, k + %s)?" % (V(*A), V(*B), V(*C), nf(A[0] + 1), nf(A[1] + 1), nf(A[2])) if A[2] >= 0 else "¿Para qué k son coplanarios A%s, B%s, C%s y D(%s, %s, k − %s)?" % (V(*A), V(*B), V(*C), nf(A[0] + 1), nf(A[1] + 1), nf(-A[2])),
             "k = %s" % nf(k), W(["k = %s" % nf(-k) if k else "k = 1", "k = %s" % nf(k + 1), "k = %s" % nf(F(nn[0] + nn[1], 1)), "k = 0" if k else "k = 2"]), "[AB, AC, AD] = 0 → <b>k = %s</b>." % nf(k))


seen = set()
sets = [("Ecuaciones de la recta", mix(R, seen, [(s_recta, 20)])), ("Ecuación del plano", mix(R, seen, [(s_plano, 20)])), ("Conceptos", mix(R, seen, [(s_conceptos, 8), (s_recta, 12)])),
        ("Plano por tres puntos y otras formas", mix(R, seen, [(s_parametros, 12), (s_plano, 8)])), ("Repaso de rectas y planos", mix(R, seen, [(s_recta, 7), (s_plano, 7), (s_parametros, 6)]))]
think = ["<b>Recta</b>: un punto P y un vector director v. Paramétricas: x = p₁ + λv₁, y = p₂ + λv₂, z = p₃ + λv₃. Continua: (x − p₁)/v₁ = (y − p₂)/v₂ = (z − p₃)/v₃.",
         "<b>Plano</b>: un punto y dos vectores, o un punto y un vector normal n = (a, b, c): ax + by + cz + d = 0.",
         "Por tres puntos A, B, C no alineados: n = AB × AC.",
         "Una recta también se puede dar como intersección de dos planos; su director es n₁ × n₂."]
ex = [("Plano por A(1, 0, 0), B(0, 1, 0), C(0, 0, 1)", ["AB = (−1, 1, 0), AC = (−1, 0, 1)", "n = (1, 1, 1)"], "x + y + z − 1 = 0")]
mist = [["Confundir director y normal", "El director va a lo largo de la recta; el normal es perpendicular al plano."], ["Signos en la continua", "Punto (2, −1, 3) → (x − 2), (y + 1), (z − 3)."], ["Usar tres puntos alineados", "No determinan un único plano."]]
body = L(think, ex, mist)
faq = [("¿Por qué una recta en el espacio necesita dos ecuaciones cartesianas?", "Porque cada ecuación lineal es un plano; la recta es la intersección de dos planos."),
       ("¿Cómo sé si un punto está en un plano?", "Sustituyes sus coordenadas en la ecuación: si se cumple, pertenece al plano.")]
unit(2, R, "rectas-y-planos-en-el-espacio", "E", "Ecuaciones de rectas y planos en el espacio: vectorial, paramétricas, continua, implícita y general; plano por tres puntos y vector normal",
     "Rectas y planos en el espacio", "Rectas y planos", "Fichas de Matemáticas II (2.º de Bachillerato): ecuaciones de la recta y del plano, vector normal, plano por tres puntos y recta como intersección de planos. 100 ejercicios.",
     "Plano: n · (X − P) = 0", "Recta: un punto y un vector director", body, faq, sets, 5)
