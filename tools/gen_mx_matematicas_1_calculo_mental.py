# -*- coding: utf-8 -*-
"""México 1.er grado (números de una y dos cifras, sin algoritmo) y 2.º grado (dos cifras): Cálculo mental de sumas y restas. Reutiliza España 1.º/2.º (gen_es_matematicas_2_calculo_mental) con otra semilla."""
from mx_common import src, unit
from mx_12 import BIG

T = {1: dict(std="Resuelve problemas de suma y resta con números de hasta dos cifras sin usar el algoritmo convencional; calcula mentalmente con números de una cifra y explica sus estrategias",
             title="Sumas y restas hasta 100: cálculo mental", short="Cálculo mental",
             meta="Ejercicios de matemáticas de 1.er grado de primaria: sumar y restar decenas, sumar 10 y 9, completar a la decena y problemas hasta 100. 100 ejercicios con respuestas.",
             kb="Suma primero las decenas", ks="34 + 20: 3 decenas y 2 decenas son 5 decenas.",
             think=["Para sumar decenas, cuenta de 10 en 10: 30 + 20 = 50, porque 3 decenas + 2 decenas = 5 decenas.",
                    "Sumar 10 cambia solo las decenas: 46 + 10 = 56. Para sumar 9, suma 10 y quita 1.",
                    "Para completar la decena, piensa cuánto falta: de 37 a 40 faltan 3."],
             ex=[("45 + 30", ["4 decenas + 3 decenas = 7 decenas", "70 + 5"], "75"), ("28 + 9", ["28 + 10 = 38", "38 − 1"], "37")],
             mist=[["Sumar las decenas con las unidades", "45 + 30: el 3 son decenas."], ["Olvidar quitar 1 al sumar 9", "28 + 9 = 37, no 38."], ["Cambiar la cifra equivocada", "+10 cambia las decenas."]],
             faq=[("¿Qué es una estrategia de cálculo mental?", "Una forma de calcular sin escribir la cuenta, por ejemplo sumar 10 y quitar 1 para sumar 9."), ("¿Cómo sumo 20 + 30?", "Piensa en decenas: 2 + 3 = 5 decenas, o sea 50.")]),
     2: dict(std="Calcula mentalmente sumas y restas con números de dos cifras; explica y verifica las estrategias que usa",
             title="Cálculo mental con dos cifras", short="Cálculo mental",
             meta="Ejercicios de matemáticas de 2.º grado de primaria: sumar y restar decenas y centenas de memoria, sumar 9 y 99, completar a la centena y problemas. 100 ejercicios con respuestas.",
             kb="Descompón en decenas y unidades", ks="47 + 25 = 40 + 20 + 7 + 5.",
             think=["Para sumar dos números de dos cifras, suma primero las decenas y luego las unidades: 47 + 25 = 60 + 12 = 72.",
                    "Para sumar 9, suma 10 y quita 1; para sumar 99, suma 100 y quita 1.",
                    "Para restar, puedes contar lo que falta: de 68 a 100 faltan 2 + 30 = 32."],
             ex=[("56 + 37", ["50 + 30 = 80", "6 + 7 = 13", "80 + 13"], "93"), ("74 − 29", ["74 − 30 = 44", "44 + 1"], "45")],
             mist=[["Olvidar juntar las unidades", "6 + 7 = 13: suma esa decena extra."], ["Restar 30 y no devolver 1", "74 − 29 = 74 − 30 + 1."], ["Contar mal al completar", "De 68 a 70 son 2; de 70 a 100, 30."]],
             faq=[("¿Por qué conviene sumar primero las decenas?", "Porque son números redondos y es más fácil: 40 + 20 = 60. Después solo falta sumar las unidades."), ("¿Cómo compruebo una resta?", "Suma el resultado y el número que restaste: debe dar el primero.")])}


def build(lv):
    t = T[lv]
    dec, diez, comp, nueve, probl = src("gen_es_matematicas_2_calculo_mental", 60500 + 1000 * lv, "s_decenas", "s_diez", "s_completar", "s_nueve", "s_problema", lv=lv, mx_=BIG)
    unit("calculo-mental", 5, "S3", t["std"], t["title"], t["short"], t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"],
         [("Sumar y restar decenas", [(dec, 20)] if lv == 2 else [(dec, 16), (diez, 4)]), ("Más 10 y menos 10" if lv == 1 else "Sumar y restar centenas", [(diez, 20)]), ("Completar", [(comp, 20)]), ("Sumar y restar 9", [(nueve, 20)]), ("Problemas", [(probl, 20)])],
         60000 + 1000 * lv + 5, lv=lv)


if __name__ == "__main__":
    build(1)
