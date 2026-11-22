# -*- coding: utf-8 -*-
"""
Italia Matematica terza media: Piano cartesiano e retta (Relazioni e funzioni)
  python3 tools/gen_it_matematica_m3_piano_cartesiano_e_retta.py
Quattro quadranti, punto medio, distanza tra due punti (Pitagora), funzioni y = mx + q: coefficiente angolare e ordinata
all’origine, punti di una retta, intersezioni con gli assi, rette parallele (stesso m) e perpendicolari (m · m′ = −1),
retta per due punti, leggere la retta dal grafico, punto d’incontro di due rette.
Errori: scambiare m e q, sbagliare il segno nel coefficiente angolare, sommare invece di sottrarre nella distanza.
"""
import math
import random
from fractions import Fraction as Fr
from it_media import M, L, unit, mix, table, W, fq, sgn, kosy, Kids
from it_m3 import P as PP, show
from de_common import BLUE, RED

R = random.Random(71307)
G = "terza-media"
K = Kids(R)
TERNE = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 3, 5), (8, 6, 10), (12, 5, 13)]


def t(x):
    return sgn(x) if x else "0"


def Pt(x, y):
    return "(%s; %s)" % (t(x), t(y))


def nz(lo=-5, hi=5):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def eq(m, q):
    m, q = Fr(m), Fr(q)
    s = show(PP([(m, {"x": 1}), (q, {})]))
    return "y = " + s


def s1_quadrante():
    x, y = nz(), nz()
    qd = {(True, True): "primo", (False, True): "secondo", (False, False): "terzo", (True, False): "quarto"}[(x > 0, y > 0)]
    if R.random() < 0.5:
        return M("In quale quadrante si trova il punto P%s?" % Pt(x, y), qd + " quadrante", [v + " quadrante" for v in ["primo", "secondo", "terzo", "quarto"] if v != qd],
                 "Ascissa %s e ordinata %s: <b>%s quadrante</b>." % ("positiva" if x > 0 else "negativa", "positiva" if y > 0 else "negativa", qd))
    names = "ABCD"
    pts = [(x, y)]
    while len(pts) < 4:
        p = (nz(), nz())
        if p not in pts:
            pts.append(p)
    R.shuffle(pts)
    i = pts.index((x, y))
    pic = kosy((), [(a, b, names[j]) for j, (a, b) in enumerate(pts)], -5, 5, 24, "piano cartesiano con quattro punti")
    return M("%sQuale punto ha coordinate %s?" % (pic, Pt(x, y)), names[i], [names[j] for j in range(4) if j != i], "Si va %s di %d e %s di %d: è <b>%s</b>." % ("a destra" if x > 0 else "a sinistra", abs(x), "in alto" if y > 0 else "in basso", abs(y), names[i]))


def s1_medio():
    x1, y1, x2, y2 = nz(-8, 8), nz(-8, 8), nz(-8, 8), nz(-8, 8)
    if (x1 + x2) % 2 or (y1 + y2) % 2 or (x1, y1) == (x2, y2):
        return None
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    return M("Qual è il punto medio del segmento con estremi A%s e B%s?" % (Pt(x1, y1), Pt(x2, y2)), "M" + Pt(mx, my), W("M" + Pt((x2 - x1) // 2, (y2 - y1) // 2) if (x2 - x1, y2 - y1) != (mx * 2 - 2 * x1, 0) else None, "M" + Pt(x1 + x2, y1 + y2), "M" + Pt(my, mx) if mx != my else "M" + Pt(mx + 1, my), "M" + Pt(-mx, my) if mx else "M" + Pt(mx, -my) if my else "M" + Pt(1, 1)),
             "x = (%s + %s) : 2 = %s; y = (%s + %s) : 2 = %s: <b>M%s</b>." % (t(x1), t(x2), t(mx), t(y1), t(y2), t(my), Pt(mx, my)))


def s2_distanza():
    a, b, c = R.choice(TERNE)
    x1, y1 = nz(-6, 6), nz(-6, 6)
    sx, sy = R.choice([1, -1]), R.choice([1, -1])
    x2, y2 = x1 + sx * a, y1 + sy * b
    if max(abs(x2), abs(y2)) > 12:
        return None
    return M("Calcola la distanza tra A%s e B%s." % (Pt(x1, y1), Pt(x2, y2)), str(c), W(a + b, c + 1, c * c, abs(abs(x2) - abs(x1)) + abs(abs(y2) - abs(y1)) if abs(abs(x2) - abs(x1)) + abs(abs(y2) - abs(y1)) != c else None),
             "Δx = %s − (%s) = %s, Δy = %s − (%s) = %s; AB = √(%d² + %d²) = √%d = <b>%d</b>." % (t(x2), t(x1), t(x2 - x1), t(y2), t(y1), t(y2 - y1), a, b, c * c, c))


def s3_mq():
    m = R.choice([Fr(v) for v in (-4, -3, -2, -1, 1, 2, 3, 4)] + [Fr(1, 2), Fr(-1, 2), Fr(2, 3), Fr(-3, 4)])
    q = Fr(R.randint(-8, 8))
    k = R.choice(["m", "q", "cresc"])
    e = eq(m, q)
    if k == "m":
        return M("Qual è il coefficiente angolare della retta %s?" % e, t(m) if m.denominator == 1 else ("−" if m < 0 else "") + fq(abs(m)), W(t(q) if q != m else None, t(-m) if m.denominator == 1 else ("" if m < 0 else "−") + fq(abs(m)), "x", "1" if m != 1 else "0"),
                 "In y = mx + q il coefficiente angolare è il numero che moltiplica x: <b>m = %s</b>." % (t(m) if m.denominator == 1 else ("−" if m < 0 else "") + fq(abs(m))))
    if k == "q":
        return M("In quale punto la retta %s taglia l’asse y?" % e, Pt(0, q), W(Pt(q, 0) if q else Pt(1, 0), Pt(0, m) if m.denominator == 1 and m != q else None, Pt(0, -q) if q else Pt(0, 1), Pt(0, q + m) if (q + m).denominator == 1 and m != 0 else None, Pt(0, q - 1), Pt(0, q + 2)),
                 "Per x = 0 si ha y = q = %s: <b>%s</b>." % (t(q), Pt(0, q)))
    ans = "crescente" if m > 0 else "decrescente"
    return M("La retta %s è…" % e, ans, ["decrescente" if m > 0 else "crescente", "parallela all’asse x", "parallela all’asse y"], "m = %s è %s: la retta è <b>%s</b>." % (t(m) if m.denominator == 1 else fq(m), "positivo" if m > 0 else "negativo", ans))


def s3_appartiene():
    m, q = nz(-3, 3), R.randint(-5, 5)
    x = nz(-4, 4)
    y = m * x + q
    good = Pt(x, y)
    bad = [Pt(x, y + 1), Pt(y, x) if y != x else Pt(x, -y) if y else Pt(x, 1), Pt(-x, y), Pt(x, -y) if y else Pt(x, 2)]
    return M("Quale punto appartiene alla retta %s?" % eq(m, q), good, W(*bad), "Per x = %s: y = %s · (%s) %s %d = %s. Il punto è <b>%s</b>." % (t(x), t(m), t(x), "+" if q >= 0 else "−", abs(q), t(y), good))


def s4_grafico():
    m = Fr(nz(-3, 3))
    q = Fr(R.randint(-3, 3))
    if R.random() < 0.3:
        m = Fr(R.choice([1, -1]), 2)
    pic = kosy([(m, q, BLUE, "")], [], -5, 5, 24, "piano cartesiano con una retta")
    others = [eq(-m, q), eq(m, -q) if q else eq(m, 1), eq(q, m) if q and m.denominator == 1 and q != m else eq(m * 2, q), eq(m, q + 1)]
    return M("%sQual è l’equazione della retta disegnata?" % pic, eq(m, q), W(*[o for o in others if o != eq(m, q)]),
             "La retta taglia l’asse y in %s, quindi q = %s; spostandosi di 1 a destra, y cambia di %s: m = %s. <b>%s</b>." % (Pt(0, q), t(q), t(m) if m.denominator == 1 else ("−" if m < 0 else "") + "½", t(m) if m.denominator == 1 else ("−" if m < 0 else "") + "½", eq(m, q)))


def s4_par_perp():
    m = R.choice([Fr(2), Fr(3), Fr(-2), Fr(1, 2), Fr(-1, 3), Fr(4), Fr(-1), Fr(3, 2)])
    q = Fr(R.randint(-6, 6))
    k = R.choice(["par", "perp"])
    q2 = q + nz(-4, 4)
    if k == "par":
        return M("Quale retta è parallela a %s?" % eq(m, q), eq(m, q2), W(eq(-m, q2), eq(1 / m, q2), eq(-1 / m, q2)), "Rette parallele hanno lo stesso coefficiente angolare m = %s: <b>%s</b>." % (fq(m), eq(m, q2)))
    return M("Quale retta è perpendicolare a %s?" % eq(m, q), eq(-1 / m, q2), W(eq(m, q2), eq(-m, q2), eq(1 / m, q2)), "Rette perpendicolari: m · m′ = −1, quindi m′ = −1/m = %s: <b>%s</b>." % (fq(-1 / m) if (-1 / m) > 0 else "−" + fq(1 / m), eq(-1 / m, q2)))


def s5_assi():
    m, q = nz(-4, 4), nz(-8, 8)
    if q % m:
        return None
    x0 = Fr(-q, m)
    return M("In quale punto la retta %s taglia l’asse x?" % eq(m, q), Pt(x0, 0), W(Pt(0, q), Pt(-x0, 0), Pt(q, 0) if q != x0 else Pt(x0 + 1, 0), Pt(Fr(q, m), 0) if Fr(q, m) != x0 else None),
             "Sull’asse x y = 0: 0 = %s → x = %s. <b>%s</b>." % (show(PP([(m, {"x": 1}), (q, {})])), t(x0), Pt(x0, 0)))


def s5_due_punti():
    m, q = nz(-3, 3), R.randint(-5, 5)
    x1, x2 = R.sample(range(-4, 5), 2)
    y1, y2 = m * x1 + q, m * x2 + q
    return M("Qual è l’equazione della retta che passa per A%s e B%s?" % (Pt(x1, y1), Pt(x2, y2)), eq(m, q), W(eq(-m, q), eq(m, -q) if q else eq(m, 2), eq(Fr(x2 - x1, y2 - y1), q) if Fr(x2 - x1, y2 - y1) != m else None, eq(m, y1) if y1 != q else eq(m, q + 1)),
             "m = (%s − (%s)) : (%s − (%s)) = %s; q = %s − (%s) · (%s) = %s. <b>%s</b>." % (t(y2), t(y1), t(x2), t(x1), t(m), t(y1), t(m), t(x1), t(q), eq(m, q)))


def s5_incontro():
    x, y = nz(-4, 4), nz(-5, 5)
    m1, m2 = nz(-3, 3), nz(-3, 3)
    if m1 == m2:
        return None
    q1, q2 = y - m1 * x, y - m2 * x
    return M("In quale punto si incontrano le rette %s e %s?" % (eq(m1, q1), eq(m2, q2)), Pt(x, y), W(Pt(y, x) if x != y else Pt(x, -y), Pt(-x, y), Pt(x, -y), Pt(0, q1) if (0, q1) != (x, y) else None),
             "%s = %s → x = %s; y = %s. <b>%s</b>." % (show(PP([(m1, {"x": 1}), (q1, {})])), show(PP([(m2, {"x": 1}), (q2, {})])), t(x), t(y), Pt(x, y)))


def main():
    seen = set()
    sets = [
        ("Quadranti e punto medio", mix(R, seen, [(s1_quadrante, 10), (s1_medio, 10)])),
        ("Distanza tra due punti", mix(R, seen, [(s2_distanza, 20)])),
        ("Coefficiente angolare e ordinata all’origine", mix(R, seen, [(s3_mq, 12), (s3_appartiene, 8)])),
        ("Grafici, rette parallele e perpendicolari", mix(R, seen, [(s4_grafico, 10), (s4_par_perp, 10)])),
        ("Assi, retta per due punti e intersezioni", mix(R, seen, [(s5_assi, 6), (s5_due_punti, 7), (s5_incontro, 7)])),
    ]
    body = L(["Gli assi dividono il piano in <b>quattro quadranti</b>: I (+; +), II (−; +), III (−; −), IV (+; −).",
              "<b>Punto medio</b>: M((x₁ + x₂) : 2; (y₁ + y₂) : 2). <b>Distanza</b>: AB = √((x₂ − x₁)² + (y₂ − y₁)²) (teorema di Pitagora).",
              "La funzione <b>y = mx + q</b> ha per grafico una retta: <b>m</b> è il coefficiente angolare (pendenza), <b>q</b> l’ordinata del punto in cui taglia l’asse y. Se q = 0 la retta passa per l’origine (proporzionalità diretta).",
              "Rette <b>parallele</b>: stesso m. Rette <b>perpendicolari</b>: m · m′ = −1."],
             [("Retta per A(1; 5) e B(3; 9)", ["m = (9 − 5) : (3 − 1) = 2", "q = 5 − 2 · 1 = 3"], "y = 2x + 3")],
             [["Scambiare m e q", "In y = 3x − 2: m = 3 (davanti a x), q = −2."],
              ["Sbagliare i segni nella distanza", "Si sottraggono le coordinate con le parentesi: 4 − (−2) = 6."],
              ["Perpendicolare = coefficiente opposto", "Il coefficiente della perpendicolare è −1/m: per m = 2 è −1/2."]],
             table(["Retta", "m", "q"], [["y = 2x + 3", "2", "3"], ["y = −x", "−1", "0"], ["y = 4", "0", "4"]]))
    faq = [("Che cosa indica il coefficiente angolare?", "Di quanto cambia y quando x aumenta di 1: se m è positivo la retta sale, se è negativo scende."),
           ("Perché la retta y = 2x passa per l’origine?", "Perché q = 0: per x = 0 si ha y = 0. Le grandezze direttamente proporzionali hanno grafici di questo tipo.")]
    unit(G, R, "piano-cartesiano-e-retta", "F",
         "Usare il piano cartesiano per rappresentare relazioni e funzioni empiriche o ricavate da tabelle, e per conoscere in particolare le funzioni del tipo y = ax, y = a/x e i loro grafici e collegarle al concetto di proporzionalità",
         "Piano cartesiano e retta", "La retta",
         "Schede di matematica per la terza media sul piano cartesiano e la retta: quadranti, punto medio, distanza, y = mx + q, coefficiente angolare, rette parallele e perpendicolari, retta per due punti e intersezioni. 100 esercizi con soluzioni.",
         "y = mx + q: m pendenza, q ordinata all’origine.", "Parallele: stesso m. Perpendicolari: m · m′ = −1.",
         body, faq, sets, 7)


if __name__ == "__main__":
    main()
