# -*- coding: utf-8 -*-
"""México 5.º grado: Suma y resta de decimales; multiplicación de decimales por naturales; divisiones con cociente decimal. Reutiliza España 6.º (nivel 5.º) con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

import re


def por_natural(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + it["e"])
    return not re.search(r"\d,\d+\s*×\s*\d+,\d|\d+,\d+\s*×\s*0,|÷\s*\d+,\d|dos factores", t)


sumar, por10, mult, div, probl = src("gen_es_matematicas_6_operaciones_con_decimales", 65309, "s1_sumar", "s2_por10", "s3_mult", "s4_div", "s5_problema", lv=5, extra=(por_natural,))

unit("operaciones-con-decimales", 4, "S",
     "Resuelve sumas y restas de números decimales; multiplica números decimales por números naturales y por 10, 100 y 1 000; resuelve divisiones de naturales con cociente decimal y problemas",
     "Operaciones con decimales", "Operaciones con decimales",
     "Ejercicios de matemáticas de 5.º grado de primaria: sumar y restar decimales, multiplicar decimales por naturales y por 10, 100 y 1 000, divisiones con cociente decimal y problemas. 100 ejercicios con respuestas.",
     "Punto debajo de punto al sumar", "Al multiplicar, cuenta las cifras decimales.",
     ["Para sumar o restar, pon el <b>punto debajo del punto</b> y completa con ceros.",
      "Para multiplicar un decimal por un natural, multiplica sin el punto y pon en el resultado tantas cifras decimales como tenía el decimal: 2.35 × 4 = 9.40.",
      "Multiplicar por 10, 100 o 1 000 mueve el punto 1, 2 o 3 lugares a la derecha. Para dividir con cociente decimal, pon el punto en el cociente y agrega ceros al residuo: 49 ÷ 2 = 24.5."],
     [("Calcula 3.6 × 7", ["36 × 7 = 252", "una cifra decimal"], "25.2"), ("Calcula 14 ÷ 8", ["14 ÷ 8 = 1, sobran 6", "60 ÷ 8 = 7, sobran 4", "40 ÷ 8 = 5"], "1.75")],
     [["Alinear por la derecha al sumar", "12.5 + 3.75: alinea los puntos."], ["Poner mal el punto al multiplicar", "3.6 × 7 = 25.2, no 252."], ["Dejar residuo cuando se puede seguir", "14 ÷ 8 = 1.75."]],
     [("¿Cómo multiplico un decimal por 100?", "Mueve el punto dos lugares a la derecha: 3.25 × 100 = 325. Si faltan cifras, agrega ceros: 4.5 × 100 = 450."),
      ("¿Cómo sigo una división cuando sobra algo?", "Escribe el punto en el cociente, agrega un 0 al residuo y sigue dividiendo.")],
     [("Sumar y restar decimales", [(sumar, 20)]), ("Por 10, 100 y 1 000", [(por10, 20)]), ("Multiplicar decimales por naturales", [(mult, 20)]), ("Divisiones con cociente decimal", [(div, 20)]),
      ("Problemas", [(probl, 20)])],
     65004, pic=mx_text(ES.vertical(["3.6", "7"], op="×")), lv=5)
