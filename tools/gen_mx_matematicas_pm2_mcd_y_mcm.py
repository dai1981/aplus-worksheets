# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 5): máximo común divisor y mínimo común múltiplo, y problemas."""
import random
from mx_common import src, unit

mcd, pro, fac = src("gen_es_matematicas_1eso_divisibilidad", 110305, "s_mcd", "s_problema", "s_factor")
unit("mcd-y-mcm", 5, ("Números", 5, "Máximo común divisor y mínimo común múltiplo"),
     "Calcula el máximo común divisor y el mínimo común múltiplo de dos o más enteros y los usa para resolver problemas de repartos y coincidencias",
     "MCD y mcm con problemas", "MCD y mcm",
     "Ejercicios de Pensamiento Matemático II: máximo común divisor y mínimo común múltiplo con factores primos, y problemas de repartos, cortes y coincidencias. 100 ejercicios con respuestas.",
     "MCD: repartir. mcm: coincidir.", "Usa la factorización prima.",
     ["<b>MCD</b>: factores primos comunes con el menor exponente. <b>mcm</b>: todos los factores con el mayor exponente.",
      "Problemas de <b>repartir</b> o cortar en partes iguales lo más grandes posible → MCD.",
      "Problemas de <b>coincidir</b> otra vez (camiones, alarmas, vueltas) → mcm. Siempre: MCD(a, b) × mcm(a, b) = a × b."],
     [("MCD(24, 36) y mcm(24, 36)", ["24 = 2³ × 3; 36 = 2² × 3²", "MCD = 2² × 3", "mcm = 2³ × 3²"], "12 y 72")],
     [["Confundir cuándo usar MCD o mcm", "Partes iguales grandes: MCD. Volver a coincidir: mcm."], ["Tomar el mayor exponente para el MCD", "MCD usa el menor."], ["Multiplicar los números para el mcm", "Solo si no tienen factores comunes."]],
     [("¿Qué son números primos entre sí?", "Números cuyo MCD es 1, como 8 y 15."), ("¿Cómo compruebo mi resultado?", "MCD × mcm debe ser igual al producto de los dos números.")],
     [("Factorizar primero", [(fac, 20)]), ("Calcular MCD y mcm", [(mcd, 20)]), ("Problemas", [(pro, 20)]),
      ("Más problemas", [(pro, 20)]), ("Repaso", [(mcd, 10), (pro, 10)])],
     110005, lv=11)
