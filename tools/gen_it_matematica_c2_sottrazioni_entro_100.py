# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Le sottrazioni entro il 100 (Numeri)
  python3 tools/gen_it_matematica_c2_sottrazioni_entro_100.py
Togliere (oggetti barrati), sottrazioni entro il 20 con il passaggio della decina, togliere le decine, numeri di due
cifre, la sottrazione come differenza (quanti di più/di meno) e come completamento (quanto manca), prova con l’addizione.
Errori: togliere la cifra più piccola dalla più grande (42 − 7 = 45), usare l’addizione per «quanti di più».
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids
import it_c2 as C
import k_pics

R = random.Random(70205)
G = "classe-seconda"
K = Kids(R)


def w(r, extra=()):
    return [num(x) for x in list(extra) + [r + 1, r - 1, r + 10, r - 10] if 0 <= x <= 100 and x != r]


def s1_barrati():
    n, t = R.randint(6, 15), None
    t = R.randint(2, n - 2)
    k = R.choice(C.KINDS)
    pic = C.it(k_pics.crossed_row_svg(n, k, t), "%s, %d barrate" % (C.cose(k, n), t))
    return mcq(pic + "Si tolgono %s barrat%s. %s %s restano?" % ("quelle" if C.COSE[k][2] == "f" else "quelli", "e" if C.COSE[k][2] == "f" else "i", C.quanti(k), C.nome(k)), str(n - t), w(n - t, [n + t, t]),
               "%d − %d = <b>%d</b>." % (n, t, n - t))


def s1_venti():
    a = R.randint(11, 18)
    b = R.randint(a - 9, 9)
    if b <= a % 10:
        return None
    r = a - b
    return mcq("Calcola: %d − %d" % (a, b), str(r), w(r, [b - a % 10 + 10 if b - a % 10 + 10 != r else r + 2]),
               "Torna al 10: %d − %d = 10, poi − %d = <b>%d</b>." % (a, a % 10, b - a % 10, r))


def s2_decine():
    a = R.randint(30, 99)
    t = R.randint(1, a // 10 - 1) * 10
    r = a - t
    return mcq("Calcola: %d − %d" % (a, t), num(r), w(r, [a - t // 10]), "Togli %s: cambia solo la cifra delle decine. <b>%d</b>." % ("1 decina" if t == 10 else "%d decine" % (t // 10), r))


def s3_due_cifre():
    a = R.randint(30, 99)
    b = R.randint(11, a - 10)
    r = a - b
    flip = abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)
    return mcq("Calcola: %d − %d" % (a, b), num(r), w(r, [flip] if flip != r else []),
               "Togli prima le decine: %d − %d = %d. Poi le unità: %d − %d = <b>%d</b>." % (a, b // 10 * 10, a - b // 10 * 10, a - b // 10 * 10, b % 10, r))


def s3_prova():
    a, b = R.randint(30, 99), R.randint(11, 29)
    r = a - b
    return mcq("%d − %d = %d. Quale addizione fa la prova?" % (a, b, r), "%d + %d = %d" % (r, b, a), ["%d + %d = %d" % (a, b, a + b), "%d + %d = %d" % (r, a, r + a), "%d − %d = %d" % (a, r, b)],
               "Resto + numero tolto = numero di partenza: <b>%d + %d = %d</b>." % (r, b, a))


def s4_differenza():
    p1, p2 = K.two()
    a, b = R.randint(20, 90), R.randint(10, 60)
    if a <= b:
        a, b = b + 5, a
    k = R.choice(["piu", "meno", "manca"])
    if k == "piu":
        return mcq("%s ha %d figurine, %s ne ha %d. Quante figurine ha in più %s?" % (p1[0], a, p2[0], b, p1[0]), num(a - b), w(a - b, [a + b]),
                   "«Quante in più» si trova con la sottrazione: %d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "meno":
        x, y = R.randint(6, 9), R.randint(60, 85)
        return mcq("%s ha %d anni, la nonna ne ha %d. Quanti anni ha in meno %s?" % (p2[0], x, y, p2[0]), num(y - x), w(y - x, [y + x] if y + x <= 100 else []),
                   "%d − %d = <b>%d</b>." % (y, x, y - x))
    return mcq("Un album ha %d figurine. %s ne ha attaccate %d. Quante ne mancano?" % (a, p1[0], b), num(a - b), w(a - b, [a + b]),
               "Quanto manca: %d − %d = <b>%d</b>. Prova: %d + %d = %d." % (a, b, a - b, b, a - b, a))


def s5():
    p = K.next()
    k = R.choice(["caramelle", "autobus", "pagine", "palloncini", "euro", "torta"])
    a, b = R.randint(25, 95), R.randint(8, 24)
    r = a - b
    t = {"caramelle": "%s ha %d caramelle. Ne regala %d. Quante caramelle restano?" % (p[0], a, b),
         "autobus": "Sull’autobus ci sono %d persone. Ne scendono %d. Quante persone restano?" % (a, b),
         "pagine": "Un libro ha %d pagine. %s ne ha lette %d. Quante pagine deve ancora leggere?" % (a, p[0], b),
         "palloncini": "Alla festa ci sono %d palloncini. Ne scoppiano %d. Quanti palloncini restano?" % (a, b),
         "euro": "%s ha %d euro. Compra un gioco da %d euro. Quanti euro restano?" % (p[0], a, b),
         "torta": "Il pasticcere prepara %d biscotti. Ne vende %d. Quanti biscotti restano?" % (a, b)}[k]
    return mcq(t, num(r), w(r, [a + b] if a + b <= 100 else []), "%d − %d = <b>%d</b>." % (a, b, r))


def main():
    seen = set()
    sets = [
        ("Togliere", mix(R, seen, [(s1_barrati, 10), (s1_venti, 10)])),
        ("Togliere le decine", mix(R, seen, [(s2_decine, 20)])),
        ("Sottrazioni con numeri di due cifre", mix(R, seen, [(s3_due_cifre, 14), (s3_prova, 6)])),
        ("Differenza e quanto manca", mix(R, seen, [(s4_differenza, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>sottrazione</b> serve a togliere, a trovare la <b>differenza</b> (quanti di più, quanti di meno) e a sapere <b>quanto manca</b>.",
         "Per tornare indietro oltre la decina, fermati al 10: 13 − 5 = 13 − 3 − 2 = 8.",
         "Con i numeri di due cifre togli prima le <b>decine</b>, poi le <b>unità</b>: 57 − 24 = 37 − 4 = 33.",
         "Prova: risultato + numero tolto = numero di partenza."],
        [("42 − 7", ["42 − 2 = 40", "40 − 5 = 35"], "35")],
        [["42 − 7 = 45", "Togli sempre il numero in basso: 42 − 7 = 35."],
         ["Usare + per «quanti di più»", "La differenza si trova con la sottrazione."],
         ["Dimenticare la prova", "Controlla con l’addizione: 35 + 7 = 42."]])
    faq = [("Perché la sottrazione si controlla con l’addizione?", "Perché sono operazioni inverse: se 42 − 7 = 35, allora 35 + 7 = 42."),
           ("Come si capisce che un problema chiede una sottrazione?", "Quando si toglie, si confronta (quanti di più, di meno) o si cerca quanto manca.")]
    make_unit(R, "sottrazioni-entro-100", "N",
              "Eseguire mentalmente semplici sottrazioni con i numeri naturali e verbalizzare le procedure di calcolo; riconoscere la sottrazione come operazione inversa dell’addizione",
              "Le sottrazioni entro il 100", "Sottrazioni entro 100",
              "Schede di matematica per la classe seconda sulle sottrazioni entro il 100: togliere, passaggio della decina, togliere le decine, numeri di due cifre, differenza, quanto manca e problemi. 100 esercizi con soluzioni.",
              "Prima togli le decine, poi le unità.", "Prova: risultato + numero tolto.",
              body, faq, sets, 5, grade=G)


if __name__ == "__main__":
    main()
