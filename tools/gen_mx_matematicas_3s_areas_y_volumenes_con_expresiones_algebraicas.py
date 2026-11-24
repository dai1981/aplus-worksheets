# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Expresiones algebraicas de áreas y volúmenes; despejar una variable en una fórmula."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69104))
unit("areas-y-volumenes-con-expresiones-algebraicas", 4, "6IA",
     "Representa algebraicamente áreas y volúmenes de cuerpos geométricos y calcula el valor de una variable en función de otras",
     "Áreas, volúmenes y fórmulas", "Fórmulas y despejes",
     "Ejercicios de matemáticas de 3.er grado de secundaria: expresiones algebraicas de áreas y volúmenes, despejar una variable en una fórmula y calcular su valor. 100 ejercicios con respuestas.",
     "Despejar: dejar la letra sola", "Usa la operación inversa en los dos lados.",
     ["El <b>volumen</b> de un prisma es largo × ancho × alto; con letras, x · x · (x + 2) = x³ + 2x².",
      "<b>Despejar</b> una variable es dejarla sola en un lado de la fórmula usando operaciones inversas: en A = b · h, h = A ÷ b.",
      "Después de despejar, sustituye los datos para calcular el valor."],
     [("Despeja h en A = b · h ÷ 2", ["× 2: 2A = b · h", "÷ b"], "h = 2A ÷ b"), ("V = 120, l = 5, a = 4", ["h = 120 ÷ 20"], "h = 6")],
     [["Hacer la operación en un solo lado", "Si divides entre b a la derecha, divide también a la izquierda."], ["Olvidar el orden de las operaciones al despejar", "Primero quita lo que suma o resta, después lo que multiplica."], ["Confundir área y volumen", "Área: unidades²; volumen: unidades³."]],
     [("¿Para qué sirve despejar?", "Para usar la misma fórmula con distintos datos desconocidos: el tiempo con la velocidad, la altura con el volumen…"), ("¿Cómo compruebo un despeje?", "Sustituye números en la fórmula original y en la despejada.")],
     [("Volúmenes con letras", [(lambda: S.alg_vol("vol"), 20)]), ("Áreas con letras", [(lambda: S.alg_figuras("area", "cuad"), 20)]), ("Despejar una variable", [(lambda: S.alg_vol("desp"), 8), (lambda: S.alg_vol("vol"), 12)]),
      ("Calcular con fórmulas", [(lambda: S.alg_vol("area"), 6), (lambda: S.alg_figuras("perim"), 14)]), ("Repaso", [(lambda: S.alg_figuras("exp"), 10), (lambda: S.alg_vol("vol"), 10)])],
     69004, lv=9)
