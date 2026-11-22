# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Comporre e scomporre i numeri, gli amici del 10 (Numeri)
  python3 tools/gen_it_matematica_c1_amici_del_10.py
Scomporre un numero fino a 10 in due parti, le coppie che fanno 10 (amici del 10), quanto manca a 10 con lo schema
del dieci, scegliere la coppia giusta, oggetti nascosti nella scatola.
Errori: dimenticare la coppia con lo 0, contare anche le caselle vuote, sommare invece di trovare la parte che manca.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C

R = random.Random(70104)
G = "classe-prima"


def s1_coppia():
    n = R.randint(3, 10)
    a = R.randint(0, n)
    b = n - a
    if R.random() < 0.5:
        pic = C.coppia(n, a, "?")
        ans = b
    else:
        pic = C.coppia(n, "?", b)
        ans = a
    return mcq(pic + "Il numero in alto è diviso in due parti. Quale numero va al posto del «?»?", str(ans), [str(n), str(ans + 1), str(abs(ans - 1)), str(n + (n - ans))],
               "%d e %d fanno %d: manca <b>%d</b>." % (n - ans, ans, n, ans))


def s2_dieci():
    n = R.randint(1, 9)
    return mcq(C.dieci(n) + "Quanti pallini mancano per riempire lo schema (10)?", str(10 - n), [str(n), str(11 - n), str(9 - n) if n < 9 else "2"],
               "Conta le caselle vuote: %d + <b>%d</b> = 10." % (n, 10 - n))


def s3_amici():
    a = R.randint(0, 10)
    k = R.choice(["a", "b", "parola"])
    if k == "parola":
        return mcq("Qual è l’amico del 10 di %d? (insieme fanno 10)" % a, str(10 - a), [str(a), str(11 - a) if a < 11 else "1", str(abs(9 - a))],
                   "%d + %d = 10: l’amico è <b>%d</b>." % (a, 10 - a, 10 - a))
    if k == "a":
        return mcq("Completa: %d + ? = 10" % a, str(10 - a), [str(10 + a) if a else "1", str(11 - a), str(a)], "%d + <b>%d</b> = 10." % (a, 10 - a))
    return mcq("Completa: ? + %d = 10" % a, str(10 - a), [str(9 - a) if a < 9 else "2", str(11 - a), str(a)], "<b>%d</b> + %d = 10." % (10 - a, a))


def s4_quale():
    n = R.randint(3, 10)
    if R.random() < 0.5:
        a = R.randint(0, n)
        ok = "%d e %d" % (a, n - a)
        bad = set()
        while len(bad) < 3:
            x, y = R.randint(0, 9), R.randint(0, 9)
            if x + y != n and abs(x + y - n) <= 2:
                bad.add("%d e %d" % (x, y))
        return mcq("Quale coppia di numeri fa %d?" % n, ok, sorted(bad), "%d + %d = %d: <b>%s</b>." % (a, n - a, n, ok))
    good = sorted({"%d e %d" % (i, n - i) for i in R.sample(range(n + 1), 3)})
    while True:
        x, y = R.randint(0, 9), R.randint(0, 9)
        if x + y != n and abs(x + y - n) <= 2:
            break
    bad = "%d e %d" % (x, y)
    return mcq("Quale coppia <b>non</b> fa %d?" % n, bad, good, "%d + %d = %d, non %d: <b>%s</b>." % (x, y, x + y, n, bad))


def s4_modi():
    n = R.randint(2, 9)
    return mcq("In quanti modi puoi dividere %d palline in due scatole? (conta anche quando una scatola è vuota)" % n, str(n + 1), [str(n), str(n - 1), str(2 * n)],
               "Le coppie sono: %s. Sono <b>%d</b>." % (", ".join("%d e %d" % (i, n - i) for i in range(n + 1)), n + 1))


def s5():
    k = R.choice(C.KINDS)
    kind = R.choice(["scatola", "scatola", "mani", "piatti", "mancano"])
    if kind == "scatola":
        tot = R.randint(5, 10)
        a = R.randint(1, tot - 1)
        return mcq(C.scatola(a, k) + "In tutto ci sono %s. %s sono nella scatola?" % (C.cose(k, tot), C.Q(k)), str(tot - a), [str(a), str(tot), str(tot - a + 1)],
                   "Fuori ce ne sono %d: %d + <b>%d</b> = %d." % (a, a, tot - a, tot))
    if kind == "mani":
        a = R.randint(0, 10)
        return mcq("Ho 10 caramelle in tutto. In una mano ne tengo %d. Quante sono nell’altra mano?" % a, str(10 - a), [str(a), str(11 - a), str(10)] if a != 0 else ["0", "9", "11"],
                   "%d + <b>%d</b> = 10." % (a, 10 - a))
    if kind == "piatti":
        n = R.randint(4, 10)
        a = R.randint(1, n - 1)
        return mcq(C.piatto(a, k) + "Nel piatto ci sono %s. Ne voglio %d. Quante ne devo aggiungere?" % (C.cose(k, a), n), str(n - a), [str(n), str(a), str(n + a)],
                   "%d + <b>%d</b> = %d." % (a, n - a, n))
    a = R.randint(3, 9)
    return mcq("Sul pullmino ci sono 10 posti. Sono seduti %d bambini. Quanti posti sono liberi?" % a, str(10 - a), [str(a), str(10 + a), str(11 - a)], "%d + <b>%d</b> = 10." % (a, 10 - a))


def main():
    seen = set()
    sets = [
        ("Un numero in due parti", mix(R, seen, [(s1_coppia, 20)])),
        ("Quanto manca a 10?", mix(R, seen, [(s2_dieci, 9), (s3_amici, 11)])),
        ("Gli amici del 10", mix(R, seen, [(s3_amici, 14), (s4_quale, 6)])),
        ("Coppie e modi", mix(R, seen, [(s4_quale, 10), (s4_modi, 8), (s1_coppia, 2)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un numero si può <b>scomporre</b> in due parti: 7 è 5 e 2, ma anche 4 e 3, 6 e 1, 7 e 0.",
         "Gli <b>amici del 10</b> sono le coppie che insieme fanno 10: 1 e 9, 2 e 8, 3 e 7, 4 e 6, 5 e 5 (e 0 e 10).",
         "Con lo schema del dieci vedi subito quanto manca a 10: conta le caselle vuote."],
        [("8 + ? = 10", ["8 pallini, 2 caselle vuote"], "2")],
        [["Dimenticare la coppia con lo 0", "Anche 0 e 7 fanno 7."],
         ["Contare i pallini invece delle caselle vuote", "Quanto manca = caselle vuote."],
         ["Fare 8 + 10 invece di cercare quanto manca", "Chiediti: 8 più quanto fa 10?"]],
        table(["Amici del 10", ""], [["1 + 9", "9 + 1"], ["2 + 8", "8 + 2"], ["3 + 7", "7 + 3"], ["4 + 6", "6 + 4"], ["5 + 5", ""]]))
    faq = [("Perché sono importanti gli amici del 10?", "Servono sempre nel calcolo a mente: 8 + 5 diventa 8 + 2 + 3 = 13."),
           ("Come si esercitano a casa?", "Con 10 oggetti e due mani: si nascondono alcuni oggetti in una mano e si chiede quanti sono nell’altra.")]
    make_unit(R, "amici-del-10", "N",
              "Comporre e scomporre i numeri entro il 10; conoscere con sicurezza le coppie di numeri che danno 10",
              "Comporre e scomporre i numeri: gli amici del 10", "Amici del 10",
              "Schede di matematica per la classe prima su comporre e scomporre i numeri: un numero in due parti, schema del dieci, gli amici del 10, coppie e problemi con la scatola. 100 esercizi con soluzioni.",
              "Gli amici del 10: 1 e 9, 2 e 8, 3 e 7, 4 e 6, 5 e 5.", "Quanto manca a 10? Conta le caselle vuote.",
              body, faq, sets, 4, grade=G)


if __name__ == "__main__":
    main()
