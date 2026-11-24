# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Perímetro y área de figuras compuestas con círculos y polígonos."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69114))
comp = src("gen_es_matematicas_6_area_de_figuras_planas", 69381, "s4_compuesta", lv=6, extra=(nomoney,))
prob = src("gen_es_matematicas_6_longitud_y_area_del_circulo", 69382, "s5_problema", lv=6, extra=(nomoney,))
unit("perimetro-y-area-de-figuras-compuestas", 14, "6ME",
     "Calcula el perímetro y el área de figuras compuestas y explora intersecciones entre círculos y figuras",
     "Perímetro y área de figuras compuestas", "Figuras compuestas",
     "Ejercicios de matemáticas de 3.er grado de secundaria: áreas sombreadas, círculos dentro de cuadrados, coronas circulares, ventanas y pistas. 100 ejercicios con respuestas.",
     "Agrega sumando, quita restando", "Área sombreada = figura grande − figura pequeña.",
     ["Para una <b>figura compuesta</b>, divídela en figuras conocidas (rectángulos, triángulos, círculos, semicírculos).",
      "Si una parte está «dentro» de otra, el área sombreada es la grande menos la pequeña. Un círculo dentro de un cuadrado de lado l tiene radio l ÷ 2.",
      "Para el <b>perímetro</b>, suma solo las líneas del contorno: dos semicírculos iguales forman un círculo completo."],
     [("Cuadrado de 10 con círculo inscrito", ["100 − 3.14 × 25"], "21.5 cm²"), ("Corona de radios 5 y 3", ["3.14 × (25 − 9)"], "50.24 cm²")],
     [["Sumar áreas que se enciman", "Si se enciman, resta la parte común."], ["Usar el diámetro como radio", "Lado 10 → radio 5."], ["Contar líneas interiores en el perímetro", "Solo cuenta el borde."]],
     [("¿Qué es una corona circular?", "La región entre dos circunferencias con el mismo centro."), ("¿Cómo calculo el perímetro de un semicírculo?", "π × r más el diámetro.")],
     [("Círculos y cuadrados", [(lambda: S.compuestas("cuad_circ", "circ_cuad"), 20)]), ("Coronas circulares", [(lambda: S.compuestas("corona"), 20)]),
      ("Ventanas y pistas", [(lambda: S.compuestas("semi", "rect_semi"), 20)]), ("Figuras con polígonos", [(comp, 20)]), ("Problemas", [(prob, 12), (S.compuestas, 8)])],
     69014, lv=9)
