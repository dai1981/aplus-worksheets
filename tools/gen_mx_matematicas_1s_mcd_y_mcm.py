# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Criterios de divisibilidad, números primos, MCD y mcm."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67105))
mult, prim, fac, mcd, prob = src("gen_es_matematicas_1eso_divisibilidad", 67351, "s_multiplos", "s_primos", "s_factor", "s_mcd", "s_problema", lv=1, extra=(nomoney,))

unit("mcd-y-mcm", 5, "6OP",
     "Usa criterios de divisibilidad y números primos al resolver problemas que impliquen calcular el máximo común divisor (MCD) y el mínimo común múltiplo (mcm)",
     "Divisibilidad, MCD y mcm", "MCD y mcm",
     "Ejercicios de matemáticas de 1.er grado de secundaria: criterios de divisibilidad, números primos, descomposición en factores primos, máximo común divisor y mínimo común múltiplo. 100 ejercicios con respuestas.",
     "MCD reparte; mcm hace coincidir", "Descompón en factores primos primero.",
     ["<b>Criterios de divisibilidad</b>: entre 2 si termina en cifra par; entre 3 si la suma de sus cifras es múltiplo de 3; entre 5 si termina en 0 o 5.",
      "Un <b>número primo</b> solo tiene dos divisores: 1 y él mismo (2, 3, 5, 7, 11…). Todo número se descompone en factores primos: 60 = 2² × 3 × 5.",
      "<b>MCD</b>: factores comunes con el menor exponente (repartir en partes iguales lo más grandes posible). <b>mcm</b>: todos los factores con el mayor exponente (cuándo vuelven a coincidir)."],
     [("MCD(24, 36)", ["24 = 2³ × 3", "36 = 2² × 3²", "comunes, menor exponente: 2² × 3"], "12"), ("mcm(6, 8)", ["2 × 3 y 2³", "2³ × 3"], "24")],
     [["Confundir MCD y mcm", "El MCD nunca es mayor que los números; el mcm nunca es menor."], ["Decir que 1 es primo", "El 1 tiene un solo divisor: no es primo."], ["Olvidar factores", "mcm(4, 6) = 12, no 24."]],
     [("¿Cuándo uso el MCD?", "Cuando quieres repartir o cortar en partes iguales lo más grandes posible."), ("¿Cuándo uso el mcm?", "Cuando dos cosas se repiten con distinta frecuencia y quieres saber cuándo coinciden.")],
     [("Múltiplos, divisores y criterios", [(mult, 20)]), ("Números primos", [(prim, 20)]), ("Factores primos", [(fac, 20)]), ("MCD y mcm", [(mcd, 20)]), ("Problemas", [(prob, 20)])],
     67005, lv=7)
