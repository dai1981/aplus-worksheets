# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 3): modelación algebraica: plantear y resolver ecuaciones a partir de problemas."""
import random
import mx_s1 as S1
from mx_common import src, unit

S1.setup(random.Random(110103))
pro, dos, par = src("gen_es_matematicas_1eso_ecuaciones", 110303, "s_problema", "s_dos_miembros", "s_parentesis", lv=2)
lpro = src("gen_es_matematicas_1eso_lenguaje_algebraico", 110313, "s_problema")
unit("modelacion-algebraica", 3, ("Lenguaje y álgebra", 3, "Modelación algebraica"),
     "Traduce problemas de su entorno a expresiones y ecuaciones algebraicas, las resuelve e interpreta la solución en el contexto",
     "Modelación con ecuaciones", "Modelación algebraica",
     "Ejercicios de Pensamiento Matemático II: escribir expresiones a partir de figuras, plantear ecuaciones de problemas, resolver ecuaciones lineales y comprobar la solución. 100 ejercicios con respuestas.",
     "Incógnita → ecuación → solución", "Comprueba la respuesta en el problema.",
     ["1. Elige la incógnita: «sea x el número de…». 2. Escribe la ecuación con los datos. 3. Resuélvela. 4. Comprueba en el problema.",
      "Para resolver: quita paréntesis, junta las x de un lado y los números del otro, y divide entre el coeficiente.",
      "Interpreta: una edad o una cantidad de personas no puede ser negativa ni decimal."],
     [("Tres números consecutivos suman 72", ["x + (x + 1) + (x + 2) = 72", "3x + 3 = 72", "x = 23"], "23, 24 y 25")],
     [["No definir la incógnita", "Escribe qué representa x."], ["Olvidar comprobar", "Sustituye en el enunciado, no solo en la ecuación."], ["Pasar un término sin cambiar el signo", "Lo que suma pasa restando."]],
     [("¿Qué hago si la solución no tiene sentido?", "Revisa el planteamiento: puede haber un error, o el problema no tiene solución en ese contexto."),
      ("¿Siempre hay una ecuación?", "No: a veces hacen falta dos ecuaciones (un sistema) o una desigualdad.")],
     [("Expresiones de figuras", [(lpro, 20)]), ("Resolver ecuaciones", [(dos, 10), (par, 10)]), ("Plantear y resolver", [(pro, 20)]),
      ("Problemas del entorno", [(S1.ec_problem, 20)]), ("Repaso", [(pro, 10), (S1.ec_problem, 10)])],
     110003, lv=11)
