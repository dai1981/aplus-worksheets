# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 3): equiprobabilidad, probabilidad teórica (regla de Laplace) y frecuencia relativa."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100103))
lap, suc = src("gen_es_matematicas_2bach_probabilidad", 100303, "s_laplace", "s_sucesos")
unit("probabilidad-teorica", 3, ("Probabilidad", 3, "Equiprobabilidad y probabilidad teórica"),
     "Usa la equiprobabilidad como hipótesis para calcular probabilidades teóricas con fracciones, decimales y porcentajes, y la compara con la frecuencia relativa de muchos ensayos",
     "Probabilidad teórica y equiprobabilidad", "Probabilidad teórica",
     "Ejercicios de Pensamiento Matemático I: regla de Laplace, dos dados, urnas, ruletas, complemento y comparación con la frecuencia relativa. 100 ejercicios con respuestas.",
     "P = favorables ÷ posibles", "Solo si todos son igual de probables.",
     ["Si todos los resultados son <b>igual de probables</b>: P(A) = casos favorables ÷ casos posibles.",
      "Con dos dados hay 6 × 6 = 36 resultados. En una ruleta, la probabilidad es el ángulo del sector ÷ 360°.",
      "El <b>complemento</b>: P(no A) = 1 − P(A)."],
     [("Suma 7 con dos dados", ["(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)", "6 de 36"], "1/6"), ("Ruleta: sector de 90°", ["90 ÷ 360"], "1/4")],
     [["Contar 11 sumas posibles como igual de probables", "Usa los 36 pares ordenados."], ["Usar Laplace con resultados no equiprobables", "Primero revisa el supuesto."], ["Olvidar el complemento", "«Al menos uno» suele ser 1 − ninguno."]],
     [("¿Cuándo no se puede usar la regla de Laplace?", "Cuando los resultados no tienen la misma probabilidad, como un dado cargado."),
      ("¿Qué pasa si comparo con un experimento real?", "Con muchos ensayos, la frecuencia relativa se acerca a la probabilidad teórica.")],
     [("Urnas y ruletas", [(lambda: S.p3("urna"), 12), (lambda: S.p3("ruleta"), 8)]), ("Dos dados", [(lambda: S.p3("dados"), 8), (lap, 12)]),
      ("Complemento y uniones", [(lambda: S.p3("comp"), 10), (suc, 10)]), ("¿Son equiprobables?", [(lambda: S.p3("equi"), 5), (lambda: S.p3("grandes"), 12), (lambda: S.p3("ruleta"), 3)]),
      ("Repaso", [(lap, 10), (suc, 6), (lambda: S.p3("urna"), 4)])],
     100003, lv=10)
