# -*- coding: utf-8 -*-
"""
México 4.º grado de primaria: Números hasta 99 999 (Estudio de los números, Fase 4)
Leer y escribir números de hasta cinco cifras, valor posicional (DM, UM, C, D, U), descomposición, antes y después,
sucesiones y números ordinales hasta el vigésimo.
Errores: olvidar los ceros intermedios (treinta mil cuarenta = 30 040), confundir la cifra con su valor.
"""
import random
from mx_common import unit, mcq, num, mx_text, letra
import es_common as ES

R = random.Random(64101)
POS = ["unidades", "decenas", "centenas", "unidades de millar", "decenas de millar"]
ORD = ["primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo", "octavo", "noveno", "décimo",
       "undécimo", "duodécimo", "decimotercero", "decimocuarto", "decimoquinto", "decimosexto", "decimoséptimo", "decimoctavo", "decimonoveno", "vigésimo"]


def rn(zeros=True):
    n = R.randint(10000, 99999)
    if zeros and R.random() < 0.5:
        ds = list(str(n))
        for i in R.sample(range(1, 5), R.randint(1, 2)):
            ds[i] = "0"
        n = int("".join(ds))
    return n


def var(n):
    """el mismo número con una cifra cambiada (cero ↔ otra cifra)"""
    ds = list(str(n))
    i = R.randrange(1, len(ds))
    ds[i] = "0" if ds[i] != "0" else str(R.randint(1, 9))
    return int("".join(ds))


def s1_letra():
    n = rn()
    ws = set()
    for _ in range(12):
        ws.add(var(n))
    s = str(n)
    if "0" in s[1:]:
        ws.add(int(s.replace("0", "", 1)) if len(s.replace("0", "", 1)) >= 4 else n + 1)
    ws.discard(n)
    ws = sorted(ws)
    R.shuffle(ws)
    if R.random() < 0.5:
        return mcq("¿Cómo se escribe con cifras «%s»?" % letra(n), num(n), [num(w) for w in ws], "«%s» = <b>%s</b>." % (letra(n), num(n)))
    return mcq("¿Cómo se lee el número %s?" % num(n), letra(n), [letra(w) for w in ws], "%s se lee «<b>%s</b>»." % (num(n), letra(n)))


def s2_valor():
    n = rn(zeros=False)
    s = str(n)
    i = R.randrange(5)
    d = int(s[i])
    pos = 4 - i
    k = R.choice(["valor", "valor", "orden", "tabla"])
    if k == "valor":
        v = d * 10 ** pos
        alts = [str(d), num(d * 10 ** (pos + 1)), num(d * 10 ** (pos - 1)) if pos else num(d * 100), num(d * 10 ** (pos - 2)) if pos >= 2 else num(d * 1000)]
        return mcq("En el número %s, ¿cuánto vale la cifra %d de las %s?" % (num(n), d, POS[pos]), num(v), alts, "%d %s = <b>%s</b>." % (d, POS[pos], num(v)))
    if k == "orden":
        if s.count(str(d)) > 1:
            return None
        return mcq("En el número %s, ¿en qué lugar está la cifra %d?" % (num(n), d), "en las " + POS[pos], ["en las " + POS[p] for p in range(5) if p != pos],
                   "Contamos desde la derecha: U, D, C, UM, DM. El %d está en las <b>%s</b>." % (d, POS[pos]))
    return mcq(mx_text(ES.tabla_valor(n, 5)) + "¿Qué número está escrito en la tabla?", num(n), [num(int(s[::-1])) if s[-1] != "0" else num(n + 1), num(n // 10), num(var(n))],
               "Leemos la tabla de izquierda a derecha: <b>%s</b>." % num(n))


def s3_descomp():
    n = rn()
    s = str(n)
    parts = [int(c) * 10 ** (4 - i) for i, c in enumerate(s) if c != "0"]
    if len(parts) < 3:
        return None
    k = R.choice(["suma", "inversa", "ordenes"])
    if k == "suma":
        txt = " + ".join(num(p) for p in parts)
        sw = list(s)
        j = R.randrange(1, 4)
        sw[j], sw[j + 1] = sw[j + 1], sw[j]
        return mcq("¿Qué número es %s?" % txt, num(n), [num(int(s.replace("0", ""))), num(int("".join(sw))), num(n + 10 ** R.randint(1, 3)), num(var(n))],
                   "Sumamos los valores: <b>%s</b>." % num(n))
    if k == "inversa":
        txt = " + ".join(num(p) for p in parts)
        w1 = " + ".join(c for c in s if c != "0")
        w2 = " + ".join(num(p // 10 if i == 0 else p) for i, p in enumerate(parts))
        w3 = " + ".join(num(p * 10 if i == len(parts) - 1 else p) for i, p in enumerate(parts))
        return mcq("¿Cuál es la descomposición de %s?" % num(n), txt, [w1, w2, w3], "Cada cifra por su valor: <b>%s</b>." % txt)
    dm, r = divmod(n, 10000)
    um, r = divmod(r, 1000)
    c, r = divmod(r, 100)
    d, u = divmod(r, 10)
    txt = "%d DM, %d UM, %d C, %d D y %d U" % (dm, um, c, d, u)
    return mcq("¿Qué número tiene %s?" % txt, num(n), [num(int(s[::-1])) if s[-1] != "0" else num(n + 2), num(n + 1000) if um < 9 else num(n - 1000), num(n + 10) if d < 9 else num(n - 10)],
               "%d × 10 000 + %d × 1 000 + %d × 100 + %d × 10 + %d = <b>%s</b>." % (dm, um, c, d, u, num(n)))


def s4_series():
    k = R.choice(["ant", "post", "post", "serie", "serie", "recta"])
    n = rn()
    if k == "ant":
        n = R.choice([n, n // 1000 * 1000, n // 100 * 100])
        return mcq("¿Qué número va justo antes de %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 1000)], "Uno menos: <b>%s</b>." % num(n - 1))
    if k == "post":
        n = R.choice([19999, 39999, 49999, 29999, 59999, 70999, 45999, 80099]) if R.random() < 0.5 else n
        return mcq("¿Qué número va justo después de %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 1000) if n + 1000 < 10 ** 5 else num(n + 100)], "Uno más: <b>%s</b>." % num(n + 1))
    if k == "serie":
        step = R.choice([1000, 10000, 100, 500, 2000, 5000])
        a = R.randint(1, 40) * 1000 + R.randint(0, 9) * 100
        if a + 5 * step >= 10 ** 5:
            return None
        xs = [a + i * step for i in range(4)]
        up = R.random() < 0.7
        if not up:
            xs = xs[::-1]
            ans = a - step
            if ans < 0:
                return None
            return mcq("Continúa la sucesión: %s, …" % ", ".join(num(x) for x in xs), num(ans), [num(a + 4 * step), num(a - step * 10) if a - step * 10 > 0 else num(a - step + 10), num(a - step // 10 if step >= 1000 else a - 10)],
                       "Baja de %s en %s: <b>%s</b>." % (num(step), num(step), num(ans)))
        ans = a + 4 * step
        return mcq("Continúa la sucesión: %s, …" % ", ".join(num(x) for x in xs), num(ans), [num(ans + step // 10 if step >= 1000 else ans + 10), num(a + 5 * step), num(a + 3 * step + step * 10)],
                   "Sube de %s en %s: <b>%s</b>." % (num(step), num(step), num(ans)))
    lo = R.randint(1, 8) * 10000
    step = 1000
    x = lo + R.randint(1, 9) * step
    g = mx_text(ES.recta(lo, lo + 10 * step, step, marks=[(x, "?")], every=5 * step))
    return mcq(g + "¿Qué número va en el lugar de «?»?", num(x), [num(x + step), num(x - step), num(lo + (x - lo) // 10)], "Cada marca vale %s: <b>%s</b>." % (num(step), num(x)))


FILA = [("La fila de las tortillas", "personas"), ("La carrera del festival", "corredores"), ("La fila para entrar al museo", "visitantes"), ("La fila de la cooperativa", "niños")]


def s5_ordinales():
    k = R.choice(["leer", "leer", "lugar", "antes", "despues"])
    n = R.randint(1, 20)
    if k == "leer":
        w = [ORD[j] for j in (n - 2, n, n + 9, n - 11) if 0 <= j < 20 and j != n - 1]
        w += [ORD[j] for j in range(20) if j != n - 1 and ORD[j] not in w][:3]
        return mcq("¿Cómo se lee el ordinal %d.º?" % n, ORD[n - 1], w, "%d.º se lee «<b>%s</b>»." % (n, ORD[n - 1]))
    if k == "lugar":
        if n < 2:
            return None
        fila, gente = R.choice(FILA)
        tot = R.randint(n + 1, 25) if n < 20 else 25
        return mcq("%s tiene %d %s. Delante de Iván hay %d. ¿En qué lugar está Iván?" % (fila, tot, gente, n - 1), ORD[n - 1],
                   [ORD[j] for j in (n - 2, n, n + 1) if 0 <= j < 20 and j != n - 1] + ["vigésimo" if n != 20 else "decimoctavo"],
                   "Hay %d delante, así que Iván es el %d.º: <b>%s</b>." % (n - 1, n, ORD[n - 1]))
    if k == "antes":
        if n == 1:
            return None
        return mcq("¿Qué lugar va justo antes del %s?" % ORD[n - 1], ORD[n - 2], [ORD[j] for j in (n, n - 3, n + 1, n - 4) if 0 <= j < 20 and j != n - 2], "%d − 1 = %d: <b>%s</b>." % (n, n - 1, ORD[n - 2]))
    if n == 20:
        return None
    return mcq("¿Qué lugar va justo después del %s?" % ORD[n - 1], ORD[n], [ORD[j] for j in (n - 2, n + 1, n - 3, n + 2) if 0 <= j < 20], "%d + 1 = %d: <b>%s</b>." % (n, n + 1, ORD[n]))


unit("numeros-hasta-99999", 1, "N",
     "Lee, escribe y ordena números naturales de hasta cinco cifras; valor posicional de unidades, decenas, centenas, unidades y decenas de millar; descomposición; sucesiones; números ordinales hasta el vigésimo",
     "Los números hasta el 99 999", "Números hasta el 99 999",
     "Ejercicios de matemáticas de 4.º grado de primaria: leer y escribir números de cinco cifras, valor posicional, descomposición, sucesiones y números ordinales. 100 ejercicios con respuestas.",
     "DM, UM, C, D y U", "Si falta un orden, escribe 0.",
     ["10 unidades de millar forman una <b>decena de millar</b> (10 000).",
      "En 47 352, el 4 vale 40 000, el 7 vale 7 000, el 3 vale 300, el 5 vale 50 y el 2 vale 2.",
      "Si un orden no se nombra, escribe 0: «treinta mil cuarenta» = 30 040.",
      "Los <b>ordinales</b> dicen el lugar: primero, segundo, …, décimo, undécimo, duodécimo, …, vigésimo."],
     [("Escribe «sesenta y dos mil ocho»", ["6 DM, 2 UM, 0 C, 0 D, 8 U"], "62 008"), ("¿Qué número va después de 39 999?", ["Sumamos 1"], "40 000")],
     [["Olvidar los ceros", "30 040, no 3 040."], ["Confundir la cifra con su valor", "En 47 352, el 4 vale 40 000."], ["Contar mal al cambiar de millar", "Después de 39 999 va 40 000."]],
     [("¿Cómo se lee un número de cinco cifras?", "Primero los millares y después el resto: 47 352 se lee «cuarenta y siete mil trescientos cincuenta y dos»."),
      ("¿Cómo se dice el lugar número 12?", "Duodécimo. El 11 es undécimo y el 20, vigésimo.")],
     [("Leer y escribir números", [(s1_letra, 20)]), ("Valor de las cifras", [(s2_valor, 20)]), ("Descomponer números", [(s3_descomp, 20)]),
      ("Antes, después y sucesiones", [(s4_series, 20)]), ("Números ordinales", [(s5_ordinales, 20)])],
     64001, pic=mx_text(ES.tabla_valor(47352, 5)), lv=4)
