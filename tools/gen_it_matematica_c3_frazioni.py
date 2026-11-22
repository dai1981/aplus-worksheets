# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le frazioni (Numeri)
  python3 tools/gen_it_matematica_c3_frazioni.py
Dividere in parti uguali, unità frazionaria, numeratore e denominatore, leggere e scrivere le frazioni,
frazione complementare, frazioni sulla retta, confrontare (stesso denominatore, unità frazionarie),
frazione di una quantità, frazioni decimali, problemi.
Errori: scambiare numeratore e denominatore, contare le parti bianche, credere che 1/8 &gt; 1/4 perché 8 &gt; 4.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, fr, striscia, cerchio, relabel, pl, DIV, FOIS
import fr_common as _F

R = random.Random(70310)
K = Kids(R)
DEN = [2, 3, 4, 5, 6, 8, 10]
NOME = {2: ("mezzo", "mezzi"), 3: ("terzo", "terzi"), 4: ("quarto", "quarti"), 5: ("quinto", "quinti"),
        6: ("sesto", "sesti"), 8: ("ottavo", "ottavi"), 10: ("decimo", "decimi")}
NUMW = ["zero", "un", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci"]


def parola(n, d):
    return NUMW[n] + " " + NOME[d][0 if n == 1 else 1]


def retta_fr(d, units, marks):
    return relabel(_F.droite_frac(d, units, marks), "retta da 0 a %d, ogni unità divisa in %d parti" % (units, d))


def s1_figura():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    pic = striscia(d, k) if R.random() < 0.5 else cerchio(d, k)
    return mcq(pic + "Quale frazione della figura è colorata?", fr(k, d),
               [fr(d, k), fr(d - k, d) if d - k != k else fr(k, d + 1), fr(k, d - k) if d - k != k else fr(k + 1, d), fr(k, d + 2)],
               "La figura è divisa in %d parti uguali (il denominatore); le parti colorate sono %d (il numeratore): <b>%s</b>." % (d, k, fr(k, d)))


def s1_uguali():
    d = R.choice([3, 4, 5, 6])
    k = R.choice(["si", "no"])
    if k == "si":
        pic = striscia(d, 1)
        return mcq(pic + "La striscia è divisa in parti uguali. Quanto vale una parte?", fr(1, d), [fr(d, 1), fr(1, d + 1), fr(d - 1, d)],
                   "La striscia è divisa in %d parti uguali: ogni parte è <b>%s</b>, un’unità frazionaria." % (d, fr(1, d)))
    n = R.randint(2, 8)
    return mcq("Una torta è tagliata in %d fette uguali. Che frazione della torta è una fetta?" % n, fr(1, n), [fr(n, 1), fr(1, n + 1), fr(n - 1, n)],
               "Una parte su %d: <b>%s</b>." % (n, fr(1, n)))


def s2_parola():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    return mcq("Come si scrive «%s» con i numeri?" % parola(k, d), fr(k, d),
               [fr(d, k), fr(k, d + 1) if d + 1 in NOME else fr(k, d - 1), fr(k + 1, d) if k + 1 < d else fr(k - 1, d) if k > 1 else fr(1, d + 2)],
               "«%s»: dividi in %d parti e ne prendi %d: <b>%s</b>." % (parola(k, d), d, k, fr(k, d)))


def s2_termini():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    if R.random() < 0.5:
        return mcq("Nella frazione %s, qual è il denominatore?" % fr(k, d), str(d), [str(k), str(d - k) if d - k not in (k, d) else str(d + k), str(d + k)],
                   "Il denominatore sta sotto la linea e dice in quante parti uguali si divide l’intero: <b>%d</b>." % d)
    return mcq("Nella frazione %s, che cosa dice il numeratore %d?" % (fr(k, d), k), "quante parti si prendono",
               ["in quante parti si divide l’intero", "quante parti restano", "quanto è grande l’intero"],
               "Il numeratore sta sopra la linea e dice <b>quante parti si prendono</b>.")


def s2_complementare():
    d = R.choice(DEN)
    k = R.randint(1, d - 1)
    pic = striscia(d, k)
    return mcq(pic + "Quale frazione della striscia <b>non</b> è colorata?", fr(d - k, d),
               [fr(k, d) if k != d - k else fr(k + 1, d), fr(d, d - k), fr(d - k, k) if d - k != k else fr(1, d)],
               "Le parti bianche sono %d su %d: <b>%s</b>. %s e %s insieme fanno l’intero (%s): sono frazioni complementari." % (d - k, d, fr(d - k, d), fr(k, d), fr(d - k, d), fr(d, d)))


def s3_retta():
    d = R.choice([2, 3, 4, 5, 6, 8, 10])
    k = R.randint(1, d - 1)
    return mcq(retta_fr(d, 1, [(k, "A")]) + "Quale frazione indica la freccia A?", fr(k, d),
               [fr(k + 1, d) if k + 1 < d else fr(k - 1, d) if k > 1 else fr(k, d + 1), fr(d, k), fr(k, d + 1) if d + 1 != k else fr(k, 2 * d), fr(k + 1, d + 1)],
               "Da 0 a 1 ci sono %d parti uguali. A è dopo %s: <b>%s</b>." % (d, pl(k, "parte", "parti"), fr(k, d)))


def s3_confronta():
    k = R.choice(["den", "num", "uno"])
    if k == "den":
        d = R.choice([4, 5, 6, 8, 10])
        a, b = R.sample(range(1, d), 2)
        g = max(a, b)
        return mcq("Qual è la frazione più grande: %s o %s?" % (fr(a, d), fr(b, d)), fr(g, d), [fr(min(a, b), d), "sono uguali", "non si può sapere"],
                   "Hanno lo stesso denominatore, quindi le parti sono uguali: %d parti sono più di %d. <b>%s</b>." % (g, min(a, b), fr(g, d)))
    if k == "num":
        a, b = R.sample(DEN, 2)
        big = min(a, b)
        return mcq("Qual è la frazione più grande: %s o %s?" % (fr(1, a), fr(1, b)), fr(1, big), [fr(1, max(a, b)), "sono uguali", "non si può sapere"],
                   "Più parti fai, più ogni parte è piccola. Una parte su %d è più grande di una parte su %d: <b>%s</b>." % (big, max(a, b), fr(1, big)))
    d = R.choice(DEN)
    n = R.choice([x for x in range(1, 2 * d) if x != d])
    right = "minore di 1" if n < d else "maggiore di 1"
    return mcq("La frazione %s è minore o maggiore di un intero?" % fr(n, d), right, ["maggiore di 1" if n < d else "minore di 1", "uguale a 1", "non si può sapere"],
               "Un intero è %s. %s è <b>%s</b> perché il numeratore è %s del denominatore." % (fr(d, d), fr(n, d), right, "minore" if n < d else "maggiore"))


def s4_quantita():
    d = R.choice([2, 3, 4, 5, 6, 10])
    q = R.randint(2, 9)
    n = d * q
    k = 1 if R.random() < 0.6 else R.randint(2, d - 1) if d > 2 else 1
    r = q * k
    w = [n - r if n - r != r else n + 1, q if k > 1 else n // 2 if n // 2 != r else n - 1, n * k // 1 if n * k != r else r + 1, d * k if d * k != r else r + 2]
    if k == 1:
        e = "Per trovare %s di %d dividi per %d: %d %s %d = <b>%d</b>." % (fr(1, d), n, d, n, DIV, d, r)
    else:
        e = "Prima %s di %d: %d %s %d = %d. Poi %s: %d %s %d = <b>%d</b>." % (fr(1, d), n, n, DIV, d, q, fr(k, d), q, FOIS, k, r)
    return mcq("Quanto fa %s di %d?" % (fr(k, d), n), str(r), [str(x) for x in w if 0 < x != r], e)


def s4_decimali():
    k = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq(striscia(10, k) + "La striscia è divisa in 10 parti. Quale frazione è colorata?", fr(k, 10),
                   [fr(10, k), fr(10 - k, 10) if 10 - k != k else fr(k, 100), fr(k, 100), fr(k + 1, 10) if k < 9 else fr(k - 1, 10)],
                   "%d parti su 10: <b>%s</b>, cioè %s. Le frazioni con denominatore 10, 100, 1000 si chiamano frazioni decimali." % (k, fr(k, 10), parola(k, 10)))
    d = R.choice([10, 100])
    n = R.randint(1, d - 1) if d == 10 else R.randint(11, 99)
    return mcq("Quale di queste è una frazione decimale?", fr(n, d), [fr(n, d + 2), fr(n, 5) if n < 5 else fr(1, 3), fr(n, 8) if n != 8 else fr(1, 4)],
               "Una frazione è decimale quando il denominatore è 10, 100, 1000…: <b>%s</b>." % fr(n, d))


def s5_problema():
    p = K.next()
    k = R.choice(["pizza", "nastro", "classe", "figurine", "rimane", "km"])
    if k == "pizza":
        d = R.choice([4, 6, 8])
        a = R.randint(1, d - 2)
        return mcq("Una pizza è divisa in %d fette uguali. %s ne mangia %d. Che frazione di pizza resta?" % (d, p[0], a), fr(d - a, d),
                   [fr(a, d), fr(d - a, a) if d - a != a else fr(1, d), fr(d, d - a)],
                   "Restano %d fette su %d: <b>%s</b>." % (d - a, d, fr(d - a, d)))
    if k == "nastro":
        d, q = R.choice([2, 3, 4, 5]), R.randint(3, 12)
        n = d * q
        return mcq("Un nastro è lungo %d cm. %s ne usa %s. Quanti centimetri usa?" % (n, p[0], fr(1, d)), "%d cm" % q,
                   ["%d cm" % (n - q), "%d cm" % (n * d) if n * d < 1000 else "%d cm" % (q + 1), "%d cm" % (n - d)],
                   "%s di %d: %d %s %d = <b>%d cm</b>." % (fr(1, d), n, n, DIV, d, q))
    if k == "classe":
        d = R.choice([2, 3, 4, 5])
        q = R.randint(4, 6)
        n = d * q
        return mcq("In una classe ci sono %d bambini. %s di loro va a scuola a piedi. Quanti bambini vanno a piedi?" % (n, fr(1, d)), str(q),
                   [str(n - q), str(d), str(n // 2) if n // 2 != q else str(q + 1)],
                   "%s di %d: %d %s %d = <b>%d</b> bambini." % (fr(1, d), n, n, DIV, d, q))
    if k == "figurine":
        d = R.choice([3, 4, 5])
        q = R.randint(3, 9)
        n = d * q
        kk = R.randint(2, d - 1)
        return mcq("%s ha %d figurine. Ne regala %s a un amico. Quante figurine regala?" % (p[0], n, fr(kk, d)), str(q * kk),
                   [str(q), str(n - q * kk), str(n // kk) if n % kk == 0 and n // kk != q * kk else str(q * kk + 1)],
                   "%s di %d = %d; %s = %d %s %d = <b>%d</b>." % (fr(1, d), n, q, fr(kk, d), q, FOIS, kk, q * kk))
    if k == "rimane":
        d = R.choice([3, 4, 5, 6, 8])
        a = R.randint(1, d - 1)
        return mcq("%s colora %s di un disegno. Che frazione deve ancora colorare?" % (p[0], fr(a, d)), fr(d - a, d),
                   [fr(a, d) if a != d - a else fr(1, d), fr(d, d - a), fr(d - a, a) if d - a != a else fr(a + 1, d)],
                   "Il disegno intero è %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), fr(d - a, d)))
    d, q = R.choice([2, 4, 5, 10]), R.randint(2, 9)
    n = d * q
    return mcq("Un percorso in bicicletta è lungo %d km. Dopo %s del percorso c’è una fontana. A quanti chilometri dalla partenza si trova?" % (n, fr(1, d)), "%d km" % q,
               ["%d km" % (n - q), "%d km" % d if d != q else "%d km" % (q + 1), "%d km" % (n + d)],
               "%s di %d: %d %s %d = <b>%d km</b>." % (fr(1, d), n, n, DIV, d, q))


def main():
    seen = set()
    sets = [
        ("Parti uguali e frazioni", mix(R, seen, [(s1_figura, 14), (s1_uguali, 6)])),
        ("Leggere e scrivere le frazioni", mix(R, seen, [(s2_parola, 8), (s2_termini, 6), (s2_complementare, 6)])),
        ("Retta e confronti", mix(R, seen, [(s3_retta, 8), (s3_confronta, 12)])),
        ("Frazione di una quantità e frazioni decimali", mix(R, seen, [(s4_quantita, 14), (s4_decimali, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Per fare una frazione dividi l’intero in <b>parti uguali</b>.",
         "Il <b>denominatore</b> (sotto la linea) dice in quante parti dividi; il <b>numeratore</b> (sopra) dice quante parti prendi.",
         "Una sola parte, come %s, è un’<b>unità frazionaria</b>. Con lo stesso numeratore, la frazione con il denominatore più grande è più piccola." % fr(1, 4),
         "Per trovare %s di 12 dividi 12 in 4 parti: 12 %s 4 = 3." % (fr(1, 4), DIV)],
        [("%s di 15" % fr(2, 5), ["%s di 15: 15 %s 5 = 3" % (fr(1, 5), DIV), "%s: 3 %s 2 = 6" % (fr(2, 5), FOIS)], "6")],
        [["Scambiare numeratore e denominatore", "Sotto scrivi in quante parti è divisa la figura, sopra quante sono colorate."],
         ["Contare le parti bianche", "Conta solo le parti colorate (o quelle prese)."],
         ["Pensare che %s sia più di %s" % (fr(1, 8), fr(1, 4)), "Se dividi in 8, ogni parte è più piccola che se dividi in 4."]],
        striscia(4, 3))
    faq = [("Che cos’è una frazione?", "È una parte di un intero diviso in parti uguali: 3/4 vuol dire che l’intero è diviso in 4 parti e se ne prendono 3."),
           ("Che cosa sono le frazioni complementari?", "Sono due frazioni che insieme formano l’intero, come 3/4 e 1/4.")]
    make_unit(R, "frazioni", "N",
              "Riconoscere frazioni come parti uguali di un intero; leggere, scrivere e confrontare frazioni semplici; calcolare la frazione di una quantità; riconoscere le frazioni decimali",
              "Le frazioni: parti uguali, numeratore e denominatore", "Frazioni",
              "Schede di matematica per la classe terza sulle frazioni: unità frazionaria, numeratore e denominatore, frazione complementare, retta, confronti, frazione di una quantità, frazioni decimali e problemi. 100 esercizi con soluzioni.",
              "Il denominatore dice in quante parti dividi, il numeratore quante ne prendi.", "Le parti devono essere uguali.",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
