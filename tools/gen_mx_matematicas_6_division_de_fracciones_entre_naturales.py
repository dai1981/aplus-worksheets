# -*- coding: utf-8 -*-
"""México 6.º grado: División de una fracción entre un número natural; multiplicación de fracciones por naturales (Multiplicación y división). Problemas propios y España 6.º con otra semilla."""
import re
import random
from math import gcd
from mx_common import src, unit, mcq, NB
from es_common import fr

pn = src("gen_es_matematicas_6_operaciones_con_fracciones", 66310, "s3_por_natural", lv=6, extra=(lambda it: not re.search(r"</span>\s*×\s*<span class='fr'>|÷| : ", it["q"]),))
R = random.Random(66110)


def fs(n, d):
    g = gcd(n, d)
    n, d = n // g, d // g
    return str(n) if d == 1 else fr(n, d)


def frac():
    d = R.randint(2, 9)
    n = R.randint(1, 2 * d)
    if gcd(n, d) > 1 or n == d:
        return None
    return n, d


def s_div():
    f = frac()
    if not f:
        return None
    n, d = f
    k = R.randint(2, 6)
    ok = fs(n, d * k)
    w = [fs(n * k, d), fs(n, d + k), fs(n + k, d * k) if n + k != n else fs(n, d), fs(k, n * d)]
    simp = "" if gcd(n, d * k) == 1 else " = <b>%s</b>" % ok
    return mcq("Calcula: %s ÷ %d" % (fr(n, d), k), ok, w, "Dividir entre %d es multiplicar el denominador por %d: %s ÷ %d = %s%s." % (k, k, fr(n, d), k, fr(n, d * k) if simp else "<b>%s</b>" % ok, simp))


def s_div_num():
    """cuando el numerador es múltiplo del divisor"""
    d = R.randint(3, 12)
    k = R.randint(2, 5)
    m = R.randint(1, 4)
    n = k * m
    if gcd(n, d) > 1:
        return None
    ok = fs(m, d)
    w = [fs(n, d * k), fs(n * k, d), fs(m, d * k), fs(n - k, d) if n > k else fs(n + k, d)]
    return mcq("Calcula: %s ÷ %d" % (fr(n, d), k), ok, [x for x in w if x != ok],
               "%d ÷ %d = %d, así que %s ÷ %d = <b>%s</b> (también: %s = %s)." % (n, k, m, fr(n, d), k, ok, fr(n, d * k), ok))


SIT = [("Se reparten %s de pizza entre %d amigos en partes iguales. ¿Qué fracción de pizza le toca a cada uno?", "de pizza"),
       ("Una botella con %s de litro de agua de horchata se reparte en %d vasos iguales. ¿Cuánto litro hay en cada vaso?", "de litro"),
       ("Se cortan %s de metro de listón en %d trozos iguales. ¿Cuánto mide cada trozo?", "de metro"),
       ("Se reparten %s de kilo de dulces entre %d niños. ¿Cuánto le toca a cada uno?", "de kilo")]


def s_prob():
    t, u = R.choice(SIT)
    d = R.choice([2, 3, 4, 5, 8])
    n = R.randint(1, d - 1)
    if gcd(n, d) > 1:
        return None
    k = R.randint(2, 6)
    ok = fs(n, d * k)
    q = t % (fr(n, d), k)
    q = q.replace("¿Cuánto litro", "¿Qué fracción de litro")
    return mcq(q, "%s %s" % (ok, u), ["%s %s" % (x, u) for x in (fs(n * k, d), fs(n, d + k), fs(k, d)) if x != ok],
               "%s ÷ %d = <b>%s</b> %s." % (fr(n, d), k, ok, u))


def s_inv():
    """multiplicar y dividir"""
    f = frac()
    if not f:
        return None
    n, d = f
    k = R.randint(2, 5)
    if R.random() < 0.5:
        ok = fs(n * k, d)
        return mcq("Calcula: %s × %d" % (fr(n, d), k), ok, [fs(n, d * k), fs(n * k, d * k), fs(n + k, d)],
                   "Se multiplica el numerador: %s × %d = %s." % (fr(n, d), k, fr(n * k, d) + ("" if fs(n * k, d) == fr(n * k, d) else " = " + fs(n * k, d))))
    ok = fs(n, d * k)
    return mcq("¿Qué operación da lo mismo que %s ÷ %d?" % (fr(n, d), k), "%s × %s" % (fr(n, d), fr(1, k)), ["%s × %d" % (fr(n, d), k), "%s ÷ %s" % (fr(n, d), fr(1, k)), "%s − %d" % (fr(n, d), k)],
               "Dividir entre %d es lo mismo que multiplicar por %s: el resultado es %s." % (k, fr(1, k), ok))


unit("division-de-fracciones-entre-naturales", 5, "P",
     "Divide fracciones entre números naturales y multiplica fracciones por números naturales; interpreta la división como un reparto en partes iguales y resuelve problemas",
     "Dividir fracciones entre un natural", "Fracción ÷ natural",
     "Ejercicios de matemáticas de 6.º grado de primaria: dividir una fracción entre un número natural, multiplicar fracciones por naturales, repartos y problemas. 100 ejercicios con respuestas.",
     "Dividir entre n: denominador × n", "Repartir 3/4 entre 2: cada uno 3/8.",
     ["Dividir una fracción entre un natural es repartirla en partes iguales. Cada parte es más pequeña: %s ÷ 2 = %s." % (fr(3, 4), fr(3, 8)),
      "Regla: se <b>multiplica el denominador</b> por el natural y el numerador se queda igual. Si el numerador se puede dividir, también sirve dividirlo: %s ÷ 3 = %s." % (fr(6, 7), fr(2, 7)),
      "Al multiplicar una fracción por un natural, se multiplica el numerador: %s × 3 = %s = 1 %s." % (fr(2, 5), fr(6, 5), fr(1, 5))],
     [("%s ÷ 4" % fr(2, 3), ["3 × 4 = 12", "%s = %s" % (fr(2, 12), fr(1, 6))], fr(1, 6)), ("Reparte %s de kilo entre 3" % fr(3, 4), ["3 ÷ 3 = 1"], "%s de kilo" % fr(1, 4))],
     [["Multiplicar el numerador al dividir", "%s ÷ 2 no es %s: el resultado debe ser menor." % (fr(3, 4), fr(6, 4))], ["Dividir el denominador", "%s ÷ 2 = %s, no %s." % (fr(1, 4), fr(1, 8), fr(1, 2))], ["Olvidar simplificar", "%s = %s." % (fr(2, 12), fr(1, 6))]],
     [("¿Por qué al dividir se multiplica el denominador?", "Porque cada parte se vuelve más pequeña: la mitad de un cuarto es un octavo, así que 1/4 ÷ 2 = 1/8."),
      ("¿Dividir entre 2 es lo mismo que multiplicar por 1/2?", "Sí. Dividir entre un número es lo mismo que multiplicar por su inverso: 3/5 ÷ 2 = 3/5 × 1/2 = 3/10.")],
     [("Dividir una fracción entre un natural", [(s_div, 20)]), ("Dividir el numerador", [(s_div_num, 20)]), ("Multiplicar y dividir", [(s_inv, 12), (pn, 8)]), ("Repartos", [(s_prob, 20)]), ("Repaso", [(s_div, 10), (pn, 10)])],
     66005, lv=6)
