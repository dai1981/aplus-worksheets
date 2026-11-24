# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas II (progresión 7): métodos numéricos: bisección, aproximaciones sucesivas y Newton-Raphson."""
import random
import mx_tsm as S
import mx_pm3 as P3
from mx_common import unit

S.setup(random.Random(140107))
unit("metodos-numericos", 7, ("Modelos y métodos numéricos", 7, "Métodos numéricos"),
     "Aproxima soluciones de ecuaciones con los métodos de bisección, aproximaciones sucesivas y Newton-Raphson, y reconoce la sensibilidad a las condiciones iniciales",
     "Bisección, punto fijo y Newton-Raphson", "Métodos numéricos",
     "Ejercicios de Temas Selectos de Matemáticas II: localizar raíces, método de bisección, aproximaciones sucesivas, método de Newton-Raphson y cuándo fallan. 100 ejercicios con respuestas.",
     "xₙ₊₁ = xₙ − f(xₙ) ÷ f′(xₙ)", "Newton usa la tangente; bisección, la mitad.",
     ["<b>Bisección</b>: si f cambia de signo en [a, b], se evalúa el punto medio y se conserva la mitad donde sigue el cambio de signo.",
      "<b>Aproximaciones sucesivas</b>: se escribe la ecuación como x = g(x) y se itera xₙ₊₁ = g(xₙ) hasta que se estabiliza.",
      "<b>Newton-Raphson</b>: xₙ₊₁ = xₙ − f(xₙ)/f′(xₙ). Es muy rápido, pero depende del punto inicial."],
     [("√5 con f(x) = x² − 5 y x₀ = 2", ["f(2) = −1, f′(2) = 4", "x₁ = 2 + 1/4"], "x₁ = 2.25 (√5 ≈ 2.236)")],
     [["Quedarse con la mitad sin cambio de signo", "El cero está donde f cambia de signo."], ["Olvidar el signo menos en Newton", "Es xₙ − f/f′."], ["Usar Newton con f′ = 0", "No se puede dividir entre 0: cambia de punto inicial."]],
     [("¿Cuál método es mejor?", "Bisección siempre funciona pero es lenta; Newton es rápido pero puede fallar si la tangente es casi horizontal."), ("¿Dónde se usan?", "En calculadoras, computadoras e ingeniería para resolver ecuaciones que no tienen fórmula.")],
     [("Localizar raíces", [(lambda: P3.q6("intervalo"), 20)]), ("Método de bisección", [(lambda: S.u7("biseccion"), 20)]), ("Aproximaciones sucesivas", [(lambda: S.u7("punto_fijo"), 20)]),
      ("Newton-Raphson", [(lambda: S.u7("newton"), 20)]), ("Comparar métodos", [(lambda: S.u7("concepto"), 6), (lambda: S.u7("newton"), 7), (lambda: S.u7("biseccion"), 7)])],
     140007, lv=14)
