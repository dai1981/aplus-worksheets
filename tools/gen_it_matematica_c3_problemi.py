# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: I problemi (Problemi)
  python3 tools/gen_it_matematica_c3_problemi.py
Scegliere l’operazione, la domanda giusta, dati utili e inutili, dati mancanti, problemi con due domande
(due operazioni), problemi con soldi, tempo e misure.
Errori: usare l’operazione suggerita da una parola («in più» → addizione sempre), usare tutti i numeri anche quelli
inutili, rispondere alla prima domanda e fermarsi.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, DIV, eur

R = random.Random(70312)
K = Kids(R)
OPS = ["un’addizione", "una sottrazione", "una moltiplicazione", "una divisione"]


def s1_operazione():
    p = K.next()
    k = R.randint(0, 3)
    a, b = R.randint(120, 480), R.randint(20, 99)
    if k == 0:
        q = "%s ha %d figurine e ne compra altre %d. Quante figurine ha adesso?" % (p[0], a, b)
        e = "Le figurine aumentano: %d + %d = %d. Serve <b>un’addizione</b>." % (a, b, a + b)
    elif k == 1:
        q = "In un cinema ci sono %d posti. %d sono occupati. Quanti posti sono liberi?" % (a, b)
        e = "Si toglie una parte dal tutto: %d − %d = %d. Serve <b>una sottrazione</b>." % (a, b, a - b)
    elif k == 2:
        x, y = R.randint(3, 9), R.randint(4, 12)
        q = "In una cassetta ci sono %d file da %d pesche. Quante pesche ci sono?" % (x, y)
        e = "Gruppi tutti uguali: %d %s %d = %d. Serve <b>una moltiplicazione</b>." % (x, FOIS, y, x * y)
    else:
        x, y = R.randint(3, 8), R.randint(4, 12)
        q = "%d matite vengono divise in parti uguali in %d astucci. Quante matite in ogni astuccio?" % (x * y, x)
        e = "Si fanno parti uguali: %d %s %d = %d. Serve <b>una divisione</b>." % (x * y, DIV, x, y)
    return mcq(q + " Quale operazione serve?", OPS[k], [o for o in OPS if o != OPS[k]], e)


def s1_trabocchetto():
    p = K.next()
    k = R.choice(["piu", "meno"])
    if k == "piu":
        a, b = R.randint(30, 90), R.randint(5, 25)
        q = "%s ha %d biglie. Ha %d biglie in più di suo fratello. Quante biglie ha il fratello?" % (p[0], a, b)
        return mcq(q, str(a - b), [str(a + b), str(b), str(a - b + 10)],
                   "Il fratello ne ha di meno! %d − %d = <b>%d</b>. Non farti ingannare da «in più»." % (a, b, a - b))
    a, b = R.randint(20, 70), R.randint(5, 18)
    q = "Il libro di %s ha %d pagine. Ha %d pagine in meno del libro di Anna. Quante pagine ha il libro di Anna?" % (p[0], a, b) if p[0] != "Anna" else None
    if not q:
        return None
    return mcq(q, str(a + b), [str(a - b), str(b), str(a + b + 10)],
               "Il libro di Anna ne ha di più: %d + %d = <b>%d</b>. «In meno» qui non vuol dire sottrarre." % (a, b, a + b))


def s2_dati():
    p = K.next()
    k = R.choice(["inutile", "inutile", "mancante"])
    if k == "inutile":
        a, b, c = R.randint(12, 40), R.randint(5, 15), R.randint(7, 11)
        q = ("%s ha %d anni. Ha %d euro nel salvadanaio e la nonna gliene regala %d. Quanti euro ha adesso? Quale dato non serve?" % (p[0], c, a, b))
        return mcq(q, "%d anni" % c, ["%d euro" % a, "%d euro" % b, "servono tutti"],
                   "Per la domanda servono solo gli euro: %d + %d = %d. L’età (<b>%d anni</b>) non serve." % (a, b, a + b, c))
    a = R.randint(3, 9)
    q = "%s compra %d gelati. Quanto spende?" % (p[0], a)
    return mcq(q + " Che cosa manca per rispondere?", "il prezzo di un gelato", ["il numero dei gelati", "il nome del gelataio", "niente, si può rispondere"],
               "Sai quanti gelati compra, ma non quanto costa ognuno: manca <b>il prezzo di un gelato</b>.")


def s2_domanda():
    p = K.next()
    a, b = R.randint(15, 40), R.randint(5, 14)
    s = "In un parco ci sono %d alberi e %d panchine." % (a, b)
    ok = "Quanti alberi ci sono in più rispetto alle panchine?"
    return mcq(s + " Il calcolo è %d − %d. Quale domanda va bene?" % (a, b), ok,
               ["Quanti alberi e panchine ci sono in tutto?", "Quante panchine ci sono?", "Quanti alberi ci sono in ogni fila?"],
               "%d − %d trova la differenza tra alberi e panchine: <b>%s</b>" % (a, b, ok))


def s3_due():
    p = K.next()
    k = R.choice(["regala", "compra", "pacchi", "pullman", "giorni"])
    if k == "regala":
        a, b, c = R.randint(40, 90), R.randint(10, 25), R.randint(5, 15)
        r = a + b - c
        return mcq("%s ha %d figurine. Ne vince %d e poi ne regala %d. Quante figurine ha alla fine?" % (p[0], a, b, c), str(r),
                   [str(a + b), str(a + b + c), str(a - b - c) if a - b - c > 0 else str(r + 10)],
                   "Prima %d + %d = %d, poi %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, r))
    if k == "compra":
        x, y, z = R.randint(2, 5), R.randint(2, 4), R.randint(1, 3)
        r = x * y + z
        return mcq("%s compra %d quaderni da %d € e una gomma da %d €. Quanto spende?" % (p[0], x, y, z), "%d €" % r,
                   ["%d €" % (x + y + z), "%d €" % (x * y), "%d €" % ((x + 1) * y + z)],
                   "Quaderni: %d %s %d = %d €; poi %d + %d = <b>%d €</b>." % (x, FOIS, y, x * y, x * y, z, r))
    if k == "pacchi":
        x, y, z = R.randint(3, 6), R.randint(6, 10), R.randint(3, 12)
        r = x * y - z
        return mcq("In un negozio ci sono %d pacchi da %d bottiglie. Se ne vendono %d. Quante bottiglie restano?" % (x, y, z), str(r),
                   [str(x * y), str(x * y + z), str(x + y - z) if x + y > z else str(r + 1)],
                   "Bottiglie: %d %s %d = %d; poi %d − %d = <b>%d</b>." % (x, FOIS, y, x * y, x * y, z, r))
    if k == "pullman":
        a, b, c = R.randint(20, 30), R.randint(20, 30), R.randint(3, 8)
        r = a + b + c
        return mcq("In gita vanno %d bambini della 3ª A, %d della 3ª B e %d insegnanti. Quante persone vanno in gita?" % (a, b, c), str(r),
                   [str(a + b), str(r + 10), str(a + b - c)],
                   "%d + %d + %d = <b>%d</b> persone." % (a, b, c, r))
    x, y = R.randint(2, 4), R.randint(5, 9)
    return mcq("%s legge %d pagine al giorno per %d settimane. Quante pagine legge?" % (p[0], y, x), str(x * 7 * y),
               [str(x * y), str(7 * y), str(x * 7 + y)],
               "%d settimane = %d %s 7 = %d giorni; %d %s %d = <b>%d</b> pagine." % (x, x, FOIS, x * 7, x * 7, FOIS, y, x * 7 * y))


def s4_soldi():
    p = K.next()
    k = R.choice(["resto", "risparmio", "insieme", "basta"])
    if k == "resto":
        a, b = R.randint(3, 12), R.randint(2, 8)
        pay = 20
        r = pay - a - b
        if r <= 0:
            return None
        return mcq("%s compra un libro da %d € e un astuccio da %d €. Paga con una banconota da 20 €. Quanto riceve di resto?" % (p[0], a, b), "%d €" % r,
                   ["%d €" % (a + b), "%d €" % (20 - a), "%d €" % (r + 1)],
                   "Spesa: %d + %d = %d €. Resto: 20 − %d = <b>%d €</b>." % (a, b, a + b, a + b, r))
    if k == "risparmio":
        a, w = R.randint(3, 9), R.randint(4, 10)
        return mcq("%s mette nel salvadanaio %d € ogni settimana. Quanti euro risparmia in %d settimane?" % (p[0], a, w), "%d €" % (a * w),
                   ["%d €" % (a + w), "%d €" % (a * w + a), "%d €" % (a * (w - 1))],
                   "%d %s %d = <b>%d €</b>." % (a, FOIS, w, a * w))
    if k == "insieme":
        (p1, _), (p2, _) = K.two()
        a, b, c = R.randint(5, 30), R.randint(5, 30), R.randint(40, 80)
        if a + b >= c:
            return None
        return mcq("%s ha %d € e %s ha %d €. Vogliono comprare insieme un gioco da %d €. Quanti euro mancano?" % (p1, a, p2, b, c), "%d €" % (c - a - b),
                   ["%d €" % (a + b), "%d €" % (c - a), "%d €" % (c + a + b) if c + a + b < 200 else "%d €" % (c - b)],
                   "Hanno %d + %d = %d €. Mancano %d − %d = <b>%d €</b>." % (a, b, a + b, c, a + b, c - a - b))
    pr, n, have = R.choice([3, 4, 5]), R.randint(3, 8), R.randint(15, 40)
    tot = pr * n
    ok = have >= tot
    return mcq("%s ha %d €. Vuole comprare %d biglietti per il cinema da %d € l’uno. Ha abbastanza soldi?" % (p[0], have, n, pr),
               "sì, avanzano %d €" % (have - tot) if ok else "no, mancano %d €" % (tot - have),
               ["no, mancano %d €" % (tot - have + 2) if ok else "sì, avanzano %d €" % (have - n), "sì, avanzano %d €" % (have - n - pr) if have - n - pr > 0 else "sì, spende %d €" % (n + pr), "non si può sapere"],
               "I biglietti costano %d %s %d = %d €. %s" % (n, FOIS, pr, tot, "Ha %d €, quindi <b>avanzano %d €</b>." % (have, have - tot) if ok else "Ha solo %d €, quindi <b>mancano %d €</b>." % (have, tot - have)))


def s5_misto():
    p = K.next()
    k = R.choice(["torta", "treno", "scaffale", "uova", "corsa", "album"])
    if k == "torta":
        f, n = R.randint(6, 12), R.randint(2, 5)
        e_ = R.randint(3, f * n - 2)
        return mcq("Per una festa si preparano %d torte da %d fette. Si mangiano %d fette. Quante fette avanzano?" % (n, f, e_), str(f * n - e_),
                   [str(f * n), str(f + n - e_) if f + n > e_ else str(f * n - e_ + 1), str(f * n + e_)],
                   "Fette: %d %s %d = %d; avanzano %d − %d = <b>%d</b>." % (n, FOIS, f, f * n, f * n, e_, f * n - e_))
    if k == "treno":
        h, m = R.randint(7, 11), R.choice([0, 10, 15, 20, 30])
        d = R.choice([25, 35, 40, 45, 50])
        mm = m + d
        return mcq("Un treno parte alle %d:%02d e il viaggio dura %d minuti. A che ora arriva?" % (h, m, d), "%d:%02d" % (h + mm // 60, mm % 60),
                   ["%d:%02d" % (h, m + d) if m + d < 60 else "%d:%02d" % (h, mm % 60), "%d:%02d" % (h + 1, m), "%d:%02d" % (h + d // 10, m), "%d:%02d" % (h + 1 - mm // 60, mm % 60), "%d:%02d" % (h + mm // 60, (mm + 10) % 60)],
                   "%d:%02d + %d min = <b>%d:%02d</b>." % (h, m, d, h + mm // 60, mm % 60))
    if k == "scaffale":
        s, l = R.randint(4, 8), R.randint(15, 30)
        n = R.randint(10, 40)
        return mcq("Una libreria ha %d ripiani con %d libri ciascuno. Arrivano altri %d libri. Quanti libri ci sono ora?" % (s, l, n), str(s * l + n),
                   [str(s * l), str(s + l + n), str(s * (l + n))],
                   "%d %s %d = %d; %d + %d = <b>%d</b> libri." % (s, FOIS, l, s * l, s * l, n, s * l + n))
    if k == "uova":
        b = R.randint(2, 4)
        n = b * R.randint(2, 4)
        tot = 6 * n
        return mcq("Un contadino ha %d uova e le mette in confezioni da 6. Poi divide le confezioni tra %d negozi. Quante confezioni riceve ogni negozio?" % (tot, b),
                   str(n // b), [str(n), str(tot // b), str(n // b + 1)],
                   "Confezioni: %d %s 6 = %d; %d %s %d = <b>%d</b>." % (tot, DIV, n, n, DIV, b, n // b))
    if k == "corsa":
        g, km = R.randint(3, 6), R.randint(2, 5)
        return mcq("%s corre %d km al giorno, %d giorni alla settimana. Quanti chilometri corre in 2 settimane?" % (p[0], km, g), "%d km" % (km * g * 2),
                   ["%d km" % (km * g), "%d km" % (km + g + 2), "%d km" % (km * 7 * 2)],
                   "In una settimana %d %s %d = %d km; in 2 settimane %d %s 2 = <b>%d km</b>." % (km, FOIS, g, km * g, km * g, FOIS, km * g * 2))
    tot, have = R.choice([180, 200, 240, 300]), None
    have = R.randint(60, tot - 40)
    per = R.choice([4, 5, 6])
    miss = tot - have
    if miss % per:
        return None
    return mcq("Un album ha %d figurine. %s ne ha %d. Le figurine si vendono in bustine da %d. Quante bustine deve comprare per finire l’album (senza doppioni)?" % (tot, p[0], have, per), str(miss // per),
               [str(miss), str(tot // per), str(miss // per + 1)],
               "Mancano %d − %d = %d figurine; %d %s %d = <b>%d</b> bustine." % (tot, have, miss, miss, DIV, per, miss // per))


def main():
    seen = set()
    sets = [
        ("Quale operazione?", mix(R, seen, [(s1_operazione, 14), (s1_trabocchetto, 6)])),
        ("Dati e domande", mix(R, seen, [(s2_dati, 12), (s2_domanda, 8)])),
        ("Problemi con due operazioni", mix(R, seen, [(s3_due, 20)])),
        ("Problemi con i soldi", mix(R, seen, [(s4_soldi, 20)])),
        ("Problemi misti", mix(R, seen, [(s5_misto, 20)])),
    ]
    body = lesson(
        ["Leggi bene il testo e trova la <b>domanda</b>: che cosa devi scoprire?",
         "Cerca i <b>dati utili</b> (i numeri che servono). A volte c’è un dato inutile, a volte manca un dato.",
         "Scegli l’operazione pensando alla situazione, non a una sola parola: si aggiunge (+), si toglie o si confronta (−), gruppi uguali (%s), parti uguali (%s)." % (FOIS, DIV),
         "Se ci sono <b>due domande</b> (una nascosta), rispondi prima alla prima e usa il risultato per la seconda. Alla fine controlla se la risposta è ragionevole."],
        [("Luca compra 3 quaderni da 2 € e una penna da 1 €. Quanto spende?", ["domanda nascosta: quanto costano i quaderni? 3 %s 2 = 6 €" % FOIS, "6 + 1 = 7 €"], "7 €")],
        [["«In più» vuol dire sempre addizione", "Chiediti chi ne ha di più e chi di meno: a volte serve una sottrazione."],
         ["Usare tutti i numeri del testo", "Usa solo i dati che servono per la domanda."],
         ["Fermarsi alla prima operazione", "Controlla di aver risposto proprio alla domanda finale."]])
    faq = [("Come si risolve un problema?", "Si legge il testo, si trova la domanda, si scelgono i dati utili, si decide l’operazione, si calcola e si scrive la risposta con l’unità (€, km, bambini…)."),
           ("Che cos’è una domanda nascosta?", "È un passaggio che il testo non chiede ma che serve: per sapere quanto spendi, prima devi sapere quanto costano i quaderni.")]
    make_unit(R, "problemi", "P",
              "Risolvere problemi con le quattro operazioni a partire da situazioni concrete; individuare dati utili, inutili e mancanti; rappresentare e spiegare il procedimento seguito",
              "I problemi: dati, domande e operazioni", "Problemi",
              "Schede di matematica per la classe terza sui problemi: scegliere l’operazione, dati utili, inutili e mancanti, domande nascoste, problemi con due operazioni, con i soldi e con il tempo. 100 esercizi con soluzioni.",
              "Trova la domanda, scegli i dati utili e poi l’operazione.", "Se c’è una domanda nascosta, rispondi prima a quella.",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
