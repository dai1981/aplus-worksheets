# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Calcolo mentale (Numeri)
  python3 tools/gen_it_matematica_c3_calcolo_mentale.py
Amici del 10 e del 100, aggiungere e togliere decine e centinaia, doppio e metà, strategie (scomporre,
arrivare alla decina, compensare), proprietà commutativa, problemi veloci.
Errori: complemento a 100 sbagliato di 10 (37 + 73), dimenticare di cambiare decina, metà di 70 = 30.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS

R = random.Random(70303)
K = Kids(R)


def s1_amici():
    k = R.choice(["10", "100", "100", "1000"])
    if k == "10":
        a = R.randint(1, 9)
        b = 10 - a
        return mcq("Quanto manca a %d per arrivare a 10? %d + ☐ = 10" % (a, a), str(b), [str(b + 1), str(b - 1) if b > 1 else "11", str(10 + a)],
                   "%d + %d = 10. Gli amici del 10 sono coppie che fanno 10: <b>%d</b>." % (a, b, b))
    if k == "100":
        a = R.randint(11, 89)
        if a % 10 == 0:
            return None
        b = 100 - a
        w = [(9 - a // 10) * 10 + (10 - a % 10) + 10 if a % 10 else None, (10 - a // 10) * 10 + (10 - a % 10), 100 - a + 10, b - 10, b + 1]
        return mcq("Completa: %d + ☐ = 100" % a, str(b), [str(x) for x in w if x and 0 < x < 100 and x != b],
                   "Prima arrivi alla decina: %d + %d = %d; poi a 100: %d + %d = 100. In tutto <b>%d</b>." % (a, 10 - a % 10, a + 10 - a % 10, a + 10 - a % 10, 100 - a - 10 + a % 10, b))
    a = R.randint(1, 9) * 100
    if R.random() < 0.5:
        a = R.randint(1, 19) * 50
    b = 1000 - a
    return mcq("Completa: %s + ☐ = 1000" % num(a), num(b), [num(b + 100), num(b - 100) if b > 100 else num(b + 50), num(100 - a // 10) if a < 1000 else None, num(b + 50)],
               "%s + %s = 1000: <b>%s</b>." % (num(a), num(b), num(b)))


def s2_decine():
    a = R.randint(101, 899)
    k = R.choice(["+d", "-d", "+h", "-h", "+dd"])
    if k == "+d":
        t = R.randint(2, 9) * 10
        r = a + t
        if r > 999:
            return None
        return mcq("Calcola a mente: %s + %d" % (num(a), t), num(r), [num(a + t // 10), num(r - 100) if r // 100 != a // 100 else num(r + 100), num(r + 10)],
                   "Aggiungi %d decine: %s + %d = <b>%s</b>." % (t // 10, num(a), t, num(r)))
    if k == "-d":
        t = R.randint(2, 9) * 10
        r = a - t
        if r < 10:
            return None
        return mcq("Calcola a mente: %s − %d" % (num(a), t), num(r), [num(a - t // 10), num(r + 100) if r // 100 != a // 100 else num(r - 100), num(r - 10)],
                   "Togli %d decine: %s − %d = <b>%s</b>." % (t // 10, num(a), t, num(r)))
    if k == "+h":
        t = R.randint(1, 5) * 100
        r = a + t
        if r > 999:
            return None
        return mcq("Calcola a mente: %s + %d" % (num(a), t), num(r), [num(a + t // 10), num(a + t // 100), num(r + 10)],
                   "Cambia solo la cifra delle centinaia: %s + %d = <b>%s</b>." % (num(a), t, num(r)))
    if k == "-h":
        t = R.randint(1, a // 100) * 100
        r = a - t
        if r < 10:
            return None
        return mcq("Calcola a mente: %s − %d" % (num(a), t), num(r), [num(a - t // 10), num(r + 10), num(a + t) if a + t < 1000 else num(r - 1)],
                   "Cambia solo la cifra delle centinaia: %s − %d = <b>%s</b>." % (num(a), t, num(r)))
    b = R.randint(11, 89)
    r = a + b
    if r > 999 or b % 10 == 0:
        return None
    return mcq("Calcola a mente: %s + %d" % (num(a), b), num(r), [num(r - 10), num(r + 10), num(a + b // 10 + b % 10 * 10)],
               "Prima le decine, poi le unità: %s + %d = %s; %s + %d = <b>%s</b>." % (num(a), b // 10 * 10, num(a + b // 10 * 10), num(a + b // 10 * 10), b % 10, num(r)))


def s3_doppio():
    k = R.choice(["doppio", "doppio", "meta", "meta", "triplo"])
    if k == "doppio":
        a = R.choice([R.randint(11, 49), R.randint(1, 4) * 100 + R.randint(1, 9) * 10, R.randint(13, 45)])
        r = 2 * a
        return mcq("Qual è il doppio di %s?" % num(a), num(r), [num(a + 2), num(r + 10), num(r - 10), num(a // 2) if a % 2 == 0 else None],
                   "Il doppio è %s %s 2 = %s + %s = <b>%s</b>." % (num(a), FOIS, num(a), num(a), num(r)))
    if k == "meta":
        a = R.choice([R.randint(5, 49) * 2, R.randint(1, 9) * 100, R.randint(11, 49) * 10])
        r = a // 2
        w = [a * 2, r + 10, r - 10, a - 2]
        if a % 20 == 10:
            w.insert(0, (a - 10) // 2)
        return mcq("Qual è la metà di %s?" % num(a), num(r), [num(x) for x in w if 0 < x < 1000],
                   "La metà è %s : 2 = <b>%s</b>, perché %s + %s = %s." % (num(a), num(r), num(r), num(r), num(a)))
    a = R.randint(11, 33)
    r = 3 * a
    return mcq("Qual è il triplo di %d?" % a, str(r), [str(2 * a), str(a + 3), str(r + 10)],
               "Il triplo è %d %s 3 = %d + %d + %d = <b>%d</b>." % (a, FOIS, a, a, a, r))


def s4_strategie():
    k = R.choice(["comp+", "comp-", "decina", "comm", "tre"])
    if k == "comp+":
        a = R.randint(110, 880)
        n9 = R.choice([9, 19, 29, 39, 49, 99])
        r = a + n9
        if r > 999:
            return None
        return mcq("Calcola a mente: %s + %d (pensa a %d − 1)" % (num(a), n9, n9 + 1), num(r), [num(r + 2), num(a + n9 + 1), num(r - 10)],
                   "%s + %d = %s, poi togli 1: <b>%s</b>." % (num(a), n9 + 1, num(a + n9 + 1), num(r)))
    if k == "comp-":
        a = R.randint(150, 990)
        n9 = R.choice([9, 19, 29, 49, 99])
        r = a - n9
        if r < 10:
            return None
        return mcq("Calcola a mente: %s − %d (pensa a %d − 1)" % (num(a), n9, n9 + 1), num(r), [num(r - 2), num(a - n9 - 1), num(r + 10)],
                   "%s − %d = %s, poi aggiungi 1: <b>%s</b>." % (num(a), n9 + 1, num(a - n9 - 1), num(r)))
    if k == "decina":
        a = R.randint(10, 98) * 10 + R.randint(5, 9)
        b = R.randint(6, 9)
        r = a + b
        if r > 999:
            return None
        return mcq("Calcola a mente: %s + %d" % (num(a), b), num(r), [num(r - 10), num(a // 10 * 10 + (a % 10 + b) % 10), num(r + 1)],
                   "Arriva alla decina: %s + %d = %s, poi aggiungi %d: <b>%s</b>." % (num(a), 10 - a % 10, num(a + 10 - a % 10), b - (10 - a % 10), num(r)))
    if k == "comm":
        a, b = R.randint(5, 9), R.randint(120, 860)
        r = a + b
        return mcq("Qual è il modo più facile per calcolare %d + %s?" % (a, num(b)), "%s + %d" % (num(b), a),
                   ["%d + %s" % (b // 10, num(a * 10)), "%s − %d" % (num(b), a), "%d + %d" % (a, b // 100)],
                   "L’addizione è commutativa: puoi partire dal numero più grande, %s + %d = %s." % (num(b), a, num(r)))
    a, b, c = R.randint(11, 89), R.randint(11, 89), None
    c = (10 - (a % 10)) % 10 + 10 * R.randint(1, 5)
    if c <= 10 or a + b + c > 300:
        return None
    r = a + b + c
    return mcq("Calcola a mente: %d + %d + %d" % (a, b, c), str(r), [str(r - 10), str(r + 10), str(a + b)],
               "Cerca la coppia comoda: %d + %d = %d, poi + %d = <b>%d</b>." % (a, c, a + c, b, r))


def s5_problema():
    p = K.next()
    k = R.choice(["pagine", "figurine", "km", "doppio", "meta", "mancano"])
    if k == "pagine":
        t, l = R.randint(120, 400), R.choice([90, 99, 100, 50, 40])
        return mcq("%s legge un libro di %s pagine. Ne ha già lette %s. Quante pagine deve ancora leggere?" % (p[0], num(t + l), num(t)), num(l),
                   [num(t + l + t) if t + l + t < 1000 else num(l + 10), num(l + 10), num(l - 10)],
                   "%s − %s = <b>%s</b> pagine." % (num(t + l), num(t), num(l)))
    if k == "figurine":
        a, b = R.randint(120, 480), R.choice([30, 40, 50, 60, 90, 100, 200])
        return mcq("%s ha %s figurine. Ne riceve altre %d. Quante figurine ha adesso?" % (p[0], num(a), b), num(a + b),
                   [num(a - b), num(a + b // 10), num(a + b + 10)],
                   "%s + %d = <b>%s</b> figurine." % (num(a), b, num(a + b)))
    if k == "km":
        a = R.randint(2, 7) * 100
        b = R.choice([50, 90, 99, 150])
        return mcq("Un treno percorre %s km. Poi ne percorre altri %d. Quanti chilometri percorre in tutto?" % (num(a), b), num(a + b) + " km",
                   [num(a + b - 10) + " km", num(a - b) + " km", num(a + b + 1) + " km" if b != 99 else num(a + 100) + " km"],
                   "%s + %d = <b>%s km</b>." % (num(a), b, num(a + b)))
    if k == "doppio":
        a = R.randint(12, 45)
        return mcq("%s ha %d biglie. Sua sorella ne ha il doppio. Quante biglie ha la sorella?" % (p[0], a), str(2 * a), [str(a + 2), str(a // 2) if a % 2 == 0 else str(a + 10), str(2 * a + 10)],
                   "Il doppio di %d è %d + %d = <b>%d</b>." % (a, a, a, 2 * a))
    if k == "meta":
        a = R.randint(12, 49) * 2
        return mcq("In una gita ci sono %d bambini. La metà prende il pullman rosso. Quanti bambini prendono il pullman rosso?" % a, str(a // 2),
                   [str(a * 2), str(a - 2), str(a // 2 + 10)],
                   "La metà di %d è <b>%d</b>." % (a, a // 2))
    a = R.randint(110, 880)
    b = (a // 100 + 1) * 100
    return mcq("Per finire l’album servono %s figurine. %s ne ha %s. Quante gliene mancano?" % (num(b), p[0], num(a)), num(b - a),
               [num(b - a + 10), num(b - a - 10) if b - a > 10 else num(b - a + 1), num(b + a) if b + a < 1000 else num(b - a + 100)],
               "Da %s a %s: %s + %d = %s. Ne mancano <b>%d</b>." % (num(a), num(b), num(a), b - a, num(b), b - a))


def main():
    seen = set()
    sets = [
        ("Amici del 10, del 100 e del 1000", mix(R, seen, [(s1_amici, 20)])),
        ("Aggiungere e togliere decine e centinaia", mix(R, seen, [(s2_decine, 20)])),
        ("Doppio, metà e triplo", mix(R, seen, [(s3_doppio, 20)])),
        ("Strategie di calcolo", mix(R, seen, [(s4_strategie, 20)])),
        ("Problemi veloci", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Nel calcolo mentale scomponi i numeri in centinaia, decine e unità e calcoli un pezzo alla volta.",
         "Gli <b>amici del 10</b> (3 + 7, 4 + 6…) aiutano ad arrivare alla decina; gli <b>amici del 100</b> (35 + 65) ad arrivare al centinaio.",
         "Per aggiungere 9, aggiungi 10 e togli 1. Per togliere 19, togli 20 e aggiungi 1.",
         "Il <b>doppio</b> è il numero preso 2 volte; la <b>metà</b> è il numero diviso in 2 parti uguali."],
        [("37 + ☐ = 100", ["37 + 3 = 40", "40 + 60 = 100", "3 + 60 = 63"], "63"),
         ("458 + 29", ["458 + 30 = 488", "488 − 1 = 487"], "487")],
        [["37 + 73 = 100", "Arriva prima alla decina (40), poi al 100: 37 + 63 = 100."],
         ["195 + 10 = 105", "Quando le decine arrivano a 10, cambia il centinaio: 205."],
         ["La metà di 70 è 30", "Scomponi: metà di 60 = 30, metà di 10 = 5, quindi 35."]])
    faq = [("Perché il calcolo mentale è importante?", "Rende veloci i calcoli di tutti i giorni e aiuta a controllare i risultati delle operazioni in colonna."),
           ("Quale strategia è la migliore?", "Quella che rende i numeri più comodi: arrivare alla decina, compensare (+ 10 − 1) o scambiare l’ordine degli addendi.")]
    make_unit(R, "calcolo-mentale", "N",
              "Eseguire mentalmente semplici operazioni con i numeri naturali e verbalizzare le procedure di calcolo; usare le proprietà delle operazioni per calcolare più velocemente",
              "Calcolo mentale: amici del 100, doppio, metà e strategie", "Calcolo mentale",
              "Schede di matematica per la classe terza sul calcolo mentale: amici del 10 e del 100, aggiungere e togliere decine e centinaia, doppio e metà, strategie e problemi. 100 esercizi con soluzioni.",
              "Scomponi i numeri e calcola un pezzo alla volta.", "Per + 9 fai + 10 − 1.",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
