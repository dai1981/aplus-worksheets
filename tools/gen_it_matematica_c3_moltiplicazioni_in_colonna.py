# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le moltiplicazioni in colonna (Numeri)
  python3 tools/gen_it_matematica_c3_moltiplicazioni_in_colonna.py
Moltiplicare un numero di 2 o 3 cifre per una cifra, senza e con riporto; per un numero di due cifre;
moltiplicare per multipli di 10; stima; problemi.
Errori: dimenticare il riporto (47 × 3 → 121), dimenticare lo spostamento della seconda riga (34 × 12 → 102),
moltiplicare solo le unità.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids, FOIS

R = random.Random(70307)
K = Kids(R)


def no_carry(a, b):
    ds = [int(d) for d in str(a)]
    return int(str(ds[0] * b) + "".join(str(d * b % 10) for d in ds[1:]))


def one(a, b):
    p = a * b
    if p > 999:
        return None
    w = [no_carry(a, b), p + 10, p - 10, a * (b + 1), a + b, a % 10 * b + a // 10 * 10]
    e = "Moltiplica %d per ogni cifra di %d, da destra a sinistra, e aggiungi i riporti. %d %s %d = <b>%s</b>." % (b, a, a, FOIS, b, num(p))
    return mcq(colonna([str(a), str(b)], op=FOIS) + "Esegui in colonna: %d %s %d" % (a, FOIS, b), num(p), [num(x) for x in w if x > 0 and x != p], e)


def s1():
    a, b = R.randint(11, 44), R.randint(2, 4)
    if a % 10 * b >= 10 or a // 10 * b >= 10:
        return None
    return one(a, b)


def s2():
    a, b = R.randint(13, 99), R.randint(2, 9)
    if a % 10 * b < 10:
        return None
    return one(a, b)


def s3():
    a, b = R.randint(102, 333), R.randint(2, 9)
    return one(a, b)


def s4_due():
    a, b = R.randint(12, 49), R.randint(11, 29)
    if b % 10 == 0 or a * b > 999:
        return None
    u, d = b % 10, b // 10
    p = a * b
    w = [a * u + a * d, a * u + a, p + 100, p - 10, a * u * 10 + a * d]
    e = "%d %s %d = %s; %d %s %d0 = %s (nella seconda riga sposti di un posto: scrivi uno 0); %s + %s = <b>%s</b>." % (
        a, FOIS, u, num(a * u), a, FOIS, d, num(a * d * 10), num(a * u), num(a * d * 10), num(p))
    return mcq(colonna([str(a), str(b)], op=FOIS) + "Esegui in colonna: %d %s %d" % (a, FOIS, b), num(p), [num(x) for x in w if 0 < x != p], e)


def s4_decine():
    a, t = R.randint(2, 9), R.choice([20, 30, 40, 50, 60, 70, 80, 90])
    if R.random() < 0.4:
        a = R.randint(11, 30)
        t = R.choice([20, 30])
    p = a * t
    if p > 999:
        return None
    return mcq("Calcola a mente: %d %s %d" % (a, FOIS, t), num(p), [num(a * t // 10), num(p * 10) if p * 10 < 10000 else num(p + 10), num(a + t), num(p + t)],
               "%d %s %d = %d, poi %s 10: <b>%s</b>." % (a, FOIS, t // 10, a * t // 10, FOIS, num(p)))


def s4_stima():
    a, b = R.randint(21, 99), R.randint(3, 9)
    if a * b > 999 or a % 10 == 0:
        return None
    ra = (a + 5) // 10 * 10
    est = ra * b
    return mcq("Stima: %d %s %d fa circa… (arrotonda %d alla decina)" % (a, FOIS, b, a), num(est),
               [num(est + 10 * b), num(est - 10 * b), num(ra + b), num(est * 10) if est * 10 < 10000 else None],
               "%d fa circa %d: %d %s %d = <b>%s</b> (il risultato esatto è %s)." % (a, ra, ra, FOIS, b, num(est), num(a * b)))


def s5_problema():
    p = K.next()
    k = R.choice(["pagine", "uova", "posti", "euro", "biscotti", "km"])
    if k == "pagine":
        a, b = R.randint(12, 48), R.randint(3, 9)
        q = "%s legge %d pagine al giorno per %d giorni. Quante pagine legge in tutto?" % (p[0], a, b)
        u = "pagine"
    elif k == "uova":
        a, b = R.randint(12, 36), R.randint(6, 12)
        if b > 9:
            b = 6
        q = "Un contadino riempie %d confezioni da %d uova. Quante uova mette nelle confezioni?" % (a, b)
        u = "uova"
    elif k == "posti":
        a, b = R.randint(14, 32), R.randint(3, 9)
        q = "In un teatro ci sono %d file da %d posti. Quanti posti ci sono?" % (b, a)
        u = "posti"
    elif k == "euro":
        a, b = R.randint(12, 95), R.randint(2, 9)
        q = "Un biglietto per il museo costa %d €. Quanto spende una famiglia per %d biglietti?" % (a, b)
        u = "€"
    elif k == "biscotti":
        a, b = R.randint(13, 24), R.randint(11, 25)
        q = "Un pacco contiene %d biscotti. Quanti biscotti ci sono in %d pacchi?" % (a, b)
        u = "biscotti"
    else:
        a, b = R.randint(35, 120), R.randint(2, 7)
        q = "Ogni giorno un camion percorre %d km. Quanti chilometri percorre in %d giorni?" % (a, b)
        u = "km"
    r = a * b
    if r > 999:
        return None
    w = [no_carry(a, b) if b < 10 else a * (b % 10) + a * (b // 10), a + b, r + 10, r - a, a * (b + 1)]
    sfx = lambda x: num(x) + " " + u if u in ("€", "km") else num(x)
    return mcq(q, sfx(r), [sfx(x) for x in w if 0 < x != r],
               "%d %s %d = <b>%s</b>." % (a, FOIS, b, sfx(r) if u in ("€", "km") else num(r) + " " + u))


def main():
    seen = set()
    sets = [
        ("Senza riporto", mix(R, seen, [(s1, 20)])),
        ("Con il riporto", mix(R, seen, [(s2, 20)])),
        ("Numeri di tre cifre per una cifra", mix(R, seen, [(s3, 20)])),
        ("Per due cifre, per le decine e stima", mix(R, seen, [(s4_due, 8), (s4_decine, 6), (s4_stima, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Scrivi in alto il numero più lungo e sotto il moltiplicatore, <b>incolonnando le unità</b>.",
         "Moltiplica la cifra in basso per ogni cifra in alto, <b>da destra a sinistra</b>.",
         "Se un prodotto fa 10 o più, scrivi le unità e porta le decine nella colonna dopo: è il <b>riporto</b>. Lo aggiungi dopo aver moltiplicato.",
         "Con un moltiplicatore di due cifre la seconda riga si sposta di un posto a sinistra (scrivi uno 0 sotto le unità)."],
        [("47 %s 3" % FOIS, ["u: 7 %s 3 = 21, scrivo 1 e riporto 2" % FOIS, "da: 4 %s 3 = 12, più 2 di riporto = 14" % FOIS], "141"),
         ("34 %s 12" % FOIS, ["34 %s 2 = 68" % FOIS, "34 %s 10 = 340" % FOIS, "68 + 340 = 408"], "408")],
        [["Dimenticare il riporto: 47 %s 3 = 121" % FOIS, "Aggiungi il riporto dopo aver moltiplicato: 12 + 2 = 14, quindi 141."],
         ["Non spostare la seconda riga: 34 %s 12 = 102" % FOIS, "La seconda riga vale decine: scrivi uno 0 e poi 34 %s 1 = 340." % FOIS],
         ["Moltiplicare solo le unità", "Ogni cifra in alto va moltiplicata."]])
    faq = [("Quando si aggiunge il riporto?", "Dopo aver moltiplicato la cifra della colonna: prima 4 × 3 = 12, poi 12 + 2 = 14."),
           ("Come controllo una moltiplicazione?", "Con una stima: 47 × 3 è vicino a 50 × 3 = 150, quindi 141 è un risultato ragionevole.")]
    make_unit(R, "moltiplicazioni-in-colonna", "N",
              "Eseguire moltiplicazioni con i numeri naturali con gli algoritmi scritti usuali; stimare il risultato; risolvere problemi di moltiplicazione",
              "Le moltiplicazioni in colonna", "Moltiplicazioni in colonna",
              "Schede di matematica per la classe terza sulle moltiplicazioni in colonna: senza e con riporto, numeri di tre cifre, moltiplicatore di due cifre, stima e problemi. 100 esercizi con soluzioni.",
              "Moltiplica ogni cifra, da destra a sinistra.", "Il riporto si aggiunge dopo aver moltiplicato.",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
