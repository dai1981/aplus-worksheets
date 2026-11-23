# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Funciones (Sentido algebraico)
build(lv): lv = 2 → «funciones-lineales»: concepto de función, pendiente y ordenada en el origen, ecuación de la recta, gráficas, problemas;
lv = 3 → «funciones-lineales-y-cuadraticas»: rectas (punto-pendiente, dos puntos, paralelas), parábolas (vértice, eje, cortes), problemas;
lv = 4 → «funciones-elementales»: cuadráticas, proporcionalidad inversa, exponenciales y logarítmicas, reconocer gráficas.
Errores: confundir pendiente y ordenada en el origen, calcular la pendiente al revés (Δx/Δy), olvidar el signo de a en la parábola.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, E, P2, sg, fq, d, num, unit, L, Kids, nz, kosy, kurve, tabla

R = None
LV = 2
K = None
BLUE, RED = "#1565c0", "#c62828"


def recta(m, b):
    return "y = %s" % E((m, "x"), (b, "")) if m else "y = %s" % fq(b)


def pt(x, y):
    return "(%s, %s)" % (fq(x), fq(y))


def s_concepto():
    q, a, w = R.choice([("En una función, a cada valor de x le corresponde…", "un único valor de y", ["dos valores de y", "ningún valor", "cualquier número de valores"]),
                        ("La gráfica de y = mx + n es…", "una recta", ["una parábola", "una hipérbola", "un círculo"]),
                        ("Si la pendiente de una recta es negativa, la función es…", "decreciente", ["creciente", "constante", "periódica"]),
                        ("La gráfica de y = 5 es…", "una recta horizontal", ["una recta vertical", "una recta que pasa por el origen", "una parábola"]),
                        ("Una función de proporcionalidad directa tiene la forma…", "y = mx", ["y = mx + n con n ≠ 0", "y = k/x", "y = x²"]),
                        ("¿Qué indica la ordenada en el origen de y = mx + n?", "dónde corta al eje Y", ["dónde corta al eje X", "la inclinación", "el valor máximo"]),
                        ("Dos rectas son paralelas si tienen…", "la misma pendiente", ["la misma ordenada en el origen", "pendientes opuestas", "el mismo punto de corte con X"]),
                        ("La variable que elegimos libremente se llama…", "variable independiente", ["variable dependiente", "pendiente", "ordenada"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_pend():
    m = F(nz(R, -4, 4), R.choice([1, 1, 2]))
    b = R.randint(-5, 5)
    t = R.choice(["mn", "dos_pts", "graf", "eval", "corte"])
    if t == "mn":
        k = R.choice(["m", "n"])
        ok = fq(m) if k == "m" else fq(b)
        return M("En la recta %s, ¿cuánto vale la %s?" % (recta(m, b), "pendiente" if k == "m" else "ordenada en el origen"), ok, [fq(b) if k == "m" else fq(m), fq(-m) if k == "m" else fq(-b) if b else "1", fq(m + 1) if k == "m" else fq(b + 1)],
                 "En y = mx + n, m es la pendiente y n la ordenada en el origen: <b>%s</b>." % ok)
    if t == "dos_pts":
        x1, x2 = R.sample(range(-4, 5), 2)
        y1, y2 = m * x1 + b, m * x2 + b
        return M("¿Cuál es la pendiente de la recta que pasa por %s y %s?" % (pt(x1, y1), pt(x2, y2)), fq(m), [fq(1 / m), fq(-m), fq((y2 + y1) / (x2 - x1)) if (y2 + y1) / (x2 - x1) != m else fq(m + 1)],
                 "m = (y₂ − y₁) / (x₂ − x₁) = %s / %s = <b>%s</b>." % (fq(y2 - y1), sg(x2 - x1), fq(m)))
    if t == "graf":
        if m.denominator != 1 or abs(b) > 4:
            return None
        pic = kosy(lines=[(m, b, BLUE, "")], lo=-5, hi=5)
        ok = recta(m, b)
        return M(pic + "¿Qué ecuación tiene la recta dibujada?", ok, [recta(-m, b), recta(m, -b) if b else recta(m, 2), recta(b if b else 1, m)], "Corta al eje Y en %s y por cada unidad a la derecha %s %s: <b>%s</b>." % (sg(b), "sube" if m > 0 else "baja", fq(abs(m)), ok))
    if t == "eval":
        x = R.randint(-4, 6)
        return M("Si f(x) = %s, ¿cuánto vale f(%s)?" % (E((m, "x"), (b, "")), sg(x)), fq(m * x + b), [fq(m + x + b), fq(m * x - b) if b else fq(m * x + 1), fq(-(m * x + b)) if m * x + b else "1"], "f(%s) = <b>%s</b>." % (sg(x), fq(m * x + b)))
    if m == 0:
        return None
    x0 = -F(b) / m
    return M("¿En qué punto corta la recta %s al eje X?" % recta(m, b), pt(x0, 0), [pt(0, b), pt(-x0, 0) if x0 else pt(1, 0), pt(F(b) / m if b else 1, 0) if F(b) / m != x0 else pt(x0 + 1, 0)], "Hacemos y = 0: %s = 0 → x = <b>%s</b>." % (E((m, "x"), (b, "")), fq(x0)))


def s_ecuacion():
    m = nz(R, -4, 4)
    x1, y1 = R.randint(-4, 4), R.randint(-6, 6)
    b = y1 - m * x1
    t = R.choice(["punto_pend", "dos", "paralela", "contexto"])
    if t == "punto_pend":
        return M("Escribe la ecuación de la recta de pendiente %s que pasa por %s." % (sg(m), pt(x1, y1)), recta(m, b), [recta(m, y1), recta(m, y1 + m * x1), recta(-m, y1 + m * x1)] if y1 + m * x1 != b else [recta(m, y1), recta(m, b + 2), recta(-m, b)],
                 "y − %s = %s(x − %s): <b>%s</b>." % ("(%s)" % sg(y1) if y1 < 0 else sg(y1), sg(m), "(%s)" % sg(x1) if x1 < 0 else sg(x1), recta(m, b)))
    if t == "dos":
        x2 = x1 + R.choice([1, 2, 3])
        y2 = m * x2 + b
        return M("Escribe la ecuación de la recta que pasa por %s y %s." % (pt(x1, y1), pt(x2, y2)), recta(m, b), [recta(-m, b), recta(m, -b) if b else recta(m, 1), recta(F(x2 - x1, y2 - y1) if y2 != y1 else 1, b)],
                 "Pendiente %s y la sustituimos con un punto: <b>%s</b>." % (sg(m), recta(m, b)))
    if t == "paralela":
        b0 = R.randint(-5, 5)
        return M("¿Cuál es la recta paralela a %s que pasa por %s?" % (recta(m, b0), pt(x1, y1)), recta(m, b), [recta(m, b0) if b0 != b else recta(m, b + 1), recta(-m, y1 + m * x1), recta(F(-1, m), b)], "Misma pendiente (%s) y pasa por el punto: <b>%s</b>." % (sg(m), recta(m, b)))
    fijo, var = R.randint(2, 30), R.randint(1, 9)
    ctx = R.choice([("Un fontanero cobra %d € por ir a casa y %d € por cada hora de trabajo." % (fijo, var), "el precio y por x horas"),
                    ("Un gimnasio cuesta %d € de matrícula y %d € al mes." % (fijo, var), "el coste y de x meses"),
                    ("Una vela mide %d cm y se consume %d cm cada hora." % (fijo * 3, var), "la altura y después de x horas")])
    if "vela" in ctx[0]:
        ok = recta(-var, fijo * 3)
        w = [recta(var, fijo * 3), recta(-fijo * 3, var), recta(-var, fijo)]
    else:
        ok = recta(var, fijo)
        w = [recta(fijo, var), recta(var + fijo, 0), recta(var, -fijo)]
    return M("%s ¿Qué función da %s?" % ctx, ok, w, "La parte fija es la ordenada en el origen y lo que cambia por unidad es la pendiente: <b>%s</b>." % ok)


def s_parabola():
    a = R.choice([1, 1, -1, 2, -2])
    h, k = R.randint(-3, 3), R.randint(-4, 4)
    b, c = -2 * a * h, a * h * h + k
    t = R.choice(["vertice", "eje", "abre", "corteY", "cortes", "graf"])
    f = P2(a, b, c)
    if t == "vertice":
        return M("¿Cuál es el vértice de la parábola y = %s?" % f, pt(h, k), [pt(-h, k) if h else pt(1, k), pt(h, c) if c != k else pt(h, k + 1), pt(k, h) if k != h else pt(h + 1, k)], "x = −b/2a = %s; y(%s) = %s: <b>%s</b>." % (sg(h), sg(h), sg(k), pt(h, k)))
    if t == "eje":
        return M("¿Cuál es el eje de simetría de y = %s?" % f, "x = %s" % sg(h), ["x = %s" % sg(-h) if h else "x = 1", "y = %s" % sg(k), "x = %s" % fq(F(b, 2 * a) if b else 2)] if F(b, 2 * a) != h else ["x = %s" % sg(-h) if h else "x = 1", "y = %s" % sg(k), "x = %s" % sg(h + 1)],
                 "x = −b / 2a = <b>%s</b>." % sg(h))
    if t == "abre":
        ok = "hacia arriba, con un mínimo" if a > 0 else "hacia abajo, con un máximo"
        return M("¿Cómo es la parábola y = %s?" % f, ok, ["hacia abajo, con un máximo" if a > 0 else "hacia arriba, con un mínimo", "hacia arriba, con un máximo", "es una recta"], "a = %s es %s: <b>%s</b>." % (sg(a), "positivo" if a > 0 else "negativo", ok))
    if t == "corteY":
        return M("¿En qué punto corta y = %s al eje Y?" % f, pt(0, c), [pt(c, 0), pt(0, k) if k != c else pt(0, c + 1), pt(0, b) if b != c else pt(0, -c) if c else pt(0, 1)], "Hacemos x = 0: y = <b>%s</b>." % sg(c))
    if t == "cortes":
        r1, r2 = R.sample(range(-5, 6), 2)
        f = P2(1, -(r1 + r2), r1 * r2)
        ok = "%s y %s" % (pt(min(r1, r2), 0), pt(max(r1, r2), 0))
        return M("¿En qué puntos corta y = %s al eje X?" % f, ok, ["%s y %s" % (pt(-max(r1, r2), 0), pt(-min(r1, r2), 0)), "%s" % pt(0, r1 * r2), "%s y %s" % (pt(min(r1, r2), 0), pt(max(r1, r2) + 1, 0))], "Resolvemos %s = 0: x = %s y x = %s: <b>%s</b>." % (f, sg(min(r1, r2)), sg(max(r1, r2)), ok))
    if abs(k) > 4 or abs(h) > 3 or abs(a) > 1:
        return None
    pic = kurve([(lambda x, a=a, h=h, k=k: a * (x - h) ** 2 + k, BLUE, "")], (-5, 5, 1), (-6, 6, 2), W=300, H=260)
    ok = "y = %s" % f
    return M(pic + "¿Qué función corresponde a la gráfica?", ok, ["y = %s" % P2(-a, -b, -c), "y = %s" % P2(a, -b, c) if b else "y = %s" % P2(a, 2, c), "y = %s" % P2(a, b, c + 2)], "El vértice es %s y abre hacia %s: <b>%s</b>." % (pt(h, k), "arriba" if a > 0 else "abajo", ok))


def s_elementales():
    t = R.choice(["tipo", "inv", "exp", "log", "asint", "crece"])
    if t == "tipo":
        f, a = R.choice([("y = 3/x", "hipérbola (proporcionalidad inversa)"), ("y = 2ˣ", "exponencial"), ("y = log₂ x", "logarítmica"), ("y = x² − 4", "parábola (cuadrática)"), ("y = 3x − 1", "recta (lineal)"),
                         ("y = 0,5ˣ", "exponencial"), ("y = −2/x", "hipérbola (proporcionalidad inversa)"), ("y = log x", "logarítmica")])
        opts = ["hipérbola (proporcionalidad inversa)", "exponencial", "logarítmica", "parábola (cuadrática)", "recta (lineal)"]
        return M("¿Qué tipo de función es %s?" % f, a, [o for o in opts if o != a], "Respuesta: <b>%s</b>." % a)
    if t == "inv":
        k = R.choice([6, 12, 24, 36, 60])
        x = R.choice([v for v in (1, 2, 3, 4, 6, 12) if k % v == 0])
        return M("Si y = %d/x, ¿cuánto vale y para x = %d?" % (k, x), str(k // x), [str(k * x), str(k - x), str(x)] if k // x != x else [str(k * x), str(k - x), str(x + 1)], "y = %d / %d = <b>%d</b>." % (k, x, k // x))
    if t == "exp":
        b = R.choice([2, 3, 5, 10])
        x = R.randint(-2, 4)
        v = F(b) ** x
        return M("Si f(x) = %dˣ, ¿cuánto vale f(%s)?" % (b, sg(x)), fq(v), [fq(F(b * x)) if b * x != v else fq(v + 1), fq(-v), fq(F(x, b)) if F(x, b) != v else fq(v * 2)], "%d%s = <b>%s</b>." % (b, "<sup>%s</sup>" % sg(x), fq(v)))
    if t == "log":
        b = R.choice([2, 3, 10])
        e = R.randint(-1, 4)
        x = F(b) ** e
        return M("Si f(x) = log<sub>%d</sub> x, ¿cuánto vale f(%s)?" % (b, fq(x)), sg(e), [sg(e + 1), fq(x / b) if x / b != e else sg(e - 1), sg(-e) if e else "1"], "%d<sup>%s</sup> = %s: <b>%s</b>." % (b, sg(e), fq(x), sg(e)))
    if t == "asint":
        q, a, w = R.choice([("¿Qué asíntotas tiene y = 4/x?", "los ejes: x = 0 e y = 0", ["solo x = 4", "y = 4", "no tiene"]),
                            ("¿Qué asíntota horizontal tiene y = 2ˣ?", "y = 0", ["x = 0", "y = 2", "no tiene"]),
                            ("¿Qué asíntota vertical tiene y = log x?", "x = 0", ["y = 0", "x = 1", "no tiene"]),
                            ("¿Por qué punto pasan todas las funciones y = aˣ?", "(0, 1)", ["(1, 0)", "(0, 0)", "(1, 1)"]),
                            ("¿Por qué punto pasan todas las funciones y = log<sub>a</sub> x?", "(1, 0)", ["(0, 1)", "(0, 0)", "(1, 1)"]),
                            ("¿Cuál es el dominio de y = log x?", "x &gt; 0", ["todos los reales", "x ≥ 0", "x ≠ 0"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    q, a, w = R.choice([("¿Cómo es y = 0,5ˣ?", "decreciente", ["creciente", "constante", "periódica"]), ("¿Cómo es y = 3ˣ?", "creciente", ["decreciente", "constante", "periódica"]),
                        ("¿Cómo es y = 5/x en x &gt; 0?", "decreciente", ["creciente", "constante", "tiene un máximo"]), ("¿Cómo es y = −2/x en x &gt; 0?", "creciente", ["decreciente", "constante", "tiene un mínimo"]),
                        ("Un capital crece un 5 % cada año. ¿Qué función describe el capital?", "exponencial", ["lineal", "cuadrática", "proporcionalidad inversa"]),
                        ("Repartir un premio fijo entre x personas da una función…", "de proporcionalidad inversa", ["lineal", "exponencial", "logarítmica"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_graf_elem():
    kind = R.choice(["inv", "exp", "log", "cuad", "lin"])
    if kind == "inv":
        k = R.choice([2, 4, -2, -4])
        f, ok = (lambda x, k=k: k / x), "y = %s/x" % sg(k)
        w = ["y = %s/x" % sg(-k), "y = %dx" % k, "y = %dˣ" % abs(k)]
    elif kind == "exp":
        b = R.choice([2, 3])
        dec = R.random() < 0.4
        f, ok = ((lambda x, b=b: (1.0 / b) ** x), "y = (1/%d)ˣ" % b) if dec else ((lambda x, b=b: b ** x), "y = %dˣ" % b)
        w = ["y = %dˣ" % b if dec else "y = (1/%d)ˣ" % b, "y = log<sub>%d</sub> x" % b, "y = x²"]
    elif kind == "log":
        b = R.choice([2, 3])
        f, ok = (lambda x, b=b: math.log(x, b)), "y = log<sub>%d</sub> x" % b
        w = ["y = %dˣ" % b, "y = 1/x", "y = −log<sub>%d</sub> x" % b]
    elif kind == "cuad":
        f, ok = (lambda x: x * x - 3), "y = x² − 3"
        w = ["y = −x² − 3", "y = x² + 3", "y = 3/x"]
    else:
        m = R.choice([2, -2, 1])
        f, ok = (lambda x, m=m: m * x + 1), "y = %s" % E((m, "x"), (1, ""))
        w = ["y = %s" % E((-m, "x"), (1, "")), "y = %dˣ" % 2, "y = x² + 1"]
    pic = kurve([(f, BLUE, "")], (-4, 4, 1), (-5, 5, 1), W=300, H=260)
    if ok in w:
        return None
    return M(pic + "¿Qué función está representada? (" + ", ".join(sorted(w + [ok])) + ")", ok, w, "Por su forma y por los puntos por los que pasa: <b>%s</b>." % ok)


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(48008 + (lv - 2) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 2:
        sets = [("Qué es una función", mix(R, seen, [(s_concepto, 8), (s_pend, 12)])), ("Pendiente y ordenada en el origen", mix(R, seen, [(s_pend, 20)])), ("Ecuación de la recta", mix(R, seen, [(s_ecuacion, 20)])),
                ("Gráficas de rectas", mix(R, seen, [(s_pend, 20)])), ("Funciones en contexto", mix(R, seen, [(s_ecuacion, 20)]))]
        think = ["Una <b>función</b> asocia a cada x un único valor de y. Su gráfica se dibuja con una tabla de valores.",
                 "En la función lineal y = mx + n, <b>m</b> es la pendiente (cuánto sube o baja por cada unidad de x) y <b>n</b> la ordenada en el origen (dónde corta al eje Y).",
                 "Pendiente entre dos puntos: m = (y₂ − y₁) / (x₂ − x₁)."]
        ex = [("Recta por (1, 3) y (3, 7)", ["m = (7 − 3)/(3 − 1) = 2", "3 = 2 · 1 + n → n = 1"], "y = 2x + 1")]
        slug, title, short, kb, ks, sort = "funciones-lineales", "Funciones lineales", "Funciones lineales", "y = mx + n", "m: pendiente. n: corte con el eje Y.", 8
        meta = "Fichas de matemáticas de 2.º de ESO: concepto de función, pendiente, ordenada en el origen, ecuación y gráfica de la recta y problemas. 100 ejercicios con soluciones."
        std = "Concepto de función; funciones lineales y afines: pendiente, ordenada en el origen, representación gráfica e interpretación en contextos"
    elif lv == 3:
        sets = [("Pendiente y ecuación de la recta", mix(R, seen, [(s_pend, 20)])), ("Rectas por puntos y paralelas", mix(R, seen, [(s_ecuacion, 20)])), ("Elementos de la parábola", mix(R, seen, [(s_parabola, 20)])),
                ("Gráficas de parábolas", mix(R, seen, [(s_parabola, 20)])), ("Funciones en contexto", mix(R, seen, [(s_ecuacion, 10), (s_parabola, 10)]))]
        think = ["Ecuación punto-pendiente: y − y₁ = m(x − x₁). Dos rectas paralelas tienen la misma pendiente.",
                 "La gráfica de y = ax² + bx + c es una <b>parábola</b>. Si a &gt; 0 abre hacia arriba; si a &lt; 0, hacia abajo.",
                 "Vértice: x = −b / 2a. Eje de simetría: la recta vertical que pasa por el vértice. Cortes con X: resolver ax² + bx + c = 0."]
        ex = [("y = x² − 4x + 3", ["Vértice x = 4/2 = 2, y = −1", "Cortes: x = 1 y x = 3"], "V(2, −1); corta en (1, 0) y (3, 0)")]
        slug, title, short, kb, ks, sort = "funciones-lineales-y-cuadraticas", "Funciones lineales y cuadráticas", "Rectas y parábolas", "Vértice: x = −b/2a", "a > 0 abre arriba; a < 0, abajo.", 8
        meta = "Fichas de matemáticas de 3.º de ESO: pendiente, ecuación de la recta, rectas paralelas, vértice, eje y cortes de la parábola. 100 ejercicios con soluciones."
        std = "Funciones lineales: ecuaciones de la recta; funciones cuadráticas: representación, vértice, eje de simetría y puntos de corte; modelización"
    else:
        sets = [("Parábolas", mix(R, seen, [(s_parabola, 20)])), ("Tipos de funciones", mix(R, seen, [(s_elementales, 20)])), ("Exponenciales y logarítmicas", mix(R, seen, [(s_elementales, 20)])),
                ("Reconocer gráficas", mix(R, seen, [(s_graf_elem, 12), (s_parabola, 8)])), ("Funciones en contexto", mix(R, seen, [(s_ecuacion, 10), (s_elementales, 10)]))]
        think = ["<b>Proporcionalidad inversa</b>: y = k/x, una hipérbola con asíntotas en los ejes.",
                 "<b>Exponencial</b>: y = aˣ (a &gt; 0); pasa por (0, 1); crece si a &gt; 1 y decrece si 0 &lt; a &lt; 1.",
                 "<b>Logarítmica</b>: y = log<sub>a</sub> x, solo para x &gt; 0; pasa por (1, 0). Es la inversa de la exponencial."]
        ex = [("f(x) = 2ˣ, f(−3)", ["2⁻³ = 1/8"], "1/8"), ("y = 12/x para x = 4", ["12 : 4"], "3")]
        slug, title, short, kb, ks, sort = "funciones-elementales", "Funciones elementales", "Funciones", "Exponencial y = aˣ pasa por (0, 1)", "Logarítmica y = logₐ x pasa por (1, 0).", 9
        meta = "Fichas de matemáticas de 4.º de ESO: parábolas, proporcionalidad inversa, funciones exponenciales y logarítmicas y reconocer gráficas. 100 ejercicios con soluciones."
        std = "Funciones elementales: lineales, cuadráticas, de proporcionalidad inversa, exponenciales y logarítmicas; características y gráficas; modelización"
    mist = [["Confundir pendiente y ordenada en el origen", "En y = 3x − 2, la pendiente es 3."], ["Calcular la pendiente al revés", "Δy entre Δx, no al contrario."], ["Olvidar el signo de a", "−x² abre hacia abajo."]]
    body = L(think, ex, mist)
    faq = [("¿Qué es la pendiente de una recta?", "Lo que aumenta (o disminuye) y cuando x aumenta una unidad."), ("¿Cómo se halla el vértice de una parábola?", "Con x = −b/2a; después se sustituye para hallar y.")]
    unit(lv, R, slug, "A", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
