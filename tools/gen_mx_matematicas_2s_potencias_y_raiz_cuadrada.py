# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Potencias, propiedades de los exponentes y raíz cuadrada."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68103))
val, prop, raiz, prob = src("gen_es_matematicas_1eso_potencias_y_raices", 68331, "s_valor", "s_prop", "s_raiz", "s_problema", lv=1, extra=(nomoney,))
rai2 = src("gen_es_matematicas_2eso_potencias", 68332, "s_raices", lv=2, extra=(lambda it: "√(" not in it["q"],))
unit("potencias-y-raiz-cuadrada", 3, "6OP",
     "Calcula potencias con exponente entero, aplica sus propiedades y obtiene raíces cuadradas exactas y aproximadas",
     "Potencias y raíz cuadrada", "Potencias y raíces",
     "Ejercicios de matemáticas de 2.º grado de secundaria: potencias de números con signo, propiedades de las potencias, raíz cuadrada exacta y aproximada y problemas. 100 ejercicios con respuestas.",
     "aᵐ · aⁿ = aᵐ⁺ⁿ", "√49 = 7 porque 7² = 49.",
     ["Una <b>potencia</b> es una multiplicación repetida: 2⁵ = 2 × 2 × 2 × 2 × 2 = 32. Con base negativa, el resultado es positivo si el exponente es par.",
      "<b>Propiedades</b>: aᵐ · aⁿ = aᵐ⁺ⁿ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐ·ⁿ; a⁰ = 1.",
      "La <b>raíz cuadrada</b> es la operación inversa de elevar al cuadrado. Si no es exacta, se ubica entre dos enteros: √50 está entre 7 y 8."],
     [("(−2)⁴", ["(−2)(−2)(−2)(−2)"], "16"), ("3⁵ ÷ 3²", ["5 − 2 = 3"], "3³ = 27"), ("√90", ["9² = 81, 10² = 100"], "entre 9 y 10")],
     [["Multiplicar base por exponente", "4³ = 64, no 12."], ["Confundir (−3)² y −3²", "(−3)² = 9; −3² = −9."], ["Multiplicar exponentes al multiplicar potencias", "2³ · 2⁴ = 2⁷, no 2¹²."]],
     [("¿Por qué a⁰ = 1?", "Porque aⁿ ÷ aⁿ = 1 y, por la propiedad del cociente, también es a⁰."), ("¿Un número negativo tiene raíz cuadrada?", "No entre los números reales: ningún número al cuadrado da negativo.")],
     [("Calcular potencias", [(val, 20)]), ("Propiedades de las potencias", [(prop, 20)]), ("Raíz cuadrada", [(raiz, 20)]), ("Raíces aproximadas", [(rai2, 12), (raiz, 8)]), ("Problemas", [(prob, 20)])],
     68003, lv=8)
