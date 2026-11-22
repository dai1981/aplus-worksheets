# -*- coding: utf-8 -*-
"""
Italia Matematica seconda media: Similitudine e teorema di Talete (Spazio e figure)
  python3 tools/gen_it_matematica_m2_similitudine_e_talete.py
Figure simili, rapporto di similitudine k, lati corrispondenti, rapporto dei perimetri (k) e delle aree (k²),
criteri di similitudine dei triangoli, teorema di Talete (fascio di rette parallele tagliate da due trasversali),
problemi con le ombre e con le scale.
Errori: pensare che anche le aree stiano nel rapporto k, confondere i lati corrispondenti, sommare invece di moltiplicare.
"""
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, num, d, fq, figure, Kids
from it_common import wrap, line, text, INK, BLUE, RED

R = random.Random(71211)
G = "seconda-media"
K = Kids(R)


def cm(v):
    return "%s cm" % d(v)


def due_tri(a, b, c, k, lab1, lab2):
    """due triangoli simili affiancati (stessa scala): lati a (base AB), b (AC), c (BC); il secondo × k"""
    import math
    x = (a * a + b * b - c * c) / (2.0 * a)
    y = math.sqrt(max(b * b - x * x, 0.01))
    k = float(k)
    big = max(1.0, k)
    sc = min(150.0 / (a * big), 150.0 / (y * big) if y else 99)
    out = []
    ox = 40.0
    base_y = 30 + y * big * sc + 10
    names = ["ABC", "DEF"]
    for t, (kk, labs) in enumerate([(1.0, lab1), (k, lab2)]):
        P = [(ox, base_y), (ox + a * kk * sc, base_y), (ox + x * kk * sc, base_y - y * kk * sc)]
        cx = sum(p[0] for p in P) / 3
        cy = sum(p[1] for p in P) / 3
        for i, j in ((0, 1), (1, 2), (2, 0)):
            out.append(line(P[i][0], P[i][1], P[j][0], P[j][1], INK, 2))
        for (i, j), lab in zip(((0, 1), (0, 2), (1, 2)), labs):
            mx, my = (P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2
            dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
            L_ = math.hypot(dx, dy)
            nx, ny = -dy / L_, dx / L_
            if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
                nx, ny = -nx, -ny
            anc = "middle" if abs(nx) < 0.6 else ("start" if nx > 0 else "end")
            out.append(text(mx + nx * (16 if anc == "middle" else 8), my + ny * 16 + 5, lab, 14, anchor=anc, col=BLUE, weight=600))
        for i, (px, py) in enumerate(P):
            dx, dy = px - cx, py - cy
            L_ = math.hypot(dx, dy) or 1
            out.append(text(px + dx / L_ * 15, py + dy / L_ * 15 + 5, names[t][i], 15))
        ox = max(p[0] for p in P) + 90
    return wrap(ox - 40, base_y + 34, "".join(out), "due triangoli simili", lg=True)


def tri_ok(a, b, c):
    return a + b > c and a + c > b and b + c > a and abs(a - b) + abs(b - c) > 0


def s1_lati():
    while True:
        a, b, c = R.randint(3, 9), R.randint(3, 9), R.randint(3, 9)
        if tri_ok(a, b, c) and len({a, b, c}) == 3 and 0.15 * a < (a * a + b * b - c * c) / (2.0 * a) < 0.85 * a and b * b - ((a * a + b * b - c * c) / (2.0 * a)) ** 2 > 0.2 * a * a:
            break
    k = R.choice([Fr(2), Fr(3, 2), Fr(1, 2), Fr(5, 4)])
    if k < 1:
        a, b, c = 2 * a, 2 * b, 2 * c
    i = R.randrange(3)
    L1 = [a, b, c]
    L2 = [v * k for v in L1]
    lab1 = [cm(v) for v in L1]
    lab2 = [cm(L2[0])] + [cm(L2[j]) if j != i else "x" for j in (1, 2)] if i != 0 else ["x", cm(L2[1]), cm(L2[2])]
    pic = due_tri(a, b, c, k, lab1, lab2)
    x = L2[i]
    return M("%sI due triangoli sono simili (il secondo è l’ingrandimento o la riduzione del primo). Quanto misura x?" % pic, cm(x), W(cm(L1[i] + (L2[(i + 1) % 3] - L1[(i + 1) % 3])) if L1[i] + (L2[(i + 1) % 3] - L1[(i + 1) % 3]) > 0 else None, cm(L1[i] / k), cm(x + 1), cm(L1[i] * 2) if k != 2 else cm(L1[i] * 3), cm(L1[i]), cm(x + 2)),
             "k = %s : %s = %s; x = %s × %s = <b>%s</b>." % (d(L2[(i + 1) % 3]), d(L1[(i + 1) % 3]), d(k), d(L1[i]), d(k), cm(x)))


def s1_k():
    a = R.randint(2, 20)
    k = R.choice([Fr(2), Fr(3), Fr(4), Fr(3, 2), Fr(5, 2), Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(5, 4)])
    b = a * k
    if b.denominator != 1 and (b * 10).denominator != 1:
        return None
    return M("Due figure sono simili. Un lato della prima misura %d cm e il lato corrispondente della seconda %s cm. Qual è il rapporto di similitudine (seconda : prima)?" % (a, d(b)), fq(k), W(fq(1 / k), fq(k * 2), d(b - a) if b > a else d(a - b)),
             "k = %s : %d = <b>%s</b>." % (d(b), a, fq(k)))


def s2_per_area():
    k = R.choice([2, 3, 4, 5, Fr(1, 2), Fr(3, 2)])
    k = Fr(k)
    t = R.choice(["per", "area", "area_k"])
    if t == "per":
        p = R.randint(6, 40)
        return M("Due poligoni simili hanno rapporto di similitudine %s. Il perimetro del primo è %d cm. Quanto è il perimetro del secondo?" % (fq(k), p), cm(p * k), W(cm(p * k * k), cm(p + k) if k.denominator == 1 else cm(p * 2), cm(p / k), cm(p * k + 1), cm(p * k - 1)),
                 "I perimetri stanno nel rapporto k: %d × %s = <b>%s</b>." % (p, d(k), cm(p * k)))
    if t == "area":
        A = R.randint(3, 30) * 4
        return M("Due poligoni simili hanno rapporto di similitudine %s. L’area del primo è %d cm². Quanto è l’area del secondo?" % (fq(k), A), "%s cm²" % d(A * k * k), W("%s cm²" % d(A * k), "%s cm²" % d(A * k * 2), "%s cm²" % d(A * k * k * k), "%s cm²" % d(A + k * k)),
                 "Le aree stanno nel rapporto k²: %d × %s = <b>%s cm²</b>." % (A, d(k * k), d(A * k * k)))
    k = Fr(R.randint(2, 5))
    return M("Le aree di due figure simili stanno nel rapporto %d. Qual è il rapporto di similitudine?" % int(k * k),
             str(int(k)), W(int(k * k), int(k * k) // 2 if k * k % 2 == 0 else int(k) + 1, int(k * k * k), int(k) + 1, int(k * k) * 2), "k² = %d, quindi k = √%d = <b>%d</b>." % (int(k * k), int(k * k), int(k)))


QZ = [("Due figure sono simili se…", "hanno gli angoli uguali e i lati in proporzione", ["hanno la stessa area", "hanno lo stesso perimetro", "hanno un lato uguale"]),
      ("Due triangoli con due angoli rispettivamente uguali sono…", "simili", ["congruenti", "equivalenti", "non si può dire"]),
      ("Due quadrati qualsiasi sono…", "sempre simili", ["sempre congruenti", "mai simili", "simili solo se hanno la stessa area"]),
      ("Due rettangoli qualsiasi sono…", "non sempre simili", ["sempre simili", "sempre congruenti", "mai simili"]),
      ("Due triangoli equilateri qualsiasi sono…", "sempre simili", ["sempre congruenti", "mai simili", "simili solo se hanno lo stesso lato"]),
      ("Se il rapporto di similitudine è 1, le figure sono…", "congruenti", ["diverse", "una il doppio dell’altra", "solo equivalenti"]),
      ("Se il rapporto di similitudine è 3, le aree stanno nel rapporto…", "9", ["3", "6", "27"]),
      ("In due figure simili, gli angoli corrispondenti sono…", "uguali", ["proporzionali", "uno il doppio dell’altro", "diversi"]),
      ("Due triangoli con i lati 3, 4, 5 e 6, 8, 10 sono…", "simili con k = 2", ["congruenti", "non simili", "simili con k = 3"]),
      ("Il teorema di Talete riguarda…", "un fascio di rette parallele tagliato da due trasversali", ["i triangoli rettangoli", "le aree dei poligoni", "le rette perpendicolari"])]


def s3_quiz():
    q, a, w = R.choice(QZ)
    return M(q, a, w, "Risposta: <b>%s</b>." % a)


def talete_svg(a, b, c, x_lab, y_lab, z_lab, w_lab):
    """tre parallele orizzontali, due trasversali; segmenti a, b sulla prima e c, d sulla seconda"""
    s = []
    ys = [30, 30 + 90 * 1.0, 30 + 180 * 1.0]
    for y in ys:
        s.append(line(16, y, 344, y, BLUE, 2))
    s.append(line(60, 10, 140, 230, INK, 2) + line(200, 10, 330, 230, INK, 2))
    def X1(y):
        return 60 + (y - 10) * 80 / 220.0
    def X2(y):
        return 200 + (y - 10) * 130 / 220.0
    for y in ys:
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/><circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (X1(y), y, INK, X2(y), y, INK))
    s.append(text(X1(75) - 10, 80, x_lab, 15, anchor="end", weight=600) + text(X1(165) - 10, 170, y_lab, 15, anchor="end", weight=600))
    s.append(text(X2(75) + 10, 80, z_lab, 15, anchor="start", weight=600) + text(X2(165) + 10, 170, w_lab, 15, anchor="start", weight=600))
    s.append(text(20, ys[0] - 6, "a", 14, col=BLUE, anchor="start") + text(20, ys[1] - 6, "b", 14, col=BLUE, anchor="start") + text(20, ys[2] - 6, "c", 14, col=BLUE, anchor="start"))
    return wrap(360, 240, "".join(s), "teorema di Talete: tre rette parallele tagliate da due trasversali", lg=True)


def s4_talete():
    p, q = R.randint(2, 12), R.randint(2, 12)
    if p == q:
        return None
    k = R.choice([Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4, 3), Fr(5, 4), Fr(1, 2)])
    r, s_ = p * k, q * k
    if (r * 10).denominator != 1 or (s_ * 10).denominator != 1:
        return None
    pos = R.randrange(4)
    vals = [Fr(p), Fr(q), r, s_]
    labs = [cm(v) if i != pos else "x" for i, v in enumerate(vals)]
    pic = talete_svg(None, None, None, *labs)
    x = vals[pos]
    other = {0: (1, 2, 3), 1: (0, 3, 2), 2: (3, 0, 1), 3: (2, 1, 0)}[pos]
    i, j, l = other
    return M("%sLe rette a, b, c sono parallele. Quanto misura x?" % pic, cm(x), W(cm(vals[i] + vals[j] - vals[l]) if vals[i] + vals[j] - vals[l] > 0 else None, cm(vals[l] * vals[i] / vals[j]) if vals[l] * vals[i] / vals[j] != x and ((vals[l] * vals[i] / vals[j]) * 100).denominator == 1 else None, cm(x + 1), cm(x * 2), cm(x + 2), cm(x / 2) if (x / 2 * 10).denominator == 1 else None),
             "Talete: %s : %s = %s : %s; x = <b>%s</b>." % tuple([d(v) if n != pos else "x" for n, v in enumerate(vals)] + [cm(x)]))


def s5():
    k = R.choice(["ombra", "foto", "mappa", "modellino", "albero"])
    if k in ("ombra", "albero"):
        h, o = R.choice([(Fr(3, 2), Fr(2)), (Fr(2), Fr(3)), (Fr(8, 5), Fr(2)), (Fr(9, 5), Fr(3)), (1, Fr(3, 2))])
        f = R.choice([4, 5, 6, 8, 10, 12])
        O = Fr(o) * f
        H = Fr(h) * f
        obj = "un albero" if k == "albero" else "un campanile"
        return M("Un bastone alto %s m fa un’ombra di %s m. Nello stesso momento %s fa un’ombra di %s m. Quanto è alto?" % (d(h), d(o), obj, d(O)), "%s m" % d(H), W("%s m" % d(O - Fr(o) + Fr(h)), "%s m" % d(O * o / Fr(h)) if ((O * o / Fr(h)) * 100).denominator == 1 else None, "%s m" % d(O), "%s m" % d(H + 1)),
                 "I triangoli bastone–ombra e %s–ombra sono simili: h = %s × %s : %s = <b>%s m</b>." % (obj.split()[1], d(O), d(h), d(o), d(H)))
    if k == "foto":
        a, b = R.choice([(10, 15), (9, 13), (13, 18), (15, 20), (20, 30)])
        f = R.choice([2, 3, 4])
        return M("Una foto di %d cm × %d cm viene ingrandita: il lato corto diventa %d cm. Quanto diventa il lato lungo?" % (a, b, a * f), cm(b * f), W(cm(b + a * f - a), cm(b * f * f), cm(a * f * 2) if a * f * 2 != b * f else cm(b * f + 1)), "k = %d : %d = %d; %d × %d = <b>%s</b>." % (a * f, a, f, b, f, cm(b * f)))
    if k == "mappa":
        sc = R.choice([25000, 50000, 100000, 200000])
        c = R.randint(2, 12)
        return M("Su una carta in scala 1 : %s due paesi distano %d cm. Quanti km distano nella realtà?" % (num(sc), c), "%s km" % d(Fr(c * sc, 100000)), W("%s km" % d(Fr(c * sc, 10000)), "%s km" % d(Fr(c * sc, 1000000)), "%s km" % num(c * sc)),
                 "%d × %s = %s cm = <b>%s km</b>." % (c, num(sc), num(c * sc), d(Fr(c * sc, 100000))))
    sc = R.choice([10, 20, 25, 50, 100])
    L_ = R.randint(2, 30) * sc
    return M("Il modellino di un’auto è in scala 1 : %d. L’auto vera è lunga %s cm. Quanto è lungo il modellino?" % (sc, num(L_)), cm(Fr(L_, sc)), W(cm(Fr(L_, sc * 10)), cm(L_ * sc), cm(L_ - sc)), "%s : %d = <b>%s</b>." % (num(L_), sc, cm(Fr(L_, sc))))


def main():
    seen = set()
    sets = [
        ("Rapporto di similitudine", mix(R, seen, [(s1_k, 8), (s1_lati, 12)])),
        ("Perimetri e aree di figure simili", mix(R, seen, [(s2_per_area, 20)])),
        ("Figure simili e criteri", mix(R, seen, [(s3_quiz, 10), (s1_lati, 10)])),
        ("Teorema di Talete", mix(R, seen, [(s4_talete, 20)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = L(["Due figure sono <b>simili</b> se hanno gli angoli corrispondenti uguali e i lati corrispondenti in proporzione. Il rapporto tra lati corrispondenti è il <b>rapporto di similitudine</b> k.",
              "Se k = 2, i lati e il perimetro raddoppiano, ma l’area diventa 2² = 4 volte più grande: <b>perimetri in rapporto k, aree in rapporto k²</b>.",
              "Due triangoli sono simili se hanno due angoli uguali, oppure i tre lati in proporzione.",
              "<b>Teorema di Talete</b>: un fascio di rette parallele tagliato da due trasversali individua segmenti proporzionali."],
             [("Triangoli simili, lati 4 cm e 6 cm corrispondenti; un altro lato del primo è 5 cm", ["k = 6 : 4 = 1,5", "5 × 1,5"], "7,5 cm")],
             [["Le aree nel rapporto k", "Le aree stanno nel rapporto k², non k."],
              ["Confondere i lati corrispondenti", "Il lato corrispondente sta di fronte all’angolo uguale."],
              ["Sommare la differenza", "Se un lato passa da 4 a 6, gli altri non aumentano di 2: si moltiplicano per 1,5."]])
    faq = [("Figure simili e figure congruenti sono la stessa cosa?", "No. Le figure congruenti sono uguali (k = 1); le figure simili hanno la stessa forma ma possono avere grandezza diversa."),
           ("Perché le aree stanno nel rapporto k²?", "Perché l’area è il prodotto di due lunghezze: se ognuna è moltiplicata per k, l’area è moltiplicata per k × k.")]
    unit(G, R, "similitudine-e-talete", "S",
         "Riconoscere figure piane simili in vari contesti e riprodurre in scala una figura assegnata; conoscere il teorema di Talete",
         "Similitudine e teorema di Talete", "Similitudine e Talete",
         "Schede di matematica per la seconda media sulla similitudine: rapporto di similitudine, perimetri e aree di figure simili, criteri dei triangoli simili, teorema di Talete e problemi con ombre e scale. 100 esercizi con soluzioni.",
         "Lati e perimetri: × k. Aree: × k².", "Talete: parallele → segmenti proporzionali.",
         body, faq, sets, 11)


if __name__ == "__main__":
    main()
