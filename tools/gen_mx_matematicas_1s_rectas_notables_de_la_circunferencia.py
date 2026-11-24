# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Radio, diámetro, cuerda, secante y tangente; posiciones de una recta y una circunferencia."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67115))
ele = src("gen_es_matematicas_1eso_circunferencia_y_circulo", 67441, "s_elementos", lv=1)
cir = src("gen_es_matematicas_6_poligonos_y_circulo", 67442, "s4_circulo", lv=6)

unit("rectas-notables-de-la-circunferencia", 15, "6CC",
     "Identifica y traza las rectas notables en la circunferencia (radio, diámetro, cuerda, secante y tangente) y las relaciones entre ellas",
     "Rectas notables de la circunferencia", "Rectas de la circunferencia",
     "Ejercicios de matemáticas de 1.er grado de secundaria: radio, diámetro, cuerda, secante y tangente; posiciones de una recta respecto a una circunferencia y sus relaciones. 100 ejercicios con respuestas.",
     "La tangente toca en un solo punto", "Y es perpendicular al radio en ese punto.",
     ["<b>Radio</b>: del centro a la circunferencia. <b>Diámetro</b>: la cuerda que pasa por el centro (mide dos radios). <b>Cuerda</b>: une dos puntos de la circunferencia.",
      "Una recta <b>secante</b> corta la circunferencia en 2 puntos; una <b>tangente</b>, en 1; una <b>exterior</b>, en ninguno. Depende de si la distancia del centro a la recta es menor, igual o mayor que el radio.",
      "La tangente es <b>perpendicular</b> al radio en el punto de tangencia, y la perpendicular desde el centro a una cuerda la divide en dos partes iguales."],
     [("Radio 6 cm", ["Diámetro = 2 × 6"], "12 cm"), ("r = 5 cm, distancia a la recta 5 cm", ["igual al radio"], "tangente")],
     [["Confundir cuerda y diámetro", "Todo diámetro es cuerda, pero no toda cuerda es diámetro."], ["Confundir secante y tangente", "La secante corta en dos puntos; la tangente toca en uno."], ["Pensar que una cuerda puede medir más que el diámetro", "El diámetro es la cuerda más larga."]],
     [("¿Qué diferencia hay entre circunferencia y círculo?", "La circunferencia es la línea curva; el círculo es la superficie que encierra."), ("¿Cuántas tangentes pasan por un punto de la circunferencia?", "Una sola.")],
     [("Identificar en la figura", [(lambda: S.cc_rectas("fig"), 20)]), ("Radio, diámetro y cuerdas", [(lambda: S.cc_rectas("rd", "cuerda"), 14), (cir, 6)]), ("Secante, tangente y exterior", [(lambda: S.cc_rectas("dist", "dist", "puntos"), 20)]),
      ("Relaciones entre las rectas", [(lambda: S.cc_rectas("tang", "mitad", "cuerda"), 12), (ele, 8)]), ("Repaso", [(ele, 10), (S.cc_rectas, 10)])],
     67015, lv=7)
