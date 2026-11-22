# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: L’euro (Misure)
  python3 tools/gen_it_matematica_c1_euro.py
Riconoscere monete (1 €, 2 €) e banconote (5 €, 10 €, 20 €), contare il denaro fino a 20 €, cambiare,
confrontare, pagare e quanto manca, problemi di spesa.
Errori: contare i pezzi invece del loro valore, pensare che una moneta valga sempre meno di una banconota grande, confondere 2 € e 20 €.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, soldi_svg, Kids

R = random.Random(70109)
G = "classe-prima"
K = Kids(R)


def E(n):
    return "%d €" % n


def pezzi(t, max_pezzi=5):
    out, r = [], t
    for v in (20, 10, 5, 2, 1):
        while r >= v and len(out) < max_pezzi:
            out.append(v)
            r -= v
    return out if r == 0 else None


def s1_nome():
    v = R.choice([1, 2, 5, 10, 20])
    tipo = "una moneta" if v <= 2 else "una banconota"
    altro = "una banconota" if v <= 2 else "una moneta"
    sw = {1: 2, 2: 20, 5: 10, 10: 5, 20: 2}[v]
    return mcq(soldi_svg([v * 100]) + "Che cosa è?", "%s da %d €" % (tipo, v), ["%s da %d €" % (altro, v), "%s da %d €" % ("una moneta" if sw <= 2 else "una banconota", sw), "%s da %d €" % (tipo, v + 1)],
               "È <b>%s da %d €</b>." % (tipo, v))


def s1_conta():
    t = R.randint(2, 20)
    items = pezzi(t) if R.random() < 0.6 else sorted(R.choices([1, 2, 5], k=R.randint(2, 5)), reverse=True)
    if not items:
        return None
    t = sum(items)
    if t > 20:
        return None
    return mcq(soldi_svg([x * 100 for x in sorted(items, reverse=True)]) + "Quanti euro ci sono?", E(t), [E(len(items)), E(t + 1), E(t - 1) if t > 1 else E(3)],
               "Conta il valore di ogni pezzo, non quanti pezzi sono: %s = <b>%d €</b>." % (" + ".join(str(x) for x in sorted(items, reverse=True)), t))


def s2_cambi():
    big, small = R.choice([(2, 1), (5, 1), (10, 5), (10, 2), (20, 10), (20, 5), (10, 1), (5, 5)])
    if big == small:
        return mcq("Quale gruppo vale come una banconota da 5 €?", "5 monete da 1 €", ["5 monete da 2 €", "2 monete da 2 €", "1 moneta da 2 € e 1 da 1 €"], "1 + 1 + 1 + 1 + 1 = <b>5 €</b>.")
    n = big // small
    return mcq("Quante %s da %d € servono per fare %d €?" % ("monete" if small <= 2 else "banconote", small, big), str(n), [str(n + 1), str(big), str(n - 1)],
               "%s = %d: ne servono <b>%d</b>." % (" + ".join([str(small)] * n), big, n))


def s2_confronta():
    a = pezzi(R.randint(3, 20), 3)
    b = pezzi(R.randint(3, 20), 3)
    if not a or not b or sum(a) == sum(b):
        return None
    ta, tb = sum(a), sum(b)
    g = "Anna" if ta > tb else "Luca"
    return mcq("Anna ha %s. Luca ha %s. Chi ha più soldi?" % (" e ".join(E(x) for x in a), " e ".join(E(x) for x in b)), g,
               ["Luca" if g == "Anna" else "Anna", "hanno gli stessi soldi", "chi ha più monete"], "Anna: %d €, Luca: %d €. Ne ha di più <b>%s</b>." % (ta, tb, g))


def s3_manca():
    p = K.next()
    pr = R.randint(5, 20)
    have = R.randint(1, pr - 1)
    return mcq("%s vuole un gioco da %d €. Ha %d €. Quanti euro %s mancano?" % (p[0], pr, have, "le" if p[1] == "lei" else "gli"), E(pr - have), [E(pr + have), E(have), E(pr - have + 1)],
               "%d + ? = %d: mancano <b>%d €</b>." % (have, pr, pr - have))


def s3_basta():
    p = K.next()
    pr = R.randint(3, 19)
    items = pezzi(R.randint(3, 20), 4)
    if not items or sum(items) == pr:
        return None
    t = sum(items)
    ok = t >= pr
    return mcq("%s ha %s. Un pallone costa %d €. Ha abbastanza soldi?" % (p[0], " e ".join(E(x) for x in items), pr), "sì" if ok else "no", ["no" if ok else "sì", "solo se paga con le monete", "non si può sapere"],
               "Ha %d €, il pallone costa %d €: %d %s %d. <b>%s</b>." % (t, pr, t, "&gt;" if t > pr else "&lt;", pr, "Sì" if ok else "No"))


def s4_resto():
    p = K.next()
    pr = R.randint(1, 19)
    pay = min(x for x in (5, 10, 20) if x > pr)
    return mcq("%s compra un quaderno da %d € e paga con %d €. Quanto riceve di resto?" % (p[0], pr, pay) if pr < 4 else "%s compra un libro da %d € e paga con una banconota da %d €. Quanto riceve di resto?" % (p[0], pr, pay),
               E(pay - pr), [E(pay + pr), E(pr), E(pay - pr + 1)], "Resto = soldi dati − prezzo: %d − %d = <b>%d €</b>." % (pay, pr, pay - pr))


def s5():
    p = K.next()
    k = R.choice(["spesa", "spesa", "salvadanaio", "due"])
    if k == "spesa":
        a, b = R.randint(1, 9), R.randint(1, 9)
        it = R.sample(["una matita", "una gomma", "un gelato", "un succo", "un quaderno", "una palla", "un libretto"], 2)
        return mcq("%s compra %s da %d € e %s da %d €. Quanto spende?" % (p[0], it[0], a, it[1], b), E(a + b), [E(abs(a - b)) if a != b else E(a), E(a + b + 1), E(a + b - 1) if a + b > 2 else E(4)], "%d + %d = <b>%d €</b>." % (a, b, a + b))
    if k == "salvadanaio":
        a, b = R.randint(5, 15), R.randint(1, 5)
        return mcq("Nel salvadanaio di %s ci sono %d €. La zia gli regala %d €. Quanti euro ci sono adesso?" % (p[0], a, b) if p[1] == "lui" else
                   "Nel salvadanaio di %s ci sono %d €. La zia le regala %d €. Quanti euro ci sono adesso?" % (p[0], a, b), E(a + b), [E(a - b), E(a + b + 1), E(b)], "%d + %d = <b>%d €</b>." % (a, b, a + b))
    a, b = R.randint(10, 20), R.randint(2, 9)
    return mcq("%s ha %d €. Spende %d € per un regalo. Quanti euro %s restano?" % (p[0], a, b, "le" if p[1] == "lei" else "gli"), E(a - b), [E(a + b), E(a - b + 1), E(b)], "%d − %d = <b>%d €</b>." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Monete e banconote", mix(R, seen, [(s1_nome, 5), (s1_conta, 15)])),
        ("Cambiare e confrontare", mix(R, seen, [(s2_cambi, 8), (s2_confronta, 12)])),
        ("Basta? Quanto manca?", mix(R, seen, [(s3_basta, 10), (s3_manca, 10)])),
        ("Il resto", mix(R, seen, [(s4_resto, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["In Italia si usa l’<b>euro</b> (€). Ci sono <b>monete</b> da 1 € e 2 € e <b>banconote</b> da 5 €, 10 €, 20 € e di più.",
         "Per contare i soldi guarda il <b>valore</b> di ogni pezzo, non quanti pezzi sono: una banconota da 10 € vale più di 3 monete da 2 €.",
         "Lo stesso valore si può fare in tanti modi: 5 € = 2 € + 2 € + 1 €.",
         "Il <b>resto</b> è quanto ti restituiscono: soldi dati − prezzo."],
        [("2 € + 2 € + 1 €", ["2 + 2 = 4", "4 + 1 = 5"], "5 €")],
        [["Contare i pezzi invece del valore", "3 monete da 2 € fanno 6 €, non 3 €."],
         ["Confondere 2 € e 20 €", "2 € è una moneta, 20 € è una banconota."],
         ["Per il resto sommare invece di togliere", "Resto = soldi dati − prezzo."]],
        table(["Monete", "Banconote"], [["1 €", "5 €"], ["2 €", "10 €"], ["", "20 €"]]))
    faq = [("Come si fa pratica con i soldi a casa?", "Giocando al negozio con monete vere o finte: un bambino vende, l’altro paga e controlla il resto."),
           ("Perché si parte dagli euro interi?", "In classe prima si lavora con numeri fino a 20; i centesimi arrivano con i numeri decimali, più avanti.")]
    make_unit(R, "euro", "M",
              "Conoscere le monete e le banconote dell’euro; contare, confrontare e usare il denaro in semplici situazioni di compravendita",
              "L’euro: monete e banconote fino a 20 €", "L’euro",
              "Schede di matematica per la classe prima sull’euro: monete da 1 € e 2 €, banconote da 5 €, 10 € e 20 €, contare i soldi, cambiare, confrontare, quanto manca, il resto e problemi. 100 esercizi con soluzioni.",
              "Conta il valore di ogni pezzo.", "Resto = soldi dati − prezzo.",
              body, faq, sets, 9, grade=G)


if __name__ == "__main__":
    main()
