# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Fracciones (Sentido numérico)
Fracciones equivalentes (amplificar y simplificar, fracción irreducible), comparar y ordenar (mismo denominador, mismo numerador,
reducción a común denominador), fracciones impropias y números mixtos, fracción de una cantidad, fracción y división.
Errores: comparar solo los denominadores, simplificar dividiendo solo el numerador, confundir número mixto e impropia.
"""
import random
from math import gcd
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, fq, fr, tira, NB

R = None
LV = 6


def pair():
    d = R.randint(2, 12 if LV == 6 else 10)
    n = R.randint(1, d - 1)
    if gcd(n, d) != 1:
        return None
    return n, d


def s1_equiv():
    p = pair()
    if not p:
        return None
    n, d = p
    m = R.randint(2, 6)
    k = R.choice(["fr", "hueco", "simp", "irred"])
    if k == "fr":
        return M("¿Qué fracción es equivalente a %s?" % fr(n, d), fr(n * m, d * m), [fr(n + m, d + m), fr(n * m, d), fr(n, d * m), fr(d * m, n * m)], "Multiplicamos los dos términos por %d: <b>%s</b>." % (m, fr(n * m, d * m)))
    if k == "hueco":
        return M("Completa: %s = %s" % (fr(n, d), fr("?", d * m)), str(n * m), [str(n + d * m - d), str(n * m + 1), str(d * m - n), str(n)], "%d × %d = %d, así que %d × %d = <b>%d</b>." % (d, m, d * m, n, m, n * m))
    N, D = n * m, d * m
    if k == "simp":
        return M("Divide los dos términos de %s entre %d." % (fr(N, D), m), fr(n, d), [fr(N - m, D - m), fr(n, D), fr(N, d)], "%d : %d = %d; %d : %d = %d → <b>%s</b>." % (N, m, n, D, m, d, fr(n, d)))
    return M("¿Cuál es la fracción irreducible de %s?" % fr(N, D), fr(n, d), [fr(N // 2, D // 2) if N % 2 == 0 and D % 2 == 0 and m > 2 else fr(n + 1, d + 1), fr(N - 1, D - 1), fr(N, D // m)],
             "Dividimos entre %d (el m.c.d.): <b>%s</b>." % (m, fr(n, d)))


def s2_comparar():
    k = R.choice(["mismo_d", "mismo_n", "comun", "comun", "orden"] if LV == 6 else ["mismo_d", "mismo_n", "comun", "unidad"])
    if k == "mismo_d":
        d = R.randint(4, 15)
        a, b = R.sample(range(1, d + 4), 2)
        ok = "%s %s %s" % (fr(a, d), "&lt;" if a < b else "&gt;", fr(b, d))
        return M("Compara %s y %s." % (fr(a, d), fr(b, d)), ok, ["%s %s %s" % (fr(a, d), "&gt;" if a < b else "&lt;", fr(b, d)), "%s = %s" % (fr(a, d), fr(b, d)), "no se pueden comparar"], "Mismo denominador: mayor numerador, mayor fracción. <b>%s</b>." % ok)
    if k == "mismo_n":
        n = R.randint(1, 5)
        a, b = R.sample(range(n + 1, 13), 2)
        ok = "%s %s %s" % (fr(n, a), "&gt;" if a < b else "&lt;", fr(n, b))
        return M("Compara %s y %s." % (fr(n, a), fr(n, b)), ok, ["%s %s %s" % (fr(n, a), "&lt;" if a < b else "&gt;", fr(n, b)), "%s = %s" % (fr(n, a), fr(n, b)), "no se pueden comparar"], "Mismo numerador: mayor denominador, partes más pequeñas. <b>%s</b>." % ok)
    if k == "unidad":
        d = R.randint(2, 10)
        n = R.choice([R.randint(1, d - 1), d, R.randint(d + 1, 3 * d)])
        ok = "menor que 1" if n < d else "igual a 1" if n == d else "mayor que 1"
        return M("¿La fracción %s es mayor, menor o igual que 1?" % fr(n, d), ok, [x for x in ["menor que 1", "igual a 1", "mayor que 1", "no se puede saber"] if x != ok], "Numerador %d, denominador %d: <b>%s</b>." % (n, d, ok))
    p, q = pair(), pair()
    if not p or not q or p[1] == q[1] or F(*p) == F(*q):
        return None
    a, b = F(*p), F(*q)
    l = p[1] * q[1] // gcd(p[1], q[1])
    if k == "comun":
        ok = "%s %s %s" % (fr(*p), "&lt;" if a < b else "&gt;", fr(*q))
        return M("Compara %s y %s." % (fr(*p), fr(*q)), ok, ["%s %s %s" % (fr(*p), "&gt;" if a < b else "&lt;", fr(*q)), "%s = %s" % (fr(*p), fr(*q)), "no se pueden comparar"],
                 "Común denominador %d: %s y %s → <b>%s</b>." % (l, fr(p[0] * l // p[1], l), fr(q[0] * l // q[1], l), ok))
    r = pair()
    if not r or len({a, b, F(*r)}) < 3:
        return None
    xs = sorted([p, q, r], key=lambda t: F(*t))
    f_ = lambda L: " &lt; ".join(fr(*t) for t in L)
    by_d = sorted([p, q, r], key=lambda t: -t[1])
    return M("Ordena de menor a mayor: %s, %s, %s" % (fr(*p), fr(*q), fr(*r)), f_(xs), [f_(xs[::-1]), f_(by_d), f_([xs[1], xs[0], xs[2]]), f_([xs[0], xs[2], xs[1]])], "Reducimos a común denominador y comparamos: <b>%s</b>." % f_(xs))


def s3_mixtos():
    d = R.randint(2, 9)
    e = R.randint(1, 5)
    n = R.randint(1, d - 1)
    t = e * d + n
    if R.random() < 0.5:
        return M("Escribe %s como número mixto." % fr(t, d), "%d%s%s" % (e, NB, fr(n, d)), ["%d%s%s" % (n, NB, fr(e, d)) if e < d else "%d%s%s" % (e + 1, NB, fr(n, d)), "%d%s%s" % (e + 1, NB, fr(n, d)), "%d%s%s" % (e, NB, fr(n + 1, d)) if n + 1 < d else "%d%s%s" % (e - 1 if e > 1 else e + 2, NB, fr(n, d))],
                 "%d : %d = %d y resto %d: <b>%d %s</b>." % (t, d, e, n, e, fr(n, d)))
    return M("Escribe %d%s%s como fracción." % (e, NB, fr(n, d)), fr(t, d), [fr(e + n, d), fr(e * n, d), fr(t, d * e), fr(t + d, d)], "%d × %d + %d = %d: <b>%s</b>." % (e, d, n, t, fr(t, d)))


def s4_cantidad():
    d = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
    n = R.randint(1, d - 1)
    t = d * R.randint(3, 40)
    k = R.choice(["calc", "ctx", "div", "todo"])
    r = t // d * n
    if k == "calc":
        return M("Calcula %s de %d." % (fr(n, d), t), num(r), [num(t // d), num(t * n), num(t - r), num(r + d)], "%d : %d = %d; %d × %d = <b>%s</b>." % (t, d, t // d, t // d, n, num(r)))
    if k == "ctx":
        c = R.choice([("En un colegio hay %d alumnos y %s van al comedor. ¿Cuántos alumnos van al comedor?", "alumnos"), ("Un depósito tiene %d litros y se gastan %s. ¿Cuántos litros se gastan?", "litros"),
                      ("Una bicicleta cuesta %d € y tiene un descuento de %s del precio. ¿Cuántos euros de descuento son?", "€"), ("Un libro tiene %d páginas y Vega ha leído %s. ¿Cuántas páginas ha leído?", "páginas")])
        return M(c[0] % (t, fr(n, d)), num(r), [num(t // d) if n > 1 else num(t // d + 1), num(t - r), num(t * n), num(r + n)], "%d : %d × %d = <b>%s</b>." % (t, d, n, num(r)))
    if k == "div":
        a, b = R.randint(1, 9), R.randint(2, 9)
        return M("¿Qué fracción es igual a la división %d : %d?" % (a, b), fr(a, b), [fr(b, a), fr(a + b, b), fr(1, a * b) if a > 1 else fr(2, b + 1)], "Una fracción es una división: numerador : denominador. <b>%s</b>." % fr(a, b))
    return M("%s de un número es %d. ¿Cuál es el número?" % (fr(n, d), r), num(t), [num(r * n), num(r // n * d + d) if r % n == 0 else num(t + d), num(r * d), num(r + d)] if n > 1 else [num(r + d), num(r * 2), num(t + d), num(t - d)],
             "%d : %d = %d es una parte; %d partes: %d × %d = <b>%s</b>." % (r, n, r // n, d, r // n, d, num(t)))


def s5_problema():
    k = R.choice(["queda", "tarta", "comparar", "dinero", "viaje"])
    if k == "queda":
        d = R.choice([4, 5, 6, 8, 10])
        n = R.randint(1, d - 2)
        t = d * R.randint(5, 30)
        return M("Una clase tiene %d € para una excursión. Gasta %s en el autobús. ¿Cuánto dinero le queda?" % (t, fr(n, d)), "%d €" % (t - t // d * n), ["%d €" % (t // d * n), "%d €" % (t - n), "%d €" % (t // d), "%d €" % (t - t // d)],
                 "Gasta %d : %d × %d = %d €; quedan %d − %d = <b>%d €</b>." % (t, d, n, t // d * n, t, t // d * n, t - t // d * n))
    if k == "tarta":
        d = R.choice([8, 10, 12])
        a, b = R.randint(1, d // 3), R.randint(1, d // 3)
        q = d - a - b
        return M("De una tarta, Hugo come %s y Lucía %s. ¿Qué fracción de tarta queda?" % (fr(a, d), fr(b, d)), fq(F(q, d)), [fq(F(a + b, d)), fr(q, 2 * d), fq(F(d - a, d)), fr(q + 1, d)],
                 "%s − %s − %s = %s%s." % (fr(d, d), fr(a, d), fr(b, d), fr(q, d), " = %s" % fq(F(q, d)) if F(q, d).denominator != d else ""))
    if k == "comparar":
        p, q = pair(), pair()
        if not p or not q or F(*p) == F(*q):
            return None
        big = "Martina" if F(*p) > F(*q) else "Álvaro"
        return M("Martina ha leído %s de un libro y Álvaro %s del mismo libro. ¿Quién ha leído más?" % (fr(*p), fr(*q)), big, ["Álvaro" if big == "Martina" else "Martina", "los dos lo mismo", "no se puede saber"],
                 "Común denominador: %s y %s → <b>%s</b>." % (fr(p[0] * q[1], p[1] * q[1]), fr(q[0] * p[1], p[1] * q[1]), big))
    if k == "dinero":
        d = R.choice([3, 4, 5])
        n = R.randint(1, d - 1)
        t = d * R.randint(4, 25)
        return M("Unos patines cuestan %d €. Pablo ya ha ahorrado %s del precio. ¿Cuánto le falta?" % (t, fr(n, d)), "%d €" % (t - t // d * n), ["%d €" % (t // d * n), "%d €" % (t - n), "%d €" % (t // d)],
                 "Tiene %d €; le faltan %d − %d = <b>%d €</b>." % (t // d * n, t, t // d * n, t - t // d * n))
    d = R.choice([3, 4, 5, 6])
    n = R.randint(1, d - 1)
    km = d * R.randint(20, 90)
    return M("Un viaje tiene %d km. Ya se han recorrido %s del camino. ¿Cuántos kilómetros se han recorrido?" % (km, fr(n, d)), "%d km" % (km // d * n), ["%d km" % (km - km // d * n), "%d km" % (km // d), "%d km" % (km * n)],
             "%d : %d × %d = <b>%d km</b>." % (km, d, n, km // d * n))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40006 + lv * 1000)
    seen = set()
    sets = [
        ("Fracciones equivalentes", mix(R, seen, [(s1_equiv, 20)])),
        ("Comparar y ordenar fracciones", mix(R, seen, [(s2_comparar, 20)])),
        ("Números mixtos", mix(R, seen, [(s3_mixtos, 20)])),
        ("Fracción de una cantidad", mix(R, seen, [(s4_cantidad, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dos fracciones son <b>equivalentes</b> si representan la misma cantidad. Se obtienen multiplicando (<b>amplificar</b>) o dividiendo (<b>simplificar</b>) los dos términos por el mismo número. La fracción <b>irreducible</b> ya no se puede simplificar.",
         "Para comparar fracciones con distinto denominador, <b>redúcelas a común denominador</b> y compara los numeradores.",
         "Si el numerador es mayor que el denominador, la fracción es mayor que 1 y se puede escribir como <b>número mixto</b>: %s = 2%s%s." % (fr(11, 4), NB, fr(3, 4))],
        [("Compara %s y %s" % (fr(2, 3), fr(3, 4)), ["Común denominador 12", "%s y %s" % (fr(8, 12), fr(9, 12))], "%s &lt; %s" % (fr(2, 3), fr(3, 4))),
         ("%s de 45" % fr(3, 5), ["45 : 5 = 9", "9 × 3"], "27")],
        [["Comparar solo los denominadores", "%s no es mayor que %s: 8 partes son más pequeñas." % (fr(1, 8), fr(1, 4))],
         ["Simplificar solo un término", "Divide numerador y denominador entre el mismo número."],
         ["Leer mal el número mixto", "2%s%s = 2 + %s = %s." % (NB, fr(3, 4), fr(3, 4), fr(11, 4))]],
        "<div>%s%s</div>" % (tira(3, 2, 260), tira(6, 4, 260)))
    faq = [("¿Cómo se comparan fracciones con distinto denominador?", "Se reducen a común denominador (por ejemplo, con el m.c.m. de los denominadores) y se compara el numerador: es mayor la fracción con mayor numerador."),
           ("¿Qué es una fracción irreducible?", "Una fracción que no se puede simplificar más porque el numerador y el denominador solo tienen el 1 como divisor común, como 3/4.")]
    make_unit(R, "fracciones", "N",
              "Fracciones: fracciones equivalentes, simplificación y fracción irreducible; comparación y ordenación; fracciones impropias y números mixtos; fracción de una cantidad; la fracción como división",
              "Fracciones: equivalentes, comparar y mixtos", "Fracciones",
              "Fichas de matemáticas de %d.º de Primaria: fracciones equivalentes, simplificar, comparar y ordenar fracciones, números mixtos, fracción de una cantidad y problemas. 100 ejercicios con soluciones." % lv,
              "Común denominador para comparar", "Simplifica dividiendo arriba y abajo.",
              body, faq, sets, 6, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
