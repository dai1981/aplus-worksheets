# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Problemas de una y dos operaciones (Sentido numérico)
Reutiliza los problemas de 4.º (mismo ciclo) con números hasta 9999.
"""
from es_low import unit, src

SEED = 33908
par, sr, mu, dv, op = src("problemas_de_dos_operaciones", SEED, "s1_parentesis", "s2_suma_resta", "s3_mult", "s4_div", "s5_operacion")

unit(3, "problemas", 8, "N", "Resolución de problemas de una y dos operaciones con números naturales; elección de la operación; comprobación de la solución",
     "Problemas de una y dos operaciones", "Problemas",
     "Fichas de matemáticas de 3.º de Primaria: elegir la operación, problemas de suma, resta, multiplicación y división, y problemas de dos pasos. 100 ejercicios con soluciones.",
     "Datos, pregunta, operación", "Al final, comprueba si tiene sentido.",
     ["Lee el problema y busca la <b>pregunta</b>.", "Piensa qué operación hace falta: juntar (suma), quitar (resta), grupos iguales (multiplicación) o repartir (división).",
      "A veces hacen falta <b>dos</b> operaciones: la primera calcula un dato que no está en el enunciado.", "Comprueba que la respuesta tiene sentido."],
     [("Compra 3 cuadernos de 2 € y paga con 10 €. ¿Cuánto le devuelven?", ["3 × 2 = 6 €", "10 − 6 = 4 €"], "4 €"), ("Hay 24 galletas en 4 platos iguales. ¿Cuántas hay en cada plato?", ["Repartir: 24 : 4"], "6 galletas")],
     [["Hacer solo una operación", "Mira si has respondido a la pregunta."], ["Elegir la operación por una palabra", "«Más» no siempre es sumar: piensa en la situación."], ["Olvidar las unidades", "Escribe la respuesta completa: 4 €, 6 galletas."]],
     [("¿Cómo se resuelve un problema?", "Se lee, se buscan los datos y la pregunta, se elige la operación, se calcula y se comprueba la solución."),
      ("¿Qué es un problema de dos operaciones?", "Un problema en el que primero hay que calcular un dato intermedio y después, con ese dato, la respuesta.")],
     [("Elegir la operación", [(op, 20)]), ("Problemas de suma y resta", [(sr, 20)]), ("Problemas de multiplicar", [(mu, 20)]), ("Problemas de dividir", [(dv, 20)]),
      ("Operaciones combinadas", [(par, 20)])], 33008)
