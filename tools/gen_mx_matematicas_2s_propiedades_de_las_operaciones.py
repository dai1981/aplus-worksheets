# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Propiedades conmutativa, asociativa y distributiva."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68102))
dis = src("gen_es_matematicas_6_jerarquia_de_las_operaciones", 68321, "s3_distrib", lv=6)
unit("propiedades-de-las-operaciones", 2, "6OP",
     "Comprueba y argumenta si las operaciones cumplen las propiedades conmutativa, asociativa y distributiva",
     "Propiedades de las operaciones", "Propiedades de las operaciones",
     "Ejercicios de matemáticas de 2.º grado de secundaria: propiedades conmutativa, asociativa y distributiva con números con signo, elemento neutro, inverso y cálculo mental. 100 ejercicios con respuestas.",
     "a(b + c) = ab + ac", "La suma y la multiplicación son conmutativas.",
     ["<b>Conmutativa</b>: el orden no cambia el resultado en la suma y la multiplicación (a + b = b + a). En la resta y la división, sí cambia.",
      "<b>Asociativa</b>: puedes agrupar como quieras en la suma y la multiplicación: (a + b) + c = a + (b + c).",
      "<b>Distributiva</b>: a(b + c) = ab + ac. Sirve para calcular mentalmente (7 × 99 = 7 × 100 − 7) y en álgebra."],
     [("−3(x − 5)", ["−3 · x = −3x", "−3 · (−5) = +15"], "−3x + 15"), ("25 × 37 × 4", ["25 × 4 = 100"], "3 700")],
     [["Distribuir solo al primer término", "4(x + 3) = 4x + 12, no 4x + 3."], ["Olvidar el signo al distribuir un negativo", "−2(x − 4) = −2x + 8."], ["Creer que la resta es conmutativa", "8 − 3 ≠ 3 − 8."]],
     [("¿Para qué sirven las propiedades?", "Para calcular más fácil y para transformar expresiones algebraicas sin cambiar su valor."), ("¿La división es asociativa?", "No: (24 ÷ 4) ÷ 2 = 3, pero 24 ÷ (4 ÷ 2) = 12.")],
     [("¿Qué propiedad es?", [(lambda: S.prop_ops("cual"), 20)]), ("Propiedades y contraejemplos", [(lambda: S.prop_ops("resta"), 6), (lambda: S.prop_ops("cual"), 14)]), ("Propiedad distributiva", [(lambda: S.prop_ops("dist"), 20)]),
      ("Cálculo mental", [(lambda: S.prop_ops("calc"), 12), (dis, 8)]), ("Repaso", [(S.prop_ops, 14), (dis, 6)])],
     68002, lv=8)
