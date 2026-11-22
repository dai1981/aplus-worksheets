# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: I numeri fino a 1000 (Numeri)
  python3 tools/gen_it_matematica_c3_numeri_fino_a_1000.py
Centinaia, decine, unità; tabella h da u; leggere e scrivere i numeri in cifre e in lettere; scomporre;
cifra delle decine e numero di decine; precedente e successivo.
Errori: dimenticare lo zero (3 h e 5 u → 35), confondere cifra e numero di decine, invertire due cifre.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, blocchi, tabella_valore, lettere, pl, retta

R = random.Random(70301)


def three():
    return R.randint(101, 999)


def parts(n):
    return n // 100, n // 10 % 10, n % 10


def wrong(n):
    h, d, u = parts(n)
    out = []
    if d == 0 or u == 0:
        z = int("".join(str(x) for x in (h, d, u) if x))
        out.append(z)
    out += [h * 100 + u * 10 + d if d != u else None, n + 100 if n < 900 else n - 100, n + 10 if n < 990 else n - 10, n - 1, u * 100 + d * 10 + h if u else None]
    return [num(x) for x in out if x and 0 < x < 1000 and x != n]


def s1_blocchi():
    h, d, u = R.randint(1, 4), R.randint(0, 6), R.randint(0, 9)
    n = 100 * h + 10 * d + u
    return mcq(blocchi(0, h, d, u) + "Quale numero è rappresentato?", num(n), wrong(n),
               "%s, %s e %s: <b>%s</b>." % (pl(h, "centinaio", "centinaia"), pl(d, "decina", "decine"), pl(u, "unità", "unità"), num(n)))


def s1_tabella():
    n = three()
    if R.random() < 0.4:
        n = n // 10 * 10 if R.random() < 0.5 else (n // 100) * 100 + n % 10
    return mcq(tabella_valore(n) + "Quale numero è scritto nella tabella?", num(n), wrong(n),
               "Leggi le cifre da sinistra a destra: h, da, u. Il numero è <b>%s</b>." % num(n))


def s1_unita():
    h, d, u = R.randint(1, 9), R.choice([0, R.randint(1, 9)]), R.choice([0, R.randint(1, 9)])
    n = 100 * h + 10 * d + u
    words = [pl(v, a, b) for v, a, b in ((h, "centinaio", "centinaia"), (d, "decina", "decine"), (u, "unità", "unità")) if v]
    if len(words) < 2:
        return None
    R.shuffle(words)
    return mcq("Quale numero ha " + ", ".join(words[:-1]) + " e " + words[-1] + "?", num(n), wrong(n),
               "Metti ogni quantità al suo posto (h, da, u) e scrivi 0 nelle colonne vuote: <b>%s</b>." % num(n))


def s2_da_lettere():
    n = three()
    if R.random() < 0.4:
        n = n // 10 * 10
    return mcq("Scrivi in cifre: <b>%s</b>." % lettere(n), num(n), wrong(n),
               "«%s» si scrive <b>%s</b>." % (lettere(n), num(n)))


def s2_in_lettere():
    n = three()
    w = [n + 10 if (n // 10) % 10 != 9 else n - 10, n + 100 if n < 900 else n - 100, n + 1 if n % 10 != 9 else n - 1,
         parts(n)[0] * 100 + parts(n)[2] * 10 + parts(n)[1]]
    return mcq("Come si scrive %s in lettere?" % num(n), lettere(n), [lettere(x) for x in w if 0 < x < 1000 and x != n],
               "%s si scrive <b>%s</b>." % (num(n), lettere(n)))


def s3_scomponi():
    n = three()
    h, d, u = parts(n)
    if d == 0 and u == 0:
        return None
    terms = [v for v in (100 * h, 10 * d, u) if v]
    sh = " + ".join(num(t) for t in terms)
    if R.random() < 0.5:
        return mcq("Quale numero è uguale a %s?" % sh, num(n), wrong(n), "%s = <b>%s</b>." % (sh, num(n)))
    w1 = " + ".join(num(t) for t in (100 * h, d, u) if t)
    w2 = " + ".join(num(t) for t in (10 * h, 10 * d, u) if t)
    w3 = " + ".join(num(t) for t in (100 * h, 10 * u, d) if t)
    return mcq("Qual è la scomposizione di %s?" % num(n), sh, [w1, w2, w3],
               "%s = %s, %s e %s = <b>%s</b>." % (num(n), pl(h, "centinaio", "centinaia"), pl(d, "decina", "decine"), pl(u, "unità", "unità"), sh))


def s3_cifra():
    n = three()
    h, d, u = parts(n)
    k = R.choice(["hc", "dc", "uc", "dn", "dn"])
    if k == "hc":
        return mcq("Qual è la cifra delle centinaia di %s?" % num(n), str(h), [str(d), str(u), str(h + 1), str(n // 10)],
                   "La cifra delle centinaia è la prima a sinistra: <b>%d</b>." % h)
    if k == "dc":
        return mcq("Qual è la cifra delle decine di %s?" % num(n), str(d), [str(h), str(u), str(n // 10), str(d + 1)],
                   "La cifra delle decine è quella al centro: <b>%d</b>." % d)
    if k == "uc":
        return mcq("Qual è la cifra delle unità di %s?" % num(n), str(u), [str(h), str(d), str(u + 1)],
                   "La cifra delle unità è l’ultima a destra: <b>%d</b>." % u)
    if d == 0 or h == 0:
        return None
    return mcq("Quante decine ci sono in tutto in %s?" % num(n), str(n // 10), [str(d), str(h), str(n // 10 + 1), str(n)],
               "%s = %d decine e %d unità, quindi ci sono <b>%d</b> decine in tutto (la cifra delle decine è solo %d)." % (num(n), n // 10, u, n // 10, d))


def s4_vicini():
    n = R.randint(101, 989)
    k = R.choice(["succ", "prec", "piu10", "piu100", "meno10", "meno100", "retta"])
    if k == "succ":
        if R.random() < 0.6:
            n = n // 10 * 10 + 9
        if n >= 999:
            return None
        return mcq("Qual è il successivo di %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 11)],
                   "Il successivo è %s + 1 = <b>%s</b>." % (num(n), num(n + 1)))
    if k == "prec":
        if R.random() < 0.6:
            n = n // 10 * 10
        if n < 110:
            return None
        return mcq("Qual è il precedente di %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 11)],
                   "Il precedente è %s − 1 = <b>%s</b>." % (num(n), num(n - 1)))
    if k == "piu10":
        n = n // 100 * 100 + 90 + R.randint(0, 9)
        if n + 10 > 999:
            return None
        return mcq("Aggiungi 1 decina a %s." % num(n), num(n + 10), [num(n + 1), num(n + 100) if n + 100 < 1000 else num(n - 90), num(n - 90)],
                   "%s + 10 = <b>%s</b>: cambia anche la cifra delle centinaia." % (num(n), num(n + 10)))
    if k == "piu100":
        if n > 899:
            return None
        return mcq("Aggiungi 1 centinaio a %s." % num(n), num(n + 100), [num(n + 10), num(n + 1), num(n - 100) if n > 199 else num(n + 110)],
                   "%s + 100 = <b>%s</b>: cambia solo la cifra delle centinaia." % (num(n), num(n + 100)))
    if k == "meno10":
        n = n // 100 * 100 + R.randint(0, 9)
        if n < 110:
            return None
        return mcq("Togli 10 a %s." % num(n), num(n - 10), [num(n - 1), num(n - 100), num(n + 90)],
                   "%s − 10 = <b>%s</b>." % (num(n), num(n - 10)))
    if k == "meno100":
        if n < 200:
            return None
        return mcq("Togli 100 a %s." % num(n), num(n - 100), [num(n - 10), num(n + 100), num(n - 1)],
                   "%s − 100 = <b>%s</b>: cambia solo la cifra delle centinaia." % (num(n), num(n - 100)))
    lo = R.randint(1, 8) * 100
    v = lo + R.randint(1, 9) * 10
    return mcq(retta(lo, lo + 100, 10, [(v, "A")], [lo, lo + 100]) + "Quale numero indica la freccia A?", num(v),
               [num(lo + (v - lo) // 10), num(v + 10), num(v - 10), num(lo + 100 - (v - lo))],
               "Ogni tacca vale 10. Da %s conti %s: <b>%s</b>." % (num(lo), pl((v - lo) // 10, "tacca", "tacche"), num(v)))


def s5_indovinello():
    h, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
    if len({h, d, u}) < 3:
        return None
    n = 100 * h + 10 * d + u
    clues = ["la mia cifra delle centinaia è %d" % h, "la mia cifra delle decine è %d" % d, "la mia cifra delle unità è %d" % u]
    R.shuffle(clues)
    cand = [num(100 * h + 10 * u + d), num(100 * d + 10 * h + u) if d else None, num(100 * u + 10 * d + h) if u else None, num(100 * h + d + 10 * u)]
    return mcq("Indovinello: %s. Chi sono?" % "; ".join(clues), num(n), cand,
               "Metti ogni cifra nella sua colonna: h = %d, da = %d, u = %d. Il numero è <b>%s</b>." % (h, d, u, num(n)))


def s5_problema():
    k = R.choice(["banconote", "scatole", "pacchi", "sacchetti"])
    h, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
    if k == "banconote":
        if not d:
            return None
        tot = 100 * h + 10 * d + u
        return mcq("Nel salvadanaio ci sono %s da 100 €, %s da 10 € e %s da 1 €. Quanti euro ci sono in tutto?" % (
                       pl(h, "banconota", "banconote"), pl(d, "banconota", "banconote"), pl(u, "moneta", "monete")),
                   num(tot) + " €", [num(h + d + u) + " €", num(100 * h + d + 10 * u) + " €", num(10 * h + 10 * d + u) + " €"],
                   "%s + %s + %s = <b>%s €</b>." % (num(100 * h), num(10 * d), num(u), num(tot)))
    n = R.randint(120, 990)
    if k == "scatole":
        return mcq("In una fabbrica ci sono %s biscotti. Si mettono in scatole da 10. Quante scatole piene si riempiono?" % num(n), str(n // 10),
                   [str(n // 10 % 10), str(n // 100), str(n // 10 + 1)],
                   "In %s ci sono %d decine: <b>%d</b> scatole piene." % (num(n), n // 10, n // 10))
    if k == "pacchi":
        return mcq("Un negozio ha %s fogli. Li mette in pacchi da 100. Quanti pacchi completi ottiene?" % num(n), str(n // 100),
                   [str(n // 10), str(n % 100), str(n // 100 + 1)],
                   "In %s ci sono %d centinaia: <b>%d</b> pacchi completi." % (num(n), n // 100, n // 100))
    return mcq("Una maestra ha %s perline. Le divide in sacchetti da 10. Quante perline restano fuori?" % num(n), str(n % 10),
               [str(n // 10), str(n % 100), str(10 - n % 10)],
               "%s = %d decine e %d unità: restano fuori <b>%d</b> perline." % (num(n), n // 10, n % 10, n % 10)) if n % 10 else None


def main():
    seen = set()
    sets = [
        ("Centinaia, decine e unità", mix(R, seen, [(s1_blocchi, 8), (s1_tabella, 6), (s1_unita, 6)])),
        ("Leggere e scrivere i numeri", mix(R, seen, [(s2_da_lettere, 10), (s2_in_lettere, 10)])),
        ("Scomporre un numero", mix(R, seen, [(s3_scomponi, 10), (s3_cifra, 10)])),
        ("Precedente, successivo, + 10 e + 100", mix(R, seen, [(s4_vicini, 20)])),
        ("Indovinelli e problemi", mix(R, seen, [(s5_indovinello, 8), (s5_problema, 12)])),
    ]
    body = lesson(
        ["Un numero fino a 999 ha al massimo <b>3 cifre</b>: centinaia (h), decine (da) e unità (u).",
         "1 centinaio = 10 decine = 100 unità. 10 centinaia = 1000 (mille).",
         "Se una colonna è vuota, scrivi <b>0</b>: 3 centinaia e 5 unità fanno 305.",
         "La <b>cifra</b> delle decine di 472 è 7, ma il <b>numero</b> di decine è 47."],
        [("Scrivi il numero: 6 centinaia e 9 unità.", ["h = 6, da = 0, u = 9"], "609"),
         ("Quante decine in tutto ci sono in 480?", ["480 = 48 decine"], "48 decine")],
        [["Dimenticare lo zero: 3 h e 5 u → 35", "Scrivi 0 in ogni colonna vuota: 305."],
         ["Confondere cifra e numero di decine", "La cifra è una sola; il numero conta anche le decine dentro le centinaia."],
         ["Invertire due cifre: 472 → 427", "Leggi le colonne in ordine: h, da, u."]],
        tabella_valore(472))
    faq = [("Fino a quale numero si arriva in classe terza?", "Di solito fino a 1000: si leggono, si scrivono e si scompongono i numeri di tre cifre."),
           ("Che cosa vogliono dire h, da e u?", "h sono le centinaia, da le decine e u le unità. Ogni posto vale 10 volte quello alla sua destra.")]
    make_unit(R, "numeri-fino-a-1000", "N",
              "Leggere e scrivere i numeri naturali in notazione decimale, avendo consapevolezza della notazione posizionale; contare in senso progressivo e regressivo; confrontarli e ordinarli, anche rappresentandoli sulla retta",
              "I numeri fino a 1000: centinaia, decine e unità", "Numeri fino a 1000",
              "Schede di matematica per la classe terza sui numeri fino a 1000: tabella h da u, numeri in cifre e in lettere, scomposizione, precedente e successivo. 100 esercizi con soluzioni.",
              "Ogni cifra vale secondo il suo posto: h, da, u.", "Nelle colonne vuote si scrive 0.",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
