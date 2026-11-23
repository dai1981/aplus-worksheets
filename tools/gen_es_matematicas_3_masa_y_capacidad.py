# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Masa y capacidad (Sentido de la medida)
kg y g, L y mL, leer básculas y jarras, elegir la unidad, problemas.
Reutiliza los generadores de 4.º (mismo ciclo) con números hasta 9999 y sin decimales.
"""
from es_low import unit, src
import gen_es_matematicas_4_masa_y_capacidad as M4

SEED = 33912
masa, cap, leer, unid, prob = src("masa_y_capacidad", SEED, "s1_masa", "s2_cap", "s3_leer", "s4_unidad", "s5_problema")

unit(3, "masa-y-capacidad", 12, "M", "Unidades de masa (kg, g) y capacidad (L, mL); estimación y medida con instrumentos; equivalencias; resolución de problemas",
     "Masa y capacidad", "Masa y capacidad",
     "Fichas de matemáticas de 3.º de Primaria: kilos y gramos, litros y mililitros, leer básculas y jarras y problemas. 100 ejercicios con soluciones.",
     "1 kg = 1000 g; 1 L = 1000 mL", "Medio kilo son 500 g.",
     ["La <b>masa</b> se mide en kilogramos (kg) y gramos (g): 1 kg = 1000 g.", "La <b>capacidad</b> se mide en litros (L) y mililitros (mL): 1 L = 1000 mL.",
      "Medio = 500; un cuarto = 250."],
     [("2 kg 300 g en gramos", ["2 kg = 2000 g", "2000 + 300"], "2300 g"), ("¿Cuántos vasos de 250 mL llenan 1 L?", ["1000 : 250"], "4 vasos")],
     [["Pensar que 1 kg = 100 g", "Son 1000 g."], ["Leer mal la báscula", "Mira cuánto vale cada rayita."], ["Comparar sin pasar a la misma unidad", "1 L y 800 mL: 1000 mL &gt; 800 mL."]],
     [("¿Cuántos gramos tiene un kilo?", "Un kilogramo tiene 1000 gramos."), ("¿Cuántos mililitros tiene un litro?", "Un litro tiene 1000 mililitros.")],
     [("Kilos y gramos", [(masa, 20)]), ("Litros y mililitros", [(cap, 20)]), ("Básculas y jarras", [(leer, 20)]), ("Elegir la unidad", [(unid, 12), (masa, 4), (cap, 4)]), ("Problemas", [(prob, 20)])],
     33012, M4.bascula(1500))
