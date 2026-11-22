# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Doppio e metà (Numeri)
  python3 tools/gen_it_matematica_c2_doppio_e_meta.py
Il doppio (× 2), la metà (: 2) con oggetti e con i numeri fino a 100, doppio e metà sono operazioni inverse,
il triplo, la metà di una figura, problemi.
Errori: doppio di 6 = 8 (+ 2), metà di 30 = 10, metà di una figura in parti non uguali.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, FOIS, DIV, striscia, cerchio
import it_c2 as C

R = random.Random(70210)
G = "classe-seconda"
K = Kids(R)


def s1_doppio_fig():
    n = R.randint(2, 9)
    kind = R.choice(C.KINDS)
    return mcq(C.riga(n, kind, 10) + "%s ha %s. %s ne ha il doppio. %s ne ha %s?" % ("Sofia", C.cose(kind, n), "Marco", C.quanti(kind), "Marco"), str(2 * n),
               [str(n + 2), str(n), str(3 * n), str(n // 2) if n % 2 == 0 else str(2 * n + 1)], "Il doppio è 2 volte: %d + %d = <b>%d</b>." % (n, n, 2 * n))


def s1_meta_fig():
    n = R.randint(2, 9) * 2
    kind = R.choice(C.KINDS)
    return mcq(C.riga(n, kind, 10) + "Prendi la metà. %s sono?" % C.quanti(kind), str(n // 2), [str(n - 2), str(2 * n), str(n // 2 + 1)],
               "La metà: dividi in 2 parti uguali. %d %s 2 = <b>%d</b>." % (n, DIV, n // 2))


def s2_doppio():
    a = R.choice([R.randint(2, 15), R.randint(10, 49), R.randint(1, 5) * 10])
    return mcq("Qual è il doppio di %d?" % a, str(2 * a), [str(a + 2), str(a * 3), str(a // 2) if a % 2 == 0 else str(a + 1), str(2 * a + 10)], "%d %s 2 = %d + %d = <b>%d</b>." % (a, FOIS, a, a, 2 * a))


def s2_meta():
    a = R.choice([R.randint(2, 20) * 2, R.randint(1, 10) * 10, R.randint(6, 49) * 2])
    r = a // 2
    w = [a * 2, r + 1, r - 1, a - 2]
    if a % 20 == 10:
        w.insert(0, (a - 10) // 2)
    return mcq("Qual è la metà di %d?" % a, str(r), [str(x) for x in w if 0 < x <= 200 and x != r], "%d %s 2 = <b>%d</b>, perché %d + %d = %d." % (a, DIV, r, r, r, a))


def s3_inversi():
    a = R.randint(3, 40)
    if R.random() < 0.5:
        return mcq("Il doppio di un numero è %d. Qual è il numero?" % (2 * a), str(a), [str(4 * a), str(2 * a - 2), str(a + 1)], "Fai il contrario: la metà di %d è <b>%d</b>." % (2 * a, a))
    return mcq("La metà di un numero è %d. Qual è il numero?" % a, str(2 * a), [str(a // 2) if a % 2 == 0 else str(a + 2), str(a + 2), str(2 * a + 1)], "Fai il contrario: il doppio di %d è <b>%d</b>." % (a, 2 * a))


def s3_triplo():
    a = R.randint(2, 15)
    return mcq("Qual è il triplo di %d?" % a, str(3 * a), [str(2 * a), str(a + 3), str(3 * a + 1)], "Il triplo è 3 volte: %d + %d + %d = <b>%d</b>." % (a, a, a, 3 * a))


def s4_figura():
    d = R.choice([2, 4, 6, 8])
    k = d // 2 if R.random() < 0.6 else R.choice([x for x in range(1, d) if x != d // 2])
    pic = striscia(d, k) if R.random() < 0.5 else cerchio(d, k)
    ok = "sì" if k * 2 == d else "no"
    return mcq(pic + "La parte colorata è la metà della figura?", ok, ["no" if ok == "sì" else "sì", "non si può sapere", "è il doppio"],
               "La figura ha %d parti uguali e ne sono colorate %d. %s" % (d, k, "<b>Sì</b>, è la metà." if ok == "sì" else "La metà sarebbe %d: <b>no</b>." % (d // 2)))


def s5():
    p = K.next()
    k = R.choice(["eta", "biglie", "torta", "pagine", "soldi", "km"])
    if k == "eta":
        a = R.randint(4, 9)
        return mcq("%s ha %d anni. Suo fratello ha il doppio dei suoi anni. Quanti anni ha il fratello?" % (p[0], a), str(2 * a), [str(a + 2), str(a // 2) if a % 2 == 0 else str(a - 1), str(3 * a)], "%d %s 2 = <b>%d</b>." % (a, FOIS, 2 * a))
    if k == "biglie":
        a = R.randint(6, 30) * 2
        return mcq("%s ha %d biglie e ne regala la metà. Quante biglie regala?" % (p[0], a), str(a // 2), [str(a - 2), str(2 * a), str(a // 2 + 1)], "%d %s 2 = <b>%d</b>." % (a, DIV, a // 2))
    if k == "torta":
        a = R.choice([8, 10, 12, 16, 20])
        return mcq("Una torta ha %d fette. La mamma ne dà la metà ai vicini. Quante fette restano?" % a, str(a // 2), [str(a - 2), str(a), str(a // 2 + 2)], "Se ne dà la metà, resta l’altra metà: <b>%d</b>." % (a // 2))
    if k == "pagine":
        a = R.randint(5, 25)
        return mcq("Lunedì %s legge %d pagine; martedì il doppio. Quante pagine legge martedì?" % (p[0], a), str(2 * a), [str(a + 2), str(a), str(2 * a + 10)], "%d %s 2 = <b>%d</b>." % (a, FOIS, 2 * a))
    if k == "soldi":
        a = R.randint(2, 25) * 2
        return mcq("Un gioco costa %d euro. Oggi costa la metà. Quanto costa oggi?" % a, "%d euro" % (a // 2), ["%d euro" % (a - 2), "%d euro" % (2 * a), "%d euro" % (a // 2 + 1)], "%d %s 2 = <b>%d euro</b>." % (a, DIV, a // 2))
    a = R.randint(5, 40)
    return mcq("Da casa al mare ci sono %d km. Andata e ritorno, quanti km?" % a, "%d km" % (2 * a), ["%d km" % a, "%d km" % (a + 2), "%d km" % (a // 2) if a % 2 == 0 else "%d km" % (3 * a)], "Andata + ritorno = il doppio: <b>%d km</b>." % (2 * a))


def main():
    seen = set()
    sets = [
        ("Doppio e metà con gli oggetti", mix(R, seen, [(s1_doppio_fig, 10), (s1_meta_fig, 10)])),
        ("Il doppio", mix(R, seen, [(s2_doppio, 20)])),
        ("La metà", mix(R, seen, [(s2_meta, 20)])),
        ("Al contrario, triplo e figure", mix(R, seen, [(s3_inversi, 8), (s3_triplo, 6), (s4_figura, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Il <b>doppio</b> di un numero è il numero preso 2 volte: doppio di 7 = 7 + 7 = 14.",
         "La <b>metà</b> di un numero si trova dividendo in 2 parti uguali: metà di 14 = 7.",
         "Doppio e metà sono uno il contrario dell’altro.",
         "Il <b>triplo</b> è il numero preso 3 volte."],
        [("Metà di 30", ["30 = 20 + 10", "metà di 20 = 10, metà di 10 = 5"], "15")],
        [["Doppio di 6 = 8", "Il doppio non è + 2: è 6 + 6 = 12."],
         ["Metà di 30 = 10", "Controlla: 10 + 10 = 20, non 30. È 15."],
         ["Metà con parti diverse", "Le due parti devono essere uguali."]],
        striscia(4, 2))
    faq = [("Come si calcola la metà di un numero dispari?", "In seconda si lavora con i numeri pari; un numero dispari non si divide in due parti uguali senza spezzare un’unità."),
           ("Perché doppio e metà sono importanti?", "Aiutano il calcolo mentale e preparano la moltiplicazione e la divisione.")]
    make_unit(R, "doppio-e-meta", "N",
              "Eseguire mentalmente semplici operazioni con i numeri naturali (doppio, metà, triplo) e verbalizzare le procedure di calcolo",
              "Doppio e metà", "Doppio e metà",
              "Schede di matematica per la classe seconda su doppio e metà: con gli oggetti, con i numeri fino a 100, operazioni inverse, triplo, metà di una figura e problemi. 100 esercizi con soluzioni.",
              "Doppio = 2 volte; metà = dividere in 2.", "Doppio e metà sono operazioni inverse.",
              body, faq, sets, 10, grade=G)


if __name__ == "__main__":
    main()
