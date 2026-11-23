# -*- coding: utf-8 -*-
"""México 3.er grado: Problemas de una y dos operaciones (suma, resta, multiplicación y división). Reutiliza España 4.º con otra semilla."""
from mx_common import src, unit

par, sr, mu, dv, op = src("gen_es_matematicas_4_problemas_de_dos_operaciones", 63209, "s1_parentesis", "s2_suma_resta", "s3_mult", "s4_div", "s5_operacion", mx_=1999)

unit("problemas", 8, "S",
     "Resuelve situaciones problemáticas vinculadas a su contexto que implican sumas, restas, multiplicaciones y divisiones; elige la operación y comprueba el resultado",
     "Problemas de una y dos operaciones", "Problemas",
     "Ejercicios de matemáticas de 3.er grado de primaria: elegir la operación, problemas de sumar, restar, multiplicar y dividir y problemas de dos operaciones. 100 ejercicios con respuestas.",
     "Lee, piensa, calcula y revisa", "¿Qué te preguntan? ¿Qué datos tienes?",
     ["Lee el problema dos veces. Busca la <b>pregunta</b> y los <b>datos</b>.",
      "Juntar o agregar: suma. Quitar o comparar: resta. Varios grupos iguales: multiplica. Repartir en partes iguales: divide.",
      "En los problemas de <b>dos operaciones</b>, haz primero la pregunta escondida y luego la final."],
     [("Compra 3 cuadernos de $25 y paga con $100. ¿Cuánto le dan de cambio?", ["3 × 25 = 75", "100 − 75 = 25"], "$25")],
     [["Usar los números sin leer", "Piensa qué pasa en la historia antes de calcular."], ["Hacer solo la primera operación", "Revisa si eso es lo que pregunta el problema."], ["No revisar", "Comprueba si el resultado tiene sentido."]],
     [("¿Cómo sé qué operación usar?", "Piensa qué pasa: si se junta, suma; si se quita o se compara, resta; si hay grupos iguales, multiplica; si se reparte, divide."),
      ("¿Qué es un problema de dos operaciones?", "Uno en el que hay que calcular un dato intermedio antes de llegar a la respuesta.")],
     [("Elegir la operación", [(op, 20)]), ("Problemas de suma y resta", [(sr, 20)]), ("Problemas de multiplicar", [(mu, 20)]), ("Problemas de dividir", [(dv, 20)]),
      ("Dos operaciones", [(par, 20)])], 63008)
