# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Probabilità (Dati e previsioni)
  python3 tools/gen_it_matematica_l2_probabilita.py
Eventi, probabilità classica, evento contrario, somma logica (eventi incompatibili e compatibili), prodotto logico
(eventi indipendenti), lancio di due dadi, estrazioni con e senza reimmissione, mazzo di 40 carte, frequenza relativa.
Errori: sommare probabilità di eventi compatibili senza togliere l’intersezione, moltiplicare eventi dipendenti come indipendenti.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, d

R = random.Random(72212)
G = "seconda-liceo"


def PW(*xs):
    return [x for x in W(*xs) if 0 < Fr(x) < 1]


def P_(x):
    return fq(Fr(x))


def s1_urna():
    r, b, v = R.randint(1, 9), R.randint(1, 9), R.randint(0, 6)
    if r == b:
        return None
    tot = r + b + v
    col, n = R.choice([("rossa", r), ("bianca", b)] + ([("verde", v)] if v else []))
    p = Fr(n, tot)
    w = [Fr(n, tot - n) if tot != n else None, Fr(1, 3 if v else 2), 1 - p]
    return M("Un’urna contiene %d palline rosse, %d bianche%s. Si estrae una pallina. Qual è la probabilità che sia %s?" % (r, b, (" e %d verdi" % v) if v else "", col), P_(p), [P_(x) for x in PW(*w) if x != p] + [P_(Fr(n, tot + 1)), P_(Fr(1, tot))],
             "Casi favorevoli %d su %d casi possibili: <b>%s</b>." % (n, tot, P_(p)))


def s1_dado():
    k = R.choice(["pari", "magg", "mult3", "primo", "div"])
    ev = {"pari": ("un numero pari", {2, 4, 6}), "magg": ("un numero maggiore di %d" % 4, {5, 6}), "mult3": ("un multiplo di 3", {3, 6}),
          "primo": ("un numero primo", {2, 3, 5}), "div": ("un divisore di 6", {1, 2, 3, 6})}[k]
    p = Fr(len(ev[1]), 6)
    return M("Si lancia un dado a sei facce. Qual è la probabilità di ottenere %s?" % ev[0], P_(p), [P_(x) for x in PW(Fr(len(ev[1]), 5), 1 - p, Fr(1, 6), Fr(len(ev[1]) + 1, 6)) if x != p],
             "Esiti favorevoli: %s, cioè %d su 6: <b>%s</b>." % (", ".join(map(str, sorted(ev[1]))), len(ev[1]), P_(p)))


SEMI = ["coppe", "denari", "bastoni", "spade"]


def s2_carte():
    k = R.choice(["seme", "figura", "asso", "seme_o_fig", "non_seme", "numero"])
    if k == "seme":
        s = R.choice(SEMI)
        p, e = Fr(10, 40), "Ogni seme ha 10 carte: 10/40 = <b>1/4</b>."
        q = "una carta di %s" % s
    elif k == "figura":
        p, e = Fr(12, 40), "Le figure (fante, cavallo, re) sono 3 per seme, 12 in tutto: 12/40 = <b>3/10</b>."
        q = "una figura"
    elif k == "asso":
        p, e = Fr(4, 40), "Gli assi sono 4: 4/40 = <b>1/10</b>."
        q = "un asso"
    elif k == "seme_o_fig":
        s = R.choice(SEMI)
        p, e = Fr(10 + 12 - 3, 40), "Eventi compatibili: 10/40 + 12/40 − 3/40 (le figure di %s contate due volte) = <b>19/40</b>." % s
        q = "una carta di %s oppure una figura" % s
    elif k == "non_seme":
        s = R.choice(SEMI)
        p, e = Fr(30, 40), "Evento contrario: 1 − 10/40 = <b>3/4</b>."
        q = "una carta che non sia di %s" % s
    else:
        n = R.randint(2, 6)
        p, e = Fr(4 * (7 - n + 1), 40), "Le carte numerate da %d a 7 sono %d per seme, %d in tutto: <b>%s</b>." % (n, 8 - n, 4 * (8 - n), P_(Fr(4 * (8 - n), 40)))
        q = "una carta con un numero da %d a 7" % n
    w = [Fr(1, 4) if p != Fr(1, 4) else Fr(1, 10), Fr(22, 40) if k == "seme_o_fig" else Fr(3, 10) if p != Fr(3, 10) else Fr(1, 3), 1 - p if 1 - p != p else Fr(1, 3), Fr(1, 40)]
    return M("Da un mazzo di 40 carte (coppe, denari, bastoni, spade; dall’asso al 7, fante, cavallo, re) si pesca una carta. Qual è la probabilità di pescare %s?" % q, P_(p), [P_(x) for x in PW(*w) if x != p], e)


def s2_contr():
    p = Fr(R.choice([x for x in range(1, 20) if x != 10]), 20)
    ev = R.choice(["piova domani", "una lampadina sia difettosa", "un tiro vada a canestro", "il treno arrivi in ritardo"])
    return M("La probabilità che %s è %s. Qual è la probabilità dell’evento contrario?" % (ev, d(p)), d(1 - p), [d(x) for x in PW(p, Fr(1, 2) if p != Fr(1, 2) else Fr(1, 4), 1 - p / 2, p * p)],
             "P(Ā) = 1 − P(A) = 1 − %s = <b>%s</b>." % (d(p), d(1 - p)))


def s3_due_dadi():
    k = R.choice(["somma", "doppio", "almeno6", "somma_magg", "diff", "pari"])
    if k == "diff":
        t = R.randint(1, 4)
        n = 2 * (6 - t)
        p = Fr(n, 36)
        return M("Si lanciano due dadi. Qual è la probabilità che la differenza tra il numero maggiore e il minore sia %d?" % t, P_(p), [P_(x) for x in PW(Fr(1, 6), Fr(6 - t, 36), Fr(n, 30), Fr(n + 2, 36)) if x != p],
                 "Le coppie (ordinate) con differenza %d sono %d su 36: <b>%s</b>." % (t, n, P_(p)))
    if k == "pari":
        t = R.choice(["somma", "prodotto"])
        p = Fr(1, 2) if t == "somma" else Fr(27, 36)
        return M("Si lanciano due dadi. Qual è la probabilità che il %s dei due numeri sia pari?" % t, P_(p), [P_(x) for x in PW(Fr(1, 4), Fr(1, 2) if p != Fr(1, 2) else Fr(3, 4), Fr(1, 3), Fr(18, 36) if False else Fr(2, 3)) if x != p],
                 ("La somma è pari se i numeri sono entrambi pari o entrambi dispari: 9 + 9 = 18 coppie su 36, <b>1/2</b>." if t == "somma" else "Il prodotto è dispari solo se tutti e due sono dispari (9 coppie): 1 − 9/36 = <b>3/4</b>."))
    if k == "somma":
        s = R.randint(2, 12)
        n = 6 - abs(s - 7)
        p = Fr(n, 36)
        e = "Le coppie con somma %d sono %d su 36: <b>%s</b>." % (s, n, P_(p))
        q = "la somma sia %d" % s
        w = [Fr(1, 11), Fr(n, 12), Fr(1, 36) if n != 1 else Fr(2, 36), Fr(n + 1, 36)]
    elif k == "doppio":
        p = Fr(6, 36)
        e = "Le coppie uguali sono 6 su 36: <b>1/6</b>."
        q = "escano due numeri uguali"
        w = [Fr(1, 36), Fr(1, 12), Fr(1, 3)]
    elif k == "almeno6":
        p = 1 - Fr(25, 36)
        t = R.randint(1, 6)
        e = "Evento contrario «nessun %d»: (5/6)² = 25/36; quindi 1 − 25/36 = <b>11/36</b>." % t
        q = "esca almeno un %d" % t
        w = [Fr(1, 3), Fr(2, 6), Fr(1, 36), Fr(25, 36)]
    else:
        s = R.randint(8, 11)
        n = sum(6 - abs(t - 7) for t in range(s + 1, 13))
        p = Fr(n, 36)
        e = "Somme maggiori di %d: %d coppie su 36, <b>%s</b>." % (s, n, P_(p))
        q = "la somma sia maggiore di %d" % s
        w = [Fr(12 - s, 11), Fr(n, 12), Fr(n + 6 - abs(s - 7), 36), Fr(12 - s, 36), Fr(n + 1, 36)]
    return M("Si lanciano due dadi. Qual è la probabilità che %s?" % q, P_(p), [P_(x) for x in PW(*w) if x != p], e)


def s4_estr():
    r, b = R.randint(2, 7), R.randint(2, 7)
    tot = r + b
    k = R.choice(["con", "senza"])
    if k == "con":
        p = Fr(r, tot) ** 2
        return M("Un’urna contiene %d palline rosse e %d blu. Si estraggono due palline <b>con reimmissione</b>. Qual è la probabilità che siano entrambe rosse?" % (r, b), P_(p),
                 [P_(x) for x in PW(Fr(r * (r - 1), tot * (tot - 1)), Fr(2 * r, tot), Fr(r, tot), Fr(r * r, tot)) if x != p],
                 "Le estrazioni sono indipendenti: (%d/%d) · (%d/%d) = <b>%s</b>." % (r, tot, r, tot, P_(p)))
    p = Fr(r * (r - 1), tot * (tot - 1))
    return M("Un’urna contiene %d palline rosse e %d blu. Si estraggono due palline <b>senza reimmissione</b>. Qual è la probabilità che siano entrambe rosse?" % (r, b), P_(p),
             [P_(x) for x in PW(Fr(r, tot) ** 2, Fr(r - 1, tot - 1), Fr(r, tot), Fr(2 * r - 1, 2 * tot)) if x != p],
             "Dopo la prima rossa restano %d %s su %d palline: (%d/%d) · (%d/%d) = <b>%s</b>." % (r - 1, "rossa" if r - 1 == 1 else "rosse", tot - 1, r, tot, r - 1, tot - 1, P_(p)))


def s4_indip():
    a, b = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    k = R.choice(["e", "o"])
    n1, n2 = R.sample(["Giulia", "Marco", "Sofia", "Luca", "Chiara", "Pietro"], 2)
    if k == "e":
        p = a * b
        return M("%s supera una prova con probabilità %s e %s con probabilità %s, in modo indipendente. Qual è la probabilità che la superino entrambi?" % (n1, d(a), n2, d(b)), d(p), [d(x) for x in PW(a + b if a + b <= 1 else None, (a + b) / 2, a + b - a * b, 1 - a * b, (1 - a) * (1 - b)) if x != p],
                 "Eventi indipendenti: P(A ∩ B) = P(A) · P(B) = <b>%s</b>." % d(p))
    p = a + b - a * b
    return M("%s supera una prova con probabilità %s e %s con probabilità %s, in modo indipendente. Qual è la probabilità che almeno uno dei due la superi?" % (n1, d(a), n2, d(b)), d(p), [d(x) for x in PW(a + b if a + b <= 1 else None, a * b, 1 - a * b, (a + b) / 2) if x != p],
             "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = %s + %s − %s = <b>%s</b>." % (d(a), d(b), d(a * b), d(p)))


def s5_freq():
    n = R.choice([50, 80, 100, 200, 250, 400, 500])
    k = R.randint(5, n // 2)
    f = Fr(k, n)
    try:
        d(f)
    except ValueError:
        return None
    m = R.choice([1000, 2000, 5000])
    return M("Su %d pezzi controllati, %d sono difettosi. Secondo la frequenza relativa, quanti difettosi ci si aspetta su %d pezzi?" % (n, k, m), str(int(f * m)) if (f * m).denominator == 1 else None or d(f * m),
             [str(x) for x in W(k * (m // n) // 2 if (f * m).denominator == 1 else None, k, int(f * m) + 10, m - int(f * m))],
             "Frequenza relativa %d/%d = %s; stima %s · %d = <b>%s</b>." % (k, n, d(f), d(f), m, d(f * m)))


def main():
    seen = set()
    sets = [
        ("Probabilità classica", mix(R, seen, [(s1_urna, 10), (s1_dado, 5), (s2_contr, 5)])),
        ("Il mazzo di 40 carte", mix(R, seen, [(s2_carte, 12), (s2_contr, 8)])),
        ("Due dadi", mix(R, seen, [(s3_due_dadi, 20)])),
        ("Estrazioni ed eventi indipendenti", mix(R, seen, [(s4_estr, 12), (s4_indip, 8)])),
        ("Frequenza e problemi", mix(R, seen, [(s5_freq, 8), (s4_indip, 6), (s4_estr, 6)])),
    ]
    body = L(["La <b>probabilità classica</b> di un evento è il rapporto tra casi favorevoli e casi possibili, se tutti i casi sono ugualmente possibili. Vale 0 per l’evento impossibile e 1 per quello certo.",
              "<b>Evento contrario</b>: P(Ā) = 1 − P(A). <b>Somma logica</b>: P(A ∪ B) = P(A) + P(B) − P(A ∩ B); se A e B sono incompatibili, P(A ∩ B) = 0.",
              "<b>Eventi indipendenti</b>: P(A ∩ B) = P(A) · P(B). Nelle estrazioni <b>senza reimmissione</b> la seconda probabilità cambia perché nell’urna c’è una pallina in meno.",
              "Lanciando due dadi ci sono 36 coppie ugualmente probabili. La <b>frequenza relativa</b> di molte prove stima la probabilità."],
             [("Due dadi: somma 7", ["Coppie (1;6), (2;5), (3;4), (4;3), (5;2), (6;1)"], "6/36 = 1/6"),
              ("Urna 3 rosse e 2 blu, due estrazioni senza reimmissione: due rosse", ["3/5 · 2/4"], "3/10")],
             [["P(carta di coppe o figura) = 10/40 + 12/40", "Le figure di coppe sono contate due volte: si tolgono 3/40."],
              ["Senza reimmissione: 3/5 · 3/5", "Dopo la prima estrazione cambiano i casi: 3/5 · 2/4."],
              ["P(almeno un 6) = 2/6", "Meglio l’evento contrario: 1 − (5/6)² = 11/36."]])
    faq = [("Che differenza c’è tra eventi incompatibili e indipendenti?", "Incompatibili: non possono accadere insieme (P(A ∩ B) = 0). Indipendenti: il verificarsi di uno non cambia la probabilità dell’altro (P(A ∩ B) = P(A) · P(B))."),
           ("Perché nel lancio di due dadi le somme non sono equiprobabili?", "Perché le somme si ottengono con numeri diversi di coppie: la somma 7 con 6 coppie, la somma 2 con una sola (1; 1).")]
    unit(G, R, "probabilita", "Q",
         "Probabilità classica e frequentista; evento contrario, somma e prodotto logico di eventi; eventi indipendenti",
         "Probabilità", "Probabilità",
         "Schede di matematica per la seconda liceo sulla probabilità: probabilità classica, evento contrario, eventi compatibili e incompatibili, mazzo di 40 carte, due dadi, estrazioni con e senza reimmissione, eventi indipendenti. 100 esercizi con soluzioni.",
         "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "Eventi indipendenti: P(A ∩ B) = P(A) · P(B). Evento contrario: 1 − P(A).",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
