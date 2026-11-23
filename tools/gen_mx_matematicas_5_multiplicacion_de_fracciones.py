# -*- coding: utf-8 -*-
"""México 5.º grado: Multiplicación de una fracción por un número natural (Multiplicación y división). Reutiliza España 6.º (nivel 5.º) con otra semilla."""
import re
import random
from math import gcd
from mx_common import src, unit, mcq, NB
from es_common import fr


def por_natural(it):
    t = re.sub(r"<[^>]*>", " ", it["q"])
    return "×" in t and not re.search(r"</span>\s*×\s*<span class='fr'>|÷| : ", it["q"])


pn = src("gen_es_matematicas_6_operaciones_con_fracciones", 65310, "s3_por_natural", lv=5, extra=(por_natural,))
R = random.Random(65110)
SIT = [("Cada vaso tiene %s de litro de agua de jamaica. ¿Cuántos litros hay en %d vasos?", "L"), ("Una receta de tamales lleva %s de kilo de masa por cada docena. ¿Cuántos kilos se necesitan para %d docenas?", "kg"),
       ("Cada vuelta a la pista mide %s de kilómetro. ¿Cuántos kilómetros recorre Itzel en %d vueltas?", "km"), ("Cada listón mide %s de metro. ¿Cuántos metros miden %d listones?", "m"),
       ("Una llave gotea %s de litro cada hora. ¿Cuántos litros gotea en %d horas?", "L")]


def mixto(n, d):
    g = gcd(n, d)
    n, d = n // g, d // g
    if d == 1:
        return str(n)
    if n < d:
        return fr(n, d)
    return "%d%s%s" % (n // d, NB, fr(n % d, d)) if n % d else str(n // d)


def probl():
    t, u = R.choice(SIT)
    d = R.choice([2, 3, 4, 5, 8, 10])
    n = R.randint(1, d - 1)
    if gcd(n, d) > 1:
        return None
    k = R.randint(2, 12)
    ok = mixto(n * k, d)
    w = [mixto(n * k, d * k), mixto(n + k, d), mixto(n * k + 1, d) if (n * k + 1) % d else mixto(n * k + 2, d), mixto(n, d * k)]
    return mcq(t % (fr(n, d), k), "%s %s" % (ok, u), ["%s %s" % (x, u) for x in w if x != ok],
               "%s × %d = %s = <b>%s %s</b>." % (fr(n, d), k, fr(n * k, d), ok, u))
cant, probf = src("gen_es_matematicas_6_fracciones", 65311, "s4_cantidad", "s5_problema", lv=5)

unit("multiplicacion-de-fracciones-por-un-natural", 7, "P",
     "Multiplica una fracción por un número natural; interpreta el producto como una suma repetida y como la fracción de una cantidad; resuelve problemas",
     "Multiplicar fracciones por un natural", "Fracción × natural",
     "Ejercicios de matemáticas de 5.º grado de primaria: multiplicar una fracción por un número natural, suma repetida, fracción de una cantidad y problemas. 100 ejercicios con respuestas.",
     "Multiplica solo el numerador", "El denominador se queda igual.",
     ["Multiplicar %s × 4 es sumar %s cuatro veces: %s + %s + %s + %s = %s." % (fr(2, 5), fr(2, 5), fr(2, 5), fr(2, 5), fr(2, 5), fr(2, 5), fr(8, 5)),
      "Por eso se multiplica <b>solo el numerador</b> y el denominador se queda igual. Después se simplifica o se escribe como número mixto: %s = 1 %s." % (fr(8, 5), fr(3, 5)),
      "%s de 20 es lo mismo que %s × 20 = %s = 15." % (fr(3, 4), fr(3, 4), fr(60, 4))],
     [("%s × 6" % fr(3, 8), ["3 × 6 = 18", "%s = %s" % (fr(18, 8), fr(9, 4))], "%s = 2 %s" % (fr(9, 4), fr(1, 4)))],
     [["Multiplicar también el denominador", "%s × 4 = %s, no %s." % (fr(2, 5), fr(8, 5), fr(8, 20))], ["Sumar en lugar de multiplicar", "%s × 4 no es %s." % (fr(2, 5), fr(6, 5))], ["Olvidar simplificar", "%s = 2." % fr(10, 5)]],
     [("¿Por qué no se multiplica el denominador?", "Porque el denominador dice el tamaño de las partes (quintos) y ese tamaño no cambia: solo cambia cuántas partes hay."),
      ("¿Qué relación hay con la fracción de una cantidad?", "Calcular 3/4 de 20 es multiplicar 3/4 × 20: 20 ÷ 4 × 3 = 15.")],
     [("Fracción por natural", [(pn, 20)]), ("Simplificar el producto", [(pn, 20)]), ("Fracción de una cantidad", [(cant, 20)]), ("Problemas con fracciones", [(probf, 20)]), ("Problemas de multiplicar", [(probl, 20)])],
     65007, lv=5)
