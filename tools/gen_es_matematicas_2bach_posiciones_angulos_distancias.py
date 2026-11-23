# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Posiciones relativas, ángulos y distancias en el espacio (Sentido espacial)
Posición relativa de dos planos, de recta y plano y de dos rectas (paralelas, se cortan, se cruzan), ángulos entre rectas y planos,
distancia de un punto a un plano, entre planos paralelos, de un punto a una recta, proyección y simétrico de un punto.
Errores: ángulo recta-plano con el coseno (es con el seno, porque se usa el normal), olvidar el valor absoluto, «se cruzan» no es «se cortan».
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, nf, r2, raiz, det3, W, MINUS, par
from es_espacio import V, add, esc, cruz, mod2, plano, simp

R = random.Random(52006)
TRN = [(1, 2, 2), (2, 3, 6), (2, 1, 2), (1, 4, 8), (4, 4, 7), (2, 6, 9), (0, 3, 4), (3, 0, 4)]


def rv(lo=-4, hi=5):
    while True:
        v = tuple(R.randint(lo, hi) for _ in range(3))
        if any(v):
            return v


def recta(P, v):
    return "(x, y, z) = %s + λ%s" % (V(*P), V(*v))


def s_planos():
    n = rv(-3, 4)
    d = R.randint(-8, 8)
    k = R.choice([2, 3, -2])
    t = R.choice(["paralelos", "coincidentes", "secantes", "secantes", "perp"])
    if t == "paralelos":
        n2, d2 = tuple(k * x for x in n), k * d + R.choice([1, 3, -2, 5])
    elif t == "coincidentes":
        n2, d2 = tuple(k * x for x in n), k * d
    elif t == "perp":
        n2 = cruz(n, rv(-2, 2))
        if not any(n2):
            return None
        n2, d2 = simp(n2), R.randint(-5, 5)
    else:
        n2, d2 = rv(-3, 4), R.randint(-5, 5)
        if not any(cruz(n, n2)) or esc(n, n2) == 0:
            return None
    ok = {"paralelos": "paralelos", "coincidentes": "coincidentes", "secantes": "secantes (se cortan en una recta)", "perp": "secantes y perpendiculares"}[t]
    return M("¿Cuál es la posición relativa de π₁: %s y π₂: %s?" % (plano(n, d), plano(n2, d2)), ok, [o for o in ["paralelos", "coincidentes", "secantes (se cortan en una recta)", "secantes y perpendiculares"] if o != ok],
             "Comparamos los vectores normales %s y %s%s: <b>%s</b>." % (V(*n), V(*n2), " (y los términos independientes)" if t in ("paralelos", "coincidentes") else "", ok))


def s_recta_plano():
    n = rv(-3, 4)
    d = R.randint(-6, 6)
    P = rv(-3, 3)
    t = R.choice(["contenida", "paralela", "secante", "secante", "corte"])
    while True:
        v = rv(-3, 3)
        if (esc(n, v) == 0) == (t in ("contenida", "paralela")):
            break
    if t == "contenida":
        d = -esc(n, P)
    elif t == "paralela":
        d = -esc(n, P) + R.choice([1, 2, -3])
    if t == "corte":
        lam = R.randint(-3, 3)
        Q = add(P, tuple(lam * x for x in v))
        d = -esc(n, Q)
        return M("¿En qué punto corta la recta r: %s al plano %s?" % (recta(P, v), plano(n, d)), V(*Q), W([V(*P), V(*add(P, tuple((lam + 1) * x for x in v))), V(*add(Q, (0, 1, 0))), V(*v)]),
                 "Sustituimos las paramétricas en el plano: λ = %s → <b>%s</b>." % (sg(lam), V(*Q)))
    ok = {"contenida": "la recta está contenida en el plano", "paralela": "la recta es paralela al plano", "secante": "la recta corta al plano en un punto"}[t]
    return M("¿Cuál es la posición de r: %s respecto del plano %s?" % (recta(P, v), plano(n, d)), ok, [o for o in ["la recta está contenida en el plano", "la recta es paralela al plano", "la recta corta al plano en un punto", "la recta es perpendicular a sí misma"] if o != ok],
             "v · n = %s%s → <b>%s</b>." % (sg(esc(n, v)), (" y el punto P %s en el plano" % ("está" if t == "contenida" else "no está")) if t != "secante" else "", ok))


def s_rectas():
    P, u = rv(-3, 3), rv(-2, 3)
    t = R.choice(["paralelas", "cortan", "cruzan", "cruzan", "coinc"])
    if t == "paralelas":
        k = R.choice([2, -1, 3])
        v = tuple(k * x for x in u)
        Q = add(P, (1, 0, 0)) if any(cruz(u, (1, 0, 0))) else add(P, (0, 1, 0))
    elif t == "coinc":
        v = tuple(2 * x for x in u)
        Q = add(P, u)
    else:
        v = rv(-2, 3)
        if not any(cruz(u, v)):
            return None
        if t == "cortan":
            X = add(P, tuple(R.randint(1, 2) * x for x in u))
            Q = add(X, tuple(-R.randint(1, 2) * x for x in v))
        else:
            Q = add(P, cruz(u, v))
    PQ = add(Q, P, -1)
    det = det3([list(PQ), list(u), list(v)])
    if t == "cortan" and det != 0 or t == "cruzan" and det == 0:
        return None
    ok = {"paralelas": "paralelas", "coinc": "coincidentes", "cortan": "se cortan en un punto", "cruzan": "se cruzan (no son coplanarias)"}[t]
    return M("¿Cuál es la posición relativa de r: %s y s: %s?" % (recta(P, u), recta(Q, v)), ok, [o for o in ["paralelas", "coincidentes", "se cortan en un punto", "se cruzan (no son coplanarias)"] if o != ok],
             "Comparamos los directores y estudiamos [PQ, u, v] = %s: <b>%s</b>." % (sg(det), ok))


def s_angulos():
    t = R.choice(["rr", "pp", "rp", "rp"])
    u, v = rv(-3, 3), rv(-3, 3)
    c = abs(esc(u, v)) / math.sqrt(mod2(u) * mod2(v))
    A = math.degrees(math.acos(min(1, c)))
    if t == "rp":
        A = 90 - A
        ok = "%s°" % r2(A, 1)
        d = R.randint(-5, 5)
        return M("Calcula el ángulo entre la recta de director u = %s y el plano %s (a las décimas)." % (V(*u), plano(v, d)), ok, W(["%s°" % r2(90 - A, 1), "%s°" % r2(180 - A, 1), "%s°" % r2(A / 2, 1)]), "sen α = |u · n|/(|u||n|) (se usa el normal): α ≈ <b>%s</b>." % ok)
    ok = "%s°" % r2(A, 1)
    if t == "pp":
        return M("Calcula el ángulo entre los planos %s y %s (a las décimas)." % (plano(u, R.randint(-4, 4)), plano(v, R.randint(-4, 4))), ok, W(["%s°" % r2(180 - A, 1), "%s°" % r2(90 - A, 1), "%s°" % r2(A / 2, 1)]), "cos α = |n₁ · n₂|/(|n₁||n₂|) → α ≈ <b>%s</b>." % ok)
    return M("Calcula el ángulo entre dos rectas con vectores directores %s y %s (a las décimas)." % (V(*u), V(*v)), ok, W(["%s°" % r2(180 - A, 1), "%s°" % r2(90 - A, 1), "%s°" % r2(A + 10, 1)]), "cos α = |u · v|/(|u||v|) → α ≈ <b>%s</b>." % ok)


def s_distancias():
    t = R.choice(["pp", "pp", "par", "pr", "pr"])
    a, b, c = R.choice(TRN)
    n = (a * R.choice([1, -1]), b, c * R.choice([1, -1]))
    m = int(math.isqrt(mod2(n)))
    if t == "pp":
        P = rv(-4, 4)
        d = R.randint(-9, 9)
        val = esc(n, P) + d
        if val == 0:
            return None
        dist = F(abs(val), m)
        return M("Calcula la distancia del punto P%s al plano %s." % (V(*P), plano(n, d)), nf(dist), W([nf(F(val, m)) if val < 0 else nf(F(abs(val), m * m)), sg(abs(val)), nf(F(abs(esc(n, P)), m)) if esc(n, P) and F(abs(esc(n, P)), m) != dist else nf(dist + 1), nf(dist * 2)]),
                 "d = |%s|/√%d = %d/%d = <b>%s</b>." % (sg(val), mod2(n), abs(val), m, nf(dist)))
    if t == "par":
        d1 = R.randint(-6, 6)
        d2 = d1 + m * R.choice([1, 2, 3, -2])
        dist = F(abs(d2 - d1), m)
        return M("Calcula la distancia entre los planos paralelos %s y %s." % (plano(n, d1), plano(n, d2)), nf(dist), W([sg(abs(d2 - d1)), nf(F(abs(d2 + d1), m)) if d1 + d2 else "1", nf(F(abs(d2 - d1), m * m)), nf(dist + 1)]), "d = |d₁ − d₂|/|n| = %d/%d = <b>%s</b>." % (abs(d2 - d1), m, nf(dist)))
    P = rv(-3, 3)
    u = (a, b, c)
    Q = add(add(P, cruz(u, (0, 0, 1)) if any(cruz(u, (0, 0, 1))) else (1, 0, 0)), tuple(R.choice([1, -1]) * x for x in u))
    w = cruz(add(Q, P, -1), u)
    dist2 = F(mod2(w), mod2(u))
    num_, den = mod2(w), mod2(u)
    from fractions import Fraction
    dd = Fraction(num_, den)
    rt_num, rt_den = math.isqrt(dd.numerator), math.isqrt(dd.denominator)
    if rt_num ** 2 == dd.numerator and rt_den ** 2 == dd.denominator:
        ok = nf(Fraction(rt_num, rt_den))
    else:
        ok = raiz(int(dd)) if dd.denominator == 1 else r2(math.sqrt(dd))
    return M("Calcula la distancia del punto Q%s a la recta r: %s%s." % (V(*Q), recta(P, u), " (a las centésimas)" if "," in ok else ""), ok, W([r2(math.sqrt(mod2(add(Q, P, -1)))), r2(math.sqrt(float(dd)) * 2), r2(math.sqrt(mod2(w))), r2(math.sqrt(float(dd)) + 1)]),
             "d = |PQ × u|/|u| = √%d/√%d → <b>%s</b>." % (num_, den, ok))


def s_proyeccion():
    a, b, c = R.choice(TRN)
    n = (a, b * R.choice([1, -1]), c)
    m2 = mod2(n)
    H = rv(-3, 3)
    d = -esc(n, H)
    k = R.choice([1, 2, -1])
    P = add(H, tuple(k * x for x in n))
    t = R.choice(["proy", "proy", "sim", "perp"])
    if t == "proy":
        return M("Halla la proyección ortogonal del punto P%s sobre el plano %s." % (V(*P), plano(n, d)), V(*H), W([V(*add(P, tuple(2 * k * x for x in n), -1)), V(*add(P, n)), V(*add(H, (1, 0, 0)))]), "Recta por P con dirección n; su corte con el plano es <b>%s</b>." % V(*H))
    if t == "sim":
        S = add(P, tuple(2 * k * x for x in n), -1)
        return M("Halla el simétrico del punto P%s respecto del plano %s." % (V(*P), plano(n, d)), V(*S), W([V(*H), V(*tuple(-x for x in P)), V(*add(P, n, -1))]), "La proyección es M%s y M es el punto medio de P y P′: P′ = 2M − P = <b>%s</b>." % (V(*H), V(*S)))
    return M("Halla la recta perpendicular al plano %s que pasa por P%s." % (plano(n, d), V(*P)), recta(P, n), W([recta(n, P), recta(P, cruz(n, (1, 0, 0))) if any(cruz(n, (1, 0, 0))) else recta(P, (1, 1, 1)), recta(H, P)]), "Su vector director es el normal del plano: <b>%s</b>." % recta(P, n))


seen = set()
sets = [("Posición de dos planos", mix(R, seen, [(s_planos, 20)])), ("Recta y plano, dos rectas", mix(R, seen, [(s_recta_plano, 10), (s_rectas, 10)])), ("Ángulos", mix(R, seen, [(s_angulos, 20)])),
        ("Distancias", mix(R, seen, [(s_distancias, 20)])), ("Proyecciones y simétricos", mix(R, seen, [(s_proyeccion, 14), (s_rectas, 6)]))]
think = ["<b>Dos planos</b>: si los normales son proporcionales, son paralelos o coincidentes; si no, se cortan en una recta.",
         "<b>Recta y plano</b>: si v · n = 0, la recta es paralela o está contenida; si no, corta en un punto. <b>Dos rectas</b>: paralelas, coincidentes, se cortan o se cruzan (estudiando [PQ, u, v]).",
         "<b>Ángulos</b>: entre rectas, cos α = |u · v|/(|u||v|); entre planos, con los normales; entre recta y plano, sen α = |u · n|/(|u||n|).",
         "<b>Distancia</b> de P(x₀, y₀, z₀) al plano ax + by + cz + d = 0: |ax₀ + by₀ + cz₀ + d| / √(a² + b² + c²)."]
ex = [("P(1, 2, 3) y el plano 2x + y + 2z − 1 = 0", ["|2 + 2 + 6 − 1| / 3"], "d = 3")]
mist = [["Ángulo recta-plano con coseno", "Con el normal se usa el seno (o 90° menos el ángulo)."], ["Distancia negativa", "Valor absoluto en el numerador."], ["Confundir cruzarse con cortarse", "Si se cruzan no tienen ningún punto común."]]
body = L(think, ex, mist)
faq = [("¿Qué significa que dos rectas se crucen?", "Que no son paralelas ni se cortan: están en planos distintos (por ejemplo, una carretera que pasa por un puente sobre otra)."),
       ("¿Cómo se calcula el simétrico de un punto respecto de un plano?", "Se halla la proyección M (corte de la perpendicular con el plano) y se usa que M es el punto medio de P y su simétrico.")]
unit(2, R, "posiciones-angulos-y-distancias", "E", "Posiciones relativas de rectas y planos, ángulos, distancias, proyecciones y simetrías en el espacio",
     "Posiciones, ángulos y distancias en el espacio", "Ángulos y distancias", "Fichas de Matemáticas II (2.º de Bachillerato): posiciones relativas de rectas y planos, ángulos, distancias, proyecciones y simétricos. 100 ejercicios.",
     "d(P, π) = |n · P + d| / |n|", "Recta y plano: el ángulo con el seno.", body, faq, sets, 6)
