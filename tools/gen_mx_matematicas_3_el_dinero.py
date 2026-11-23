# -*- coding: utf-8 -*-
"""
México 3.er grado de primaria: El dinero (monedas y billetes de pesos; contar, equivalencias, comparar, cambio y problemas de compras).
Monedas de 50 centavos, $1, $2, $5, $10 y $20; billetes de $20, $50, $100 y $200. Errores: contar monedas en lugar de su valor, confundir 50 centavos con $50, restar mal el cambio.
"""
import random
from mx_common import mcq, num, unit, peso, dinero_svg, Kids

R = random.Random(63116)
K = Kids(R)
COINS = [50, 100, 200, 500, 1000]
BILLS = ["b2000", "b5000", "b10000"]


def val(v):
    return int(v[1:]) if isinstance(v, str) else v


def s_contar():
    n = R.randint(3, 6)
    items = sorted([R.choice(COINS + (BILLS if R.random() < 0.4 else [])) for _ in range(n)], key=lambda v: -val(v))
    tot = sum(val(v) for v in items)
    return mcq(dinero_svg(items) + "¿Cuánto dinero hay?", peso(tot), [peso(tot + 100), peso(tot - 50) if tot > 50 else peso(tot + 50), peso(n * 100), peso(sum(val(v) for v in items if val(v) != 50)) if 50 in items else peso(tot + 1000)],
               "Sumamos el valor de cada moneda y billete, no cuántos hay: <b>%s</b>." % peso(tot))


def s_equiv():
    t = R.choice(["cuantas", "cuantas", "centavos", "cincuenta", "billete"])
    if t == "cuantas":
        c = R.choice([100, 200, 500, 1000])
        k = R.randint(2, 10)
        return mcq("¿Cuántas monedas de %s necesitas para juntar %s?" % (peso(c), peso(c * k)), str(k), [str(c * k // 100), str(k + 1), str(k * 2)] if c != 100 else [str(k + 1), str(k * 2), str(k - 1)],
                   "%s ÷ %s = <b>%d</b> monedas." % (num(c * k // 100), num(c // 100), k))
    if t == "centavos":
        p = R.randint(2, 9)
        return mcq("¿Cuántos centavos son %s?" % peso(p * 100), "%s centavos" % num(p * 100), ["%d centavos" % (p * 10), "%d centavos" % p, "%s centavos" % num(p * 1000)], "$1 = 100 centavos: %d × 100 = <b>%s centavos</b>." % (p, num(p * 100)))
    if t == "cincuenta":
        p = R.randint(1, 8)
        return mcq("¿Cuántas monedas de 50 centavos hacen %s?" % peso(p * 100), str(2 * p), [str(p), str(p * 50), str(2 * p + 1)], "Dos monedas de 50 centavos son $1: %d × 2 = <b>%d</b>." % (p, 2 * p))
    b, c = R.choice([(5000, 1000), (2000, 500), (10000, 2000), (10000, 5000), (5000, 500), (2000, 1000), (20000, 10000), (10000, 1000)])
    k = b // c
    lab = "billetes" if c in (2000, 5000, 10000) and c != 2000 else "monedas"
    return mcq("Un billete de %s, ¿a cuántas %s de %s equivale?" % (peso(b), lab, peso(c)), str(k), [str(k + 1), str(k * 2), str(b // 100)] if b // 100 != k else [str(k + 1), str(k * 2), str(k - 1)],
               "%s ÷ %s = <b>%d</b>." % (num(b // 100), num(c // 100), k))


def s_comparar():
    t = R.choice(["precio", "precio", "quien"])
    if t == "precio":
        e = R.randint(10, 90)
        a, b = R.sample([5, 50, 55, 15, 10], 2)
        p1, p2 = e * 100 + a, e * 100 + b
        ok = peso(max(p1, p2))
        return mcq("¿Qué cuesta más: %s o %s?" % (peso(p1), peso(p2)), ok, [peso(min(p1, p2)), "cuestan lo mismo", "no se puede saber"],
                   "Mismos pesos; comparamos los centavos: %d &gt; %d. <b>%s</b>." % (max(a, b), min(a, b), ok))
    (n1, _), (n2, _) = K.two()
    s1 = sorted(R.sample(COINS, 3), reverse=True)
    s2 = sorted([R.choice(COINS) for _ in range(5)], reverse=True)
    t1, t2 = sum(s1), sum(s2)
    if t1 == t2:
        return None
    ok = n1 if t1 > t2 else n2
    return mcq("Dinero de %s:%sDinero de %s:%s¿Quién tiene más dinero?" % (n1, dinero_svg(s1), n2, dinero_svg(s2)), ok, [n2 if ok == n1 else n1, "tienen lo mismo", "el que tiene más monedas"],
               "%s tiene %s y %s tiene %s: <b>%s</b>. No importa cuántas monedas hay, sino cuánto valen." % (n1, peso(t1), n2, peso(t2), ok))


ART = [("una paleta", 8, 15), ("un jugo", 12, 25), ("una torta", 25, 45), ("un cuaderno", 18, 35), ("una caja de colores", 35, 70), ("un balón", 60, 150),
       ("una mochila", 120, 190), ("un libro", 70, 180), ("unos tenis", 150, 199), ("una bolsa de pan", 20, 45)]


def s_cambio():
    nm, lo, hi = R.choice(ART)
    p = R.randint(lo, hi) * 100 + R.choice([0, 0, 0, 50])
    b = min(x for x in (2000, 5000, 10000, 20000, 50000) if x > p)
    ch = b - p
    return mcq("Compras %s de %s y pagas con un billete de %s. ¿Cuánto te dan de cambio?" % (nm, peso(p), peso(b)), peso(ch), [peso(b + p), peso(ch + 100), peso(ch - 100) if ch > 100 else peso(ch + 1000), peso(p)],
               "Cambio = lo que pagas − el precio: %s − %s = <b>%s</b>." % (peso(b), peso(p), peso(ch)))


def s_problema():
    t = R.choice(["varios", "varios", "dos", "ahorro", "falta"])
    p, _ = K.next()
    if t == "varios":
        nm, lo, hi, g = R.choice([("paletas", 8, 15, "una"), ("jugos", 12, 25, "uno"), ("tortas", 25, 45, "una"), ("cuadernos", 18, 35, "uno"), ("lápices", 5, 12, "uno"), ("conchas", 7, 14, "una")])
        k, pr = R.randint(2, 6), R.randint(lo, hi)
        return mcq("%s compra %d %s de %s cada %s. ¿Cuánto paga?" % (p, k, nm, peso(pr * 100), g), peso(k * pr * 100), [peso((k + pr) * 100), peso(pr * 100), peso((k * pr + pr) * 100)],
                   "%d × %s = <b>%s</b>." % (k, peso(pr * 100), peso(k * pr * 100)))
    if t == "dos":
        (a, pa, _), (b, pb, _) = R.sample(ART[:8], 2)
        pa, pb = R.randint(pa, pa + 20), R.randint(pb, pb + 20)
        return mcq("%s compra %s de %s y %s de %s. ¿Cuánto gasta?" % (p, a, peso(pa * 100), b, peso(pb * 100)), peso((pa + pb) * 100), [peso(abs(pa - pb) * 100), peso((pa + pb + 10) * 100), peso((pa + pb - 1) * 100)],
                   "%s + %s = <b>%s</b>." % (peso(pa * 100), peso(pb * 100), peso((pa + pb) * 100)))
    if t == "ahorro":
        a, w = R.choice([10, 15, 20, 25, 50]), R.randint(3, 9)
        return mcq("%s ahorra %s cada semana. ¿Cuánto junta en %d semanas?" % (p, peso(a * 100), w), peso(a * w * 100), [peso((a + w) * 100), peso(a * (w - 1) * 100), peso(a * w * 10)],
                   "%d × %s = <b>%s</b>." % (w, peso(a * 100), peso(a * w * 100)))
    nm, lo, hi = R.choice(ART[4:])
    pr = R.randint(lo, hi)
    tiene = R.randint(lo // 2, pr - 5)
    return mcq("%s quiere comprar %s de %s y tiene %s. ¿Cuánto le falta?" % (p, nm, peso(pr * 100), peso(tiene * 100)), peso((pr - tiene) * 100), [peso((pr + tiene) * 100), peso((pr - tiene + 10) * 100), peso(tiene * 100)],
               "%s − %s = <b>%s</b>." % (peso(pr * 100), peso(tiene * 100), peso((pr - tiene) * 100)))


unit("el-dinero", 16, "S",
     "Resuelve situaciones de compra y venta con monedas y billetes de pesos; cuenta, compara y equivale cantidades de dinero; calcula el cambio",
     "El dinero", "El dinero",
     "Ejercicios de matemáticas de 3.er grado de primaria: monedas y billetes de pesos, contar dinero, centavos, comparar precios, cambio y problemas de compras. 100 ejercicios con respuestas.",
     "$1 = 100 centavos", "Cuenta el valor, no las monedas.",
     ["En México usamos <b>pesos</b> ($) y <b>centavos</b>: $1 = 100 centavos. Dos monedas de 50 centavos son $1.",
      "Monedas: 50 centavos, $1, $2, $5, $10 y $20. Billetes: $20, $50, $100, $200, $500 y $1 000.",
      "Para contar dinero, empieza por lo que vale más y ve sumando. El <b>cambio</b> es lo que pagas menos lo que cuesta."],
     [("Un billete de $50, una moneda de $10 y dos de $2", ["50 + 10 = 60", "60 + 2 + 2 = 64"], "$64"), ("Cuesta $37 y pagas con $50", ["50 − 37"], "$13 de cambio")],
     [["Contar monedas en lugar de su valor", "3 monedas de $10 son $30, no $3."], ["Confundir 50 centavos con $50", "50 centavos es medio peso."], ["Restar al revés el cambio", "Cambio = lo que pagas − el precio."]],
     [("¿Cuántos centavos tiene un peso?", "Un peso tiene 100 centavos. Por eso $2.50 son 2 pesos y 50 centavos."),
      ("¿Cómo calculo el cambio?", "Resta el precio al dinero con el que pagas. Si pagas $100 por algo de $65, te dan $35.")],
     [("Contar dinero", [(s_contar, 20)]), ("Monedas, billetes y centavos", [(s_equiv, 20)]), ("Comparar", [(s_comparar, 20)]), ("El cambio", [(s_cambio, 20)]), ("Problemas de compras", [(s_problema, 20)])],
     63016, pic=dinero_svg(["b5000", 1000, 200, 200]))
