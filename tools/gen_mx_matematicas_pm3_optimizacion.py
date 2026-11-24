# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 11): problemas de optimización con derivadas."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120111))
opt_ = src("gen_es_matematicas_1bach_aplicaciones_derivadas", 120311, "s_optim", lv=1)
eco = src("gen_es_matematicas_2ccss_derivadas_y_aplicaciones", 120321, "s_economia")
unit("optimizacion", 11, ("Derivadas", 11, "Optimización"),
     "Resuelve problemas de optimización de su entorno (áreas, volúmenes, costos e ingresos) planteando una función y usando la derivada",
     "Optimización con derivadas", "Optimización",
     "Ejercicios de Pensamiento Matemático III: área máxima con un perímetro fijo, producto máximo, caja de volumen máximo, ingreso y ganancia máximos. 100 ejercicios con respuestas.",
     "Función → derivada = 0 → revisa", "El óptimo está donde f′ = 0 o en un extremo.",
     ["1. Escribe la cantidad a optimizar en función de <b>una</b> variable (usa la condición para quitar la otra).",
      "2. Deriva e iguala a 0. 3. Comprueba que es máximo o mínimo (signo de f′ o de f″) y que tiene sentido en el problema.",
      "Con un perímetro fijo, el rectángulo de área máxima es el cuadrado."],
     [("60 m de malla, área máxima", ["A(x) = x(30 − x)", "A′(x) = 30 − 2x = 0"], "cuadrado de 15 m")],
     [["Derivar con dos variables", "Primero deja todo en función de una."], ["No revisar el dominio", "Las medidas deben ser positivas."], ["Dar x y no la cantidad pedida", "Lee qué se pregunta: medida, área o ganancia."]],
     [("¿Dónde se usa la optimización?", "En empaques, rutas, producción y precios: para gastar lo menos o ganar lo más."), ("¿Siempre hay un óptimo?", "En un intervalo cerrado, una función continua siempre alcanza un máximo y un mínimo.")],
     [("Cercas y terrenos", [(lambda: S.q11("cerca"), 10), (lambda: S.q11("rio"), 10)]), ("Números", [(lambda: S.q11("producto"), 10), (opt_, 10)]),
      ("Cajas y volúmenes", [(lambda: S.q11("caja"), 10), (opt_, 10)]), ("Economía", [(eco, 14), (lambda: S.q11("ingreso"), 6)]),
      ("Repaso", [(lambda: S.q11("rio"), 8), (lambda: S.q11("cerca"), 6), (eco, 6)])],
     120011, lv=12)
