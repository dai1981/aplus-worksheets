# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Del lenguaje común al algebraico y viceversa; valor numérico; términos semejantes."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67107))
tra, val, mon, red, prob = src("gen_es_matematicas_1eso_lenguaje_algebraico", 67371, "s_traducir", "s_valor", "s_monomio", "s_reducir", "s_problema", lv=1, extra=(nomoney,))

unit("lenguaje-algebraico", 7, "6IA",
     "Interpreta y plantea diversas situaciones del lenguaje común al lenguaje algebraico y viceversa; calcula el valor numérico de expresiones y reduce términos semejantes",
     "Lenguaje algebraico", "Lenguaje algebraico",
     "Ejercicios de matemáticas de 1.er grado de secundaria: pasar del lenguaje común al algebraico, valor numérico, términos semejantes y expresiones en contexto. 100 ejercicios con respuestas.",
     "Una letra representa un número", "«El doble de un número más 3» = 2x + 3",
     ["En álgebra, una <b>letra</b> (x, y, n…) representa un número que no conocemos o que puede cambiar.",
      "Traduce por partes: «el doble» = 2x, «la mitad» = x/2, «el triple disminuido en 5» = 3x − 5, «dos números consecutivos» = x y x + 1.",
      "El <b>valor numérico</b> se obtiene sustituyendo la letra: si x = 4, 3x − 2 = 3 × 4 − 2 = 10. Solo se suman <b>términos semejantes</b> (misma letra y exponente)."],
     [("«El triple de un número menos 7»", ["triple: 3x", "menos 7"], "3x − 7"), ("x² + 2x con x = −3", ["9 + (−6)"], "3"), ("5a + 2b − 3a", ["5a − 3a = 2a"], "2a + 2b")],
     [["Confundir 2x con x²", "2x = x + x; x² = x × x."], ["Sumar términos no semejantes", "3x + 2y no se puede juntar."], ["Olvidar los paréntesis al sustituir", "Si x = −2, x² = (−2)² = 4."]],
     [("¿Qué es un término semejante?", "Un término con la misma parte literal: 4x² y −x² son semejantes; 4x² y 4x no."), ("¿Por qué se usan letras?", "Para escribir reglas que sirven para cualquier número, como el perímetro de un cuadrado: P = 4l.")],
     [("Del lenguaje común al algebraico", [(tra, 20)]), ("Valor numérico", [(val, 20)]), ("Términos y monomios", [(mon, 20)]), ("Reducir términos semejantes", [(red, 20)]), ("Expresiones en contexto", [(prob, 20)])],
     67007, lv=7)
