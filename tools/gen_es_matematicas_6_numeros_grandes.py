# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Números grandes (Sentido numérico)
build(lv): lv = 6 → hasta 999 999 999; lv = 5 → hasta 9 999 999.
Leer y escribir millones, valor posicional (UMi, DMi, CMi…), descomponer, comparar, ordenar y redondear números grandes.
Errores: olvidar los ceros de un grupo (dos millones cinco mil = 2 005 000), leer los millones como miles.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, letra_big, bank
from es_common import tabla_valor

POS = ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar", "centenas de millar", "unidades de millón", "decenas de millón", "centenas de millón"]
R = None
D = 9


def big(zeros=True):
    n = R.randint(10 ** (D - 2), 10 ** D - 1)
    if zeros and R.random() < 0.6:
        s = list(str(n))
        for i in R.sample(range(1, len(s)), R.randint(2, min(5, len(s) - 1))):
            s[i] = "0"
        n = int("".join(s))
    return n


def var(n):
    s = list(str(n))
    i = R.randrange(1, len(s))
    s[i] = "0" if s[i] != "0" else str(R.randint(1, 9))
    return int("".join(s))


def s1_leer():
    n = big()
    if n < 10 ** 6:
        return None
    k = R.choice(["cifras", "letra"])
    ws = [var(n) for _ in range(6)] + [n // 1000 if n % 1000 == 0 else n * 10 // 10 + 1000]
    if k == "cifras":
        return M("¿Cómo se escribe en cifras «%s»?" % letra_big(n), num(n), [num(w) for w in ws], "«%s» = <b>%s</b>." % (letra_big(n), num(n)))
    return M("¿Cómo se lee %s?" % num(n), letra_big(n), [letra_big(w) for w in ws], "Separamos los millones, los miles y las unidades: <b>%s</b>." % letra_big(n))


def s2_valor():
    n = big(zeros=False)
    s = str(n)
    i = R.randrange(len(s))
    dg = int(s[i])
    pos = len(s) - 1 - i
    if dg == 0 or s.count(s[i]) > 1:
        return None
    if R.random() < 0.5:
        v = dg * 10 ** pos
        return M("En el número %s, ¿cuánto vale la cifra %d?" % (num(n), dg), num(v), [num(v // 10) if pos else "10", num(v * 10), num(v // 1000) if pos >= 3 else num(v * 100), str(dg)],
                 "El %d está en las %s: vale <b>%s</b>." % (dg, POS[pos], num(v)))
    return M("En el número %s, ¿qué orden ocupa la cifra %d?" % (num(n), dg), POS[pos], [POS[p] for p in (pos - 1, pos + 1, pos - 3, pos + 3, pos + 2) if 0 <= p < 9],
             "Contando desde la derecha: U, D, C, UM, DM, CM, UMi, DMi, CMi. Ocupa las <b>%s</b>." % POS[pos])


def s2_tabla():
    n = big()
    return M(tabla_valor(n, len(str(n))) + "¿Qué número está escrito en la tabla?", num(n), [num(var(n)), num(n // 10), num(n * 10) if n * 10 < 10 ** 9 else num(n + 10 ** 6), num(int(str(n)[::-1]))],
             "Leemos de izquierda a derecha: <b>%s</b>." % num(n))


def s3_desc():
    n = big()
    s = str(n)
    parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    txt = " + ".join(num(p) for p in parts)
    if R.random() < 0.5:
        alt = list(parts)
        alt[-1] = alt[-1] * 10
        return M("¿Qué número es %s?" % txt, num(n), [num(sum(alt)), num(int(s.replace("0", ""))), num(n + 10 ** R.randint(2, D - 2)), num(var(n))],
                 "Sumamos los valores: <b>%s</b>." % num(n))
    w1 = " + ".join(num(p // 10 if i == 0 else p) for i, p in enumerate(parts))
    w2 = " + ".join(num(p * 10 if i == len(parts) - 1 else p) for i, p in enumerate(parts))
    w3 = " + ".join(c for c in s if c != "0")
    return M("¿Cuál es la descomposición de %s?" % num(n), txt, [w1, w2, w3], "Cada cifra por su valor: <b>%s</b>." % txt)


def s4_comparar():
    k = R.choice(["mayor", "orden", "redondeo", "redondeo"])
    if k == "redondeo":
        p = R.choice([1000, 10000, 100000, 10 ** 6] + ([10 ** 7] if D == 9 else []))
        n = big(zeros=False)
        if n < p * 10:
            return None
        r = (n + p // 2) // p * p
        nm = {1000: "los millares", 10000: "las decenas de millar", 100000: "las centenas de millar", 10 ** 6: "los millones", 10 ** 7: "las decenas de millón"}[p]
        other = n // p * p if r != n // p * p else n // p * p + p
        return M("Redondea %s a %s." % (num(n), nm), num(r), [num(other), num((n + p * 5) // (p * 10) * p * 10), num((n + p // 20) // (p // 10) * (p // 10))],
                 "Miramos la cifra siguiente: %s <b>%s</b>." % ("5 o más, hacia arriba:" if r > n else "menor que 5, hacia abajo:", num(r)))
    xs = sorted({big() for _ in range(4)})
    if len(xs) < 4 or len({len(str(x)) for x in xs}) < 2:
        base = big(zeros=False)
        xs = sorted({base, var(base), var(base), base // 10})
        if len(xs) < 4:
            return None
    sh = list(xs)
    R.shuffle(sh)
    if k == "mayor":
        return M("¿Cuál es el número mayor? %s" % "; ".join(num(x) for x in sh), num(xs[-1]), [num(x) for x in xs[:-1]], "Primero miramos cuántas cifras tiene; después comparamos de izquierda a derecha: <b>%s</b>." % num(xs[-1]))
    f = lambda L: " &lt; ".join(num(x) for x in L)
    return M("Ordena de menor a mayor: %s" % "; ".join(num(x) for x in sh), f(xs), [f([xs[1], xs[0], xs[2], xs[3]]), f([xs[0], xs[2], xs[1], xs[3]]), f([xs[0], xs[1], xs[3], xs[2]])], "<b>%s</b>." % f(xs))


DATOS = [("España", 48), ("Madrid (comunidad)", 7), ("Andalucía", 8), ("Cataluña", 8), ("Comunidad Valenciana", 5), ("Galicia", 2), ("Castilla y León", 2), ("Canarias", 2)]


def s5_vida():
    k = R.choice(["hab", "precio", "suma", "dif", "km"])
    if k == "hab":
        nm, m = R.choice(DATOS)
        n = m * 10 ** 6 + R.randint(1, 999) * 1000 + R.randint(0, 999)
        r = (n + 500000) // 10 ** 6 * 10 ** 6
        return M("%s tiene %s habitantes (dato aproximado). ¿Cuántos millones de habitantes son, redondeando?" % (nm, num(n)), "unos %s" % num(r // 10 ** 6) + " millones",
                 ["unos %s millones" % num(x) for x in (r // 10 ** 6 + 1, max(1, r // 10 ** 6 - 1), r // 10 ** 5, r // 10 ** 6 * 10)], "%s ≈ <b>%s</b>." % (num(n), num(r)))
    if k == "precio":
        n = R.randint(150, 990) * 1000
        return M("Una casa cuesta %s €. ¿Cómo se lee esa cantidad?" % num(n), letra_big(n) + " euros", [letra_big(var(n)) + " euros", letra_big(n * 10) + " euros", letra_big(n // 10) + " euros"],
                 "<b>%s euros</b>." % letra_big(n))
    if k == "suma":
        a, b = R.randint(1, 9) * 10 ** 6, R.randint(1, 999) * 1000
        return M("¿Qué número es %s millones y %s mil?" % (num(a // 10 ** 6), num(b // 1000)), num(a + b), [num(a + b // 1000), num(a // 1000 + b), num(a + b * 10), num(a * 10 + b)],
                 "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "dif":
        a = R.randint(2, 9) * 10 ** 6
        b = R.randint(1, 9) * 10 ** 5
        return M("Un estadio tiene una media de %s espectadores al año y otro, %s menos. ¿Cuántos tiene el segundo?" % (num(a), num(b)), num(a - b), [num(a + b), num(a - b * 10) if a > b * 10 else num(a - b // 10), num(a - b // 10), num(b)],
                 "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    n = R.randint(1, 9) * 10 ** 6 + R.randint(1, 9) * 10 ** 5
    return M("Un avión ha volado %s km en toda su vida. ¿Cuántos millones de kilómetros son, más o menos?" % num(n), "unos %d millones" % ((n + 500000) // 10 ** 6),
             ["unos %d millones" % x for x in ((n + 500000) // 10 ** 6 + 1, n // 10 ** 5, (n + 500000) // 10 ** 6 * 10, max(0, (n + 500000) // 10 ** 6 - 1))], "%s ≈ <b>%s</b>." % (num(n), num((n + 500000) // 10 ** 6 * 10 ** 6)))


def build(lv):
    global R, D
    R = random.Random(40001 + lv * 1000)
    D = 9 if lv == 6 else 7
    seen = set()
    sets = [
        ("Leer y escribir números grandes", mix(R, seen, [(s1_leer, 20)])),
        ("Valor posicional", mix(R, seen, [(s2_valor, 14), (s2_tabla, 6)])),
        ("Descomponer números", mix(R, seen, [(s3_desc, 20)])),
        ("Comparar, ordenar y redondear", mix(R, seen, [(s4_comparar, 20)])),
        ("Números grandes en la vida diaria", mix(R, seen, [(s5_vida, 20)])),
    ]
    top = "999 999 999" if lv == 6 else "9 999 999"
    body = lesson(
        ["Para leer un número grande, sepáralo en grupos de tres cifras desde la derecha: <b>millones | miles | unidades</b>. 4 305 020 = cuatro millones trescientos cinco mil veinte.",
         "Cada cifra vale según su posición: U, D, C, UM, DM, CM, <b>UMi</b> (unidad de millón), DMi, CMi. Un millón son mil millares: 1 000 000.",
         "Si falta un grupo, escribe <b>000</b>: «dos millones cinco mil» = 2 005 000."],
        [("Escribe «siete millones cuarenta mil trescientos»", ["millones: 7", "miles: 040", "unidades: 300"], "7 040 300"),
         ("Redondea 3 486 200 a los millones", ["La cifra siguiente a los millones es 4", "4 &lt; 5 → hacia abajo"], "3 000 000")],
        [["Olvidar los ceros de un grupo", "Cada grupo tiene tres cifras: 2 005 000."],
         ["Leer los millones como miles", "Separa bien los grupos: 4 | 305 | 020."],
         ["Confundir la cifra con su valor", "El 4 de 4 305 020 vale 4 000 000."]],
        tabla_valor(4305020, 7))
    faq = [("¿Cómo se leen los números de siete o más cifras?", "Se separan en grupos de tres cifras desde la derecha. Primero se leen los millones, después los miles y al final las unidades: 4 305 020 = cuatro millones trescientos cinco mil veinte."),
           ("¿Cuántos ceros tiene un millón?", "Seis: 1 000 000. Un millón son mil millares.")]
    make_unit(R, "numeros-grandes", "N",
              "Números naturales grandes (hasta %s): lectura, escritura, valor posicional, descomposición, comparación, ordenación y redondeo" % top,
              "Números grandes: los millones", "Números grandes",
              "Fichas de matemáticas de %d.º de Primaria: leer y escribir millones, valor posicional, descomponer, comparar, ordenar y redondear números grandes. 100 ejercicios con soluciones." % lv,
              "Grupos de tres cifras", "millones | miles | unidades",
              body, faq, sets, 1, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
