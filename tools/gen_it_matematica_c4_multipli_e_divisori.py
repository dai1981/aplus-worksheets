# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Multipli e divisori (Numeri)
  python3 tools/gen_it_matematica_c4_multipli_e_divisori.py
Multipli di un numero (successione dei multipli), divisori e coppie di fattori, criteri di divisibilità per 2, 3, 5, 10,
numeri primi e composti, problemi con multipli e divisori.
Errori: confondere multiplo e divisore, dimenticare 1 e il numero stesso tra i divisori, credere che ogni dispari sia primo.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids, FOIS, DIV, table
import gen_it_matematica_c5_multipli_divisori_e_numeri_primi as M5

R = random.Random(70405)
G = "classe-quarta"
K = Kids(R)


def s1_successione():
    a = R.randint(3, 15)
    k = R.randint(3, 8)
    seq = [a * i for i in range(k, k + 4)]
    f = lambda L: ", ".join(map(str, L))
    return mcq("Continua la successione dei multipli di %d: %s, …" % (a, f(seq[:3])), str(seq[3]), [str(seq[3] + 1), str(seq[2] + a + a), str(seq[3] - 1), str(seq[2] + 10)],
               "Ogni multiplo si trova aggiungendo %d: %d + %d = <b>%d</b>." % (a, seq[2], a, seq[3]))


def s1_vero():
    a = R.randint(3, 9)
    m = a * R.randint(3, 12)
    q, ok, w = R.choice([("%d è multiplo di %d" % (m, a), True, None), ("%d è divisore di %d" % (a, m), True, None), ("%d è multiplo di %d" % (a, m), False, "%d è più piccolo: è un divisore di %d" % (a, m)),
                         ("%d è divisore di %d" % (m, a), False, "%d è più grande: è un multiplo di %d" % (m, a)), ("%d è multiplo di %d" % (m + 1, a), False, None)])
    if (m + 1) % a == 0 and str(m + 1) in q:
        return None
    if ok:
        return mcq("È vero che %s?" % q, "sì, perché %d %s %d = %d" % (m // a, FOIS, a, m), ["no, è il contrario", "no, %d non sta in %d" % (a, m), "solo se %d è pari" % m],
                   "%d %s %d = %d senza resto: <b>%s</b>." % (m, DIV, a, m // a, q))
    return mcq("È vero che %s?" % q, "no", ["sì", "solo a volte", "non si può sapere"], "<b>No</b>: %s." % (w or "%d %s %d dà resto %d" % (m + 1, DIV, a, (m + 1) % a)))


def s2_coppie():
    n = R.choice([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 64, 72])
    ds = M5.divisori(n)
    d = R.choice([x for x in ds if 1 < x < n])
    other = [x for x in range(2, n) if n % x]
    R.shuffle(other)
    return mcq("%d %s ? = %d. Quale numero manca?" % (d, FOIS, n), str(n // d), [str(n - d), str(n // d + 1), str(other[0]), str(n * d) if n * d < 1000 else None],
               "%d %s %d = <b>%d</b>: %d e %d sono una coppia di divisori di %d." % (n, DIV, d, n // d, d, n // d, n))


def s2_crit():
    return M5.s2_criterio()


def s5():
    p = K.next()
    k = R.choice(["m5", "m5", "biscotti", "giri", "calendario", "squadre"])
    if k == "m5":
        return M5.s5()
    if k == "biscotti":
        n = R.choice([24, 30, 36, 40, 48])
        opts = [d for d in M5.divisori(n) if 2 <= d <= 12]
        bad = [x for x in range(5, 12) if n % x]
        if not bad:
            return None
        d = R.choice(opts)
        b = R.choice(bad)
        return mcq("%s ha %d biscotti. In quale modo li divide in sacchetti uguali senza che ne avanzi nessuno?" % (p[0], n), "sacchetti da %d" % d,
                   ["sacchetti da %d" % b] + ["sacchetti da %d" % x for x in bad if x != b][:2], "%d è divisibile per %d: <b>%d sacchetti da %d</b>." % (n, d, n // d, d))
    if k == "giri":
        a = R.choice([3, 4, 6])
        t = R.choice([24, 30, 36, 48])
        if t % a:
            return None
        return mcq("Un faro si accende ogni %d secondi, la prima volta dopo %d secondi. Quante volte si accende in %d secondi?" % (a, a, t), str(t // a),
                   [str(t // a + 1), str(t - a), str(a)], "Le accensioni sono ai multipli di %d fino a %d: %d %s %d = <b>%d</b>." % (a, t, t, DIV, a, t // a))
    if k == "calendario":
        d = R.choice([3, 4, 5, 6])
        last = R.choice([28, 30, 31])
        days = [x for x in range(d, last + 1, d)]
        return mcq("%s va in piscina ogni %d giorni, a partire dal %d del mese. Quante volte ci va in un mese di %d giorni?" % (p[0], d, d, last), str(len(days)),
                   [str(len(days) + 1), str(len(days) - 1), str(last // 10)], "I giorni sono i multipli di %d: %s. Sono <b>%d</b>." % (d, ", ".join(map(str, days)), len(days)))
    n = R.choice([20, 24, 28, 30, 36])
    g = [d for d in M5.divisori(n) if 2 <= d <= 10]
    return mcq("In palestra ci sono %d bambini. In quanti modi si possono formare squadre uguali con 2–10 bambini ciascuna, senza che nessuno resti fuori?" % n, str(len(g)),
               [str(len(g) + 1), str(len(g) - 1), str(len(M5.divisori(n)))], "Le squadre possono avere %s bambini (divisori di %d tra 2 e 10): <b>%d</b> modi." % (", ".join(map(str, g)), n, len(g)))


def main():
    M5.R = R
    seen = set()
    sets = [
        ("I multipli", mix(R, seen, [(M5.s1_multiplo, 8), (s1_successione, 6), (s1_vero, 6)])),
        ("I divisori", mix(R, seen, [(M5.s1_lista, 8), (s2_coppie, 12)])),
        ("Criteri di divisibilità", mix(R, seen, [(s2_crit, 12), (M5.s2_trova, 8)])),
        ("Numeri primi e composti", mix(R, seen, [(M5.s3_primo, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["I <b>multipli</b> di un numero si ottengono moltiplicandolo per 1, 2, 3, …: i multipli di 6 sono 6, 12, 18, 24, … (sono infiniti).",
         "Un <b>divisore</b> di un numero lo divide senza resto: i divisori di 12 sono 1, 2, 3, 4, 6, 12. Si trovano a coppie: 1 × 12, 2 × 6, 3 × 4.",
         "Criteri: un numero è divisibile per <b>2</b> se finisce con cifra pari, per <b>5</b> se finisce con 0 o 5, per <b>10</b> se finisce con 0, per <b>3</b> se la somma delle cifre è multiplo di 3.",
         "Un numero <b>primo</b> ha solo due divisori: 1 e sé stesso (2, 3, 5, 7, 11, 13 …). Gli altri, tranne 1, sono <b>composti</b>."],
        [("È vero che 4 è divisore di 28?", ["28 : 4 = 7 senza resto", "quindi 28 è multiplo di 4"], "sì")],
        [["Confondere multiplo e divisore", "Il multiplo è più grande (o uguale), il divisore più piccolo (o uguale)."],
         ["Dimenticare 1 e il numero stesso", "Ogni numero è divisibile per 1 e per sé stesso."],
         ["Pensare che 9 o 21 siano primi perché dispari", "9 = 3 × 3, 21 = 3 × 7: sono composti."]],
        table(["Numero", "Divisori", "Primo?"], [["7", "1, 7", "sì"], ["12", "1, 2, 3, 4, 6, 12", "no"], ["13", "1, 13", "sì"], ["15", "1, 3, 5, 15", "no"]]))
    faq = [("Che differenza c’è tra «multiplo di» e «divisore di»?", "Se 24 = 6 × 4, allora 24 è multiplo di 6 e 6 è divisore di 24: sono due modi di dire la stessa relazione."),
           ("Il numero 1 è primo?", "No: un numero primo ha esattamente due divisori, mentre 1 ne ha uno solo.")]
    make_unit(R, "multipli-e-divisori", "N",
              "Individuare multipli e divisori di un numero; conoscere i criteri di divisibilità; riconoscere i numeri primi",
              "Multipli, divisori e numeri primi", "Multipli e divisori",
              "Schede di matematica per la classe quarta su multipli e divisori: successione dei multipli, coppie di divisori, criteri di divisibilità per 2, 3, 5, 10, numeri primi e composti, problemi. 100 esercizi con soluzioni.",
              "Il multiplo è più grande, il divisore è più piccolo.", "Un numero primo ha solo due divisori: 1 e sé stesso.",
              body, faq, sets, 5, grade=G)


if __name__ == "__main__":
    main()
