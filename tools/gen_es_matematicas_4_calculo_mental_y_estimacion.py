# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Cálculo mental y estimación (Sentido numérico)
Sumar y restar decenas, centenas y millares; descomponer para sumar; sumar 9, 99, 999; dobles y mitades;
multiplicar por 10, 100 y 1000; estimar sumas, restas y productos redondeando.
Errores: añadir el cero en el orden equivocado, estimar con el número exacto en vez de redondear.
"""
import random
from es_common import mcq, mix, lesson, make_unit, num, POR, bank, Kids

R = random.Random(44005)
K = Kids(R)


def rd(n, p):
    return (n + p // 2) // p * p


def s1_redondos():
    k = R.choice(["+1000", "-1000", "+100", "-100", "+10000", "-10000"])
    p = int(k[1:])
    n = R.randint(10000, 899999)
    m = R.randint(1, 9) * p
    if k[0] == "+":
        r = n + m
        txt = "%s + %s" % (num(n), num(m))
    else:
        if m >= n:
            return None
        r = n - m
        txt = "%s − %s" % (num(n), num(m))
    return mcq("Calcula mentalmente: %s" % txt, num(r), [num(n + m // 10 if k[0] == "+" else n - m // 10), num(n + m * 10 if k[0] == "+" else n - m * 10) if (n - m * 10) > 0 else num(r + 1), num(r + p), num(r - p)],
               "Solo cambia la cifra de las %s: <b>%s</b>." % ({10: "decenas", 100: "centenas", 1000: "unidades de millar", 10000: "decenas de millar"}[p], num(r)))


def s1_casi():
    k = R.choice(["9", "99", "999", "-9", "-99", "-999"])
    v = int(k.strip("-"))
    n = R.randint(100, 9999) if v < 999 else R.randint(2000, 99999)
    if k[0] == "-":
        r = n - v
        return mcq("Calcula mentalmente: %s − %s" % (num(n), num(v)), num(r), [num(n - v - 1 - 1), num(n - v - 1 + 1 + 1), num(n - (v + 1)), num(n - v + 10)],
                   "Restar %s es restar %s y sumar 1: %s − %s + 1 = <b>%s</b>." % (num(v), num(v + 1), num(n), num(v + 1), num(r)))
    r = n + v
    return mcq("Calcula mentalmente: %s + %s" % (num(n), num(v)), num(r), [num(n + v + 1 + 1), num(n + v + 1), num(n + v - 10), num(n + v + 10)],
               "Sumar %s es sumar %s y restar 1: %s + %s − 1 = <b>%s</b>." % (num(v), num(v + 1), num(n), num(v + 1), num(r)))


def s2_dobles():
    k = R.choice(["doble", "mitad", "doble", "mitad", "x10"])
    if k == "doble":
        n = R.choice([R.randint(11, 99) * 10, R.randint(11, 499), R.randint(11, 99) * 100 + R.choice([0, 50])])
        return mcq("¿Cuál es el doble de %s?" % num(n), num(2 * n), [num(n // 2) if n % 2 == 0 else num(n + 2), num(2 * n + 10), num(2 * n - 10), num(n + 2)],
                   "El doble es %s + %s = <b>%s</b>." % (num(n), num(n), num(2 * n)))
    if k == "mitad":
        n = 2 * R.choice([R.randint(11, 99) * 10, R.randint(11, 499), R.randint(6, 99) * 100 + R.choice([0, 50])])
        return mcq("¿Cuál es la mitad de %s?" % num(n), num(n // 2), [num(2 * n), num(n // 2 + 10), num(n // 2 - 10), num(n - 2)],
                   "La mitad es %s : 2 = <b>%s</b>." % (num(n), num(n // 2)))
    a = R.randint(2, 99)
    m = R.choice([10, 100, 1000])
    return mcq("Calcula mentalmente: %d %s %s" % (a, POR, num(m)), num(a * m), [num(a * m // 10), num(a * m * 10), num(a + m)],
               "Multiplicar por %s es añadir %s cero%s: <b>%s</b>." % (num(m), {10: "un", 100: "dos", 1000: "tres"}[m], "" if m == 10 else "s", num(a * m)))


def s2_descomponer():
    a = R.randint(21, 99) * 100 + R.randint(1, 9) * 10
    b = R.randint(11, 59) * 100 + R.randint(1, 9) * 10
    if (a % 1000 + b % 1000) < 1000 and R.random() < 0.6:
        return None
    s = a + b
    return mcq("Calcula mentalmente descomponiendo: %s + %s" % (num(a), num(b)), num(s), [num(s - 1000), num(s + 100), num(s - 10), num(s + 1000)],
               "%s + %s = %s, y %s + %s = %s: <b>%s</b>." % (num(a), num(b // 1000 * 1000), num(a + b // 1000 * 1000), num(a + b // 1000 * 1000), num(b % 1000), num(s), num(s)))


def s3_estimar():
    k = R.choice(["suma", "resta", "prod"])
    if k == "suma":
        a, b = R.randint(1100, 9800), R.randint(1100, 9800)
        ea, eb = rd(a, 1000), rd(b, 1000)
        e = ea + eb
        return mcq("Estima redondeando a los millares: %s + %s" % (num(a), num(b)), "unos %s" % num(e), ["unos %s" % num(e + 1000), "unos %s" % num(e - 1000), "unos %s" % num(e + 2000), "unos %s" % num(e // 10)],
                   "%s ≈ %s y %s ≈ %s; %s + %s = <b>%s</b>." % (num(a), num(ea), num(b), num(eb), num(ea), num(eb), num(e)))
    if k == "resta":
        a, b = R.randint(31000, 98000), R.randint(11000, 29000)
        ea, eb = rd(a, 10000), rd(b, 10000)
        e = ea - eb
        if e <= 0:
            return None
        return mcq("Estima redondeando a las decenas de millar: %s − %s" % (num(a), num(b)), "unos %s" % num(e), ["unos %s" % num(e + 10000), "unos %s" % num(e - 10000) if e > 10000 else "unos %s" % num(e + 20000), "unos %s" % num(ea + eb), "unos %s" % num(e // 10)],
                   "%s ≈ %s y %s ≈ %s; %s − %s = <b>%s</b>." % (num(a), num(ea), num(b), num(eb), num(ea), num(eb), num(e)))
    a, b = R.randint(12, 98), R.randint(3, 9)
    ea = rd(a, 10)
    e = ea * b
    return mcq("Estima redondeando a las decenas: %d %s %d" % (a, POR, b), "unos %s" % num(e), ["unos %s" % num(e + 10 * b), "unos %s" % num(e - 10 * b), "unos %s" % num(ea + b), "unos %s" % num(e * 10)],
               "%d ≈ %d; %d %s %d = <b>%s</b>." % (a, ea, ea, POR, b, num(e)))


def s4_razonable():
    a, b = R.randint(1100, 49000), R.randint(1100, 49000)
    s = a + b
    k = R.choice(["suma", "resta"])
    if k == "resta":
        a, b = max(a, b), min(a, b)
        s = a - b
        if s < 1000:
            return None
        op = "−"
    else:
        op = "+"
    cands = [s, s * 10, s // 10, s + R.choice([10000, -10000]) if s > 10000 else s + 20000]
    return mcq("Sin hacer la cuenta exacta, ¿qué resultado es razonable para %s %s %s?" % (num(a), op, num(b)), num(s), [num(x) for x in cands[1:] if x > 0],
               "Redondeando: %s %s %s ≈ %s. El más cercano es <b>%s</b>." % (num(rd(a, 1000)), op, num(rd(b, 1000)), num(rd(a, 1000) + rd(b, 1000) if op == "+" else rd(a, 1000) - rd(b, 1000)), num(s)))


def s5_problema():
    k = R.choice(["compra", "km", "entradas", "papel", "hucha", "colegio"])
    p, g = K.next()
    if k == "compra":
        xs = [R.randint(11, 79) * 10 + R.choice([0, 5]) for _ in range(3)]
        tot = sum(xs)
        lim = (tot // 100 + R.choice([0, 1])) * 100
        ok = tot <= lim
        if abs(tot - lim) < 20:
            return None
        return mcq("En una tienda hay una tele de %d €, una tablet de %d € y unos cascos de %d €. ¿Bastan %d € para comprar las tres cosas?" % (xs[0], xs[1], xs[2], lim),
                   "sí" if ok else "no", ["no" if ok else "sí", "solo si se redondea hacia arriba", "no se puede saber"],
                   "Estimamos: %d + %d + %d = %d €. %s" % (xs[0], xs[1], xs[2], tot, "Es menor que %d: <b>sí</b>." % lim if ok else "Es mayor que %d: <b>no</b>." % lim))
    if k == "km":
        a, b = R.randint(310, 690), R.randint(310, 690)
        e = rd(a, 100) + rd(b, 100)
        return mcq("Un camión recorre %d km el lunes y %d km el martes. ¿Cuántos kilómetros recorre aproximadamente en los dos días?" % (a, b), "unos %s km" % num(e), ["unos %s km" % num(e + 100), "unos %s km" % num(e - 100), "unos %s km" % num(e * 10), "unos %s km" % num(e + 1000)],
                   "%d ≈ %d y %d ≈ %d: unos <b>%s km</b>." % (a, rd(a, 100), b, rd(b, 100), num(e)))
    if k == "entradas":
        n = R.randint(21, 89) * 100
        pr = R.choice([2, 3, 4, 5])
        return mcq("Un museo vende %s entradas a %d € cada una. ¿Cuánto dinero recauda?" % (num(n), pr), "%s €" % num(n * pr), ["%s €" % num(n * pr // 10), "%s €" % num(n + pr), "%s €" % num(n * pr * 10), "%s €" % num(n * pr + 100)],
                   "%s %s %d = <b>%s €</b>." % (num(n), POR, pr, num(n * pr)))
    if k == "papel":
        n = R.randint(2, 9)
        return mcq("Un paquete tiene 500 hojas. ¿Cuántas hojas hay en %d paquetes?" % n, num(500 * n), [num(50 * n), num(5000 * n), num(500 + n), num(500 * n + 100)],
                   "500 %s %d = <b>%s</b>." % (POR, n, num(500 * n)))
    if k == "hucha":
        a = R.randint(101, 499)
        b = R.choice([99, 199, 299, 9, 49])
        if b >= a:
            return None
        return mcq("%s tiene %d € en la hucha y gasta %d €. ¿Cuánto le queda?" % (p, a, b), "%d €" % (a - b), ["%d €" % (a - b - 2), "%d €" % (a - b + 2), "%d €" % (a - b - 1), "%d €" % (a + b)],
                   "Restar %d es restar %d y sumar 1: %d − %d + 1 = <b>%d €</b>." % (b, b + 1, a, b + 1, a - b))
    n = R.randint(21, 49) * 10 + R.randint(1, 9)
    m = R.randint(21, 49) * 10 + R.randint(1, 9)
    e = rd(n, 100) + rd(m, 100)
    return mcq("En un colegio hay %d alumnos de Infantil y %d de Primaria. ¿Cuántos alumnos hay aproximadamente?" % (n, m), "unos %s" % num(e), ["unos %s" % num(e + 100), "unos %s" % num(e - 100), "unos %s" % num(e + 1000), "unos %s" % num(e // 10)],
               "%d ≈ %d y %d ≈ %d: unos <b>%s</b>." % (n, rd(n, 100), m, rd(m, 100), num(e)))


def main():
    seen = set()
    sets = [
        ("Sumar y restar números redondos", mix(R, seen, [(s1_redondos, 20)])),
        ("Sumar y restar 9, 99 y 999", mix(R, seen, [(s1_casi, 14), (s2_descomponer, 6)])),
        ("Dobles, mitades y ×10, ×100, ×1000", mix(R, seen, [(s2_dobles, 20)])),
        ("Estimar", mix(R, seen, [(s3_estimar, 14), (s4_razonable, 6)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Para sumar o restar números redondos, cambia solo la cifra de ese orden: 45 300 + 2000 = 47 300.",
         "Para sumar 99, suma 100 y resta 1. Para restar 99, resta 100 y suma 1.",
         "Para <b>estimar</b>, redondea los números y calcula con los números redondeados. Así sabes si un resultado es razonable."],
        [("4567 + 999", ["4567 + 1000 = 5567", "5567 − 1 = 5566"], "5566"),
         ("Estima 3812 + 5279", ["3812 ≈ 4000; 5279 ≈ 5000", "4000 + 5000 = 9000"], "unos 9000")],
        [["Sumar 99 y restar 1 de más", "+ 99 = + 100 − 1 (y − 99 = − 100 + 1)."],
         ["Cambiar el orden equivocado", "45 300 + 2000: cambia la unidad de millar, no la centena."],
         ["Estimar sin redondear", "Primero redondea; después calcula."]])
    faq = [("¿Para qué sirve estimar?", "Para calcular rápido un resultado aproximado y para comprobar si el resultado exacto de una cuenta es razonable."),
           ("¿Cómo se multiplica por 10, 100 o 1000?", "Se añaden a la derecha uno, dos o tres ceros: 45 × 100 = 4500.")]
    make_unit(R, "calculo-mental-y-estimacion", "N",
              "Estrategias de cálculo mental con números naturales; estimación de resultados de sumas, restas y multiplicaciones; valoración de la razonabilidad de un resultado",
              "Cálculo mental y estimación", "Cálculo mental y estimación",
              "Fichas de matemáticas de 4.º de Primaria: cálculo mental con números redondos, sumar y restar 9, 99 y 999, dobles y mitades, multiplicar por 10, 100 y 1000, y estimar. 100 ejercicios con soluciones.",
              "Redondea para estimar", "+ 99 = + 100 − 1. Estima antes de calcular.",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
