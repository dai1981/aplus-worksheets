# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Divisibilidad (Sentido numérico)
Múltiplos y divisores, criterios de divisibilidad, primos y compuestos, descomposición en factores primos, m.c.d. y m.c.m., problemas.
Errores: confundir múltiplo y divisor, creer que 1 es primo, tomar los factores con mayor exponente para el m.c.d.
"""
import math
import random
from es_eso import M, W, mix, num, sup, unit, L, Kids, table

R = random.Random(47001)
K = Kids(R)
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def fact(n):
    out, p = {}, 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def fs(f):
    return " · ".join("%d%s" % (p, sup(e)) for p, e in sorted(f.items()))


def divisores(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def lcm(a, b):
    return a * b // math.gcd(a, b)


def s_multiplos():
    t = R.choice(["mult", "div", "lista", "cuantos", "criterio"])
    if t == "mult":
        a = R.randint(6, 19)
        k = R.randint(3, 15)
        n = a * k
        w = [n + 1, n + a // 2 if a % 2 else n + 2, n - 1]
        return M("¿Cuál de estos números es múltiplo de %d?" % a, num(n), [num(x) for x in w], "%d = %d · %d: es <b>múltiplo de %d</b>." % (n, a, k, a))
    if t == "div":
        n = R.choice([36, 48, 60, 72, 84, 90, 96, 100, 120, 126, 144, 150, 180])
        ds = divisores(n)
        ok = R.choice([x for x in ds if 6 < x < n])
        w = [x for x in range(7, n) if n % x and x not in (ok,)]
        R.shuffle(w)
        return M("¿Cuál de estos números es divisor de %d?" % n, num(ok), [num(x) for x in w[:5]], "%d : %d = %d, división exacta: <b>%d</b> es divisor." % (n, ok, n // ok, ok))
    if t == "lista":
        n = R.choice([12, 18, 20, 24, 28, 30, 32, 40, 42, 45, 50])
        ds = divisores(n)
        ok = ", ".join(map(str, ds))
        w1 = ", ".join(map(str, ds[1:-1]))
        w2 = ", ".join(str(n * k) for k in range(1, 5)) + "…"
        w3 = ", ".join(map(str, [x for x in ds if x % 2 == 0]))
        w4 = ", ".join(str(x) for x in ds if x != ds[len(ds) // 2])
        return M("¿Cuáles son todos los divisores de %d?" % n, ok, [w1, w2, w3 if w3 else None, w4], "Buscamos los números que dividen a %d de forma exacta: <b>%s</b>." % (n, ok))
    if t == "cuantos":
        a = R.randint(3, 12)
        top = R.choice([50, 60, 80, 100])
        c = top // a
        return M("¿Cuántos múltiplos de %d hay entre 1 y %d?" % (a, top), str(c), [str(c + 1), str(c - 1), str(top - a)], "%d : %d = %d y algo: hay <b>%d</b>." % (top, a, c, c))
    k = R.choice([2, 3, 5, 9, 10, 11])
    regla = {2: "termina en cifra par", 3: "la suma de sus cifras es múltiplo de 3", 5: "termina en 0 o en 5", 9: "la suma de sus cifras es múltiplo de 9",
             10: "termina en 0", 11: "la diferencia entre la suma de las cifras de lugar impar y las de lugar par es 0 o múltiplo de 11"}[k]
    ok_n = R.randint(100, 9999 // k) * k
    ws = []
    while len(ws) < 3:
        x = R.randint(100, 9999)
        if x % k and x not in ws and abs(x - ok_n) > 5:
            ws.append(x)
    return M("¿Cuál de estos números es divisible entre %d: %s?" % (k, ", ".join(num(x) for x in sorted(ws + [ok_n]))), num(ok_n), [num(x) for x in ws], "Un número es divisible entre %d si %s: <b>%s</b>." % (k, regla, num(ok_n)))


def s_primos():
    t = R.choice(["primo", "comp", "def", "entre"])
    if t == "primo":
        p = R.choice([x for x in PR if x > 10])
        ws = R.sample([x for x in range(21, 100, 2) if x not in PR and x % 5], 3)
        return M("¿Cuál de estos números es primo: %s?" % ", ".join(str(x) for x in sorted(ws + [p])), str(p), [str(x) for x in ws], "%d solo tiene dos divisores, 1 y %d: es <b>primo</b>." % (p, p))
    if t == "comp":
        c = R.choice([x for x in range(51, 100, 2) if x not in PR and x % 5])
        ws = R.sample([x for x in PR if x > 40], 3)
        dv = [k for k in range(3, c) if c % k == 0][0]
        return M("¿Cuál de estos números es compuesto: %s?" % ", ".join(str(x) for x in sorted(ws + [c])), str(c), [str(x) for x in ws], "%d = %d · %d: tiene más de dos divisores, es <b>compuesto</b>." % (c, dv, c // dv))
    if t == "entre":
        a = R.choice([10, 20, 30, 40, 50, 60, 70, 80])
        ps = [x for x in PR if a < x < a + 10]
        if not ps:
            return None
        ok = ", ".join(map(str, ps))
        alt = ", ".join(str(x) for x in range(a + 1, a + 10, 2) if x % 5)
        return M("¿Qué números primos hay entre %d y %d?" % (a, a + 10), ok, [alt, ", ".join(map(str, ps[:-1])) if len(ps) > 1 else str(ps[0] + 2), ", ".join(str(x) for x in ps) + ", %d" % (a + 9), ", ".join(str(x) for x in sorted(ps + [[y for y in range(a + 1, a + 10, 2) if y not in PR][0]]))],
                 "Comprobamos que no tengan divisores distintos de 1 y de sí mismos: <b>%s</b>." % ok)
    q, a, w = R.choice([("¿Es primo el número 1?", "no: solo tiene un divisor", ["sí: solo se divide entre 1", "sí, es el primer primo", "depende"]),
                        ("¿Cuál es el único número primo par?", "2", ["4", "1", "no hay ninguno"]),
                        ("¿Cuántos divisores tiene un número primo?", "2", ["1", "3", "infinitos"]),
                        ("¿Es 91 un número primo?", "no: 91 = 7 · 13", ["sí: no es par", "sí: no termina en 5", "sí: 9 + 1 = 10"]),
                        ("¿Es 57 un número primo?", "no: 57 = 3 · 19", ["sí: es impar", "sí: no termina en 5", "sí: no está en la tabla del 7"]),
                        ("Para saber si 97 es primo, ¿hasta qué número hay que probar divisores?", "hasta 9 (porque 10 · 10 = 100)", ["hasta 97", "hasta 48", "hasta 2"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_factor():
    k = R.choice([2, 3, 3, 4])
    f = {}
    for p in R.sample([2, 2, 2, 3, 3, 5, 7, 11], k):
        f[p] = f.get(p, 0) + 1
    n = 1
    for p, e in f.items():
        n *= p ** e
    if n < 24 or n > 2000:
        return None
    ok = fs(f)
    w = []
    g = dict(f)
    p0 = min(g)
    g[p0] += 1
    w.append(fs(g))
    h = dict(f)
    if h[p0] > 1:
        h[p0] -= 1
        w.append(fs(h))
    w.append(" · ".join("%d · %d" % (p, e) for p, e in sorted(f.items())))
    w.append(" · ".join(str(p) for p in sorted(f)))
    nxt = {2: 3, 3: 5, 5: 7, 7: 11, 11: 13}
    pm = max(f)
    j = dict(f)
    e = j.pop(pm)
    j[nxt[pm]] = j.get(nxt[pm], 0) + e
    w.append(fs(j))
    if R.random() < 0.5:
        return M("¿Cuál es la descomposición en factores primos de %s?" % num(n), ok, w, "Dividimos entre 2, 3, 5… hasta llegar a 1: %s = <b>%s</b>." % (num(n), ok))
    return M("¿Qué número es %s?" % ok, num(n), [num(n * 2), num(n // min(f)), num(sum(p * e for p, e in f.items()))], "Multiplicamos: %s = <b>%s</b>." % (ok, num(n)))


def s_mcd():
    g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18])
    a, b = R.sample(range(2, 13), 2)
    if math.gcd(a, b) != 1:
        return None
    A, B = g * a, g * b
    if A > 400 or B > 400:
        return None
    L_ = lcm(A, B)
    t = R.choice(["mcd", "mcm", "mcd", "mcm", "rel"])
    if t == "mcd":
        return M("Calcula m.c.d.(%d, %d)." % (A, B), str(g), [str(L_), str(min(A, B)), str(g * 2) if (g * 2) not in (A, B) else str(g + 1)],
                 "%d = %s y %d = %s. Factores comunes con menor exponente: <b>%d</b>." % (A, fs(fact(A)), B, fs(fact(B)), g))
    if t == "mcm":
        return M("Calcula m.c.m.(%d, %d)." % (A, B), num(L_), [num(A * B) if A * B != L_ else num(L_ * 2), str(g), num(L_ // 2) if L_ % 2 == 0 and L_ // 2 not in (A, B) else num(L_ + g)],
                 "Factores comunes y no comunes con mayor exponente: <b>%s</b>." % num(L_))
    return M("Si m.c.d.(%d, %d) = %d, ¿cuánto vale m.c.m.(%d, %d)?" % (A, B, g, A, B), num(L_), [num(A * B), num(A * B * g), num(A + B)], "m.c.d. · m.c.m. = %d · %d, así que m.c.m. = %s : %d = <b>%s</b>." % (A, B, num(A * B), g, num(L_)))


def s_problema():
    p = K.next()[0]
    t = R.choice(["bus", "cinta", "baldosa", "luces", "grupos"])
    if t == "bus":
        a, b = R.sample([10, 12, 15, 18, 20, 24, 30], 2)
        L_ = lcm(a, b)
        if L_ > 120:
            return None
        return M("Un autobús sale cada %d minutos y otro cada %d minutos. Si salen juntos a las 8:00, ¿cuántos minutos después vuelven a salir juntos?" % (a, b), "%d min" % L_,
                 ["%d min" % (a * b) if a * b != L_ else "%d min" % (2 * L_), "%d min" % math.gcd(a, b), "%d min" % (a + b)], "m.c.m.(%d, %d) = <b>%d</b> minutos." % (a, b, L_))
    if t == "luces":
        a, b = R.sample([4, 6, 8, 9, 10, 12, 15], 2)
        L_ = lcm(a, b)
        return M("Una luz se enciende cada %d segundos y otra cada %d segundos. Se encienden a la vez ahora. ¿Dentro de cuántos segundos vuelven a coincidir?" % (a, b), "%d s" % L_,
                 ["%d s" % (a * b) if a * b != L_ else "%d s" % (2 * L_), "%d s" % math.gcd(a, b), "%d s" % (a + b)], "m.c.m.(%d, %d) = <b>%d</b> s." % (a, b, L_))
    g = R.choice([4, 5, 6, 8, 9, 10, 12, 15])
    a, b = R.sample(range(2, 9), 2)
    if math.gcd(a, b) != 1:
        return None
    A, B = g * a, g * b
    if t == "cinta":
        return M("%s tiene dos cintas de %d cm y %d cm. Quiere cortarlas en trozos iguales, lo más largos posible, sin que sobre nada. ¿Cuánto mide cada trozo?" % (p, A, B), "%d cm" % g,
                 ["%d cm" % lcm(A, B), "%d cm" % (B - A if B > A else A - B) if abs(A - B) != g else "%d cm" % (g * 2), "%d cm" % min(A, B)], "m.c.d.(%d, %d) = <b>%d</b> cm." % (A, B, g))
    if t == "baldosa":
        return M("Un patio rectangular mide %d dm por %d dm. Queremos cubrirlo con baldosas cuadradas lo más grandes posible, sin cortar ninguna. ¿Cuánto mide el lado de cada baldosa?" % (A, B), "%d dm" % g,
                 ["%d dm" % lcm(A, B), "%d dm" % min(A, B), "%d dm" % (g // 2) if g % 2 == 0 else "%d dm" % (g + 1)], "m.c.d.(%d, %d) = <b>%d</b> dm." % (A, B, g))
    return M("En una clase hay %d chicas y %d chicos. Queremos hacer grupos con el mismo número de chicas y de chicos en cada uno, el mayor número de grupos posible. ¿Cuántos grupos salen?" % (A, B), str(g),
             [str(lcm(A, B)), str(a + b), str(g * 2)], "m.c.d.(%d, %d) = <b>%d</b> grupos." % (A, B, g))


seen = set()
sets = [("Múltiplos, divisores y criterios", mix(R, seen, [(s_multiplos, 20)])), ("Primos y compuestos", mix(R, seen, [(s_primos, 20)])),
        ("Descomposición en factores primos", mix(R, seen, [(s_factor, 20)])), ("m.c.d. y m.c.m.", mix(R, seen, [(s_mcd, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["<b>a</b> es múltiplo de <b>b</b> si la división a : b es exacta; entonces b es divisor de a.",
          "Un número <b>primo</b> solo tiene dos divisores: 1 y él mismo. El 1 no es primo.",
          "Para el <b>m.c.d.</b>, se toman los factores primos comunes con el menor exponente. Para el <b>m.c.m.</b>, los comunes y no comunes con el mayor exponente."],
         [("m.c.d. y m.c.m. de 24 y 36", ["24 = 2³ · 3", "36 = 2² · 3²", "m.c.d. = 2² · 3 = 12", "m.c.m. = 2³ · 3² = 72"], "12 y 72")],
         [["Confundir múltiplo y divisor", "24 es múltiplo de 6; 6 es divisor de 24."], ["Decir que 1 es primo", "Un primo tiene exactamente dos divisores."],
          ["Mezclar las reglas del m.c.d. y del m.c.m.", "m.c.d.: comunes, menor exponente. m.c.m.: todos, mayor exponente."]],
         table(["Número", "Factores primos"], [["24", "2³ · 3"], ["36", "2² · 3²"], ["90", "2 · 3² · 5"]]))
faq = [("¿Cuándo se usa el m.c.m. en un problema?", "Cuando algo se repite cada cierto tiempo y queremos saber cuándo vuelve a coincidir."),
       ("¿Cuándo se usa el m.c.d.?", "Cuando queremos repartir o cortar en partes iguales lo más grandes posible, sin que sobre nada.")]
unit(1, R, "divisibilidad", "N", "Múltiplos y divisores; criterios de divisibilidad; números primos y compuestos; descomposición en factores primos; máximo común divisor y mínimo común múltiplo",
     "Divisibilidad: primos, m.c.d. y m.c.m.", "Divisibilidad",
     "Fichas de matemáticas de 1.º de ESO: múltiplos y divisores, primos, descomposición en factores, m.c.d., m.c.m. y problemas. 100 ejercicios con soluciones.",
     "m.c.d.: comunes, menor exponente", "m.c.m.: todos, con el mayor exponente.", body, faq, sets, 1)
