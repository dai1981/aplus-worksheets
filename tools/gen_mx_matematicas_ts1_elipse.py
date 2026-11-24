# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 7): la elipse como sección cónica; aplicaciones a órbitas planetarias."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130107))
eli = src("gen_es_matematicas_1bach_conicas", 130307, "s_elipse", rep=[("Halla ", "Encuentra ")])
unit("elipse", 7, ("Cónicas", 7, "La elipse"),
     "Reconoce la elipse como lugar geométrico, determina ejes, focos y excentricidad a partir de su ecuación y la relaciona con las órbitas de los planetas",
     "Elipse: ejes, focos y excentricidad", "Elipse",
     "Ejercicios de Temas Selectos de Matemáticas I: ecuación de la elipse, eje mayor y menor, focos, relación a² = b² + c², excentricidad y órbitas planetarias. 100 ejercicios con respuestas.",
     "(x − h)²/a² + (y − k)²/b² = 1", "c² = a² − b²;  e = c/a",
     ["La <b>elipse</b> son los puntos cuya suma de distancias a dos puntos fijos (<b>focos</b>) es constante: 2a.",
      "En (x − h)²/a² + (y − k)²/b² = 1 con a &gt; b, el eje mayor mide 2a y el menor 2b. Los focos están a c del centro, con c² = a² − b².",
      "La <b>excentricidad</b> e = c/a está entre 0 y 1: cerca de 0 es casi un círculo; cerca de 1, muy alargada."],
     [("x²/25 + y²/9 = 1", ["a = 5, b = 3", "c = √(25 − 9) = 4"], "focos (±4, 0), e = 0.8")],
     [["Confundir a con a²", "En el denominador está a²."], ["Sumar en vez de restar para c", "c² = a² − b²."], ["Poner los focos en el eje menor", "Siempre están sobre el eje mayor."]],
     [("¿Dónde está el Sol en la órbita de la Tierra?", "En uno de los focos de la elipse (primera ley de Kepler)."), ("¿Una circunferencia es una elipse?", "Sí, una elipse con a = b y excentricidad 0.")],
     [("Ejes", [(lambda: S.t7("ejes"), 20)]), ("Focos", [(lambda: S.t7("focos"), 14), (lambda: S.t7("c"), 6)]), ("Excentricidad", [(lambda: S.t7("exc"), 20)]),
      ("Más elipses", [(eli, 20)]), ("Órbitas y propiedades", [(lambda: S.t7("orbita"), 6), (lambda: S.t7("exc"), 8), (eli, 6)])],
     130007, lv=13)
