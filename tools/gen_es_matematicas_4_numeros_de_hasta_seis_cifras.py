# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Números de hasta seis cifras (Sentido numérico)
  python3 tools/gen_es_matematicas_4_numeros_de_hasta_seis_cifras.py
Leer y escribir números hasta 999 999 (en cifras y en letra), valor posicional (CM, DM, UM, C, D, U),
descomposición, anterior y posterior, series de 1000 en 1000 y de 10 000 en 10 000, la recta numérica.
Errores: olvidar los ceros intermedios (doscientos cinco mil ocho = 205 008), confundir el valor de una cifra con la cifra.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, letra, tabla_valor, recta, bank, POR

R = random.Random(44001)
POS = ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar", "centenas de millar"]


def rnd6(zeros=True):
    n = R.randint(100000, 999999)
    if zeros and R.random() < 0.5:
        ds = list(str(n))
        for i in R.sample(range(1, 6), R.randint(1, 3)):
            ds[i] = "0"
        n = int("".join(ds))
    return n


def s1_letra():
    n = rnd6() if R.random() < 0.7 else R.randint(10000, 99999)
    k = R.choice(["a_cifras", "a_letra"])
    s = str(n)
    wrong = set()
    for _ in range(10):
        ds = list(s)
        i = R.randrange(1, len(ds))
        if ds[i] != "0":
            ds[i] = "0"
        else:
            ds[i] = str(R.randint(1, 9))
        wrong.add(int("".join(ds)))
    wrong.discard(n)
    wrong.add(int(s[:-1]) if len(s) > 5 and s.endswith("0") else n * 10 if n < 100000 else n // 10)
    ws = sorted(wrong)
    R.shuffle(ws)
    if k == "a_cifras":
        return mcq("¿Cómo se escribe en cifras «%s»?" % letra(n), num(n), [num(w) for w in ws], "«%s» = <b>%s</b>." % (letra(n), num(n)))
    return mcq("¿Cómo se lee el número %s?" % num(n), letra(n), [letra(w) for w in ws if w < 10 ** 6], "%s se lee «<b>%s</b>»." % (num(n), letra(n)))


def s2_valor():
    n = rnd6(zeros=False)
    s = str(n)
    i = R.randrange(6)
    d = int(s[i])
    if d == 0:
        return None
    pos = 5 - i
    k = R.choice(["valor", "orden", "tabla"])
    if k == "valor":
        v = d * 10 ** pos
        return mcq("En el número %s, ¿cuál es el valor de la cifra %d que está en el lugar de las %s?" % (num(n), d, POS[pos]), num(v), [str(d), num(d * 10 ** (pos - 1)) if pos else num(d * 10), num(d * 10 ** (pos + 1)) if pos < 5 else num(d * 10 ** (pos - 2)), num(d * 10 ** (pos + 2))],
                   "%d %s = <b>%s</b>." % (d, POS[pos], num(v)))
    if k == "orden":
        if s.count(str(d)) > 1:
            return None
        return mcq("En el número %s, ¿qué orden ocupa la cifra %d?" % (num(n), d), POS[pos], [POS[p] for p in (pos - 1, pos + 1, pos + 2, pos - 2, pos + 3, pos - 3) if 0 <= p < 6],
                   "Contando desde la derecha: U, D, C, UM, DM, CM. El %d está en las <b>%s</b>." % (d, POS[pos]))
    return mcq(tabla_valor(n, 6) + "¿Qué número está escrito en la tabla?", num(n), [num(int(s[::-1])), num(n // 10), num(n + 10 ** R.randint(0, 4))], "Leyendo la tabla de izquierda a derecha: <b>%s</b>." % num(n))


def s3_descomp():
    n = rnd6()
    s = str(n)
    parts = [int(c) * 10 ** (5 - i) for i, c in enumerate(s) if c != "0"]
    k = R.choice(["suma", "inversa", "unidades"])
    if k == "suma":
        txt = " + ".join(num(p) for p in parts)
        alt = list(parts)
        alt[-1] = alt[-1] * 10 if alt[-1] < 100000 else alt[-1] // 10
        sw = list(s)
        j = R.randrange(1, 5)
        sw[j], sw[j + 1] = sw[j + 1], sw[j]
        return mcq("¿Qué número es %s?" % txt, num(n), [num(sum(alt)), num(int(s.replace("0", ""))), num(int("".join(sw))), num(n + 10 ** R.randint(1, 4)), num(n - 10 ** R.randint(1, 4))], "Sumamos los valores: <b>%s</b>." % num(n))
    if k == "inversa":
        txt = " + ".join(num(p) for p in parts)
        w1 = " + ".join(str(int(c)) for c in s if c != "0")
        w2 = " + ".join(num(p // 10 if i == 0 else p) for i, p in enumerate(parts))
        w3 = " + ".join(num(p * 10 if p < 100000 else p) for p in parts)
        return mcq("¿Cuál es la descomposición de %s?" % num(n), txt, [w2, w3, w1], "Cada cifra por su valor: <b>%s</b>." % txt)
    cm, r = divmod(n, 100000)
    dm, r = divmod(r, 10000)
    um, r = divmod(r, 1000)
    c, r = divmod(r, 100)
    d, u = divmod(r, 10)
    txt = "%d CM, %d DM, %d UM, %d C, %d D y %d U" % (cm, dm, um, c, d, u)
    return mcq("¿Qué número tiene %s?" % txt, num(n), [num(int(s[::-1])), num(n // 10 * 10 + (u + 1) % 10) if u != 9 else num(n - 1), num(n + 100000) if cm < 9 else num(n - 100000)], "<b>%s</b>." % num(n))


def s4_series():
    k = R.choice(["ant", "post", "serie", "recta"])
    n = rnd6()
    if k == "ant":
        return mcq("¿Cuál es el número anterior a %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 1000)], "Anterior = uno menos: <b>%s</b>." % num(n - 1))
    if k == "post":
        n = R.choice([199999, 409999, 99999, 239999, 599999, 309999, 789999]) if R.random() < 0.5 else n
        return mcq("¿Cuál es el número posterior a %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 1000) if n + 1000 < 10 ** 6 else num(n + 100)], "Posterior = uno más: <b>%s</b>." % num(n + 1))
    if k == "serie":
        step = R.choice([1000, 10000, 100000, 100, 5000])
        a = R.randint(1, 80) * 1000 + R.randint(0, 9) * 100
        if a + 5 * step >= 10 ** 6:
            return None
        xs = [a + i * step for i in range(4)]
        return mcq("Continúa la serie: %s, …" % ", ".join(num(x) for x in xs), num(a + 4 * step), [num(a + 4 * step + step // 10 if step >= 1000 else a + 4 * step + 10), num(a + 3 * step + step * 10), num(a + 5 * step)],
                   "Va de %s en %s: <b>%s</b>." % (num(step), num(step), num(a + 4 * step)))
    lo = R.randint(1, 90) * 10000
    step = 1000
    x = lo + R.randint(1, 9) * step
    g = recta(lo, lo + 10 * step, step, marks=[(x, "?")], every=5 * step)
    return mcq(g + "¿Qué número está en el lugar de «?»?", num(x), [num(x + step), num(x - step), num(lo + (x - lo) // 10)], "Cada marca vale %s: <b>%s</b>." % (num(step), num(x)))


s5_conceptos = bank(R, [
    ("¿Cuántas unidades tiene una centena de millar?", "100 000".replace(" ", " "), ["10 000".replace(" ", " "), "1000", "1 000 000".replace(" ", " ")]),
    ("¿Cuántas decenas de millar hay en 100 000?".replace(" 100 000", " 100 000"), "10", ["100", "1000", "1"]),
    ("¿Cuál es el mayor número de seis cifras?", "999 999", ["100 000", "99 999", "900 000"]),
    ("¿Cuál es el menor número de seis cifras?", "100 000", ["999 999", "10 000", "111 111"]),
    ("¿Cuántas unidades de millar hay en 45 000?".replace("45 000", "45 000"), "45", ["4", "450", "5"]),
    ("Diez unidades de millar forman…", "una decena de millar", ["una centena de millar", "una centena", "un millón"]),
    ("¿Cuántas cifras tiene el número doscientos mil?", "6", ["3", "5", "4"]),
], "s5_conceptos")


def main():
    seen = set()
    sets = [
        ("Leer y escribir números", mix(R, seen, [(s1_letra, 20)])),
        ("Valor posicional", mix(R, seen, [(s2_valor, 15), (s5_conceptos, 5)])),
        ("Descomponer números", mix(R, seen, [(s3_descomp, 20)])),
        ("Anterior, posterior y series", mix(R, seen, [(s4_series, 18), (s5_conceptos, 2)])),
        ("Repaso", mix(R, seen, [(s1_letra, 7), (s2_valor, 7), (s3_descomp, 6)])),
    ]
    body = lesson(
        ["Los números de seis cifras se leen en dos partes: primero los <b>miles</b> y después el resto. 345 210 se lee «trescientos cuarenta y cinco mil doscientos diez».",
         "Cada cifra tiene un <b>valor</b> según su posición: U, D, C, UM, DM, CM. En 345 210, el 4 vale 40 000.",
         "Si falta un orden, escribe un <b>0</b> en su lugar: «doscientos cinco mil ocho» = 205 008."],
        [("Escribe «setenta mil cuatrocientos tres»", ["70 mil → 70", "cuatrocientos tres → 403"], "70 403"),
         ("Descompón 508 130", ["5 CM, 0 DM, 8 UM, 1 C, 3 D, 0 U"], "500 000 + 8000 + 100 + 30")],
        [["Olvidar los ceros", "Si no se nombra un orden, escribe 0 en ese lugar."],
         ["Confundir la cifra con su valor", "El 4 de 345 210 vale 40 000, no 4."],
         ["Leer cifra a cifra", "Separa los miles: 345 | 210."]],
        tabla_valor(345210, 6))
    faq = [("¿Cómo se leen los números de seis cifras?", "Se separan los tres primeros dígitos (los miles) y los tres últimos. Se lee primero la parte de los miles seguida de «mil» y después el resto: 345 210 = trescientos cuarenta y cinco mil doscientos diez."),
           ("¿Qué dice el currículo de 4.º de Primaria?", "En el segundo ciclo, el alumnado lee, escribe, compara y ordena números naturales hasta seis cifras y comprende el valor posicional de sus cifras.")]
    make_unit(R, "numeros-de-hasta-seis-cifras", "N",
              "Lectura, escritura, representación y comparación de números naturales de hasta seis cifras; valor posicional de las cifras; composición y descomposición",
              "Números de hasta seis cifras", "Números de hasta seis cifras",
              "Fichas de matemáticas de 4.º de Primaria: leer y escribir números de hasta seis cifras, valor posicional, descomposición, anterior y posterior, series y recta numérica. 100 ejercicios con soluciones.",
              "Cada cifra vale según su posición", "CM, DM, UM, C, D, U: escribe 0 si falta un orden.",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
