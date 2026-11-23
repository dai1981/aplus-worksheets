# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º y 2.º de Primaria: Dobles, mitades, tercios y cuartos (Sentido numérico)
build(lv): lv = 1 → «dobles-y-mitades» hasta 20 con dibujos; lv = 2 → «mitad-tercio-y-cuarto»: partes iguales,
la mitad, la tercera parte y la cuarta parte de un número, dobles.
Errores: partir en partes que no son iguales, confundir doble y mitad, contar las partes sin colorear.
"""
import random
from es_common import mcq, mix, lesson, make_unit, tira, circulo, fig
import es_pics as P

R = None
LV = 2
PARTE = {2: "un medio (la mitad)", 3: "un tercio", 4: "un cuarto"}
NOMBRES = ["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo", "Vega", "Leo", "Alba", "Mario"]


def s_doble():
    n = R.randint(1, 10) if LV == 1 else R.randint(6, 50)
    if LV == 1:
        kind = R.choice(P.KINDS)
        return mcq(P.dos_grupos(n, kind, n) + "¿Cuál es el doble de %d?" % n, str(2 * n), [str(n + 1), str(n), str(2 * n + 1)], "%d + %d = <b>%d</b>." % (n, n, 2 * n))
    return mcq("¿Cuál es el doble de %d?" % n, str(2 * n), [str(n + 2), str(n // 2) if n % 2 == 0 else str(2 * n + 10), str(2 * n + 10), str(2 * n - 2)], "%d + %d = <b>%d</b>." % (n, n, 2 * n))


def s_mitad():
    n = R.randint(1, 10) if LV == 1 else R.randint(3, 50)
    if LV == 1:
        kind = R.choice(P.KINDS)
        return mcq(P.fila(2 * n, kind, 10) + "Repartimos %s entre 2 niños por igual. ¿Cuántas le tocan a cada uno?" % P.cosas(kind, 2 * n) if P.fem(kind) else
                   P.fila(2 * n, kind, 10) + "Repartimos %s entre 2 niños por igual. ¿Cuántos le tocan a cada uno?" % P.cosas(kind, 2 * n),
                   str(n), [str(2 * n), str(n + 1), str(n - 1) if n > 1 else str(n + 2)], "La mitad de %d es <b>%d</b>, porque %d + %d = %d." % (2 * n, n, n, n, 2 * n))
    return mcq("¿Cuál es la mitad de %d?" % (2 * n), str(n), [str(4 * n), str(n + 1), str(2 * n - 2), str(n - 1)], "%d + %d = %d: la mitad es <b>%d</b>." % (n, n, 2 * n, n))


def s_parte():
    d = R.choice([2, 3, 4]) if LV == 2 else 2
    if R.random() < 0.45:
        if LV == 1:
            d = R.choice([2, 4])
        k = R.randint(1, d - 1) if d > 2 else 1
        pic = R.choice([tira, circulo])(d, k)
        t = R.choice(["partes", "color", "blanco"])
        if t == "partes":
            return mcq(pic + "¿En cuántas partes iguales está partida la figura?", str(d), [str(x) for x in (1, 2, 3, 4, 5, 6) if x != d], "Contamos todas las partes: <b>%d</b>." % d)
        if t == "color":
            return mcq(pic + "¿Cuántas partes están coloreadas?", str(k), [str(x) for x in (0, 1, 2, 3, 4) if x != k], "Contamos las partes coloreadas: <b>%d</b>." % k)
        return mcq(pic + "¿Cuántas partes faltan por colorear?", str(d - k), [str(x) for x in (0, 1, 2, 3, 4) if x != d - k], "%d − %d = <b>%d</b>." % (d, k, d - k))
    if LV == 1:
        d = R.choice([2, 2, 4])
        k = 1
        pic = R.choice([tira, circulo])(d, k)
        ok = "la mitad" if d == 2 else "un cuarto"
        return mcq(pic + "¿Qué parte está coloreada?", ok, ["la mitad" if d == 4 else "un cuarto", "todo", "nada"], "La figura está partida en %d partes iguales y hay 1 coloreada: <b>%s</b>." % (d, ok))
    k = R.choice([1, 1, d - 1]) if d > 2 else 1
    pic = R.choice([tira, circulo])(d, k)
    if k == 1:
        ok = PARTE[d]
        return mcq(pic + "¿Qué parte está coloreada?", ok, [PARTE[x] for x in (2, 3, 4) if x != d] + ["un quinto"], "Partes iguales: %d. Coloreada: 1. Es <b>%s</b>." % (d, ok))
    ok = {3: "dos tercios", 4: "tres cuartos"}[d]
    return mcq(pic + "¿Qué parte está coloreada?", ok, ["dos tercios" if d == 4 else "tres cuartos", "un tercio" if d == 3 else "un cuarto", "dos cuartos" if d == 4 else "un medio"],
               "Partes iguales: %d. Coloreadas: %d. Es <b>%s</b>." % (d, k, ok))


def s_cuantas():
    d = R.choice([2, 3, 4])
    q, a = {2: ("¿En cuántas partes iguales partes algo para sacar la mitad?", "2"), 3: ("¿En cuántas partes iguales partes algo para sacar un tercio?", "3"),
            4: ("¿En cuántas partes iguales partes algo para sacar un cuarto?", "4")}[d]
    if LV == 1:
        return None
    t = R.choice(["cuantas", "ter", "cua"])
    if t == "cuantas":
        return mcq(q, a, [str(x) for x in (1, 2, 3, 4, 5) if str(x) != a], "Respuesta: <b>%s</b>." % a)
    n = R.randint(2, 10) * (3 if t == "ter" else 4)
    if n > 40:
        return None
    dd = 3 if t == "ter" else 4
    nm = "la tercera parte" if dd == 3 else "la cuarta parte"
    kind = R.choice(P.KINDS)
    pic = P.grupos(dd, n // dd, kind) if n <= 24 else ""
    return mcq(pic + "¿Cuánto es %s de %d?" % (nm, n), str(n // dd), [str(n // 2) if n % 2 == 0 else str(n // dd + 2), str(n - dd), str(n // dd + 1)], "Repartimos %d en %d partes iguales: %d : %d = <b>%d</b>." % (n, dd, n, dd, n // dd))


def s_problema():
    p = R.choice(NOMBRES)
    t = R.choice(["mitad", "doble", "doble2"] + (["tercio", "cuarto"] if LV == 2 else []))
    if t == "mitad":
        n = R.randint(2, 10) * 2 if LV == 1 else R.randint(6, 40) * 2
        return mcq("%s tiene %d cromos y regala la mitad a su hermana. ¿Cuántos cromos regala?" % (p, n), str(n // 2), [str(n * 2), str(n - 2), str(n // 2 + 1)], "La mitad de %d es <b>%d</b>." % (n, n // 2))
    if t == "doble":
        n = R.randint(2, 10) if LV == 1 else R.randint(10, 45)
        return mcq("%s ha leído %d páginas y su hermano ha leído el doble. ¿Cuántas páginas ha leído su hermano?" % (p, n), str(2 * n), [str(n + 2), str(n // 2) if n % 2 == 0 else str(2 * n + 1), str(n)], "El doble de %d es %d + %d = <b>%d</b>." % (n, n, n, 2 * n))
    if t == "doble2":
        n = R.randint(2, 10) if LV == 1 else R.randint(10, 45)
        return mcq("En una caja hay %d lápices. En otra caja hay el doble. ¿Cuántos lápices hay en la otra caja?" % n, str(2 * n), [str(n + 2), str(n), str(2 * n + 2)], "El doble de %d es <b>%d</b>." % (n, 2 * n))
    dd = 3 if t == "tercio" else 4
    n = R.randint(2, 10) * dd
    return mcq("Una tarta tiene %d fresas. %s se come %s. ¿Cuántas fresas se come?" % (n, p, "la tercera parte" if dd == 3 else "la cuarta parte"), str(n // dd), [str(n // 2) if n % 2 == 0 and n // 2 != n // dd else str(n - dd), str(n - n // dd), str(n // dd + 1)],
               "%d : %d = <b>%d</b>." % (n, dd, n // dd))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(30009 + lv * 1000)
    seen = set()
    if lv == 1:
        sets = [("El doble", mix(R, seen, [(s_doble, 20)])), ("La mitad", mix(R, seen, [(s_mitad, 20)])), ("La mitad coloreada", mix(R, seen, [(s_parte, 6), (s_doble, 7), (s_mitad, 7)])),
                ("Dobles y mitades", mix(R, seen, [(s_doble, 6), (s_mitad, 6), (s_problema, 8)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["El <b>doble</b> de un número es sumarlo dos veces: el doble de 4 es 4 + 4 = 8.", "La <b>mitad</b> es repartir en 2 partes iguales: la mitad de 8 es 4.", "Doble y mitad son contrarios: el doble de 4 es 8 y la mitad de 8 es 4."]
        ex = [("El doble de 6", ["6 + 6"], "12"), ("La mitad de 10", ["5 + 5 = 10"], "5")]
        mist = [["Confundir doble y mitad", "Doble: más grande. Mitad: más pequeño."], ["Repartir en partes que no son iguales", "En la mitad, las dos partes tienen lo mismo."], ["Sumar 2 en vez de doblar", "El doble de 7 es 14, no 9."]]
        kb, ks = "Doble de 4 = 8; mitad de 8 = 4", "Doble: suma el número dos veces."
        meta = "Fichas de matemáticas de 1.º de Primaria: el doble y la mitad de un número hasta 20 con dibujos y problemas. 100 ejercicios con soluciones."
        std = "Dobles y mitades de números hasta 20; repartos en dos partes iguales"
        slug, title, short = "dobles-y-mitades", "Dobles y mitades", "Dobles y mitades"
        pic = P.dos_grupos(4, "apple", 4)
    else:
        sets = [("Partes iguales", mix(R, seen, [(s_parte, 20)])), ("La mitad", mix(R, seen, [(s_mitad, 20)])), ("La tercera y la cuarta parte", mix(R, seen, [(s_cuantas, 20)])),
                ("El doble", mix(R, seen, [(s_doble, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        think = ["Para hacer <b>medios</b>, <b>tercios</b> o <b>cuartos</b>, se parte en 2, 3 o 4 partes <b>iguales</b>.", "La mitad de 12 es 6; la tercera parte de 12 es 4; la cuarta parte de 12 es 3.",
                 "El doble es lo contrario de la mitad: el doble de 6 es 12."]
        ex = [("La tercera parte de 15", ["15 en 3 partes iguales", "5 + 5 + 5 = 15"], "5"), ("Un círculo en 4 partes iguales con 1 coloreada", ["4 partes, 1 coloreada"], "un cuarto")]
        mist = [["Partes que no son iguales", "Medios, tercios y cuartos son partes iguales."], ["Contar las partes sin colorear", "Cuenta las coloreadas."], ["Confundir tercio y cuarto", "Tercio: 3 partes. Cuarto: 4 partes."]]
        kb, ks = "Mitad 2, tercio 3, cuarto 4 partes", "Siempre partes iguales."
        meta = "Fichas de matemáticas de 2.º de Primaria: partes iguales, la mitad, la tercera y la cuarta parte de un número, dobles y problemas. 100 ejercicios con soluciones."
        std = "La mitad, la tercera parte y la cuarta parte como partes iguales de una unidad o de una cantidad; dobles"
        slug, title, short = "mitad-tercio-y-cuarto", "Mitad, tercio y cuarto", "Mitad, tercio y cuarto"
        pic = circulo(4, 1)
    body = lesson(think, ex, mist, pic)
    faq = [("¿Qué es la mitad?", "Es cada una de las dos partes iguales en que se reparte algo. La mitad de 10 es 5."), ("¿Qué es el doble?", "Es sumar un número dos veces. El doble de 7 es 14.")]
    make_unit(R, slug, "N", std, title, short, meta, kb, ks, body, faq, sets, 8 if lv == 2 else 6, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(2)
