# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: L’euro (Misure)
  python3 tools/gen_it_matematica_c2_euro.py
Monete (1 €, 2 €) e banconote (5, 10, 20, 50 €), contare il denaro fino a 100 €, cambi (2 monete da 1 € = 2 €),
confrontare somme, pagare con meno pezzi, quanto manca, spesa e resto semplice.
Errori: contare i pezzi invece del valore, confondere 5 € e 50 €, resto con l’addizione.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, soldi_svg
import it_c2 as C

R = random.Random(70212)
G = "classe-seconda"
K = Kids(R)
PEZZI = [5000, 2000, 1000, 500, 200, 100]


def E(n):
    return "%d €" % n


def s1_conta():
    items = sorted(R.sample(PEZZI[1:] + [100, 200], R.randint(2, 4)), reverse=True)
    if R.random() < 0.3:
        items = sorted(R.choices([100, 200, 500], k=R.randint(3, 5)), reverse=True)
    t = sum(items) // 100
    return mcq(soldi_svg(items) + "Quanti euro ci sono?", E(t), [E(len(items)), E(t + 1), E(t - min(items) // 100) if t > min(items) // 100 else E(t + 2), E(t + 10)],
               "Somma il valore di ogni pezzo: %s = <b>%d €</b>." % (" + ".join(str(x // 100) for x in items), t))


def s1_nome():
    v = R.choice([1, 2, 5, 10, 20, 50])
    kind = "moneta" if v <= 2 else "banconota"
    return mcq(soldi_svg([v * 100]) + "Che cosa è?", "%s da %d €" % ("una moneta" if v <= 2 else "una banconota", v),
               ["%s da %d €" % ("una banconota" if v <= 2 else "una moneta", v), "%s da %d €" % ("una moneta" if v <= 2 else "una banconota", {1: 2, 2: 1, 5: 50, 10: 20, 20: 10, 50: 5}[v]), "una moneta da 50 cent"],
               "È <b>%s da %d €</b>." % ("una moneta" if v <= 2 else "una banconota", v))


def s2_cambi():
    big, small = R.choice([(2, 1), (5, 1), (10, 5), (10, 2), (20, 10), (20, 5), (50, 10), (50, 20), (100, 50), (100, 20), (10, 1)])
    if big % small:
        return None
    n = big // small
    return mcq("Quante %s da %d € servono per fare %d €?" % ("monete" if small <= 2 else "banconote", small, big), str(n), [str(n + 1), str(n - 1), str(big), str(small)],
               "%d %s %d = %d: ne servono <b>%d</b>." % (small, "×", n, big, n))


def s2_confronta():
    a = sorted(R.sample(PEZZI, R.randint(2, 3)), reverse=True)
    b = sorted(R.sample(PEZZI, R.randint(2, 3)), reverse=True)
    ta, tb = sum(a) // 100, sum(b) // 100
    if ta == tb:
        return None
    g = "Anna" if ta > tb else "Luca"
    return mcq("Anna ha %s. Luca ha %s. Chi ha più soldi?" % (" + ".join(E(x // 100) for x in a), " + ".join(E(x // 100) for x in b)), g,
               ["Luca" if g == "Anna" else "Anna", "hanno gli stessi soldi", "chi ha più pezzi"], "Anna: %d €, Luca: %d €. Ne ha di più <b>%s</b>." % (ta, tb, g))


def s3_pagare():
    t = R.randint(3, 99)
    best, r = [], t
    for v in (50, 20, 10, 5, 2, 1):
        while r >= v:
            best.append(v)
            r -= v
    n = len(best)
    return mcq("Vuoi pagare %d € con meno pezzi possibile. Quanti pezzi usi?" % t, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(t), str(n + 2)],
               "Prendi prima i pezzi più grandi: %s. Sono <b>%d</b>." % (" + ".join(E(x) for x in best), n))


def s3_manca():
    p = K.next()
    pr = R.randint(10, 95)
    have = R.randint(3, pr - 2)
    return mcq("%s vuole un gioco da %d €. Ha %d €. Quanti euro %s mancano?" % (p[0], pr, have, "le" if p[1] == "lei" else "gli"), E(pr - have), [E(pr + have) if pr + have <= 100 else E(pr - have + 10), E(have), E(pr - have + 1)],
               "Da %d a %d: %d − %d = <b>%d €</b>." % (have, pr, pr, have, pr - have))


def s4_resto():
    p = K.next()
    pr = R.randint(2, 48)
    pay = min(x for x in (5, 10, 20, 50) if x > pr)
    return mcq("%s compra un libro da %d € e paga con %d €. Quanto riceve di resto?" % (p[0], pr, pay), E(pay - pr), [E(pay + pr) if pay + pr <= 100 else E(pay - pr + 10), E(pr), E(pay - pr + 1)],
               "Resto = soldi dati − prezzo: %d − %d = <b>%d €</b>." % (pay, pr, pay - pr))


def s5():
    p = K.next()
    k = R.choice(["spesa", "spesa", "tanti", "risparmi"])
    if k == "spesa":
        a, b = R.randint(2, 30), R.randint(2, 30)
        it = R.sample(["un libro", "un pallone", "una maglietta", "un puzzle", "un astuccio", "uno zaino"], 2)
        return mcq("%s compra %s da %d € e %s da %d €. Quanto spende?" % (p[0], it[0], a, it[1], b), E(a + b), [E(abs(a - b)), E(a + b + 1), E(a + b + 10)], "%d + %d = <b>%d €</b>." % (a, b, a + b))
    if k == "tanti":
        n, pr = R.randint(2, 5), R.randint(2, 9)
        return mcq("Un quaderno costa %d €. Quanto costano %d quaderni?" % (pr, n), E(n * pr), [E(n + pr), E(n * pr + pr), E(pr)], "%d × %d = <b>%d €</b>." % (n, pr, n * pr))
    a, w = R.randint(2, 5), R.randint(3, 10)
    return mcq("%s mette nel salvadanaio %d € ogni settimana. Quanti euro ha dopo %d settimane?" % (p[0], a, w), E(a * w), [E(a + w), E(a * w + a), E(a * (w - 1))], "%d × %d = <b>%d €</b>." % (a, w, a * w))


def main():
    seen = set()
    sets = [
        ("Monete e banconote", mix(R, seen, [(s1_nome, 6), (s1_conta, 14)])),
        ("Cambi e confronti", mix(R, seen, [(s2_cambi, 10), (s2_confronta, 10)])),
        ("Pagare e quanto manca", mix(R, seen, [(s3_pagare, 10), (s3_manca, 10)])),
        ("Il resto", mix(R, seen, [(s4_resto, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["In Italia si usa l’<b>euro</b> (€). Ci sono <b>monete</b> da 1 € e 2 € e <b>banconote</b> da 5, 10, 20, 50, 100 €…",
         "Per contare i soldi conta il <b>valore</b> di ogni pezzo, non quanti pezzi ci sono. Parti dai pezzi più grandi.",
         "Il <b>resto</b> è quello che ti restituiscono: soldi dati − prezzo."],
        [("Paghi un gioco da 13 € con 20 €.", ["20 − 13 = 7"], "7 € di resto")],
        [["Contare i pezzi invece del valore", "3 pezzi da 10 € fanno 30 €, non 3 €."],
         ["Confondere 5 € e 50 €", "Guarda bene il numero sulla banconota."],
         ["Trovare il resto con l’addizione", "Il resto si trova togliendo il prezzo."]],
        soldi_svg([2000, 1000, 500, 200, 100]))
    faq = [("Come si impara a usare i soldi?", "Giocando al negozio con monete e banconote finte: comprare, pagare e dare il resto."),
           ("In seconda si usano i centesimi?", "Si conoscono le monete, ma i calcoli si fanno soprattutto con gli euro interi.")]
    make_unit(R, "euro", "M",
              "Usare monete e banconote in euro in situazioni concrete; contare, confrontare somme di denaro e calcolare semplici spese e resti",
              "L’euro: monete, banconote e resto", "Euro",
              "Schede di matematica per la classe seconda sull’euro: monete e banconote, contare i soldi, cambi, confronti, pagare, quanto manca, resto e problemi. 100 esercizi con soluzioni.",
              "Conta il valore di ogni pezzo.", "Resto = soldi dati − prezzo.",
              body, faq, sets, 12, grade=G)


if __name__ == "__main__":
    main()
