# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Números romanos (Sentido numérico)
Las siete letras (I, V, X, L, C, D, M), reglas de suma y resta, leer y escribir números romanos hasta 3999,
usos en la vida diaria (siglos, capítulos, reyes, relojes).
Errores: escribir IIII o VV, restar letras que no se pueden restar (IC, VX), leer de derecha a izquierda.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, bank

R = random.Random(44003)
VAL = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
LET = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def rom(n):
    s = ""
    for v, r in VAL:
        while n >= v:
            s += r
            n -= v
    return s


def naive(n):
    """error frecuente: sin restas (4 = IIII, 9 = VIIII)"""
    s = ""
    for v, r in [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]:
        while n >= v:
            s += r
            n -= v
    return s


def wrong_val(r):
    """leer sumando todo (IX = 11)"""
    return sum(LET[c] for c in r)


def rnd(hi):
    k = R.random()
    if k < 0.4:
        return R.choice([4, 9, 14, 19, 24, 29, 39, 40, 44, 49, 90, 94, 99, 140, 190, 400, 440, 490, 900, 940, 990, 1400, 1900, 1994, 2024, 1492, 1808, 1979, 2026, 1936, 1898, 1714])
    return R.randint(1, hi)


def s1_letras():
    k = R.choice(list(LET))
    vals = sorted(LET.values())
    return mcq("¿Cuánto vale la letra romana %s?" % k, num(LET[k]), [num(v) for v in vals if v != LET[k]][::-1][:6] if R.random() < 0.5 else [num(v) for v in vals if v != LET[k]],
               "%s = <b>%s</b>." % (k, num(LET[k])))


def s1_leer():
    n = rnd(40)
    if n > 40:
        n = R.randint(1, 40)
    r = rom(n)
    return mcq("¿Qué número es %s?" % r, num(n), [num(wrong_val(r)) if wrong_val(r) != n else None, num(n + 1), num(n - 1) if n > 1 else None, num(n + 10), num(n + 2)],
               "%s = <b>%s</b>." % (r, num(n)))


def s2_leer():
    n = rnd(3999)
    if n < 40:
        return None
    r = rom(n)
    alts = [wrong_val(r), n + 10, n - 10, n + 100, n + 1, n - 1]
    return mcq("¿Qué número es %s?" % r, num(n), [num(x) for x in alts if x != n and x > 0],
               "%s = <b>%s</b>." % (" + ".join(rom(v) if v not in (900, 400, 90, 40, 9, 4) else rom(v) for v in parts(n)) + " → " + " + ".join(num(v) for v in parts(n)), num(n)))


def parts(n):
    out = []
    for v, r in VAL:
        c = 0
        while n >= v:
            n -= v
            c += v
        if c:
            out.append(c)
    return out


def s3_escribir():
    n = rnd(3999)
    r = rom(n)
    w = {naive(n), rom(n + 1), rom(n - 1) if n > 1 else None, rom(n + 10), rom(n - 10) if n > 10 else None, rom(n + 100)}
    w.discard(r)
    w.discard(None)
    ws = sorted(w)
    R.shuffle(ws)
    return mcq("¿Cómo se escribe %s en números romanos?" % num(n), r, ws,
               "%s = %s → <b>%s</b>." % (num(n), " + ".join(num(v) for v in parts(n)), r))


def s4_reglas():
    k = R.choice(["valido", "valido", "comparar", "mayor"])
    if k == "valido":
        n = rnd(999)
        r = rom(n)
        bad = []
        if "IV" in r or "IX" in r or "XL" in r or "XC" in r or "CD" in r or "CM" in r:
            bad.append(naive(n))
        for a, b in [("IX", "VIV"), ("XC", "LXL"), ("CM", "DCD")]:
            if a in r:
                bad.append(r.replace(a, b, 1))
        if n % 10 == 9 and n >= 10:
            bad.append(rom(n - 9) + "IX".replace("IX", "IX")[:0] + "VIIII")
        bad += ["IC" if n == 99 else None, "VX" if n == 5 else None, "IIII" if n == 4 else None, "XXXX" if n // 10 % 10 == 4 else None, "VV" if n == 10 else None, "LL" if n == 100 else None, "IL" if n == 49 else None, "XM" if n == 990 else None]
        bad = [b for b in bad if b and b != r]
        if len(bad) < 1:
            return None
        bad = sorted(set(bad))
        R.shuffle(bad)
        return mcq("¿Cuál es la forma correcta de escribir %s en números romanos?" % num(n), r, bad + [rom(n + 1), rom(n - 1) if n > 1 else rom(n + 2), rom(n + 5)],
                   "Una letra no se repite más de tres veces y solo se resta I, X o C delante de las dos letras siguientes: <b>%s</b>." % r)
    a, b = R.sample(range(10, 3999), 2)
    if k == "comparar":
        ok = "%s %s %s" % (rom(a), "&lt;" if a < b else "&gt;", rom(b))
        return mcq("Compara %s y %s. ¿Qué es correcto?" % (rom(a), rom(b)), ok, ["%s %s %s" % (rom(a), "&gt;" if a < b else "&lt;", rom(b)), "%s = %s" % (rom(a), rom(b)), "no se pueden comparar"],
                   "%s = %s y %s = %s: <b>%s</b>." % (rom(a), num(a), rom(b), num(b), ok))
    xs = sorted({R.randint(10, 3999) for _ in range(4)})
    if len(xs) < 4:
        return None
    rs = [rom(x) for x in xs]
    R.shuffle(rs)
    m = rom(max(xs))
    return mcq("¿Cuál es el número mayor? %s" % ", ".join(rs), m, rs, "%s = %s es el mayor." % (m, num(max(xs))))


SIGLOS = [(1492, "XV"), (1605, "XVII"), (1808, "XIX"), (1936, "XX"), (2026, "XXI"), (1212, "XIII"), (711, "VIII"), (1750, "XVIII"), (1520, "XVI"), (1085, "XI"), (1137, "XII"), (1348, "XIV")]
REYES = [("Felipe VI", 6), ("Carlos III", 3), ("Felipe II", 2), ("Alfonso XIII", 13), ("Fernando VII", 7), ("Isabel II", 2), ("Carlos IV", 4), ("Felipe V", 5), ("Alfonso XII", 12), ("Alfonso X", 10)]


def s5_vida():
    k = R.choice(["siglo", "siglo2", "rey", "capitulo", "reloj", "edificio", "olimpiada"])
    if k == "siglo":
        y, s = R.choice(SIGLOS)
        n = (y - 1) // 100 + 1
        return mcq("El año %s pertenece a un siglo. ¿Cómo se escribe ese siglo en números romanos?" % y, "siglo %s" % s,
                   ["siglo %s" % rom(n - 1), "siglo %s" % rom(n + 1), "siglo %s" % naive(n) if naive(n) != s else "siglo %s" % rom(y // 100)],
                   "Del año %d01 al %d00 es el siglo %s: <b>siglo %s</b>." % (n - 1, n, num(n), s))
    if k == "siglo2":
        n = R.randint(5, 21)
        return mcq("¿Qué número es el siglo %s?" % rom(n), num(n), [num(wrong_val(rom(n))) if wrong_val(rom(n)) != n else num(n + 2), num(n + 1), num(n - 1), num(n + 10)], "%s = <b>%s</b>." % (rom(n), num(n)))
    if k == "rey":
        nm, n = R.choice(REYES)
        r = nm.split()[1]
        return mcq("En la historia de España hubo un rey llamado %s. ¿Qué número va detrás de su nombre?" % nm, num(n), [num(wrong_val(r)) if wrong_val(r) != n else num(n + 2), num(n + 1), num(n - 1) if n > 1 else num(n + 3), num(n + 10)],
                   "%s = <b>%s</b>." % (r, num(n)))
    if k == "capitulo":
        n = R.randint(11, 49)
        return mcq("Un libro empieza el capítulo %s. ¿Cuál es el siguiente capítulo?" % rom(n), rom(n + 1), [rom(n - 1), naive(n + 1) if naive(n + 1) != rom(n + 1) else rom(n + 2), rom(n + 10), rom(n) + "I" if rom(n) + "I" != rom(n + 1) else rom(n + 5)],
                   "%s = %s, el siguiente es %s = <b>%s</b>." % (rom(n), num(n), num(n + 1), rom(n + 1)))
    if k == "reloj":
        h = R.randint(1, 12)
        return mcq("En la esfera de un reloj antiguo las horas están en números romanos. ¿Qué hora indica el número %s?" % rom(h), "las %s" % h if h > 1 else "la 1",
                   ["las %s" % x for x in sorted({wrong_val(rom(h)), h + 1, h - 1, h + 2} - {h, 0, 1}, key=lambda _: R.random())] + ["la 1"],
                   "%s = <b>%s</b>." % (rom(h), h))
    if k == "edificio":
        y = R.choice([1882, 1929, 1888, 1992, 1749, 1785, 1563, 1616, 1907, 1964])
        return mcq("En la fachada de un edificio pone %s. ¿En qué año se construyó?" % rom(y),
                   str(y), [str(y + 10), str(y - 10), str(y + 100), str(wrong_val(rom(y)))], "%s = <b>%s</b>." % (rom(y), y))
    n = R.randint(20, 35)
    return mcq("Unos juegos se celebran por %s.ª vez. ¿Cómo se escribe ese número en romanos?" % n, rom(n), [naive(n) if naive(n) != rom(n) else rom(n + 2), rom(n + 1), rom(n - 1), rom(n + 10)],
               "%s = <b>%s</b>." % (n, rom(n)))


def main():
    seen = set()
    sets = [
        ("Las letras y los números hasta 40", mix(R, seen, [(s1_letras, 7), (s1_leer, 13)])),
        ("Leer números romanos", mix(R, seen, [(s2_leer, 20)])),
        ("Escribir números romanos", mix(R, seen, [(s3_escribir, 20)])),
        ("Reglas y comparación", mix(R, seen, [(s4_reglas, 20)])),
        ("Números romanos en la vida diaria", mix(R, seen, [(s5_vida, 20)])),
    ]
    body = lesson(
        ["Los romanos usaban siete letras: <b>I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000</b>.",
         "Una letra a la derecha de otra igual o mayor <b>suma</b>: VI = 6, XX = 20, CL = 150.",
         "I, X o C a la izquierda de una de las dos letras siguientes <b>resta</b>: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900.",
         "I, X, C y M se pueden repetir hasta tres veces; V, L y D nunca se repiten."],
        [("Escribe 1994", ["1000 + 900 + 90 + 4", "M + CM + XC + IV"], "MCMXCIV"),
         ("Lee CDXLVII", ["CD = 400, XL = 40, VII = 7"], "447")],
        [["Escribir IIII o XXXX", "4 = IV y 40 = XL."],
         ["Restar cualquier letra", "IC no existe: 99 = XCIX."],
         ["Sumar todas las letras", "IX no es 11: la I resta, IX = 9."]])
    faq = [("¿Cómo se escriben los siglos?", "En España los siglos se escriben con números romanos: el año 2026 está en el siglo XXI, y el año 1492, en el siglo XV."),
           ("¿Cuál es el número más grande que se escribe con estas reglas?", "Con las siete letras y las reglas de la escuela se llega hasta 3999 = MMMCMXCIX.")]
    make_unit(R, "numeros-romanos", "N",
              "El sistema de numeración romano: lectura y escritura de números romanos; reglas de suma y resta; uso en la vida cotidiana",
              "Números romanos", "Números romanos",
              "Fichas de matemáticas de 4.º de Primaria: números romanos. Valor de I, V, X, L, C, D y M, leer y escribir números romanos, reglas y siglos. 100 ejercicios con soluciones.",
              "I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000", "Delante de una letra mayor resta (IV = 4); detrás, suma (VI = 6).",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
