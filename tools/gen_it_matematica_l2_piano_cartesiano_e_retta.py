# -*- coding: utf-8 -*-
"""
Italia Matematica seconda liceo: Piano cartesiano e retta (Geometria)
  python3 tools/gen_it_matematica_l2_piano_cartesiano_e_retta.py
Distanza tra due punti, punto medio, coefficiente angolare, equazione della retta (esplicita e implicita), retta per due punti,
appartenenza di un punto, rette parallele e perpendicolari, intersezione di due rette, aree di triangoli.
Errori: (x₂ − x₁)/(y₂ − y₁), punto medio con la differenza, perpendicolare con m′ = −m invece di −1/m.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, kosy, relabel, simp_root

R = random.Random(72205)
G = "seconda-liceo"
BLUE, GREEN = "#1f6fd1", "#15803d"


def pt(x, y, n=""):
    return "%s(%s; %s)" % (n, fq(x), fq(y))


def rt(n):
    k, m = simp_root(n)
    if m == 1:
        return str(k)
    return ("" if k == 1 else str(k)) + "√" + str(m)


def retta(m, q):
    if m == 0:
        return "y = %s" % fq(q)
    t = show(P([(m, {"x": 1}), (q, {})])) if m.denominator == 1 and q.denominator == 1 else None
    if t is None:
        mm = ("" if abs(m) == 1 else fq(abs(m))) + "x"
        t = ("−" if m < 0 else "") + mm + ("" if q == 0 else (" + " if q > 0 else " − ") + fq(abs(q)))
    return "y = %s" % t


def s1_dist():
    x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    if R.random() < 0.5:
        a, b = R.choice([(3, 4), (6, 8), (5, 12), (4, 3), (8, 6)])
    else:
        a, b = R.randint(1, 6), R.randint(1, 6)
    a *= R.choice([1, -1])
    b *= R.choice([1, -1])
    x2, y2 = x1 + a, y1 + b
    d2 = a * a + b * b
    ans = rt(d2)
    w = [rt(abs(a) + abs(b)) if False else str(abs(a) + abs(b)), rt((x1 + x2) ** 2 + (y1 + y2) ** 2) if (x1 + x2) ** 2 + (y1 + y2) ** 2 else "0", rt(abs(a * a - b * b)) if a * a != b * b else rt(2 * d2), str(d2)]
    return M("Calcola la distanza tra %s e %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), ans, [x for x in w if x != ans],
             "AB = √[(x<sub>B</sub> − x<sub>A</sub>)² + (y<sub>B</sub> − y<sub>A</sub>)²] = √(%d + %d) = <b>%s</b>." % (a * a, b * b, ans))


def s1_medio():
    x1, y1, x2, y2 = [R.randint(-8, 8) for _ in range(4)]
    if (x1, y1) == (x2, y2):
        return None
    mx, my = Fr(x1 + x2, 2), Fr(y1 + y2, 2)
    ans = pt(mx, my, "M")
    w = [pt(Fr(x2 - x1, 2), Fr(y2 - y1, 2), "M"), pt(x1 + x2, y1 + y2, "M"), pt(my, mx, "M")]
    return M("Trova il punto medio M del segmento di estremi %s e %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), ans, [x for x in w if x != ans],
             "M = ((x<sub>A</sub> + x<sub>B</sub>)/2; (y<sub>A</sub> + y<sub>B</sub>)/2) = <b>%s</b>." % ans)


def s1_simm():
    x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    mx, my = R.randint(-4, 4), R.randint(-4, 4)
    x2, y2 = 2 * mx - x1, 2 * my - y1
    if (x1, y1) == (mx, my):
        return None
    ans = pt(x2, y2, "B")
    return M("M%s è il punto medio di AB e A%s. Trova B." % (pt(mx, my), pt(x1, y1)), ans, [pt(Fr(x1 + mx, 2), Fr(y1 + my, 2), "B"), pt(mx - x1, my - y1, "B"), pt(-x2, -y2, "B") if (x2, y2) != (0, 0) else pt(1, 1, "B")],
             "x<sub>B</sub> = 2x<sub>M</sub> − x<sub>A</sub>, y<sub>B</sub> = 2y<sub>M</sub> − y<sub>A</sub>: <b>%s</b>." % ans)


def s2_m():
    x1, y1, x2, y2 = [R.randint(-6, 6) for _ in range(4)]
    if x1 == x2 or y1 == y2:
        return None
    m = Fr(y2 - y1, x2 - x1)
    w = [Fr(x2 - x1, y2 - y1), -m, Fr(y2 + y1, x2 + x1) if x2 + x1 else m + 1]
    return M("Qual è il coefficiente angolare della retta passante per %s e %s?" % (pt(x1, y1, "A"), pt(x2, y2, "B")), "m = %s" % fq(m), ["m = %s" % fq(v) for v in w + [m + 1, 2 * m] if v != m],
             "m = (y<sub>B</sub> − y<sub>A</sub>)/(x<sub>B</sub> − x<sub>A</sub>) = (%s)/(%s) = <b>%s</b>." % (fq(y2 - y1), fq(x2 - x1), fq(m)))


def s2_impl():
    a, b, c = nz(R, -6, 6), nz(R, -6, 6), R.randint(-9, 9)
    m, q = Fr(-a, b), Fr(-c, b)
    k = R.choice(["m", "q"])
    eq = "%s = 0" % show(P([(a, {"x": 1}), (b, {"y": 1}), (c, {})]))
    if k == "m":
        return M("Qual è il coefficiente angolare della retta %s?" % eq, "m = %s" % fq(m), ["m = %s" % fq(v) for v in (Fr(a, b), Fr(-b, a), Fr(b, a)) if v != m] + ["m = %s" % fq(a)],
                 "Esplicito: y = −(a/b)x − c/b, quindi m = −a/b = <b>%s</b>." % fq(m))
    return M("In quale punto la retta %s taglia l’asse y?" % eq, pt(0, q), [pt(0, v) for v in (Fr(c, b), Fr(-c, a), -q if q else Fr(1)) if v != q] + [pt(q, 0) if q else pt(1, 0)],
             "Pongo x = 0: %s = 0 → y = %s: <b>%s</b>." % (show(P([(b, {"y": 1}), (c, {})])), fq(q), pt(0, q)))


def s3_due():
    x1, x2 = R.sample(range(-5, 6), 2)
    m = Fr(nz(R, -3, 3), R.choice([1, 1, 2]))
    q = Fr(R.randint(-4, 4))
    y1, y2 = m * x1 + q, m * x2 + q
    if y1.denominator != 1 or y2.denominator != 1:
        return None
    ans = retta(m, q)
    w = [retta(-m, q), retta(m, -q) if q else retta(m, 1), retta(1 / m, q), retta(m, y1)]
    return M("Scrivi l’equazione della retta passante per %s e %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), ans, [x for x in w if x != ans],
             "m = %s; sostituisco A in y = mx + q: q = %s. <b>%s</b>." % (fq(m), fq(q), ans))


def s3_par():
    m = Fr(nz(R, -4, 4), R.choice([1, 1, 2, 3]))
    q0 = R.randint(-5, 5)
    x0, y0 = R.randint(-4, 4), R.randint(-4, 4)
    k = R.choice(["par", "perp"])
    mm = m if k == "par" else -1 / m
    q = y0 - mm * x0
    ans = retta(mm, q)
    w = [retta(-m, y0 + m * x0) if k == "par" else retta(-m, y0 + m * x0), retta(1 / m, y0 - x0 / m), retta(m if k == "perp" else -1 / m, y0 - (m if k == "perp" else -1 / m) * x0), retta(mm, q + 1), retta(mm, -q) if q else retta(mm, 2)]
    return M("Scrivi la retta %s a %s e passante per %s." % ("parallela" if k == "par" else "perpendicolare", retta(m, q0), pt(x0, y0, "P")), ans, [x for x in w if x != ans],
             "%s: m′ = %s. y − %s = %s(x − %s) → <b>%s</b>." % ("Le parallele hanno lo stesso m" if k == "par" else "Per le perpendicolari m · m′ = −1", fq(mm), "(%s)" % fq(y0) if y0 < 0 else fq(y0), fq(mm), "(%s)" % fq(x0) if x0 < 0 else fq(x0), ans))


def s4_inters():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    m1, m2 = R.sample([-3, -2, -1, 1, 2, 3], 2)
    q1, q2 = y - m1 * x, y - m2 * x
    fig = relabel(kosy([(m1, q1, BLUE, "r"), (m2, q2, GREEN, "s")], [], -6, 6, 20), "due rette nel piano cartesiano") if abs(q1) <= 6 and abs(q2) <= 6 else ""
    ans = pt(x, y)
    return M("%sTrova il punto di intersezione delle rette r: %s e s: %s." % (fig, retta(Fr(m1), Fr(q1)), retta(Fr(m2), Fr(q2))), ans, [pt(y, x), pt(-x, y) if x else pt(1, y), pt(x, -y) if y else pt(x, 1), pt(x + 1, y)],
             "Metto a sistema: %s = %s → x = %s, y = %s: <b>%s</b>." % (show(P([(m1, {"x": 1}), (q1, {})])), show(P([(m2, {"x": 1}), (q2, {})])), fq(x), fq(y), ans))


def s4_app():
    m, q = nz(R, -4, 4), R.randint(-6, 6)
    x = R.randint(-5, 5)
    y = m * x + q + R.choice([0, 0, 1, -1, 2])
    ok = y == m * x + q
    ans = "sì" if ok else "no"
    return M("Il punto %s appartiene alla retta %s?" % (pt(x, y, "P"), retta(Fr(m), Fr(q))), ans, ["no" if ok else "sì", "solo se x = 0", "non si può stabilire"],
             "Sostituisco x = %s: y = %s. %s: <b>%s</b>." % (fq(x), fq(m * x + q), "Coincide con l’ordinata di P" if ok else "È diverso da %s" % fq(y), ans))


def s5_area():
    a = nz(R, -6, 6)
    b = nz(R, -6, 6)
    # retta che taglia gli assi in (a; 0) e (0; b)
    m, q = Fr(-b, a), Fr(b)
    area = Fr(abs(a * b), 2)
    return M("La retta %s forma con gli assi cartesiani un triangolo. Quanto vale la sua area?" % retta(m, q), fq(area), [fq(v) for v in W(abs(a * b), Fr(abs(a) + abs(b), 2), area + 1, area * 4)],
             "Taglia gli assi in (%s; 0) e (0; %s): area = |%s| · |%s| : 2 = <b>%s</b>." % (fq(a), fq(b), fq(a), fq(b), fq(area)))


def s5_tipo():
    k = R.choice(["orizz", "vert", "orig", "bis"])
    c = nz(R, -6, 6)
    if k == "orizz":
        q, ans = "y = %s" % fq(c), "parallela all’asse x"
    elif k == "vert":
        q, ans = "x = %s" % fq(c), "parallela all’asse y"
    elif k == "orig":
        q, ans = "y = %sx" % ("" if c == 1 else "−" if c == -1 else fq(c)), "passante per l’origine"
    else:
        q, ans = R.choice(["y = x", "y = −x"]), "bisettrice di due quadranti"
    return M("Che retta è %s?" % q, ans, [o for o in ["parallela all’asse x", "parallela all’asse y", "passante per l’origine", "bisettrice di due quadranti"] if o != ans],
             "%s: <b>%s</b>." % (q, ans))


def main():
    seen = set()
    sets = [
        ("Distanza e punto medio", mix(R, seen, [(s1_dist, 10), (s1_medio, 6), (s1_simm, 4)])),
        ("Coefficiente angolare ed equazioni", mix(R, seen, [(s2_m, 8), (s2_impl, 8), (s5_tipo, 4)])),
        ("Retta per due punti", mix(R, seen, [(s3_due, 14), (s4_app, 6)])),
        ("Rette parallele e perpendicolari", mix(R, seen, [(s3_par, 20)])),
        ("Intersezioni e aree", mix(R, seen, [(s4_inters, 12), (s5_area, 8)])),
    ]
    body = L(["<b>Distanza</b> tra A e B: √[(x<sub>B</sub> − x<sub>A</sub>)² + (y<sub>B</sub> − y<sub>A</sub>)²]. <b>Punto medio</b>: la media delle coordinate.",
              "Una retta non verticale ha equazione <b>y = mx + q</b>: m è il <b>coefficiente angolare</b> (la pendenza), q l’ordinata all’origine. In forma implicita ax + by + c = 0, m = −a/b.",
              "m tra due punti: (y<sub>B</sub> − y<sub>A</sub>)/(x<sub>B</sub> − x<sub>A</sub>). Retta per un punto: y − y<sub>0</sub> = m(x − x<sub>0</sub>).",
              "Rette <b>parallele</b>: stesso m. Rette <b>perpendicolari</b>: m · m′ = −1, cioè m′ = −1/m. L’intersezione di due rette si trova mettendo a sistema le equazioni."],
             [("Retta per A(1; 2) e B(3; 8)", ["m = 6/2 = 3", "y − 2 = 3(x − 1)"], "y = 3x − 1"),
              ("Perpendicolare a y = 2x + 1 per O", ["m′ = −1/2"], "y = −½x")],
             [["m = (x<sub>B</sub> − x<sub>A</sub>)/(y<sub>B</sub> − y<sub>A</sub>)", "Sopra le y, sotto le x."],
              ["Perpendicolare con m′ = −m", "Serve l’antireciproco: m′ = −1/m."],
              ["Punto medio con la differenza", "Si fa la media: (x<sub>A</sub> + x<sub>B</sub>)/2."]])
    faq = [("Che cosa indica il coefficiente angolare?", "Di quanto aumenta y quando x aumenta di 1. Se m &gt; 0 la retta sale, se m &lt; 0 scende, se m = 0 è orizzontale."),
           ("Le rette verticali hanno un coefficiente angolare?", "No: hanno equazione x = k e non si possono scrivere nella forma y = mx + q.")]
    unit(G, R, "piano-cartesiano-e-retta", "G",
         "Il metodo delle coordinate cartesiane: distanza, punto medio, equazione della retta, rette parallele e perpendicolari",
         "Piano cartesiano e retta", "Piano cartesiano e retta",
         "Schede di matematica per la seconda liceo su piano cartesiano e retta: distanza tra due punti, punto medio, coefficiente angolare, retta per due punti, rette parallele e perpendicolari, intersezioni, aree. 100 esercizi con soluzioni.",
         "Parallele: m = m′. Perpendicolari: m · m′ = −1.", "Retta per P con pendenza m: y − y₀ = m(x − x₀).",
         body, faq, sets, 5)


if __name__ == "__main__":
    main()
