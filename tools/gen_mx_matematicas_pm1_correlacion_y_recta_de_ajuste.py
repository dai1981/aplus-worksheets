# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 9): relación entre variables cuantitativas, correlación y recta de ajuste."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100109))
cor, reg = src("gen_es_matematicas_1bach_estadistica_bidimensional", 100309, "s_correlacion", "s_regresion")
ctx = src("gen_es_matematicas_1ccss_estadistica_bidimensional", 100319, "s_contexto")
nube = src("gen_es_matematicas_1eso_estadistica", 100329, "s_correlacion", lv=4)
unit("correlacion-y-recta-de-ajuste", 9, ("Estadística", 9, "Correlación entre variables cuantitativas"),
     "Analiza la relación entre dos variables cuantitativas con diagramas de dispersión, el coeficiente de correlación y la recta de ajuste, e interpreta su pendiente para hacer estimaciones",
     "Correlación y recta de ajuste", "Correlación y recta de ajuste",
     "Ejercicios de Pensamiento Matemático I: diagramas de dispersión, tipo de correlación, coeficiente r, recta de regresión, interpretar la pendiente y hacer estimaciones. 100 ejercicios con respuestas.",
     "La pendiente es el cambio promedio", "r cerca de ±1: relación lineal fuerte.",
     ["En un <b>diagrama de dispersión</b> cada punto es una pareja (x, y). Si suben juntos, la correlación es positiva; si una baja, negativa.",
      "El <b>coeficiente de correlación</b> r va de −1 a 1. Cerca de ±1: fuerte; cerca de 0: no hay relación lineal.",
      "La <b>recta de ajuste</b> ŷ = a + bx sirve para estimar. La pendiente b es el cambio promedio de y por cada unidad de x."],
     [("ŷ = 50 + 4x (x = horas de estudio, y = calificación)", ["Pendiente 4: +4 puntos por hora", "x = 6: 50 + 24"], "ŷ = 74")],
     [["Pensar que correlación es causa", "Puede haber una variable de confusión."], ["Estimar muy lejos de los datos", "La recta vale cerca del rango observado."], ["Confundir r = −0.9 con relación débil", "El signo indica dirección; el valor, fuerza."]],
     [("¿Qué es la recta de mínimos cuadrados?", "La recta que hace más pequeña la suma de los cuadrados de las distancias verticales de los puntos a la recta."),
      ("¿r = 0 significa que no hay ninguna relación?", "Significa que no hay relación lineal; podría haber una relación curva.")],
     [("Diagramas de dispersión", [(nube, 10), (cor, 10)]), ("Tipo de correlación", [(lambda: S.p9("r"), 7), (lambda: S.p9("signo"), 6), (ctx, 7)]),
      ("Interpretar la pendiente", [(lambda: S.p9("pend"), 20)]), ("Estimar con la recta", [(lambda: S.p9("pred"), 20)]),
      ("Recta de regresión", [(reg, 20)])],
     100009, lv=10)
