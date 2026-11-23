# -*- coding: utf-8 -*-
"""México 6.º grado: Polígonos regulares e irregulares; ángulos interiores de triángulos y polígonos; trazos (Figuras geométricas y sus características). Reutiliza España 6.º y 4.º con otra semilla."""
from mx_common import src, unit

pol = src("gen_es_matematicas_6_poligonos_y_circulo", 66317, "s1_poligonos", lv=6)
tri, probl, rel = src("gen_es_matematicas_6_angulos", 66315, "s3_triangulo", "s5_problema", "s2_relaciones", lv=6)
suma, poli4, lados = src("gen_es_matematicas_4_triangulos_y_cuadrilateros", 66217, "s2_suma", "s4_poligonos", "s1_lados")

unit("poligonos-regulares", 9, "F",
     "Distingue polígonos regulares e irregulares; identifica sus elementos (lados, vértices, ángulos, diagonales); calcula ángulos interiores de triángulos y otros polígonos y perímetros de polígonos regulares",
     "Polígonos regulares y sus ángulos", "Polígonos regulares",
     "Ejercicios de matemáticas de 6.º grado de primaria: polígonos regulares e irregulares, nombres, diagonales, ángulos de triángulos y polígonos, perímetro y problemas. 100 ejercicios con respuestas.",
     "Regular: lados y ángulos iguales", "Los ángulos de un triángulo suman 180°.",
     ["Un polígono es <b>regular</b> si todos sus lados y todos sus ángulos son iguales, como el cuadrado o el hexágono regular. Si no, es <b>irregular</b>.",
      "Los ángulos interiores de un triángulo suman 180°; los de un cuadrilátero, 360°; los de un pentágono, 540°. Cada lado más suma 180°.",
      "El perímetro de un polígono regular es número de lados × lado: un hexágono regular de 5 cm tiene 6 × 5 = 30 cm."],
     [("Ángulo de un hexágono regular", ["suma: 4 × 180° = 720°", "720 ÷ 6"], "120°"), ("Triángulo con 35° y 85°", ["180 − 35 − 85"], "60°")],
     [["Pensar que un rombo es regular", "Tiene lados iguales, pero sus ángulos no lo son."], ["Sumar los ángulos de un cuadrilátero a 180°", "Suman 360°."], ["Contar mal las diagonales", "Desde un vértice no se traza diagonal a sus vecinos."]],
     [("¿El cuadrado es un polígono regular?", "Sí: sus 4 lados son iguales y sus 4 ángulos miden 90°. El rectángulo no lo es, porque sus lados no son todos iguales."),
      ("¿Cuánto suman los ángulos de un pentágono?", "540°. Se puede dividir en 3 triángulos desde un vértice: 3 × 180° = 540°.")],
     [("Nombres y elementos de los polígonos", [(pol, 12), (poli4, 8)]), ("Ángulos de un triángulo", [(tri, 20)]), ("Suma de ángulos", [(suma, 20)]), ("Triángulos por sus lados y relaciones de ángulos", [(lados, 10), (rel, 10)]),
      ("Problemas", [(probl, 20)])],
     66009, lv=6)
