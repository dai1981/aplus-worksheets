# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: La divisione (Numeri)
  python3 tools/gen_it_matematica_c4_divisioni.py
Divisioni in colonna con una cifra al divisore (dividendo di tre e quattro cifre, zeri nel quoziente, resto),
prime divisioni con due cifre al divisore, : 10, 100, 1000, proprietà invariantiva, prova, problemi con il resto.
Errori: dimenticare lo 0 nel quoziente, resto maggiore del divisore, ignorare il resto nei problemi.
"""
import random
from it_common import mcq, num, pl, lesson, make_unit, mix, Kids, FOIS, DIV, table
import gen_it_matematica_c5_divisioni_con_due_cifre_al_divisore as D5

R = random.Random(70404)
G = "classe-quarta"
K = Kids(R)
res = D5.res


def s1():
    return D5.task(21, 99, 2, 9) if R.random() < 0.5 else D5.task(101, 499, 2, 9)


def s2_zero():
    d = R.randint(2, 9)
    q = R.choice([R.randint(1, 9) * 100 + R.randint(1, 9), R.randint(1, 9) * 1000 + R.randint(1, 9) * 10 + R.randint(0, 9), R.randint(1, 9) * 10 ** 3 + R.randint(1, 9) * 100 + R.randint(1, 9)])
    if "0" not in str(q):
        return None
    r = R.randint(0, d - 1)
    n = d * q + r
    return mcq("Esegui: %s %s %d" % (num(n), DIV, d), res(q, r), [res(int(str(q).replace("0", "", 1)), r), res(q + 10, r), res(q, r + d) if r + d < 2 * d else res(q - 1, r + d), res(q * 10, r)],
               "Quando un gruppo è più piccolo del divisore scrivi <b>0</b> nel quoziente e abbassa la cifra dopo. %s %s %d = <b>%s</b>." % (num(n), DIV, d, res(q, r)))


def s2_grande():
    return D5.task(1001, 4999, 2, 9) if R.random() < 0.5 else D5.task(1001, 9999, 3, 9, rest=False)


def s3_due():
    return D5.task(2, 9, 12, 39) if R.random() < 0.6 else D5.task(11, 40, 12, 25)


def s4_dieci():
    k = R.choice([10, 100, 1000])
    q = R.randint(2, 99) * R.choice([1, 1, 10])
    n = q * k
    if n >= 10 ** 6:
        return None
    w2 = n // (k // 10) if k > 10 else (q + 10)
    return mcq("Calcola: %s %s %s" % (num(n), DIV, num(k)), num(q), [num(q * 10), num(w2), num(q + 1), num(q // 10) if q % 10 == 0 else None],
               "Per %s %s togli %d zeri a destra: <b>%s</b>." % (DIV, num(k), len(str(k)) - 1, num(q)))


def s4_invariantiva():
    q = R.randint(3, 25)
    d = R.choice([20, 30, 40, 50, 60, 200, 300])
    n = q * d
    z = 2 if d >= 100 else 1
    return mcq("Con la proprietà invariantiva, %s %s %d è uguale a…" % (num(n), DIV, d), "%s %s %d" % (num(n // 10 ** z), DIV, d // 10 ** z),
               ["%s %s %d" % (num(n // 10 ** z), DIV, d), "%s %s %d" % (num(n), DIV, d // 10 ** z), "%s %s %d" % (num(n * 10), DIV, d // 10)],
               "Se dividi dividendo e divisore per lo stesso numero il quoziente non cambia: %s %s %d = <b>%s</b>." % (num(n // 10 ** z), DIV, d // 10 ** z, num(q)))


def s4_prova():
    if R.random() < 0.5:
        d, q = R.randint(3, 9), R.randint(102, 999)
        r = R.randint(1, d - 1)
        n = d * q + r
        return mcq("%s %s %d = %d con resto %d. Quale calcolo è la prova?" % (num(n), DIV, d, q, r), "%d %s %d + %d = %s" % (q, FOIS, d, r, num(n)),
                   ["%d %s %d − %d = %s" % (q, FOIS, d, r, num(d * q - r)), "%d %s %d + %d = %s" % (q, FOIS, r, d, num(q * r + d)), "%d + %d + %d = %d" % (q, d, r, q + d + r)],
                   "Quoziente %s divisore + resto = dividendo: <b>%d %s %d + %d = %s</b>." % (FOIS, q, FOIS, d, r, num(n)))
    d = R.randint(3, 9)
    n = R.randint(30, 400)
    q, r = divmod(n, d)
    return mcq("In una divisione per %d, quale resto <b>non</b> è possibile?" % d, str(d + R.randint(0, 3)), [str(x) for x in R.sample(range(0, d), 3)],
               "Il resto è sempre <b>più piccolo del divisore</b>: per %d può essere da 0 a %d." % (d, d - 1))


def s5():
    p = K.next()
    k = R.choice(["torte", "posti", "caramelle", "giorni", "auto", "costo", "nastro", "fila"])
    if k == "torte":
        d = R.choice([6, 8])
        n = d * R.randint(12, 60) + R.randint(1, d - 1)
        q, r = divmod(n, d)
        return mcq("Un pasticciere ha %d pasticcini. Li mette in vassoi da %d. Quanti vassoi pieni prepara? Quanti pasticcini avanzano?" % (n, d), "%d vassoi, avanzano %d" % (q, r),
                   ["%d vassoi, avanzano %d" % (q + 1, 0), "%d vassoi, avanzano %d" % (q, d - r), "%d vassoi, avanzano %d" % (r, q)],
                   "%d %s %d = %d con resto %d: <b>%d vassoi</b> pieni e <b>%d</b> pasticcini avanzati." % (n, DIV, d, q, r, q, r))
    if k == "posti":
        d = R.choice([4, 5, 6])
        n = d * R.randint(10, 40) + R.randint(1, d - 1)
        q, r = divmod(n, d)
        return mcq("%d bambini vanno in gita su auto da %d posti per i bambini. Quante auto servono, al minimo?" % (n, d), str(q + 1), [str(q), str(r), str(q + 2)],
                   "%d %s %d = %d con resto %d: per i %d bambini che restano serve un’altra auto. <b>%d</b> auto." % (n, DIV, d, q, r, r, q + 1))
    if k == "caramelle":
        d = R.randint(3, 9)
        q = R.randint(25, 130)
        return mcq("%s divide %d caramelle in parti uguali tra %d amici. Quante caramelle a ciascuno?" % (p[0], d * q, d), str(q),
                   [str(q + 1), str(d * q - d), str(q * 10 if q < 100 else q // 10)], "%d %s %d = <b>%d</b>." % (d * q, DIV, d, q))
    if k == "giorni":
        n = R.randint(40, 365)
        q, r = divmod(n, 7)
        if r == 0:
            return None
        f = lambda a, b: "%s e %s" % (pl(a, "settimana", "settimane"), pl(b, "giorno", "giorni"))
        return mcq("Quante settimane complete ci sono in %d giorni? Quanti giorni restano?" % n, f(q, r),
                   [f(q + 1, 0), f(q, 7 - r) if 7 - r != r else f(q - 1, r + 7), f(n // 10, n % 10)],
                   "Una settimana = 7 giorni: %d %s 7 = %d con resto %d." % (n, DIV, q, r))
    if k == "auto":
        d = R.choice([4, 5, 6, 8])
        q = R.randint(120, 950)
        n = d * q
        return mcq("Un’auto consuma %s litri di benzina in %d mesi, sempre la stessa quantità. Quanti litri al mese?" % (num(n), d), num(q),
                   [num(q + 10), num(n - d), num(q * 10)], "%s %s %d = <b>%s</b> litri." % (num(n), DIV, d, num(q)))
    if k == "costo":
        d = R.choice([12, 15, 20, 24, 25])
        q = R.randint(8, 40)
        return mcq("La classe spende %s € per %d biglietti del museo, tutti dello stesso prezzo. Quanto costa un biglietto?" % (num(d * q), d), "%d €" % q,
                   ["%d €" % (q + 1), "%d €" % (q * 10), "%s €" % num(d * q - d)], "%s %s %d = <b>%d €</b>." % (num(d * q), DIV, d, q))
    if k == "nastro":
        d = R.choice([3, 4, 5, 6])
        q = R.randint(15, 95)
        return mcq("Un nastro lungo %d cm si taglia in %d pezzi uguali. Quanto è lungo ogni pezzo?" % (d * q, d), "%d cm" % q,
                   ["%d cm" % (q + 1), "%d cm" % (d * q - d), "%d cm" % (q * d // 10 if q * d // 10 != q else q + 10)], "%d %s %d = <b>%d cm</b>." % (d * q, DIV, d, q))
    d = R.randint(12, 25)
    q = R.randint(5, 18)
    return mcq("In palestra ci sono %d sedie da mettere in file da %d. Quante file si formano?" % (d * q, d), str(q),
               [str(q + 1), str(d * q - d), str(d)], "%d %s %d = <b>%d</b> file." % (d * q, DIV, d, q))


def main():
    D5.R = R
    seen = set()
    sets = [
        ("Una cifra al divisore", mix(R, seen, [(s1, 20)])),
        ("Lo zero nel quoziente", mix(R, seen, [(s2_zero, 20)])),
        ("Dividendo di quattro cifre", mix(R, seen, [(s2_grande, 12), (s4_prova, 8)])),
        ("Due cifre al divisore, : 10, 100, 1000", mix(R, seen, [(s3_due, 8), (s4_dieci, 6), (s4_invariantiva, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Nella divisione in colonna prendi a sinistra la cifra (o le cifre) che contengono il divisore, trovi quante volte ci sta, moltiplichi, sottrai e <b>abbassi</b> la cifra dopo.",
         "Se il gruppo è più piccolo del divisore, scrivi <b>0</b> nel quoziente e abbassi un’altra cifra.",
         "Il <b>resto</b> è sempre più piccolo del divisore. Prova: quoziente × divisore + resto = dividendo.",
         "Per : 10, 100, 1000 togli 1, 2, 3 zeri. Proprietà invariantiva: 1200 : 40 = 120 : 4."],
        [("856 : 4", ["8 : 4 = 2", "5 : 4 = 1, resto 1 → 16", "16 : 4 = 4"], "214")],
        [["Dimenticare lo 0 nel quoziente", "Se abbassi una cifra e il gruppo non basta, scrivi 0."],
         ["Resto più grande del divisore", "Il divisore ci stava ancora una volta: aumenta il quoziente."],
         ["Ignorare il resto nei problemi", "Leggi la domanda: a volte serve un pullman (o una scatola) in più."]],
        table(["Termine", "In 856 : 4 = 214"], [["dividendo", "856"], ["divisore", "4"], ["quoziente", "214"], ["resto", "0"]]))
    faq = [("Che cosa vuol dire «abbassare» una cifra?", "Scrivere accanto al resto la cifra successiva del dividendo, per formare un nuovo numero da dividere."),
           ("Quando il resto conta nei problemi?", "Se servono contenitori, pullman o vassoi, gli oggetti che avanzano ne richiedono uno in più.")]
    make_unit(R, "divisioni", "N",
              "Eseguire divisioni con i numeri naturali, in colonna e a mente, con il resto e con una o due cifre al divisore; utilizzare la proprietà invariantiva",
              "La divisione in colonna con il resto", "Divisioni",
              "Schede di matematica per la classe quarta sulla divisione: in colonna con una cifra al divisore, lo zero nel quoziente, due cifre al divisore, : 10, 100, 1000, prova e problemi con il resto. 100 esercizi con soluzioni.",
              "Il resto è sempre più piccolo del divisore.", "Prova: quoziente × divisore + resto = dividendo.",
              body, faq, sets, 4, grade=G)


if __name__ == "__main__":
    main()
