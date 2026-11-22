# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: La sottrazione entro il 10 (Numeri)
  python3 tools/gen_it_matematica_c1_sottrazioni_entro_10.py
Togliere (oggetti barrati), il segno −, sottrazioni sulla retta (salti indietro), confrontare (quanti in più),
quanto manca, togliere 0 e togliere tutto, legame con l’addizione, problemi.
Errori: contare anche gli oggetti tolti, scambiare i numeri (3 − 7), confondere «togliere» e «aggiungere».
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C

R = random.Random(70106)
G = "classe-prima"


def w(r, a):
    return [str(x) for x in (r + 1, r - 1, a, r + 2) if 0 <= x <= 10 and x != r]


def s1_barrati():
    a = R.randint(3, 10)
    b = R.randint(1, a - 1)
    k = R.choice(C.KINDS)
    return mcq(C.barrati(a, k, b) + "Si tolgono quelle barrate. %s restano?" % C.Q(k) if C.COSE[k][2] == "f" else C.barrati(a, k, b) + "Si tolgono quelli barrati. %s restano?" % C.Q(k),
               str(a - b), w(a - b, a) + [str(b)], "%d − %d = <b>%d</b>." % (a, b, a - b))


def s1_scrivi():
    a = R.randint(3, 10)
    b = R.randint(1, a - 1)
    k = R.choice(C.KINDS)
    f = lambda x, y, z: "%d − %d = %d" % (x, y, z)
    return mcq(C.barrati(a, k, b) + "Quale sottrazione va bene per il disegno?", f(a, b, a - b), [f(a, b, a - b + 1), "%d + %d = %d" % (a, b, a + b), f(a, a - b, b) if b != a - b else f(a, b - 1, a - b + 1)],
               "Erano %d, ne tolgo %d: <b>%s</b>." % (a, b, f(a, b, a - b)))


def s2_retta():
    a = R.randint(3, 10)
    b = R.randint(1, min(4, a))
    return mcq(C.salti(a, -b) + "Parti da %d e fai %d salti indietro. Dove arrivi?" % (a, b), str(a - b), [str(a - b + 1), str(a - b - 1) if a - b else "1", str(a + b) if a + b <= 10 else str(b)],
               "%d − %d = <b>%d</b>." % (a, b, a - b))


def s2_calcola():
    a = R.randint(1, 10)
    b = R.randint(0, a)
    return mcq("Quanto fa %d − %d?" % (a, b), str(a - b), w(a - b, a) + [str(a + b) if a + b <= 12 else "0"], "%d − %d = <b>%d</b>." % (a, b, a - b))


def s3_confronta():
    k = R.choice(C.KINDS)
    a, b = R.sample(range(1, 10), 2)
    if a < b:
        a, b = b, a
    return mcq(C.due(a, k, b, k, "|") + ("Quante %s ci sono in più nel primo gruppo?" if C.COSE[k][2] == "f" else "Quanti %s ci sono in più nel primo gruppo?") % C.nome(k),
               str(a - b), [str(a + b), str(a), str(b)], "Fai le coppie e conta chi resta senza compagno: %d − %d = <b>%d</b>." % (a, b, a - b))


def s3_legame():
    a, b = R.randint(1, 6), R.randint(1, 5)
    if a + b > 10:
        return None
    s = a + b
    if R.random() < 0.5:
        return mcq("%d + %d = %d. Allora %d − %d fa…" % (a, b, s, s, b), str(a), [str(b) if b != a else str(a + 1), str(s), str(s + b) if s + b <= 12 else str(a - 1)], "Addizione e sottrazione sono legate: %d − %d = <b>%d</b>." % (s, b, a))
    return mcq("Completa: %d − ? = %d" % (s, a), str(b), [str(s), str(a), str(b + 1)], "%d − <b>%d</b> = %d, perché %d + %d = %d." % (s, b, a, a, b, s))


def s4_speciali():
    a = R.randint(1, 10)
    k = R.choice(["zero", "tutto", "uno"])
    if k == "zero":
        return mcq("Quanto fa %d − 0?" % a, str(a), ["0", str(a - 1), str(a + 1)], "Se non togli niente, resta <b>%d</b>." % a)
    if k == "tutto":
        return mcq("Quanto fa %d − %d?" % (a, a), "0", [str(a), "1", str(2 * a)], "Se togli tutto, resta <b>0</b>.")
    return mcq("Quanto fa %d − 1?" % a, str(a - 1), [str(a + 1), str(a), str(a - 2) if a > 1 else "2"], "Togliere 1 = il numero che viene prima: <b>%d</b>." % (a - 1))


STORIE = [("Sul ramo ci sono %d uccellini. Ne volano via %d. Quanti uccellini restano?", "uccellini"),
          ("Giulia ha %d caramelle. Ne mangia %d. Quante caramelle le restano?", "caramelle"),
          ("Nel cortile giocano %d bambini. %d vanno a casa. Quanti bambini restano?", "bambini"),
          ("Marco ha %d palloncini. Ne scoppiano %d. Quanti palloncini gli restano?", "palloncini"),
          ("Nel cestino ci sono %d mele. La mamma ne prende %d. Quante mele restano?", "mele"),
          ("Sul tavolo ci sono %d biscotti. Luca ne mangia %d. Quanti biscotti restano?", "biscotti"),
          ("In un parcheggio ci sono %d auto. Ne partono %d. Quante auto restano?", "auto"),
          ("Anna ha %d matite. Ne presta %d a un’amica. Quante matite ha ancora?", "matite"),
          ("Nell’acquario ci sono %d pesci. %d sono rossi, gli altri sono gialli. Quanti pesci sono gialli?", "pesci gialli"),
          ("Pietro ha %d anni. Sua sorella ha %d anni in meno. Quanti anni ha sua sorella?", "anni")]


def s5():
    t, u = R.choice(STORIE)
    a = R.randint(4, 10)
    b = R.randint(1, a - 1)
    if a - b == 1 and u in ("anni", "auto"):
        return None
    return mcq(t % (a, b), str(a - b), [str(a + b), str(a - b + 1), str(b) if b != a - b else str(a)], "Togliere: %d − %d = <b>%d</b> %s." % (a, b, a - b, u))


def main():
    seen = set()
    sets = [
        ("Togliere", mix(R, seen, [(s1_barrati, 12), (s1_scrivi, 8)])),
        ("Salti indietro sulla retta", mix(R, seen, [(s2_retta, 12), (s2_calcola, 8)])),
        ("Quanti in più?", mix(R, seen, [(s3_confronta, 12), (s4_speciali, 8)])),
        ("Sottrazione e addizione", mix(R, seen, [(s3_legame, 12), (s2_calcola, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>sottrazione</b> serve per togliere: si scrive con il segno <b>−</b> (meno). Il risultato si chiama <b>differenza</b>.",
         "Sulla retta: parti dal primo numero e fai tanti salti indietro quanti dice il secondo.",
         "Serve anche per confrontare: quanti ne ha in più? Fai le coppie e conta quelli senza compagno.",
         "Sottrazione e addizione sono legate: 3 + 4 = 7, quindi 7 − 4 = 3."],
        [("7 − 3", ["parto da 7", "6, 5, 4"], "4")],
        [["Contare anche gli oggetti tolti", "Conta solo quelli che restano (non barrati)."],
         ["Scrivere 3 − 7 invece di 7 − 3", "Prima si scrive quanti erano, poi quanti si tolgono."],
         ["Fare + invece di −", "«Restano», «volano via», «mangia» vogliono dire togliere."]],
        table(["Se so che…", "allora…"], [["4 + 3 = 7", "7 − 3 = 4 e 7 − 4 = 3"], ["5 + 5 = 10", "10 − 5 = 5"], ["6 + 2 = 8", "8 − 2 = 6 e 8 − 6 = 2"]]))
    faq = [("Perché si fa vedere il legame tra + e −?", "Perché chi sa 4 + 3 = 7 trova subito 7 − 3 = 4: la sottrazione diventa più facile."),
           ("Si può togliere un numero più grande?", "In classe prima no: dai numeri naturali si toglie sempre un numero più piccolo o uguale.")]
    make_unit(R, "sottrazioni-entro-10", "N",
              "Eseguire mentalmente semplici sottrazioni con i numeri naturali e verbalizzare le procedure di calcolo",
              "La sottrazione entro il 10", "Sottrazioni entro 10",
              "Schede di matematica per la classe prima sulla sottrazione entro il 10: togliere con le figure, il segno −, salti indietro sulla retta, quanti in più, legame con l’addizione e problemi. 100 esercizi con soluzioni.",
              "Sottrazione = togliere o confrontare.", "Se 3 + 4 = 7, allora 7 − 4 = 3.",
              body, faq, sets, 6, grade=G)


if __name__ == "__main__":
    main()
