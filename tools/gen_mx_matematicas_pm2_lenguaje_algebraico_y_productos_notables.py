# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 2): sintaxis algebraica: simplificar, desarrollar, productos notables y factorizar."""
import random
import mx_s2 as S2
from mx_common import src, unit

S2.setup(random.Random(110102))
mon, ope, ide, fac = src("gen_es_matematicas_2eso_polinomios", 110302, "s_monomios", "s_operar", "s_identidades", "s_factor_comun", lv=2,
                         rep=[("Saca factor común", "Factoriza sacando el factor común")], extra=(S2.nocommute,))
tri = src("gen_es_matematicas_1eso_ecuaciones", 110312, "s_factor", lv=3, extra=(S2.nocommute,))
unit("lenguaje-algebraico-y-productos-notables", 2, ("Lenguaje y álgebra", 2, "Sintaxis algebraica y productos notables"),
     "Elige la forma más útil de una expresión algebraica (simplificada, desarrollada o factorizada) usando operaciones con polinomios, productos notables y factorización",
     "Productos notables y factorización", "Productos notables",
     "Ejercicios de Pensamiento Matemático II: operaciones con monomios y polinomios, binomio al cuadrado, binomios conjugados, factor común y factorizar trinomios. 100 ejercicios con respuestas.",
     "(a + b)² = a² + 2ab + b²", "Factorizar es el camino de regreso.",
     ["Para <b>simplificar</b> se juntan términos semejantes. Para <b>desarrollar</b> se multiplica todo.",
      "<b>Productos notables</b>: (a + b)² = a² + 2ab + b²; (a − b)² = a² − 2ab + b²; (a + b)(a − b) = a² − b².",
      "<b>Factorizar</b> es escribir como producto: factor común, diferencia de cuadrados o trinomio cuadrado perfecto."],
     [("(x + 6)²", ["x² + 2 × 6 × x + 36"], "x² + 12x + 36"), ("Factoriza x² − 49", ["Diferencia de cuadrados"], "(x + 7)(x − 7)")],
     [["(a + b)² = a² + b²", "Falta el término 2ab."], ["Factorizar a medias", "Revisa que no quede un factor común."], ["Cambiar el signo al quitar paréntesis", "−(x − 3) = −x + 3."]],
     [("¿Para qué sirve factorizar?", "Para resolver ecuaciones (producto igual a 0), simplificar fracciones algebraicas y ver los ceros de una función."),
      ("¿Cuál forma es la mejor?", "Depende: la desarrollada sirve para sumar; la factorizada, para encontrar ceros.")],
     [("Monomios", [(mon, 20)]), ("Operaciones con polinomios", [(ope, 20)]), ("Productos notables", [(ide, 20)]),
      ("Factor común", [(fac, 20)]), ("Factorizar trinomios", [(tri, 20)])],
     110002, lv=11)
