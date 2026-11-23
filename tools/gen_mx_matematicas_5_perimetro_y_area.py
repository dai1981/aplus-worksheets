# -*- coding: utf-8 -*-
"""México 5.º grado: Perímetro y área de rectángulos, cuadrados y figuras compuestas; área en cuadrícula (Perímetro, área y noción de volumen). Reutiliza España 6.º (nivel 5.º) y 4.º con otra semilla."""
import re
from mx_common import src, unit


def sin_tri(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + it["e"])
    return not re.search(r"triángulo|romb|trapecio|paralelogramo|romboide|hectárea|área agraria|\bha\b|km²|dam²|hm²", t)


rect, comp, probl = src("gen_es_matematicas_6_area_de_figuras_planas", 65317, "s1_rect", "s4_compuesta", "s5_problema", lv=5, extra=(sin_tri,))
cuad = src("gen_es_matematicas_6_superficie", 65318, "s4_cuadricula", lv=5, extra=(sin_tri,))
per, falta = src("gen_es_matematicas_4_perimetro_y_area", 65220, "s2_perimetro", "s4_falta")

unit("perimetro-y-area", 11, "V",
     "Calcula el perímetro de polígonos con una fórmula y el área de rectángulos y cuadrados; estima áreas en cuadrícula; calcula el área de figuras compuestas por rectángulos; resuelve problemas",
     "Perímetro y área de rectángulos", "Perímetro y área",
     "Ejercicios de matemáticas de 5.º grado de primaria: perímetro con fórmula, área de rectángulos y cuadrados, área en cuadrícula, figuras compuestas y problemas. 100 ejercicios con respuestas.",
     "Área = base × altura", "Perímetro = suma de los lados.",
     ["El <b>perímetro</b> es la suma de los lados. En un rectángulo: P = 2 × (base + altura); en un cuadrado, P = 4 × lado.",
      "El <b>área</b> de un rectángulo es base × altura, y la de un cuadrado, lado × lado. Se mide en unidades cuadradas: cm², m².",
      "Para una figura compuesta, divídela en rectángulos, calcula el área de cada uno y suma."],
     [("Rectángulo de 12 m por 7 m", ["P = 2 × (12 + 7) = 38 m", "A = 12 × 7 = 84 m²"], "38 m y 84 m²"), ("Figura en L: 8 × 3 y 4 × 5", ["24 + 20"], "44 cm²")],
     [["Confundir perímetro y área", "El perímetro va en m; el área, en m²."], ["Sumar solo dos lados", "P = 2 × (base + altura)."], ["Contar dos veces una parte de la figura compuesta", "Los rectángulos no deben encimarse."]],
     [("¿Por qué el área se mide en cm²?", "Porque cuenta cuántos cuadrados de 1 cm de lado caben dentro de la figura."),
      ("¿Cómo calculo el área de una figura en forma de L?", "Divídela en dos rectángulos, calcula el área de cada uno y suma los resultados.")],
     [("Perímetro", [(per, 20)]), ("Área de rectángulos y cuadrados", [(rect, 20)]), ("Área en cuadrícula", [(cuad, 20)]), ("Figuras compuestas", [(comp, 12), (falta, 8)]), ("Problemas", [(probl, 20)])],
     65011, lv=5)
