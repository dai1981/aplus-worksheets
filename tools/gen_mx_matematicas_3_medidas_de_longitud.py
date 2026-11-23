# -*- coding: utf-8 -*-
"""México 3.er grado: Medición de longitud (m, dm, cm, mm, km; regla, equivalencias, problemas). Reutiliza España 4.º con otra semilla."""
import re
from mx_common import src, unit, mx_text
import gen_es_matematicas_4_medidas_de_longitud as L4

uni, adec, reg, pasar, comp, prob = src("gen_es_matematicas_4_medidas_de_longitud", 63212, "s1_unidades", "s1_adecuada", "s2_regla", "s3_pasar", "s4_complejas", "s5_problema", extra=(lambda it: not re.search(r"\d\s?(hm|dam)\b|hectómetro|decámetro", re.sub(r"<[^>]*>", " ", it["q"] + " ".join(it["c"]) + it["e"])),))

unit("medidas-de-longitud", 12, "L",
     "Mide, estima y compara longitudes con el metro, el decímetro y el centímetro (y el milímetro y el kilómetro); usa la regla y resuelve problemas de su contexto",
     "Medidas de longitud", "Longitud",
     "Ejercicios de matemáticas de 3.er grado de primaria: metro, decímetro, centímetro y milímetro, medir con la regla, convertir unidades y problemas. 100 ejercicios con respuestas.",
     "1 m = 10 dm = 100 cm", "1 cm = 10 mm; 1 km = 1 000 m.",
     ["El <b>metro</b> (m) es la unidad principal. 1 m = 10 dm = 100 cm; 1 cm = 10 mm; 1 km = 1 000 m.", "Para medir con la regla, empieza en el <b>0</b>, no en la orilla.",
      "Elige la unidad según el tamaño: un lápiz en cm, el salón en m, un viaje en km."],
     [("3 m 25 cm en cm", ["3 m = 300 cm", "300 + 25"], "325 cm"), ("4 km en m", ["1 km = 1 000 m", "4 × 1 000"], "4 000 m")],
     [["Medir desde la orilla de la regla", "Coloca el objeto en el 0."], ["Confundir 100 y 1 000", "1 m = 100 cm, pero 1 km = 1 000 m."], ["Comparar sin pasar a la misma unidad", "2 m y 150 cm: 200 cm &gt; 150 cm."]],
     [("¿Cuántos centímetros tiene un metro?", "Un metro tiene 100 centímetros (y 10 decímetros)."), ("¿Qué unidad se usa para medir distancias entre ciudades?", "El kilómetro (km). 1 km son 1 000 metros.")],
     [("Unidades de longitud", [(uni, 14), (adec, 6)]), ("Medir con la regla", [(reg, 20)]), ("Convertir unidades", [(pasar, 20)]), ("Comparar longitudes", [(comp, 20)]), ("Problemas", [(prob, 20)])],
     63012, pic=mx_text(L4.regla(7, 4)))
