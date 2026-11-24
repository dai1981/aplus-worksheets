# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 6): los números reales: conjuntos, decimales, irracionales, orden, densidad y propiedades de campo."""
import random
import mx_pm2 as S
from mx_common import src, unit

S.setup(random.Random(110106))
tip, irr, fd, gen, orde, rea = src("gen_es_matematicas_3eso_numeros_reales", 110306, "s_tipo_num", "s_cual_irr", "s_frac_dec", "s_generatriz", "s_ordenar", "s_reales", lv=3)
unit("numeros-reales", 6, ("Números", 6, "Los números reales"),
     "Reconoce la estructura de los números reales: naturales, enteros, racionales e irracionales, su expresión decimal, su orden y densidad, y las propiedades de campo de sus operaciones",
     "Números reales y sus propiedades", "Números reales",
     "Ejercicios de Pensamiento Matemático II: clasificar números, decimales exactos y periódicos, fracción generatriz, irracionales, orden, densidad y propiedades de campo. 100 ejercicios con respuestas.",
     "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ", "Los irracionales completan la recta.",
     ["<b>Naturales</b> ℕ (1, 2, 3…) ⊂ <b>enteros</b> ℤ (con negativos y 0) ⊂ <b>racionales</b> ℚ (fracciones) ⊂ <b>reales</b> ℝ.",
      "Un racional tiene decimal exacto o periódico. Un <b>irracional</b> (√2, π) tiene infinitas cifras sin periodo.",
      "En ℝ valen las <b>propiedades de campo</b>: conmutativa, asociativa, distributiva, neutros (0 y 1) e inversos. Entre dos reales siempre hay otro (densidad)."],
     [("0.<span class='ov'>36</span> como fracción", ["x = 0.3636…", "100x − x = 36", "x = 36/99"], "4/11")],
     [["Creer que √9 es irracional", "√9 = 3 es entero."], ["Pensar que 0.333… no es racional", "Es 1/3."], ["Olvidar que el inverso de 0 no existe", "No se puede dividir entre 0."]],
     [("¿π es igual a 3.14?", "No; 3.14 es una aproximación. π es irracional: sus cifras no terminan ni se repiten."),
      ("¿Qué significa que ℝ es un campo ordenado?", "Que sus operaciones cumplen las propiedades de campo y que se pueden comparar: dados dos reales, uno es mayor o son iguales.")],
     [("Conjuntos de números", [(tip, 10), (irr, 10)]), ("Decimales y fracciones", [(fd, 8), (gen, 12)]), ("Orden y densidad", [(orde, 10), (lambda: S.lp6("densidad"), 6), (lambda: S.lp6("orden"), 4)]),
      ("Propiedades de campo", [(lambda: S.lp6("prop"), 8), (lambda: S.lp6("ejemplo"), 12)]), ("Inversos y repaso", [(lambda: S.lp6("inverso"), 12), (rea, 8)])],
     110006, lv=11)
