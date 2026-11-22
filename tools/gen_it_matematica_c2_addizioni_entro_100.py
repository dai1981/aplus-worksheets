# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Le addizioni entro il 100 (Numeri)
  python3 tools/gen_it_matematica_c2_addizioni_entro_100.py
Amici del 10, addizioni entro il 20 con il passaggio della decina, aggiungere le decine, addizioni con numeri di due
cifre (prima le decine, poi le unità), proprietà commutativa e associativa, numero mancante, problemi.
Errori: contare anche il numero di partenza, 38 + 5 = 33, sommare le decine con le unità (24 + 3 = 54).
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids
import it_c2 as C

R = random.Random(70204)
G = "classe-seconda"
K = Kids(R)


def w(r, extra=()):
    return [num(x) for x in list(extra) + [r + 1, r - 1, r + 10, r - 10] if 0 <= x <= 100 and x != r]


def s1_amici():
    a = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq("Completa: %d + ☐ = 10" % a, str(10 - a), [str(11 - a), str(9 - a) if a < 9 else "2", str(a)], "%d + %d = 10: sono amici del 10. <b>%d</b>." % (a, 10 - a, 10 - a))
    b = R.randint(2, 9)
    if a + b <= 10:
        return None
    r = a + b
    return mcq("Calcola: %d + %d" % (a, b), str(r), w(r, [r - 10 + 1]), "Arriva al 10: %d + %d = 10, poi aggiungi %d. <b>%d</b>." % (a, 10 - a, b - (10 - a), r))


def s1_figure():
    k = R.choice(C.KINDS)
    a, b = R.randint(3, 9), R.randint(3, 9)
    return mcq(C.riga(a, k, 10) + C.riga(b, k, 10) + "%s %s ci sono in tutto?" % (C.quanti(k), C.nome(k)), str(a + b), w(a + b),
               "%d + %d = <b>%d</b>." % (a, b, a + b))


def s2_decine():
    a = R.randint(11, 79)
    t = R.randint(1, 9) * 10
    if a + t > 100:
        return None
    r = a + t
    if R.random() < 0.3:
        a = R.randint(1, 9) * 10
        t = R.randint(1, 9) * 10
        if a + t > 100:
            return None
        r = a + t
        return mcq("Calcola: %d + %d" % (a, t), num(r), w(r, [a // 10 + t // 10]), "%d decine + %d decine = %d decine: <b>%d</b>." % (a // 10, t // 10, r // 10, r))
    return mcq("Calcola: %d + %d" % (a, t), num(r), w(r, [a + t // 10]), "Aggiungi %s: cambia solo la cifra delle decine. <b>%d</b>." % ("1 decina" if t == 10 else "%d decine" % (t // 10), r))


def s3_due_cifre():
    a, b = R.randint(11, 69), R.randint(11, 39)
    r = a + b
    if r > 99:
        return None
    nc = (a // 10 + b // 10) * 10 + (a % 10 + b % 10) % 10
    return mcq("Calcola: %d + %d" % (a, b), num(r), w(r, [nc] if nc != r else []),
               "Prima le decine: %d + %d = %d. Poi le unità: %d + %d = %d. <b>%d</b>." % (a, b // 10 * 10, a + b // 10 * 10, a + b // 10 * 10, b % 10, r, r))


def s3_passaggio():
    a = R.randint(1, 8) * 10 + R.randint(5, 9)
    b = R.randint(3, 9)
    r = a + b
    if r > 100 or a % 10 + b < 10:
        return None
    return mcq("Calcola: %d + %d" % (a, b), num(r), w(r, [r - 10]), "Arriva alla decina: %d + %d = %d, poi + %d = <b>%d</b>." % (a, 10 - a % 10, a + 10 - a % 10, b - (10 - a % 10), r))


def s4_mancante():
    a = R.randint(10, 70)
    b = R.randint(5, 29)
    r = a + b
    if r > 100:
        return None
    if R.random() < 0.5:
        return mcq("Quale numero manca? %d + ☐ = %d" % (a, r), str(b), [str(r + a) if r + a <= 100 else str(b + 1), str(b + 10), str(b - 1)],
                   "Conta da %d fino a %d: mancano <b>%d</b>. Prova: %d + %d = %d." % (a, r, b, a, b, r))
    return mcq("Quale numero manca? ☐ + %d = %d" % (b, r), str(a), [str(a + 1), str(a - 10) if a > 10 else str(a + 10), str(r + b) if r + b <= 100 else str(a - 1)],
               "%d − %d = <b>%d</b>." % (r, b, a))


def s4_tre():
    a, b, c = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
    if (a + b) % 10 and (b + c) % 10 and (a + c) % 10:
        c = 10 - a if 10 - a >= 2 else c
    r = a + b + c
    return mcq("Calcola: %d + %d + %d" % (a, b, c), str(r), w(r, [a + b, r + 2]),
               "Cerca gli amici del 10 se ci sono, poi somma il resto: <b>%d</b>." % r)


def s5():
    p = K.next()
    k = R.choice(["figurine", "pagine", "autobus", "biglie", "fiori", "punti"])
    a, b = R.randint(12, 58), R.randint(8, 39)
    r = a + b
    if r > 100:
        return None
    t = {"figurine": "%s ha %d figurine. Ne vince altre %d. Quante figurine ha ora?" % (p[0], a, b),
         "pagine": "%s legge %d pagine lunedì e %d martedì. Quante pagine legge in tutto?" % (p[0], a, b),
         "autobus": "Sull’autobus ci sono %d persone. Ne salgono %d. Quante persone ci sono ora?" % (a, b),
         "biglie": "%s ha %d biglie rosse e %d biglie blu. Quante biglie ha?" % (p[0], a, b),
         "fiori": "In un giardino ci sono %d margherite e %d rose. Quanti fiori ci sono?" % (a, b),
         "punti": "%s fa %d punti nella prima partita e %d nella seconda. Quanti punti fa in tutto?" % (p[0], a, b)}[k]
    return mcq(t, num(r), w(r, [a - b] if a > b else []), "%d + %d = <b>%d</b>." % (a, b, r))


def main():
    seen = set()
    sets = [
        ("Amici del 10 e passaggio della decina", mix(R, seen, [(s1_amici, 12), (s1_figure, 8)])),
        ("Aggiungere le decine", mix(R, seen, [(s2_decine, 20)])),
        ("Addizioni con numeri di due cifre", mix(R, seen, [(s3_due_cifre, 12), (s3_passaggio, 8)])),
        ("Numero mancante e tre addendi", mix(R, seen, [(s4_mancante, 12), (s4_tre, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Gli <b>amici del 10</b> sono coppie che fanno 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.",
         "Per superare la decina arriva prima al 10: 8 + 5 = 8 + 2 + 3 = 13.",
         "Con i numeri di due cifre aggiungi prima le <b>decine</b>, poi le <b>unità</b>: 34 + 25 = 54 + 5 = 59.",
         "Puoi cambiare l’ordine degli addendi: il risultato non cambia (proprietà commutativa)."],
        [("38 + 5", ["38 + 2 = 40", "40 + 3 = 43"], "43")],
        [["Contare anche il numero da cui parti", "Parti dal numero e conta solo i passi in avanti."],
         ["38 + 5 = 33", "Superi la decina: il risultato è più grande, 43."],
         ["24 + 3 = 54", "Il 3 sono unità: si somma con il 4, 27."]])
    faq = [("Perché sono importanti gli amici del 10?", "Perché aiutano a superare la decina a mente: basta arrivare a 10 e poi aggiungere il resto."),
           ("Si può usare la tabella del 100 per le addizioni?", "Sì: si scende di una riga per ogni decina e ci si sposta a destra per le unità.")]
    make_unit(R, "addizioni-entro-100", "N",
              "Eseguire mentalmente semplici addizioni con i numeri naturali e verbalizzare le procedure di calcolo; conoscere con sicurezza le combinazioni additive entro il 20",
              "Le addizioni entro il 100", "Addizioni entro 100",
              "Schede di matematica per la classe seconda sulle addizioni entro il 100: amici del 10, passaggio della decina, aggiungere decine, numeri di due cifre, numero mancante e problemi. 100 esercizi con soluzioni.",
              "Prima arriva al 10, poi aggiungi il resto.", "Prima le decine, poi le unità.",
              body, faq, sets, 4, grade=G)


if __name__ == "__main__":
    main()
