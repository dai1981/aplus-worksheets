# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático I (progresión 4): técnicas de conteo (principio multiplicativo, permutaciones, combinaciones) y probabilidad."""
import random
import mx_pm1 as S
from mx_common import src, unit

S.setup(random.Random(100104))
mul, fac, var, com, ele = src("gen_es_matematicas_4eso_combinatoria", 100304, "s_multiplicativo", "s_factorial", "s_variaciones", "s_combinaciones", "s_elegir",
                              rep=[("Variaciones con repetición", "Permutaciones con repetición"), ("variaciones con repetición", "permutaciones con repetición"), (" primeros, ", " entradas, "), (" segundos y ", " platos fuertes y "),
                                   ("Variaciones sin repetición", "Permutaciones de n en k"), ("variaciones sin repetición", "permutaciones de n en k"),
                                   ("variaciones", "permutaciones de n en k"), ("Variaciones", "Permutaciones de n en k"), ("quiniela", "quiniela de fútbol"), ("V<sub>", "P<sub>")])
unit("tecnicas-de-conteo", 4, ("Probabilidad", 4, "Técnicas de conteo"),
     "Utiliza técnicas de conteo (diagramas de árbol, principio multiplicativo, permutaciones y combinaciones) para contar los resultados de un experimento y calcular probabilidades de eventos simples",
     "Técnicas de conteo: permutaciones y combinaciones", "Técnicas de conteo",
     "Ejercicios de Pensamiento Matemático I: principio multiplicativo, factorial, permutaciones con y sin repetición, combinaciones y cuándo usar cada una. 100 ejercicios con respuestas.",
     "¿Importa el orden? ¿Se repite?", "Orden: permutación. Sin orden: combinación.",
     ["<b>Principio multiplicativo</b>: si una elección tiene m opciones y otra n, juntas tienen m × n.",
      "<b>Permutaciones</b> (importa el orden): n! = n × (n − 1) × … × 1; de n en k: n!/(n − k)!.",
      "<b>Combinaciones</b> (no importa el orden): C(n, k) = n!/(k!(n − k)!)."],
     [("Playera (3) y pantalón (4)", ["3 × 4"], "12 formas"), ("Elegir 2 de 5 sabores", ["C(5, 2) = 5 × 4 ÷ 2"], "10")],
     [["Usar permutación cuando el orden no importa", "Pregúntate si AB y BA son distintos."], ["Sumar en vez de multiplicar", "Etapas sucesivas se multiplican."], ["Calcular 0! = 0", "0! = 1."]],
     [("¿Qué es un factorial?", "n! es el producto de todos los enteros de 1 a n. Por ejemplo, 4! = 24."),
      ("¿Cómo distingo permutación de combinación?", "Si cambiar el orden da un resultado distinto (un podio, una contraseña), es permutación; si no (un equipo), es combinación.")],
     [("Principio multiplicativo", [(mul, 20)]), ("Factorial", [(fac, 20)]), ("Permutaciones", [(var, 20)]), ("Combinaciones", [(com, 20)]),
      ("¿Qué técnica uso?", [(ele, 20)])],
     100004, lv=10)
