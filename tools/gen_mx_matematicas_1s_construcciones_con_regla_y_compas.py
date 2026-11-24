# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Punto medio, mediatriz, bisectriz, perpendiculares, paralelas y triángulos con regla y compás."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67113))
unit("construcciones-con-regla-y-compas", 13, "6CF",
     "Utiliza la regla y el compás para trazar: punto medio, mediatriz de un segmento, segmentos y ángulos congruentes, bisectriz de un ángulo, rectas perpendiculares y paralelas; verifica la existencia de triángulos",
     "Construcciones con regla y compás", "Regla y compás",
     "Ejercicios de matemáticas de 1.er grado de secundaria: punto medio, mediatriz, bisectriz, perpendiculares, paralelas, segmentos congruentes y construcción de triángulos con regla y compás. 100 ejercicios con respuestas.",
     "Mediatriz: mismo lado a A que a B", "Bisectriz: divide el ángulo en dos iguales.",
     ["La <b>mediatriz</b> de un segmento es la recta perpendicular que pasa por su <b>punto medio</b>. Cada punto de la mediatriz está a la misma distancia de los dos extremos.",
      "La <b>bisectriz</b> divide un ángulo en dos ángulos iguales. Con el compás también se copian segmentos y ángulos <b>congruentes</b> (iguales).",
      "Un triángulo solo existe si cada lado es <b>menor que la suma</b> de los otros dos (desigualdad del triángulo)."],
     [("Mediatriz de un segmento de 9 cm", ["Corta en el punto medio"], "4.5 cm a cada lado"), ("Bisectriz de 128°", ["128 ÷ 2"], "64° y 64°"), ("¿Triángulo de 3, 4 y 9 cm?", ["3 + 4 = 7 &lt; 9"], "no existe")],
     [["Cerrar el compás entre un arco y otro", "Para la mediatriz, los dos arcos deben tener el mismo radio."], ["Confundir mediatriz y bisectriz", "La mediatriz es de un segmento; la bisectriz, de un ángulo."], ["No revisar si el triángulo existe", "Con lados 2, 3 y 6 no se cierra."]],
     [("¿Por qué el compás sirve para la mediatriz?", "Porque un arco reúne los puntos a la misma distancia de su centro; donde se cortan los arcos de A y B, los puntos están a la misma distancia de los dos."),
      ("¿Qué es un segmento congruente?", "Un segmento que mide lo mismo que otro.")],
     [("Punto medio y mediatriz", [(lambda: S.cf_construccion("med", "medP", "medio"), 20)]), ("Bisectriz", [(lambda: S.cf_construccion("bis", "bis2"), 20)]),
      ("Perpendiculares y paralelas", [(lambda: S.cf_construccion("perp", "par", "par", "instr"), 20)]),
      ("Segmentos congruentes y triángulos", [(lambda: S.cf_construccion("copia", "compas", "equi", "exist", "exist"), 20)]), ("Repaso", [(S.cf_construccion, 20)])],
     67013, lv=7)
