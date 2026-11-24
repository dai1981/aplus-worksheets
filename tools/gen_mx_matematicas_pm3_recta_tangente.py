# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 2): el problema de la recta tangente: secantes que se acercan a la tangente."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120102))
tan = src("gen_es_matematicas_1bach_derivadas", 120302, "s_tangente", lv=1, rep=[("Halla la recta tangente", "Encuentra la recta tangente")])
unit("recta-tangente", 2, ("Variación y funciones", 2, "El problema de la recta tangente"),
     "Comprende de forma intuitiva el problema de la recta tangente: las rectas secantes se acercan a la tangente y su pendiente es la razón de cambio instantánea",
     "Rectas secantes y recta tangente", "Recta tangente",
     "Ejercicios de Pensamiento Matemático III: pendiente de rectas secantes, cómo se acercan a la tangente, pendiente de la tangente y su ecuación. 100 ejercicios con respuestas.",
     "Tangente: límite de secantes", "Su pendiente es f′(a).",
     ["Una <b>secante</b> pasa por dos puntos de la curva; su pendiente es [f(a + h) − f(a)] ÷ h.",
      "Si h se hace cada vez más pequeño, las secantes se acercan a la <b>tangente</b> en x = a. Su pendiente es la derivada f′(a).",
      "Ecuación de la tangente: y − f(a) = f′(a)(x − a)."],
     [("f(x) = x², secantes desde x = 3", ["h = 1: 7; h = 0.1: 6.1; h = 0.01: 6.01"], "pendiente de la tangente 6")],
     [["Usar un solo punto para la secante", "Se necesitan dos puntos."], ["Olvidar f(a) en la ecuación", "La recta pasa por (a, f(a))."], ["Creer que la tangente solo toca en un punto siempre", "Puede volver a cortar la curva lejos."]],
     [("¿Por qué es importante la tangente?", "Porque su pendiente dice qué tan rápido cambia la función en ese instante."),
      ("¿Toda curva tiene tangente?", "No en todos sus puntos: en un pico o una esquina no hay una sola tangente.")],
     [("Pendiente de una secante", [(lambda: S.q2("secante"), 20)]), ("Secantes que se acercan", [(lambda: S.q2("acerca"), 20)]),
      ("Pendiente de la tangente", [(lambda: S.q2("pend"), 15), (lambda: S.q2("concepto"), 5)]), ("Ecuación de la tangente", [(lambda: S.q2("ecuacion"), 20)]),
      ("Más tangentes", [(tan, 20)])],
     120002, lv=12)
