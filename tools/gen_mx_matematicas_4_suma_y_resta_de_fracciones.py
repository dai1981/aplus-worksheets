# -*- coding: utf-8 -*-
"""México 4.º grado: Suma y resta de fracciones con igual y distinto denominador usando fracciones equivalentes (Suma y resta). Reutiliza España 5.º/4.º con otra semilla."""
import re
import random
from math import gcd
from fractions import Fraction
from mx_common import src, unit, mcq as _mcq
from es_common import fr


def dens(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    ds = [int(d) for d in re.findall(r"class='fd'>(\d+)<", t)]
    return ds and max(ds) <= 12 and not re.search(r"\d\s*<span class='fr'>|mixto|m\.c\.m|mínimo común", t)


def multiplo(it):
    ds = [int(d) for d in re.findall(r"class='fd'>(\d+)<", it["q"])]
    return all(max(ds) % d == 0 for d in ds)


def es_suma(it):
    return " + " in re.sub(r"<[^>]*>", "", it["q"])


def es_resta(it):
    return " − " in re.sub(r"<[^>]*>", "", it["q"])


mismo, distinto, probl = src("gen_es_matematicas_6_operaciones_con_fracciones", 64314, "s1_mismo", "s2_distinto", "s5_problema", lv=5, extra=(dens, multiplo, lambda it: "×" not in it["e"]))
R = random.Random(64114)


def val(h):
    m = re.search(r"class='fn'>(\d+)<.*class='fd'>(\d+)<", h)
    return Fraction(int(m.group(1)), int(m.group(2))) if m else None


def mcq(q, ok, w, e):
    v = val(ok)
    return _mcq(q, ok, [x for x in w if val(x) != v], e)
PARES = [(b, d) for b in range(2, 7) for d in range(b * 2, 13, b)]


def simp(n, d):
    g = gcd(n, d)
    return n // g, d // g


def frs(n, d):
    a, b = simp(n, d)
    return fr(n, d) if (a, b) == (n, d) else "%s = %s" % (fr(n, d), fr(a, b))


def dist(op):
    def mk():
        b, d = R.choice(PARES)
        k = d // b
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if gcd(a, b) > 1 or gcd(c, d) > 1:
            return None
        x, y = (a * k, c) if R.random() < 0.6 else (c, a * k)
        f1, f2 = ((fr(a, b), fr(c, d)) if x == a * k else (fr(c, d), fr(a, b)))
        n = x + y if op == "+" else x - y
        if n <= 0:
            return None
        A, B = simp(n, d)
        ok = fr(A, B)
        w = [fr(x + y if op == "+" else abs(a - c), b + d) if op == "+" or a != c else fr(a + c, b + d), fr(n, b) if n < 2 * b and simp(n, b) != (A, B) else fr(n + 1, d),
             fr(a + c if op == "+" else max(a, c) - min(a, c) + 1, d), fr(A + 1, B)]
        e = "%s = %s; %s %s %s = %s." % (fr(a, b), fr(a * k, d), fr(x, d), op.replace("-", "−"), fr(y, d), frs(n, d))
        return mcq("Calcula y simplifica: %s %s %s" % (f1, op.replace("-", "−"), f2), ok, w, e)
    mk.__name__ = "dist" + op
    return mk


COSAS = [("pastel", "come", "comen"), ("pizza", "come", "comen"), ("barda", "pinta", "pintan"), ("terreno", "siembra", "siembran"), ("cuerda", "usa", "usan")]


def prob():
    b, d = R.choice(PARES)
    k = d // b
    a, c = R.randint(1, b - 1), R.randint(1, d - 1)
    p, q = R.sample(["Ximena", "Diego", "Regina", "Mateo", "Itzel", "Emiliano", "Camila", "Rodrigo"], 2)
    t = R.choice(["junto", "resto", "mas"])
    cosa, v1, v2 = R.choice(COSAS)
    if gcd(a, b) > 1 or gcd(c, d) > 1:
        return None
    art = "una" if cosa in ("pizza", "barda", "cuerda") else "un"
    if t == "junto":
        n = a * k + c
        if n > d:
            return None
        A, B = simp(n, d)
        return mcq("De %s %s, %s %s %s y %s, %s. ¿Qué fracción %s entre los dos?" % (art, cosa, p, v1, fr(a, b), q, fr(c, d), v2), fr(A, B), [fr(a + c, b + d), fr(n, b) if n != b else fr(n + 1, d), fr(A + 1, B) if A + 1 < B else fr(1, d)],
                   "%s = %s; %s + %s = %s." % (fr(a, b), fr(a * k, d), fr(a * k, d), fr(c, d), frs(n, d)))
    if t == "resto":
        n = d - a * k - c
        if n <= 0:
            return None
        A, B = simp(n, d)
        return mcq("De %s %s, %s %s %s y %s, %s. ¿Qué fracción queda?" % (art, cosa, p, v1, fr(a, b), q, fr(c, d)), fr(A, B), [fr(a * k + c, d), fr(b + d - a - c, b + d), fr(A + 1, B) if A + 1 < B else fr(2, d + 1)],
                   "Entre los dos: %s + %s = %s; queda %s − %s = %s." % (fr(a * k, d), fr(c, d), fr(a * k + c, d), fr(d, d), fr(a * k + c, d), frs(n, d)))
    x, y = a * k, c
    if x == y:
        return None
    m, mn = (p, q) if x > y else (q, p)
    n = abs(x - y)
    A, B = simp(n, d)
    return mcq("De %s %s, %s %s %s y %s, %s. ¿Cuánto más %s %s?" % (art, cosa, p, v1, fr(a, b), q, fr(c, d), v1, m), fr(A, B), [fr(abs(a - c) if a != c else 1, abs(b - d)), fr(x + y, d) if x + y <= d else fr(n + 1, d), fr(A + 1, B) if A + 1 < B else fr(1, d + 1)],
               "%s = %s; %s − %s = %s." % (fr(a, b), fr(x, d), fr(max(x, y), d), fr(min(x, y), d), frs(n, d)))
suma4, prob4 = src("gen_es_matematicas_4_fracciones", 64214, "s4_suma", "s5_problema", extra=(dens,))

unit("suma-y-resta-de-fracciones", 12, "S",
     "Resuelve sumas y restas de fracciones con el mismo denominador y con denominadores distintos, uno múltiplo del otro, usando fracciones equivalentes; resuelve problemas",
     "Suma y resta de fracciones", "Suma y resta de fracciones",
     "Ejercicios de matemáticas de 4.º grado de primaria: sumar y restar fracciones con igual denominador y con distinto denominador usando fracciones equivalentes. 100 ejercicios con respuestas.",
     "Primero, el mismo denominador", "Se suman los numeradores, no los denominadores.",
     ["Con el <b>mismo denominador</b>, se suman o restan los numeradores y el denominador se queda igual: %s + %s = %s." % (fr(2, 9), fr(5, 9), fr(7, 9)),
      "Con <b>denominadores distintos</b>, primero busca fracciones equivalentes con el mismo denominador: %s + %s = %s + %s = %s." % (fr(1, 2), fr(1, 6), fr(3, 6), fr(1, 6), fr(4, 6)),
      "Si el resultado se puede simplificar, simplifícalo: %s = %s." % (fr(4, 6), fr(2, 3))],
     [("%s + %s" % (fr(1, 3), fr(2, 9)), ["%s = %s" % (fr(1, 3), fr(3, 9)), "3 + 2 = 5"], fr(5, 9)), ("%s − %s" % (fr(4, 5), fr(3, 10)), ["%s = %s" % (fr(4, 5), fr(8, 10)), "8 − 3 = 5"], "%s = %s" % (fr(5, 10), fr(1, 2)))],
     [["Sumar numeradores y denominadores", "%s + %s no es %s." % (fr(1, 2), fr(1, 6), fr(2, 8))], ["Cambiar solo el denominador", "%s = %s: el numerador también se multiplica." % (fr(1, 3), fr(3, 9))],
      ["Olvidar simplificar", "%s se puede escribir %s." % (fr(5, 10), fr(1, 2))]],
     [("¿Por qué no se suman los denominadores?", "Porque el denominador dice el tamaño de las partes. Si sumas tercios con tercios, siguen siendo tercios: 1/3 + 1/3 = 2/3."),
      ("¿Cómo sumo fracciones con distinto denominador?", "Convierte una de ellas en una fracción equivalente con el mismo denominador que la otra. Por ejemplo, 1/2 = 3/6, y así 1/2 + 1/6 = 3/6 + 1/6 = 4/6.")],
     [("Mismo denominador", [(mismo, 12), (suma4, 8)]), ("Distinto denominador: sumar", [(dist("+"), 20)]), ("Distinto denominador: restar", [(dist("-"), 20)]),
      ("Problemas con el mismo denominador", [(prob4, 20)]), ("Problemas", [(prob, 14), (probl, 6)])],
     64012, lv=4)
