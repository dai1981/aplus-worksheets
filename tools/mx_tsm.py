# -*- coding: utf-8 -*-
"""
México, bachillerato: Temas Selectos de Matemáticas I y II (DGB, SEP 2024). Problemas propios.
setup(R) antes de usar. t* = Temas Selectos I (geometría, cónicas, fractales); u* = Temas Selectos II (sistemas dinámicos, sucesiones, integral, métodos numéricos).
"""
import math
from fractions import Fraction as F
import mx_pm3 as P3
from mx_pm3 import ev, der, nz, poly, pt  # noqa: F401
from mx_pm1 import opt, from_bank, d2, show, pick, name  # noqa: F401
from mx_s1 import fq, dexact, tabla_html, MINUS, sg  # noqa: F401
from mx_common import num, dec, NB  # noqa: F401

R = None


def setup(rnd):
    global R
    P3.setup(rnd)
    R = P3.R


def sq(v, n):
    """(x − h)² con el signo correcto"""
    if n == 0:
        return v + "²"
    return "(%s %s %s)²" % (v, "−" if n > 0 else "+", num(abs(n)))


# ============================================================ TSM I-1: geometría básica y razones trigonométricas
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (9, 40, 41), (12, 16, 20), (15, 20, 25)]


def t1(*ks):
    t = pick(ks, ["razon", "lado", "angulo", "autosim"])
    a, b, c = R.choice(TRIPLES)
    if R.random() < .5:
        a, b = b, a
    if t == "razon":
        fn = R.choice(["sen", "cos", "tan"])
        v = {"sen": F(a, c), "cos": F(b, c), "tan": F(a, b)}[fn]
        return opt("En un triángulo rectángulo, el cateto opuesto al ángulo α mide %d, el adyacente %d y la hipotenusa %d. ¿Cuánto vale %s α?" % (a, b, c, fn), fq(v),
                   [fq(F(b, c)) if fn != "cos" else fq(F(a, c)), fq(F(b, a)), fq(F(c, a)) if fn != "sen" else fq(F(c, b))],
                   "%s α = %s = <b>%s</b>." % (fn, {"sen": "opuesto ÷ hipotenusa", "cos": "adyacente ÷ hipotenusa", "tan": "opuesto ÷ adyacente"}[fn], fq(v)))
    if t == "lado":
        ang = R.choice([20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
        h = R.choice([10, 12, 15, 20, 25, 30, 40])
        fn = R.choice(["op", "ady"])
        v = h * (math.sin if fn == "op" else math.cos)(math.radians(ang))
        return opt("La hipotenusa de un triángulo rectángulo mide %d cm y un ángulo agudo %d°. ¿Cuánto mide el cateto %s a ese ángulo? (a los décimos)" % (h, ang, "opuesto" if fn == "op" else "adyacente"),
                   d2(v, 1) + " cm", [d2(h * (math.cos if fn == "op" else math.sin)(math.radians(ang)), 1) + " cm", d2(h * math.tan(math.radians(ang)), 1) + " cm", d2(h / math.sin(math.radians(ang)), 1) + " cm"],
                   "%s = %d × %s %d° ≈ <b>%s cm</b>." % ("opuesto" if fn == "op" else "adyacente", h, "sen" if fn == "op" else "cos", ang, d2(v, 1)))
    if t == "angulo":
        v = math.degrees(math.atan2(a, b))
        return opt("Los catetos de un triángulo rectángulo miden %d y %d. ¿Cuánto mide el ángulo opuesto al cateto de %d? (a los décimos de grado)" % (a, b, a), d2(v, 1) + "°",
                   [d2(90 - v, 1) + "°", d2(math.degrees(math.atan2(b, a)) / 2, 1) + "°", d2(v + 10, 1) + "°"],
                   "tan α = %d/%d → α = tan⁻¹(%s) ≈ <b>%s°</b>." % (a, b, d2(a / b, 3), d2(v, 1)))
    k = R.choice([2, 3, 4])
    n = R.randint(1, 3)
    return opt("Dos triángulos semejantes tienen razón de semejanza %d. Si el área del pequeño es %d cm², ¿cuál es el área del grande?" % (k, n * 6), "%d cm²" % (n * 6 * k * k),
               ["%d cm²" % (n * 6 * k), "%d cm²" % (n * 6 * k * k * k), "%d cm²" % (n * 6 + k)], "Las áreas se multiplican por el cuadrado de la razón: %d × %d² = <b>%d cm²</b>." % (n * 6, k, n * 6 * k * k))


# ============================================================ TSM I-3: geometría euclidiana y no euclidiana
def t3(*ks):
    t = pick(ks, ["esfera", "exceso", "postulado", "suma", "paralelas"])
    if t == "exceso":
        A, B = R.randint(60, 120), R.randint(60, 120)
        C = R.randint(max(1, 200 - A - B), 150)
        e = A + B + C - 180
        if e <= 0:
            return None
        return opt("Un triángulo dibujado sobre una esfera tiene ángulos de %d°, %d° y %d°. ¿Cuánto vale su exceso esférico (suma − 180°)?" % (A, B, C), "%d°" % e,
                   ["%d°" % (A + B + C), "0°", "%d°" % (360 - A - B - C) if 360 - A - B - C > 0 else "%d°" % (e + 90)],
                   "Suma = %d°; exceso = %d° − 180° = <b>%d°</b>. En la esfera, los ángulos de un triángulo suman más de 180°." % (A + B + C, A + B + C, e))
    if t == "suma":
        n = R.randint(3, 12)
        return opt("En geometría euclidiana, ¿cuánto suman los ángulos interiores de un polígono de %d lados?" % n, "%s°" % num(180 * (n - 2)),
                   ["%s°" % num(180 * n), "%s°" % num(360), "%s°" % num(180 * (n - 1))], "S = 180° × (n − 2) = 180° × %d = <b>%s°</b>." % (n - 2, num(180 * (n - 2))))
    if t == "paralelas":
        a = R.randint(25, 155)
        q = R.choice(["alternos internos", "correspondientes", "conjugados internos"])
        v = 180 - a if q == "conjugados internos" else a
        return opt("Dos rectas paralelas son cortadas por una transversal. Si un ángulo mide %d°, ¿cuánto mide su ángulo %s? (Esto depende del quinto postulado de Euclides.)" % (a, {"alternos internos": "alterno interno", "correspondientes": "correspondiente", "conjugados internos": "conjugado interno"}[q]),
                   "%d°" % v, ["%d°" % (180 - v), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "%d°" % (360 - a)],
                   "Los ángulos %s son %s: <b>%d°</b>." % (q, "suplementarios (suman 180°)" if q == "conjugados internos" else "iguales", v))
    items = [("El quinto postulado de Euclides dice, en una de sus formas, que…", "por un punto exterior a una recta pasa una sola paralela", ["todos los ángulos rectos son iguales", "por dos puntos pasa una recta", "un círculo tiene centro y radio"], "Es el postulado de las paralelas (forma de Playfair)."),
             ("En la geometría sobre una esfera, las «rectas» son…", "círculos máximos (como el ecuador)", ["paralelos de latitud", "líneas rectas que atraviesan la esfera", "espirales"], "Son el camino más corto entre dos puntos de la esfera."),
             ("En la geometría esférica, ¿cuántas paralelas a una recta pasan por un punto exterior?", "ninguna", ["una", "infinitas", "dos"], "Todos los círculos máximos se cortan."),
             ("En la geometría hiperbólica, los ángulos de un triángulo suman…", "menos de 180°", ["exactamente 180°", "más de 180°", "360°"], "Por un punto pasan infinitas paralelas y los triángulos son «delgados»."),
             ("Sobre la Tierra, un triángulo con un vértice en el polo norte y dos en el ecuador puede tener…", "tres ángulos rectos", ["ángulos que suman 180°", "un solo ángulo", "lados rectos en el plano"], "Es un triángulo esférico con suma 270°."),
             ("¿Por qué los aviones siguen rutas curvas en un mapa plano?", "porque el camino más corto sobre la esfera es un arco de círculo máximo", ["para evitar el viento", "porque el mapa está mal", "porque así gastan más combustible"], "En el mapa plano el círculo máximo se ve curvo."),
             ("¿Qué matemáticos desarrollaron las geometrías no euclidianas en el siglo XIX?", "Lobachevski, Bolyai y Riemann", ["Newton y Leibniz", "Pitágoras y Tales", "Pascal y Fermat"], "Cambiaron el quinto postulado y obtuvieron geometrías coherentes."),
             ("Un axioma o postulado es…", "una afirmación que se acepta sin demostrar", ["un teorema demostrado", "una figura geométrica", "un error de cálculo"], "A partir de los postulados se demuestran los teoremas.")]
    if t == "postulado":
        return from_bank(items)
    R_ = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 6371])
    E = R.choice([30, 45, 60, 90, 120, 180])
    Er = {30: "π/6", 45: "π/4", 60: "π/3", 90: "π/2", 120: "2π/3", 180: "π"}[E]
    if R_ == 6371:
        return from_bank(items)
    k = F(E, 180)
    return opt("El área de un triángulo esférico es (exceso en radianes) × r². Si el exceso es %d° y r = %d, ¿cuál es el área?" % (E, R_), ("%sπ" % (fq(k * R_ * R_)) if k * R_ * R_ != 1 else "π") + " u²",
               [("%sπ" % fq(k * R_)) + " u²" if k * R_ != 1 else "π u²", "%d u²" % (E * R_ * R_), ("%sπ" % fq(k * R_ * R_ * 2)) + " u²"],
               "%d° = %s rad. Área = %s × %d² = <b>%sπ u²</b>." % (E, Er, Er, R_, fq(k * R_ * R_) if k * R_ * R_ != 1 else ""))


# ============================================================ TSM I-4: Cramer 2 × 2
def t4(*ks):
    t = pick(ks, ["det", "cramer", "x"])
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, b, c, d = [nz(-6, 6) for _ in range(4)]
    D = a * d - b * c
    if D == 0:
        return None
    e, f = a * x + b * y, c * x + d * y
    sys_ = "<span class='sys'>%s = %s<br>%s = %s</span>" % (poly([a, 0]).replace("x", "x") + (" + " if b > 0 else " − ") + (num(abs(b)) if abs(b) != 1 else "") + "y", sg(e),
                                                       poly([c, 0]) + (" + " if d > 0 else " − ") + (num(abs(d)) if abs(d) != 1 else "") + "y", sg(f))
    if t == "det":
        return opt("Para resolver por Cramer el sistema %s, ¿cuánto vale el determinante del sistema Δ = ad − bc?" % sys_, sg(D), [sg(a * d + b * c), sg(b * c - a * d), sg(a * b - c * d)],
                   "Δ = (%s)(%s) − (%s)(%s) = <b>%s</b>. Como Δ ≠ 0, hay una solución." % (sg(a), sg(d), sg(b), sg(c), sg(D)))
    Dx, Dy = e * d - b * f, a * f - e * c
    if t == "x":
        return opt("Resuelve por Cramer el sistema %s. ¿Cuánto vale Δ<sub>x</sub> (se cambia la columna de x por los términos independientes)?" % sys_, sg(Dx), [sg(Dy), sg(D), sg(-Dx) if Dx else "1"],
                   "Δ<sub>x</sub> = (%s)(%s) − (%s)(%s) = <b>%s</b>; x = Δ<sub>x</sub>/Δ = %s." % (sg(e), sg(d), sg(b), sg(f), sg(Dx), sg(x)))
    return opt("Resuelve por la regla de Cramer: %s" % sys_, "x = %s, y = %s" % (sg(x), sg(y)), ["x = %s, y = %s" % (sg(y), sg(x)), "x = %s, y = %s" % (sg(-x), sg(y)), "x = %s, y = %s" % (sg(x), sg(-y))],
               "Δ = %s, Δ<sub>x</sub> = %s, Δ<sub>y</sub> = %s. x = %s, y = %s." % (sg(D), sg(Dx), sg(Dy), sg(x), sg(y)))


# ============================================================ TSM I-5: parábola
def t5(*ks):
    t = pick(ks, ["vertice", "foco", "directriz", "lado", "abre", "modelo"])
    h, k = R.randint(-6, 6), R.randint(-6, 6)
    p = nz(-4, 4)
    vert = R.random() < .6   # (x − h)² = 4p(y − k): abre arriba/abajo
    eq = ("%s = %s%s" % (sq("x", h), sg(4 * p), "(y %s %s)" % ("−" if k > 0 else "+", num(abs(k))) if k else "y")) if vert else \
         ("%s = %s%s" % (sq("y", k), sg(4 * p), "(x %s %s)" % ("−" if h > 0 else "+", num(abs(h))) if h else "x"))
    foco = pt(h, k + p) if vert else pt(h + p, k)
    if t == "vertice":
        return opt("¿Cuál es el vértice de la parábola %s?" % eq, pt(h, k), [pt(-h, -k), pt(k, h), foco], "En la forma (x − h)² = 4p(y − k) el vértice es (h, k): <b>%s</b>." % pt(h, k))
    if t == "foco":
        return opt("¿Cuál es el foco de la parábola %s?" % eq, foco, [pt(h, k - p) if vert else pt(h - p, k), pt(h, k), pt(h + 4 * p, k) if vert else pt(h, k + 4 * p)],
                   "4p = %s → p = %s. El foco está a p del vértice %s: <b>%s</b>." % (sg(4 * p), sg(p), pt(h, k), foco))
    if t == "directriz":
        ok = ("y = %s" % sg(k - p)) if vert else ("x = %s" % sg(h - p))
        return opt("¿Cuál es la directriz de la parábola %s?" % eq, ok, [("y = %s" % sg(k + p)) if vert else ("x = %s" % sg(h + p)), ("x = %s" % sg(h - p)) if vert else ("y = %s" % sg(k - p)), ("y = %s" % sg(k)) if vert else ("x = %s" % sg(h))],
                   "p = %s; la directriz está a p del vértice, del lado contrario al foco: <b>%s</b>." % (sg(p), ok))
    if t == "lado":
        return opt("¿Cuánto mide el lado recto de la parábola %s?" % eq, num(abs(4 * p)), [num(abs(p)), num(abs(2 * p)), num(abs(8 * p))], "Lado recto = |4p| = <b>%d</b>." % abs(4 * p))
    if t == "abre":
        ok = ("hacia arriba" if p > 0 else "hacia abajo") if vert else ("hacia la derecha" if p > 0 else "hacia la izquierda")
        return opt("¿Hacia dónde abre la parábola %s?" % eq, ok, [x for x in ["hacia arriba", "hacia abajo", "hacia la derecha", "hacia la izquierda"] if x != ok],
                   "%s y 4p = %s: abre <b>%s</b>." % ("La x está al cuadrado" if vert else "La y está al cuadrado", sg(4 * p), ok))
    w = R.choice([4, 6, 8, 10, 12, 20])
    d_ = R.choice([1, 2, 3, 4, 5])
    pp = F(w * w, 16 * d_)
    return opt("Una antena parabólica mide %d dm de ancho y %d dm de profundidad. Si su vértice está en el origen y abre hacia arriba, ¿a qué altura está el foco (donde se pone el receptor)?" % (w, d_), show(pp) + " dm",
               [show(pp * 2) + " dm", show(F(w, 4)) + " dm", show(F(d_, 2)) + " dm"],
               "x² = 4py pasa por (%s, %d): %s = 4p × %d → p = <b>%s dm</b>." % (show(F(w, 2)), d_, show(F(w * w, 4)), d_, show(pp)))


# ============================================================ TSM I-6: circunferencia
def t6(*ks):
    t = pick(ks, ["ecuacion", "centro", "general", "punto", "diametro"])
    h, k = R.randint(-7, 7), R.randint(-7, 7)
    r = R.randint(1, 9)
    can = "%s + %s = %d" % (sq("x", h), sq("y", k), r * r)
    if t == "ecuacion":
        return opt("¿Cuál es la ecuación de la circunferencia con centro %s y radio %d?" % (pt(h, k), r), can,
                   ["%s + %s = %d" % (sq("x", -h), sq("y", -k), r * r), "%s + %s = %d" % (sq("x", h), sq("y", k), r), "%s + %s = %d" % (sq("x", k), sq("y", h), r * r)],
                   "(x − h)² + (y − k)² = r² → <b>%s</b>." % can)
    if t == "centro":
        return opt("¿Cuál es el centro y el radio de %s?" % can, "centro %s, radio %d" % (pt(h, k), r),
                   ["centro %s, radio %d" % (pt(-h, -k), r), "centro %s, radio %d" % (pt(h, k), r * r), "centro %s, radio %d" % (pt(k, h), r)], "Se lee directamente: centro (h, k) y r = √%d = <b>%d</b>." % (r * r, r))
    if t == "general":
        D, E, Fc = -2 * h, -2 * k, h * h + k * k - r * r
        gen = "x² + y² %s %s = 0" % (("%s %s" % (("+ " + num(D) + "x") if D > 0 else ("− " + num(-D) + "x") if D else "", ("+ " + num(E) + "y") if E > 0 else ("− " + num(-E) + "y") if E else "")).strip(),
                                    ("+ " + num(Fc)) if Fc > 0 else ("− " + num(-Fc)) if Fc else "")
        gen = gen.replace("  ", " ")
        return opt("¿Cuál es el centro y el radio de la circunferencia %s?" % gen, "centro %s, radio %d" % (pt(h, k), r),
                   ["centro %s, radio %d" % (pt(-h, -k), r), "centro %s, radio %d" % (pt(D, E), r), "centro %s, radio %d" % (pt(h, k), r * r)],
                   "Completando cuadrados: %s → <b>centro %s, radio %d</b>." % (can, pt(h, k), r))
    if t == "punto":
        a = R.choice([(3, 4), (4, 3), (0, 5), (5, 0), (6, 8), (8, 6), (5, 12), (12, 5)])
        rr = int(math.hypot(*a))
        sx, sy = R.choice([1, -1]), R.choice([1, -1])
        P = (h + sx * a[0], k + sy * a[1])
        Q = (P[0] + 1, P[1]) if R.random() < .5 else P
        dentro = (Q[0] - h) ** 2 + (Q[1] - k) ** 2
        ok = "sobre la circunferencia" if dentro == rr * rr else "fuera" if dentro > rr * rr else "dentro"
        return opt("¿Dónde está el punto %s respecto a la circunferencia %s + %s = %d?" % (pt(*Q), sq("x", h), sq("y", k), rr * rr), ok, [x for x in ["sobre la circunferencia", "fuera", "dentro", "en el centro"] if x != ok],
                   "Sustituimos: (%s)² + (%s)² = %d %s %d → <b>%s</b>." % (sg(Q[0] - h), sg(Q[1] - k), dentro, "=" if dentro == rr * rr else "&gt;" if dentro > rr * rr else "&lt;", rr * rr, ok))
    x1, y1 = h - R.randint(1, 6), k - R.randint(-5, 5)
    x2, y2 = 2 * h - x1, 2 * k - y1
    r2 = (x2 - h) ** 2 + (y2 - k) ** 2
    return opt("Los extremos de un diámetro son %s y %s. ¿Cuál es la ecuación de la circunferencia?" % (pt(x1, y1), pt(x2, y2)), "%s + %s = %d" % (sq("x", h), sq("y", k), r2),
               ["%s + %s = %d" % (sq("x", h), sq("y", k), 4 * r2), "%s + %s = %d" % (sq("x", -h), sq("y", -k), r2), "%s + %s = %d" % (sq("x", x1), sq("y", y1), r2)],
               "Centro = punto medio %s; r² = %d. Ecuación: <b>%s + %s = %d</b>." % (pt(h, k), r2, sq("x", h), sq("y", k), r2))


# ============================================================ TSM I-7: elipse
def t7(*ks):
    t = pick(ks, ["ejes", "focos", "c", "exc", "orbita"])
    a, b, c = R.choice([(5, 4, 3), (5, 3, 4), (10, 8, 6), (10, 6, 8), (13, 12, 5), (13, 5, 12), (17, 15, 8), (25, 24, 7), (15, 12, 9), (15, 9, 12)])
    h, k = R.randint(-5, 5), R.randint(-5, 5)
    horiz = R.random() < .5
    X, Y = sq("x", h), sq("y", k)
    eq = "%s/%d + %s/%d = 1" % (X, a * a if horiz else b * b, Y, b * b if horiz else a * a)
    if t == "ejes":
        return opt("En la elipse %s, ¿cuánto miden el eje mayor y el eje menor?" % eq, "%d y %d" % (2 * a, 2 * b), ["%d y %d" % (a, b), "%d y %d" % (a * a, b * b), "%d y %d" % (2 * a, 2 * c)],
                   "a² = %d → a = %d; b² = %d → b = %d. Eje mayor 2a = <b>%d</b>, eje menor 2b = <b>%d</b>." % (a * a, a, b * b, b, 2 * a, 2 * b))
    if t == "focos":
        f1, f2 = ((h - c, k), (h + c, k)) if horiz else ((h, k - c), (h, k + c))
        g1, g2 = ((h, k - c), (h, k + c)) if horiz else ((h - c, k), (h + c, k))
        return opt("¿Dónde están los focos de la elipse %s?" % eq, "%s y %s" % (pt(*f1), pt(*f2)), ["%s y %s" % (pt(*g1), pt(*g2)), "%s y %s" % (pt(h - a, k), pt(h + a, k)) if horiz else "%s y %s" % (pt(h, k - a), pt(h, k + a)), "%s y %s" % (pt(h - b, k), pt(h + b, k))],
                   "c² = a² − b² = %d − %d = %d → c = %d. Los focos están sobre el eje mayor, a %d del centro %s." % (a * a, b * b, c * c, c, c, pt(h, k)))
    if t == "c":
        return opt("En una elipse, a = %d y b = %d. ¿Cuánto vale c (distancia del centro a cada foco)?" % (a, b), num(c), [num(a + b), num(a - b), num(int(round(math.sqrt(a * a + b * b))))],
                   "c = √(a² − b²) = √(%d − %d) = <b>%d</b>." % (a * a, b * b, c))
    if t == "exc":
        return opt("¿Cuál es la excentricidad de la elipse %s?" % eq, fq(F(c, a)), [fq(F(b, a)), fq(F(a, c)), fq(F(c, b))], "e = c/a = %d/%d = <b>%s</b>. Entre más cerca de 0, más redonda." % (c, a, fq(F(c, a))))
    items = [("Según la primera ley de Kepler, los planetas giran alrededor del Sol en órbitas…", "elípticas, con el Sol en uno de los focos", ["circulares, con el Sol en el centro", "parabólicas", "hiperbólicas"], "Kepler lo descubrió con los datos de Tycho Brahe."),
             ("La excentricidad de una circunferencia es…", "0", ["1", "mayor que 1", "infinita"], "Si c = 0 los focos coinciden con el centro."),
             ("La excentricidad de cualquier elipse está…", "entre 0 y 1", ["entre 1 y 2", "por encima de 1", "siempre en 1"], "e = c/a y c &lt; a."),
             ("La suma de las distancias de un punto de la elipse a los dos focos es…", "constante e igual a 2a", ["igual a 2c", "variable", "igual a 0"], "Es la definición de la elipse."),
             ("La órbita de la Tierra tiene excentricidad ≈ 0.017. Eso significa que es…", "casi circular", ["muy alargada", "una parábola", "una recta"], "Una excentricidad tan pequeña da una elipse casi redonda."),
             ("En un salón elíptico, un susurro en un foco se oye en el otro foco porque…", "el sonido se refleja hacia el otro foco", ["el salón es pequeño", "el eco viaja en línea recta", "hay altavoces"], "Es la propiedad de reflexión de la elipse.")]
    return from_bank(items)


# ============================================================ TSM I-8: ecuación general de segundo grado
def t8(*ks):
    t = pick(ks, ["tipo", "tipo", "disc"])
    kind = R.choice(["circunferencia", "elipse", "parábola", "hipérbola"])
    D, E, Fc = R.randint(-8, 8), R.randint(-8, 8), R.randint(-20, 20)
    if kind == "circunferencia":
        A = C = R.randint(1, 5)
    elif kind == "elipse":
        A, C = R.sample(range(1, 10), 2)
    elif kind == "parábola":
        A, C = (R.randint(1, 6), 0) if R.random() < .5 else (0, R.randint(1, 6))
        if A == 0 and D == 0:
            D = nz(-6, 6)
        if C == 0 and E == 0:
            E = nz(-6, 6)
    else:
        A, C = R.randint(1, 9), -R.randint(1, 9)
        if R.random() < .5:
            A, C = C, A
    def term(c, v, first=False):
        if c == 0:
            return ""
        s = (num(abs(c)) if abs(c) != 1 or v == "" else "") + v
        return ((MINUS if c < 0 else "") + s) if first else ((" − " if c < 0 else " + ") + s)
    parts = [(A, "x²"), (C, "y²"), (D, "x"), (E, "y"), (Fc, "")]
    eq, first = "", True
    for c, v in parts:
        if c:
            eq += term(c, v, first)
            first = False
    eq += " = 0"
    if t == "disc":
        B = R.choice([0, 0, 2, 4, 6])
        A, C = R.randint(1, 6) * R.choice([1, -1]), R.randint(1, 6) * R.choice([1, -1])
        disc = B * B - 4 * A * C
        k2 = "una elipse (o circunferencia)" if disc < 0 else "una parábola" if disc == 0 else "una hipérbola"
        return opt("Para Ax² + Bxy + Cy² + Dx + Ey + F = 0 con A = %s, B = %s y C = %s, ¿qué cónica es (en general), según B² − 4AC?" % (sg(A), sg(B), sg(C)), k2,
                   [x for x in ["una elipse (o circunferencia)", "una parábola", "una hipérbola", "una recta"] if x != k2],
                   "B² − 4AC = %d − %d = %d: %s → <b>%s</b>." % (B * B, 4 * A * C, disc, "negativo" if disc < 0 else "cero" if disc == 0 else "positivo", k2))
    return opt("¿Qué cónica representa %s?" % eq, kind, [x for x in ["circunferencia", "elipse", "parábola", "hipérbola"] if x != kind],
               {"circunferencia": "A = C: circunferencia.", "elipse": "A y C del mismo signo pero distintos: elipse.", "parábola": "Solo una variable está al cuadrado: parábola.", "hipérbola": "A y C de signos contrarios: hipérbola."}[kind])


# ============================================================ TSM I-9: fractales
def t9(*ks):
    t = pick(ks, ["cantor", "sierp", "koch", "dim", "mandel"])
    n = R.randint(1, 8)
    if t == "cantor":
        q = R.choice(["seg", "long"])
        if q == "seg":
            return opt("En el conjunto de Cantor se quita el tercio central de cada segmento. Empezando con 1 segmento, ¿cuántos segmentos hay después de %d pasos?" % n, num(2 ** n),
                       [num(3 ** n), num(2 * n), num(2 ** (n + 1))], "Cada segmento se convierte en 2: 2<sup>%d</sup> = <b>%s</b>." % (n, num(2 ** n)))
        L = R.choice([1, 3, 9, 27, 81])
        v = F(L) * F(2, 3) ** n
        return opt("Se construye el conjunto de Cantor sobre un segmento de longitud %d. ¿Cuánta longitud queda después de %d pasos?" % (L, n), fq(v), [fq(F(L) * F(1, 3) ** n), fq(F(L) * F(2, 3) ** (n + 1)), fq(F(L) - F(L, 3) * n) if L - F(L, 3) * n > 0 else "0"],
                   "En cada paso queda 2/3 de la longitud: %d × (2/3)<sup>%d</sup> = <b>%s</b>. Con infinitos pasos la longitud tiende a 0." % (L, n, fq(v)))
    if t == "sierp":
        q = R.choice(["tri", "area"])
        if q == "tri":
            return opt("En el triángulo de Sierpiński, cada triángulo se divide en 4 y se quita el central. ¿Cuántos triángulos negros hay después de %d pasos?" % n, num(3 ** n),
                       [num(4 ** n), num(3 * n), num(2 ** n)], "Cada triángulo deja 3: 3<sup>%d</sup> = <b>%s</b>." % (n, num(3 ** n)))
        A = R.choice([16, 32, 64, 128, 256])
        v = F(A) * F(3, 4) ** n
        return opt("Un triángulo de Sierpiński empieza con área %d cm². ¿Qué área queda después de %d pasos?" % (A, n), show(v) + " cm²", [show(F(A) * F(1, 4) ** n) + " cm²", show(F(A) * F(3, 4) ** (n + 1)) + " cm²", show(F(A, 4 * n)) + " cm²"],
                   "Cada paso deja 3/4 del área: %d × (3/4)<sup>%d</sup> = <b>%s cm²</b>." % (A, n, show(v)))
    if t == "koch":
        q = R.choice(["seg", "per"])
        if q == "seg":
            return opt("En el copo de Koch, cada segmento se reemplaza por 4 segmentos de 1/3 de su longitud. Empezando con un triángulo (3 lados), ¿cuántos segmentos hay después de %d pasos?" % n, num(3 * 4 ** n),
                       [num(4 ** n), num(3 * 3 ** n), num(3 * 4 * n)], "3 × 4<sup>%d</sup> = <b>%s</b>." % (n, num(3 * 4 ** n)))
        P = R.choice([3, 6, 9, 12, 27])
        v = F(P) * F(4, 3) ** n
        return opt("El copo de Koch empieza con un triángulo de perímetro %d. ¿Cuál es el perímetro después de %d pasos?" % (P, n), show(v), [show(F(P) * F(3, 4) ** n), show(F(P) * F(4, 3) ** (n + 1)), show(F(P) + n)],
                   "Cada paso multiplica el perímetro por 4/3: %d × (4/3)<sup>%d</sup> = <b>%s</b>. El perímetro crece sin límite, pero el área no." % (P, n, show(v)))
    if t == "dim":
        N, s, name_ = R.choice([(2, 3, "conjunto de Cantor"), (3, 2, "triángulo de Sierpiński"), (4, 3, "curva de Koch"), (8, 3, "alfombra de Sierpiński"), (4, 2, "cuadrado"), (8, 2, "cubo"), (2, 2, "segmento"), (20, 3, "esponja de Menger")])
        D = math.log(N) / math.log(s)
        return opt("El %s está formado por %d copias reducidas a 1/%d. ¿Cuál es su dimensión de autosimilitud D = log N ÷ log s? (a los centésimos)" % (name_, N, s), d2(D, 2),
                   [d2(N / s, 2), d2(math.log(s) / math.log(N), 2), d2(D + 1, 2)], "D = log %d ÷ log %d ≈ <b>%s</b>. %s" % (N, s, d2(D, 2), "Es un número no entero: por eso se llama fractal." if abs(D - round(D)) > 1e-9 else "Da un entero: no es un fractal."))
    c = R.choice([-2, -1, 0, 1, F(-1, 2), F(1, 4), F(1, 2), -3])
    z = F(0)
    seq = []
    for _ in range(4):
        z = z * z + c
        seq.append(z)
    bounded = c in (-2, -1, 0, F(-1, 2), F(1, 4))
    if R.random() < .5:
        return opt("Para el conjunto de Mandelbrot se itera z → z² + c desde z = 0. Con c = %s, ¿cuáles son los primeros tres valores?" % fq(c), ", ".join(fq(x) for x in seq[:3]),
                   [", ".join(fq(x) for x in [c, 2 * c, 3 * c]), ", ".join(fq(x) for x in [c, c * c, c * c * c]), ", ".join(fq(x + 1) for x in seq[:3])],
                   "z₁ = 0² + c = %s; z₂ = %s² + c = %s; z₃ = %s." % (fq(seq[0]), fq(seq[0]), fq(seq[1]), fq(seq[2])))
    return opt("Al iterar z → z² + c desde z = 0 con c = %s se obtiene %s, … ¿El número c pertenece al conjunto de Mandelbrot?" % (fq(c), ", ".join(fq(x) for x in seq)), "sí, porque los valores no se van al infinito" if bounded else "no, porque los valores crecen sin límite",
               ["no, porque los valores crecen sin límite" if bounded else "sí, porque los valores no se van al infinito", "solo si c es positivo", "no se puede saber nunca"],
               "c está en el conjunto de Mandelbrot si la sucesión se mantiene acotada: aquí %s." % ("se mantiene acotada" if bounded else "crece sin límite"))


# ============================================================ TSM II-1: composición y sistemas dinámicos discretos
def u1(*ks):
    t = pick(ks, ["iter", "fijo", "rec", "orbita", "logistica", "concepto"])
    if t == "iter":
        m, b = nz(-3, 3), R.randint(-5, 5)
        x0 = R.randint(-3, 4)
        n = R.choice([2, 3])
        x = x0
        for _ in range(n):
            x = m * x + b
        return opt("Si f(x) = %s, ¿cuánto vale %s con x₀ = %s?" % (poly([m, b]), "f(f(x₀))" if n == 2 else "f(f(f(x₀)))", sg(x0)), sg(x), [sg(m * x0 + b), sg(n * (m * x0 + b)), sg(x + m)],
                   "Se aplica f %d veces: %s → <b>%s</b>." % (n, " → ".join(sg(v) for v in _orb(lambda z: m * z + b, x0, n)), sg(x)))
    if t == "fijo":
        m, b = R.choice([2, 3, F(1, 2), -1, -2, F(1, 3)]), R.randint(-6, 6)
        x = F(b) / (1 - F(m))
        return opt("¿Cuál es el punto fijo de f(x) = %sx %s %d (el valor con f(x) = x)?" % (fq(m) if m != -1 else "−", "+" if b >= 0 else "−", abs(b)), fq(x), [fq(-x) if x else "1", fq(F(b) / (1 + F(m))) if m != -1 else "0", sg(b)],
                   "x = %sx %s %d → x(1 − %s) = %d → <b>x = %s</b>." % (fq(m) if m != -1 else "−", "+" if b >= 0 else "−", abs(b), fq(m), b, fq(x)))
    if t == "rec":
        r = R.choice([2, 3, F(1, 2), -1])
        b = R.randint(-5, 5)
        a0 = R.randint(-4, 6)
        seq = [F(a0)]
        for _ in range(3):
            seq.append(F(r) * seq[-1] + b)
        return opt("Una sucesión cumple a<sub>n+1</sub> = %s·a<sub>n</sub> %s %d y a₀ = %s. ¿Cuánto vale a₃?" % (fq(r), "+" if b >= 0 else "−", abs(b), sg(a0)), fq(seq[3]), [fq(seq[2]), fq(seq[3] + b), fq(F(a0) * F(r) ** 3)],
                   "a₁ = %s, a₂ = %s, a₃ = <b>%s</b>." % (fq(seq[1]), fq(seq[2]), fq(seq[3])))
    if t == "orbita":
        m = R.choice([F(1, 2), F(-1, 2), 2, F(1, 3)])
        x0 = R.choice([8, 16, 24, 48, -8])
        orb = _orb(lambda z: m * z, F(x0), 3)
        kind = "se acerca a 0" if abs(m) < 1 else "crece sin límite"
        return opt("La órbita de x₀ = %d con f(x) = %sx es %s, … ¿Qué pasa a la larga?" % (x0, fq(m), ", ".join(fq(v) for v in orb)), kind, [x for x in ["se acerca a 0", "crece sin límite", "se repite cada 2 pasos", "se queda en %d" % x0] if x != kind],
                   "|%s| %s 1, así que la órbita <b>%s</b>." % (fq(m), "&lt;" if abs(m) < 1 else "&gt;", kind))
    if t == "logistica":
        r = R.choice([2, F(5, 2), 3, F(7, 2), 4, F(3, 2)])
        x0 = R.choice([F(1, 2), F(1, 4), F(1, 5), F(1, 10), F(1, 3), F(2, 5)])
        x1 = r * x0 * (1 - x0)
        return opt("En el modelo logístico discreto x<sub>n+1</sub> = r·x<sub>n</sub>(1 − x<sub>n</sub>), con r = %s y x₀ = %s, ¿cuánto vale x₁?" % (fq(r), fq(x0)), fq(x1),
                   [fq(r * x0), fq(r * (1 - x0)), fq(x0 * (1 - x0))], "x₁ = %s × %s × %s = <b>%s</b>." % (fq(r), fq(x0), fq(1 - x0), fq(x1)))
    items = [("Un sistema dinámico discreto es…", "una regla que se aplica una y otra vez para obtener el siguiente estado", ["una ecuación sin solución", "una gráfica de barras", "un sistema de dos ecuaciones lineales"], "Por ejemplo x<sub>n+1</sub> = f(x<sub>n</sub>)."),
             ("La «sensibilidad a las condiciones iniciales» significa que…", "dos inicios casi iguales pueden terminar muy distintos", ["el resultado no depende del inicio", "siempre se llega al mismo punto", "la función es lineal"], "Es la marca del caos (efecto mariposa)."),
             ("¿Quién descubrió el atractor que lleva su nombre al estudiar el clima?", "Edward Lorenz", ["Isaac Newton", "Carl Friedrich Gauss", "Benoît Mandelbrot"], "Lorenz notó en los años 60 que pequeños redondeos cambiaban el pronóstico."),
             ("Un punto fijo de f es…", "un valor x con f(x) = x", ["un valor con f(x) = 0", "el máximo de f", "el valor inicial"], "Si llegas a él, la iteración ya no cambia."),
             ("La órbita de x₀ bajo f es…", "la sucesión x₀, f(x₀), f(f(x₀)), …", ["la gráfica de f", "el dominio de f", "el área bajo f"], "Son los valores que se obtienen al iterar."),
             ("Iterar f(x) = x/2 desde cualquier número hace que los valores…", "se acerquen a 0", ["crezcan sin límite", "se queden igual", "cambien de signo"], "Cada vez es la mitad.")]
    return from_bank(items)


def _orb(f, x0, n):
    out = [x0]
    for _ in range(n):
        out.append(f(out[-1]))
    return out


# ============================================================ TSM II-2: sucesiones y series
def u2(*ks):
    t = pick(ks, ["lim", "serie", "fib", "converge", "sierp"])
    if t == "lim":
        a, b, c, d = nz(-6, 6), R.randint(-9, 9), nz(1, 6), R.randint(-9, 9)
        return opt("¿A qué número se acerca a<sub>n</sub> = (%s)/(%s) cuando n → ∞?" % (poly([a, b]).replace("x", "n"), poly([c, d]).replace("x", "n")), fq(F(a, c)),
                   [fq(F(b, d)) if d else "0", "∞", fq(F(c, a))], "Para n muy grande mandan los términos con n: %s/%s = <b>%s</b>." % (sg(a), sg(c), fq(F(a, c))))
    if t == "serie":
        a = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
        r = R.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2), F(1, 5)])
        S = F(a) / (1 - r)
        terms = [F(a) * r ** i for i in range(3)]
        return opt("Calcula la suma de la serie infinita %s + …" % " + ".join(fq(x) for x in terms).replace("+ −", "− "), fq(S), [fq(F(a) / (1 + r)), fq(sum(terms)), "∞"],
                   "Serie geométrica con a = %d y r = %s (|r| &lt; 1): S = a ÷ (1 − r) = <b>%s</b>." % (a, fq(r), fq(S)))
    if t == "fib":
        a, b = R.randint(1, 5), R.randint(1, 8)
        s = [a, b]
        n = R.randint(6, 9)
        while len(s) < n:
            s.append(s[-1] + s[-2])
        return opt("Una sucesión tipo Fibonacci empieza %s, %s, y cada término es la suma de los dos anteriores. ¿Cuál es el término %d?" % (a, b, n), num(s[-1]), [num(s[-2]), num(s[-1] + s[-2]), num(s[-1] - 1)],
                   "%s → <b>%s</b>." % (", ".join(map(str, s)), num(s[-1])))
    if t == "converge":
        items = [("¿Converge la serie 1 + 1/2 + 1/3 + 1/4 + … (serie armónica)?", "no, crece sin límite aunque muy despacio", ["sí, a 2", "sí, a 1", "sí, a e"], "Es un resultado famoso de Oresme (siglo XIV)."),
                 ("La serie 1 + 1/2 + 1/4 + 1/8 + … converge a…", "2", ["1", "∞", "1.5"], "Geométrica con r = 1/2: 1 ÷ (1 − 1/2) = 2."),
                 ("Una serie geométrica converge si…", "|r| &lt; 1", ["r &gt; 1", "r = 1", "su primer término es 0"], "Si |r| ≥ 1 los términos no se hacen pequeños."),
                 ("Si los términos de una sucesión no se acercan a 0, la serie…", "no converge", ["siempre converge", "converge a 0", "converge a 1"], "Es una condición necesaria para converger."),
                 ("El cociente entre términos consecutivos de Fibonacci se acerca a…", "la razón áurea φ ≈ 1.618", ["2", "π", "1"], "8/5 = 1.6, 13/8 = 1.625, 21/13 ≈ 1.615…"),
                 ("0.999… (con nueves infinitos) es igual a…", "1", ["0.9", "casi 1, pero menor", "no es un número"], "Es la serie 9/10 + 9/100 + … = 0.9 ÷ (1 − 0.1) = 1.")]
        return from_bank(items)
    n = R.randint(1, 6)
    q = R.choice(["area", "per"])
    if q == "area":
        return opt("En el triángulo de Sierpiński, ¿qué fracción del área original queda después de %d pasos?" % n, fq(F(3, 4) ** n), [fq(F(1, 4) ** n), fq(F(3, 4) ** (n + 1)), fq(F(3 * n, 4 * n + 1))],
                   "(3/4)<sup>%d</sup> = <b>%s</b>. El área tiende a 0." % (n, fq(F(3, 4) ** n)))
    return opt("En el triángulo de Sierpiński, la suma de los perímetros de los triángulos es 3 × (3/2)<sup>n</sup>. ¿Cuánto vale con n = %d?" % n, fq(3 * F(3, 2) ** n),
               [fq(3 * F(2, 3) ** n), fq(3 * F(3, 2) ** (n + 1)), fq(F(9, 2) * n)], "3 × (3/2)<sup>%d</sup> = <b>%s</b>. El perímetro crece sin límite mientras el área tiende a 0." % (n, fq(3 * F(3, 2) ** n)))


# ============================================================ TSM II-3: sumas de Riemann
def u3(*ks):
    t = pick(ks, ["dx", "suma", "medio", "sigma", "limite"])
    a = R.randint(0, 3)
    b = a + R.choice([2, 3, 4, 6])
    n = R.choice([2, 3, 4, 6])
    dx = F(b - a, n)
    if t == "dx":
        return opt("Se divide [%d, %d] en %d subintervalos iguales. ¿Cuánto mide cada uno (Δx)?" % (a, b, n), fq(dx), [fq(F(b, n)), fq(F(n, b - a)), fq(dx * 2)], "Δx = (b − a) ÷ n = %d ÷ %d = <b>%s</b>." % (b - a, n, fq(dx)))
    m, c = R.randint(0, 3), R.randint(0, 5)
    f = lambda x: m * x * x + c
    fx = poly([m, 0, c]) if m else str(c)
    if t in ("suma", "medio"):
        if m == 0:
            return None
        pts = [a + dx * (i + F(1, 2)) for i in range(n)] if t == "medio" else [a + dx * (i + 1) for i in range(n)]
        S = sum(f(p) for p in pts) * dx
        L = sum(f(a + dx * i) for i in range(n)) * dx
        exact = F(m, 3) * (b ** 3 - a ** 3) + c * (b - a)
        return opt("Aproxima ∫ de %d a %d de (%s) dx con %d rectángulos, usando el %s de cada subintervalo." % (a, b, fx, n, "punto medio" if t == "medio" else "extremo derecho"), show(S),
                   [show(L) if L != S else show(S + 1), show(exact) if exact != S else show(S + 2), show(S / dx)],
                   "Δx = %s; puntos %s. Suma = Δx × Σ f = <b>%s</b> (el valor exacto es %s)." % (show(dx), ", ".join(show(p) for p in pts), show(S), show(exact)))
    if t == "sigma":
        k = R.randint(3, 8)
        c1, c0 = R.randint(1, 5), R.randint(-3, 5)
        v = sum(c1 * i + c0 for i in range(1, k + 1))
        return opt("Calcula Σ<sub>i=1</sub><sup>%d</sup> (%s)." % (k, poly([c1, c0]).replace("x", "i")), num(v), [num(c1 * k + c0), num(v + c0), num(c1 * k * (k + 1))],
                   "Se suman los valores para i = 1, …, %d: <b>%s</b>." % (k, num(v)))
    items = [("Si el número de rectángulos de una suma de Riemann tiende a infinito, la suma tiende a…", "la integral definida (el área exacta)", ["0", "infinito", "la derivada"], "Esa es la definición de la integral de Riemann."),
             ("Con la función creciente f(x) = x² en [0, 2], usar el extremo izquierdo de cada rectángulo da…", "una aproximación por debajo del área real", ["una aproximación por encima", "el valor exacto", "un número negativo"], "En una función creciente el lado izquierdo es el más bajo."),
             ("En la suma de Riemann Σ f(xᵢ)Δx, el factor Δx representa…", "el ancho de cada rectángulo", ["la altura de cada rectángulo", "el número de rectángulos", "el área total"], "f(xᵢ) es la altura."),
             ("¿Quién formalizó la integral como límite de sumas en el siglo XIX?", "Bernhard Riemann", ["Pitágoras", "René Descartes", "Blaise Pascal"], "Por eso se llaman sumas de Riemann."),
             ("Si f es negativa en un intervalo, la integral definida en él es…", "negativa", ["siempre positiva", "cero", "infinita"], "Los rectángulos quedan por debajo del eje x.")]
    return from_bank(items)


# ============================================================ TSM II-7: métodos numéricos
def u7(*ks):
    t = pick(ks, ["biseccion", "newton", "punto_fijo", "concepto"])
    if t == "biseccion":
        while True:
            cs = [1, R.randint(-4, 4), R.randint(-6, 6), R.randint(-8, 8)]
            a = R.randint(-3, 2)
            b = a + 2
            if ev(cs, a) * ev(cs, b) < 0 and ev(cs, a + 1) != 0:
                break
        m = a + 1
        nxt = "[%s, %s]" % (sg(a), sg(m)) if ev(cs, a) * ev(cs, m) < 0 else "[%s, %s]" % (sg(m), sg(b))
        return opt("Con el método de bisección para f(x) = %s en [%s, %s] (f(%s) = %s, f(%s) = %s), se evalúa el punto medio x = %s. ¿Qué intervalo sigue?" % (poly(cs), sg(a), sg(b), sg(a), sg(ev(cs, a)), sg(b), sg(ev(cs, b)), sg(m)),
                   nxt, [x for x in ["[%s, %s]" % (sg(a), sg(m)), "[%s, %s]" % (sg(m), sg(b)), "[%s, %s]" % (sg(a), sg(b)), "[%s, %s]" % (sg(a - 1), sg(a))] if x != nxt][:3],
                   "f(%s) = %s. El cero está donde hay cambio de signo: <b>%s</b>." % (sg(m), sg(ev(cs, m)), nxt))
    if t == "newton":
        N = R.choice([2, 3, 5, 6, 7, 10, 11, 13, 17])
        x0 = R.choice([1, 2, 3, 4])
        x1 = F(x0) - F(x0 * x0 - N, 2 * x0)
        return opt("Para aproximar √%d se usa Newton-Raphson con f(x) = x² − %d y x₀ = %d: x₁ = x₀ − f(x₀)/f′(x₀). ¿Cuánto vale x₁?" % (N, N, x0), show(x1),
                   [show(F(x0) + F(x0 * x0 - N, 2 * x0)), show(F(x0) - F(x0 * x0 - N, x0)), show(F(N, x0))],
                   "f(%d) = %s, f′(%d) = %d. x₁ = %d − (%s)/%d = <b>%s</b> (√%d ≈ %s)." % (x0, sg(x0 * x0 - N), x0, 2 * x0, x0, sg(x0 * x0 - N), 2 * x0, show(x1), N, d2(math.sqrt(N), 3)))
    if t == "punto_fijo":
        k = R.choice([2, 3, 4, 5])
        b = R.randint(1, 9)
        x0 = R.randint(0, 6)
        x1 = F(x0, k) + b
        x2 = x1 / k + b
        return opt("Con aproximaciones sucesivas x<sub>n+1</sub> = x<sub>n</sub>/%d + %d y x₀ = %d, ¿cuánto vale x₂?" % (k, b, x0), show(x2), [show(x1), show(x2 + b), show(F(b * k, k - 1))],
                   "x₁ = %d/%d + %d = %s; x₂ = %s/%d + %d = <b>%s</b>. Se acerca al punto fijo %s." % (x0, k, b, show(x1), show(x1), k, b, show(x2), show(F(b * k, k - 1))))
    items = [("El método de bisección siempre funciona si…", "f es continua y cambia de signo en el intervalo", ["f es derivable en todo ℝ", "f es un polinomio de grado 2", "el intervalo empieza en 0"], "Se apoya en el teorema del valor intermedio."),
             ("En cada paso del método de bisección, el intervalo…", "se reduce a la mitad", ["se duplica", "se reduce a un tercio", "no cambia"], "Por eso converge, aunque despacio."),
             ("El método de Newton-Raphson usa…", "la recta tangente para acercarse al cero", ["rectas paralelas al eje x", "solo el punto medio", "áreas bajo la curva"], "x₁ es donde la tangente en x₀ corta al eje x."),
             ("Newton-Raphson puede fallar si…", "f′(x) es 0 cerca de la aproximación", ["f es un polinomio", "el número inicial es positivo", "la raíz es entera"], "Habría que dividir entre 0 o la tangente es casi horizontal."),
             ("Comparado con bisección, Newton-Raphson suele…", "converger mucho más rápido", ["ser más lento", "no necesitar derivada", "funcionar siempre"], "Cuando funciona, duplica las cifras correctas en cada paso."),
             ("¿Para qué sirven los métodos numéricos?", "para aproximar soluciones que no se pueden obtener con una fórmula", ["para evitar usar calculadora", "para dibujar gráficas de barras", "para calcular medias"], "Las computadoras los usan todo el tiempo.")]
    return from_bank(items)


# ============================================================ TSM II-6: modelos con ecuaciones diferenciales
def u6(*ks):
    t = pick(ks, ["lotka", "logistico", "newton", "kuramoto"])
    if t == "lotka":
        a, b = R.choice([F(1, 2), 1, F(1, 5), F(1, 10)]), R.choice([F(1, 100), F(1, 50), F(1, 20)])
        x, y = R.choice([100, 200, 50, 40]), R.choice([10, 20, 5, 30])
        v = a * x - b * x * y
        return opt("En un modelo presa-depredador, las presas cumplen dx/dt = %sx − %s·xy. Si hay x = %d presas e y = %d depredadores, ¿a qué ritmo cambian las presas?" % ("" if a == 1 else fq(a) + "·", fq(b), x, y), fq(v),
                   [fq(a * x), fq(-v) if v else "1", fq(b * x * y)], "dx/dt = %s × %d − %s × %d × %d = <b>%s</b>. %s" % (fq(a), x, fq(b), x, y, fq(v), "Las presas aumentan." if v > 0 else "Las presas disminuyen." if v < 0 else "Están en equilibrio."))
    if t == "logistico":
        k = R.choice([F(1, 10), F(1, 5), F(1, 2)])
        M = R.choice([1000, 2000, 5000, 10000])
        P = R.choice([M // 10, M // 4, M // 2, 3 * M // 4, M])
        v = k * P * (1 - F(P, M))
        return opt("Una población sigue dP/dt = %s·P(1 − P/%s). ¿A qué ritmo crece cuando P = %s?" % (fq(k), num(M), num(P)), show(v), [show(k * P), show(k * M), show(k * P * F(P, M))],
                   "dP/dt = %s × %s × (1 − %s/%s) = <b>%s</b>. %s" % (fq(k), num(P), num(P), num(M), show(v), "En P = M el crecimiento se detiene." if P == M else ""))
    if t == "newton":
        k = R.choice([F(1, 10), F(1, 20), F(1, 5)])
        Ta = R.choice([20, 22, 25])
        T = R.choice([90, 80, 70, 60, 45])
        v = -k * (T - Ta)
        return opt("Un café se enfría según dT/dt = −%s(T − %d) (°C por minuto). ¿A qué ritmo cambia su temperatura cuando está a %d °C?" % (fq(k), Ta, T), show(v) + " °C/min",
                   [show(-v) + " °C/min", show(-k * T) + " °C/min", show(T - Ta) + " °C/min"], "dT/dt = −%s × (%d − %d) = <b>%s °C/min</b>: se enfría más rápido cuanto más caliente está." % (fq(k), T, Ta, show(v)))
    items = [("El modelo de Kuramoto describe…", "cómo muchos osciladores (como luciérnagas o metrónomos) llegan a sincronizarse", ["el crecimiento de una población aislada", "el interés compuesto", "la caída de un objeto"], "Cada oscilador ajusta su ritmo según los demás."),
             ("En el modelo de Lotka-Volterra, si no hay depredadores (y = 0), las presas…", "crecen exponencialmente", ["se extinguen", "se quedan constantes", "oscilan"], "dx/dt = ax: crecimiento exponencial."),
             ("En el modelo de Lotka-Volterra, si no hay presas, los depredadores…", "disminuyen", ["aumentan", "se quedan igual", "se duplican"], "Sin alimento su población baja: dy/dt = −cy."),
             ("Las soluciones del modelo presa-depredador suelen ser…", "oscilaciones: cuando suben las presas, después suben los depredadores", ["rectas", "constantes", "siempre crecientes"], "Las dos poblaciones suben y bajan con un desfase."),
             ("Un punto de equilibrio de dP/dt = f(P) es un valor de P con…", "f(P) = 0", ["f(P) = P", "f(P) = 1", "P = 0 siempre"], "Allí la población no cambia."),
             ("En dP/dt = kP(1 − P/M), M representa…", "la capacidad de carga (población máxima sostenible)", ["la tasa de crecimiento", "la población inicial", "el tiempo"], "La población se acerca a M.")]
    return from_bank(items)
