# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Números enteros (Sentido numérico)
Números positivos y negativos en la vida diaria (temperaturas, plantas de un edificio, altitudes, saldos), la recta numérica,
comparar y ordenar, opuesto y valor absoluto; 6.º también suma y resta de enteros sencilla.
Errores: pensar que −8 es mayor que −3 porque 8 &gt; 3, contar mal al cruzar el 0.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, sg, recta, MINUS

R = None
LV = 6


def rx():
    return R.randint(-15, 15) if LV == 5 else R.randint(-40, 40)


def s1_vida():
    k = R.choice(["temp", "planta", "altitud", "saldo", "temp2"])
    if k == "temp":
        t = R.randint(1, 12)
        return M("El termómetro marca %d grados bajo cero. ¿Cómo se escribe?" % t, "%s%d °C" % (MINUS, t), ["+%d °C" % t, "%d °C" % t, "%s%d °C" % (MINUS, t + 10)], "Bajo cero es negativo: <b>%s%d °C</b>." % (MINUS, t))
    if k == "planta":
        p = R.randint(1, 4)
        return M("En un ascensor, el aparcamiento está %d %s por debajo de la planta baja (0). ¿Qué número tiene?" % (p, "planta" if p == 1 else "plantas"), sg(-p), [sg(p), "0", sg(-p - 1), sg(-p + 1) if p > 1 else sg(2)],
                 "Por debajo del 0 los números son negativos: <b>%s</b>." % sg(-p))
    if k == "altitud":
        a = R.randint(2, 40) * 10
        return M("Un submarino está a %d metros por debajo del nivel del mar. ¿Qué número representa su altitud?" % a, "%s m" % sg(-a), ["%s m" % sg(a), "%s m" % sg(-a // 10), "0 m"], "Bajo el nivel del mar: <b>%s m</b>." % sg(-a))
    if k == "saldo":
        a = R.randint(10, 90)
        return M("Una cuenta del banco debe %d €. ¿Qué número indica su saldo?" % a, "%s €" % sg(-a), ["%s €" % sg(a), "0 €", "%s €" % sg(-a - 10)], "Una deuda es un número negativo: <b>%s €</b>." % sg(-a))
    a = R.randint(-10, 5)
    b = R.randint(1, 12)
    return M("A las 7:00 la temperatura era %s °C y a mediodía había subido %d grados. ¿Qué temperatura hacía a mediodía?" % (sg(a), b), "%s °C" % sg(a + b),
             ["%s °C" % sg(a - b), "%s °C" % sg(-a + b) if -a + b != a + b else "%s °C" % sg(a + b + 2), "%s °C" % sg(abs(a) + b) if abs(a) + b != a + b else "%s °C" % sg(a + b - 1)],
             "Subir %d grados desde %s: <b>%s °C</b>." % (b, sg(a), sg(a + b)))


def s2_recta():
    lo = R.choice([-10, -8, -6, -5])
    x = R.randint(lo + 1, -1) if R.random() < 0.7 else R.randint(1, 4)
    g = recta(lo, lo + 15, 1, marks=[(x, "?")], labels=[lo, 0, lo + 15], every=5)
    return M(g + "¿Qué número está en «?»?", sg(x), [sg(-x), sg(x + 1), sg(x - 1)], "Contamos desde el 0: <b>%s</b>." % sg(x))


def s2_comparar():
    k = R.choice(["dos", "mayor", "menor", "orden", "opuesto", "abs"])
    if k == "dos":
        a, b = R.sample(range(-20, 21), 2)
        if a >= 0 and b >= 0:
            return None
        ok = "%s %s %s" % (sg(a), "&lt;" if a < b else "&gt;", sg(b))
        return M("Compara %s y %s. ¿Qué es correcto?" % (sg(a), sg(b)), ok, ["%s %s %s" % (sg(a), "&gt;" if a < b else "&lt;", sg(b)), "%s = %s" % (sg(a), sg(b)), "no se pueden comparar"],
                 "En la recta, el número que está más a la derecha es el mayor: <b>%s</b>." % ok)
    if k in ("mayor", "menor"):
        xs = sorted(set(R.sample(range(-20, 21), 4)))
        if len(xs) < 4 or sum(1 for x in xs if x < 0) < 2:
            return None
        sh = list(xs)
        R.shuffle(sh)
        a = xs[-1] if k == "mayor" else xs[0]
        return M("¿Cuál es el número %s? %s" % (k, "; ".join(sg(x) for x in sh)), sg(a), [sg(x) for x in xs], "El %s es <b>%s</b>." % (k, sg(a)))
    if k == "orden":
        xs = sorted(set(R.sample(range(-15, 16), 4)))
        if len(xs) < 4 or sum(1 for x in xs if x < 0) < 2:
            return None
        sh = list(xs)
        R.shuffle(sh)
        f = lambda L: " &lt; ".join(sg(x) for x in L)
        neg = [x for x in xs if x < 0]
        wrong = sorted(neg, key=abs) + [x for x in xs if x >= 0]
        return M("Ordena de menor a mayor: %s" % "; ".join(sg(x) for x in sh), f(xs), [f(wrong), f(xs[::-1]), f([xs[1], xs[0], xs[2], xs[3]])], "<b>%s</b>." % f(xs))
    a = R.randint(1, 30) * R.choice([-1, 1])
    if k == "opuesto":
        return M("¿Cuál es el opuesto de %s?" % sg(a), sg(-a), [sg(a), "0", sg(-a + 1) if -a + 1 != 0 else sg(-a - 1)], "El opuesto está a la misma distancia del 0, al otro lado: <b>%s</b>." % sg(-a))
    return M("¿Cuál es el valor absoluto de %s, |%s|?" % (sg(a), sg(a)), num(abs(a)), [sg(-abs(a)), "0", num(abs(a) + 1)], "Es la distancia al 0: <b>%s</b>." % num(abs(a)))


def s3_operar():
    a, b = rx(), R.randint(1, 15 if LV == 5 else 30)
    k = R.choice(["+", "-"])
    r = a + b if k == "+" else a - b
    txt = "%s + %d" % (sg(a), b) if k == "+" else "%s − %d" % (sg(a), b)
    return M("Calcula: %s" % txt, sg(r), [sg(-r) if r else sg(1), sg(a - b if k == "+" else a + b), sg(r + 1), sg(r - 2)],
             "Desde %s nos movemos %d %s en la recta: <b>%s</b>." % (sg(a), b, "a la derecha" if k == "+" else "a la izquierda", sg(r)))


def s3_dif():
    a = R.randint(1, 20)
    b = -R.randint(1, 15)
    k = R.choice(["temp", "altura", "año"])
    if k == "temp":
        return M("En una ciudad hay %s °C y en otra %s °C. ¿Cuántos grados de diferencia hay?" % (sg(a), sg(b)), "%d °C" % (a - b), ["%d °C" % (a + b) if a + b > 0 else "%d °C" % (a - b + 2), "%d °C" % (a - b - 1), "%d °C" % abs(b), "%d °C" % (a - b + 10)],
                 "De %s a 0 hay %d, y de 0 a %s, %d más: %d + %d = <b>%d °C</b>." % (sg(b), -b, sg(a), a, -b, a, a - b))
    if k == "altura":
        h = R.randint(3, 20) * 100
        p = R.randint(1, 9) * 10
        return M("Una montaña mide %s m y la sima de una cueva está a %s m. ¿Cuántos metros hay entre la cima y el fondo de la sima?" % (num(h), sg(-p)), "%s m" % num(h + p), ["%s m" % num(h - p), "%s m" % num(h), "%s m" % num(h + p + 10)],
                 "%s + %d = <b>%s m</b>." % (num(h), p, num(h + p)))
    s = R.randint(1, 6)
    return M("Un ascensor está en la planta %s. Sube %d plantas. ¿En qué planta está ahora?" % (sg(-s), s + a // 4), sg(-s + s + a // 4), [sg(-s - s - a // 4), sg(s + s + a // 4), sg(-s + s + a // 4 + 1)],
             "%s + %d = <b>%s</b>." % (sg(-s), s + a // 4, sg(-s + s + a // 4)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40002 + lv * 1000)
    seen = set()
    sets = [
        ("Los números negativos en la vida diaria", mix(R, seen, [(s1_vida, 20)])),
        ("La recta numérica", mix(R, seen, [(s2_recta, 14), (s2_comparar, 6)])),
        ("Comparar y ordenar enteros", mix(R, seen, [(s2_comparar, 20)])),
        ("Sumar y restar en la recta", mix(R, seen, [(s3_operar, 20)])),
        ("Problemas", mix(R, seen, [(s3_dif, 12), (s1_vida, 8)])),
    ]
    body = lesson(
        ["Los <b>números enteros</b> son los positivos (+3), el 0 y los negativos (−3). Usamos negativos para temperaturas bajo cero, plantas de sótano, deudas o profundidades.",
         "En la recta numérica, los negativos están a la izquierda del 0. <b>Es mayor el que está más a la derecha</b>: −3 &gt; −8.",
         "El <b>opuesto</b> de 5 es −5. El <b>valor absoluto</b> es la distancia al 0: |−5| = 5."],
        [("La temperatura es −4 °C y sube 6 grados", ["Desde −4, 6 pasos a la derecha"], "2 °C"),
         ("Ordena −2, 3, −7, 0", ["El más a la izquierda es −7"], "−7 &lt; −2 &lt; 0 &lt; 3")],
        [["Creer que −8 &gt; −3", "Cuanto más a la izquierda, menor: −8 &lt; −3."],
         ["Olvidar el 0 al contar", "De −2 a 3 hay 5 pasos: −2, −1, 0, 1, 2, 3."],
         ["Confundir opuesto y valor absoluto", "Opuesto de −5: 5. Valor absoluto de −5: 5. Opuesto de 5: −5."]],
        recta(-6, 6, 1, labels=[-6, -3, 0, 3, 6]))
    faq = [("¿Qué número es mayor, −3 o −8?", "−3, porque en la recta numérica está más a la derecha (más cerca del 0)."),
           ("¿Para qué sirven los números negativos?", "Para expresar cantidades por debajo de un punto de referencia: temperaturas bajo cero, plantas de sótano, deudas o profundidades bajo el nivel del mar.")]
    make_unit(R, "numeros-enteros", "N",
              "Números enteros: interpretación en contextos de la vida cotidiana, representación en la recta numérica, comparación y ordenación" + ("; suma y resta en situaciones sencillas" if lv == 6 else ""),
              "Números enteros: positivos y negativos", "Números enteros",
              "Fichas de matemáticas de %d.º de Primaria: números negativos en la vida diaria, la recta numérica, comparar y ordenar enteros, opuesto, valor absoluto y problemas. 100 ejercicios con soluciones." % lv,
              "En la recta, mayor a la derecha", "−3 es mayor que −8.",
              body, faq, sets, 2, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
