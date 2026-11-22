# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: La moltiplicazione (Numeri)
  python3 tools/gen_it_matematica_c4_moltiplicazioni.py
Moltiplicazioni in colonna con una e due cifre al moltiplicatore, × 10, 100, 1000 e per i multipli di 10,
proprietà commutativa, associativa e distributiva, calcolo mentale, stima, problemi.
Errori: non spostare di un posto il secondo prodotto parziale, dimenticare il riporto, sommare invece di moltiplicare.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids, FOIS, table

R = random.Random(70403)
G = "classe-quarta"
K = Kids(R)


def no_carry(a, b):
    ds = [int(d) for d in str(a)]
    return int(str(ds[0] * b) + "".join(str(d * b % 10) for d in ds[1:]))


def una(a, b):
    p = a * b
    w = [no_carry(a, b), p + 10, p - 100, a * (b + 1), p + 1000]
    return mcq(colonna([str(a), str(b)], op=FOIS) + "Esegui in colonna: %s %s %d" % (num(a), FOIS, b), num(p), [num(x) for x in w if x > 0 and x != p],
               "Moltiplica %d per ogni cifra di %s, da destra a sinistra, e aggiungi i riporti: <b>%s</b>." % (b, num(a), num(p)))


def due(a, b):
    u, d = b % 10, b // 10
    if u == 0:
        return None
    p = a * b
    w = [a * u + a * d, a * u + a * d * 100, p + 100, p - 10, a * (u + d)]
    return mcq(colonna([str(a), str(b)], op=FOIS) + "Esegui in colonna: %s %s %d" % (num(a), FOIS, b), num(p), [num(x) for x in w if 0 < x != p],
               "%s %s %d = %s; %s %s %d0 = %s (la seconda riga è spostata di un posto: sotto le unità scrivi 0); %s + %s = <b>%s</b>." % (
                   num(a), FOIS, u, num(a * u), num(a), FOIS, d, num(a * d * 10), num(a * u), num(a * d * 10), num(p)))


def s1():
    return una(R.randint(102, 9876), R.randint(3, 9))


def s2():
    return due(R.randint(23, 99), R.randint(12, 98))


def s3():
    return due(R.randint(112, 987), R.randint(12, 79))


def s4_dieci():
    k = R.choice([10, 100, 1000])
    a = R.choice([R.randint(3, 99), R.randint(101, 999), R.randint(10, 90) * 10])
    if a * k >= 10 ** 6:
        return None
    w = [a * k * 10, a * k // 10 if a * k // 10 != a else a * k * 100, a + k, int(str(a) + "0" * (len(str(k)) - 2)) if len(str(k)) > 2 else a * 1000]
    return mcq("Quanto fa %s %s %s?" % (num(a), FOIS, num(k)), num(a * k), [num(x) for x in w if 0 < x < 10 ** 7 and x != a * k],
               "Per %s aggiungi %d zeri a destra: <b>%s</b>." % (num(k), len(str(k)) - 1, num(a * k)))


def s4_multipli():
    a, t = R.randint(2, 9) * R.choice([1, 1, 10]), R.choice([20, 30, 40, 50, 60, 70, 80, 90, 200, 300, 400, 500, 600])
    if a * t >= 10 ** 5:
        return None
    base = t // 10 if t < 100 else t // 100
    z = 1 if t < 100 else 2
    return mcq("Calcola a mente: %s %s %s" % (num(a), FOIS, num(t)), num(a * t), [num(a * base), num(a * t * 10), num(a * t // 10), num(a + t)],
               "%s %s %d = %s, poi aggiungi %s: <b>%s</b>." % (num(a), FOIS, base, num(a * base), "uno zero" if z == 1 else "due zeri", num(a * t)))


def s4_proprieta():
    k = R.choice(["comm", "ass", "dist", "dist"])
    if k == "comm":
        a, b = R.randint(12, 99), R.randint(12, 99)
        return mcq("%d %s %d = %s. Quanto fa %d %s %d?" % (a, FOIS, b, num(a * b), b, FOIS, a), num(a * b), [num(a * b + a), num(a + b), "non si può sapere"],
                   "Proprietà <b>commutativa</b>: cambiando l’ordine dei fattori il prodotto non cambia: <b>%s</b>." % num(a * b))
    if k == "ass":
        a = R.randint(3, 19)
        b, c = R.choice([(2, 5), (5, 2), (4, 25), (25, 4), (5, 20), (2, 50)])
        return mcq("Calcola in fretta: %d %s %d %s %d" % (a, FOIS, b, FOIS, c), num(a * b * c), [num(a * b + c), num(a + b * c), num(a * b * c * 10)],
                   "Proprietà <b>associativa</b>: prima %d %s %d = %d, poi %d %s %d = <b>%s</b>." % (b, FOIS, c, b * c, a, FOIS, b * c, num(a * b * c)))
    a = R.randint(3, 9)
    t, u = R.randint(1, 9) * 10, R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("Proprietà distributiva: %d %s %d è uguale a…" % (a, FOIS, t + u), "%d %s %d + %d %s %d" % (a, FOIS, t, a, FOIS, u),
                   ["%d %s %d + %d" % (a, FOIS, t, u), "%d %s %d %s %d" % (a, FOIS, t, FOIS, u), "%d + %d %s %d" % (a, t, FOIS, u)],
                   "Moltiplica %d per <b>ogni</b> parte: %d %s %d + %d %s %d = %d + %d = %s." % (a, a, FOIS, t, a, FOIS, u, a * t, a * u, num(a * (t + u))))
    b = R.randint(11, 59) * 10 - R.randint(1, 2)
    r = b % 10
    c = 10 - r if r else 0
    return mcq("Calcola a mente con la distributiva: %d %s %d" % (a, FOIS, b), num(a * b), [num(a * (b + c)), num(a * (b + c) - c), num(a * b + a)],
               "%d = %d − %d: %d %s %d − %d %s %d = %s − %d = <b>%s</b>." % (b, b + c, c, a, FOIS, b + c, a, FOIS, c, num(a * (b + c)), a * c, num(a * b)))


def s4_stima():
    a, b = R.randint(21, 89), R.randint(11, 49)
    if a % 10 in (0, 5) or b % 10 in (0, 5):
        return None
    ra, rb = (a + 5) // 10 * 10, (b + 5) // 10 * 10
    est = ra * rb
    return mcq("Stima arrotondando alle decine: %d %s %d fa circa…" % (a, FOIS, b), num(est),
               [num(est * 10), num(ra + rb), num(a // 10 * 10 * (b // 10 * 10)) if a // 10 * 10 * (b // 10 * 10) != est else num(est + ra), num(est // 10)],
               "%d ≈ %d e %d ≈ %d: %d %s %d = <b>%s</b> (esatto: %s)." % (a, ra, b, rb, ra, FOIS, rb, num(est), num(a * b)))


def s5():
    p = K.next()
    k = R.choice(["pullman", "scatole", "biglietti", "pagine", "stipendio", "uova", "file", "ore"])
    if k == "pullman":
        a, b = R.randint(12, 25), R.randint(48, 56)
        return mcq("Per una gita partono %d pullman con %d posti ciascuno. Quanti posti ci sono in tutto?" % (a, b), num(a * b),
                   [num(a + b), num(a * b + b), num(due_wrong(a, b))], "%d %s %d = <b>%s</b>." % (a, FOIS, b, num(a * b)))
    if k == "scatole":
        a, b = R.randint(120, 480), R.randint(12, 36)
        return mcq("Un negozio riceve %s scatole di matite. Ogni scatola contiene %d matite. Quante matite in tutto?" % (num(a), b), num(a * b),
                   [num(a + b), num(due_wrong(a, b)), num(a * b + 1000)], "%s %s %d = <b>%s</b>." % (num(a), FOIS, b, num(a * b)))
    if k == "biglietti":
        a, b = R.randint(250, 950), R.randint(12, 28)
        return mcq("Al cinema sono stati venduti %s biglietti da %d €. Quanto ha incassato il cinema?" % (num(a), b), num(a * b) + " €",
                   [num(a + b) + " €", num(due_wrong(a, b)) + " €", num(a * b // 10) + " €"], "%s %s %d = <b>%s €</b>." % (num(a), FOIS, b, num(a * b)))
    if k == "pagine":
        a, b = R.randint(24, 58), R.randint(110, 360)
        return mcq("%s legge un libro di %d pagine al mese. Dopo %d mesi, quante pagine ha letto?" % (p[0], b, a // 2), num(a // 2 * b),
                   [num(a // 2 + b), num(a // 2 * b + b), num(a * b)], "%d %s %d = <b>%s</b> pagine." % (b, FOIS, a // 2, num(a // 2 * b)))
    if k == "stipendio":
        a = R.randint(14, 19) * 100 + R.choice([0, 50])
        return mcq("Un operaio guadagna %s € al mese. Quanto guadagna in 12 mesi?" % num(a), num(a * 12) + " €",
                   [num(a * 10) + " €", num(a + 12) + " €", num(due_wrong(a, 12)) + " €"], "%s %s 12 = <b>%s €</b>." % (num(a), FOIS, num(a * 12)))
    if k == "uova":
        a = R.randint(35, 95)
        return mcq("Un allevamento riempie %d confezioni da una dozzina di uova. Quante uova in tutto?" % a, num(a * 12),
                   [num(a + 12), num(a * 10), num(a * 6)], "Una dozzina = 12: %d %s 12 = <b>%s</b>." % (a, FOIS, num(a * 12)))
    if k == "file":
        a, b = R.randint(18, 45), R.randint(22, 38)
        return mcq("In un teatro ci sono %d file di poltrone. Ogni fila ha %d poltrone. Quante poltrone in tutto?" % (a, b), num(a * b),
                   [num(a + b), num(due_wrong(a, b)), num(a * b - a)], "%d %s %d = <b>%s</b>." % (a, FOIS, b, num(a * b)))
    a = R.randint(12, 30)
    return mcq("Un ciclista percorre %d km ogni ora. Quanti chilometri percorre in %d ore?" % (a, a // 6 + 2), num(a * (a // 6 + 2)) + " km",
               [num(a + a // 6 + 2) + " km", num(a * (a // 6 + 3)) + " km", num(a * 10) + " km"],
               "%d %s %d = <b>%s km</b>." % (a, FOIS, a // 6 + 2, num(a * (a // 6 + 2))))


def due_wrong(a, b):
    u, d = b % 10, b // 10
    return a * u + a * d


def main():
    seen = set()
    sets = [
        ("Per una cifra", mix(R, seen, [(s1, 20)])),
        ("Per due cifre", mix(R, seen, [(s2, 20)])),
        ("Tre cifre per due cifre", mix(R, seen, [(s3, 20)])),
        ("Calcolo mentale, proprietà e stima", mix(R, seen, [(s4_dieci, 5), (s4_multipli, 5), (s4_proprieta, 6), (s4_stima, 4)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Moltiplica il primo fattore per le <b>unità</b> del secondo, poi per le <b>decine</b>: la seconda riga si sposta di un posto (sotto le unità scrivi 0).",
         "Somma i prodotti parziali: è il risultato.",
         "Per 10, 100, 1000 aggiungi 1, 2, 3 zeri. Per 30 fai × 3 e poi × 10.",
         "Proprietà: <b>commutativa</b> (3 × 4 = 4 × 3), <b>associativa</b> (7 × 2 × 5 = 7 × 10), <b>distributiva</b> (6 × 23 = 6 × 20 + 6 × 3)."],
        [("47 × 23", ["47 × 3 = 141", "47 × 20 = 940", "141 + 940 = 1081"], "1081")],
        [["Non spostare la seconda riga", "Il 2 di 23 vale 20: sotto le unità metti 0."],
         ["Sommare i prodotti delle cifre", "47 × 23 non è 141 + 94: la seconda riga è 940."],
         ["Dimenticare il riporto", "Scrivilo piccolo sopra la cifra dopo e aggiungilo."]],
        table(["Proprietà", "Esempio"], [["commutativa", "25 × 8 = 8 × 25"], ["associativa", "13 × 2 × 5 = 13 × 10"], ["distributiva", "4 × 98 = 4 × 100 − 4 × 2"]]))
    faq = [("Perché nella seconda riga si scrive uno 0?", "Perché si moltiplica per le decine: 47 × 2 decine = 94 decine = 940."),
           ("Come si controlla il risultato?", "Con la stima: 47 × 23 fa circa 50 × 20 = 1000, quindi 1081 è ragionevole.")]
    make_unit(R, "moltiplicazioni", "N",
              "Eseguire moltiplicazioni con i numeri naturali, in colonna e a mente, utilizzando le proprietà delle operazioni; stimare il risultato",
              "La moltiplicazione con due cifre al moltiplicatore", "Moltiplicazioni",
              "Schede di matematica per la classe quarta sulla moltiplicazione: in colonna per una e per due cifre, per 10, 100, 1000, proprietà commutativa, associativa e distributiva, stima e problemi. 100 esercizi con soluzioni.",
              "Prima per le unità, poi per le decine (con lo 0).", "Poi somma i prodotti parziali.",
              body, faq, sets, 3, grade=G)


if __name__ == "__main__":
    main()
