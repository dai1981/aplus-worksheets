# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 8): variables categóricas, tablas de doble entrada, independencia y riesgo relativo."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100108))
cont = src("gen_es_matematicas_1ccss_probabilidad", 100318, "s_contingencia")
unit("tablas-de-doble-entrada", 8, ("Estadística", 8, "Variables categóricas y tablas de doble entrada"),
     "Analiza la relación entre dos variables categóricas con tablas de doble entrada, proporciones condicionales y riesgo relativo, y decide si son independientes",
     "Tablas de doble entrada y riesgo relativo", "Tablas de doble entrada",
     "Ejercicios de Pensamiento Matemático I: tablas de doble entrada, totales y proporciones, independencia de variables categóricas y riesgo relativo. 100 ejercicios con respuestas.",
     "Compara proporciones por fila", "Iguales: independientes. RR = riesgo ÷ riesgo.",
     ["Una <b>tabla de doble entrada</b> cruza dos variables categóricas. Los totales están en la última fila y columna.",
      "Para ver si hay relación, compara las <b>proporciones por fila</b>. Si son iguales, las variables son <b>independientes</b>.",
      "<b>Riesgo relativo</b>: RR = riesgo en el grupo expuesto ÷ riesgo en el no expuesto. RR = 1: no hay diferencia; RR = 2: el doble."],
     [("Fuman: 20 de 100 con tos. No fuman: 10 de 200 con tos.", ["0.2 ÷ 0.05"], "RR = 4")],
     [["Comparar números absolutos", "Compara proporciones: los grupos tienen distinto tamaño."], ["Dividir entre el total de la tabla", "El riesgo se calcula dentro de cada grupo."], ["Concluir causa", "Una relación en la tabla no prueba que una cause la otra."]],
     [("¿RR menor que 1 qué indica?", "Que el riesgo es menor en el grupo expuesto: el factor podría ser protector (por ejemplo, una vacuna)."),
      ("¿Independiente significa que no hay relación?", "Sí: saber el valor de una variable no cambia las proporciones de la otra.")],
     [("Leer la tabla", [(lambda: S.p8("marg"), 12), (cont, 8)]), ("Riesgo en cada grupo", [(lambda: S.p8("riesgo"), 20)]),
      ("Riesgo relativo", [(lambda: S.p8("rr"), 15), (lambda: S.p8("interp"), 5)]), ("¿Son independientes?", [(lambda: S.p8("indep"), 20)]),
      ("Probabilidades con tablas", [(cont, 12), (lambda: S.p8("rr"), 8)])],
     100008, lv=10)
