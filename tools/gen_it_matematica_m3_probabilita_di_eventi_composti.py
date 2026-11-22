# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Probabilità di eventi composti (Dati e previsioni)
  python3 tools/gen_it_matematica_m3_probabilita_di_eventi_composti.py
Eventi incompatibili (p(A o B) = p(A) + p(B)), compatibili (− p(A e B)), eventi indipendenti (p(A e B) = p(A) × p(B)),
due dadi e la tabella dei 36 casi, monete, estrazioni con e senza reimmissione, «almeno uno» con l’evento contrario.
Errori: sommare probabilità di eventi compatibili senza togliere l’intersezione, sommare invece di moltiplicare, dimenticare che senza reimmissione i casi diminuiscono.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from it_media import M, L, unit, mix, table, W, fq, Kids

R = random.Random(71312)
G = "terza-media"
K = Kids(R)
COL = [("rosse", "rossa"), ("blu", "blu"), ("verdi", "verde"), ("gialle", "gialla"), ("bianche", "bianca"), ("nere", "nera")]


def s1_tipo():
    q, a = R.choice([
        ("Lanciando un dado: «esce 2» e «esce 5».", "incompatibili"), ("Lanciando un dado: «esce un numero pari» e «esce un numero maggiore di 3».", "compatibili"),
        ("Lanciando un dado: «esce un numero pari» e «esce un numero dispari».", "incompatibili"), ("Estraendo una carta: «è un asso» e «è di coppe».", "compatibili"),
        ("Estraendo una carta: «è un re» e «è un asso».", "incompatibili"), ("Lanciando un dado: «esce un multiplo di 3» e «esce un numero pari».", "compatibili"),
        ("Lanciando un dado: «esce 1» e «esce un numero primo».", "incompatibili"), ("Estraendo un numero da 1 a 20: «è pari» e «è multiplo di 5».", "compatibili")])
    return M("Gli eventi sono compatibili o incompatibili? %s" % q, a, ["compatibili" if a == "incompatibili" else "incompatibili", "indipendenti", "contrari"],
             "Possono verificarsi insieme? %s: <b>%s</b>." % ("Sì" if a == "compatibili" else "No", a))


def dado_ev():
    return R.choice([("un numero pari", {2, 4, 6}), ("un numero dispari", {1, 3, 5}), ("un numero maggiore di 4", {5, 6}), ("un numero minore di 3", {1, 2}), ("un multiplo di 3", {3, 6}), ("un numero primo", {2, 3, 5}), ("il 6", {6}), ("l’1", {1}), ("un numero maggiore di 3", {4, 5, 6})])


def s2_somma():
    (na, A), (nb, B) = R.sample([dado_ev() for _ in range(6)], 2)
    if na == nb or A == B:
        return None
    U = A | B
    p = Fr(len(U), 6)
    if p == 1:
        return None
    comp = bool(A & B)
    wrong = [Fr(len(A) + len(B), 6), Fr(len(A & B), 6) if A & B else Fr(len(A) * len(B), 36), Fr(len(A), 6) * Fr(len(B), 6), 1 - p, Fr(len(U) - 1, 6), Fr(len(U) + 1, 6), Fr(len(A), 6)]
    return M("Si lancia un dado. Qual è la probabilità che esca %s oppure %s?" % (na, nb), fq(p), W(*[fq(w) for w in wrong if w != p and w <= 1]),
             ("Gli eventi sono compatibili (in comune: %s): %d/6 + %d/6 − %d/6 = <b>%s</b>." % (", ".join(map(str, sorted(A & B))), len(A), len(B), len(A & B), fq(p))) if comp else
             "Gli eventi sono incompatibili: %d/6 + %d/6 = <b>%s</b>." % (len(A), len(B), fq(p)))


def s3_due_dadi():
    k = R.choice(["somma", "somma", "doppio", "entrambi", "prodotto"])
    cases = list(product(range(1, 7), repeat=2))
    if k == "somma":
        s = R.randint(2, 12)
        f = sum(1 for a, b in cases if a + b == s)
        p = Fr(f, 36)
        return M("Si lanciano due dadi. Qual è la probabilità che la somma sia %d?" % s, fq(p), W(fq(Fr(1, 11)), fq(Fr(f, 12)) if Fr(f, 12) != p else None, fq(Fr(1, 6)) if p != Fr(1, 6) else fq(Fr(1, 12)), fq(Fr(f + 1, 36))),
                 "Su 36 casi, quelli con somma %d sono %d: p = %d/36 = <b>%s</b>." % (s, f, f, fq(p)))
    if k == "doppio":
        return M("Si lanciano due dadi. Qual è la probabilità di ottenere due numeri uguali?", fq(Fr(1, 6)), [fq(Fr(1, 36)), fq(Fr(1, 12)), fq(Fr(2, 6))], "I casi (1;1), (2;2)… (6;6) sono 6 su 36: <b>1/6</b>.")
    if k == "entrambi":
        (na, A), (nb, B) = dado_ev(), dado_ev()
        p = Fr(len(A), 6) * Fr(len(B), 6)
        return M("Si lanciano due dadi. Qual è la probabilità che sul primo esca %s e sul secondo %s?" % (na, nb), fq(p), W(fq(Fr(len(A), 6) + Fr(len(B), 6)) if Fr(len(A), 6) + Fr(len(B), 6) <= 1 else fq(Fr(len(A) + len(B), 12)), fq(Fr(len(A) * len(B), 12)), fq(Fr(len(A) + len(B), 36)), fq(Fr(len(A), 6)), fq(p * 2), fq(Fr(1, 36)) if p != Fr(1, 36) else fq(Fr(1, 12))),
                 "Eventi indipendenti: %s × %s = <b>%s</b>." % (fq(Fr(len(A), 6)), fq(Fr(len(B), 6)), fq(p)))
    t = R.choice([6, 12, 4, 36, 10])
    f = sum(1 for a, b in cases if a * b == t)
    if f == 0:
        return None
    p = Fr(f, 36)
    return M("Si lanciano due dadi. Qual è la probabilità che il prodotto dei due numeri sia %d?" % t, fq(p), W(fq(Fr(f, 6)), fq(Fr(1, 36)) if f != 1 else fq(Fr(2, 36)), fq(Fr(f + 1, 36)), fq(Fr(f, 12))),
             "Casi con prodotto %d: %s → %d su 36: <b>%s</b>." % (t, ", ".join("(%d;%d)" % (a, b) for a, b in cases if a * b == t), f, fq(p)))


def s4_estrazioni():
    a, b = R.randint(2, 7), R.randint(2, 7)
    cs = R.sample(COL, 2)
    n = a + b
    k = R.choice(["con", "senza", "senza"])
    if k == "con":
        p = Fr(a, n) * Fr(a, n)
        return M("Un sacchetto contiene %d palline %s e %d %s. Si estrae una pallina, la si rimette nel sacchetto e se ne estrae un’altra. Qual è la probabilità che siano entrambe %s?" % (a, cs[0][0], b, cs[1][0], cs[0][0]), fq(p), W(fq(Fr(a, n) * Fr(a - 1, n - 1)), fq(Fr(2 * a, n)) if 2 * a <= n else fq(Fr(a, 2 * n)), fq(Fr(a, n)), fq(Fr(2 * a, n * n))),
                 "Con reimmissione: %s × %s = <b>%s</b>." % (fq(Fr(a, n)), fq(Fr(a, n)), fq(p)))
    p = Fr(a, n) * Fr(a - 1, n - 1)
    return M("Un sacchetto contiene %d palline %s e %d %s. Si estraggono due palline una dopo l’altra senza rimetterle. Qual è la probabilità che siano entrambe %s?" % (a, cs[0][0], b, cs[1][0], cs[0][0]), fq(p), W(fq(Fr(a, n) * Fr(a, n)), fq(Fr(a, n)), fq(Fr(a - 1, n - 1)), fq(Fr(a, n) * Fr(a - 1, n))),
             "Senza reimmissione: %s × %s = <b>%s</b> (alla seconda estrazione le palline sono una in meno)." % (fq(Fr(a, n)), fq(Fr(a - 1, n - 1)), fq(p)))


def s5_almeno():
    k = R.choice(["monete", "dadi6", "tiri"])
    if k == "monete":
        n = R.randint(2, 5)
        p = 1 - Fr(1, 2 ** n)
        return M("Si lanciano %d monete. Qual è la probabilità di ottenere almeno una testa?" % n, fq(p), W(fq(Fr(1, 2 ** n)), fq(Fr(n, 2 ** n)), fq(Fr(1, 2)), fq(Fr(n - 1, n)), fq(Fr(n, n + 1)), fq(Fr(2 ** n - 1, 2 ** n + 1))),
                 "Contrario: nessuna testa, cioè tutte croci: (1/2)%s = 1/%d. p = 1 − 1/%d = <b>%s</b>." % ("²³⁴⁵"[n - 2], 2 ** n, 2 ** n, fq(p)))
    if k == "dadi6":
        n = R.choice([2, 3])
        p = 1 - Fr(5, 6) ** n
        return M("Si lanciano %d dadi. Qual è la probabilità che esca almeno un 6?" % n, fq(p), W(fq(Fr(n, 6)), fq(Fr(1, 6) ** n), fq(Fr(5, 6) ** n), fq(Fr(1, 6))),
                 "Contrario: nessun 6: (5/6)%s = %s. p = 1 − %s = <b>%s</b>." % ("²³"[n - 2], fq(Fr(5, 6) ** n), fq(Fr(5, 6) ** n), fq(p)))
    q = R.choice([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(3, 5), Fr(4, 5), Fr(1, 3)])
    p = 1 - (1 - q) ** 2
    return M("%s centra il bersaglio con probabilità %s a ogni tiro. Tira due volte. Qual è la probabilità che lo centri almeno una volta?" % (K.next()[0], fq(q)), fq(p), W(fq(q * q), fq((1 - q) ** 2), fq(2 * q) if 2 * q <= 1 else fq(q), fq(q * (1 - q)), fq(q), fq(2 * q * (1 - q))),
             "Contrario: due errori: (%s)² = %s. p = 1 − %s = <b>%s</b>." % (fq(1 - q), fq((1 - q) ** 2), fq((1 - q) ** 2), fq(p)))


def s5_carte():
    ev = R.choice([("un asso o una carta di coppe", 4 + 10 - 1), ("un re o un asso", 8), ("una figura o una carta di denari", 12 + 10 - 3), ("un sette o un otto", 4), ("una carta di spade o di bastoni", 20), ("un due o una carta di coppe", 4 + 10 - 1), ("un asso, un re o un cavallo", 12), ("una carta che non sia una figura", 28), ("un tre oppure il re di spade", 5), ("un fante di coppe oppure una carta di denari", 11)])
    p = Fr(ev[1], 40)
    return M("Si estrae una carta da un mazzo di 40 carte italiane. Qual è la probabilità di estrarre %s?" % ev[0], fq(p), W(fq(Fr(ev[1] + 1, 40)), fq(Fr(ev[1] - 1, 40)) if ev[1] > 1 else None, fq(Fr(ev[1], 52)), fq(1 - p)),
             "Casi favorevoli: %d (senza contare due volte le carte in comune): p = %d/40 = <b>%s</b>." % (ev[1], ev[1], fq(p)))


def main():
    seen = set()
    sets = [
        ("Eventi compatibili e incompatibili", mix(R, seen, [(s1_tipo, 8), (s2_somma, 12)])),
        ("Probabilità totale", mix(R, seen, [(s2_somma, 12), (s5_carte, 8)])),
        ("Due dadi ed eventi indipendenti", mix(R, seen, [(s3_due_dadi, 20)])),
        ("Estrazioni con e senza reimmissione", mix(R, seen, [(s4_estrazioni, 20)])),
        ("Almeno uno: l’evento contrario", mix(R, seen, [(s5_almeno, 20)])),
    ]
    body = L(["Due eventi sono <b>incompatibili</b> se non possono verificarsi insieme: p(A o B) = p(A) + p(B).",
              "Se sono <b>compatibili</b> bisogna togliere i casi in comune: p(A o B) = p(A) + p(B) − p(A e B).",
              "Due eventi sono <b>indipendenti</b> se il primo non influenza il secondo: p(A e B) = p(A) × p(B). Nelle estrazioni <b>senza reimmissione</b> la seconda probabilità cambia.",
              "Per «almeno uno» conviene l’<b>evento contrario</b>: p(almeno uno) = 1 − p(nessuno)."],
             [("Dado: pari oppure maggiore di 4", ["pari: 2, 4, 6; maggiore di 4: 5, 6", "in comune: 6"], "3/6 + 2/6 − 1/6 = 4/6 = 2/3")],
             [["Sommare senza togliere i casi comuni", "Il 6 è pari e maggiore di 4: va contato una volta sola."],
              ["Sommare per «e»", "«e» con eventi indipendenti: si moltiplica."],
              ["Senza reimmissione usare gli stessi casi", "Dopo la prima estrazione c’è una pallina in meno."]],
             table(["Situazione", "Regola"], [["A o B, incompatibili", "p(A) + p(B)"], ["A o B, compatibili", "p(A) + p(B) − p(A e B)"], ["A e B, indipendenti", "p(A) × p(B)"], ["almeno uno", "1 − p(nessuno)"]]))
    faq = [("Quanti sono i casi possibili lanciando due dadi?", "36: per ognuno dei 6 risultati del primo dado ci sono 6 risultati del secondo."),
           ("Con due dadi qual è la somma più probabile?", "Il 7: si ottiene in 6 modi su 36, cioè con probabilità 1/6.")]
    unit(G, R, "probabilita-di-eventi-composti", "D",
         "In semplici situazioni aleatorie, individuare gli eventi elementari, assegnare a essi una probabilità, calcolare la probabilità di qualche evento, scomponendolo in eventi elementari disgiunti; riconoscere coppie di eventi complementari, incompatibili, indipendenti",
         "Probabilità di eventi composti", "Eventi composti",
         "Schede di matematica per la terza media sulla probabilità di eventi composti: eventi compatibili e incompatibili, probabilità totale, eventi indipendenti, due dadi, estrazioni con e senza reimmissione, almeno uno. 100 esercizi con soluzioni.",
         "Incompatibili: si somma. Indipendenti: si moltiplica.", "Almeno uno = 1 − nessuno.",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
