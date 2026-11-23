# -*- coding: utf-8 -*-
"""México 3.er grado: Multiplicación (productos de hasta tres cifras, por 10 y 100, propiedades, problemas). Reutiliza España 3.º/4.º con otra semilla."""
import random
from mx_common import src, unit, mx_text, mcq, num
import es_common as ES

R = random.Random(63107)
sin_ = src("gen_es_matematicas_3_multiplicacion", 63107, "s_sin", mx_=999)


def ceros():
    m = R.choice([10, 10, 100])
    a = R.randint(2, 99) if m == 100 else R.randint(2, 999)
    if a * m > 9999:
        return None
    return mcq("Calcula: %s × %s" % (num(a), num(m)), num(a * m), [num(a * m // 10) if m == 100 else num(a * 100), num(a + m), num(a * m * 10) if a * m * 10 <= 9999 else num(a * m + m)],
               "Multiplicar por %s es añadir %s a la derecha: <b>%s</b>." % (num(m), "un cero" if m == 10 else "dos ceros", num(a * m)))


def sin_llevar(a, b):
    return int("".join(str(int(c) * b % 10) for c in str(a)))


def con():
    b = R.randint(2, 9)
    a = R.randint(12, 999 // b)
    p = a * b
    if sin_llevar(a, b) == p:
        return None
    return mcq(mx_text(ES.vertical([str(a), str(b)], op="×")) + "Calcula: %s × %d" % (num(a), b), num(p), [num(sin_llevar(a, b)), num(p + 10), num(p - 10 * b) if p > 10 * b else num(p + 1), num(a + b)],
               "Si un producto pasa de 9, escribe las unidades y lleva las decenas a la columna siguiente: <b>%s</b>." % num(p))
prop, probl = src("gen_es_matematicas_4_multiplicacion", 63207, "s4_prop", "s5_problema", mx_=999)

unit("multiplicacion", 6, "P",
     "Resuelve multiplicaciones cuyo producto es un número natural de hasta tres cifras; multiplica por 10 y por 100; usa la propiedad conmutativa y resuelve problemas",
     "Multiplicación", "Multiplicación",
     "Ejercicios de matemáticas de 3.er grado de primaria: multiplicaciones por una cifra con y sin reagrupación, por 10 y por 100, propiedades y problemas. 100 ejercicios con respuestas.",
     "Multiplica cada cifra", "Empieza por las unidades y lleva.",
     ["Para multiplicar 124 × 3, multiplica cada cifra por 3 empezando por las <b>unidades</b>.",
      "Si un producto pasa de 9, escribe las unidades y <b>lleva</b> las decenas a la columna siguiente.",
      "Multiplicar por 10 es añadir un cero a la derecha: 23 × 10 = 230. Por 100, dos ceros."],
     [("Calcula 126 × 3", ["6 × 3 = 18: escribo 8 y llevo 1", "2 × 3 + 1 = 7", "1 × 3 = 3"], "378")],
     [["Olvidar lo que se lleva", "126 × 3 = 378, no 368."], ["Sumar en vez de multiplicar", "126 × 3 no es 126 + 3."], ["Poner mal los ceros", "45 × 10 = 450."]],
     [("¿Qué quiere decir que la multiplicación es conmutativa?", "Que el orden de los factores no cambia el producto: 7 × 4 = 4 × 7 = 28."),
      ("¿Cómo multiplico por 10 o por 100?", "Escribe el número y añade un cero (por 10) o dos ceros (por 100) a la derecha.")],
     [("Sin reagrupación", [(sin_, 20)]), ("Con reagrupación", [(con, 20)]), ("Por 10 y por 100", [(ceros, 20)]), ("Propiedades", [(prop, 20)]), ("Problemas", [(probl, 20)])],
     63006, pic=mx_text(ES.vertical(["126", "3"], op="×")))
