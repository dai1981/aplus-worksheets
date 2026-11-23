# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Polinomios, ecuaciones e inecuaciones (Sentido algebraico)
Teorema del resto y Ruffini, factorización de polinomios, ecuaciones polinómicas de grado mayor que 2, fracciones algebraicas y ecuaciones racionales,
inecuaciones polinómicas y racionales (tabla de signos).
Errores: olvidar el cero en Ruffini, cerrar el intervalo en un valor que anula el denominador, perder soluciones al dividir entre x.
"""
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, fq, num, unit, L, E, poly, sol, MINUS, nf, W

R = random.Random(51003)
INF, MINF = "+∞", MINUS + "∞"


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def from_roots(rs, lead=1):
    p = [lead]
    for r in rs:
        p = pmul(p, [1, -r])
    return p


def ev(p, x):
    v = 0
    for c in p:
        v = v * x + c
    return v


def fac(rs, lead=1):
    out = "" if lead == 1 else ("%s" % sg(lead) if lead != -1 else MINUS)
    for r in sorted(set(rs)):
        k = rs.count(r)
        f = "x" if r == 0 else "(x %s %d)" % ("−" if r > 0 else "+", abs(r))
        out += f + ("²" if k == 2 else "³" if k == 3 else "")
    return out


def ivl(a, b, ca=False, cb=False):
    return "%s%s, %s%s" % ("[" if ca else "(", MINF if a is None else nf(a), INF if b is None else nf(b), "]" if cb else ")")


def s_resto():
    t = R.choice(["resto", "resto", "k", "raiz"])
    rs = [R.randint(-4, 4) for _ in range(3)]
    p = from_roots(rs)
    p[-1] += R.randint(-6, 6)
    a = R.randint(-3, 3)
    if t == "resto":
        r = ev(p, a)
        return M("¿Cuál es el resto de dividir %s entre %s?" % (poly(p), E((1, "x"), (-a, ""))), sg(r), [sg(ev(p, -a)) if ev(p, -a) != r else sg(r + 1), sg(p[-1]) if p[-1] != r else sg(r - 1), "0" if r else "1"], "Teorema del resto: P(%s) = <b>%s</b>." % (sg(a), sg(r)))
    if t == "k":
        b, c = R.randint(-5, 5), R.randint(-5, 5)
        if b == 0 or c == 0 or a == 0:
            return None
        k = -(a ** 3 + b * a * a + c * a)
        return M("¿Qué valor de k hace que x³ %s %s + k sea divisible entre %s?" % (("+ %dx²" % b) if b > 0 else ("− %dx²" % -b) if b < 0 else "", ("+ %dx" % c) if c > 0 else ("− %dx" % -c) if c < 0 else "", E((1, "x"), (-a, ""))),
                 "k = %s" % sg(k), ["k = %s" % sg(-k) if k else "k = 1", "k = %s" % sg(a), "k = %s" % sg(k + a) if a else "k = %s" % sg(k + 2)], "P(%s) = 0 → %s + k = 0 → <b>k = %s</b>." % (sg(a), sg(-k), sg(k)))
    rs = R.sample(range(-4, 5), 3)
    p = from_roots(rs)
    cand = [x for x in range(-6, 7) if x not in rs and abs(x) <= 6]
    R.shuffle(cand)
    r = R.choice(rs)
    return M("¿Cuál de estos números es raíz de P(x) = %s?" % poly(p), sg(r), [sg(x) for x in cand[:3]], "P(%s) = 0: <b>%s</b> es raíz." % (sg(r), sg(r)))


def s_factorizar():
    t = R.choice(["c3", "c3", "c3", "comun", "doble"])
    if t == "comun":
        rs = [0] + R.sample([x for x in range(-5, 6) if x], 2)
    elif t == "doble":
        r = R.choice([x for x in range(-4, 5) if x])
        rs = [r, r, R.choice([x for x in range(-4, 5) if x != r])]
    else:
        rs = R.sample([x for x in range(-5, 6) if x], 3)
    lead = R.choice([1, 1, 1, 2])
    p = from_roots(rs, lead)
    ok = fac(rs, lead)
    alt = [fac([-r for r in rs], lead), fac(rs[:2] + [rs[2] + 1], lead), fac(rs, 1) if lead != 1 else fac(rs[:1] + [-rs[1]] + rs[2:], lead)]
    return M("Factoriza P(x) = %s." % poly(p), ok, alt, "Con Ruffini buscamos raíces entre los divisores del término independiente: %s. <b>%s</b>." % (", ".join(sg(r) for r in sorted(set(rs))), ok))


def s_ecuacion():
    t = R.choice(["c3", "c3", "c4", "racional", "racional2"])
    if t == "c3":
        rs = R.sample(range(-5, 6), 3)
        p = from_roots(rs)
        return M("Resuelve %s = 0." % poly(p), sol(sorted(rs)), [sol(sorted(-r for r in rs)), sol(sorted(rs[:2])), sol(sorted([rs[0], rs[1], rs[2] + 1]))], "Ruffini: <b>%s</b>." % sol(sorted(rs)))
    if t == "c4":
        a, b = R.sample(range(1, 5), 2)
        rs = [a, -a, b, -b] if R.random() < 0.5 else [0, 0, a, -a]
        p = from_roots(rs)
        xs = sorted(set(rs))
        return M("Resuelve %s = 0." % poly(p), sol(xs), [sol(sorted(set(abs(x) for x in xs))), sol(sorted(set(x * x for x in xs))), sol(xs[:-1])], "Factorizamos (factor común o bicuadrada): <b>%s</b>." % sol(xs))
    if t == "racional":
        r1, r2 = R.sample([x for x in range(-6, 7) if x not in (0, 1)], 2)
        # 1/(x − 1) + k/x … simpler: (x + a)/(x − 1) = b/(x − 1)·… use x − s + p/x form shifted
        a = R.randint(1, 4)
        # x/(x − a) + ... keep classic: 2/x + x/(x + a) = ... too complex; use (x² ...)/(x − a)
        s_, pr = r1 + r2, r1 * r2
        if a in (r1, r2):
            return None
        eq = "(x² %s %s)/(x − %d) = %s" % ("+" if pr >= 0 else "−", abs(pr), a, E((s_, ""), (0, ""))) if False else None
        # x²/(x − a) form: x² + p = s(x)... use: (x² + pr)/x = s_
        if pr == 0:
            return None
        eq = "(x² %s %d) / x = %s" % ("+" if pr > 0 else "−", abs(pr), sg(s_))
        return M("Resuelve %s." % eq, sol(sorted([r1, r2])), [sol(sorted([-r1, -r2])), "x = %s" % sg(s_), sol(sorted([r1, r2, 0]))], "x² %s %d = %sx → %s = 0 → <b>%s</b> (ninguna anula el denominador)." % ("+" if pr > 0 else "−", abs(pr), sg(s_), poly([1, -s_, pr]), sol(sorted([r1, r2]))))
    a = R.randint(1, 5)
    b = R.randint(1, 5)
    if a == b:
        return None
    # 1/(x − a) − 1/(x − b) = (a − b)/((x − a)(x − b)) ... trap: x/(x − a) = a/(x − a) → x = a, no vale
    k = R.randint(2, 4)
    eq = "x/(x − %d) + %d = %d/(x − %d)" % (a, k, a, a)
    return M("Resuelve %s." % eq, "no tiene solución", ["x = %d" % a, "x = %s" % nf(F(k * a, k + 1)), "x = %s" % nf(F(a, k))],
             "x + %d(x − %d) = %d → %dx = %d → x = %d, pero x = %d anula el denominador: <b>no tiene solución</b>." % (k, a, a, k + 1, a * (k + 1), a, a))


def s_inecuacion():
    t = R.choice(["cuad", "cuad", "cub", "rac", "rac"])
    if t == "cuad":
        r1, r2 = sorted(R.sample(range(-6, 7), 2))
        op = R.choice(["&lt;", "&gt;", "≤", "≥"])
        neg = op in ("&lt;", "≤")
        cl = op in ("≤", "≥")
        ok = ivl(r1, r2, cl, cl) if neg else "%s ∪ %s" % (ivl(None, r1, False, cl), ivl(r2, None, cl, False))
        out = "%s ∪ %s" % (ivl(None, r1, False, cl), ivl(r2, None, cl, False)) if neg else ivl(r1, r2, cl, cl)
        return M("Resuelve %s %s 0." % (poly([1, -(r1 + r2), r1 * r2]), op), ok, [out, ivl(r1, r2, not cl, not cl) if neg else "%s ∪ %s" % (ivl(None, r1, False, not cl), ivl(r2, None, not cl, False)), ivl(-r2, -r1, cl, cl)],
                 "Raíces %s y %s; entre ellas el polinomio es negativo. <b>%s</b>." % (sg(r1), sg(r2), ok))
    if t == "cub":
        r1, r2, r3 = sorted(R.sample(range(-5, 6), 3))
        op = R.choice(["&gt;", "&lt;"])
        pos = op == "&gt;"
        ok = "%s ∪ %s" % (ivl(r1, r2), ivl(r3, None)) if pos else "%s ∪ %s" % (ivl(None, r1), ivl(r2, r3))
        other = "%s ∪ %s" % (ivl(None, r1), ivl(r2, r3)) if pos else "%s ∪ %s" % (ivl(r1, r2), ivl(r3, None))
        return M("Resuelve %s %s 0." % (fac([r1, r2, r3]), op), ok, [other, ivl(r1, r3), "%s ∪ %s" % (ivl(r1, r2, True, True), ivl(r3, None, True))], "Tabla de signos con las raíces %s, %s y %s (de derecha a izquierda: +, −, +, −). <b>%s</b>." % (sg(r1), sg(r2), sg(r3), ok))
    a, b = R.sample(range(-6, 7), 2)
    op = R.choice(["≥", "≤"])
    pos = op == "≥"
    lo, hi = min(a, b), max(a, b)
    # (x − a)/(x − b): numerator root a included, denominator root b excluded
    cla = lambda v: v == a
    if pos:
        ok = "%s ∪ %s" % (ivl(None, lo, False, cla(lo)), ivl(hi, None, cla(hi), False))
        wr = "%s ∪ %s" % (ivl(None, lo, False, True), ivl(hi, None, True, False))
    else:
        ok = ivl(lo, hi, cla(lo), cla(hi))
        wr = ivl(lo, hi, True, True)
    return M("Resuelve (%s)/(%s) %s 0." % (E((1, "x"), (-a, "")), E((1, "x"), (-b, "")), op), ok, [wr, ivl(lo, hi, cla(lo), cla(hi)) if pos else "%s ∪ %s" % (ivl(None, lo, False, cla(lo)), ivl(hi, None, cla(hi), False)), ivl(lo, hi)],
             "Puntos críticos %s y %s; x = %s anula el denominador y nunca se incluye. <b>%s</b>." % (sg(a), sg(b), sg(b), ok))


def s_fraccion():
    t = R.choice(["simp", "simp", "suma", "prod"])
    a, b = R.sample([x for x in range(-5, 6) if x], 2)
    if t == "simp":
        c = R.choice([x for x in range(-5, 6) if x not in (a, b)])
        nume = poly(from_roots([a, c]))
        den = poly(from_roots([a, b]))
        ok = "(%s)/(%s)" % (E((1, "x"), (-c, "")), E((1, "x"), (-b, "")))
        return M("Simplifica (%s)/(%s)." % (nume, den), ok, ["(%s)/(%s)" % (E((1, "x"), (c, "")), E((1, "x"), (b, ""))), "%s/%s" % (sg(c * a), sg(a * b)), "(%s)/(%s)" % (E((1, "x"), (-a, "")), E((1, "x"), (-b, "")))],
                 "Factorizamos: (x %s %d)(x %s %d) / ((x %s %d)(x %s %d)) y simplificamos el factor común: <b>%s</b>." % ("−" if a > 0 else "+", abs(a), "−" if c > 0 else "+", abs(c), "−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b), ok))
    if t == "suma":
        nume = E((2, "x"), (-(a + b), ""))
        den = poly(from_roots([a, b]))
        ok = "(%s)/(%s)" % (nume, den)
        return M("Calcula 1/(%s) + 1/(%s)." % (E((1, "x"), (-a, "")), E((1, "x"), (-b, ""))), ok, ["2/(%s)" % E((2, "x"), (-(a + b), "")), "2/(%s)" % den, "(%s)/(%s)" % (E((2, "x"), (a + b, "")), den)], "Denominador común (x %s %d)(x %s %d): <b>%s</b>." % ("−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b), ok))
    k = R.randint(2, 5)
    ok = "%d/(%s)" % (k, E((1, "x"), (-b, "")))
    return M("Calcula (%s)/(%s) · %d/(%s)." % (E((1, "x"), (-a, "")), E((1, "x"), (-b, "")), k, E((1, "x"), (-a, ""))), ok, ["%d/(%s)" % (k, E((1, "x"), (-a, ""))), "%d(%s)/(%s)" % (k, E((1, "x"), (-a, "")), E((1, "x"), (-b, ""))), "%d" % k], "Se simplifica (%s) arriba y abajo: <b>%s</b>." % (E((1, "x"), (-a, "")), ok))


seen = set()
sets = [("Teorema del resto y raíces", mix(R, seen, [(s_resto, 20)])), ("Factorizar polinomios", mix(R, seen, [(s_factorizar, 20)])), ("Fracciones algebraicas", mix(R, seen, [(s_fraccion, 20)])),
        ("Ecuaciones polinómicas y racionales", mix(R, seen, [(s_ecuacion, 20)])), ("Inecuaciones", mix(R, seen, [(s_inecuacion, 20)]))]
think = ["<b>Teorema del resto</b>: el resto de dividir P(x) entre x − a es P(a). Si P(a) = 0, a es <b>raíz</b> y x − a es un factor.",
         "Para <b>factorizar</b>, se prueban con Ruffini los divisores del término independiente.",
         "En las ecuaciones con x en el denominador, se comprueba que la solución no anula ningún denominador.",
         "<b>Inecuaciones</b>: se buscan las raíces y se estudia el signo en cada intervalo (tabla de signos). Los valores que anulan un denominador nunca se incluyen."]
ex = [("x³ − 2x² − 5x + 6 = 0", ["x = 1 es raíz", "x² − x − 6 = 0"], "x₁ = −2, x₂ = 1, x₃ = 3"), ("(x − 1)/(x + 2) ≥ 0", ["críticos −2 y 1"], "(−∞, −2) ∪ [1, +∞)")]
mist = [["Olvidar el término que falta en Ruffini", "Escribe 0 en los huecos: x³ − 4 → 1, 0, 0, −4."], ["Cerrar el intervalo donde se anula el denominador", "Ese valor no está en el dominio."], ["Dividir entre x", "Se pierde la solución x = 0: saca factor común."]]
body = L(think, ex, mist)
faq = [("¿Qué raíces pruebo en Ruffini?", "Los divisores del término independiente (positivos y negativos); si el coeficiente principal no es 1, también fracciones."),
       ("¿Cómo se hace una tabla de signos?", "Se ordenan los puntos críticos en la recta y se mira el signo de cada factor en cada trozo; el producto da el signo final.")]
unit(1, R, "ecuaciones-e-inecuaciones", "A", "Polinomios: teorema del resto, factorización y fracciones algebraicas; ecuaciones polinómicas y racionales; inecuaciones polinómicas y racionales",
     "Polinomios, ecuaciones e inecuaciones", "Ecuaciones e inecuaciones", "Fichas de Matemáticas I (1.º de Bachillerato): teorema del resto, Ruffini, factorizar, fracciones algebraicas, ecuaciones de grado 3 y 4, inecuaciones. 100 ejercicios con soluciones.",
     "Si P(a) = 0, x − a es un factor", "En inecuaciones, estudia el signo por trozos.", body, faq, sets, 3)
