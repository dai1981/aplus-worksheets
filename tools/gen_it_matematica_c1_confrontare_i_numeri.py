# -*- coding: utf-8 -*-
"""
Italia Matematica classe prima: Confrontare e ordinare i numeri (Numeri)
  python3 tools/gen_it_matematica_c1_confrontare_i_numeri.py
Di più, di meno, tanti quanti (corrispondenza uno a uno); maggiore, minore, uguale (&gt; &lt; =) fino a 20;
il più grande e il più piccolo; ordinare; primo, secondo, terzo… (numeri ordinali).
Errori: pensare che ci siano «più oggetti» dove la fila è più lunga, girare il segno &gt; &lt;.
"""
import random
from it_common import mcq, lesson, make_unit, mix, table
import it_c1 as C
import gen_it_matematica_c2_confrontare_e_ordinare_i_numeri as C2

R = random.Random(70103)
G = "classe-prima"
LT, GT = "&lt;", "&gt;"


def s1_piu():
    k = R.choice(C.KINDS)
    a, b = R.randint(1, 9), R.randint(1, 9)
    q = R.choice(["più", "meno", "uguale"])
    if q == "uguale":
        b = a
        return mcq(C.due(a, k, b, k, "|") + "I due gruppi hanno tanti oggetti quanti?", "sì, tanti quanti", ["no, il primo ne ha di più", "no, il secondo ne ha di più", "non si può sapere"],
                   "%d e %d: sono <b>tanti quanti</b>." % (a, b))
    if a == b:
        return None
    if q == "più":
        g = "il primo" if a > b else "il secondo"
        return mcq(C.due(a, k, b, k, "|") + "Quale gruppo ha più %s?" % C.nome(k), g, ["il primo" if g == "il secondo" else "il secondo", "sono tanti quanti", "nessuno"],
                   "%d e %d: ne ha di più <b>%s</b>." % (a, b, g))
    g = "il primo" if a < b else "il secondo"
    return mcq(C.due(a, k, b, k, "|") + "Quale gruppo ha meno %s?" % C.nome(k), g, ["il primo" if g == "il secondo" else "il secondo", "sono tanti quanti", "nessuno"],
               "%d e %d: ne ha di meno <b>%s</b>." % (a, b, g))


def s1_quanti_in_piu():
    k = R.choice(C.KINDS)
    a, b = R.sample(range(2, 10), 2)
    if a < b:
        a, b = b, a
    return mcq(C.due(a, k, b, k, "|") + "Quante %s in più ci sono nel primo gruppo?" % C.nome(k) if C.COSE[k][2] == "f" else C.due(a, k, b, k, "|") + "Quanti %s in più ci sono nel primo gruppo?" % C.nome(k),
               str(a - b), [str(a), str(b), str(a + b)], "Fai le coppie: ne restano <b>%d</b> senza compagno. %d − %d = %d." % (a - b, a, b, a - b))


def s2_segno():
    a = R.randint(0, 20)
    b = a + R.choice([-3, -2, -1, 0, 1, 2, 3, 5, -5, 10, -10])
    if not 0 <= b <= 20:
        return None
    s = LT if a < b else GT if a > b else "="
    return mcq("Quale segno va tra %d e %d?" % (a, b), s, [LT, GT, "=", "+"],
               "%d %s %d: %s." % (a, s, b, "il becco aperto «mangia» il numero più grande" if s != "=" else "sono uguali"))


def s2_vero():
    a, b = R.sample(range(0, 21), 2)
    s = LT if a < b else GT
    f = lambda x, o, y: "%d %s %d" % (x, o, y)
    return mcq("Confronta %d e %d. Quale scrittura è vera?" % (a, b), f(a, s, b), [f(a, o, b) for o in (LT, GT, "=") if o != s] + [f(b, s, a)],
               "<b>%s</b>: la punta del segno indica il numero più piccolo." % f(a, s, b))


def s3_estremi():
    ns = R.sample(range(0, 21), 4)
    big = R.random() < 0.5
    t = max(ns) if big else min(ns)
    return mcq("Qual è il numero %s: %s?" % ("più grande" if big else "più piccolo", ", ".join(map(str, ns))), str(t), [str(x) for x in ns if x != t],
               "Il %s è <b>%d</b>." % ("più grande" if big else "più piccolo", t))


def s3_ordine():
    ns = sorted(R.sample(range(0, 21), 4))
    cres = R.random() < 0.5
    ok = ns if cres else ns[::-1]
    f = lambda L: ", ".join(map(str, L))
    sh = ns[:]
    R.shuffle(sh)
    w3 = ok[:]
    w3[1], w3[2] = w3[2], w3[1]
    return mcq("Metti in ordine %s: %s" % ("dal più piccolo al più grande" if cres else "dal più grande al più piccolo", f(sh)), f(ok), [f(ok[::-1]), f(w3), f([ok[0], ok[3], ok[1], ok[2]])],
               "In ordine: <b>%s</b>." % f(ok))


def s3_tra():
    a = R.randint(0, 15)
    b = a + R.choice([3, 4, 5])
    x = R.randint(a + 1, b - 1)
    return mcq("Quale numero è maggiore di %d e minore di %d?" % (a, b), str(x), [str(a), str(b), str(b + 1)], "%d &lt; <b>%d</b> &lt; %d." % (a, x, b))


def s5():
    p = R.choice(["Marco", "Giulia", "Luca", "Sofia", "Pietro", "Anna"])
    k = R.choice(["corsa", "altezza", "figurine", "punti", "ord"])
    if k == "ord":
        return C2.s4_ordinali()
    if k == "corsa":
        n = R.randint(3, 6)
        pos = R.randint(1, n)
        m = p in ("Marco", "Luca", "Pietro")
        o = C2.ORD[pos - 1] if m else C2.ORD[pos - 1][:-1] + "a"
        return mcq("In una corsa arrivano %d bambini. %s arriva %s. Quanti bambini arrivano prima di %s?" % (n, p, o, "lui" if m else "lei"), str(pos - 1),
                   [str(pos), str(n - pos) if n - pos != pos - 1 else str(pos + 1), str(n)], "%s vuol dire posizione %d: prima ci sono <b>%d</b> bambini." % (o.capitalize(), pos, pos - 1))
    a, b = R.sample(range(5, 20), 2)
    who = (p, "Mattia") if p != "Mattia" else (p, "Chiara")
    if k == "altezza":
        a, b = R.sample(range(110, 130), 2)
        g = who[0] if a > b else who[1]
        return mcq("%s è alto %d cm, %s è alto %d cm. Chi è più alto?" % (who[0], a, who[1], b), g, [who[1] if g == who[0] else who[0], "sono alti uguali", "non si può sapere"],
                   "%d %s %d: è più alto <b>%s</b>." % (a, GT if a > b else LT, b, g))
    if k == "figurine":
        g = who[0] if a < b else who[1]
        return mcq("%s ha %d figurine, %s ne ha %d. Chi ne ha di meno?" % (who[0], a, who[1], b), g, [who[1] if g == who[0] else who[0], "ne hanno tante uguali", "non si può sapere"],
                   "%d %s %d: ne ha di meno <b>%s</b>." % (a, GT if a > b else LT, b, g))
    g = who[0] if a > b else who[1]
    return mcq("A un gioco %s fa %d punti e %s %d punti. Vince chi fa più punti. Chi vince?" % (who[0], a, who[1], b), g, [who[1] if g == who[0] else who[0], "pareggiano", "non si può sapere"],
               "%d %s %d: vince <b>%s</b>." % (a, GT if a > b else LT, b, g))


def main():
    C2.R = R
    seen = set()
    sets = [
        ("Di più, di meno, tanti quanti", mix(R, seen, [(s1_piu, 14), (s1_quanti_in_piu, 6)])),
        ("Maggiore, minore, uguale", mix(R, seen, [(s2_segno, 12), (s2_vero, 8)])),
        ("Il più grande e il più piccolo", mix(R, seen, [(s3_estremi, 10), (s3_tra, 10)])),
        ("Mettere in ordine", mix(R, seen, [(s3_ordine, 12), (C2.s4_ordinali, 8)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per sapere dove ci sono <b>più</b> oggetti, fai le coppie: chi ne ha qualcuno senza compagno ne ha di più.",
         "I segni: <b>&gt;</b> maggiore, <b>&lt;</b> minore, <b>=</b> uguale. La parte aperta del segno sta verso il numero più grande: 7 &gt; 4, 3 &lt; 9.",
         "Sulla retta dei numeri, andando verso destra i numeri diventano più grandi.",
         "Primo, secondo, terzo, quarto, quinto… dicono il posto in una fila."],
        [("Confronta 12 e 9", ["12 viene dopo 9 contando"], "12 &gt; 9")],
        [["Pensare che la fila più lunga abbia più oggetti", "Conta o fai le coppie: conta il numero, non la lunghezza."],
         ["Girare il segno: 3 &gt; 9", "La punta indica il numero più piccolo: 3 &lt; 9."],
         ["Confondere «terzo» e «tre»", "Terzo dice il posto, tre dice quanti."]],
        table(["Segno", "Si legge", "Esempio"], [["&gt;", "maggiore di", "8 &gt; 5"], ["&lt;", "minore di", "2 &lt; 6"], ["=", "uguale a", "4 = 4"]]))
    faq = [("Come si ricorda il verso dei segni > e <?", "Si può immaginare una bocca di coccodrillo aperta che vuole mangiare il numero più grande."),
           ("Che cosa sono i numeri ordinali?", "Sono le parole che dicono il posto: primo, secondo, terzo… e si scrivono anche 1°, 2°, 3°.")]
    make_unit(R, "confrontare-i-numeri", "N",
              "Confrontare e ordinare i numeri naturali, anche rappresentandoli sulla retta; usare i simboli >, <, =",
              "Confrontare e ordinare i numeri fino a 20", "Confrontare i numeri",
              "Schede di matematica per la classe prima sul confronto dei numeri: di più, di meno, tanti quanti, maggiore, minore, uguale, mettere in ordine, numeri ordinali e problemi. 100 esercizi con soluzioni.",
              "La punta del segno indica il numero più piccolo.", "Verso destra sulla retta i numeri crescono.",
              body, faq, sets, 3, grade=G)


if __name__ == "__main__":
    main()
