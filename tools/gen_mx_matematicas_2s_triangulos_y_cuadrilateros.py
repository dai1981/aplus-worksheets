# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Construcción y clasificación de triángulos y cuadriláteros; suma de ángulos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68113))
tri, cua = src("gen_es_matematicas_6_poligonos_y_circulo", 68411, "s2_triangulos", "s3_cuadrilateros", lv=6)
unit("triangulos-y-cuadrilateros", 13, "6CF",
     "Construye y clasifica triángulos y cuadriláteros a partir de distinta información; usa la suma de sus ángulos interiores y la desigualdad del triángulo",
     "Triángulos y cuadriláteros", "Triángulos y cuadriláteros",
     "Ejercicios de matemáticas de 2.º grado de secundaria: clasificar triángulos y cuadriláteros, suma de ángulos interiores, ángulo exterior, triángulos isósceles y existencia de triángulos. 100 ejercicios con respuestas.",
     "Triángulo: 180°. Cuadrilátero: 360°.", "Exterior = suma de los interiores lejanos.",
     ["Los ángulos interiores de un <b>triángulo</b> suman 180°; los de un <b>cuadrilátero</b>, 360°.",
      "Un triángulo se clasifica por sus lados (equilátero, isósceles, escaleno) y por sus ángulos (acutángulo, rectángulo, obtusángulo).",
      "Un <b>ángulo exterior</b> de un triángulo mide lo mismo que la suma de los dos interiores no adyacentes."],
     [("Ángulos 48° y 75°", ["180 − 48 − 75"], "57°"), ("Isósceles con ángulo desigual de 40°", ["(180 − 40) ÷ 2"], "70° y 70°")],
     [["Usar 360° en un triángulo", "Los triángulos suman 180°."], ["Pensar que todo rombo es cuadrado", "El rombo no tiene por qué tener ángulos rectos."], ["Olvidar que un triángulo puede no existir", "Con lados 2, 3 y 7 no se puede."]],
     [("¿Un triángulo puede tener dos ángulos rectos?", "No: ya sumarían 180° y no quedaría nada para el tercero."), ("¿Todo cuadrado es rectángulo?", "Sí: tiene cuatro ángulos rectos.")],
     [("Clasificar triángulos", [(tri, 10), (lambda: S.triangulos("clas"), 10)]), ("Ángulos del triángulo", [(lambda: S.triangulos("suma", "iso"), 20)]), ("Ángulo exterior", [(lambda: S.triangulos("ext"), 20)]),
      ("Cuadriláteros", [(cua, 10), (lambda: S.triangulos("cuad"), 10)]), ("¿Existe el triángulo?", [(lambda: S.triangulos("exist"), 20)])],
     68013, lv=8)
