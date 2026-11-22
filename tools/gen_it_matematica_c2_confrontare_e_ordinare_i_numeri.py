# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: Confrontare e ordinare i numeri (Numeri)
  python3 tools/gen_it_matematica_c2_confrontare_e_ordinare_i_numeri.py
Maggiore, minore, uguale (&lt; &gt; =), confrontare guardando prima le decine, ordine crescente e decrescente,
il più grande e il più piccolo, numeri sulla retta, numeri ordinali (primo … decimo).
Errori: guardare solo le unità (29 &gt; 31), confondere &lt; e &gt;, crescente e decrescente.
"""
import random
from it_common import mcq, num, lesson, make_unit, mix, Kids
import it_c2 as C

R = random.Random(70202)
G = "classe-seconda"
K = Kids(R)
LT, GT = "&lt;", "&gt;"


def pair():
    a = R.randint(10, 99)
    k = R.choice(["d", "u", "swap"])
    if k == "d":
        b = R.randint(1, 9) * 10 + R.randint(0, 9)
    elif k == "u":
        b = a // 10 * 10 + R.randint(0, 9)
    else:
        b = int(str(a)[::-1]) if a % 10 else a + 5
    return a, b


def s1_simbolo():
    a, b = pair()
    if a == b or b < 10:
        return None
    s = LT if a < b else GT
    f = lambda x, o, y: "%d %s %d" % (x, o, y)
    return mcq("Confronta %d e %d. Quale scrittura è vera?" % (a, b), f(a, s, b), [f(a, o, b) for o in (LT, GT, "=") if o != s] + [f(b, s, a)],
               "Guarda prima le decine, poi le unità: <b>%s</b>. La punta indica il numero più piccolo." % f(a, s, b))


def s1_figure():
    k = R.choice(C.KINDS)
    a, b = R.sample(range(3, 16), 2)
    pic = C.riga(a, k, 10) + C.riga(b, k, 10)
    big = "la prima riga" if a > b else "la seconda riga"
    return mcq(pic + "Dove ci sono più %s?" % C.nome(k), big, ["la seconda riga" if big == "la prima riga" else "la prima riga", "sono uguali", "non si può sapere"],
               "Prima riga: %d, seconda riga: %d. Ce ne sono di più nel%s." % (a, b, "la <b>prima riga</b>" if a > b else "la <b>seconda riga</b>"))


def s2_estremi():
    ns = R.sample(range(10, 100), 4)
    big = R.random() < 0.5
    t = max(ns) if big else min(ns)
    by_u = max(ns, key=lambda x: (x % 10, x)) if big else min(ns, key=lambda x: (x % 10, x))
    return mcq("Qual è il numero %s: %s?" % ("più grande" if big else "più piccolo", ", ".join(map(str, ns))), num(t), [num(by_u)] + [num(x) for x in ns if x != t],
               "Confronta prima le decine: il %s è <b>%d</b>." % ("più grande" if big else "più piccolo", t))


def s2_ordine():
    ns = sorted(R.sample(range(10, 100), 4))
    cres = R.random() < 0.5
    ok = ns if cres else ns[::-1]
    f = lambda L: ", ".join(map(str, L))
    sh = ns[:]
    R.shuffle(sh)
    w3 = ok[:]
    w3[1], w3[2] = w3[2], w3[1]
    return mcq("Metti in ordine %s: %s" % ("crescente (dal più piccolo)" if cres else "decrescente (dal più grande)", f(sh)), f(ok),
               [f(ok[::-1]), f(w3), f(sorted(ns, key=lambda x: (x % 10, x))), f([ok[0], ok[3], ok[1], ok[2]])], "In ordine %s: <b>%s</b>." % ("crescente" if cres else "decrescente", f(ok)))


def s3_retta():
    lo = R.randint(0, 8) * 10
    a, b = R.sample(range(lo + 1, lo + 20), 2)
    if b > 99 or a > 99:
        return None
    pic = C.retta100(lo, lo + 20, [(a, "A"), (b, "B")], 1, 5, 420)
    g = "A" if a > b else "B"
    return mcq(pic + "Quale numero è più grande, A o B?", "%s (%d)" % (g, max(a, b)), ["%s (%d)" % ("B" if g == "A" else "A", min(a, b)), "sono uguali", "%s (%d)" % (g, max(a, b) + 1)],
               "Sulla retta il numero più a destra è il più grande: <b>%s = %d</b>." % (g, max(a, b)))


def s3_tra():
    a = R.randint(10, 80)
    b = a + R.choice([5, 10, 15, 20])
    x = R.randint(a + 1, b - 1)
    return mcq("Quale numero è maggiore di %d e minore di %d?" % (a, b), num(x), [num(a - R.randint(1, 5)), num(b + R.randint(1, 5)), num(b) if R.random() < 0.5 else num(a)],
               "%d &lt; <b>%d</b> &lt; %d." % (a, x, b))


ORD = ["primo", "secondo", "terzo", "quarto", "quinto", "sesto", "settimo", "ottavo", "nono", "decimo"]
ANIM = ["il cane", "il gatto", "il coniglio", "la papera", "il pesce", "la gallina", "il cavallo", "la mucca", "il maiale", "la pecora"]


def s4_ordinali():
    n = R.randint(5, 8)
    fila = R.sample(ANIM, n)
    i = R.randrange(n)
    if R.random() < 0.5:
        return mcq("In fila ci sono: %s. Chi è %s?" % (", ".join(fila), ORD[i]), fila[i], [fila[(i + 1) % n], fila[i - 1], fila[(i + 2) % n]],
                   "Conta dal primo: %s è <b>%s</b>." % (ORD[i], fila[i]))
    return mcq("In fila ci sono: %s. In che posizione è %s?" % (", ".join(fila), fila[i]), ORD[i], [ORD[(i + 1) % 10], ORD[i - 1] if i else ORD[i + 2], ORD[(i + 3) % 10]],
               "Conta: %s è <b>%s</b>." % (fila[i], ORD[i]))


def s5():
    p1, p2 = K.two()
    k = R.choice(["fig", "punti", "alto", "ultimo", "gara"])
    if k == "fig":
        a, b = pair()
        if a == b or b < 10:
            return None
        return mcq("%s ha %d figurine, %s ne ha %d. Chi ne ha di più?" % (p1[0], a, p2[0], b), p1[0] if a > b else p2[0], [p2[0] if a > b else p1[0], "sono uguali", "nessuno"],
                   "%d %s %d: ne ha di più <b>%s</b>." % (max(a, b), GT, min(a, b), p1[0] if a > b else p2[0]))
    if k == "punti":
        a, b = pair()
        if a == b or b < 10:
            return None
        return mcq("In un gioco vince chi fa meno punti. %s fa %d punti, %s ne fa %d. Chi vince?" % (p1[0], a, p2[0], b), p1[0] if a < b else p2[0], [p2[0] if a < b else p1[0], "pareggiano", "vince chi fa più punti"],
                   "%d %s %d: vince <b>%s</b>." % (min(a, b), LT, max(a, b), p1[0] if a < b else p2[0]))
    if k == "alto":
        hs = R.sample(range(115, 135), 3)
        nm = [p1[0], p2[0], K.next()[0]]
        if len(set(nm)) < 3:
            return None
        i = hs.index(min(hs))
        return mcq("Le altezze: %s %d cm, %s %d cm, %s %d cm. Chi è il più basso?" % (nm[0], hs[0], nm[1], hs[1], nm[2], hs[2]), nm[i], [x for x in nm if x != nm[i]] + ["sono alti uguali"],
                   "Il numero più piccolo è %d: <b>%s</b>." % (hs[i], nm[i]))
    if k == "ultimo":
        n = R.randint(6, 10)
        return mcq("In una fila ci sono %d bambini. Chi è l’ultimo della fila?" % n, "il " + ORD[n - 1], ["il " + ORD[n - 2], "il primo", "il " + ORD[n % 10] if n < 10 else "l’undicesimo"],
                   "Se sono %d, l’ultimo è <b>il %s</b>." % (n, ORD[n - 1]))
    pos = R.randint(2, 6)
    return mcq("In una gara %s arriva %s. Quanti bambini sono arrivati prima di %s?" % (p1[0], ORD[pos - 1], "lei" if p1[1] == "lei" else "lui"), str(pos - 1), [str(pos), str(pos + 1), str(pos - 2) if pos > 2 else "nessuno"],
               ("Prima del %s c’è <b>1</b> bambino." % ORD[pos - 1]) if pos == 2 else "Prima del %s ci sono <b>%d</b> bambini." % (ORD[pos - 1], pos - 1))


def main():
    seen = set()
    sets = [
        ("Maggiore, minore, uguale", mix(R, seen, [(s1_simbolo, 14), (s1_figure, 6)])),
        ("Il più grande e l’ordine", mix(R, seen, [(s2_estremi, 10), (s2_ordine, 10)])),
        ("Sulla retta", mix(R, seen, [(s3_retta, 10), (s3_tra, 10)])),
        ("Primo, secondo, terzo…", mix(R, seen, [(s4_ordinali, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Per confrontare due numeri guarda prima le <b>decine</b>: 52 è maggiore di 48 perché 5 decine sono più di 4.",
         "Se le decine sono uguali, guarda le <b>unità</b>: 47 &gt; 43.",
         "&gt; vuol dire «maggiore», &lt; vuol dire «minore». La punta indica sempre il numero più piccolo.",
         "Ordine <b>crescente</b>: dal più piccolo al più grande. <b>Decrescente</b>: dal più grande al più piccolo."],
        [("Confronta 29 e 31.", ["decine: 2 e 3", "3 decine sono di più"], "29 &lt; 31")],
        [["Dire 29 &gt; 31 perché 9 &gt; 1", "Guarda prima le decine."],
         ["Confondere &lt; e &gt;", "La bocca aperta guarda il numero più grande."],
         ["Scambiare crescente e decrescente", "Crescente: i numeri crescono, diventano più grandi."]])
    faq = [("Come ricordo il simbolo >?", "Pensa a una bocca affamata: si apre sempre verso il numero più grande."),
           ("Che cosa sono i numeri ordinali?", "Dicono la posizione: primo, secondo, terzo… Si usano per le file e le gare.")]
    make_unit(R, "confrontare-e-ordinare-i-numeri", "N",
              "Confrontare e ordinare i numeri naturali, anche rappresentandoli sulla retta; usare i simboli <, > e =; usare i numeri ordinali",
              "Confrontare e ordinare i numeri fino a 100", "Confrontare e ordinare i numeri",
              "Schede di matematica per la classe seconda su confronto e ordine dei numeri fino a 100: maggiore e minore, ordine crescente e decrescente, retta, numeri ordinali e problemi. 100 esercizi con soluzioni.",
              "Confronta prima le decine, poi le unità.", "La punta di < e > indica il numero più piccolo.",
              body, faq, sets, 2, grade=G)


if __name__ == "__main__":
    main()
