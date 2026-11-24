# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 4): análisis gráfico: simetrías, continuidad, crecimiento, máximos y mínimos y concavidad (intuitivo)."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120104))
gra, pro = src("gen_es_matematicas_3eso_funciones_propiedades", 120304, "s_grafica", "s_propiedades", lv=3)
tra = src("gen_es_matematicas_1bach_funciones", 120314, "s_transformacion")
unit("analisis-grafico-de-funciones", 4, ("Variación y funciones", 4, "Análisis gráfico de funciones"),
     "Analiza de forma intuitiva la gráfica de una función: simetrías, continuidad, intervalos de crecimiento y decrecimiento, máximos y mínimos relativos y concavidad",
     "Simetría, crecimiento y extremos", "Análisis gráfico",
     "Ejercicios de Pensamiento Matemático III: leer gráficas, funciones pares e impares, crecimiento, máximos y mínimos, concavidad y traslaciones. 100 ejercicios con respuestas.",
     "Sube, baja, se curva, se repite", "Lee la gráfica de izquierda a derecha.",
     ["Una función es <b>creciente</b> donde su gráfica sube de izquierda a derecha y <b>decreciente</b> donde baja. Donde cambia, hay un máximo o un mínimo relativo.",
      "<b>Par</b>: simétrica respecto al eje y (f(−x) = f(x)). <b>Impar</b>: simétrica respecto al origen (f(−x) = −f(x)).",
      "<b>Cóncava hacia arriba</b>: forma de U (la pendiente aumenta). <b>Hacia abajo</b>: forma de ∩."],
     [("f(x) = −(x − 2)² + 5", ["Parábola que abre hacia abajo", "Vértice (2, 5)"], "crece en (−∞, 2), máximo 5")],
     [["Leer el crecimiento con los valores de y", "Los intervalos se dan con valores de x."], ["Pensar que todo máximo es el mayor valor de la función", "Un máximo relativo es el mayor de su vecindad."], ["Confundir par con «tiene números pares»", "Mira las potencias de x y la simetría."]],
     [("¿Una función puede ser par e impar a la vez?", "Solo la función f(x) = 0."), ("¿Qué indica la concavidad?", "Si la razón de cambio aumenta (hacia arriba) o disminuye (hacia abajo).")],
     [("Leer gráficas", [(gra, 20)]), ("Simetrías", [(lambda: S.q4("paridad"), 14), (pro, 6)]), ("Crecimiento", [(lambda: S.q4("crece"), 14), (pro, 6)]),
      ("Máximos, mínimos y concavidad", [(lambda: S.q4("max"), 12), (lambda: S.q4("concav"), 8)]), ("Traslaciones", [(tra, 20)])],
     120004, lv=12)
