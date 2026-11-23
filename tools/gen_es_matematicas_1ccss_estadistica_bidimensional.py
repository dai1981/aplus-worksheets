# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales I (1.º de Bachillerato): Estadística bidimensional (Sentido estocástico)
Medias y desviaciones típicas, nube de puntos, covarianza, coeficiente de correlación de Pearson, recta de regresión, estimaciones y su fiabilidad.
Reutiliza los generadores de Matemáticas I con otra semilla y añade datos de ciencias sociales (horas de estudio y notas, renta y gasto, publicidad y ventas).
Errores: confundir correlación con causalidad, estimar muy fuera del rango de los datos.
"""
import random
from es_ccss import M, mix, unit, L, use_, tabla, r2, W, num

R = random.Random(53008)
EB = "gen_es_matematicas_1bach_estadistica_bidimensional"
s_medias, s_covarianza, s_correlacion, s_regresion = use_(EB, 53208, "s_medias", "s_covarianza", "s_correlacion", "s_regresion")

CASOS = [("horas de estudio semanales", "nota del examen"), ("gasto en publicidad (miles de €)", "ventas (miles de €)"), ("renta familiar (miles de €)", "gasto en ocio (cientos de €)"),
         ("años de experiencia", "salario (miles de €)"), ("temperatura máxima (°C)", "helados vendidos (decenas)"), ("precio (€)", "unidades vendidas (cientos)")]


def s_contexto():
    t = R.choice(["signo", "signo", "estimar", "fiable", "causa"])
    a, b = R.choice(CASOS)
    if t == "signo":
        inv = "precio" in a
        ok = "negativa: al subir el precio se venden menos unidades" if inv else "positiva: cuando una crece, la otra tiende a crecer"
        return M("Se estudian x = %s e y = %s en un grupo de datos. ¿Qué correlación es de esperar?" % (a, b), ok,
                 ["positiva: cuando una crece, la otra tiende a crecer" if inv else "negativa: al crecer una, la otra baja", "nula: no tienen relación", "exacta: r = 1"],
                 "Respuesta: <b>%s</b>." % ok)
    if t == "estimar":
        m, n = R.choice([(0.5, 2), (1.2, 3), (2, 5), (0.8, 1.5), (1.5, 4)])
        x0 = R.randint(3, 9)
        v = m * x0 + n
        return M("Para x = %s e y = %s, la recta de regresión es y = %sx + %s (r = %s). Estima y para x = %d." % (a, b, r2(m), r2(n), r2(R.choice([0.86, 0.91, 0.94])), x0), r2(v),
                 W([r2(m * x0), r2((x0 - n) / m), r2(v + m), r2(n * x0 + m)]), "y = %s · %d + %s = <b>%s</b>. Como |r| está cerca de 1, la estimación es fiable." % (r2(m), x0, r2(n), r2(v)))
    if t == "fiable":
        r = R.choice([0.12, -0.15, 0.35, 0.93, -0.9, 0.97])
        ok = "sí, porque |r| está cerca de 1" if abs(r) > 0.8 else "no, porque la correlación es débil"
        return M("Entre x = %s e y = %s se obtiene r = %s. ¿Es fiable estimar y con la recta de regresión (dentro del rango de los datos)?" % (a, b, r2(r)), ok,
                 ["no, porque la correlación es débil" if abs(r) > 0.8 else "sí, porque |r| está cerca de 1", "sí, siempre", "solo si r es positivo"], "Respuesta: <b>%s</b>." % ok)
    ok = "no necesariamente: correlación no implica causalidad"
    return M("Hay una correlación alta entre x = %s e y = %s. ¿Se puede afirmar que x es la causa de y?" % (a, b), ok,
             ["sí, siempre que r &gt; 0,8", "sí, porque la covarianza es positiva", "solo si r = 1"], "Puede haber un tercer factor o ser casualidad: <b>%s</b>." % ok)


seen = set()
sets = [("Medias y desviación típica", mix(R, seen, [(s_medias, 20)])), ("Covarianza", mix(R, seen, [(s_covarianza, 20)])), ("Coeficiente de correlación", mix(R, seen, [(s_correlacion, 20)])),
        ("Recta de regresión", mix(R, seen, [(s_regresion, 20)])), ("Interpretar datos sociales", mix(R, seen, [(s_contexto, 20)]))]
think = ["Una <b>variable bidimensional</b> (x, y) se representa con una <b>nube de puntos</b>. Su centro de gravedad es (x̄, ȳ).",
         "<b>Covarianza</b>: σ<sub>xy</sub> = Σxy/n − x̄ · ȳ. Positiva: relación directa; negativa: inversa.",
         "<b>Coeficiente de correlación</b>: r = σ<sub>xy</sub>/(σ<sub>x</sub>σ<sub>y</sub>), entre −1 y 1. Cerca de ±1, la relación lineal es fuerte.",
         "<b>Recta de regresión</b> de y sobre x: y − ȳ = (σ<sub>xy</sub>/σ<sub>x</sub>²)(x − x̄). Sirve para estimar, solo dentro del rango de los datos y si |r| es alto."]
ex = [("Horas de estudio y nota: x̄ = 5, ȳ = 6, σ<sub>xy</sub> = 3, σ<sub>x</sub>² = 4", ["m = 3/4 = 0,75", "y − 6 = 0,75(x − 5)"], "y = 0,75x + 2,25")]
mist = [["Correlación = causalidad", "Dos variables pueden ir juntas por un tercer factor."], ["Estimar muy lejos de los datos", "La recta solo es fiable dentro del rango."], ["Fiarse de r pequeño", "Si |r| es bajo, la estimación no vale."]]
body = L(think, ex, mist, tabla(["x: horas de estudio", "2", "4", "5", "7", "8"], [["y: nota", "4", "5", "6", "7", "9"]]))
faq = [("¿Qué mide el coeficiente de correlación?", "La fuerza y el sentido de la relación lineal entre dos variables: −1 (inversa perfecta), 0 (sin relación lineal), 1 (directa perfecta)."),
       ("¿Cuándo es fiable una estimación?", "Cuando |r| está cerca de 1 y el valor de x está dentro del rango de los datos observados.")]
unit(1, R, "estadistica-bidimensional", "S", "Estadística bidimensional: nube de puntos, covarianza, coeficiente de correlación, recta de regresión y estimaciones con datos sociales y económicos",
     "Estadística bidimensional", "Estadística bidimensional", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales I: covarianza, correlación, recta de regresión y estimaciones con datos sociales. 100 ejercicios.",
     "r cerca de ±1: relación fuerte", "Correlación no implica causalidad.", body, faq, sets, 8)
