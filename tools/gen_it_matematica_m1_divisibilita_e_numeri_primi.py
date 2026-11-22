# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Divisibilità e numeri primi (Numeri)
  python3 tools/gen_it_matematica_m1_divisibilita_e_numeri_primi.py
Multipli e divisori, criteri di divisibilità (2, 3, 4, 5, 9, 10, 11, 25), numeri primi e composti, crivello di
Eratostene, scomposizione in fattori primi con le potenze, numero dei divisori.
Errori: considerare 1 un numero primo, fermarsi nella scomposizione a un fattore composto, applicare il criterio del 3 all’ultima cifra.
"""
import random
from it_media import M, L, unit, mix, table, W, num, FOIS, Kids
import gen_it_matematica_c5_multipli_divisori_e_numeri_primi as M5

R = random.Random(71106)
G = "prima-media"
CRIT = dict(M5.CRIT)
CRIT.update({11: "la differenza tra la somma delle cifre di posto dispari e quella delle cifre di posto pari è 0 o un multiplo di 11", 25: "le ultime due cifre sono 00, 25, 50 o 75"})


def s1_crit():
    k = R.choice([2, 3, 4, 5, 9, 10, 11, 25])
    if R.random() < 0.4:
        return M("Quando un numero è divisibile per %d?" % k, "quando " + CRIT[k], ["quando " + CRIT[x] for x in R.sample([x for x in CRIT if x != k], 3)],
                 "Criterio di divisibilità per %d: <b>%s</b>." % (k, CRIT[k]))
    ok = k * R.randint(12, 999)
    bad = []
    while len(bad) < 3:
        x = ok + R.choice([-1, 1, 2, -2, 3, 10, -10, k // 2 or 1])
        if x % k and x > 0 and x not in bad:
            bad.append(x)
    extra = " (somma delle cifre %d)" % sum(map(int, str(ok))) if k in (3, 9) else ""
    return M("Quale numero è divisibile per %d?" % k, num(ok), [num(x) for x in bad], "Per %d: %s. %s%s → <b>%s</b>." % (k, CRIT[k], num(ok), extra, num(ok)))


def s2_primi():
    return M5.s3_primo()


def s2_crivello():
    lo = R.choice([20, 30, 40, 50, 60, 70, 80, 90])
    ps = [x for x in range(lo, lo + 10) if M5.primo(x)]
    k = R.random()
    if k < 0.5:
        return M("Quanti numeri primi ci sono tra %d e %d?" % (lo, lo + 9), str(len(ps)), W(len(ps) + 1, len(ps) - 1 if ps else 2, 5, len([x for x in range(lo, lo + 10) if x % 2])),
                 "Sono: %s. In tutto <b>%d</b>." % (", ".join(map(str, ps)) or "nessuno", len(ps)))
    n = R.randint(2, 100)
    p = M5.primo(n)
    why = "ha solo i divisori 1 e %d" % n if p else "%d = %d %s %d" % (n, [d for d in range(2, n) if n % d == 0][0], FOIS, n // [d for d in range(2, n) if n % d == 0][0]) if n > 1 else ""
    return M("Il numero %d è primo o composto?" % n, "primo" if p else "composto", ["composto" if p else "primo", "né primo né composto", "primo perché è dispari" if n % 2 else "composto perché è pari"],
             "%d %s: è <b>%s</b>." % (n, why, "primo" if p else "composto")) if n > 1 else None


def s3_scomponi():
    return M5.s4_scomponi()


def s4_fattori():
    k = R.choice(["valore", "divisori", "potenza"])
    if k == "valore":
        a, b, c = R.randint(1, 4), R.randint(0, 2), R.randint(0, 2)
        n = 2 ** a * 3 ** b * 5 ** c
        if n < 10 or n > 2000:
            return None
        f = M5.ff([2] * a + [3] * b + [5] * c).strip()
        return M("Quale numero ha questa scomposizione: %s?" % f, num(n), W(num(2 * a * 3 ** b * 5 ** c), num(n * 2), num(n // 2) if n % 2 == 0 else None, num(2 * a + 3 * b + 5 * c)),
                 "Calcola le potenze e moltiplica: <b>%s</b>." % num(n))
    if k == "divisori":
        a, b = R.randint(1, 4), R.randint(1, 3)
        p, q = R.sample([2, 3, 5, 7], 2)
        n = p ** a * q ** b
        if n > 1000:
            return None
        nd = (a + 1) * (b + 1)
        return M("%s = %s. Quanti divisori ha?" % (num(n), M5.ff([p] * a + [q] * b).strip()), str(nd), W(a * b, a + b, nd + 1, a + b + 2 if a + b + 2 != nd else nd - 1),
                 "Si moltiplicano gli esponenti aumentati di 1: (%d + 1) %s (%d + 1) = <b>%d</b>. Divisori: %s." % (a, FOIS, b, nd, ", ".join(map(str, M5.divisori(n)))))
    n = R.choice([4, 8, 16, 32, 64, 9, 27, 81, 25, 125, 49, 343, 100, 1000])
    for p in (2, 3, 5, 7, 10):
        e = 0
        m = n
        while m % p == 0:
            m //= p
            e += 1
        if m == 1:
            break
    sup = str(e).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return M("%s è una potenza di %d. Con quale esponente?" % (num(n), p), "%d%s" % (p, sup), W("%d%s" % (p, str(e + 1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))), "%d%s" % (p, str(e - 1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))) if e > 1 else "%d²" % n, "%d%s" % (e, str(p).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")))),
             "%s = %s: <b>%d%s</b>." % (num(n), (" %s " % FOIS).join([str(p)] * e), p, sup))


def s5():
    return M5.s5()


def main():
    M5.R = R
    M5.K = Kids(R)
    seen = set()
    sets = [
        ("Multipli e divisori", mix(R, seen, [(M5.s1_multiplo, 10), (M5.s1_lista, 10)])),
        ("Criteri di divisibilità", mix(R, seen, [(s1_crit, 14), (M5.s2_trova, 6)])),
        ("Numeri primi e composti", mix(R, seen, [(s2_primi, 10), (s2_crivello, 10)])),
        ("Scomposizione in fattori primi", mix(R, seen, [(s3_scomponi, 12), (s4_fattori, 8)])),
        ("Divisori, potenze e problemi", mix(R, seen, [(s4_fattori, 10), (s5, 10)])),
    ]
    body = L(["a è <b>multiplo</b> di b (e b è <b>divisore</b> di a) se a : b non ha resto. I multipli di un numero sono infiniti, i divisori sono finiti.",
              "Criteri: per 2 ultima cifra pari; per 3 (e 9) somma delle cifre multipla di 3 (di 9); per 5 ultima cifra 0 o 5; per 4 (e 25) le ultime due cifre; per 10 ultima cifra 0; per 11 differenza tra le cifre di posto dispari e pari.",
              "Un numero <b>primo</b> ha esattamente due divisori: 1 e sé stesso. 1 non è primo. Gli altri numeri maggiori di 1 sono <b>composti</b>.",
              "Ogni numero composto si scompone in modo unico in <b>fattori primi</b>: 360 = 2³ × 3² × 5."],
             [("Scomponi 180", ["180 : 2 = 90", "90 : 2 = 45", "45 : 3 = 15", "15 : 3 = 5", "5 : 5 = 1"], "2² × 3² × 5")],
             [["Considerare 1 un numero primo", "1 ha un solo divisore: non è primo."],
              ["Fermarsi a un fattore composto: 36 = 4 × 9", "Continua: 4 = 2², 9 = 3², quindi 36 = 2² × 3²."],
              ["Usare il criterio del 3 sull’ultima cifra", "Per il 3 si sommano tutte le cifre."]],
             table(["Divisibile per", "Criterio"], [["2", "ultima cifra pari"], ["3", "somma delle cifre multipla di 3"], ["4", "ultime due cifre multiple di 4 (o 00)"], ["5", "ultima cifra 0 o 5"], ["9", "somma delle cifre multipla di 9"], ["10", "ultima cifra 0"]]))
    faq = [("Quanti sono i numeri primi?", "Infiniti: lo dimostrò Euclide più di 2000 anni fa. Non esiste un numero primo «più grande di tutti»."),
           ("A che cosa serve la scomposizione in fattori primi?", "A trovare MCD e mcm, a semplificare le frazioni e a capire quanti divisori ha un numero.")]
    unit(G, R, "divisibilita-e-numeri-primi", "N",
         "Individuare multipli e divisori di un numero naturale; conoscere i criteri di divisibilità; scomporre numeri naturali in fattori primi e conoscere l’utilità di tale scomposizione",
         "Divisibilità, numeri primi e scomposizione in fattori", "Divisibilità e numeri primi",
         "Schede di matematica per la prima media su divisibilità e numeri primi: multipli e divisori, criteri di divisibilità, numeri primi e composti, scomposizione in fattori primi, numero dei divisori e problemi. 100 esercizi con soluzioni.",
         "Un numero primo ha solo due divisori: 1 e sé stesso.", "Ogni numero composto si scompone in modo unico in fattori primi.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
