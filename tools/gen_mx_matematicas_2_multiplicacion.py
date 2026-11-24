# -*- coding: utf-8 -*-
"""México 2.º grado: Multiplicación de números naturales menores que 10: grupos iguales, arreglos y cálculo mental (Construcción de la noción de multiplicación y división). Reutiliza España 2.º con otra semilla."""
from mx_common import src, unit
import re
from mx_12 import BIG, plain


def menor10(it):
    return not re.search(r"×\s*10\b|\b10\s*×|grupos de 10|del 10\b", plain(it))


sumas, filas, serie, falta, probl = src("gen_es_matematicas_3_tablas_de_multiplicar", 62701, "s_sumas", "s_filas", "s_serie", "s_falta", "s_problema", lv=2, mx_=BIG, extra=(menor10,))
mult = src("gen_es_matematicas_2_problemas", 62702, "s_mult", lv=2, mx_=BIG, extra=(menor10,))

unit("multiplicacion", 7, "P3",
     "Calcula mentalmente multiplicaciones de números naturales menores que 10 con diversas estrategias (sumas repetidas, arreglos, dobles); resuelve problemas de multiplicación",
     "Multiplicación: grupos iguales y tablas", "Multiplicación",
     "Ejercicios de matemáticas de 2.º grado de primaria: grupos iguales, filas y columnas, contar de 2 en 2 y de 5 en 5, tablas y problemas. 100 ejercicios con respuestas.",
     "4 × 3 = 3 + 3 + 3 + 3", "Multiplicar es sumar grupos iguales.",
     ["<b>Multiplicar</b> es sumar varias veces el mismo número: 4 × 3 son 4 grupos de 3 = 3 + 3 + 3 + 3 = 12.",
      "En un arreglo de filas y columnas: 3 filas de 5 = 3 × 5 = 15. El orden no cambia el resultado: 3 × 5 = 5 × 3.",
      "Para recordar las tablas, cuenta de 2 en 2, de 3 en 3 o de 5 en 5."],
     [("5 bolsas con 4 naranjas", ["4 + 4 + 4 + 4 + 4", "5 × 4"], "20 naranjas"), ("6 × 2", ["el doble de 6"], "12")],
     [["Sumar los factores", "4 × 3 no es 7."], ["Contar un grupo de más", "Cuenta los grupos con cuidado."], ["Olvidar que 3 × 5 = 5 × 3", "El orden de los factores no cambia el producto."]],
     [("¿Qué significa 6 × 4?", "Seis veces cuatro: 4 + 4 + 4 + 4 + 4 + 4 = 24."), ("¿Cuál es una estrategia para 7 × 2?", "Piensa en el doble de 7: 7 + 7 = 14.")],
     [("Grupos iguales", [(sumas, 20)]), ("Filas y columnas", [(filas, 20)]), ("Contar de 2 en 2, de 3 en 3 y de 5 en 5", [(serie, 20)]), ("El factor que falta", [(falta, 20)]), ("Problemas", [(probl, 10), (mult, 10)])],
     62007, lv=2)
