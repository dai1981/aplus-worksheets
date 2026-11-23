# -*- coding: utf-8 -*-
"""México 4.º grado: Cálculo mental de dobles, triples, mitades y cuartos; estimación (Multiplicación y división). Problemas propios y España 4.º con otra semilla."""
import random
from mx_common import src, unit, mcq, num

dobles, estimar = src("gen_es_matematicas_4_calculo_mental_y_estimacion", 64208, "s2_dobles", "s3_estimar", mx_=99999)
R = random.Random(64108)


def pick():
    return R.choice([R.randint(12, 99), R.randint(11, 99) * 10, R.randint(101, 499), R.randint(11, 99) * 100, R.randint(2, 40) * 250])


def triple():
    n = pick()
    if 3 * n > 99999:
        return None
    return mcq("¿Cuál es el triple de %s?" % num(n), num(3 * n), [num(2 * n), num(n + 3), num(3 * n + 10), num(3 * n - 10)],
               "El triple es 3 veces el número: %s + %s + %s = <b>%s</b>." % (num(n), num(n), num(n), num(3 * n)))


def cuarto():
    k = R.choice(["mitad", "cuarto", "tercio", "doble_doble"])
    if k == "mitad":
        n = 2 * R.choice([R.randint(13, 99) * 10 + 5, R.randint(51, 499), R.randint(11, 99) * 100 + 50])
        h = n // 2
        return mcq("¿Cuál es la mitad de %s?" % num(n), num(h), [num(2 * n), num(h + 10), num(h - 1), num(h + 5)],
                   "Partimos en dos: %s ÷ 2 = <b>%s</b>. Comprueba: %s + %s = %s." % (num(n), num(h), num(h), num(h), num(n)))
    if k == "cuarto":
        q = R.choice([R.randint(11, 99), R.randint(11, 99) * 10, R.randint(3, 99) * 25])
        n = 4 * q
        return mcq("¿Cuánto es la cuarta parte de %s?" % num(n), num(q), [num(n // 2), num(q * 2), num(q + 4), num(n - 4)],
                   "La cuarta parte es la mitad de la mitad: %s → %s → <b>%s</b>." % (num(n), num(n // 2), num(q)))
    if k == "tercio":
        q = R.choice([R.randint(11, 99), R.randint(11, 99) * 10, R.randint(11, 99) * 100])
        n = 3 * q
        return mcq("¿Cuánto es la tercera parte de %s?" % num(n), num(q), [num(n // 2) if n % 2 == 0 else num(q + 3), num(q * 2), num(n - 3), num(q + 10)],
                   "Repartimos en 3 partes iguales: %s ÷ 3 = <b>%s</b>, porque %s × 3 = %s." % (num(n), num(q), num(q), num(n)))
    n = pick()
    if 4 * n > 99999:
        return None
    return mcq("¿Cuánto es el doble del doble de %s?" % num(n), num(4 * n), [num(2 * n), num(3 * n), num(4 * n + 4), num(n + 4)],
               "El doble de %s es %s, y el doble de %s es <b>%s</b>: es multiplicar por 4." % (num(n), num(2 * n), num(2 * n), num(4 * n)))


COSAS = [("Un boleto de autobús foráneo", "boletos"), ("Una mochila", "mochilas"), ("Una caja de mangos", "cajas"), ("Un balón", "balones"), ("Una lámpara", "lámparas"), ("Un pastel", "pasteles")]


def problema():
    k = R.choice(["doble", "triple", "mitad", "cuarto", "tercio"])
    cosa, pl_ = R.choice(COSAS)
    p = R.choice([R.randint(12, 99) * 10, R.randint(25, 99) * 2, R.randint(5, 40) * 50])
    if k == "doble":
        return mcq("%s cuesta $%s. ¿Cuánto cuestan 2?" % (cosa, num(p)), "$" + num(2 * p), ["$" + num(p + 2), "$" + num(p // 2), "$" + num(3 * p)], "El doble de %s es <b>$%s</b>." % (num(p), num(2 * p)))
    if k == "triple":
        return mcq("%s cuesta $%s. ¿Cuánto cuestan 3?" % (cosa, num(p)), "$" + num(3 * p), ["$" + num(2 * p), "$" + num(p + 3), "$" + num(3 * p + 100)], "El triple de %s es <b>$%s</b>." % (num(p), num(3 * p)))
    if k == "mitad":
        n = 2 * R.randint(150, 4999)
        return mcq("En una feria del libro de Guadalajara hay %s libros. La mitad son de cuentos. ¿Cuántos libros de cuentos hay?" % num(n), num(n // 2), [num(2 * n), num(n // 4) if n % 4 == 0 else num(n // 2 + 1), num(n - 2)],
                   "%s ÷ 2 = <b>%s</b>." % (num(n), num(n // 2)))
    if k == "cuarto":
        q = R.randint(25, 999)
        return mcq("En un estadio hay %s personas. La cuarta parte son niños. ¿Cuántos niños hay?" % num(4 * q), num(q), [num(2 * q), num(4 * q - 4), num(q + 4)],
                   "La mitad de %s es %s y la mitad de %s es <b>%s</b>." % (num(4 * q), num(2 * q), num(2 * q), num(q)))
    q = R.randint(12, 333)
    return mcq("Una cuerda de %s cm se corta en 3 partes iguales. ¿Cuánto mide cada parte?" % num(3 * q), "%s cm" % num(q), ["%s cm" % num(3 * q - 3), "%s cm" % num(q * 2), "%s cm" % num(q + 3)],
               "%s ÷ 3 = <b>%s cm</b>." % (num(3 * q), num(q)))


unit("dobles-triples-y-mitades", 6, "P",
     "Calcula mentalmente dobles, triples, mitades, tercios y cuartos de números naturales; estima resultados de sumas, restas y multiplicaciones; resuelve problemas de cálculo mental",
     "Dobles, triples, mitades y cuartos", "Dobles y mitades",
     "Ejercicios de matemáticas de 4.º grado de primaria: dobles, triples, mitades, la tercera y la cuarta parte, estimar y problemas de cálculo mental. 100 ejercicios con respuestas.",
     "El doble es × 2; la mitad, ÷ 2", "La cuarta parte es la mitad de la mitad.",
     ["El <b>doble</b> es dos veces el número (× 2) y el <b>triple</b>, tres veces (× 3). La <b>mitad</b> es repartir entre 2 y la <b>cuarta parte</b>, entre 4.",
      "Para calcular mentalmente, descompón: el doble de 365 es el doble de 300 (600) + el doble de 65 (130) = 730.",
      "La cuarta parte es la mitad de la mitad: 840 → 420 → 210. Para estimar, redondea primero."],
     [("Triple de 240", ["3 × 200 = 600", "3 × 40 = 120", "600 + 120"], "720"), ("Cuarta parte de 1 000", ["mitad: 500", "mitad: 250"], "250")],
     [["Confundir doble y mitad", "El doble es más grande; la mitad, más pequeña."], ["Calcular el triple como el número + 3", "El triple de 40 es 120, no 43."], ["Hacer solo una mitad", "La cuarta parte de 840 es 210, no 420."]],
     [("¿Qué es el triple de un número?", "Es el número tres veces: el triple de 25 es 25 + 25 + 25 = 75."),
      ("¿Cómo calculo la cuarta parte de memoria?", "Saca la mitad dos veces: la cuarta parte de 600 es la mitad de 300, o sea 150.")],
     [("Dobles y mitades", [(dobles, 20)]), ("Triples", [(triple, 20)]), ("Tercios y cuartos", [(cuarto, 20)]), ("Estimar", [(estimar, 20)]), ("Problemas", [(problema, 20)])],
     64006, lv=4)
