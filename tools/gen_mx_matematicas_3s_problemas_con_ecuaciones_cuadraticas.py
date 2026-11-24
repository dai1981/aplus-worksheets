# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Problemas que se resuelven con una ecuación cuadrática."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69106))
prob = src("gen_es_matematicas_1eso_ecuaciones", 69341, "s_problema", lv=3, extra=(nomoney, lambda it: re.search(r"cuadrado|producto|área|²", it["q"]),))
unit("problemas-con-ecuaciones-cuadraticas", 6, "6EC",
     "Resuelve problemas que implican el planteamiento de una ecuación cuadrática",
     "Problemas con ecuaciones cuadráticas", "Problemas cuadráticos",
     "Ejercicios de matemáticas de 3.er grado de secundaria: plantear y resolver problemas de áreas, números consecutivos, marcos y productos con ecuaciones cuadráticas. 100 ejercicios con respuestas.",
     "Plantea, iguala a cero y resuelve", "Descarta las soluciones sin sentido.",
     ["Lee el problema y llama x a lo que no conoces. Si aparece un <b>área</b> o un <b>producto</b> de dos cantidades con x, la ecuación será cuadrática.",
      "Pasa todo a un lado (= 0) y resuelve por factorización o con la fórmula general.",
      "Revisa las dos soluciones: una medida o una edad no puede ser negativa."],
     [("Rectángulo: largo = ancho + 3, área 70", ["x(x + 3) = 70", "x² + 3x − 70 = 0", "(x + 10)(x − 7) = 0"], "ancho 7"), ("Consecutivos con producto 132", ["x(x + 1) = 132"], "11 y 12")],
     [["Quedarse con la solución negativa", "Un ancho de −10 m no tiene sentido."], ["No igualar a cero", "Para factorizar, un lado debe ser 0."], ["Plantear mal el área", "Área de un rectángulo: largo × ancho."]],
     [("¿Por qué salen dos soluciones?", "Porque la ecuación tiene x²; el contexto dice cuál sirve."), ("¿Y si ninguna solución sirve?", "Revisa el planteamiento: quizá hay un error.")],
     [("Áreas de rectángulos", [(lambda: S.ec2_problema("rect"), 20)]), ("Números", [(lambda: S.ec2_problema("cons", "cuad", "num"), 20)]), ("Marcos y bordes", [(lambda: S.ec2_problema("marco"), 10), (lambda: S.ec2_problema("rect"), 10)]),
      ("Problemas variados", [(prob, 8), (S.ec2_problema, 12)]), ("Repaso", [(S.ec2_problema, 20)])],
     69006, lv=9)
