# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º, 2.º y 3.º de Primaria: Comparar y ordenar números (Sentido numérico)
build(lv): lv = 1 hasta 99, lv = 2 hasta 999, lv = 3 hasta 9999 (y redondeo a las decenas y centenas).
Mayor que, menor que e igual (&gt;, &lt;, =), ordenar de menor a mayor y de mayor a menor, números entre dos dados,
lv = 3: redondear.
Errores: mirar solo la última cifra, confundir los signos &lt; y &gt;, redondear un 5 hacia abajo.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, recta
import es_pics as P

R = None
LV = 3
TOP = {1: 99, 2: 999, 3: 9999}


def rn():
    return R.randint(10 ** LV, TOP[LV]) if R.random() < 0.8 else R.randint(10 ** (LV - 1), TOP[LV])


def near(n):
    s = list(str(n))
    i = R.randrange(len(s))
    s[i] = str((int(s[i]) + R.choice([1, 2, 7, 8, 9])) % 10)
    if s[0] == "0":
        s[0] = "1"
    return int("".join(s))


def s1_dibujos():
    if LV > 1:
        a, b = rn(), None
        b = near(a)
        if a == b:
            return None
        A, B = num(a), num(b)
        ok = "%s %s %s" % (A, "&lt;" if a < b else "&gt;", B)
        return mcq("Compara %s y %s. ¿Qué es correcto?" % (A, B), ok, ["%s %s %s" % (A, "&gt;" if a < b else "&lt;", B), "%s %s %s" % (B, "&lt;" if a < b else "&gt;", A), "%s = %s" % (A, B)],
                   "Comparamos las cifras de izquierda a derecha: <b>%s</b>." % ok)
    a, b = R.sample(range(3, 16), 2)
    ka, kb = R.sample(P.KINDS, 2)
    pic = P.dos_grupos(a, ka, b, kb, "?")
    return mcq(pic + "¿Hay más %s o más %s?" % (P.nombre(ka), P.nombre(kb)), "más %s" % P.nombre(ka if a > b else kb), ["más %s" % P.nombre(kb if a > b else ka), "hay los mismos", "no se puede saber"],
               "%d %s %d: hay <b>más %s</b>." % (a, "&gt;" if a > b else "&lt;", b, P.nombre(ka if a > b else kb)))


def s2_signo():
    a = rn()
    b = near(a) if R.random() < 0.7 else a
    s = "&lt;" if a < b else "&gt;" if a > b else "="
    ok = "%s %s %s" % (num(a), s, num(b))
    return mcq("¿Qué signo va en el hueco? %s ___ %s" % (num(a), num(b)), s, [x for x in ("&lt;", "&gt;", "=") if x != s] + ["+"],
               "<b>%s</b>. La abertura del signo mira hacia el número mayor." % ok if s != "=" else "Son iguales: <b>%s</b>." % ok)


def s3_ordenar():
    base = rn()
    xs = sorted({base, near(base), near(base), near(base), near(base)})
    if len(xs) < 4:
        return None
    xs = xs[:4]
    sh = list(xs)
    R.shuffle(sh)
    k = R.choice(["mayor", "menor", "asc", "desc"])
    if k in ("mayor", "menor"):
        a = xs[-1] if k == "mayor" else xs[0]
        return mcq("¿Cuál es el número %s: %s?" % (k, ", ".join(num(x) for x in sh)), num(a), [num(x) for x in xs], "El %s es <b>%s</b>." % (k, num(a)))
    seq = xs if k == "asc" else xs[::-1]
    sep = " &lt; " if k == "asc" else " &gt; "
    f = lambda L: sep.join(num(x) for x in L)
    return mcq("Ordena de %s: %s" % ("menor a mayor" if k == "asc" else "mayor a menor", ", ".join(num(x) for x in sh)), f(seq), [f(seq[::-1]), f([seq[1], seq[0], seq[2], seq[3]]), f([seq[0], seq[2], seq[1], seq[3]])], "<b>%s</b>." % f(seq))


def s4_entre():
    k = R.choice(["entre", "recta", "redondeo"] if LV == 3 else ["entre", "recta", "decena"])
    if k == "entre":
        a = R.randint(10 ** (LV - 1), TOP[LV] - 20)
        b = a + R.randint(3, 12)
        x = R.randint(a + 1, b - 1)
        ws = [a - R.randint(1, 5), b + R.randint(1, 5), a, b]
        return mcq("¿Qué número está entre %s y %s?" % (num(a), num(b)), num(x), [num(w) for w in ws], "%s &lt; %s &lt; %s." % (num(a), num(x), num(b)))
    if k == "decena":
        n = R.randint(11, TOP[LV] - 10)
        if n % 10 in (0, 5):
            return None
        r = (n + 5) // 10 * 10
        return mcq("¿A qué decena está más cerca %s?" % num(n), num(r), [num(n // 10 * 10 if r != n // 10 * 10 else r + 10), num(n + 10), num(n // 10)], "%s está más cerca de <b>%s</b>." % (num(n), num(r)))
    if k == "recta":
        step = {1: 1, 2: 10, 3: 100}[LV]
        lo = R.randint(0, TOP[LV] // (10 * step) - 1) * 10 * step
        a, b = R.sample(range(1, 10), 2)
        g = recta(lo, lo + 10 * step, step, marks=[(lo + a * step, "A"), (lo + b * step, "B")], every=5 * step)
        big = "A" if a > b else "B"
        return mcq(g + "¿Qué número es mayor, A o B?", "el punto %s, que vale %s" % (big, num(lo + max(a, b) * step)), ["el punto %s, que vale %s" % ("B" if big == "A" else "A", num(lo + min(a, b) * step)), "son iguales", "el punto %s, que vale %s" % (big, num(lo + max(a, b) * step + step))],
                   "En la recta, el mayor está más a la derecha: <b>%s = %s</b>." % (big, num(lo + max(a, b) * step)))
    p = R.choice([10, 100, 1000])
    n = R.randint(1001, 9999)
    r = (n + p // 2) // p * p
    if r == n:
        return None
    nm = {10: "las decenas", 100: "las centenas", 1000: "los millares"}[p]
    return mcq("Redondea %s a %s." % (num(n), nm), num(r), [num(n // p * p if r != n // p * p else r + p), num((n + 5) // 10 * 10) if p != 10 else num(n + 10), num((n + 50) // 100 * 100) if p == 1000 else num((n + 500) // 1000 * 1000)],
               "Miramos la cifra siguiente: %s <b>%s</b>." % ("5 o más, hacia arriba:" if r > n else "menor que 5, hacia abajo:", num(r)))


def s5_problema():
    k = R.choice(["edad", "puntos", "altura", "precio", "libros"])
    nombres = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo"]
    a, b = R.sample(nombres, 2)
    x = rn()
    y = near(x)
    if x == y:
        return None
    if k == "edad" and LV == 1:
        x, y = R.sample(range(6, 9), 2)
        return mcq("%s tiene %d años y %s tiene %d. ¿Quién es mayor?" % (a, x, b, y), a if x > y else b, [b if x > y else a, "los dos igual", "no se puede saber"], "%d %s %d: <b>%s</b>." % (x, "&gt;" if x > y else "&lt;", y, a if x > y else b))
    ctx = {"edad": ("puntos", "En un juego, %s hace %s puntos y %s, %s. ¿Quién ha hecho más puntos?"), "puntos": ("puntos", "En un concurso, %s consigue %s puntos y %s, %s. ¿Quién tiene más?"),
           "altura": ("cromos", "%s tiene %s cromos y %s tiene %s. ¿Quién tiene menos cromos?"), "precio": ("€", "Una bici cuesta %s € y un patinete %s €… %s %s"), "libros": ("libros", "La biblioteca de %s tiene %s libros y la de %s, %s. ¿Cuál tiene más libros?")}[k]
    if k == "precio":
        return mcq("Una bicicleta cuesta %s € y un patinete cuesta %s €. ¿Qué es más barato?" % (num(x), num(y)), "el patinete" if y < x else "la bicicleta", ["la bicicleta" if y < x else "el patinete", "cuestan lo mismo", "no se puede saber"],
                   "%s %s %s: <b>%s</b>." % (num(x), "&gt;" if x > y else "&lt;", num(y), "el patinete" if y < x else "la bicicleta")) if LV > 1 else None
    if k == "libros":
        ca, cb = R.sample(["mi colegio", "el colegio de mi primo", "mi barrio", "el pueblo de mi abuela"], 2)
        return mcq(ctx[1] % (ca, num(x), cb, num(y)), ca if x > y else cb, [cb if x > y else ca, "las dos igual", "no se puede saber"], "%s %s %s." % (num(x), "&gt;" if x > y else "&lt;", num(y)))
    menos = k == "altura"
    win = (a if x < y else b) if menos else (a if x > y else b)
    return mcq(ctx[1] % (a, num(x), b, num(y)), win, [b if win == a else a, "los dos igual", "no se puede saber"], "%s %s %s: <b>%s</b>." % (num(x), "&gt;" if x > y else "&lt;", num(y), win))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30002 + lv * 1000)
    seen = set()
    sets = [
        ("Más, menos o igual", mix(R, seen, [(s1_dibujos, 20)])),
        ("Mayor que, menor que o igual", mix(R, seen, [(s2_signo, 20)])),
        ("Ordenar números", mix(R, seen, [(s3_ordenar, 20)])),
        ("Entre, la recta y el redondeo" if lv == 3 else "Entre dos números y la recta", mix(R, seen, [(s4_entre, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    think = ["Para comparar, mira primero cuántas cifras tiene cada número. Si tienen las mismas, compara de izquierda a derecha.",
             "<b>&gt;</b> significa «mayor que» y <b>&lt;</b>, «menor que». La parte abierta del signo mira siempre al número mayor: 45 &gt; 38."]
    if lv == 3:
        think.append("Para <b>redondear</b>, mira la cifra siguiente: si es 5 o más, hacia arriba; si es menor que 5, hacia abajo.")
    body = lesson(think,
                  [("Compara %s" % {1: "47 y 52", 2: "382 y 328", 3: "4521 y 4512"}[lv], ["Miramos la primera cifra distinta"], {1: "47 &lt; 52", 2: "382 &gt; 328", 3: "4521 &gt; 4512"}[lv]),
                   ("Ordena de menor a mayor %s" % {1: "35, 53, 30", 2: "250, 205, 520", 3: "3060, 3600, 3006"}[lv], ["Comparamos de izquierda a derecha"], {1: "30 &lt; 35 &lt; 53", 2: "205 &lt; 250 &lt; 520", 3: "3006 &lt; 3060 &lt; 3600"}[lv])],
                  [["Mirar solo la última cifra", "En 39 y 41, manda la primera cifra: 39 &lt; 41."],
                   ["Confundir &lt; y &gt;", "La boca abierta del signo «se come» al número mayor."],
                   ["Redondear el 5 hacia abajo" if lv == 3 else "Olvidar el cero", "Con 5, hacia arriba: 4350 → 4400." if lv == 3 else "305 no es igual que 35."]])
    faq = [("¿Cómo se comparan dos números?", "Si tienen distinto número de cifras, es mayor el que tiene más. Si tienen las mismas, se comparan las cifras de izquierda a derecha hasta encontrar una distinta."),
           ("¿Qué significan los signos < y >?", "< significa «es menor que» y > significa «es mayor que». La abertura apunta al número mayor.")]
    make_unit(R, "comparar-y-ordenar-numeros" if lv < 3 else "comparar-ordenar-y-redondear", "N",
              "Comparación y ordenación de números naturales hasta %s con los signos <, > e =; situación en la recta numérica" % num(TOP[lv]) + ("; redondeo" if lv == 3 else ""),
              "Comparar y ordenar números" if lv < 3 else "Comparar, ordenar y redondear", "Comparar y ordenar" if lv < 3 else "Comparar y redondear",
              "Fichas de matemáticas de %d.º de Primaria: mayor que, menor que e igual, signos < y >, ordenar números%s y problemas. 100 ejercicios con soluciones." % (lv, ", la recta y el redondeo" if lv == 3 else " y la recta numérica"),
              "El signo mira al número mayor", "Compara de izquierda a derecha.",
              body, faq, sets, 2, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(3)
