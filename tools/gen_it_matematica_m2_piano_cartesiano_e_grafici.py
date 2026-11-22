# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Piano cartesiano e grafici (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m2_piano_cartesiano_e_grafici.py
Coordinate di un punto (primo quadrante), distanza tra punti con la stessa ascissa o ordinata, perimetro e area di
poligoni con i vertici sul piano, traslazioni e simmetrie rispetto a una retta parallela agli assi, punti di una retta y = kx + q,
tabella e grafico di una funzione.
Errori: scambiare ascissa e ordinata, contare i quadretti invece della differenza, dimenticare di dividere per 2 nel triangolo.
"""
import random
from it_media import M, L, unit, mix, table, W, kosy, Kids
from de_common import BLUE

R = random.Random(71206)
G = "seconda-media"
K = Kids(R)
LET = "ABCDEFGH"


def P(x, y):
    return "(%d; %d)" % (x, y)


def pic(pts, lines=(), label="piano cartesiano"):
    return kosy(lines, pts, 0, 10, 26, label)


def s1_leggi():
    x, y = R.randint(1, 9), R.randint(1, 9)
    if x == y:
        return None
    n = R.choice(LET)
    return M("%sQuali sono le coordinate del punto %s?" % (pic([(x, y, n)]), n), P(x, y), W(P(y, x), P(x + 1, y), P(x, y - 1), P(x - 1, y + 1)),
             "Ascissa (orizzontale) %d, ordinata (verticale) %d: %s<b>%s</b>." % (x, y, n, P(x, y)))


def s1_quale():
    pts = []
    while len(pts) < 4:
        p = (R.randint(1, 9), R.randint(1, 9))
        if p not in pts and (p[1], p[0]) not in pts:
            pts.append(p)
    i = R.randrange(4)
    x, y = pts[i]
    if x == y:
        return None
    sw = [j for j, p in enumerate(pts) if p == (y, x)]
    names = list(LET[:4])
    return M("%sQuale punto ha coordinate %s?" % (pic([(a, b, names[j]) for j, (a, b) in enumerate(pts)]), P(x, y)), names[i], [names[j] for j in range(4) if j != i],
             "Si va a destra di %d e in alto di %d: è il punto <b>%s</b>." % (x, y, names[i]))


def s1_quiz():
    q, a, w = R.choice([
        ("Nel punto P(3; 7) il numero 3 si chiama…", "ascissa", ["ordinata", "origine", "quadrante"]),
        ("Nel punto P(3; 7) il numero 7 si chiama…", "ordinata", ["ascissa", "origine", "quadrante"]),
        ("L’origine degli assi ha coordinate…", "(0; 0)", ["(1; 1)", "(0; 1)", "(1; 0)"]),
        ("Un punto sull’asse delle ascisse ha sempre…", "ordinata 0", ["ascissa 0", "ascissa uguale all’ordinata", "ordinata 1"]),
        ("Un punto sull’asse delle ordinate ha sempre…", "ascissa 0", ["ordinata 0", "ascissa uguale all’ordinata", "ascissa 1"]),
        ("I punti con la stessa ordinata stanno su una retta…", "parallela all’asse x", ["parallela all’asse y", "che passa per l’origine", "obliqua"]),
        ("I punti con la stessa ascissa stanno su una retta…", "parallela all’asse y", ["parallela all’asse x", "che passa per l’origine", "obliqua"]),
    ])
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def s2_distanza():
    if R.random() < 0.5:
        x = R.randint(1, 9)
        a, b = sorted(R.sample(range(0, 11), 2))
        A, B = (x, a), (x, b)
    else:
        y = R.randint(1, 9)
        a, b = sorted(R.sample(range(0, 11), 2))
        A, B = (a, y), (b, y)
    if b - a < 2:
        return None
    return M("%sQuanto è lungo il segmento AB, con A%s e B%s? (unità: 1 quadretto)" % (pic([(A[0], A[1], "A"), (B[0], B[1], "B")]), P(*A), P(*B)), str(b - a), W(a + b, b - a + 1, b - a - 1, b, b - a + 2),
             "Hanno la stessa %s: si sottraggono le altre coordinate: %d − %d = <b>%d</b>." % ("ascissa" if A[0] == B[0] else "ordinata", b, a, b - a))


def s3_area():
    k = R.choice(["rett", "tri", "per"])
    x1, x2 = sorted(R.sample(range(0, 11), 2))
    y1, y2 = sorted(R.sample(range(0, 11), 2))
    b, h = x2 - x1, y2 - y1
    if b < 2 or h < 2 or b == h:
        return None
    if k == "tri":
        xc = R.randint(0, 10)
        if b * h % 2:
            return None
        pts = [(x1, y1, "A"), (x2, y1, "B"), (xc, y2, "C")]
        return M("%sCalcola l’area del triangolo A%s, B%s, C%s. (unità: 1 quadretto)" % (pic(pts), P(x1, y1), P(x2, y1), P(xc, y2)), str(b * h // 2), W(b * h, b + h, b * h // 2 + b, 2 * (b + h)),
                 "Base AB = %d − %d = %d, altezza = %d − %d = %d; area = %d × %d : 2 = <b>%d</b>." % (x2, x1, b, y2, y1, h, b, h, b * h // 2))
    pts = [(x1, y1, "A"), (x2, y1, "B"), (x2, y2, "C"), (x1, y2, "D")]
    co = "A%s, B%s, C%s, D%s" % (P(x1, y1), P(x2, y1), P(x2, y2), P(x1, y2))
    if k == "rett":
        return M("%sCalcola l’area del rettangolo %s." % (pic(pts), co), str(b * h), W(2 * (b + h), b + h, b * h // 2 if b * h % 2 == 0 else b * h + 1, (b + 1) * (h + 1)),
                 "Base %d, altezza %d: area = %d × %d = <b>%d</b>." % (b, h, b, h, b * h))
    return M("%sCalcola il perimetro del rettangolo %s." % (pic(pts), co), str(2 * (b + h)), W(b * h, b + h, 2 * (b + h) + 2, 4 * b, 2 * (b + h) - 2),
             "Base %d, altezza %d: perimetro = 2 × (%d + %d) = <b>%d</b>." % (b, h, b, h, 2 * (b + h)))


def s3_quarto():
    x1, x2 = sorted(R.sample(range(1, 10), 2))
    y1, y2 = sorted(R.sample(range(1, 10), 2))
    return M("Tre vertici di un rettangolo sono A%s, B%s e C%s. Quali sono le coordinate del quarto vertice D?" % (P(x1, y1), P(x2, y1), P(x2, y2)), P(x1, y2), W(P(y2, x1), P(x2, y1 + y2) if y1 + y2 <= 10 else P(x1, y1 + 1), P(x1 + x2, y2) if x1 + x2 <= 10 else P(x2, x1), P(x1, y1)),
             "D ha l’ascissa di A (%d) e l’ordinata di C (%d): <b>D%s</b>." % (x1, y2, P(x1, y2)))


def s4_trasla():
    x, y = R.randint(1, 6), R.randint(1, 6)
    dx, dy = R.randint(1, 4), R.randint(1, 4)
    k = R.choice(["dest", "sin"])
    if k == "dest":
        return M("Il punto A%s si sposta di %s a destra e %d in alto. Quali sono le nuove coordinate?" % (P(x, y), "1 quadretto" if dx == 1 else "%d quadretti" % dx, dy), P(x + dx, y + dy), W(P(x + dy, y + dx), P(x - dx, y + dy) if x > dx else P(x + dx, y), P(x + dx, y - dy) if y > dy else P(x, y + dy), P(dx, dy)),
                 "Ascissa %d + %d, ordinata %d + %d: <b>%s</b>." % (x, dx, y, dy, P(x + dx, y + dy)))
    x += 4
    y += 4
    return M("Il punto A%s si sposta di %s a sinistra e %d in basso. Quali sono le nuove coordinate?" % (P(x, y), "1 quadretto" if dx == 1 else "%d quadretti" % dx, dy), P(x - dx, y - dy), W(P(x + dx, y + dy), P(x - dy, y - dx), P(x - dx, y + dy), P(dx, dy)),
             "Ascissa %d − %d, ordinata %d − %d: <b>%s</b>." % (x, dx, y, dy, P(x - dx, y - dy)))


def s4_simm():
    k = R.choice(["x", "y"])
    c = R.randint(3, 7)
    if k == "x":
        x = R.randint(max(0, 2 * c - 10), 2 * c)
        y = R.randint(1, 9)
        if x == c:
            return None
        return M("Qual è il simmetrico del punto A%s rispetto alla retta x = %d?" % (P(x, y), c), P(2 * c - x, y), W(P(x, 2 * c - y) if 0 <= 2 * c - y <= 10 else P(y, x), P(2 * c - x, 2 * c - y) if 0 <= 2 * c - y <= 10 else P(c, y), P(c, y), P(x + c, y)),
                 "La retta x = %d è verticale: l’ordinata non cambia; A dista %d dalla retta, il simmetrico ha ascissa %d: <b>%s</b>." % (c, abs(x - c), 2 * c - x, P(2 * c - x, y)))
    y = R.randint(max(0, 2 * c - 10), 2 * c)
    x = R.randint(1, 9)
    if y == c:
        return None
    return M("Qual è il simmetrico del punto A%s rispetto alla retta y = %d?" % (P(x, y), c), P(x, 2 * c - y), W(P(2 * c - x, y) if 0 <= 2 * c - x <= 10 else P(y, x), P(2 * c - x, 2 * c - y) if 0 <= 2 * c - x <= 10 else P(x, c), P(x, c), P(x, y + c)),
             "La retta y = %d è orizzontale: l’ascissa non cambia; il simmetrico ha ordinata %d: <b>%s</b>." % (c, 2 * c - y, P(x, 2 * c - y)))


def eqs(m, q):
    t = ("x" if m == 1 else "%dx" % m) if m else ""
    if q:
        t = (t + " + %d" % q) if t else str(q)
    return "y = " + (t or "0")


def calc(m, q, x):
    t = ("%d × %d" % (m, x)) if m != 1 else str(x)
    if q:
        t += " + %d" % q
    return t + " = %d" % (m * x + q) if (m != 1 or q) else "%d" % x


def s5_retta():
    m, q = R.choice([(1, 0), (2, 0), (3, 0), (1, 1), (1, 2), (2, 1), (1, 3)])
    f = lambda x: m * x + q
    eq = eqs(m, q)
    k = R.choice(["appartiene", "valore", "grafico"])
    if k == "appartiene":
        x = R.randint(1, 4)
        good = P(x, f(x))
        bad = [P(x, f(x) + 1), P(x + 1, f(x)), P(f(x), x) if f(x) != x else P(x, f(x) + 2)]
        return M("Quale punto appartiene alla retta %s?" % eq, good, W(*bad), "Per x = %d: y = %s. Il punto è <b>%s</b>." % (x, calc(m, q, x), good))
    if k == "valore":
        x = R.randint(2, 4)
        lines = [(m, q, BLUE, "")]
        return M("%sLa retta del grafico ha equazione %s. Leggi o calcola: quanto vale y quando x = %d?" % (pic([], lines), eq, x), str(f(x)), W(f(x) + 1, f(x) - 1, m * x, f(x) + 2, x),
                 "y = %s: <b>%d</b>." % (calc(m, q, x), f(x)))
    xs = [0, 1, 2, 3]
    ys = [f(x) for x in xs]
    wrong = [eqs(m + q, 0) if q else eqs(1, m) if m > 1 else eqs(1, 1), eqs(m + 1, q), eqs(m, q + 1), eqs(q, m) if q else eqs(m + 2, 0)]
    return M("Quale equazione corrisponde alla tabella?<br>%s" % table(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]]), eq, W(*wrong),
             "Per x = 0 si ha y = %d; ogni volta che x aumenta di 1, y aumenta di %d: <b>%s</b>." % (q, m, eq))


def main():
    seen = set()
    sets = [
        ("Coordinate dei punti", mix(R, seen, [(s1_leggi, 8), (s1_quale, 7), (s1_quiz, 5)])),
        ("Distanze sul piano", mix(R, seen, [(s2_distanza, 20)])),
        ("Poligoni sul piano", mix(R, seen, [(s3_area, 14), (s3_quarto, 6)])),
        ("Traslazioni e simmetrie", mix(R, seen, [(s4_trasla, 10), (s4_simm, 10)])),
        ("Rette e tabelle", mix(R, seen, [(s5_retta, 20)])),
    ]
    body = L(["Il <b>piano cartesiano</b> ha due assi perpendicolari che si incontrano nell’<b>origine</b> O(0; 0). Ogni punto ha due coordinate: <b>ascissa</b> (orizzontale) e <b>ordinata</b> (verticale): P(x; y).",
              "Prima si legge l’ascissa, poi l’ordinata: P(3; 5) si trova 3 a destra e 5 in alto.",
              "Se due punti hanno la stessa ascissa (o la stessa ordinata), la loro distanza è la differenza delle altre coordinate.",
              "Una tabella x → y si può disegnare sul piano: se i punti stanno su una retta, la relazione si scrive y = mx + q."],
             [("A(2; 3) e B(2; 8)", ["stessa ascissa", "8 − 3"], "AB = 5"), ("Rettangolo A(1; 1), B(6; 1), C(6; 4)", ["base 6 − 1 = 5, altezza 4 − 1 = 3", "5 × 3"], "area 15")],
             [["Scambiare le coordinate", "(3; 5) e (5; 3) sono punti diversi: prima x, poi y."],
              ["Contare i punti della griglia invece della distanza", "Da 3 a 8 ci sono 5 quadretti, non 6."],
              ["Nel triangolo dimenticare : 2", "Area = base × altezza : 2."]])
    faq = [("Perché si scrive P(3; 5) con il punto e virgola?", "Perché in italiano la virgola indica i decimali: con il punto e virgola P(2,5; 3) non si confonde."),
           ("Come trovo il simmetrico rispetto alla retta x = 4?", "L’ordinata resta uguale; l’ascissa si trova alla stessa distanza dalla retta, dall’altra parte.")]
    unit(G, R, "piano-cartesiano-e-grafici", "F",
         "Usare il piano cartesiano per rappresentare relazioni e funzioni; rappresentare punti, segmenti e figure; calcolare perimetri e aree di figure nel piano",
         "Piano cartesiano e grafici", "Piano cartesiano",
         "Schede di matematica per la seconda media sul piano cartesiano: coordinate, distanze, perimetro e area di poligoni, traslazioni, simmetrie e rette y = mx + q. 100 esercizi con soluzioni.",
         "P(x; y): prima l’ascissa, poi l’ordinata.", "Stessa ascissa: distanza = differenza delle ordinate.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
