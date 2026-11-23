# -*- coding: utf-8 -*-
"""México 3.er grado: División (reparto y agrupamiento, división como inversa de la multiplicación, dos cifras entre una cifra). Reutiliza España 3.º/4.º."""
import random
from mx_common import src, unit, mcq
import es_pics as P

R = random.Random(63208)


def una():
    d = R.randint(2, 9)
    c = R.randint(3, 99 // d)
    r = R.randint(0, d - 1) if R.random() < 0.55 else 0
    D = c * d + r
    if D > 99 or D < 10:
        return None
    ans = str(c) if r == 0 else "%d y residuo %d" % (c, r)
    alts = ([str(c + 1), str(c - 1), str(d)] if r == 0 else
            ["%d y residuo %d" % (c - 1, r + d), "%d y residuo %d" % (c + 1, r), "%d y residuo %d" % (c, r + 1) if r + 1 < d else "%d y residuo %d" % (c, r - 1), str(c)])
    return mcq("Calcula: %d ÷ %d" % (D, d), ans, alts,
               "%d × %d = %d%s. <b>%s</b>." % (d, c, c * d, "" if r == 0 else " y sobran %d − %d = %d" % (D, c * d, r), ans))

reparto, tabla = src("gen_es_matematicas_3_division", 63108, "s_reparto", "s_tabla")
terminos, probl = src("gen_es_matematicas_4_division", 63208, "s3_terminos", "s5_problema", mx_=99)

unit("division", 7, "P",
     "Resuelve situaciones de reparto y agrupamiento con divisiones de números de dos cifras entre números de una cifra; relaciona la división con la multiplicación",
     "División", "División",
     "Ejercicios de matemáticas de 3.er grado de primaria: repartir en partes iguales, la división y las tablas, dividir entre una cifra, el residuo y problemas. 100 ejercicios con respuestas.",
     "Dividir: repartir en partes iguales", "Usa las tablas para dividir.",
     ["<b>Dividir</b> es repartir en partes iguales: 12 ÷ 3 = 4 porque 3 grupos de 4 son 12.",
      "La división es la operación inversa de la multiplicación: si 6 × 7 = 42, entonces 42 ÷ 6 = 7.",
      "A veces sobra algo: 17 ÷ 5 = 3 y residuo 2. El <b>residuo</b> siempre es menor que el divisor."],
     [("Reparte 24 lápices entre 4 niños", ["¿Qué número por 4 da 24?", "4 × 6 = 24"], "6 lápices cada uno"), ("Calcula 29 ÷ 4", ["4 × 7 = 28", "29 − 28 = 1"], "7 y residuo 1")],
     [["Un residuo mayor que el divisor", "Si sobra 5 al dividir entre 4, cabe una vez más."], ["Confundir dividendo y divisor", "En 24 ÷ 4, repartes 24 entre 4."], ["Olvidar el residuo en el problema", "Lee qué pide: a veces hay que sumar 1 (un viaje más)."]],
     [("¿Qué es el residuo?", "Lo que sobra cuando no se puede repartir más en partes iguales. Siempre es menor que el divisor."),
      ("¿Cómo compruebo una división?", "Multiplica el divisor por el cociente y suma el residuo: debe dar el dividendo.")],
     [("Repartir en partes iguales", [(reparto, 20)]), ("La división y las tablas", [(tabla, 20)]), ("Dividir entre una cifra", [(una, 20)]),
      ("Términos y comprobación", [(terminos, 20)]), ("Problemas", [(probl, 20)])], 63007, pic=P.grupos(3, 4, "star"))
