# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 6): la circunferencia en la geometría analítica."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130106))
cir = src("gen_es_matematicas_1bach_conicas", 130306, "s_circ", rep=[("Halla ", "Encuentra ")])
unit("circunferencia", 6, ("Cónicas", 6, "La circunferencia"),
     "Obtiene la ecuación ordinaria y general de la circunferencia, su centro y radio, y la posición de un punto respecto a ella",
     "Ecuación de la circunferencia", "Circunferencia",
     "Ejercicios de Temas Selectos de Matemáticas I: ecuación ordinaria y general de la circunferencia, centro y radio, completar cuadrados, diámetro y posición de un punto. 100 ejercicios con respuestas.",
     "(x − h)² + (y − k)² = r²", "Centro (h, k) y radio r.",
     ["La <b>circunferencia</b> son los puntos a distancia r del centro (h, k): (x − h)² + (y − k)² = r².",
      "Al desarrollar se obtiene la forma <b>general</b> x² + y² + Dx + Ey + F = 0. Para volver a la ordinaria se <b>completan cuadrados</b>.",
      "Un punto está dentro si su distancia al centro es menor que r, sobre ella si es igual y fuera si es mayor."],
     [("x² + y² − 6x + 4y − 12 = 0", ["(x − 3)² − 9 + (y + 2)² − 4 = 12", "(x − 3)² + (y + 2)² = 25"], "centro (3, −2), radio 5")],
     [["Tomar r² como el radio", "r = √(r²)."], ["Errores de signo en el centro", "(x + 4)² corresponde a h = −4."], ["Olvidar sumar lo mismo de los dos lados al completar", "Lo que agregas a un lado, agrégalo al otro."]],
     [("¿Toda ecuación x² + y² + Dx + Ey + F = 0 es una circunferencia?", "No: si al completar cuadrados el lado derecho queda negativo, no hay puntos."), ("¿Cómo se calcula el centro con el diámetro?", "Es el punto medio de sus extremos.")],
     [("Ecuación ordinaria", [(lambda: S.t6("ecuacion"), 20)]), ("Centro y radio", [(lambda: S.t6("centro"), 20)]), ("Forma general", [(lambda: S.t6("general"), 20)]),
      ("Posición y diámetro", [(lambda: S.t6("punto"), 10), (lambda: S.t6("diametro"), 10)]), ("Más circunferencias", [(cir, 20)])],
     130006, lv=13)
