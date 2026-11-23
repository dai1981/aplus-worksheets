# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Comparar y redondear números (Sentido numérico)
Comparar con los signos &lt; y &gt;, ordenar de mayor a menor y de menor a mayor, redondear a las decenas, centenas,
unidades de millar y decenas de millar, estimar con la recta numérica.
Errores: comparar por la primera cifra sin mirar cuántas cifras tiene, redondear hacia abajo cuando la cifra siguiente es 5.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, recta, bank

R = random.Random(44002)
ORD = {10: "decena", 100: "centena", 1000: "unidad de millar", 10000: "decena de millar", 100000: "centena de millar"}
ORDP = {10: "las decenas", 100: "las centenas", 1000: "las unidades de millar", 10000: "las decenas de millar", 100000: "las centenas de millar"}


def rd(n, p):
    return (n + p // 2) // p * p


def near(n):
    s = list(str(n))
    i = R.randrange(1, len(s))
    s[i] = str((int(s[i]) + R.choice([1, 2, 7, 8, 9])) % 10)
    return int("".join(s))


def s1_signo():
    a = R.randint(10000, 999999)
    if R.random() < 0.3:
        b = int(str(a)[:-1]) if a >= 100000 else a * 10 + R.randint(0, 9)
        if b >= 10 ** 6 or b < 1000:
            return None
    else:
        b = near(a)
    if a == b:
        return None
    A, B = num(a), num(b)
    ok = "%s %s %s" % (A, "&lt;" if a < b else "&gt;", B)
    bad = ["%s %s %s" % (A, "&gt;" if a < b else "&lt;", B), "%s %s %s" % (B, "&lt;" if a < b else "&gt;", A), "%s = %s" % (A, B)]
    return mcq("Compara %s y %s. ¿Qué es correcto?" % (A, B), ok, bad,
               "<b>%s</b>. %s" % (ok, "Primero miramos cuántas cifras tiene cada número." if len(str(a)) != len(str(b)) else "Tienen las mismas cifras: comparamos de izquierda a derecha hasta encontrar una cifra distinta."))


def s1_verdad():
    a = R.randint(10000, 999999)
    k = R.choice(["mayor", "menor"])
    s_ = str(a)
    i = R.randrange(1, len(s_) - 1)
    d = int(s_[i])
    if d in (0, 9):
        return None
    up = int(s_[:i] + str(d + 1) + s_[i + 1:])
    dn = [int(s_[:i] + str(d - 1) + s_[i + 1:]), int(s_[:i] + str(d) + "0" * (len(s_) - i - 1)), int(s_[:-1]) if a >= 100000 else a - 1]
    lo = int(s_[:i] + str(d - 1) + s_[i + 1:])
    upl = [up, int(s_[:i] + str(d) + "9" * (len(s_) - i - 1)), a * 10 if a < 100000 else a + 1]
    if k == "mayor":
        return mcq("¿Qué número es mayor que %s?" % num(a), num(up), [num(x) for x in dn if x != a], "%s &gt; %s." % (num(up), num(a)))
    return mcq("¿Qué número es menor que %s?" % num(a), num(lo), [num(x) for x in upl if x != a and x != up] + [num(up)], "%s &lt; %s." % (num(lo), num(a)))


def s2_orden():
    base = R.randint(10, 99) * 1000 + R.randint(0, 999)
    xs = sorted({base, near(base), near(base), near(base) // 10 if base > 99999 else base * 10 + R.randint(0, 9)})
    if len(xs) < 4:
        return None
    xs = xs[:4]
    R.shuffle(xs)
    k = R.choice(["mayor", "menor", "asc", "desc"])
    lst = ", ".join(num(x) for x in xs)
    if k == "mayor":
        return mcq("¿Cuál es el número mayor? %s" % lst, num(max(xs)), [num(x) for x in xs], "El mayor es <b>%s</b>." % num(max(xs)))
    if k == "menor":
        return mcq("¿Cuál es el número menor? %s" % lst, num(min(xs)), [num(x) for x in xs], "El menor es <b>%s</b>." % num(min(xs)))
    up = sorted(xs)
    seq = up if k == "asc" else up[::-1]
    sep = " &lt; " if k == "asc" else " &gt; "
    w1 = list(seq[::-1])
    w2 = list(seq)
    w2[1], w2[2] = w2[2], w2[1]
    w3 = list(seq)
    w3[0], w3[1] = w3[1], w3[0]
    f = lambda L: sep.join(num(x) for x in L)
    return mcq("Ordena de %s: %s" % ("menor a mayor" if k == "asc" else "mayor a menor", lst), f(seq), [f(w2), f(w3), f(w1) if False else f([seq[0], seq[2], seq[1], seq[3]]), f([seq[3], seq[1], seq[2], seq[0]])],
               "<b>%s</b>." % f(seq))


def s3_redondear():
    p = R.choice([10, 100, 1000, 1000, 10000, 10000, 100000])
    n = R.randint(1000 if p < 10000 else 10000, 999999 if p < 100000 else 949999)
    if R.random() < 0.3:
        n = n // p * p + p // 2 + R.randint(0, p // 10 if p > 10 else 0)
    r = rd(n, p)
    if r == n or r >= 10 ** 6:
        return None
    down, up = n // p * p, n // p * p + p
    nxt = str(n % p).rjust(len(str(p)) - 1, "0")[0]
    return mcq("Redondea %s a %s." % (num(n), ORDP[p]), num(r), [num(down if r == up else up), num(rd(n, p // 10)) if p > 10 else num(n + 1), num(rd(n, p * 10)) if p < 100000 else num(r + p)],
               "Miramos la cifra siguiente a %s: es %s. %s: <b>%s</b>." % (ORDP[p], nxt, "Como es 5 o más, redondeamos hacia arriba" if int(nxt) >= 5 else "Como es menor que 5, redondeamos hacia abajo", num(r)))


def s4_recta():
    p = R.choice([1000, 10000])
    lo = R.randint(1, 80) * p
    n = lo + R.randint(1, 9) * p // 10 + R.randint(1, p // 10 - 1)
    if p // 10 * (n - lo) // p == 5:
        return None
    r = rd(n, p)
    g = recta(lo, lo + p, p // 10, marks=[(n // (p // 10) * (p // 10), "")], labels=[lo, lo + p], width=420)
    return mcq(g + "El número %s está entre %s y %s. ¿A cuál está más cerca?" % (num(n), num(lo), num(lo + p)), num(r), [num(lo if r != lo else lo + p), num(lo + p // 2), num(rd(n, p // 10)), num(lo - p) if lo > p else num(lo + 2 * p)],
               "%s está más cerca de <b>%s</b>." % (num(n), num(r)))


def s4_entre():
    p = R.choice([100, 1000, 10000])
    n = R.randint(10000, 989999)
    if n % p == 0:
        return None
    a, b = n // p * p, n // p * p + p
    return mcq("¿Entre qué dos %s está %s?" % ({100: "centenas", 1000: "unidades de millar", 10000: "decenas de millar"}[p], num(n)),
               "entre %s y %s" % (num(a), num(b)), ["entre %s y %s" % (num(a - p), num(a)), "entre %s y %s" % (num(b), num(b + p)), "entre %s y %s" % (num(a - 2 * p), num(a - p)), "entre %s y %s" % (num(b + p), num(b + 2 * p)) if b + 2 * p < 10 ** 6 else None],
               "%s &lt; %s &lt; %s." % (num(a), num(n), num(b)))


NM = ["Ana", "Pablo", "Lucía", "Hugo", "Sofía", "Mateo"]


def s5_problema():
    k = R.choice(["ciudades", "visitas", "precio", "mayor_cifra", "redondeo_ctx", "estadio"])
    if k == "ciudades":
        c = R.sample([("Salamanca", 144000), ("Burgos", 174000), ("León", 122000), ("Cádiz", 111000), ("Logroño", 152000), ("Badajoz", 150000), ("Huelva", 142000), ("Lleida", 140000), ("Jaén", 111000), ("Albacete", 174000), ("Castellón", 172000), ("Tarragona", 136000)], 4)
        c = [(a, b + R.randint(1, 999)) for a, b in c]
        if len({b for a, b in c}) < 4:
            return None
        t = ", ".join("%s: %s" % (a, num(b)) for a, b in c)
        m = max(c, key=lambda x: x[1])
        return mcq("Habitantes de cuatro ciudades (aproximados): %s. ¿Qué ciudad tiene más habitantes?" % t, m[0], [a for a, b in c], "%s es el número mayor." % num(m[1]))
    if k == "visitas":
        n = R.randint(10000, 99999)
        p = R.choice([1000, 10000])
        r = rd(n, p)
        return mcq("Un museo tuvo %s visitas en un año. Redondeado a %s, ¿cuántas visitas fueron?" % (num(n), ORDP[p]), "unas %s" % num(r),
                   ["unas %s" % num(r - p if r > n else r + p), "unas %s" % num(rd(n, p // 10)), "unas %s" % num(rd(n, p * 10)) if rd(n, p * 10) != r else "unas %s" % num(r + 2 * p)],
                   "Redondeamos %s a %s: <b>%s</b>." % (num(n), ORDP[p], num(r)))
    if k == "precio":
        a, b = R.sample(range(12000, 39999), 2)
        y = R.choice(["furgoneta", "caravana", "moto grande", "barca"])
        return mcq("Un coche cuesta %s € y una %s cuesta %s €. ¿Qué es más caro?" % (num(a), y, num(b)),
                   "el coche" if a > b else "la %s" % y, ["la %s" % y if a > b else "el coche", "cuestan lo mismo", "no se puede saber"], "%s %s %s." % (num(a), "&gt;" if a > b else "&lt;", num(b)))
    if k == "mayor_cifra":
        ds = R.sample(range(1, 10), 5) + [0]
        R.shuffle(ds)
        big = int("".join(sorted(map(str, ds), reverse=True)))
        sm = sorted(map(str, ds))
        sm[0], sm[1] = sm[1], sm[0]
        small = int("".join(sm))
        q = R.choice(["mayor", "menor"])
        cs = ", ".join(map(str, sorted(ds)))
        ans = big if q == "mayor" else small
        w = [int("".join(sorted(map(str, ds)))), small if q == "mayor" else big, int(str(big)[:-2] + str(big)[-1] + str(big)[-2]) if q == "mayor" else int(str(small)[:-2] + str(small)[-1] + str(small)[-2])]
        return mcq("Con las cifras %s (sin repetir), ¿cuál es el número %s de seis cifras que puedes formar?" % (cs, q), num(ans), [num(x) for x in w if x >= 100000] + [num(ans + 9) if q == "mayor" else num(ans + 90)],
                   "El %s: <b>%s</b>%s." % (q, num(ans), "" if q == "mayor" else " (el 0 no puede ir el primero)"))
    if k == "redondeo_ctx":
        n = R.randint(100, 999) * 100 + R.randint(1, 99)
        if rd(n, 1000) in (rd(n, 100), rd(n, 10000)):
            return None
        return mcq("En una carrera popular hay %s corredores. El periódico dice que hay «unos %s». ¿A qué orden ha redondeado?" % (num(n), num(rd(n, 1000))),
                   "a las unidades de millar", ["a las centenas", "a las decenas", "a las decenas de millar"], "%s → %s: redondeo a las <b>unidades de millar</b>." % (num(n), num(rd(n, 1000))))
    eq = R.sample(["Real Madrid", "Barcelona", "Atlético", "Betis", "Sevilla", "Valencia", "Athletic", "Real Sociedad"], 4)
    base = R.randint(40, 79) * 1000
    vs = sorted({base + R.randint(0, 9999) for _ in range(4)})
    if len(vs) < 4:
        return None
    R.shuffle(vs)
    q = R.choice(["más", "menos"])
    m = (max if q == "más" else min)(range(4), key=lambda i: vs[i])
    t = "; ".join("%s: %s" % (e, num(v)) for e, v in zip(eq, vs))
    return mcq("Espectadores en cuatro estadios un domingo: %s. ¿En qué estadio había %s espectadores?" % (t, q), "en el del %s" % eq[m], ["en el del %s" % e for e in eq],
               "%s es el número %s." % (num(vs[m]), "mayor" if q == "más" else "menor"))


def main():
    seen = set()
    sets = [
        ("Comparar con &lt; y &gt;", mix(R, seen, [(s1_signo, 14), (s1_verdad, 6)])),
        ("Ordenar números", mix(R, seen, [(s2_orden, 20)])),
        ("Redondear", mix(R, seen, [(s3_redondear, 20)])),
        ("Recta numérica y aproximaciones", mix(R, seen, [(s4_recta, 10), (s4_entre, 10)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para <b>comparar</b>, mira primero cuántas cifras tiene cada número: el que tiene más cifras es mayor.",
         "Si tienen las mismas cifras, compara de izquierda a derecha: 45 812 &lt; 45 912 porque 8 &lt; 9 en las centenas.",
         "Para <b>redondear</b>, mira la cifra siguiente al orden pedido: si es 0, 1, 2, 3 o 4, hacia abajo; si es 5, 6, 7, 8 o 9, hacia arriba."],
        [("Redondea 36 482 a las unidades de millar", ["La cifra de las UM es 6; la siguiente es 4", "4 &lt; 5 → hacia abajo"], "36 000"),
         ("Redondea 128 550 a las centenas", ["La cifra siguiente a las centenas es 5", "5 → hacia arriba"], "128 600")],
        [["Comparar solo la primera cifra", "9876 &lt; 12 345: primero cuenta las cifras."],
         ["Redondear un 5 hacia abajo", "Con 5, siempre hacia arriba."],
         ["Cambiar las cifras de la izquierda", "Al redondear, las cifras a la izquierda solo cambian si hay que sumar 1."]])
    faq = [("¿Cómo se redondea un número?", "Se mira la cifra que está a la derecha del orden al que redondeamos. Si es menor que 5 se deja igual y las cifras de la derecha pasan a 0; si es 5 o más, se suma 1 a ese orden."),
           ("¿Qué significan los signos < y >?", "< significa «es menor que» y > significa «es mayor que». La abertura apunta siempre hacia el número mayor.")]
    make_unit(R, "comparar-y-redondear-numeros", "N",
              "Comparación y ordenación de números naturales de hasta seis cifras utilizando los signos < y >; redondeo y estimación de números naturales",
              "Comparar, ordenar y redondear números", "Comparar y redondear números",
              "Fichas de matemáticas de 4.º de Primaria: comparar números con < y >, ordenar de mayor a menor, redondear a decenas, centenas y millares, recta numérica y problemas. 100 ejercicios con soluciones.",
              "Compara de izquierda a derecha", "Para redondear, mira la cifra siguiente: de 5 en adelante, hacia arriba.",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
