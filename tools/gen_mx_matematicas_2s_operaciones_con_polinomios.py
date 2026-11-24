# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Monomios y polinomios: sumar, restar y multiplicar."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68106))
mon, ope, fc = src("gen_es_matematicas_2eso_polinomios", 68351, "s_monomios", "s_operar", "s_factor_comun", lv=2, extra=(lambda it: "÷ (x" not in it["q"],))
red = src("gen_es_matematicas_1eso_lenguaje_algebraico", 68352, "s_reducir", lv=1)
unit("operaciones-con-polinomios", 6, "6IA",
     "Usa las propiedades de los exponentes en operaciones algebraicas: suma, resta y multiplicación de monomios y polinomios",
     "Operaciones con monomios y polinomios", "Operaciones con polinomios",
     "Ejercicios de matemáticas de 2.º grado de secundaria: sumar, restar, multiplicar y dividir monomios, operaciones con polinomios y factor común. 100 ejercicios con respuestas.",
     "Suma solo términos semejantes", "Al multiplicar, suma los exponentes.",
     ["Para <b>sumar o restar</b> polinomios, junta los términos semejantes (misma letra y exponente). Al restar, cambia el signo de todos los términos del segundo.",
      "Para <b>multiplicar monomios</b>, multiplica los coeficientes y suma los exponentes: (3x²)(4x³) = 12x⁵.",
      "Para multiplicar un monomio por un polinomio, usa la propiedad distributiva. El <b>factor común</b> es el camino de regreso: 6x + 9 = 3(2x + 3)."],
     [("(5x² − 2x) − (x² + 4x)", ["5x² − x² = 4x²", "−2x − 4x = −6x"], "4x² − 6x"), ("(−2x³)(5x)", ["−2 · 5 = −10", "3 + 1 = 4"], "−10x⁴")],
     [["No cambiar todos los signos al restar", "−(x² + 4x) = −x² − 4x."], ["Multiplicar los exponentes", "x² · x³ = x⁵, no x⁶."], ["Juntar términos no semejantes", "3x² + 2x no se puede simplificar."]],
     [("¿Qué es un polinomio?", "Una suma de monomios, como 3x² − 5x + 1."), ("¿Qué es el grado de un polinomio?", "El mayor exponente de la variable.")],
     [("Reducir términos", [(red, 20)]), ("Multiplicar y dividir monomios", [(mon, 20)]), ("Sumar y restar polinomios", [(ope, 20)]), ("Factor común", [(fc, 20)]), ("Repaso", [(mon, 7), (ope, 7), (fc, 6)])],
     68006, lv=8)
