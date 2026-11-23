# -*- coding: utf-8 -*-
"""México 4.º grado: División de números de hasta tres cifras entre números de una y dos cifras, con residuo (Multiplicación y división). Reutiliza España 4.º con otra semilla."""
import random
from mx_common import src, unit, mcq, num

M = "gen_es_matematicas_4_division"
terminos, probl = src(M, 64207, "s3_terminos", "s5_problema", mx_=999)
R = random.Random(64107)


def res(q, r):
    return str(q) if r == 0 else "%d y residuo %d" % (q, r)


def ceros():
    k = R.choice(["10", "100", "dec", "dec"])
    if k == "10":
        q = R.randint(2, 99) * 10 if R.random() < 0.5 else R.randint(12, 99)
        n = q * 10
        return mcq("Calcula mentalmente: %s ÷ 10" % num(n), num(q), [num(n // 100) if n % 100 == 0 else num(q + 10), num(n * 10), num(q * 10 if q * 10 != n else q + 1)],
                   "Dividir entre 10 es quitar un cero: <b>%s</b>." % num(q))
    if k == "100":
        q = R.randint(2, 99)
        n = q * 100
        return mcq("Calcula mentalmente: %s ÷ 100" % num(n), num(q), [num(q * 10), num(n // 1000) if n >= 1000 else num(q + 1), num(n * 100) if n * 100 <= 99999 else num(q + 10)],
                   "Dividir entre 100 es quitar dos ceros: <b>%s</b>." % num(q))
    d, q = R.randint(2, 9), R.randint(2, 9)
    m = R.choice([10, 100])
    n = d * q * (10 if m == 10 else 100)
    dv = d * 10
    if m == 100:
        q = q * 10
    return mcq("Calcula mentalmente: %s ÷ %d" % (num(n), dv), num(q), [num(q * 10), num(q // 10) if q >= 10 else num(q + 1), num(q + d)],
               "Quitamos un cero a cada número: %s ÷ %d = <b>%s</b>." % (num(n // 10), d, num(q)))


def una():
    d = R.randint(2, 9)
    q = R.randint(100 // d + 1, 999 // d)
    r = R.randint(0, d - 1) if R.random() < 0.7 else 0
    n = d * q + r
    if n > 999 or n < 100:
        return None
    w = [res(q + 1, r), res(q - 1, r + d) if r + d < 100 else res(q - 1, r), res(q, r + 1) if r + 1 < d else res(q, r - 1) if r else res(q + 10, 0)]
    if "0" in str(q)[1:]:
        w.append(res(int(str(q).replace("0", "")), r))
    return mcq("Calcula: %s ÷ %d" % (num(n), d), res(q, r), w, "%s ÷ %d = <b>%s</b>. Prueba: %d × %d%s = %s." % (num(n), d, res(q, r), d, q, " + %d" % r if r else "", num(n)))


def dos():
    d = R.randint(11, 49)
    q = R.randint(3, 999 // d)
    r = R.randint(0, d - 1) if R.random() < 0.6 else 0
    n = d * q + r
    if n > 999 or n < 100:
        return None
    w = [res(q + 1, r) if d * (q + 1) + r <= 999 or True else res(q, r), res(q - 1, r + d), res(q, (r + 1) % d) if d > 2 else res(q + 2, r), res(q * 10, r)]
    return mcq("Calcula: %s ÷ %d" % (num(n), d), res(q, r), w, "%d × %d = %s%s: <b>%s</b>." % (d, q, num(d * q), (" y %s + %d = %s; el residuo es menor que %d" % (num(d * q), r, num(n), d)) if r else "", res(q, r)))

unit("division", 5, "P",
     "Resuelve divisiones de números de hasta tres cifras entre números de una o dos cifras; interpreta el cociente y el residuo; usa la relación entre la multiplicación y la división para comprobar; resuelve problemas",
     "División con residuo", "División",
     "Ejercicios de matemáticas de 4.º grado de primaria: divisiones entre una y dos cifras, cociente y residuo, la prueba de la división y problemas de reparto. 100 ejercicios con respuestas.",
     "El residuo es menor que el divisor", "Dividendo = divisor × cociente + residuo.",
     ["Para dividir 745 ÷ 6, empieza por la izquierda: 7 ÷ 6 = 1 y sobra 1; bajas el 4: 14 ÷ 6 = 2 y sobran 2; bajas el 5: 25 ÷ 6 = 4 y sobra 1. Cociente 124, residuo 1.",
      "Para dividir entre dos cifras, busca cuántas veces cabe el divisor: 384 ÷ 24 → 38 ÷ 24 = 1 y sobran 14; 144 ÷ 24 = 6. Cociente 16.",
      "<b>Prueba de la división</b>: divisor × cociente + residuo = dividendo. El residuo tiene que ser menor que el divisor."],
     [("Calcula 745 ÷ 6", ["7 ÷ 6 = 1, sobra 1", "14 ÷ 6 = 2, sobran 2", "25 ÷ 6 = 4, sobra 1"], "cociente 124 y residuo 1"), ("Comprueba 124 × 6 + 1", ["744 + 1"], "745")],
     [["Olvidar un cero en el cociente", "618 ÷ 3 = 206, no 26."], ["Dejar un residuo mayor que el divisor", "Si sobra más que el divisor, cabe una vez más."], ["Confundir cociente y residuo", "El cociente es lo que toca a cada uno; el residuo, lo que sobra."]],
     [("¿Qué es el residuo?", "Lo que sobra al repartir en partes iguales. Siempre es menor que el divisor; si es 0, la división es exacta."),
      ("¿Cómo compruebo una división?", "Multiplica el divisor por el cociente y suma el residuo: debe dar el dividendo.")],
     [("Entre una cifra", [(una, 20)]), ("Entre dos cifras", [(dos, 20)]), ("Términos y prueba de la división", [(terminos, 20)]), ("Dividir entre 10, 100 y decenas", [(ceros, 20)]),
      ("Problemas", [(probl, 20)])],
     64005, lv=4)
