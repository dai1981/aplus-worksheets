# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Números enteros (Sentido numérico)
Representar, ordenar, valor absoluto y opuesto; sumar y restar; multiplicar y dividir (regla de los signos); operaciones combinadas; problemas.
Errores: pensar que −8 > −3, olvidar cambiar el signo al quitar un paréntesis precedido de −, aplicar mal la regla de los signos.
"""
import random
from es_eso import M, mix, sg, par, unit, L, Kids, recta, nz

R = random.Random(47002)
K = Kids(R)


def s_orden():
    t = R.choice(["mayor", "menor", "orden", "abs", "opuesto", "recta"])
    if t in ("mayor", "menor"):
        xs = R.sample(range(-15, 16), 4)
        ok = max(xs) if t == "mayor" else min(xs)
        return M("¿Cuál es el %s de estos números: %s?" % (t, ", ".join(sg(x) for x in xs)), sg(ok), [sg(x) for x in xs if x != ok] + [sg(-ok)],
                 "En la recta, el %s es el que está más a la %s: <b>%s</b>." % (t, "derecha" if t == "mayor" else "izquierda", sg(ok)))
    if t == "orden":
        xs = R.sample(range(-12, 13), 4)
        if not any(x < 0 for x in xs):
            return None
        ok = " &lt; ".join(sg(x) for x in sorted(xs))
        w1 = " &lt; ".join(sg(x) for x in sorted(xs, key=abs))
        w2 = " &lt; ".join(sg(x) for x in sorted(xs, reverse=True))
        neg = sorted([x for x in xs if x < 0], reverse=True) + sorted([x for x in xs if x >= 0])
        w3 = " &lt; ".join(sg(x) for x in neg)
        return M("Ordena de menor a mayor: %s" % ", ".join(sg(x) for x in xs), ok, [w1, w2, w3], "Los negativos van primero; entre ellos, el que tiene mayor valor absoluto es el menor: <b>%s</b>." % ok)
    if t == "abs":
        a = nz(R, -40, 40)
        return M("¿Cuánto vale |%s|?" % sg(a), sg(abs(a)), [sg(-abs(a)), sg(abs(a) + 1), "0"], "El valor absoluto es la distancia al 0: <b>%s</b>." % sg(abs(a)))
    if t == "opuesto":
        a = nz(R, -40, 40)
        return M("¿Cuál es el opuesto de %s?" % sg(a), sg(-a), [sg(a), "0", sg(-a + 1) if a > 0 else sg(-a - 1)], "El opuesto está a la misma distancia del 0, al otro lado: <b>%s</b>." % sg(-a))
    v = R.randint(-9, 9)
    if v == 0:
        return None
    pic = recta(-10, 10, 1, [(v, "A")], every=5)
    return M(pic + "¿Qué número entero marca la letra A?", sg(v), [sg(-v), sg(v + 1), sg(v - 1)], "A está %d unidades a la %s del 0: <b>%s</b>." % (abs(v), "derecha" if v > 0 else "izquierda", sg(v)))


def s_suma():
    a, b = nz(R, -30, 30), nz(R, -30, 30)
    t = R.choice(["+", "-", "+", "-", "tres"])
    if t == "+":
        r = a + b
        return M("Calcula: %s + %s" % (sg(a), par(b)), sg(r), [sg(a - b), sg(-r) if r else "1", sg(abs(a) + abs(b)) if r != abs(a) + abs(b) else sg(r + 2)],
                 "%s: <b>%s</b>." % ("Mismo signo: sumamos y dejamos el signo" if a * b > 0 else "Distinto signo: restamos y ponemos el signo del de mayor valor absoluto", sg(r)))
    if t == "-":
        r = a - b
        return M("Calcula: %s − %s" % (sg(a), par(b)), sg(r), [sg(a + b), sg(-r) if r else "1", sg(r + 2)], "Restar es sumar el opuesto: %s + %s = <b>%s</b>." % (sg(a), par(-b), sg(r)))
    c = nz(R, -20, 20)
    r = a - b + c
    return M("Calcula: %s − %s + %s" % (sg(a), par(b), par(c)), sg(r), [sg(a + b + c), sg(a - b - c), sg(-r) if r else "2"], "Quitamos paréntesis: %s %s %s %s %s = <b>%s</b>." % (sg(a), "+" if b < 0 else "−", abs(b), "+" if c > 0 else "−", abs(c), sg(r)))


def s_mult():
    a, b = nz(R, -12, 12), nz(R, -12, 12)
    t = R.choice(["x", "x", ":", "tres", "pot"])
    if t == "x":
        return M("Calcula: %s · %s" % (sg(a), par(b)), sg(a * b), [sg(-a * b), sg(a + b), sg(a * b + a)], "%s: <b>%s</b>." % ("Signos iguales, resultado positivo" if a * b > 0 else "Signos distintos, resultado negativo", sg(a * b)))
    if t == ":":
        p = a * b
        return M("Calcula: %s : %s" % (sg(p), par(b)), sg(a), [sg(-a), sg(p - b), sg(b)] if a != b else [sg(-a), sg(p - b), sg(a + 1)], "%s · %s = %s, así que el cociente es <b>%s</b>." % (sg(a), par(b), sg(p), sg(a)))
    if t == "pot":
        a = nz(R, -6, 6)
        n = R.choice([2, 3, 4])
        return M("Calcula: (%s)<sup>%d</sup>" % (sg(a), n) if a < 0 else "Calcula: %s<sup>%d</sup>" % (sg(a), n), sg(a ** n), [sg(-(a ** n)), sg(a * n), sg(abs(a) ** n + 1)],
                 "%s: <b>%s</b>." % ("Base negativa y exponente par: positivo" if a < 0 and n % 2 == 0 else "Base negativa y exponente impar: negativo" if a < 0 else "Base positiva", sg(a ** n)))
    c = nz(R, -5, 5)
    r = a * b * c
    return M("Calcula: %s · %s · %s" % (sg(a), par(b), par(c)), sg(r), [sg(-r), sg(a + b + c), sg(a * b + c)], "Contamos los signos negativos: %s. Resultado: <b>%s</b>." % ("par" if r > 0 else "impar", sg(r)))


def s_comb():
    a, b, c = nz(R, -9, 9), nz(R, -9, 9), nz(R, -9, 9)
    t = R.choice(["a+bc", "(a+b)c", "a-bc", "a-(b-c)", "ab-c"])
    if t == "a+bc":
        q, r, w = "%s + %s · %s" % (sg(a), par(b), par(c)), a + b * c, (a + b) * c
    elif t == "(a+b)c":
        q, r, w = "(%s + %s) · %s" % (sg(a), par(b), par(c)), (a + b) * c, a + b * c
    elif t == "a-bc":
        q, r, w = "%s − %s · %s" % (sg(a), par(b), par(c)), a - b * c, (a - b) * c
    elif t == "a-(b-c)":
        q, r, w = "%s − (%s − %s)" % (sg(a), sg(b), par(c)), a - (b - c), a - b - c
    else:
        q, r, w = "%s · %s − %s" % (sg(a), par(b), par(c)), a * b - c, a * (b - c)
    return M("Calcula: %s" % q, sg(r), [sg(w), sg(-r) if r else "1", sg(r + 2)], "Primero los paréntesis, después las multiplicaciones y al final sumas y restas: <b>%s</b>." % sg(r))


def s_problema():
    p = K.next()[0]
    t = R.choice(["temp", "ascensor", "cuenta", "buzo", "historia"])
    if t == "temp":
        a, b = R.randint(-12, 4), R.randint(3, 15)
        return M("A las 6:00 la temperatura era de %s °C y a las 14:00 había subido %d grados. ¿Qué temperatura había a las 14:00?" % (sg(a), b), "%s °C" % sg(a + b),
                 ["%s °C" % sg(a - b), "%s °C" % sg(-(a + b)) if a + b else "1 °C", "%s °C" % sg(abs(a) + b)], "%s + %d = <b>%s °C</b>." % (sg(a), b, sg(a + b)))
    if t == "ascensor":
        a, s, b = R.randint(-3, 8), R.randint(2, 9), R.randint(3, 12)
        r = a + s - b
        return M("Un ascensor está en la planta %s. Sube %d plantas y luego baja %d. ¿En qué planta está?" % (sg(a), s, b), sg(r), [sg(a - s + b), sg(-r) if r else "1", sg(r + 1)], "%s + %d − %d = <b>%s</b>." % (sg(a), s, b, sg(r)))
    if t == "cuenta":
        a, g = R.randint(20, 150), R.randint(30, 250)
        return M("%s tiene %d € en el banco y paga una factura de %d €. ¿Qué saldo le queda?" % (p, a, g), "%s €" % sg(a - g), ["%s €" % sg(g - a), "%s €" % sg(a + g), "%s €" % sg(a - g + 10)], "%d − %d = <b>%s €</b>." % (a, g, sg(a - g)))
    if t == "buzo":
        a, b = R.randint(5, 30), R.randint(3, 15)
        return M("Un buzo está a %s m. Sube %d m. ¿A qué profundidad está ahora?" % (sg(-a), b), "%s m" % sg(-a + b), ["%s m" % sg(-a - b), "%s m" % sg(a - b), "%s m" % sg(-a + b + 1)], "%s + %d = <b>%s m</b>." % (sg(-a), b, sg(-a + b)))
    n, m = R.randint(50, 600), R.randint(100, 1500)
    return M("Una ciudad se fundó en el año %d a. C. Otra, en el año %d d. C. ¿Cuántos años pasaron entre las dos fundaciones? (Tomamos a. C. como negativo y no contamos el año 0.)" % (n, m),
             str(m + n - 1), [str(m - n) if m > n else str(n - m + 1), str(m + n), str(m + n + 1)], "%d − (%s) = %d; sin el año 0, <b>%d</b> años." % (m, sg(-n), m + n, m + n - 1))


seen = set()
sets = [("Ordenar, valor absoluto y opuesto", mix(R, seen, [(s_orden, 20)])), ("Sumas y restas", mix(R, seen, [(s_suma, 20)])),
        ("Multiplicaciones, divisiones y potencias", mix(R, seen, [(s_mult, 20)])), ("Operaciones combinadas", mix(R, seen, [(s_comb, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["Los números enteros son los naturales, el 0 y los negativos. En la recta, es mayor el que está más a la derecha: −3 &gt; −8.",
          "Sumar: con el mismo signo, se suman y se deja el signo; con distinto signo, se restan y se pone el signo del de mayor valor absoluto.",
          "Restar es sumar el opuesto: 5 − (−3) = 5 + 3.", "Multiplicar y dividir: signos iguales dan +; signos distintos dan −."],
         [("−7 + 4 − (−5)", ["−7 + 4 + 5", "−3 + 5"], "2"), ("(−3) · 4 − (−6) : 2", ["−12 − (−3)", "−12 + 3"], "−9")],
         [["Pensar que −8 &gt; −3", "Más a la izquierda es menor."], ["No cambiar el signo al quitar «−( )»", "−(4 − 7) = −4 + 7."], ["Aplicar la regla de los signos a la suma", "−3 − 5 = −8, no +8."]],
         recta(-6, 6, 1, [(-3, "A"), (4, "B")]))
faq = [("¿Qué es el valor absoluto?", "La distancia de un número al 0, sin signo: |−7| = 7."), ("¿Por qué menos por menos es más?", "Porque multiplicar por −1 cambia el signo: si lo haces dos veces, vuelves al signo de partida.")]
unit(1, R, "numeros-enteros", "N", "Números enteros: representación en la recta, orden, valor absoluto y opuesto; operaciones con enteros y jerarquía de las operaciones; problemas en contexto",
     "Números enteros", "Números enteros",
     "Fichas de matemáticas de 1.º de ESO: ordenar enteros, valor absoluto, sumas, restas, regla de los signos, operaciones combinadas y problemas. 100 ejercicios con soluciones.",
     "Signos iguales +, distintos −", "Restar es sumar el opuesto.", body, faq, sets, 2)
