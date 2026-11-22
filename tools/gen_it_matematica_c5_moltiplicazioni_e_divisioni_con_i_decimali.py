# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Moltiplicazioni e divisioni con i decimali (Numeri)
  python3 tools/gen_it_matematica_c5_moltiplicazioni_e_divisioni_con_i_decimali.py
× e : per 10, 100, 1000 con i decimali (spostare la virgola), moltiplicare un decimale per un naturale e per un
decimale (contare le cifre decimali), dividere un decimale per un naturale, divisore decimale (proprietà
invariantiva), problemi (costo unitario, prezzo al kg).
Errori: spostare la virgola nel verso sbagliato, contare male le cifre decimali (0,3 × 0,2 = 0,6), dimenticare la virgola nel quoziente.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, eur, FOIS, DIV

R = random.Random(70506)
G = "classe-quinta"
K = Kids(R)


def D(n, p):
    """n intero con p decimali → stringa senza zeri finali"""
    neg = n < 0
    ip, fp_ = divmod(abs(n), 10 ** p)
    s = (str(fp_).rjust(p, "0") if p else "").rstrip("0")
    return ("−" if neg else "") + num(ip) + ("," + s if s else "")


def dec_of(lo, hi, p):
    v = R.randint(lo, hi)
    if v % 10 == 0:
        v += 1
    return v, p


def s1_dieci():
    n, p = dec_of(11, 9999, R.choice([1, 2, 3]))
    k = R.choice([10, 100, 1000])
    z = {10: 1, 100: 2, 1000: 3}[k]
    if R.random() < 0.5:
        r = (n * k, p)
        w = [(n, p + z), (n * k * 10, p), (n * 10, p) if k != 10 else (n * 100, p), (n * k // 10, p) if k > 10 else (n * 1000, p), (n, max(p - z, 0))]
        e = "Per %s %s la virgola si sposta di %d %s verso destra (il numero diventa più grande)." % (FOIS, num(k), z, "posto" if z == 1 else "posti")
        q = "Quanto fa %s %s %s?" % (D(n, p), FOIS, num(k))
    else:
        r = (n, p + z)
        w = [(n * k, p), (n, p + z + 1), (n, p + z - 1) if z > 1 else (n, p + 2)]
        e = "Per %s %s la virgola si sposta di %d %s verso sinistra (il numero diventa più piccolo); se mancano cifre si aggiungono zeri." % (DIV, num(k), z, "posto" if z == 1 else "posti")
        q = "Quanto fa %s %s %s?" % (D(n, p), DIV, num(k))
    return mcq(q, D(*r), [D(*x) for x in w], e + " <b>%s</b>." % D(*r))


def s2_per_naturale():
    n, p = dec_of(11, 999, R.choice([1, 2]))
    m = R.randint(2, 9)
    r = n * m
    w = [D(r, p - 1) if p > 1 else D(r, 0), D(r, p + 1), D(n * m + n, p), D(r + 10 ** p, p)]
    return mcq("Quanto fa %s %s %d?" % (D(n, p), FOIS, m), D(r, p), w,
               "Moltiplica senza virgola: %d %s %d = %s. Il fattore ha %d %s decimali: <b>%s</b>." % (n, FOIS, m, num(r), p, "cifra" if p == 1 else "cifre", D(r, p)))


def s2_per_decimale():
    a, pa = R.randint(2, 99), 1
    b, pb = R.randint(2, 99), R.choice([1, 2])
    if a % 10 == 0 or b % 10 == 0:
        return None
    r = a * b
    p = pa + pb
    sep = (a // 10) * (b // 10 ** pb)
    dp = (a % 10) * (b % 10 ** pb)
    w = [D(r, max(pa, pb)), D(r, p + 1), D(r, p - 1), "%s,%s" % (num(sep), dp) if dp else None, D(r + 10 ** p, p), D(r - 10 ** p, p) if r > 10 ** p else None]
    return mcq("Quanto fa %s %s %s?" % (D(a, pa), FOIS, D(b, pb)), D(r, p), w,
               "%d %s %d = %s. In tutto i fattori hanno %d + %d = %d cifre decimali: <b>%s</b>." % (a, FOIS, b, num(r), pa, pb, p, D(r, p)))


def s3_diviso_naturale():
    m = R.randint(2, 9)
    q = R.randint(11, 999)
    p = R.choice([1, 2])
    n = q * m
    return mcq("Quanto fa %s %s %d?" % (D(n, p), DIV, m), D(q, p), [D(q, p - 1) if p > 1 else num(q), D(q, p + 1), D(q + 10 ** (p - 1), p), D(n, p + 1)],
               "Dividi come con i naturali: %s %s %d = %s; quando «abbassi» la prima cifra decimale metti la virgola nel quoziente. <b>%s</b>." % (num(n), DIV, m, num(q), D(q, p)))


def s3_resto_zero():
    m = R.choice([2, 4, 5, 8])
    a = R.randint(3, 49)
    if a % m == 0:
        return None
    r10 = a * 1000 // m
    if a * 1000 % m:
        return None
    return mcq("Continua la divisione con i decimali: %d %s %d = ?" % (a, DIV, m), D(r10, 3), [num(a // m), "%d con resto %d" % (a // m, a % m), D(r10, 2) if r10 % 10 == 0 else D(r10 * 10, 3), D(r10, 4)],
               "Dopo le unità metti la virgola nel quoziente e aggiungi zeri al dividendo: %d,000 %s %d = <b>%s</b>." % (a, DIV, m, D(r10, 3)))


def s4_divisore_decimale():
    return _s4(R.randint(2, 9), R.randint(2, 40))


def _s4(b, q):
    a = b * q
    k = R.choice(["dd", "nd"])
    if k == "dd":
        return mcq("Quanto fa %s %s %s?" % (D(a, 1), DIV, D(b, 1)), num(q), [D(q, 1), num(q * 10), num(q * 100)],
                   "Proprietà invariantiva: moltiplica tutti e due per 10. %d %s %d = <b>%s</b>." % (a, DIV, b, num(q)))
    return mcq("Quanto fa %s %s %s?" % (num(a), DIV, D(b, 1)), num(q * 10), [num(q), D(q, 1), num(q * 100)],
               "Moltiplica tutti e due per 10: %s %s %d = <b>%s</b>." % (num(a * 10), DIV, b, num(q * 10)))


def s4_inv():
    a, b = R.randint(2, 9), R.randint(12, 99)
    k = R.choice([10, 100])
    return mcq("Quale divisione ha lo stesso risultato di %s %s %s?" % (D(b * k // 10, 2 if k == 100 else 1), DIV, D(a * k // 10, 2 if k == 100 else 1)),
               "%s %s %s" % (num(b * k // 10), DIV, num(a * k // 10)),
               ["%s %s %s" % (D(b * k // 10, 2 if k == 100 else 1), DIV, num(a * k // 10)), "%s %s %s" % (num(b * k // 10), DIV, D(a * k // 10, 2 if k == 100 else 1)), "%s %s %s" % (num(b), DIV, num(a * k))],
               "Se moltiplichi dividendo e divisore per lo stesso numero (%s), il quoziente non cambia: <b>%s %s %s</b>." % (num(k), num(b * k // 10), DIV, num(a * k // 10)))


def s5():
    p = K.next()
    k = R.choice(["kg", "litri", "unitario", "metri", "quaderni", "benzina"])
    if k == "kg":
        pr, w = R.randint(120, 690), R.choice([2, 3, 4, 5])
        return mcq("Le mele costano %s al kg. %s ne compra %d kg. Quanto spende?" % (eur(pr), p[0], w), eur(pr * w), [eur(pr + w * 100), eur(pr * w + pr), eur(pr * w // 10)],
                   "%s %s %d = <b>%s</b>." % (eur(pr), FOIS, w, eur(pr * w)))
    if k == "litri":
        n = R.choice([4, 5, 8])
        q = R.randint(11, 60) * 5
        tot = q * n
        return mcq("%s litri di succo si versano in %d brocche uguali. Quanti litri in ogni brocca?" % (D(tot, 2), n), D(q, 2) + " l",
                   [D(q, 1) + " l", D(q, 3) + " l", D(q + 100, 2) + " l"], "%s %s %d = <b>%s l</b>." % (D(tot, 2), DIV, n, D(q, 2)))
    if k == "unitario":
        n = R.randint(3, 8)
        pr = R.randint(45, 390)
        return mcq("%d quaderni costano %s. Quanto costa un quaderno?" % (n, eur(pr * n)), eur(pr), [eur(pr * n * n), eur(pr + 100), eur(pr * 10)],
                   "%s %s %d = <b>%s</b>." % (eur(pr * n), DIV, n, eur(pr)))
    if k == "metri":
        l, n = R.randint(12, 95), R.randint(3, 9)
        return mcq("Per un lavoro servono %d pezzi di filo lunghi %s m. Quanti metri di filo servono?" % (n, D(l, 2)), D(l * n, 2) + " m",
                   [D(l * n, 1) + " m", D(l * n, 3) + " m", D(l + n * 100, 2) + " m"], "%s %s %d = <b>%s m</b>." % (D(l, 2), FOIS, n, D(l * n, 2)))
    if k == "quaderni":
        pr = R.choice([125, 150, 175, 250])
        have = R.choice([10, 15, 20]) * 100
        n = have // pr
        return mcq("Un album costa %s. Quanti album si comprano al massimo con %s?" % (eur(pr), eur(have)), str(n), [str(n + 1), str(have // 100), str(n * 10)],
                   "%s %s %s = %s: al massimo <b>%d</b> album." % (eur(have), DIV, eur(pr), D(have * 100 // pr, 2), n))
    pr = R.randint(1650, 1950)
    l = R.choice([10, 20, 30])
    tot = pr * l
    return mcq("Un litro di benzina costa %s €. Quanto si spende per %d litri?" % (D(pr, 3), l), D(tot, 3) + " €",
               [D(tot, 2) + " €", D(pr * (l + 1), 3) + " €", D(tot, 4) + " €"], "%s %s %d = <b>%s €</b>." % (D(pr, 3), FOIS, l, D(tot, 3)))


def main():
    seen = set()
    sets = [
        ("Per e diviso 10, 100, 1000", mix(R, seen, [(s1_dieci, 20)])),
        ("Moltiplicare per un numero naturale", mix(R, seen, [(s2_per_naturale, 20)])),
        ("Moltiplicare due decimali", mix(R, seen, [(s2_per_decimale, 20)])),
        ("Dividere con i decimali", mix(R, seen, [(s3_diviso_naturale, 8), (s3_resto_zero, 4), (s4_divisore_decimale, 4), (s4_inv, 4)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per %s 10, 100, 1000 la virgola si sposta a <b>destra</b> di 1, 2, 3 posti; per %s 10, 100, 1000 a <b>sinistra</b>." % (FOIS, DIV),
         "Per moltiplicare due numeri decimali, moltiplica senza virgola e poi metti nel risultato <b>tante cifre decimali quante ne hanno in tutto i fattori</b>.",
         "Per dividere un decimale per un naturale, quando passi alla prima cifra decimale metti la virgola nel quoziente.",
         "Se il divisore è decimale, moltiplica dividendo e divisore per 10 o 100 (proprietà invariantiva): il quoziente non cambia."],
        [("2,4 %s 1,3" % FOIS, ["24 %s 13 = 312" % FOIS, "cifre decimali: 1 + 1 = 2"], "3,12"),
         ("7,5 %s 2,5" % DIV, ["× 10: 75 %s 25" % DIV], "3")],
        [["Spostare la virgola dalla parte sbagliata", "%s 10 rende il numero più grande: la virgola va a destra." % FOIS],
         ["0,3 %s 0,2 = 0,6" % FOIS, "3 %s 2 = 6 e le cifre decimali sono 2: 0,06." % FOIS],
         ["Dimenticare la virgola nel quoziente", "Quando abbassi la cifra dei decimi, scrivi subito la virgola."]])
    faq = [("Perché moltiplicando per un decimale minore di 1 il numero diventa più piccolo?", "Perché prendi solo una parte del numero: 8 × 0,5 è la metà di 8, cioè 4."),
           ("Che cos’è la proprietà invariantiva?", "Se moltiplichi o dividi dividendo e divisore per lo stesso numero, il quoziente non cambia: 7,5 : 2,5 = 75 : 25 = 3.")]
    make_unit(R, "moltiplicazioni-e-divisioni-con-i-decimali", "N",
              "Eseguire le quattro operazioni con sicurezza, anche con i numeri decimali; moltiplicare e dividere per 10, 100, 1000; usare la proprietà invariantiva della divisione",
              "Moltiplicazioni e divisioni con i numeri decimali", "Moltiplicazioni e divisioni con i decimali",
              "Schede di matematica per la classe quinta su moltiplicazioni e divisioni con i numeri decimali: per 10, 100, 1000, moltiplicare decimali, dividere, proprietà invariantiva e problemi. 100 esercizi con soluzioni.",
              "Nel prodotto ci sono tante cifre decimali quante nei fattori.", "Divisore decimale: moltiplica tutti e due per 10.",
              body, faq, sets, 6, grade=G)


if __name__ == "__main__":
    main()
