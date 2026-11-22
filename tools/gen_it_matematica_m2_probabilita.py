# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Probabilità (Dati e previsioni)
  python3 tools/gen_it_matematica_m2_probabilita.py
Eventi certi, impossibili, probabili; casi favorevoli e casi possibili; probabilità come frazione, decimale e percentuale;
evento contrario (1 − p); frequenza relativa e confronto con la probabilità; problemi con dadi, monete, urne, carte.
Errori: casi favorevoli : casi sfavorevoli, probabilità maggiore di 1, dimenticare che il dado ha 6 facce.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, d, fq, Kids

R = random.Random(71212)
G = "seconda-media"
K = Kids(R)
COL = [("rosse", "rossa"), ("blu", "blu"), ("verdi", "verde"), ("gialle", "gialla"), ("bianche", "bianca"), ("nere", "nera")]


def pc(p):
    p = Fr(p) * 100
    return "%s%%" % d(p) if (p * 10).denominator == 1 else None


def s1_tipo():
    q, a = R.choice([
        ("Lanciando un dado esce un numero minore di 7.", "certo"), ("Lanciando un dado esce il 7.", "impossibile"), ("Lanciando un dado esce il 3.", "probabile"),
        ("Lanciando una moneta esce testa.", "probabile"), ("Da un sacchetto con solo palline rosse si estrae una pallina rossa.", "certo"),
        ("Da un sacchetto con solo palline rosse si estrae una pallina blu.", "impossibile"), ("Lanciando due dadi la somma è 13.", "impossibile"),
        ("Lanciando due dadi la somma è almeno 2.", "certo"), ("Lanciando un dado esce un numero pari.", "probabile"),
        ("Domani il giorno dopo il lunedì sarà martedì.", "certo"), ("Estraendo una carta da un mazzo di 40 carte esce un asso.", "probabile"),
        ("Lanciando un dado esce un numero maggiore di 6.", "impossibile")])
    return M("Di che tipo è questo evento? %s" % q, a, [v for v in ["certo", "impossibile", "probabile"] if v != a] + ["non si può dire"],
             "L’evento è <b>%s</b>%s." % (a, {"certo": ": p = 1", "impossibile": ": p = 0", "probabile": ": 0 &lt; p &lt; 1"}[a]))


def s2_dado():
    ev = R.choice([("un numero pari", [2, 4, 6]), ("un numero dispari", [1, 3, 5]), ("un numero maggiore di 4", [5, 6]), ("un numero minore di 3", [1, 2]),
                   ("il 6", [6]), ("un multiplo di 3", [3, 6]), ("un numero primo", [2, 3, 5]), ("un numero maggiore di 1", [2, 3, 4, 5, 6]),
                   ("un divisore di 6", [1, 2, 3, 6]), ("un numero minore o uguale a 4", [1, 2, 3, 4])])
    f = len(ev[1])
    p = Fr(f, 6)
    return M("Si lancia un dado a 6 facce. Qual è la probabilità che esca %s?" % ev[0], fq(p), W(fq(Fr(f, 6 - f)) if f != 6 and Fr(f, 6 - f) != p else None, fq(Fr(f, 10)), fq(1 - p) if 1 - p != p else fq(Fr(f + 1, 6)), "%d" % f),
             "Casi favorevoli: %s (%d); casi possibili: 6. p = %d/6 = <b>%s</b>." % (", ".join(map(str, ev[1])), f, f, fq(p)))


def s2_urna():
    a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(0, 6)
    cs = R.sample(COL, 3)
    tot = a + b + c
    pick = R.choice([0, 1])
    f = [a, b][pick]
    p = Fr(f, tot)
    desc = "%d palline %s, %d %s" % (a, cs[0][0], b, cs[1][0]) + (" e %d %s" % (c, cs[2][0]) if c else "")
    return M("In un sacchetto ci sono %s. Si estrae una pallina a caso. Qual è la probabilità che sia %s?" % (desc, cs[pick][1]), fq(p), W(fq(Fr(f, tot - f)) if Fr(f, tot - f) != p else None, fq(Fr(1, tot)), fq(1 - p) if 1 - p != p else fq(Fr(f, tot + 1)), fq(Fr(f, 10)) if tot != 10 else fq(Fr(f, 12))),
             "Casi favorevoli: %d; casi possibili: %d. p = <b>%s</b>." % (f, tot, fq(p)))


def s3_forme():
    n = R.choice([4, 5, 8, 10, 20, 25, 50])
    f = R.randint(1, n - 1)
    p = Fr(f, n)
    if pc(p) is None or p == Fr(1, 2):
        return None
    k = R.choice(["dec", "pc"])
    if k == "dec":
        return M("Una probabilità vale %s. Come si scrive come numero decimale?" % fq(p), d(p), W(d(p * 10), d(p / 10), d(Fr(p.numerator, 10)) if p.denominator != 10 else d(p * 100)),
                 "%s = %s : %d = <b>%s</b>." % (fq(p), p.numerator, p.denominator, d(p)))
    return M("Una probabilità vale %s. Quanto vale in percentuale?" % fq(p), pc(p), W(pc(p / 10) if pc(p / 10) else None, "%d%%" % p.numerator, pc(1 - p), "%d%%" % p.denominator),
             "%s = %s = <b>%s</b>." % (fq(p), d(p), pc(p)))


def s3_contrario():
    n = R.choice([6, 8, 10, 12, 20, 25, 40, 50, 100])
    f = R.randint(1, n - 1)
    p = Fr(f, n)
    if p == Fr(1, 2):
        return None
    k = R.choice(["frac", "pc", "pioggia"])
    if k == "pioggia":
        q_ = R.choice([10, 15, 20, 25, 30, 35, 40, 60, 65, 70, 75, 80, 85, 90])
        return M("La probabilità che domani piova è del %d%%. Qual è la probabilità che non piova?" % q_, "%d%%" % (100 - q_), W("%d%%" % q_, "%d%%" % (100 - q_ + 10) if 100 - q_ + 10 <= 100 else "%d%%" % (100 - q_ - 10), "%s%%" % d(Fr(100, q_)) if (Fr(100, q_) * 10).denominator == 1 else "0%", "%d%%" % (100 - q_ - 5), "50%" if q_ != 50 else "40%"),
                 "p(contrario) = 100%% − %d%% = <b>%d%%</b>." % (q_, 100 - q_))
    if k == "pc":
        if pc(p) is None:
            return None
        return M("La probabilità di vincere un gioco è %s. Qual è la probabilità di non vincere?" % pc(p), pc(1 - p), W(pc(p), pc(Fr(1, 1) - p / 10) if pc(Fr(1) - p / 10) else None, pc(Fr(1, 2)) if p != Fr(1, 2) else None, pc(min(1, 1 - p + Fr(1, 10)))),
                 "1 − %s = <b>%s</b>." % (d(p), pc(1 - p)))
    return M("La probabilità di un evento E è %s. Qual è la probabilità dell’evento contrario?" % fq(p), fq(1 - p), W(fq(p), fq(Fr(n - f, f)) if f != n - f else None, fq(Fr(1, n - f)), fq(Fr(n - f + 1, n)), fq(Fr(n - f, n + 1)), fq(Fr(1, n))),
             "p(non E) = 1 − %s = <b>%s</b>." % (fq(p), fq(1 - p)))


def s4_freq():
    k = R.choice(["fr", "conf", "prev"])
    if k == "fr":
        n = R.choice([20, 25, 40, 50, 60, 80, 100, 200])
        f = R.randint(1, n - 1)
        fr = Fr(f, n)
        if pc(fr) is None:
            return None
        obj = R.choice(["testa con una moneta", "il 6 con un dado", "una pallina rossa da un’urna", "il colore rosso con una ruota"])
        return M("Si ripete %d volte l’esperimento «esce %s» e l’evento si verifica %d volte. Qual è la frequenza relativa (in percentuale)?" % (n, obj, f), pc(fr), W("%d%%" % f if f <= 100 and f != fr * 100 else None, pc(1 - fr), pc(fr / 10) if pc(fr / 10) else None, "%d%%" % (n - f) if n - f <= 100 and n - f != fr * 100 else None, pc(fr + Fr(1, 10)) if fr <= Fr(9, 10) else pc(fr - Fr(1, 5)), pc(fr * 2) if fr <= Fr(1, 2) else pc(fr / 2)),
                     "f = %d/%d = %s = <b>%s</b>." % (f, n, d(fr), pc(fr)))
    if k == "prev":
        n = R.choice([60, 120, 300, 600, 1200])
        ev, f = R.choice([("esca il 6", 6), ("esca un numero pari", 2), ("esca un multiplo di 3", 3)])
        return M("Si lancia un dado %s volte. Quante volte ci si aspetta circa che %s?" % (num(n), ev), num(n // f), W(num(n // 6) if f != 6 else num(n // 2), num(n // f * 2), num(n - n // f), num(f)),
                 "p = 1/%d: %s × 1/%d = <b>%s</b> volte (circa)." % (f, num(n), f, num(n // f)))
    q, a, w = R.choice([("Lanciando una moneta 10 volte sono uscite 7 teste. La probabilità di testa al lancio successivo è…", "1/2", ["7/10", "3/10", "1"]),
                        ("Più si ripete un esperimento, più la frequenza relativa…", "si avvicina alla probabilità", ["si allontana dalla probabilità", "diventa 1", "diventa 0"]),
                        ("La frequenza relativa di un evento è sempre un numero…", "tra 0 e 1", ["maggiore di 1", "negativo", "intero"]),
                        ("Se lanciando un dado 600 volte il 6 esce 300 volte, probabilmente il dado…", "è truccato", ["è perfetto", "ha 2 facce", "non si può lanciare"])])
    a2 = a if "/" not in a else fq(Fr(a))
    return M(q, a2, [fq(Fr(x)) if "/" in x else x for x in w], "Risposta: <b>%s</b>." % a2)


def s5():
    p_ = K.next()
    k = R.choice(["carte", "lotteria", "classe", "ruota", "due_monete", "lettere"])
    if k == "carte":
        ev, f = R.choice([("un asso", 4), ("una carta di coppe", 10), ("un re o una regina", 8), ("una figura (fante, cavallo o re)", 12), ("il sette di denari", 1), ("una carta che non sia di spade", 30)])
        p = Fr(f, 40)
        return M("Da un mazzo di 40 carte italiane si estrae una carta. Qual è la probabilità di estrarre %s?" % ev, fq(p), W(fq(Fr(f, 40 - f)), fq(Fr(f, 52)), fq(1 - p), fq(Fr(1, 40)) if f != 1 else fq(Fr(1, 4))), "%d casi favorevoli su 40: p = %d/40 = <b>%s</b>." % (f, f, fq(p)))
    if k == "lotteria":
        n = R.choice([100, 200, 250, 500, 1000])
        b = R.choice([1, 2, 4, 5, 10, 20])
        p = Fr(b, n)
        return M("In una lotteria si vendono %s biglietti e %s ne compra %d. Qual è la probabilità che vinca il primo premio?" % (num(n), p_[0], b), fq(p), W(fq(Fr(b, n - b)), fq(Fr(1, n)) if b != 1 else fq(Fr(1, n - 1)), fq(Fr(1, b)) if b != 1 else fq(Fr(1, 2)), fq(Fr(b, 100)) if n != 100 else fq(Fr(b, 1000)), fq(Fr(n - b, n))), "p = %d/%s = <b>%s</b>." % (b, num(n), fq(p)))
    if k == "classe":
        m, f = R.randint(8, 15), R.randint(8, 15)
        if m == f:
            return None
        p = Fr(f, m + f)
        return M("In una classe ci sono %d maschi e %d femmine. Si estrae a sorte un alunno per l’interrogazione. Qual è la probabilità che sia una femmina?" % (m, f), fq(p), W(fq(Fr(f, m)), fq(Fr(m, m + f)), fq(Fr(1, m + f))), "p = %d/%d = <b>%s</b>." % (f, m + f, fq(p)))
    if k == "ruota":
        n = R.choice([8, 10, 12])
        r = R.randint(1, n - 1)
        if 2 * r == n:
            return None
        p = Fr(r, n)
        return M("Una ruota è divisa in %d settori uguali; %d sono rossi. Qual è la probabilità che la ruota si fermi su un settore non rosso?" % (n, r), fq(1 - p), W(fq(p), fq(Fr(n - r, r)) if n - r != r else None, fq(Fr(1, n)), fq(Fr(n - r, 10)) if n != 10 else fq(Fr(n - r, 12))), "Non rossi: %d su %d: p = <b>%s</b>." % (n - r, n, fq(1 - p)))
    if k == "due_monete":
        ev, f = R.choice([("due teste", 1), ("una testa e una croce (in qualsiasi ordine)", 2), ("almeno una testa", 3), ("nessuna testa", 1)])
        return M("Si lanciano due monete. I casi possibili sono TT, TC, CT, CC. Qual è la probabilità di ottenere %s?" % ev, fq(Fr(f, 4)), W(fq(Fr(f, 3)), fq(Fr(f, 2)) if Fr(f, 2) != Fr(f, 4) else None, fq(1 - Fr(f, 4)) if 1 - Fr(f, 4) != Fr(f, 4) else fq(Fr(1, 3)), fq(Fr(1, 2)) if f != 2 else fq(Fr(1, 3))),
                 "Casi favorevoli: %d su 4: p = <b>%s</b>." % (f, fq(Fr(f, 4))))
    w = R.choice(["MATEMATICA", "PROBABILITA", "GEOMETRIA", "STATISTICA", "CALCOLO"])
    ch = R.choice(sorted(set(w)))
    f = w.count(ch)
    p = Fr(f, len(w))
    return M("Si scrivono le lettere della parola %s su cartoncini uguali e se ne estrae uno. Qual è la probabilità di estrarre la lettera %s?" % (w, ch), fq(p), W(fq(Fr(1, len(set(w)))) if Fr(1, len(set(w))) != p else None, fq(Fr(1, len(w))) if f != 1 else fq(Fr(2, len(w))), fq(Fr(f, len(set(w)))) if Fr(f, len(set(w))) != p else None, fq(1 - p)),
             "La parola ha %d lettere; la %s compare %d volt%s: p = <b>%s</b>." % (len(w), ch, f, "a" if f == 1 else "e", fq(p)))


def main():
    seen = set()
    sets = [
        ("Eventi certi, impossibili, probabili", mix(R, seen, [(s1_tipo, 12), (s2_dado, 8)])),
        ("Probabilità classica", mix(R, seen, [(s2_urna, 20)])),
        ("Frazioni, decimali, percentuali ed evento contrario", mix(R, seen, [(s3_forme, 8), (s3_contrario, 12)])),
        ("Frequenza relativa", mix(R, seen, [(s4_freq, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Un evento è <b>certo</b> se si verifica sempre (p = 1), <b>impossibile</b> se non si verifica mai (p = 0), <b>probabile</b> negli altri casi (0 &lt; p &lt; 1).",
              "Se tutti i casi sono ugualmente possibili: <b>p = casi favorevoli : casi possibili</b>.",
              "La probabilità si scrive come frazione, numero decimale o percentuale: 1/4 = 0,25 = 25%.",
              "L’<b>evento contrario</b> si verifica quando E non si verifica: p(non E) = 1 − p(E).",
              "La <b>frequenza relativa</b> è il numero di volte che l’evento si è verificato diviso il numero di prove. Con molte prove si avvicina alla probabilità."],
             [("Dado: esce un numero maggiore di 4", ["favorevoli: 5, 6 → 2", "possibili: 6"], "p = 2/6 = 1/3")],
             [["Favorevoli : sfavorevoli", "Si divide per tutti i casi possibili, non per quelli sfavorevoli."],
              ["Probabilità maggiore di 1", "La probabilità è sempre tra 0 e 1 (tra 0% e 100%)."],
              ["«È uscita testa 5 volte, ora esce croce»", "La moneta non ricorda: la probabilità resta 1/2."]],
             table(["Evento", "Probabilità"], [["certo", "1 (100%)"], ["impossibile", "0 (0%)"], ["probabile", "tra 0 e 1"], ["contrario di E", "1 − p(E)"]]))
    faq = [("Quante carte ha un mazzo di carte italiane?", "40: quattro semi (coppe, denari, bastoni, spade) di 10 carte ciascuno (dall’asso al 7, fante, cavallo, re)."),
           ("Che differenza c’è tra probabilità e frequenza relativa?", "La probabilità si calcola prima dell’esperimento; la frequenza relativa si misura dopo averlo ripetuto. Con molte prove i due numeri si avvicinano.")]
    unit(G, R, "probabilita", "D",
         "In semplici situazioni aleatorie, individuare gli eventi elementari, assegnare a essi una probabilità, calcolare la probabilità di qualche evento; riconoscere eventi complementari",
         "Probabilità", "Probabilità",
         "Schede di matematica per la seconda media sulla probabilità: eventi certi, impossibili e probabili, casi favorevoli e possibili, evento contrario, frequenza relativa e problemi con dadi, monete e carte. 100 esercizi con soluzioni.",
         "p = casi favorevoli : casi possibili", "Evento contrario: 1 − p.",
         body, faq, sets, 12)


if __name__ == "__main__":
    main()
