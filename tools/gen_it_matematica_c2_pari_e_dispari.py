# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Numeri pari e dispari (Numeri)
  python3 tools/gen_it_matematica_c2_pari_e_dispari.py
Formare coppie (pari: nessuno resta da solo), riconoscere pari e dispari dalla cifra delle unità, sequenze di pari
e dispari, pari + pari, pari + dispari, problemi (squadre a due, calzini).
Errori: guardare la cifra delle decine (34 dispari perché 3), pensare che 0 non sia pari.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, wrap, text, INK, GREEN, FILL
import it_c2 as C
import k_pics

R = random.Random(70203)
G = "classe-seconda"
K = Kids(R)


def coppie(n, kind):
    s = []
    pairs, rest = divmod(n, 2)
    x = 8
    for i in range(pairs):
        s.append("<rect x='%d' y='6' width='34' height='64' rx='10' fill='none' stroke='%s' stroke-width='1.6'/>" % (x, GREEN))
        s.append(k_pics.obj(kind, x + 17, 22, 11))
        s.append(k_pics.obj(kind, x + 17, 52, 11))
        x += 40
    if rest:
        s.append(k_pics.obj(kind, x + 17, 22, 11))
        x += 40
    return C.it(wrap(x + 4, 76, "".join(s), ""), "%s messi a coppie" % C.cose(kind, n))


def tipo(n):
    return "pari" if n % 2 == 0 else "dispari"


def s1_coppie():
    n = R.randint(3, 15)
    k = R.choice(C.KINDS)
    t = tipo(n)
    return mcq(coppie(n, k) + "Le %s sono messe a coppie. %d è pari o dispari?" % (C.nome(k), n) if C.COSE[k][2] == "f" else coppie(n, k) + "I %s sono messi a coppie. %d è pari o dispari?" % (C.nome(k), n),
               t, ["dispari" if t == "pari" else "pari", "né pari né dispari", "pari e dispari"],
               "%s: è <b>%s</b>." % ("Tutti hanno un compagno" if t == "pari" else "Ne resta uno da solo", t))


def s2_cifra():
    n = R.randint(10, 99)
    t = tipo(n)
    return mcq("%d è un numero pari o dispari?" % n, t, ["dispari" if t == "pari" else "pari", "né pari né dispari", "dipende dalle decine"],
               "Guarda solo la cifra delle unità: %d è %s. <b>%d è %s</b>." % (n % 10, t, n, t))


def s2_quale():
    want = R.choice(["pari", "dispari"])
    ns = []
    while len(ns) < 3:
        x = R.randint(10, 99)
        if tipo(x) != want and x not in ns:
            ns.append(x)
    ok = R.randint(10, 99)
    while tipo(ok) != want:
        ok = R.randint(10, 99)
    trap = [x for x in ns if (x // 10) % 2 == (0 if want == "pari" else 1)]
    return mcq("Quale numero è %s: %s?" % (want, ", ".join(map(str, sorted(ns + [ok])))), str(ok), [str(x) for x in ns],
               "Un numero è %s se la cifra delle unità è %s: <b>%d</b>." % (want, "0, 2, 4, 6 o 8" if want == "pari" else "1, 3, 5, 7 o 9", ok))


def s3_sequenza():
    a = R.randint(10, 80)
    seq = [a + 2 * i for i in range(4)]
    t = tipo(a)
    k = R.choice(["dopo", "manca"])
    if k == "dopo":
        return mcq("Continua la fila dei numeri %s: %s, …" % (t, ", ".join(map(str, seq))), str(seq[-1] + 2), [str(seq[-1] + 1), str(seq[-1] + 3), str(seq[-1] + 10)],
                   "I numeri %s vanno di 2 in 2: %d + 2 = <b>%d</b>." % (t, seq[-1], seq[-1] + 2))
    i = R.randint(1, 2)
    shown = [str(x) if j != i else "☐" for j, x in enumerate(seq)]
    return mcq("Quale numero manca? %s" % ", ".join(shown), str(seq[i]), [str(seq[i] + 1), str(seq[i] - 1), str(seq[i] + 10)], "Si va di 2 in 2: <b>%d</b>." % seq[i])


def s3_conta():
    a, b = sorted(R.sample(range(10, 40), 2))
    if b - a < 4 or b - a > 12:
        return None
    want = R.choice(["pari", "dispari"])
    lst = [x for x in range(a, b + 1) if tipo(x) == want]
    return mcq("Quanti numeri %s ci sono da %d a %d (compresi)?" % (want, a, b), str(len(lst)), [str(len(lst) + 1), str(b - a), str(len(lst) - 1) if len(lst) > 1 else str(len(lst) + 2)],
               "Sono: %s. In tutto <b>%d</b>." % (", ".join(map(str, lst)), len(lst)))


def s4_somme():
    k = R.choice(["pp", "dd", "pd"])
    if k == "pp":
        a, b = R.randrange(2, 40, 2), R.randrange(2, 40, 2)
    elif k == "dd":
        a, b = R.randrange(1, 40, 2), R.randrange(1, 40, 2)
    else:
        a, b = R.randrange(2, 40, 2), R.randrange(1, 40, 2)
    t = tipo(a + b)
    return mcq("%d + %d fa un numero pari o dispari?" % (a, b), t, ["dispari" if t == "pari" else "pari", "dipende", "né pari né dispari"],
               "%d + %d = %d: è <b>%s</b>. %s" % (a, b, a + b, t, {"pp": "Pari + pari = pari.", "dd": "Dispari + dispari = pari.", "pd": "Pari + dispari = dispari."}[k]))


def s5():
    p = K.next()
    k = R.choice(["squadre", "calzini", "banchi", "dadi", "case"])
    if k == "squadre":
        n = R.randint(15, 29)
        return mcq("In classe ci sono %d bambini. Si mettono a coppie. Resta qualcuno da solo?" % n, "sì, uno resta da solo" if n % 2 else "no, %d coppie" % (n // 2),
                   ["no, %d coppie" % (n // 2) if n % 2 else "sì, uno resta da solo", "sì, ne restano due", "no, %d coppie" % n],
                   "%d è %s: %s." % (n, tipo(n), "<b>uno resta da solo</b>" if n % 2 else "<b>%d coppie</b>, nessuno da solo" % (n // 2)))
    if k == "calzini":
        n = R.randint(5, 15) * 2 + R.choice([0, 1])
        return mcq("Nel cassetto ci sono %d calzini. Si possono fare tutte coppie?" % n, "sì" if n % 2 == 0 else "no, ne avanza uno", ["no, ne avanza uno" if n % 2 == 0 else "sì", "no, ne avanzano due", "solo se sono rossi"],
                   "%d è %s: <b>%s</b>." % (n, tipo(n), "sì" if n % 2 == 0 else "ne avanza uno"))
    if k == "banchi":
        n = R.randint(3, 13)
        return mcq("In un’aula ci sono %d banchi da due posti, tutti pieni. I bambini sono un numero pari o dispari?" % n, "pari", ["dispari", "dipende dai banchi", "né pari né dispari"],
                   "%d %s 2 = %d: chi è seduto a due a due forma sempre un numero <b>pari</b>." % (n, "×", n * 2))
    if k == "dadi":
        a, b = R.randint(1, 6), R.randint(1, 6)
        return mcq("%s lancia due dadi: escono %d e %d. La somma è pari o dispari?" % (p[0], a, b), tipo(a + b), ["dispari" if (a + b) % 2 == 0 else "pari", "dipende", "è sempre pari"],
                   "%d + %d = %d: <b>%s</b>." % (a, b, a + b, tipo(a + b)))
    n = R.randint(2, 40)
    lato = "pari" if n % 2 == 0 else "dispari"
    return mcq("In una via le case con i numeri pari sono a destra e quelle con i numeri dispari a sinistra. La casa numero %d da che parte è?" % n, "a destra" if lato == "pari" else "a sinistra",
               ["a sinistra" if lato == "pari" else "a destra", "in mezzo", "non si può sapere"], "%d è %s: <b>%s</b>." % (n, lato, "a destra" if lato == "pari" else "a sinistra"))


def main():
    seen = set()
    sets = [
        ("Fare le coppie", mix(R, seen, [(s1_coppie, 20)])),
        ("Pari o dispari?", mix(R, seen, [(s2_cifra, 12), (s2_quale, 8)])),
        ("File di numeri pari e dispari", mix(R, seen, [(s3_sequenza, 12), (s3_conta, 8)])),
        ("Somme pari e dispari", mix(R, seen, [(s4_somme, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un numero è <b>pari</b> se puoi fare tutte coppie e nessuno resta da solo. È <b>dispari</b> se ne resta uno.",
         "Per capirlo basta guardare la <b>cifra delle unità</b>: 0, 2, 4, 6, 8 → pari; 1, 3, 5, 7, 9 → dispari.",
         "Pari e dispari si alternano: 10, 11, 12, 13… Anche lo 0 è pari."],
        [("34 è pari o dispari?", ["cifra delle unità: 4", "4 è pari"], "pari")],
        [["Guardare le decine: 34 dispari perché 3", "Conta solo la cifra delle unità."],
         ["Pensare che 0 non sia pari", "0 è pari: 0, 2, 4…"],
         ["Saltare un numero nella fila", "Pari e dispari si alternano sempre."]],
        coppie(9, "apple"))
    faq = [("Lo zero è pari?", "Sì: nella fila 0, 2, 4, 6… lo 0 è pari, e zero oggetti si dividono in coppie senza che ne resti uno."),
           ("Perché basta guardare l’ultima cifra?", "Perché le decine sono sempre pari (10, 20, 30…): conta solo se le unità si possono dividere in coppie.")]
    make_unit(R, "pari-e-dispari", "N",
              "Riconoscere numeri pari e dispari; contare in senso progressivo e regressivo per salti di due",
              "Numeri pari e dispari", "Pari e dispari",
              "Schede di matematica per la classe seconda sui numeri pari e dispari: fare le coppie, cifra delle unità, file di numeri, somme pari e dispari e problemi. 100 esercizi con soluzioni.",
              "Pari: tutti in coppia. Dispari: ne resta uno.", "Guarda la cifra delle unità.",
              body, faq, sets, 3, grade=G)


if __name__ == "__main__":
    main()
