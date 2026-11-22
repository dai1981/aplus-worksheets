# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Multipli, divisori e numeri primi (Numeri)
  python3 tools/gen_it_matematica_c5_multipli_divisori_e_numeri_primi.py
Multipli e divisori, criteri di divisibilità per 2, 3, 5, 9, 10, 100, numeri primi e composti,
scomposizione in fattori primi (albero), problemi (gruppi uguali, file).
Errori: confondere multiplo e divisore, 1 è primo, 9 è primo perché dispari, criterio del 3 sull’ultima cifra.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, DIV, table

R = random.Random(70508)
G = "classe-quinta"
K = Kids(R)


def divisori(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def primo(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def s1_multiplo():
    a = R.randint(3, 12)
    if R.random() < 0.5:
        m = a * R.randint(3, 12)
        others = [m + 1, m - 1, m + a // 2 if a > 2 and (m + a // 2) % a else m + 2, a + 10 if (a + 10) % a else a + 1]
        return mcq("Quale numero è un multiplo di %d?" % a, num(m), [num(x) for x in others if x % a], "%d = %d %s %d: <b>%s</b> è multiplo di %d." % (m, a, FOIS, m // a, num(m), a))
    n = a * R.randint(2, 9)
    ds = divisori(n)
    d = R.choice([x for x in ds if 1 < x < n])
    nd = [x for x in range(2, n) if n % x and x not in (n + 1,)]
    R.shuffle(nd)
    return mcq("Quale numero è un divisore di %d?" % n, str(d), [str(x) for x in nd[:2]] + [str(n * 2)], "%d %s %d = %d senza resto: <b>%d</b> è divisore di %d." % (n, DIV, d, n // d, d, n))


def s1_lista():
    n = R.choice([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48])
    ds = divisori(n)
    f = lambda L: ", ".join(map(str, L))
    w1 = [d for d in ds if d not in (1, n)]
    w2 = ds[:-1]
    w3 = sorted(set(ds) | {n * 2})
    w4 = [n * k for k in range(1, 5)]
    return mcq("Quali sono tutti i divisori di %d?" % n, f(ds), [f(w1), f(w2), f(w3), f(w4)],
               "Cerca le coppie che danno %d: %s. Divisori: <b>%s</b>." % (n, ", ".join("%d %s %d" % (d, FOIS, n // d) for d in ds if d * d <= n), f(ds)))


CRIT = {2: "l’ultima cifra è pari (0, 2, 4, 6, 8)", 3: "la somma delle cifre è un multiplo di 3", 5: "l’ultima cifra è 0 o 5",
        9: "la somma delle cifre è un multiplo di 9", 10: "l’ultima cifra è 0", 4: "le ultime due cifre formano un multiplo di 4"}


def s2_criterio():
    k = R.choice([2, 3, 5, 9, 10, 3, 9, 4])
    if R.random() < 0.6:
        ok = k * R.randint(12, 999)
        bad = []
        while len(bad) < 5:
            x = R.randint(100, 9999)
            if x % k:
                bad.append(x)
        if k in (3, 9):
            bad.insert(0, ok + (1 if ok % 10 < 9 else -1) * (1 if k == 3 else 3))
            bad = [x for x in bad if x % k]
        return mcq("Quale numero è divisibile per %d?" % k, num(ok), [num(x) for x in bad],
                   "Un numero è divisibile per %d se %s. %s%s: <b>%s</b>." % (k, CRIT[k], num(ok), " (somma delle cifre %d)" % sum(map(int, str(ok))) if k in (3, 9) else "", num(ok)))
    return mcq("Quando un numero è divisibile per %d?" % k, "quando " + CRIT[k], ["quando " + CRIT[x] for x in CRIT if x != k][:4], "Un numero è divisibile per %d <b>quando %s</b>." % (k, CRIT[k]))


def s2_trova():
    n = R.randint(100, 9999)
    ks = [k for k in (2, 3, 5, 9, 10) if n % k == 0]
    if not ks or len(ks) > 3:
        return None
    f = lambda L: ", ".join(map(str, L)) if L else "nessuno"
    alt = [[k for k in (2, 3, 5, 9, 10) if k not in ks][:len(ks)], ks + [k for k in (3, 9, 5) if k not in ks][:1], ks[:-1] if len(ks) > 1 else [2 if 2 not in ks else 5], [2, 5, 10] if ks != [2, 5, 10] else [2, 10]]
    return mcq("Per quali di questi numeri è divisibile %s: 2, 3, 5, 9, 10?" % num(n), f(ks), [f(x) for x in alt],
               "Somma delle cifre: %d; ultima cifra: %d. È divisibile per <b>%s</b>." % (sum(map(int, str(n))), n % 10, f(ks)))


def s3_primo():
    k = R.choice(["quale", "quale", "nonprimo", "vero"])
    if k == "quale":
        p = R.choice([x for x in range(11, 98) if primo(x)])
        comp = [x for x in (21, 27, 33, 39, 49, 51, 57, 63, 69, 77, 81, 87, 91, 93, 1, 9, 15, 25, 35, 45) if abs(x - p) < 40]
        R.shuffle(comp)
        comp = comp[:3]
        return mcq("Quale di questi numeri è primo: %s?" % ", ".join(map(str, sorted(comp + [p]))), str(p), [str(x) for x in comp], "%d ha solo due divisori, 1 e %d: è <b>primo</b>. Gli altri hanno altri divisori." % (p, p))
    if k == "nonprimo":
        c = R.choice([21, 27, 33, 39, 49, 51, 57, 63, 69, 77, 87, 91])
        ps = [x for x in range(11, 98) if primo(x)]
        R.shuffle(ps)
        d = [x for x in divisori(c) if 1 < x < c][0]
        return mcq("Quale di questi numeri <b>non</b> è primo: %s?" % ", ".join(map(str, sorted(ps[:3] + [c]))), str(c), [str(x) for x in ps[:3]],
                   "%d = %d %s %d: ha più di due divisori, quindi è <b>composto</b>." % (c, d, FOIS, c // d))
    q, a, w = R.choice([("Il numero 1 è primo?", "no, ha un solo divisore", ["sì, è il primo numero", "sì, perché è dispari", "solo a volte"]),
                        ("Il numero 2 è primo?", "sì, è l’unico primo pari", ["no, perché è pari", "no, ha tre divisori", "non si sa"]),
                        ("Quanti divisori ha un numero primo?", "2", ["1", "3", "nessuno"]),
                        ("Tutti i numeri dispari sono primi?", "no, per esempio 9 = 3 × 3", ["sì, sempre", "sì, tranne l’1", "no, solo quelli sopra 100"]),
                        ("Quanti numeri primi ci sono tra 1 e 20?", "8", ["10", "7", "9"]),
                        ("Quale coppia contiene solo numeri primi?", "17 e 23", ["21 e 23", "15 e 17", "27 e 29"])])
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def fattori(n):
    f, d = [], 2
    while n > 1:
        while n % d == 0:
            f.append(d)
            n //= d
        d += 1
    return f


def ff(f):
    from collections import Counter
    c = Counter(f)
    return " %s " % FOIS.join("%d<sup>%d</sup>" % (p, e) if e > 1 else str(p) for p, e in sorted(c.items()))


def s4_scomponi():
    n = R.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 72, 75, 80, 84, 90, 96, 100, 108, 120, 126, 150, 180])
    f = fattori(n)
    ok = ff(f).strip()
    w1 = ff(f[:-1] + [f[-1] * 2]).strip() if len(f) > 1 else None
    w2 = (" %s " % FOIS).join(map(str, f[:-2] + [f[-2] * f[-1]])) if len(f) > 2 else None
    w3 = ff(f + [2]).strip()
    w4 = ff([x for x in f if x != 2] + [3]).strip() if 2 in f else ff(f + [3]).strip()
    return mcq("Qual è la scomposizione in fattori primi di %d?" % n, ok, [w1, w2, w3, w4],
               "Dividi per i numeri primi: %s. Quindi %d = <b>%s</b>." % (" → ".join(str(n // __import__('math').prod(f[:i])) for i in range(len(f) + 1)), n, ok))


def s5():
    p = K.next()
    k = R.choice(["file", "gruppi", "pacchi", "autobus", "bancarelle"])
    if k == "file":
        n = R.choice([24, 30, 36, 48, 60])
        ds = divisori(n)
        return mcq("%s vuole disporre %d piantine in file uguali (almeno 2 file, almeno 2 piantine per fila). In quanti modi diversi?" % (p[0], n), str(len(ds) - 2),
                   [str(len(ds)), str(len(ds) - 1), str(len(ds) // 2)],
                   "Servono i divisori di %d diversi da 1 e da %d: %s. Sono <b>%d</b> modi." % (n, n, ", ".join(map(str, ds[1:-1])), len(ds) - 2))
    if k == "gruppi":
        n = R.choice([18, 20, 24, 28, 30, 32])
        g = R.choice([d for d in divisori(n) if 2 < d < n])
        return mcq("In una classe di %d bambini si possono fare gruppi di %d senza che nessuno resti fuori?" % (n, g), "sì, %d gruppi" % (n // g),
                   ["no, resta fuori qualcuno", "sì, %d gruppi" % (n // g + 1), "sì, %d gruppi" % g if g != n // g else "sì, %d gruppi" % (g + 2)],
                   "%d è un divisore di %d: %d %s %d = <b>%d gruppi</b>." % (g, n, n, DIV, g, n // g))
    if k == "pacchi":
        a, b = R.choice([(4, 6), (6, 8), (6, 9), (4, 10), (8, 12)])
        import math
        l = a * b // math.gcd(a, b)
        return mcq("Le matite si vendono in pacchi da %d, le gomme da %d. Qual è il numero più piccolo per avere lo stesso numero di matite e di gomme?" % (a, b), str(l),
                   [str(a * b) if a * b != l else str(l * 2), str(a + b), str(l + a)],
                   "Cerca il primo multiplo comune di %d e %d: <b>%d</b>." % (a, b, l))
    if k == "autobus":
        a, b = R.choice([(10, 15), (12, 18), (15, 20), (20, 30), (8, 12)])
        import math
        l = a * b // math.gcd(a, b)
        h = 8
        mm = l
        return mcq("Alle %d:00 partono insieme due autobus: uno passa ogni %d minuti, l’altro ogni %d. Dopo quanti minuti ripartono insieme?" % (h, a, b), "%d minuti" % l,
                   ["%d minuti" % (a * b) if a * b != l else "%d minuti" % (l * 2), "%d minuti" % (a + b), "%d minuti" % max(a, b)],
                   "Serve il più piccolo multiplo comune di %d e %d: <b>%d minuti</b>." % (a, b, l))
    n = R.choice([24, 36, 48, 60, 72])
    m = R.choice([d for d in divisori(n) if 3 <= d <= 12])
    return mcq("Un fioraio ha %d rose e vuole fare mazzi tutti uguali da %d rose. Avanzano rose?" % (n, m), "no, fa %d mazzi" % (n // m),
               ["sì, ne avanza 1", "no, fa %d mazzi" % (n // m + 1), "sì, ne avanzano %d" % m], "%d è divisibile per %d: <b>%d mazzi</b> e non avanza niente." % (n, m, n // m))


def main():
    seen = set()
    sets = [
        ("Multipli e divisori", mix(R, seen, [(s1_multiplo, 14), (s1_lista, 6)])),
        ("Criteri di divisibilità", mix(R, seen, [(s2_criterio, 10), (s2_trova, 10)])),
        ("Numeri primi e composti", mix(R, seen, [(s3_primo, 20)])),
        ("Scomposizione in fattori primi", mix(R, seen, [(s4_scomponi, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["I <b>multipli</b> di 6 sono i numeri della tabellina del 6: 6, 12, 18… I <b>divisori</b> di 12 sono i numeri che dividono 12 senza resto: 1, 2, 3, 4, 6, 12.",
         "Divisibile per 2: ultima cifra pari. Per 5: ultima cifra 0 o 5. Per 10: ultima cifra 0. Per 3 o per 9: la <b>somma delle cifre</b> è multiplo di 3 o di 9.",
         "Un numero è <b>primo</b> se ha solo due divisori: 1 e se stesso (2, 3, 5, 7, 11…). Altrimenti è <b>composto</b>. L’1 non è né primo né composto.",
         "Ogni numero composto si scrive come prodotto di numeri primi: 60 = 2² %s 3 %s 5." % (FOIS, FOIS)],
        [("Scomponi 60", ["60 %s 2 = 30" % DIV, "30 %s 2 = 15" % DIV, "15 %s 3 = 5" % DIV, "5 %s 5 = 1" % DIV], "2² × 3 × 5")],
        [["Confondere multiplo e divisore", "Il multiplo è più grande (o uguale), il divisore più piccolo (o uguale)."],
         ["Dire che 1 è primo", "Un primo ha esattamente due divisori; 1 ne ha uno solo."],
         ["Dire che 9 è primo perché è dispari", "9 = 3 × 3: è composto."]],
        table(["Divisibile per", "Regola"], [["2", "ultima cifra pari"], ["3", "somma delle cifre multipla di 3"], ["5", "ultima cifra 0 o 5"], ["9", "somma delle cifre multipla di 9"], ["10", "ultima cifra 0"]]))
    faq = [("Quali sono i numeri primi fino a 30?", "2, 3, 5, 7, 11, 13, 17, 19, 23, 29."),
           ("A che cosa servono i criteri di divisibilità?", "A capire velocemente se una divisione avrà resto 0, senza farla: utile per semplificare le frazioni e per scomporre i numeri.")]
    make_unit(R, "multipli-divisori-e-numeri-primi", "N",
              "Individuare multipli e divisori di un numero; conoscere i criteri di divisibilità; riconoscere numeri primi e composti",
              "Multipli, divisori e numeri primi", "Multipli, divisori e numeri primi",
              "Schede di matematica per la classe quinta su multipli, divisori e numeri primi: criteri di divisibilità per 2, 3, 5, 9 e 10, numeri primi e composti, scomposizione in fattori primi e problemi. 100 esercizi con soluzioni.",
              "Un numero primo ha solo due divisori: 1 e se stesso.", "Per 3 e per 9 guarda la somma delle cifre.",
              body, faq, sets, 8, grade=G)


if __name__ == "__main__":
    main()
