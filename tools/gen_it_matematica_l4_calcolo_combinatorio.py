# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Calcolo combinatorio (Dati e previsioni)
  python3 tools/gen_it_matematica_l4_calcolo_combinatorio.py
Principio moltiplicativo, fattoriale, permutazioni semplici e con ripetizione (anagrammi), disposizioni semplici e con ripetizione,
combinazioni e coefficienti binomiali, proprietà (C(n, k) = C(n, n − k)), problemi (codici, podi, comitati, strette di mano).
Errori: usare le disposizioni quando l’ordine non conta, n! / k! al posto di n!/(n − k)!, anagrammi senza dividere per le ripetizioni.
"""
import math
import random
from collections import Counter
from it_liceo import M, L, unit, mix, table, W, fq, d

R = random.Random(72410)
G = "quarta-liceo"


def D(n, k):
    return math.perm(n, k)


def C(n, k):
    return math.comb(n, k)


def s1_fatt():
    k = R.choice(["fatt", "rapp"])
    if k == "fatt":
        n = R.randint(4, 8)
        v = math.factorial(n)
        return M("Calcola %d!" % n, d(v), [d(x) for x in W(n * (n - 1), math.factorial(n - 1), n * n, sum(range(1, n + 1)))],
                 "%d! = %s = <b>%s</b>." % (n, " · ".join(str(i) for i in range(n, 0, -1)), d(v)))
    n = R.randint(6, 12)
    m = n - R.randint(2, 3)
    v = math.factorial(n) // math.factorial(m)
    return M("Calcola %d! / %d!" % (n, m), d(v), [d(x) for x in W(n - m, math.factorial(n - m), n, v * (m + 1) if v * (m + 1) < 10 ** 6 else v + 1)],
             "Si semplifica %d!: restano i fattori da %d a %d, <b>%s</b>." % (m, m + 1, n, d(v)))


def s2_perm():
    k = R.choice(["fila", "libri", "anag"])
    if k == "anag":
        word = R.choice(["ROMA", "MATEMATICA", "ANNA", "PALLA", "MAMMA", "TORINO", "BOLOGNA", "NAPOLI", "PISA", "LECCE", "BARI", "OTTO", "SASSO", "GENOVA"])
        cnt = Counter(word)
        den = 1
        for c in cnt.values():
            den *= math.factorial(c)
        v = math.factorial(len(word)) // den
        if v > 10 ** 7:
            return None
        rep = [c for c in cnt.values() if c > 1]
        return M("Quanti anagrammi (anche senza senso) si possono formare con le lettere della parola %s?" % word, d(v), [d(x) for x in W(math.factorial(len(word)), v // 2 if den > 1 and v % 2 == 0 else v * 2, len(word) ** 2, v + len(word)) if x != v],
                 "%s%s = <b>%s</b>." % ("%d!" % len(word), (" / (%s)" % " · ".join("%d!" % c for c in rep)) if rep else " (lettere tutte diverse)", d(v)))
    n = R.randint(4, 8)
    v = math.factorial(n)
    q = ("In quanti modi %d amici possono sedersi in fila su %d sedie?" % (n, n)) if k == "fila" else ("In quanti modi si possono ordinare %d libri diversi su uno scaffale?" % n)
    return M(q, d(v), [d(x) for x in W(n * n, 2 ** n, n * (n - 1), math.factorial(n - 1))],
             "Permutazioni di %d oggetti: P<sub>%d</sub> = %d! = <b>%s</b>." % (n, n, n, d(v)))


def s3_disp():
    k = R.choice(["podio", "codice", "rip", "ruoli"])
    if k == "podio":
        n = R.randint(5, 16)
        v = D(n, 3)
        return M("In una gara ci sono %d atleti. In quanti modi diversi si può formare il podio (1°, 2°, 3°)?" % n, d(v), [d(x) for x in W(C(n, 3), n ** 3, 3 * n, math.factorial(n) // 6 if math.factorial(n) < 10 ** 7 else v + 1)],
                 "Conta l’ordine e non ci sono ripetizioni: D<sub>%d,3</sub> = %d · %d · %d = <b>%s</b>." % (n, n, n - 1, n - 2, d(v)))
    if k == "codice":
        L_ = R.randint(3, 5)
        v = 10 ** L_
        return M("Quanti codici di %d cifre (da 0 a 9, anche ripetute) si possono formare?" % L_, d(v), [d(x) for x in W(D(10, L_), C(10, L_), 10 * L_, 9 ** L_)],
                 "Disposizioni con ripetizione: 10<sup>%d</sup> = <b>%s</b>." % (L_, d(v)))
    if k == "rip":
        n, kk = R.choice([(2, 5), (2, 8), (3, 4), (4, 3), (2, 10), (6, 3)])
        v = n ** kk
        ctx = {2: "Si lancia una moneta %d volte. Quante sono le sequenze possibili di testa e croce?", 3: "Una schedina ha %d partite con 3 risultati possibili (1, X, 2). Quante schedine diverse si possono compilare?",
               4: "Quante parole di %d lettere si possono scrivere con le lettere A, B, C, D (anche ripetute)?", 6: "Si lancia un dado %d volte. Quante sono le sequenze possibili dei risultati?"}[n]
        return M(ctx % kk, d(v), [d(x) for x in W(n * kk, kk ** n, D(n, kk) if kk <= n else n * kk + 1, C(n + kk - 1, kk))],
                 "Disposizioni con ripetizione di %d oggetti a %d a %d: %d<sup>%d</sup> = <b>%s</b>." % (n, kk, kk, n, kk, d(v)))
    n = R.randint(6, 28)
    v = D(n, 2)
    return M("Una classe di %d studenti deve eleggere un rappresentante e un vice. In quanti modi?" % n, d(v), [d(x) for x in W(C(n, 2), n * n, 2 * n)],
             "Due ruoli diversi, quindi conta l’ordine: D<sub>%d,2</sub> = %d · %d = <b>%s</b>." % (n, n, n - 1, d(v)))


def s4_comb():
    k = R.choice(["comitato", "strette", "lotto", "calc", "pizza"])
    if k == "calc":
        n = R.randint(5, 12)
        kk = R.randint(2, n - 2)
        v = C(n, kk)
        return M("Calcola il coefficiente binomiale (%d su %d), cioè C<sub>%d,%d</sub>." % (n, kk, n, kk), d(v), [d(x) for x in W(D(n, kk), math.factorial(n) // math.factorial(kk), C(n, kk - 1), n * kk) if x != v],
                 "C<sub>n,k</sub> = n!/(k!(n − k)!) = %d!/(%d! · %d!) = <b>%s</b>." % (n, kk, n - kk, d(v)))
    if k == "strette":
        n = R.randint(5, 20)
        v = C(n, 2)
        return M("A una festa ci sono %d persone e ognuna stringe la mano a tutte le altre una volta. Quante strette di mano ci sono?" % n, d(v), [d(x) for x in W(n * (n - 1), n * n, n - 1, 2 * n)],
                 "Ogni stretta è una coppia non ordinata: C<sub>%d,2</sub> = %d · %d / 2 = <b>%s</b>." % (n, n, n - 1, d(v)))
    if k == "comitato":
        n, kk = R.randint(8, 15), R.choice([3, 4])
        v = C(n, kk)
        return M("Da una classe di %d studenti si sceglie un gruppo di %d per un progetto. Quanti gruppi diversi si possono formare?" % (n, kk), d(v), [d(x) for x in W(D(n, kk), n ** kk if n ** kk < 10 ** 6 else n * kk, n * kk)],
                 "L’ordine non conta: combinazioni C<sub>%d,%d</sub> = <b>%s</b>." % (n, kk, d(v)))
    if k == "pizza":
        n, kk = R.choice([(8, 3), (10, 2), (6, 3), (9, 4), (7, 2)])
        v = C(n, kk)
        return M("Una pizzeria offre %d ingredienti. Quante pizze diverse si possono fare con %d ingredienti diversi?" % (n, kk), d(v), [d(x) for x in W(D(n, kk), n ** kk, n * kk)],
                 "Conta solo quali ingredienti, non l’ordine: C<sub>%d,%d</sub> = <b>%s</b>." % (n, kk, d(v)))
    v = C(90, 5)
    return M("Nel gioco del lotto si estraggono 5 numeri da 90. Quante sono le cinquine possibili (senza ordine)?", d(v), [d(x) for x in W(D(90, 5), 90 ** 5 // 1000, C(90, 4))],
             "C<sub>90,5</sub> = 90 · 89 · 88 · 87 · 86 / 5! = <b>%s</b>." % d(v))


def s5_prop():
    n = R.randint(6, 20)
    k = R.choice(["sim", "somma", "tot"])
    if k == "sim":
        kk = R.randint(2, n - 2)
        return M("Quale coefficiente binomiale è uguale a C<sub>%d,%d</sub>?" % (n, kk), "C<sub>%d,%d</sub>" % (n, n - kk), ["C<sub>%d,%d</sub>" % (n, kk + 1), "C<sub>%d,%d</sub>" % (n - kk, kk), "C<sub>%d,%d</sub>" % (n + kk, kk)],
                 "Scegliere %d elementi equivale a scegliere i %d che restano fuori: C<sub>n,k</sub> = C<sub>n,n−k</sub>, quindi <b>C<sub>%d,%d</sub></b>." % (kk, n - kk, n, n - kk))
    if k == "somma":
        kk = R.randint(1, n - 2)
        return M("A che cosa è uguale C<sub>%d,%d</sub> + C<sub>%d,%d</sub>?" % (n, kk, n, kk + 1), "C<sub>%d,%d</sub>" % (n + 1, kk + 1), ["C<sub>%d,%d</sub>" % (n, kk + 2), "C<sub>%d,%d</sub>" % (2 * n, 2 * kk + 1), "C<sub>%d,%d</sub>" % (n + 1, kk)],
                 "Formula di Stifel (triangolo di Tartaglia): C<sub>n,k</sub> + C<sub>n,k+1</sub> = C<sub>n+1,k+1</sub>: <b>C<sub>%d,%d</sub></b>." % (n + 1, kk + 1))
    n = R.randint(3, 10)
    return M("Quanti sottoinsiemi ha un insieme di %d elementi (somma di tutti i C<sub>%d,k</sub>)?" % (n, n), d(2 ** n), [d(x) for x in W(n * n, math.factorial(n), 2 * n, 2 ** n - 1)],
             "C<sub>n,0</sub> + C<sub>n,1</sub> + … + C<sub>n,n</sub> = 2<sup>n</sup> = <b>%s</b>." % d(2 ** n))


def main():
    seen = set()
    sets = [
        ("Fattoriale e permutazioni", mix(R, seen, [(s1_fatt, 8), (s2_perm, 12)])),
        ("Disposizioni", mix(R, seen, [(s3_disp, 20)])),
        ("Combinazioni", mix(R, seen, [(s4_comb, 20)])),
        ("Anagrammi e proprietà", mix(R, seen, [(s2_perm, 10), (s5_prop, 10)])),
        ("Problemi misti", mix(R, seen, [(s3_disp, 8), (s4_comb, 8), (s5_prop, 4)])),
    ]
    body = L(["<b>Principio moltiplicativo</b>: se una scelta si fa in m modi e una seconda in n modi, insieme si fanno in m · n modi.",
              "<b>Permutazioni</b> di n oggetti: n! = n · (n − 1) · … · 1. Con oggetti ripetuti (anagrammi) si divide per i fattoriali delle ripetizioni.",
              "<b>Disposizioni</b> (conta l’ordine): semplici D<sub>n,k</sub> = n!/(n − k)!, con ripetizione n<sup>k</sup>. <b>Combinazioni</b> (l’ordine non conta): C<sub>n,k</sub> = n!/(k!(n − k)!).",
              "Domanda chiave: <b>conta l’ordine?</b> Se sì, disposizioni; se no, combinazioni."],
             [("Podio con 8 atleti", ["Conta l’ordine", "8 · 7 · 6"], "336"),
              ("Gruppi di 3 da 8 persone", ["L’ordine non conta", "336 / 3!"], "56")],
             [["Usare D quando l’ordine non conta", "Un gruppo {A, B, C} è uno solo: si divide per k!, cioè si usano le combinazioni."],
              ["Anagrammi di ANNA = 4!", "Le lettere ripetute vanno divise: 4!/(2! · 2!) = 6."],
              ["D<sub>n,k</sub> = n!/k!", "D<sub>n,k</sub> = n!/(n − k)!."]])
    faq = [("Che differenza c’è tra disposizioni e combinazioni?", "Nelle disposizioni conta l’ordine (podio, password); nelle combinazioni no (gruppi, mani di carte). Ogni combinazione di k elementi corrisponde a k! disposizioni."),
           ("Perché 0! = 1?", "Per convenzione, così le formule valgono anche quando k = n: c’è un solo modo di ordinare zero oggetti, e C<sub>n,n</sub> = n!/(n! · 0!) = 1.")]
    unit(G, R, "calcolo-combinatorio", "Q",
         "Elementi di calcolo combinatorio: permutazioni, disposizioni, combinazioni, coefficienti binomiali",
         "Calcolo combinatorio", "Calcolo combinatorio",
         "Schede di matematica per la quarta liceo sul calcolo combinatorio: fattoriale, permutazioni e anagrammi, disposizioni semplici e con ripetizione, combinazioni, coefficienti binomiali e loro proprietà, problemi. 100 esercizi con soluzioni.",
         "Conta l’ordine? Disposizioni. Non conta? Combinazioni.", "Dₙ,ₖ = n!/(n − k)!, Cₙ,ₖ = n!/(k!(n − k)!).",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
