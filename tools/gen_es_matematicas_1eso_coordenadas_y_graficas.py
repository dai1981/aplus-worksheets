# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Coordenadas y gráficas (Sentido algebraico)
Coordenadas en los cuatro cuadrantes, tablas de valores, gráficas de relaciones de proporcionalidad directa (y = kx), leer e interpretar gráficas en contexto.
Reutiliza las coordenadas de 6.º de Primaria (leer puntos, cuadrantes) con otra semilla.
Errores: cambiar el orden (x, y), leer mal la escala de un eje, pensar que un tramo horizontal significa que se mueve.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, sg, num, E, unit, L, Kids, kosy, kurve, tabla, use_, nz

R = random.Random(47009)
K = Kids(R)
leer, cuad = use_("gen_es_matematicas_6_coordenadas_y_movimientos", 47914, "s1_leer", "s2_cuadrante")
BLUE = "#1565c0"


def s_tabla():
    k = nz(R, -4, 4)
    b = R.randint(-5, 5) if R.random() < 0.5 else 0
    xs = sorted(R.sample(range(-3, 6), 4))
    i = R.randrange(4)
    ys = [k * x + b for x in xs]
    row = [sg(y) if j != i else "?" for j, y in enumerate(ys)]
    t = R.choice(["hueco", "expr"])
    pic = tabla(["x"] + [sg(x) for x in xs], [["y"] + row])
    if t == "hueco":
        return M(pic + "La tabla sigue la regla y = %s. ¿Qué número va en «?»?" % E((k, "x"), (b, "")), sg(ys[i]), [sg(-ys[i]) if ys[i] else "1", sg(ys[i] + k), sg(k * xs[i] - b) if b else sg(ys[i] + 1)],
                 "y = %s · %s %s = <b>%s</b>." % (sg(k), "(%s)" % sg(xs[i]) if xs[i] < 0 else sg(xs[i]), ("+ %d" % b if b > 0 else "− %d" % -b) if b else "", sg(ys[i])))
    pic = tabla(["x"] + [sg(x) for x in xs], [["y"] + [sg(y) for y in ys]])
    ok = "y = %s" % E((k, "x"), (b, ""))
    return M(pic + "¿Qué regla relaciona x e y?", ok, ["y = %s" % E((k, "x"), (-b, "")) if b else "y = %s" % E((k, "x"), (k, "")), "y = %s" % E((-k, "x"), (b, "")), "y = %s" % E((1, "x"), (ys[0] - xs[0], "")) if k != 1 else "y = %s" % E((2, "x"), (b, ""))],
             "Comprobamos con cada par de la tabla: <b>%s</b>." % ok)


def s_recta():
    k = R.choice([F(1), F(2), F(3), F(-1), F(-2), F(1, 2), F(-1, 2), F(3, 2)])
    t = R.choice(["cual", "pasa"])
    if t == "cual":
        ok = "y = %s" % E((k, "x"))
        pic = kosy(lines=[(k, 0, BLUE, "")], lo=-5, hi=5)
        return M(pic + "¿Qué expresión corresponde a la recta dibujada?", ok, ["y = %s" % E((-k, "x")), "y = %s" % E((1 / k, "x")) if abs(k) != 1 else "y = %s" % E((2 * k, "x")), "y = %s" % E((1, "x"), (k, "")) if k != 1 else "y = x + 2"],
                 "Pasa por el origen y por (1, %s): <b>%s</b>." % (d(k) if k.denominator == 1 else d(k), ok))
    x = R.choice([2, 4, -2, -4, 6, -6, 8, 3, -3, 5])
    y = k * x
    if y.denominator != 1:
        return None
    ok = "(%s, %s)" % (sg(x), sg(int(y)))
    return M("¿Qué punto de la recta y = %s tiene x = %s?" % (E((k, "x")), sg(x)), ok, ["(%s, %s)" % (sg(int(y)), sg(x)) if int(y) != x else "(%s, %s)" % (sg(x), sg(int(y) + 1)), "(%s, %s)" % (sg(x), sg(-int(y))) if y else "(%s, 1)" % sg(x), "(%s, %s)" % (sg(x + 1), sg(int(y)))],
             "Para x = %s, y = %s · %s = %s: <b>%s</b>." % (sg(x), d(k), "(%s)" % sg(x) if x < 0 else sg(x), sg(int(y)), ok))


def paseo():
    """gráfica distancia–tiempo a trozos"""
    t1 = R.choice([10, 15, 20])
    d1 = R.choice([400, 600, 800, 1000, 1200])
    t2 = t1 + R.choice([10, 15, 20])
    t3 = t2 + R.choice([10, 15, 20, 25])
    pts = [(0, 0), (t1, d1), (t2, d1), (t3, 0)]

    def f(x):
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            if xa <= x <= xb:
                return ya + (yb - ya) * (x - xa) / float(xb - xa)
        return None
    pic = kurve([(f, BLUE, "")], (0, t3, 5 if t3 <= 50 else 10), (0, 1400, 200), label="gráfica distancia al tiempo", W=360, H=250)
    return pic, t1, d1, t2, t3


def s_interpretar():
    pic, t1, d1, t2, t3 = paseo()
    p = K.next()
    t = R.choice(["max", "parada", "vuelta", "en"])
    pre = pic + "La gráfica muestra la distancia (en metros) a la que está %s de su casa durante un paseo (tiempo en minutos). " % p[0]
    if t == "max":
        return M(pre + "¿A qué distancia máxima de casa llegó?", "%s m" % num(d1), ["%s m" % num(d1 * 2), "%d m" % t1, "%s m" % num(d1 - 200)], "El punto más alto de la gráfica está a <b>%s m</b>." % num(d1))
    if t == "parada":
        return M(pre + "¿Cuántos minutos estuvo parad%s?" % ("a" if p[1] == "ella" else "o"), "%d min" % (t2 - t1), ["%d min" % t1, "%d min" % t2, "%d min" % (t3 - t2)], "En el tramo horizontal la distancia no cambia: de %d a %d min, <b>%d min</b>." % (t1, t2, t2 - t1))
    if t == "vuelta":
        return M(pre + "¿Cuánto tardó en volver a casa?", "%d min" % (t3 - t2), ["%d min" % t3, "%d min" % t1, "%d min" % (t2 - t1)] if t3 - t2 != t1 else ["%d min" % t3, "%d min" % (t1 + 5), "%d min" % (t2 - t1 + 1)],
                 "La vuelta va de %d a %d min: <b>%d min</b>." % (t2, t3, t3 - t2))
    x = t1 // 2 if t1 % 2 == 0 else t1
    y = d1 * x // t1
    return M(pre + "¿A qué distancia estaba a los %d minutos?" % x, "%s m" % num(y), ["%s m" % num(d1), "%d m" % x, "%s m" % num(y + 200)], "A los %d min la gráfica marca <b>%s m</b>." % (x, num(y)))


def s_funcion():
    q, a, w = R.choice([("Un taxi cobra 3 € al subir y 1 € por kilómetro. ¿Qué expresión da el precio y para x km?", "y = x + 3", ["y = 3x + 1", "y = 3x", "y = x − 3"]),
                        ("Un kilo de tomates cuesta 2 €. ¿Qué expresión da el precio y de x kilos?", "y = 2x", ["y = x + 2", "y = x/2", "y = 2"]),
                        ("Un depósito tiene 50 L y pierde 2 L cada hora. ¿Qué expresión da los litros y después de x horas?", "y = 50 − 2x", ["y = 2x − 50", "y = 50 + 2x", "y = 48x"]),
                        ("Cada entrada cuesta 6 € y hay 2 € de gastos de gestión por la compra. ¿Qué expresión da el precio y de x entradas?", "y = 6x + 2", ["y = 8x", "y = 2x + 6", "y = 6 + x"]),
                        ("¿Cuál de estas relaciones es de proporcionalidad directa?", "y = 4x", ["y = x + 4", "y = 4", "y = 4 − x"]),
                        ("La gráfica de una proporcionalidad directa es una recta que…", "pasa por el origen (0, 0)", ["es horizontal", "no corta los ejes", "pasa por (0, 1)"]),
                        ("En una gráfica distancia–tiempo, un tramo horizontal significa que…", "está parado", ["va muy rápido", "vuelve a casa", "sube una cuesta"]),
                        ("En una gráfica distancia–tiempo, el tramo más empinado es…", "el de mayor velocidad", ["el más lento", "una parada", "el más largo"]),
                        ("¿En qué eje se pone normalmente la variable independiente?", "en el eje horizontal (x)", ["en el eje vertical (y)", "en los dos", "en ninguno"]),
                        ("Si el punto (a, b) está en el tercer cuadrante, entonces…", "a &lt; 0 y b &lt; 0", ["a &gt; 0 y b &lt; 0", "a &lt; 0 y b &gt; 0", "a &gt; 0 y b &gt; 0"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Coordenadas de puntos", mix(R, seen, [(leer, 14), (cuad, 6)])), ("Tablas de valores", mix(R, seen, [(s_tabla, 20)])), ("Rectas y proporcionalidad", mix(R, seen, [(s_recta, 20)])),
        ("Interpretar gráficas", mix(R, seen, [(s_interpretar, 20)])), ("Relaciones en contexto", mix(R, seen, [(s_funcion, 10), (s_interpretar, 10)]))]
body = L(["Un punto tiene dos coordenadas (x, y): primero el eje horizontal y después el vertical.",
          "Con una regla como y = 2x + 1 se hace una <b>tabla de valores</b> y se dibujan los puntos.",
          "Si y = kx, las magnitudes son directamente proporcionales y la gráfica es una recta que pasa por (0, 0).",
          "En una gráfica en contexto, lee siempre qué representa cada eje y su escala."],
         [("Tabla de y = 2x − 1", ["x = 0 → y = −1", "x = 1 → y = 1", "x = 2 → y = 3"], "(0, −1), (1, 1), (2, 3)")],
         [["Cambiar el orden de las coordenadas", "(2, 5) no es lo mismo que (5, 2)."], ["Leer mal la escala", "Mira cuánto vale cada cuadrito del eje."], ["Pensar que un tramo horizontal es movimiento", "Si la distancia no cambia, está parado."]],
         kosy(lines=[(2, -1, BLUE, "")], pts=[(0, -1, ""), (1, 1, ""), (2, 3, "")], lo=-4, hi=4))
faq = [("¿Cómo se sabe en qué cuadrante está un punto?", "Por los signos: (+, +) primero, (−, +) segundo, (−, −) tercero y (+, −) cuarto."),
       ("¿Cómo es la gráfica de y = kx?", "Una recta que pasa por el origen. Si k es positivo, sube; si es negativo, baja.")]
unit(1, R, "coordenadas-y-graficas", "A", "Coordenadas cartesianas; tablas de valores; relaciones de proporcionalidad directa y su gráfica; interpretación de gráficas en contextos cotidianos",
     "Coordenadas, tablas y gráficas", "Coordenadas y gráficas",
     "Fichas de matemáticas de 1.º de ESO: coordenadas en los cuatro cuadrantes, tablas de valores, rectas y = kx e interpretar gráficas. 100 ejercicios con soluciones.",
     "(x, y): primero horizontal", "Después el eje vertical.", body, faq, sets, 9)
