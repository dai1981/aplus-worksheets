# -*- coding: utf-8 -*-
"""México 1.er grado de secundaria (Fase 6): Resolver Ax = B, Ax + B = C y Ax + B = Cx + D con las propiedades de la igualdad."""
import random
import mx_s1 as S
from mx_common import src, unit, nomoney, noplanta  # noqa: F401

S.setup(random.Random(67108))
com, bas, dos, par = src("gen_es_matematicas_1eso_ecuaciones", 67381, "s_comprobar", "s_basica", "s_dos_miembros", "s_parentesis", lv=1)

unit("ecuaciones-lineales", 8, "6EC",
     "Resuelve ecuaciones de la forma Ax = B, Ax + B = C, Ax + B = Cx + D con el uso de las propiedades de la igualdad",
     "Ecuaciones lineales", "Ecuaciones lineales",
     "Ejercicios de matemáticas de 1.er grado de secundaria: ecuaciones de la forma Ax = B, Ax + B = C y Ax + B = Cx + D, comprobar soluciones y ecuaciones con paréntesis. 100 ejercicios con respuestas.",
     "Haz lo mismo en los dos lados", "Así la igualdad se conserva.",
     ["Una <b>ecuación</b> es una igualdad con un número desconocido. Resolverla es encontrar el valor que la hace verdadera.",
      "<b>Propiedades de la igualdad</b>: puedes sumar, restar, multiplicar o dividir los dos lados por el mismo número (distinto de 0 al dividir).",
      "Para Ax + B = Cx + D: junta las x en un lado y los números en el otro, y al final divide. <b>Comprueba</b> sustituyendo."],
     [("5x = 35", ["÷ 5 en los dos lados"], "x = 7"), ("3x + 4 = 19", ["−4: 3x = 15", "÷ 3"], "x = 5"), ("6x − 2 = 4x + 8", ["−4x: 2x − 2 = 8", "+2: 2x = 10"], "x = 5")],
     [["Cambiar el signo al dividir", "−3x = 12 → x = −4 (se divide entre −3)."], ["Hacer la operación en un solo lado", "Si restas 4 a la izquierda, resta 4 a la derecha."], ["No comprobar", "Sustituye: si no da igual, hay un error."]],
     [("¿Una ecuación siempre tiene solución?", "Las de esta forma casi siempre tienen una sola solución. Si las x se cancelan, puede no tener ninguna o tener infinitas."),
      ("¿Qué significa «despejar»?", "Dejar la incógnita sola en un lado de la igualdad.")],
     [("Comprobar soluciones", [(com, 20)]), ("Ax = B y Ax + B = C", [(bas, 20)]), ("Ax + B = Cx + D", [(dos, 20)]), ("Ecuaciones con paréntesis", [(par, 20)]), ("Repaso", [(bas, 7), (dos, 7), (par, 6)])],
     67008, lv=7)
