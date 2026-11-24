# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Ecuaciones cuadráticas por factorización y fórmula general."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69105))
inc, comp, dis, fac = src("gen_es_matematicas_1eso_ecuaciones", 69331, "s_incompleta", "s_completa", "s_discr", "s_factor", lv=3, extra=(S.nocommute,))
unit("ecuaciones-cuadraticas", 5, "6EC",
     "Resuelve ecuaciones cuadráticas de la forma Ax² + Bx + C = 0 por factorización y por la fórmula general",
     "Ecuaciones cuadráticas", "Ecuaciones cuadráticas",
     "Ejercicios de matemáticas de 3.er grado de secundaria: ecuaciones cuadráticas incompletas y completas, factorización, fórmula general y discriminante. 100 ejercicios con respuestas.",
     "x = (−b ± √(b² − 4ac)) ÷ 2a", "El discriminante dice cuántas soluciones hay.",
     ["Una ecuación <b>cuadrática</b> tiene la forma ax² + bx + c = 0 y puede tener dos, una o ninguna solución real.",
      "<b>Por factorización</b>: si x² − 5x + 6 = 0, entonces (x − 2)(x − 3) = 0 y x = 2 o x = 3 (si un producto es 0, algún factor es 0).",
      "<b>Fórmula general</b>: x = (−b ± √(b² − 4ac)) ÷ 2a. El <b>discriminante</b> b² − 4ac: positivo, dos soluciones; cero, una; negativo, ninguna real."],
     [("x² = 49", ["x = ±7"], "x₁ = −7, x₂ = 7"), ("x² + 2x − 15 = 0", ["(x + 5)(x − 3) = 0"], "x₁ = −5, x₂ = 3"), ("2x² − 8x = 0", ["2x(x − 4) = 0"], "x₁ = 0, x₂ = 4")],
     [["Olvidar la solución negativa", "x² = 25 tiene x = 5 y x = −5."], ["Dividir entre x", "En x² = 3x se pierde la solución x = 0."], ["Errores de signo en la fórmula", "Es −b: si b = −6, −b = 6."]],
     [("¿Cuándo uso la fórmula general?", "Cuando no encuentras fácilmente la factorización; siempre funciona."), ("¿Qué significa que no tenga solución real?", "Que la parábola no corta el eje x.")],
     [("Ecuaciones incompletas", [(inc, 20)]), ("Por factorización", [(fac, 20)]), ("Ecuaciones completas", [(comp, 20)]), ("El discriminante", [(dis, 20)]), ("Repaso", [(comp, 7), (inc, 7), (fac, 6)])],
     69005, lv=9)
