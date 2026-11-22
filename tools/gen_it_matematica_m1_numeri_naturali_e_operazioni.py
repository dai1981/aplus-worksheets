# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Numeri naturali e operazioni (Numeri)
  python3 tools/gen_it_matematica_m1_numeri_naturali_e_operazioni.py
Sistema di numerazione decimale e posizionale, numeri romani, approssimare, termini delle operazioni, proprietà
(commutativa, associativa, dissociativa, distributiva, invariantiva), 0 e 1 nelle operazioni, stima e calcolo mentale.
Errori: dividere per 0, applicare l’invariantiva alla sottrazione moltiplicando, distribuire solo sul primo termine.
"""
import random
from it_media import M, L, unit, mix, table, W, num, FOIS, DIV, Kids
import gen_it_matematica_c5_grandi_numeri as G5
import gen_it_matematica_c5_numeri_romani as R5
import gen_it_matematica_c4_addizioni_e_sottrazioni as AS4
import gen_it_matematica_c4_moltiplicazioni as MO4
import gen_it_matematica_c4_divisioni as DV4

R = random.Random(71102)
G = "prima-media"


def s2_termini():
    q, a, w = R.choice([("Nella sottrazione 45 − 12 = 33, come si chiama 45?", "minuendo", ["sottraendo", "differenza", "addendo"]),
                        ("Nella divisione 56 : 8 = 7, come si chiama 8?", "divisore", ["dividendo", "quoziente", "resto"]),
                        ("Nella moltiplicazione 6 × 9 = 54, come si chiamano 6 e 9?", "fattori", ["addendi", "prodotti", "divisori"]),
                        ("Il risultato dell’addizione si chiama…", "somma", ["prodotto", "differenza", "quoziente"]),
                        ("Il risultato della divisione si chiama…", "quoziente", ["prodotto", "dividendo", "somma"]),
                        ("Quanto fa 0 : 7?", "0", ["7", "non si può fare", "1"]),
                        ("Quanto fa 7 : 0?", "è impossibile", ["0", "7", "1"]),
                        ("Quanto fa 0 : 0?", "è indeterminata", ["0", "1", "è impossibile"]),
                        ("Qual è l’elemento neutro della moltiplicazione?", "1", ["0", "10", "non esiste"]),
                        ("Qual è l’elemento neutro dell’addizione?", "0", ["1", "10", "non esiste"]),
                        ("Un prodotto è uguale a 0 quando…", "almeno un fattore è 0", ["tutti i fattori sono 1", "un fattore è 1", "mai"]),
                        ("Nella sottrazione tra numeri naturali, quando è possibile?", "quando il minuendo è maggiore o uguale al sottraendo", ["sempre", "mai", "solo con numeri pari"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s3_prop():
    k = R.choice(["dis", "dis", "dissoc", "inv_div", "add", "mol"])
    if k == "add":
        return AS4.s4_proprieta()
    if k == "mol":
        return MO4.s4_proprieta()
    if k == "inv_div":
        return DV4.s4_invariantiva()
    if k == "dissoc":
        a = R.randint(3, 9)
        b = R.choice([12, 14, 15, 16, 18, 24, 25])
        f = R.choice([x for x in (2, 3, 4, 5) if b % x == 0])
        return M("Con la proprietà dissociativa, %d %s %d è uguale a…" % (a, FOIS, b), "%d %s %d %s %d" % (a, FOIS, f, FOIS, b // f), W("%d %s %d + %d" % (a, FOIS, f, b // f), "%d %s %d" % (a + f, FOIS, b // f), "%d %s %d %s %d" % (a, FOIS, f, FOIS, b)),
                 "Si scompone %d in %d %s %d: %d %s %d %s %d = <b>%s</b>." % (b, f, FOIS, b // f, a, FOIS, f, FOIS, b // f, num(a * b)))
    a, b, c = R.randint(2, 9), R.randint(11, 40), R.randint(2, 9)
    if R.random() < 0.5:
        return M("Con la proprietà distributiva, %d %s (%d + %d) = …" % (a, FOIS, b, c), "%d %s %d + %d %s %d" % (a, FOIS, b, a, FOIS, c), W("%d %s %d + %d" % (a, FOIS, b, c), "%d + %d %s %d" % (a, b, FOIS, c), "(%d %s %d) %s %d" % (a, FOIS, b, FOIS, c)),
                     "Si moltiplica %d per ciascun addendo: <b>%d %s %d + %d %s %d</b> = %d." % (a, a, FOIS, b, a, FOIS, c, a * (b + c)))
    return M("Raccogli il fattore comune: %d %s %d + %d %s %d = …" % (a, FOIS, b, a, FOIS, c), "%d %s (%d + %d)" % (a, FOIS, b, c), W("%d %s %d %s %d" % (a, FOIS, b, FOIS, c), "(%d + %d) %s (%d + %d)" % (a, a, FOIS, b, c), "%d %s (%d %s %d)" % (a, FOIS, b, FOIS, c)),
             "Distributiva al contrario: <b>%d %s (%d + %d)</b> = %d %s %d = %d." % (a, FOIS, b, c, a, FOIS, b + c, a * (b + c)))


def s4_mentale():
    k = R.choice(["x5", "x25", "x99", "x11", "x9"])
    a = R.randint(12, 98)
    if k == "x5":
        return M("Calcola a mente: %d %s 5" % (a, FOIS), num(a * 5), W(num(a * 10), num(a * 5 + 5), num(a // 2 * 10) if a % 2 else num(a * 5 - 10)), "× 5 = × 10 : 2: %d %s 10 = %d; %d : 2 = <b>%s</b>." % (a, FOIS, a * 10, a * 10, num(a * 5)))
    if k == "x25":
        a = R.randint(4, 40)
        return M("Calcola a mente: %d %s 25" % (a, FOIS), num(a * 25), W(num(a * 20 + 5), num(a * 100), num(a * 25 + 25)), "× 25 = × 100 : 4: %s : 4 = <b>%s</b>." % (num(a * 100), num(a * 25)))
    if k == "x99":
        return M("Calcola a mente: %d %s 99" % (a, FOIS), num(a * 99), W(num(a * 100 - 1), num(a * 100 + a), num(a * 99 + 99)), "%d %s 100 − %d = %s − %d = <b>%s</b>." % (a, FOIS, a, num(a * 100), a, num(a * 99)))
    if k == "x11":
        return M("Calcola a mente: %d %s 11" % (a, FOIS), num(a * 11), W(num(a * 10 + 1), num(a * 11 + 10), num(a * 12)), "%d %s 10 + %d = %d + %d = <b>%s</b>." % (a, FOIS, a, a * 10, a, num(a * 11)))
    return M("Calcola a mente: %d %s 9" % (a, FOIS), num(a * 9), W(num(a * 10 - 9), num(a * 10 - 1), num(a * 9 + 9)), "%d %s 10 − %d = %d − %d = <b>%s</b>." % (a, FOIS, a, a * 10, a, num(a * 9)))


def main():
    for m in (G5, R5, AS4, MO4, DV4):
        m.R = R
    for m in (R5, AS4, MO4, DV4):
        if hasattr(m, "K"):
            m.K = Kids(R)
    seen = set()
    sets = [
        ("Sistema decimale e numeri romani", mix(R, seen, [(G5.s1_valore, 8), (G5.s2_scomponi, 6), (R5.s2_leggi, 6)])),
        ("Confrontare e approssimare", mix(R, seen, [(G5.s3_confronta, 6), (G5.s4_arrotonda, 14)])),
        ("Termini, 0 e 1 nelle operazioni", mix(R, seen, [(s2_termini, 12), (R5.s2_scrivi, 8)])),
        ("Proprietà delle operazioni", mix(R, seen, [(s3_prop, 20)])),
        ("Calcolo mentale e stima", mix(R, seen, [(s4_mentale, 14), (AS4.s4_stima, 6)])),
    ]
    body = L(["Il nostro sistema di numerazione è <b>decimale</b> (si raggruppa per 10) e <b>posizionale</b> (il valore di una cifra dipende dal posto). Quello romano è additivo e sottrattivo (IV = 4, VI = 6).",
              "Proprietà: <b>commutativa</b> (+ e ×), <b>associativa</b> e <b>dissociativa</b> (+ e ×), <b>distributiva</b> della × rispetto a + e −, <b>invariantiva</b> (− e :).",
              "0 è elemento neutro dell’addizione, 1 della moltiplicazione. Un prodotto con un fattore 0 vale 0. a : 0 è impossibile; 0 : 0 è indeterminata.",
              "Le proprietà servono per il calcolo mentale: 37 × 99 = 37 × 100 − 37 = 3663."],
             [("24 × 25 a mente", ["× 25 = × 100 : 4", "2400 : 4"], "600")],
             [["Dire che 7 : 0 = 0", "Nessun numero moltiplicato per 0 dà 7: la divisione è impossibile."],
              ["Distribuire su un solo addendo: 3 × (10 + 4) = 30 + 4", "Moltiplica tutti gli addendi: 30 + 12."],
              ["Usare l’invariantiva della sottrazione moltiplicando", "Nella sottrazione si aggiunge o si toglie lo stesso numero; nella divisione si moltiplica o si divide."]],
             table(["Proprietà", "Operazioni", "Esempio"], [["commutativa", "+ ×", "4 × 7 = 7 × 4"], ["associativa", "+ ×", "(2 × 5) × 9 = 2 × (5 × 9)"], ["dissociativa", "+ ×", "6 × 15 = 6 × 3 × 5"],
                                                           ["distributiva", "× su + e −", "4 × (10 + 3) = 40 + 12"], ["invariantiva", "− :", "96 − 19 = 97 − 20; 300 : 25 = 1200 : 100"]]))
    faq = [("Perché non si può dividere per 0?", "Perché la divisione è l’inversa della moltiplicazione: 7 : 0 = ? vorrebbe un numero che moltiplicato per 0 dia 7, e non esiste."),
           ("Le proprietà valgono per tutte le operazioni?", "No: la sottrazione e la divisione non sono commutative né associative (10 − 4 ≠ 4 − 10).")]
    unit(G, R, "numeri-naturali-e-operazioni", "N",
         "Eseguire addizioni, sottrazioni, moltiplicazioni e divisioni tra numeri naturali, quando possibile a mente oppure utilizzando gli usuali algoritmi scritti; utilizzare le proprietà delle operazioni; dare stime approssimate per il risultato di un’operazione",
         "Numeri naturali, operazioni e proprietà", "Numeri naturali e operazioni",
         "Schede di matematica per la prima media su numeri naturali e operazioni: sistema decimale, numeri romani, approssimazione, termini delle operazioni, 0 e 1, proprietà, calcolo mentale e stima. 100 esercizi con soluzioni.",
         "Proprietà: commutativa, associativa, dissociativa, distributiva, invariantiva.", "Non si divide per 0.",
         body, faq, sets, 2)


if __name__ == "__main__":
    main()
