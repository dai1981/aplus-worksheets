# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Addizioni e sottrazioni in colonna (Numeri)
  python3 tools/gen_it_matematica_c2_addizioni_e_sottrazioni_in_colonna.py
Incolonnare da sotto da e u sotto u; addizioni senza e con il cambio (riporto); sottrazioni senza e con il cambio
(prestito); prova; problemi. Numeri fino a 99.
Errori: incolonnare male (34 + 5 → 84), dimenticare il riporto, togliere la cifra piccola dalla grande.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids, blocchi

R = random.Random(70206)
G = "classe-seconda"
K = Kids(R)


def wa(a, b):
    r = a + b
    out = [(a // 10 + b // 10) * 10 + (a % 10 + b % 10) % 10, r + 10, r - 10, r + 1]
    if b < 10:
        out.insert(0, a + b * 10)
    return [num(x) for x in out if 0 < x <= 120 and x != r]


def ws(a, b):
    r = a - b
    out = [abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10), r + 10, r - 10, r + 1]
    return [num(x) for x in out if 0 <= x <= 100 and x != r]


def add(cambio):
    a, b = R.randint(11, 79), R.randint(2, 49)
    if a + b > 99 or ((a % 10 + b % 10) >= 10) != cambio:
        return None
    e = "Unità: %d + %d = %d%s. Decine: %d + %d%s = %d. <b>%d</b>." % (a % 10, b % 10, a % 10 + b % 10, ", scrivo %d e porto 1 decina" % ((a % 10 + b % 10) % 10) if cambio else "",
                                                                        a // 10, b // 10, " + 1" if cambio else "", a // 10 + b // 10 + (1 if cambio else 0), a + b)
    return mcq(colonna([str(a), str(b)]) + "Esegui in colonna: %d + %d" % (a, b), num(a + b), wa(a, b), e)


def sub(cambio):
    a, b = R.randint(20, 99), R.randint(2, 59)
    if b >= a - 9 or ((a % 10) < (b % 10)) != cambio:
        return None
    e = ("Unità: %d − %d non si può: cambio 1 decina in 10 unità, %d − %d = %d. Decine: %d − 1 − %d = %d. <b>%d</b>." % (a % 10, b % 10, a % 10 + 10, b % 10, a % 10 + 10 - b % 10, a // 10, b // 10, a // 10 - 1 - b // 10, a - b)
         if cambio else "Unità: %d − %d = %d. Decine: %d − %d = %d. <b>%d</b>." % (a % 10, b % 10, a % 10 - b % 10, a // 10, b // 10, a // 10 - b // 10, a - b))
    return mcq(colonna([str(a), str(b)], op="−") + "Esegui in colonna: %d − %d" % (a, b), num(a - b), ws(a, b), e)


def s1():
    return add(False) if R.random() < 0.5 else sub(False)


def s2():
    return add(True)


def s3():
    return sub(True)


def s4_blocchi():
    d1, u1, d2, u2 = R.randint(1, 5), R.randint(3, 9), R.randint(1, 3), R.randint(3, 9)
    a, b = 10 * d1 + u1, 10 * d2 + u2
    r = a + b
    if r > 99:
        return None
    return mcq(blocchi(0, 0, d1, u1) + blocchi(0, 0, d2, u2) + "Metti insieme i due gruppi. Quanto fa %d + %d?" % (a, b), num(r), wa(a, b),
               "Decine: %d + %d = %d. Unità: %d + %d = %d%s. <b>%d</b>." % (d1, d2, d1 + d2, u1, u2, u1 + u2, " = 1 decina e %d unità" % ((u1 + u2) % 10) if u1 + u2 >= 10 else "", r))


def s4_mancante():
    a, b = R.randint(21, 59), R.randint(12, 39)
    r = a + b
    if r > 99:
        return None
    sa = str(a)
    i = R.randint(0, 1)
    d = sa[i]
    shown = sa[:i] + "?" + sa[i + 1:]
    return mcq("Quale cifra manca? %s + %d = %d" % (shown, b, r), d, [str((int(d) + 1) % 10), str((int(d) + 9) % 10), str((int(d) + 2) % 10)],
               "%d + %d = %d: la cifra che manca è <b>%s</b>." % (a, b, r, d))


def s5():
    p = K.next()
    k = R.choice(["piu", "piu", "meno", "meno"])
    if k == "piu":
        a, b = R.randint(15, 59), R.randint(15, 39)
        if a + b > 99:
            return None
        t = R.choice(["%s ha %d biglie e ne vince %d. Quante biglie ha?" % (p[0], a, b), "In biblioteca ci sono %d libri di fiabe e %d di avventure. Quanti libri ci sono?" % (a, b),
                      "Nella prima classe ci sono %d bambini, nella seconda %d. Quanti bambini in tutto?" % (a // 2 + 10, b // 2 + 10)])
        if "bambini" in t:
            a, b = a // 2 + 10, b // 2 + 10
        return mcq(t, num(a + b), wa(a, b), "%d + %d = <b>%d</b>." % (a, b, a + b))
    a, b = R.randint(40, 99), R.randint(15, 39)
    t = R.choice(["Un contadino ha %d uova. Ne vende %d. Quante uova restano?" % (a, b), "%s ha %d punti. Ne perde %d. Quanti punti ha ora?" % (p[0], a, b),
                  "In un parcheggio ci sono %d auto. Ne escono %d. Quante auto restano?" % (a, b)])
    return mcq(t, num(a - b), ws(a, b), "%d − %d = <b>%d</b>." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Senza cambio", mix(R, seen, [(s1, 20)])),
        ("Addizioni con il cambio", mix(R, seen, [(s2, 20)])),
        ("Sottrazioni con il cambio", mix(R, seen, [(s3, 20)])),
        ("Con i blocchi e cifre mancanti", mix(R, seen, [(s4_blocchi, 10), (s4_mancante, 10)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Scrivi i numeri uno sotto l’altro: <b>unità sotto unità, decine sotto decine</b>.",
         "Comincia sempre dalle <b>unità</b>, a destra.",
         "Addizione: se le unità fanno 10 o più, 10 unità diventano 1 decina e la porti nella colonna delle decine (cambio).",
         "Sottrazione: se in alto le unità sono poche, cambia 1 decina in 10 unità."],
        [("47 + 25", ["u: 7 + 5 = 12, scrivo 2 e porto 1", "da: 4 + 2 + 1 = 7"], "72"),
         ("52 − 18", ["u: 2 − 8 non si può: cambio, 12 − 8 = 4", "da: 4 − 1 = 3"], "34")],
        [["Incolonnare 34 + 5 come 34 + 50", "Il 5 va sotto le unità: 39."],
         ["Dimenticare il riporto", "Scrivi il piccolo 1 sopra le decine."],
         ["52 − 18 = 46", "In alto ci sono poche unità: fai il cambio, 34."]])
    faq = [("Che cos’è il cambio?", "È lo scambio tra 10 unità e 1 decina: nell’addizione 10 unità diventano 1 decina, nella sottrazione 1 decina diventa 10 unità."),
           ("Perché si parte dalle unità?", "Perché se le unità superano 9, il cambio va aggiunto alle decine.")]
    make_unit(R, "addizioni-e-sottrazioni-in-colonna", "N",
              "Eseguire le operazioni con i numeri naturali con gli algoritmi scritti usuali (addizioni e sottrazioni in colonna, con e senza cambio)",
              "Addizioni e sottrazioni in colonna con il cambio", "Addizioni e sottrazioni in colonna",
              "Schede di matematica per la classe seconda su addizioni e sottrazioni in colonna: incolonnare, senza cambio, con il cambio, blocchi, cifre mancanti e problemi. 100 esercizi con soluzioni.",
              "Unità sotto unità, decine sotto decine.", "Si comincia dalle unità.",
              body, faq, sets, 6, grade=G)


if __name__ == "__main__":
    main()
