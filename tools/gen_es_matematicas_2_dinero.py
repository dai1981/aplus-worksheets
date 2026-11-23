# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: El dinero (Sentido de la medida)
build(lv): lv = 1 → «monedas-y-billetes»: monedas de 1 y 2 € y billetes de 5, 10 y 20 €, contar, comparar, ¿tengo bastante?, compras sencillas;
lv = 2 → «el-dinero»: también céntimos (10, 20 y 50 c), 1 € = 100 céntimos, compras y vueltas hasta 100 €.
Errores: contar monedas sin mirar su valor, pensar que un billete vale lo mismo que una moneda, restar mal las vueltas.
"""
import random
from es_common import mcq, mix, lesson, make_unit, eur, dinero_svg

R = None
LV = 2
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]
COSAS = [("un cuento", 6), ("una pelota", 8), ("un bocadillo", 3), ("un zumo", 2), ("un yoyó", 4), ("una libreta", 2), ("un puzle", 9), ("unos rotuladores", 5),
         ("una cometa", 12), ("un peluche", 15), ("una gorra", 7), ("una entrada al cine", 6)]


def piezas():
    if LV == 1:
        it = [R.choice([100, 200, 500, 1000]) for _ in range(R.randint(2, 4))]
        return it if sum(it) <= 2000 else None
    k = R.choice(["mon", "mix", "cent"])
    if k == "cent":
        it = [R.choice([10, 20, 50]) for _ in range(R.randint(3, 6))]
    elif k == "mon":
        it = [R.choice([50, 100, 200]) for _ in range(R.randint(3, 5))]
    else:
        it = [R.choice([500, 1000, 2000])] + [R.choice([10, 20, 50, 100, 200]) for _ in range(R.randint(2, 4))]
    return it


def s_contar():
    it = piezas()
    if not it:
        return None
    it.sort(reverse=True)
    t = sum(it)
    return mcq(dinero_svg(it) + "¿Cuánto dinero hay?", eur(t, LV == 2), [eur(t + 100, LV == 2), eur(t - 100, LV == 2) if t > 100 else eur(t + 200, LV == 2), eur(len(it) * 100, LV == 2), eur(t + 10, LV == 2) if LV == 2 else eur(t + 300)],
               "Empezamos por lo que vale más: <b>%s</b>." % eur(t, LV == 2))


def s_valor():
    if LV == 1:
        q, a, w = R.choice([("¿Cuántas monedas de 1 € valen lo mismo que una de 2 €?", "2", ["1", "3", "5"]),
                            ("¿Cuántas monedas de 1 € valen lo mismo que un billete de 5 €?", "5", ["2", "1", "10"]),
                            ("¿Cuántos billetes de 5 € valen lo mismo que uno de 10 €?", "2", ["5", "1", "10"]),
                            ("¿Cuántos billetes de 10 € valen lo mismo que uno de 20 €?", "2", ["10", "1", "20"]),
                            ("¿Cuántas monedas de 2 € valen lo mismo que un billete de 10 €?", "5", ["2", "10", "4"]),
                            ("¿Qué vale más, un billete de 5 € o una moneda de 2 €?", "el billete de 5 €", ["la moneda de 2 €", "valen lo mismo", "no se puede saber"]),
                            ("¿Qué vale más, tres monedas de 1 € o una de 2 €?", "tres monedas de 1 €", ["una de 2 €", "valen lo mismo", "no se puede saber"]),
                            ("¿Cuál es una moneda?", "2 €", ["5 €", "10 €", "20 €"]), ("¿Cuál es un billete?", "10 €", ["1 €", "2 €", "50 céntimos"]),
                            ("¿Cuánto son 2 monedas de 2 € y 1 moneda de 1 €?", "5 €", ["3 €", "4 €", "6 €"]),
                            ("¿Cuánto son 2 billetes de 5 €?", "10 €", ["7 €", "5 €", "25 €"]), ("¿Cuánto son 1 billete de 10 € y 1 de 5 €?", "15 €", ["2 €", "11 €", "105 €"])])
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    k = R.choice(["cent", "euro", "cuantas", "falta"])
    if k == "cent":
        e = R.randint(1, 9)
        c = R.choice([0, 10, 20, 50])
        v = e * 100 + c
        return mcq("¿Cuántos céntimos son %s?" % eur(v), "%d céntimos" % v, ["%d céntimos" % (e + c) if c else "%d céntimos" % (e * 10), "%d céntimos" % (v * 10), "%d céntimos" % (v + 100)], "1 € = 100 céntimos: <b>%d céntimos</b>." % v)
    if k == "euro":
        e = R.randint(1, 5)
        return mcq("¿Cuántos euros son %d céntimos?" % (100 * e), "%d €" % e, ["%d €" % (10 * e), "%d €" % (100 * e), "%d €" % (e + 1)], "100 céntimos = 1 €: <b>%d €</b>." % e)
    if k == "cuantas":
        v = R.choice([10, 20, 50])
        t = R.choice([100, 200])
        return mcq("¿Cuántas monedas de %d céntimos hacen %s?" % (v, eur(t)), str(t // v), [str(t // v + 1), str(v), str(t // v * 2)], "%s = %d céntimos: <b>%d</b> monedas." % (eur(t), t, t // v))
    c = R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90])
    return mcq("Tengo %d céntimos. ¿Cuánto me falta para tener 1 €?" % c, "%d céntimos" % (100 - c), ["%d céntimos" % c if c != 50 else "40 céntimos", "%d céntimos" % (100 - c + 10), "%d céntimos" % (10 - c // 10)], "100 − %d = <b>%d céntimos</b>." % (c, 100 - c))


def s_bastante():
    it = piezas()
    if not it:
        return None
    it.sort(reverse=True)
    t = sum(it)
    if LV == 1:
        thing, pr = R.choice(COSAS)
        pr *= 100
    else:
        thing, pr = R.choice(COSAS)
        pr = pr * 100 + R.choice([0, 0, 50, 20, 80])
    if t == pr:
        return None
    ok = "sí, y me sobran %s" % eur(t - pr, LV == 2) if t > pr else "no, me faltan %s" % eur(pr - t, LV == 2)
    return mcq(dinero_svg(it) + "Quiero comprar %s que %s %s. ¿Tengo bastante dinero?" % (thing, "cuestan" if thing.startswith("unos") else "cuesta", eur(pr)), ok,
               ["sí, y me sobran %s" % eur(abs(t - pr), LV == 2) if t < pr else "no, me faltan %s" % eur(abs(t - pr), LV == 2), "sí, justo", "no, me faltan %s" % eur(pr, LV == 2) if t < pr else "sí, y me sobran %s" % eur(t, LV == 2)],
               "Tengo %s y cuesta %s: <b>%s</b>." % (eur(t, LV == 2), eur(pr), ok))


def s_compra():
    (a, pa), (b, pb) = R.sample(COSAS, 2)
    p = R.choice(NOMBRES)
    if LV == 1:
        if pa + pb > 20:
            return None
        t = R.choice(["juntos", "vueltas"])
        if t == "juntos":
            return mcq("%s cuesta %d € y %s cuesta %d €. ¿Cuánto cuestan juntos?" % (a[0].upper() + a[1:], pa, b, pb), "%d €" % (pa + pb), ["%d €" % abs(pa - pb) if pa != pb else "%d €" % (pa + pb + 2), "%d €" % (pa + pb + 1), "%d €" % (pa + pb - 1)],
                       "%d + %d = <b>%d €</b>." % (pa, pb, pa + pb))
        pay = 10 if pa < 10 else 20
        return mcq("%s compra %s de %d € y paga con un billete de %d €. ¿Cuánto le devuelven?" % (p, a, pa, pay), "%d €" % (pay - pa), ["%d €" % (pay + pa), "%d €" % pa if pa != pay - pa else "%d €" % (pa + 1), "%d €" % (pay - pa + 1)],
                   "%d − %d = <b>%d €</b>." % (pay, pa, pay - pa))
    pa, pb = pa * 100 + R.choice([0, 50, 20]), pb * 100 + R.choice([0, 50, 30])
    t = R.choice(["juntos", "vueltas", "dos"])
    if t == "juntos":
        s = pa + pb
        return mcq("%s cuesta %s y %s cuesta %s. ¿Cuánto cuestan juntos?" % (a[0].upper() + a[1:], eur(pa), b, eur(pb)), eur(s), [eur(s + 100), eur(abs(pa - pb)), eur(s - 10)], "%s + %s = <b>%s</b>." % (eur(pa), eur(pb), eur(s)))
    if t == "dos":
        if pa % 100 or a.startswith("unos"):
            return None
        return mcq("Cada %s cuesta %s. %s compra dos. ¿Cuánto paga?" % (a.split(" ", 1)[1], eur(pa), p), eur(2 * pa), [eur(pa + 200), eur(pa), eur(2 * pa + 100)], "%s + %s = <b>%s</b>." % (eur(pa), eur(pa), eur(2 * pa)))
    pay = 1000 if pa < 1000 else 2000
    return mcq("%s compra %s de %s y paga con %s. ¿Cuánto le devuelven?" % (p, a, eur(pa), eur(pay)), eur(pay - pa, True), [eur(pay - pa + 100, True), eur(pa), eur(pay - pa - 10, True)], "%s − %s = <b>%s</b>." % (eur(pay), eur(pa), eur(pay - pa, True)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30014 + lv * 1000)
    seen = set()
    sets = [("Contar dinero", mix(R, seen, [(s_contar, 20)])), ("Monedas y billetes" if lv == 1 else "Euros y céntimos", mix(R, seen, [(s_valor, 12 if lv == 1 else 20)] + ([(s_contar, 8)] if lv == 1 else []))),
            ("¿Tengo bastante?", mix(R, seen, [(s_bastante, 20)])), ("Compras", mix(R, seen, [(s_compra, 20)])), ("Repaso", mix(R, seen, [(s_contar, 8), (s_bastante, 6), (s_compra, 6)]))]
    if lv == 1:
        think = ["Hay <b>monedas</b> de 1 € y de 2 €, y <b>billetes</b> de 5 €, 10 € y 20 €.", "Para contar, empieza por lo que vale más y ve sumando.", "Una moneda de 2 € vale lo mismo que dos de 1 €."]
        ex = [("Un billete de 5 € y dos monedas de 2 €", ["5 + 2 + 2"], "9 €"), ("Cuesta 7 € y pago con 10 €", ["10 − 7"], "me devuelven 3 €")]
        kb, ks = "Mira cuánto vale cada moneda", "Empieza por el billete más grande."
        meta = "Fichas de matemáticas de 1.º de Primaria: monedas de 1 y 2 € y billetes de 5, 10 y 20 €, contar dinero y compras sencillas. 100 ejercicios con soluciones."
        std = "Monedas y billetes de euro hasta 20 €; valor y equivalencias; compras sencillas"
        slug, title, short = "monedas-y-billetes", "Monedas y billetes", "El dinero"
        pic = dinero_svg([500, 200, 200])
        sort = 10
    else:
        think = ["<b>1 € = 100 céntimos</b>. Hay monedas de 10, 20 y 50 céntimos y de 1 y 2 €.", "3,50 € son 3 euros y 50 céntimos.", "Las <b>vueltas</b> son lo que pagas menos lo que cuesta."]
        ex = [("Un billete de 5 €, una moneda de 1 € y una de 50 céntimos", ["5 + 1 = 6 €", "+ 50 céntimos"], "6,50 €"), ("Cuesta 3,50 € y pago con 5 €", ["5 − 3,50"], "1,50 €")]
        kb, ks = "1 € = 100 céntimos", "Cuenta primero los billetes."
        meta = "Fichas de matemáticas de 2.º de Primaria: contar monedas y billetes, euros y céntimos, ¿tengo bastante?, compras y vueltas. 100 ejercicios con soluciones."
        std = "Monedas y billetes de euro; equivalencia entre euros y céntimos; compras y vueltas"
        slug, title, short = "el-dinero", "El dinero: euros y céntimos", "El dinero"
        pic = dinero_svg([500, 100, 50])
        sort = 13
    mist = [["Contar las monedas sin mirar su valor", "Tres monedas no son 3 €: mira cuánto vale cada una."], ["Pensar que un billete de 5 € vale lo mismo que una moneda", "El billete de 5 € vale 5 monedas de 1 €."], ["Restar mal las vueltas", "Comprueba: precio + vueltas = lo que pagas."]]
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué monedas de euro hay?", "Monedas de 1, 2, 5, 10, 20 y 50 céntimos y de 1 y 2 euros."), ("¿Cómo se calculan las vueltas?", "Se resta el precio de lo que se ha pagado.")]
    make_unit(R, slug, "M", std, title, short, meta, kb, ks, body, faq, sets, sort, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
