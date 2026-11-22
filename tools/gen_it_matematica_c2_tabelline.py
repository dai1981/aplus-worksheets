# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Le tabelline (Numeri)
  python3 tools/gen_it_matematica_c2_tabelline.py
Contare a salti (2, 3, 5, 10), tabelline del 2, 5 e 10, del 3 e 4, del 6, 7, 8 e 9, per 0 e per 1,
la tabella della moltiplicazione, il fattore mancante, problemi.
Errori: confondere × con + (4 × 3 = 7), saltare un numero nel conto a salti, 0 × 6 = 6.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, FOIS, table
import it_c2 as C

R = random.Random(70208)
G = "classe-seconda"
K = Kids(R)


def wr(a, b):
    p = a * b
    return [str(x) for x in (a + b, p + a, p - b, p + 1, (a + 1) * b) if x >= 0 and x != p]


def s1_salti():
    st = R.choice([2, 3, 4, 5, 10])
    k = R.randint(1, 5)
    seq = [st * (k + i) for i in range(4)]
    if R.random() < 0.5:
        return mcq("Conta a salti di %d: %s, … Qual è il numero dopo?" % (st, ", ".join(map(str, seq))), str(seq[-1] + st), [str(seq[-1] + 1), str(seq[-1] + st + 1), str(seq[-1] + 2 * st)],
                   "Aggiungi %d: %d + %d = <b>%d</b>." % (st, seq[-1], st, seq[-1] + st))
    i = R.randint(1, 2)
    shown = [str(x) if j != i else "☐" for j, x in enumerate(seq)]
    return mcq("Quale numero manca? %s" % ", ".join(shown), str(seq[i]), [str(seq[i] + 1), str(seq[i] - 1), str(seq[i] + st)], "Si va di %d in %d: <b>%d</b>." % (st, st, seq[i]))


def fatto(tabs):
    t = R.choice(tabs)
    b = R.randint(1, 10)
    a, b = (t, b) if R.random() < 0.5 else (b, t)
    return mcq("Quanto fa %d %s %d?" % (a, FOIS, b), str(a * b), wr(a, b), "Tabellina del %d: %d %s %d = <b>%d</b>." % (t, a, FOIS, b, a * b))


def s2():
    return fatto([2, 5, 10])


def s3():
    return fatto([3, 4])


def s4():
    return fatto([6, 7, 8, 9])


def s4_zero_uno():
    a = R.randint(2, 10)
    k = R.choice([0, 1])
    return mcq("Quanto fa %d %s %d?" % (a, FOIS, k) if R.random() < 0.5 else "Quanto fa %d %s %d?" % (k, FOIS, a), str(a * k),
               [str(a), str(a + 1), "1"] if k == 0 else ["1", str(a + 1), "0"], "%s <b>%d</b>." % ("Per 0 fa sempre 0." if k == 0 else "Per 1 il numero resta uguale.", a * k))


def s4_mancante():
    a, b = R.randint(2, 10), R.randint(2, 10)
    return mcq("Quale numero manca? %d %s ☐ = %d" % (a, FOIS, a * b), str(b), [str(a * b - a) if a * b - a != b else str(b + 2), str(b + 1), str(b - 1)],
               "Nella tabellina del %d: %d %s %d = %d. <b>%d</b>." % (a, a, FOIS, b, a * b, b))


def s5():
    p = K.next()
    k = R.choice(["settimane", "mani", "zampe", "euro", "uova", "file"])
    if k == "settimane":
        n = R.randint(2, 9)
        return mcq("Quanti giorni ci sono in %d settimane?" % n, str(7 * n), wr(n, 7), "Una settimana ha 7 giorni: %d %s 7 = <b>%d</b>." % (n, FOIS, 7 * n))
    if k == "mani":
        n = R.randint(2, 10)
        return mcq("Quante dita ci sono in %d mani?" % n, str(5 * n), wr(n, 5), "Ogni mano ha 5 dita: %d %s 5 = <b>%d</b>." % (n, FOIS, 5 * n))
    if k == "zampe":
        n = R.randint(2, 9)
        an, z = R.choice([("ragni", 8), ("api", 6), ("cavalli", 4), ("struzzi", 2)])
        return mcq("Quante zampe hanno %d %s?" % (n, an), str(n * z), wr(n, z), "%d %s %d = <b>%d</b>." % (n, FOIS, z, n * z))
    if k == "euro":
        n, c = R.randint(2, 9), R.randint(2, 9)
        return mcq("Un quaderno costa %d euro. Quanto costano %d quaderni?" % (c, n), "%d euro" % (n * c), [x + " euro" for x in wr(n, c)], "%d %s %d = <b>%d euro</b>." % (n, FOIS, c, n * c))
    if k == "uova":
        n = R.randint(2, 9)
        return mcq("%s compra %d confezioni da 6 uova. Quante uova sono?" % (p[0], n), str(6 * n), wr(n, 6), "%d %s 6 = <b>%d</b>." % (n, FOIS, 6 * n))
    n, c = R.randint(2, 9), R.randint(3, 9)
    return mcq("Nell’orto ci sono %d file con %d piantine. Quante piantine ci sono?" % (n, c), str(n * c), wr(n, c), "%d %s %d = <b>%d</b>." % (n, FOIS, c, n * c))


def main():
    seen = set()
    sets = [
        ("Contare a salti", mix(R, seen, [(s1_salti, 20)])),
        ("Tabelline del 2, del 5 e del 10", mix(R, seen, [(s2, 20)])),
        ("Tabelline del 3 e del 4", mix(R, seen, [(s3, 16), (s4_zero_uno, 4)])),
        ("Tabelline del 6, 7, 8 e 9", mix(R, seen, [(s4, 14), (s4_mancante, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Una <b>tabellina</b> è un conto a salti: la tabellina del 3 è 3, 6, 9, 12, 15…",
         "Comincia dalle più facili: del <b>2</b> (i doppi), del <b>5</b> (finiscono con 0 o 5), del <b>10</b> (aggiungi uno 0).",
         "Se scambi i numeri il risultato non cambia: 3 %s 7 = 7 %s 3. Così le tabelline da imparare sono la metà!" % (FOIS, FOIS),
         "Per 1 il numero resta uguale; per 0 fa sempre 0."],
        [("6 %s 4" % FOIS, ["6 %s 4 = 4 %s 6" % (FOIS, FOIS), "4, 8, 12, 16, 20, 24"], "24")],
        [["4 %s 3 = 7" % FOIS, "Il segno %s vuol dire «volte»: 4 volte 3 = 12." % FOIS],
         ["Saltare un numero contando", "Conta con le dita a ogni salto."],
         ["0 %s 6 = 6" % FOIS, "0 volte 6 non fa niente: 0."]],
        table([FOIS] + [str(i) for i in range(1, 11)], [[str(r)] + [str(r * c) for c in range(1, 11)] for r in (2, 5, 10)]))
    faq = [("In che ordine si imparano le tabelline?", "Di solito prima 2, 5 e 10, poi 3 e 4, infine 6, 7, 8 e 9. Con la proprietà commutativa molte sono già note."),
           ("Come si ripassano a casa?", "Pochi minuti al giorno: conta a salti, gioca con le carte, cerca le tabelline nella vita di tutti i giorni (dita, ruote, settimane).")]
    make_unit(R, "tabelline", "N",
              "Conoscere con sicurezza le tabelline della moltiplicazione dei numeri fino a 10; contare per salti",
              "Le tabelline: contare a salti e moltiplicare", "Tabelline",
              "Schede di matematica per la classe seconda sulle tabelline: contare a salti, tabelline del 2, 5 e 10, del 3 e 4, del 6, 7, 8 e 9, per 0 e per 1, problemi. 100 esercizi con soluzioni.",
              "Una tabellina è un conto a salti.", "3 × 7 = 7 × 3.",
              body, faq, sets, 8, grade=G)


if __name__ == "__main__":
    main()
