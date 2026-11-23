# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de ESO: Geometría analítica (Sentido espacial)
Vectores (coordenadas, suma, producto por un número, módulo), distancia entre dos puntos y punto medio, pendiente, ecuaciones de la recta (explícita, general, punto-pendiente),
rectas paralelas y perpendiculares, posición relativa e intersección de dos rectas.
Errores: restar al revés las coordenadas, confundir la pendiente perpendicular (−1/m) con la opuesta, olvidar la raíz en la distancia.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, sg, fq, num, unit, L, E, MINUS, raiz, kosy

R = random.Random(50008)
BLUE, RED = "#1565c0", "#c62828"


def P(x, y, n=""):
    return "%s(%s, %s)" % (n, fq(x), fq(y))


def V(x, y):
    return "(%s, %s)" % (fq(x), fq(y))


def expl(m, n):
    return "y = %s" % E((m, "x"), (n, ""))


def gen(A, B, C):
    return "%s = 0" % E((A, "x"), (B, "y"), (C, ""))


def s_vectores():
    t = R.choice(["suma", "resta", "esc", "comb", "mod"])
    u = (R.randint(-6, 6), R.randint(-6, 6))
    v = (R.randint(-6, 6), R.randint(-6, 6))
    k = R.choice([-3, -2, 2, 3, 4])
    if t == "suma":
        r = (u[0] + v[0], u[1] + v[1])
        return M("Si u = %s y v = %s, calcula u + v." % (V(*u), V(*v)), V(*r), [V(u[0] - v[0], u[1] - v[1]), V(u[0] * v[0], u[1] * v[1]), V(u[0] + v[1], u[1] + v[0])], "Sumamos coordenada a coordenada: <b>%s</b>." % V(*r))
    if t == "resta":
        r = (u[0] - v[0], u[1] - v[1])
        return M("Si u = %s y v = %s, calcula u − v." % (V(*u), V(*v)), V(*r), [V(v[0] - u[0], v[1] - u[1]), V(u[0] + v[0], u[1] + v[1]), V(u[0] - v[1], u[1] - v[0])], "Restamos coordenada a coordenada: <b>%s</b>." % V(*r))
    if t == "esc":
        r = (k * u[0], k * u[1])
        return M("Si u = %s, calcula %s · u." % (V(*u), sg(k)), V(*r), [V(k * u[0], u[1]), V(u[0] + k, u[1] + k), V(-r[0], -r[1])], "Multiplicamos cada coordenada por %s: <b>%s</b>." % (sg(k), V(*r)))
    if t == "comb":
        r = (2 * u[0] - v[0], 2 * u[1] - v[1])
        return M("Si u = %s y v = %s, calcula 2u − v." % (V(*u), V(*v)), V(*r), [V(2 * u[0] + v[0], 2 * u[1] + v[1]), V(2 * (u[0] - v[0]), 2 * (u[1] - v[1])), V(u[0] - 2 * v[0], u[1] - 2 * v[1])], "2u = %s; 2u − v = <b>%s</b>." % (V(2 * u[0], 2 * u[1]), V(*r)))
    a, b = R.randint(-8, 8), R.randint(-8, 8)
    if a == 0 or b == 0:
        return None
    n = a * a + b * b
    return M("¿Cuál es el módulo del vector %s?" % V(a, b), raiz(n), [num(abs(a) + abs(b)), num(n), raiz(abs(a * a - b * b)) if a * a != b * b else raiz(2 * n)], "|v| = √(%s² + %s²) = √%d = <b>%s</b>." % (sg(a), sg(b), n, raiz(n)))


def s_distancia():
    t = R.choice(["dist", "dist", "medio", "medio", "sim"])
    x1, y1 = R.randint(-8, 8), R.randint(-8, 8)
    if t == "dist":
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (8, 15), (1, 2), (2, 3), (1, 3), (2, 5), (4, 4), (7, 24)])
        a, b = (a, b) if R.random() < 0.5 else (b, a)
        x2, y2 = x1 + a * R.choice([1, -1]), y1 + b * R.choice([1, -1])
        n = a * a + b * b
        return M("¿Cuál es la distancia entre %s y %s?" % (P(x1, y1, "A"), P(x2, y2, "B")), raiz(n), [num(a + b), num(n), raiz(abs(a * a - b * b)) if a != b else raiz(4 * n)], "d = √(%d² + %d²) = √%d = <b>%s</b>." % (a, b, n, raiz(n)))
    x2, y2 = R.randint(-8, 8), R.randint(-8, 8)
    if t == "medio":
        m = (F(x1 + x2, 2), F(y1 + y2, 2))
        return M("¿Cuál es el punto medio del segmento de extremos %s y %s?" % (P(x1, y1, "A"), P(x2, y2, "B")), P(*m, n="M"), [P(x2 - x1, y2 - y1, "M"), P(F(x2 - x1, 2), F(y2 - y1, 2), "M"), P(x1 + x2, y1 + y2, "M")], "M = ((x₁ + x₂)/2, (y₁ + y₂)/2) = <b>%s</b>." % P(*m))
    s = (2 * x2 - x1, 2 * y2 - y1)
    return M("¿Cuál es el simétrico de %s respecto de %s?" % (P(x1, y1, "A"), P(x2, y2, "M")), P(*s, n="A′"), [P(F(x1 + x2, 2), F(y1 + y2, 2), "A′"), P(-x1, -y1, "A′"), P(x2 - x1, y2 - y1, "A′")], "M es el punto medio de AA′: A′ = 2M − A = <b>%s</b>." % P(*s))


def s_pendiente():
    t = R.choice(["dos", "dos", "expl", "general", "punto"])
    x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    dx, dy = R.choice([1, 2, 3, 4, -2, -1]), R.randint(-6, 6)
    if dy == 0:
        return None
    x2, y2 = x1 + dx, y1 + dy
    m = F(dy, dx)
    n = y1 - m * x1
    if t == "dos":
        return M("¿Cuál es la pendiente de la recta que pasa por %s y %s?" % (P(x1, y1, "A"), P(x2, y2, "B")), fq(m), [fq(1 / m), fq(-m), fq(F(y2 + y1, x2 + x1)) if x1 + x2 and F(y2 + y1, x2 + x1) != m else fq(m + 1)], "m = (y₂ − y₁)/(x₂ − x₁) = %s/%s = <b>%s</b>." % (sg(dy), sg(dx), fq(m)))
    if t == "expl":
        if n.denominator > 1:
            return None
        ok = expl(m, n)
        return M("¿Cuál es la ecuación explícita de la recta que pasa por %s y %s?" % (P(x1, y1, "A"), P(x2, y2, "B")), ok, [expl(-m, n), expl(m, -n) if n else expl(m, 1), expl(1 / m, n), expl(m, y1)], "m = %s; n = y₁ − m·x₁ = %s. <b>%s</b>." % (fq(m), fq(n), ok))
    if t == "general":
        A, B = R.randint(-6, 6), R.randint(-6, 6)
        C = R.randint(-9, 9)
        if A == 0 or B == 0:
            return None
        mm = F(-A, B)
        return M("¿Cuál es la pendiente de la recta %s?" % gen(A, B, C), fq(mm), [fq(F(A, B)), fq(F(-B, A)), fq(F(-C, B)) if F(-C, B) != mm else fq(mm + 1)], "Despejamos y: y = %s. <b>m = %s</b>." % (E((mm, "x"), (F(-C, B), "")), fq(mm)))
    ok = "y %s = %s(x %s)" % (("− %s" % sg(y1)) if y1 > 0 else ("+ %s" % sg(-y1)) if y1 < 0 else "", fq(m), ("− %s" % sg(x1)) if x1 > 0 else ("+ %s" % sg(-x1)) if x1 < 0 else "")
    ok = ok.replace("y  =", "y =").replace("(x )", "x").replace("(x)", "x")
    if n.denominator > 1:
        return None
    return M("Una recta pasa por %s y tiene pendiente %s. ¿Cuál es su ecuación?" % (P(x1, y1, "A"), fq(m)), expl(m, n), [expl(m, y1), expl(m, -n) if n else expl(m, x1), expl(-m, n), expl(m, x1 - y1) if x1 - y1 != n else expl(m, n + 1)],
             "Punto-pendiente: %s → <b>%s</b>." % (ok, expl(m, n)))


def s_paralelas():
    m = F(R.choice([-4, -3, -2, 2, 3, 4]), R.choice([1, 1, 5, 7]))
    n = R.randint(-6, 6)
    x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
    t = R.choice(["par", "perp", "perp", "pend"])
    if t == "pend":
        k = R.choice(["paralela", "perpendicular"])
        ok = fq(m) if k == "paralela" else fq(-1 / m)
        return M("¿Qué pendiente tiene una recta %s a %s?" % (k, expl(m, n)), ok, [fq(-m), fq(1 / m), fq(-1 / m) if k == "paralela" else fq(m)], "%s: <b>%s</b>." % ("Paralelas: misma pendiente" if k == "paralela" else "Perpendiculares: m′ = −1/m", ok))
    mm = m if t == "par" else -1 / m
    nn = y0 - mm * x0
    if nn.denominator > 1:
        return None
    ok = expl(mm, nn)
    alt = -m if t == "par" else m
    return M("¿Cuál es la recta %s a %s que pasa por %s?" % ("paralela" if t == "par" else "perpendicular", expl(m, n), P(x0, y0, "P")), ok, [expl(mm, n) if n != nn else expl(mm, nn + 1), expl(alt, y0 - alt * x0), expl(1 / m if t == "perp" else -1 / m, y0 - (1 / m if t == "perp" else -1 / m) * x0)],
             "Pendiente %s y pasa por P: n = %s − %s · %s = %s. <b>%s</b>." % (fq(mm), sg(y0), "(%s)" % fq(mm) if mm < 0 else fq(mm), "(%s)" % sg(x0) if x0 < 0 else sg(x0), fq(nn), ok))


def s_posicion():
    t = R.choice(["corte", "corte", "relativa", "pertenece"])
    if t == "corte":
        x, y = R.randint(-5, 5), R.randint(-5, 5)
        m1, m2 = R.sample([-3, -2, -1, 1, 2, 3], 2)
        n1, n2 = y - m1 * x, y - m2 * x
        pic = kosy(lines=[(m1, n1, BLUE, ""), (m2, n2, RED, "")], lo=-6, hi=6) if abs(x) <= 5 and abs(y) <= 5 else ""
        return M(pic + "¿En qué punto se cortan las rectas r: %s y s: %s?" % (expl(m1, n1), expl(m2, n2)), P(x, y), [P(y, x) if x != y else P(-x, y), P(x, n1), P(0, n1), P(-x, -y) if x or y else P(1, 1), P(x + 1, y), P(x, y - 1)], "Igualamos: %s = %s → x = %s, y = %s. <b>%s</b>." % (E((m1, "x"), (n1, "")), E((m2, "x"), (n2, "")), sg(x), sg(y), P(x, y)))
    if t == "relativa":
        m = R.choice([-3, -2, -1, 1, 2, 3])
        n = R.randint(-6, 6)
        k = R.choice(["paralelas", "coincidentes", "secantes", "perpendiculares"])
        c = R.choice([2, 3])
        if k == "paralelas":
            A2, B2, C2 = -m * c, c, -(n + R.choice([1, 2, -1])) * c
        elif k == "coincidentes":
            A2, B2, C2 = -m * c, c, -n * c
        elif k == "secantes":
            mm = m + R.choice([1, 2]) if m + 1 != 0 and -1 / F(m) != m + 1 else m + 3
            if F(mm) * m == -1:
                return None
            A2, B2, C2 = -mm, 1, R.randint(-5, 5)
        else:
            A2, B2, C2 = 1, m, R.randint(-5, 5)
        return M("¿Cuál es la posición relativa de las rectas r: %s y s: %s?" % (expl(m, n), gen(A2, B2, C2)), k if k != "perpendiculares" else "secantes y perpendiculares", [x for x in ["paralelas", "coincidentes", "secantes (no perpendiculares)", "secantes y perpendiculares"] if not x.startswith(k[:6])],
                 "Comparamos pendientes y ordenadas: <b>%s</b>." % (k if k != "perpendiculares" else "secantes y perpendiculares"))
    m, n = R.choice([-3, -2, -1, 2, 3]), R.randint(-6, 6)
    xs = R.sample(range(-5, 6), 4)
    pts = [(xs[0], m * xs[0] + n)] + [(x, m * x + n + R.choice([-2, -1, 1, 2])) for x in xs[1:]]
    return M("¿Qué punto pertenece a la recta %s?" % expl(m, n), P(*pts[0]), [P(*p) for p in pts[1:]], "Sustituimos x = %s: y = %s. <b>%s</b>." % (sg(pts[0][0]), sg(pts[0][1]), P(*pts[0])))


seen = set()
sets = [("Vectores", mix(R, seen, [(s_vectores, 20)])), ("Distancia y punto medio", mix(R, seen, [(s_distancia, 20)])), ("Pendiente y ecuaciones de la recta", mix(R, seen, [(s_pendiente, 20)])),
        ("Paralelas y perpendiculares", mix(R, seen, [(s_paralelas, 20)])), ("Posición relativa e intersección", mix(R, seen, [(s_posicion, 20)]))]
think = ["El vector AB = (x₂ − x₁, y₂ − y₁). Su <b>módulo</b> es √(a² + b²): la distancia entre A y B.",
         "<b>Punto medio</b>: M = ((x₁ + x₂)/2, (y₁ + y₂)/2).",
         "<b>Pendiente</b>: m = (y₂ − y₁)/(x₂ − x₁). Ecuación explícita: y = mx + n; general: Ax + By + C = 0 (m = −A/B).",
         "<b>Paralelas</b>: misma pendiente. <b>Perpendiculares</b>: m · m′ = −1, es decir, m′ = −1/m."]
ex = [("A(1, 2), B(4, 6)", ["AB = (3, 4)", "d = √(9 + 16)"], "d = 5"), ("Recta por (1, 3) con m = 2", ["y − 3 = 2(x − 1)"], "y = 2x + 1")]
mist = [["Restar al revés", "Siempre segundo punto menos primero, en x y en y."], ["Perpendicular con −m", "Es −1/m: la inversa y cambiada de signo."], ["Olvidar la raíz en la distancia", "d = √(Δx² + Δy²)."]]
body = L(think, ex, mist, kosy(lines=[(2, 1, BLUE, ""), (F(-1, 2), 3, RED, "")], lo=-5, hi=5))
faq = [("¿Cómo sé si dos rectas son perpendiculares?", "Multiplica sus pendientes: si da −1, son perpendiculares."),
       ("¿Qué significa la n en y = mx + n?", "Es la ordenada en el origen: el punto (0, n) donde la recta corta al eje Y.")]
unit(4, R, "geometria-analitica", "E", "Geometría analítica: vectores, distancia y punto medio; ecuaciones de la recta; pendiente; paralelismo y perpendicularidad; posiciones relativas de rectas",
     "Geometría analítica", "Geometría analítica", "Fichas de matemáticas de 4.º de ESO: vectores, distancia, punto medio, pendiente, ecuaciones de la recta, paralelas, perpendiculares e intersección. 100 ejercicios con soluciones.",
     "Perpendiculares: m · m′ = −1", "Paralelas: la misma pendiente.", body, faq, sets, 8)
