# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Múltiplos y divisores (Sentido numérico)
Múltiplos de un número (la tabla y más allá), divisores, «es múltiplo de», «es divisor de», criterios de divisibilidad
por 2, 5 y 10 (y por 3), números pares e impares, números primos y compuestos sencillos.
Errores: confundir múltiplo y divisor, olvidar el 1 y el propio número entre los divisores.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, DIV, bank

R = random.Random(44008)


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def s1_multiplos():
    k = R.choice(["es", "lista", "siguiente", "entre"])
    a = R.randint(2, 12)
    if k == "es":
        m = a * R.randint(3, 15)
        ws = sorted({m + 1, m - 1, m + a // 2 if a > 2 else m + 3, a * 10 + 1, m + 2} - {m})
        ws = [w for w in ws if w % a]
        R.shuffle(ws)
        return mcq("¿Cuál de estos números es múltiplo de %d?" % a, str(m), [str(w) for w in ws], "%d = %d %s %d: <b>%d</b> es múltiplo de %d." % (m, a, POR, m // a, m, a))
    if k == "lista":
        st = R.randint(1, 6)
        ok = ", ".join(str(a * i) for i in range(st, st + 4))
        w1 = ", ".join(str(a + i) for i in range(st, st + 4))
        w2 = ", ".join(str(x) for x in divs(a * 6)[:4]) if len(divs(a * 6)) >= 4 else None
        w3 = ", ".join(str(a * i + 1) for i in range(st, st + 4))
        return mcq("¿Qué lista tiene solo múltiplos de %d?" % a, ok, [w1, w2, w3, ", ".join(str(a * i) for i in range(st, st + 3)) + ", %d" % (a * (st + 3) + 1)],
                   "Los múltiplos de %d se obtienen multiplicando %d por 1, 2, 3, …: <b>%s</b>." % (a, a, ok))
    if k == "siguiente":
        n = R.randint(20, 150)
        nx = (n // a + 1) * a
        return mcq("¿Cuál es el primer múltiplo de %d mayor que %d?" % (a, n), str(nx), [str(n + 1) if (n + 1) % a else str(n + 2), str(nx + a), str(nx - a) if nx - a > n else str(nx + 2 * a), str(n + a) if (n + a) != nx else str(nx + 1)],
                   "%d %s %d = %d: <b>%d</b>." % (a, POR, nx // a, nx, nx))
    lo = R.randint(10, 60)
    hi = lo + R.randint(15, 30)
    c = len([x for x in range(lo, hi + 1) if x % a == 0])
    if c < 2:
        return None
    return mcq("¿Cuántos múltiplos de %d hay entre %d y %d (los dos incluidos)?" % (a, lo, hi), str(c), [str(c + 1), str(c - 1), str(hi - lo), str(c + 2)],
               "Son %s: <b>%d</b>." % (", ".join(str(x) for x in range(lo, hi + 1) if x % a == 0), c))


def s2_divisores():
    k = R.choice(["todos", "es", "cuantos", "no"])
    n = R.choice([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72, 80, 90, 96, 100, 15, 21, 27, 35])
    D = divs(n)
    if k == "todos":
        ok = ", ".join(map(str, D))
        w1 = ", ".join(map(str, D[1:-1]))
        w2 = ", ".join(map(str, D[:-1]))
        w3 = ", ".join(str(n * i) for i in range(1, 5))
        return mcq("¿Cuáles son todos los divisores de %d?" % n, ok, [w1, w2, w3], "Buscamos parejas que multiplicadas den %d: <b>%s</b>." % (n, ok))
    if k == "es":
        d = R.choice(D[1:-1])
        ws = [x for x in range(2, 13) if n % x]
        R.shuffle(ws)
        return mcq("¿Cuál de estos números es divisor de %d?" % n, str(d), [str(x) for x in ws] + [str(n * 2)], "%d %s %d = %d, exacta: <b>%d</b> es divisor de %d." % (n, DIV, d, n // d, d, n))
    if k == "cuantos":
        return mcq("¿Cuántos divisores tiene %d?" % n, str(len(D)), [str(len(D) - 2), str(len(D) - 1), str(len(D) + 1), str(len(D) + 2)],
                   "Los divisores de %d son %s: <b>%d</b>." % (n, ", ".join(map(str, D)), len(D)))
    d = R.randint(3, 9)
    m = d * R.randint(3, 12)
    st = [("%d es múltiplo de %d" % (m, d), True), ("%d es divisor de %d" % (d, m), True), ("%d es divisor de %d" % (m, d), False), ("%d es múltiplo de %d" % (d, m), False)]
    R.shuffle(st)
    good = [s for s, v in st if v]
    bad = [s for s, v in st if not v]
    return mcq("Sabemos que %d = %d %s %d. ¿Qué frase es falsa?" % (m, d, POR, m // d), bad[0], good + [bad[1]], "El número grande es múltiplo del pequeño y el pequeño es divisor del grande. Falsa: <b>%s</b>." % bad[0])


def s3_criterios():
    k = R.choice([2, 5, 10, 3, "par"])
    if k == "par":
        n = R.randint(1000, 99999)
        ok = "par" if n % 2 == 0 else "impar"
        return mcq("¿El número %s es par o impar?" % num(n), ok, ["impar" if ok == "par" else "par", "ni par ni impar", "depende de la primera cifra"],
                   "Termina en %d: es <b>%s</b>." % (n % 10, ok))
    d = k
    m = d * R.randint(100, 9999)
    ws = []
    while len(ws) < 6:
        x = R.randint(100, 99999)
        if x % d:
            ws.append(x)
    rule = {2: "termina en 0, 2, 4, 6 u 8", 5: "termina en 0 o en 5", 10: "termina en 0", 3: "la suma de sus cifras es múltiplo de 3"}[d]
    return mcq("¿Qué número es divisible entre %d?" % d, num(m), [num(x) for x in ws], "Un número es divisible entre %d si %s: <b>%s</b>." % (d, rule, num(m)))


def s4_primos():
    k = R.choice(["compuesto", "def", "pareja", "pareja"])
    P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    C = [4, 6, 8, 9, 10, 12, 14, 15, 16, 21, 25, 27, 33, 35, 39, 49, 51]
    if k == "compuesto":
        c = R.choice(C)
        ws = R.sample([x for x in P if x > 2], 3)
        lst = sorted([c] + ws)
        return mcq("De estos números (%s), ¿cuál es compuesto?" % ", ".join(map(str, lst)), str(c), [str(x) for x in ws],
                   "%d tiene más de dos divisores (%s): es <b>compuesto</b>." % (c, ", ".join(map(str, divs(c)))))
    if k == "def":
        return bank(R, [
            ("Un número primo es el que…", "solo tiene dos divisores: el 1 y él mismo", ["tiene muchos divisores", "es par", "termina en 1, 3, 7 o 9"]),
            ("¿El número 1 es primo?", "no, porque solo tiene un divisor", ["sí, porque solo se divide entre 1", "sí, es el primer primo", "depende"]),
            ("¿Cuál es el único número primo par?", "2", ["4", "1", "0"]),
            ("¿Qué número es divisor de todos los números?", "1", ["0", "2", "10"]),
            ("¿Cuántos múltiplos tiene un número?", "infinitos", ["10", "tantos como divisores", "ninguno"]),
        ], "def")()
    p = R.choice(P)
    ws = R.sample(C, 3)
    lst = sorted([p] + ws)
    return mcq("De estos números (%s), ¿cuál es primo?" % ", ".join(map(str, lst)), str(p), [str(x) for x in ws],
               "%d solo tiene dos divisores, 1 y %d: es <b>primo</b>." % (p, p))


def s5_problema():
    k = R.choice(["filas", "cajas", "autobus", "coincide", "sobran"])
    if k == "filas":
        n = R.choice([24, 30, 36, 40, 48, 60, 72])
        D = divs(n)
        r = R.choice([d for d in D if 2 <= d <= n // 2])
        return mcq("En el patio hay %d alumnos. ¿Pueden ponerse en filas de %d sin que sobre ninguno?" % (n, r), "sí, en %d filas" % (n // r), ["no, sobra 1", "sí, en %d filas" % (n // r + 1), "no, sobran %d" % r],
                   "%d es divisor de %d: %d %s %d = <b>%d filas</b>." % (r, n, n, DIV, r, n // r))
    if k == "cajas":
        n = R.choice([18, 20, 24, 30, 36, 42, 45])
        D = [d for d in divs(n) if 1 < d < n]
        ws = [x for x in range(2, 12) if n % x]
        R.shuffle(ws)
        return mcq("Tienes %d galletas y quieres repartirlas en bolsas iguales sin que sobre ninguna. ¿Cuántas galletas puedes poner en cada bolsa?" % n, str(R.choice(D)), [str(x) for x in ws],
                   "Sirve cualquier divisor de %d: %s." % (n, ", ".join(map(str, divs(n)))))
    if k == "autobus":
        a = R.choice([10, 12, 15, 20])
        n = R.randint(4, 9)
        return mcq("Un autobús pasa cada %d minutos a partir de las 9:00. ¿Cuál de estas horas es de paso del autobús?" % a, "9:%02d" % (a * min(n, 59 // a)), ["9:%02d" % x for x in range(1, 59) if x % a and x % 5 == 0][:6],
                   "Los minutos tienen que ser múltiplo de %d: <b>9:%02d</b>." % (a, a * min(n, 59 // a)))
    if k == "coincide":
        a, b = R.choice([(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 8), (6, 9)])
        import math
        m = a * b // math.gcd(a, b)
        return mcq("Lucía va a la piscina cada %d días y Hugo cada %d días. Hoy han ido los dos. ¿Dentro de cuántos días volverán a coincidir?" % (a, b), str(m), [str(a + b), str(a * b) if a * b != m else str(m + a), str(max(a, b)), str(m * 2)],
                   "Buscamos el primer múltiplo común de %d y %d: <b>%d</b>." % (a, b, m))
    n = R.randint(30, 99)
    d = R.choice([2, 5, 10])
    ok = n % d == 0
    return mcq("Un granjero tiene %d huevos. ¿Puede guardarlos todos en hueveras de %d sin que sobre ninguno?" % (n, d), "sí" if ok else "no", ["no" if ok else "sí", "solo si %d es par" % n, "no se puede saber"],
               "%d %s divisible entre %d: <b>%s</b>." % (n, "es" if ok else "no es", d, "sí" if ok else "no"))


def main():
    seen = set()
    sets = [
        ("Múltiplos", mix(R, seen, [(s1_multiplos, 20)])),
        ("Divisores", mix(R, seen, [(s2_divisores, 20)])),
        ("Criterios de divisibilidad", mix(R, seen, [(s3_criterios, 20)])),
        ("Números primos y compuestos", mix(R, seen, [(s4_primos, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Los <b>múltiplos</b> de un número se obtienen multiplicándolo por 1, 2, 3, 4…: múltiplos de 6 = 6, 12, 18, 24…",
         "Un número es <b>divisor</b> de otro si lo divide de forma exacta: 6 es divisor de 24 porque 24 : 6 = 4.",
         "Si 24 = 6 × 4, entonces 24 es múltiplo de 6 y 6 es divisor de 24.",
         "Divisible entre 2: termina en cifra par. Entre 5: termina en 0 o 5. Entre 10: termina en 0. Entre 3: la suma de sus cifras es múltiplo de 3.",
         "Un número <b>primo</b> solo tiene dos divisores: el 1 y él mismo (2, 3, 5, 7, 11…)."],
        [("Divisores de 18", ["1 × 18, 2 × 9, 3 × 6"], "1, 2, 3, 6, 9, 18"),
         ("¿Es 471 divisible entre 3?", ["4 + 7 + 1 = 12", "12 es múltiplo de 3"], "sí")],
        [["Confundir múltiplo y divisor", "El múltiplo es el número grande; el divisor, el pequeño."],
         ["Olvidar el 1 y el propio número", "Todo número es divisor de sí mismo y el 1 es divisor de todos."],
         ["Pensar que todos los impares son primos", "9, 15 y 21 son impares pero no son primos."]])
    faq = [("¿Qué diferencia hay entre múltiplo y divisor?", "Si 24 = 6 × 4, 24 es múltiplo de 6 (es el resultado de multiplicar) y 6 es divisor de 24 (lo divide de forma exacta)."),
           ("¿El 1 es un número primo?", "No. Un número primo tiene exactamente dos divisores, y el 1 solo tiene uno.")]
    make_unit(R, "multiplos-y-divisores", "N",
              "Múltiplos y divisores de números naturales; relación entre múltiplo y divisor; criterios de divisibilidad; números primos y compuestos",
              "Múltiplos y divisores", "Múltiplos y divisores",
              "Fichas de matemáticas de 4.º de Primaria: múltiplos y divisores, criterios de divisibilidad por 2, 3, 5 y 10, números pares e impares, primos y compuestos, y problemas. 100 ejercicios con soluciones.",
              "Si 24 = 6 × 4, 24 es múltiplo de 6 y 6 es divisor de 24", "Primo: solo dos divisores, el 1 y él mismo.",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
