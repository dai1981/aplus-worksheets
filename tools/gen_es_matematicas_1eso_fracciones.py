# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Fracciones (Sentido numérico)
Fracciones equivalentes y simplificación, comparar y ordenar, sumar y restar (m.c.m.), multiplicar y dividir, fracción de una cantidad, problemas.
Errores: sumar numeradores y denominadores, no simplificar, dividir sin invertir la segunda fracción.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, fq, unit, L, Kids, tira, num

R = random.Random(47004)
K = Kids(R)


def rf(lo=2, hi=12, proper=True):
    while True:
        dd = R.randint(lo, hi)
        n = R.randint(1, dd - 1 if proper else 2 * dd)
        if math.gcd(n, dd) == 1:
            return F(n, dd)


def raw(n, dd):
    from es_eso import fr
    return fr(n, dd)


def s_equiv():
    t = R.choice(["simp", "simp", "equiv", "falta", "irred"])
    if t == "simp":
        f = rf(2, 12)
        k = R.randint(2, 9)
        n, dd = f.numerator * k, f.denominator * k
        return M("Simplifica hasta la fracción irreducible: %s" % raw(n, dd), fq(f), [raw(f.numerator + 1, f.denominator), raw(n // k, dd), fq(F(dd, n)) if n != dd else None] + ([raw(n // 2, dd // 2)] if (n % 2 == 0 and dd % 2 == 0 and F(n // 2, dd // 2).numerator != f.numerator) else []),
                 "Dividimos numerador y denominador entre m.c.d.(%d, %d) = %d: <b>%s</b>." % (n, dd, k, fq(f)))
    if t == "equiv":
        f = rf(2, 9)
        k = R.randint(2, 8)
        ok = raw(f.numerator * k, f.denominator * k)
        return M("¿Qué fracción es equivalente a %s?" % fq(f), ok, [raw(f.numerator * k, f.denominator * (k + 1)), raw(f.numerator + k, f.denominator + k), raw(f.numerator * k, f.denominator + k)],
                 "Multiplicamos numerador y denominador por %d: <b>%s</b>." % (k, ok))
    if t == "falta":
        f = rf(2, 9)
        k = R.randint(2, 7)
        return M("¿Qué número falta? %s = %s" % (fq(f), raw(0, f.denominator * k).replace("<span class='fn'>0</span>", "<span class='fn'>?</span>")), str(f.numerator * k),
                 [str(f.numerator + k), str(f.numerator * k + 1), str(f.denominator * k - f.numerator)], "El denominador se multiplicó por %d; el numerador también: <b>%d</b>." % (k, f.numerator * k))
    fs = [rf(2, 12) for _ in range(1)][0]
    k = R.randint(2, 5)
    ws = [raw(fs.numerator * k, fs.denominator * k)]
    g = rf(2, 12)
    while g == fs:
        g = rf(2, 12)
    ws += [raw(g.numerator * 2, g.denominator * 2), raw(R.choice([2, 4, 6]), R.choice([8, 10, 12]))]
    return M("¿Cuál de estas fracciones es irreducible?", fq(fs), ws, "Numerador y denominador no tienen divisores comunes: <b>%s</b>." % fq(fs)) if len(set(ws)) == 3 else None


def s_comparar():
    a, b = rf(2, 12), rf(2, 12)
    if a == b:
        return None
    t = R.choice(["mayor", "orden"])
    if t == "mayor":
        ok = max(a, b)
        return M("¿Qué fracción es mayor: %s o %s?" % (fq(a), fq(b)), fq(ok), [fq(min(a, b)), "son iguales", "no se puede saber"], "Reducimos a común denominador o pasamos a decimal: <b>%s</b> es mayor." % fq(ok))
    c = rf(2, 12)
    if c in (a, b):
        return None
    xs = [a, b, c]
    ok = " &lt; ".join(fq(x) for x in sorted(xs))
    w1 = " &lt; ".join(fq(x) for x in sorted(xs, key=lambda x: x.denominator))
    w2 = " &lt; ".join(fq(x) for x in sorted(xs, reverse=True))
    w3 = " &lt; ".join(fq(x) for x in sorted(xs, key=lambda x: x.numerator))
    return M("Ordena de menor a mayor: %s, %s, %s" % (fq(a), fq(b), fq(c)), ok, [w1, w2, w3], "Con común denominador se comparan los numeradores: <b>%s</b>." % ok)


def s_suma():
    a, b = rf(2, 10), rf(2, 10)
    t = R.choice(["+", "-", "+", "int"])
    if t == "+":
        r = a + b
        w = raw(a.numerator + b.numerator, a.denominator + b.denominator)
        return M("Calcula y simplifica: %s + %s" % (fq(a), fq(b)), fq(r), [w, fq(a * b), fq(r + F(1, r.denominator))], "m.c.m. de los denominadores y sumamos numeradores: <b>%s</b>." % fq(r))
    if t == "-":
        if a < b:
            a, b = b, a
        if a == b:
            return None
        r = a - b
        w = raw(abs(a.numerator - b.numerator), abs(a.denominator - b.denominator)) if a.denominator != b.denominator else fq(r + F(1, r.denominator))
        return M("Calcula y simplifica: %s − %s" % (fq(a), fq(b)), fq(r), [w, fq(a + b), fq(r + F(1, r.denominator)) if r + F(1, r.denominator) != a + b else fq(r * 2)], "Común denominador y restamos numeradores: <b>%s</b>." % fq(r))
    n = R.randint(1, 4)
    r = n - a
    return M("Calcula: %d − %s" % (n, fq(a)), fq(r), [raw(abs(n - a.numerator), a.denominator) if n != a.numerator else "0", fq(n + a), fq(r + F(1, a.denominator))], "%d = %s, y restamos: <b>%s</b>." % (n, raw(n * a.denominator, a.denominator), fq(r)))


def s_mult():
    a, b = rf(2, 9, False), rf(2, 9)
    t = R.choice(["x", ":", "x", ":", "comb"])
    if t == "x":
        r = a * b
        return M("Calcula y simplifica: %s · %s" % (fq(a), fq(b)), fq(r), [fq(a / b), raw(a.numerator * b.numerator, a.denominator + b.denominator), fq(a + b)], "Numerador por numerador y denominador por denominador: <b>%s</b>." % fq(r))
    if t == ":":
        r = a / b
        return M("Calcula y simplifica: %s : %s" % (fq(a), fq(b)), fq(r), [fq(a * b), fq(b / a) if b != a else None, fq(r + 1)], "Multiplicamos por la inversa de %s: <b>%s</b>." % (fq(b), fq(r)))
    c = rf(2, 6)
    r = a + b * c
    return M("Calcula: %s + %s · %s" % (fq(a), fq(b), fq(c)), fq(r), [fq((a + b) * c), fq(a * b + c), fq(r + 1)], "Primero la multiplicación, después la suma: <b>%s</b>." % fq(r))


def s_problema():
    p = K.next()
    t = R.choice(["de", "resto", "total", "suma", "dos"])
    if t == "de":
        f = rf(2, 8)
        n = f.denominator * R.randint(3, 25)
        r = n * f
        return M("En un instituto hay %d alumnos y %s van en autobús. ¿Cuántos alumnos van en autobús?" % (n, fq(f)), num(int(r)), [num(n // f.denominator), num(n - int(r)), num(int(r) + f.denominator)],
                 "%d : %d = %d; %d · %d = <b>%d</b>." % (n, f.denominator, n // f.denominator, n // f.denominator, f.numerator, int(r)))
    if t == "resto":
        f = rf(2, 8)
        n = f.denominator * R.randint(3, 20)
        r = n - n * f
        return M("%s tiene %d € y gasta %s. ¿Cuánto dinero le queda?" % (p[0], n, fq(f)), "%d €" % int(r), ["%d €" % int(n * f), "%d €" % (n - f.numerator), "%d €" % (n // f.denominator)], "Gasta %d €; le quedan %d − %d = <b>%d €</b>." % (int(n * f), n, int(n * f), int(r)))
    if t == "total":
        f = rf(2, 8)
        part = f.numerator * R.randint(2, 12)
        tot = part / f
        return M("%s de un depósito son %d litros. ¿Cuántos litros caben en el depósito?" % (fq(f), part), "%d L" % int(tot), ["%d L" % int(part * f) if (part * f).denominator == 1 else "%d L" % (part + f.denominator), "%d L" % (part + f.denominator), "%d L" % (part * f.denominator)],
                 "%d : %d = %d es %s; el total es %d · %d = <b>%d L</b>." % (part, f.numerator, part // f.numerator, fq(F(1, f.denominator)), part // f.numerator, f.denominator, int(tot)))
    if t == "suma":
        a, b = rf(3, 10), rf(3, 10)
        if a + b >= 1:
            return None
        r = 1 - a - b
        return M("%s lee %s de un libro el lunes y %s el martes. ¿Qué fracción del libro le queda por leer?" % (p[0], fq(a), fq(b)), fq(r), [fq(a + b), fq(1 - a), fq(r + F(1, r.denominator))], "1 − %s − %s = <b>%s</b>." % (fq(a), fq(b), fq(r)))
    a = rf(2, 5)
    n = a.denominator * R.randint(4, 12)
    b = rf(2, 4)
    rest = n - n * a
    if (rest * b).denominator != 1:
        return None
    r = rest - rest * b
    return M("Una tienda tiene %d camisetas. Vende %s el sábado y %s de las que quedan el domingo. ¿Cuántas camisetas quedan?" % (n, fq(a), fq(b)), str(int(r)),
             [str(int(rest)), str(int(n - n * a - n * b)) if (n * b).denominator == 1 and n - n * a - n * b > 0 else str(int(r) + 1), str(int(rest * b))],
             "Quedan %d tras el sábado; vende %d el domingo; quedan <b>%d</b>." % (int(rest), int(rest * b), int(r)))


seen = set()
sets = [("Equivalentes y simplificar", mix(R, seen, [(s_equiv, 20)])), ("Comparar y ordenar", mix(R, seen, [(s_comparar, 20)])), ("Sumar y restar", mix(R, seen, [(s_suma, 20)])),
        ("Multiplicar y dividir", mix(R, seen, [(s_mult, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["Dos fracciones son <b>equivalentes</b> si representan la misma cantidad: 2/3 = 4/6. Para <b>simplificar</b>, dividimos arriba y abajo entre el mismo número.",
          "Para sumar o restar, reducimos a común denominador (el m.c.m.) y sumamos o restamos los numeradores.",
          "Para multiplicar, numerador por numerador y denominador por denominador. Para dividir, multiplicamos por la <b>inversa</b>."],
         [("2/3 + 1/4", ["m.c.m.(3, 4) = 12", "8/12 + 3/12"], "11/12"), ("3/5 : 9/10", ["3/5 · 10/9", "30/45"], "2/3")],
         [["Sumar numeradores y denominadores", "1/2 + 1/3 no es 2/5: es 5/6."], ["Dividir sin dar la vuelta a la segunda", "a/b : c/d = a/b · d/c."], ["Dejar el resultado sin simplificar", "6/8 = 3/4."]],
         tira(4, 3))
faq = [("¿Cómo se calcula la fracción de una cantidad?", "Se divide la cantidad entre el denominador y se multiplica por el numerador: 3/4 de 20 = 15."),
       ("¿Qué es una fracción irreducible?", "La que no se puede simplificar más, porque numerador y denominador no tienen divisores comunes.")]
unit(1, R, "fracciones", "N", "Fracciones: equivalencia, simplificación, comparación y ordenación; operaciones con fracciones; fracción de una cantidad; resolución de problemas",
     "Fracciones y operaciones", "Fracciones",
     "Fichas de matemáticas de 1.º de ESO: fracciones equivalentes, simplificar, comparar, sumar, restar, multiplicar, dividir y problemas. 100 ejercicios con soluciones.",
     "Para sumar, común denominador", "Para dividir, multiplica por la inversa.", body, faq, sets, 4)
