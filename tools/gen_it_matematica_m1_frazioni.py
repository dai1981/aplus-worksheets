# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Le frazioni (Numeri)
  python3 tools/gen_it_matematica_m1_frazioni.py
Frazione come operatore, frazioni proprie, improprie, apparenti, numeri misti, frazioni equivalenti, proprietà
invariantiva, ridurre ai minimi termini con il MCD, ridurre allo stesso denominatore con il mcm, confrontare e ordinare.
Errori: semplificare sottraendo, confrontare solo i denominatori, ridurre al denominatore comune senza cambiare i numeratori.
"""
import random
from math import gcd
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, Kids
import gen_it_matematica_c5_frazioni as F5

R = random.Random(71108)
G = "prima-media"


def s2_riduci():
    a, b = R.randint(1, 9), R.randint(2, 12)
    if gcd(a, b) != 1 or a == b:
        return None
    k = R.randint(2, 12)
    n, d = a * k, b * k
    return M("Riduci ai minimi termini: %s" % F5.F(n, d), F5.F(a, b),
             W(F5.F(n // 2, d // 2) if n % 2 == 0 and d % 2 == 0 and k != 2 else None, F5.F(n - k, d - k) if n > k else None, F5.F(b, a), F5.F(a + 1, b) if a + 1 != b else F5.F(a, b + 1)),
             "MCD(%d, %d) = %d: dividi numeratore e denominatore per %d. <b>%s</b>." % (n, d, k, k, F5.F(a, b)))


def s2_mcd():
    a, b = R.randint(2, 9), R.randint(2, 12)
    c, d = R.randint(2, 9), R.randint(2, 12)
    if b == d or gcd(a, b) != 1 or gcd(c, d) != 1 or a >= b or c >= d:
        return None
    m = b * d // gcd(b, d)
    return M("Riduci allo stesso denominatore (il minimo): %s e %s" % (F5.F(a, b), F5.F(c, d)), "%s e %s" % (F5.F(a * m // b, m), F5.F(c * m // d, m)),
             W("%s e %s" % (F5.F(a, m), F5.F(c, m)), "%s e %s" % (F5.F(a * d, b * d), F5.F(c * b, b * d)) if b * d != m else "%s e %s" % (F5.F(a * m // b + 1, m), F5.F(c * m // d, m)), "%s e %s" % (F5.F(a * m // b, m * 2), F5.F(c * m // d, m * 2))),
             "mcm(%d, %d) = %d. %d %s %d = %d e %d %s %d = %d: moltiplica i numeratori per gli stessi numeri. <b>%s e %s</b>." % (b, d, m, m, ":", b, m // b, m, ":", d, m // d, F5.F(a * m // b, m), F5.F(c * m // d, m)))


def s3_ordina():
    fs = set()
    while len(fs) < 4:
        b = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
        a = R.randint(1, b - 1)
        fs.add(Fr(a, b))
    fs = sorted(fs)
    f = lambda L_: "; ".join(fq(x) for x in L_)
    sh = fs[:]
    R.shuffle(sh)
    by_den = sorted(fs, key=lambda x: (x.denominator, x.numerator))
    w = fs[:]
    w[1], w[2] = w[2], w[1]
    return M("Metti in ordine crescente: %s" % f(sh), f(fs), W(f(fs[::-1]), f(by_den) if by_den != fs else None, f(w), f(sorted(fs, key=lambda x: x.numerator))),
             "Riduci allo stesso denominatore e confronta i numeratori: <b>%s</b>." % f(fs))


def main():
    F5.R = R
    seen = set()
    sets = [
        ("Proprie, improprie, apparenti e numeri misti", mix(R, seen, [(F5.s1_tipo, 12), (F5.s1_misto, 8)])),
        ("Frazioni equivalenti", mix(R, seen, [(F5.s2_equivalenti, 8), (F5.s2_mancante, 6), (F5.s2_riduci, 6)])),
        ("Ridurre ai minimi termini e allo stesso denominatore", mix(R, seen, [(s2_riduci, 10), (s2_mcd, 10)])),
        ("Confrontare e ordinare", mix(R, seen, [(F5.s3_confronta, 10), (s3_ordina, 6), (F5.s4_retta, 4)])),
        ("Problemi", mix(R, seen, [(F5.s5, 20)])),
    ]
    F = F5.F
    body = L(["La frazione %s indica che l’intero è diviso in b parti uguali (denominatore) e se ne prendono a (numeratore). È anche un operatore: %s di 20 = 20 : 4 × 3 = 15." % (F("a", "b"), F(3, 4)),
              "<b>Propria</b> (a &lt; b), <b>impropria</b> (a &gt; b), <b>apparente</b> (a multiplo di b). Un’impropria si può scrivere come numero misto: %s = 2 e %s." % (F(11, 4), F(3, 4)),
              "<b>Proprietà invariantiva</b>: moltiplicando o dividendo numeratore e denominatore per lo stesso numero si ottiene una frazione equivalente. Si riduce ai minimi termini dividendo per il MCD.",
              "Per confrontare frazioni si riducono allo stesso denominatore (il mcm dei denominatori) e si confrontano i numeratori."],
             [("Confronta %s e %s" % (F(5, 6), F(7, 9)), ["mcm(6, 9) = 18", "%s = %s, %s = %s" % (F(5, 6), F(15, 18), F(7, 9), F(14, 18)), "15 &gt; 14"], "%s &gt; %s" % (F(5, 6), F(7, 9)))],
             [["Semplificare sottraendo: %s → %s" % (F(6, 9), F(3, 6)), "Si divide (non si sottrae): %s = %s." % (F(6, 9), F(2, 3))],
              ["Confrontare guardando solo i denominatori", "Porta allo stesso denominatore e confronta i numeratori."],
              ["Cambiare il denominatore senza cambiare il numeratore", "Quello che fai sotto lo fai anche sopra."]],
             table(["Frazione", "Tipo"], [[F(3, 7), "propria"], [F(9, 4), "impropria"], [F(12, 4), "apparente (= 3)"]]))
    faq = [("Perché si riduce ai minimi termini?", "Per lavorare con numeri più piccoli e riconoscere subito frazioni equivalenti: 18/24 e 3/4 sono la stessa frazione."),
           ("Qual è il denominatore comune più comodo?", "Il minimo comune multiplo dei denominatori: con numeri più piccoli si sbaglia meno.")]
    unit(G, R, "frazioni", "N",
         "Utilizzare frazioni equivalenti e la proprietà invariantiva; confrontare e ordinare frazioni riducendole allo stesso denominatore; rappresentarle sulla retta",
         "Le frazioni: equivalenti, minimi termini e confronto", "Frazioni",
         "Schede di matematica per la prima media sulle frazioni: proprie, improprie, apparenti, numeri misti, frazioni equivalenti, minimi termini, minimo comune denominatore, confronto e ordine, problemi. 100 esercizi con soluzioni.",
         "Proprietà invariantiva: stesso numero sopra e sotto.", "Per confrontare: stesso denominatore, poi i numeratori.",
         body, faq, sets, 8)


if __name__ == "__main__":
    main()
