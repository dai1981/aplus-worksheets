# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: Multiplicación por una cifra (Sentido numérico)
Multiplicar números de 2, 3 y 4 cifras por una cifra en vertical (sin y con llevadas), por 10, 100 y 1000, propiedades y problemas.
Errores: olvidar sumar la llevada, multiplicar solo las unidades, poner un cero de menos.
"""
import random
from es_common import mcq, num, vertical
from es_low import unit, src

R = random.Random(33006)
SEED = 33906


def sin_llevar(a, b):
    return int("".join(str(int(c) * b % 10) for c in str(a)))


def s_sin():
    b = R.randint(2, 4)
    a = int("".join(str(R.randint(1, 9 // b)) for _ in range(R.choice([2, 3, 3]))))
    p = a * b
    return mcq(vertical([str(a), str(b)], op="×") + "Calcula: %s × %d" % (num(a), b), num(p), [num(a + b), num(p + b), num(p - 10) if p > 10 else num(p + 10)], "Multiplicamos cada cifra por %d, empezando por las unidades: <b>%s</b>." % (b, num(p)))


def s_con():
    b = R.randint(2, 9)
    a = R.randint(12, 9999 // b)
    p = a * b
    if sin_llevar(a, b) == p:
        return None
    return mcq(vertical([str(a), str(b)], op="×") + "Calcula: %s × %d" % (num(a), b), num(p), [num(sin_llevar(a, b)), num(p + 10), num(p - 10 * b) if p > 10 * b else num(p + 1)],
               "Si un producto pasa de 9, escribe las unidades y llévate las decenas a la columna siguiente: <b>%s</b>." % num(p))


def s_ceros():
    m = R.choice([10, 100, 1000])
    a = R.randint(2, 9999 // m)
    if a * m > 9999:
        return None
    return mcq("Calcula: %s × %s" % (num(a), num(m)), num(a * m), [num(a * m // 10) if a * m // 10 != a else num(a * m * 10), num(a * m * 10) if a * m * 10 <= 99999 else num(a + m), num(a + m)],
               "Multiplicar por %s es añadir %s a la derecha: <b>%s</b>." % (num(m), {10: "un cero", 100: "dos ceros", 1000: "tres ceros"}[m], num(a * m)))


prop, problema = src("multiplicacion", SEED, "s4_prop", "s5_problema")

unit(3, "multiplicacion", 6, "N", "Multiplicación de números naturales por una cifra; multiplicar por 10, 100 y 1000; propiedades conmutativa y asociativa",
     "Multiplicación por una cifra", "Multiplicación",
     "Fichas de matemáticas de 3.º de Primaria: multiplicar por una cifra en vertical, con y sin llevadas, por 10, 100 y 1000, y problemas. 100 ejercicios con soluciones.",
     "Empieza por las unidades", "Lo que te llevas se suma después.",
     ["Coloca el número de una cifra debajo de las unidades.", "Multiplica cada cifra empezando por las unidades. Si el resultado pasa de 9, escribe las unidades y <b>llévate</b> las decenas.",
      "La llevada se <b>suma</b> después de multiplicar la cifra siguiente.", "Por 10, 100 o 1000: añade 1, 2 o 3 ceros."],
     [("246 × 3", ["3 × 6 = 18: escribo 8 y me llevo 1", "3 × 4 = 12, + 1 = 13: escribo 3 y me llevo 1", "3 × 2 = 6, + 1 = 7"], "738"), ("57 × 100", ["Añado dos ceros"], "5700")],
     [["Olvidar sumar la llevada", "Escribe la llevada pequeña encima de la columna siguiente."], ["Multiplicar solo las unidades", "Multiplica todas las cifras, una a una."], ["Poner un cero de menos", "× 100 son dos ceros: 34 × 100 = 3400."]],
     [("¿Qué es la propiedad conmutativa?", "Que el orden de los factores no cambia el producto: 4 × 7 = 7 × 4."), ("¿Cómo se multiplica por 1000?", "Se añaden tres ceros a la derecha del número: 6 × 1000 = 6000.")],
     [("Sin llevadas", [(s_sin, 20)]), ("Con llevadas", [(s_con, 20)]), ("Por 10, 100 y 1000", [(s_ceros, 20)]), ("Propiedades", [(prop, 20)]), ("Problemas", [(problema, 20)])], 33006,
     vertical(["246", "3"], op="×", result="738"))
