# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: L’addizione entro il 10 (Numeri)
  python3 tools/gen_it_matematica_c1_addizioni_entro_10.py
Mettere insieme e aggiungere con le figure, il segno + e =, addizioni sulla retta (salti in avanti),
scambiare gli addendi, addizioni con lo 0, numero mancante, problemi.
Errori: contare di nuovo dal primo oggetto, contare il numero di partenza come primo salto, scrivere la somma al posto di un addendo.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C

R = random.Random(70105)
G = "classe-prima"


def w(r):
    return [str(x) for x in (r + 1, r - 1, r + 2) if 0 <= x <= 12 and x != r]


def s1_figure():
    a, b = R.randint(1, 6), R.randint(1, 5)
    if a + b > 10:
        return None
    k = R.choice(C.KINDS)
    k2 = k if R.random() < 0.6 else R.choice(C.KINDS)
    if k2 == k:
        return mcq(C.due(a, k, b, k, "+") + "%s ci sono in tutto?" % C.Q(k), str(a + b), w(a + b), "%d + %d = <b>%d</b>." % (a, b, a + b))
    return mcq(C.due(a, k, b, k2, "+") + "Quanti oggetti ci sono in tutto?", str(a + b), w(a + b), "%d %s e %d %s: %d + %d = <b>%d</b> oggetti." % (a, C.nome(k, a), b, C.nome(k2, b), a, b, a + b))


def s1_scrivi():
    a, b = R.randint(1, 6), R.randint(1, 5)
    if a + b > 10:
        return None
    k = R.choice(C.KINDS)
    f = lambda x, y, z: "%d + %d = %d" % (x, y, z)
    return mcq(C.due(a, k, b, k, "+") + "Quale addizione va bene per il disegno?", f(a, b, a + b), [f(a, b, a + b + 1), f(a, a, 2 * a) if a != b else f(a, b + 1, a + b + 1), "%d − %d = %d" % (max(a, b), min(a, b), abs(a - b))],
               "Un gruppo da %d e uno da %d: <b>%s</b>." % (a, b, f(a, b, a + b)))


def s2_retta():
    a, b = R.randint(0, 7), R.randint(1, 4)
    if a + b > 10:
        return None
    return mcq(C.salti(a, b) + "Parti da %d e fai %d salti in avanti. Dove arrivi?" % (a, b), str(a + b), [str(a + b - 1), str(a + b + 1), str(b)],
               "%d + %d = <b>%d</b>. Non contare il numero di partenza." % (a, b, a + b))


def s2_calcola():
    a, b = R.randint(0, 9), R.randint(0, 9)
    if a + b > 10:
        return None
    return mcq("Quanto fa %d + %d?" % (a, b), str(a + b), w(a + b) + [str(abs(a - b))], "%d + %d = <b>%d</b>." % (a, b, a + b))


def s3_scambia():
    a, b = R.randint(1, 8), R.randint(1, 8)
    if a + b > 10 or a == b:
        return None
    k = R.random()
    if k < 0.5:
        return mcq("%d + %d = %d. Quanto fa %d + %d?" % (a, b, a + b, b, a), str(a + b), w(a + b) + ["non si può sapere"], "Se scambi i numeri il risultato non cambia: <b>%d</b>." % (a + b))
    big, small = max(a, b), min(a, b)
    return mcq("Per calcolare %d + %d, da quale numero conviene partire?" % (small, big), "dal %d" % big, ["dal %d" % small, "da 0", "da 10"],
               "Parti dal numero più grande (%d) e aggiungi %d: %d + %d = %d." % (big, small, big, small, a + b))


def s3_zero():
    a = R.randint(0, 10)
    if R.random() < 0.5:
        return mcq("Quanto fa %d + 0?" % a, str(a), [str(a + 1), "0", str(a * 10) if a else "1"], "Aggiungere 0 non cambia il numero: <b>%d</b>." % a)
    return mcq("Quanto fa 0 + %d?" % a, str(a), [str(a + 1), "0", "10" if a != 10 else "1"], "Aggiungere 0 non cambia il numero: <b>%d</b>." % a)


def s4_mancante():
    a = R.randint(1, 8)
    r = R.randint(a + 1, 10)
    b = r - a
    if R.random() < 0.5:
        return mcq("Completa: %d + ? = %d" % (a, r), str(b), [str(r), str(a + r) if a + r <= 20 else str(b + 2), str(b + 1)], "%d + <b>%d</b> = %d." % (a, b, r))
    return mcq("Completa: ? + %d = %d" % (a, r), str(b), [str(r), str(b + 1), str(b - 1) if b else "2"], "<b>%d</b> + %d = %d." % (b, a, r))


def s4_tre():
    a, b, c = R.randint(1, 4), R.randint(1, 4), R.randint(1, 3)
    if a + b + c > 10:
        return None
    return mcq("Quanto fa %d + %d + %d?" % (a, b, c), str(a + b + c), w(a + b + c) + [str(a + b)], "%d + %d = %d; %d + %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b + c))


STORIE = [("Sul ramo ci sono %d uccellini. Ne arrivano altri %d. Quanti uccellini ci sono adesso?", "uccellini"),
          ("Giulia ha %d caramelle. La nonna gliene dà altre %d. Quante caramelle ha adesso?", "caramelle"),
          ("Nel cortile giocano %d bambini. Ne arrivano altri %d. Quanti bambini giocano adesso?", "bambini"),
          ("Marco ha %d macchinine rosse e %d blu. Quante macchinine ha in tutto?", "macchinine"),
          ("Nel vaso ci sono %d fiori gialli e %d fiori rossi. Quanti fiori ci sono in tutto?", "fiori"),
          ("Luca legge %d pagine al mattino e %d pagine la sera. Quante pagine legge in tutto?", "pagine"),
          ("In un acquario nuotano %d pesci rossi e %d pesci blu. Quanti pesci ci sono?", "pesci"),
          ("Anna mette %d mele nel cestino e poi altre %d. Quante mele ci sono nel cestino?", "mele"),
          ("Sul tavolo ci sono %d piatti. La mamma ne porta altri %d. Quanti piatti ci sono?", "piatti"),
          ("Pietro fa %d canestri nel primo tempo e %d nel secondo. Quanti canestri fa?", "canestri")]


def s5():
    t, u = R.choice(STORIE)
    a, b = R.randint(1, 7), R.randint(1, 5)
    if a + b > 10:
        return None
    return mcq(t % (a, b), str(a + b), [str(a + b + 1), str(abs(a - b)), str(a + b - 1)], "Mettere insieme / aggiungere: %d + %d = <b>%d</b> %s." % (a, b, a + b, u))


def main():
    seen = set()
    sets = [
        ("Mettere insieme", mix(R, seen, [(s1_figure, 12), (s1_scrivi, 8)])),
        ("Salti sulla retta", mix(R, seen, [(s2_retta, 12), (s2_calcola, 8)])),
        ("Scambiare e lo zero", mix(R, seen, [(s3_scambia, 10), (s3_zero, 4), (s2_calcola, 6)])),
        ("Numero mancante e tre numeri", mix(R, seen, [(s4_mancante, 12), (s4_tre, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["L’<b>addizione</b> serve per mettere insieme due gruppi o per aggiungere: si scrive con il segno <b>+</b> (più). Il risultato si chiama <b>somma</b>.",
         "Sulla retta: parti dal primo numero e fai tanti salti in avanti quanti dice il secondo.",
         "Se scambi i numeri la somma non cambia: 2 + 5 = 5 + 2. Conviene partire dal numero più grande.",
         "Aggiungere 0 non cambia il numero: 6 + 0 = 6."],
        [("3 + 4", ["parto da 4", "5, 6, 7"], "7")],
        [["Ricontare tutto dal primo oggetto", "Parti dal numero che già sai e conta solo quelli in più."],
         ["Contare il numero di partenza come primo salto", "Il primo salto porta al numero dopo."],
         ["Pensare che + 0 faccia 0", "Se non aggiungi niente, resta lo stesso numero."]],
        table(["+", "0", "1", "2", "3", "4", "5"], [[str(a)] + [str(a + b) for b in range(6)] for a in range(0, 6)]))
    faq = [("Perché si insegna a partire dal numero più grande?", "Perché si fanno meno salti: per 2 + 7 si parte da 7 e si conta 8, 9."),
           ("È normale usare le dita?", "Sì, all’inizio aiutano; con l’esercizio molte addizioni si ricordano a memoria.")]
    make_unit(R, "addizioni-entro-10", "N",
              "Eseguire mentalmente semplici addizioni con i numeri naturali e verbalizzare le procedure di calcolo",
              "L’addizione entro il 10", "Addizioni entro 10",
              "Schede di matematica per la classe prima sull’addizione entro il 10: mettere insieme con le figure, il segno + e =, salti sulla retta, scambiare gli addendi, lo zero, numero mancante e problemi. 100 esercizi con soluzioni.",
              "Addizione = mettere insieme o aggiungere.", "Parti dal numero più grande.",
              body, faq, sets, 5, grade=G)


if __name__ == "__main__":
    main()
