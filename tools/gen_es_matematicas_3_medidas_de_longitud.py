# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Medidas de longitud (Sentido de la medida)
km, m, cm y mm; elegir la unidad; medir con la regla; pasar de una unidad a otra; comparar; problemas.
Reutiliza los generadores de 4.º (mismo ciclo) con números hasta 9999 y sin decimales.
"""
from es_low import unit, src
import gen_es_matematicas_4_medidas_de_longitud as L4

SEED = 33911
uni, adec, reg, pasar, comp, prob = src("medidas_de_longitud", SEED, "s1_unidades", "s1_adecuada", "s2_regla", "s3_pasar", "s4_complejas", "s5_problema")

unit(3, "medidas-de-longitud", 11, "M", "Unidades de longitud (km, m, cm, mm); estimación y medida con instrumentos; equivalencias entre unidades; resolución de problemas",
     "Medidas de longitud", "Longitud",
     "Fichas de matemáticas de 3.º de Primaria: km, m, cm y mm, medir con la regla, pasar de una unidad a otra y problemas. 100 ejercicios con soluciones.",
     "1 m = 100 cm; 1 km = 1000 m", "1 cm = 10 mm.",
     ["El <b>metro</b> (m) es la unidad principal. 1 m = 100 cm; 1 cm = 10 mm; 1 km = 1000 m.", "Para medir con la regla, empieza en el <b>0</b>, no en el borde.",
      "Elige la unidad según el tamaño: un lápiz en cm, una clase en m, un viaje en km."],
     [("3 m 25 cm en cm", ["3 m = 300 cm", "300 + 25"], "325 cm"), ("4 km en m", ["1 km = 1000 m", "4 × 1000"], "4000 m")],
     [["Medir desde el borde de la regla", "Coloca el objeto en el 0."], ["Confundir 100 y 1000", "1 m = 100 cm, pero 1 km = 1000 m."], ["Comparar sin pasar a la misma unidad", "2 m y 150 cm: 200 cm &gt; 150 cm."]],
     [("¿Cuántos centímetros tiene un metro?", "Un metro tiene 100 centímetros."), ("¿Qué unidad se usa para medir distancias entre ciudades?", "El kilómetro (km). 1 km son 1000 metros.")],
     [("Unidades de longitud", [(uni, 14), (adec, 6)]), ("Medir con la regla", [(reg, 20)]), ("Pasar de una unidad a otra", [(pasar, 20)]), ("Comparar longitudes", [(comp, 20)]), ("Problemas", [(prob, 20)])],
     33011, L4.regla(7, 4))
