# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Integrales definidas y áreas (Sentido de la medida)
Regla de Barrow, propiedades, área bajo una curva, área cuando la función cambia de signo, área entre dos curvas, teorema fundamental del cálculo, aplicaciones.
Errores: restar al revés en Barrow, dar un área negativa, integrar de golpe cuando la función corta el eje X.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, poly, nf, kurve, BLUE, RED, W, MINUS, par

R = random.Random(52011)


def prim(cs):
    n = len(cs) - 1
    return [F(c, n - i + 1) for i, c in enumerate(cs)] + [0]


def ev(cs, x):
    v = F(0)
    for c in cs:
        v = v * x + c
    return v


def integ(cs, a, b):
    P = prim(cs)
    return ev(P, b) - ev(P, a)


def s_barrow():
    t = R.choice(["poli", "poli", "poli", "exp", "inv", "trig"])
    if t == "poli":
        cs = [R.choice([1, 2, 3, -1]), R.randint(-4, 4), R.randint(-5, 5)][R.randint(0, 1):]
        a, b = sorted(R.sample(range(-2, 4), 2))
        v = integ(cs, a, b)
        return M("Calcula ∫<sub>%s</sub><sup>%s</sup> (%s) dx." % (sg(a), sg(b), poly(cs)), nf(v), W([nf(-v) if v else "1", nf(ev(cs, b) - ev(cs, a)), nf(ev(prim(cs), b)), nf(v + 1)]), "Barrow: F(%s) − F(%s) con F(x) = %s → <b>%s</b>." % (sg(b), sg(a), poly(prim(cs)), nf(v)))
    if t == "exp":
        k = R.randint(1, 3)
        return M("Calcula ∫<sub>0</sub><sup>%d</sup> eˣ dx." % k, "e<sup>%d</sup> − 1" % k if k > 1 else "e − 1", ["e<sup>%d</sup>" % k if k > 1 else "e", "e<sup>%d</sup> + 1" % k if k > 1 else "e + 1", "1 − e<sup>%d</sup>" % k if k > 1 else "1 − e"], "[eˣ] de 0 a %d = e<sup>%d</sup> − e⁰ = <b>%s</b>." % (k, k, "e<sup>%d</sup> − 1" % k if k > 1 else "e − 1"))
    if t == "inv":
        k = R.choice([2, 3, 5, 10])
        return M("Calcula ∫<sub>1</sub><sup>%d</sup> 1/x dx." % k, "ln %d" % k, ["%s" % nf(F(1, k) - 1), "ln %d − 1" % k, "%s" % nf(F(k * k - 1, 2))], "[ln x] de 1 a %d = ln %d − ln 1 = <b>ln %d</b>." % (k, k, k))
    q, a, w = R.choice([("∫<sub>0</sub><sup>π</sup> sen x dx", "2", ["0", "1", "−2"]), ("∫<sub>0</sub><sup>π/2</sup> cos x dx", "1", ["0", "−1", "π/2"]), ("∫<sub>0</sub><sup>2π</sup> sen x dx", "0", ["2", "4", "π"]),
                        ("∫<sub>0</sub><sup>π/2</sup> sen x dx", "1", ["0", "2", "−1"])])
    return M("Calcula %s." % q, a, w, "Regla de Barrow con la primitiva (−cos x o sen x): <b>%s</b>." % a)


def s_propiedades():
    t = R.choice(["suma", "inv", "par", "teo", "k"])
    a, b, c = sorted(R.sample(range(-3, 8), 3))
    p, q = R.randint(-6, 9), R.randint(-6, 9)
    if t == "suma":
        return M("Si ∫<sub>%s</sub><sup>%s</sup> f = %s y ∫<sub>%s</sub><sup>%s</sup> f = %s, ¿cuánto vale ∫<sub>%s</sub><sup>%s</sup> f?" % (sg(a), sg(b), sg(p), sg(b), sg(c), sg(q), sg(a), sg(c)), sg(p + q), W([sg(p - q), sg(q - p), sg(p * q), sg(p + q + 1)]), "Se suman los intervalos contiguos: <b>%s</b>." % sg(p + q))
    if t == "inv":
        return M("Si ∫<sub>%s</sub><sup>%s</sup> f(x) dx = %s, ¿cuánto vale ∫<sub>%s</sub><sup>%s</sup> f(x) dx?" % (sg(a), sg(b), sg(p), sg(b), sg(a)), sg(-p), W([sg(p), "0", nf(F(1, p)) if p else "1", sg(-p + 1)]), "Al cambiar los límites cambia el signo: <b>%s</b>." % sg(-p))
    if t == "k":
        k = R.choice([2, 3, -2, 5])
        return M("Si ∫<sub>%s</sub><sup>%s</sup> f(x) dx = %s, ¿cuánto vale ∫<sub>%s</sub><sup>%s</sup> %s f(x) dx?" % (sg(a), sg(b), sg(p), sg(a), sg(b), sg(k)), sg(k * p), W([sg(p + k), sg(p), sg(k * p + k), nf(F(p, k))]), "Las constantes salen fuera: %s · %s = <b>%s</b>." % (sg(k), par(p), sg(k * p)))
    if t == "par":
        n = R.choice([3, 5])
        aa = R.randint(1, 4)
        return M("Calcula ∫<sub>−%d</sub><sup>%d</sup> x%s dx." % (aa, aa, "³" if n == 3 else "⁵"), "0", [sg(2 * aa ** (n + 1) // (n + 1)) if (2 * aa ** (n + 1)) % (n + 1) == 0 else nf(F(2 * aa ** (n + 1), n + 1)), nf(F(aa ** (n + 1), n + 1)), sg(aa ** n)], "x%s es impar: las áreas a cada lado se compensan, <b>0</b>." % ("³" if n == 3 else "⁵"))
    q_, a_, w = R.choice([("Si F(x) = ∫<sub>0</sub><sup>x</sup> f(t) dt con f continua, entonces F′(x) es…", "f(x)", ["F(x)", "f′(x)", "0"]),
                          ("Si F(x) = ∫<sub>1</sub><sup>x</sup> t² dt, ¿cuánto vale F′(3)?", "9", ["3", "26/3", "6"]),
                          ("∫<sub>a</sub><sup>a</sup> f(x) dx vale…", "0", ["f(a)", "a", "1"]), ("Si f(x) ≥ 0 en [a, b], ∫<sub>a</sub><sup>b</sup> f(x) dx es…", "el área bajo la curva (mayor o igual que 0)", ["negativa", "la pendiente media", "f(b) − f(a)"])])
    return M(q_, a_, w, "Teorema fundamental del cálculo y propiedades: <b>%s</b>." % a_)


def s_area():
    t = R.choice(["simple", "simple", "cambio", "parabola"])
    if t == "simple":
        a = R.randint(1, 3)
        k = R.randint(1, 5)
        b = R.randint(1, 4)
        cs = [a, 0, k]
        v = integ(cs, 0, b)
        pic = kurve([(lambda x: a * x * x + k, BLUE, "")], (-1, 5, 1), (0, a * b * b + k + 2, 5 if a * b * b + k > 12 else 2), W=320, H=240, label="área bajo una parábola", shade=None) if False else ""
        return M("Calcula el área limitada por f(x) = %s, el eje X y las rectas x = 0 y x = %d." % (poly(cs), b), "%s u²" % nf(v), W(["%s u²" % nf(ev(cs, b)), "%s u²" % nf(v * 2), "%s u²" % nf(v - k * b), "%s u²" % nf(v + 1)]), "f &gt; 0 en [0, %d]: A = ∫<sub>0</sub><sup>%d</sup> f = <b>%s u²</b>." % (b, b, nf(v)))
    if t == "parabola":
        r = R.randint(1, 4)
        cs = [-1, 0, r * r]
        v = integ(cs, -r, r)
        return M("Calcula el área limitada por f(x) = %s y el eje X." % poly(cs), "%s u²" % nf(v), W(["%s u²" % nf(v / 2), "%s u²" % nf(F(2 * r ** 3)), "%s u²" % nf(-v), "%s u²" % nf(v + 2)]), "Corta al eje X en ±%d: A = ∫<sub>−%d</sub><sup>%d</sup> (%s) dx = <b>%s u²</b>." % (r, r, r, poly(cs), nf(v)))
    r = R.randint(1, 3)
    cs = [1, -r]
    b = r + R.randint(1, 3)
    A1 = abs(integ(cs, 0, r))
    A2 = abs(integ(cs, r, b))
    tot = A1 + A2
    neto = integ(cs, 0, b)
    return M("Calcula el área entre f(x) = %s, el eje X y las rectas x = 0 y x = %d." % (E((1, "x"), (-r, "")), b), "%s u²" % nf(tot), W(["%s u²" % nf(abs(neto)) if abs(neto) != tot else "%s u²" % nf(tot + 1), "%s u²" % nf(A2), "%s u²" % nf(A1 * 2), "%s u²" % nf(neto)]),
             "f cambia de signo en x = %d: A = |∫<sub>0</sub><sup>%d</sup> f| + |∫<sub>%d</sub><sup>%d</sup> f| = %s + %s = <b>%s u²</b>." % (r, r, r, b, nf(A1), nf(A2), nf(tot)))


def s_entre():
    t = R.choice(["recta_par", "recta_par", "dos_par", "dos_par"])
    if t == "recta_par":
        p, q = sorted(R.sample(range(-2, 5), 2))
        # entre y = x² y y = (p+q)x − pq
        diff = [-1, p + q, -p * q]
        v = integ(diff, p, q)
        line = E((p + q, "x"), (-p * q, ""))
        return M("Calcula el área entre la parábola y = x² y la recta y = %s." % line if line != "0" else "Calcula el área entre y = x² y el eje X.", "%s u²" % nf(v), W(["%s u²" % nf(integ([1, 0, 0], p, q)), "%s u²" % nf(-v), "%s u²" % nf(v * 2), "%s u²" % nf(v / 2)]),
                 "Se cortan en x = %s y x = %s; A = ∫ (recta − parábola) dx = <b>%s u²</b>." % (sg(p), sg(q), nf(v)))
    r = R.randint(1, 3)
    # entre y = x² y y = 2r² − x² → cortan en ±r ; diff = 2r² − 2x²
    v = integ([-2, 0, 2 * r * r], -r, r)
    return M("Calcula el área encerrada entre la parábola y = x² y la parábola y = %d − x²." % (2 * r * r), "%s u²" % nf(v), W(["%s u²" % nf(v / 2), "%s u²" % nf(integ([1, 0, 0], -r, r)), "%s u²" % nf(F(2 * r * r * 2 * r)), "%s u²" % nf(v + 1)]), "Se cortan en x = ±%d: A = ∫<sub>−%d</sub><sup>%d</sup> (%d − 2x²) dx = <b>%s u²</b>." % (r, r, r, 2 * r * r, nf(v)))


def s_aplicaciones():
    t = R.choice(["vel", "vel", "media", "cost"])
    if t == "vel":
        a, b = R.randint(1, 4), R.randint(0, 6)
        T = R.randint(2, 6)
        d = integ([a, b], 0, T)
        return M("Un móvil se mueve con velocidad v(t) = %s m/s. ¿Qué distancia recorre en los %d primeros segundos?" % (E((a, "t"), (b, "")), T), "%s m" % nf(d), W(["%s m" % nf(a * T + b), "%s m" % nf(F(a * T * T + b * T)), "%s m" % nf(d / T), "%s m" % nf(d + b)]), "d = ∫<sub>0</sub><sup>%d</sup> v(t) dt = <b>%s m</b>." % (T, nf(d)))
    if t == "media":
        b = R.randint(1, 4)
        v = F(b * b, 3)
        return M("Calcula el valor medio de f(x) = x² en [0, %d]." % b, nf(v), W([nf(F(b ** 3, 3)), nf(F(b * b, 2)), nf(F(b, 2)), nf(v + 1)]), "Valor medio = (1/%d) ∫<sub>0</sub><sup>%d</sup> x² dx = (1/%d) · %s = <b>%s</b>." % (b, b, b, nf(F(b ** 3, 3)), nf(v)))
    a = R.randint(2, 10)
    q = R.randint(5, 20)
    c = integ([2, a], 0, q)
    return M("El coste marginal de producir x unidades es C′(x) = 2x + %d €. ¿Cuánto aumenta el coste al pasar de 0 a %d unidades?" % (a, q), "%s €" % nf(c), W(["%s €" % nf(2 * q + a), "%s €" % nf(F(q * q)), "%s €" % nf(c / 2), "%s €" % nf(c + a)]), "∫<sub>0</sub><sup>%d</sup> (2x + %d) dx = %d² + %d · %d = <b>%s €</b>." % (q, a, q, a, q, nf(c)))


seen = set()
sets = [("Regla de Barrow", mix(R, seen, [(s_barrow, 20)])), ("Propiedades y teorema fundamental", mix(R, seen, [(s_propiedades, 20)])), ("Área bajo una curva", mix(R, seen, [(s_area, 20)])),
        ("Área entre dos curvas", mix(R, seen, [(s_entre, 14), (s_area, 6)])), ("Aplicaciones", mix(R, seen, [(s_aplicaciones, 20)]))]
think = ["<b>Regla de Barrow</b>: ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a), donde F es una primitiva de f.",
         "Si f ≥ 0 en [a, b], la integral es el área bajo la curva. Si f cambia de signo, se separa en trozos y se suman los valores absolutos.",
         "<b>Área entre dos curvas</b>: A = ∫<sub>a</sub><sup>b</sup> (f − g) dx, con f por encima de g entre los puntos de corte.",
         "<b>Teorema fundamental</b>: si F(x) = ∫<sub>a</sub><sup>x</sup> f(t) dt, entonces F′(x) = f(x)."]
ex = [("Área entre y = x² y y = 2x", ["cortes en 0 y 2", "∫<sub>0</sub><sup>2</sup> (2x − x²) dx"], "4/3 u²")]
mist = [["Restar F(a) − F(b)", "Es F(b) − F(a): el límite de arriba menos el de abajo."], ["Áreas negativas", "Un área siempre es positiva: usa valores absolutos."], ["Integrar de golpe si cambia de signo", "Separa el intervalo en los cortes con el eje X."]]
body = L(think, ex, mist, kurve([(lambda x: 2 * x, RED, "y = 2x"), (lambda x: x * x, BLUE, "y = x²")], (-1, 3, 1), (-1, 6, 1), W=300, H=260, label="área entre y = x² y y = 2x"))
faq = [("¿Qué diferencia hay entre integral definida e indefinida?", "La indefinida es una familia de funciones (F + C); la definida es un número (por ejemplo, un área)."),
       ("¿Para qué sirven las integrales definidas?", "Para calcular áreas, volúmenes, distancias recorridas a partir de la velocidad, trabajo o costes totales a partir del coste marginal.")]
unit(2, R, "integrales-definidas-y-areas", "M", "Integral definida: regla de Barrow, propiedades, teorema fundamental del cálculo, cálculo de áreas y aplicaciones",
     "Integrales definidas y áreas", "Integrales definidas", "Fichas de Matemáticas II (2.º de Bachillerato): regla de Barrow, propiedades, teorema fundamental, área bajo una curva y entre dos curvas. 100 ejercicios.",
     "∫ de a a b de f = F(b) − F(a)", "Un área nunca es negativa.", body, faq, sets, 11)
