# -*- coding: utf-8 -*-
"""México 6.º grado: Perímetro y área de triángulos, paralelogramos, trapecios y figuras compuestas (Perímetro, área y noción de volumen). Reutiliza España 6.º con otra semilla."""
import re
from mx_common import src, unit


def ok(it):
    return not re.search(r"hectárea|\bha\b|área agraria|dam²|hm²", re.sub(r"<[^>]*>", " ", it["q"] + it["e"]))


rect, tri, otros, comp, probl = src("gen_es_matematicas_6_area_de_figuras_planas", 66317, "s1_rect", "s2_tri_para", "s3_otros", "s4_compuesta", "s5_problema", lv=6, extra=(ok,))
camb = src("gen_es_matematicas_6_superficie", 66319, "s1_cambio", lv=6, extra=(ok,))

unit("perimetro-y-area", 11, "V",
     "Calcula el perímetro y el área de rectángulos, cuadrados, triángulos, paralelogramos, rombos y trapecios con sus fórmulas; calcula áreas de figuras compuestas; convierte unidades de superficie",
     "Área de triángulos y otras figuras", "Perímetro y área",
     "Ejercicios de matemáticas de 6.º grado de primaria: área del rectángulo, el triángulo, el paralelogramo, el rombo y el trapecio, figuras compuestas, unidades de superficie y problemas. 100 ejercicios con respuestas.",
     "Triángulo: base × altura ÷ 2", "Paralelogramo: base × altura.",
     ["Rectángulo y paralelogramo: A = base × altura. Triángulo: A = base × altura ÷ 2, porque es la mitad de un paralelogramo.",
      "Rombo: A = diagonal mayor × diagonal menor ÷ 2. Trapecio: A = (base mayor + base menor) × altura ÷ 2.",
      "La <b>altura</b> es perpendicular a la base, no es el lado inclinado. Para figuras compuestas, divide y suma."],
     [("Triángulo de base 12 cm y altura 7 cm", ["12 × 7 = 84", "84 ÷ 2"], "42 cm²"), ("Trapecio de bases 10 y 6 m, altura 4 m", ["(10 + 6) × 4 = 64", "64 ÷ 2"], "32 m²")],
     [["Olvidar dividir entre 2 en el triángulo", "base × altura ÷ 2."], ["Usar el lado inclinado como altura", "La altura es perpendicular a la base."], ["Confundir cm y cm²", "El área va en unidades cuadradas."]],
     [("¿Por qué el área del triángulo se divide entre 2?", "Porque dos triángulos iguales forman un paralelogramo de la misma base y altura."),
      ("¿Cuántos cm² tiene 1 m²?", "10 000 cm², porque 1 m² es un cuadrado de 100 cm × 100 cm.")],
     [("Rectángulos y cuadrados", [(rect, 20)]), ("Triángulos y paralelogramos", [(tri, 20)]), ("Rombos y trapecios", [(otros, 20)]), ("Figuras compuestas", [(comp, 14), (camb, 6)]), ("Problemas", [(probl, 20)])],
     66011, lv=6)
