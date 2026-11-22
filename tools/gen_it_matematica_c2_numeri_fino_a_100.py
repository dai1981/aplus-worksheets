# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: I numeri fino a 100 (Numeri)
  python3 tools/gen_it_matematica_c2_numeri_fino_a_100.py
Contare a gruppi di 10, decine e unità (da u), leggere e scrivere i numeri in cifre e in lettere, la tabella del 100,
la retta, precedente e successivo, contare avanti e indietro, il centinaio.
Errori: scambiare decine e unità (37 → 73), «trenta e sette» scritto 307, saltare un numero contando.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, blocchi, tabella_valore, lettere, pl
import it_c2 as C

R = random.Random(70201)
G = "classe-seconda"


def w(n):
    d, u = divmod(n, 10)
    out = [u * 10 + d if u else None, n + 10 if n <= 89 else n - 10, n + 1 if n < 99 else n - 2, d + u if d + u != n else None, int("%d0%d" % (d, u)) if u else None]
    return [num(x) for x in out if x and x != n]


def s1_riga():
    n = R.randint(11, 59)
    k = R.choice(C.KINDS)
    return mcq(C.riga(n, k) + "%s %s ci sono?" % (C.quanti(k), C.nome(k)), num(n), w(n),
               "Conta le file da 10: %s e %s. In tutto <b>%d</b>." % (pl(n // 10, "decina", "decine"), pl(n % 10, "unità", "unità"), n))


def s1_blocchi():
    d, u = R.randint(1, 9), R.randint(0, 9)
    n = 10 * d + u
    return mcq(blocchi(0, 0, d, u) + "Quale numero è?", num(n), w(n), "%s e %s: <b>%d</b>." % (pl(d, "decina", "decine"), pl(u, "unità", "unità"), n))


def s2_dau():
    n = R.randint(11, 99)
    d, u = divmod(n, 10)
    k = R.choice(["tab", "da", "u", "quale"])
    if k == "tab":
        return mcq(tabella_valore(n, 2) + "Quale numero è scritto?", num(n), w(n), "da = %d, u = %d: <b>%d</b>." % (d, u, n))
    if k == "da":
        return mcq("Quante decine ci sono in %d?" % n, str(d), [str(u) if u != d else str(d + 1), str(n), str(d + 1) if u != d + 1 else str(d - 1)], "%d = %d da e %d u: <b>%d</b> decine." % (n, d, u, d))
    if k == "u":
        return mcq("Quante unità ci sono in %d (cifra delle unità)?" % n, str(u), [str(d) if d != u else str(u + 1), str(n), "10"], "%d = %d da e <b>%d</b> u." % (n, d, u))
    return mcq("Quale numero ha %s e %s?" % (pl(d, "decina", "decine"), pl(u, "unità", "unità")), num(n), w(n), "%d da e %d u = <b>%d</b>." % (d, u, n))


def s3_lettere():
    n = R.randint(11, 99)
    if R.random() < 0.5:
        return mcq("Scrivi in cifre: <b>%s</b>" % lettere(n), num(n), w(n), "«%s» = <b>%d</b>." % (lettere(n), n))
    alt = [x for x in (int(str(n)[::-1]) if n % 10 else n + 1, n + 10 if n < 90 else n - 10, n + 1 if n < 99 else n - 1) if x != n and 0 < x < 100]
    return mcq("Come si scrive %d in lettere?" % n, lettere(n), [lettere(x) for x in alt], "%d si scrive <b>%s</b>." % (n, lettere(n)))


def s3_tabella():
    n = R.randint(12, 98)
    return mcq(C.tabella100(n) + "Quanti pallini sono colorati?", num(n), w(n), "Ogni riga ha 10 pallini: %s piene e %s. <b>%d</b>." % (pl(n // 10, "riga", "righe"), pl(n % 10, "pallino", "pallini"), n))


def s4_vicini():
    n = R.randint(11, 98)
    k = R.choice(["prec", "succ", "+10", "-10", "tra"])
    if k == "prec":
        if R.random() < 0.5:
            n = n // 10 * 10 or 20
        return mcq("Qual è il numero che viene prima di %d?" % n, num(n - 1), [num(n + 1), num(n - 10), num(n - 2)], "Il precedente è %d − 1 = <b>%d</b>." % (n, n - 1))
    if k == "succ":
        if R.random() < 0.5:
            n = n // 10 * 10 + 9
        if n >= 99:
            n = 89
        return mcq("Qual è il numero che viene dopo %d?" % n, num(n + 1), [num(n - 1), num(n + 10), num(n // 10 * 10 + 10 + 1) if n % 10 == 9 else num(n + 2)], "Il successivo è %d + 1 = <b>%d</b>." % (n, n + 1))
    if k == "+10":
        if n > 89:
            n -= 10
        return mcq("Quanto fa %d + 10?" % n, num(n + 10), [num(n + 1), num(n + 11), num(n - 10) if n > 10 else num(n + 20)], "Aumenta di 1 la cifra delle decine: <b>%d</b>." % (n + 10))
    if k == "-10":
        if n < 20:
            n += 20
        return mcq("Quanto fa %d − 10?" % n, num(n - 10), [num(n - 1), num(n + 10) if n < 90 else num(n - 11), num(n - 11)], "Diminuisci di 1 la cifra delle decine: <b>%d</b>." % (n - 10))
    a = R.randint(10, 90)
    return mcq("Quale numero sta tra %d e %d?" % (a, a + 2), num(a + 1), [num(a + 3), num(a - 1), num(a + 10)], "%d, <b>%d</b>, %d." % (a, a + 1, a + 2))


def s4_retta():
    lo = R.randint(0, 8) * 10
    v = lo + R.randint(1, 19)
    if v >= 100:
        return None
    return mcq(C.retta100(lo, lo + 20, [(v, "A")], 1, 5, 420) + "Quale numero indica la freccia A?", num(v), w(v), "Conta le tacche da %d: <b>%d</b>." % (lo, v))


def s5():
    k = R.choice(["scatole", "sacchetti", "conta2", "cento", "pagine"])
    if k == "scatole":
        d, u = R.randint(2, 9), R.randint(1, 9)
        return mcq("Ci sono %s da 10 pastelli e %s sciolti. Quanti pastelli in tutto?" % (pl(d, "scatola", "scatole"), pl(u, "pastello", "pastelli")), num(10 * d + u), w(10 * d + u),
                   "%d decine e %d unità: <b>%d</b>." % (d, u, 10 * d + u))
    if k == "sacchetti":
        n = R.randint(21, 99)
        return mcq("La maestra ha %d caramelle. Le mette in sacchetti da 10. Quanti sacchetti pieni fa?" % n, str(n // 10), [str(n % 10) if n % 10 != n // 10 else str(n // 10 + 1), str(n), str(n // 10 + 1)],
                   "%d = %d decine e %d unità: <b>%d</b> sacchetti pieni." % (n, n // 10, n % 10, n // 10))
    if k == "conta2":
        a = R.randint(10, 80)
        st = R.choice([2, 5, 10])
        seq = [a + st * i for i in range(4)]
        return mcq("Continua: %s, … Qual è il numero dopo?" % ", ".join(map(str, seq)), num(seq[-1] + st), [num(seq[-1] + 1), num(seq[-1] + st + 1), num(seq[-1] + st * 2)],
                   "Si va avanti di %d in %d: %d + %d = <b>%d</b>." % (st, st, seq[-1], st, seq[-1] + st))
    if k == "cento":
        n = R.randint(30, 95)
        return mcq("Luca ha %d figurine. Quante gliene mancano per arrivare a 100?" % n, num(100 - n), [num(n), num(100 - n + 10), num(100 - n - 1)], "%d + %d = 100: ne mancano <b>%d</b>." % (n, 100 - n, 100 - n))
    n = R.randint(20, 90)
    return mcq("Sofia legge un libro. È a pagina %d. Legge altre 10 pagine. A che pagina arriva?" % n, num(n + 10), [num(n + 1), num(n + 11), num(n + 20)],
               "%d + 10 = <b>%d</b>." % (n, n + 10))


def main():
    seen = set()
    sets = [
        ("Contare a decine", mix(R, seen, [(s1_riga, 10), (s1_blocchi, 10)])),
        ("Decine e unità", mix(R, seen, [(s2_dau, 20)])),
        ("Cifre, lettere e tabella del 100", mix(R, seen, [(s3_lettere, 12), (s3_tabella, 8)])),
        ("Prima, dopo e retta", mix(R, seen, [(s4_vicini, 12), (s4_retta, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["10 unità fanno <b>1 decina</b>. 10 decine fanno <b>1 centinaio</b> (100).",
         "Nei numeri di due cifre, a sinistra ci sono le <b>decine</b> (da), a destra le <b>unità</b> (u).",
         "37 = 3 decine e 7 unità = 30 + 7."],
        [("Scrivi il numero: 6 decine e 4 unità.", ["da = 6", "u = 4"], "64")],
        [["Scambiare decine e unità: 37 → 73", "Le decine vanno a sinistra."],
         ["Scrivere «trentasette» come 307", "Trenta = 3 decine: 37."],
         ["Saltare un numero contando", "Conta piano, uno alla volta."]],
        blocchi(0, 0, 3, 7))
    faq = [("Come aiuto un bambino a capire decine e unità?", "Con oggetti da raggruppare a 10 (cannucce, mattoncini): ogni gruppo da 10 è una decina."),
           ("Fino a quale numero si arriva in seconda?", "Di solito fino a 100, e a fine anno si comincia a contare oltre il 100.")]
    make_unit(R, "numeri-fino-a-100", "N",
              "Contare oggetti o eventi, a voce e mentalmente, in senso progressivo e regressivo e per salti; leggere e scrivere i numeri naturali in notazione decimale, con la consapevolezza del valore che le cifre hanno a seconda della loro posizione",
              "I numeri fino a 100: decine e unità", "Numeri fino a 100",
              "Schede di matematica per la classe seconda sui numeri fino a 100: contare a decine, decine e unità, cifre e lettere, tabella del 100, precedente e successivo, problemi. 100 esercizi con soluzioni.",
              "10 unità = 1 decina.", "A sinistra le decine, a destra le unità.",
              body, faq, sets, 1, grade=G)


if __name__ == "__main__":
    main()
