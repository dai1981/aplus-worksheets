# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de Primaria: División entre una cifra (Sentido numérico)
Repartos en partes iguales, la división y las tablas, dividir entre una cifra (exactas y con resto), términos y prueba, problemas.
Errores: un resto mayor que el divisor, olvidar el 0 del cociente, no tener en cuenta el resto en los problemas.
"""
import random
from es_common import mcq, num
from es_low import unit, src
import es_pics as P

R = random.Random(33007)
SEED = 33907


def s_reparto():
    g = R.randint(2, 5)
    k = R.randint(2, 6)
    kind = R.choice(P.KINDS)
    n = g * k
    t = R.choice(["cada", "div"])
    pic = P.grupos(g, k, kind)
    if t == "cada":
        return mcq(pic + "Repartimos %s en %d grupos iguales. ¿Cuántas hay en cada grupo?" % (P.cosas(kind, n), g) if P.fem(kind) else pic + "Repartimos %s en %d grupos iguales. ¿Cuántos hay en cada grupo?" % (P.cosas(kind, n), g),
                   str(k), [str(g) if g != k else str(k + 2), str(n - g), str(k + 1)], "%d : %d = <b>%d</b>." % (n, g, k))
    return mcq(pic + "¿Qué división corresponde al dibujo?", "%d : %d = %d" % (n, g, k), ["%d : %d = %d" % (n, k + 1, g), "%d − %d = %d" % (n, g, n - g), "%d × %d = %d" % (n, g, n * g)], "%s en %d grupos de %d: <b>%d : %d = %d</b>." % (P.cosas(kind, n), g, k, n, g, k))


def s_tabla():
    a = R.randint(2, 9)
    b = R.randint(2, 10)
    if R.random() < 0.5:
        return mcq("Calcula: %d : %d" % (a * b, a), str(b), [str(a * b - a), str(b + 1), str(b - 1)], "%d × %d = %d, así que %d : %d = <b>%d</b>." % (a, b, a * b, a * b, a, b))
    return mcq("Si %d × %d = %d, ¿cuánto es %d : %d?" % (a, b, a * b, a * b, b), str(a), [str(b), str(a + 1), str(a * b - b)] if a != b else [str(a + 2), str(a + 1), str(a * b - b)],
               "La división es la operación inversa de la multiplicación: <b>%d</b>." % a)


una, terminos, problema = src("division", SEED, "s1_una", "s3_terminos", "s5_problema")

unit(3, "division", 7, "N", "La división como reparto en partes iguales y como operación inversa de la multiplicación; división entre una cifra; división exacta y entera",
     "División entre una cifra", "División",
     "Fichas de matemáticas de 3.º de Primaria: repartos, la división y las tablas, dividir entre una cifra, resto y prueba de la división. 100 ejercicios con soluciones.",
     "Dividir es hacer partes iguales", "El resto es menor que el divisor.",
     ["<b>Dividir</b> es repartir en partes iguales: 12 : 3 = 4, porque 3 × 4 = 12.", "En 17 : 5 = 3 y resto 2: 17 es el dividendo, 5 el divisor, 3 el cociente y 2 el resto.",
      "El resto tiene que ser <b>menor</b> que el divisor.", "<b>Prueba</b>: divisor × cociente + resto = dividendo."],
     [("28 : 4", ["¿Qué número por 4 da 28?", "4 × 7 = 28"], "7"), ("38 : 5", ["5 × 7 = 35", "38 − 35 = 3"], "7 y resto 3")],
     [["Resto mayor que el divisor", "En 38 : 5, un resto de 8 no vale: cabe otra vez el 5."], ["Olvidar el 0 del cociente", "618 : 3 = 206, no 26."], ["No usar el resto en el problema", "Si sobran niños, hace falta otro coche."]],
     [("¿Qué es la prueba de la división?", "Multiplicar el divisor por el cociente y sumar el resto. Debe dar el dividendo."), ("¿Cuándo una división es exacta?", "Cuando el resto es 0.")],
     [("Repartir en partes iguales", [(s_reparto, 20)]), ("La división y las tablas", [(s_tabla, 20)]), ("Dividir entre una cifra", [(una, 20)]),
      ("Términos y prueba", [(terminos, 20)]), ("Problemas", [(problema, 20)])], 33007, P.grupos(3, 4, "star"))
