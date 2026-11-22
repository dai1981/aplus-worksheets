# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Divisioni con due cifre al divisore (Numeri)
  python3 tools/gen_it_matematica_c5_divisioni_con_due_cifre_al_divisore.py
Stimare il quoziente (quante volte il divisore sta nel dividendo), divisioni con 2 cifre al divisore con e senza
resto, quante cifre ha il quoziente, prova, divisioni per 10, 100 e multipli di 10, problemi.
Errori: resto maggiore del divisore, dimenticare lo 0 nel quoziente (2 436 : 12 = 23), stima troppo grande.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, DIV

R = random.Random(70507)
G = "classe-quinta"
K = Kids(R)


def res(q, r):
    return num(q) if r == 0 else "%s con resto %s" % (num(q), num(r))


def task(lo, hi, d_lo=11, d_hi=49, rest=True):
    d = R.randint(d_lo, d_hi)
    q = R.randint(lo, hi)
    r = R.randint(1, d - 1) if rest and R.random() < 0.6 else 0
    n = d * q + r
    w = [res(q - 1, r + d), res(q + 1, r), res(q * 10, r) if q < 100 else res(q // 10, r)]
    s = str(q)
    if "0" in s:
        w.insert(0, res(int(s.replace("0", "", 1)), r))
    if r:
        w.append(num(q))
    return mcq("Esegui: %s %s %d" % (num(n), DIV, d), res(q, r), w,
               "Prendi a sinistra tante cifre quante bastano per contenere %d e stima quante volte ci sta. %s %s %d = <b>%s</b>. Prova: %s %s %d%s = %s." % (
                   d, num(n), DIV, d, res(q, r), num(q), FOIS, d, " + %d" % r if r else "", num(n)))


def s1_stima():
    d = R.randint(12, 89)
    k = R.randint(2, 9)
    n = d * k + R.randint(0, d - 1)
    return mcq("Quante volte il %d sta nel %d?" % (d, n), str(k), [str(k + 1), str(k - 1), str(k + 2), str(n // ((d + 9) // 10 * 10 - 10)) if n // ((d + 9) // 10 * 10 - 10) not in (k, k + 1, k - 1, k + 2) else str(k - 2)],
               "Pensa %d ≈ %d e %d ≈ %d: circa %d volte. Controlla: %d %s %d = %d e %d %s %d = %d è troppo. Ci sta <b>%d</b> volte." % (
                   d, (d + 5) // 10 * 10, n, (n + 5) // 10 * 10, k, d, FOIS, k, d * k, d, FOIS, k + 1, d * (k + 1), k))


def s1_base():
    return task(2, 9, 12, 49)


def s2():
    return task(11, 99, 12, 49)


def s3():
    return task(101, 999, 12, 79) if R.random() < 0.6 else task(101, 909, 12, 49, rest=False)


def s4_cifre():
    d = R.randint(12, 89)
    n = R.randint(d * 10, d * 999)
    q = n // d
    nc = len(str(q))
    return mcq("Senza fare il calcolo: quante cifre avrà il quoziente di %s %s %d?" % (num(n), DIV, d), str(nc), [str(nc + 1), str(nc - 1) if nc > 1 else "4", str(len(str(n)))],
               "Il primo gruppo che contiene %d è %s: da lì il quoziente ha <b>%d</b> cifre (%s %s %d = %s)." % (d, str(n)[:len(str(n)) - nc + 1], nc, num(n), DIV, d, num(q)))


def s4_dieci():
    k = R.choice([10, 20, 30, 40, 50, 100])
    q = R.randint(3, 90)
    n = k * q
    return mcq("Calcola a mente: %s %s %d" % (num(n), DIV, k), num(q), [num(q * 10), num(n // 10) if k != 10 else num(q + 10), num(n // 1000) if n >= 1000 and k == 100 else num(q + 1), num(q + 1)],
               "%s %s %d: togli uno zero a tutti e due%s. <b>%s</b>." % (num(n), DIV, k, "" if k in (10, 100) else " e poi dividi per %d" % (k // 10), num(q)))


def s4_prova():
    d, q = R.randint(12, 49), R.randint(12, 99)
    r = R.randint(1, d - 1)
    n = d * q + r
    return mcq("%s %s %d = %d con resto %d. Quale calcolo è la prova?" % (num(n), DIV, d, q, r), "%d %s %d + %d = %s" % (q, FOIS, d, r, num(n)),
               ["%d %s %d − %d = %s" % (q, FOIS, d, r, num(d * q - r)), "%d %s %d + %d = %s" % (q, FOIS, r, d, num(q * r + d)), "%d + %d + %d = %d" % (q, d, r, q + d + r)],
               "Quoziente %s divisore + resto = dividendo: <b>%d %s %d + %d = %s</b>." % (FOIS, q, FOIS, d, r, num(n)))


def s5():
    p = K.next()
    k = R.choice(["pullman", "scatole", "rate", "squadre", "pagine", "uova"])
    if k == "pullman":
        c = R.choice([48, 52, 54, 56])
        n = c * R.randint(3, 8) + R.randint(1, c - 1)
        q, r = divmod(n, c)
        return mcq("Alla gita partecipano %s persone. Ogni pullman ha %d posti. Quanti pullman servono?" % (num(n), c), str(q + 1), [str(q), str(r), str(q + 2)],
                   "%s %s %d = %d con resto %d: per le %d persone in più serve un altro pullman. Servono <b>%d</b> pullman." % (num(n), DIV, c, q, r, r, q + 1))
    if k == "scatole":
        c = R.choice([12, 15, 24, 36])
        n = c * R.randint(15, 80)
        return mcq("Una fabbrica ha %s biscotti e li mette in scatole da %d. Quante scatole riempie?" % (num(n), c), num(n // c), [num(n // c + 1), num(n // c * 10), num(n - c)],
                   "%s %s %d = <b>%s</b>." % (num(n), DIV, c, num(n // c)))
    if k == "rate":
        m = R.choice([12, 18, 24, 36])
        r_ = R.randint(15, 60)
        tot = m * r_
        return mcq("Un computer costa %s € e si paga in %d rate uguali. Quanto costa ogni rata?" % (num(tot), m), "%d €" % r_, ["%d €" % (r_ + 1), "%d €" % (r_ * 10), "%s €" % num(tot - m)],
                   "%s %s %d = <b>%d €</b>." % (num(tot), DIV, m, r_))
    if k == "squadre":
        s = R.choice([11, 12, 15])
        n = s * R.randint(8, 20) + R.randint(1, s - 1)
        q, r = divmod(n, s)
        return mcq("A un torneo si iscrivono %d ragazzi. Si formano squadre da %d. Quanti ragazzi restano senza squadra?" % (n, s), str(r), [str(q), str(s - r), str(r + 1)],
                   "%d %s %d = %d con resto %d: restano <b>%d</b> ragazzi." % (n, DIV, s, q, r, r))
    if k == "pagine":
        g = R.choice([14, 21, 28, 30])
        pp = R.randint(12, 35)
        return mcq("%s deve leggere un libro di %d pagine in %d giorni, ogni giorno lo stesso numero. Quante pagine al giorno?" % (p[0], g * pp, g), str(pp),
                   [str(pp + 1), str(pp * 10), str(g * pp - g)], "%d %s %d = <b>%d</b> pagine." % (g * pp, DIV, g, pp))
    c = 12
    n = c * R.randint(20, 90)
    return mcq("Un allevamento raccoglie %s uova e le confeziona in scatole da una dozzina. Quante scatole?" % num(n), num(n // c), [num(n // 6), num(n // c + 1), num(n // 10)],
               "Una dozzina = 12. %s %s 12 = <b>%s</b>." % (num(n), DIV, num(n // c)))


def main():
    seen = set()
    sets = [
        ("Stimare il quoziente", mix(R, seen, [(s1_stima, 10), (s1_base, 10)])),
        ("Quoziente di due cifre", mix(R, seen, [(s2, 20)])),
        ("Quoziente di tre cifre", mix(R, seen, [(s3, 20)])),
        ("Cifre del quoziente, calcolo mentale e prova", mix(R, seen, [(s4_cifre, 7), (s4_dieci, 7), (s4_prova, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Prendi a sinistra del dividendo tante cifre quante servono per contenere il divisore.",
         "<b>Stima</b> quante volte ci sta: arrotonda il divisore alla decina (23 ≈ 20) e prova. Se il prodotto supera, prova con un numero più piccolo.",
         "Moltiplica, sottrai, abbassa la cifra successiva e ricomincia. Se il divisore non ci sta, scrivi <b>0</b> nel quoziente.",
         "Il resto deve essere minore del divisore. Prova: quoziente %s divisore + resto = dividendo." % FOIS],
        [("2436 %s 12" % DIV, ["24 %s 12 = 2" % DIV, "abbasso 3: 3 %s 12 = 0" % DIV, "abbasso 6: 36 %s 12 = 3" % DIV], "203")],
        [["Resto più grande del divisore", "Se il resto è uguale o più grande, il divisore ci stava una volta in più."],
         ["Dimenticare lo 0: 2436 %s 12 = 23" % DIV, "Ogni volta che abbassi una cifra scrivi una cifra nel quoziente, anche 0."],
         ["Stima troppo grande", "Se il prodotto supera il numero, prova con una cifra più piccola."]])
    faq = [("Come si stima quante volte ci sta il divisore?", "Si arrotondano i numeri: 157 : 23 è circa 160 : 20 = 8. Poi si controlla: 23 × 7 = 161 è troppo, quindi 6."),
           ("Perché a volte nel quoziente c’è uno 0?", "Quando, abbassata una cifra, il numero è più piccolo del divisore: quella cifra del quoziente vale 0.")]
    make_unit(R, "divisioni-con-due-cifre-al-divisore", "N",
              "Eseguire la divisione con resto fra numeri naturali; individuare multipli e divisori; stimare il risultato di una operazione",
              "Le divisioni con due cifre al divisore", "Divisioni con due cifre al divisore",
              "Schede di matematica per la classe quinta sulle divisioni con due cifre al divisore: stimare il quoziente, divisioni con e senza resto, zeri nel quoziente, prova e problemi. 100 esercizi con soluzioni.",
              "Stima, moltiplica, sottrai, abbassa.", "Il resto è sempre minore del divisore.",
              body, faq, sets, 7, grade=G)


if __name__ == "__main__":
    main()
