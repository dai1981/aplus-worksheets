# -*- coding: utf-8 -*-
"""
Italia Matematica prima media: Enti geometrici e segmenti (Spazio e figure)
  python3 tools/gen_it_matematica_m1_enti_geometrici_e_segmenti.py
Punto, retta, semiretta, segmento, piano; rette incidenti e parallele; segmenti consecutivi e adiacenti, punto medio,
somma, differenza e multipli di segmenti, problemi con somma e differenza o con il rapporto tra segmenti.
Errori: confondere retta, semiretta e segmento, misurare un segmento contando i punti, sommare quando c’è una differenza.
"""
import random
from it_media import M, L, unit, mix, table, W, FOIS, DIV, Kids
from it_common import wrap, text, line, INK, RED, BLUE, GREEN
import gen_it_matematica_c3_linee_e_angoli as A3

R = random.Random(71110)
G = "prima-media"


def punti(xs, names, W_=420):
    s = [line(20, 50, W_ - 20, 50, INK, 2)]
    lo, hi = min(xs), max(xs)
    X = lambda v: 40 + (v - lo) / float(hi - lo) * (W_ - 80)
    for v, n in zip(xs, names):
        s.append("<circle cx='%.1f' cy='50' r='4.5' fill='%s'/>" % (X(v), RED))
        s.append(text(X(v), 30, n, 17, weight=700))
    return wrap(W_, 80, "".join(s), "punti su una retta")


def s1_enti():
    q, a, w = R.choice([("Come si chiama una parte di retta limitata da due punti?", "segmento", ["semiretta", "retta", "piano"]),
                        ("Come si chiama una parte di retta che ha un’origine ma non ha fine?", "semiretta", ["segmento", "retta", "angolo"]),
                        ("Quante rette passano per due punti distinti?", "una sola", ["infinite", "due", "nessuna"]),
                        ("Quante rette passano per un punto?", "infinite", ["una sola", "due", "nessuna"]),
                        ("Due rette che hanno un punto in comune si dicono…", "incidenti", ["parallele", "coincidenti", "consecutive"]),
                        ("Due rette del piano che non hanno punti in comune si dicono…", "parallele", ["incidenti", "perpendicolari", "consecutive"]),
                        ("Quanti punti ha un segmento?", "infiniti", ["due", "uno", "dieci"]),
                        ("Due segmenti che hanno in comune solo un estremo si dicono…", "consecutivi", ["adiacenti", "paralleli", "congruenti"]),
                        ("Due segmenti consecutivi che stanno sulla stessa retta si dicono…", "adiacenti", ["paralleli", "incidenti", "perpendicolari"]),
                        ("Il punto che divide un segmento in due parti congruenti si chiama…", "punto medio", ["vertice", "origine", "estremo"]),
                        ("Due segmenti che si possono sovrapporre perfettamente si dicono…", "congruenti", ["consecutivi", "adiacenti", "incidenti"]),
                        ("Due rette incidenti che formano quattro angoli retti si dicono…", "perpendicolari", ["parallele", "coincidenti", "oblique"])])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s1_disegno():
    return A3.s1_retta()


def s2_misura():
    xs = sorted(R.sample(range(0, 30), 4))
    names = "ABCD"
    i, j = sorted(R.sample(range(4), 2))
    d = xs[j] - xs[i]
    if R.random() < 0.5:
        return M(punti(xs, names) + "Sulla retta: A = %d cm, B = %d cm, C = %d cm, D = %d cm (distanze da un punto O). Quanto misura %s%s?" % (tuple(xs) + (names[i], names[j])), "%d cm" % d,
                 W("%d cm" % (xs[i] + xs[j]), "%d cm" % (d + 1), "%d cm" % xs[j], "%d cm" % (j - i)), "%s%s = %d − %d = <b>%d cm</b>." % (names[i], names[j], xs[j], xs[i], d))
    a, b = R.randint(3, 20), R.randint(3, 20)
    return M("A, B, C sono in quest’ordine su una retta. AB = %d cm e BC = %d cm. Quanto misura AC?" % (a, b), "%d cm" % (a + b), W("%d cm" % abs(a - b) if a != b else "0 cm", "%d cm" % (a * b), "%d cm" % (a + b + 1)),
             "AB e BC sono adiacenti: AC = AB + BC = <b>%d cm</b>." % (a + b))


def s2_medio():
    a = R.randint(2, 30) * 2
    k = R.choice(["meta", "doppio", "medio2"])
    if k == "meta":
        return M("M è il punto medio di AB e AB = %d cm. Quanto misura AM?" % a, "%d cm" % (a // 2), W("%d cm" % a, "%d cm" % (a * 2), "%d cm" % (a // 4) if a % 4 == 0 else "%d cm" % (a // 2 + 1)), "AM = AB : 2 = <b>%d cm</b>." % (a // 2))
    if k == "doppio":
        return M("M è il punto medio di AB e MB = %d cm. Quanto misura AB?" % (a // 2), "%d cm" % a, W("%d cm" % (a // 2), "%d cm" % (a // 4) if a % 4 == 0 else "%d cm" % (a + 1), "%d cm" % (a * 2)), "AB = 2 %s MB = <b>%d cm</b>." % (FOIS, a))
    b = R.randint(2, 20) * 2
    return M("AB = %d cm e BC = %d cm sono adiacenti. M è il punto medio di AC. Quanto misura AM?" % (a, b), "%d cm" % ((a + b) // 2), W("%d cm" % (a + b), "%d cm" % (a // 2), "%d cm" % (abs(a - b) // 2) if a != b else "%d cm" % a),
             "AC = %d + %d = %d; AM = %d : 2 = <b>%d cm</b>." % (a, b, a + b, a + b, (a + b) // 2))


def s3_multipli():
    a = R.randint(2, 15)
    k = R.randint(2, 6)
    if R.random() < 0.5:
        return M("AB = %d %s CD e CD = %d cm. Quanto misura AB?" % (k, FOIS, a), "%d cm" % (k * a), W("%d cm" % (k + a), "%d cm" % a, "%d cm" % (k * a + a)), "AB = %d %s %d = <b>%d cm</b>." % (k, FOIS, a, k * a))
    return M("AB = %d %s CD e AB = %d cm. Quanto misura CD?" % (k, FOIS, k * a), "%d cm" % a, W("%d cm" % (k * a * k), "%d cm" % (k * a - k), "%d cm" % (k * a)), "CD = AB : %d = <b>%d cm</b>." % (k, a))


def s5():
    k = R.choice(["sd", "sd", "rap", "rap", "tre"])
    if k == "sd":
        a, b = R.randint(10, 60), R.randint(2, 25)
        s, d = 2 * a + b, b
        return M("La somma di due segmenti misura %d cm e la loro differenza %d cm. Quanto misura il segmento maggiore?" % (s, d), "%d cm" % (a + b), W("%d cm" % a, "%d cm" % ((s - d)), "%d cm" % (s // 2)),
                 "Maggiore = (somma + differenza) : 2 = (%d + %d) : 2 = <b>%d cm</b>. Il minore misura %d cm." % (s, d, a + b, a))
    if k == "rap":
        a = R.randint(3, 20)
        m, n = R.choice([(2, 1), (3, 1), (3, 2), (4, 1), (5, 2), (4, 3)])
        s = a * (m + n)
        return M("La somma di due segmenti AB e CD è %d cm. AB è formato da %d parti uguali e CD da %d delle stesse parti. Quanto misura AB?" % (s, m, n), "%d cm" % (a * m),
                 W("%d cm" % (a * n), "%d cm" % a, "%d cm" % (s // 2) if s % 2 == 0 else "%d cm" % (s - a)), "Una parte: %d : (%d + %d) = %d cm; AB = %d %s %d = <b>%d cm</b>." % (s, m, n, a, a, FOIS, m, a * m))
    a, b, c = R.randint(5, 20), R.randint(5, 20), R.randint(5, 20)
    return M("I segmenti AB, BC e CD sono adiacenti. AB = %d cm, BC supera AB di %d cm, CD = %d cm. Quanto misura AD?" % (a, b, c), "%d cm" % (2 * a + b + c),
             W("%d cm" % (a + b + c), "%d cm" % (2 * a + b), "%d cm" % (a + b + c + a + 1)), "BC = %d + %d = %d; AD = %d + %d + %d = <b>%d cm</b>." % (a, b, a + b, a, a + b, c, 2 * a + b + c))


def main():
    A3.R = R
    seen = set()
    sets = [
        ("Punti, rette, semirette, segmenti", mix(R, seen, [(s1_enti, 12), (s1_disegno, 8)])),
        ("Misurare i segmenti", mix(R, seen, [(s2_misura, 20)])),
        ("Punto medio", mix(R, seen, [(s2_medio, 20)])),
        ("Multipli e sottomultipli di segmenti", mix(R, seen, [(s3_multipli, 20)])),
        ("Problemi con i segmenti", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Gli <b>enti geometrici</b> fondamentali sono il punto, la retta e il piano. Per due punti passa una sola retta; per un punto ne passano infinite.",
              "La <b>semiretta</b> è una parte di retta con un’origine; il <b>segmento</b> è la parte di retta tra due punti, gli estremi.",
              "Segmenti <b>consecutivi</b> hanno in comune solo un estremo; se stanno anche sulla stessa retta sono <b>adiacenti</b> e si possono sommare.",
              "Il <b>punto medio</b> divide un segmento in due parti congruenti. Problemi «somma e differenza»: maggiore = (s + d) : 2, minore = (s − d) : 2."],
             [("AB + CD = 40 cm, AB − CD = 8 cm", ["AB = (40 + 8) : 2 = 24 cm", "CD = (40 − 8) : 2 = 16 cm"], "AB = 24 cm, CD = 16 cm")],
             [["Confondere retta, semiretta e segmento", "La retta non ha estremi, la semiretta ne ha uno, il segmento due."],
              ["Misurare contando i punti", "Si misura la distanza tra gli estremi."],
              ["Nei problemi sommare quando c’è una differenza", "Disegna i segmenti: aiuta a capire quali parti si sommano."]],
             table(["Ente", "Estremi", "Lunghezza"], [["retta", "nessuno", "illimitata"], ["semiretta", "uno (origine)", "illimitata"], ["segmento", "due", "si può misurare"]]))
    faq = [("Perché il punto non ha dimensioni?", "È un ente primitivo: si immagina come la traccia lasciata da una matita appuntitissima, senza lunghezza, larghezza né spessore."),
           ("Come si risolvono i problemi con i segmenti?", "Si disegnano i segmenti con le parti uguali (come nel metodo delle barre) e si scrive che cosa rappresenta ogni numero.")]
    unit(G, R, "enti-geometrici-e-segmenti", "S",
         "Conoscere definizioni e proprietà significative degli enti geometrici fondamentali (punto, retta, semiretta, segmento); operare con i segmenti e risolvere problemi",
         "Enti geometrici fondamentali e segmenti", "Enti geometrici e segmenti",
         "Schede di matematica per la prima media su enti geometrici e segmenti: punto, retta, semiretta, segmento, rette incidenti e parallele, segmenti consecutivi e adiacenti, punto medio e problemi. 100 esercizi con soluzioni.",
         "La retta non ha estremi, la semiretta ne ha uno, il segmento due.", "Maggiore = (somma + differenza) : 2.",
         body, faq, sets, 10)


if __name__ == "__main__":
    main()
