# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Rectas, segmentos, semirrectas y ángulos: notación, clasificación, relaciones y distancia entre dos puntos."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67112))
med, rel, prob = src("gen_es_matematicas_6_angulos", 67421, "s1_medir", "s2_relaciones", "s5_problema", lv=6)
rect, para = src("gen_es_matematicas_1eso_rectas_y_angulos", 67422, "s_rectas", "s_paralelas", lv=1)

unit("rectas-y-angulos", 12, "6RA",
     "Explora las figuras básicas como rectas y ángulos y su notación; introduce la idea de distancia entre dos puntos como la longitud del segmento que los une",
     "Rectas, ángulos y distancia", "Rectas y ángulos",
     "Ejercicios de matemáticas de 1.er grado de secundaria: rectas, segmentos y semirrectas, notación de ángulos, clasificación, ángulos complementarios y suplementarios, paralelas y distancia entre dos puntos. 100 ejercicios con respuestas.",
     "En ∠ABC, el vértice es B", "La distancia es la longitud del segmento.",
     ["Una <b>recta</b> no tiene principio ni fin; una <b>semirrecta</b> tiene origen; un <b>segmento</b> tiene dos extremos y se puede medir: <span class='ov'>AB</span>.",
      "Un <b>ángulo</b> se nombra con tres letras y el vértice en medio: ∠ABC. Se clasifica en agudo (&lt; 90°), recto, obtuso, llano (180°), entrante y perigonal (360°).",
      "Complementarios suman 90°; suplementarios, 180°. La <b>distancia entre dos puntos</b> es la longitud del segmento que los une; en la recta numérica, |a − b|."],
     [("Suplementario de 65°", ["180° − 65°"], "115°"), ("Distancia entre −4 y 7", ["|7 − (−4)|"], "11")],
     [["Poner el vértice al principio", "En ∠PQR el vértice es Q."], ["Confundir complementario y suplementario", "Complementario: 90°. Suplementario: 180°."], ["Distancias negativas", "Una distancia siempre es positiva o cero."]],
     [("¿Qué significan ⊥ y ∥?", "⊥ significa «es perpendicular a» y ∥ «es paralela a»."), ("¿Qué es un ángulo entrante?", "Uno que mide más de 180° y menos de 360°; también se llama cóncavo.")],
     [("Rectas, segmentos y notación", [(S.ra_notacion, 14), (rect, 6)]), ("Medir y clasificar ángulos", [(med, 10), (S.ra_notacion, 10)]), ("Complementarios y suplementarios", [(rel, 20)]),
      ("Ángulos entre paralelas", [(para, 20)]), ("Distancia entre dos puntos", [(S.ra_distancia, 16), (prob, 4)])],
     67012, lv=7)
