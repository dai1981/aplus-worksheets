# -*- coding: utf-8 -*-
"""
España Matemáticas I (1.º de Bachillerato): Estadística bidimensional (Sentido estocástico)
Medias y desviaciones típicas, nube de puntos, covarianza, coeficiente de correlación de Pearson, recta de regresión de y sobre x, estimaciones y su fiabilidad.
Errores: confundir correlación con causalidad, usar la recta para estimar muy fuera de los datos, signo de r distinto del de la covarianza (imposible).
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, nf, r2, tabla, W, MINUS, E
from ws_common import text, line
from de_common import wrap

R = random.Random(51014)


def datos():
    while True:
        n = 5
        xs = sorted(R.sample(range(1, 11), n))
        m = R.choice([1, 2, -1, 3, F(1, 2)])
        b = R.randint(-3, 8)
        ys = [int(m * x + b + R.choice([-2, -1, 0, 1, 2])) for x in xs]
        if len(set(ys)) < 4:
            continue
        mx, my = F(sum(xs), n), F(sum(ys), n)
        if mx.denominator > 1 or my.denominator > 1:
            continue
        sxy = F(sum(x * y for x, y in zip(xs, ys)), n) - mx * my
        if sxy == 0:
            continue
        return xs, ys, mx, my, sxy


def stats(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum(x * x for x in xs) / n - mx * mx)
    sy = math.sqrt(sum(y * y for y in ys) / n - my * my)
    sxy = sum(x * y for x, y in zip(xs, ys)) / n - mx * my
    return mx, my, sx, sy, sxy, sxy / (sx * sy)


def tab(xs, ys):
    return tabla(["x"] + [str(x) for x in xs], [["y"] + [sg(y) for y in ys]])


def nube(xs, ys):
    W_, H_ = 300, 220
    lo, hi = min(ys + [0]), max(ys)
    X = lambda x: 40 + x * 24
    Y = lambda y: 190 - (y - lo) * 160 / max(1, hi - lo)
    s = [line(40, 190, 285, 190, "#263238", 2), line(40, 190, 40, 20, "#263238", 2), text(288, 194, "x", 14, italic=True), text(36, 18, "y", 14, italic=True)]
    for x in range(0, 11, 2):
        s.append(text(X(x), 206, str(x), 11))
    s += ["<circle cx='%.1f' cy='%.1f' r='4.5' fill='#1565c0'/>" % (X(x), Y(y)) for x, y in zip(xs, ys)]
    return wrap(W_, H_, "".join(s), "nube de puntos", lg=True)


def s_medias():
    xs, ys, mx, my, sxy = datos()
    t = R.choice(["mx", "my", "sx", "centro"])
    T = tab(xs, ys)
    if t == "mx":
        return M(T + "Calcula la media de x.", nf(mx), W([nf(my), nf(mx + 1), nf(F(sum(xs), 4)), nf(F(max(xs) + min(xs), 2)) if F(max(xs) + min(xs), 2) != mx else nf(mx - 1)]), "x̄ = %d/5 = <b>%s</b>." % (sum(xs), nf(mx)))
    if t == "my":
        return M(T + "Calcula la media de y.", nf(my), W([nf(mx), nf(my + 1), nf(F(sum(ys), 4)), nf(my - 2)]), "ȳ = %d/5 = <b>%s</b>." % (sum(ys), nf(my)))
    if t == "sx":
        s = stats(xs, ys)[2]
        v = sum(x * x for x in xs) / 5 - float(mx) ** 2
        return M(T + "Calcula la desviación típica de x (a las centésimas).", r2(s), W([r2(v), r2(s * math.sqrt(5 / 4)), r2(s / 2), r2(s + 1)]), "σ<sub>x</sub> = √(Σx²/n − x̄²) = √%s ≈ <b>%s</b>." % (r2(v), r2(s)))
    return M(T + "¿Cuál es el centro de gravedad de la nube de puntos?", "(%s, %s)" % (nf(mx), nf(my)), W(["(%s, %s)" % (nf(my), nf(mx)), "(%s, %s)" % (nf(mx), nf(my + 1)), "(%s, %s)" % (nf(F(max(xs) + min(xs), 2)), nf(F(max(ys) + min(ys), 2)))]), "Es el punto (x̄, ȳ) = <b>(%s, %s)</b>." % (nf(mx), nf(my)))


def s_covarianza():
    xs, ys, mx, my, sxy = datos()
    T = tab(xs, ys)
    sxy_f = float(sxy)
    t = R.choice(["cov", "cov", "signo"])
    if t == "cov":
        return M(T + "Calcula la covarianza σ<sub>xy</sub> (a las centésimas).", r2(sxy_f), W([r2(-sxy_f), r2(sum(x * y for x, y in zip(xs, ys)) / 5), r2(sxy_f * 5 / 4), r2(sxy_f / 2)]),
                 "σ<sub>xy</sub> = Σxy/n − x̄ · ȳ = %s − %s · %s = <b>%s</b>." % (r2(sum(x * y for x, y in zip(xs, ys)) / 5), nf(mx), nf(my), r2(sxy_f)))
    ok = "positiva (relación directa)" if sxy > 0 else "negativa (relación inversa)"
    return M(T + "¿Qué signo tiene la covarianza?", ok, [o for o in ["positiva (relación directa)", "negativa (relación inversa)", "cero", "no se puede saber"] if o != ok], "Cuando x crece, y tiende a %s: <b>%s</b>." % ("crecer" if sxy > 0 else "decrecer", ok))


def s_correlacion():
    t = R.choice(["calc", "calc", "interp", "nube", "teo"])
    if t == "calc":
        xs, ys, mx, my, sxy = datos()
        mx_, my_, sx, sy, sxy_, r = stats(xs, ys)
        return M(tab(xs, ys) + "Calcula el coeficiente de correlación r (a las centésimas).", r2(r), W([r2(-r), r2(sxy_), r2(r * r), r2(min(0.99, abs(r) + 0.2) * (1 if r > 0 else -1))]),
                 "r = σ<sub>xy</sub> / (σ<sub>x</sub> · σ<sub>y</sub>) = %s / (%s · %s) ≈ <b>%s</b>." % (r2(sxy_), r2(sx), r2(sy), r2(r)))
    if t == "interp":
        r = R.choice([0.95, 0.88, -0.92, -0.85, 0.12, -0.08, 0.55, -0.6])
        ok = ("fuerte y directa" if r > 0.8 else "fuerte e inversa" if r < -0.8 else "muy débil (casi no hay relación lineal)" if abs(r) < 0.3 else "débil o moderada")
        rs = "%s" % r2(r)
        return M("Si r = %s, ¿cómo es la correlación?" % rs, ok, [o for o in ["fuerte y directa", "fuerte e inversa", "muy débil (casi no hay relación lineal)", "débil o moderada"] if o != ok], "|r| cerca de 1: fuerte; cerca de 0: débil. El signo indica si es directa o inversa: <b>%s</b>." % ok)
    if t == "nube":
        xs, ys, mx, my, sxy = datos()
        r = stats(xs, ys)[5]
        ok = "positiva" if r > 0 else "negativa"
        return M(nube(xs, ys) + "¿Qué tipo de correlación muestra esta nube de puntos? (x = %d … %d)" % (xs[0], xs[-1]), ok, ["positiva" if r < 0 else "negativa", "nula", "funcional (exacta)"], "Los puntos %s hacia la derecha: <b>%s</b>." % ("suben" if r > 0 else "bajan", ok))
    q, a, w = R.choice([("¿Entre qué valores está siempre r?", "entre −1 y 1", ["entre 0 y 1", "entre −∞ y +∞", "entre 0 y 100"]),
                        ("Si r = 1, los puntos…", "están todos sobre una recta creciente", ["están muy dispersos", "forman una parábola", "están sobre una recta decreciente"]),
                        ("Hay una correlación fuerte entre las ventas de helados y los ahogamientos en verano. ¿Significa que los helados causan ahogamientos?", "no: correlación no implica causalidad (los dos dependen del calor)", ["sí, claramente", "solo si r = 1", "sí, si r &gt; 0,9"]),
                        ("Si la covarianza es negativa, r es…", "negativo", ["positivo", "cero", "mayor que 1"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def rl(m, n):
    return "y = %sx" % r2(m) + ("" if r2(abs(n)) == "0" else " %s %s" % ("+" if n >= 0 else "−", r2(abs(n))))


def s_regresion():
    t = R.choice(["recta", "recta", "estima", "estima", "fiable"])
    if t in ("recta", "estima"):
        xs, ys, mx, my, sxy = datos()
        mx_, my_, sx, sy, sxy_, r = stats(xs, ys)
        m = sxy_ / sx ** 2
        n = my_ - m * mx_
        if t == "recta":
            ok = rl(m, n)
            return M(tab(xs, ys) + "Halla la recta de regresión de y sobre x (coeficientes a las centésimas).", ok, W([rl(sy * sy / sxy_, n), rl(m, -n) if r2(abs(n)) != "0" else rl(m, 1), rl(sxy_, my_ - sxy_ * mx_), rl(m * 5 / 4, n)]),
                     "m = σ<sub>xy</sub>/σ<sub>x</sub>² = %s; pasa por (x̄, ȳ) = (%s, %s): <b>%s</b>." % (r2(m), nf(mx), nf(my), ok))
        x0 = R.randint(4, 12)
        v = m * x0 + n
        return M(tab(xs, ys) + "La recta de regresión de y sobre x es %s. Estima y para x = %d." % (rl(m, n), x0), r2(v), W([r2(m * x0), r2(v + m), r2((x0 - n) / m) if m else r2(v + 1)]), "y = %s · %d%s ≈ <b>%s</b>." % (r2(m), x0, "" if r2(abs(n)) == "0" else " %s %s" % ("+" if n >= 0 else "−", r2(abs(n))), r2(v)))
    q, a, w = R.choice([("Una estimación con la recta de regresión es fiable cuando…", "|r| está cerca de 1 y x está dentro del rango de los datos", ["r está cerca de 0", "x es muy grande", "la covarianza es positiva"]),
                        ("¿Por qué punto pasa siempre la recta de regresión?", "por el centro de gravedad (x̄, ȳ)", ["por el origen", "por el primer dato", "por el punto (σ<sub>x</sub>, σ<sub>y</sub>)"]),
                        ("¿Qué signo tiene la pendiente de la recta de regresión si r &lt; 0?", "negativo", ["positivo", "cero", "depende de la media"]),
                        ("Con datos de alumnos de 12 a 16 años, ¿es fiable estimar la altura a los 40 años con la recta de regresión?", "no, está muy fuera del rango de los datos", ["sí, siempre", "sí, si r = 0,5", "solo si la pendiente es positiva"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


seen = set()
sets = [("Medias y desviación típica", mix(R, seen, [(s_medias, 20)])), ("Covarianza", mix(R, seen, [(s_covarianza, 20)])), ("Coeficiente de correlación", mix(R, seen, [(s_correlacion, 20)])),
        ("Recta de regresión", mix(R, seen, [(s_regresion, 20)])), ("Interpretar y estimar", mix(R, seen, [(s_correlacion, 10), (s_regresion, 10)]))]
think = ["Una <b>variable bidimensional</b> (x, y) se representa con una <b>nube de puntos</b>. Su centro de gravedad es (x̄, ȳ).",
         "<b>Covarianza</b>: σ<sub>xy</sub> = Σxy/n − x̄ · ȳ. Su signo indica si la relación es directa (+) o inversa (−).",
         "<b>Coeficiente de correlación</b>: r = σ<sub>xy</sub>/(σ<sub>x</sub>σ<sub>y</sub>), entre −1 y 1. Cuanto más cerca de ±1, más fuerte es la relación lineal.",
         "<b>Recta de regresión</b> de y sobre x: y − ȳ = (σ<sub>xy</sub>/σ<sub>x</sub>²)(x − x̄). Sirve para estimar y a partir de x."]
ex = [("x̄ = 4, ȳ = 10, σ<sub>xy</sub> = 6, σ<sub>x</sub>² = 2", ["m = 6/2 = 3", "y − 10 = 3(x − 4)"], "y = 3x − 2")]
mist = [["Correlación = causalidad", "Dos variables pueden ir juntas por un tercer factor."], ["Estimar muy lejos de los datos", "La recta solo es fiable dentro del rango."], ["r y covarianza con signos distintos", "Siempre tienen el mismo signo."]]
body = L(think, ex, mist, nube([1, 2, 4, 5, 7, 8], [2, 3, 5, 5, 8, 9]))
faq = [("¿Qué diferencia hay entre covarianza y correlación?", "La covarianza depende de las unidades; r no tiene unidades y siempre está entre −1 y 1, por eso permite comparar."),
       ("¿Qué es la recta de regresión?", "La recta que mejor se ajusta a la nube de puntos (minimiza los cuadrados de las distancias verticales).")]
unit(1, R, "estadistica-bidimensional", "S", "Estadística bidimensional: nube de puntos, covarianza, coeficiente de correlación lineal, recta de regresión y estimaciones",
     "Estadística bidimensional", "Estadística bidimensional", "Fichas de Matemáticas I (1.º de Bachillerato): nube de puntos, covarianza, correlación de Pearson, recta de regresión y estimaciones. 100 ejercicios con soluciones.",
     "r cerca de ±1: relación fuerte", "Correlación no implica causalidad.", body, faq, sets, 14)
