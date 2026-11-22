# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Moltiplicare e dividere per 10, 100, 1000 (Numeri)
  python3 tools/gen_it_matematica_c3_moltiplicare_e_dividere_per_10_100_1000.py
× 10, × 100, × 1000 (le cifre si spostano a sinistra, si aggiungono zeri), : 10, : 100, : 1000 con numeri che finiscono
con zeri, numero mancante, cambi (decine, centinaia, migliaia), problemi.
Errori: aggiungere un solo zero per × 100, togliere uno zero di troppo, confondere × e :.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, DIV, pl

R = random.Random(70309)
K = Kids(R)
Z = {10: 1, 100: 2, 1000: 3}


def s1_per10():
    a = R.randint(2, 99)
    r = a * 10
    return mcq("Quanto fa %d %s 10?" % (a, FOIS), num(r), [num(a * 100), num(a + 10), num(a), str(a) + "1"],
               "Per moltiplicare per 10 le cifre si spostano di un posto a sinistra: aggiungi uno 0. <b>%s</b>." % num(r))


def s1_diviso10():
    a = R.randint(2, 99) * 10
    r = a // 10
    return mcq("Quanto fa %s %s 10?" % (num(a), DIV), num(r), [num(a * 10), num(a - 10), num(r // 10) if r >= 10 and r % 10 == 0 else num(r + 1), num(a // 100) if a >= 100 else num(r * 2)],
               "Per dividere per 10 le cifre si spostano di un posto a destra: togli uno 0. <b>%s</b>." % num(r))


def s2():
    k = R.choice([10, 100, 100, 1000])
    a = R.randint(2, 9) if k == 1000 else R.randint(2, 99 if k == 10 else 9 if R.random() < 0.6 else 99)
    if a * k > 9999:
        return None
    r = a * k
    other = [x for x in (10, 100, 1000) if x != k]
    return mcq("Quanto fa %d %s %s?" % (a, FOIS, num(k)), num(r), [num(a * o) for o in other if a * o < 100000] + [num(a + k)],
               "Quando moltiplichi per %s aggiungi %s a destra: <b>%s</b>." % (num(k), pl(Z[k], "zero", "zeri"), num(r)))


def s3():
    k = R.choice([10, 100, 100, 1000])
    r = R.randint(2, 9 if k == 1000 else 99)
    a = r * k
    if a > 9999:
        return None
    other = [x for x in (10, 100, 1000) if x != k and a % x == 0]
    return mcq("Quanto fa %s %s %s?" % (num(a), DIV, num(k)), num(r), [num(a // o) for o in other] + [num(a * 10) if a * 10 < 100000 else None, num(a - k), num(r + 1)],
               "Quando dividi per %s togli %s a destra: <b>%s</b>." % (num(k), pl(Z[k], "zero", "zeri"), num(r)))


def s4_mancante():
    k = R.choice([10, 100, 1000])
    a = R.randint(2, 9 if k == 1000 else 50)
    r = a * k
    if r > 9999:
        return None
    if R.random() < 0.5:
        return mcq("Quale numero va nel quadratino? %d %s ☐ = %s" % (a, FOIS, num(r)), num(k), [num(x) for x in (10, 100, 1000) if x != k] + ["0"],
                   "Da %d a %s si aggiungono %s: il numero è <b>%s</b>." % (a, num(r), pl(Z[k], "zero", "zeri"), num(k)))
    return mcq("Quale numero va nel quadratino? %s %s ☐ = %d" % (num(r), DIV, a), num(k), [num(x) for x in (10, 100, 1000) if x != k] + ["0"],
               "Da %s a %d si tolgono %s: il numero è <b>%s</b>." % (num(r), a, pl(Z[k], "zero", "zeri"), num(k)))


def s4_cambi():
    k = R.choice(["dau", "hda", "hu", "ukh"])
    a = R.randint(2, 9 if k in ("hu", "ukh") else 30)
    if k == "dau":
        return mcq("%s quante unità sono?" % pl(a, "decina", "decine").capitalize(), num(a * 10), [num(a * 100), num(a), num(a + 10)],
                   "1 decina = 10 unità: %d %s 10 = <b>%s</b> unità." % (a, FOIS, num(a * 10)))
    if k == "hda":
        a = R.randint(2, 9)
        return mcq("%s quante decine sono?" % pl(a, "centinaio", "centinaia").capitalize(), num(a * 10), [num(a * 100), num(a), num(a + 10)],
                   "1 centinaio = 10 decine: %d %s 10 = <b>%s</b> decine." % (a, FOIS, num(a * 10)))
    if k == "hu":
        return mcq("%s quante unità sono?" % pl(a, "centinaio", "centinaia").capitalize(), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)],
                   "1 centinaio = 100 unità: %d %s 100 = <b>%s</b> unità." % (a, FOIS, num(a * 100)))
    return mcq("%s quante centinaia sono?" % pl(a, "migliaio", "migliaia").capitalize(), num(a * 10), [num(a * 100), num(a), num(a * 1000)],
               "1 migliaio = 10 centinaia: %d %s 10 = <b>%s</b> centinaia." % (a, FOIS, num(a * 10)))


def s5_problema():
    p = K.next()
    k = R.choice(["pacchi", "euro", "scatole", "cent", "fogli", "metri"])
    if k == "pacchi":
        a = R.randint(3, 60)
        return mcq("Un negozio riceve %d pacchi di quaderni. In ogni pacco ci sono 10 quaderni. Quanti quaderni riceve?" % a, num(a * 10),
                   [num(a * 100), num(a + 10), num(a)], "%d %s 10 = <b>%s</b> quaderni." % (a, FOIS, num(a * 10)))
    if k == "euro":
        a = R.randint(2, 9)
        return mcq("%s ha %s da 100 €. Quanti euro ha?" % (p[0], pl(a, "banconota", "banconote")), num(a * 100) + " €",
                   [num(a * 10) + " €", num(a * 1000) + " €", num(a + 100) + " €"], "%d %s 100 = <b>%s €</b>." % (a, FOIS, num(a * 100)))
    if k == "scatole":
        a = R.randint(2, 60) * 10
        return mcq("In una fabbrica ci sono %s matite. Si mettono in scatole da 10. Quante scatole servono?" % num(a), num(a // 10),
                   [num(a * 10), num(a - 10), num(a // 100) if a >= 100 else num(a // 10 + 1)], "%s %s 10 = <b>%s</b> scatole." % (num(a), DIV, num(a // 10)))
    if k == "cent":
        a = R.randint(2, 9)
        return mcq("1 € vale 100 centesimi. Quanti centesimi valgono %d €?" % a, num(a * 100),
                   [num(a * 10), num(a * 1000), num(a + 100)], "%d %s 100 = <b>%s</b> centesimi." % (a, FOIS, num(a * 100)))
    if k == "fogli":
        a = R.randint(2, 9) * 100
        return mcq("Una risma di %s fogli viene divisa in pacchetti da 100. Quanti pacchetti si fanno?" % num(a), num(a // 100),
                   [num(a // 10), num(a - 100), num(a // 100 + 1)], "%s %s 100 = <b>%s</b> pacchetti." % (num(a), DIV, num(a // 100)))
    a = R.randint(2, 9)
    return mcq("Un chilometro è lungo 1000 metri. Quanti metri sono %d km?" % a, num(a * 1000) + " m",
               [num(a * 100) + " m", num(a * 10) + " m", num(a + 1000) + " m"], "%d %s 1000 = <b>%s m</b>." % (a, FOIS, num(a * 1000)))


def main():
    seen = set()
    sets = [
        ("Per 10 e diviso 10", mix(R, seen, [(s1_per10, 10), (s1_diviso10, 10)])),
        ("Per 10, per 100, per 1000", mix(R, seen, [(s2, 20)])),
        ("Diviso 10, diviso 100, diviso 1000", mix(R, seen, [(s3, 20)])),
        ("Numero mancante e cambi", mix(R, seen, [(s4_mancante, 10), (s4_cambi, 10)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Quando moltiplichi per <b>10</b> ogni cifra si sposta di un posto a sinistra: le unità diventano decine. Si scrive uno 0 a destra.",
         "Per <b>100</b> si aggiungono due zeri, per <b>1000</b> tre zeri.",
         "Quando dividi per 10, 100 o 1000 un numero che finisce con abbastanza zeri, togli uno, due o tre zeri.",
         "10 unità = 1 decina; 10 decine = 1 centinaio; 10 centinaia = 1 migliaio."],
        [("36 %s 100" % FOIS, ["aggiungo due zeri"], "3600"),
         ("4500 %s 10" % DIV, ["tolgo uno zero"], "450")],
        [["36 %s 100 = 360" % FOIS, "Per 100 gli zeri sono due: 3600."],
         ["4500 %s 10 = 45" % DIV, "Diviso 10 si toglie un solo zero: 450."],
         ["Confondere %s e %s" % (FOIS, DIV), "Moltiplicare fa diventare il numero più grande, dividere più piccolo."]])
    faq = [("Perché per 10 si aggiunge uno zero?", "Perché ogni cifra vale 10 volte di più: le unità diventano decine e il posto delle unità resta vuoto, così si scrive 0."),
           ("Si può dividere per 10 un numero che non finisce con 0?", "Sì, ma il risultato ha la virgola (35 : 10 = 3,5). In classe terza si usano soprattutto numeri che finiscono con 0.")]
    make_unit(R, "moltiplicare-e-dividere-per-10-100-1000", "N",
              "Eseguire mentalmente moltiplicazioni e divisioni per 10, 100 e 1000; conoscere le relazioni tra unità, decine, centinaia e migliaia nella notazione posizionale",
              "Moltiplicare e dividere per 10, 100 e 1000", "Per 10, 100, 1000",
              "Schede di matematica per la classe terza su moltiplicazioni e divisioni per 10, 100 e 1000: aggiungere e togliere zeri, numero mancante, cambi tra decine e centinaia, problemi. 100 esercizi con soluzioni.",
              "Per 10, 100, 1000 si aggiungono 1, 2, 3 zeri.", "Per : 10, : 100, : 1000 si tolgono 1, 2, 3 zeri.",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
