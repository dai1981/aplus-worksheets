# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Massimo comune divisore e minimo comune multiplo (Numeri)
  python3 tools/gen_it_matematica_m1_mcd_e_mcm.py
Divisori comuni e MCD, multipli comuni e mcm, calcolo con la scomposizione in fattori primi (fattori comuni con
l’esponente minore; comuni e non comuni con l’esponente maggiore), numeri primi tra loro, problemi.
Errori: scambiare MCD e mcm, prendere gli esponenti sbagliati, scegliere il prodotto dei due numeri come mcm.
"""
import random
from math import gcd
from it_media import M, L, unit, mix, table, W, num, FOIS, DIV, Kids
import gen_it_matematica_c5_multipli_divisori_e_numeri_primi as M5

R = random.Random(71107)
G = "prima-media"


def lcm(a, b):
    return a * b // gcd(a, b)


def pair(lo=6, hi=90):
    while True:
        a, b = R.randint(lo, hi), R.randint(lo, hi)
        if a != b and gcd(a, b) > 1 and a % b and b % a:
            return a, b


def s1_div_comuni():
    a, b = pair(8, 60)
    dc = [x for x in M5.divisori(a) if b % x == 0]
    f = lambda L_: ", ".join(map(str, L_))
    if R.random() < 0.5:
        return M("Quali sono i divisori comuni di %d e %d?" % (a, b), f(dc), W(f(M5.divisori(a)), f(dc[:-1]) if len(dc) > 1 else None, f(sorted(set(M5.divisori(a)) | set(M5.divisori(b)))), f(dc + [max(dc) * 2])),
                 "Divisori di %d: %s. Di %d: %s. Comuni: <b>%s</b>." % (a, f(M5.divisori(a)), b, f(M5.divisori(b)), f(dc)))
    m = lcm(a, b)
    return M("Qual è il primo multiplo comune (diverso da 0) di %d e %d?" % (a, b), num(m), W(num(a * b) if a * b != m else None, num(gcd(a, b)), num(m * 2), num(max(a, b))),
             "Scrivi i multipli del più grande e cerca il primo che è anche multiplo dell’altro: <b>%s</b>." % num(m))


def fac(n):
    return M5.ff(M5.fattori(n)).strip()


def s2_mcd():
    a, b = pair(12, 200)
    g = gcd(a, b)
    return M("Calcola il MCD di %d e %d." % (a, b), str(g), W(lcm(a, b), g * 2 if a % (g * 2) == 0 or b % (g * 2) == 0 else g + 1, min(a, b), 1),
             "%d = %s; %d = %s. Fattori comuni con l’esponente minore: MCD = <b>%d</b>." % (a, fac(a), b, fac(b), g))


def s2_mcm():
    a, b = pair(4, 60)
    m = lcm(a, b)
    return M("Calcola il mcm di %d e %d." % (a, b), num(m), W(num(a * b) if a * b != m else num(m * 2), num(gcd(a, b)), num(max(a, b)), num(m + max(a, b))),
             "%d = %s; %d = %s. Fattori comuni e non comuni con l’esponente maggiore: mcm = <b>%s</b>." % (a, fac(a), b, fac(b), num(m)))


def s3_tre():
    a, b, c = R.sample([4, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30], 3)
    if R.random() < 0.5:
        g = gcd(gcd(a, b), c)
        return M("Calcola il MCD di %d, %d e %d." % (a, b, c), str(g), W(gcd(a, b) if gcd(a, b) != g else None, g * 2, 1 if g != 1 else 2, min(a, b, c)),
                 "%s. MCD = <b>%d</b>." % ("; ".join("%d = %s" % (x, fac(x)) for x in (a, b, c)), g))
    m = lcm(lcm(a, b), c)
    return M("Calcola il mcm di %d, %d e %d." % (a, b, c), num(m), W(num(a * b * c), num(lcm(a, b)), num(m * 2), num(gcd(gcd(a, b), c))),
             "%s. mcm = <b>%s</b>." % ("; ".join("%d = %s" % (x, fac(x)) for x in (a, b, c)), num(m)))


def s3_primi_tra_loro():
    a, b = R.randint(4, 40), R.randint(4, 40)
    if a == b:
        return None
    g = gcd(a, b)
    ok = g == 1
    if R.random() < 0.5:
        return M("%d e %d sono primi tra loro?" % (a, b), "sì, MCD = 1" if ok else "no, MCD = %d" % g, W("no, MCD = %d" % (2 if ok else 1) if not ok else "no, MCD = 2", "sì, perché sono dispari" if ok else "sì, MCD = 1", "solo se sono primi", "sì, MCD = %d" % (a * b)),
                 "MCD(%d, %d) = %d: %s." % (a, b, g, "<b>sono primi tra loro</b>" if ok else "<b>non sono primi tra loro</b>"))
    a, b = R.choice([(8, 15), (9, 14), (7, 12), (10, 21), (4, 9), (5, 12), (11, 20)])
    return M("%d e %d sono primi tra loro. Quanto vale il loro mcm?" % (a, b), str(a * b), W(a + b, max(a, b), 1, a * b * 2), "Se il MCD è 1, il mcm è il prodotto: %d %s %d = <b>%d</b>." % (a, FOIS, b, a * b))


def s4_quale():
    k = R.random()
    a, b = pair(8, 60)
    if k < 0.5:
        q, ok = R.choice([("Si vogliono dividere %d caramelle e %d cioccolatini in sacchetti tutti uguali, il più grande numero possibile di sacchetti. Serve…", "il MCD"),
                          ("Due fari si accendono uno ogni %d secondi e l’altro ogni %d secondi. Dopo quanto si accendono di nuovo insieme? Serve…", "il mcm"),
                          ("Si vogliono tagliare due nastri lunghi %d cm e %d cm in pezzi uguali, i più lunghi possibile. Serve…", "il MCD"),
                          ("Due autobus partono insieme: uno passa ogni %d minuti, l’altro ogni %d minuti. Quando ripartono insieme? Serve…", "il mcm")])
        return M(q % (a, b), ok, W("il mcm" if ok == "il MCD" else "il MCD", "il prodotto dei due numeri", "la somma dei due numeri"),
                 "%s" % ("Si cerca il divisore comune più grande: <b>il MCD</b>." if ok == "il MCD" else "Si cerca il primo multiplo comune: <b>il mcm</b>."))
    g, m = gcd(a, b), lcm(a, b)
    return M("MCD(%d, %d) = %d. Quanto vale il mcm? (MCD %s mcm = prodotto dei due numeri)" % (a, b, g, FOIS), num(m), W(num(a * b), num(g * 2), num(a * b // 2) if a * b // 2 != m else None, num(m + g)),
             "%d %s %d %s %d = <b>%s</b>." % (a, FOIS, b, DIV, g, num(m)))


def s5():
    p = K.next()
    k = R.choice(["sacchetti", "nastri", "fari", "bus", "piastrelle", "turni"])
    a, b = pair(12, 90)
    g, m = gcd(a, b), lcm(a, b)
    if k == "sacchetti":
        return M("%s ha %d caramelle e %d cioccolatini. Vuole fare il maggior numero di sacchetti tutti uguali senza avanzi. Quanti sacchetti?" % (p[0], a, b), str(g),
                 W(m, g * 2, a + b, g // 2 if g > 2 else g + 1), "MCD(%d, %d) = <b>%d</b> sacchetti (ognuno con %d caramelle e %d cioccolatini)." % (a, b, g, a // g, b // g))
    if k == "nastri":
        return M("Due nastri sono lunghi %d cm e %d cm. Si tagliano in pezzi uguali, i più lunghi possibile, senza avanzi. Quanto è lungo ogni pezzo?" % (a, b), "%d cm" % g,
                 W("%d cm" % m, "%d cm" % (g * 2), "%d cm" % abs(a - b) if abs(a - b) != g else "1 cm", "%d cm" % min(a, b)), "MCD(%d, %d) = <b>%d cm</b>." % (a, b, g))
    a, b = R.sample([4, 6, 8, 9, 10, 12, 15, 18, 20], 2)
    m = lcm(a, b)
    if k == "fari":
        return M("Due fari si accendono insieme; il primo si riaccende ogni %d secondi, il secondo ogni %d. Dopo quanti secondi si riaccendono insieme?" % (a, b), "%d secondi" % m,
                 W("%d secondi" % (a * b) if a * b != m else "%d secondi" % (m * 2), "%d secondi" % gcd(a, b), "%d secondi" % (a + b)), "mcm(%d, %d) = <b>%d secondi</b>." % (a, b, m))
    if k == "bus":
        return M("Alle 8:00 partono insieme due autobus: uno ogni %d minuti, l’altro ogni %d minuti. Dopo quanti minuti ripartono di nuovo insieme?" % (a, b), "%d minuti" % m,
                 W("%d minuti" % (a * b) if a * b != m else "%d minuti" % (m * 2), "%d minuti" % gcd(a, b), "%d minuti" % (a + b)), "mcm(%d, %d) = <b>%d minuti</b>." % (a, b, m))
    if k == "piastrelle":
        a, b = R.choice([(240, 180), (360, 270), (300, 180), (420, 280), (480, 360)])
        g = gcd(a, b)
        return M("Una stanza misura %d cm × %d cm. Si vuole coprire con piastrelle quadrate tutte uguali, le più grandi possibile, senza tagliarle. Quanto misura il lato di una piastrella?" % (a, b), "%d cm" % g,
                 W("%d cm" % lcm(a, b), "%d cm" % (g // 2), "%d cm" % (g * 2), "%d cm" % (a - b)), "MCD(%d, %d) = <b>%d cm</b>." % (a, b, g))
    return M("Luca va in piscina ogni %d giorni e Marta ogni %d giorni. Oggi ci sono andati insieme. Fra quanti giorni si rivedranno in piscina?" % (a, b), "%d giorni" % m,
             W("%d giorni" % (a * b) if a * b != m else "%d giorni" % (m * 2), "%d giorni" % gcd(a, b), "%d giorni" % (a + b)), "mcm(%d, %d) = <b>%d giorni</b>." % (a, b, m))


K = Kids(R)


def main():
    M5.R = R
    seen = set()
    sets = [
        ("Divisori comuni e multipli comuni", mix(R, seen, [(s1_div_comuni, 20)])),
        ("Il massimo comune divisore", mix(R, seen, [(s2_mcd, 20)])),
        ("Il minimo comune multiplo", mix(R, seen, [(s2_mcm, 20)])),
        ("Tre numeri e numeri primi tra loro", mix(R, seen, [(s3_tre, 10), (s3_primi_tra_loro, 6), (s4_quale, 4)])),
        ("Problemi", mix(R, seen, [(s5, 14), (s4_quale, 6)])),
    ]
    body = L(["Il <b>MCD</b> (massimo comune divisore) è il più grande divisore comune di due o più numeri. Il <b>mcm</b> (minimo comune multiplo) è il più piccolo multiplo comune diverso da 0.",
              "Con la scomposizione: MCD = prodotto dei fattori <b>comuni</b>, presi una volta con l’esponente <b>minore</b>; mcm = prodotto dei fattori <b>comuni e non comuni</b>, con l’esponente <b>maggiore</b>.",
              "Se il MCD è 1 i numeri sono <b>primi tra loro</b> e il mcm è il loro prodotto.",
              "Nei problemi: «il più grande possibile», «dividere in parti uguali» → MCD; «di nuovo insieme», «ogni quanto» → mcm."],
             [("MCD e mcm di 24 e 36", ["24 = 2³ × 3", "36 = 2² × 3²", "MCD = 2² × 3 = 12", "mcm = 2³ × 3² = 72"], "MCD 12, mcm 72")],
             [["Scambiare MCD e mcm", "Il MCD è più piccolo dei numeri (o uguale), il mcm più grande (o uguale)."],
              ["Per il MCD prendere l’esponente maggiore", "MCD: comuni, esponente minore."],
              ["Pensare che il mcm sia sempre il prodotto", "Solo se i numeri sono primi tra loro: mcm(4, 6) = 12, non 24."]],
             table(["", "Fattori", "Esponente"], [["MCD", "solo comuni", "minore"], ["mcm", "comuni e non comuni", "maggiore"]]))
    faq = [("A che cosa servono MCD e mcm?", "Il mcm serve per sommare le frazioni (minimo comune denominatore), il MCD per semplificarle; nei problemi aiutano a dividere in parti uguali o a trovare quando due eventi si ripetono insieme."),
           ("C’è un legame tra MCD e mcm?", "Sì: per due numeri, MCD × mcm = prodotto dei due numeri.")]
    unit(G, R, "mcd-e-mcm", "N",
         "Individuare divisori e multipli comuni a più numeri; comprendere il significato e l’utilità del multiplo comune più piccolo e del divisore comune più grande, in matematica e in situazioni concrete",
         "MCD e mcm: massimo comune divisore e minimo comune multiplo", "MCD e mcm",
         "Schede di matematica per la prima media su MCD e mcm: divisori e multipli comuni, calcolo con la scomposizione in fattori primi, tre numeri, numeri primi tra loro e problemi. 100 esercizi con soluzioni.",
         "MCD: fattori comuni, esponente minore.", "mcm: fattori comuni e non comuni, esponente maggiore.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
