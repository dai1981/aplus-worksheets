# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 1): lenguaje natural y lenguaje matemático, proposiciones, conectivos y negación."""
import random
import mx_pm2 as S
from mx_common import src, unit

S.setup(random.Random(110101))
tra = src("gen_es_matematicas_1eso_lenguaje_algebraico", 110301, "s_traducir")
unit("lenguaje-natural-y-lenguaje-matematico", 1, ("Lenguaje y álgebra", 1, "Lenguaje natural y lenguaje matemático"),
     "Distingue el lenguaje natural del matemático, traduce enunciados a símbolos, reconoce proposiciones y su valor de verdad, conectivos lógicos, cuantificadores y negaciones",
     "Lenguaje matemático y lógica", "Lenguaje matemático",
     "Ejercicios de Pensamiento Matemático II: traducir enunciados a lenguaje algebraico, proposiciones verdaderas o falsas, conectivos lógicos, negación y contraejemplos. 100 ejercicios con respuestas.",
     "Cada palabra tiene un solo sentido", "«Todos» se niega con «al menos uno no».",
     ["En matemáticas cada frase tiene un solo significado. «El doble de un número aumentado en 5» es 2x + 5, pero «el doble de la suma de un número y 5» es 2(x + 5).",
      "Una <b>proposición</b> es una frase que es verdadera o falsa. Se unen con conectivos: ∧ (y), ∨ (o), → (si…, entonces), ↔ (si y solo si), ¬ (no).",
      "Para negar: «todos» → «al menos uno no»; «p y q» → «no p o no q». Un solo <b>contraejemplo</b> basta para mostrar que una frase general es falsa."],
     [("«Todos los primos son impares»", ["2 es primo y es par"], "falsa (contraejemplo: 2)"), ("Negación de «llueve y hace frío»", ["¬(p ∧ q) = ¬p ∨ ¬q"], "no llueve o no hace frío")],
     [["Traducir en el orden de las palabras", "Primero identifica qué operación se hace al final."], ["Negar «todos» con «ninguno»", "La negación es «al menos uno no»."], ["Pensar que p → q es falsa si p es falsa", "Si p es falsa, p → q es verdadera."]],
     [("¿Por qué «si p, entonces q» es verdadera cuando p es falsa?", "Porque la promesa solo se rompe si ocurre p y no ocurre q."),
      ("¿Para qué sirve la lógica en matemáticas?", "Para razonar sin ambigüedad y demostrar que una afirmación es verdadera para todos los casos.")],
     [("Traducir a símbolos", [(lambda: S.lp1("trad"), 12), (tra, 8)]), ("Verdadera o falsa", [(lambda: S.lp1("valor"), 14), (lambda: S.lp1("contra"), 3), (lambda: S.lp1("conn"), 3)]),
      ("Conectivos y valores de verdad", [(lambda: S.lp1("verdad"), 18), (lambda: S.lp1("conn"), 2)]), ("Negaciones", [(lambda: S.lp1("neg"), 12), (tra, 8)]),
      ("Repaso", [(lambda: S.lp1("verdad"), 6), (tra, 14)])],
     110001, lv=11)
