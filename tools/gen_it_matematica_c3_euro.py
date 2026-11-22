# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: L’euro (Misure)
  python3 tools/gen_it_matematica_c3_euro.py
Monete e banconote, contare il denaro, euro e centesimi, scrivere con la virgola, confrontare, cambi, pagare
con meno monete possibile, il resto, spesa, costo unitario e totale, problemi.
Errori: 1 € = 10 cent, 3,5 € letto come 3 € e 5 cent, resto calcolato con l’addizione.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, soldi_svg, eur, NB, FOIS, DIV

R = random.Random(70315)
K = Kids(R)
COINS = [200, 100, 50, 20, 10, 5, 2, 1]
NOTES = [5000, 2000, 1000, 500]


def euc(c):
    """3 € e 50 cent"""
    e, r = divmod(c, 100)
    if e and r:
        return "%d%s€ e %d%scent" % (e, NB, r, NB)
    if e:
        return "%d%s€" % (e, NB)
    return "%d%scent" % (r, NB)


def s1():
    k = R.choice(["monete", "monete", "banconote"])
    if k == "monete":
        items = R.sample(COINS[:7], R.randint(3, 5))
    else:
        items = R.sample(NOTES, R.randint(1, 3)) + R.sample(COINS[:4], R.randint(1, 3))
    t = sum(items)
    return mcq(soldi_svg(items) + "Quanti soldi ci sono?", eur(t), [eur(t + 100), eur(t - min(items)) if t - min(items) > 0 else eur(t + 50), "%d%s€" % (len(items), NB), eur(t + 10)],
               "Somma il valore di ogni moneta e banconota: <b>%s</b>." % eur(t))


def s2():
    k = R.choice(["e_c", "ec_c", "c_ec", "virg", "virg2"])
    e, c = R.randint(1, 9), R.choice([5, 10, 20, 25, 30, 45, 50, 60, 75, 80, 95])
    if k == "e_c":
        return mcq("Completa: %d%s€ = … centesimi" % (e, NB), num(e * 100), [num(e * 10), num(e * 1000), num(e + 100)], "1 € = 100 centesimi, quindi %d € = <b>%s centesimi</b>." % (e, num(e * 100)))
    if k == "ec_c":
        return mcq("Completa: %s = … centesimi" % euc(e * 100 + c), num(e * 100 + c), [num(e * 10 + c), num(e + c), num(e * 1000 + c)],
                   "%d € = %d centesimi; %d + %d = <b>%d centesimi</b>." % (e, e * 100, e * 100, c, e * 100 + c))
    if k == "c_ec":
        n = e * 100 + c
        return mcq("Completa: %d centesimi = …" % n, euc(n), [euc(n // 10 * 100 + n % 10) if n // 10 < 100 else euc(n + 100), euc((e + 1) * 100 + c), euc(n - 100) if e > 1 else euc(n + 5)],
                   "100 centesimi = 1 €. %d centesimi = %d + %d = <b>%s</b>." % (n, e * 100, c, euc(n)))
    if k == "virg":
        return mcq("Come si scrive %s con la virgola?" % euc(e * 100 + c), eur(e * 100 + c),
                   ["%d,%d%s€" % (e, c // 10, NB) if c % 10 == 0 else "%d,%02d%s€" % (e + 1, c, NB), eur(c * 100 + e) if c * 100 + e < 10000 else eur(e * 100 + c + 1), "%d%s€" % (e + c, NB)],
                   "Le due cifre dopo la virgola sono i centesimi: <b>%s</b>." % eur(e * 100 + c))
    return mcq("Che cosa vuol dire %s?" % eur(e * 100 + c), euc(e * 100 + c),
               [euc(e * 100 + c // 10) if c % 10 == 0 and c // 10 else euc(e * 100 + c + 5), "%d%s€ e %d%scent" % (c, NB, e, NB), euc((e + 1) * 100 + c)],
               "Prima della virgola gli euro, dopo la virgola i centesimi: <b>%s</b>." % euc(e * 100 + c))


def s3():
    k = R.choice(["cmp", "quante", "meno"])
    if k == "cmp":
        a = R.randint(1, 9) * 100 + R.choice([5, 50, 20, 75, 90])
        b = a + R.choice([-45, -15, 15, 45, 4, -4])
        if b <= 0 or b == a:
            return None
        A, B = eur(a), euc(b)
        big = A if a > b else B
        return mcq("Quale somma è maggiore: %s o %s?" % (A, B), big, [B if big == A else A, "sono uguali", "non si può sapere"],
                   "%s = %s. La somma maggiore è <b>%s</b>." % (A, euc(a), big))
    if k == "quante":
        piece, tot = R.choice([(200, 1000), (200, 2000), (50, 500), (20, 200), (10, 100), (50, 300), (20, 100), (100, 1000), (500, 2000), (1000, 5000)])
        n = tot // piece
        kind = "banconote" if piece >= 500 else "monete"
        return mcq("Quante %s da %s servono per fare %s?" % (kind, eur(piece, c=True), eur(tot)), str(n), [str(n * 10) if n * 10 < 200 else str(n + 2), str(tot // 100), str(n + 1), str(n - 1)],
                   "%s %s %d = %s: servono <b>%d</b> %s." % (eur(piece, c=True), FOIS, n, eur(tot), n, kind))
    t = R.choice([130, 160, 270, 350, 380, 420, 560, 740, 830, 960, 1250, 1570, 2340])
    best, r = [], t
    for v in [2000, 1000, 500, 200, 100, 50, 20, 10]:
        while r >= v:
            best.append(v)
            r -= v
    n = len(best)
    return mcq("Vuoi pagare %s usando meno monete e banconote possibile. Quante te ne servono?" % eur(t), str(n), [str(n + 1), str(n + 2), str(n - 1), str(t // 100)],
               "Prendi prima i valori più grandi: %s. Ne servono <b>%d</b>." % (" + ".join(eur(v, c=True) for v in best), n))


def s4():
    p = K.next()
    prezzo = R.randint(1, 18) * 100 + R.choice([0, 20, 50, 75, 30, 90, 40, 60])
    banc = [b for b in [500, 1000, 2000] if b > prezzo][0]
    r = banc - prezzo
    wr = [eur(banc + prezzo), eur(r + 100), eur(r - 10) if r > 10 else eur(r + 10), eur(r + 50)]
    return mcq("%s compra un gioco che costa %s e paga con una banconota da %s. Quanto riceve di resto?" % (p[0], eur(prezzo), eur(banc)), eur(r), [w for w in wr if w != eur(r)],
               "Calcola %s − %s. Puoi anche contare in avanti: da %s a %s %s <b>%s</b>." % (eur(banc), eur(prezzo), eur(prezzo), eur(banc), "manca" if r == 100 else "mancano", eur(r)))


ITEMS = [("un cornetto", "cornetti", 120), ("un panino", "panini", 250), ("un quaderno", "quaderni", 230), ("una penna", "penne", 150),
         ("un fumetto", "fumetti", 590), ("un pallone", "palloni", 875), ("un gelato", "gelati", 250), ("un succo di frutta", "succhi di frutta", 120),
         ("un libro", "libri", 1290), ("un astuccio", "astucci", 760), ("una merendina", "merendine", 90), ("una borraccia", "borracce", 940)]


def s5():
    p = K.next()
    lui = "gli" if p[1] == "lui" else "le"
    k = R.choice(["due", "tanti", "basta", "resta", "costo"])
    if k == "due":
        (a, _, pa), (b, _, pb) = R.sample(ITEMS, 2)
        t = pa + pb
        nc = (pa // 100 + pb // 100) * 100 + (pa % 100 + pb % 100) % 100
        return mcq("%s compra %s a %s e %s a %s. Quanto spende?" % (p[0], a, eur(pa), b, eur(pb)), eur(t), [eur(abs(pa - pb)), eur(t + 100), eur(nc) if nc != t else eur(t - 10)],
                   "%s + %s = <b>%s</b>." % (eur(pa), eur(pb), eur(t)))
    if k == "tanti":
        a, pl_, pa = R.choice([x for x in ITEMS if x[2] < 300])
        n = R.randint(2, 6)
        return mcq("%s costa %s. Quanto costano %d %s?" % (a[0].upper() + a[1:], eur(pa), n, pl_), eur(n * pa), [eur(n + pa), eur(n * pa + pa), eur(n * (pa // 100) * 100)],
                   "%d %s %s = <b>%s</b>." % (n, FOIS, eur(pa), eur(n * pa)))
    if k == "basta":
        a, _, pa = R.choice(ITEMS)
        have = pa + R.choice([-150, -60, -25, 30, 80, 150])
        if have <= 0:
            return None
        ok = have >= pa
        return mcq("%s ha %s. Può comprare %s a %s?" % (p[0], eur(have), a, eur(pa)), "sì, %s restano %s" % (lui, eur(have - pa)) if ok else "no, %s mancano %s" % (lui, eur(pa - have)),
                   ["no, %s mancano %s" % (lui, eur(have - pa)) if ok else "sì, %s restano %s" % (lui, eur(pa - have)),
                    "sì, %s restano %s" % (lui, eur(have - pa + 100)) if ok else "no, %s mancano %s" % (lui, eur(pa - have + 100)), "sì, e non %s resta niente" % lui],
                   "%s − %s: %s." % (eur(max(have, pa)), eur(min(have, pa)), "restano <b>%s</b>" % eur(have - pa) if ok else "mancano <b>%s</b>" % eur(pa - have)))
    if k == "resta":
        have = R.randint(10, 30) * 100
        (a, _, pa), (b, _, pb) = R.sample(ITEMS, 2)
        if pa + pb >= have:
            return None
        r = have - pa - pb
        return mcq("%s ha %s. Compra %s a %s e %s a %s. Quanto %s resta?" % (p[0], eur(have), a, eur(pa), b, eur(pb), lui), eur(r), [eur(pa + pb), eur(have - pa), eur(r + 100)],
                   "%s + %s = %s; %s − %s = <b>%s</b>." % (eur(pa), eur(pb), eur(pa + pb), eur(have), eur(pa + pb), eur(r)))
    a, pl_, pa = R.choice([x for x in ITEMS if x[2] % 10 == 0 and x[2] < 400])
    n = R.randint(2, 5)
    return mcq("%d %s costano %s. Quanto costa %s?" % (n, pl_, eur(n * pa), a), eur(pa), [eur(n * pa * n), eur(n * pa - n * 100) if n * pa > n * 100 else eur(pa + 10), eur(pa + 100)],
               "Costo unitario = costo totale %s numero: %s %s %d = <b>%s</b>." % (DIV, eur(n * pa), DIV, n, eur(pa)))


def main():
    seen = set()
    sets = [
        ("Contare monete e banconote", mix(R, seen, [(s1, 20)])),
        ("Euro e centesimi", mix(R, seen, [(s2, 20)])),
        ("Confrontare e cambiare", mix(R, seen, [(s3, 20)])),
        ("Il resto", mix(R, seen, [(s4, 20)])),
        ("Problemi di spesa", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le <b>monete</b> sono da 1, 2, 5, 10, 20, 50 centesimi (nei disegni: c) e da 1 € e 2 €. Le <b>banconote</b> sono da 5, 10, 20, 50 €…",
         "1 € = 100 centesimi. Si scrive con la virgola: 3,50 € vuol dire 3 euro e 50 centesimi.",
         "Il <b>resto</b> è quello che ti restituiscono: soldi dati − prezzo. Puoi trovarlo anche contando in avanti dal prezzo.",
         "Costo totale = costo unitario %s quantità; costo unitario = costo totale %s quantità." % (FOIS, DIV)],
        [("Paghi un libro da 7,40 € con 10 €. Resto?", ["7,40 + 0,60 = 8 €", "8 + 2 = 10 €", "0,60 + 2 = 2,60"], "2,60 €")],
        [["1 € = 10 centesimi", "1 € = 100 centesimi."],
         ["Leggere 3,5 € come 3 € e 5 cent", "3,5 € = 3,50 €: sono 50 centesimi."],
         ["Trovare il resto sommando", "Il resto si trova togliendo il prezzo dai soldi dati."]],
        soldi_svg([500, 200, 50, 20]))
    faq = [("Perché il prezzo ha due cifre dopo la virgola?", "Perché le due cifre dopo la virgola sono i centesimi: 2,05 € sono 2 euro e 5 centesimi."),
           ("Come si calcola il resto velocemente?", "Si conta in avanti dal prezzo fino ai soldi dati: da 7,40 € a 8 € sono 60 cent, da 8 € a 10 € sono 2 €; in tutto 2,60 €.")]
    make_unit(R, "euro", "M",
              "Usare monete e banconote in euro in situazioni concrete; esprimere somme di denaro con euro e centesimi anche con la virgola; calcolare spesa, ricavo e resto",
              "L’euro: monete, banconote e resto", "Euro",
              "Schede di matematica per la classe terza sull’euro: contare monete e banconote, euro e centesimi, scrivere con la virgola, cambi, resto, costo unitario e problemi di spesa. 100 esercizi con soluzioni.",
              "1 € = 100 centesimi.", "Resto = soldi dati − prezzo.",
              body, faq, sets, 15)


if __name__ == "__main__":
    main()
