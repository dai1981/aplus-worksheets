# -*- coding: utf-8 -*-
"""México 4.º grado: Medición de longitud, masa y capacidad (m, dm, cm, mm, km; kg, g; L, mL; medios y cuartos). Reutiliza España 5.º/4.º con otra semilla."""
import re
from mx_common import src, unit, mx_text
import es_common as ES


def units_ok(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
    return not re.search(r"\d\s?(hm|dam|hL|daL|dL|cL|hg|dag|dg|cg|mg|t)\b|hecto|deca|centil|decil|tonelada|Madrid|Valencia|kL", t) and not re.search(r"\d[.,]\d{3}|\d[.,]\d+\s?(dm|mm)\b", t)


M = "gen_es_matematicas_6_medidas"
cambio, complejas, comparar, probl = src(M, 64316, "s1_cambio", "s2_complejas", "s3_comparar", "s5_problema", lv=5, extra=(units_ok,))
masa, cap = src("gen_es_matematicas_4_masa_y_capacidad", 64216, "s1_masa", "s2_cap", extra=(units_ok,))
comp4, prob4 = src("gen_es_matematicas_4_medidas_de_longitud", 64217, "s4_complejas", "s5_problema", extra=(units_ok,))

unit("longitud-masa-y-capacidad", 13, "L",
     "Estima, mide, compara y ordena longitudes, masas y capacidades con el metro, el decímetro, el centímetro, el milímetro y el kilómetro, el kilogramo y el gramo, el litro y el mililitro, y con medios y cuartos de esas unidades; convierte unidades y resuelve problemas",
     "Longitud, masa y capacidad", "Longitud, masa y capacidad",
     "Ejercicios de matemáticas de 4.º grado de primaria: metros, centímetros y kilómetros, kilos y gramos, litros y mililitros, medio y cuarto de kilo, convertir unidades y problemas. 100 ejercicios con respuestas.",
     "1 m = 100 cm; 1 kg = 1 000 g", "1 km = 1 000 m; 1 L = 1 000 mL.",
     ["Longitud: 1 km = 1 000 m; 1 m = 10 dm = 100 cm; 1 cm = 10 mm.",
      "Masa: 1 kg = 1 000 g; <b>medio kilo</b> = 500 g y <b>un cuarto de kilo</b> = 250 g. Capacidad: 1 L = 1 000 mL; medio litro = 500 mL.",
      "Para pasar a una unidad más pequeña, <b>multiplica</b> (3 m = 300 cm); para pasar a una más grande, <b>divide</b> (4 000 g = 4 kg)."],
     [("¿Cuántos centímetros son 2 m 35 cm?", ["2 m = 200 cm", "200 + 35"], "235 cm"), ("¿Cuántos gramos son 3 kilos y cuarto?", ["3 kg = 3 000 g", "1/4 kg = 250 g"], "3 250 g")],
     [["Multiplicar cuando hay que dividir", "De g a kg hay que dividir entre 1 000."], ["Pensar que 1 m = 1 000 cm", "1 m = 100 cm; 1 km = 1 000 m."], ["Sumar medidas con unidades distintas", "Pasa todo a la misma unidad."]],
     [("¿Cuántos gramos tiene medio kilo?", "500 gramos, porque 1 kilogramo tiene 1 000 gramos y la mitad de 1 000 es 500. Un cuarto de kilo son 250 g."),
      ("¿Cuántos mililitros tiene un litro?", "1 000 mL. Medio litro son 500 mL y un cuarto de litro, 250 mL.")],
     [("Convertir unidades", [(cambio, 20)]), ("Medidas con dos unidades", [(complejas, 12), (comp4, 8)]), ("Comparar medidas", [(comparar, 20)]), ("Kilos, litros, medios y cuartos", [(masa, 10), (cap, 10)]),
      ("Problemas", [(probl, 10), (prob4, 10)])],
     64013, lv=4)
