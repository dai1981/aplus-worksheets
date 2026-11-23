# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Divisibilidad (Sentido numérico)
Múltiplos y divisores, criterios de divisibilidad (2, 3, 5, 9, 10), números primos y compuestos;
6.º: descomposición en factores primos, mínimo común múltiplo y máximo común divisor, problemas.
Errores: confundir mcm y mcd, olvidar factores al descomponer, creer que todos los impares son primos.
"""
import random
from math import gcd
from es_c3 import M, mix, lesson, make_unit, num, POR, DIV

R = None
LV = 6
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
SUP = {"2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶"}


def divs(n):
    return [x for x in range(1, n + 1) if n % x == 0]


def lcm(a, b):
    return a * b // gcd(a, b)


def fact(n):
    f = []
    p = 2
    while n > 1:
        while n % p == 0:
            f.append(p)
            n //= p
        p += 1
    return f


def ftxt(f):
    out = []
    for p in sorted(set(f)):
        c = f.count(p)
        out.append(str(p) + (SUP[str(c)] if c > 1 else ""))
    return (" %s " % POR).join(out)


def s1_multiplos():
    k = R.choice(["es", "lista", "divisor", "todos"])
    a = R.randint(3, 15)
    if k == "es":
        m = a * R.randint(4, 20)
        ws = [w for w in (m + 1, m - 1, m + a // 2 if a > 3 else m + 2, a * 11 + 1, m + 2) if w % a]
        return M("¿Cuál de estos números es múltiplo de %d: %s?" % (a, ", ".join(map(str, sorted([m] + ws[:3])))), str(m), [str(w) for w in ws[:3]], "%d = %d %s %d: <b>%d</b>." % (m, a, POR, m // a, m))
    if k == "lista":
        st = R.randint(2, 8)
        ok = ", ".join(str(a * i) for i in range(st, st + 4))
        return M("¿Qué lista tiene solo múltiplos de %d?" % a, ok, [", ".join(str(a + i) for i in range(st, st + 4)), ", ".join(str(a * i + 1) for i in range(st, st + 4)), ", ".join(str(x) for x in divs(a * 4)[:4])],
                 "Multiplicamos %d por %d, %d, %d y %d: <b>%s</b>." % (a, st, st + 1, st + 2, st + 3, ok))
    n = R.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 54, 56, 60, 72, 80, 84, 90, 96, 100])
    D = divs(n)
    if k == "divisor":
        dd = R.choice(D[1:-1])
        ws = [x for x in range(2, 16) if n % x]
        R.shuffle(ws)
        return M("¿Cuál de estos números es divisor de %d: %s?" % (n, ", ".join(map(str, sorted([dd] + ws[:3])))), str(dd), [str(x) for x in ws[:3]], "%d %s %d = %d, exacta: <b>%d</b>." % (n, DIV, dd, n // dd, dd))
    return M("¿Cuántos divisores tiene %d?" % n, str(len(D)), [str(len(D) - 1), str(len(D) + 1), str(len(D) - 2), str(len(D) + 2)], "Los divisores de %d son %s: <b>%d</b>." % (n, ", ".join(map(str, D)), len(D)))


def s2_criterios():
    d = R.choice([2, 3, 5, 9, 10, 3, 9])
    rule = {2: "termina en cifra par", 3: "la suma de sus cifras es múltiplo de 3", 5: "termina en 0 o en 5", 9: "la suma de sus cifras es múltiplo de 9", 10: "termina en 0"}[d]
    m = d * R.randint(120, 9999)
    ws = []
    while len(ws) < 3:
        x = R.randint(1000, 99999)
        if x % d and (d not in (3, 9) or x % 3 == 0 or R.random() < 0.5):
            ws.append(x)
    if R.random() < 0.5:
        return M("¿Qué número es divisible entre %d: %s?" % (d, ", ".join(num(x) for x in sorted([m] + ws))), num(m), [num(x) for x in ws],
                 "Divisible entre %d si %s: <b>%s</b>%s." % (d, rule, num(m), " (%s = %d)" % (" + ".join(str(m)), sum(map(int, str(m)))) if d in (3, 9) else ""))
    n = R.choice([m, ws[0]])
    ok = n % d == 0
    return M("¿Es %s divisible entre %d?" % (num(n), d), "sí" if ok else "no", ["no" if ok else "sí", "solo si es par", "no se puede saber sin dividir"],
             "Divisible entre %d si %s%s: <b>%s</b>." % (d, rule, " (%s = %d)" % (" + ".join(str(n)), sum(map(int, str(n)))) if d in (3, 9) else "", "sí" if ok else "no"))


def s3_primos():
    k = R.choice(["primo", "compuesto", "def", "cuantos"])
    C = [x for x in range(4, 100) if x not in PR]
    if k == "primo":
        p = R.choice(PR[2:])
        ws = R.sample([c for c in C if c % 2], 3)
        return M("¿Cuál es primo: %s?" % ", ".join(map(str, sorted([p] + ws))), str(p), [str(w) for w in ws],
                 "%d solo tiene dos divisores, 1 y %d. Los otros: %s." % (p, p, "; ".join("%d = %d %s %d" % (w, divs(w)[1], POR, w // divs(w)[1]) for w in ws)))
    if k == "compuesto":
        c = R.choice([x for x in C if x % 2])
        ws = R.sample(PR[2:], 3)
        return M("¿Cuál es compuesto: %s?" % ", ".join(map(str, sorted([c] + ws))), str(c), [str(w) for w in ws], "%d = %d %s %d: tiene más de dos divisores, es <b>compuesto</b>." % (c, divs(c)[1], POR, c // divs(c)[1]))
    if k == "cuantos":
        lo = R.choice([1, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        ps = [p for p in PR if lo <= p <= lo + 10]
        return M("¿Cuántos números primos hay entre %d y %d?" % (lo, lo + 10), str(len(ps)), [str(len(ps) + 1), str(len(ps) - 1) if len(ps) else "3", str(len(ps) + 2)],
                 "Son %s: <b>%d</b>." % (", ".join(map(str, ps)) or "ninguno", len(ps)))
    q, a, w = R.choice([("Un número primo tiene…", "exactamente dos divisores", ["muchos divisores", "un solo divisor", "solo divisores pares"]),
                        ("¿El 1 es un número primo?", "no, solo tiene un divisor", ["sí, es el primero", "sí, porque es impar", "depende"]),
                        ("¿Cuál es el único número primo par?", "2", ["4", "0", "1"]),
                        ("¿Es primo el 51?", "no, porque 51 = 3 × 17", ["sí, porque es impar", "sí, porque termina en 1", "no, porque es par"]),
                        ("¿Es primo el 91?", "no, porque 91 = 7 × 13", ["sí, porque es impar", "sí, no se puede dividir", "no, porque termina en 1"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s4_factores():
    n = R.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 72, 75, 80, 84, 90, 96, 100, 108, 120, 126, 150, 180])
    f = fact(n)
    ok = ftxt(f)
    w1 = ftxt(f[:-1])
    w2 = ftxt(f + [2])
    alt = list(f)
    alt[-1] = alt[-1] + 2 if alt[-1] + 2 in PR else alt[-1] + 4
    w3 = ftxt(alt)
    if R.random() < 0.6:
        return M("¿Cuál es la descomposición en factores primos de %d?" % n, ok, [w1, w2, w3, "%d %s %d" % (divs(n)[1], POR, n // divs(n)[1])], "Dividimos entre primos: %d = <b>%s</b>." % (n, ok))
    return M("¿Qué número es %s?" % ok, str(n), [str(n * 2), str(n // f[-1]), str(sum(f))], "<b>%d</b>." % n)


def s4_mcm_mcd():
    k = R.choice(["mcm", "mcd", "mcm", "mcd"])
    while True:
        a, b = R.randint(4, 40), R.randint(4, 40)
        if a != b and gcd(a, b) > 1 and lcm(a, b) <= 240:
            break
    if k == "mcm":
        m = lcm(a, b)
        return M("Calcula el mínimo común múltiplo: m.c.m.(%d, %d)" % (a, b), str(m), [str(a * b) if a * b != m else str(m * 2), str(gcd(a, b)), str(max(a, b)), str(m + min(a, b))],
                 "Múltiplos comunes de %d y %d: %d, %d, …; el menor es <b>%d</b>." % (a, b, m, 2 * m, m))
    g = gcd(a, b)
    return M("Calcula el máximo común divisor: m.c.d.(%d, %d)" % (a, b), str(g), [str(lcm(a, b)), str(min(a, b)) if min(a, b) != g else str(g * 2), "1" if g != 1 else "2", str(g // 2) if g > 3 else str(g + 1)],
             "Divisores comunes de %d y %d: %s; el mayor es <b>%d</b>." % (a, b, ", ".join(str(x) for x in divs(g)), g))


def s5_problema():
    k = R.choice(["autobus", "cinta", "flores", "luces", "baldosas", "equipos"])
    a, b = R.choice([(12, 18), (15, 20), (10, 15), (8, 12), (6, 10), (20, 30), (9, 12), (14, 21), (16, 24), (18, 24)])
    if k == "autobus":
        return M("Un autobús sale cada %d minutos y otro cada %d minutos. A las 8:00 salen juntos. ¿Dentro de cuántos minutos volverán a salir juntos?" % (a, b), "%d minutos" % lcm(a, b),
                 ["%d minutos" % (a * b), "%d minutos" % gcd(a, b), "%d minutos" % (a + b)], "Es el m.c.m.(%d, %d) = <b>%d</b>." % (a, b, lcm(a, b)))
    if k == "luces":
        return M("Una luz se enciende cada %d segundos y otra cada %d segundos. Ahora se encienden a la vez. ¿Cuándo vuelven a coincidir?" % (a, b), "a los %d segundos" % lcm(a, b),
                 ["a los %d segundos" % (a * b), "a los %d segundos" % gcd(a, b), "a los %d segundos" % (a + b)], "m.c.m.(%d, %d) = <b>%d</b>." % (a, b, lcm(a, b)))
    if k == "cinta":
        return M("Tenemos dos cintas de %d cm y %d cm. Queremos cortarlas en trozos iguales lo más largos posible, sin que sobre nada. ¿Cuánto mide cada trozo?" % (a * 5, b * 5), "%d cm" % (gcd(a, b) * 5),
                 ["%d cm" % (lcm(a, b) * 5), "%d cm" % 5, "%d cm" % (abs(a - b) * 5) if abs(a - b) * 5 != gcd(a, b) * 5 else "%d cm" % (gcd(a, b) * 10)], "Es el m.c.d.(%d, %d) = <b>%d cm</b>." % (a * 5, b * 5, gcd(a, b) * 5))
    if k == "flores":
        return M("Una floristería tiene %d rosas y %d tulipanes. Quiere hacer el mayor número de ramos iguales sin que sobre ninguna flor. ¿Cuántos ramos hace?" % (a, b), str(gcd(a, b)),
                 [str(lcm(a, b)), str(a + b), str(min(a, b))], "Es el m.c.d.(%d, %d) = <b>%d</b>." % (a, b, gcd(a, b)))
    if k == "baldosas":
        return M("Un suelo mide %d dm por %d dm. Se quiere cubrir con baldosas cuadradas iguales, lo más grandes posible, sin cortarlas. ¿Cuánto mide el lado de cada baldosa?" % (a * 10, b * 10), "%d dm" % (gcd(a, b) * 10),
                 ["%d dm" % (lcm(a, b) * 10), "%d dm" % 10, "%d dm" % (a * 10)], "m.c.d.(%d, %d) = <b>%d dm</b>." % (a * 10, b * 10, gcd(a, b) * 10))
    return M("En un colegio hay %d alumnos de 5.º y %d de 6.º. Se forman equipos iguales, lo más grandes posible, con alumnos de un solo curso. ¿Cuántos alumnos tiene cada equipo?" % (a * 2, b * 2), str(gcd(a, b) * 2),
             [str(lcm(a, b) * 2), str(a + b), "2"], "m.c.d.(%d, %d) = <b>%d</b>." % (a * 2, b * 2, gcd(a, b) * 2))


def s5_simple():
    k = R.choice(["filas", "cajas", "par"])
    if k == "filas":
        n = R.choice([24, 30, 36, 40, 48, 60, 72])
        r = R.choice([x for x in divs(n) if 2 <= x <= n // 2])
        return M("En el patio hay %d alumnos. ¿Pueden ponerse en filas de %d sin que sobre ninguno?" % (n, r), "sí, en %d filas" % (n // r), ["no, sobra 1", "sí, en %d filas" % (n // r + 1), "no, sobran %d" % r],
                 "%d es divisor de %d: <b>%d filas</b>." % (r, n, n // r))
    if k == "cajas":
        n = R.randint(100, 999)
        d = R.choice([2, 3, 5, 9])
        ok = n % d == 0
        return M("Una fábrica tiene %d galletas y las mete en bolsas de %d. ¿Pueden ir todas en bolsas completas?" % (n, d), "sí" if ok else "no", ["no" if ok else "sí", "solo si %d es par" % n, "no se puede saber"],
                 "%d %s divisible entre %d: <b>%s</b>." % (n, "es" if ok else "no es", d, "sí" if ok else "no"))
    a, b = R.choice([(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 8), (6, 9)])
    return M("Lucía va a la piscina cada %d días y Pablo cada %d días. Hoy han ido los dos. ¿Dentro de cuántos días coinciden otra vez?" % (a, b), str(lcm(a, b)), [str(a + b), str(a * b) if a * b != lcm(a, b) else str(lcm(a, b) + a), str(max(a, b))],
             "El primer múltiplo común de %d y %d es <b>%d</b>." % (a, b, lcm(a, b)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40004 + lv * 1000)
    seen = set()
    if lv == 6:
        sets = [
            ("Múltiplos y divisores", mix(R, seen, [(s1_multiplos, 20)])),
            ("Criterios de divisibilidad", mix(R, seen, [(s2_criterios, 20)])),
            ("Números primos y factores primos", mix(R, seen, [(s3_primos, 8), (s4_factores, 12)])),
            ("m.c.m. y m.c.d.", mix(R, seen, [(s4_mcm_mcd, 20)])),
            ("Problemas", mix(R, seen, [(s5_problema, 20)])),
        ]
    else:
        sets = [
            ("Múltiplos", mix(R, seen, [(s1_multiplos, 20)])),
            ("Criterios de divisibilidad", mix(R, seen, [(s2_criterios, 20)])),
            ("Números primos y compuestos", mix(R, seen, [(s3_primos, 20)])),
            ("Repaso", mix(R, seen, [(s1_multiplos, 10), (s2_criterios, 10)])),
            ("Problemas", mix(R, seen, [(s5_simple, 20)])),
        ]
    think = ["Si 24 = 6 × 4, entonces 24 es <b>múltiplo</b> de 6 y 6 es <b>divisor</b> de 24.",
             "Criterios: entre 2, si termina en cifra par; entre 3, si la suma de sus cifras es múltiplo de 3; entre 5, si termina en 0 o 5; entre 9, si la suma de sus cifras es múltiplo de 9; entre 10, si termina en 0.",
             "Un número <b>primo</b> solo tiene dos divisores: el 1 y él mismo (2, 3, 5, 7, 11…). Si tiene más, es <b>compuesto</b>."]
    if lv == 6:
        think.append("El <b>m.c.m.</b> es el menor múltiplo común (sirve para saber cuándo coinciden dos cosas). El <b>m.c.d.</b> es el mayor divisor común (sirve para repartir en partes iguales lo más grandes posible).")
    body = lesson(think,
                  [("¿Es 738 divisible entre 9?", ["7 + 3 + 8 = 18", "18 es múltiplo de 9"], "sí"),
                   ("m.c.m.(6, 8) y m.c.d.(6, 8)" if lv == 6 else "Divisores de 18", ["Múltiplos de 8: 8, 16, 24 → 24 también es de 6", "Divisores comunes: 1 y 2"] if lv == 6 else ["1 × 18, 2 × 9, 3 × 6"], "24 y 2" if lv == 6 else "1, 2, 3, 6, 9, 18")],
                  [["Confundir múltiplo y divisor", "El múltiplo es el grande; el divisor, el pequeño."],
                   ["Pensar que los impares son primos", "9, 15, 21 y 51 son impares y compuestos."],
                   ["Confundir m.c.m. y m.c.d." if lv == 6 else "Olvidar el 1 y el propio número", "Coincidir → m.c.m.; repartir en partes iguales → m.c.d." if lv == 6 else "Todo número es divisor de sí mismo y el 1 divide a todos."]])
    faq = [("¿Qué es un número primo?", "Un número que solo tiene dos divisores, el 1 y él mismo, como 2, 3, 5, 7, 11 o 13. El 1 no es primo."),
           ("¿Cuándo se usa el m.c.m. y cuándo el m.c.d.?", "El m.c.m. se usa para saber cuándo vuelven a coincidir dos cosas que se repiten; el m.c.d., para repartir o cortar en partes iguales lo más grandes posible.")]
    make_unit(R, "multiplos-divisores-mcm-y-mcd" if lv == 6 else "multiplos-divisores-y-primos", "N",
              "Múltiplos y divisores; criterios de divisibilidad; números primos y compuestos" + ("; descomposición en factores primos; mínimo común múltiplo y máximo común divisor" if lv == 6 else ""),
              "Múltiplos, divisores, m.c.m. y m.c.d." if lv == 6 else "Múltiplos, divisores y números primos", "Divisibilidad",
              "Fichas de matemáticas de %d.º de Primaria: múltiplos y divisores, criterios de divisibilidad, números primos%s y problemas. 100 ejercicios con soluciones." % (lv, ", factores primos, m.c.m. y m.c.d." if lv == 6 else ""),
              "Coincidir: m.c.m. Repartir: m.c.d." if lv == 6 else "24 = 6 × 4: 24 es múltiplo de 6", "Primo: solo divisible entre 1 y él mismo.",
              body, faq, sets, 4, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
