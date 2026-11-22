# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Operazioni con le frazioni (Numeri)
  python3 tools/gen_it_matematica_c5_operazioni_con_le_frazioni.py
Frazione di un numero, calcolare l’intero conoscendo una parte (problema inverso), addizioni e sottrazioni
con lo stesso denominatore, frazione complementare, problemi con le frazioni.
Errori: sommare anche i denominatori (1/5 + 2/5 = 3/10), nel problema inverso dividere invece di moltiplicare,
moltiplicare per il numeratore senza dividere per il denominatore.
"""
import random
from math import gcd
from it_common import mcq, num, lesson, make_unit, mix, Kids, fr, eur, DIV, FOIS

R = random.Random(70512)
G = "classe-quinta"
K = Kids(R)
F = fr


def s1_di():
    d = R.randint(2, 10)
    n = R.randint(1, d - 1)
    if gcd(n, d) > 1:
        return None
    q = R.randint(2, 25)
    tot = d * q
    r = q * n
    return mcq("Quanto fa %s di %s?" % (F(n, d), num(tot)), num(r), [num(q), num(tot * n), num(tot - r) if tot - r != r else num(r + q), num(tot // n) if tot % n == 0 and n > 1 else num(r + 1)],
               "Dividi per il denominatore e moltiplica per il numeratore: %s %s %d = %d; %d %s %d = <b>%s</b>." % (num(tot), DIV, d, q, q, FOIS, n, num(r)))


def s2_inverso():
    d = R.randint(2, 10)
    n = R.randint(1, d - 1)
    if gcd(n, d) > 1:
        return None
    q = R.randint(2, 30)
    part, tot = q * n, q * d
    return mcq("%s di un numero è %s. Qual è il numero?" % (F(n, d), num(part)), num(tot), [num(part * n // d) if (part * n) % d == 0 else num(part // n * d + d), num(part * d), num(part // n) if n > 1 else num(part + d), num(tot + q)],
               "Trova l’unità frazionaria: %s %s %d = %d (cioè %s); poi moltiplica per %d: <b>%s</b>." % (num(part), DIV, n, q, F(1, d), d, num(tot)))


def s3_somma():
    d = R.randint(3, 15)
    a, b = R.randint(1, d - 2), R.randint(1, d - 2)
    if R.random() < 0.5:
        if a + b > d:
            return None
        r = F(a + b, d)
        return mcq("Calcola: %s + %s" % (F(a, d), F(b, d)), r, [F(a + b, 2 * d), F(a * b, d), F(a + b + 1, d), F(a + b, d + 1)],
                   "Stesso denominatore: sommi solo i numeratori. %d + %d = %d: <b>%s</b>." % (a, b, a + b, r))
    if a <= b:
        a, b = b, a
    if a == b:
        return None
    r = F(a - b, d)
    return mcq("Calcola: %s − %s" % (F(a, d), F(b, d)), r, [F(a - b, d - 1), F(a + b, d), F(a - b + 1, d), "0"],
               "Stesso denominatore: sottrai solo i numeratori. %d − %d = %d: <b>%s</b>." % (a, b, a - b, r))


def s3_complementare():
    d = R.randint(3, 12)
    n = R.randint(1, d - 1)
    return mcq("Qual è la frazione complementare di %s?" % F(n, d), F(d - n, d), [F(n, d - n) if d - n != n else F(n + 1, d), F(d, n), F(d - n, d + n), F(1, d)],
               "Insieme devono fare l’intero %s: %s + <b>%s</b> = %s." % (F(d, d), F(n, d), F(d - n, d), F(d, d)))


def s4_tre():
    d = R.choice([4, 5, 6, 8, 10, 12])
    a, b = R.randint(1, d - 2), R.randint(1, d - 2)
    c = d - a - b if d - a - b > 0 else None
    if not c:
        return None
    return mcq("Calcola: %s + %s + %s" % (F(a, d), F(b, d), F(c, d)), "1", [F(a + b + c, 3 * d), F(d - 1, d), "3"],
               "%d + %d + %d = %d: %s = <b>1</b> intero." % (a, b, c, d, F(d, d)))


def s5():
    p = K.next()
    k = R.choice(["paga", "km", "spesa", "inverso", "resta", "torta", "inverso2"])
    if k == "paga":
        d, n = R.choice([(4, 3), (5, 2), (3, 2), (10, 3), (8, 5)])
        tot = d * R.randint(4, 30) * 10
        return mcq("%s ha %s € e spende %s dei suoi soldi per un regalo. Quanto spende?" % (p[0], num(tot), F(n, d)), "%s €" % num(tot // d * n),
                   ["%s €" % num(tot // d), "%s €" % num(tot - tot // d * n), "%s €" % num(tot * n)], "%s %s %d %s %d = <b>%s €</b>." % (num(tot), DIV, d, FOIS, n, num(tot // d * n)))
    if k == "km":
        d, n = R.choice([(4, 1), (5, 2), (3, 1), (6, 5), (8, 3)])
        tot = d * R.randint(10, 60)
        return mcq("Un percorso è lungo %s km. Dopo %s del percorso c’è una sosta. Quanti km mancano dalla sosta all’arrivo?" % (num(tot), F(n, d)), "%s km" % num(tot - tot // d * n),
                   ["%s km" % num(tot // d * n), "%s km" % num(tot // d), "%s km" % num(tot - n)], "Fatti: %s km; mancano %s − %s = <b>%s km</b>." % (num(tot // d * n), num(tot), num(tot // d * n), num(tot - tot // d * n)))
    if k == "spesa":
        d = R.choice([2, 4, 5, 10])
        pr = d * R.randint(3, 40) * 100
        return mcq("Una bicicletta costa %s. Oggi c’è uno sconto di %s del prezzo. Quanto si risparmia?" % (eur(pr), F(1, d)), eur(pr // d), [eur(pr - pr // d), eur(pr * d), eur(pr // d + 100)],
                   "%s di %s: %s %s %d = <b>%s</b>." % (F(1, d), eur(pr), eur(pr), DIV, d, eur(pr // d)))
    if k == "inverso":
        d, n = R.choice([(4, 3), (5, 2), (3, 2), (6, 5), (10, 7)])
        q = R.randint(3, 20)
        part = q * n
        return mcq("%s ha letto %d pagine, cioè %s del libro. Quante pagine ha il libro?" % (p[0], part, F(n, d)), str(q * d), [str(part * d), str(q), str(part + q)],
                   "%d %s %d = %d (pagine di %s); %d %s %d = <b>%d</b> pagine." % (part, DIV, n, q, F(1, d), q, FOIS, d, q * d))
    if k == "resta":
        d = R.choice([5, 8, 10])
        a, b = R.randint(1, d // 2), R.randint(1, d // 2)
        if a + b >= d:
            return None
        return mcq("Di una torta %s ne mangia %s e la sorella %s. Che parte di torta resta?" % (p[0], F(a, d), F(b, d)), F(d - a - b, d), [F(a + b, d), F(d - a - b, 2 * d), F(d - a, d)],
                   "Mangiate: %s; resta %s − %s = <b>%s</b>." % (F(a + b, d), F(d, d), F(a + b, d), F(d - a - b, d)))
    if k == "torta":
        d, n = R.choice([(3, 2), (4, 3), (5, 3)])
        g = d * R.randint(5, 15) * 10
        return mcq("Per una torta servono %d g di farina; Chiara ne ha già messi %s. Quanti grammi ha messo?" % (g, F(n, d)), "%d g" % (g // d * n), ["%d g" % (g // d), "%d g" % (g - g // d * n), "%d g" % (g * n)],
                   "%d %s %d %s %d = <b>%d g</b>." % (g, DIV, d, FOIS, n, g // d * n))
    d = R.choice([3, 4, 5])
    q = R.randint(5, 30)
    return mcq("I %s dei bambini di una scuola fanno sport: sono %d. Quanti bambini ci sono nella scuola?" % (F(d - 1, d), q * (d - 1)), num(q * d),
               [num(q * (d - 1) * d), num(q), num(q * (d - 1) + q * 2)], "%d %s %d = %d; %d %s %d = <b>%s</b>." % (q * (d - 1), DIV, d - 1, q, q, FOIS, d, num(q * d)))


def main():
    seen = set()
    sets = [
        ("Frazione di un numero", mix(R, seen, [(s1_di, 20)])),
        ("Dalla parte all’intero", mix(R, seen, [(s2_inverso, 20)])),
        ("Addizioni e sottrazioni", mix(R, seen, [(s3_somma, 14), (s4_tre, 6)])),
        ("Frazione complementare", mix(R, seen, [(s3_complementare, 12), (s1_di, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per calcolare %s di 24: dividi per il denominatore (24 %s 4 = 6) e moltiplica per il numeratore (6 %s 3 = 18)." % (F(3, 4), DIV, FOIS),
         "Problema inverso: se %s di un numero è 18, dividi per il numeratore (18 %s 3 = 6, cioè %s) e moltiplica per il denominatore (6 %s 4 = 24)." % (F(3, 4), DIV, F(1, 4), FOIS),
         "Per sommare o sottrarre frazioni con lo <b>stesso denominatore</b> si sommano o sottraggono solo i numeratori.",
         "La frazione <b>complementare</b> è quella che manca per arrivare all’intero."],
        [("%s di 35" % F(2, 5), ["35 %s 5 = 7" % DIV, "7 %s 2 = 14" % FOIS], "14"),
         ("%s di un numero = 21" % F(3, 7), ["21 %s 3 = 7" % DIV, "7 %s 7 = 49" % FOIS], "49")],
        [["%s + %s = %s" % (F(1, 5), F(2, 5), F(3, 10)), "Il denominatore resta 5: %s." % F(3, 5)],
         ["Nel problema inverso dividere per il denominatore", "Conosci la parte: dividi per il numeratore, moltiplica per il denominatore."],
         ["Moltiplicare per il numeratore e basta", "Prima dividi per il denominatore."]])
    faq = [("Come si calcola l’intero conoscendo una frazione?", "Si divide la parte per il numeratore (si trova l’unità frazionaria) e si moltiplica per il denominatore."),
           ("Perché nelle addizioni il denominatore non cambia?", "Perché indica la grandezza delle parti: 1 quinto + 2 quinti = 3 quinti, le parti sono sempre quinti.")]
    make_unit(R, "operazioni-con-le-frazioni", "N",
              "Calcolare la frazione di una quantità e risalire all’intero conoscendo una sua parte; addizionare e sottrarre frazioni con lo stesso denominatore; risolvere problemi con le frazioni",
              "Operazioni con le frazioni: frazione di un numero e problemi", "Operazioni con le frazioni",
              "Schede di matematica per la classe quinta sulle operazioni con le frazioni: frazione di un numero, dalla parte all’intero, addizioni e sottrazioni, frazione complementare e problemi. 100 esercizi con soluzioni.",
              "Frazione di un numero: dividi per il denominatore, moltiplica per il numeratore.", "Dalla parte all’intero: dividi per il numeratore, moltiplica per il denominatore.",
              body, faq, sets, 12, grade=G)


if __name__ == "__main__":
    main()
