# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: La divisione (Numeri)
  python3 tools/gen_it_matematica_c2_la_divisione.py
Distribuire in parti uguali (ripartizione), formare gruppi (contenenza), il segno :, divisione e tabelline,
avanza qualcosa? (resto), problemi.
Errori: gruppi non uguali, confondere il numero dei gruppi con il numero in ogni gruppo, dimenticare ciò che avanza.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, FOIS, DIV
import it_c2 as C

R = random.Random(70209)
G = "classe-seconda"
K = Kids(R)


def s1_parti():
    g, k = R.randint(2, 5), R.randint(2, 5)
    kind = R.choice(C.KINDS)
    n = g * k
    if R.random() < 0.5:
        return mcq(C.riga(n, kind, 10) + "Dividi %s in %d piatti, in parti uguali. %s in ogni piatto?" % (C.cose(kind, n), g, C.quanti(kind)), str(k), [str(g) if g != k else str(k + 1), str(n - g), str(k + 1)],
                   "%d %s %d = <b>%d</b>: in ogni piatto %s." % (n, DIV, g, k, C.cose(kind, k)))
    return mcq(C.gruppi(g, k, kind) + "%s sono stati divisi in %d gruppi uguali. Quale divisione?" % (C.cose(kind, n).capitalize(), g) if C.COSE[kind][2] == "m" else
               C.gruppi(g, k, kind) + "%s sono state divise in %d gruppi uguali. Quale divisione?" % (C.cose(kind, n).capitalize(), g), "%d %s %d = %d" % (n, DIV, g, k),
               ["%d %s %d = %d" % (n, DIV, k, g) if g != k else "%d − %d = %d" % (n, g, n - g), "%d %s %d = %d" % (g, FOIS, k, n), "%d − %d = %d" % (n, g, n - g)], "%d diviso %d fa <b>%d</b>." % (n, g, k))


def s2_contenenza():
    g, k = R.randint(2, 6), R.randint(2, 5)
    n = g * k
    p = K.next()
    return mcq("%s ha %d figurine. Le mette in bustine da %d. Quante bustine riempie?" % (p[0], n, k), str(g), [str(k) if k != g else str(g + 1), str(n - k), str(g + 1)],
               "Quante volte il %d sta nel %d? %d %s %d = <b>%d</b> bustine." % (k, n, n, DIV, k, g))


def s3_tabelline():
    b, k = R.randint(2, 10), R.randint(2, 10)
    n = b * k
    if R.random() < 0.6:
        return mcq("Quanto fa %d %s %d?" % (n, DIV, b), str(k), [str(k + 1), str(k - 1), str(n - b), str(b) if b != k else str(k + 2)],
                   "Pensa alla tabellina del %d: %d %s %d = %d. Quindi <b>%d</b>." % (b, b, FOIS, k, n, k))
    return mcq("%d %s %d = %d. Quale divisione è giusta?" % (b, FOIS, k, n), "%d %s %d = %d" % (n, DIV, b, k), ["%d %s %d = %d" % (n, DIV, b, k + 1), "%d %s %d = %d" % (b, DIV, k, n), "%d %s %d = %d" % (n, DIV, n, b)],
               "La divisione è il contrario della moltiplicazione: <b>%d %s %d = %d</b>." % (n, DIV, b, k))


def s4_resto():
    b = R.randint(2, 5)
    k = R.randint(2, 5)
    r = R.randint(0, b - 1)
    n = b * k + r
    kind = R.choice(C.KINDS)
    ans = "no, non avanza niente" if r == 0 else ("sì, ne avanza 1" if r == 1 else "sì, ne avanzano %d" % r)
    opts = ["no, non avanza niente", "sì, ne avanza 1", "sì, ne avanzano 2", "sì, ne avanzano 3", "sì, ne avanzano 4"]
    return mcq(C.riga(n, kind, 10) + "Dividi %s tra %d bambini, in parti uguali. Avanza qualcosa?" % (C.cose(kind, n), b), ans, [o for o in opts if o != ans],
               ("Ogni bambino ne riceve %d (%d %s %d = %d): <b>non avanza niente</b>." % (k, b, FOIS, k, n)) if r == 0 else
               ("Ogni bambino ne riceve %d (%d %s %d = %d); %s <b>%d</b>." % (k, b, FOIS, k, b * k, "avanza" if r == 1 else "avanzano", r)))


def s5():
    p = K.next()
    k = R.choice(["squadre", "macchine", "caramelle", "torta", "vasi", "settimane"])
    if k == "squadre":
        g, s = R.randint(2, 4), R.randint(4, 6)
        return mcq("%d bambini giocano. Fanno %d squadre uguali. Quanti bambini in ogni squadra?" % (g * s, g), str(s), [str(g), str(g * s - g), str(s + 1)], "%d %s %d = <b>%d</b>." % (g * s, DIV, g, s))
    if k == "macchine":
        n = R.randint(3, 6) * 4
        return mcq("%d persone vanno in gita. In ogni auto salgono 4 persone. Quante auto servono?" % n, str(n // 4), [str(4), str(n - 4), str(n // 4 + 1)], "%d %s 4 = <b>%d</b> auto." % (n, DIV, n // 4))
    if k == "caramelle":
        b, k_ = R.randint(2, 5), R.randint(3, 6)
        return mcq("%s ha %d caramelle e le divide con %d amici: in tutto sono %d bambini. Quante caramelle a testa?" % (p[0], b * k_, b - 1, b), str(k_), [str(b), str(b * k_ // (b - 1)) if b > 1 and (b * k_) % (b - 1) == 0 and b * k_ // (b - 1) != k_ else str(k_ + 1), str(k_ - 1)],
                   "Sono %d bambini (con %s): %d %s %d = <b>%d</b>." % (b, p[0], b * k_, DIV, b, k_))
    if k == "torta":
        f = R.choice([6, 8, 10, 12])
        b = R.choice([x for x in (2, 3, 4, 5, 6) if f % x == 0])
        return mcq("Una torta ha %d fette. La dividono %d bambini. Quante fette a testa?" % (f, b), str(f // b), [str(b), str(f - b), str(f // b + 1)], "%d %s %d = <b>%d</b>." % (f, DIV, b, f // b))
    if k == "vasi":
        v, f = R.randint(2, 5), R.randint(3, 6)
        return mcq("Il nonno ha %d fiori e li mette in %d vasi, lo stesso numero in ognuno. Quanti fiori per vaso?" % (v * f, v), str(f), [str(v), str(v * f - v), str(f + 2)], "%d %s %d = <b>%d</b>." % (v * f, DIV, v, f))
    w = R.randint(2, 5)
    return mcq("Quante settimane sono %d giorni?" % (7 * w), str(w), [str(7), str(7 * w - 7), str(w + 1)], "Una settimana ha 7 giorni: %d %s 7 = <b>%d</b>." % (7 * w, DIV, w))


def main():
    seen = set()
    sets = [
        ("Dividere in parti uguali", mix(R, seen, [(s1_parti, 20)])),
        ("Fare gruppi", mix(R, seen, [(s2_contenenza, 20)])),
        ("Divisione e tabelline", mix(R, seen, [(s3_tabelline, 20)])),
        ("Avanza qualcosa?", mix(R, seen, [(s4_resto, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["<b>Dividere</b> vuol dire fare parti uguali (12 caramelle a 3 bambini: 4 a testa) oppure fare gruppi (12 caramelle in sacchetti da 3: 4 sacchetti).",
         "Il segno della divisione sono i due punti: 12 %s 3 = 4." % DIV,
         "La divisione è il contrario della moltiplicazione: 3 %s 4 = 12, quindi 12 %s 3 = 4." % (FOIS, DIV),
         "A volte qualcosa <b>avanza</b>: 7 caramelle a 3 bambini → 2 a testa e ne avanza 1."],
        [("15 mele in 3 cestini", ["3 %s 5 = 15" % FOIS, "15 %s 3 = 5" % DIV], "5 mele per cestino")],
        [["Fare parti non uguali", "Ogni parte deve avere lo stesso numero."],
         ["Confondere gruppi e oggetti nei gruppi", "Leggi bene: quanti gruppi o quanti in ogni gruppo?"],
         ["Dimenticare ciò che avanza", "Conta quello che resta alla fine."]],
        C.gruppi(3, 4, "apple"))
    faq = [("Come si spiega la divisione a un bambino di seconda?", "Con oggetti veri: distribuire biscotti nei piatti uno alla volta finché sono finiti, poi contare quanti ce ne sono in ogni piatto."),
           ("Perché la divisione si lega alle tabelline?", "Perché per dividere 20 per 4 basta cercare nella tabellina del 4 il numero che dà 20: 4 × 5.")]
    make_unit(R, "la-divisione", "N",
              "Eseguire divisioni come ripartizione e contenenza in situazioni concrete; riconoscere la divisione come operazione inversa della moltiplicazione",
              "La divisione: parti uguali e gruppi", "La divisione",
              "Schede di matematica per la classe seconda sulla divisione: dividere in parti uguali, fare gruppi, divisione e tabelline, avanza qualcosa e problemi. 100 esercizi con soluzioni.",
              "Dividere = fare parti uguali.", "12 : 3 = 4 perché 3 × 4 = 12.",
              body, faq, sets, 9, grade=G)


if __name__ == "__main__":
    main()
