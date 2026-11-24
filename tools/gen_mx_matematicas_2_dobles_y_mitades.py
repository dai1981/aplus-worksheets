# -*- coding: utf-8 -*-
"""México 2.º grado: Dobles, mitades, triples y cuartos (Construcción de la noción de multiplicación y división). Reutiliza España 2.º con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

doble, mitad, parte, cuantas, probl = src("gen_es_matematicas_2_mitades", 62901, "s_doble", "s_mitad", "s_parte", "s_cuantas", "s_problema", lv=2, mx_=BIG)

unit("dobles-y-mitades", 9, "P3",
     "Calcula mentalmente dobles y mitades, triples y la cuarta parte de números naturales; reparte en dos, tres y cuatro partes iguales",
     "Dobles, mitades y cuartos", "Dobles y mitades",
     "Ejercicios de matemáticas de 2.º grado de primaria: el doble y la mitad, la tercera y la cuarta parte, partes iguales de una figura y problemas. 100 ejercicios con respuestas.",
     "Doble: × 2. Mitad: entre 2", "La mitad de 18 es 9, porque 9 + 9 = 18.",
     ["El <b>doble</b> de un número es ese número dos veces: el doble de 15 es 15 + 15 = 30.",
      "La <b>mitad</b> es repartir entre 2: la mitad de 30 es 15. El doble y la mitad son operaciones contrarias.",
      "Una figura partida en 2 partes iguales tiene dos <b>medios</b>; en 4 partes iguales, cuatro <b>cuartos</b>."],
     [("Doble de 23", ["20 + 20 = 40", "3 + 3 = 6"], "46"), ("Mitad de 48", ["mitad de 40 = 20", "mitad de 8 = 4"], "24")],
     [["Confundir doble y mitad", "El doble es más grande; la mitad, más pequeña."], ["Partes que no son iguales", "Medios y cuartos deben ser del mismo tamaño."], ["Olvidar las decenas", "Doble de 23 = 46, no 26."]],
     [("¿Cómo calculo la mitad de un número de dos cifras?", "Saca la mitad de las decenas y la de las unidades: la mitad de 46 es 20 + 3 = 23."), ("¿Qué es un cuarto?", "Una de 4 partes iguales de un entero.")],
     [("El doble", [(doble, 20)]), ("La mitad", [(mitad, 20)]), ("Partes iguales", [(parte, 20)]), ("¿Cuántas partes?", [(cuantas, 20)]), ("Problemas", [(probl, 20)])],
     62009, lv=2)
