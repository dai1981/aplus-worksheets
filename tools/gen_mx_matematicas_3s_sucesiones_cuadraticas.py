# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Sucesiones con progresión cuadrática de figuras y números."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69102))
unit("sucesiones-cuadraticas", 2, "6RP",
     "Representa algebraicamente una sucesión con progresión cuadrática de figuras y números",
     "Sucesiones cuadráticas", "Sucesiones cuadráticas",
     "Ejercicios de matemáticas de 3.er grado de secundaria: sucesiones cuadráticas de números y figuras, segundas diferencias, regla general an² + bn + c y términos. 100 ejercicios con respuestas.",
     "Segunda diferencia constante → n²", "Si es 2, empieza con n²; si es 4, con 2n².",
     ["En una sucesión <b>cuadrática</b>, las primeras diferencias no son constantes, pero las <b>segundas diferencias</b> sí.",
      "Si la segunda diferencia es d, la regla empieza con (d ÷ 2)n². Después ajustas con bn + c para que coincidan los primeros términos.",
      "Ejemplo: 3, 6, 11, 18, 27… diferencias 3, 5, 7, 9 y segunda diferencia 2: regla n² + 2."],
     [("2, 5, 10, 17", ["Diferencias 3, 5, 7", "Segunda 2: n²", "n² + 1"], "n² + 1"), ("Término 10 de n² + 1", ["100 + 1"], "101")],
     [["Usar la primera diferencia como si fuera lineal", "Si las diferencias cambian, no es aritmética."], ["Olvidar dividir la segunda diferencia entre 2", "Segunda diferencia 6 → 3n²."], ["No comprobar", "Prueba la regla con n = 1, 2 y 3."]],
     [("¿Dónde aparecen las sucesiones cuadráticas?", "En figuras cuadradas, en el área de cuadrados y en la caída libre de objetos."), ("¿Qué pasa si la segunda diferencia tampoco es constante?", "Entonces no es cuadrática; puede ser cúbica u otra.")],
     [("Siguiente término", [(lambda: S.seq_cuad("sig"), 20)]), ("Segundas diferencias", [(lambda: S.seq_cuad("dif2"), 20)]), ("Regla general", [(lambda: S.seq_cuad("gen"), 20)]),
      ("Calcular términos", [(lambda: S.seq_cuad("term"), 20)]), ("Sucesiones de figuras", [(lambda: S.seq_cuad("fig"), 20)])],
     69002, lv=9)
