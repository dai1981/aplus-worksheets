# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Cálculo mental y estimación (Sentido numérico)
Sumar y restar decenas y centenas, sumar 9 y 99, dobles y mitades, descomponer, estimar redondeando.
Reutiliza los generadores de 4.º (mismo ciclo) con números hasta 9999.
"""
import random
from es_common import mcq, num
from es_low import unit, src

R = random.Random(33004)
SEED = 33904


def s_redondos():
    p = R.choice([10, 100, 1000])
    n = R.randint(100, 8999)
    m = R.randint(1, 9) * p
    if R.random() < 0.5:
        if n + m > 9999:
            return None
        return mcq("Calcula mentalmente: %s + %s" % (num(n), num(m)), num(n + m), [num(n + m // 10), num(n + m * 10) if n + m * 10 <= 99999 else num(n + m + 1), num(n + m + p), num(n + m - p)],
                   "Solo cambia la cifra de las %s: <b>%s</b>." % ({10: "decenas", 100: "centenas", 1000: "unidades de millar"}[p], num(n + m)))
    if n - m < 0:
        return None
    return mcq("Calcula mentalmente: %s − %s" % (num(n), num(m)), num(n - m), [num(n - m // 10), num(n - m + p), num(n - m - p) if n - m - p >= 0 else num(n + m)],
               "Solo cambia la cifra de las %s: <b>%s</b>." % ({10: "decenas", 100: "centenas", 1000: "unidades de millar"}[p], num(n - m)))


def s_doble():
    n = R.choice([R.randint(11, 49), R.randint(1, 49) * 10, R.randint(1, 45) * 100])
    if R.random() < 0.5:
        return mcq("¿Cuál es el doble de %s?" % num(n), num(2 * n), [num(n + 2), num(n // 2) if n % 2 == 0 else num(2 * n + 10), num(2 * n + 10), num(2 * n - 1)], "%s + %s = <b>%s</b>." % (num(n), num(n), num(2 * n)))
    m = 2 * n
    return mcq("¿Cuál es la mitad de %s?" % num(m), num(n), [num(2 * m), num(n + 1), num(n - 10) if n > 10 else num(n + 2)], "%s + %s = %s: la mitad es <b>%s</b>." % (num(n), num(n), num(m), num(n)))


casi, descomp, estimar, problema = src("calculo_mental_y_estimacion", SEED, "s1_casi", "s2_descomponer", "s3_estimar", "s5_problema")

unit(3, "calculo-mental", 4, "N", "Estrategias de cálculo mental con números naturales; estimación de resultados redondeando",
     "Cálculo mental y estimación", "Cálculo mental",
     "Fichas de matemáticas de 3.º de Primaria: sumar y restar decenas y centenas, sumar 9 y 99, dobles, mitades y estimar. 100 ejercicios con soluciones.",
     "Busca números redondos", "Suma 100 y quita 1 para sumar 99.",
     ["Para sumar decenas o centenas, solo cambia una cifra: 3450 + 200 = 3650.", "Para sumar 9, suma 10 y quita 1. Para sumar 99, suma 100 y quita 1.",
      "Para <b>estimar</b>, redondea los números y calcula con los redondos: 498 + 307 es unos 500 + 300 = 800."],
     [("2346 + 99", ["2346 + 100 = 2446", "2446 − 1 = 2445"], "2445"), ("Estima 612 + 289", ["600 + 300"], "unos 900")],
     [["Cambiar la cifra equivocada", "En 4520 + 300, cambia las centenas: 4820."], ["Sumar 99 y olvidar quitar 1", "+ 100 − 1, siempre los dos pasos."], ["Estimar sin redondear", "Redondea primero; después calcula."]],
     [("¿Para qué sirve estimar?", "Para saber si un resultado es razonable antes o después de hacer la cuenta."), ("¿Cómo se suma 99 mentalmente?", "Se suma 100 y después se resta 1.")],
     [("Decenas, centenas y millares", [(s_redondos, 20)]), ("Sumar 9, 99 y números cercanos", [(casi, 20)]), ("Dobles, mitades y descomponer", [(s_doble, 10), (descomp, 10)]),
      ("Estimar", [(estimar, 20)]), ("Problemas", [(problema, 20)])], 33004)
