# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Perímetro y área de polígonos regulares e irregulares."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67116))
pol = src("gen_es_matematicas_6_poligonos_y_circulo", 67451, "s1_poligonos", lv=6)
tp, otros, comp, prob = src("gen_es_matematicas_6_area_de_figuras_planas", 67452, "s2_tri_para", "s3_otros", "s4_compuesta", "s5_problema", lv=6, extra=(nomoney,))
inv = src("gen_es_matematicas_1eso_poligonos_y_areas", 67453, "s_inversa", lv=1)

unit("perimetro-y-area-de-poligonos", 16, "6ME",
     "Obtiene y aplica fórmulas, o usa otras estrategias, para calcular el perímetro y el área de polígonos regulares e irregulares",
     "Perímetro y área de polígonos", "Área de polígonos",
     "Ejercicios de matemáticas de 1.er grado de secundaria: perímetro y área de triángulos, paralelogramos, rombos, trapecios, polígonos regulares y figuras compuestas. 100 ejercicios con respuestas.",
     "Triángulo: base × altura ÷ 2", "Polígono regular: perímetro × apotema ÷ 2",
     ["<b>Rectángulo y romboide</b>: base × altura. <b>Triángulo</b>: base × altura ÷ 2. <b>Rombo</b>: diagonal mayor × diagonal menor ÷ 2. <b>Trapecio</b>: (B + b) × h ÷ 2.",
      "<b>Polígono regular</b>: perímetro × apotema ÷ 2 (la apotema va del centro al punto medio de un lado).",
      "Para una figura <b>irregular</b>, divídela en figuras conocidas y suma sus áreas. El <b>perímetro</b> es la suma de todos los lados."],
     [("Trapecio B = 10, b = 6, h = 4", ["(10 + 6) × 4 ÷ 2"], "32 cm²"), ("Hexágono regular lado 6, apotema 5.2", ["P = 36", "36 × 5.2 ÷ 2"], "93.6 cm²")],
     [["Usar el lado inclinado como altura", "La altura es perpendicular a la base."], ["Olvidar dividir entre 2", "Triángulo, rombo y trapecio llevan ÷ 2."], ["Confundir unidades", "El perímetro va en cm; el área, en cm²."]],
     [("¿Qué es la apotema?", "El segmento que une el centro de un polígono regular con el punto medio de un lado; es perpendicular a ese lado."),
      ("¿Dos figuras con el mismo perímetro tienen la misma área?", "No necesariamente: un rectángulo de 1 × 9 y un cuadrado de 5 × 5 tienen perímetro 20, pero áreas 9 y 25.")],
     [("Polígonos y perímetro", [(pol, 20)]), ("Triángulos y paralelogramos", [(tp, 20)]), ("Rombo, trapecio y polígonos regulares", [(otros, 20)]),
      ("Figuras compuestas", [(comp, 14), (inv, 6)]), ("Problemas", [(prob, 20)])],
     67016, lv=7)
