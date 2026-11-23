# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Geometría analítica: la recta (Sentido espacial)
Ecuaciones de la recta (vectorial, paramétricas, continua, general, explícita, punto-pendiente), vector director y normal, posiciones relativas,
ángulo entre rectas, distancia de un punto a una recta, simétricos y mediatriz.
Errores: confundir vector director (−B, A) y normal (A, B), olvidar el valor absoluto en la distancia, signo de la pendiente.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, nf, r2, raiz, V, kosy, BLUE, RED, W, MINUS

R = random.Random(51008)


def gen(A, B, C):
    return "%s = 0" % E((A, "x"), (B, "y"), (C, ""))


def expl(m, n):
    return "y = %s" % E((m, "x"), (n, ""))


def rv():
    while True:
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        if a and b:
            return a, b


def s_ecuaciones():
    P = (R.randint(-5, 5), R.randint(-5, 5))
    v = rv()
    t = R.choice(["param", "gen", "gen", "continua", "director"])
    A, B = v[1], -v[0]
    C = -(A * P[0] + B * P[1])
    g = math.gcd(math.gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // g, B // g, C // g
    if A < 0:
        A, B, C = -A, -B, -C
    if t == "param":
        ok = "x = %s, y = %s" % (E((P[0], ""), (v[0], "t")), E((P[1], ""), (v[1], "t")))
        return M("Escribe las ecuaciones paramétricas de la recta que pasa por P%s con vector director %s." % (V(*P), V(*v)), ok,
                 W(["x = %s, y = %s" % (E((v[0], ""), (P[0], "t")), E((v[1], ""), (P[1], "t"))), "x = %s, y = %s" % (E((P[0], ""), (v[1], "t")), E((P[1], ""), (v[0], "t"))), "x = %s, y = %s" % (E((P[0], ""), (-v[0], "t")), E((P[1], ""), (v[1], "t")))]),
                 "(x, y) = P + t·v: <b>%s</b>." % ok)
    if t == "gen":
        ok = gen(A, B, C)
        return M("Halla la ecuación general de la recta que pasa por P%s con vector director %s." % (V(*P), V(*v)), ok, W([gen(v[0], v[1], -(v[0] * P[0] + v[1] * P[1])), gen(A, -B, -(A * P[0] - B * P[1])), gen(A, B, -C) if C else gen(A, B, 1)]),
                 "Con v = (a, b) la recta es b·x − a·y + C = 0; sustituyendo P: <b>%s</b>." % ok)
    if t == "continua":
        ok = "(x %s %d)/%s = (y %s %d)/%s" % ("−" if P[0] >= 0 else "+", abs(P[0]), sg(v[0]), "−" if P[1] >= 0 else "+", abs(P[1]), sg(v[1]))
        bad = "(x %s %d)/%s = (y %s %d)/%s" % ("+" if P[0] >= 0 else "−", abs(P[0]), sg(v[0]), "+" if P[1] >= 0 else "−", abs(P[1]), sg(v[1]))
        bad2 = "(x %s %d)/%s = (y %s %d)/%s" % ("−" if P[0] >= 0 else "+", abs(P[0]), sg(v[1]), "−" if P[1] >= 0 else "+", abs(P[1]), sg(v[0]))
        bad3 = "(x %s %d)/%s = (y %s %d)/%s" % ("−" if v[0] >= 0 else "+", abs(v[0]), sg(P[0]) if P[0] else "1", "−" if v[1] >= 0 else "+", abs(v[1]), sg(P[1]) if P[1] else "1")
        return M("Escribe la ecuación continua de la recta que pasa por P%s con vector director %s." % (V(*P), V(*v)), ok, W([bad, bad2, bad3]), "(x − x₀)/v₁ = (y − y₀)/v₂: <b>%s</b>." % ok)
    Ag, Bg, Cg = R.randint(1, 5), R.randint(-5, 5), R.randint(-9, 9)
    if Bg == 0:
        return None
    k = R.choice(["dir", "nor"])
    if k == "dir":
        return M("¿Cuál es un vector director de la recta %s?" % gen(Ag, Bg, Cg), V(-Bg, Ag), W([V(Ag, Bg), V(Bg, Ag), V(-Ag, Bg)]), "Si la recta es Ax + By + C = 0, un vector director es (−B, A): <b>%s</b>." % V(-Bg, Ag))
    return M("¿Cuál es un vector normal (perpendicular) a la recta %s?" % gen(Ag, Bg, Cg), V(Ag, Bg), W([V(-Bg, Ag), V(Bg, Ag), V(Ag, Cg) if Cg != Bg else V(Ag, -Bg)]), "El vector normal es (A, B): <b>%s</b>." % V(Ag, Bg))


def s_pendiente():
    t = R.choice(["dos", "dos", "gen", "pp", "angulo"])
    x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
    dx, dy = R.choice([1, 2, 3, -1, 4]), R.randint(-6, 6)
    if dy == 0:
        return None
    m = F(dy, dx)
    n = y1 - m * x1
    if t == "dos":
        if n.denominator > 1:
            return None
        return M("Halla la ecuación explícita de la recta que pasa por A%s y B%s." % (V(x1, y1), V(x1 + dx, y1 + dy)), expl(m, n), W([expl(1 / m, n), expl(-m, n), expl(m, -n) if n else expl(m, 1), expl(m, y1) if y1 != n else expl(m, n + 2)]), "m = %s/%s = %s; n = %s. <b>%s</b>." % (sg(dy), sg(dx), nf(m), nf(n), expl(m, n)))
    if t == "gen":
        A, B, C = R.randint(-5, 5), R.randint(1, 5), R.randint(-9, 9)
        if A == 0:
            return None
        mm = F(-A, B)
        return M("¿Cuál es la pendiente de %s?" % gen(A, B, C), nf(mm), W([nf(F(A, B)), nf(F(-B, A)), nf(F(B, A)), nf(F(-C, B)) if C else "0"]), "m = −A/B = <b>%s</b>." % nf(mm))
    if t == "pp":
        if n.denominator > 1:
            return None
        return M("¿Qué recta pasa por P%s y tiene pendiente %s?" % (V(x1, y1), nf(m)), expl(m, n), W([expl(m, y1) if y1 != n else expl(m, n + 1), expl(m, -n) if n else expl(m, 3), expl(-m, y1 + m * x1) if y1 + m * x1 != n else expl(-m, n), expl(m, x1 - y1)]),
                 "%s = %s(%s) → <b>%s</b>." % (E((1, "y"), (-y1, "")), nf(m) if m != 1 else "", E((1, "x"), (-x1, "")), expl(m, n)))
    g = R.choice([30, 45, 60, 135, 120, 150])
    v = {30: "√3/3", 45: "1", 60: "√3", 120: MINUS + "√3", 135: MINUS + "1", 150: MINUS + "√3/3"}[g]
    return M("¿Qué pendiente tiene una recta que forma un ángulo de %d° con el eje X?" % g, "m = %s" % v, W(["m = %s" % x for x in ["√3/3", "1", "√3", MINUS + "√3", MINUS + "1", MINUS + "√3/3", "1/2", "√3/2"] if x != v][:5]), "m = tg %d° = <b>%s</b>." % (g, v))


def s_posicion():
    t = R.choice(["rel", "rel", "corte", "paral", "perp"])
    m = F(R.choice([-3, -2, -1, 1, 2, 3]), R.choice([1, 1, 2]))
    n = R.randint(-6, 6)
    if t == "rel":
        k = R.choice(["paralelas", "coincidentes", "secantes", "perpendiculares"])
        A1, B1, C1 = -m.numerator, m.denominator, -n * m.denominator
        c = R.choice([2, -2, 3])
        if k == "paralelas":
            A2, B2, C2 = A1 * c, B1 * c, C1 * c + R.choice([1, 2, 5])
        elif k == "coincidentes":
            A2, B2, C2 = A1 * c, B1 * c, C1 * c
        elif k == "perpendiculares":
            A2, B2, C2 = B1, -A1, R.randint(-5, 5)
        else:
            A2, B2, C2 = A1 + 1, B1, R.randint(-5, 5)
            if A2 * A1 + B2 * B1 == 0 or A2 * B1 == B2 * A1:
                return None
        ok = k if k != "perpendiculares" else "secantes y perpendiculares"
        return M("¿Cuál es la posición relativa de r: %s y s: %s?" % (gen(A1, B1, C1), gen(A2, B2, C2)), ok, [x for x in ["paralelas", "coincidentes", "secantes", "secantes y perpendiculares"] if x != ok], "Comparamos A, B y C: <b>%s</b>." % ok)
    x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
    if t == "corte":
        m1, m2 = R.sample([-3, -2, -1, 1, 2, 3], 2)
        return M("Halla el punto de corte de r: %s y s: %s." % (expl(m1, y0 - m1 * x0), expl(m2, y0 - m2 * x0)), V(x0, y0), W([V(y0, x0) if x0 != y0 else V(-x0, y0), V(x0, y0 - m1 * x0), V(0, y0 - m1 * x0), V(-x0, -y0), V(x0 + 1, y0)]), "Igualamos y despejamos x = %s; y = %s. <b>%s</b>." % (sg(x0), sg(y0), V(x0, y0)))
    mm = m if t == "paral" else -1 / m
    nn = y0 - mm * x0
    if nn.denominator > 1:
        return None
    alt = -m if t == "paral" else m
    return M("Halla la recta %s a %s que pasa por P%s." % ("paralela" if t == "paral" else "perpendicular", expl(m, n), V(x0, y0)), expl(mm, nn), W([expl(alt, y0 - alt * x0), expl(mm, n) if n != nn else expl(mm, nn + 1), expl(-mm, y0 + mm * x0), expl(mm, -nn) if nn else expl(mm, 2)]),
             "%s: m = %s; pasa por P → n = %s. <b>%s</b>." % ("Paralela" if t == "paral" else "Perpendicular", nf(mm), nf(nn), expl(mm, nn)))


def s_distancia():
    t = R.choice(["pr", "pr", "pr", "par", "ang"])
    if t in ("pr", "par"):
        A, B = R.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (1, 1), (1, 2), (2, 1), (8, 15)])
        A, B = A * R.choice([1, -1]), B
        C = R.randint(-10, 10)
        nrm = A * A + B * B
        if t == "pr":
            x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
            num_ = abs(A * x0 + B * y0 + C)
            rt = math.isqrt(nrm)
            v = F(num_, rt) if rt * rt == nrm else None
            ok = nf(v) if v is not None else ("%d/√%d" % (num_, nrm) if num_ else "0")
            if num_ == 0:
                return None
            return M("Calcula la distancia del punto P%s a la recta %s." % (V(x0, y0), gen(A, B, C)), ok, W([sg(A * x0 + B * y0 + C) if A * x0 + B * y0 + C < 0 else nf(F(num_, nrm)), sg(num_), nf(F(num_, nrm)) if rt * rt == nrm else "%d/%d" % (num_, nrm), nf(F(num_ + abs(C), rt)) if rt * rt == nrm else "%d/√%d" % (num_ + 1, nrm)]),
                     "d = |%s · %s + %s · %s + %s| / √(%d + %d) = %d/%s = <b>%s</b>." % (sg(A), "(%s)" % sg(x0) if x0 < 0 else sg(x0), sg(B), "(%s)" % sg(y0) if y0 < 0 else sg(y0), "(%s)" % sg(C) if C < 0 else sg(C), A * A, B * B, num_, raiz(nrm), ok))
        rt = math.isqrt(nrm)
        if rt * rt != nrm:
            return None
        C2 = C + R.choice([5, 10, 15, -10]) * rt // math.gcd(rt, 5) if False else C + rt * R.choice([1, 2, 3])
        dd = F(abs(C2 - C), rt)
        return M("Calcula la distancia entre las rectas paralelas %s y %s." % (gen(A, B, C), gen(A, B, C2)), nf(dd), W([nf(F(abs(C2 - C), nrm)), sg(abs(C2 - C)), nf(F(abs(C2 + C), rt)) if C2 + C else "1"]), "d = |C − C′| / √(A² + B²) = %d/%d = <b>%s</b>." % (abs(C2 - C), rt, nf(dd)))
    m1, m2 = R.choice([(1, 0), (1, -1), (2, F(-1, 2)), (3, 0), (1, 2), (F(1, 2), 3)])
    tg = abs((m2 - m1) / (1 + m1 * m2)) if 1 + m1 * m2 else None
    A = 90 if tg is None else math.degrees(math.atan(tg))
    ok = "%s°" % r2(A, 1)
    return M("Calcula el ángulo que forman las rectas r: y = %s y s: y = %s (a las décimas de grado)." % (E((m1, "x")), E((m2, "x")) if m2 else "0"), ok, W(["%s°" % r2(180 - A, 1) if A != 90 else "0°", "%s°" % r2(90 - A, 1) if A != 90 else "45°", "%s°" % r2(A / 2, 1), "%s°" % r2(A + 15, 1)]),
             "tg α = |(m₂ − m₁)/(1 + m₁m₂)| → α ≈ <b>%s</b>." % ok if A != 90 else "m₁ · m₂ = −1: son perpendiculares, <b>90°</b>.")


def s_simetrico():
    t = R.choice(["medio", "sim", "mediatriz", "pertenece"])
    A = (R.randint(-6, 6), R.randint(-6, 6))
    B = (R.randint(-6, 6), R.randint(-6, 6))
    if A == B:
        return None
    if t == "medio":
        m = (F(A[0] + B[0], 2), F(A[1] + B[1], 2))
        return M("Halla el punto medio del segmento AB con A%s y B%s." % (V(*A), V(*B)), V(*m), W([V(B[0] - A[0], B[1] - A[1]), V(F(B[0] - A[0], 2), F(B[1] - A[1], 2)), V(A[0] + B[0], A[1] + B[1])]), "M = ((x₁ + x₂)/2, (y₁ + y₂)/2) = <b>%s</b>." % V(*m))
    if t == "sim":
        s = (2 * B[0] - A[0], 2 * B[1] - A[1])
        return M("Halla el simétrico de A%s respecto del punto M%s." % (V(*A), V(*B)), V(*s), W([V(F(A[0] + B[0], 2), F(A[1] + B[1], 2)), V(-A[0], -A[1]), V(B[0] - A[0], B[1] - A[1]), V(2 * A[0] - B[0], 2 * A[1] - B[1])]), "M es el punto medio de A y A′: A′ = 2M − A = <b>%s</b>." % V(*s))
    if t == "mediatriz":
        a, b = B[0] - A[0], B[1] - A[1]
        C = -F(B[0] ** 2 + B[1] ** 2 - A[0] ** 2 - A[1] ** 2, 2)
        if C.denominator > 1:
            a, b, C = 2 * a, 2 * b, 2 * C
        g = math.gcd(math.gcd(abs(a), abs(b)), abs(int(C))) or 1
        a, b, C = a // g, b // g, int(C) // g
        if a < 0 or (a == 0 and b < 0):
            a, b, C = -a, -b, -C
        ok = gen(a, b, C)
        return M("Halla la mediatriz del segmento de extremos A%s y B%s." % (V(*A), V(*B)), ok, W([gen(b, -a, C) if b else gen(a, 1, C), gen(a, b, -C) if C else gen(a, b, 1), gen(-b, a, C) if b else gen(a, 2, C)]),
                 "Puntos que están a la misma distancia de A y de B (perpendicular a AB por el punto medio): <b>%s</b>." % ok)
    m, n = R.choice([-3, -2, -1, 1, 2, 3]), R.randint(-6, 6)
    xs = R.sample(range(-5, 6), 4)
    pts = [(xs[0], m * xs[0] + n)] + [(x, m * x + n + R.choice([-2, -1, 1, 2])) for x in xs[1:]]
    return M("¿Qué punto está en la recta %s?" % expl(m, n), V(*pts[0]), [V(*p) for p in pts[1:]], "Sustituimos x = %s: y = %s. <b>%s</b>." % (sg(pts[0][0]), sg(pts[0][1]), V(*pts[0])))


seen = set()
sets = [("Ecuaciones de la recta", mix(R, seen, [(s_ecuaciones, 20)])), ("Pendiente y forma explícita", mix(R, seen, [(s_pendiente, 20)])), ("Posiciones relativas", mix(R, seen, [(s_posicion, 20)])),
        ("Distancias y ángulos", mix(R, seen, [(s_distancia, 20)])), ("Puntos medios, simétricos y mediatriz", mix(R, seen, [(s_simetrico, 20)]))]
think = ["Una recta queda determinada por un punto P(x₀, y₀) y un <b>vector director</b> v = (v₁, v₂): (x, y) = (x₀, y₀) + t·(v₁, v₂).",
         "En la ecuación <b>general</b> Ax + By + C = 0, el vector (A, B) es <b>normal</b> a la recta y (−B, A) es director. La pendiente es m = −A/B.",
         "Distancia de P(x₀, y₀) a Ax + By + C = 0: d = |Ax₀ + By₀ + C| / √(A² + B²).",
         "Rectas paralelas: misma pendiente. Perpendiculares: m · m′ = −1."]
ex = [("Recta por (1, 2) con v = (3, −1)", ["−x − 3y + C = 0", "C = 7"], "x + 3y − 7 = 0"), ("Distancia de (2, 1) a 3x + 4y − 5 = 0", ["|6 + 4 − 5| / 5"], "1")]
mist = [["Confundir director y normal", "(A, B) es normal; (−B, A) es director."], ["Olvidar el valor absoluto", "Una distancia nunca es negativa."], ["Perpendicular con la pendiente opuesta", "Es −1/m, no −m."]]
body = L(think, ex, mist, kosy(lines=[(2, 1, BLUE, ""), (F(-1, 2), 3, RED, "")], lo=-5, hi=5))
faq = [("¿Cuál es la mejor ecuación de la recta?", "Depende del problema: la general sirve para distancias, la explícita para dibujar y la paramétrica para recorrer la recta."),
       ("¿Qué es la mediatriz?", "La recta perpendicular a un segmento por su punto medio: todos sus puntos están a la misma distancia de los dos extremos.")]
unit(1, R, "geometria-analitica", "E", "Geometría analítica en el plano: ecuaciones de la recta, posiciones relativas, ángulos, distancias, simetrías y lugares geométricos sencillos",
     "Geometría analítica: la recta", "Geometría analítica", "Fichas de Matemáticas I (1.º de Bachillerato): ecuaciones de la recta, vector director y normal, posiciones relativas, ángulos, distancias y mediatriz. 100 ejercicios.",
     "Ax + By + C = 0: normal (A, B)", "d = |Ax₀ + By₀ + C| / √(A² + B²)", body, faq, sets, 8)
