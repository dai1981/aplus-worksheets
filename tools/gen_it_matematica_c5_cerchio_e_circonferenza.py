# -*- coding: utf-8 -*-
"""
Italia Matematica classe quinta: Cerchio e circonferenza (Spazio e figure)
  python3 tools/gen_it_matematica_c5_cerchio_e_circonferenza.py
Centro, raggio, diametro, corda; circonferenza e cerchio; π ≈ 3,14; lunghezza della circonferenza (d × 3,14),
area del cerchio (r × r × 3,14), formule inverse (diametro dalla circonferenza), problemi.
Errori: confondere raggio e diametro, usare il diametro nella formula dell’area, confondere cerchio e circonferenza.
"""
import random
from it_common import eur, mcq, num, lesson, make_unit, mix, Kids, wrap, text, line, INK, GREEN, FILL, RED, BLUE, NB, FOIS, DIV

R = random.Random(70518)
G = "classe-quinta"
K = Kids(R)


def D(n, p):
    ip, fp_ = divmod(n, 10 ** p)
    s = (str(fp_).rjust(p, "0") if p else "").rstrip("0")
    return num(ip) + ("," + s if s else "")


def cm(v100):
    """v in centesimi di cm"""
    return "%s%scm" % (D(v100, 2), NB)


def cm2(v100):
    return "%s%scm²" % (D(v100, 2), NB)


def disegno(kind, val=None):
    s = ["<circle cx='110' cy='100' r='80' fill='%s' stroke='%s' stroke-width='2.4'/>" % (FILL, GREEN), "<circle cx='110' cy='100' r='3.5' fill='%s'/>" % INK, text(104, 96, "O", 13, anchor="end")]
    if kind == "raggio":
        s += [line(110, 100, 166.6, 43.4, RED, 2.6), text(150, 80, val or "?", 13, col=RED)]
    elif kind == "diametro":
        s += [line(30, 100, 190, 100, RED, 2.6), text(150, 94, val or "?", 13, col=RED)]
    elif kind == "corda":
        s += [line(45, 53, 175, 53, RED, 2.6)]
    elif kind == "arco":
        s += ["<path d='M110 20 A80 80 0 0 1 190 100' fill='none' stroke='%s' stroke-width='5'/>" % RED]
    elif kind == "settore":
        s += ["<path d='M110 100 L110 20 A80 80 0 0 1 190 100 Z' fill='#f6c9c9' stroke='%s' stroke-width='2'/>" % RED]
    return wrap(220, 200, "".join(s), "cerchio di centro O", lg=True)


def s1_elementi():
    k = R.choice(["raggio", "diametro", "corda", "arco", "settore"])
    names = {"raggio": "il raggio", "diametro": "il diametro", "corda": "una corda", "arco": "un arco", "settore": "un settore circolare"}
    why = {"raggio": "va dal centro a un punto della circonferenza", "diametro": "passa per il centro e unisce due punti della circonferenza", "corda": "unisce due punti della circonferenza senza passare per il centro",
           "arco": "è una parte della circonferenza", "settore": "è la parte di cerchio tra due raggi e un arco"}
    return mcq(disegno(k) + "Che cosa è colorato in rosso?", names[k], [v for x, v in names.items() if x != k], "Il segmento o la parte rossa %s: è <b>%s</b>." % (why[k], names[k]))


def s1_rd():
    r = R.randint(2, 40)
    if R.random() < 0.5:
        return mcq("Il raggio di un cerchio misura %d cm. Quanto misura il diametro?" % r, "%d cm" % (2 * r), ["%d cm" % (r // 2) if r % 2 == 0 else "%d cm" % (r + 2), "%d cm" % r, "%d cm" % (4 * r)],
                   "Il diametro è il doppio del raggio: %d %s 2 = <b>%d cm</b>." % (r, FOIS, 2 * r))
    return mcq("Il diametro di un cerchio misura %d cm. Quanto misura il raggio?" % (2 * r), "%d cm" % r, ["%d cm" % (4 * r), "%d cm" % (2 * r), "%d cm" % (r + 1)],
               "Il raggio è la metà del diametro: %d %s 2 = <b>%d cm</b>." % (2 * r, DIV, r))


TEO = [("Quanti raggi si possono tracciare in un cerchio?", "infiniti", ["4", "2", "1"]),
       ("Qual è la corda più lunga di un cerchio?", "il diametro", ["il raggio", "un arco", "nessuna, sono tutte uguali"]),
       ("Che differenza c’è tra cerchio e circonferenza?", "la circonferenza è il contorno, il cerchio è la superficie", ["sono la stessa cosa", "il cerchio è il contorno, la circonferenza la superficie", "la circonferenza è più grande"]),
       ("Quanto vale circa il numero π (pi greco)?", "3,14", ["3", "2,14", "31,4"]),
       ("La circonferenza è circa quante volte il diametro?", "3,14 volte", ["2 volte", "4 volte", "3,14 volte il raggio"]),
       ("Con quale strumento si disegna una circonferenza?", "il compasso", ["il goniometro", "la squadra", "il righello"]),
       ("Due diametri dello stesso cerchio sono…", "uguali", ["diversi", "perpendicolari sempre", "uno il doppio dell’altro"]),
       ("La ruota di una bicicletta, mentre gira di un giro, percorre una strada lunga quanto…", "la sua circonferenza", ["il suo diametro", "il suo raggio", "la sua area"])]


def s2_teoria():
    q, a, w = R.choice(TEO)
    return mcq(q, a, w, "Risposta: <b>%s</b>." % a)


def s2_circ():
    k = R.random() < 0.5
    d = R.randint(2, 40)
    c = d * 314
    if k:
        return mcq(disegno("diametro", "%d cm" % d) + "Quanto è lunga la circonferenza? (π = 3,14)", cm(c), [cm(d * 314 // 2), cm(c * 2), cm(d * 300)],
                   "C = diametro %s 3,14 = %d %s 3,14 = <b>%s</b>." % (FOIS, d, FOIS, cm(c)))
    r = R.randint(2, 30)
    c = 2 * r * 314
    return mcq(disegno("raggio", "%d cm" % r) + "Quanto è lunga la circonferenza? (π = 3,14)", cm(c), [cm(r * 314), cm(c * 2), cm(r * r * 314)],
               "Diametro = %d %s 2 = %d cm; C = %d %s 3,14 = <b>%s</b>." % (r, FOIS, 2 * r, 2 * r, FOIS, cm(c)))


def s3_area():
    r = R.randint(2, 20)
    a = r * r * 314
    if R.random() < 0.6:
        return mcq(disegno("raggio", "%d cm" % r) + "Qual è l’area del cerchio? (π = 3,14)", cm2(a), [cm2(4 * r * r * 314), cm2(2 * r * 314), cm2(r * 314)],
                   "A = r %s r %s 3,14 = %d %s %d %s 3,14 = <b>%s</b>." % (FOIS, FOIS, r, FOIS, r, FOIS, cm2(a)))
    return mcq(disegno("diametro", "%d cm" % (2 * r)) + "Qual è l’area del cerchio? (π = 3,14)", cm2(a), [cm2(4 * r * r * 314), cm2(2 * r * 314), cm2(r * r * 314 * 2)],
               "Raggio = %d %s 2 = %d cm; A = %d %s %d %s 3,14 = <b>%s</b>." % (2 * r, DIV, r, r, FOIS, r, FOIS, cm2(a)))


def s4_inversa():
    k = R.choice(["d", "r"])
    d = R.randint(2, 40)
    c = d * 314
    if k == "d":
        return mcq("Una circonferenza è lunga %s. Quanto misura il diametro? (π = 3,14)" % cm(c), "%d cm" % d, ["%d cm" % (2 * d), "%d cm" % (d // 2) if d % 2 == 0 else "%d cm" % (d + 1), cm(c * 314 // 100)],
                   "d = C %s 3,14 = %s %s 3,14 = <b>%d cm</b>." % (DIV, D(c, 2), DIV, d))
    if d % 2:
        d += 1
    c = d * 314
    return mcq("Una circonferenza è lunga %s. Quanto misura il raggio? (π = 3,14)" % cm(c), "%d cm" % (d // 2), ["%d cm" % d, "%d cm" % (2 * d), "%d cm" % (d // 2 + 2)],
               "d = %s %s 3,14 = %d cm; r = %d %s 2 = <b>%d cm</b>." % (D(c, 2), DIV, d, d, DIV, d // 2))


def s5():
    p = K.next()
    k = R.choice(["ruota", "tavolo", "aiuola", "pista", "pizza", "recinto"])
    if k == "ruota":
        d, g = R.choice([50, 60, 70]), R.choice([10, 100, 50])
        c = d * 314
        return mcq("La ruota della bicicletta di %s ha il diametro di %d cm. Quanti metri percorre in %d giri?" % (p[0], d, g), "%s m" % D(c * g // 100, 2),
                   ["%s m" % D(c * g // 200, 2), "%s m" % D(d * g, 2), "%s m" % D(c * g // 10, 2)], "Un giro: %d %s 3,14 = %s cm; %d giri: %s cm = <b>%s m</b>." % (d, FOIS, D(c, 2), g, D(c * g, 2), D(c * g // 100, 2)))
    if k == "tavolo":
        r = R.choice([40, 50, 60, 70])
        return mcq("Un tavolo rotondo ha il raggio di %d cm. Quanto deve essere lungo un bordo decorativo tutto intorno?" % r, cm(2 * r * 314), [cm(r * 314), cm(r * r * 314), cm(4 * r * 314)],
                   "C = %d %s 3,14 = <b>%s</b>." % (2 * r, FOIS, cm(2 * r * 314)))
    if k == "aiuola":
        r = R.randint(2, 6)
        return mcq("Un’aiuola rotonda ha il raggio di %d m. Qual è la sua area? (π = 3,14)" % r, "%s m²" % D(r * r * 314, 2), ["%s m²" % D(2 * r * 314, 2), "%s m²" % D(4 * r * r * 314, 2), "%s m" % D(r * r * 314, 2)],
                   "A = %d %s %d %s 3,14 = <b>%s m²</b>." % (r, FOIS, r, FOIS, D(r * r * 314, 2)))
    if k == "pista":
        d = R.choice([20, 30, 40, 50])
        n = R.randint(2, 5)
        return mcq("Una pista circolare ha il diametro di %d m. %s fa %d giri. Quanti metri percorre?" % (d, p[0], n), "%s m" % D(d * 314 * n, 2), ["%s m" % D(d * 314, 2), "%s m" % D(d * n * 100, 2), "%s m" % D(d * 314 * n // 2, 2)],
                   "Un giro: %d %s 3,14 = %s m; %s %s %d = <b>%s m</b>." % (d, FOIS, D(d * 314, 2), D(d * 314, 2), FOIS, n, D(d * 314 * n, 2)))
    if k == "pizza":
        a, b = R.choice([(15, 20), (14, 18), (16, 22)])
        g = "la pizza da %d cm" % (2 * b)
        return mcq("Una pizza ha il diametro di %d cm, un’altra di %d cm. Di quanti cm² è più grande l’area della seconda? (π = 3,14)" % (2 * a, 2 * b), cm2((b * b - a * a) * 314),
                   [cm2((2 * b - 2 * a) * 314), cm2((b - a) * (b - a) * 314), cm2((4 * b * b - 4 * a * a) * 314)], "%d %s %d %s 3,14 − %d %s %d %s 3,14 = <b>%s</b>." % (b, FOIS, b, FOIS, a, FOIS, a, FOIS, cm2((b * b - a * a) * 314)))
    r = R.randint(3, 10)
    pr = R.randint(2, 6)
    return mcq("Una vasca rotonda ha il raggio di %d m. Si vuole mettere una rete tutto intorno, a %d € al metro. Quanto si spende?" % (r, pr), eur(2 * r * 314 * pr),
               [eur(r * 314 * pr), eur(r * r * 314 * pr), eur(2 * r * 314)], "C = %d %s 3,14 = %s m; %s %s %d = <b>%s</b>." % (2 * r, FOIS, D(2 * r * 314, 2), D(2 * r * 314, 2), FOIS, pr, eur(2 * r * 314 * pr)))


def main():
    seen = set()
    sets = [
        ("Gli elementi del cerchio", mix(R, seen, [(s1_elementi, 5), (s1_rd, 15)])),
        ("Cerchio, circonferenza e π", mix(R, seen, [(s2_teoria, 8), (s2_circ, 12)])),
        ("L’area del cerchio", mix(R, seen, [(s3_area, 20)])),
        ("Dalla circonferenza al diametro", mix(R, seen, [(s4_inversa, 14), (s2_circ, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>circonferenza</b> è la linea chiusa; il <b>cerchio</b> è la superficie che racchiude. Il <b>raggio</b> va dal centro alla circonferenza; il <b>diametro</b> è il doppio del raggio.",
         "La circonferenza è circa <b>3,14 volte</b> il diametro. Questo numero si chiama <b>π</b> (pi greco).",
         "Lunghezza della circonferenza: C = d %s 3,14 (oppure r %s 2 %s 3,14)." % (FOIS, FOIS, FOIS),
         "Area del cerchio: A = r %s r %s 3,14. Usa il <b>raggio</b>, non il diametro." % (FOIS, FOIS)],
        [("Cerchio con raggio 5 cm", ["C = 10 %s 3,14 = 31,4 cm" % FOIS, "A = 5 %s 5 %s 3,14 = 78,5 cm²" % (FOIS, FOIS)], "C = 31,4 cm; A = 78,5 cm²")],
        [["Confondere raggio e diametro", "Il diametro attraversa tutto il cerchio: è il doppio del raggio."],
         ["Usare il diametro nell’area", "A = r %s r %s 3,14: prima dividi il diametro per 2." % (FOIS, FOIS)],
         ["Confondere cerchio e circonferenza", "La circonferenza si misura in cm, il cerchio in cm²."]],
        disegno("raggio", "r"))
    faq = [("Che cos’è π?", "È il numero di volte che la circonferenza contiene il diametro: circa 3,14, per qualsiasi cerchio."),
           ("Perché l’area si calcola con il raggio?", "Perché la formula A = r × r × 3,14 nasce dal quadrato costruito sul raggio: con il diametro si otterrebbe un’area 4 volte più grande.")]
    make_unit(R, "cerchio-e-circonferenza", "S",
              "Riconoscere e rappresentare il cerchio e i suoi elementi; calcolare la lunghezza della circonferenza e l’area del cerchio usando π ≈ 3,14",
              "Cerchio e circonferenza: raggio, diametro e π", "Cerchio e circonferenza",
              "Schede di matematica per la classe quinta su cerchio e circonferenza: centro, raggio, diametro, corda, π, lunghezza della circonferenza, area del cerchio, formule inverse e problemi. 100 esercizi con soluzioni.",
              "C = d × 3,14; A = r × r × 3,14.", "Il diametro è il doppio del raggio.",
              body, faq, sets, 18, grade=G)


if __name__ == "__main__":
    main()
