# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Le frazioni (Numeri)
  python3 tools/gen_it_matematica_c5_frazioni.py
Frazioni proprie, improprie e apparenti, frazioni equivalenti, ridurre ai minimi termini, confrontare e ordinare,
frazioni sulla retta, frazioni decimali e numeri decimali, numeri misti.
Errori: confondere impropria e apparente, aggiungere lo stesso numero sopra e sotto, 1/8 &gt; 1/4 perché 8 &gt; 4.
"""
import random
from math import gcd
from it_common import mcq, num, lesson, make_unit, mix, fr, striscia, retta, relabel, DIV, FOIS
import fr_common as _F

R = random.Random(70511)
G = "classe-quinta"


def F(n, d):
    return fr(n, d)


def tipo(n, d):
    return "apparente" if n % d == 0 else "propria" if n < d else "impropria"


def s1_tipo():
    d = R.randint(2, 12)
    k = R.choice(["propria", "impropria", "apparente"])
    n = R.randint(1, d - 1) if k == "propria" else d * R.randint(1, 4) if k == "apparente" else R.choice([x for x in range(d + 1, 4 * d) if x % d])
    t = tipo(n, d)
    why = {"propria": "il numeratore è minore del denominatore: è meno di un intero", "impropria": "il numeratore è maggiore del denominatore ma non è un suo multiplo: è più di un intero",
           "apparente": "il numeratore è un multiplo del denominatore: è uguale a %d %s" % (n // d, "intero" if n // d == 1 else "interi")}[t]
    return mcq("Che tipo di frazione è %s?" % F(n, d), t, [x for x in ("propria", "impropria", "apparente") if x != t] + ["decimale"],
               "In %s %s: è <b>%s</b>." % (F(n, d), why, t))


def s1_misto():
    d = R.randint(2, 9)
    i = R.randint(1, 4)
    r = R.randint(1, d - 1)
    n = i * d + r
    if R.random() < 0.5:
        return mcq("Quanti interi e quale frazione ci sono in %s?" % F(n, d), "%d interi e %s" % (i, F(r, d)) if i > 1 else "1 intero e %s" % F(r, d),
                   ["%d interi e %s" % (i + 1, F(r, d)), "%d interi e %s" % (r, F(i, d)) if r > 1 else "1 intero e %s" % F(i, d), "%d interi e %s" % (i, F(r + 1, d)) if r + 1 < d else "%d interi" % (i + 1)],
                   "%d %s %d = %d con resto %d: %s = <b>%d %s e %s</b>." % (n, DIV, d, i, r, F(n, d), i, "intero" if i == 1 else "interi", F(r, d)))
    return mcq("Scrivi come frazione: %d %s e %s" % (i, "intero" if i == 1 else "interi", F(r, d)), F(n, d), [F(i + r, d), F(i * r, d), F(n, i * d) if i > 1 else F(r + d + 1, d)],
               "%d %s %d + %d = %d: <b>%s</b>." % (i, FOIS, d, r, n, F(n, d)))


def s2_equivalenti():
    n, d = R.randint(1, 6), R.randint(2, 9)
    if n >= d or gcd(n, d) > 1:
        return None
    k = R.randint(2, 6)
    return mcq("Quale frazione è equivalente a %s?" % F(n, d), F(n * k, d * k), [F(n + k, d + k), F(n * k, d + k), F(n, d * k), F(n * k + 1, d * k)],
               "Moltiplica numeratore e denominatore per lo stesso numero (%d): %s = <b>%s</b>." % (k, F(n, d), F(n * k, d * k)))


def s2_mancante():
    n, d = R.randint(1, 8), R.randint(2, 10)
    if n >= d or gcd(n, d) > 1:
        return None
    k = R.randint(2, 8)
    return mcq("Completa: %s = %s" % (F(n, d), F("?", d * k)), str(n * k), [str(n + d * k - d), str(n * k + 1), str(d * k - n), str(k)],
               "%d %s %d = %d, quindi anche %d %s %d = <b>%d</b>." % (d, FOIS, k, d * k, n, FOIS, k, n * k))


def s2_riduci():
    n, d = R.randint(1, 8), R.randint(2, 12)
    if n >= d or gcd(n, d) > 1:
        return None
    k = R.choice([2, 3, 4, 5, 6])
    N, Dd = n * k, d * k
    half = None
    for p in (2, 3, 5):
        if k % p == 0 and k != p:
            half = F(N // p, Dd // p)
    return mcq("Riduci ai minimi termini: %s" % F(N, Dd), F(n, d), [half, F(N - k, Dd - k) if N > k else None, F(n, Dd), F(d, n)],
               "Dividi numeratore e denominatore per il loro divisore comune più grande (%d): <b>%s</b>." % (k, F(n, d)))


def s3_confronta():
    k = R.choice(["den", "num", "uno", "diversi"])
    if k == "den":
        d = R.randint(5, 15)
        a, b = R.sample(range(1, d), 2)
        A, B, va, vb = F(a, d), F(b, d), a / d, b / d
        why = "Stesso denominatore: è maggiore quella con il numeratore maggiore."
    elif k == "num":
        n = R.randint(1, 5)
        a, b = R.sample(range(n + 1, 16), 2)
        A, B, va, vb = F(n, a), F(n, b), n / a, n / b
        why = "Stesso numeratore: è maggiore quella con il denominatore minore (le parti sono più grandi)."
    elif k == "uno":
        d = R.randint(3, 9)
        a = R.randint(1, d - 1)
        b = R.randint(d + 1, 2 * d)
        A, B, va, vb = F(a, d), F(b, d + R.randint(0, 2)) if b > d + 2 else F(b, d), a / d, None
        vb = 1.5
        why = "Una è minore di 1 (propria), l’altra maggiore di 1 (impropria)."
    else:
        d1, d2 = R.choice([(2, 4), (3, 6), (4, 8), (2, 6), (5, 10), (3, 9), (4, 12)])
        a, b = R.randint(1, d1 - 1), R.randint(1, d2 - 1)
        if a * d2 == b * d1:
            return None
        A, B, va, vb = F(a, d1), F(b, d2), a / d1, b / d2
        why = "Trasforma %s in %s, con lo stesso denominatore di %s." % (A, F(a * d2 // d1, d2), B)
    g, s_ = (A, B) if va > vb else (B, A)
    return mcq("Qual è la frazione maggiore: %s o %s?" % (A, B), g, [s_, "sono uguali", "non si può sapere"], "%s <b>%s</b>." % (why, g))


def s3_ordina():
    d = R.choice([6, 8, 10, 12])
    ns = sorted(R.sample(range(1, d), 4))
    if R.random() < 0.5:
        n = R.randint(1, 3)
        ds = sorted(R.sample(range(n + 1, 13), 4), reverse=True)
        o = [F(n, x) for x in ds]
        wrong = [F(n, x) for x in sorted(ds)]
        why = "Stesso numeratore: più grande il denominatore, più piccola la frazione."
    else:
        o = [F(x, d) for x in ns]
        wrong = o[::-1]
        why = "Stesso denominatore: si ordinano i numeratori."
    f = lambda L: "; ".join(L)
    sh = o[:]
    R.shuffle(sh)
    w2 = o[:]
    w2[1], w2[2] = w2[2], w2[1]
    return mcq("Metti in ordine crescente: %s" % f(sh), f(o), [f(wrong), f(w2), f([o[1], o[0]] + o[2:])], "%s <b>%s</b>." % (why, f(o)))


def s4_decimali():
    k = R.choice(["fd", "fd", "df", "conv"])
    if k == "fd":
        d = R.choice([10, 100, 1000])
        n = R.randint(1, d * 3)
        if n % 10 == 0:
            return None
        p = len(str(d)) - 1
        Dd = lambda v, q: "%s,%s" % (num(v // 10 ** q), str(v % 10 ** q).rjust(q, "0")) if q else num(v)
        s_ = Dd(n, p)
        alt = [Dd(n, p + 1), Dd(n, p - 1) if p > 1 else "%d,%d" % (n, d), "%d,%d" % (n, d), Dd(n + 10 ** p, p)]
        return mcq("Scrivi %s come numero decimale." % F(n, d), s_, alt, "Il denominatore %s ha %d %s: dopo la virgola %d %s. <b>%s</b>." % (num(d), p, "zero" if p == 1 else "zeri", p, "cifra" if p == 1 else "cifre", s_))
    if k == "df":
        n = R.randint(1, 999)
        p = R.choice([1, 2, 3])
        if n >= 10 ** p * 3 or n % 10 == 0:
            return None
        s = "%d,%s" % (n // 10 ** p, str(n % 10 ** p).rjust(p, "0"))
        return mcq("Scrivi %s come frazione decimale." % s, F(n, 10 ** p), [F(n, 10 ** (p + 1)), F(n, 10 ** (p - 1)) if p > 1 else F(n, 1000), F(n % 10 ** p, 10 ** p) if n >= 10 ** p else F(n, 10 ** p * 10 + 0)],
                   "%d cifre dopo la virgola: denominatore %s. <b>%s</b>." % (p, num(10 ** p), F(n, 10 ** p)))
    n, d, dec = R.choice([(1, 2, "0,5"), (1, 4, "0,25"), (3, 4, "0,75"), (1, 5, "0,2"), (2, 5, "0,4"), (3, 5, "0,6"), (4, 5, "0,8"), (1, 20, "0,05"), (3, 20, "0,15"), (1, 25, "0,04")])
    return mcq("Quale numero decimale è uguale a %s?" % F(n, d), dec, ["%d,%d" % (n, d), "0,%d" % (n * 10 // d + 1), "0,%d" % d],
               "Trasforma in frazione decimale: %s = %s = <b>%s</b>." % (F(n, d), F(n * (100 // d), 100), dec))


def s4_retta():
    d = R.choice([2, 3, 4, 5, 6])
    n = R.randint(1, 2 * d - 1)
    if n == d:
        return None
    pic = relabel(_F.droite_frac(d, 2, [(n, "A")]), "retta da 0 a 2, ogni unità divisa in %d parti" % d)
    return mcq(pic + "Quale frazione indica la freccia A?", F(n, d), [F(n, d + 1), F(n + 1, d), F(d, n), F(n, 2 * d)],
               "Ogni unità è divisa in %d parti; A è dopo %d parti: <b>%s</b>%s." % (d, n, F(n, d), " (più di un intero: frazione impropria)" if n > d else ""))


def s5():
    k = R.choice(["torta", "maratona", "classe", "bottiglie", "pagine"])
    if k == "torta":
        a, b = R.choice([(2, 8), (1, 4), (3, 12), (2, 6), (1, 3)])
        c, d = R.choice([(3, 8), (1, 2), (5, 12), (1, 6), (2, 9)])
        if abs(a / b - c / d) < 1e-9:
            return None
        g = ("Anna", F(a, b)) if a / b > c / d else ("Luca", F(c, d))
        return mcq("Anna mangia %s di una pizza, Luca %s di una pizza uguale. Chi ha mangiato di più?" % (F(a, b), F(c, d)), g[0], ["Anna" if g[0] == "Luca" else "Luca", "hanno mangiato uguale", "non si può sapere"],
                   "Porta allo stesso denominatore e confronta: ha mangiato di più <b>%s</b> (%s)." % (g[0], g[1]))
    if k == "maratona":
        d = R.choice([4, 5, 8, 10])
        n = R.randint(d + 1, 2 * d - 1)
        return mcq("In una settimana %s percorre %s di km. Ha percorso più o meno di 1 km?" % (R.choice(["Marco", "Giulia", "Pietro"]), F(n, d)), "più di 1 km",
                   ["meno di 1 km", "esattamente 1 km", "non si può sapere"], "%s è una frazione impropria: numeratore maggiore del denominatore, quindi <b>più di 1 km</b>." % F(n, d))
    if k == "classe":
        n, d = R.choice([(12, 24), (8, 20), (15, 25), (6, 18), (10, 25), (9, 27), (14, 28)])
        g = gcd(n, d)
        return mcq("In una classe di %d bambini, %d vanno a scuola in bicicletta. Che frazione è, ridotta ai minimi termini?" % (d, n), F(n // g, d // g),
                   [F(n, d), F(d // g, n // g), F(n // 2, d // 2) if n % 2 == 0 and d % 2 == 0 and g != 2 else F(n // g + 1, d // g)],
                   "%s ridotta (dividi per %d) = <b>%s</b>." % (F(n, d), g, F(n // g, d // g)))
    if k == "bottiglie":
        d = R.choice([2, 4])
        n = R.randint(d + 1, 3 * d)
        if n % d == 0:
            return None
        return mcq("Una ricetta usa %s di litro di latte. Quanti litri interi e quale parte?" % F(n, d), "%d %s e %s" % (n // d, "litro" if n // d == 1 else "litri", F(n % d, d)),
                   ["%d %s e %s" % (n // d + 1, "litri", F(n % d, d)), "%d %s e %s" % (n % d, "litro" if n % d == 1 else "litri", F(n // d, d)), "%d litri" % n],
                   "%d %s %d = %d con resto %d: <b>%d %s e %s</b>." % (n, DIV, d, n // d, n % d, n // d, "litro" if n // d == 1 else "litri", F(n % d, d)))
    a, b = R.choice([(3, 4), (2, 3), (5, 6), (7, 10), (4, 5)])
    c = R.choice([x for x in (6, 8, 9, 10, 12, 15, 20) if x % b == 0])
    return mcq("Sofia ha letto %s di un libro, Marco %s di un libro uguale. Hanno letto la stessa parte?" % (F(a, b), F(a * c // b, c)), "sì, le frazioni sono equivalenti",
               ["no, Marco ha letto di più", "no, Sofia ha letto di più", "non si può sapere"], "%s = %s (moltiplica per %d): <b>sì, sono equivalenti</b>." % (F(a, b), F(a * c // b, c), c // b))


def main():
    seen = set()
    sets = [
        ("Proprie, improprie, apparenti", mix(R, seen, [(s1_tipo, 12), (s1_misto, 8)])),
        ("Frazioni equivalenti", mix(R, seen, [(s2_equivalenti, 7), (s2_mancante, 7), (s2_riduci, 6)])),
        ("Confrontare e ordinare", mix(R, seen, [(s3_confronta, 14), (s3_ordina, 6)])),
        ("Frazioni, decimali e retta", mix(R, seen, [(s4_decimali, 12), (s4_retta, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Una frazione è <b>propria</b> se è minore di 1 (%s), <b>impropria</b> se è maggiore di 1 (%s), <b>apparente</b> se è uguale a interi (%s = 2)." % (F(3, 4), F(7, 4), F(8, 4)),
         "Due frazioni sono <b>equivalenti</b> se indicano la stessa parte: moltiplica o dividi numeratore e denominatore per lo stesso numero.",
         "Per <b>ridurre ai minimi termini</b> dividi sopra e sotto per il divisore comune più grande: %s = %s." % (F(12, 18), F(2, 3)),
         "Per confrontare frazioni con denominatori diversi portale allo stesso denominatore."],
        [("Confronta %s e %s" % (F(3, 4), F(5, 8)), ["%s = %s" % (F(3, 4), F(6, 8)), "%s &gt; %s" % (F(6, 8), F(5, 8))], "%s è maggiore" % F(3, 4))],
        [["Confondere impropria e apparente", "Apparente: il numeratore è un multiplo del denominatore."],
         ["Aggiungere lo stesso numero sopra e sotto", "Per le equivalenti si moltiplica o si divide, non si somma."],
         ["Pensare che %s &gt; %s" % (F(1, 8), F(1, 4)), "Più parti fai, più ogni parte è piccola."]],
        striscia(4, 3))
    faq = [("Che cosa vuol dire «ridurre ai minimi termini»?", "Scrivere la frazione con i numeri più piccoli possibili, dividendo numeratore e denominatore per lo stesso numero finché si può."),
           ("Una frazione impropria si può scrivere in un altro modo?", "Sì, come interi più una frazione propria: 7/4 = 1 intero e 3/4.")]
    make_unit(R, "frazioni", "N",
              "Operare con le frazioni e riconoscere frazioni equivalenti; confrontare e ordinare frazioni; riconoscere frazioni proprie, improprie e apparenti; passare dalle frazioni decimali ai numeri decimali",
              "Le frazioni: equivalenti, proprie, improprie e apparenti", "Frazioni",
              "Schede di matematica per la classe quinta sulle frazioni: proprie, improprie e apparenti, frazioni equivalenti, minimi termini, confronti, frazioni decimali e problemi. 100 esercizi con soluzioni.",
              "Frazioni equivalenti: moltiplica o dividi sopra e sotto per lo stesso numero.", "Propria < 1, impropria > 1, apparente = interi.",
              body, faq, sets, 11, grade=G)


if __name__ == "__main__":
    main()
