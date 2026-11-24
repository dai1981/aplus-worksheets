# -*- coding: utf-8 -*-
"""México 3.er grado de secundaria (Fase 6): Reparto proporcional directo e inverso."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(69108))
unit("reparto-proporcional", 8, "6FU",
     "Explora procedimientos para resolver problemas de reparto proporcional",
     "Reparto proporcional", "Reparto proporcional",
     "Ejercicios de matemáticas de 3.er grado de secundaria: reparto proporcional directo entre dos y tres personas, razones y reparto inversamente proporcional. 100 ejercicios con respuestas.",
     "Suma las partes y divide", "Cada parte vale total ÷ número de partes.",
     ["En un <b>reparto proporcional directo</b>, quien aporta más recibe más. Suma las partes de la razón: si es 2 : 3, hay 5 partes.",
      "Divide el total entre el número de partes para saber cuánto vale una parte; luego multiplica por las partes de cada uno.",
      "En un <b>reparto inverso</b>, quien tiene más (faltas, tiempo) recibe menos: se reparte en proporción a 1/a y 1/b."],
     [("$900 en razón 2 : 3 : 4", ["9 partes", "1 parte = $100"], "$200, $300 y $400"), ("$1 200 inverso a 1 y 3 faltas", ["1/1 : 1/3 = 3 : 1", "4 partes de $300"], "$900 y $300")],
     [["Repartir en partes iguales", "Si aportaron distinto, no toca lo mismo."], ["Dividir entre el número de personas", "Se divide entre el número de partes."], ["Olvidar invertir en el reparto inverso", "Más faltas, menos premio."]],
     [("¿Cómo compruebo un reparto?", "Las partes deben sumar el total y guardar la razón."), ("¿Dónde se usa?", "Para repartir ganancias de un negocio, gastos de un viaje o premios.")],
     [("Entre dos personas", [(lambda: S.reparto("dir"), 20)]), ("Entre tres personas", [(lambda: S.reparto("tres"), 20)]), ("Reparto inverso", [(lambda: S.reparto("inv"), 20)]),
      ("Problemas", [(lambda: S.reparto("dir", "tres"), 20)]), ("Repaso", [(S.reparto, 20)])],
     69008, lv=9)
