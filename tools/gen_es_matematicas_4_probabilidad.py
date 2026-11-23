# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Probabilidad (Sentido estocástico)
Sucesos seguros, posibles e imposibles; más probable, menos probable e igual de probable; bolsas con bolas, ruletas y dados;
contar los casos posibles y favorables; expresar la probabilidad con una fracción sencilla; experimentos repetidos.
Errores: pensar que lo poco probable es imposible, comparar el número de bolas de un color sin mirar el total.
"""
import random
from es_common import mcq, mix, lesson, make_unit, fr, bank
import math

R = random.Random(44025)
COL = {"rojas": "#c0392b", "azules": "#1f5fbf", "verdes": "#2e7d32", "amarillas": "#f2c14e"}
SING = {"rojas": "roja", "azules": "azul", "verdes": "verde", "amarillas": "amarilla"}


def bolsa(cnt):
    s = ["<path d='M40 40 Q20 160 110 170 Q200 160 180 40 Z' fill='#f3ead9' stroke='#333' stroke-width='2'/>", "<rect x='70' y='26' width='80' height='16' rx='6' fill='#e0cfa8' stroke='#333'/>"]
    balls = [c for c, n in cnt for _ in range(n)]
    R2 = random.Random(len(balls) * 7 + sum(ord(c[0]) for c in balls))
    R2.shuffle(balls)
    for i, c in enumerate(balls):
        x = 62 + (i % 6) * 19 + (8 if (i // 6) % 2 else 0)
        y = 64 + (i // 6) * 20
        s.append("<circle cx='%d' cy='%d' r='8' fill='%s' stroke='#333'/>" % (x, y, COL[c]))
    return "<div class='fig'><svg viewBox='0 0 220 180' width='220' role='img' aria-label='bolsa con bolas de colores'>%s</svg></div>" % "".join(s)


def ruleta(secs):
    s = []
    n = len(secs)
    cx, cy, r = 100, 100, 80
    for i, c in enumerate(secs):
        a1, a2 = math.radians(-90 + 360.0 * i / n), math.radians(-90 + 360.0 * (i + 1) / n)
        x1, y1, x2, y2 = cx + r * math.cos(a1), cy + r * math.sin(a1), cx + r * math.cos(a2), cy + r * math.sin(a2)
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='#333' stroke-width='1.5'/>" % (cx, cy, x1, y1, r, r, x2, y2, COL[c]))
    s.append("<polygon points='100,8 92,-4 108,-4' fill='#333' transform='translate(0,6)'/>")
    return "<div class='fig'><svg viewBox='0 0 200 200' width='200' role='img' aria-label='ruleta de colores'>%s</svg></div>" % "".join(s)


def s1_sucesos():
    k = R.choice(["bolsa", "bolsa", "dado", "bank"])
    if k == "bolsa":
        cs = R.sample(list(COL), R.randint(1, 3))
        cnt = [(c, R.randint(1, 6)) for c in cs]
        q = R.choice(["seguro", "imposible", "posible"])
        if q == "seguro" and len(cs) == 1:
            c = cs[0]
        elif q == "seguro":
            return None
        elif q == "imposible":
            c = R.choice([x for x in COL if x not in cs])
        else:
            if len(cs) < 2:
                return None
            c = R.choice(cs)
        ans = "seguro" if len(cs) == 1 and c in cs else "imposible" if c not in cs else "posible"
        return mcq(bolsa(cnt) + "Sacas una bola sin mirar. Sacar una bola %s es…" % SING[c], ans, [x for x in ("seguro", "posible", "imposible", "muy probable siempre") if x != ans],
                   "%s" % {"seguro": "Todas las bolas son %s: es <b>seguro</b>." % c, "imposible": "No hay bolas %s: es <b>imposible</b>." % c, "posible": "Hay bolas %s y de otros colores: es <b>posible</b>." % c}[ans])
    if k == "dado":
        q, a = R.choice([("sacar un 7", "imposible"), ("sacar un número menor que 7", "seguro"), ("sacar un 6", "posible"), ("sacar un número par", "posible"), ("sacar un 0", "imposible"),
                         ("sacar un número de 1 a 6", "seguro"), ("sacar un número mayor que 4", "posible"), ("sacar un número mayor que 6", "imposible")])
        return mcq("Lanzas un dado normal de 6 caras. ¿Cómo es el suceso «%s»?" % q, a, [x for x in ("seguro", "posible", "imposible", "probable siempre") if x != a],
                   "El dado tiene los números del 1 al 6: es <b>%s</b>." % a)
    return bank(R, [
        ("Mañana el sol saldrá por el este. Es un suceso…", "seguro", ["imposible", "posible", "poco probable"]),
        ("Un gato hablará en clase de matemáticas. Es un suceso…", "imposible", ["seguro", "posible", "muy probable"]),
        ("Al lanzar una moneda sale cara. Es un suceso…", "posible", ["seguro", "imposible", "cierto siempre"]),
        ("En agosto nevará en Sevilla. Es un suceso…", "muy poco probable", ["seguro", "muy probable", "igual de probable que no"]),
        ("Mañana será el día después de hoy. Es un suceso…", "seguro", ["posible", "imposible", "poco probable"]),
        ("En un sorteo de 30 alumnos, te toca a ti el premio. Es un suceso…", "posible pero poco probable", ["seguro", "imposible", "muy probable"]),
    ], "suc")()


def s2_comparar():
    cs = R.sample(list(COL), R.randint(2, 3))
    ns = R.sample(range(1, 8), len(cs))
    cnt = list(zip(cs, ns))
    k = R.choice(["mas", "menos", "par"])
    if k == "mas":
        c = cs[ns.index(max(ns))]
        return mcq(bolsa(cnt) + "Sacas una bola sin mirar. ¿De qué color es más probable que salga?", SING[c], [SING[x] for x in cs if x != c] + ["todos igual de probables"],
                   "Hay más bolas %s (%d): es más probable <b>%s</b>." % (c, max(ns), SING[c]))
    if k == "menos":
        c = cs[ns.index(min(ns))]
        return mcq(bolsa(cnt) + "Sacas una bola sin mirar. ¿De qué color es menos probable que salga?", SING[c], [SING[x] for x in cs if x != c] + ["todos igual de probables"],
                   "Hay menos bolas %s (%d): es menos probable <b>%s</b>." % (c, min(ns), SING[c]))
    a, b = R.sample(list(COL), 2)
    n = R.randint(2, 6)
    cnt = [(a, n), (b, n)] + ([(R.choice([x for x in COL if x not in (a, b)]), R.randint(1, 6))] if R.random() < 0.5 else [])
    return mcq(bolsa(cnt) + "¿Es más probable sacar una bola %s o una %s?" % (SING[a], SING[b]), "igual de probable", ["más probable %s" % SING[a], "más probable %s" % SING[b], "imposible las dos"],
               "Hay %d de cada color: <b>igual de probable</b>." % n)


def s2_ruleta():
    n = R.choice([4, 6, 8])
    cs = R.sample(list(COL), R.randint(2, 3))
    secs = [R.choice(cs) for _ in range(n)]
    cn = {c: secs.count(c) for c in cs if secs.count(c)}
    if len(cn) < 2 or len(set(cn.values())) < len(cn):
        return None
    c = max(cn, key=cn.get)
    return mcq(ruleta(secs) + "Giras la ruleta. ¿En qué color es más probable que pare la flecha?", "en el %s" % SING[c].replace("roja", "rojo").replace("amarilla", "amarillo"),
               ["en el %s" % SING[x].replace("roja", "rojo").replace("amarilla", "amarillo") for x in cn if x != c] + ["en todos igual", "no se puede saber"],
               "El color %s ocupa más partes (%d de %d)." % (SING[c].replace("roja", "rojo").replace("amarilla", "amarillo"), cn[c], n))


def s3_fraccion():
    k = R.choice(["bolsa", "bolsa", "dado", "ruleta"])
    if k == "bolsa":
        cs = R.sample(list(COL), R.randint(2, 3))
        ns = [R.randint(1, 6) for _ in cs]
        tot = sum(ns)
        i = R.randrange(len(cs))
        return mcq(bolsa(list(zip(cs, ns))) + "Sacas una bola sin mirar. ¿Qué probabilidad hay de que sea %s?" % SING[cs[i]], fr(ns[i], tot),
                   [fr(ns[i], tot - ns[i]) if tot - ns[i] != ns[i] else fr(ns[i], tot + 1), fr(tot - ns[i], tot), fr(1, ns[i]) if ns[i] > 1 else fr(1, tot + 1), fr(ns[i], 10) if tot != 10 else fr(ns[i] + 1, tot)],
                   "Casos favorables: %d; casos posibles: %d. Probabilidad: <b>%s</b>." % (ns[i], tot, fr(ns[i], tot)))
    if k == "dado":
        q, f, n = R.choice([("un 3", 1, "1 número"), ("un número par", 3, "3 números (2, 4 y 6)"), ("un número mayor que 4", 2, "2 números (5 y 6)"), ("un número menor que 3", 2, "2 números (1 y 2)"),
                            ("un número impar", 3, "3 números (1, 3 y 5)"), ("un 5 o un 6", 2, "2 números"), ("un número menor que 5", 4, "4 números (1, 2, 3 y 4)")])
        return mcq("Lanzas un dado de 6 caras. ¿Qué probabilidad hay de sacar %s?" % q, fr(f, 6), [fr(1, f) if f > 1 else fr(1, 2), fr(6 - f, 6), fr(f, 12), fr(f + 1, 6) if f < 5 else fr(1, 6)],
                   "Casos favorables: %s; casos posibles: 6. Probabilidad: <b>%s</b>." % (n, fr(f, 6)))
    n = R.choice([4, 5, 6, 8])
    m = R.randint(1, n - 1)
    return mcq("Una ruleta tiene %d partes iguales y %d son verdes. ¿Qué probabilidad hay de que salga verde?" % (n, m), fr(m, n), [fr(n - m, n), fr(m, n - m), fr(1, m) if m > 1 else fr(1, n + 1), fr(m, n + 2)],
               "Favorables: %d; posibles: %d. Probabilidad: <b>%s</b>." % (m, n, fr(m, n)))


def s4_casos():
    k = R.choice(["moneda", "dado", "menu", "ropa", "letras"])
    if k == "moneda":
        return mcq("Lanzas una moneda. ¿Cuántos resultados posibles hay?", "2", ["1", "3", "6"], "Cara o cruz: <b>2</b>.")
    if k == "dado":
        return mcq("Lanzas un dado de 6 caras. ¿Cuántos resultados posibles hay?", "6", ["1", "5", "12"], "1, 2, 3, 4, 5 o 6: <b>6</b>.")
    if k == "menu":
        a, b = R.randint(2, 4), R.randint(2, 4)
        return mcq("En el comedor hay %d primeros platos y %d postres. ¿Cuántos menús distintos de primero y postre puedes elegir?" % (a, b), str(a * b), [str(a + b), str(a * b + 1), str(max(a, b)), str(a * b * 2)],
                   "Con cada primero puedes elegir %d postres: %d × %d = <b>%d</b>." % (b, a, b, a * b))
    if k == "ropa":
        a, b = R.randint(2, 5), R.randint(2, 4)
        return mcq("%s tiene %d camisetas y %d pantalones. ¿De cuántas formas distintas puede vestirse con una camiseta y un pantalón?" % (R.choice(["Lucía", "Hugo", "Sofía", "Mateo"]), a, b), str(a * b), [str(a + b), str(a * b - 1), str(a * b + a), str(a * a)] if a * a != a * b else [str(a + b), str(a * b - 1), str(a * b + a), str(a * b * 2)],
                   "%d × %d = <b>%d</b>." % (a, b, a * b))
    w = R.choice(["SOL", "MAR", "PAN", "LUZ"])
    return mcq("¿De cuántas formas distintas puedes ordenar las tres letras de la palabra %s (sin repetir letras)?" % w, "6", ["3", "9", "4"],
               "Para la primera posición hay 3 letras, para la segunda 2 y para la tercera 1: 3 × 2 × 1 = <b>6</b>.")


def s5_experimento():
    n = R.choice([20, 30, 40, 50])
    cs = R.sample(list(COL), 3)
    a = R.randint(n // 3, n // 2 + 5)
    b = R.randint(2, n - a - 2)
    c = n - a - b
    if c <= 0 or len({a, b, c}) < 3:
        return None
    res = list(zip(cs, [a, b, c]))
    tb = "<table class='sn-table' style='width:auto'><thead><tr><th>Color</th><th>Veces</th></tr></thead><tbody>%s</tbody></table>" % "".join("<tr><td>%s</td><td>%d</td></tr>" % (SING[x], v) for x, v in res)
    k = R.choice(["mas", "menos", "total"])
    if k == "total":
        return mcq(tb + "Se ha sacado una bola de una bolsa %d veces (devolviéndola cada vez) y se ha anotado su color. Sale %s %d veces y %s %d veces. ¿Cuántas veces salió %s?" % (n, SING[cs[0]], a, SING[cs[1]], b, SING[cs[2]]),
                   str(c), [str(a + b), str(n), str(c + 1), str(c - 1) if c > 1 else str(c + 2)], "%d − %d − %d = <b>%d</b>." % (n, a, b, c))
    f = max if k == "mas" else min
    m = f(res, key=lambda t: t[1])[0]
    return mcq(tb + "Se ha sacado una bola de una bolsa %d veces (devolviéndola cada vez). ¿De qué color crees que hay %s bolas en la bolsa?" % (n, "más" if k == "mas" else "menos"), SING[m],
               [SING[x] for x in cs if x != m] + ["no hay ninguna pista"], "El color que %s veces ha salido es el %s: probablemente hay %s bolas <b>%s</b>." % ("más" if k == "mas" else "menos", SING[m].replace("roja", "rojo").replace("amarilla", "amarillo"), "más" if k == "mas" else "menos", m))


def main():
    seen = set()
    sets = [
        ("Seguro, posible o imposible", mix(R, seen, [(s1_sucesos, 20)])),
        ("Más o menos probable", mix(R, seen, [(s2_comparar, 12), (s2_ruleta, 8)])),
        ("Contar los casos", mix(R, seen, [(s4_casos, 10), (s3_fraccion, 10)])),
        ("La probabilidad como fracción", mix(R, seen, [(s3_fraccion, 20)])),
        ("Experimentos", mix(R, seen, [(s5_experimento, 14), (s2_comparar, 6)])),
    ]
    body = lesson(
        ["Un suceso es <b>seguro</b> si va a ocurrir siempre, <b>imposible</b> si no puede ocurrir nunca y <b>posible</b> si puede ocurrir o no.",
         "Es <b>más probable</b> lo que tiene más casos a favor: si en una bolsa hay 5 bolas rojas y 2 azules, es más probable sacar roja.",
         "La probabilidad se puede escribir como una fracción: casos favorables / casos posibles. Con 5 rojas y 2 azules, la probabilidad de roja es %s." % fr(5, 7)],
        [("Dado de 6 caras: probabilidad de sacar par", ["Favorables: 2, 4 y 6 → 3", "Posibles: 6"], fr(3, 6)),
         ("3 camisetas y 2 pantalones", ["Cada camiseta con cada pantalón", "3 × 2"], "6 formas")],
        [["Pensar que lo poco probable es imposible", "Si hay 1 bola azul entre 20, sacar azul es poco probable, pero posible."],
         ["Mirar solo un color", "La probabilidad depende también del total de bolas."],
         ["Creer que lo que salió antes cambia lo siguiente", "Si devuelves la bola, cada vez la probabilidad es la misma."]],
        bolsa([("rojas", 5), ("azules", 2)]))
    faq = [("¿Qué es un suceso imposible?", "Un suceso que no puede ocurrir nunca, como sacar un 7 con un dado normal de seis caras."),
           ("¿Cómo se calcula una probabilidad sencilla?", "Se cuentan los casos favorables y los casos posibles y se escribe la fracción favorables / posibles. Sacar un 3 con un dado: 1/6.")]
    make_unit(R, "probabilidad", "S",
              "Incertidumbre: sucesos seguros, posibles e imposibles; comparación de la probabilidad de sucesos; identificación de casos posibles y favorables en experimentos aleatorios sencillos; aproximación a la probabilidad con fracciones",
              "Probabilidad: seguro, posible e imposible", "Probabilidad",
              "Fichas de matemáticas de 4.º de Primaria: sucesos seguros, posibles e imposibles, más y menos probable, bolsas, ruletas y dados, contar casos y probabilidad con fracciones. 100 ejercicios con soluciones.",
              "Favorables / posibles", "Más casos a favor, más probable.",
              body, faq, sets, 25)


if __name__ == "__main__":
    main()
