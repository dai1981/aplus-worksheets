# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de ESO: Funciones y sus propiedades (Sentido algebraico)
Leer gráficas: dominio, recorrido, puntos de corte, crecimiento y decrecimiento, máximos y mínimos, continuidad, simetría, tasa de variación media; dominio de expresiones sencillas.
Errores: confundir dominio (x) y recorrido (y), dar el intervalo de crecimiento con valores de y, confundir máximo relativo y absoluto.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, sg, fq, num, unit, L, E, P2, MINUS, kurve

R = random.Random(49007)
BLUE = "#1565c0"
INF, MINF = "+∞", MINUS + "∞"


def P(x, y):
    return "(%s, %s)" % (sg(x), sg(y))


def ivl(a, b, ca=False, cb=False):
    return "%s%s, %s%s" % ("[" if ca else "(", MINF if a is None else sg(a), INF if b is None else sg(b), "]" if cb else ")")


def poly_graph():
    """polilínea con vértices enteros, sin tramos horizontales"""
    while True:
        n = R.randint(4, 6)
        xs = sorted(R.sample(range(-5, 6), n))
        ys = [R.randint(-4, 4) for _ in xs]
        if any(ys[i] == ys[i + 1] for i in range(n - 1)):
            continue
        dirs = [1 if ys[i + 1] > ys[i] else -1 for i in range(n - 1)]
        if len(set(dirs)) < 2:
            continue
        if len([i for i in range(1, n - 1) if dirs[i - 1] != dirs[i]]) < 1:
            continue
        return xs, ys


def f_of(xs, ys):
    def f(x):
        if x < xs[0] - 1e-9 or x > xs[-1] + 1e-9:
            return None
        for i in range(len(xs) - 1):
            if xs[i] - 1e-9 <= x <= xs[i + 1] + 1e-9:
                t = (x - xs[i]) / (xs[i + 1] - xs[i])
                return ys[i] + t * (ys[i + 1] - ys[i])
    return f


def pic_of(xs, ys):
    return kurve([(f_of(xs, ys), BLUE, "")], (-6, 6, 1), (-5, 5, 1), pts=[(xs[0], ys[0], ""), (xs[-1], ys[-1], "")], W=330, H=280, label="gráfica de una función")


def runs(xs, ys):
    out = []
    i = 0
    n = len(xs)
    while i < n - 1:
        dr = ys[i + 1] > ys[i]
        j = i
        while j < n - 1 and (ys[j + 1] > ys[j]) == dr:
            j += 1
        out.append((xs[i], xs[j], dr))
        i = j
    return out


def s_grafica():
    xs, ys = poly_graph()
    pic = pic_of(xs, ys)
    t = R.choice(["dom", "rec", "val", "cy", "crece", "decrece", "max", "min", "absmax", "tvm"])
    if t == "dom":
        ok = ivl(xs[0], xs[-1], True, True)
        return M(pic + "¿Cuál es el dominio de la función?", ok, [ivl(min(ys), max(ys), True, True), ivl(xs[0], xs[-1]), ivl(xs[0] + 1, xs[-1], True, True), ivl(None, None)], "Los valores de x que tienen imagen: de %s a %s. <b>%s</b>." % (sg(xs[0]), sg(xs[-1]), ok))
    if t == "rec":
        ok = ivl(min(ys), max(ys), True, True)
        return M(pic + "¿Cuál es el recorrido de la función?", ok, [ivl(xs[0], xs[-1], True, True), ivl(ys[0], ys[-1], True, True) if sorted([ys[0], ys[-1]]) != [min(ys), max(ys)] else ivl(min(ys), max(ys)), ivl(min(ys), max(ys) + 1, True, True)],
                 "Los valores de y que alcanza: del mínimo %s al máximo %s. <b>%s</b>." % (sg(min(ys)), sg(max(ys)), ok))
    f = f_of(xs, ys)
    if t == "val":
        i = R.randrange(len(xs))
        x = xs[i]
        others = [y for y in set(ys) if y != ys[i]]
        return M(pic + "Según la gráfica, ¿cuánto vale f(%s)?" % sg(x), sg(ys[i]), [sg(x) if x != ys[i] else None] + [sg(y) for y in sorted(others)], "Buscamos x = %s y leemos la altura: <b>%s</b>." % (sg(x), sg(ys[i])))
    if t == "cy":
        if not xs[0] < 0 < xs[-1]:
            return None
        y0 = f(0)
        if abs(y0 - round(y0)) > 1e-9:
            return None
        y0 = int(round(y0))
        return M(pic + "¿En qué punto corta la gráfica al eje Y?", P(0, y0), [P(y0, 0), P(0, y0 + 1), P(0, -y0) if y0 else P(0, 2), P(xs[0], ys[0])], "Corte con el eje Y: x = 0, y = f(0) = %s. <b>%s</b>." % (sg(y0), P(0, y0)))
    rs = runs(xs, ys)
    if t in ("crece", "decrece"):
        want = t == "crece"
        good = [r for r in rs if r[2] == want]
        bad = [r for r in rs if r[2] != want]
        if not good or not bad:
            return None
        a, b, _ = R.choice(good)
        ok = ivl(a, b)
        w = [ivl(*r[:2]) for r in bad] + [ivl(f(a), f(b)) if f(a) < f(b) else ivl(f(b), f(a)), ivl(a, b + 1) if b + 1 <= xs[-1] else ivl(a - 1, b)]
        w = [x.replace(".0", "") for x in w]
        return M(pic + "¿En qué intervalo es %s la función?" % ("creciente" if want else "decreciente"), ok, w,
                 "%s: <b>%s</b>." % ("Al avanzar hacia la derecha, la gráfica sube" if want else "Al avanzar hacia la derecha, la gráfica baja", ok))
    if t in ("max", "min"):
        want = t == "max"
        ext = [(xs[i], ys[i]) for i in range(1, len(xs) - 1) if ((ys[i] > ys[i - 1] and ys[i] > ys[i + 1]) if want else (ys[i] < ys[i - 1] and ys[i] < ys[i + 1]))]
        if not ext:
            return None
        x, y = R.choice(ext)
        other = [(xs[i], ys[i]) for i in range(len(xs)) if (xs[i], ys[i]) not in ext]
        return M(pic + "¿En qué punto tiene la función un %s relativo?" % ("máximo" if want else "mínimo"), P(x, y), [P(y, x)] + [P(*p) for p in other], "La gráfica pasa de %s en x = %s: <b>%s</b>." % ("subir a bajar" if want else "bajar a subir", sg(x), P(x, y)))
    if t == "absmax":
        want = R.random() < 0.5
        v = max(ys) if want else min(ys)
        if ys.count(v) > 1:
            return None
        i = ys.index(v)
        return M(pic + "¿Cuál es el %s absoluto de la función?" % ("máximo" if want else "mínimo"), "%s, en x = %s" % (sg(v), sg(xs[i])), ["%s, en x = %s" % (sg(xs[i]), sg(v)), "%s, en x = %s" % (sg(min(ys) if want else max(ys)), sg(xs[ys.index(min(ys) if want else max(ys))])), "%s, en x = %s" % (sg(ys[-1]), sg(xs[-1])) if ys[-1] != v else "%s, en x = %s" % (sg(ys[0]), sg(xs[0]))],
                 "El valor más %s que alcanza y: <b>%s, en x = %s</b>." % ("alto" if want else "bajo", sg(v), sg(xs[i])))
    i, j = sorted(R.sample(range(len(xs)), 2))
    a, b = xs[i], xs[j]
    tv = F(ys[j] - ys[i], b - a)
    return M(pic + "Calcula la tasa de variación media de f en [%s, %s]." % (sg(a), sg(b)), fq(tv), [fq(F(b - a, ys[j] - ys[i])), sg(ys[j] - ys[i]), fq(-tv) if tv else "1"],
             "TVM = (f(%s) − f(%s)) / (%s − %s) = (%s − %s) / %d = <b>%s</b>." % (sg(b), sg(a), sg(b), "(%s)" % sg(a) if a < 0 else sg(a), sg(ys[j]), "(%s)" % sg(ys[i]) if ys[i] < 0 else sg(ys[i]), b - a, fq(tv)))


def s_cortes():
    t = R.choice(["lin", "cuad", "cuad", "y"])
    if t == "lin":
        m, x0 = R.choice([-4, -3, -2, 2, 3, 4, 5]), R.randint(-6, 6)
        b = -m * x0
        if b == 0:
            return None
        f = E((m, "x"), (b, ""))
        return M("¿En qué punto corta f(x) = %s al eje X?" % f, P(x0, 0), [P(0, b), P(b, 0), P(-x0, 0)], "f(x) = 0 → %s = 0 → x = %s. <b>%s</b>." % (f, sg(x0), P(x0, 0)))
    if t == "cuad":
        r1, r2 = sorted(R.sample(range(-7, 8), 2))
        b, c = -(r1 + r2), r1 * r2
        f = P2(1, b, c)
        ok = "%s y %s" % (P(r1, 0), P(r2, 0))
        return M("¿En qué puntos corta f(x) = %s al eje X?" % f, ok, ["%s y %s" % (P(-r1, 0), P(-r2, 0)), "%s y %s" % (P(0, r1), P(0, r2)), P(0, c)], "x² %s = 0 → x = %s o x = %s. <b>%s</b>." % (f[2:], sg(r1), sg(r2), ok))
    a, b, c = R.choice([1, -1, 2, -2, 3]), R.randint(-6, 6), R.randint(-9, 9)
    f = P2(a, b, c)
    return M("¿En qué punto corta f(x) = %s al eje Y?" % f, P(0, c), [P(c, 0), P(0, a), P(0, a + b + c) if a + b + c != c else P(0, b)], "x = 0 → f(0) = %s. <b>%s</b>." % (sg(c), P(0, c)))


def s_dominio():
    t = R.choice(["poli", "frac", "frac2", "raiz", "raiz2"])
    a = R.randint(-9, 9)
    xa = "x" if a == 0 else ("x − %d" % a if a > 0 else "x + %d" % -a)
    if t == "poli":
        f = P2(R.choice([1, -1, 2, 3]), R.randint(-5, 5), R.randint(-9, 9))
        return M("¿Cuál es el dominio de f(x) = %s?" % f, "ℝ", ["ℝ − {0}", ivl(0, None, True), ivl(0, None)], "Un polinomio se puede calcular para cualquier x: <b>ℝ</b>.")
    if t == "frac":
        ok = "ℝ − {%s}" % sg(a)
        return M("¿Cuál es el dominio de f(x) = 1 / (%s)?" % xa, ok, ["ℝ − {%s}" % sg(-a) if a else "ℝ", "ℝ", ivl(a, None)], "El denominador no puede ser 0: %s ≠ 0 → x ≠ %s. <b>%s</b>." % (xa, sg(a), ok))
    if t == "frac2":
        r = R.randint(1, 9)
        ok = "ℝ − {%s, %s}" % (sg(-r), sg(r))
        return M("¿Cuál es el dominio de f(x) = 3 / (x² − %d)?" % (r * r), ok, ["ℝ − {%s}" % sg(r * r), "ℝ − {%s}" % sg(r), ivl(-r, r, True, True)], "x² − %d = 0 → x = ±%d. <b>%s</b>." % (r * r, r, ok))
    if t == "raiz":
        ok = ivl(a, None, True)
        return M("¿Cuál es el dominio de f(x) = √(%s)?" % xa, ok, [ivl(a, None), ivl(None, a, False, True), ivl(-a, None, True) if a else "ℝ"], "Dentro de la raíz no puede haber un número negativo: %s ≥ 0 → x ≥ %s. <b>%s</b>." % (xa, sg(a), ok))
    k = R.randint(1, 12)
    ok = ivl(None, k, False, True)
    return M("¿Cuál es el dominio de f(x) = √(%d − x)?" % k, ok, [ivl(k, None, True), ivl(None, k), ivl(-k, None, True)], "%d − x ≥ 0 → x ≤ %d. <b>%s</b>." % (k, k, ok))


def s_propiedades():
    t = R.choice(["par", "par", "cont", "per", "tvm"])
    if t == "par":
        k = R.choice(["par", "impar", "ninguna"])
        a, b = R.randint(1, 6), R.randint(1, 9)
        f = {"par": R.choice(["x² + %d" % b, "%dx⁴ − x²" % a, "|x|", "%d − x²" % b]), "impar": R.choice(["x³", "%dx" % a if a > 1 else "x", "x³ − %dx" % a, "1/x"]), "ninguna": R.choice(["x² + x", "x + %d" % b, "x³ + %d" % b, "%dx − x²" % a])}[k]
        ok = {"par": "par (simétrica respecto al eje Y)", "impar": "impar (simétrica respecto al origen)", "ninguna": "ni par ni impar"}[k]
        return M("¿Qué simetría tiene f(x) = %s?" % f, ok, [o for o in ["par (simétrica respecto al eje Y)", "impar (simétrica respecto al origen)", "ni par ni impar", "simétrica respecto al eje X"] if o != ok],
                 "Calculamos f(−x) y comparamos con f(x) y con −f(x): <b>%s</b>." % ok)
    if t == "cont":
        q, a, w = R.choice([("¿Es continua la función f(x) = 1/x?", "no, se rompe en x = 0", ["sí, en todo ℝ", "no, se rompe en x = 1", "no, se rompe en y = 0"]),
                            ("¿Qué indica un «salto» en la gráfica de una función?", "una discontinuidad", ["un máximo", "un punto de corte", "que la función es par"]),
                            ("La tarifa de un aparcamiento es 2 € por cada hora o fracción. ¿Cómo es su gráfica?", "escalonada y discontinua", ["una recta continua", "una parábola", "una recta que pasa por el origen"]),
                            ("¿Es continua la temperatura de un día dibujada en función de la hora?", "sí", ["no, cambia cada hora", "no, porque baja de noche", "solo de día"]),
                            ("¿Es continua f(x) = x² − 3x?", "sí, en todo ℝ", ["no, en x = 0", "no, en x = 3", "solo para x ≥ 0"]),
                            ("¿Dónde es discontinua f(x) = 2 / (x − 4)?", "en x = 4", ["en x = 2", "en x = −4", "en ningún punto"])])
        return M(q, a, w, "Respuesta: <b>%s</b>." % a)
    if t == "per":
        p = R.choice([2, 3, 4, 5, 6, 12, 24])
        x = R.randint(1, p - 1)
        v = R.randint(-9, 9)
        k = R.randint(2, 6)
        return M("Una función es periódica de período %d y f(%d) = %s. ¿Cuánto vale f(%d)?" % (p, x, sg(v), x + k * p), sg(v), [sg(v + k * p), sg(v * k), sg(-v) if v else "1"], "Cada %d unidades se repite: f(%d) = f(%d) = <b>%s</b>." % (p, x + k * p, x, sg(v)))
    a, b = sorted(R.sample(range(-4, 6), 2))
    c = R.randint(-5, 5)
    f = lambda x: x * x + c
    tv = F(f(b) - f(a), b - a)
    return M("Calcula la tasa de variación media de f(x) = %s en [%s, %s]." % (P2(1, 0, c), sg(a), sg(b)), fq(tv), [sg(f(b) - f(a)), fq(F(b - a, f(b) - f(a))) if f(b) != f(a) else "1", fq(F(f(b) + f(a), b - a))],
             "(f(%s) − f(%s)) / (%s − %s) = (%s − %s) / %d = <b>%s</b>." % (sg(b), sg(a), sg(b), "(%s)" % sg(a) if a < 0 else sg(a), sg(f(b)), "(%s)" % sg(f(a)) if f(a) < 0 else sg(f(a)), b - a, fq(tv)))


def s_contexto():
    t = R.choice(["excursion", "temp", "deposito", "tabla"])
    if t == "excursion":
        xs = [0, 1, 2, 3, 4, 5]
        while True:
            ys = [0] + [R.randint(1, 4) for _ in range(4)] + [0]
            if all(ys[i] != ys[i + 1] for i in range(5)):
                break
        pic = kurve([(f_of(xs, ys), BLUE, "")], (0, 6, 1), (0, 5, 1), W=330, H=240, label="distancia a casa (km) según el tiempo (h)")
        i = ys.index(max(ys))
        k = R.choice(["max", "vuelta", "dist"])
        if k == "max":
            return M(pic + "La gráfica muestra la distancia a casa (km) de una excursión según las horas. ¿Cuándo está más lejos?", "a las %d h" % xs[i], ["a las %d h" % x for x in xs if x != xs[i]], "El punto más alto de la gráfica: <b>a las %d h</b>, a %d km." % (xs[i], ys[i]))
        if k == "vuelta":
            return M(pic + "La gráfica muestra la distancia a casa (km) de una excursión según las horas. ¿Cuántos km está de casa a las 3 h?", "%d km" % ys[3], ["%d km" % y for y in sorted(set(ys)) if y != ys[3]] + ["3 km" if ys[3] != 3 else "6 km"], "Leemos la gráfica en x = 3: <b>%d km</b>." % ys[3])
        h = R.choice([1, 2, 3, 4])
        dd = ys[h + 1] - ys[h]
        return M(pic + "La gráfica muestra la distancia a casa (km) de una excursión según las horas. ¿Qué ocurre entre la hora %d y la %d?" % (h, h + 1), "se aleja de casa" if dd > 0 else "se acerca a casa", ["se acerca a casa" if dd > 0 else "se aleja de casa", "está parado", "vuelve a salir de casa"],
                 "La distancia %s: <b>%s</b>." % ("aumenta" if dd > 0 else "disminuye", "se aleja de casa" if dd > 0 else "se acerca a casa"))
    if t == "temp":
        q, a, w = R.choice([("Variable independiente al estudiar la temperatura a lo largo del día", "la hora", ["la temperatura", "el termómetro", "el lugar"]),
                            ("Variable dependiente al estudiar el precio de unas naranjas según los kilos", "el precio", ["los kilos", "la tienda", "el tipo de naranja"]),
                            ("Variable independiente al estudiar el área de un cuadrado según su lado", "el lado", ["el área", "el perímetro", "los vértices"]),
                            ("Variable dependiente al estudiar la altura de una planta según los días", "la altura", ["los días", "el riego", "la maceta"])])
        return M("¿Cuál es la %s?" % (q[0].lower() + q[1:]), a, w, "La %s es la que %s: <b>%s</b>." % ("independiente" if "independiente" in q else "dependiente", "elegimos libremente" if "independiente" in q else "depende de la otra", a))
    if t == "deposito":
        v0, c = R.choice([(100, 5), (120, 8), (200, 10), (90, 6), (150, 6), (60, 4)])
        h = R.randint(1, v0 // c - 1)
        return M("Un depósito tiene %d L y se vacía a %d L por minuto. ¿Qué fórmula da los litros que quedan, V, según los minutos, t?" % (v0, c), "V = %d − %dt" % (v0, c), ["V = %d + %dt" % (v0, c), "V = %dt − %d" % (c, v0), "V = %d / %dt" % (v0, c)], "Empieza en %d y baja %d cada minuto: <b>V = %d − %dt</b>. A los %d min quedan %d L." % (v0, c, v0, c, h, v0 - c * h))
    m, b = R.randint(2, 6), R.randint(-5, 8)
    xs = sorted(R.sample(range(-3, 7), 4))
    rows = [[sg(x) for x in xs], [sg(m * x + b) for x in xs]]
    from es_eso import tabla
    pic = tabla(["x"] + rows[0], [["y"] + rows[1]])
    f = E((m, "x"), (b, ""))
    return M(pic + "¿Qué fórmula corresponde a esta tabla? (x = %s, y = %s)" % (sg(xs[0]), sg(m * xs[0] + b)), "y = %s" % f, ["y = %s" % E((m, "x"), (b + 1, "")), "y = %s" % E((m + 1, "x"), (b, "")), "y = %s" % E((b if b not in (0, m) else m + 2, "x"), (m, ""))],
             "Por cada unidad de x, y aumenta %d; para x = 0, y = %s: <b>y = %s</b>." % (m, sg(b), f))


seen = set()
sets = [("Leer gráficas", mix(R, seen, [(s_grafica, 20)])), ("Crecimiento y extremos", mix(R, seen, [(s_grafica, 20)])), ("Puntos de corte y dominio", mix(R, seen, [(s_cortes, 10), (s_dominio, 10)])),
        ("Continuidad, simetría y TVM", mix(R, seen, [(s_propiedades, 20)])), ("Funciones en contexto", mix(R, seen, [(s_contexto, 20)]))]
think = ["El <b>dominio</b> son los valores de x que tienen imagen; el <b>recorrido</b>, los valores de y que se alcanzan.",
         "Una función es <b>creciente</b> en un intervalo si al aumentar x aumenta y. Los intervalos se dan con valores de x.",
         "En un <b>máximo relativo</b> la gráfica pasa de subir a bajar; en un <b>mínimo relativo</b>, de bajar a subir.",
         "Corte con el eje X: f(x) = 0. Corte con el eje Y: x = 0.",
         "<b>Par</b>: f(−x) = f(x) (simétrica respecto al eje Y). <b>Impar</b>: f(−x) = −f(x) (simétrica respecto al origen).",
         "Tasa de variación media en [a, b]: (f(b) − f(a)) / (b − a)."]
ex = [("f(x) = x² − 5x + 6, cortes con el eje X", ["x² − 5x + 6 = 0", "x = 2, x = 3"], "(2, 0) y (3, 0)"), ("Dominio de √(x − 2)", ["x − 2 ≥ 0"], "[2, +∞)")]
mist = [["Dar el crecimiento con valores de y", "Los intervalos de crecimiento son de x."], ["Confundir dominio y recorrido", "Dominio: eje X. Recorrido: eje Y."], ["Llamar máximo absoluto a cualquier máximo", "El absoluto es el más alto de todos."]]
xs0, ys0 = [-4, -1, 2, 5], [-2, 3, -1, 2]
body = L(think, ex, mist, pic_of(xs0, ys0))
faq = [("¿Qué diferencia hay entre máximo relativo y absoluto?", "El relativo es más alto que los puntos cercanos; el absoluto es el valor más alto de toda la función."),
       ("¿Para qué sirve la tasa de variación media?", "Mide cuánto cambia y, por término medio, por cada unidad de x: es como la velocidad media.")]
unit(3, R, "funciones-y-sus-propiedades", "A", "Funciones: formas de representación; dominio y recorrido; continuidad; puntos de corte; crecimiento y decrecimiento; máximos y mínimos; simetrías y periodicidad; tasa de variación media",
     "Funciones y sus propiedades", "Propiedades de funciones", "Fichas de matemáticas de 3.º de ESO: dominio, recorrido, cortes con los ejes, crecimiento, máximos y mínimos, continuidad, simetría y TVM. 100 ejercicios con soluciones.",
     "Dominio: valores de x", "Recorrido: valores de y que alcanza.", body, faq, sets, 7)
