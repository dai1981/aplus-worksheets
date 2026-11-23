# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Vectores en el espacio (Sentido espacial)
Coordenadas y operaciones, módulo, dependencia lineal, producto escalar (ángulos y perpendicularidad), producto vectorial (área de paralelogramos y triángulos),
producto mixto (volumen de paralelepípedos y tetraedros).
Errores: u × v = v × u (cambia el signo), olvidar el valor absoluto en el producto mixto, tetraedro = 1/6 del producto mixto (no 1/3).
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, nf, r2, raiz, det_h, det3, W, MINUS
from es_espacio import V, add, esc, cruz, mod2

R = random.Random(52004)


def rv(lo=-4, hi=5):
    while True:
        v = tuple(R.randint(lo, hi) for _ in range(3))
        if any(v):
            return v


def s_operaciones():
    u, v = rv(), rv()
    t = R.choice(["comb", "ab", "medio", "mod", "mod"])
    if t == "comb":
        k = R.choice([2, 3, -2])
        r = add(tuple(k * x for x in u), v, -1)
        return M("Si u = %s y v = %s, calcula %su − v." % (V(*u), V(*v), sg(k)), V(*r), W([V(*add(tuple(k * x for x in u), v)), V(*add(u, tuple(k * x for x in v), -1)), V(*tuple(k * x for x in add(u, v, -1))), V(*tuple(-x for x in r))]), "Coordenada a coordenada: <b>%s</b>." % V(*r))
    if t == "ab":
        return M("Halla el vector AB con A%s y B%s." % (V(*u), V(*v)), V(*add(v, u, -1)), W([V(*add(u, v, -1)), V(*add(u, v)), V(*add(v, u, -1)[::-1]) if add(v, u, -1)[::-1] != add(v, u, -1) else V(*add(v, u))]), "B − A = <b>%s</b>." % V(*add(v, u, -1)))
    if t == "medio":
        m = tuple(F(a + b, 2) for a, b in zip(u, v))
        return M("Halla el punto medio de A%s y B%s." % (V(*u), V(*v)), V(*m), W([V(*add(v, u, -1)), V(*tuple(F(b - a, 2) for a, b in zip(u, v))), V(*add(u, v))]), "M = (A + B)/2 = <b>%s</b>." % V(*m))
    a, b, c = R.choice([(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7), (1, 1, 1), (1, 2, 3), (2, 2, 1), (3, 4, 12)])
    s = R.choice([1, -1])
    n = a * a + b * b + c * c
    return M("Calcula el módulo de u = %s." % V(a, s * b, c), raiz(n), W([num(a + b + c), num(n), raiz(abs(a * a + b * b - c * c)) if a * a + b * b != c * c else "0"]), "|u| = √(%d + %d + %d) = <b>%s</b>." % (a * a, b * b, c * c, raiz(n)))


def s_dependencia():
    t = R.choice(["paral", "paral", "dep3", "dep3", "k"])
    if t == "paral":
        u = rv(-3, 3)
        k = R.choice([2, -2, 3])
        if R.random() < 0.5:
            v = tuple(k * x for x in u)
            ok = "sí, v = %su" % sg(k)
        else:
            v = add(tuple(k * x for x in u), (0, 0, 1))
            if not any(cruz(u, v)):
                return None
            ok = "no, las coordenadas no son proporcionales"
        return M("¿Son paralelos u = %s y v = %s?" % (V(*u), V(*v)), ok, W([x for x in ["sí, v = %su" % sg(k), "no, las coordenadas no son proporcionales", "sí, porque u · v = 0", "no, porque tienen distinto módulo"] if x != ok]), "Comprobamos si v = k · u: <b>%s</b>." % ok)
    if t == "dep3":
        u, v = rv(-3, 3), rv(-3, 3)
        if R.random() < 0.5:
            a, b = R.choice([1, 2, -1]), R.choice([1, -1, 2])
            w = add(tuple(a * x for x in u), tuple(b * x for x in v))
        else:
            w = rv(-3, 3)
        d = det3([list(u), list(v), list(w)])
        ok = "linealmente dependientes (coplanarios)" if d == 0 else "linealmente independientes (forman una base)"
        return M("¿Cómo son u = %s, v = %s y w = %s?" % (V(*u), V(*v), V(*w)), ok, [x for x in ["linealmente dependientes (coplanarios)", "linealmente independientes (forman una base)", "perpendiculares dos a dos", "paralelos"] if x != ok], "El determinante que forman vale %s: <b>%s</b>." % (sg(d), ok))
    u, v = rv(-3, 3), rv(-3, 3)
    # w = (1, 1, k) dependiente si det = 0 → lineal en k
    d0 = det3([list(u), list(v), [1, 1, 0]])
    d1 = det3([list(u), list(v), [0, 0, 1]])
    if d1 == 0:
        return None
    k = F(-d0, d1)
    return M("¿Para qué valor de k son coplanarios u = %s, v = %s y w = (1, 1, k)?" % (V(*u), V(*v)), "k = %s" % nf(k), W(["k = %s" % nf(-k) if k else "k = 1", "k = %s" % nf(F(d0, 1)), "k = %s" % nf(F(d1, d0)) if d0 else "k = 2", "k = %s" % nf(k + 1)]), "det(u, v, w) = %s + %sk = 0 → <b>k = %s</b>." % (sg(d0), sg(d1), nf(k)))


def s_escalar():
    u, v = rv(), rv()
    p = esc(u, v)
    t = R.choice(["prod", "prod", "perp", "ang", "proy"])
    if t == "prod":
        return M("Calcula u · v con u = %s y v = %s." % (V(*u), V(*v)), sg(p), W([V(*(a * b for a, b in zip(u, v))), sg(p + 1), sg(-p) if p else "1", V(*cruz(u, v))]), "u₁v₁ + u₂v₂ + u₃v₃ = <b>%s</b>." % sg(p))
    if t == "perp":
        a, b = u[0], u[1]
        c = u[2]
        if c == 0:
            return None
        x, y = R.randint(-3, 3), R.randint(-3, 3)
        k = F(-(a * x + b * y), c)
        return M("¿Para qué valor de k son perpendiculares u = %s y v = (%s, %s, k)?" % (V(*u), sg(x), sg(y)), "k = %s" % nf(k), W(["k = %s" % nf(-k) if k else "k = 1", "k = %s" % nf(F(a * x + b * y, 1)), "k = %s" % nf(k + 1), "k = 0" if k else "k = 2"]), "u · v = %s + %sk = 0 → <b>k = %s</b>." % (sg(a * x + b * y), sg(c), nf(k)))
    if t == "ang":
        c = p / math.sqrt(mod2(u) * mod2(v))
        A = math.degrees(math.acos(max(-1, min(1, c))))
        ok = "%s°" % r2(A, 1)
        return M("Calcula el ángulo entre u = %s y v = %s (a las décimas)." % (V(*u), V(*v)), ok, W(["%s°" % r2(180 - A, 1), "%s°" % r2(abs(90 - A), 1), "%s°" % r2(A / 2, 1)]), "cos α = %s/(√%d · √%d) → α ≈ <b>%s</b>." % (sg(p), mod2(u), mod2(v), ok))
    u = R.choice([(1, 2, 2), (2, 3, 6), (2, 1, 2), (0, 3, 4), (1, 4, 8)])
    n = int(math.isqrt(mod2(u)))
    pr = F(esc(u, v), n)
    return M("Calcula la proyección de v = %s sobre u = %s." % (V(*v), V(*u)), nf(pr), W([sg(esc(u, v)), nf(F(esc(u, v), n * n)), nf(-pr) if pr else "1", nf(pr + 1)]), "proy = u · v / |u| = %s/%d = <b>%s</b>." % (sg(esc(u, v)), n, nf(pr)))


def s_vectorial():
    u, v = rv(-3, 4), rv(-3, 4)
    w = cruz(u, v)
    if not any(w):
        return None
    t = R.choice(["calc", "calc", "area", "tri", "teo"])
    if t == "calc":
        return M("Calcula u × v con u = %s y v = %s." % (V(*u), V(*v)), V(*w), W([V(*cruz(v, u)), V(*(a * b for a, b in zip(u, v))), V(w[0], -w[1], w[2]), V(*w[::-1])]), "Determinante con i, j, k en la primera fila: <b>%s</b>." % V(*w))
    if t in ("area", "tri"):
        n = mod2(w)
        ar = raiz(n)
        if t == "area":
            return M("Calcula el área del paralelogramo determinado por u = %s y v = %s." % (V(*u), V(*v)), ar, W([raiz(n * 4) if raiz(n * 4) != ar else num(n), num(n), "%s/2" % ar if not ar.isdigit() else nf(F(int(ar), 2)), sg(esc(u, v)) if esc(u, v) else "0"]), "Área = |u × v| = |%s| = <b>%s</b>." % (V(*w), ar))
        half = ("%s/2" % ar) if not ar.isdigit() else nf(F(int(ar), 2))
        return M("Calcula el área del triángulo de vértices A(0, 0, 0), B%s y C%s." % (V(*u), V(*v)), half, W([ar, num(n), "%s/3" % ar if not ar.isdigit() else nf(F(int(ar), 3))]), "Área = |AB × AC|/2 = %s/2 = <b>%s</b>." % (ar, half))
    q, a, w_ = R.choice([("¿Cómo es u × v respecto a u y a v?", "perpendicular a los dos", ["paralelo a u", "paralelo a v", "es un número"]), ("v × u es igual a…", "−(u × v)", ["u × v", "u · v", "0"]),
                         ("Si u y v son paralelos, u × v es…", "el vector nulo", ["un vector unitario", "perpendicular a u de módulo 1", "un número"]), ("¿Qué da el módulo de u × v?", "el área del paralelogramo de lados u y v", ["el volumen del paralelepípedo", "el ángulo entre u y v", "la longitud de u"])])
    return M(q, a, w_, "Respuesta: <b>%s</b>." % a)


def s_mixto():
    u, v, w = rv(-3, 3), rv(-3, 3), rv(-3, 3)
    d = det3([list(u), list(v), list(w)])
    if d == 0:
        return None
    t = R.choice(["calc", "vol", "tetra", "tetra"])
    if t == "calc":
        return M("Calcula el producto mixto [u, v, w] con u = %s, v = %s y w = %s." % (V(*u), V(*v), V(*w)), sg(d), W([sg(-d), sg(d * 2), sg(esc(u, v) * esc(v, w)) if esc(u, v) * esc(v, w) != d else sg(d + 1)]), "Es el determinante %s = <b>%s</b>." % (det_h([list(u), list(v), list(w)]), sg(d)))
    if t == "vol":
        return M("Calcula el volumen del paralelepípedo de aristas u = %s, v = %s y w = %s." % (V(*u), V(*v), V(*w)), num(abs(d)), W([sg(-abs(d)), nf(F(abs(d), 6)), nf(F(abs(d), 3)), num(abs(d) * 2)]), "V = |[u, v, w]| = |%s| = <b>%s</b>." % (sg(d), num(abs(d))))
    return M("Calcula el volumen del tetraedro de vértices O(0, 0, 0), A%s, B%s y C%s." % (V(*u), V(*v), V(*w)), nf(F(abs(d), 6)), W([num(abs(d)), nf(F(abs(d), 3)), nf(F(abs(d), 2)), nf(F(-abs(d), 6))]), "V = |[OA, OB, OC]|/6 = %d/6 = <b>%s</b>." % (abs(d), nf(F(abs(d), 6))))


seen = set()
sets = [("Coordenadas y operaciones", mix(R, seen, [(s_operaciones, 20)])), ("Dependencia lineal", mix(R, seen, [(s_dependencia, 20)])), ("Producto escalar", mix(R, seen, [(s_escalar, 20)])),
        ("Producto vectorial", mix(R, seen, [(s_vectorial, 20)])), ("Producto mixto", mix(R, seen, [(s_mixto, 20)]))]
think = ["En el espacio, un vector tiene tres coordenadas: u = (u₁, u₂, u₃) y |u| = √(u₁² + u₂² + u₃²).",
         "<b>Producto escalar</b>: u · v = u₁v₁ + u₂v₂ + u₃v₃ = |u||v| cos α (un número). u · v = 0 ⇔ perpendiculares.",
         "<b>Producto vectorial</b> u × v: un vector perpendicular a u y a v; su módulo es el área del paralelogramo que forman.",
         "<b>Producto mixto</b> [u, v, w] = u · (v × w): el determinante de los tres vectores. |[u, v, w]| es el volumen del paralelepípedo; el tetraedro es 1/6."]
ex = [("u = (1, 0, 2), v = (0, 1, 1)", ["u × v = (0·1 − 2·1, 2·0 − 1·1, 1·1 − 0·0)"], "(−2, −1, 1)")]
mist = [["u × v = v × u", "Cambia el signo: v × u = −(u × v)."], ["Volumen negativo", "Toma el valor absoluto del producto mixto."], ["Tetraedro con 1/3", "Es 1/6 del paralelepípedo."]]
body = L(think, ex, mist)
faq = [("¿Qué diferencia hay entre producto escalar y vectorial?", "El escalar da un número (sirve para ángulos); el vectorial da un vector perpendicular a los dos (sirve para áreas y normales)."),
       ("¿Cuándo tres vectores forman una base?", "Cuando son linealmente independientes, es decir, cuando su determinante (producto mixto) es distinto de 0.")]
unit(2, R, "vectores-en-el-espacio", "E", "Vectores en el espacio: operaciones, dependencia lineal, productos escalar, vectorial y mixto, y sus aplicaciones (ángulos, áreas y volúmenes)",
     "Vectores en el espacio", "Vectores en el espacio", "Fichas de Matemáticas II (2.º de Bachillerato): operaciones, dependencia lineal, producto escalar, vectorial y mixto, áreas y volúmenes. 100 ejercicios con soluciones.",
     "|u × v| = área del paralelogramo", "|[u, v, w]| = volumen del paralelepípedo", body, faq, sets, 4)
