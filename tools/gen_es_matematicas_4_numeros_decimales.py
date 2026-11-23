# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Números decimales (Sentido numérico)
Décimas y centésimas, fracciones decimales y números decimales, leer y escribir decimales, valor de cada cifra,
comparar y ordenar, la recta numérica, redondear a la unidad, decimales en euros y en medidas.
Errores: pensar que 2,35 &gt; 2,5 porque 35 &gt; 5, leer 0,07 como «siete décimas», olvidar el 0 en 3,05.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, dz, fr, tabla_decimal, recta, eur, letra, Kids

R = random.Random(44012)
K = Kids(R)


def leer(c):
    """centésimas → «2 unidades y 35 centésimas»"""
    e, r = divmod(c, 100)
    if r % 10 == 0:
        t = "%s %s" % (r // 10, "décima" if r // 10 == 1 else "décimas")
    else:
        t = "%s %s" % (r, "centésima" if r == 1 else "centésimas")
    return "%s %s y %s" % (e, "unidad" if e == 1 else "unidades", t)


def s1_fraccion():
    k = R.choice(["d", "c", "a_fr", "dib"])
    if k == "d":
        n = R.randint(1, 9)
        return mcq("¿Qué número decimal es igual a %s?" % fr(n, 10), dz(n, 1), ["0,0%d" % n, str(n), "%d,10" % n, dz(n + 1, 1)],
                   "%s = %d décima%s = <b>%s</b>." % (fr(n, 10), n, "" if n == 1 else "s", dz(n, 1)))
    if k == "c":
        n = R.randint(1, 99)
        if n % 10 == 0:
            return None
        return mcq("¿Qué número decimal es igual a %s?" % fr(n, 100), dz(n, 2, keep=True), [dz(n, 1) if n < 100 else None, "%d,100" % n, dz(n, 3), dz(n + 1, 2, keep=True)],
                   "%s = %d centésima%s = <b>%s</b>." % (fr(n, 100), n, "" if n == 1 else "s", dz(n, 2, keep=True)))
    if k == "a_fr":
        n = R.randint(1, 99)
        if n % 10 == 0:
            return None
        return mcq("¿Qué fracción decimal es %s?" % dz(n, 2, keep=True), fr(n, 100), [fr(n, 10), fr(n, 1000), fr(100, n), fr(n + 1, 100)], "%s = <b>%s</b>." % (dz(n, 2, keep=True), fr(n, 100)))
    n = R.randint(1, 9)
    from es_common import tira
    return mcq(tira(10, n) + "La tira es una unidad dividida en 10 partes. ¿Qué número decimal representa la parte coloreada?", dz(n, 1), [str(n), "0,0%d" % n, dz(10 - n, 1) if 10 - n != n else dz(n + 1, 1), "%d,10" % n],
               "%d de 10 partes = %d décimas = <b>%s</b>." % (n, n, dz(n, 1)))


def s2_leer():
    c = R.randint(101, 9999)
    if c % 100 == 0:
        return None
    k = R.choice(["leer", "escribir", "cifra", "tabla"])
    if k == "leer":
        e, r = divmod(c, 100)
        alt = leer(e * 100 + (r * 10 if r < 10 else r // 10 if r % 10 == 0 else r))
        ws = [alt if alt != leer(c) else None, "%s unidades y %s décimas" % (e, r) if r % 10 else None, "%s unidades y %s centésimas" % (r, e) if e != r else None, leer(c + 100), leer(c - 1) if (c - 1) % 100 else leer(c + 1)]
        return mcq("¿Cómo se lee %s?" % dz(c, 2, keep=r % 10 != 0), leer(c), ws, "%s = <b>%s</b>." % (dz(c, 2, keep=r % 10 != 0), leer(c)))
    if k == "escribir":
        e, r = divmod(c, 100)
        ws = ["%d,%d" % (e, r) if r < 10 else None, dz(c, 1) if c < 1000 else dz(c, 3), "%d,%02d" % (r, e) if r != e else None, dz(c + 10, 2, keep=True)]
        return mcq("Escribe con cifras: %s." % leer(c), dz(c, 2, keep=r % 10 != 0), ws, "<b>%s</b>%s." % (dz(c, 2, keep=r % 10 != 0), " (el 0 de las décimas no se puede olvidar)" if r < 10 else ""))
    if k == "cifra":
        s = str(c)
        if len(s) < 3 or s[-1] == "0" or s[-2] == "0":
            return None
        pos = R.choice(["d", "c"])
        dig = int(s[-2] if pos == "d" else s[-1])
        val = dz(dig, 1) if pos == "d" else dz(dig, 2, keep=True)
        return mcq("En el número %s, ¿cuánto vale la cifra %d de las %s?" % (dz(c, 2, keep=True), dig, "décimas" if pos == "d" else "centésimas"), val,
                   [str(dig), dz(dig, 2, keep=True) if pos == "d" else dz(dig, 1), str(dig * 10)], "%d %s = <b>%s</b>." % (dig, "décimas" if pos == "d" else "centésimas", val))
    return mcq(tabla_decimal(c, 2, 2 if c >= 1000 else 1) + "¿Qué número decimal está en la tabla?", dz(c, 2, keep=True), [dz(c, 1), dz(c, 3), num(c), dz(c + 1, 2, keep=True)],
               "<b>%s</b>." % dz(c, 2, keep=True))


def s3_comparar():
    k = R.choice(["dos", "dos", "mayor", "orden"])
    if k == "dos":
        e = R.randint(0, 20)
        a = R.randint(1, 9)
        b = R.randint(11, 99)
        if b % 10 == 0 or b // 10 == a:
            return None
        x, y = e * 100 + a * 10, e * 100 + b
        A, B = dz(x, 1), dz(y, 2)
        ok = "%s %s %s" % (A, "&lt;" if x < y else "&gt;", B)
        return mcq("Compara %s y %s. ¿Qué es correcto?" % (A, B), ok, ["%s %s %s" % (A, "&gt;" if x < y else "&lt;", B), "%s = %s" % (A, B), "no se pueden comparar"],
                   "%s = %s; comparamos las décimas: <b>%s</b>." % (A, dz(x, 2, keep=True), ok))
    xs = set()
    e = R.randint(0, 12)
    while len(xs) < 4:
        xs.add(e * 100 + R.choice([R.randint(1, 9) * 10, R.randint(1, 99)]))
    xs = sorted(xs)
    sh = [dz(x, 2) for x in xs]
    R.shuffle(sh)
    if k == "mayor":
        return mcq("¿Cuál es el número mayor? %s" % "; ".join(sh), dz(max(xs), 2), sh, "Igualamos las cifras decimales y comparamos: <b>%s</b>." % dz(max(xs), 2))
    asc = [dz(x, 2) for x in xs]
    f = lambda L: " &lt; ".join(L)
    w1 = sorted(asc, key=lambda t: int(t.split(",")[1]) if "," in t else 0)
    w2 = [asc[1], asc[0], asc[2], asc[3]]
    w3 = asc[::-1]
    w4 = [asc[0], asc[2], asc[1], asc[3]]
    w5 = [asc[0], asc[1], asc[3], asc[2]]
    return mcq("Ordena de menor a mayor: %s" % "; ".join(sh), f(asc), [f(w1), f(w2), f(w3), f(w4), f(w5)], "<b>%s</b>." % f(asc))


def s4_recta():
    k = R.choice(["recta", "redondear", "entre"])
    if k == "recta":
        e = R.randint(0, 8)
        n = R.randint(1, 9)
        g = recta(e * 10, e * 10 + 10, 1, marks=[(e * 10 + n, "?")], labels=[e * 10, e * 10 + 10])
        g = g.replace(">%d<" % (e * 10), ">%d<" % e).replace(">%d<" % (e * 10 + 10), ">%d<" % (e + 1))
        return mcq(g + "La recta va de %d a %d en décimas. ¿Qué número está en «?»?" % (e, e + 1), dz(e * 10 + n, 1), [dz(e * 10 + n + 1, 1), dz(e * 10 + n - 1, 1) if n > 1 else dz(e * 10 + n + 2, 1), "%d,0%d" % (e, n), str(e + n)],
                       "Cada marca es una décima: <b>%s</b>." % dz(e * 10 + n, 1))
    if k == "redondear":
        c = R.randint(101, 4999)
        if c % 100 == 50:
            return None
        r = (c + 50) // 100
        return mcq("Redondea %s a las unidades." % dz(c, 2, keep=True), str(r), [str(c // 100 if r != c // 100 else r + 1), dz(c // 10, 1), str(r - 1), str(r + 2), str(c)],
                   "Miramos las décimas: %d. %s <b>%d</b>." % (c // 10 % 10, "Como es 5 o más, hacia arriba:" if c // 10 % 10 >= 5 else "Como es menor que 5, hacia abajo:", r))
    c = R.randint(11, 999)
    if c % 10 == 0:
        return None
    a, b = c // 10, c // 10 + 1
    return mcq("¿Entre qué dos números con una cifra decimal está %s?" % dz(c, 2, keep=True), "entre %s y %s" % (dz(a, 1, keep=True), dz(b, 1, keep=True)),
               ["entre %s y %s" % (dz(a - 1, 1, keep=True), dz(a, 1, keep=True)) if a > 0 else None, "entre %s y %s" % (dz(b, 1, keep=True), dz(b + 1, 1, keep=True)), "entre %d y %d" % (c // 100 + 1, c // 100 + 2), "entre %s y %s" % (dz(a + 2, 1, keep=True), dz(a + 3, 1, keep=True))],
               "%s &lt; %s &lt; %s." % (dz(a, 1, keep=True), dz(c, 2, keep=True), dz(b, 1, keep=True)))


def s5_vida():
    p, g = K.next()
    k = R.choice(["euros", "euros2", "salto", "altura", "carrera", "cent"])
    if k == "euros":
        c = R.randint(105, 2999)
        if c % 100 == 0:
            return None
        e, r = divmod(c, 100)
        return mcq("Un libro cuesta %s. ¿Cuántos euros y céntimos son?" % eur(c), "%d euros y %d céntimos" % (e, r),
                   ["%d euros y %d céntimos" % (r, e), "%d euros y %d céntimos" % (e, r * 10) if r < 10 else "%d euros y %d céntimos" % (e + 1, r), "%d céntimos" % (e + r), "%d euros y %d céntimos" % (e - 1, r) if e > 1 else "%d euros" % c],
                   "%s = <b>%d euros y %d céntimos</b>." % (eur(c), e, r))
    if k == "euros2":
        a, b = R.randint(105, 999), R.randint(105, 999)
        if a == b:
            return None
        x, y = R.sample(["un balón", "una mochila", "un estuche", "un cómic", "una camiseta", "una gorra"], 2)
        return mcq("%s cuesta %s y %s cuesta %s. ¿Qué es más caro?" % (x[0].upper() + x[1:], eur(a), y, eur(b)), x if a > b else y, [y if a > b else x, "cuestan lo mismo", "no se puede saber"],
                   "%s %s %s: <b>%s</b>." % (eur(a), "&gt;" if a > b else "&lt;", eur(b), x if a > b else y))
    if k == "salto":
        ns = R.sample(range(250, 450), 3)
        names = [K.next()[0] for _ in range(3)]
        if len(set(names)) < 3:
            return None
        m = max(range(3), key=lambda i: ns[i])
        return mcq("En salto de longitud, %s saltó %s m, %s saltó %s m y %s saltó %s m. ¿Quién saltó más?" % (names[0], dz(ns[0], 2), names[1], dz(ns[1], 2), names[2], dz(ns[2], 2)),
                   names[m], names + ["saltaron lo mismo"], "%s m es el mayor: <b>%s</b>." % (dz(ns[m], 2), names[m]))
    if k == "altura":
        c = R.randint(121, 159)
        return mcq("%s mide %s m. ¿Cuántos centímetros son?" % (p, dz(c, 2, keep=True)), "%d cm" % c, ["%d cm" % (c // 10), "%d cm" % (c * 10), "%d cm" % (c % 100), "%d cm" % (c + 10)],
                   "1 m = 100 cm; %s m = <b>%d cm</b>." % (dz(c, 2, keep=True), c))
    if k == "carrera":
        ts = R.sample(range(1101, 1499), 4)
        names = ["Ana", "Leo", "Vega", "Iker"]
        m = min(range(4), key=lambda i: ts[i])
        return mcq("Tiempos en una carrera de 100 m: %s. ¿Quién ganó (el menor tiempo)?" % "; ".join("%s, %s s" % (n, dz(t, 2)) for n, t in zip(names, ts)), names[m], names,
                   "El menor tiempo es %s s: <b>%s</b>." % (dz(ts[m], 2), names[m]))
    n = R.randint(1, 99)
    return mcq("¿Cuántos euros son %d céntimos?" % n, eur(n), [eur(n * 10) if n < 10 else "%d,%d €" % (0, n), "%d €" % n, eur(n * 100), eur(n + 1)],
               "100 céntimos = 1 €; %d céntimos = <b>%s</b>." % (n, eur(n)))


def main():
    seen = set()
    sets = [
        ("Décimas y centésimas", mix(R, seen, [(s1_fraccion, 20)])),
        ("Leer y escribir decimales", mix(R, seen, [(s2_leer, 20)])),
        ("Comparar y ordenar", mix(R, seen, [(s3_comparar, 20)])),
        ("Recta numérica y redondeo", mix(R, seen, [(s4_recta, 20)])),
        ("Decimales en la vida diaria", mix(R, seen, [(s5_vida, 20)])),
    ]
    body = lesson(
        ["Si divides la unidad en 10 partes, cada parte es una <b>décima</b>: %s = 0,1. Si la divides en 100, cada parte es una <b>centésima</b>: %s = 0,01." % (fr(1, 10), fr(1, 100)),
         "En un número decimal, la <b>coma</b> separa la parte entera de la parte decimal: en 3,45 hay 3 unidades, 4 décimas y 5 centésimas.",
         "Para comparar, mira primero la parte entera. Si es igual, compara las décimas y después las centésimas. Puedes añadir un 0 al final: 2,5 = 2,50."],
        [("Compara 2,5 y 2,35", ["2,5 = 2,50", "50 centésimas &gt; 35 centésimas"], "2,5 &gt; 2,35"),
         ("Escribe «3 unidades y 5 centésimas»", ["0 décimas, 5 centésimas"], "3,05")],
        [["Creer que 2,35 &gt; 2,5", "Iguala las cifras decimales: 2,35 &lt; 2,50."],
         ["Leer 0,07 como «siete décimas»", "0,07 son siete centésimas; siete décimas es 0,7."],
         ["Olvidar el cero", "3 unidades y 5 centésimas es 3,05, no 3,5."]],
        tabla_decimal(345, 2, 1))
    faq = [("¿Qué es una décima y una centésima?", "Una décima es una de las 10 partes iguales de la unidad (0,1) y una centésima, una de las 100 partes iguales (0,01). 10 centésimas = 1 décima."),
           ("¿Cómo se comparan números decimales?", "Se compara primero la parte entera; si es igual, se comparan las décimas y después las centésimas. Para que sea más fácil, se escriben con el mismo número de cifras decimales.")]
    make_unit(R, "numeros-decimales", "N",
              "Números decimales hasta las centésimas: relación con las fracciones decimales, lectura, escritura, valor posicional, comparación, ordenación, representación en la recta y redondeo; uso en contextos de dinero y medida",
              "Números decimales: décimas y centésimas", "Números decimales",
              "Fichas de matemáticas de 4.º de Primaria: décimas y centésimas, fracciones decimales, leer y escribir decimales, comparar, ordenar, redondear y decimales en euros y medidas. 100 ejercicios con soluciones.",
              "La coma separa unidades y décimas", "Para comparar: 2,5 = 2,50.",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
