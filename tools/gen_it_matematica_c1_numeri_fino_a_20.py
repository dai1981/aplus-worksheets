# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: I numeri fino a 20 (Numeri)
  python3 tools/gen_it_matematica_c1_numeri_fino_a_20.py
La decina, decine e unità (da u), regoli e schema del dieci, leggere e scrivere i numeri fino a 20 in cifre e
in parole, retta dei numeri, precedente e successivo, contare a salti di 2.
Errori: scrivere 1 decina e 4 unità come 104, scambiare le cifre (14 e 41), confondere undici, dodici e tredici.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table, tabella_valore
import it_c1 as C

R = random.Random(70102)
G = "classe-prima"


def w(n):
    out = [n + 1, n - 1, n + 10 if n < 10 else n - 10, int(str(n)[::-1]) if n > 10 and n % 10 else None, n + 2]
    return [str(x) for x in out if x is not None and 0 <= x <= 99 and x != n]


def s1_dieci():
    n = R.randint(11, 20)
    k = R.random()
    if k < 0.4:
        return mcq(C.dieci(n, 2) + "Quanti pallini ci sono?", str(n), w(n), "Uno schema pieno = 10. 10 e %d = <b>%d</b>." % (n - 10, n))
    if k < 0.7:
        return mcq(C.regoli(1, n - 10) + "Il regolo lungo vale 10. Quale numero è?", str(n), w(n) + ["%d" % (100 + n - 10)], "1 decina e %d unità = <b>%d</b>." % (n - 10, n))
    kd = R.choice(C.KINDS)
    return mcq(C.riga(n, kd, 10) + "%s ci sono?" % C.Q(kd), str(n), w(n), "Una fila da 10 e %d: <b>%d</b>." % (n - 10, n))


def s1_dau():
    n = R.randint(10, 20)
    d, u = divmod(n, 10)
    k = R.choice(["tab", "da", "quale", "u"])
    if k == "tab":
        return mcq(tabella_valore(n, 2) + "Quale numero è scritto?", str(n), w(n), "da = %d, u = %d: <b>%d</b>." % (d, u, n))
    if k == "da":
        return mcq("Quante decine ci sono nel numero %d?" % n, str(d), [str(u) if u != d else "0", str(n), "10"], "%d = %d da e %d u: <b>%d</b>." % (n, d, u, d))
    if k == "u":
        return mcq("Quante unità ci sono nel numero %d oltre alla decina?" % n, str(u), [str(n), str(u + 1), "1" if u != 1 else "2"], "%d = 1 decina e <b>%d</b> unità." % (n, u))
    if n == 20:
        return mcq("Quanto fanno 2 decine?", "20", ["2", "12", "22"], "2 decine = 10 + 10 = <b>20</b>.")
    return mcq("Quale numero ha 1 decina e %d unità?" % u, str(n), [str(10 * u + 1) if u else "1", "1%d0" % u if u else "100", str(n + 1)], "1 da e %d u = <b>%d</b>." % (u, n))


def s2_parole():
    n = R.randint(10, 20)
    if R.random() < 0.5:
        return mcq("Come si scrive in cifre «%s»?" % C.num_parola(n), str(n), w(n), "«%s» si scrive <b>%d</b>." % (C.num_parola(n), n))
    alt = [x for x in (n + 1, n - 1, n + 2, n - 2) if 10 <= x <= 20]
    return mcq("Come si scrive in parole il numero %d?" % n, C.num_parola(n), [C.num_parola(x) for x in alt], "%d si scrive <b>%s</b>." % (n, C.num_parola(n)))


def s3_retta():
    n = R.randint(1, 19)
    if n in (10,):
        return None
    marks = {v: str(v) for v in (0, 10, 20)}
    marks[n] = "?"
    return mcq(C.retta(0, 20, marks) + "Quale numero va al posto del «?»?", str(n), [x for x in w(n) if int(x) <= 20], "Conta i trattini partendo dal numero più vicino: <b>%d</b>." % n)


def s3_vicini():
    n = R.randint(10, 19)
    k = R.choice(["prima", "dopo", "tra"])
    if k == "dopo":
        return mcq("Quale numero viene subito dopo il %d?" % n, str(n + 1), [str(n - 1), str(n + 2), str(n + 10) if n + 10 < 30 else str(n)], "%d + 1 = <b>%d</b>." % (n, n + 1))
    if k == "prima":
        n += 1
        return mcq("Quale numero viene subito prima del %d?" % n, str(n - 1), [str(n + 1), str(n - 2), str(n - 10)], "%d − 1 = <b>%d</b>." % (n, n - 1))
    return mcq("Quale numero sta tra %d e %d?" % (n - 1, n + 1), str(n), [str(n - 1), str(n + 1), str(n + 2)], "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))


def s4_salti():
    k = R.choice([2, 2, 5, 10, 1])
    a = R.choice([0, 1, 2]) if k == 2 else 0 if k in (5, 10) else R.randint(5, 12)
    seq = [a + k * i for i in range(5)]
    if seq[-1] > 20:
        return None
    i = R.randint(2, 4)
    show = [str(x) if j != i else "?" for j, x in enumerate(seq)]
    ans = seq[i]
    return mcq(C.carte(show) + "Si conta a salti. Quale numero manca?", str(ans), [str(ans + 1), str(ans - 1), str(ans + k) if ans + k <= 20 else str(ans + 2)],
               "Ogni volta si aggiunge %d: manca il <b>%d</b>." % (k, ans))


def s4_indietro():
    a = R.randint(12, 20)
    seq = [a - i for i in range(5)]
    i = R.randint(1, 4)
    ans = seq[i]
    show = [str(x) if j != i else "?" for j, x in enumerate(seq)]
    return mcq(C.carte(show) + "Si conta all’indietro. Quale numero manca?", str(ans), [str(ans + 2), str(ans - 1), str(ans + 1) if ans + 1 != seq[i - 1] else str(ans - 2)],
               "Ogni volta si toglie 1: manca il <b>%d</b>." % ans)


def s5():
    k = R.choice(["matite", "uova", "piano", "calendario", "squadra", "figurine"])
    if k == "matite":
        u = R.randint(1, 9)
        return mcq("Ho una scatola da 10 matite e altre %d matite sciolte. Quante matite ho?" % u, str(10 + u), [str(u), str(11 + u), str(10 * u + 1)],
                   "10 e %d: <b>%d</b>." % (u, 10 + u))
    if k == "uova":
        n = R.randint(11, 18)
        return mcq("In un cesto ci sono %d uova. Quante decine di uova ci sono? (una decina = 10)" % n, "1 decina e %d uova" % (n - 10), ["%d decine" % (n - 10), "%d decine" % n, "2 decine"],
                   "%d = 10 + %d: <b>1 decina e %d uova</b>." % (n, n - 10, n - 10))
    if k == "piano":
        n = R.randint(11, 19)
        return mcq("Sono al piano %d di un palazzo. Salgo di un piano. A che piano arrivo?" % n, str(n + 1), [str(n - 1), str(n + 2), str(n)], "%d + 1 = <b>%d</b>." % (n, n + 1))
    if k == "calendario":
        n = R.randint(10, 19)
        return mcq("Oggi è il %d. Che giorno era ieri?" % n, "il %d" % (n - 1), ["il %d" % (n + 1), "il %d" % (n - 2), "il %d" % n], "Ieri è un giorno prima: %d − 1 = <b>%d</b>." % (n, n - 1))
    if k == "squadra":
        n = R.randint(7, 15)
        ok = n >= 11
        return mcq("Per una squadra di calcio servono 11 bambini. Oggi ne arrivano %d. Bastano?" % n, "sì" if ok else "no", ["no" if ok else "sì", "non si può sapere", "servono 20 bambini"],
                   "%d è %s 11: <b>%s</b>." % (n, "uguale a" if n == 11 else "più di" if ok else "meno di", "sì" if ok else "no"))
    a = R.randint(11, 19)
    b = a + R.choice([-2, -1, 1, 2])
    if b > 20 or b == a:
        return None
    win = "Anna" if a > b else "Luca"
    return mcq("Anna ha %d figurine, Luca ne ha %d. Chi ne ha di più?" % (a, b), win, ["Luca" if win == "Anna" else "Anna", "ne hanno tante uguali", "non si può sapere"], "%d e %d: ne ha di più <b>%s</b>." % (a, b, win))


def main():
    seen = set()
    sets = [
        ("La decina", mix(R, seen, [(s1_dieci, 20)])),
        ("Decine e unità", mix(R, seen, [(s1_dau, 14), (s2_parole, 6)])),
        ("Leggere e scrivere i numeri", mix(R, seen, [(s2_parole, 10), (s3_vicini, 10)])),
        ("Retta e salti", mix(R, seen, [(s3_retta, 8), (s4_salti, 7), (s4_indietro, 5)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Quando conti 10 oggetti, puoi metterli insieme: fanno una <b>decina</b> (da).",
         "Da 11 a 19 c’è 1 decina e qualche <b>unità</b> (u): 14 = 1 da e 4 u.",
         "20 = 2 decine. Nei numeri di due cifre la cifra a sinistra dice le decine, quella a destra le unità.",
         "Undici, dodici, tredici, quattordici, quindici, sedici, diciassette, diciotto, diciannove, venti."],
        [("1 decina e 6 unità", ["10 + 6"], "16")],
        [["Scrivere 1 decina e 4 unità come 104", "Si scrivono solo due cifre: 14."],
         ["Scambiare le cifre: 41 invece di 14", "Prima le decine (1), poi le unità (4)."],
         ["Confondere 12 e 20", "12 = 1 da e 2 u; 20 = 2 da e 0 u."]],
        table(["Numero", "da", "u"], [["13", "1", "3"], ["17", "1", "7"], ["20", "2", "0"]]))
    faq = [("Perché si raggruppa per 10?", "Perché contare a decine è più veloce e più sicuro: 10 mani di bambini sono 10 decine di dita."),
           ("Come si leggono i numeri da 11 a 16?", "Hanno nomi speciali: undici, dodici, tredici, quattordici, quindici, sedici; da 17 si dice «dicia-»: diciassette, diciotto, diciannove.")]
    make_unit(R, "numeri-fino-a-20", "N",
              "Leggere e scrivere i numeri naturali in notazione decimale, avendo consapevolezza della notazione posizionale; contare in senso progressivo e regressivo e per salti di due",
              "I numeri fino a 20: la decina", "Numeri fino a 20",
              "Schede di matematica per la classe prima sui numeri fino a 20: la decina, decine e unità, regoli e schema del dieci, numeri in cifre e in parole, retta, prima e dopo, salti, problemi. 100 esercizi con soluzioni.",
              "10 unità fanno 1 decina.", "14 = 1 decina e 4 unità.",
              body, faq, sets, 2, grade=G)


if __name__ == "__main__":
    main()
