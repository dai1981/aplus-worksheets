# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Números decimales (Sentido numérico)
Décimas, centésimas y milésimas; leer y escribir decimales; fracción decimal y número decimal; valor de las cifras;
comparar, ordenar, redondear y representar en la recta; 6.º: fracción → decimal dividiendo.
Errores: pensar que 2,45 &gt; 2,5 porque 45 &gt; 5, olvidar los ceros (3,05), confundir décimas y milésimas.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, dz, fr, recta, d as dec

R = None
LV = 6
ORD = {1: "décimas", 2: "centésimas", 3: "milésimas"}
ORD1 = {1: "décima", 2: "centésima", 3: "milésima"}


def leer(n, k):
    e, r = divmod(n, 10 ** k)
    while k > 1 and r % 10 == 0:
        r //= 10
        k -= 1
    if r == 0:
        return "%d unidades" % e
    return "%s %s y %s %s" % (num(e), "unidad" if e == 1 else "unidades", num(r), ORD1[k] if r == 1 else ORD[k])


def rn():
    k = R.choice([1, 2, 3, 3] if LV == 6 else [1, 2, 2, 3])
    n = R.randint(10 ** k + 1, 99 * 10 ** k)
    if n % 10 == 0:
        n += R.randint(1, 9)
    return n, k


def s1_fraccion():
    k = R.choice([1, 2, 3])
    n = R.randint(1, 10 ** k - 1)
    if n % 10 == 0:
        return None
    if R.random() < 0.5:
        return M("¿Qué número decimal es %s?" % fr(n, 10 ** k), dz(n, k, keep=True), [dz(n, k - 1, keep=True) if k > 1 else str(n), dz(n, k + 1, keep=True), num(n)], "%s = %d %s = <b>%s</b>." % (fr(n, 10 ** k), n, ORD[k], dz(n, k, keep=True)))
    return M("¿Qué fracción decimal es %s?" % dz(n, k, keep=True), fr(n, 10 ** k), [fr(n, 10 ** (k + 1)), fr(n, 10 ** (k - 1)) if k > 1 else fr(n, 1), fr(10 ** k, n)], "%s = <b>%s</b>." % (dz(n, k, keep=True), fr(n, 10 ** k)))


def s2_leer():
    n, k = rn()
    t = R.choice(["leer", "escribir", "valor"])
    if t == "leer":
        return M("¿Cómo se lee %s?" % dz(n, k, keep=True), leer(n, k), [leer(n, k + 1) if n % 10 and k < 3 else None, leer(n, k - 1) if k > 1 else leer(n * 10, k + 1), leer(n + 10 ** k, k), leer(n + 1, k)], "<b>%s</b>." % leer(n, k))
    if t == "escribir":
        e, r = divmod(n, 10 ** k)
        return M("Escribe con cifras: %s." % leer(n, k), dz(n, k, keep=True), [("%d,%d" % (e, r)) if str(r) != str(r).rjust(k, "0") else None, dz(n, k + 1), dz(n, k - 1) if k > 1 else num(n), dz(n + 10 ** k, k, keep=True)],
                     "<b>%s</b>." % dz(n, k, keep=True))
    s = dz(n, k, keep=True).split(",")[1]
    i = R.randrange(k)
    dg = int(s[i])
    if dg == 0:
        return None
    return M("En el número %s, ¿cuánto vale la cifra %d de las %s?" % (dz(n, k, keep=True), dg, ORD[i + 1]), dz(dg, i + 1, keep=True), [dz(dg, i + 2, keep=True) if i < 2 else str(dg * 10), dz(dg, i, keep=True) if i else str(dg), str(dg)],
             "%d %s = <b>%s</b>." % (dg, ORD[i + 1], dz(dg, i + 1, keep=True)))


def s3_comparar():
    t = R.choice(["dos", "dos", "mayor", "orden"])
    e = R.randint(0, 30)
    if t == "dos":
        a = e * 1000 + R.randint(1, 9) * 100
        b = e * 1000 + R.randint(11, 99) * 10 + (R.randint(1, 9) if LV == 6 else 0)
        if a == b or a // 100 == b // 100:
            return None
        A, B = dec(F(a, 1000)), dec(F(b, 1000))
        ok = "%s %s %s" % (A, "&lt;" if a < b else "&gt;", B)
        return M("Compara %s y %s." % (A, B), ok, ["%s %s %s" % (A, "&gt;" if a < b else "&lt;", B), "%s = %s" % (A, B), "no se pueden comparar"], "Igualamos las cifras decimales: %s y %s → <b>%s</b>." % (dz(a, 3, keep=True), dz(b, 3, keep=True), ok))
    xs = set()
    while len(xs) < 4:
        xs.add(e * 1000 + R.choice([R.randint(1, 9) * 100, R.randint(1, 99) * 10, R.randint(1, 999)]))
    xs = sorted(xs)
    sh = [dec(F(x, 1000)) for x in xs]
    R.shuffle(sh)
    if t == "mayor":
        return M("¿Cuál es el número mayor? %s" % "; ".join(sh), dec(F(xs[-1], 1000)), [dec(F(x, 1000)) for x in xs[:-1]], "Igualamos a milésimas y comparamos: <b>%s</b>." % dec(F(xs[-1], 1000)))
    f = lambda L: " &lt; ".join(dec(F(x, 1000)) for x in L)
    by_len = sorted(xs, key=lambda x: (len(dec(F(x, 1000))), x))
    return M("Ordena de menor a mayor: %s" % "; ".join(sh), f(xs), [f(by_len) if by_len != xs else None, f(xs[::-1]), f([xs[1], xs[0], xs[2], xs[3]]), f([xs[0], xs[2], xs[1], xs[3]])], "<b>%s</b>." % f(xs))


def s4_redondear():
    t = R.choice(["u", "d", "c", "recta"] if LV == 6 else ["u", "d", "recta"])
    n = R.randint(1001, 99999)
    if n % 10 == 0:
        return None
    if t == "recta":
        e = R.randint(0, 9)
        x = R.randint(1, 9)
        g = recta(e * 10, e * 10 + 10, 1, marks=[(e * 10 + x, "?")], labels=[e * 10, e * 10 + 10])
        g = g.replace(">%d<" % (e * 10), ">%d<" % e).replace(">%d<" % (e * 10 + 10), ">%d<" % (e + 1))
        return M(g + "La recta va de %d a %d en décimas. ¿Qué número está en «?»?" % (e, e + 1), dz(e * 10 + x, 1), [dz(e * 10 + x + 1, 1), "%d,0%d" % (e, x), str(e + x), dz(e * 10 + x - 1, 1) if x > 1 else dz(e * 10 + 3, 1)],
                 "Cada marca es una décima: <b>%s</b>." % dz(e * 10 + x, 1))
    p = {"u": 3, "d": 2, "c": 1}[t]
    q = 10 ** p
    r = (n + q // 2) // q * q
    if r == n:
        return None
    nm = {"u": "las unidades", "d": "las décimas", "c": "las centésimas"}[t]
    other = n // q * q if r != n // q * q else n // q * q + q
    f = lambda x: dz(x // q, 3 - p, keep=True)
    return M("Redondea %s a %s." % (dz(n, 3, keep=True), nm), f(r), [f(other), f(r + q) if r + q != other else f(r - q), f(r + 2 * q), dz(n // 10, 2, keep=True) if p == 1 else None],
             "Miramos la cifra siguiente: %s <b>%s</b>." % ("5 o más, hacia arriba:" if r > n else "menor que 5, hacia abajo:", f(r)))


def s5_vida():
    k = R.choice(["salto", "carrera", "precio", "frdec", "altura"] if LV == 6 else ["salto", "carrera", "precio", "altura"])
    if k == "frdec":
        f = R.choice([F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1, 8), F(3, 8), F(7, 10), F(9, 20), F(3, 25), F(13, 50)])
        return M("Escribe %s como número decimal (divide el numerador entre el denominador)." % fr(f.numerator, f.denominator), dec(f), [dz(f.numerator * 10 // f.denominator, 2) if f.numerator * 10 % f.denominator == 0 else "%d,%d" % (f.numerator, f.denominator), "%d,%d" % (f.denominator, f.numerator), dec(f + F(1, 10))],
                 "%d : %d = <b>%s</b>." % (f.numerator, f.denominator, dec(f)))
    if k == "salto":
        ns = R.sample(range(250, 450), 4)
        names = ["Lucía", "Hugo", "Vega", "Leo"]
        m = max(range(4), key=lambda i: ns[i])
        return M("Salto de longitud: %s. ¿Quién saltó más?" % "; ".join("%s, %s m" % (a, dz(b, 2)) for a, b in zip(names, ns)), names[m], names, "%s m es el mayor: <b>%s</b>." % (dz(ns[m], 2), names[m]))
    if k == "carrera":
        ts = R.sample(range(10001, 14999), 4)
        names = ["Ana", "Pablo", "Noa", "Iker"]
        m = min(range(4), key=lambda i: ts[i])
        return M("Tiempos en 100 m (en segundos): %s. ¿Quién ganó?" % "; ".join("%s, %s" % (a, dz(t, 3)) for a, t in zip(names, ts)), names[m], names, "El menor tiempo es %s s: <b>%s</b>." % (dz(ts[m], 3), names[m]))
    if k == "precio":
        a, b = R.randint(105, 999), R.randint(105, 999)
        if a // 10 == b // 10 or a == b:
            return None
        x, y = "una libreta", "un bolígrafo"
        return M("%s cuesta %s € y %s, %s €. ¿Qué es más barato?" % (x.capitalize(), dz(a, 2, keep=True), y, dz(b, 2, keep=True)), x if a < b else y, [y if a < b else x, "cuestan lo mismo", "no se puede saber"],
                 "%s %s %s: <b>%s</b>." % (dz(a, 2, keep=True), "&lt;" if a < b else "&gt;", dz(b, 2, keep=True), x if a < b else y))
    c = R.randint(1201, 1699)
    return M("La altura de Martina es %s m. Redondeada a las centésimas, ¿cuánto mide?" % dz(c, 3), "%s m" % dz((c + 5) // 10, 2, keep=True), ["%s m" % dz(c // 10, 2, keep=True) if c // 10 != (c + 5) // 10 else "%s m" % dz(c // 10 + 1, 2, keep=True), "%s m" % dz((c + 50) // 100, 1), "%s m" % dz(c, 2)],
             "<b>%s m</b>." % dz((c + 5) // 10, 2, keep=True)) if c % 10 and c % 10 != 5 else None


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40008 + lv * 1000)
    seen = set()
    sets = [
        ("Fracciones decimales y decimales", mix(R, seen, [(s1_fraccion, 20)])),
        ("Leer y escribir decimales", mix(R, seen, [(s2_leer, 20)])),
        ("Comparar y ordenar", mix(R, seen, [(s3_comparar, 20)])),
        ("Redondear y la recta numérica", mix(R, seen, [(s4_redondear, 20)])),
        ("Decimales en la vida diaria", mix(R, seen, [(s5_vida, 20)])),
    ]
    body = lesson(
        ["La unidad se divide en 10 <b>décimas</b>, en 100 <b>centésimas</b> o en 1000 <b>milésimas</b>: 0,1 = %s; 0,01 = %s; 0,001 = %s." % (fr(1, 10), fr(1, 100), fr(1, 1000)),
         "En 4,375 hay 4 unidades, 3 décimas, 7 centésimas y 5 milésimas. Se lee «4 unidades y 375 milésimas».",
         "Para comparar, iguala las cifras decimales añadiendo ceros: 2,5 = 2,50 &gt; 2,45."],
        [("Compara 3,7 y 3,68", ["3,70 y 3,68", "70 centésimas &gt; 68 centésimas"], "3,7 &gt; 3,68"),
         ("Redondea 5,463 a las décimas", ["La cifra siguiente es 6", "hacia arriba"], "5,5")],
        [["Creer que 2,45 &gt; 2,5", "Iguala: 2,45 &lt; 2,50."],
         ["Olvidar los ceros", "3 unidades y 5 centésimas = 3,05."],
         ["Confundir décimas y milésimas", "0,7 = siete décimas; 0,007 = siete milésimas."]])
    faq = [("¿Cómo se comparan números decimales?", "Se compara la parte entera; si es igual, se igualan las cifras decimales con ceros y se comparan como números naturales: 2,5 = 2,50 es mayor que 2,45."),
           ("¿Cómo se pasa una fracción a número decimal?", "Se divide el numerador entre el denominador: 3/8 = 3 : 8 = 0,375.")]
    make_unit(R, "numeros-decimales", "N",
              "Números decimales hasta las milésimas: relación con las fracciones decimales, lectura, escritura, valor posicional, comparación, ordenación, representación en la recta y redondeo",
              "Números decimales: hasta las milésimas", "Números decimales",
              "Fichas de matemáticas de %d.º de Primaria: décimas, centésimas y milésimas, leer y escribir decimales, comparar, ordenar, redondear y la recta numérica. 100 ejercicios con soluciones." % lv,
              "Para comparar, iguala las cifras", "2,5 = 2,50: es mayor que 2,45.",
              body, faq, sets, 8, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
