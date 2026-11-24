# -*- coding: utf-8 -*-
"""México 1.er y 2.º grado: Regularidades en la sucesión numérica y patrones (Estudio de los números). Reutiliza España 1.º/2.º (gen_es_matematicas_2_patrones, gen_es_matematicas_3_numeros) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG, q_le

T = {1: dict(std="Identifica regularidades en la sucesión numérica hasta 100; cuenta hacia adelante y hacia atrás de uno en uno, de dos en dos, de cinco en cinco y de diez en diez; continúa patrones",
             title="Sucesiones y patrones", meta="Ejercicios de matemáticas de 1.er grado de primaria: contar de 2 en 2, de 5 en 5 y de 10 en 10, qué sigue en una serie, patrones de figuras y la regla de una sucesión. 100 ejercicios con respuestas.",
             kb="Busca qué se repite", ks="O cuánto aumenta cada vez.",
             think=["En un <b>patrón</b>, algo se repite: círculo, cuadrado, círculo, cuadrado… Busca el grupo que se repite.",
                    "En una <b>sucesión</b> de números, mira cuánto aumenta o disminuye cada vez: 5, 10, 15, 20 va de 5 en 5.",
                    "Para seguir, suma (o resta) siempre lo mismo."],
             ex=[("10, 20, 30, ___", ["aumenta 10"], "40"), ("rojo, azul, azul, rojo, azul, azul, ___", ["se repite rojo, azul, azul"], "rojo")],
             mist=[["Mirar solo los dos últimos", "Revisa toda la serie."], ["Sumar 1 cuando va de 2 en 2", "Calcula la diferencia entre dos números seguidos."], ["Olvidar que puede bajar", "20, 18, 16… va hacia atrás."]],
             faq=[("¿Qué es un patrón?", "Un orden que se repite siempre igual, como los colores de un collar."), ("¿Cómo sé de cuánto en cuánto va una serie?", "Resta dos números seguidos: en 3, 6, 9, la diferencia es 3.")]),
     2: dict(std="Identifica regularidades en la sucesión numérica hasta 1 000 en las unidades, decenas y centenas; cuenta de 2 en 2, de 5 en 5, de 10 en 10 y de 100 en 100; continúa patrones",
             title="Sucesiones y patrones", meta="Ejercicios de matemáticas de 2.º grado de primaria: sucesiones de 10 en 10 y de 100 en 100, qué número falta, la regla de una serie y patrones de figuras. 100 ejercicios con respuestas.",
             kb="Busca la regla", ks="¿Cuánto aumenta o disminuye cada vez?",
             think=["En una <b>sucesión</b>, cada número se obtiene del anterior siguiendo una <b>regla</b>: 120, 130, 140 suma 10.",
                    "Al sumar 10, cambian las decenas; al sumar 100, cambian las centenas: 345, 445, 545.",
                    "Para encontrar un número que falta, aplica la regla hacia adelante o hacia atrás."],
             ex=[("250, 300, 350, ___", ["aumenta 50"], "400"), ("890, 790, 690, ___", ["disminuye 100"], "590")],
             mist=[["Cambiar la cifra equivocada", "Al sumar 100, cambian las centenas."], ["Olvidar cambiar de centena", "Después de 290 + 10 viene 300."], ["Pensar que siempre sube", "También hay series que bajan."]],
             faq=[("¿Qué es la regla de una sucesión?", "Lo que se hace para pasar de un número al siguiente, por ejemplo «sumar 5»."), ("¿Qué cambia al contar de 100 en 100?", "Solo la cifra de las centenas: 215, 315, 415.")])}


def build(lv):
    t = T[lv]
    sig, grupo, serie, regla, igual = src("gen_es_matematicas_2_patrones", 60300 + 1000 * lv, "s_siguiente", "s_grupo", "s_serie", "s_regla", "s_igual", lv=lv, mx_=BIG, extra=(q_le(100 if lv == 1 else 999),))
    ser = src("gen_es_matematicas_3_numeros", 60310 + 1000 * lv, "s4_series", lv=lv, mx_=BIG)
    unit("sucesiones-y-patrones", 3, "N", t["std"], t["title"], "Sucesiones y patrones", t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"],
         [("¿Qué sigue?", [(sig, 20)]), ("El grupo que se repite", [(grupo, 20)]), ("Sucesiones de números", [(serie, 10), (ser, 10)]), ("La regla", [(regla, 20)]), ("Igualdades y repaso", [(igual, 12), (ser, 8)])],
         60000 + 1000 * lv + 3, lv=lv)


if __name__ == "__main__":
    build(1)
