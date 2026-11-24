# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Sumar, restar, multiplicar y dividir fracciones y decimales."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67104))
suma, mult, prob = src("gen_es_matematicas_1eso_fracciones", 67341, "s_suma", "s_mult", "s_problema", lv=1, extra=(nomoney,))
ops = src("gen_es_matematicas_1eso_numeros_decimales", 67342, "s_ops", lv=1)
comb = src("gen_es_matematicas_2eso_fracciones_y_decimales", 67343, "s_comb", lv=2)

unit("operaciones-con-fracciones-y-decimales", 4, "6OP",
     "Reconoce el significado de las cuatro operaciones básicas y sus relaciones inversas; resuelve problemas con números fraccionarios y decimales",
     "Operaciones con fracciones y decimales", "Fracciones y decimales: operaciones",
     "Ejercicios de matemáticas de 1.er grado de secundaria: suma, resta, multiplicación y división de fracciones y decimales, operaciones combinadas y problemas. 100 ejercicios con respuestas.",
     "Iguala denominadores para sumar", "Para dividir, multiplica por el recíproco.",
     ["Para <b>sumar o restar fracciones</b>, usa un denominador común (el mcm) y suma los numeradores.",
      "Para <b>multiplicar</b>, numerador por numerador y denominador por denominador. Para <b>dividir</b>, multiplica por el recíproco del divisor.",
      "Con <b>decimales</b>, para sumar alinea el punto; para multiplicar, cuenta las cifras decimales de los factores."],
     [("2/3 + 1/4", ["mcm = 12", "8/12 + 3/12"], "11/12"), ("3/5 ÷ 9/10", ["3/5 × 10/9 = 30/45"], "2/3"), ("1.2 × 0.3", ["12 × 3 = 36", "2 cifras decimales"], "0.36")],
     [["Sumar denominadores", "1/2 + 1/3 no es 2/5: es 5/6."], ["Dividir sin invertir", "a/b ÷ c/d = a/b × d/c."], ["Mal el punto al multiplicar", "0.4 × 0.2 = 0.08, no 0.8."]],
     [("¿Qué es el recíproco?", "La fracción invertida: el recíproco de 3/7 es 7/3. Un número por su recíproco da 1."),
      ("¿Cómo sumo una fracción y un decimal?", "Pasa los dos a la misma forma: 1/4 + 0.5 = 0.25 + 0.5 = 0.75.")],
     [("Sumar y restar fracciones", [(suma, 20)]), ("Multiplicar y dividir fracciones", [(mult, 20)]), ("Operaciones con decimales", [(ops, 20)]),
      ("Operaciones combinadas", [(comb, 20)]), ("Problemas", [(prob, 20)])],
     67004, lv=7)
