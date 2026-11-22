# -*- coding: utf-8 -*-
"""
Italia Matematica classe terza: I numeri decimali (Numeri)
  python3 tools/gen_it_matematica_c3_numeri_decimali.py
Decimi e centesimi, dalla frazione decimale al numero con la virgola, parte intera e parte decimale, tabella
(da u, d c), confrontare, addizioni e sottrazioni con soldi e misure.
Errori: 3/10 = 0,03, credere che 0,25 &gt; 0,3 perché 25 &gt; 3, incolonnare senza allineare le virgole.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, fr, striscia, eur, dec, NB

R = random.Random(70311)
K = Kids(R)


def d1(n):
    """decimi: 23 → 2,3"""
    return dec(n / 10.0, 1)


def d2(n):
    return dec(n / 100.0, 2)


def tabella(n):
    s = "%.2f" % (n / 100.0)
    ip, fp_ = s.split(".")
    ip = ip.rjust(2, " ")
    head = ["da", "u", "d", "c"]
    cells = [ip[0], ip[1], fp_[0], fp_[1]]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s%s</td>" % (c if c != " " else "", "," if i == 1 else "") for i, c in enumerate(cells))))


def s1_decimi():
    k = R.randint(1, 9)
    if R.random() < 0.5:
        return mcq(striscia(10, k) + "L’intero è diviso in 10 parti. Quale numero decimale indica la parte colorata?", d1(k),
                   [d2(k), str(k), d1(10 - k) if k != 5 else d1(k + 1), "%d,%d" % (k, k)],
                   "%d parti su 10 sono %s, cioè <b>%s</b> (%s decimi)." % (k, fr(k, 10), d1(k), k))
    return mcq("Come si scrive %s con la virgola?" % fr(k, 10), d1(k), [d2(k), str(k) + ",0", "%d,%d" % (10, k)],
               "%s = %d decimi = <b>%s</b>." % (fr(k, 10), k, d1(k)))


def s1_centesimi():
    k = R.randint(1, 99)
    if k % 10 == 0:
        return None
    return mcq("Come si scrive %s con la virgola?" % fr(k, 100), d2(k), [d1(k) if k < 100 else None, "%d,%d" % (k, 0), d2(k * 10) if k < 10 else d2(k + 10), "0,%d" % k if k < 10 else d2(k - 10)],
               "%s = %d centesimi = <b>%s</b>: la cifra dei centesimi è il secondo posto dopo la virgola." % (fr(k, 100), k, d2(k)))


def s2_parti():
    n = R.randint(11, 999)
    if n % 10 == 0:
        return None
    v = d1(n) if R.random() < 0.6 else d2(n)
    ip, fp_ = v.split(",")
    k = R.choice(["intera", "decimale"])
    if k == "intera":
        return mcq("Nel numero %s, qual è la parte intera?" % v, ip, [fp_, v.replace(",", ""), str(int(ip) + 1)],
                   "La parte intera è prima della virgola: <b>%s</b>." % ip)
    return mcq("Nel numero %s, qual è la parte decimale?" % v, fp_, [ip, v.replace(",", ""), fp_[::-1] if len(fp_) > 1 and fp_[::-1] != fp_ else str(int(fp_) + 1)],
               "La parte decimale è dopo la virgola: <b>%s</b>." % fp_)


def s2_tabella():
    n = R.randint(101, 9999)
    if n % 10 == 0:
        return None
    v = d2(n)
    w = [d1(n) if n < 1000 else d2(n // 10), str(n), d2(int(str(n)[::-1])) if str(n)[::-1][0] != "0" else d2(n + 1), d2(n + 10)]
    return mcq(tabella(n) + "Quale numero è scritto nella tabella?", v, w,
               "da e u sono la parte intera, d (decimi) e c (centesimi) la parte decimale: <b>%s</b>." % v)


def s2_cifra():
    n = R.randint(101, 999)
    v = d2(n)
    ds = v.replace(",", "")
    a, b, c = ds[-3], ds[-2], ds[-1]
    k = R.choice(["d", "c"])
    if k == "d":
        return mcq("Nel numero %s, qual è la cifra dei decimi?" % v, b, [c, a, str((int(b) + 1) % 10)] if len({a, b, c}) == 3 else [c, a, str((int(b) + 1) % 10), str((int(b) + 2) % 10)],
                   "I decimi sono il primo posto dopo la virgola: <b>%s</b>." % b)
    return mcq("Nel numero %s, qual è la cifra dei centesimi?" % v, c, [b, a, str((int(c) + 1) % 10), str((int(c) + 2) % 10)],
               "I centesimi sono il secondo posto dopo la virgola: <b>%s</b>." % c)


def s3_confronta():
    k = R.choice(["d1", "mix", "int"])
    if k == "d1":
        a, b = R.sample(range(1, 99), 2)
        A, B = d1(a), d1(b)
        g = max(a, b)
    elif k == "mix":
        x = R.randint(1, 9)
        y = R.randint(11, 99)
        if y // 10 == x or y % 10 == 0:
            return None
        A, B = "0,%d" % x, d2(y)
        g = None
        big = A if x * 10 > y else B
        small = B if big == A else A
        return mcq("Qual è il numero più grande: %s o %s?" % (A, B), big, [small, "sono uguali", "non si può sapere"],
                   "Confronta prima i decimi: %s e %s. %s è più grande: <b>%s</b> (0,%d = 0,%d0)." % (A[2], B[2], big, big, x, x))
    else:
        a, b = R.randint(10, 99), R.randint(10, 99)
        if a // 10 == b // 10:
            return None
        A, B = d1(a), d1(b)
        g = max(a, b)
    if a == b:
        return None
    gs, ss = d1(g), d1(min(a, b))
    return mcq("Qual è il numero più grande: %s o %s?" % (A, B), gs, [ss, "sono uguali", "non si può sapere"],
               "Confronta prima la parte intera, poi i decimi: <b>%s</b> &gt; %s." % (gs, ss))


def s3_ordina():
    ns = R.sample(range(1, 99), 4)
    vs = sorted(ns)
    f = lambda L: "; ".join(d1(x) for x in L)
    sh = ns[:]
    R.shuffle(sh)
    w1 = vs[::-1]
    w2 = sorted(ns, key=lambda x: (x % 10, x))
    w3 = vs[:]
    w3[0], w3[1] = w3[1], w3[0]
    return mcq("Metti in ordine crescente: %s" % f(sh), f(vs), [f(x) for x in (w1, w2, w3) if x != vs],
               "Dal più piccolo al più grande: <b>%s</b>." % f(vs))


def s4_soldi():
    a, b = R.randint(1, 9) * 100 + R.choice([10, 20, 30, 50, 60, 80]), R.randint(1, 5) * 100 + R.choice([10, 20, 40, 50, 70, 90])
    if R.random() < 0.5:
        r = a + b
        return mcq("Calcola: %s + %s" % (eur(a), eur(b)), eur(r), [eur(r + 100), eur(r - 10), eur((a // 100 + b // 100) * 100 + (a % 100 + b % 100) % 100) if (a % 100 + b % 100) >= 100 else eur(r + 10)],
                   "Somma gli euro con gli euro e i centesimi con i centesimi: <b>%s</b>." % eur(r))
    if a <= b:
        a, b = b + 100, a
    r = a - b
    return mcq("Calcola: %s − %s" % (eur(a), eur(b)), eur(r), [eur(r + 100), eur(r - 10) if r > 10 else eur(r + 20), eur(a + b), eur(r + 10)],
               "%s − %s = <b>%s</b>." % (eur(a), eur(b), eur(r)))


def s4_misure():
    a, b = R.randint(11, 79), R.randint(11, 49)
    u = R.choice(["m", "kg", "l"])
    if R.random() < 0.5:
        r = a + b
        return mcq("Calcola: %s %s + %s %s" % (d1(a), u, d1(b), u), "%s %s" % (d1(r), u),
                   ["%s %s" % (d1(r + 10), u), "%s %s" % (d2(r), u), "%s %s" % (str(r), u), "%s %s" % (d1(r - 1), u)],
                   "Incolonna le virgole: %s + %s = <b>%s %s</b>." % (d1(a), d1(b), d1(r), u))
    if a <= b:
        a, b = b, a
    if a == b:
        return None
    r = a - b
    return mcq("Calcola: %s %s − %s %s" % (d1(a), u, d1(b), u), "%s %s" % (d1(r), u),
               ["%s %s" % (d1(r + 10), u), "%s %s" % (d2(r), u), "%s %s" % (d1(a + b), u)],
               "Incolonna le virgole: %s − %s = <b>%s %s</b>." % (d1(a), d1(b), d1(r), u))


def s5_problema():
    p = K.next()
    k = R.choice(["spesa", "resto", "salto", "nastro", "acqua", "gelato"])
    if k == "spesa":
        a, b = R.randint(1, 4) * 100 + R.choice([20, 50, 80]), R.randint(1, 3) * 100 + R.choice([10, 40, 50, 90])
        r = a + b
        return mcq("%s compra un quaderno da %s e una penna da %s. Quanto spende?" % (p[0], eur(a), eur(b)), eur(r),
                   [eur(r + 100), eur(r - 10), eur(abs(a - b))], "%s + %s = <b>%s</b>." % (eur(a), eur(b), eur(r)))
    if k == "resto":
        a = R.randint(1, 4) * 100 + R.choice([20, 30, 50, 60, 80])
        r = 500 - a
        return mcq("%s compra un libro da %s e paga con 5 €. Quanto riceve di resto?" % (p[0], eur(a)), eur(r),
                   [eur(r + 100), eur(600 - a), eur(r - 10) if r > 10 else eur(r + 20)], "5 € − %s = <b>%s</b>." % (eur(a), eur(r)))
    if k == "salto":
        a, b = R.randint(15, 28), R.randint(2, 6)
        return mcq("Nel salto in lungo %s salta %s m. Al secondo salto fa %s m in più. Quanto salta la seconda volta?" % (p[0], d1(a), d1(b)), "%s m" % d1(a + b),
                   ["%s m" % d1(a - b), "%s m" % d1(a + b + 10), "%s m" % str(a + b)], "%s + %s = <b>%s m</b>." % (d1(a), d1(b), d1(a + b)))
    if k == "nastro":
        a, b = R.randint(25, 60), R.randint(5, 20)
        return mcq("Un nastro è lungo %s m. Se ne tagliano %s m. Quanti metri restano?" % (d1(a), d1(b)), "%s m" % d1(a - b),
                   ["%s m" % d1(a + b), "%s m" % d1(a - b + 10), "%s m" % d2(a - b)], "%s − %s = <b>%s m</b>." % (d1(a), d1(b), d1(a - b)))
    if k == "acqua":
        a, b = R.randint(10, 20), R.randint(3, 9)
        return mcq("Una bottiglia contiene %s l d’acqua. Se ne bevono %s l. Quanta acqua resta?" % (d1(a), d1(b)), "%s l" % d1(a - b),
                   ["%s l" % d1(a + b), "%s l" % d1(a - b - 1), "%s l" % d2(a - b)], "%s − %s = <b>%s l</b>." % (d1(a), d1(b), d1(a - b)))
    a = R.choice([150, 180, 220, 250, 280])
    b = R.choice([50, 70, 80, 120])
    return mcq("Un gelato costa %s e un succo %s. Quanto costano insieme?" % (eur(a), eur(b)), eur(a + b),
               [eur(a + b + 100), eur(a + b - 10), eur(abs(a - b))], "%s + %s = <b>%s</b>." % (eur(a), eur(b), eur(a + b)))


def main():
    seen = set()
    sets = [
        ("Decimi e centesimi", mix(R, seen, [(s1_decimi, 10), (s1_centesimi, 10)])),
        ("Parte intera e parte decimale", mix(R, seen, [(s2_parti, 8), (s2_tabella, 6), (s2_cifra, 6)])),
        ("Confrontare e ordinare", mix(R, seen, [(s3_confronta, 14), (s3_ordina, 6)])),
        ("Addizioni e sottrazioni con soldi e misure", mix(R, seen, [(s4_soldi, 10), (s4_misure, 10)])),
        ("Problemi", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Se dividi l’unità in 10 parti uguali ottieni i <b>decimi</b>: %s = 0,1. Se la dividi in 100 parti ottieni i <b>centesimi</b>: %s = 0,01." % (fr(1, 10), fr(1, 100)),
         "Nel numero 2,35 la <b>virgola</b> separa la parte intera (2) dalla parte decimale (35): 3 decimi e 5 centesimi.",
         "Per confrontare due numeri decimali guarda prima la parte intera, poi i decimi, poi i centesimi.",
         "Per sommare o sottrarre <b>incolonna le virgole</b>: 1,5 m + 2,3 m = 3,8 m. Con gli euro: i centesimi sono la parte decimale."],
        [("Scrivi %s con la virgola." % fr(7, 10), ["7 decimi"], "0,7"),
         ("Qual è più grande: 0,3 o 0,25?", ["decimi: 3 e 2", "0,3 = 0,30"], "0,3")],
        [["Scrivere %s = 0,03" % fr(3, 10), "I decimi sono il primo posto dopo la virgola: 0,3."],
         ["Pensare che 0,25 &gt; 0,3 perché 25 &gt; 3", "Confronta posto per posto: 2 decimi &lt; 3 decimi."],
         ["Incolonnare a destra 1,5 + 2,35", "Metti le virgole una sotto l’altra."]],
        tabella(235))
    faq = [("Perché in classe terza si studiano i numeri decimali?", "Perché si usano ogni giorno con i soldi (2,50 €) e con le misure (1,5 m). In terza si lavora soprattutto con decimi e centesimi."),
           ("0,5 e 0,50 sono lo stesso numero?", "Sì: 5 decimi sono uguali a 50 centesimi. Uno zero alla fine della parte decimale non cambia il valore.")]
    make_unit(R, "numeri-decimali", "N",
              "Leggere, scrivere e confrontare numeri decimali in notazione posizionale; eseguire addizioni e sottrazioni con numeri decimali in situazioni concrete (denaro, misure)",
              "I numeri decimali: decimi e centesimi", "Numeri decimali",
              "Schede di matematica per la classe terza sui numeri decimali: decimi e centesimi, frazioni decimali, parte intera e decimale, confronti, addizioni e sottrazioni con euro e misure. 100 esercizi con soluzioni.",
              "La virgola separa la parte intera dalla parte decimale.", "Decimi: primo posto dopo la virgola; centesimi: secondo.",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
