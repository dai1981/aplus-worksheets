# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Lugares geométricos y cónicas (Sentido espacial)
Lugares geométricos (mediatriz, bisectriz, circunferencia), circunferencia (centro y radio, ecuación, posición de un punto y de una recta),
elipse, hipérbola y parábola (elementos, focos, excentricidad, ecuación reducida), reconocer cónicas.
Errores: olvidar completar cuadrados, confundir a y b en la elipse, c² = a² − b² (elipse) frente a c² = a² + b² (hipérbola).
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, E, nf, r2, raiz, V, W, MINUS, fq

R = random.Random(51009)
TR = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)]


def sq(v, k):
    """(x − a)²"""
    return "%s²" % ("(%s %s %d)" % (v, "−" if k > 0 else "+", abs(k)) if k else v)


def s_circ():
    a, b, r = R.randint(-6, 6), R.randint(-6, 6), R.randint(1, 9)
    t = R.choice(["ec", "cr", "cr", "gen", "punto"])
    D, Ee, Ff = -2 * a, -2 * b, a * a + b * b - r * r
    eq = "%s + %s = %d" % (sq("x", a), sq("y", b), r * r)
    if t == "ec":
        return M("¿Cuál es la ecuación de la circunferencia de centro C%s y radio %d?" % (V(a, b), r), eq, W(["%s + %s = %d" % (sq("x", -a), sq("y", -b), r * r), "%s + %s = %d" % (sq("x", a), sq("y", b), r), "%s + %s = %d" % (sq("x", b), sq("y", a), r * r) if a != b else "%s + %s = %d" % (sq("x", a), sq("y", b), 2 * r)]),
                 "(x − a)² + (y − b)² = r²: <b>%s</b>." % eq)
    if t == "cr":
        return M("Halla el centro y el radio de %s." % eq, "C%s, r = %d" % (V(a, b), r), W(["C%s, r = %d" % (V(-a, -b), r), "C%s, r = %d" % (V(a, b), r * r), "C%s, r = %d" % (V(-a, -b), r * r)]), "Leemos la ecuación: <b>C%s, r = %d</b>." % (V(a, b), r))
    if t == "gen":
        g = "x² + y² %s = 0" % E((D, "x"), (Ee, "y"), (Ff, "")) if (D or Ee or Ff) else "x² + y² = 0"
        g = g.replace("y² ", "y² + ", 1) if not E((D, "x"), (Ee, "y"), (Ff, "")).startswith(MINUS) else g.replace("y² " + MINUS, "y² − ", 1)
        return M("Halla el centro y el radio de %s." % g, "C%s, r = %d" % (V(a, b), r), W(["C%s, r = %d" % (V(-a, -b), r), "C%s, r = %d" % (V(D, Ee), r), "C%s, r = %s" % (V(a, b), raiz(abs(Ff)) if Ff else "1")]),
                 "C = (−D/2, −E/2) = %s y r = √(a² + b² − F) = <b>%d</b>." % (V(a, b), r))
    x, y = R.randint(-9, 9), R.randint(-9, 9)
    dd = (x - a) ** 2 + (y - b) ** 2
    ok = "interior" if dd < r * r else "exterior" if dd > r * r else "en la circunferencia"
    return M("¿Dónde está el punto P%s respecto de la circunferencia %s?" % (V(x, y), eq), ok, [o for o in ["interior", "exterior", "en la circunferencia", "en el centro"] if o != ok], "Distancia² al centro: %d; r² = %d → <b>%s</b>." % (dd, r * r, ok))


def s_lugares():
    t = R.choice(["tipo", "tipo", "circ_por", "tangente"])
    if t == "tipo":
        q, a, w = R.choice([("puntos que equidistan de dos puntos A y B", "la mediatriz de AB", ["la bisectriz", "una circunferencia", "una parábola"]),
                            ("puntos que equidistan de dos rectas que se cortan", "las bisectrices del ángulo", ["la mediatriz", "una elipse", "una hipérbola"]),
                            ("puntos a una distancia fija de un punto", "una circunferencia", ["una elipse", "una recta", "una parábola"]),
                            ("puntos cuya suma de distancias a dos puntos fijos es constante", "una elipse", ["una hipérbola", "una circunferencia", "una parábola"]),
                            ("puntos cuya diferencia de distancias (en valor absoluto) a dos puntos fijos es constante", "una hipérbola", ["una elipse", "una parábola", "la mediatriz"]),
                            ("puntos que equidistan de un punto fijo y de una recta", "una parábola", ["una hipérbola", "una circunferencia", "la bisectriz"])])
        return M("¿Qué lugar geométrico forman los %s?" % q, a, w, "Por definición: <b>%s</b>." % a)
    if t == "circ_por":
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        p, q, r = R.choice(TR[:3])
        x, y = a + p * R.choice([1, -1]), b + q * R.choice([1, -1])
        return M("Halla la circunferencia de centro C%s que pasa por P%s." % (V(a, b), V(x, y)), "%s + %s = %d" % (sq("x", a), sq("y", b), r * r), W(["%s + %s = %d" % (sq("x", a), sq("y", b), r), "%s + %s = %d" % (sq("x", -a), sq("y", -b), r * r), "%s + %s = %d" % (sq("x", x), sq("y", y), r * r)]),
                 "r = d(C, P) = √(%d + %d) = %d: <b>%s + %s = %d</b>." % (p * p, q * q, r, sq("x", a), sq("y", b), r * r))
    A, B = R.choice([(3, 4), (4, 3), (5, 12), (6, 8), (12, 5)])
    a, b = R.randint(-4, 4), R.randint(-4, 4)
    rr = R.randint(1, 4)
    C = -(A * a + B * b) + rr * int(math.isqrt(A * A + B * B)) * R.choice([1, -1])
    nrm = int(math.isqrt(A * A + B * B))
    dd = F(abs(A * a + B * b + C), nrm)
    r0 = R.choice([rr, rr + 1, rr - 1 if rr > 1 else rr + 2])
    ok = "tangente" if dd == r0 else "secante" if dd < r0 else "exterior"
    return M("¿Cuál es la posición de la recta %s = 0 respecto de la circunferencia de centro C%s y radio %d?" % (E((A, "x"), (B, "y"), (C, "")), V(a, b), r0), ok, [o for o in ["tangente", "secante", "exterior", "pasa por el centro"] if o != ok],
             "d(C, recta) = %s y r = %d → <b>%s</b>." % (nf(dd), r0, ok))


def s_elipse():
    b, c, a = R.choice(TR)
    if R.random() < 0.3:
        b, c = c, b
    t = R.choice(["ec", "focos", "exc", "c", "ejes"])
    eq = "x²/%d + y²/%d = 1" % (a * a, b * b)
    if t == "ec":
        return M("¿Cuál es la ecuación reducida de la elipse de semiejes a = %d (horizontal) y b = %d?" % (a, b), eq, W(["x²/%d + y²/%d = 1" % (a, b), "x²/%d − y²/%d = 1" % (a * a, b * b), "x²/%d + y²/%d = 1" % (b * b, a * a)]), "x²/a² + y²/b² = 1: <b>%s</b>." % eq)
    if t == "focos":
        return M("¿Dónde están los focos de la elipse %s?" % eq, "F(±%d, 0)" % c, W(["F(±%d, 0)" % a, "F(0, ±%d)" % c, "F(±%d, 0)" % (a * a - b * b), "F(±%d, 0)" % int(math.sqrt(a * a + b * b)) if math.isqrt(a * a + b * b) ** 2 == a * a + b * b else "F(±%d, 0)" % (a + b)]), "c² = a² − b² = %d − %d = %d → c = %d: <b>F(±%d, 0)</b>." % (a * a, b * b, c * c, c, c))
    if t == "exc":
        e = F(c, a)
        return M("¿Cuál es la excentricidad de la elipse %s?" % eq, fq(e), W([fq(F(a, c)), fq(F(b, a)), fq(F(c, b))]), "e = c/a = %d/%d = <b>%s</b> (siempre menor que 1)." % (c, a, fq(e)))
    if t == "c":
        return M("Una elipse tiene semieje mayor %d y distancia focal 2c = %d. ¿Cuánto mide el semieje menor?" % (a, 2 * c), str(b), W([str(a - c), str(int(math.sqrt(a * a + c * c))) if math.isqrt(a * a + c * c) ** 2 == a * a + c * c else str(a + c), str(2 * b), str(c)]), "b² = a² − c² = %d − %d = %d → <b>b = %d</b>." % (a * a, c * c, b * b, b))
    return M("¿Cuánto miden los ejes (mayor y menor) de la elipse %s?" % eq, "%d y %d" % (2 * a, 2 * b), W(["%d y %d" % (a, b), "%d y %d" % (a * a, b * b), "%d y %d" % (2 * a, 2 * c)]), "Semiejes a = %d y b = %d; los ejes miden el doble: <b>%d y %d</b>." % (a, b, 2 * a, 2 * b))


def s_hiperbola():
    a, b, c = R.choice(TR)
    if R.random() < 0.5:
        a, b = b, a
    t = R.choice(["focos", "asint", "exc", "ec"])
    eq = "x²/%d − y²/%d = 1" % (a * a, b * b)
    if t == "focos":
        return M("¿Dónde están los focos de la hipérbola %s?" % eq, "F(±%d, 0)" % c, W(["F(±%d, 0)" % a, "F(0, ±%d)" % c, "F(±%s, 0)" % raiz(abs(a * a - b * b)) if a != b else "F(±%d, 0)" % (a + b), "F(±%d, 0)" % (a + b)]), "c² = a² + b² = %d → c = %d: <b>F(±%d, 0)</b>." % (c * c, c, c))
    if t == "asint":
        m = F(b, a)
        return M("¿Cuáles son las asíntotas de la hipérbola %s?" % eq, "y = ±%sx" % fq(m) if m.denominator > 1 else "y = ±%dx" % m, W(["y = ±%sx" % fq(1 / m) if (1 / m).denominator > 1 else "y = ±%dx" % (1 / m), "y = ±%sx" % fq(F(b * b, a * a)), "x = ±%d" % a]), "y = ±(b/a)x = <b>±%sx</b>." % (fq(m) if m.denominator > 1 else str(m)))
    if t == "exc":
        e = F(c, a)
        return M("¿Cuál es la excentricidad de la hipérbola %s?" % eq, fq(e), W([fq(F(a, c)), fq(F(b, a)) if F(b, a) != e else fq(F(a, b)), fq(F(c, b))]), "e = c/a = %d/%d = <b>%s</b> (siempre mayor que 1)." % (c, a, fq(e)))
    return M("¿Cuál es la ecuación de la hipérbola con focos F(±%d, 0) y vértices A(±%d, 0)?" % (c, a), eq, W(["x²/%d + y²/%d = 1" % (a * a, b * b), "x²/%d − y²/%d = 1" % (c * c, a * a), "x²/%d − y²/%d = 1" % (a, b)]), "b² = c² − a² = %d: <b>%s</b>." % (b * b, eq))


def s_parabola():
    p = R.choice([1, 2, 3, 4, 5, 6, 8])
    t = R.choice(["foco", "foco", "dir", "ec", "vert"])
    s = R.choice([1, -1])
    if t == "foco":
        if R.random() < 0.5:
            return M("¿Cuál es el foco de la parábola y² = %s%dx?" % ("" if s > 0 else MINUS, 4 * p), "F%s" % V(s * p, 0), W(["F%s" % V(s * 4 * p, 0), "F%s" % V(0, s * p), "F%s" % V(s * 2 * p, 0), "F%s" % V(-s * p, 0)]), "y² = 4px con p = %s: <b>F%s</b>." % (sg(s * p), V(s * p, 0)))
        return M("¿Cuál es el foco de la parábola x² = %s%dy?" % ("" if s > 0 else MINUS, 4 * p), "F%s" % V(0, s * p), W(["F%s" % V(0, s * 4 * p), "F%s" % V(s * p, 0), "F%s" % V(0, s * 2 * p), "F%s" % V(0, -s * p)]), "x² = 4py con p = %s: <b>F%s</b>." % (sg(s * p), V(0, s * p)))
    if t == "dir":
        return M("¿Cuál es la directriz de la parábola y² = %s%dx?" % ("" if s > 0 else MINUS, 4 * p), "x = %s" % sg(-s * p), W(["x = %s" % sg(s * p), "y = %s" % sg(-s * p), "x = %s" % sg(-s * 4 * p)]), "La directriz es x = −p: <b>x = %s</b>." % sg(-s * p))
    if t == "ec":
        return M("¿Cuál es la ecuación de la parábola con foco F%s y directriz x = %s?" % (V(s * p, 0), sg(-s * p)), "y² = %s%dx" % ("" if s > 0 else MINUS, 4 * p), W(["y² = %s%dx" % ("" if s > 0 else MINUS, 2 * p), "x² = %s%dy" % ("" if s > 0 else MINUS, 4 * p), "y² = %s%dx" % ("" if s < 0 else MINUS, 4 * p), "y² = %s%dx" % ("" if s > 0 else MINUS, p)]),
                 "y² = 4px con p = %s: <b>y² = %s%dx</b>." % (sg(s * p), "" if s > 0 else MINUS, 4 * p))
    h, k = R.randint(-5, 5), R.randint(-5, 5)
    return M("¿Cuál es el vértice de la parábola (y %s %d)² = %d(x %s %d)?" % ("−" if k >= 0 else "+", abs(k), 4 * p, "−" if h >= 0 else "+", abs(h)), "V%s" % V(h, k), W(["V%s" % V(-h, -k), "V%s" % V(k, h) if h != k else "V%s" % V(h, -k), "V%s" % V(h + p, k)]), "Forma (y − k)² = 4p(x − h): <b>V%s</b>." % V(h, k))


def s_reconocer():
    t = R.choice(["tipo", "tipo", "tipo", "gen"])
    if t == "tipo":
        a, b = R.sample([4, 9, 16, 25, 36, 49], 2)
        k = R.choice(["circ", "elip", "hip", "par"])
        eq = {"circ": "x² + y² = %d" % a, "elip": "x²/%d + y²/%d = 1" % (a, b), "hip": "x²/%d − y²/%d = 1" % (a, b), "par": "y² = %dx" % a}[k]
        ok = {"circ": "una circunferencia", "elip": "una elipse", "hip": "una hipérbola", "par": "una parábola"}[k]
        return M("¿Qué cónica es %s?" % eq, ok, [o for o in ["una circunferencia", "una elipse", "una hipérbola", "una parábola"] if o != ok], "Por la forma de la ecuación: <b>%s</b>." % ok)
    q, a, w = R.choice([("¿Qué cónica tiene excentricidad 0?", "la circunferencia", ["la parábola", "la hipérbola", "la elipse"]), ("¿Qué cónica tiene excentricidad 1?", "la parábola", ["la circunferencia", "la elipse", "la hipérbola"]),
                        ("¿Qué cónica tiene asíntotas?", "la hipérbola", ["la elipse", "la parábola", "la circunferencia"]), ("Al cortar un cono con un plano paralelo a la generatriz se obtiene…", "una parábola", ["una elipse", "una circunferencia", "una hipérbola"]),
                        ("Al cortar un cono con un plano perpendicular al eje se obtiene…", "una circunferencia", ["una parábola", "una hipérbola", "una elipse"]), ("¿Qué trayectoria sigue la Tierra alrededor del Sol?", "una elipse", ["una circunferencia exacta", "una parábola", "una hipérbola"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Lugares geométricos", mix(R, seen, [(s_lugares, 20)])), ("La circunferencia", mix(R, seen, [(s_circ, 20)])), ("La elipse", mix(R, seen, [(s_elipse, 20)])),
        ("La hipérbola y la parábola", mix(R, seen, [(s_hiperbola, 10), (s_parabola, 10)])), ("Reconocer cónicas", mix(R, seen, [(s_reconocer, 8), (s_parabola, 6), (s_hiperbola, 6)]))]
think = ["Un <b>lugar geométrico</b> es el conjunto de puntos que cumplen una propiedad: la mediatriz, la bisectriz o la circunferencia.",
         "<b>Circunferencia</b>: (x − a)² + (y − b)² = r². Si viene desarrollada, se completan cuadrados.",
         "<b>Elipse</b>: x²/a² + y²/b² = 1, con c² = a² − b² y e = c/a &lt; 1. <b>Hipérbola</b>: x²/a² − y²/b² = 1, con c² = a² + b², e &gt; 1 y asíntotas y = ±(b/a)x.",
         "<b>Parábola</b>: y² = 4px, con foco F(p, 0) y directriz x = −p."]
ex = [("x² + y² − 4x + 6y − 12 = 0", ["(x − 2)² + (y + 3)² = 25"], "C(2, −3), r = 5"), ("x²/25 + y²/9 = 1", ["c² = 25 − 9 = 16"], "F(±4, 0), e = 4/5")]
mist = [["c² = a² + b² en la elipse", "En la elipse c² = a² − b²."], ["Signo del centro", "(x + 2)² → a = −2."], ["Confundir a y b", "a va con el eje mayor."]]
body = L(think, ex, mist)
faq = [("¿Por qué se llaman cónicas?", "Porque se obtienen al cortar un cono con un plano: según la inclinación sale una circunferencia, una elipse, una parábola o una hipérbola."),
       ("¿Dónde aparecen las cónicas?", "En las órbitas de los planetas (elipses), en las antenas parabólicas y los faros (parábolas) y en la navegación (hipérbolas).")]
unit(1, R, "lugares-geometricos-y-conicas", "E", "Lugares geométricos del plano; cónicas: circunferencia, elipse, hipérbola y parábola, elementos y ecuaciones reducidas",
     "Lugares geométricos y cónicas", "Cónicas", "Fichas de Matemáticas I (1.º de Bachillerato): mediatriz, circunferencia, elipse, hipérbola y parábola: elementos, focos, excentricidad y ecuaciones. 100 ejercicios.",
     "Elipse: c² = a² − b²", "Hipérbola: c² = a² + b². Parábola: y² = 4px.", body, faq, sets, 9)
