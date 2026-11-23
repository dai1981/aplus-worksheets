# -*- coding: utf-8 -*-
"""México 4.º grado: Problemas de varias operaciones con números de hasta cinco cifras (Multiplicación y división). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit

par, sr, mu, dv, op = src("gen_es_matematicas_4_problemas_de_dos_operaciones", 64215, "s1_parentesis", "s2_suma_resta", "s3_mult", "s4_div", "s5_operacion", mx_=99999)

unit("problemas", 7, "P",
     "Resuelve problemas de dos o más pasos con sumas, restas, multiplicaciones y divisiones de números naturales; elige las operaciones y comprueba si el resultado es razonable",
     "Problemas de varias operaciones", "Problemas",
     "Ejercicios de matemáticas de 4.º grado de primaria: problemas de dos pasos con suma, resta, multiplicación y división, operaciones con paréntesis y elegir la operación. 100 ejercicios con respuestas.",
     "Lee, planea, calcula y comprueba", "Haz primero lo que está entre paréntesis.",
     ["Lee el problema y pregúntate: ¿qué sé?, ¿qué me preguntan?, ¿qué tengo que calcular <b>primero</b>?",
      "Escribe cada paso con su operación. Las operaciones entre <b>paréntesis</b> se hacen primero: (20 − 8) × 3 = 12 × 3 = 36.",
      "Al terminar, comprueba si el resultado tiene sentido: si repartes, cada uno recibe menos que el total."],
     [("Compra 4 cuadernos de $35 y paga con $200", ["4 × 35 = 140", "200 − 140"], "$60 de cambio"), ("(45 + 15) ÷ 6", ["45 + 15 = 60", "60 ÷ 6"], "10")],
     [["Hacer las operaciones en el orden en que aparecen", "Primero lo del paréntesis."], ["Responder con el resultado del primer paso", "Lee otra vez la pregunta."], ["Elegir mal la operación", "Repartir en partes iguales es dividir."]],
     [("¿Cómo sé qué operación usar?", "Juntar o agregar es sumar; quitar o comparar, restar; varias veces lo mismo, multiplicar; repartir en partes iguales, dividir."),
      ("¿Para qué sirven los paréntesis?", "Indican qué operación se hace primero: en (8 + 2) × 5 primero sumamos 8 + 2 = 10 y después 10 × 5 = 50.")],
     [("Operaciones con paréntesis", [(par, 20)]), ("Sumar y restar en dos pasos", [(sr, 20)]), ("Problemas con multiplicación", [(mu, 20)]), ("Problemas con división", [(dv, 20)]),
      ("¿Qué operación hay que hacer?", [(op, 20)])],
     64007, lv=4)
