# -*- coding: utf-8 -*-
"""México, Pensamiento Matemático II (progresión 13): sistemas de ecuaciones lineales 2 × 2: resolución, interpretación geométrica y problemas."""
import random
from mx_common import src, unit

com, res, tip, gra, pro = src("gen_es_matematicas_2eso_sistemas", 110313, "s_comprobar", "s_resolver", "s_tipo", "s_grafica", "s_problema", lv=2,
                              rep=[("compatible determinado (una solución)", "una solución (las rectas se cortan)"), ("incompatible (ninguna solución)", "ninguna solución (rectas paralelas)"),
                                   ("compatible indeterminado (infinitas soluciones)", "infinitas soluciones (la misma recta)")])
unit("sistemas-de-ecuaciones-lineales", 13, ("Funciones y sistemas", 13, "Sistemas de ecuaciones lineales"),
     "Resuelve sistemas de dos ecuaciones lineales con dos incógnitas por métodos algebraicos y gráficos, e interpreta geométricamente sus soluciones",
     "Sistemas de ecuaciones lineales 2 × 2", "Sistemas de ecuaciones",
     "Ejercicios de Pensamiento Matemático II: comprobar soluciones, resolver por sustitución, igualación y eliminación, solución gráfica, tipos de sistemas y problemas. 100 ejercicios con respuestas.",
     "La solución es el punto de corte", "Paralelas: sin solución.",
     ["Un sistema 2 × 2 son dos ecuaciones con x e y. La solución es el par (x, y) que cumple las dos.",
      "Métodos: <b>sustitución</b> (despeja y sustituye), <b>igualación</b> y <b>eliminación</b> (suma o resta para cancelar una incógnita).",
      "Cada ecuación es una recta: si se cortan hay <b>una solución</b>; si son paralelas, <b>ninguna</b>; si son la misma recta, <b>infinitas</b>."],
     [("x + y = 10; x − y = 4", ["Sumando: 2x = 14", "x = 7; y = 3"], "(7, 3)")],
     [["Comprobar solo en una ecuación", "Debe cumplir las dos."], ["Errores de signo al restar ecuaciones", "Resta término a término con cuidado."], ["Confundir x con y en la respuesta", "Escribe el par en orden (x, y)."]],
     [("¿Qué método es mejor?", "El que deje cuentas más sencillas: sustitución si una incógnita ya está despejada, eliminación si los coeficientes son opuestos."),
      ("¿Cómo sé si no tiene solución sin graficar?", "Si al eliminar llegas a algo imposible como 0 = 5.")],
     [("Comprobar soluciones", [(com, 20)]), ("Resolver", [(res, 20)]), ("Interpretación gráfica", [(gra, 12), (tip, 8)]),
      ("Tipos de sistemas", [(tip, 12), (res, 8)]), ("Problemas", [(pro, 20)])],
     110013, lv=11)
