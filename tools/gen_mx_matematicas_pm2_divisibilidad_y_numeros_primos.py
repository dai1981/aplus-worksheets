# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 4): divisibilidad, criterios de divisibilidad, números primos y factorización prima."""
import random
from mx_common import src, unit

mul, pri, fac = src("gen_es_matematicas_1eso_divisibilidad", 110304, "s_multiplos", "s_primos", "s_factor")
unit("divisibilidad-y-numeros-primos", 4, ("Números", 4, "Divisibilidad y números primos"),
     "Explica las relaciones entre números enteros con la divisibilidad, los criterios de divisibilidad, los números primos y la descomposición en factores primos",
     "Divisibilidad y números primos", "Divisibilidad y primos",
     "Ejercicios de Pensamiento Matemático II: múltiplos y divisores, criterios de divisibilidad, reconocer números primos y descomponer en factores primos. 100 ejercicios con respuestas.",
     "Todo entero es producto de primos", "Y esa descomposición es única.",
     ["a es <b>divisor</b> de b si b ÷ a es exacta; entonces b es <b>múltiplo</b> de a.",
      "Criterios: entre 2 si termina en par; entre 3 si la suma de cifras es múltiplo de 3; entre 5 si termina en 0 o 5; entre 9 si la suma de cifras es múltiplo de 9.",
      "Un <b>número primo</b> solo tiene dos divisores: 1 y él mismo. Todo entero mayor que 1 se descompone de forma única en primos (teorema fundamental de la aritmética)."],
     [("Factoriza 180", ["180 = 2 × 90 = 2 × 2 × 45", "45 = 3 × 3 × 5"], "2² × 3² × 5"), ("¿Es 91 primo?", ["91 = 7 × 13"], "no")],
     [["Creer que 1 es primo", "Un primo tiene exactamente dos divisores."], ["Pensar que todo impar es primo", "9, 15, 21 y 91 no son primos."], ["Dejar factores compuestos", "Sigue dividiendo hasta tener solo primos."]],
     [("¿Hasta dónde pruebo para saber si un número es primo?", "Basta probar con los primos menores o iguales a su raíz cuadrada."),
      ("¿Hay infinitos números primos?", "Sí; Euclides lo demostró hace más de 2 000 años.")],
     [("Múltiplos y divisores", [(mul, 20)]), ("Números primos", [(pri, 20)]), ("Factores primos", [(fac, 20)]),
      ("Repaso de divisibilidad", [(mul, 12), (pri, 8)]), ("Repaso", [(fac, 8), (pri, 6), (mul, 6)])],
     110004, lv=11)
