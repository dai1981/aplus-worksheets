# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático III (progresión 3): funciones reales de variable real: operaciones, composición e inversa para modelar situaciones de cambio."""
import random
import mx_pm3 as S
from mx_common import src, unit

S.setup(random.Random(120103))
dom, com, inv, tro = src("gen_es_matematicas_1bach_funciones", 120303, "s_dominio", "s_composicion", "s_inversa", "s_trozos")
mod = src("gen_es_matematicas_1ccss_funciones", 120313, "s_modelos")
unit("modelacion-con-funciones", 3, ("Variación y funciones", 3, "Modelación con funciones"),
     "Modela situaciones de cambio con funciones reales de variable real y opera con ellas: suma, resta, producto, cociente, composición e inversa",
     "Operaciones y composición de funciones", "Modelación con funciones",
     "Ejercicios de Pensamiento Matemático III: dominio, suma, producto y cociente de funciones, composición f(g(x)), función inversa y modelos de situaciones reales. 100 ejercicios con respuestas.",
     "(f ∘ g)(x) = f(g(x))", "Primero se aplica g, luego f.",
     ["Con dos funciones se forman otras: (f + g)(x) = f(x) + g(x), (f · g)(x) = f(x) · g(x), (f/g)(x) = f(x) ÷ g(x) con g(x) ≠ 0.",
      "La <b>composición</b> f(g(x)) encadena procesos: por ejemplo, piezas producidas en t horas y costo de esas piezas.",
      "El <b>dominio</b> son los valores de x permitidos: no se divide entre 0 ni se saca raíz cuadrada de negativos."],
     [("f(x) = 2x + 1, g(x) = x²", ["f(g(3)) = f(9) = 19", "g(f(3)) = g(7) = 49"], "19 y 49: el orden importa")],
     [["Pensar que f(g(x)) = g(f(x))", "La composición no es conmutativa."], ["Multiplicar en vez de componer", "f(g(x)) no es f(x) · g(x)."], ["Olvidar los ceros del denominador", "Quítalos del dominio."]],
     [("¿Qué es una función real de variable real?", "Una regla que a cada número real x de su dominio le asigna un único número real f(x)."),
      ("¿Para qué sirve la inversa?", "Para regresar: si f convierte °C en °F, su inversa convierte °F en °C.")],
     [("Dominio", [(dom, 20)]), ("Suma, producto y cociente", [(lambda: S.q3("suma"), 7), (lambda: S.q3("prod"), 7), (lambda: S.q3("coc"), 6)]),
      ("Composición", [(com, 10), (lambda: S.q3("comp"), 5), (lambda: S.q3("comp2"), 5)]), ("Inversa y a trozos", [(inv, 12), (tro, 8)]),
      ("Modelos", [(mod, 14), (lambda: S.q3("modelo"), 6)])],
     120003, lv=12)
