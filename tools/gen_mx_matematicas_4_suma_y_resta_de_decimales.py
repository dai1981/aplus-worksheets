# -*- coding: utf-8 -*-
"""México 4.º grado: Suma y resta de números decimales hasta centésimos (Suma y resta). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit, mx_text
import es_common as ES

suma, resta, mental, pesos, probl = src("gen_es_matematicas_4_suma_y_resta_de_decimales", 64213, "s1_suma", "s2_resta", "s3_mental", "s4_euros", "s5_problema")

unit("suma-y-resta-de-decimales", 11, "S",
     "Resuelve sumas y restas de números decimales hasta centésimos con el algoritmo convencional y con cálculo mental, en situaciones de dinero y medición",
     "Suma y resta de decimales", "Suma y resta de decimales",
     "Ejercicios de matemáticas de 4.º grado de primaria: sumar y restar decimales hasta centésimos en columna y de memoria, con pesos y centavos, y problemas. 100 ejercicios con respuestas.",
     "Punto debajo de punto", "Completa con ceros: 4.5 = 4.50.",
     ["Para sumar o restar decimales, escribe los números en columna con el <b>punto debajo del punto</b>: décimos bajo décimos y centésimos bajo centésimos.",
      "Si un número tiene menos decimales, complétalo con ceros: 7 − 2.35 = 7.00 − 2.35 = 4.65.",
      "Después se calcula como con números naturales y se pone el punto en el resultado, en la misma columna."],
     [("Calcula 12.5 + 3.75", ["12.50 + 3.75", "punto debajo del punto"], "16.25"), ("Paga $50 por algo de $36.40", ["50.00 − 36.40"], "$13.60")],
     [["Alinear por la derecha", "12.5 + 3.75 no es 4.00: alinea los puntos."], ["Olvidar el punto en el resultado", "Ponlo en la misma columna."], ["No completar con ceros", "7 − 2.35: piensa 7.00 − 2.35."]],
     [("¿Por qué hay que poner el punto debajo del punto?", "Para sumar décimos con décimos y centésimos con centésimos, igual que se suman unidades con unidades."),
      ("¿Cómo resto a un número entero un decimal?", "Escribe el entero con punto y ceros: 20 = 20.00. Después resta como siempre.")],
     [("Sumar decimales", [(suma, 20)]), ("Restar decimales", [(resta, 20)]), ("Cálculo mental", [(mental, 20)]), ("Pesos y centavos", [(pesos, 20)]), ("Problemas", [(probl, 20)])],
     64011, pic=mx_text(ES.vertical(["12.50", "3.75"], op="+")), lv=4)
