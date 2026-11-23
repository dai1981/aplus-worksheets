# -*- coding: utf-8 -*-
"""México 5.º grado: Medición de la longitud, masa y capacidad (km, m, cm, mm; t, kg, g; L, mL); conversiones con decimales (Fase 5). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
import re
from mx_common import src, unit


def units_ok(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
    return not re.search(r"\d\s?(hm|dam|hL|daL|dL|cL|hg|dag|dg|cg|kL)\b|hecto|deca|centil|decil|Madrid|Valencia", t) and not re.search(r"\d[.,]\d{4}", t)


cambio, compl, comp, unid, probl = src("gen_es_matematicas_6_medidas", 65314, "s1_cambio", "s2_complejas", "s3_comparar", "s4_unidad", "s5_problema", lv=5, extra=(units_ok,))

unit("longitud-masa-y-capacidad", 10, "L5",
     "Usa el kilómetro, el metro, el centímetro y el milímetro, la tonelada, el kilogramo y el gramo, el litro y el mililitro; convierte unidades con números naturales y decimales; compara medidas y resuelve problemas",
     "Longitud, masa y capacidad: conversiones", "Longitud, masa y capacidad",
     "Ejercicios de matemáticas de 5.º grado de primaria: kilómetros, toneladas, kilos y gramos, litros y mililitros, conversiones con decimales, comparar medidas y problemas. 100 ejercicios con respuestas.",
     "A una unidad menor: multiplica", "A una unidad mayor: divide.",
     ["Longitud: 1 km = 1 000 m; 1 m = 100 cm = 1 000 mm. Masa: 1 t = 1 000 kg; 1 kg = 1 000 g. Capacidad: 1 L = 1 000 mL.",
      "De una unidad grande a una pequeña se <b>multiplica</b>: 2.5 km = 2 500 m. De una pequeña a una grande se <b>divide</b>: 750 g = 0.75 kg.",
      "Para comparar o sumar medidas, pásalas primero a la misma unidad."],
     [("¿Cuántos kilos son 3.2 t?", ["1 t = 1 000 kg", "3.2 × 1 000"], "3 200 kg"), ("¿Cuántos litros son 1 250 mL?", ["1 250 ÷ 1 000"], "1.25 L")],
     [["Multiplicar cuando hay que dividir", "750 g a kg: 750 ÷ 1 000."], ["Pensar que 1 m = 1 000 cm", "1 m = 100 cm; 1 km = 1 000 m."], ["Mover mal el punto", "2.5 km = 2 500 m, no 250 m."]],
     [("¿Cuántos kilogramos tiene una tonelada?", "1 000 kilogramos. Se usa para pesar cosas muy pesadas, como un camión o una ballena."),
      ("¿Cómo convierto 750 gramos a kilogramos?", "Divide entre 1 000: 750 ÷ 1 000 = 0.75 kg.")],
     [("Convertir unidades", [(cambio, 20)]), ("Medidas con dos unidades", [(compl, 20)]), ("Comparar medidas", [(comp, 20)]), ("La unidad adecuada y más conversiones", [(unid, 6), (cambio, 14)]), ("Problemas", [(probl, 20)])],
     65010, lv=5)
