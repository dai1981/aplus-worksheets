# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Addizioni e sottrazioni con i decimali (Numeri)
  python3 tools/gen_it_matematica_c5_addizioni_e_sottrazioni_con_i_decimali.py
Incolonnare con la virgola sotto la virgola, aggiungere gli zeri, addizioni e sottrazioni in colonna, calcolo
mentale (complemento all’unità), proprietà, stima, problemi con euro, metri, chilogrammi e tempi.
Errori: incolonnare a destra (2,5 + 1,25 = 1,50), 5 − 1,3 = 4,3, dimenticare il cambio tra decimi e unità.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, colonna, Kids, eur

R = random.Random(70505)
G = "classe-quinta"
K = Kids(R)


def D(n, p, trim=True):
    ip, fp_ = divmod(abs(n), 10 ** p)
    s = str(fp_).rjust(p, "0") if p else ""
    if trim:
        s = s.rstrip("0")
    return ("−" if n < 0 else "") + num(ip) + ("," + s if s else "")


def rand_dec(lo, hi, p):
    """valore intero in millesimi, con p cifre decimali significative"""
    v = R.randint(lo * 10 ** p, hi * 10 ** p)
    if v % 10 == 0 and p:
        v += R.randint(1, 9)
    return v * 10 ** (3 - p)


def S(v):
    return D(v, 3)


def misalign(a, b):
    """errore: incolonnare a destra senza guardare la virgola"""
    sa, sb = S(a).replace(",", ""), S(b).replace(",", "")
    pa = len(S(a).split(",")[1]) if "," in S(a) else 0
    pb = len(S(b).split(",")[1]) if "," in S(b) else 0
    if pa == pb:
        return None
    p = max(pa, pb)
    return D(int(sa) + int(sb), p)


def col(vals, op):
    p = max(len(S(v).split(",")[1]) if "," in S(v) else 0 for v in vals)
    return colonna([D(v // 10 ** (3 - p), p, trim=False).replace(" ", "").replace(" ", "") for v in vals], op=op)


def add_task(pa, pb, lo=1, hi=99):
    a, b = rand_dec(lo, hi, pa), rand_dec(1, 60, pb)
    r = a + b
    w = [misalign(a, b), S(r + 100), S(r - 100) if r > 100 else None, S(r + 1000), S(r + 10)]
    return mcq(col([a, b], "+") + "Esegui in colonna: %s + %s" % (S(a), S(b)), S(r), [x for x in w if x],
               "Metti la virgola sotto la virgola e completa con gli zeri. %s + %s = <b>%s</b>." % (S(a), S(b), S(r)))


def sub_task(pa, pb, lo=10, hi=99):
    a, b = rand_dec(lo, hi, pa), rand_dec(1, 9, pb)
    if b >= a:
        return None
    r = a - b
    w = [S(r + 100), S(r - 100) if r > 100 else None, S(a + b), S(r + 1000)]
    sa, sb = S(a), S(b)
    return mcq(col([a, b], "−") + "Esegui in colonna: %s − %s" % (sa, sb), S(r), [x for x in w if x],
               "Metti la virgola sotto la virgola; se servono, aggiungi zeri a destra. %s − %s = <b>%s</b>." % (sa, sb, S(r)))


def s1():
    return add_task(R.choice([1, 2]), R.choice([1, 2]))


def s2():
    return add_task(R.choice([1, 2, 3]), R.choice([1, 2, 3]))


def s3():
    if R.random() < 0.35:
        a = R.randint(2, 30) * 1000
        b = rand_dec(1, a // 1000 - 1, R.choice([1, 2])) if a > 2000 else rand_dec(0, 1, 2)
        if b >= a or b <= 0:
            return None
        r = a - b
        wrong = D(a - (b // 1000) * 1000 + (b % 1000), 3)  # 5 − 1,3 = 4,3
        return mcq(col([a, b], "−") + "Esegui in colonna: %s − %s" % (S(a), S(b)), S(r), [wrong, S(r + 1000), S(a + b), S(r + 100)],
                   "Scrivi %s come %s e poi sottrai: <b>%s</b>." % (S(a), D(a // 10 ** (3 - len(S(b).split(",")[1])), len(S(b).split(",")[1]), trim=False), S(r)))
    return sub_task(R.choice([1, 2]), R.choice([1, 2, 3]))


def s4_mentale():
    k = R.choice(["compl", "compl", "piu", "stima"])
    if k == "compl":
        b = R.randint(1, 99)
        if b % 10 == 0:
            return None
        a = b * 10
        r = 1000 - a
        return mcq("Quanto manca a %s per arrivare a 1?" % S(a), S(r), [S(1000 - b), S(r + 100), S(r - 10) if r > 10 else S(r + 20), D(100 - b, 1)],
                   "%s + %s = 1. Manca <b>%s</b>." % (S(a), S(r), S(r)))
    if k == "piu":
        a = rand_dec(1, 20, 2)
        t = R.choice([100, 10, 1000])
        r = a + t
        name = {100: "un decimo", 10: "un centesimo", 1000: "un’unità"}[t]
        return mcq("Aggiungi %s a %s." % (name, S(a)), S(r), [S(a + 100 if t != 100 else 10), S(a + 1000 if t != 1000 else 100), S(a + 1)],
                   "%s + %s = <b>%s</b>." % (S(a), S(t), S(r)))
    a, b = rand_dec(3, 40, 2), rand_dec(2, 30, 2)
    ra, rb = (a + 500) // 1000, (b + 500) // 1000
    return mcq("Stima arrotondando all’unità: %s + %s fa circa…" % (S(a), S(b)), num(ra + rb), [num(ra + rb + 1), num(ra + rb - 1), num(ra + rb + 10)],
               "%s ≈ %d e %s ≈ %d: %d + %d = <b>%d</b> (esatto: %s)." % (S(a), ra, S(b), rb, ra, rb, ra + rb, S(a + b)))


def s4_tre():
    vals = [rand_dec(1, 20, R.choice([1, 2])) for _ in range(3)]
    r = sum(vals)
    return mcq("Calcola: %s" % " + ".join(S(v) for v in vals), S(r), [S(r + 100), S(r - 10) if r > 10 else S(r + 20), S(r + 1000), S(r - 100)],
               "Incolonna le virgole e somma: <b>%s</b>." % S(r))


def s5():
    p = K.next()
    k = R.choice(["spesa", "resto", "salto", "nastro", "corsa", "peso", "budget"])
    if k == "spesa":
        a, b, c = R.randint(120, 950), R.randint(80, 640), R.randint(50, 390)
        r = a + b + c
        return mcq("%s compra pane a %s, frutta a %s e latte a %s. Quanto spende?" % (p[0], eur(a), eur(b), eur(c)), eur(r), [eur(r + 100), eur(r - 10), eur(a + b)],
                   "%s + %s + %s = <b>%s</b>." % (eur(a), eur(b), eur(c), eur(r)))
    if k == "resto":
        a = R.randint(1105, 4890)
        pay = (a // 1000 + 1) * 1000 if a % 1000 else a + 1000
        pay = max(pay, 2000) if a < 2000 else 5000
        r = pay - a
        return mcq("%s spende %s e paga con %s. Quanto riceve di resto?" % (p[0], eur(a), eur(pay)), eur(r), [eur(r + 100), eur(pay + a), eur(r - 10) if r > 10 else eur(r + 20)],
                   "%s − %s = <b>%s</b>." % (eur(pay), eur(a), eur(r)))
    if k == "salto":
        a, b = R.randint(250, 390), R.randint(5, 40)
        return mcq("Al primo salto %s fa %s m; al secondo %s m in più. Quanto misura il secondo salto?" % (p[0], D(a, 2), D(b, 2)), D(a + b, 2) + " m",
                   [D(a - b, 2) + " m", D(a + b * 10, 2) + " m", D(a + b + 10, 2) + " m"], "%s + %s = <b>%s m</b>." % (D(a, 2), D(b, 2), D(a + b, 2)))
    if k == "nastro":
        a = R.randint(3, 9) * 1000
        b = rand_dec(1, a // 1000 - 1, 2)
        return mcq("Un rotolo ha %s m di nastro. Se ne tagliano %s m. Quanti metri restano?" % (S(a), S(b)), S(a - b) + " m",
                   [D(a - (b // 1000) * 1000 + b % 1000, 3) + " m", S(a + b) + " m", S(a - b + 1000) + " m"], "%s − %s = <b>%s m</b>." % (S(a), S(b), S(a - b)))
    if k == "corsa":
        a, b = R.randint(1180, 1320), R.randint(3, 60)
        return mcq("Nei 100 m %s corre in %s s. Il vincitore ci mette %s s in meno. Qual è il tempo del vincitore?" % (p[0], D(a, 2), D(b, 2)), D(a - b, 2) + " s",
                   [D(a + b, 2) + " s", D(a - b * 10, 2) + " s", D(a - b - 10, 2) + " s"], "%s − %s = <b>%s s</b>." % (D(a, 2), D(b, 2), D(a - b, 2)))
    if k == "peso":
        a, b = R.randint(1200, 3800), R.randint(250, 900)
        return mcq("Una borsa pesa %s kg. Si aggiunge un pacco da %s kg. Quanto pesa ora?" % (S(a), S(b)), S(a + b) + " kg",
                   [S(a + b + 1000) + " kg", S(a - b) + " kg", S(a + b // 10) + " kg"], "%s + %s = <b>%s kg</b>." % (S(a), S(b), S(a + b)))
    have = R.randint(15, 40) * 100
    a, b = R.randint(450, 1290), R.randint(380, 990)
    if a + b >= have:
        return None
    return mcq("%s ha %s. Compra un libro da %s e un gioco da %s. Quanto %s resta?" % (p[0], eur(have), eur(a), eur(b), "le" if p[1] == "lei" else "gli"),
               eur(have - a - b), [eur(a + b), eur(have - a), eur(have - a - b + 100)], "%s + %s = %s; %s − %s = <b>%s</b>." % (eur(a), eur(b), eur(a + b), eur(have), eur(a + b), eur(have - a - b)))


def main():
    seen = set()
    sets = [
        ("Addizioni in colonna", mix(R, seen, [(s1, 20)])),
        ("Addizioni con cifre decimali diverse", mix(R, seen, [(s2, 14), (s4_tre, 6)])),
        ("Sottrazioni in colonna", mix(R, seen, [(s3, 20)])),
        ("Calcolo mentale e stima", mix(R, seen, [(s4_mentale, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Incolonna i numeri con la <b>virgola sotto la virgola</b>: unità sotto unità, decimi sotto decimi.",
         "Se un numero ha meno cifre decimali, aggiungi degli <b>zeri</b> a destra: 5 = 5,00.",
         "Calcola come con i numeri naturali, da destra a sinistra, e nel risultato metti la virgola sotto le altre.",
         "Prima di calcolare fai una stima arrotondando all’unità."],
        [("12,5 + 3,75", ["12,50 + 3,75", "u: 0 + 5, d: 5 + 7 = 12 …"], "16,25"),
         ("5 − 1,3", ["5,0 − 1,3"], "3,7")],
        [["Incolonnare a destra: 2,5 + 1,25 = 1,50", "La virgola va sotto la virgola: 2,50 + 1,25 = 3,75."],
         ["5 − 1,3 = 4,3", "Scrivi 5,0: 5,0 − 1,3 = 3,7."],
         ["Dimenticare il cambio tra decimi e unità", "10 decimi = 1 unità, come 10 unità = 1 decina."]])
    faq = [("Perché si mettono gli zeri a destra?", "Perché non cambiano il valore (3,5 = 3,50) e aiutano a incolonnare le cifre dello stesso posto."),
           ("Come controllo il risultato?", "Con una stima: 12,5 + 3,75 è circa 13 + 4 = 17, quindi 16,25 è ragionevole.")]
    make_unit(R, "addizioni-e-sottrazioni-con-i-decimali", "N",
              "Eseguire le quattro operazioni con sicurezza, anche con i numeri decimali, valutando l’opportunità di ricorrere al calcolo mentale, scritto o con la calcolatrice; stimare il risultato",
              "Addizioni e sottrazioni con i numeri decimali", "Addizioni e sottrazioni con i decimali",
              "Schede di matematica per la classe quinta su addizioni e sottrazioni con i numeri decimali: incolonnare con la virgola, zeri, colonna, calcolo mentale, stima e problemi. 100 esercizi con soluzioni.",
              "Virgola sotto la virgola.", "Aggiungi zeri a destra: 5 = 5,0.",
              body, faq, sets, 5, grade=G)


if __name__ == "__main__":
    main()
