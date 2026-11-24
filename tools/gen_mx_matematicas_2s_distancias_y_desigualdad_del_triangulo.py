# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Distancia de un punto a una recta, entre paralelas y desigualdad del triángulo."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68115))
unit("distancias-y-desigualdad-del-triangulo", 15, "6ME",
     "Calcula la distancia de un punto a una recta y entre dos rectas paralelas; explora la desigualdad del triángulo",
     "Distancias y desigualdad del triángulo", "Desigualdad del triángulo",
     "Ejercicios de matemáticas de 2.º grado de secundaria: distancia de un punto a una recta, distancia entre paralelas y desigualdad del triángulo. 100 ejercicios con respuestas.",
     "La perpendicular es lo más corto", "Cada lado &lt; suma de los otros dos.",
     ["La <b>distancia de un punto a una recta</b> se mide sobre la perpendicular: es el segmento más corto.",
      "La <b>distancia entre dos paralelas</b> es la longitud de un segmento perpendicular a las dos; es la misma en todos lados.",
      "<b>Desigualdad del triángulo</b>: cada lado es menor que la suma de los otros dos y mayor que su diferencia. Con lados 5 y 8, el tercero está entre 3 y 13."],
     [("Lados 7 y 12", ["12 − 7 = 5", "12 + 7 = 19"], "entre 5 y 19"), ("¿Triángulo de 4, 5 y 10?", ["4 + 5 = 9 &lt; 10"], "no existe")],
     [["Medir la distancia con un segmento inclinado", "Siempre es la perpendicular."], ["Incluir los límites", "Con lados 3 y 5, el tercero no puede medir 8: queda plano."], ["Olvidar la diferencia", "El tercer lado también debe ser mayor que la diferencia."]],
     [("¿Por qué el camino recto es más corto?", "Por la desigualdad del triángulo: ir por un tercer punto siempre suma más."), ("¿Las paralelas se cortan?", "No: siempre están a la misma distancia.")],
     [("Tercer lado posible", [(lambda: S.distancias("rango"), 20)]), ("¿Qué medida sirve?", [(lambda: S.distancias("tercer"), 20)]), ("Distancia a una recta", [(lambda: S.distancias("punto", "paral"), 20)]),
      ("Caminos más cortos", [(lambda: S.distancias("corto"), 12), (lambda: S.distancias("tercer"), 8)]), ("Repaso", [(S.distancias, 20)])],
     68015, lv=8)
