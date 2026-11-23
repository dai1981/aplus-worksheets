# -*- coding: utf-8 -*-
"""México 3.er grado: Tablas de multiplicar (Multiplicación y división; repertorio multiplicativo). Reutiliza España 3.º con otra semilla."""
from mx_common import src, unit
import importlib

M = "gen_es_matematicas_3_tablas_de_multiplicar"
m = importlib.import_module(M)
sumas, filas, serie, falta, probl = src(M, 63106, "s_sumas", "s_filas", "s_serie", "s_falta", "s_problema", lv=3)
import mx_common as X
t257 = X.mx(m.s_tabla([2, 5, 10]))
t346 = X.mx(m.s_tabla([3, 4, 6]))
t789 = X.mx(m.s_tabla([7, 8, 9]))

unit("tablas-de-multiplicar", 5, "P",
     "Construye y usa el repertorio multiplicativo de los factores de una cifra (tablas del 1 al 10); relaciona la multiplicación con la suma repetida y con arreglos rectangulares",
     "Las tablas de multiplicar", "Tablas de multiplicar",
     "Ejercicios de matemáticas de 3.er grado de primaria: tablas de multiplicar del 2 al 9, el factor que falta, sucesiones y problemas. 100 ejercicios con respuestas.",
     "4 × 3 = 3 + 3 + 3 + 3", "El orden de los factores no cambia el producto.",
     ["Multiplicar es sumar varias veces el mismo número: 4 × 3 = 3 + 3 + 3 + 3 = 12.",
      "El orden no importa: 4 × 3 = 3 × 4. Si te sabes una, te sabes la otra.",
      "Trucos: la tabla del 4 es el doble de la del 2; la del 8, el doble de la del 4; en la del 9, las cifras del resultado suman 9 (9 × 6 = 54)."],
     [("7 × 8", ["7 × 4 = 28", "el doble de 28"], "56"), ("¿Qué número falta? 6 × ___ = 42", ["¿Qué número por 6 da 42?"], "7")],
     [["Confundir × con +", "6 × 3 = 18, no 9."], ["Saltarse un número al contar", "Recita la tabla en orden: 6, 12, 18, 24…"], ["Pensar que el orden cambia el resultado", "3 × 7 = 7 × 3 = 21."]],
     [("¿Cómo aprendo las tablas más rápido?", "Empieza por las del 2, 5 y 10. Usa que el orden no importa: si sabes 3 × 8, ya sabes 8 × 3. Así quedan muy pocas por memorizar."),
      ("¿Qué es un arreglo rectangular?", "Objetos en filas y columnas iguales. 4 filas de 6 son 4 × 6 = 24.")],
     [("Tablas del 2, 5 y 10", [(t257, 20)]), ("Tablas del 3, 4 y 6", [(t346, 20)]), ("Tablas del 7, 8 y 9", [(t789, 20)]),
      ("El factor que falta y las sucesiones", [(falta, 14), (serie, 6)]), ("Problemas", [(probl, 20)])], 63005)
