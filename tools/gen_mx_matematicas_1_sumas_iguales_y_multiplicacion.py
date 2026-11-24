# -*- coding: utf-8 -*-
"""México 1.er grado: Sumas de sumandos iguales y multiplicaciones hasta 10 con arreglos rectangulares (Construcción de la noción de multiplicación y división). Preguntas propias y España 1.º/2.º con otra semilla."""
import random
from mx_common import src, unit
from mx_12 import BIG, s_iguales, all_le

sumas, filas = src("gen_es_matematicas_3_tablas_de_multiplicar", 61701, "s_sumas", "s_filas", lv=1, mx_=BIG, extra=(all_le(10),))
mult = src("gen_es_matematicas_2_problemas", 61702, "s_mult", lv=1, mx_=BIG, extra=(all_le(10),))
doble = src("gen_es_matematicas_2_mitades", 61703, "s_doble", lv=1, mx_=BIG, extra=(all_le(10),))
ig = s_iguales(random.Random(61107))

unit("sumas-iguales-y-multiplicacion", 7, "P3",
     "Resuelve problemas de multiplicación con resultados hasta 10 usando material concreto, sumas repetidas o arreglos rectangulares y el signo ×; distingue las sumas de sumandos iguales de las de sumandos diferentes",
     "Sumas iguales y multiplicación", "Sumas iguales",
     "Ejercicios de matemáticas de 1.er grado de primaria: sumas de sumandos iguales, grupos iguales, filas y columnas, el signo × y dobles hasta 10. 100 ejercicios con respuestas.",
     "3 veces 2 es 2 + 2 + 2", "Se escribe 3 × 2 = 6.",
     ["Cuando sumas varias veces el mismo número, es una <b>suma de sumandos iguales</b>: 2 + 2 + 2.",
      "Se puede escribir más corto con el signo <b>×</b>: 2 + 2 + 2 = 3 × 2 = 6 (tres veces dos).",
      "En un <b>arreglo</b> de filas y columnas, multiplica las filas por los objetos de cada fila."],
     [("4 grupos de 2 lápices", ["2 + 2 + 2 + 2", "4 × 2"], "8 lápices"), ("2 filas de 5 sillas", ["5 + 5"], "10 sillas")],
     [["Sumar el número de grupos y el de objetos", "3 grupos de 2 no son 3 + 2: son 2 + 2 + 2."], ["Contar mal los grupos", "Tacha cada grupo al contarlo."], ["Pensar que 2 + 3 es suma de iguales", "Los sumandos deben ser el mismo número."]],
     [("¿Qué significa 3 × 2?", "Tres veces dos: 2 + 2 + 2 = 6."), ("¿Qué es el doble de un número?", "Es el número dos veces: el doble de 4 es 4 + 4 = 8.")],
     [("Grupos iguales", [(sumas, 20)]), ("Filas y columnas", [(filas, 20)]), ("¿Sumandos iguales?", [(ig, 20)]), ("Dobles", [(doble, 20)]), ("Problemas", [(mult, 6), (ig, 14)])],
     61007, lv=1)
