# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 3): postulados de Euclides, el quinto postulado y geometrías no euclidianas (esférica)."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130103))
par = src("gen_es_matematicas_1eso_rectas_y_angulos", 130303, "s_paralelas", lv=1)
unit("geometria-euclidiana-y-no-euclidiana", 3, ("Geometría y trigonometría", 3, "Geometría euclidiana y no euclidiana"),
     "Reconoce los postulados de Euclides, el papel del quinto postulado y ejemplos de geometrías no euclidianas como la geometría esférica",
     "Euclides y la geometría de la esfera", "Geometrías no euclidianas",
     "Ejercicios de Temas Selectos de Matemáticas I: postulados de Euclides, ángulos entre paralelas, suma de ángulos de polígonos, triángulos esféricos y exceso esférico. 100 ejercicios con respuestas.",
     "En el plano los ángulos suman 180°", "En la esfera, más de 180°.",
     ["La geometría de <b>Euclides</b> parte de cinco postulados. El <b>quinto</b> (de las paralelas) dice que por un punto exterior a una recta pasa una sola paralela.",
      "De él salen los ángulos entre paralelas y que los ángulos de un triángulo suman 180°.",
      "En la <b>esfera</b> las «rectas» son círculos máximos, no hay paralelas y los ángulos de un triángulo suman más de 180°. La diferencia es el <b>exceso esférico</b>."],
     [("Triángulo esférico con ángulos 90°, 90° y 90°", ["Suma 270°", "Exceso 270° − 180°"], "90°")],
     [["Pensar que la geometría de Euclides es la única posible", "Cambiando el quinto postulado salen otras geometrías válidas."], ["Usar 180° en la esfera", "Allí la suma es mayor."], ["Confundir paralelos de latitud con «rectas» de la esfera", "Solo el ecuador es un círculo máximo."]],
     [("¿Cuál geometría es la «verdadera»?", "Depende del espacio: en un papel funciona la de Euclides; sobre la Tierra o en el universo a gran escala, otras."), ("¿Para qué sirve la geometría esférica?", "Para navegación, rutas de aviones y astronomía.")],
     [("Postulados de Euclides", [(lambda: S.t3("postulado"), 7), (lambda: S.t3("suma"), 8), (lambda: S.t3("paralelas"), 5)]), ("Rectas paralelas", [(lambda: S.t3("paralelas"), 12), (par, 8)]),
      ("Triángulos esféricos", [(lambda: S.t3("exceso"), 20)]), ("Áreas en la esfera", [(lambda: S.t3("esfera"), 20)]),
      ("Repaso", [(lambda: S.t3("exceso"), 10), (lambda: S.t3("paralelas"), 10)])],
     130003, lv=13)
