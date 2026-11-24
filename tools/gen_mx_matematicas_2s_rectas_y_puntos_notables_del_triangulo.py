# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Alturas, medianas, mediatrices y bisectrices; ortocentro, baricentro, circuncentro e incentro."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68112))
unit("rectas-y-puntos-notables-del-triangulo", 12, "6CF",
     "Traza las rectas notables en triángulos (alturas, medianas, mediatrices y bisectrices) e identifica sus puntos de intersección",
     "Rectas y puntos notables del triángulo", "Rectas notables del triángulo",
     "Ejercicios de matemáticas de 2.º grado de secundaria: alturas, medianas, mediatrices y bisectrices de un triángulo; ortocentro, baricentro, circuncentro e incentro. 100 ejercicios con respuestas.",
     "Mediatrices → circuncentro", "Bisectrices → incentro; medianas → baricentro.",
     ["<b>Altura</b>: perpendicular desde un vértice al lado opuesto. Las tres se cortan en el <b>ortocentro</b>.",
      "<b>Mediana</b>: une un vértice con el punto medio del lado opuesto. Se cortan en el <b>baricentro</b>, que divide cada mediana en partes 2 : 1.",
      "<b>Mediatriz</b>: perpendicular a un lado por su punto medio; se cortan en el <b>circuncentro</b> (centro de la circunferencia que pasa por los vértices). <b>Bisectriz</b>: divide un ángulo en dos iguales; se cortan en el <b>incentro</b>."],
     [("Mediana de 18 cm", ["2/3 de 18"], "12 cm del vértice al baricentro"), ("Bisectriz de un ángulo de 70°", ["70 ÷ 2"], "35° y 35°")],
     [["Confundir mediana y mediatriz", "La mediana sale de un vértice; la mediatriz es perpendicular al lado."], ["Confundir altura y mediana", "La altura es perpendicular; la mediana va al punto medio."], ["Pensar que el circuncentro siempre está dentro", "En un triángulo obtusángulo queda fuera."]],
     [("¿Para qué sirve el circuncentro?", "Para encontrar un punto a la misma distancia de tres lugares, por ejemplo, dónde poner una antena para tres pueblos."), ("¿Para qué sirve el baricentro?", "Es el punto de equilibrio del triángulo.")],
     [("Las rectas notables", [(lambda: S.notables("def"), 4), (lambda: S.notables("med", "bis"), 16)]), ("Puntos notables", [(lambda: S.notables("punto", "punto2"), 9), (lambda: S.notables("bar"), 11)]),
      ("Medianas y baricentro", [(lambda: S.notables("med", "bar"), 20)]), ("Casos especiales", [(lambda: S.notables("circ", "punto2", "bis"), 20)]), ("Repaso", [(S.notables, 20)])],
     68012, lv=8)
