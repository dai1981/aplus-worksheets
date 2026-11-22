# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Addizioni e sottrazioni entro il 20 (Numeri)
  python3 tools/gen_it_matematica_c1_addizioni_e_sottrazioni_entro_20.py
10 + un numero, addizioni e sottrazioni senza cambio (13 + 4, 17 − 5), passaggio della decina con gli amici del 10
(8 + 5 = 8 + 2 + 3), doppi e quasi doppi, sottrazioni oltre la decina, numero mancante, problemi.
Errori: scrivere 10 + 4 = 104, nel passaggio della decina dimenticare il pezzo che resta, togliere dalle decine.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C

R = random.Random(70107)
G = "classe-prima"


def w(r):
    return [str(x) for x in (r + 1, r - 1, r + 10 if r < 10 else r - 10, r + 2) if 0 <= x <= 20 and x != r]


def s1_dieci_piu():
    u = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("Quanto fa 10 + %d?" % u, str(10 + u), [str(11 + u), "10%d" % u, str(u)], "10 + %d = 1 decina e %d unità = <b>%d</b>." % (u, u, 10 + u))
    return mcq("Quanto fa %d − 10?" % (10 + u), str(u), [str(u + 1), str(10 + u), "1"] if u != 1 else ["2", "11", "10"], "Togli la decina: restano <b>%d</b> unità." % u)


def s1_senza():
    a = R.randint(11, 18)
    if R.random() < 0.5:
        b = R.randint(1, 19 - a) if a < 19 else 1
        if a % 10 + b > 9:
            return None
        return mcq("Quanto fa %d + %d?" % (a, b), str(a + b), w(a + b), "Aggiungi alle unità: %d + %d = %d, quindi <b>%d</b>." % (a % 10, b, a % 10 + b, a + b))
    b = R.randint(1, a % 10) if a % 10 else None
    if not b:
        return None
    return mcq("Quanto fa %d − %d?" % (a, b), str(a - b), w(a - b), "Togli dalle unità: %d − %d = %d, quindi <b>%d</b>." % (a % 10, b, a % 10 - b, a - b))


def s2_passaggio():
    a = R.randint(5, 9)
    b = R.randint(10 - a + 1, 9)
    r = a + b
    p1 = 10 - a
    return mcq(C.dieci(a, 2) + "Quanto fa %d + %d? (prima arriva a 10)" % (a, b) if R.random() < 0.5 else "Quanto fa %d + %d?" % (a, b), str(r), w(r) + ["1%d" % (r % 10 + 1)],
               "%d + %d = 10, poi 10 + %d = <b>%d</b> (%d = %d + %d)." % (a, p1, b - p1, r, b, p1, b - p1))


def s2_spiega():
    a = R.randint(6, 9)
    b = R.randint(10 - a + 1, 9)
    p1 = 10 - a
    ok = "%d + %d + %d" % (a, p1, b - p1)
    return mcq("Quale calcolo aiuta a fare %d + %d?" % (a, b), ok, ["%d + %d + %d" % (a, b - p1, b - p1 + 1), "%d + 10" % a, "%d − %d + 10" % (a, p1)],
               "Arriva prima a 10: %d + %d = 10; poi aggiungi il resto (%d): %s = %d." % (a, p1, b - p1, ok, a + b))


def s3_doppi():
    a = R.randint(1, 10)
    k = R.random()
    if k < 0.35:
        return mcq("Quanto fa %d + %d (il doppio di %d)?" % (a, a, a), str(2 * a), w(2 * a), "Doppio di %d: <b>%d</b>." % (a, 2 * a))
    if k < 0.55:
        return mcq("%d è il doppio di quale numero?" % (2 * a), str(a), [str(2 * a), str(a + 1), str(a - 1) if a > 1 else "3"], "%d + %d = %d: <b>%d</b>." % (a, a, 2 * a, a))
    if a > 9:
        return None
    return mcq("Sai che %d + %d = %d. Quanto fa %d + %d?" % (a, a, 2 * a, a, a + 1), str(2 * a + 1), [str(2 * a), str(2 * a + 2), str(2 * a - 1)],
               "È il doppio più 1: %d + 1 = <b>%d</b>." % (2 * a, 2 * a + 1))


def s3_sotto():
    a = R.randint(11, 18)
    b = R.randint(a % 10 + 1, 9)
    if b > a - 1:
        return None
    r = a - b
    p1 = a - 10
    return mcq("Quanto fa %d − %d?" % (a, b), str(r), w(r) + [str(b - a % 10 + 10)], "Prima togli %d e arrivi a 10, poi togli ancora %d: 10 − %d = <b>%d</b>." % (p1, b - p1, b - p1, r))


def s4_mancante():
    a = R.randint(2, 15)
    r = R.randint(a + 1, 20)
    b = r - a
    if R.random() < 0.5:
        return mcq("Completa: %d + ? = %d" % (a, r), str(b), [str(r), str(b + 1), str(b - 1) if b > 1 else "2"], "%d + <b>%d</b> = %d." % (a, b, r))
    return mcq("Completa: %d − ? = %d" % (r, a), str(b), [str(r + a) if r + a <= 30 else str(b + 2), str(b + 1), str(a)], "%d − <b>%d</b> = %d." % (r, b, a))


STORIE_PIU = [("Al parco ci sono %d bambini. Ne arrivano %d. Quanti bambini ci sono?", "bambini"),
              ("Sofia ha %d perline rosse e %d blu. Quante perline ha?", "perline"),
              ("In una scatola ci sono %d pastelli; Luca ne aggiunge %d. Quanti pastelli ci sono?", "pastelli"),
              ("Marco ha %d anni. Suo fratello ha %d anni in più. Quanti anni ha il fratello?", "anni"),
              ("Il lunedì Anna legge %d pagine, il martedì %d. Quante pagine legge?", "pagine")]
STORIE_MENO = [("Sull’autobus ci sono %d persone. Ne scendono %d. Quante persone restano?", "persone"),
               ("Giulia ha %d figurine. Ne regala %d. Quante figurine le restano?", "figurine"),
               ("Nel prato ci sono %d papere. %d vanno nel laghetto. Quante papere restano nel prato?", "papere"),
               ("Un libro ha %d pagine. Pietro ne ha lette %d. Quante pagine deve ancora leggere?", "pagine"),
               ("La mamma compra %d uova e ne usa %d per la torta. Quante uova restano?", "uova")]


def s5():
    if R.random() < 0.5:
        t, u = R.choice(STORIE_PIU)
        a, b = R.randint(6, 12), R.randint(3, 8)
        if a + b > 20:
            return None
        return mcq(t % (a, b), str(a + b), [str(a + b + 1), str(a - b) if a > b else str(b - a), str(a + b - 1)], "%d + %d = <b>%d</b> %s." % (a, b, a + b, u))
    t, u = R.choice(STORIE_MENO)
    a, b = R.randint(11, 20), R.randint(3, 9)
    return mcq(t % (a, b), str(a - b), [str(a + b), str(a - b + 1), str(a - b - 1)], "%d − %d = <b>%d</b> %s." % (a, b, a - b, u))


def main():
    seen = set()
    sets = [
        ("10 + un numero e senza cambio", mix(R, seen, [(s1_dieci_piu, 8), (s1_senza, 12)])),
        ("Il passaggio della decina", mix(R, seen, [(s2_passaggio, 14), (s2_spiega, 6)])),
        ("Doppi e quasi doppi", mix(R, seen, [(s3_doppi, 20)])),
        ("Sottrazioni oltre il 10 e numero mancante", mix(R, seen, [(s3_sotto, 10), (s4_mancante, 10)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["10 + 4 = 14: una decina e quattro unità. 14 − 10 = 4.",
         "Per superare il 10 usa gli amici del 10: 8 + 5 → 8 + <b>2</b> = 10, poi 10 + <b>3</b> = 13.",
         "I <b>doppi</b> si ricordano facilmente: 6 + 6 = 12. Il quasi doppio: 6 + 7 = 12 + 1 = 13.",
         "Per togliere oltre il 10: 13 − 5 → 13 − 3 = 10, poi 10 − 2 = 8."],
        [("7 + 6", ["7 + 3 = 10", "10 + 3 = 13"], "13")],
        [["Scrivere 10 + 4 = 104", "10 + 4 = 14: due cifre."],
         ["Dimenticare il pezzo che resta: 8 + 5 = 10", "Hai usato 2 dei 5: aggiungi ancora 3."],
         ["Togliere dalle decine: 15 − 3 = 5", "Si toglie dalle unità: 15 − 3 = 12."]],
        table(["Doppi", ""], [["1 + 1 = 2", "6 + 6 = 12"], ["2 + 2 = 4", "7 + 7 = 14"], ["3 + 3 = 6", "8 + 8 = 16"], ["4 + 4 = 8", "9 + 9 = 18"], ["5 + 5 = 10", "10 + 10 = 20"]]))
    faq = [("Che cos’è il passaggio della decina?", "È quando un’addizione supera il 10 (o una sottrazione scende sotto il 10): conviene fermarsi a 10 e poi continuare."),
           ("Come si imparano i doppi?", "Con le dita delle due mani, con i dadi doppi e con le filastrocche: poi aiutano anche per i quasi doppi.")]
    make_unit(R, "addizioni-e-sottrazioni-entro-20", "N",
              "Eseguire mentalmente semplici addizioni e sottrazioni con i numeri naturali entro il 20 e verbalizzare le procedure di calcolo",
              "Addizioni e sottrazioni entro il 20", "Addizioni e sottrazioni entro 20",
              "Schede di matematica per la classe prima su addizioni e sottrazioni entro il 20: 10 + un numero, passaggio della decina, doppi e quasi doppi, sottrazioni oltre il 10, numero mancante e problemi. 100 esercizi con soluzioni.",
              "Per superare il 10, arriva prima a 10.", "8 + 5 = 8 + 2 + 3 = 13.",
              body, faq, sets, 7, grade=G)


if __name__ == "__main__":
    main()
