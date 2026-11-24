# -*- coding: utf-8 -*-
"""México 1.er y 2.º grado: Problemas de suma y resta (juntar, quitar, comparar, completar, dos pasos). Reutiliza España 1.º/2.º (gen_es_matematicas_2_problemas) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

T = {1: dict(std="Resuelve problemas de suma y resta con números de hasta dos cifras usando material, dibujos y sus propias estrategias; distingue cuándo hay que juntar, quitar, comparar o completar",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: problemas de juntar, quitar, comparar y completar con números hasta 100. 100 ejercicios con respuestas.",
             think=["Lee el problema y pregúntate: ¿se juntan cosas, se quitan, se comparan o falta algo?",
                    "<b>Juntar</b> o <b>agregar</b> es sumar. <b>Quitar</b>, perder o regalar es restar.",
                    "Para <b>comparar</b> («¿cuántos más?») o <b>completar</b> («¿cuántos faltan?»), resta el menor del mayor."],
             ex=[("Ana tiene 12 canicas y gana 5", ["se juntan: 12 + 5"], "17"), ("Hay 15 niños y 9 sillas. ¿Cuántas sillas faltan?", ["15 − 9"], "6")]),
     2: dict(std="Resuelve problemas de suma y resta con números menores que 1 000 que implican agregar, quitar, comparar y completar, incluso de dos pasos",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: problemas de juntar, quitar, comparar y completar, problemas de dos pasos y elegir la operación. 100 ejercicios con respuestas.",
             think=["Lee el problema dos veces. Subraya los números y la pregunta.",
                    "Juntar o agregar es sumar; quitar es restar. Para saber «cuántos más» o «cuántos faltan», también se resta.",
                    "En los problemas de <b>dos pasos</b>, primero calcula lo que te falta saber y después responde la pregunta."],
             ex=[("Hay 245 libros y llegan 130", ["245 + 130"], "375 libros"), ("Tenía 80 pesos, gastó 25 y luego 30", ["80 − 25 = 55", "55 − 30"], "25 pesos")])}


def build(lv):
    t = T[lv]
    jun, qui, comp, compl, dos, eleg = src("gen_es_matematicas_2_problemas", 60600 + 1000 * lv, "s_juntar", "s_quitar", "s_comparar", "s_completar", "s_dos", "s_elegir", lv=lv, mx_=BIG)
    unit("problemas-de-suma-y-resta", 6, "S3", t["std"], "Problemas de suma y resta", "Problemas de suma y resta", t["meta"], "¿Juntar, quitar o comparar?", "Lee la pregunta antes de calcular.",
         t["think"], t["ex"],
         [["Sumar cuando hay que restar", "«¿Cuántos quedan?» es restar."], ["Usar todos los números sin pensar", "Algunos datos no se necesitan."], ["Olvidar el segundo paso", "Revisa qué te preguntan al final."]],
         [("¿Cómo sé si un problema es de suma o de resta?", "Si se juntan o se agregan cosas, es suma. Si se quitan, se pierden o se compara cuántos más hay, es resta."),
          ("¿Qué hago si no entiendo el problema?", "Haz un dibujo o usa objetos para representarlo.")],
         [("Juntar y agregar", [(jun, 20)]), ("Quitar", [(qui, 20)]), ("Comparar", [(comp, 20)]), ("Completar", [(compl, 20)]), ("Dos pasos y elegir la operación", [(dos, 10), (eleg, 10)])],
         60000 + 1000 * lv + 6, lv=lv)


if __name__ == "__main__":
    build(1)
