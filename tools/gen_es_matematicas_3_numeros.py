# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º, 2.º y 3.º de Primaria: Los números (Sentido numérico)
build(lv): lv = 3 → hasta 9999 (UM, C, D, U); lv = 2 → hasta 999; lv = 1 → hasta 99 (con dibujos).
Contar, leer y escribir números en cifras y en letra, valor posicional, descomponer, anterior y posterior, series, la recta numérica.
Errores: escribir 307 como 3007 o 37, confundir el valor de una cifra con la cifra, contar mal al pasar de decena o de centena.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, letra, recta, bloques, tabla_valor
import es_pics as P

R = None
LV = 3
POS = ["unidades", "decenas", "centenas", "unidades de millar"]
SLUG = {1: "numeros-hasta-99", 2: "numeros-hasta-999", 3: "numeros-hasta-9999"}
TOP = {1: 99, 2: 999, 3: 9999}


def rn(lo=None):
    D = LV + 1
    n = R.randint(lo or 10 ** (D - 1), TOP[LV])
    if LV >= 2 and R.random() < 0.4:
        s = list(str(n))
        i = R.randrange(1, len(s))
        s[i] = "0"
        n = int("".join(s))
    return n


def var(n):
    s = list(str(n))
    if len(s) == 1:
        return n + 1
    i = R.randrange(len(s))
    s[i] = str((int(s[i]) + R.choice([1, 2, 8, 9])) % 10)
    if s[0] == "0":
        s[0] = "1"
    return int("".join(s))


def s1_contar():
    if LV == 1:
        k = R.choice(["fila", "marco", "regletas", "regletas"])
        if k == "fila":
            n = R.randint(6, 20)
            kind = R.choice(P.KINDS)
            return mcq(P.fila(n, kind) + "%s %s hay?" % (P.cuantos(kind), P.nombre(kind)), str(n), [str(n + 1), str(n - 1), str(n + 2), str(n - 2)], "Contamos de uno en uno: <b>%d</b>." % n)
        if k == "marco":
            n = R.randint(11, 20)
            return mcq(P.marco10(n, 2) + "¿Cuántos puntos hay?", str(n), [str(n + 1), str(n - 1), str(n - 10), str(n + 10)], "Un marco lleno son 10; 10 + %d = <b>%d</b>." % (n - 10, n))
        t, o = R.randint(1, 9), R.randint(0, 9)
        return mcq(P.regletas(t, o) + "¿Qué número es?", str(10 * t + o), [str(10 * o + t) if o else str(t), str(t + o), str(10 * t + o + 10) if t < 9 else str(10 * t + o - 10)], "%d decenas y %d unidades: <b>%d</b>." % (t, o, 10 * t + o))
    n = rn()
    c, r = divmod(n, 100)
    d_, u = divmod(r, 10)
    m, c = divmod(c, 10)
    if LV == 3 and m > 4:
        return None
    pic = bloques(m, c, d_, u) if (m + c) <= 9 else tabla_valor(n, LV + 1)
    return mcq(pic + "¿Qué número representan?", num(n), [num(var(n)), num(int(str(n)[::-1])) if str(n)[::-1][0] != "0" else num(n + 10), num(n + 100) if n + 100 <= TOP[LV] else num(n - 100), num(m * 1000 + c * 10 + d_ + u) if LV == 3 else num(c * 10 + d_ + u)],
               "%s<b>%s</b>." % ("%d unidades de millar, " % m if m else "", num(n)) if m else "%d centenas, %d decenas y %d unidades: <b>%s</b>." % (c, d_, u, num(n)))


def s2_letra():
    n = rn(1 if LV == 1 else None)
    if LV == 1 and n < 11:
        n += 10
    ws = list({var(n) for _ in range(6)} - {n})
    ws.sort()
    R.shuffle(ws)
    if R.random() < 0.5:
        return mcq("¿Cómo se escribe en cifras «%s»?" % letra(n), num(n), [num(w) for w in ws] + [num(int(str(n)[0] + "0" + str(n)[1:]))], "«%s» = <b>%s</b>." % (letra(n), num(n)))
    return mcq("¿Cómo se lee %s?" % num(n), letra(n), [letra(w) for w in ws], "%s se lee «<b>%s</b>»." % (num(n), letra(n)))


def s3_valor():
    n = rn()
    s = str(n)
    i = R.randrange(len(s))
    dg = int(s[i])
    pos = len(s) - 1 - i
    if dg == 0 or s.count(s[i]) > 1:
        return None
    k = R.choice(["valor", "orden", "desc"])
    if k == "valor":
        v = dg * 10 ** pos
        return mcq("En el número %s, ¿cuánto vale la cifra %d?" % (num(n), dg), num(v), [str(dg), num(dg * 10 ** (pos + 1)), num(dg * 10 ** (pos - 1)) if pos else num(dg * 100)], "El %d está en las %s: vale <b>%s</b>." % (dg, POS[pos], num(v)))
    if k == "orden":
        return mcq("En el número %s, ¿en qué lugar está la cifra %d?" % (num(n), dg), "en las " + POS[pos], ["en las " + POS[p] for p in range(LV + 1) if p != pos] + ["en las " + POS[min(pos + 1, 3)]], "Contamos desde la derecha: <b>%s</b>." % POS[pos])
    parts = [int(c) * 10 ** (len(s) - 1 - j) for j, c in enumerate(s) if c != "0"]
    txt = " + ".join(num(p) for p in parts)
    w1 = " + ".join(c for c in s if c != "0")
    w2 = " + ".join(num(p * 10 if j == len(parts) - 1 else p) for j, p in enumerate(parts))
    w3 = " + ".join(num(p // 10 if j == 0 and p >= 10 else p) for j, p in enumerate(parts))
    return mcq("¿Cuál es la descomposición de %s?" % num(n), txt, [w1, w2, w3], "Cada cifra por su valor: <b>%s</b>." % txt)


def s4_series():
    k = R.choice(["ant", "post", "serie", "recta"])
    if k in ("ant", "post"):
        n = rn(2 if LV == 1 else None)
        if R.random() < 0.5:
            n = n // 10 * 10 + (9 if k == "post" else 0)
            if n < 2 or n >= TOP[LV]:
                return None
        if k == "ant":
            return mcq("¿Qué número va justo antes de %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n // 10 * 10 - 1 + 10) if n % 10 == 0 else num(n - 2)], "Uno menos: <b>%s</b>." % num(n - 1))
        return mcq("¿Qué número va justo después de %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n // 10 * 10 + 100) if n % 10 == 9 and n + 100 <= TOP[LV] else num(n + 2)], "Uno más: <b>%s</b>." % num(n + 1))
    if k == "serie":
        step = R.choice({1: [2, 5, 10, 1, 3], 2: [2, 5, 10, 100, 50, 3, 4], 3: [10, 100, 1000, 50, 25, 200, 500]}[LV])
        a = R.randint(0, TOP[LV] // 2) // step * step + (R.randint(0, 9) if LV > 1 and step >= 10 else 0)
        xs = [a + i * step for i in range(5)]
        if xs[-1] > TOP[LV]:
            return None
        hole = R.randint(1, 4)
        shown = ", ".join("___" if i == hole else num(x) for i, x in enumerate(xs))
        return mcq("¿Qué número falta? %s" % shown, num(xs[hole]), [num(xs[hole] + 1), num(xs[hole] - 1), num(xs[hole] + step), num(xs[hole] + 10) if step != 10 else num(xs[hole] + 100)], "Va de %s en %s: <b>%s</b>." % (num(step), num(step), num(xs[hole])))
    step = {1: 1, 2: 10, 3: 100}[LV]
    lo = R.randint(0, TOP[LV] // (10 * step) - 1) * 10 * step
    x = lo + R.randint(1, 9) * step
    g = recta(lo, lo + 10 * step, step, marks=[(x, "?")], every=5 * step)
    return mcq(g + "¿Qué número está en «?»?", num(x), [num(x + step), num(x - step), num(lo + (x - lo) // step)], "Cada marca vale %s: <b>%s</b>." % (num(step), num(x)))


def s5_par():
    k = R.choice(["par", "pares", "decenas", "conceptos"])
    if k == "par":
        n = rn(2)
        ok = "par" if n % 2 == 0 else "impar"
        return mcq("¿El número %s es par o impar?" % num(n), ok, ["impar" if ok == "par" else "par", "ni par ni impar", "depende de la primera cifra"], "Termina en %d: es <b>%s</b>." % (n % 10, ok))
    if k == "pares":
        xs = sorted(R.sample(range(2, min(TOP[LV], 99)), 4))
        ev = [x for x in xs if x % 2 == 0]
        if len(ev) != 1:
            return None
        return mcq("¿Cuál de estos números es par: %s?" % ", ".join(map(str, xs)), str(ev[0]), [str(x) for x in xs if x != ev[0]], "Los pares terminan en 0, 2, 4, 6 u 8: <b>%d</b>." % ev[0])
    if k == "decenas":
        n = rn(10)
        return mcq("¿Cuántas decenas completas hay en %s?" % num(n), num(n // 10), [num(n % 10) if n % 10 != n // 10 else num(n // 10 + 1), num(n // 100) if n >= 100 else num(n), num(n // 10 + 1)], "%s = %s decenas y %d unidades: <b>%s</b>." % (num(n), num(n // 10), n % 10, num(n // 10)))
    items = {1: [("¿Cuántas unidades hay en una decena?", "10", ["100", "1", "5"]), ("¿Cuál es el mayor número de dos cifras?", "99", ["90", "100", "10"]), ("¿Cuál es el menor número de dos cifras?", "10", ["11", "1", "99"]),
                 ("10 decenas forman…", "una centena (100)", ["una decena", "99", "un millar"]), ("¿Qué número es 7 decenas?", "70", ["7", "17", "700"])],
             2: [("¿Cuántas unidades hay en una centena?", "100", ["10", "1000", "1"]), ("¿Cuántas decenas hay en una centena?", "10", ["100", "1", "20"]), ("¿Cuál es el mayor número de tres cifras?", "999", ["900", "1000", "99"]),
                 ("¿Cuál es el menor número de tres cifras?", "100", ["101", "999", "10"]), ("10 centenas forman…", "un millar (1000)", ["una decena", "una centena", "999"])],
             3: [("¿Cuántas unidades hay en una unidad de millar?", "1000", ["100", "10", "10 000"]), ("¿Cuántas centenas hay en un millar?", "10", ["100", "1000", "1"]), ("¿Cuál es el mayor número de cuatro cifras?", "9999", ["9000", "1000", "999"]),
                 ("¿Cuál es el menor número de cuatro cifras?", "1000", ["1001", "9999", "100"]), ("¿Cuántas decenas hay en 1000?", "100", ["10", "1000", "1"])]}[LV]
    q, a, w = R.choice(items)
    return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30001 + lv * 1000)
    seen = set()
    sets = [
        ("Contar y representar números", mix(R, seen, [(s1_contar, 20)])),
        ("Leer y escribir números", mix(R, seen, [(s2_letra, 20)])),
        ("Valor de las cifras", mix(R, seen, [(s3_valor, 20)])),
        ("Anterior, posterior y series", mix(R, seen, [(s4_series, 20)])),
        ("Pares, impares y decenas", mix(R, seen, [(s5_par, 20)])),
    ]
    ej = {1: ("Escribe «cuarenta y siete»", ["4 decenas = 40", "7 unidades"], "47"), 2: ("Escribe «trescientos siete»", ["3 centenas, 0 decenas, 7 unidades"], "307"),
          3: ("Escribe «cuatro mil sesenta»", ["4 UM, 0 C, 6 D, 0 U"], "4060")}[lv]
    think = {1: ["Contamos las <b>decenas</b> (grupos de 10) y las <b>unidades</b> sueltas: 3 decenas y 5 unidades = 35.", "En 35, el 3 vale 30 y el 5 vale 5."],
             2: ["10 unidades forman una <b>decena</b> y 10 decenas forman una <b>centena</b>.", "En 352, el 3 vale 300, el 5 vale 50 y el 2 vale 2. Si falta un orden, escribe 0: «trescientos siete» = 307."],
             3: ["10 centenas forman una <b>unidad de millar</b> (1000).", "En 4352, el 4 vale 4000, el 3 vale 300, el 5 vale 50 y el 2 vale 2. Si falta un orden, escribe 0: «cuatro mil sesenta» = 4060."]}[lv]
    body = lesson(think + ["Los números <b>pares</b> terminan en 0, 2, 4, 6 u 8; los <b>impares</b>, en 1, 3, 5, 7 o 9."],
                  [ej, ("¿Qué número va después de %s?" % {1: "39", 2: "299", 3: "3999"}[lv], ["Sumamos 1"], {1: "40", 2: "300", 3: "4000"}[lv])],
                  [["Olvidar el cero", "%s, no %s." % ({1: "40", 2: "307", 3: "4060"}[lv], {1: "4", 2: "37", 3: "460"}[lv])],
                   ["Confundir la cifra con su valor", "En %s, el %s vale %s." % ({1: "35", 2: "352", 3: "4352"}[lv], {1: "3", 2: "3", 3: "4"}[lv], {1: "30", 2: "300", 3: "4000"}[lv])],
                   ["Contar mal al cambiar de decena", "Después de %s va %s." % ({1: "29", 2: "199", 3: "2999"}[lv], {1: "30", 2: "200", 3: "3000"}[lv])]],
                  bloques(0, 3, 5, 2) if lv >= 2 else P.regletas(3, 5))
    faq = [("¿Cómo se escribe un número con un cero en medio?", "Se escribe un 0 en el lugar que no se nombra. «Trescientos siete» no tiene decenas: 307."),
           ("¿Cómo sé si un número es par?", "Mira la última cifra: si es 0, 2, 4, 6 u 8, el número es par.")]
    make_unit(R, SLUG[lv], "N",
              "Números naturales hasta %s: conteo, lectura, escritura, valor posicional, composición y descomposición, orden y series; números pares e impares" % num(TOP[lv]),
              "Los números hasta el %s" % num(TOP[lv]), "Números hasta el %s" % num(TOP[lv]),
              "Fichas de matemáticas de %d.º de Primaria: contar, leer y escribir números hasta el %s, valor de las cifras, anterior y posterior, series, pares e impares. 100 ejercicios con soluciones." % (lv, num(TOP[lv])),
              {1: "Decenas y unidades", 2: "Centenas, decenas y unidades", 3: "UM, C, D y U"}[lv], "Si falta un orden, escribe 0.",
              body, faq, sets, 1, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(3)
