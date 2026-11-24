# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Números positivos y negativos: situaciones, recta numérica, orden, valor absoluto."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67101))
orden = src("gen_es_matematicas_1eso_numeros_enteros", 67311, "s_orden", lv=1)
vida, recta, comp = src("gen_es_matematicas_6_numeros_enteros", 67312, "s1_vida", "s2_recta", "s2_comparar", lv=6, extra=(nomoney, noplanta))

unit("numeros-con-signo", 1, "6PN",
     "Reconoce la necesidad de los números negativos a partir de usar cantidades que tienen al cero como referencia; los ubica en la recta numérica, los compara y los ordena; usa el valor absoluto y el simétrico (opuesto)",
     "Números positivos y negativos", "Números con signo",
     "Ejercicios de matemáticas de 1.er grado de secundaria: números positivos y negativos en situaciones reales, recta numérica, comparar y ordenar, valor absoluto y opuesto. 100 ejercicios con respuestas.",
     "El cero es el punto de referencia", "A la izquierda del 0 están los negativos.",
     ["Los <b>números negativos</b> sirven para cantidades por debajo de un punto de referencia (el 0): temperaturas bajo cero, deudas, pisos bajo tierra, años antes de Cristo.",
      "En la recta numérica, un número es <b>mayor</b> cuanto más a la derecha está. Por eso −2 &gt; −7.",
      "El <b>valor absoluto</b> |a| es la distancia de a al 0 (nunca es negativo). El <b>opuesto</b> o simétrico de a está a la misma distancia, del otro lado: el de −5 es 5."],
     [("Ordena: 3, −8, 0, −2", ["Los negativos van primero", "−8 está más a la izquierda que −2"], "−8 &lt; −2 &lt; 0 &lt; 3"), ("|−9|", ["Distancia de −9 al 0"], "9")],
     [["Pensar que −8 es mayor que −2", "Entre negativos, el mayor es el más cercano al 0: −2 &gt; −8."], ["Dar un valor absoluto negativo", "|−6| = 6. Una distancia no es negativa."], ["Confundir opuesto con inverso", "El opuesto de 4 es −4, no 1/4."]],
     [("¿Para qué sirven los números negativos?", "Para expresar cantidades menores que el punto de referencia: grados bajo cero, deudas, profundidades o pisos de estacionamiento."),
      ("¿El 0 es positivo o negativo?", "Ninguno de los dos: es el punto de referencia que separa positivos y negativos.")],
     [("Situaciones con números negativos", [(S.pn_context, 12), (vida, 8)]), ("La recta numérica", [(recta, 20)]), ("Comparar y ordenar", [(orden, 20)]),
      ("Valor absoluto y opuesto", [(comp, 12), (orden, 8)]), ("Problemas", [(S.pn_context, 20)])],
     67001, lv=7)
