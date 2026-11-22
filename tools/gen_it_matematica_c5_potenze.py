# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Le potenze (Numeri)
  python3 tools/gen_it_matematica_c5_potenze.py
Base ed esponente, scrivere un prodotto di fattori uguali come potenza, calcolare potenze, quadrati e cubi,
potenze del 10 e forma polinomiale, esponente 1 e 0, problemi.
Errori: 3² = 6 (base × esponente), 10⁴ = 1000, 5⁰ = 0.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, table

R = random.Random(70509)
G = "classe-quinta"
K = Kids(R)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def pw(b, e):
    return "%s%s" % (num(b), str(e).translate(SUP))


def s1_scrivi():
    b, e = R.randint(2, 9), R.randint(2, 6)
    prod = (" %s " % FOIS).join([str(b)] * e)
    return mcq("Come si scrive %s come potenza?" % prod, pw(b, e), [pw(e, b), "%d %s %d" % (b, FOIS, e), pw(b, e + 1), pw(b, e - 1) if e > 2 else pw(b * e, 1)],
               "Il %d è moltiplicato per se stesso %d volte: base %d, esponente %d. <b>%s</b>." % (b, e, b, e, pw(b, e)))


def s1_parti():
    b, e = R.randint(2, 12), R.randint(2, 5)
    if b == e:
        return None
    if R.random() < 0.5:
        return mcq("Nella potenza %s qual è la base?" % pw(b, e), str(b), [str(e), str(b ** e), str(b * e)], "La base è il numero in basso, quello che si moltiplica: <b>%d</b>." % b)
    return mcq("Nella potenza %s che cosa indica l’esponente %d?" % (pw(b, e), e), "quante volte si moltiplica la base", ["per quanto si moltiplica la base", "quante volte si somma la base", "il risultato"],
               "L’esponente dice <b>quante volte la base si moltiplica per se stessa</b>: %s = %s." % (pw(b, e), (" %s " % FOIS).join([str(b)] * e)))


def calc(b, e):
    r = b ** e
    w = [b * e, b + e, b ** (e - 1) if e > 1 else b + 1, b ** (e + 1), e ** b if e ** b != r else r + b]
    return mcq("Quanto fa %s?" % pw(b, e), num(r), [num(x) for x in w if x != r],
               "%s = %s = <b>%s</b> (non %d %s %d!)." % (pw(b, e), (" %s " % FOIS).join([num(b)] * e) if e <= 6 else "…", num(r), b, FOIS, e))


def s2():
    return calc(R.randint(2, 15), 2) if R.random() < 0.6 else calc(R.randint(2, 10), 3)


def s3():
    b, e = R.choice([(2, R.randint(4, 10)), (3, R.randint(4, 6)), (4, 4), (5, 4), (R.randint(2, 9), 1), (R.randint(2, 9), 0), (R.choice([20, 30, 40, 50]), 2)])
    if e <= 1:
        r = b ** e
        return mcq("Quanto fa %s?" % pw(b, e), str(r), [str(b) if e == 0 else "1", "0", str(b * 10)] if e == 0 else ["1", "0", str(b * b)],
                   "%s. <b>%d</b>." % ("Ogni numero (diverso da 0) con esponente 0 dà 1" if e == 0 else "Con esponente 1 il risultato è la base", r))
    return calc(b, e)


def s4_dieci():
    k = R.choice(["val", "esp", "poli", "poli"])
    if k == "val":
        e = R.randint(2, 9)
        return mcq("Quanto fa %s?" % pw(10, e), num(10 ** e), [num(10 ** (e - 1)), num(10 ** (e + 1)), num(10 * e)],
                   "%s è 1 seguito da %d zeri: <b>%s</b>." % (pw(10, e), e, num(10 ** e)))
    if k == "esp":
        e = R.randint(3, 9)
        return mcq("%s si scrive come potenza del 10…" % num(10 ** e), pw(10, e), [pw(10, e - 1), pw(10, e + 1), pw(e, 10)],
                   "Conta gli zeri: sono %d. <b>%s</b>." % (e, pw(10, e)))
    n = R.randint(1000, 99999)
    s = str(n)
    parts = [(int(c), len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    ok = " + ".join("%d %s %s" % (c, FOIS, pw(10, e)) if e else str(c) for c, e in parts)
    w1 = " + ".join("%d %s %s" % (c, FOIS, pw(10, e + 1)) if e else str(c) for c, e in parts)
    w2 = " + ".join("%d %s %s" % (c, FOIS, pw(10, e - 1)) if e > 1 else ("%d %s 10" % (c, FOIS) if e == 1 else str(c)) for c, e in parts)
    w3 = " + ".join("%s %s %d" % (pw(c, e), FOIS, 10) if e else str(c) for c, e in parts)
    return mcq("Qual è la forma polinomiale di %s?" % num(n), ok, [w1, w2, w3],
               "Ogni cifra si moltiplica per la potenza del 10 del suo posto: <b>%s</b>." % ok)


def s4_confronta():
    a, b = R.sample([(2, 5), (5, 2), (3, 4), (4, 3), (2, 6), (6, 2), (3, 3), (10, 2), (2, 10), (9, 2), (2, 7), (7, 2), (4, 4)], 2)
    va, vb = a[0] ** a[1], b[0] ** b[1]
    if va == vb:
        return None
    g = pw(*a) if va > vb else pw(*b)
    return mcq("Qual è la potenza maggiore: %s o %s?" % (pw(*a), pw(*b)), g, [pw(*b) if g == pw(*a) else pw(*a), "sono uguali", "non si può sapere"],
               "%s = %s e %s = %s: la maggiore è <b>%s</b>." % (pw(*a), num(va), pw(*b), num(vb), g))


def s5():
    p = K.next()
    k = R.choice(["quadrato", "cubo", "catena", "batteri", "scatole"])
    if k == "quadrato":
        l = R.randint(3, 15)
        return mcq("Un orto quadrato ha il lato di %d m. Quanti quadrati di 1 m di lato servono per ricoprirlo?" % l, num(l * l), [num(l * 4), num(l * 2), num((l + 1) ** 2)],
                   "%d %s %d = %s = <b>%s</b>." % (l, FOIS, l, pw(l, 2), num(l * l)))
    if k == "cubo":
        l = R.randint(2, 6)
        return mcq("%s costruisce un grande cubo con cubetti: %d cubetti per ogni spigolo. Quanti cubetti usa?" % (p[0], l), num(l ** 3), [num(l * 3), num(l ** 2), num(l * 12)],
                   "%d %s %d %s %d = %s = <b>%s</b>." % (l, FOIS, l, FOIS, l, pw(l, 3), num(l ** 3)))
    if k == "catena":
        g = R.randint(3, 5)
        return mcq("%s manda un messaggio a 2 amici; il giorno dopo ognuno lo manda ad altri 2, e così via. Quante persone lo ricevono il giorno %d?" % (p[0], g), num(2 ** g),
                   [num(2 * g), num(2 ** (g + 1)), num(2 ** (g - 1))], "Ogni giorno si moltiplica per 2: %s = <b>%s</b>." % (pw(2, g), num(2 ** g)))
    if k == "batteri":
        h = R.randint(3, 6)
        return mcq("In un esperimento i batteri raddoppiano ogni ora. All’inizio c’è 1 batterio. Quanti sono dopo %d ore?" % h, num(2 ** h), [num(2 * h), num(2 ** (h + 1)), num(h ** 2)],
                   "1 %s %s = <b>%s</b>." % (FOIS, pw(2, h), num(2 ** h)))
    a = R.choice([3, 4, 5, 10])
    return mcq("In un magazzino ci sono %d scaffali, ogni scaffale ha %d scatole, ogni scatola ha %d pacchi. Quanti pacchi ci sono?" % (a, a, a), num(a ** 3),
               [num(a * 3), num(a ** 2), num(a + a + a)], "%d %s %d %s %d = %s = <b>%s</b>." % (a, FOIS, a, FOIS, a, pw(a, 3), num(a ** 3)))


def main():
    seen = set()
    sets = [
        ("Base ed esponente", mix(R, seen, [(s1_scrivi, 12), (s1_parti, 8)])),
        ("Quadrati e cubi", mix(R, seen, [(s2, 20)])),
        ("Calcolare le potenze", mix(R, seen, [(s3, 20)])),
        ("Potenze del 10 e confronti", mix(R, seen, [(s4_dieci, 14), (s4_confronta, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Una <b>potenza</b> è una moltiplicazione di fattori uguali: 5 %s 5 %s 5 = 5³." % (FOIS, FOIS),
         "Il numero in basso è la <b>base</b>, quello piccolo in alto è l’<b>esponente</b>: dice quante volte si moltiplica la base.",
         "5² si legge «5 al quadrato», 5³ «5 al cubo». Con esponente 1 il risultato è la base; con esponente 0 il risultato è 1.",
         "Le potenze del 10 sono 1 seguito da tanti zeri quanto dice l’esponente: 10⁴ = 10 000."],
        [("Calcola 3⁴", ["3 %s 3 = 9" % FOIS, "9 %s 3 = 27" % FOIS, "27 %s 3 = 81" % FOIS], "81")],
        [["3² = 6", "Non è 3 %s 2: è 3 %s 3 = 9." % (FOIS, FOIS)],
         ["10⁴ = 1000", "Gli zeri sono quanti l’esponente: 10 000."],
         ["5⁰ = 0", "Ogni numero diverso da 0 con esponente 0 vale 1."]],
        table(["n", "n²", "n³"], [[str(n), str(n * n), str(n ** 3)] for n in range(2, 7)]))
    faq = [("Perché 5² si chiama «al quadrato»?", "Perché è il numero di quadratini in un quadrato con il lato di 5: 5 × 5 = 25."),
           ("A che cosa servono le potenze del 10?", "A scrivere velocemente i grandi numeri e la forma polinomiale: 3 × 10³ + 4 × 10² = 3400.")]
    make_unit(R, "potenze", "N",
              "Conoscere le potenze come prodotto di fattori uguali; calcolare semplici potenze; scrivere i numeri in forma polinomiale con le potenze del 10",
              "Le potenze: base ed esponente", "Potenze",
              "Schede di matematica per la classe quinta sulle potenze: base ed esponente, quadrati e cubi, esponente 0 e 1, potenze del 10, forma polinomiale e problemi. 100 esercizi con soluzioni.",
              "L’esponente dice quante volte moltiplicare la base.", "3² = 3 × 3 = 9, non 6.",
              body, faq, sets, 9, grade=G)


if __name__ == "__main__":
    main()
