# -*- coding: utf-8 -*-
"""México 2.º grado de secundaria (Fase 6): Sistemas de dos ecuaciones lineales con dos incógnitas."""
import random
import re  # noqa: F401
import mx_s2 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(68108))
com, res, comp, tipo, gra, prob = src("gen_es_matematicas_2eso_sistemas", 68361, "s_comprobar", "s_resolver", "s_complejo", "s_tipo", "s_grafica", "s_problema", lv=2, extra=(nomoney,))
unit("sistemas-de-ecuaciones", 8, "6EC",
     "Modela y resuelve sistemas de dos ecuaciones lineales con dos incógnitas por algún método (igualación, sustitución, suma y resta o gráfico)",
     "Sistemas de ecuaciones lineales 2 × 2", "Sistemas de ecuaciones",
     "Ejercicios de matemáticas de 2.º grado de secundaria: sistemas de dos ecuaciones con dos incógnitas por sustitución, igualación, suma y resta y método gráfico, y problemas. 100 ejercicios con respuestas.",
     "La solución cumple las dos", "En la gráfica, es donde se cruzan las rectas.",
     ["Un <b>sistema</b> de dos ecuaciones lineales busca los valores de x e y que cumplen las dos al mismo tiempo.",
      "<b>Sustitución</b>: despeja una letra y sustitúyela en la otra ecuación. <b>Igualación</b>: despeja la misma letra en las dos e iguala. <b>Suma y resta</b>: suma las ecuaciones para eliminar una letra.",
      "<b>Método gráfico</b>: cada ecuación es una recta; la solución es el punto donde se cortan. Si son paralelas, no hay solución."],
     [("x + y = 10, x − y = 4", ["Sumamos: 2x = 14", "x = 7, y = 3"], "(7, 3)"), ("y = 2x, x + y = 9", ["x + 2x = 9"], "x = 3, y = 6")],
     [["Comprobar solo en una ecuación", "La solución debe cumplir las dos."], ["Olvidar multiplicar todos los términos", "Para eliminar, multiplica toda la ecuación."], ["Confundir el orden (x, y)", "Primero va x, después y."]],
     [("¿Un sistema siempre tiene solución?", "No: si las rectas son paralelas no tiene; si son la misma recta, tiene infinitas."), ("¿Qué método es mejor?", "El que te deje menos cuentas: si una letra ya está despejada, usa sustitución.")],
     [("Comprobar soluciones", [(com, 20)]), ("Sustitución e igualación", [(res, 20)]), ("Suma y resta", [(comp, 20)]), ("Método gráfico y tipos", [(gra, 6), (tipo, 14)]), ("Problemas", [(prob, 20)])],
     68008, lv=8)
