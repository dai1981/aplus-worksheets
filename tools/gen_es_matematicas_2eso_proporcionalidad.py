# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º de ESO: Proporcionalidad directa e inversa (Sentido numérico)
Reconocer magnitudes directa e inversamente proporcionales, regla de tres directa e inversa, proporcionalidad compuesta, repartos directamente e inversamente proporcionales.
Errores: usar la regla de tres directa con magnitudes inversas, repartir en partes iguales, invertir mal en el reparto inverso.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, num, eur, unit, L, Kids, tabla

R = random.Random(48003)
K = Kids(R)


def s_tipo():
    q, a = R.choice([("El número de obreros y el tiempo que tardan en hacer una obra", "inversamente proporcionales"), ("Los kilos de fruta comprados y lo que se paga", "directamente proporcionales"),
                     ("La velocidad de un coche y el tiempo que tarda en un trayecto fijo", "inversamente proporcionales"), ("Las horas trabajadas y el sueldo (a tanto la hora)", "directamente proporcionales"),
                     ("La edad de una persona y su altura", "no son proporcionales"), ("El número de grifos iguales abiertos y el tiempo en llenar un depósito", "inversamente proporcionales"),
                     ("El número de invitados y la cantidad de comida necesaria", "directamente proporcionales"), ("El número de amigos que pagan un regalo y lo que paga cada uno", "inversamente proporcionales"),
                     ("El lado de un cuadrado y su área", "no son proporcionales"), ("Los litros de gasolina y los kilómetros recorridos (mismo consumo)", "directamente proporcionales"),
                     ("El número de vacas y los días que dura el pienso", "inversamente proporcionales"), ("La temperatura y la hora del día", "no son proporcionales")])
    opts = ["directamente proporcionales", "inversamente proporcionales", "no son proporcionales", "son iguales"]
    return M("¿Cómo son estas magnitudes? %s." % q, a, [o for o in opts if o != a], "Si una se duplica y la otra %s: <b>%s</b>." % ({"directamente proporcionales": "también", "inversamente proporcionales": "se reduce a la mitad", "no son proporcionales": "no cambia de forma fija"}[a], a))


def s_tabla():
    k = R.randint(12, 60)
    t = R.choice(["dir", "inv"])
    xs = sorted(R.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], 4))
    if t == "dir":
        ys = [k * x for x in xs]
    else:
        k = R.choice([24, 48, 60, 72, 120, 240])
        if any(k % x for x in xs):
            return None
        ys = [k // x for x in xs]
    i = R.randint(1, 3)
    row = [str(y) if j != i else "?" for j, y in enumerate(ys)]
    pic = tabla(["Magnitud A"] + [str(x) for x in xs], [["Magnitud B"] + row])
    w = [str(ys[0] * xs[i] // xs[0]) if t == "inv" else str(k // xs[i]) if k % xs[i] == 0 else str(ys[i] + 1), str(ys[i] + k), str(ys[i - 1] + ys[0])]
    return M(pic + "Las magnitudes son %s proporcionales. ¿Qué número va en «?»?" % ("directamente" if t == "dir" else "inversamente"), str(ys[i]), w,
             "%s: <b>%d</b>." % ("El cociente B/A es constante (%d)" % k if t == "dir" else "El producto A · B es constante (%d)" % k, ys[i]))


def s_regla():
    t = R.choice(["dir", "inv", "inv"])
    p = K.next()[0]
    if t == "dir":
        a, b = R.randint(2, 9), R.randint(2, 15)
        u = R.randint(3, 25)
        if a == b:
            return None
        return M("Por %d horas de trabajo se pagan %d €. ¿Cuánto se paga por %d horas?" % (a, a * u, b), "%d €" % (b * u), ["%s €" % d(F(a * u * a, b)), "%d €" % (a * u + b - a), "%d €" % (b * u + u)], "Directa: %d : %d · %d = <b>%d €</b>." % (a * u, a, b, b * u))
    ctx = R.choice(["obreros", "grifos", "velocidad", "amigos", "pienso"])
    a, b = R.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
    c = a * b * R.randint(1, 3)
    if ctx == "obreros":
        q = "%d obreros tardan %d días en hacer una obra. ¿Cuántos días tardarán %d obreros?" % (a, c // a, b) if c % a == 0 else None
        if not q:
            return None
        ans = F(a * (c // a), b)
        u = "días"
    elif ctx == "grifos":
        q = "%d grifos iguales llenan un depósito en %d horas. ¿Cuánto tardan %d grifos?" % (a, c // a, b) if c % a == 0 else None
        if not q:
            return None
        ans, u = F(a * (c // a), b), "h"
    elif ctx == "velocidad":
        v1, v2 = R.sample([40, 50, 60, 80, 90, 100, 120], 2)
        t1 = R.choice([2, 3, 4, 5, 6])
        ans = F(v1 * t1, v2)
        q = "A %d km/h, un coche tarda %d horas en un viaje. ¿Cuánto tardará a %d km/h?" % (v1, t1, v2)
        u = "h"
        a, b = v1, v2
    elif ctx == "amigos":
        e = R.randint(5, 20)
        q = "Un regalo se paga entre %d amigos y cada uno pone %d €. Si fueran %d amigos, ¿cuánto pondría cada uno?" % (a, e, b)
        ans, u = F(a * e, b), "€"
    else:
        dias = R.randint(10, 40)
        q = "Para %d vacas hay pienso para %d días. ¿Para cuántos días habrá si hay %d vacas?" % (a, dias, b)
        ans, u = F(a * dias, b), "días"
    if ans.denominator not in (1, 2, 4, 5):
        return None
    direct = ans * b * b / (a * a)
    return M(q, "%s %s" % (d(ans), u), ["%s %s" % (d(direct), u) if direct.denominator in (1, 2, 4, 5) and direct != ans else "%s %s" % (d(ans + 2), u), "%s %s" % (d(ans + 1), u), "%s %s" % (d(ans * 2), u)],
             "Inversa: el producto es constante; %s = <b>%s %s</b>." % ("se multiplica y se divide al revés", d(ans), u))


def s_compuesta():
    a, b, c = R.randint(2, 6), R.randint(2, 8), R.randint(2, 6)
    t = R.choice(["dir", "mix"])
    if t == "dir":
        p = a * b * R.randint(3, 10)
        a2, b2 = R.randint(2, 9), R.randint(2, 10)
        ans = F(p * a2 * b2, a * b)
        if ans.denominator != 1:
            return None
        return M("%d máquinas trabajando %d horas fabrican %d piezas. ¿Cuántas piezas fabrican %d máquinas en %d horas?" % (a, b, p, a2, b2), num(int(ans)), [num(p * a2 * b // (a * b2)) if p * a2 * b % (a * b2) == 0 and p * a2 * b // (a * b2) != ans else num(int(ans) + p), num(p + a2 + b2 - a - b) if p + a2 + b2 - a - b > 0 else num(int(ans) * 2), num(int(ans) // 2) if int(ans) % 2 == 0 else num(int(ans) + 1)],
                 "Las dos son directas: %d · %d/%d · %d/%d = <b>%s</b>." % (p, a2, a, b2, b, num(int(ans))))
    dias = R.randint(4, 12)
    a2, h2 = R.randint(2, 8), R.choice([4, 5, 6, 8, 10])
    h = R.choice([4, 5, 6, 8, 10])
    ans = F(dias * a * h, a2 * h2)
    if ans.denominator != 1 or (a2 == a and h2 == h):
        return None
    return M("%d pintores, trabajando %d horas diarias, pintan una casa en %d días. ¿Cuántos días tardarán %d pintores trabajando %d horas diarias?" % (a, h, dias, a2, h2), "%d días" % ans,
             ["%s días" % d(F(dias * a2 * h2, a * h)) if F(dias * a2 * h2, a * h).denominator in (1, 2, 4, 5) else "%d días" % (int(ans) + 2), "%d días" % (int(ans) + 1), "%d días" % (dias + a2 - a) if dias + a2 - a > 0 else "%d días" % (dias * 2)],
             "Las dos son inversas: %d · %d/%d · %d/%d = <b>%d días</b>." % (dias, a, a2, h, h2, int(ans)))


def s_reparto():
    t = R.choice(["dir", "dir", "inv"])
    p, q, r = K.next()[0], K.next()[0], K.next()[0]
    if t == "dir":
        xs = R.sample(range(2, 9), 3)
        k = R.randint(5, 40)
        tot = sum(xs) * k
        i = R.randrange(3)
        nm = [p, q, r][i]
        return M("Tres amigos (%s, %s y %s) ponen %d €, %d € y %d € para un boleto que gana %d €. Se reparte de forma directamente proporcional a lo que pusieron. ¿Cuánto recibe %s?" % (p, q, r, xs[0], xs[1], xs[2], tot, nm),
                 "%d €" % (xs[i] * k), ["%s €" % d(F(tot, 3)), "%d €" % (xs[i] * k + k), "%d €" % (tot - xs[i] * k)], "Cada euro aportado recibe %d : %d = %d €; %d · %d = <b>%d €</b>." % (tot, sum(xs), k, xs[i], k, xs[i] * k))
    xs = R.sample([2, 3, 4, 6], 2)
    inv = [F(1, x) for x in xs]
    tot = R.choice([100, 150, 200, 300, 600])
    k = tot / sum(inv)
    parts = [k * v for v in inv]
    if any(pt.denominator != 1 for pt in parts):
        return None
    return M("Se reparten %d € de forma inversamente proporcional a las faltas de dos alumnos: %s tiene %d faltas y %s tiene %d. ¿Cuánto recibe %s?" % (tot, p, xs[0], q, xs[1], p), "%d €" % parts[0],
             ["%d €" % parts[1], "%s €" % d(F(tot * xs[0], sum(xs))), "%s €" % d(F(tot, 2))], "Repartimos en proporción a 1/%d y 1/%d: %s recibe <b>%d €</b>." % (xs[0], xs[1], p, parts[0]))


seen = set()
sets = [("Directa, inversa o ninguna", mix(R, seen, [(s_tipo, 12), (s_tabla, 8)])), ("Tablas de proporcionalidad", mix(R, seen, [(s_tabla, 20)])), ("Regla de tres directa e inversa", mix(R, seen, [(s_regla, 20)])),
        ("Proporcionalidad compuesta", mix(R, seen, [(s_compuesta, 20)])), ("Repartos proporcionales", mix(R, seen, [(s_reparto, 20)]))]
body = L(["Dos magnitudes son <b>directamente proporcionales</b> si al doble le corresponde el doble: su cociente es constante.",
          "Son <b>inversamente proporcionales</b> si al doble le corresponde la mitad: su producto es constante.",
          "En la proporcionalidad <b>compuesta</b> intervienen tres o más magnitudes: se estudia cada una por separado frente a la incógnita.",
          "En un reparto directamente proporcional, cada parte es proporcional a su número; en uno inverso, a su inverso."],
         [("4 obreros tardan 6 días. ¿Cuánto tardan 3?", ["Inversa: 4 · 6 = 24", "24 : 3"], "8 días"), ("Repartir 90 € en proporción a 2 y 4", ["90 : 6 = 15 € por parte", "2 · 15 y 4 · 15"], "30 € y 60 €")],
         [["Usar la regla de tres directa con magnitudes inversas", "Más obreros, menos días: es inversa."], ["Repartir en partes iguales", "Reparte según la proporción."], ["Invertir mal en el reparto inverso", "Usa 1/a, 1/b…"]])
faq = [("¿Cómo sé si una proporcionalidad es inversa?", "Si al aumentar una magnitud la otra disminuye en la misma proporción: el doble de grifos tarda la mitad."),
       ("¿Qué es un reparto proporcional?", "Repartir una cantidad en partes que guardan la misma proporción que unos números dados.")]
unit(2, R, "proporcionalidad-directa-e-inversa", "N", "Magnitudes directa e inversamente proporcionales; constante de proporcionalidad; regla de tres simple y compuesta; repartos proporcionales",
     "Proporcionalidad directa e inversa", "Proporcionalidad",
     "Fichas de matemáticas de 2.º de ESO: magnitudes directa e inversamente proporcionales, regla de tres, proporcionalidad compuesta y repartos. 100 ejercicios con soluciones.",
     "Inversa: el producto es constante", "Directa: el cociente es constante.", body, faq, sets, 3)
