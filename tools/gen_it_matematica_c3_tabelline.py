# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le tabelline (Numeri)
  python3 tools/gen_it_matematica_c3_tabelline.py
Moltiplicazione come addizione ripetuta e schieramento, tabelline fino al 10, fattore mancante, proprietà
commutativa, tabella della moltiplicazione, problemi.
Errori: confondere × con + (6 × 4 = 10), sbagliare di una riga (7 × 8 = 48), 0 × 5 = 5.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, wrap, Kids, FOIS, GREEN, FILL, INK, text

R = random.Random(70306)
K = Kids(R)


def schieramento(r, c):
    s = []
    for i in range(r):
        for j in range(c):
            s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1.5'/>" % (18 + j * 26, 18 + i * 26, FILL, GREEN))
    return wrap(c * 26 + 10, r * 26 + 10, "".join(s), "schieramento di %d righe e %d colonne" % (r, c))


def wrongs(a, b):
    p = a * b
    w = [a + b, p + a if a != b else p + 1, p - b if p - b > 0 else None, (a + 1) * b, a * (b - 1) if b > 1 else None, p + 10, p - 1]
    return [str(x) for x in w if x is not None and x >= 0 and x != p]


def s1_addizione():
    a, b = R.randint(2, 6), R.randint(2, 9)
    sh = " + ".join([str(b)] * a)
    return mcq("Quale moltiplicazione corrisponde a %s?" % sh, "%d %s %d" % (a, FOIS, b),
               ["%d %s %d" % (b, FOIS, b) if a != b else "%d %s %d" % (a + 1, FOIS, b), "%d + %d" % (a, b), "%d %s %d" % (a + 1, FOIS, b), "%d %s %d" % (a, FOIS, b + 1)],
               "Il numero %d è ripetuto %d volte: %s = <b>%d %s %d</b> = %d." % (b, a, sh, a, FOIS, b, a * b))


def s1_schieramento():
    r, c = R.randint(2, 6), R.randint(2, 8)
    return mcq(schieramento(r, c) + "Quanti pallini ci sono? Scegli la moltiplicazione giusta.", "%d %s %d = %d" % (r, FOIS, c, r * c),
               ["%d + %d = %d" % (r, c, r + c), "%d %s %d = %d" % (r, FOIS, c + 1, r * (c + 1)), "%d %s %d = %d" % (r - 1, FOIS, c, (r - 1) * c) if r > 2 else "%d %s %d = %d" % (r + 1, FOIS, c, (r + 1) * c)],
               "Ci sono %d righe da %d pallini: <b>%d %s %d = %d</b>." % (r, c, r, FOIS, c, r * c))


def fatto(lo, hi):
    a, b = R.randint(lo, hi), R.randint(2, 10)
    if R.random() < 0.5:
        a, b = b, a
    return mcq("Quanto fa %d %s %d?" % (a, FOIS, b), str(a * b), wrongs(a, b),
               "%d %s %d = <b>%d</b>." % (a, FOIS, b, a * b))


def s2():
    return fatto(2, 5)


def s3():
    return fatto(6, 9)


def s3_zero_uno():
    a = R.randint(2, 10)
    k = R.choice([0, 1, 10])
    if R.random() < 0.5:
        q = "Quanto fa %d %s %d?" % (a, FOIS, k)
    else:
        q = "Quanto fa %d %s %d?" % (k, FOIS, a)
    p = a * k
    w = {0: [str(a), "1", str(a + 1)], 1: ["1", str(a + 1), str(a * 10), "0"], 10: [str(a + 10), str(a * 100), str(a) + "1", "10"]}[k]
    rule = {0: "Un numero per 0 fa sempre 0", 1: "Un numero per 1 resta uguale", 10: "Per moltiplicare per 10 aggiungi uno 0 a destra"}[k]
    return mcq(q, str(p), w, "%s: <b>%d</b>." % (rule, p))


def s4_mancante():
    a, b = R.randint(2, 10), R.randint(2, 10)
    p = a * b
    return mcq("Quale numero va nel quadratino? %d %s ☐ = %d" % (a, FOIS, p), str(b),
               [str(p - a) if p - a > 0 and p - a != b else str(b + 2), str(b + 1), str(b - 1) if b > 1 else str(b + 3), str(p // 2) if p % 2 == 0 and p // 2 != b else None],
               "%d %s %d = %d, quindi il numero è <b>%d</b>. Puoi anche fare %d : %d = %d." % (a, FOIS, b, p, b, p, a, b))


def s4_commutativa():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    return mcq("%d %s %d = %d. Quale moltiplicazione ha lo stesso risultato?" % (a, FOIS, b, a * b), "%d %s %d" % (b, FOIS, a),
               ["%d + %d" % (a, b), "%d %s %d" % (a, FOIS, b + 1), "%d %s %d" % (a + 1, FOIS, b - 1) if (a + 1) * (b - 1) != a * b else "%d %s %d" % (a + 2, FOIS, b)],
               "Proprietà commutativa: se scambi i fattori il prodotto non cambia. <b>%d %s %d</b> = %d." % (b, FOIS, a, a * b))


def s4_tabella():
    a = R.randint(2, 9)
    start = R.randint(1, 6)
    ss = [a * (start + i) for i in range(4)]
    k = R.randint(1, 3)
    shown = [str(x) if i != k else "☐" for i, x in enumerate(ss)]
    return mcq("Nella tabellina del %d, quale numero manca? %s" % (a, ", ".join(shown)), str(ss[k]),
               [str(ss[k] + 1), str(ss[k] - 1), str(ss[k] + a), str(ss[k - 1] + 1)],
               "Nella tabellina del %d si va avanti di %d in %d: <b>%d</b>." % (a, a, a, ss[k]))


def s5_problema():
    p = K.next()
    k = R.choice(["scatole", "zampe", "settimane", "file", "euro", "ruote", "petali"])
    if k == "scatole":
        a, b = R.randint(3, 9), R.choice([6, 8, 10, 12])
        if b > 10:
            b = R.randint(6, 9)
        return mcq("%s compra %d scatole di pastelli. In ogni scatola ci sono %d pastelli. Quanti pastelli compra in tutto?" % (p[0], a, b), str(a * b), wrongs(a, b),
                   "%d %s %d = <b>%d</b> pastelli." % (a, FOIS, b, a * b))
    if k == "zampe":
        a = R.randint(3, 9)
        an, z = R.choice([("gatti", 4), ("cani", 4), ("galline", 2), ("ragni", 8), ("api", 6)])
        return mcq("In un cortile ci sono %d %s. Quante zampe hanno in tutto?" % (a, an), str(a * z), wrongs(a, z),
                   "Ogni animale ha %d zampe: %d %s %d = <b>%d</b>." % (z, a, FOIS, z, a * z))
    if k == "settimane":
        a = R.randint(2, 9)
        return mcq("Quanti giorni ci sono in %d settimane?" % a, str(a * 7), wrongs(a, 7),
                   "Una settimana ha 7 giorni: %d %s 7 = <b>%d</b> giorni." % (a, FOIS, a * 7))
    if k == "file":
        a, b = R.randint(3, 9), R.randint(4, 8)
        return mcq("Nella palestra le sedie sono in %d file da %d sedie. Quante sedie ci sono?" % (a, b), str(a * b), wrongs(a, b),
                   "%d %s %d = <b>%d</b> sedie." % (a, FOIS, b, a * b))
    if k == "euro":
        a, b = R.randint(2, 9), R.randint(2, 9)
        return mcq("Un quaderno costa %d €. Quanto costano %d quaderni?" % (b, a), "%d €" % (a * b), [x + " €" for x in wrongs(a, b)],
                   "%d %s %d = <b>%d €</b>." % (a, FOIS, b, a * b))
    if k == "ruote":
        a = R.randint(3, 9)
        v, z = R.choice([("biciclette", 2), ("tricicli", 3), ("automobili", 4)])
        return mcq("Davanti alla scuola ci sono %d %s. Quante ruote ci sono in tutto?" % (a, v), str(a * z), wrongs(a, z),
                   "%d %s %d = <b>%d</b> ruote." % (a, FOIS, z, a * z))
    a, b = R.randint(3, 9), R.choice([5, 6])
    return mcq("%s disegna %d fiori. Ogni fiore ha %d petali. Quanti petali disegna?" % (p[0], a, b), str(a * b), wrongs(a, b),
               "%d %s %d = <b>%d</b> petali." % (a, FOIS, b, a * b))


def main():
    seen = set()
    sets = [
        ("Che cos’è la moltiplicazione", mix(R, seen, [(s1_addizione, 10), (s1_schieramento, 10)])),
        ("Tabelline del 2, 3, 4 e 5", mix(R, seen, [(s2, 20)])),
        ("Tabelline del 6, 7, 8 e 9", mix(R, seen, [(s3, 14), (s3_zero_uno, 6)])),
        ("Fattore mancante e proprietà", mix(R, seen, [(s4_mancante, 8), (s4_commutativa, 6), (s4_tabella, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["La <b>moltiplicazione</b> è un’addizione ripetuta: 4 %s 3 = 3 + 3 + 3 + 3 = 12." % FOIS,
         "Puoi vederla come uno <b>schieramento</b>: 4 righe da 3 pallini.",
         "Se scambi i fattori il prodotto non cambia: 4 %s 3 = 3 %s 4 (proprietà commutativa)." % (FOIS, FOIS),
         "Un numero per 1 resta uguale; un numero per 0 fa 0; per 10 si aggiunge uno 0."],
        [("7 %s 8" % FOIS, ["7 %s 8 = 8 %s 7" % (FOIS, FOIS), "7 %s 7 = 49, poi 49 + 7 = 56" % FOIS], "56")],
        [["6 %s 4 = 10" % FOIS, "Il segno %s vuol dire «volte»: 6 volte 4 = 24." % FOIS],
         ["7 %s 8 = 48" % FOIS, "Parti da un fatto che sai: 7 %s 7 = 49, poi aggiungi 7: 56." % FOIS],
         ["0 %s 5 = 5" % FOIS, "Zero volte 5 è zero: 0 %s 5 = 0." % FOIS]],
        schieramento(4, 3))
    faq = [("Come si imparano le tabelline?", "Un po’ ogni giorno: parti da quelle facili (2, 5, 10), usa la proprietà commutativa e i fatti che conosci per trovare gli altri."),
           ("Perché 3 × 4 e 4 × 3 fanno lo stesso?", "Uno schieramento di 3 righe da 4 girato diventa 4 righe da 3: i pallini sono sempre 12.")]
    make_unit(R, "tabelline", "N",
              "Conoscere con sicurezza le tabelline della moltiplicazione dei numeri fino a 10; eseguire moltiplicazioni come addizioni ripetute e schieramenti",
              "Le tabelline fino al 10", "Tabelline",
              "Schede di matematica per la classe terza sulle tabelline: moltiplicazione come addizione ripetuta, schieramenti, tabelline dal 2 al 10, fattore mancante, proprietà commutativa e problemi. 100 esercizi con soluzioni.",
              "Moltiplicare vuol dire sommare più volte lo stesso numero.", "Se scambi i fattori, il prodotto non cambia.",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
