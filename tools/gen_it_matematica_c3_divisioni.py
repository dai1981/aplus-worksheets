# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: Le divisioni (Numeri)
  python3 tools/gen_it_matematica_c3_divisioni.py
Divisione come ripartizione e come contenenza, divisione e tabelline, divisione con il resto, dividere un numero
di due o tre cifre per una cifra, prova, problemi (pari e dispari, quanti gruppi, quanto avanza).
Errori: resto maggiore del divisore, confondere dividendo e divisore, dimenticare il resto nei problemi.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, wrap, Kids, FOIS, DIV, GREEN, FILL, INK, line

R = random.Random(70308)
K = Kids(R)


def gruppi(n, g):
    """n pallini in gruppi di g, cerchiati"""
    k, r = divmod(n, g)
    s, x = [], 8
    for i in range(k):
        w = g * 20 + 8
        s.append("<rect x='%d' y='6' width='%d' height='34' rx='14' fill='none' stroke='%s' stroke-width='1.8'/>" % (x, w, GREEN))
        for j in range(g):
            s.append("<circle cx='%d' cy='23' r='7' fill='%s' stroke='%s' stroke-width='1.3'/>" % (x + 14 + j * 20, FILL, GREEN))
        x += w + 10
    for j in range(r):
        s.append("<circle cx='%d' cy='23' r='7' fill='#fde68a' stroke='%s' stroke-width='1.3'/>" % (x + 10 + j * 20, INK))
    x += r * 20 + 10
    return wrap(x + 4, 46, "".join(s), "%d pallini in gruppi da %d" % (n, g))


def q_div(a, b):
    return "%s %s %d" % (num(a), DIV, b)


def s1_gruppi():
    g, k = R.randint(2, 5), R.randint(2, 5)
    n = g * k
    return mcq(gruppi(n, g) + "Quale divisione racconta il disegno?", "%d %s %d = %d" % (n, DIV, g, k),
               ["%d %s %d = %d" % (n, DIV, k, g) if g != k else "%d − %d = %d" % (n, g, n - g), "%d %s %d = %d" % (k, FOIS, g, n), "%d − %d = %d" % (n, g, n - g), "%d %s %d = %d" % (n, DIV, g, k + 1)],
               "Ci sono %d pallini in gruppi da %d: i gruppi sono %d. <b>%d %s %d = %d</b>." % (n, g, k, n, DIV, g, k))


def s1_ripartizione():
    p = K.next()
    b, k = R.randint(2, 6), R.randint(2, 9)
    n = b * k
    return mcq("%s divide %d caramelle in parti uguali tra %d amici. Quante caramelle riceve ciascuno?" % (p[0], n, b), str(k),
               [str(n - b), str(k + 1), str(b), str(n + b)],
               "%d %s %d = <b>%d</b>, perché %d %s %d = %d." % (n, DIV, b, k, b, FOIS, k, n))


def fatto():
    b, k = R.randint(2, 10), R.randint(2, 10)
    n = b * k
    return mcq("Quanto fa %d %s %d?" % (n, DIV, b), str(k), [str(k + 1), str(k - 1), str(n - b), str(b) if b != k else str(k + 2)],
               "Pensa alla tabellina del %d: %d %s %d = %d, quindi %d %s %d = <b>%d</b>." % (b, b, FOIS, k, n, n, DIV, b, k))


def s2_fatti():
    return fatto()


def s2_inversa():
    b, k = R.randint(2, 9), R.randint(2, 9)
    n = b * k
    return mcq("%d %s %d = %d. Quale divisione è giusta?" % (b, FOIS, k, n), "%d %s %d = %d" % (n, DIV, b, k),
               ["%d %s %d = %d" % (n, DIV, b, k + 1), "%d %s %d = %d" % (b, DIV, k, n), "%d %s %d = %d" % (n, DIV, n, b)],
               "La divisione è l’operazione inversa della moltiplicazione: <b>%d %s %d = %d</b>." % (n, DIV, b, k))


def s3_resto():
    b = R.randint(2, 9)
    k = R.randint(2, 9)
    r = R.randint(1, b - 1) if b > 2 else 1
    n = b * k + r
    ans = "%d con resto %d" % (k, r)
    return mcq("Quanto fa %d %s %d?" % (n, DIV, b), ans,
               ["%d con resto %d" % (k - 1, r + b), "%d con resto %d" % (k + 1, r), "%d con resto %d" % (k, r + 1) if r + 1 < b else "%d con resto %d" % (k, 0), "%d" % (k + 1)],
               "Il multiplo di %d più vicino senza superare %d è %d = %d %s %d. Avanzano %d − %d = %d. <b>%s</b> (il resto è sempre minore di %d)." % (b, n, b * k, b, FOIS, k, n, b * k, r, ans, b))


def s3_pari():
    n = R.randint(11, 99)
    ok = n % 2 == 0
    return mcq("%d è un numero pari o dispari?" % n, "pari" if ok else "dispari",
               ["dispari" if ok else "pari", "né pari né dispari", "pari e dispari"],
               "%d %s 2 = %d %s: il numero è <b>%s</b>. Basta guardare la cifra delle unità (%d)." % (n, DIV, n // 2, "senza resto" if ok else "con resto 1", "pari" if ok else "dispari", n % 10))


def s4_colonna():
    b = R.randint(2, 9)
    k = R.randint(11, 99 if b < 5 else 49)
    r = R.choice([0, 0, R.randint(0, b - 1)])
    n = b * k + r
    if n > 999 or n < 20:
        return None
    ans = num(k) if r == 0 else "%s con resto %d" % (num(k), r)
    w = [num(k + 1), num(k - 1), num(k * 10) if k * 10 < 1000 else None, "%s con resto %d" % (num(k - 1), r + b) if r + b < 10 else None, num(n // b + 10)]
    if r:
        w = [num(k)] + ["%s con resto %d" % (num(k + 1), r), "%s con resto %d" % (num(k), b + r) if b + r < 20 else None] + w
    step = "Dividi una cifra alla volta, partendo da sinistra: quante volte %d sta in ogni parte?" % b
    return mcq("Esegui: %s" % q_div(n, b), ans, w,
               "%s %s %d = <b>%s</b>. Prova: %s %s %d%s = %s." % (step + " " + num(n), DIV, b, ans, num(k), FOIS, b, (" + %d" % r) if r else "", num(n)))


def s4_prova():
    b, k = R.randint(3, 9), R.randint(12, 60)
    r = R.randint(1, b - 1)
    n = b * k + r
    if n > 999:
        return None
    return mcq("%s %s %d = %d con resto %d. Come si fa la prova?" % (num(n), DIV, b, k, r), "%d %s %d + %d = %s" % (k, FOIS, b, r, num(n)),
               ["%d %s %d − %d = %s" % (k, FOIS, b, r, num(k * b - r)), "%d + %d + %d = %d" % (k, b, r, k + b + r), "%d %s %d = %s" % (k, FOIS, r, num(k * r))],
               "Quoziente per divisore, più il resto, dà il dividendo: <b>%d %s %d + %d = %s</b>." % (k, FOIS, b, r, num(n)))


def s5_problema():
    p = K.next()
    k = R.choice(["squadre", "macchine", "scatole", "pagine", "avanza", "settimane"])
    if k == "squadre":
        b, q = R.randint(3, 6), R.randint(3, 8)
        n = b * q
        return mcq("Nella classe ci sono %d bambini. La maestra fa squadre da %d. Quante squadre forma?" % (n, b), str(q), [str(n - b), str(q + 1), str(n * b)],
                   "%d %s %d = <b>%d</b> squadre." % (n, DIV, b, q))
    if k == "macchine":
        b = 4
        q, r = R.randint(3, 9), R.randint(1, 3)
        n = b * q + r
        return mcq("%d persone vanno in gita. In ogni automobile salgono 4 persone. Quante automobili servono?" % n, str(q + 1), [str(q), str(r), str(q + r)],
                   "%d %s 4 = %d con resto %d: le %d persone che avanzano hanno bisogno di un’altra automobile, quindi servono <b>%d</b> automobili." % (n, DIV, q, r, r, q + 1))
    if k == "scatole":
        b, q = R.choice([6, 8, 9]), R.randint(11, 40)
        n = b * q
        if n > 999:
            return None
        return mcq("Una pasticceria ha %s pasticcini e li mette in vassoi da %d. Quanti vassoi riempie?" % (num(n), b), num(q), [num(q + 1), num(q - 1), num(n - b), num(q * 10) if q * 10 < 1000 else None],
                   "%s %s %d = <b>%s</b> vassoi." % (num(n), DIV, b, num(q)))
    if k == "pagine":
        b, q = R.randint(3, 7), R.randint(12, 30)
        n = b * q
        return mcq("%s deve leggere %d pagine in %d giorni, lo stesso numero ogni giorno. Quante pagine al giorno?" % (p[0], n, b), str(q), [str(q + 1), str(n - b), str(q - 2)],
                   "%d %s %d = <b>%d</b> pagine al giorno." % (n, DIV, b, q))
    if k == "avanza":
        b = R.randint(3, 8)
        q, r = R.randint(3, 9), R.randint(1, b - 1)
        n = b * q + r
        return mcq("La nonna ha %d biscotti e li divide tra %d nipoti in parti uguali. Quanti biscotti avanzano?" % (n, b), str(r), [str(q), str(b - r) if b - r != r else str(r + 1), "0"],
                   "%d %s %d = %d con resto %d: ogni nipote ne riceve %d e ne avanzano <b>%d</b>." % (n, DIV, b, q, r, q, r))
    q = R.randint(2, 9)
    n = 7 * q
    return mcq("Quante settimane ci sono in %d giorni?" % n, str(q), [str(q + 1), str(n - 7), str(n * 7)],
               "Una settimana ha 7 giorni: %d %s 7 = <b>%d</b> settimane." % (n, DIV, q))


def main():
    seen = set()
    sets = [
        ("Dividere in parti uguali", mix(R, seen, [(s1_gruppi, 10), (s1_ripartizione, 10)])),
        ("Divisioni e tabelline", mix(R, seen, [(s2_fatti, 14), (s2_inversa, 6)])),
        ("La divisione con il resto", mix(R, seen, [(s3_resto, 14), (s3_pari, 6)])),
        ("Divisioni con numeri più grandi e prova", mix(R, seen, [(s4_colonna, 14), (s4_prova, 6)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dividere vuol dire fare <b>parti uguali</b> (ripartizione) oppure contare <b>quanti gruppi</b> si possono fare (contenenza).",
         "La divisione è l’inversa della moltiplicazione: se 4 %s 6 = 24, allora 24 %s 4 = 6." % (FOIS, DIV),
         "Quando non si può dividere esattamente, rimane un <b>resto</b>. Il resto è sempre <b>minore del divisore</b>.",
         "Prova: quoziente %s divisore + resto = dividendo." % FOIS],
        [("23 %s 5" % DIV, ["5 %s 4 = 20, 5 %s 5 = 25 è troppo" % (FOIS, FOIS), "23 − 20 = 3"], "4 con resto 3"),
         ("84 %s 4" % DIV, ["8 decine %s 4 = 2 decine" % DIV, "4 unità %s 4 = 1 unità" % DIV], "21")],
        [["23 %s 5 = 3 con resto 8" % DIV, "Il resto deve essere minore di 5: 4 con resto 3."],
         ["Confondere dividendo e divisore: 4 %s 24" % DIV, "Il numero da dividere (dividendo) si scrive per primo: 24 %s 4." % DIV],
         ["Nei problemi dimenticare il resto", "Chiediti che cosa succede a ciò che avanza: a volte serve un gruppo in più."]])
    faq = [("Che simbolo si usa per la divisione?", "In Italia si usano i due punti: 24 : 4 = 6. Il quoziente è il risultato."),
           ("Perché il resto deve essere più piccolo del divisore?", "Se fosse uguale o più grande, potresti fare ancora un gruppo.")]
    make_unit(R, "divisioni", "N",
              "Eseguire divisioni con i numeri naturali come operazione inversa della moltiplicazione, in situazioni di ripartizione e di contenenza; riconoscere il resto; risolvere problemi di divisione",
              "Le divisioni: in parti uguali e con il resto", "Divisioni",
              "Schede di matematica per la classe terza sulle divisioni: ripartizione e contenenza, divisioni e tabelline, divisione con il resto, prova e problemi. 100 esercizi con soluzioni.",
              "La divisione è l’inversa della moltiplicazione.", "Il resto è sempre minore del divisore.",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
