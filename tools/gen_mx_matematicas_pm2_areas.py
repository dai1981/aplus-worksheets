# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 9): concepto de área y fórmulas del rectángulo, triángulo, paralelogramo, trapecio y figuras compuestas."""
import random
from mx_common import src, unit, nomoney

tp, otros, comp, prob = src("gen_es_matematicas_6_area_de_figuras_planas", 110309, "s2_tri_para", "s3_otros", "s4_compuesta", "s5_problema", lv=6, extra=(nomoney,))
inv = src("gen_es_matematicas_1eso_poligonos_y_areas", 110319, "s_inversa", lv=1)
unit("areas", 9, ("Geometría", 9, "Áreas de figuras planas"),
     "Comprende el concepto de área y deduce y aplica las fórmulas del área de rectángulos, triángulos, paralelogramos, trapecios y figuras compuestas",
     "Áreas de figuras planas", "Áreas",
     "Ejercicios de Pensamiento Matemático II: área de triángulos, paralelogramos, rombos, trapecios y polígonos, figuras compuestas, datos que faltan y problemas. 100 ejercicios con respuestas.",
     "Área = cuadritos de 1 u² que caben", "Triángulo: la mitad de un paralelogramo.",
     ["El <b>área</b> es cuántos cuadrados de 1 unidad² cubren la figura. Rectángulo: A = b × h.",
      "Un paralelogramo se recorta y se vuelve rectángulo: A = b × h. Un triángulo es medio paralelogramo: A = b × h ÷ 2. Trapecio: A = (B + b) × h ÷ 2.",
      "Para una <b>figura compuesta</b>, divídela en figuras conocidas y suma (o resta) sus áreas."],
     [("Trapecio con bases 10 y 6 cm, altura 4 cm", ["(10 + 6) × 4 ÷ 2"], "32 cm²"), ("Triángulo de área 24 cm² y base 8 cm", ["24 = 8 × h ÷ 2"], "h = 6 cm")],
     [["Usar el lado inclinado como altura", "La altura es perpendicular a la base."], ["Olvidar dividir entre 2", "Triángulo y trapecio llevan ÷ 2."], ["Mezclar unidades", "Pasa todo a la misma unidad antes de multiplicar."]],
     [("¿Por qué el área de un triángulo es b × h ÷ 2?", "Porque dos triángulos iguales forman un paralelogramo de área b × h."),
      ("¿Qué es la geometría sintética?", "La que razona con figuras y propiedades, sin coordenadas: por ejemplo, recortar y reacomodar para obtener una fórmula.")],
     [("Triángulos y paralelogramos", [(tp, 20)]), ("Rombos, trapecios y polígonos", [(otros, 20)]), ("Figuras compuestas", [(comp, 20)]),
      ("Datos que faltan", [(inv, 20)]), ("Problemas", [(prob, 20)])],
     110009, lv=11)
