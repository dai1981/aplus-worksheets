# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: I problemi (Problemi)
  python3 tools/gen_it_matematica_c2_problemi.py
Capire la situazione (aggiungere, togliere, gruppi uguali, dividere), scegliere l’operazione, la domanda giusta,
dati inutili, problemi con due domande, problemi con il disegno.
Errori: scegliere l’operazione da una sola parola, usare tutti i numeri, fermarsi alla prima operazione.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, FOIS, DIV
import it_c2 as C

R = random.Random(70211)
G = "classe-seconda"
K = Kids(R)
OPS = ["addizione", "sottrazione", "moltiplicazione", "divisione"]


def s1_op():
    p = K.next()
    k = R.randint(0, 3)
    a, b = R.randint(12, 50), R.randint(3, 20)
    x, y = R.randint(2, 5), R.randint(2, 6)
    q = ["%s ha %d biglie. Ne trova altre %d. Quante biglie ha ora?" % (p[0], a, b),
         "Sull’albero ci sono %d mele. Ne cadono %d. Quante mele restano?" % (a, b),
         "%s compra %d pacchetti con %d caramelle ciascuno. Quante caramelle compra?" % (p[0], x, y),
         "%d fiori si mettono in %d vasi, lo stesso numero in ognuno. Quanti fiori per vaso?" % (x * y, x)][k]
    e = ["Si aggiunge: <b>addizione</b>, %d + %d = %d." % (a, b, a + b), "Si toglie: <b>sottrazione</b>, %d − %d = %d." % (a, b, a - b),
         "Gruppi uguali: <b>moltiplicazione</b>, %d %s %d = %d." % (x, FOIS, y, x * y), "Parti uguali: <b>divisione</b>, %d %s %d = %d." % (x * y, DIV, x, y)][k]
    return mcq(q + " Quale operazione serve?", OPS[k], [o for o in OPS if o != OPS[k]], e)


def s2_risolvi():
    p = K.next()
    k = R.choice(["piu", "meno", "per", "diviso"])
    if k == "piu":
        a, b = R.randint(15, 60), R.randint(5, 35)
        return mcq("In un pollaio ci sono %d galline. Il contadino ne compra %d. Quante galline ci sono ora?" % (a, b), str(a + b), [str(a - b), str(a + b + 1), str(a + b - 10)], "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "meno":
        a, b = R.randint(30, 90), R.randint(5, 25)
        return mcq("Nel cinema ci sono %d posti. %d sono occupati. Quanti posti sono liberi?" % (a, b), str(a - b), [str(a + b) if a + b <= 100 else str(a - b + 10), str(a - b - 1), str(b)], "%d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "per":
        x, y = R.randint(2, 6), R.randint(3, 9)
        return mcq("%s ha %d scatole con %d matite ciascuna. Quante matite ha?" % (p[0], x, y), str(x * y), [str(x + y), str(x * y + y), str(y)], "%d %s %d = <b>%d</b>." % (x, FOIS, y, x * y))
    x, y = R.randint(2, 5), R.randint(3, 8)
    return mcq("La maestra ha %d quaderni e li dà a %d bambini, lo stesso numero a ognuno. Quanti quaderni a testa?" % (x * y, x), str(y), [str(x), str(x * y - x), str(y + 1)], "%d %s %d = <b>%d</b>." % (x * y, DIV, x, y))


def s3_domanda():
    p = K.next()
    a, b = R.randint(10, 40), R.randint(3, 9)
    k = R.choice(["meno", "piu"])
    if k == "meno":
        return mcq("Nel prato ci sono %d farfalle e %d api. Il calcolo è %d − %d. Quale domanda va bene?" % (a, b, a, b), "Quante farfalle ci sono in più delle api?",
                   ["Quanti insetti ci sono in tutto?", "Quante api ci sono?", "Quante zampe hanno?"], "%d − %d trova <b>quante farfalle in più</b>." % (a, b))
    return mcq("%s ha %d figurine e %d adesivi. Il calcolo è %d + %d. Quale domanda va bene?" % (p[0], a, b, a, b), "Quante cose ha in tutto?",
               ["Quante figurine ha in più degli adesivi?", "Quanti adesivi ha?", "Quante figurine regala?"], "%d + %d trova <b>quante cose in tutto</b>." % (a, b))


def s3_inutile():
    p = K.next()
    a, b, c = R.randint(10, 40), R.randint(3, 15), R.randint(6, 9)
    return mcq("%s ha %d anni. Ha %d euro e ne spende %d. Quanti euro le restano? Quale numero non serve?" % (p[0], c, a, b) if p[1] == "lei" else
               "%s ha %d anni. Ha %d euro e ne spende %d. Quanti euro gli restano? Quale numero non serve?" % (p[0], c, a, b), "%d (gli anni)" % c,
               ["%d (gli euro che ha)" % a, "%d (gli euro spesi)" % b, "servono tutti"], "Per la domanda servono solo gli euro: %d − %d = %d. <b>Gli anni non servono</b>." % (a, b, a - b))


def s4_due():
    p = K.next()
    k = R.choice(["regala", "compra", "bus", "torte"])
    if k == "regala":
        a, b, c = R.randint(20, 50), R.randint(5, 20), R.randint(3, 15)
        return mcq("%s ha %d figurine. Ne vince %d, poi ne regala %d. Quante ne ha alla fine?" % (p[0], a, b, c), str(a + b - c), [str(a + b), str(a + b + c), str(a - b - c) if a > b + c else str(a + b - c + 1)],
                   "Prima %d + %d = %d, poi %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))
    if k == "compra":
        x, y, z = R.randint(2, 4), R.randint(2, 5), R.randint(1, 5)
        return mcq("%s compra %d penne da %d euro e una gomma da %d euro. Quanto spende?" % (p[0], x, y, z), "%d euro" % (x * y + z), ["%d euro" % (x + y + z), "%d euro" % (x * y), "%d euro" % (x * (y + z))],
                   "Penne: %d %s %d = %d euro; + %d = <b>%d euro</b>." % (x, FOIS, y, x * y, z, x * y + z))
    if k == "bus":
        a, b, c = R.randint(10, 30), R.randint(3, 10), R.randint(2, 8)
        return mcq("Sull’autobus ci sono %d persone. Alla fermata ne salgono %d e ne scendono %d. Quante persone ci sono ora?" % (a, b, c), str(a + b - c), [str(a + b + c), str(a + b), str(a - b - c) if a > b + c else str(a + b - c + 2)],
                   "%d + %d − %d = <b>%d</b>." % (a, b, c, a + b - c))
    t, f, m = R.randint(2, 4), R.choice([6, 8, 10]), R.randint(3, 9)
    return mcq("Alla festa ci sono %d torte da %d fette. Se ne mangiano %d. Quante fette restano?" % (t, f, m), str(t * f - m), [str(t * f), str(t + f - m) if t + f > m else str(t * f + m), str(t * f - m + 1)],
               "Fette: %d %s %d = %d; %d − %d = <b>%d</b>." % (t, FOIS, f, t * f, t * f, m, t * f - m))


def s5_disegno():
    g, k = R.randint(2, 5), R.randint(2, 5)
    kind = R.choice(C.KINDS)
    t = R.randint(1, k * g - 1)
    return mcq(C.gruppi(g, k, kind) + "Nel disegno ci sono %d gruppi da %d. Se ne tolgo %d, %s %s restano?" % (g, k, t, C.quanti(kind).lower(), C.nome(kind)), str(g * k - t),
               [str(g * k), str(g + k - t) if g + k > t else str(g * k - t + 1), str(g * k + t)], "%d %s %d = %d; %d − %d = <b>%d</b>." % (g, FOIS, k, g * k, g * k, t, g * k - t))


def main():
    seen = set()
    sets = [
        ("Quale operazione?", mix(R, seen, [(s1_op, 20)])),
        ("Risolvi", mix(R, seen, [(s2_risolvi, 20)])),
        ("La domanda e i dati", mix(R, seen, [(s3_domanda, 6), (s3_inutile, 14)])),
        ("Problemi con due operazioni", mix(R, seen, [(s4_due, 20)])),
        ("Problemi con il disegno", mix(R, seen, [(s5_disegno, 20)])),
    ]
    body = lesson(
        ["Leggi il problema e immagina la scena. Trova la <b>domanda</b>.",
         "Si aggiunge → <b>+</b>. Si toglie o si confronta → <b>−</b>. Gruppi uguali → <b>%s</b>. Parti uguali → <b>%s</b>." % (FOIS, DIV),
         "Usa solo i numeri che servono. Se ci sono due passaggi, fai prima il primo.",
         "Scrivi la risposta con le parole: «Restano 12 mele»."],
        [("Luca ha 3 sacchetti da 5 biglie e ne regala 4.", ["3 %s 5 = 15" % FOIS, "15 − 4 = 11"], "11 biglie")],
        [["Scegliere l’operazione da una sola parola", "Immagina la scena: si aggiunge o si toglie?"],
         ["Usare tutti i numeri", "Alcuni numeri non servono per la domanda."],
         ["Fermarsi alla prima operazione", "Controlla di aver risposto alla domanda."]])
    faq = [("Come si aiuta un bambino a risolvere un problema?", "Facendogli raccontare la storia con parole sue o con un disegno: capita la situazione, l’operazione viene da sola."),
           ("Perché ci sono dati che non servono?", "Per imparare a leggere con attenzione e a scegliere solo le informazioni utili.")]
    make_unit(R, "problemi", "P",
              "Risolvere semplici problemi con l’addizione, la sottrazione, la moltiplicazione e la divisione a partire da situazioni concrete; rappresentarli con disegni e operazioni",
              "I problemi: quale operazione?", "Problemi",
              "Schede di matematica per la classe seconda sui problemi: scegliere l’operazione, la domanda giusta, dati inutili, problemi con due operazioni e con il disegno. 100 esercizi con soluzioni.",
              "Immagina la scena, poi scegli l’operazione.", "Usa solo i numeri che servono.",
              body, faq, sets, 11, grade=G)


if __name__ == "__main__":
    main()
