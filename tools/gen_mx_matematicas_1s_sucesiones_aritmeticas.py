# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Sucesiones con progresión aritmética de figuras y números y su expresión algebraica."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67106))
gen, pat, ari, prob = src("gen_es_matematicas_3eso_sucesiones", 67361, "s_general", "s_patron", "s_aritmetica", "s_problema", lv=3, extra=(S.arit, lambda it: "sueldo" not in it["q"] and "bote" not in it["q"]))

unit("sucesiones-aritmeticas", 6, "6RP",
     "Representa algebraicamente una sucesión con progresión aritmética de figuras y números; encuentra términos y su regla general",
     "Sucesiones aritméticas: la regla general", "Sucesiones aritméticas",
     "Ejercicios de matemáticas de 1.er grado de secundaria: sucesiones con progresión aritmética de números y figuras, diferencia, término general y problemas. 100 ejercicios con respuestas.",
     "Término n = diferencia × n + ajuste", "En 5, 8, 11… la regla es 3n + 2.",
     ["En una sucesión <b>aritmética</b>, cada término se obtiene sumando siempre la misma cantidad: la <b>diferencia</b> d.",
      "La regla general es d × n + (primer término − d). En 5, 8, 11, 14…, d = 3 y la regla es 3n + 2: el término 10 es 3 × 10 + 2 = 32.",
      "Con <b>figuras</b>, cuenta cuántos elementos se agregan en cada paso: esa es la diferencia."],
     [("4, 7, 10, 13, …", ["d = 3", "4 − 3 = 1"], "3n + 1"), ("Término 20 de 3n + 1", ["3 × 20 + 1"], "61")],
     [["Usar el primer término como ajuste", "En 5, 8, 11 no es 3n + 5: es 3n + 2."], ["Confundir el lugar con el valor", "n es la posición (1.º, 2.º, 3.º…), no el número."], ["Sumar en vez de multiplicar", "El término 50 no se obtiene sumando 50 veces a mano: usa la regla."]],
     [("¿Qué es una progresión aritmética?", "Una sucesión en la que la diferencia entre términos consecutivos es siempre la misma."), ("¿Para qué sirve la regla general?", "Para calcular cualquier término sin escribir todos los anteriores.")],
     [("Siguiente término", [(pat, 20)]), ("Sucesiones de figuras", [(lambda: S.sc_figuras("cuenta", "lugar"), 20)]), ("Regla general", [(lambda: S.sc_figuras("regla"), 10), (gen, 10)]), ("Calcular términos", [(ari, 20)]),
      ("Problemas", [(S.sc_contexto, 12), (prob, 8)])],
     67006, lv=7)
