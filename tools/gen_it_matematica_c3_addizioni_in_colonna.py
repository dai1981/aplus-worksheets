# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le addizioni in colonna (Numeri)
  python3 tools/gen_it_matematica_c3_addizioni_in_colonna.py
Addizioni in colonna con numeri fino a 999, senza e con riporto, con tre addendi, cifre mancanti, stima, problemi.
Errori: dimenticare il riporto (345 + 238 → 573), incolonnare male (345 + 42 → 765), scrivere 13 in una colonna.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids

R = random.Random(70304)
K = Kids(R)
NAME = {1: "decina", 2: "centinaio"}


def digits(n, k=3):
    return [int(d) for d in str(n).rjust(k, "0")][::-1]


def carries(nums):
    out, c = {}, 0
    for k in range(3):
        s = sum(digits(x)[k] for x in nums) + c
        c = s // 10
        if c and k < 2:
            out[k + 1] = c
    return out


def no_carry(nums):
    return int("".join(str(sum(digits(x)[k] for x in nums) % 10) for k in (2, 1, 0)))


def misaligned(nums):
    big = max(nums)
    return sum(x * (10 ** (len(str(big)) - len(str(x)))) for x in nums)


def task(nums, need=None):
    r = sum(nums)
    if r > 999 or (need is not None and len(carries(nums)) != need):
        return None
    cs = carries(nums)
    w = [no_carry(nums) if cs else None, r + 10, r - 10, r + 100, r + 1]
    if len({len(str(x)) for x in nums}) > 1:
        w.insert(0, misaligned(nums))
    e = "Incolonna i numeri: unità sotto unità, decine sotto decine. Poi calcola da destra a sinistra."
    if cs:
        e += " Riporti: %s." % ", ".join("%d %s" % (v, NAME[k] if v == 1 else {1: "decine", 2: "centinaia"}[k]) for k, v in sorted(cs.items()))
    e += " Risultato: <b>%s</b>." % num(r)
    return mcq(colonna([str(x) for x in nums]) + "Esegui in colonna: %s" % " + ".join(num(x) for x in nums), num(r),
               [num(x) for x in w if x and 0 < x < 1000 and x != r], e)


def s1():
    return task([R.randint(101, 687), R.randint(11, 311)], 0)


def s2():
    return task([R.randint(105, 689), R.randint(15, 289)], 1)


def s3():
    return task([R.randint(156, 689), R.randint(56, 289)], 2)


def s3b():
    return task([R.randint(205, 889), R.randint(12, 98)])


def s4_tre():
    nums = [R.randint(101, 499), R.randint(101, 299), R.randint(12, 99)]
    if not carries(nums):
        return None
    return task(nums)


def s4_mancante():
    a, b = R.randint(105, 689), R.randint(105, 289)
    r = a + b
    if r > 999:
        return None
    pos = R.randint(0, 2)
    sa = str(a)
    i = 2 - pos
    d = sa[i]
    shown = sa[:i] + "?" + sa[i + 1:]
    return mcq("Quale cifra va al posto del «?»: %s + %s = %s" % (shown, num(b), num(r)), d,
               [str((int(d) + 1) % 10), str((int(d) + 9) % 10), str((int(d) + 2) % 10)],
               "%s + %s = %s, quindi la cifra nascosta è <b>%s</b>." % (num(a), num(b), num(r), d))


def s4_stima():
    a, b = R.randint(1, 6) * 100 + R.randint(11, 89), R.randint(1, 3) * 100 + R.randint(11, 89)
    if a + b > 999:
        return None
    ra, rb = (a + 50) // 100 * 100, (b + 50) // 100 * 100
    est = ra + rb
    return mcq("Stima arrotondando al centinaio: %s + %s fa circa…" % (num(a), num(b)), num(est),
               [num(est + 100), num(est - 100), num(a // 100 * 100 + b // 100 * 100) if a // 100 * 100 + b // 100 * 100 != est else num(est + 200)],
               "%s fa circa %s e %s fa circa %s: %s + %s = <b>%s</b> (il risultato esatto è %s)." % (num(a), num(ra), num(b), num(rb), num(ra), num(rb), num(est), num(a + b)))


def s5_problema():
    p = K.next()
    k = R.choice(["km", "libri", "euro", "visitatori", "punti", "mele"])
    a, b = R.randint(120, 580), R.randint(85, 390)
    if a + b > 999:
        return None
    r = a + b
    wr = [num(no_carry([a, b])) if carries([a, b]) else num(r + 100), num(r + 10), num(a - b) if a > b else num(r - 10)]
    if k == "km":
        return mcq("Una famiglia percorre %s km all’andata e %s km al ritorno. Quanti chilometri percorre in tutto?" % (num(a), num(b)), num(r) + " km", [x + " km" for x in wr],
                   "%s + %s = <b>%s km</b>." % (num(a), num(b), num(r)))
    if k == "libri":
        return mcq("La biblioteca della scuola ha %s libri. Ne compra altri %s. Quanti libri ha adesso?" % (num(a), num(b)), num(r), wr,
                   "%s + %s = <b>%s</b> libri." % (num(a), num(b), num(r)))
    if k == "euro":
        return mcq("Il papà di %s spende %s € per una bicicletta e %s € per un monopattino. Quanto spende in tutto?" % (p[0], num(a), num(b)), num(r) + " €", [x + " €" for x in wr],
                   "%s + %s = <b>%s €</b>." % (num(a), num(b), num(r)))
    if k == "visitatori":
        return mcq("Sabato %s persone visitano il museo; domenica %s persone. Quanti visitatori ci sono in tutto?" % (num(a), num(b)), num(r), wr,
                   "%s + %s = <b>%s</b> visitatori." % (num(a), num(b), num(r)))
    if k == "punti":
        return mcq("Nel primo gioco %s fa %s punti, nel secondo %s punti. Quanti punti fa in tutto?" % (p[0], num(a), num(b)), num(r), wr,
                   "%s + %s = <b>%s</b> punti." % (num(a), num(b), num(r)))
    return mcq("Un contadino raccoglie %s mele il lunedì e %s mele il martedì. Quante mele raccoglie in tutto?" % (num(a), num(b)), num(r), wr,
               "%s + %s = <b>%s</b> mele." % (num(a), num(b), num(r)))


def main():
    seen = set()
    sets = [
        ("Senza riporto", mix(R, seen, [(s1, 20)])),
        ("Con un riporto", mix(R, seen, [(s2, 20)])),
        ("Con due riporti", mix(R, seen, [(s3, 14), (s3b, 6)])),
        ("Tre addendi, cifre mancanti e stima", mix(R, seen, [(s4_tre, 8), (s4_mancante, 6), (s4_stima, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["<b>Incolonna</b> i numeri: unità sotto unità, decine sotto decine, centinaia sotto centinaia.",
         "Calcola colonna per colonna, <b>da destra a sinistra</b>: prima le unità.",
         "Se in una colonna ottieni 10 o più, scrivi le unità e porta 1 nella colonna successiva: è il <b>riporto</b>.",
         "Prima di calcolare fai una <b>stima</b>: ti aiuta a controllare il risultato."],
        [("457 + 386", ["u: 7 + 6 = 13, scrivo 3 e riporto 1", "da: 1 + 5 + 8 = 14, scrivo 4 e riporto 1", "h: 1 + 4 + 3 = 8"], "843")],
        [["Dimenticare il riporto: 345 + 238 = 573", "Scrivi il riporto in alto sulla colonna successiva: 583."],
         ["Incolonnare a sinistra: 345 + 42 = 765", "Allinea le unità a destra: 387."],
         ["Scrivere 13 in una colonna", "In ogni colonna va una sola cifra; la decina diventa riporto."]])
    faq = [("Perché bisogna incolonnare bene?", "Per sommare cifre che hanno lo stesso valore: unità con unità, decine con decine, centinaia con centinaia."),
           ("Come controllo un’addizione?", "Con una stima arrotondando i numeri, oppure rifacendo il calcolo cambiando l’ordine degli addendi.")]
    make_unit(R, "addizioni-in-colonna", "N",
              "Eseguire addizioni con i numeri naturali con gli algoritmi scritti usuali; stimare il risultato di un’operazione; risolvere problemi di addizione",
              "Le addizioni in colonna con il riporto", "Addizioni in colonna",
              "Schede di matematica per la classe terza sulle addizioni in colonna: senza riporto, con uno e due riporti, tre addendi, cifre mancanti, stima e problemi. 100 esercizi con soluzioni.",
              "Incolonna e calcola da destra a sinistra.", "Se una colonna fa 10 o più, riporti 1.",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
