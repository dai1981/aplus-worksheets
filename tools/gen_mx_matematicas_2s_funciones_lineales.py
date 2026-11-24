# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Funciones lineales: pendiente, ordenada al origen y gráficas."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68110))
MB = [("mx + n", "mx + b"), (" y n ", " y b ")]
con, pen, ecu = src("gen_es_matematicas_2eso_funciones", 68381, "s_concepto", "s_pend", "s_ecuacion", lv=2, rep=MB)
rec = src("gen_es_matematicas_1eso_coordenadas_y_graficas", 68382, "s_recta", lv=1)
unit("funciones-lineales", 10, "6FU",
     "Modela y resuelve situaciones con relaciones lineales y de proporcionalidad de constante positiva y negativa; interpreta la pendiente y la ordenada al origen",
     "Funciones lineales: y = mx + b", "Funciones lineales",
     "Ejercicios de matemáticas de 2.º grado de secundaria: función lineal y = mx + b, pendiente, ordenada al origen, gráficas, tablas y ecuación de la recta. 100 ejercicios con respuestas.",
     "m: inclinación; b: corte con y", "Si m &lt; 0, la recta baja.",
     ["Una <b>función lineal</b> se escribe y = mx + b y su gráfica es una recta.",
      "La <b>pendiente</b> m dice cuánto cambia y cuando x aumenta 1: si m &gt; 0 la recta sube; si m &lt; 0, baja. Se calcula con dos puntos: m = (y₂ − y₁) ÷ (x₂ − x₁).",
      "La <b>ordenada al origen</b> b es donde la recta corta el eje y. Si b = 0, la recta pasa por el origen y es de proporcionalidad directa."],
     [("Recta por (0, 3) y (2, 7)", ["m = (7 − 3) ÷ 2 = 2", "b = 3"], "y = 2x + 3"), ("y = −3x + 5 con x = 2", ["−6 + 5"], "−1")],
     [["Invertir la fórmula de la pendiente", "Es cambio en y entre cambio en x."], ["Confundir m y b", "En y = 4x − 1, m = 4 y b = −1."], ["Olvidar el signo de la pendiente", "Una recta que baja tiene m negativa."]],
     [("¿Qué representa la pendiente en un problema?", "Una razón de cambio: pesos por kilo, kilómetros por hora, litros por minuto."), ("¿Toda recta es una función?", "Todas, menos las verticales.")],
     [("Conceptos", [(con, 8), (pen, 12)]), ("Pendiente y valores", [(pen, 20)]), ("Ecuación de la recta", [(ecu, 20)]), ("Gráficas", [(rec, 20)]), ("Constante negativa", [(lambda: S.prop_inv("neg"), 20)])],
     68010, lv=8)
