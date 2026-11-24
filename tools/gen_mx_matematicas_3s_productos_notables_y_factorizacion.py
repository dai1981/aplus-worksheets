# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Binomio al cuadrado, binomios conjugados, binomios con término común y factorización."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69103))
ide, fc = src("gen_es_matematicas_2eso_polinomios", 69321, "s_identidades", "s_factor_comun", lv=2, extra=(S.nocommute,))
fac = src("gen_es_matematicas_1eso_ecuaciones", 69322, "s_factor", lv=3, extra=(S.nocommute,))
unit("productos-notables-y-factorizacion", 3, "6IA",
     "Representa algebraicamente áreas que generan expresiones cuadráticas; usa productos notables y la factorización para transformar expresiones",
     "Productos notables y factorización", "Productos notables",
     "Ejercicios de matemáticas de 3.er grado de secundaria: binomio al cuadrado, binomios conjugados, binomios con término común, factor común y factorización de trinomios. 100 ejercicios con respuestas.",
     "(a + b)² = a² + 2ab + b²", "(a + b)(a − b) = a² − b²",
     ["<b>Binomio al cuadrado</b>: (a + b)² = a² + 2ab + b². No es a² + b²: falta el doble producto.",
      "<b>Binomios conjugados</b>: (a + b)(a − b) = a² − b² (diferencia de cuadrados). <b>Término común</b>: (x + m)(x + n) = x² + (m + n)x + mn.",
      "<b>Factorizar</b> es el proceso inverso: x² + 7x + 12 = (x + 3)(x + 4), porque 3 + 4 = 7 y 3 × 4 = 12."],
     [("(x + 5)²", ["x² + 2(5)x + 25"], "x² + 10x + 25"), ("x² − 49", ["diferencia de cuadrados"], "(x + 7)(x − 7)"), ("x² − x − 12", ["−4 + 3 = −1", "−4 × 3 = −12"], "(x − 4)(x + 3)")],
     [["(a + b)² = a² + b²", "Falta 2ab: (x + 3)² = x² + 6x + 9."], ["Signos en la diferencia de cuadrados", "x² − 9 = (x + 3)(x − 3)."], ["Buscar números que sumen el término independiente", "Deben multiplicar ese número y sumar el coeficiente de x."]],
     [("¿Para qué sirve factorizar?", "Para resolver ecuaciones cuadráticas y simplificar expresiones."), ("¿Todo trinomio se puede factorizar con enteros?", "No; a veces se necesita la fórmula general.")],
     [("Binomio al cuadrado y conjugados", [(ide, 20)]), ("Área de cuadrados y rectángulos", [(lambda: S.alg_figuras("cuad", "area"), 20)]), ("Factor común", [(fc, 20)]),
      ("Factorizar trinomios", [(fac, 20)]), ("Repaso", [(ide, 7), (fac, 7), (fc, 6)])],
     69003, lv=9)
