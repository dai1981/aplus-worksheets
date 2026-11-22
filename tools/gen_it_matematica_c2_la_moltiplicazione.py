# -*- coding: utf-8 -*-
"""
Italia Matematica classe seconda: La moltiplicazione (Numeri)
  python3 tools/gen_it_matematica_c2_la_moltiplicazione.py
Gruppi uguali, addizione ripetuta, schieramenti (righe e colonne), il segno ×, gli incroci (combinazioni),
proprietà commutativa con gli schieramenti, problemi con gruppi uguali.
Errori: contare i gruppi invece degli oggetti, scrivere 3 + 4 per 3 gruppi da 4, gruppi non uguali.
"""
import random
from it_common import mcq, lesson, make_unit, mix, Kids, FOIS, table
import it_c2 as C

R = random.Random(70207)
G = "classe-seconda"
K = Kids(R)


def s1_gruppi():
    g, k = R.randint(2, 5), R.randint(2, 5)
    kind = R.choice(C.KINDS)
    if R.random() < 0.5:
        return mcq(C.gruppi(g, k, kind) + "%s %s ci sono in tutto?" % (C.quanti(kind), C.nome(kind)), str(g * k), [str(g + k), str(g), str(k), str(g * k + 1)],
                   "%d gruppi da %d: %s = <b>%d</b>." % (g, k, " + ".join([str(k)] * g), g * k))
    return mcq(C.gruppi(g, k, kind) + "Quale moltiplicazione descrive il disegno?", "%d %s %d" % (g, FOIS, k), ["%d + %d" % (g, k), "%d %s %d" % (g + 1, FOIS, k), "%d %s %d" % (g, FOIS, k + 1)],
               "%d gruppi, ognuno con %s: <b>%d %s %d</b> = %d." % (g, C.cose(kind, k), g, FOIS, k, g * k))


def s1_ripetuta():
    a, b = R.randint(2, 6), R.randint(2, 9)
    sh = " + ".join([str(b)] * a)
    if R.random() < 0.5:
        return mcq("Scrivi come moltiplicazione: %s" % sh, "%d %s %d" % (a, FOIS, b), ["%d %s %d" % (b, FOIS, b) if a != b else "%d %s %d" % (a + 1, FOIS, b), "%d + %d" % (a, b), "%d %s %d" % (a + 1, FOIS, b)],
                   "Il %d si ripete %d volte: <b>%d %s %d</b>." % (b, a, a, FOIS, b))
    return mcq("Scrivi come addizione: %d %s %d" % (a, FOIS, b), sh, ["%d + %d" % (a, b), " + ".join([str(a)] * b) if a != b else " + ".join([str(b)] * (a + 1)), " + ".join([str(b)] * (a + 1))],
               "%d volte il %d: <b>%s</b> = %d." % (a, b, sh, a * b))


def s2_schieramento():
    r, c = R.randint(2, 5), R.randint(2, 7)
    if R.random() < 0.5:
        return mcq(C.punti(r, c) + "Quanti pallini ci sono?", str(r * c), [str(r + c), str(r * c + c), str(r * (c - 1))], "%d righe da %d: %d %s %d = <b>%d</b>." % (r, c, r, FOIS, c, r * c))
    return mcq(C.punti(r, c) + "Quale moltiplicazione va bene per questo schieramento?", "%d %s %d" % (r, FOIS, c), ["%d + %d" % (r, c), "%d %s %d" % (r, FOIS, r) if r != c else "%d %s %d" % (r, FOIS, c + 1), "%d %s %d" % (c, FOIS, c) if r != c else "%d %s %d" % (r + 1, FOIS, c)],
               ("%d righe con %d pallini: <b>%d %s %d</b>." % (r, c, r, FOIS, c)) if r == c else "%d righe con %d pallini: <b>%d %s %d</b>. Va bene anche %d %s %d (colonne)." % (r, c, r, FOIS, c, c, FOIS, r))


def s2_commutativa():
    a, b = R.randint(2, 9), R.randint(2, 9)
    if a == b:
        return None
    return mcq("%d %s %d = %d. Quanto fa %d %s %d?" % (a, FOIS, b, a * b, b, FOIS, a), str(a * b), [str(a + b), str(a * b + a), str(a * b - b)],
               "Se scambi i numeri il risultato non cambia: <b>%d</b>. Uno schieramento girato ha gli stessi pallini." % (a * b))


MAGLIE = ["rossa", "blu", "verde", "gialla", "bianca"]
PANT = ["pantaloni neri", "pantaloni blu", "una gonna", "pantaloncini", "jeans"]
GUSTI = ["fragola", "cioccolato", "limone", "pistacchio", "vaniglia"]
CONI = ["cono", "coppetta", "cialda"]


def s3_incroci():
    k = R.choice(["vestiti", "gelato", "panino"])
    if k == "vestiti":
        a, b = R.randint(2, 5), R.randint(2, 4)
        return mcq("Giulia ha %d magliette (%s) e %d tipi di pantaloni (%s). In quanti modi diversi si può vestire?" % (a, ", ".join(MAGLIE[:a]), b, ", ".join(PANT[:b])), str(a * b),
                   [str(a + b), str(a), str(a * b + 1)], "Ogni maglietta va con ogni pantalone: %d %s %d = <b>%d</b> modi (è un incrocio)." % (a, FOIS, b, a * b))
    if k == "gelato":
        a, b = R.randint(2, 5), R.randint(2, 3)
        return mcq("Al bar ci sono %d gusti di gelato (%s) e %d modi di servirlo (%s). Scegli un gusto e un modo. Quante scelte diverse ci sono?" % (a, ", ".join(GUSTI[:a]), b, ", ".join(CONI[:b])), str(a * b),
                   [str(a + b), str(a * b - 1), str(2 * a)], "%d %s %d = <b>%d</b> scelte." % (a, FOIS, b, a * b))
    a, b = R.randint(2, 4), R.randint(2, 4)
    return mcq("Per il panino puoi scegliere %d tipi di pane e %d tipi di formaggio. Quanti panini diversi puoi fare?" % (a, b), str(a * b), [str(a + b), str(a * b + 2), str(max(a, b))],
               "Tabella degli incroci: %d righe e %d colonne = <b>%d</b> panini." % (a, b, a * b))


def s4_doppio():
    k = R.choice(["doppio", "triplo"])
    a = R.randint(2, 12)
    if k == "doppio":
        return mcq("Qual è il doppio di %d?" % a, str(2 * a), [str(a + 2), str(a), str(3 * a)], "Il doppio è 2 volte: %d %s 2 = <b>%d</b>." % (a, FOIS, 2 * a))
    a = R.randint(2, 9)
    return mcq("Qual è il triplo di %d?" % a, str(3 * a), [str(a + 3), str(2 * a), str(3 * a + 1)], "Il triplo è 3 volte: %d %s 3 = <b>%d</b>." % (a, FOIS, 3 * a))


def s5():
    p = K.next()
    k = R.choice(["ruote", "zampe", "scatole", "file", "mani", "piatti"])
    if k == "ruote":
        n, r_ = R.randint(2, 9), R.choice([2, 3, 4])
        v = {2: "biciclette", 3: "tricicli", 4: "automobili"}[r_]
        return mcq("Ci sono %d %s. Quante ruote in tutto?" % (n, v), str(n * r_), [str(n + r_), str(n), str(n * r_ + r_)], "%d %s %d = <b>%d</b>." % (n, FOIS, r_, n * r_))
    if k == "zampe":
        n, z = R.randint(2, 9), R.choice([2, 4])
        an = "galline" if z == 2 else "cani"
        return mcq("Nel cortile ci sono %d %s. Quante zampe hanno in tutto?" % (n, an), str(n * z), [str(n + z), str(n), str(n * z - z)], "Ogni animale ha %d zampe: %d %s %d = <b>%d</b>." % (z, n, FOIS, z, n * z))
    if k == "scatole":
        n, c = R.randint(2, 5), R.randint(3, 6)
        return mcq("%s ha %d scatole con %d pastelli ciascuna. Quanti pastelli ha?" % (p[0], n, c), str(n * c), [str(n + c), str(n * c - 1), str(c)], "%d %s %d = <b>%d</b>." % (n, FOIS, c, n * c))
    if k == "file":
        n, c = R.randint(2, 5), R.randint(3, 8)
        return mcq("In palestra ci sono %d file di sedie, ognuna con %d sedie. Quante sedie ci sono?" % (n, c), str(n * c), [str(n + c), str(n * c + c), str(n * c - n)], "%d %s %d = <b>%d</b>." % (n, FOIS, c, n * c))
    if k == "mani":
        n = R.randint(2, 9)
        return mcq("%d bambini alzano tutte e due le mani. Quante mani sono alzate?" % n, str(2 * n), [str(n + 2), str(n), str(4 * n)], "%d %s 2 = <b>%d</b>." % (n, FOIS, 2 * n))
    n, c = R.randint(2, 6), R.randint(2, 5)
    return mcq("Sul tavolo ci sono %d piatti. In ogni piatto ci sono %d biscotti. Quanti biscotti in tutto?" % (n, c), str(n * c), [str(n + c), str(n * c + 1), str(c)], "%d %s %d = <b>%d</b>." % (n, FOIS, c, n * c))


def main():
    seen = set()
    sets = [
        ("Gruppi uguali", mix(R, seen, [(s1_gruppi, 14), (s1_ripetuta, 6)])),
        ("Addizione ripetuta e schieramenti", mix(R, seen, [(s1_ripetuta, 8), (s2_schieramento, 12)])),
        ("Scambiare i fattori e doppio", mix(R, seen, [(s2_commutativa, 10), (s4_doppio, 10)])),
        ("Gli incroci", mix(R, seen, [(s3_incroci, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>moltiplicazione</b> serve quando ci sono <b>gruppi uguali</b>: 3 gruppi da 4 = 3 %s 4 = 12." % FOIS,
         "È un’addizione ripetuta: 3 %s 4 = 4 + 4 + 4." % FOIS,
         "In uno <b>schieramento</b> conti le righe e quanti oggetti ci sono in ogni riga.",
         "Negli <b>incroci</b> ogni cosa del primo gruppo si unisce con ogni cosa del secondo: 3 magliette e 2 pantaloni = 3 %s 2 = 6 modi." % FOIS],
        [("4 sacchetti con 5 caramelle ciascuno", ["5 + 5 + 5 + 5 = 20", "4 %s 5 = 20" % FOIS], "20 caramelle")],
        [["Contare solo i gruppi", "Conta gli oggetti: gruppi %s oggetti in ogni gruppo." % FOIS],
         ["Scrivere 3 + 4 per 3 gruppi da 4", "Sono 3 volte il 4: 3 %s 4." % FOIS],
         ["Usare la moltiplicazione con gruppi diversi", "Si moltiplica solo se i gruppi sono tutti uguali."]],
        table(["", "pane bianco", "pane nero"], [["formaggio", "✓", "✓"], ["prosciutto", "✓", "✓"], ["verdure", "✓", "✓"]]))
    faq = [("Perché si dice «per»?", "Perché 3 × 4 si legge «3 per 4» e vuol dire «3 volte il 4»."),
           ("Che cos’è un incrocio?", "È una tabella in cui ogni riga si unisce con ogni colonna: il numero delle caselle si trova con una moltiplicazione.")]
    make_unit(R, "la-moltiplicazione", "N",
              "Eseguire moltiplicazioni come addizioni ripetute, con schieramenti e incroci; verbalizzare le procedure di calcolo",
              "La moltiplicazione: gruppi, schieramenti e incroci", "La moltiplicazione",
              "Schede di matematica per la classe seconda sulla moltiplicazione: gruppi uguali, addizione ripetuta, schieramenti, scambiare i fattori, doppio e triplo, incroci e problemi. 100 esercizi con soluzioni.",
              "Moltiplicare = sommare gruppi uguali.", "3 × 4 = 4 + 4 + 4.",
              body, faq, sets, 7, grade=G)


if __name__ == "__main__":
    main()
