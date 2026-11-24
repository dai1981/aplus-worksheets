# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Comparar y ordenar números con signo (enteros, fracciones y decimales) y densidad."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68101))
orden = src("gen_es_matematicas_1eso_numeros_enteros", 68311, "s_orden", lv=1)
unit("numeros-con-signo-en-la-recta", 1, "6PN",
     "Compara y ordena números con signo (enteros, fracciones y decimales) en la recta numérica y analiza la propiedad de densidad",
     "Números con signo en la recta numérica", "Números con signo en la recta",
     "Ejercicios de matemáticas de 2.º grado de secundaria: comparar y ordenar números con signo enteros, fraccionarios y decimales, ubicarlos en la recta y la propiedad de densidad. 100 ejercicios con respuestas.",
     "Más a la derecha, mayor", "Entre dos números siempre hay infinitos más.",
     ["En la recta numérica, un número es <b>mayor</b> cuanto más a la derecha está: −0.5 &gt; −3/4, porque −0.5 está más cerca del 0.",
      "Para comparar fracciones y decimales con signo, pásalos a la misma forma (por ejemplo, todo a decimal) y ubícalos en la recta.",
      "<b>Densidad</b>: entre dos números racionales distintos siempre hay otro (por ejemplo, su promedio). Por eso hay infinitos números entre 0.1 y 0.2."],
     [("¿−2/3 o −0.7?", ["−2/3 ≈ −0.667", "−0.667 está más a la derecha"], "−2/3 es mayor"), ("Un número entre −1/2 y −1/4", ["Promedio: (−1/2 − 1/4) ÷ 2"], "−3/8")],
     [["Comparar negativos como positivos", "−3/4 es menor que −1/2, aunque 3/4 &gt; 1/2."], ["Pensar que no hay números entre 0.1 y 0.2", "0.15, 0.101, 0.1999… hay infinitos."], ["Contar mal las divisiones de la recta", "Fíjate en cuántas partes tiene cada unidad."]],
     [("¿Qué es la densidad de los números racionales?", "Que entre dos racionales distintos siempre puedes encontrar otro racional, y por tanto infinitos."), ("¿Los enteros son densos?", "No: entre 3 y 4 no hay ningún entero.")],
     [("Comparar enteros", [(orden, 20)]), ("Comparar fracciones y decimales", [(lambda: S.rn_recta("mayor"), 20)]), ("Ordenar números con signo", [(lambda: S.rn_recta("orden"), 20)]),
      ("La recta numérica", [(lambda: S.rn_recta("recta"), 12), (lambda: S.rn_recta("entre"), 8)]), ("Densidad", [(lambda: S.rn_recta("densidad", "entre"), 20)])],
     68001, lv=8)
