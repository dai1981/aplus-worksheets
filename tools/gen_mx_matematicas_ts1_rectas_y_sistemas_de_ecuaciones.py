# -*- coding: utf-8 -*-
"""México, Temas Selectos de Matemáticas I (progresión 4): ecuaciones de la recta y sistemas de ecuaciones por la regla de Cramer y Gauss-Jordan."""
import random
import mx_tsm as S
from mx_common import src, unit

S.setup(random.Random(130104))
ecu, pen, pos = src("gen_es_matematicas_1bach_geometria_analitica", 130304, "s_ecuaciones", "s_pendiente", "s_posicion")
gau = src("gen_es_matematicas_1bach_sistemas_metodo_de_gauss", 130314, "s_gauss", rep=[("método de Gauss", "método de Gauss-Jordan")])
unit("rectas-y-sistemas-de-ecuaciones", 4, ("Geometría analítica", 4, "Rectas y sistemas de ecuaciones"),
     "Determina ecuaciones de rectas y su posición relativa, y resuelve sistemas de ecuaciones lineales con la regla de Cramer y el método de Gauss-Jordan",
     "Rectas, regla de Cramer y Gauss-Jordan", "Rectas y sistemas",
     "Ejercicios de Temas Selectos de Matemáticas I: ecuaciones de la recta, pendiente, rectas paralelas y perpendiculares, determinantes, regla de Cramer y Gauss-Jordan. 100 ejercicios con respuestas.",
     "x = Δₓ/Δ,  y = Δᵧ/Δ", "Si Δ = 0, no hay solución única.",
     ["Una recta se escribe y = mx + b (pendiente m) o Ax + By + C = 0. Paralelas: misma pendiente; perpendiculares: m₁ · m₂ = −1.",
      "<b>Regla de Cramer</b> (2 × 2): Δ = ad − bc; Δₓ y Δᵧ cambian la columna de x o de y por los términos independientes. x = Δₓ/Δ, y = Δᵧ/Δ.",
      "<b>Gauss-Jordan</b>: se combinan ecuaciones para dejar una incógnita en cada ecuación."],
     [("2x + y = 7; x − y = 2", ["Δ = 2(−1) − 1(1) = −3", "Δₓ = −9, Δᵧ = −3"], "x = 3, y = 1")],
     [["Cambiar la columna equivocada", "Para Δₓ se sustituye la columna de x."], ["Olvidar que Δ = 0 no tiene solución única", "Las rectas son paralelas o la misma."], ["Errores de signo en ad − bc", "Multiplica en cruz con cuidado."]],
     [("¿Cuándo conviene Cramer?", "En sistemas pequeños con coeficientes enteros; para sistemas grandes se usa Gauss-Jordan."), ("¿Qué es un determinante?", "Un número que se calcula con los coeficientes; si es 0, el sistema no tiene una solución única.")],
     [("Ecuaciones de la recta", [(ecu, 10), (pen, 10)]), ("Posición de rectas", [(pos, 20)]), ("Determinantes", [(lambda: S.t4("det"), 20)]),
      ("Regla de Cramer", [(lambda: S.t4("cramer"), 12), (lambda: S.t4("x"), 8)]), ("Gauss-Jordan", [(gau, 20)])],
     130004, lv=13)
