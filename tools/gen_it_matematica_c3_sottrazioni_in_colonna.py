# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le sottrazioni in colonna (Numeri)
  python3 tools/gen_it_matematica_c3_sottrazioni_in_colonna.py
Sottrazioni in colonna con numeri fino a 999, senza e con il cambio (prestito), con gli zeri, prova con l’addizione,
problemi (resto, differenza, quanti di più).
Errori: togliere la cifra più piccola dalla più grande in ogni colonna (523 − 278 → 355), dimenticare il cambio,
usare l’addizione per trovare una differenza.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids

R = random.Random(70305)
K = Kids(R)


def digits(n, k=3):
    return [int(d) for d in str(n).rjust(k, "0")][::-1]


def borrows(a, b):
    da, db = digits(a), digits(b)
    c, n = 0, 0
    for k in range(3):
        if da[k] - db[k] - c < 0:
            n += 1
            c = 1
        else:
            c = 0
    return n


def flip(a, b):
    da, db = digits(a), digits(b)
    return int("".join(str(abs(da[k] - db[k])) for k in (2, 1, 0)))


def no_borrow(a, b):
    da, db = digits(a), digits(b)
    return int("".join(str((da[k] - db[k]) % 10) for k in (2, 1, 0)))


def task(a, b, need=None):
    if b >= a:
        return None
    n = borrows(a, b)
    if need is not None and n != need:
        return None
    r = a - b
    w = [flip(a, b) if n else None, no_borrow(a, b) if n else None, r + 10, r - 10, r + 100, a + b if a + b < 1000 else None]
    e = "Incolonna i numeri e calcola da destra a sinistra."
    if n:
        e += " Quando la cifra in alto è più piccola, fai un cambio: prendi 1 dalla colonna a sinistra, che vale 10 nella colonna dove sei."
    e += " %s − %s = <b>%s</b>. Prova: %s + %s = %s." % (num(a), num(b), num(r), num(r), num(b), num(a))
    return mcq(colonna([str(a), str(b)], op="−") + "Esegui in colonna: %s − %s" % (num(a), num(b)), num(r),
               [num(x) for x in w if x and 0 < x < 1000 and x != r], e)


def s1():
    return task(R.randint(250, 999), R.randint(11, 249), 0)


def s2():
    return task(R.randint(250, 999), R.randint(15, 499), 1)


def s3():
    return task(R.randint(300, 999), R.randint(105, 599), 2)


def s4_zero():
    a = R.choice([R.randint(2, 9) * 100, R.randint(2, 9) * 100 + R.randint(1, 9), R.randint(2, 9) * 100 + R.randint(1, 9) * 10])
    return task(a, R.randint(11, a - 20))


def s4_prova():
    a, b = R.randint(300, 990), R.randint(110, 290)
    r = a - b
    return mcq("%s − %s = %s. Quale addizione serve per fare la prova?" % (num(a), num(b), num(r)), "%s + %s = %s" % (num(r), num(b), num(a)),
               ["%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(a), num(r), num(b)), "%s + %s = %s" % (num(r), num(a), num(r + a))],
               "Resto più sottraendo dà il minuendo: <b>%s + %s = %s</b>." % (num(r), num(b), num(a)))


def s5_problema():
    p = K.next()
    a, b = R.randint(250, 980), R.randint(95, 240)
    r = a - b
    k = R.choice(["resto", "differenza", "piu", "manca", "anni"])
    wr = [num(a + b) if a + b < 1000 else num(r + 100), num(flip(a, b)) if borrows(a, b) else num(r + 10), num(r - 10)]
    if k == "resto":
        return mcq("Un negozio ha %s quaderni. Ne vende %s. Quanti quaderni restano?" % (num(a), num(b)), num(r), wr,
                   "%s − %s = <b>%s</b> quaderni." % (num(a), num(b), num(r)))
    if k == "differenza":
        return mcq("Il monte A è alto %s m e la collina B è alta %s m. Quanti metri di differenza ci sono?" % (num(a), num(b)), num(r) + " m", [x + " m" for x in wr],
                   "Per la differenza fai una sottrazione: %s − %s = <b>%s m</b>." % (num(a), num(b), num(r)))
    if k == "piu":
        return mcq("Nella scuola A ci sono %s alunni, nella scuola B %s. Quanti alunni ha in più la scuola A?" % (num(a), num(b)), num(r), wr,
                   "«In più» vuol dire differenza: %s − %s = <b>%s</b>." % (num(a), num(b), num(r)))
    if k == "manca":
        return mcq("%s vuole comprare una bicicletta che costa %s €. Ha già %s €. Quanti euro gli mancano?" % (p[0], num(a), num(b)) if p[1] == "lui" else
                   "%s vuole comprare una bicicletta che costa %s €. Ha già %s €. Quanti euro le mancano?" % (p[0], num(a), num(b)), num(r) + " €", [x + " €" for x in wr],
                   "%s − %s = <b>%s €</b>." % (num(a), num(b), num(r)))
    a, b = R.randint(70, 95), R.randint(8, 40)
    return mcq("Il nonno di %s ha %d anni. %s ha %d anni. Quanti anni di differenza ci sono tra loro?" % (p[0], a, p[0], b), str(a - b),
               [str(a + b), str(a - b + 10), str(a - b - 1)],
               "%d − %d = <b>%d</b> anni." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Senza cambio", mix(R, seen, [(s1, 20)])),
        ("Con un cambio", mix(R, seen, [(s2, 20)])),
        ("Con due cambi", mix(R, seen, [(s3, 20)])),
        ("Con gli zeri e la prova", mix(R, seen, [(s4_zero, 12), (s4_prova, 8)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Scrivi in alto il numero più grande (il minuendo) e <b>incolonna</b> le unità.",
         "Calcola da destra a sinistra. Se la cifra in alto è più piccola di quella in basso, fai un <b>cambio</b>: prendi 1 decina (o 1 centinaio) dalla colonna a sinistra e la trasformi in 10 unità (o 10 decine).",
         "Fai la <b>prova</b> con l’addizione: resto + sottraendo = minuendo."],
        [("524 − 168", ["u: 4 − 8 non si può, cambio 1 decina: 14 − 8 = 6", "da: restano 1 decina, 1 − 6 non si può, cambio 1 centinaio: 11 − 6 = 5", "h: restano 4 centinaia, 4 − 1 = 3"], "356")],
        [["Togliere la cifra piccola dalla grande: 523 − 278 = 355", "Togli sempre la cifra in basso da quella in alto: 523 − 278 = 245."],
         ["Dimenticare il cambio", "Quando prendi 1 dalla colonna a sinistra, quella cifra diminuisce di 1."],
         ["Addizionare per trovare la differenza", "«Quanto di più?» e «quanto manca?» si risolvono con una sottrazione."]])
    faq = [("Che cos’è il cambio nella sottrazione?", "Quando la cifra in alto è troppo piccola, si prende 1 dalla colonna a sinistra: 1 decina diventa 10 unità, 1 centinaio diventa 10 decine. Qualcuno lo chiama prestito."),
           ("Come faccio la prova?", "Sommo il resto e il sottraendo: devo ottenere il minuendo.")]
    make_unit(R, "sottrazioni-in-colonna", "N",
              "Eseguire sottrazioni con i numeri naturali con gli algoritmi scritti usuali; controllare il risultato con l’operazione inversa; risolvere problemi di resto, differenza e completamento",
              "Le sottrazioni in colonna con il cambio", "Sottrazioni in colonna",
              "Schede di matematica per la classe terza sulle sottrazioni in colonna: senza cambio, con uno e due cambi, con gli zeri, prova con l’addizione e problemi. 100 esercizi con soluzioni.",
              "Incolonna e calcola da destra a sinistra.", "Se la cifra in alto è più piccola, fai un cambio.",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
