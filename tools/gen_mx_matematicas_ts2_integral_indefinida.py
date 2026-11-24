# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 4): integral indefinida de polinomios y propiedades de la integral (operador lineal)."""
import random
import mx_tsm as S
import mx_pm3 as P3
from mx_common import src, unit

S.setup(random.Random(140104))
inm, cad, pri = src("gen_es_matematicas_2bach_integrales_indefinidas", 140304, "s_inmediatas", "s_cadena", "s_primitiva", rep=[("primitivas", "antiderivadas"), ("primitiva", "antiderivada"), ("Halla ", "Encuentra ")])
unit("integral-indefinida", 4, ("Integral", 4, "Integral indefinida"),
     "Calcula integrales indefinidas de polinomios lineales y cuadráticos y de funciones sencillas, y usa la linealidad de la integral",
     "Integral indefinida y antiderivadas", "Integral indefinida",
     "Ejercicios de Temas Selectos de Matemáticas II: antiderivadas de polinomios, integrales inmediatas, linealidad, constante de integración y antiderivada que pasa por un punto. 100 ejercicios con respuestas.",
     "∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C", "Integrar deshace la derivada.",
     ["Una <b>antiderivada</b> de f es una F con F′ = f. La <b>integral indefinida</b> ∫ f(x) dx = F(x) + C reúne todas.",
      "Regla de la potencia: ∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C (n ≠ −1). <b>Linealidad</b>: ∫ (af + bg) dx = a∫ f dx + b∫ g dx.",
      "Para encontrar C se usa un dato: un punto por el que pasa F."],
     [("∫ (6x² − 4x + 3) dx", ["6x³/3 − 4x²/2 + 3x"], "2x³ − 2x² + 3x + C")],
     [["Olvidar + C", "Hay infinitas antiderivadas."], ["Multiplicar por el exponente en vez de dividir", "Se sube el exponente y se divide entre él."], ["No comprobar", "Deriva tu resultado: debe dar f."]],
     [("¿Por qué la integral es un operador lineal?", "Porque la integral de una suma es la suma de las integrales y las constantes salen fuera."), ("¿Cómo compruebo una integral?", "Derivando el resultado.")],
     [("Antiderivadas de polinomios", [(lambda: P3.q15("anti"), 20)]), ("Integrales inmediatas", [(inm, 20)]), ("Cambio de variable sencillo", [(cad, 20)]),
      ("Constante de integración", [(pri, 20)]), ("Repaso", [(inm, 10), (lambda: P3.q15("anti"), 10)])],
     140004, lv=14)
