# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: Retta e fasci di rette (Geometria)
  python3 tools/gen_it_matematica_l3_retta_e_fasci_di_rette.py
Equazione generale ax + by + c = 0, distanza di un punto da una retta, asse di un segmento, area di un triangolo
con le coordinate, fasci di rette propri (per un punto) e impropri (paralleli), retta del fascio per un punto, parametro
per rette parallele o perpendicolari, centro di un fascio.
Errori: distanza senza valore assoluto o senza √(a² + b²), condizione di perpendicolarità aa′ − bb′ = 0, area senza dividere per 2.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, WP, fq, nz, P, show, d, simp_root

R = random.Random(72304)
G = "terza-liceo"


def gen(a, b, c):
    return "%s = 0" % show(P([(a, {"x": 1}), (b, {"y": 1}), (c, {})]))


def pt(x, y, n=""):
    return "%s(%s; %s)" % (n, fq(x), fq(y))


def rq(c, m):
    """c·√m con c razionale → testo (frazione HTML)"""
    c = Fr(c)
    top = ("" if c.numerator == 1 else str(c.numerator)) + "√%d" % m
    return top if c.denominator == 1 else "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (top, c.denominator)


def rt(n):
    k, m = simp_root(n)
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def s1_dist():
    a, b = R.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 15), (1, 0), (0, 1), (1, 1), (1, 2), (2, 1)])
    a *= R.choice([1, -1])
    c = R.randint(-10, 10)
    x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
    num = abs(a * x0 + b * y0 + c)
    den2 = a * a + b * b
    r = math.isqrt(den2)
    if r * r == den2:
        v = Fr(num, r)
        ans = d(v) if (v * 100).denominator == 1 or v.denominator in (1, 2, 4, 5, 10, 13) and False else fq(v)
        try:
            ans = d(v)
        except ValueError:
            ans = fq(v)
        w = [fq(num) if num != v else fq(num + 1), fq(Fr(num, den2)), fq(Fr(abs(a * x0 + b * y0 - c), r)) if abs(a * x0 + b * y0 - c) != num else fq(v + 1)]
    else:
        if num == 0:
            return None
        k, m = simp_root(den2)
        ans = rq(Fr(num, k * m), m)
        w = [fq(num), rq(Fr(num, den2), 1) if False else fq(Fr(num, den2)), rq(Fr(abs(a * x0 + b * y0), k * m), m) if abs(a * x0 + b * y0) not in (num, 0) else rq(Fr(num + 1, k * m), m), rq(Fr(num, k), m)]
    if num == 0:
        return None
    return M("Calcola la distanza del punto %s dalla retta %s." % (pt(x0, y0, "P"), gen(a, b, c)), ans, [x for x in w if x != ans],
             "d = |ax<sub>0</sub> + by<sub>0</sub> + c| / √(a² + b²) = |%s| / √%d = <b>%s</b>." % (fq(a * x0 + b * y0 + c), den2, ans))


def s1_asse():
    x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
    x2, y2 = x1 + 2 * nz(R, -3, 3), y1 + 2 * nz(R, -3, 3)
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    # asse: (x2 − x1)(x − mx) + (y2 − y1)(y − my) = 0
    a, b = x2 - x1, y2 - y1
    g = math.gcd(a, b)
    a, b = a // g, b // g
    if b < 0:
        a, b = -a, -b
    c = -(a * mx + b * my)
    m = Fr(-a, b)
    q = Fr(-c, b)
    ans = "y = %s" % show(P([(m, {"x": 1}), (q, {})])) if m.denominator == 1 and q.denominator == 1 else gen(a, b, c)
    mw = Fr(b, a) if a else None
    w = [gen(b, -a, -(b * mx - a * my)) if a else gen(1, 0, -mx), gen(a, b, -c) if c else gen(a, b, 1), gen(a, b, -(a * x1 + b * y1))]
    w = [x for x in w if x != ans and x != gen(a, b, c)]
    return M("Scrivi l’equazione dell’asse del segmento di estremi %s e %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), ans, w,
             "L’asse passa per il punto medio M%s ed è perpendicolare ad AB (m<sub>AB</sub> = %s): <b>%s</b>." % (pt(mx, my), fq(Fr(y2 - y1, x2 - x1)) if x2 != x1 else "∞", ans))


def s2_area():
    while True:
        P_ = [(R.randint(-5, 6), R.randint(-5, 6)) for _ in range(3)]
        (x1, y1), (x2, y2), (x3, y3) = P_
        A2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        if A2:
            break
    v = Fr(A2, 2)
    return M("Calcola l’area del triangolo di vertici %s, %s, %s." % (pt(x1, y1, "A"), pt(x2, y2, "B"), pt(x3, y3, "C")), d(v), [d(x) for x in WP(A2, Fr(A2, 4), v + 1, Fr(abs(x1 * y2 - x2 * y1), 2))],
             "Area = ½ |x<sub>A</sub>(y<sub>B</sub> − y<sub>C</sub>) + x<sub>B</sub>(y<sub>C</sub> − y<sub>A</sub>) + x<sub>C</sub>(y<sub>A</sub> − y<sub>B</sub>)| = ½ · %d = <b>%s</b>." % (A2, d(v)))


def s3_fascio():
    x0, y0 = R.randint(-4, 4), R.randint(-4, 4)
    x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
    if x1 == x0:
        return None
    m = Fr(y1 - y0, x1 - x0)
    q = y0 - m * x0
    k = R.choice(["m", "centro"])
    if k == "m":
        fas = "y %s %s = m(x %s %s)" % ("−" if y0 >= 0 else "+", fq(abs(y0)), "−" if x0 >= 0 else "+", fq(abs(x0)))
        return M("Nel fascio di rette %s, quale valore di m dà la retta passante per %s?" % (fas, pt(x1, y1, "Q")), "m = %s" % fq(m), ["m = %s" % fq(x) for x in W(Fr(x1 - x0, y1 - y0) if y1 != y0 else None, -m, Fr(y1 + y0, x1 + x0) if x1 + x0 else m + 1, m + 1) if x != m],
                     "Sostituisco Q: %s %s %s = m(%s %s %s) → <b>m = %s</b>." % (fq(y1), "−" if y0 >= 0 else "+", fq(abs(y0)), fq(x1), "−" if x0 >= 0 else "+", fq(abs(x0)), fq(m)))
    a1, b1 = nz(R, -3, 3), nz(R, -3, 3)
    a2, b2 = nz(R, -3, 3), nz(R, -3, 3)
    if a1 * b2 == a2 * b1:
        return None
    c1, c2 = -(a1 * x0 + b1 * y0), -(a2 * x0 + b2 * y0)
    f = "(%s) + k(%s) = 0" % (show(P([(a1, {"x": 1}), (b1, {"y": 1}), (c1, {})])), show(P([(a2, {"x": 1}), (b2, {"y": 1}), (c2, {})])))
    return M("Qual è il centro del fascio di rette %s?" % f, pt(x0, y0, "C"), [pt(y0, x0, "C") if x0 != y0 else pt(x0, -y0, "C"), pt(-x0, -y0, "C") if (x0, y0) != (0, 0) else pt(1, 1, "C"), pt(x0 + 1, y0, "C")],
             "Il centro è l’intersezione delle due rette generatrici: risolvo il sistema e trovo <b>%s</b>." % pt(x0, y0, "C"))


def s4_param():
    a, b = nz(R, -4, 4), nz(R, -4, 4)
    k = R.choice(["par", "perp"])
    c = R.randint(-5, 5)
    # retta r: ax + by + c = 0 ; s: (k)x + 2y − 1 = 0 → parallela se k/a = 2/b ; perpendicolare se a·k + b·2 = 0
    bb = R.choice([1, 2, 3])
    if k == "par":
        kk = Fr(a * bb, b)
        ans = "k = %s" % fq(kk)
        w = ["k = %s" % fq(x) for x in W(-kk, Fr(-b * bb, a), Fr(b * bb, a)) if x != kk]
        e = "Parallele se a/a′ = b/b′: k/%s = %d/%s → <b>k = %s</b>." % ("(%s)" % fq(a) if a < 0 else fq(a), bb, "(%s)" % fq(b) if b < 0 else fq(b), fq(kk))
    else:
        kk = Fr(-b * bb, a)
        ans = "k = %s" % fq(kk)
        w = ["k = %s" % fq(x) for x in W(-kk, Fr(a * bb, b), Fr(b * bb, a), Fr(-a * bb, b), kk + 1) if x != kk]
        e = "Perpendicolari se aa′ + bb′ = 0: %s · k + %s · %d = 0 → <b>k = %s</b>." % (fq(a), "(%s)" % fq(b) if b < 0 else fq(b), bb, fq(kk))
    return M("Per quale valore di k la retta kx + %sy − 1 = 0 è %s alla retta %s?" % ("" if bb == 1 else bb, "parallela" if k == "par" else "perpendicolare", gen(a, b, c)), ans, w, e)


def s5_bis():
    k = R.choice(["dist2", "par_dist"])
    if k == "dist2":
        a, b = R.choice([(3, 4), (4, 3), (5, 12), (6, 8)])
        c1, c2 = R.sample(range(-20, 21), 2)
        v = Fr(abs(c1 - c2), int(math.sqrt(a * a + b * b)))
        try:
            ans = d(v)
        except ValueError:
            ans = fq(v)
        return M("Calcola la distanza tra le rette parallele %s e %s." % (gen(a, b, c1), gen(a, b, c2)), ans, [fq(x) for x in WP(abs(c1 - c2), Fr(abs(c1 + c2), 5) if abs(c1 + c2) else None, v + 1, Fr(abs(c1 - c2), a + b))],
                     "Prendo un punto della prima retta e calcolo la distanza dalla seconda: |c − c′|/√(a² + b²) = %d/%d = <b>%s</b>." % (abs(c1 - c2), int(math.sqrt(a * a + b * b)), ans))
    m = nz(R, -3, 3)
    q = R.randint(-5, 5)
    t = R.randint(1, 5)
    # rette parallele a y = mx + q a distanza t√(1 + m²): y = mx + q ± t√(1+m²) → solo m = 0 per numeri belli
    if m:
        return None
    return M("Quali rette sono parallele a y = %s e distano %d da essa?" % (fq(q), t), "y = %s e y = %s" % (fq(q - t), fq(q + t)), ["y = %s" % fq(q + t), "y = %s e y = %s" % (fq(-t), fq(t)), "x = %s e x = %s" % (fq(q - t), fq(q + t))],
             "Le rette orizzontali a distanza %d sono <b>y = %s e y = %s</b>." % (t, fq(q - t), fq(q + t)))


def main():
    seen = set()
    sets = [
        ("Distanza di un punto da una retta", mix(R, seen, [(s1_dist, 20)])),
        ("Asse di un segmento e aree", mix(R, seen, [(s1_asse, 10), (s2_area, 10)])),
        ("Fasci di rette", mix(R, seen, [(s3_fascio, 20)])),
        ("Rette parallele e perpendicolari con parametro", mix(R, seen, [(s4_param, 20)])),
        ("Distanze tra rette e riepilogo", mix(R, seen, [(s5_bis, 8), (s2_area, 6), (s1_dist, 6)])),
    ]
    body = L(["Ogni retta ha un’equazione <b>generale</b> ax + by + c = 0. Due rette sono parallele se a/a′ = b/b′, perpendicolari se aa′ + bb′ = 0.",
              "<b>Distanza</b> di P(x<sub>0</sub>; y<sub>0</sub>) dalla retta: d = |ax<sub>0</sub> + by<sub>0</sub> + c| / √(a² + b²). L’<b>asse</b> di un segmento è la perpendicolare nel punto medio.",
              "Un <b>fascio proprio</b> è l’insieme delle rette per un punto C: y − y<sub>C</sub> = m(x − x<sub>C</sub>). Un <b>fascio improprio</b> è l’insieme delle rette parallele a una direzione: y = mx + q con m fisso.",
              "Un fascio si può scrivere come combinazione di due rette: r + k s = 0. Il centro è l’intersezione delle due rette."],
             [("Distanza di P(1; 2) da 3x + 4y − 1 = 0", ["|3 + 8 − 1| / √25 = 10/5"], "2"),
              ("Area di A(0; 0), B(4; 0), C(1; 3)", ["½ |0 + 4 · 3 + 0|"], "6")],
             [["d = (ax<sub>0</sub> + by<sub>0</sub> + c)/(a² + b²)", "Serve il valore assoluto e la radice: √(a² + b²)."],
              ["Perpendicolari se aa′ − bb′ = 0", "La condizione è aa′ + bb′ = 0 (cioè m · m′ = −1)."],
              ["Area senza ½", "La formula con le coordinate dà il doppio dell’area: si divide per 2."]])
    faq = [("Perché nella distanza punto-retta c’è il valore assoluto?", "Perché ax<sub>0</sub> + by<sub>0</sub> + c può essere negativo (il punto sta dall’altra parte della retta), ma una distanza è sempre positiva."),
           ("Che cosa rappresenta il parametro k in un fascio?", "Ogni valore di k individua una retta del fascio. Per trovare quella che passa per un punto si sostituiscono le coordinate e si ricava k.")]
    unit(G, R, "retta-e-fasci-di-rette", "G",
         "La retta nel piano cartesiano: equazione generale, distanza punto-retta, asse di un segmento, aree, fasci di rette",
         "Retta e fasci di rette", "Retta e fasci di rette",
         "Schede di matematica per la terza liceo sulla retta: equazione generale, distanza di un punto da una retta, asse di un segmento, area di un triangolo con le coordinate, fasci propri e impropri, rette parallele e perpendicolari con parametro. 100 esercizi con soluzioni.",
         "d = |ax₀ + by₀ + c| / √(a² + b²)", "Parallele: a/a′ = b/b′. Perpendicolari: aa′ + bb′ = 0.",
         body, faq, sets, 4)


if __name__ == "__main__":
    main()
