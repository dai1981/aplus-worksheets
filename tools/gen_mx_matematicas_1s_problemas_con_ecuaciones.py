# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Modelar y resolver problemas con una ecuación lineal."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67109))
prob = src("gen_es_matematicas_1eso_ecuaciones", 67391, "s_problema", lv=1, extra=(nomoney,))
tra = src("gen_es_matematicas_1eso_lenguaje_algebraico", 67392, "s_traducir", lv=1)

unit("problemas-con-ecuaciones", 9, "6EC",
     "Modela y resuelve problemas cuyo planteamiento es una ecuación lineal",
     "Problemas con ecuaciones lineales", "Problemas con ecuaciones",
     "Ejercicios de matemáticas de 1.er grado de secundaria: plantear y resolver problemas con ecuaciones lineales de compras, edades, repartos, perímetros y números consecutivos. 100 ejercicios con respuestas.",
     "Nombra x, plantea y comprueba", "x es lo que te preguntan.",
     ["1) Decide qué es <b>x</b> (normalmente lo que te preguntan). 2) Escribe las demás cantidades con x.",
      "3) Plantea la <b>ecuación</b> con el dato que da el total. 4) Resuélvela. 5) <b>Comprueba</b> que la respuesta tiene sentido.",
      "Ejemplo: 3 boletos iguales y unas palomitas de $65 cuestan $305 → 3x + 65 = 305 → x = $80."],
     [("Dos números consecutivos suman 57", ["x + (x + 1) = 57", "2x = 56"], "28 y 29"), ("Juan tiene el triple que Ana; juntos $480", ["x + 3x = 480"], "Ana $120")],
     [["Contestar con x y no con lo que piden", "Si piden el largo y x es el ancho, suma lo que falta."], ["Plantear con datos de distinta unidad", "Pasa todo a la misma unidad antes."], ["No comprobar", "Sustituye en el enunciado, no solo en la ecuación."]],
     [("¿Qué letra uso?", "Cualquiera, pero escribe qué representa: «x = precio de un boleto»."), ("¿Y si el resultado no es entero?", "Puede pasar con dinero o medidas; si hablan de personas u objetos, revisa el planteamiento.")],
     [("Plantear la ecuación", [(tra, 20)]), ("Compras y dinero", [(S.ec_problem, 20)]), ("Edades y números", [(prob, 10), (S.ec_problem, 10)]), ("Repartos y perímetros", [(S.ec_problem, 12), (prob, 8)]), ("Problemas variados", [(S.ec_problem, 10), (prob, 10)])],
     67009, lv=7)
