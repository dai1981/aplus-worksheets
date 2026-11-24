# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Jerarquía de operaciones y símbolos de agrupación con números con signo."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69101))
sin_, con, par = src("gen_es_matematicas_6_jerarquia_de_las_operaciones", 69311, "s1_sin", "s2_con", "s5_parentesis", lv=6)
unit("jerarquia-de-operaciones", 1, "6OP",
     "Aplica la jerarquía de operaciones y los símbolos de agrupación al operar con números con signo y potencias",
     "Jerarquía de operaciones", "Jerarquía de operaciones",
     "Ejercicios de matemáticas de 3.er grado de secundaria: jerarquía de operaciones con paréntesis, corchetes, potencias y números con signo. 100 ejercicios con respuestas.",
     "Paréntesis → potencias → × ÷ → + −", "Multiplica y divide de izquierda a derecha.",
     ["Primero se resuelven los <b>símbolos de agrupación</b> (paréntesis, corchetes y llaves), de adentro hacia afuera.",
      "Después las <b>potencias y raíces</b>, luego <b>multiplicaciones y divisiones</b> de izquierda a derecha y al final <b>sumas y restas</b>.",
      "Con números con signo, cuida la ley de los signos en cada paso: −2 + 3 × (−4) = −2 − 12 = −14."],
     [("5 − 2 × (−3)²", ["(−3)² = 9", "2 × 9 = 18"], "−13"), ("[4 − (−2)] × 3 − 1", ["[6] × 3 = 18"], "17")],
     [["Sumar antes de multiplicar", "2 + 3 × 4 = 14, no 20."], ["Confundir −3² con (−3)²", "−3² = −9; (−3)² = 9."], ["Dividir antes de multiplicar siempre", "Van en el orden en que aparecen."]],
     [("¿Por qué existe una jerarquía?", "Para que todos obtengamos el mismo resultado con la misma expresión."), ("¿Las calculadoras la respetan?", "Las científicas sí; las sencillas a veces no.")],
     [("Sin paréntesis", [(sin_, 20)]), ("Con paréntesis", [(con, 20)]), ("Con números con signo", [(lambda: S.jerarquia("a", "c"), 20)]), ("Con potencias", [(lambda: S.jerarquia("b"), 20)]), ("¿Dónde va el paréntesis?", [(par, 12), (S.jerarquia, 8)])],
     69001, lv=9)
