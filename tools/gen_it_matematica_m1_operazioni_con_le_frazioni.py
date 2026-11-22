# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Operazioni con le frazioni (Numeri)
  python3 tools/gen_it_matematica_m1_operazioni_con_le_frazioni.py
Addizione e sottrazione con denominatori diversi (mcm), moltiplicazione con semplificazione in croce, frazione
reciproca e divisione, potenza di una frazione, espressioni con le frazioni.
Errori: sommare numeratori e denominatori, dividere senza fare il reciproco del secondo termine, elevare solo il numeratore.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, FOIS, DIV

R = random.Random(71109)
G = "prima-media"
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def rf(lo=2, hi=12, proper=True):
    while True:
        b = R.randint(lo, hi)
        a = R.randint(1, b - 1 if proper else 2 * b)
        if gcd(a, b) == 1 and a != b:
            return Fr(a, b)


def s1_som():
    x, y = rf(), rf()
    if x.denominator == y.denominator:
        return None
    sub = R.random() < 0.4
    if sub and x < y:
        x, y = y, x
    r = x - y if sub else x + y
    op = "−" if sub else "+"
    naive = Fr(abs(x.numerator - y.numerator) if sub else x.numerator + y.numerator, x.denominator + y.denominator)
    m = x.denominator * y.denominator // gcd(x.denominator, y.denominator)
    return M("Calcola: %s %s %s" % (fq(x), op, fq(y)), fq(r), W(fq(naive) if naive != r else None, fq(r + Fr(1, m)), fq(Fr((x.numerator - y.numerator) if sub else (x.numerator + y.numerator), m)) if Fr((x.numerator - y.numerator) if sub else (x.numerator + y.numerator), m) != r else None, fq(x * y)),
             "mcm(%d, %d) = %d: %s %s %s = <b>%s</b> (ridotta ai minimi termini)." % (x.denominator, y.denominator, m, frm(x, m), op, frm(y, m), fq(r)))


def frm(x, m):
    from it_common import fr
    return fr(int(x * m), m)


def s2_per():
    x, y = rf(2, 12, False), rf(2, 12, False)
    r = x * y
    return M("Calcola: %s %s %s" % (fq(x), FOIS, fq(y)), fq(r), W(fq(Fr(x.numerator * y.denominator, x.denominator * y.numerator)) if x != y else None, fq(r * 2), fq(Fr(x.numerator + y.numerator, x.denominator * y.denominator)), fq(x + y)),
             "Numeratore per numeratore, denominatore per denominatore (semplifica in croce se puoi): <b>%s</b>." % fq(r))


def s2_rec():
    x = rf(2, 12, False)
    if R.random() < 0.4:
        return M("Qual è il reciproco di %s?" % fq(x), fq(1 / x), W(fq(-x), fq(x), fq(Fr(x.numerator, x.denominator * 2)), "1"), "Si scambiano numeratore e denominatore: <b>%s</b> (%s %s %s = 1)." % (fq(1 / x), fq(x), FOIS, fq(1 / x)))
    y = rf(2, 12, False)
    r = x / y
    return M("Calcola: %s %s %s" % (fq(x), DIV, fq(y)), fq(r), W(fq(x * y), fq(y / x) if y / x != r else None, fq(r * 2), fq(r + 1)),
             "Si moltiplica la prima per il reciproco della seconda: %s %s %s = <b>%s</b>." % (fq(x), FOIS, fq(1 / y), fq(r)))


def s3_pot():
    x = rf(2, 7, False)
    e = R.choice([2, 2, 3])
    r = x ** e
    return M("Calcola: (%s)%s" % (fq(x), str(e).translate(SUP)), fq(r), W(fq(Fr(x.numerator ** e, x.denominator)), fq(Fr(x.numerator * e, x.denominator * e)), fq(x * e), fq(Fr(x.numerator, x.denominator ** e))),
             "Si elevano numeratore e denominatore: <b>%s</b>." % fq(r))


def s4_espr():
    a, b, c = rf(2, 6), rf(2, 6), rf(2, 6, False)
    k = R.choice(["som_per", "per_som", "div"])
    if k == "som_per":
        r = (a + b) * c
        q = "(%s + %s) %s %s" % (fq(a), fq(b), FOIS, fq(c))
        w = a + b * c
        st = "%s + %s = %s; %s %s %s = %s" % (fq(a), fq(b), fq(a + b), fq(a + b), FOIS, fq(c), fq(r))
    elif k == "per_som":
        r = a + b * c
        q = "%s + %s %s %s" % (fq(a), fq(b), FOIS, fq(c))
        w = (a + b) * c
        st = "prima %s %s %s = %s; poi %s + %s = %s" % (fq(b), FOIS, fq(c), fq(b * c), fq(a), fq(b * c), fq(r))
    else:
        if a <= b:
            a, b = b, a
        if a == b:
            return None
        r = (a - b) / c
        q = "(%s − %s) %s %s" % (fq(a), fq(b), DIV, fq(c))
        w = (a - b) * c
        st = "%s − %s = %s; %s %s %s = %s" % (fq(a), fq(b), fq(a - b), fq(a - b), FOIS, fq(1 / c), fq(r))
    return M("Calcola: %s" % q, fq(r), W(fq(w) if w != r else None, fq(r + 1), fq(r * 2), fq(r / 2)), "%s. <b>%s</b>." % (st, fq(r)))


def s5():
    k = R.choice(["torta", "tanica", "viaggio", "pizza", "stipendio"])
    if k == "torta":
        a, b = rf(2, 8), rf(2, 8)
        if a + b >= 1 or a.denominator == b.denominator:
            return None
        r = 1 - a - b
        return M("Luca mangia %s di una torta e Anna %s. Che parte di torta resta?" % (fq(a), fq(b)), fq(r), W(fq(a + b), fq(1 - a), fq(Fr(1, 1) - Fr(a.numerator + b.numerator, a.denominator + b.denominator))),
                 "Mangiano %s + %s = %s; resta 1 − %s = <b>%s</b>." % (fq(a), fq(b), fq(a + b), fq(a + b), fq(r)))
    if k == "tanica":
        x = rf(2, 8)
        n = R.choice([2, 3, 4, 5])
        return M("Una bottiglia contiene %s di litro. Quanti litri ci sono in %d bottiglie?" % (fq(x), n), fq(x * n), W(fq(x / n), fq(Fr(x.numerator, x.denominator * n)), fq(x + n)),
                 "%s %s %d = <b>%s</b> litri." % (fq(x), FOIS, n, fq(x * n)))
    if k == "viaggio":
        a = rf(2, 6)
        b = rf(2, 6)
        r = (1 - a) * b
        return M("Un’auto percorre %s del viaggio al mattino; del resto, ne percorre %s nel pomeriggio. Che parte del viaggio percorre nel pomeriggio?" % (fq(a), fq(b)), fq(r), W(fq(b), fq(a * b), fq(1 - a - b) if 1 - a - b > 0 else fq(r + Fr(1, 2))),
                 "Resto: 1 − %s = %s; %s di %s = %s %s %s = <b>%s</b>." % (fq(a), fq(1 - a), fq(b), fq(1 - a), fq(b), FOIS, fq(1 - a), fq(r)))
    if k == "pizza":
        p = R.choice([2, 3, 4])
        x = Fr(R.choice([1, 3]), R.choice([4, 8]))
        return M("Hai %d pizze. Ognuno ne mangia %s. Per quante persone bastano?" % (p, fq(x)), fq(p / x), W(fq(p * x), fq(x / p), fq(p / x + 1)), "%d %s %s = %d %s %s = <b>%s</b>." % (p, DIV, fq(x), p, FOIS, fq(1 / x), fq(p / x)))
    a, b = rf(2, 5), rf(2, 5)
    if a + b >= 1:
        return None
    s = R.choice([1200, 1500, 1800, 2400])
    if (s * (1 - a - b)).denominator != 1:
        return None
    return M("Di uno stipendio di %d €, %s va per l’affitto e %s per la spesa. Quanti euro restano?" % (s, fq(a), fq(b)), "%d €" % int(s * (1 - a - b)),
             W("%d €" % int(s * (a + b)) if (s * (a + b)).denominator == 1 else None, "%d €" % int(s * (1 - a)) if (s * (1 - a)).denominator == 1 else None, "%d €" % (s - 100)),
             "Spese: %s + %s = %s; resta %s di %d = <b>%d €</b>." % (fq(a), fq(b), fq(a + b), fq(1 - a - b), s, int(s * (1 - a - b))))


def main():
    seen = set()
    sets = [
        ("Addizione e sottrazione", mix(R, seen, [(s1_som, 20)])),
        ("Moltiplicazione", mix(R, seen, [(s2_per, 20)])),
        ("Reciproco e divisione", mix(R, seen, [(s2_rec, 14), (s3_pot, 6)])),
        ("Espressioni con le frazioni", mix(R, seen, [(s4_espr, 14), (s3_pot, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    from it_common import fr as F
    body = L(["<b>Addizione e sottrazione</b>: riduci allo stesso denominatore (mcm), poi somma o sottrai i numeratori. Il denominatore resta.",
              "<b>Moltiplicazione</b>: numeratore per numeratore, denominatore per denominatore. Prima semplifica «in croce».",
              "<b>Divisione</b>: moltiplica la prima frazione per il <b>reciproco</b> della seconda (scambi numeratore e denominatore).",
              "<b>Potenza</b>: si elevano sia il numeratore sia il denominatore. Alla fine riduci sempre ai minimi termini."],
             [("%s + %s" % (F(2, 3), F(1, 4)), ["mcm(3, 4) = 12", "%s + %s" % (F(8, 12), F(3, 12))], F(11, 12))],
             [["%s + %s = %s" % (F(1, 2), F(1, 3), F(2, 5)), "Prima lo stesso denominatore: %s + %s = %s." % (F(3, 6), F(2, 6), F(5, 6))],
              ["Dividere senza fare il reciproco", "%s : %s = %s × %s." % (F(2, 3), F(4, 5), F(2, 3), F(5, 4))],
              ["Elevare solo il numeratore", "(%s)² = %s, non %s." % (F(2, 3), F(4, 9), F(4, 3))]],
             table(["Operazione", "Come si fa"], [["+ e −", "stesso denominatore, poi i numeratori"], ["×", "sopra per sopra, sotto per sotto"], [":", "per il reciproco"], ["potenza", "sopra e sotto"]]))
    faq = [("Perché nella divisione si usa il reciproco?", "Dividere per una frazione equivale a chiedersi quante volte ci sta: dividere per 1/2 vuol dire raddoppiare."),
           ("Si può semplificare prima di moltiplicare?", "Sì, anche «in croce» (il numeratore di una con il denominatore dell’altra): i numeri restano più piccoli.")]
    unit(G, R, "operazioni-con-le-frazioni", "N",
         "Eseguire addizioni, sottrazioni, moltiplicazioni, divisioni e potenze con le frazioni; eseguire semplici espressioni con le frazioni",
         "Operazioni con le frazioni", "Operazioni con le frazioni",
         "Schede di matematica per la prima media sulle operazioni con le frazioni: addizione e sottrazione con il mcm, moltiplicazione, reciproco e divisione, potenza, espressioni e problemi. 100 esercizi con soluzioni.",
         "+ e −: stesso denominatore. ×: sopra per sopra, sotto per sotto.", "Dividere = moltiplicare per il reciproco.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
