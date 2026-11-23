# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Suma y resta de decimales (Sentido numérico)
Sumar y restar números decimales hasta las centésimas colocando las comas en columna, completar con ceros,
cálculo mental con décimas, sumar y restar euros y metros, problemas de compras.
Errores: alinear los números por la derecha y no por la coma, olvidar poner la coma en el resultado.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, dz, eur, Kids

R = random.Random(44013)
K = Kids(R)


def wrong_align(a, pa, b, pb):
    """error: alinear por la derecha (2,5 + 1,25 → 1,50)"""
    x = a * (10 ** (2 - pa))
    y = b * (10 ** (2 - pb))
    if pa != pb:
        return dz(a + b, max(pa, pb), keep=True)
    return None


def s1_suma():
    pa, pb = R.choice([(1, 1), (2, 2), (1, 2), (2, 1)])
    a = R.randint(11, 999) if pa == 1 else R.randint(101, 9999)
    b = R.randint(11, 999) if pb == 1 else R.randint(101, 9999)
    A, B = a * 10 ** (2 - pa), b * 10 ** (2 - pb)
    s = A + B
    w = wrong_align(a, pa, b, pb)
    return mcq("Calcula: %s + %s" % (dz(a, pa), dz(b, pb)), dz(s, 2), [w, dz(s + 10, 2), dz(s - 1, 2), num(a + b) if pa == pb else dz(s + 100, 2), dz(s * 10, 2)],
               "Colocamos coma debajo de coma%s: <b>%s</b>." % (" (añadimos un 0: %s = %s)" % (dz(a if pa == 1 else b, 1), dz((a if pa == 1 else b) * 10, 2, keep=True)) if pa != pb else "", dz(s, 2)))


def s2_resta():
    pa, pb = R.choice([(1, 1), (2, 2), (1, 2), (2, 1), (0, 1), (0, 2)])
    a = R.randint(2, 99) if pa == 0 else R.randint(21, 999) if pa == 1 else R.randint(201, 9999)
    A = a * 10 ** (2 - pa)
    B = R.randint(1, A - 1)
    if pb == 1:
        B = B // 10 * 10 or 10
    if B >= A:
        return None
    b = B // 10 ** (2 - pb)
    r = A - B
    w = dz(abs(a - b), max(pa, pb)) if pa != pb else None
    return mcq("Calcula: %s − %s" % (dz(a, pa), dz(b, pb)), dz(r, 2), [w, dz(r + 10, 2), dz(r + 1, 2), dz(r - 100, 2) if r > 100 else dz(r + 100, 2), dz(r * 10, 2)],
               "Coma debajo de coma%s: <b>%s</b>." % (" y completamos con ceros: %s = %s" % (dz(a, pa), dz(A, 2, keep=True)) if pa < 2 else "", dz(r, 2)))


def s3_mental():
    k = R.choice(["+0,1", "-0,1", "+0,01", "+1", "completar1", "completar10"])
    c = R.randint(101, 9899)
    if k == "+0,1":
        return mcq("Calcula mentalmente: %s + 0,1" % dz(c, 2), dz(c + 10, 2), [dz(c + 1, 2), dz(c + 100, 2), dz(c, 2) + "1", dz(c + 11, 2)], "Sumamos una décima: <b>%s</b>." % dz(c + 10, 2))
    if k == "-0,1":
        return mcq("Calcula mentalmente: %s − 0,1" % dz(c, 2), dz(c - 10, 2), [dz(c - 1, 2), dz(c - 100, 2), dz(c + 10, 2), dz(c - 11, 2)], "Restamos una décima: <b>%s</b>." % dz(c - 10, 2))
    if k == "+0,01":
        return mcq("Calcula mentalmente: %s + 0,01" % dz(c, 2), dz(c + 1, 2), [dz(c + 10, 2), dz(c + 100, 2), dz(c + 11, 2), dz(c - 1, 2)], "Sumamos una centésima: <b>%s</b>." % dz(c + 1, 2))
    if k == "+1":
        return mcq("Calcula mentalmente: %s + 1" % dz(c, 2), dz(c + 100, 2), [dz(c + 10, 2), dz(c + 1, 2), dz(c + 110, 2), dz(c + 1000, 2)], "Sumamos una unidad: <b>%s</b>." % dz(c + 100, 2))
    if k == "completar1":
        c = R.randint(1, 99)
        if c % 10 == 0 and R.random() < 0.5:
            return None
        return mcq("¿Cuánto le falta a %s para llegar a 1?" % dz(c, 2), dz(100 - c, 2), [dz(10 - c % 10 if c % 10 else 10, 2) if c > 10 else dz(100 - c + 10, 2), dz(1000 - c * 10, 2) if c < 100 else None, dz(99 - c, 2) if c < 99 else dz(2, 2), dz(100 - c + 1, 2)],
                   "%s + %s = 1: <b>%s</b>." % (dz(c, 2), dz(100 - c, 2), dz(100 - c, 2)))
    c = R.randint(10, 99)
    return mcq("¿Cuánto le falta a %s para llegar a 10?" % dz(c, 1), dz(100 - c, 1), [dz(100 - c + 10, 1), dz(99 - c, 1), dz(100 - c - 10, 1) if c < 90 else dz(100 - c + 1, 1), dz(1000 - c, 1)],
               "%s + %s = 10: <b>%s</b>." % (dz(c, 1), dz(100 - c, 1), dz(100 - c, 1)))


def s4_euros():
    k = R.choice(["suma", "cambio", "dos"])
    p, g = K.next()
    if k == "suma":
        a, b = R.randint(105, 1999), R.randint(105, 1999)
        return mcq("Calcula: %s + %s" % (eur(a), eur(b)), eur(a + b), [eur(a + b - 100), eur(a + b + 10), eur(a + b + 100), eur(a + b - 1)], "<b>%s</b>." % eur(a + b))
    if k == "cambio":
        m = R.choice([500, 1000, 2000, 5000])
        a = R.randint(105, m - 5)
        return mcq("Algo cuesta %s y pagas con %s. ¿Cuánto te devuelven?" % (eur(a), eur(m)), eur(m - a), [eur(m - a + 100), eur(m - a - 10) if m - a > 10 else eur(m - a + 10), eur(m - a + 1), eur(abs(m // 100 - a // 100) * 100 + abs(a % 100))],
                   "%s − %s = <b>%s</b>." % (eur(m), eur(a), eur(m - a)))
    a, b = R.randint(105, 1999), R.randint(105, 1999)
    if a == b:
        return None
    return mcq("Un juego cuesta %s y un puzle %s. ¿Cuánto más caro es el %s?" % (eur(a), eur(b), "juego" if a > b else "puzle"), eur(abs(a - b)), [eur(a + b), eur(abs(a - b) + 100), eur(abs(a - b) + 10), eur(abs(a - b) - 1) if abs(a - b) > 1 else eur(abs(a - b) + 2)],
               "%s − %s = <b>%s</b>." % (eur(max(a, b)), eur(min(a, b)), eur(abs(a - b))))


def s5_problema():
    p, g = K.next()
    k = R.choice(["compra", "metros", "litros", "kilos", "salto", "ahorro"])
    if k == "compra":
        it = R.sample([("un cuaderno", 245), ("un lápiz", 75), ("una goma", 60), ("un rotulador", 135), ("una regla", 180), ("un sacapuntas", 95), ("unas tijeras", 320)], 3)
        tot = sum(c for _, c in it)
        m = 1000 if tot < 1000 else 2000
        return mcq("%s compra %s (%s), %s (%s) y %s (%s). Paga con %s. ¿Cuánto le devuelven?" % (p, it[0][0], eur(it[0][1]), it[1][0], eur(it[1][1]), it[2][0], eur(it[2][1]), eur(m)),
                   eur(m - tot), [eur(tot), eur(m - tot + 100), eur(m - it[0][1] - it[1][1]), eur(m - tot - 10)],
                   "%s + %s + %s = %s; %s − %s = <b>%s</b>." % (eur(it[0][1]), eur(it[1][1]), eur(it[2][1]), eur(tot), eur(m), eur(tot), eur(m - tot)))
    if k == "metros":
        a, b = R.randint(105, 450), R.randint(105, 450)
        return mcq("%s tiene una cuerda de %s m y otra de %s m. Las ata (sin perder longitud). ¿Cuánto mide la cuerda entera?" % (p, dz(a, 2), dz(b, 2)), "%s m" % dz(a + b, 2), ["%s m" % dz(abs(a - b), 2), "%s m" % dz(a + b + 10, 2), "%s m" % dz(a + b, 1), "%s m" % dz(a + b - 100, 2)],
                   "%s + %s = <b>%s m</b>." % (dz(a, 2), dz(b, 2), dz(a + b, 2)))
    if k == "litros":
        t = R.choice([5, 8, 10])
        a = R.randint(11, t * 10 - 5)
        return mcq("Un bidón tiene %d L de agua. Se gastan %s L. ¿Cuántos litros quedan?" % (t, dz(a, 1)), "%s L" % dz(t * 10 - a, 1), ["%s L" % dz(t * 10 + a, 1), "%s L" % dz(t * 10 - a + 10, 1), "%s L" % dz(abs(t - a), 0) if abs(t - a) else "%s L" % dz(t * 10 - a - 1, 1), "%s L" % dz(t * 10 - a - 10, 1)],
                   "%d = %s; %s − %s = <b>%s L</b>." % (t, dz(t * 10, 1, keep=True), dz(t * 10, 1, keep=True), dz(a, 1), dz(t * 10 - a, 1)))
    if k == "kilos":
        a, b = R.randint(105, 399), R.randint(105, 399)
        return mcq("En la frutería, %s compra %s kg de naranjas y %s kg de manzanas. ¿Cuántos kilos lleva?" % (p, dz(a, 2), dz(b, 2)), "%s kg" % dz(a + b, 2), ["%s kg" % dz(abs(a - b), 2), "%s kg" % dz(a + b + 100, 2), "%s kg" % dz(a + b - 10, 2), "%s kg" % dz(a + b + 1, 2)],
                   "%s + %s = <b>%s kg</b>." % (dz(a, 2), dz(b, 2), dz(a + b, 2)))
    if k == "salto":
        a = R.randint(250, 420)
        b = R.randint(5, 60)
        return mcq("%s saltó %s m. Su amiga saltó %s m más. ¿Cuánto saltó su amiga?" % (p, dz(a, 2), dz(b, 2)), "%s m" % dz(a + b, 2), ["%s m" % dz(a - b, 2), "%s m" % dz(a + b * 10, 2), "%s m" % dz(a + b + 100, 2), "%s m" % dz(a + b - 1, 2)],
                   "%s + %s = <b>%s m</b>." % (dz(a, 2), dz(b, 2), dz(a + b, 2)))
    a, b = R.randint(500, 2500), R.randint(105, 499)
    return mcq("%s tenía %s en la hucha. Se gastó %s. ¿Cuánto le queda?" % (p, eur(a), eur(b)), eur(a - b), [eur(a + b), eur(a - b + 100), eur(a - b - 10), eur(a - b + 1)],
               "%s − %s = <b>%s</b>." % (eur(a), eur(b), eur(a - b)))


def main():
    seen = set()
    sets = [
        ("Sumar decimales", mix(R, seen, [(s1_suma, 20)])),
        ("Restar decimales", mix(R, seen, [(s2_resta, 20)])),
        ("Cálculo mental con decimales", mix(R, seen, [(s3_mental, 20)])),
        ("Sumar y restar euros", mix(R, seen, [(s4_euros, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para sumar o restar decimales, coloca los números con <b>coma debajo de coma</b>: unidades con unidades, décimas con décimas, centésimas con centésimas.",
         "Si un número tiene menos cifras decimales, añade <b>ceros</b> a la derecha: 4,5 = 4,50; 7 = 7,00.",
         "Suma o resta como con números naturales y pon la <b>coma</b> en el resultado, debajo de las otras comas."],
        [("4,5 + 2,38", ["4,50 + 2,38", "450 + 238 = 688 centésimas"], "6,88"),
         ("10 − 3,25", ["10,00 − 3,25"], "6,75")],
        [["Alinear por la derecha", "En 4,5 + 2,38 el 5 son décimas: va debajo del 3, no del 8."],
         ["Olvidar la coma", "El resultado de 4,5 + 2,38 es 6,88, no 688."],
         ["Restar mal al completar con ceros", "10 − 3,25: escribe 10,00 y pide prestado."]])
    faq = [("¿Cómo se suman números decimales?", "Se colocan en columna con la coma debajo de la coma, se completan con ceros si hace falta y se suman como números naturales; la coma del resultado va debajo de las otras."),
           ("¿Por qué se pueden añadir ceros a la derecha de un decimal?", "Porque no cambian su valor: 4,5 y 4,50 son el mismo número (5 décimas = 50 centésimas).")]
    make_unit(R, "suma-y-resta-de-decimales", "N",
              "Suma y resta de números decimales hasta las centésimas; cálculo mental con decimales; resolución de problemas de dinero y medida",
              "Suma y resta de números decimales", "Suma y resta de decimales",
              "Fichas de matemáticas de 4.º de Primaria: sumar y restar decimales con la coma en columna, cálculo mental con décimas y centésimas, euros y problemas. 100 ejercicios con soluciones.",
              "Coma debajo de coma", "Completa con ceros: 4,5 = 4,50.",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
