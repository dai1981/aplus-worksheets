# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Addizioni e sottrazioni con i grandi numeri (Numeri)
  python3 tools/gen_it_matematica_c4_addizioni_e_sottrazioni.py
Addizioni e sottrazioni in colonna con numeri fino a 999 999 (con riporti e cambi, anche con gli zeri),
proprietà commutativa, associativa e invariantiva, prova, stima, problemi.
Errori: non incolonnare, dimenticare il riporto, togliere la cifra più piccola dalla più grande (flip), cambi con gli zeri.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids, table

R = random.Random(70402)
G = "classe-quarta"
K = Kids(R)


def dg(n, k=7):
    return [int(d) for d in str(n).rjust(k, "0")][::-1]


def n_carries(nums):
    c, n = 0, 0
    for k in range(7):
        s = sum(dg(x)[k] for x in nums) + c
        c = s // 10
        n += c > 0
    return n


def no_carry(nums):
    k = len(str(max(nums)))
    return int("".join(str(sum(dg(x)[i] for x in nums) % 10) for i in range(k - 1, -1, -1)))


def flip(a, b):
    k = len(str(a))
    return int("".join(str(abs(dg(a)[i] - dg(b)[i])) for i in range(k - 1, -1, -1)))


def n_borrow(a, b):
    c, n = 0, 0
    for k in range(7):
        if dg(a)[k] - dg(b)[k] - c < 0:
            n, c = n + 1, 1
        else:
            c = 0
    return n


def add_task(nums, lo=1, hi=9):
    r = sum(nums)
    nc = n_carries(nums)
    if r >= 10 ** 6 or not lo <= nc <= hi:
        return None
    big = max(nums)
    w = [no_carry(nums), r + 1000, r - 10, r + 100, r - 1000]
    if len({len(str(x)) for x in nums}) > 1:
        w.insert(0, sum(x * 10 ** (len(str(big)) - len(str(x))) for x in nums))
    return mcq(colonna([str(x) for x in nums]) + "Esegui in colonna: %s" % " + ".join(num(x) for x in nums), num(r),
               [num(x) for x in w if 0 < x < 10 ** 6 and x != r],
               "Incolonna unità sotto unità e calcola da destra; ogni volta che superi 9 scrivi le unità e riporta 1 alla colonna dopo (%s). <b>%s</b>." % ("1 riporto" if nc == 1 else "%d riporti" % nc, num(r)))


def sub_task(a, b, lo=1, hi=9):
    if b >= a:
        return None
    nb = n_borrow(a, b)
    if not lo <= nb <= hi:
        return None
    r = a - b
    w = [flip(a, b), r + 1000, r - 10, r + 100, a - b // 10 if b >= 10 else None]
    return mcq(colonna([str(a), str(b)], op="−") + "Esegui in colonna: %s − %s" % (num(a), num(b)), num(r),
               [num(x) for x in w if x and 0 < x < 10 ** 6 and x != r],
               "Quando la cifra in alto è più piccola fai un cambio con la colonna a sinistra (se lì c’è 0, il cambio passa alla colonna ancora più a sinistra). %s − %s = <b>%s</b>. Prova: %s + %s = %s." % (num(a), num(b), num(r), num(r), num(b), num(a)))


def s1():
    return add_task([R.randint(1200, 68000), R.randint(1100, 29000)], 1, 2)


def s1b():
    return add_task([R.randint(10000, 480000), R.randint(10000, 390000), R.randint(100, 9999)] if R.random() < 0.4 else [R.randint(10000, 580000), R.randint(1000, 390000)], 2, 5)


def s2():
    return sub_task(R.randint(5000, 98000), R.randint(1000, 49000), 1, 2)


def s3():
    a = R.choice([R.randint(1, 9) * 10 ** R.randint(4, 5), R.randint(10, 90) * 1000 + R.choice([0, 5, 50, 500]), R.randint(1, 9) * 10 ** 5 + R.randint(1, 9) * 1000])
    b = R.randint(a // 20, a - 1)
    return sub_task(a, b, 2, 6)


def s3b():
    return sub_task(R.randint(100000, 999999), R.randint(10000, 600000), 2, 5)


def s4_proprieta():
    k = R.choice(["comm", "ass", "inv", "inv"])
    if k == "comm":
        a, b = R.randint(120, 9800), R.randint(120, 9800)
        return mcq("%s + %s = %s. Quanto fa %s + %s, senza calcolare?" % (num(a), num(b), num(a + b), num(b), num(a)), num(a + b),
                   [num(a + b + 1), num(abs(a - b)), "non si può sapere"], "Proprietà <b>commutativa</b>: cambiando l’ordine degli addendi la somma non cambia: <b>%s</b>." % num(a + b))
    if k == "ass":
        a, b = R.randint(12, 89), R.randint(1, 9)
        c = 10 * R.randint(1, 9) - b if b else 10
        return mcq("Per calcolare %d + %d + %d in fretta, quale coppia conviene sommare prima?" % (a, b, c), "%d + %d = %d" % (b, c, b + c),
                   ["%d + %d = %d" % (a, b, a + b), "%d + %d = %d" % (a, c, a + c), "nessuna: si somma sempre da sinistra"],
                   "Proprietà <b>associativa</b>: puoi sommare prima %d + %d = %d (un numero tondo), poi %d + %d = %d." % (b, c, b + c, a, b + c, a + b + c))
    a, b = R.randint(1, 9) * 1000 + R.randint(1, 9) * 100 + R.randint(10, 99), R.randint(1, 9) * 100 + R.randint(1, 9) * 10 + R.randint(1, 9)
    if b >= a:
        return None
    d = 10 - b % 10
    return mcq("Proprietà invariantiva: %s − %s è uguale a…" % (num(a), num(b)), "%s − %s" % (num(a + d), num(b + d)),
               ["%s − %s" % (num(a + d), num(b)), "%s − %s" % (num(a - d), num(b + d)), "%s − %s" % (num(a), num(b + d))],
               "Se aggiungi lo stesso numero (%d) a <b>tutti e due</b> i termini, la differenza non cambia: %s − %s = %s." % (d, num(a + d), num(b + d), num(a - b)))


def s4_prova():
    a, b = R.randint(5000, 90000), R.randint(1000, 4999)
    r = a - b
    if R.random() < 0.5:
        return mcq("Hai calcolato %s − %s = %s. Come fai la prova?" % (num(a), num(b), num(r)), "%s + %s = %s" % (num(r), num(b), num(a)),
                   ["%s − %s = %s" % (num(r), num(b), num(r - b)), "%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(a), num(r), num(b))],
                   "La prova della sottrazione è l’addizione: differenza + sottraendo = minuendo, <b>%s + %s = %s</b>." % (num(r), num(b), num(a)))
    return mcq("%s + ? = %s. Qual è il numero mancante?" % (num(b), num(a)), num(r), [num(a + b), num(r + 1000), num(r - 10)],
               "Il numero mancante si trova con la sottrazione: %s − %s = <b>%s</b>." % (num(a), num(b), num(r)))


def s4_stima():
    a, b = R.randint(11, 79) * 1000 + R.randint(101, 899), R.randint(11, 49) * 1000 + R.randint(101, 899)
    ra, rb = (a + 500) // 1000 * 1000, (b + 500) // 1000 * 1000
    if R.random() < 0.5:
        est = ra + rb
        return mcq("Stima arrotondando alle migliaia: %s + %s fa circa…" % (num(a), num(b)), num(est),
                   [num(est + 10000), num(est - 1000) if est - 1000 != a // 1000 * 1000 + b // 1000 * 1000 else num(est + 2000), num(a // 1000 * 1000 + b // 1000 * 1000) if a // 1000 * 1000 + b // 1000 * 1000 != est else num(est + 1000)],
                   "%s ≈ %s e %s ≈ %s: la somma è circa <b>%s</b> (esatta: %s)." % (num(a), num(ra), num(b), num(rb), num(est), num(a + b)))
    if a < b:
        a, b, ra, rb = b, a, rb, ra
    est = ra - rb
    if est <= 0:
        return None
    return mcq("Stima arrotondando alle migliaia: %s − %s fa circa…" % (num(a), num(b)), num(est),
               [num(est + 10000), num(ra + rb), num(est + 1000)],
               "%s ≈ %s e %s ≈ %s: la differenza è circa <b>%s</b> (esatta: %s)." % (num(a), num(ra), num(b), num(rb), num(est), num(a - b)))


def s5():
    p = K.next()
    k = R.choice(["auto", "risparmi", "montagna", "biglietti", "fabbrica", "anni", "spettatori", "km"])
    if k == "auto":
        a, b = R.randint(12000, 25000), R.randint(800, 4500)
        return mcq("Un’auto costa %s €. Lo sconto è di %s €. Quanto si paga?" % (num(a), num(b)), num(a - b) + " €", [num(a + b) + " €", num(flip(a, b)) + " €", num(a - b + 1000) + " €"],
                   "%s − %s = <b>%s €</b>." % (num(a), num(b), num(a - b)))
    if k == "risparmi":
        a, b, c = R.randint(1200, 4800), R.randint(900, 3900), R.randint(500, 2500)
        return mcq("Una famiglia mette da parte %s € a gennaio, %s € a febbraio e %s € a marzo. Quanto risparmia in tutto?" % (num(a), num(b), num(c)), num(a + b + c) + " €",
                   [num(a + b) + " €", num(a + b + c + 1000) + " €", num(no_carry([a, b, c])) + " €"], "%s + %s + %s = <b>%s €</b>." % (num(a), num(b), num(c), num(a + b + c)))
    if k == "montagna":
        a, b = R.choice([("il Monte Bianco", 4806), ("il Monte Rosa", 4634), ("il Cervino", 4478), ("il Gran Paradiso", 4061)]), R.choice([("l’Etna", 3357), ("il Vesuvio", 1281), ("il Monte Amiata", 1738), ("il Gran Sasso", 2912)])
        return mcq("%s è alto %s m, %s %s m. Quanti metri di differenza ci sono?" % (a[0][0].upper() + a[0][1:], num(a[1]), b[0], num(b[1])), num(a[1] - b[1]) + " m",
                   [num(a[1] + b[1]) + " m", num(flip(a[1], b[1])) + " m", num(a[1] - b[1] + 100) + " m"], "%s − %s = <b>%s m</b>." % (num(a[1]), num(b[1]), num(a[1] - b[1])))
    if k == "biglietti":
        a, b = R.randint(30000, 80000), R.randint(10000, 29999)
        c = a - b
        return mcq("Per un concerto sono stati messi in vendita %s biglietti. Ne sono stati venduti %s. Quanti biglietti restano?" % (num(a), num(c)), num(b),
                   [num(a + c), num(flip(a, c)) if flip(a, c) != b else num(b + 100), num(b + 1000)], "%s − %s = <b>%s</b>." % (num(a), num(c), num(b)))
    if k == "fabbrica":
        a, b = R.randint(120000, 450000), R.randint(80000, 350000)
        return mcq("Una fabbrica produce %s bottiglie a maggio e %s a giugno. Quante bottiglie in tutto?" % (num(a), num(b)), num(a + b),
                   [num(a + b + 100000), num(abs(a - b)), num(no_carry([a, b]))], "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
    if k == "anni":
        a = R.choice([("la scoperta dell’America", 1492), ("l’Unità d’Italia", 1861), ("la nascita di Leonardo da Vinci", 1452), ("la nascita di Dante", 1265), ("il primo viaggio sulla Luna", 1969)])
        y = 2026
        return mcq("Quanti anni sono passati dal %d (%s) al %d?" % (a[1], a[0], y), str(y - a[1]), [str(y - a[1] + 10), str(flip(y, a[1])), str(y - a[1] - 100)],
                   "%d − %d = <b>%d</b> anni." % (y, a[1], y - a[1]))
    if k == "spettatori":
        a, b = R.randint(41000, 69000), R.randint(1000, 9000)
        return mcq("Domenica allo stadio c’erano %s spettatori, %s in più della partita prima. Quanti erano alla partita prima?" % (num(a), num(b)), num(a - b),
                   [num(a + b), num(a - b + 1000), num(flip(a, b)) if flip(a, b) != a - b else num(a - b - 10)], "«In più» oggi: alla partita prima erano di meno, %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))
    a, b = R.randint(1200, 3800), R.randint(900, 2900)
    return mcq("%s parte con l’auto: il contachilometri segna %s km. All’arrivo segna %s km. Quanti chilometri ha percorso?" % (p[0], num(a * 10), num(a * 10 + b)), num(b) + " km",
               [num(a * 20 + b) + " km", num(b + 1000) + " km", num(a * 10) + " km"], "%s − %s = <b>%s km</b>." % (num(a * 10 + b), num(a * 10), num(b)))


def main():
    seen = set()
    sets = [
        ("Addizioni in colonna", mix(R, seen, [(s1, 10), (s1b, 10)])),
        ("Sottrazioni in colonna", mix(R, seen, [(s2, 12), (s3b, 8)])),
        ("Sottrazioni con gli zeri", mix(R, seen, [(s3, 20)])),
        ("Proprietà, prova e stima", mix(R, seen, [(s4_proprieta, 8), (s4_prova, 6), (s4_stima, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Incolonna i numeri partendo da destra: <b>unità sotto unità</b>, decine sotto decine, e così via fino alle centinaia di migliaia.",
         "Nell’addizione, se una colonna supera 9, scrivi le unità e <b>riporta</b> 1 nella colonna a sinistra.",
         "Nella sottrazione, se la cifra in alto è più piccola, fai un <b>cambio</b>: 1 della colonna a sinistra vale 10. Se lì c’è 0, il cambio passa ancora più a sinistra.",
         "Proprietà: <b>commutativa</b> e <b>associativa</b> per l’addizione; <b>invariantiva</b> per la sottrazione (aggiungi o togli lo stesso numero a tutti e due i termini).",
         "Prova della sottrazione: differenza + sottraendo = minuendo."],
        [("40 000 − 12 345", ["0 − 5: cambio da 4 decine di migliaia, le colonne con 0 diventano 9", "40 000 − 12 345 = 27 655", "prova: 27 655 + 12 345 = 40 000"], "27 655")],
        [["Non incolonnare da destra", "Le unità vanno sempre sotto le unità."],
         ["Fare 2 − 5 = 3", "Non si scambiano le cifre: fai un cambio."],
         ["Dimenticare che dopo il cambio lo 0 diventa 9", "Segna sopra ogni colonna la nuova cifra."]],
        table(["Proprietà", "Esempio"], [["commutativa", "245 + 37 = 37 + 245"], ["associativa", "38 + 7 + 3 = 38 + 10"], ["invariantiva", "502 − 98 = 504 − 100"]]))
    faq = [("A che cosa serve la proprietà invariantiva?", "A rendere più facile una sottrazione: 502 − 98 diventa 504 − 100 = 404."),
           ("Perché si fa la stima?", "Per controllare se il risultato è ragionevole: se 48 900 + 21 300 fa circa 70 000, un risultato di 7020 è sbagliato.")]
    make_unit(R, "addizioni-e-sottrazioni", "N",
              "Eseguire addizioni e sottrazioni con i numeri naturali, in colonna e a mente, conoscendo le proprietà delle operazioni; stimare il risultato di un’operazione",
              "Addizioni e sottrazioni con i grandi numeri", "Addizioni e sottrazioni",
              "Schede di matematica per la classe quarta su addizioni e sottrazioni in colonna con i grandi numeri: riporti, cambi con gli zeri, proprietà commutativa, associativa e invariantiva, prova, stima e problemi. 100 esercizi con soluzioni.",
              "Incolonna da destra: unità sotto unità.", "Prova della sottrazione: differenza + sottraendo = minuendo.",
              body, faq, sets, 2, grade=G)


if __name__ == "__main__":
    main()
