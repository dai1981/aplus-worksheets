# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Ángulos que se forman al cortarse dos rectas o segmentos; paralelas cortadas por una secante."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68111))
para = src("gen_es_matematicas_1eso_rectas_y_angulos", 68391, "s_paralelas", lv=1)
unit("angulos-entre-rectas", 11, "6RA",
     "Encuentra y calcula los ángulos que se forman al intersecar dos segmentos o rectas, y los ángulos entre rectas paralelas cortadas por una secante",
     "Ángulos entre rectas que se cortan", "Ángulos entre rectas",
     "Ejercicios de matemáticas de 2.º grado de secundaria: ángulos opuestos por el vértice, adyacentes, ángulos entre paralelas cortadas por una secante y ecuaciones con ángulos. 100 ejercicios con respuestas.",
     "Opuestos por el vértice: iguales", "Adyacentes: suman 180°.",
     ["Cuando dos rectas se cortan forman cuatro ángulos. Los <b>opuestos por el vértice</b> son iguales y los <b>adyacentes</b> suman 180°.",
      "Si dos <b>paralelas</b> son cortadas por una secante, los ángulos correspondientes, alternos internos y alternos externos son iguales.",
      "Con expresiones: si dos ángulos opuestos miden 3x + 10 y 70, entonces 3x + 10 = 70 y x = 20."],
     [("Un ángulo de 65°", ["opuesto: 65°", "adyacente: 180° − 65°"], "65° y 115°"), ("(2x + 30)° y 110° adyacentes", ["2x + 30 + 110 = 180"], "x = 20")],
     [["Restar de 90° en lugar de 180°", "Los adyacentes en una recta suman 180°."], ["Pensar que todos los ángulos son iguales", "Solo los opuestos por el vértice."], ["Olvidar que las rectas deben ser paralelas", "Sin paralelas, los alternos no tienen por qué ser iguales."]],
     [("¿Cuánto suman los cuatro ángulos?", "360°, una vuelta completa."), ("¿Qué son ángulos alternos internos?", "Los que están entre las paralelas, en lados distintos de la secante.")],
     [("Opuestos y adyacentes", [(lambda: S.ang_cruce("fig"), 20)]), ("Cálculos con ángulos", [(lambda: S.ang_cruce("op", "ady", "tres"), 20)]), ("Paralelas y secante", [(para, 20)]),
      ("Ecuaciones con ángulos", [(lambda: S.ang_cruce("ecu"), 20)]), ("Repaso", [(S.ang_cruce, 12), (para, 8)])],
     68011, lv=8)
