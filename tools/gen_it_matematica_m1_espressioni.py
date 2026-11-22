# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Le espressioni (Numeri)
  python3 tools/gen_it_matematica_m1_espressioni.py
Ordine delle operazioni, espressioni con le parentesi tonde, quadre e graffe, espressioni con le potenze,
tradurre una frase in espressione, problemi risolti con un’espressione.
Errori: eseguire le operazioni da sinistra a destra senza priorità, calcolare la potenza dopo la moltiplicazione, togliere le parentesi senza calcolarle.
"""
import random
from it_media import M, L, unit, mix, table, W, num, FOIS, DIV, Kids
import gen_it_matematica_c5_espressioni as E5
import gen_it_matematica_c5_potenze as P5

R = random.Random(71105)
G = "prima-media"
K = Kids(R)
pw = P5.pw


def s3_graffe():
    a, b, c, d, e = R.randint(2, 9), R.randint(2, 9), R.randint(2, 6), R.randint(1, 9), R.randint(2, 5)
    inner = (a + b) * c - d
    tot = inner + e
    k = R.choice([2, 3, 4, 5])
    if tot % k:
        return None
    r = tot // k
    q = "{[(%d + %d) %s %d − %d] + %d} %s %d" % (a, b, FOIS, c, d, e, DIV, k)
    wr = (a + b * c - d + e) // k if (a + b * c - d + e) % k == 0 else tot
    return M("Calcola: %s" % q, num(r), W(num(wr), num(tot), num(r + 1), num(inner // k) if inner % k == 0 else None),
             "Tonde: %d; quadre: %d %s %d − %d = %d; graffe: %d + %d = %d; %d %s %d = <b>%d</b>." % (a + b, a + b, FOIS, c, d, inner, inner, e, tot, tot, DIV, k, r))


def s4_pot():
    a, b, c = R.randint(2, 6), R.randint(2, 4), R.randint(2, 9)
    k = R.choice(["p1", "p2", "p3"])
    if k == "p1":
        r = a ** 2 + b * c
        return M("Calcola: %s + %d %s %d" % (pw(a, 2), b, FOIS, c), num(r), W(num((a * a + b) * c), num(2 * a + b * c), num(r + 1)),
                 "Prima la potenza: %s = %d; poi %d %s %d = %d; %d + %d = <b>%d</b>." % (pw(a, 2), a * a, b, FOIS, c, b * c, a * a, b * c, r))
    if k == "p2":
        r = (a + b) ** 2
        return M("Calcola: (%d + %d)%s" % (a, b, "²"), num(r), W(num(a * a + b * b), num(2 * (a + b)), num(a + b * b)),
                 "Prima la parentesi: %d + %d = %d; poi %s = <b>%d</b> (non %d² + %d²)." % (a, b, a + b, pw(a + b, 2), r, a, b))
    r = c * b ** 3 - a
    if r < 0:
        return None
    return M("Calcola: %d %s %s − %d" % (c, FOIS, pw(b, 3), a), num(r), W(num((c * b) ** 3 - a), num(c * b * 3 - a), num(r + 2)),
             "Prima la potenza: %s = %d; %d %s %d = %d; %d − %d = <b>%d</b>." % (pw(b, 3), b ** 3, c, FOIS, b ** 3, c * b ** 3, c * b ** 3, a, r))


def s4_traduci():
    a, b, c = R.randint(2, 20), R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["somma_per", "per_somma", "diff_quad", "doppio"])
    if k == "somma_per":
        return M("Quale espressione traduce: «moltiplica per %d la somma di %d e %d»?" % (c, a, b), "(%d + %d) %s %d" % (a, b, FOIS, c),
                 W("%d + %d %s %d" % (a, b, FOIS, c), "%d %s %d + %d" % (a, FOIS, c, b), "(%d %s %d) + %d" % (a, FOIS, b, c)), "Prima la somma, quindi tra parentesi: <b>(%d + %d) %s %d</b>." % (a, b, FOIS, c))
    if k == "per_somma":
        return M("Quale espressione traduce: «aggiungi %d al prodotto di %d e %d»?" % (a, b, c), "%d %s %d + %d" % (b, FOIS, c, a),
                 W("%d %s (%d + %d)" % (b, FOIS, c, a), "(%d + %d) %s %d" % (a, b, FOIS, c), "%d + %d + %d" % (a, b, c)), "Prodotto e poi somma: <b>%d %s %d + %d</b>." % (b, FOIS, c, a))
    if k == "diff_quad":
        if a <= b:
            a, b = b + 2, a
        return M("Quale espressione traduce: «il quadrato della differenza tra %d e %d»?" % (a, b), "(%d − %d)²" % (a, b),
                 W("%d² − %d²" % (a, b), "%d − %d²" % (a, b), "(%d − %d) %s 2" % (a, b, FOIS)), "Prima la differenza, poi il quadrato: <b>(%d − %d)²</b>." % (a, b))
    return M("Quale espressione traduce: «il doppio della somma di %d e %d»?" % (a, b), "2 %s (%d + %d)" % (FOIS, a, b),
             W("2 %s %d + %d" % (FOIS, a, b), "(%d + %d)²" % (a, b), "%d + %d %s 2" % (a, b, FOIS)), "Il doppio di tutta la somma: <b>2 %s (%d + %d)</b>." % (FOIS, a, b))


def s5():
    p = K.next()
    k = R.choice(["spesa", "torte", "posti", "giornali", "gara"])
    if k == "spesa":
        a, b, c, d = R.randint(2, 5), R.randint(3, 9), R.randint(2, 4), R.randint(5, 15)
        pay = 50 if a * b + c * d < 50 else 100
        r = pay - (a * b + c * d)
        if r <= 0:
            return None
        return M("%s compra %d quaderni da %d € e %d libri da %d €. Paga con %d €. Quale espressione dà il resto e quanto vale?" % (p[0], a, b, c, d, pay), "%d − (%d %s %d + %d %s %d) = %d €" % (pay, a, FOIS, b, c, FOIS, d, r),
                 W("%d − %d %s %d + %d %s %d = %d €" % (pay, a, FOIS, b, c, FOIS, d, pay - a * b + c * d), "(%d − %d) %s %d + %d %s %d = %d €" % (pay, a, FOIS, b, c, FOIS, d, (pay - a) * b + c * d), "%d − (%d %s %d + %d %s %d) = %d €" % (pay, a, FOIS, b, c, FOIS, d, r + 10)),
                 "Prima la spesa totale (tra parentesi), poi il resto: <b>%d €</b>." % r)
    if k == "torte":
        t, f, m = R.randint(3, 6), R.choice([8, 10, 12]), R.randint(5, 20)
        r = t * f - m
        return M("Per una festa si preparano %d torte da %d fette; se ne mangiano %d. Quante fette restano?" % (t, f, m), str(r), W(t * (f - m) if f > m else None, t * f + m, r + 1, t + f - m),
                 "%d %s %d − %d = %d − %d = <b>%d</b>." % (t, FOIS, f, m, t * f, m, r))
    if k == "posti":
        b, pp, n = R.randint(3, 6), R.choice([50, 52, 54]), R.randint(10, 40)
        r = b * pp - n
        return M("Per una gita ci sono %d pullman da %d posti. I posti liberi sono %d. Quante persone partono?" % (b, pp, n), str(r), W(b * pp + n, b * (pp - n), r + 10, b + pp - n),
                 "%d %s %d − %d = <b>%d</b>." % (b, FOIS, pp, n, r))
    if k == "giornali":
        a, b, g = R.randint(20, 60), R.randint(10, 40), R.randint(5, 7)
        return M("Un’edicola vende %d giornali al mattino e %d al pomeriggio, per %d giorni. Quanti giornali vende?" % (a, b, g), num((a + b) * g), W(num(a + b * g), num(a * g + b), num((a + b) * g + g)),
                 "(%d + %d) %s %d = <b>%s</b>." % (a, b, FOIS, g, num((a + b) * g)))
    a, b, c = R.randint(3, 8), R.randint(2, 5), R.randint(1, 4)
    r = a * 3 + b * 1 - c
    return M("In un torneo una vittoria vale 3 punti, un pareggio 1 punto; si perde 1 punto per ogni cartellino rosso. Una squadra ha %d vittorie, %d pareggi e %d cartellini rossi. Quanti punti ha?" % (a, b, c), str(r),
             W(a + b - c, (a + b) * 3 - c, r + c, a * 3 + b - c * 3), "%d %s 3 + %d %s 1 − %d = <b>%d</b>." % (a, FOIS, b, FOIS, c, r))


def main():
    E5.R = R
    E5.K = Kids(R)
    seen = set()
    sets = [
        ("Ordine delle operazioni", mix(R, seen, [(E5.s1_semplice, 10), (E5.s2_quattro, 10)])),
        ("Parentesi tonde e quadre", mix(R, seen, [(E5.s3_parentesi, 20)])),
        ("Parentesi graffe", mix(R, seen, [(s3_graffe, 20)])),
        ("Espressioni con le potenze e traduzioni", mix(R, seen, [(s4_pot, 12), (s4_traduci, 8)])),
        ("Problemi con le espressioni", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["In un’espressione senza parentesi si calcolano prima le <b>potenze</b>, poi <b>moltiplicazioni e divisioni</b>, infine <b>addizioni e sottrazioni</b>, da sinistra a destra.",
              "Con le parentesi si calcolano prima le <b>tonde</b> ( ), poi le <b>quadre</b> [ ], poi le <b>graffe</b> { }.",
              "Dentro ogni parentesi vale lo stesso ordine delle operazioni.",
              "Per tradurre una frase pensa a quale operazione si fa per ultima: «il doppio della somma» → 2 × (a + b)."],
             [("{[(3 + 5) × 2 − 4] + 6} : 3", ["tonde: 8", "quadre: 8 × 2 − 4 = 12", "graffe: 12 + 6 = 18", "18 : 3 = 6"], "6")],
             [["Calcolare da sinistra a destra: 5 + 3 × 2 = 16", "Prima la moltiplicazione: 5 + 6 = 11."],
              ["Fare (2 + 3)² = 4 + 9", "Prima la parentesi: 5² = 25."],
              ["Togliere le parentesi senza calcolarle", "Le parentesi spariscono solo quando dentro resta un numero."]],
             table(["Ordine", "Che cosa"], [["1", "parentesi tonde, quadre, graffe"], ["2", "potenze"], ["3", "× e :"], ["4", "+ e −"]]))
    faq = [("Perché esiste un ordine delle operazioni?", "Perché ognuno deve ottenere lo stesso risultato leggendo la stessa espressione: è una regola condivisa in tutto il mondo."),
           ("Le calcolatrici rispettano l’ordine?", "Quelle scientifiche sì; quelle semplici spesso calcolano da sinistra a destra, quindi conviene fare attenzione.")]
    unit(G, R, "espressioni", "N",
         "Eseguire espressioni di calcolo con i numeri conosciuti, essendo consapevoli del significato delle parentesi e delle convenzioni sulla precedenza delle operazioni",
         "Le espressioni con le parentesi e le potenze", "Espressioni",
         "Schede di matematica per la prima media sulle espressioni: ordine delle operazioni, parentesi tonde, quadre e graffe, espressioni con le potenze, tradurre frasi in espressioni e problemi. 100 esercizi con soluzioni.",
         "Tonde, quadre, graffe; poi potenze, × e :, + e −.", "Dentro le parentesi vale lo stesso ordine.",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
