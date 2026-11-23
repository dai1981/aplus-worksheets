# -*- coding: utf-8 -*-
"""
Italia Matematica terza liceo: La circonferenza nel piano cartesiano (Geometria)
  python3 tools/gen_it_matematica_l3_circonferenza_nel_piano_cartesiano.py
Equazione (x − α)² + (y − β)² = r² e forma x² + y² + ax + by + c = 0, centro e raggio, condizione di realtà,
circonferenza di diametro AB, posizione di un punto e di una retta, retta tangente in un punto (perpendicolare al raggio),
intersezioni con gli assi.
Errori: centro (a/2; b/2) senza il segno meno, r² scambiato con r, equazioni con x² e y² di coefficienti diversi.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, WP, fq, nz, P, show, simp_root

R = random.Random(72306)
G = "terza-liceo"


def pt(x, y, n=""):
    return "%s(%s; %s)" % (n, fq(x), fq(y))


def gen(al, be, r2):
    a, b, c = -2 * al, -2 * be, al * al + be * be - r2
    return "%s = 0" % show(P([(1, {"x": 2}), (1, {"y": 2}), (a, {"x": 1}), (b, {"y": 1}), (c, {})]))


def std(al, be, r2):
    xs = "x²" if al == 0 else "(x %s %s)²" % ("−" if al > 0 else "+", fq(abs(al)))
    ys = "y²" if be == 0 else "(y %s %s)²" % ("−" if be > 0 else "+", fq(abs(be)))
    return "%s + %s = %s" % (xs, ys, fq(r2))


def rt(n):
    n = Fr(n)
    if n.denominator != 1:
        return "√(%s)" % fq(n)
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def s1_eq():
    al, be = R.randint(-5, 5), R.randint(-5, 5)
    r = R.randint(1, 6)
    ans = gen(al, be, r * r)
    w = [gen(-al, -be, r * r) if (al, be) != (0, 0) else gen(1, 0, r * r), gen(al, be, r), gen(al, be, -r * r) if al * al + be * be > r * r else gen(al, be, r * r + 1)]
    return M("Scrivi l’equazione della circonferenza di centro %s e raggio %d." % (pt(al, be, "C"), r), ans, [x for x in w if x != ans],
             "%s; sviluppando: <b>%s</b>." % (std(al, be, r * r), ans))


def s1_cr():
    al, be = R.randint(-5, 5), R.randint(-5, 5)
    r2 = R.choice([1, 4, 9, 16, 25, 2, 5, 8, 10, 13, 18, 20])
    t = R.choice(["C", "r"])
    q = gen(al, be, r2)
    if t == "C":
        return M("Qual è il centro della circonferenza %s?" % q, pt(al, be, "C"), [pt(-al, -be, "C") if (al, be) != (0, 0) else pt(1, 1, "C"), pt(-2 * al, -2 * be, "C") if (al, be) != (0, 0) else pt(2, 0, "C"), pt(be, al, "C") if al != be else pt(al, be + 1, "C")],
                 "C(−a/2; −b/2) = <b>%s</b>." % pt(al, be, "C"))
    return M("Qual è il raggio della circonferenza %s?" % q, rt(r2), [x for x in W(fq(r2), rt(r2 + 2 * (al * al + be * be)) if al or be else rt(r2 + 1), rt(abs(al * al + be * be - r2)) if al * al + be * be != r2 else "0", rt(2 * r2)) if x != rt(r2)],
             "r = √(a²/4 + b²/4 − c) = √(%d + %d − (%s)) = √%d = <b>%s</b>." % (al * al, be * be, fq(al * al + be * be - r2), r2, rt(r2)))


def s2_real():
    al, be = R.randint(-4, 4), R.randint(-4, 4)
    c = R.randint(-10, 30)
    r2 = al * al + be * be - c
    q = "%s = 0" % show(P([(1, {"x": 2}), (1, {"y": 2}), (-2 * al, {"x": 1}), (-2 * be, {"y": 1}), (c, {})]))
    ans = "sì, raggio %s" % rt(r2) if r2 > 0 else ("no, si riduce a un punto" if r2 == 0 else "no, nessun punto reale")
    w = ["sì, raggio %s" % rt(abs(r2) + 1), "no, nessun punto reale", "no, si riduce a un punto", "sì, raggio %s" % rt(c) if c > 0 else "sì, raggio 1"]
    return M("L’equazione %s rappresenta una circonferenza reale?" % q, ans, [x for x in w if x != ans][:3],
             "a²/4 + b²/4 − c = %d + %d − (%s) = %s: %s" % (al * al, be * be, fq(c), fq(r2), "<b>%s</b>." % ans))


def s2_diam():
    x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
    x2, y2 = x1 + 2 * nz(R, -3, 3), y1 + 2 * R.randint(-3, 3)
    al, be = (x1 + x2) // 2, (y1 + y2) // 2
    r2 = (x1 - al) ** 2 + (y1 - be) ** 2
    ans = std(al, be, r2)
    w = [std(al, be, 4 * r2), std(-al, -be, r2) if (al, be) != (0, 0) else std(1, 0, r2), std(al, be, int(math.sqrt(r2)) if math.isqrt(r2) ** 2 == r2 else 2 * r2)]
    return M("Scrivi l’equazione della circonferenza di diametro AB con %s e %s." % (pt(x1, y1, "A"), pt(x2, y2, "B")), ans, [x for x in w if x != ans],
             "Centro nel punto medio M%s; raggio = AM, r² = %d: <b>%s</b>." % (pt(al, be), r2, ans))


def s3_punto():
    al, be = R.randint(-4, 4), R.randint(-4, 4)
    r = R.randint(2, 6)
    dx, dy = R.randint(-7, 7), R.randint(-7, 7)
    d2 = dx * dx + dy * dy
    ans = "interno" if d2 < r * r else "sulla circonferenza" if d2 == r * r else "esterno"
    return M("Il punto %s rispetto alla circonferenza %s è…" % (pt(al + dx, be + dy, "P"), std(al, be, r * r)), ans, [o for o in ["interno", "sulla circonferenza", "esterno", "il centro"] if o != ans],
             "Distanza al quadrato dal centro: %d, contro r² = %d: <b>%s</b>." % (d2, r * r, ans))


def s3_retta():
    al, be = R.randint(-4, 4), R.randint(-4, 4)
    r = R.choice([5, 10, 13, 5, 10])
    a, b = R.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (0, 1), (1, 0)])
    nn = int(math.sqrt(a * a + b * b))
    dist = R.choice([r * nn, r * nn - R.randint(1, 5), r * nn + R.randint(1, 5)])
    c = dist - a * al - b * be
    d_ = Fr(abs(a * al + b * be + c), nn)
    ans = "secante" if d_ < r else "tangente" if d_ == r else "esterna"
    rq = "%s = 0" % show(P([(a, {"x": 1}), (b, {"y": 1}), (c, {})]))
    return M("Com’è la retta %s rispetto alla circonferenza %s?" % (rq, std(al, be, r * r)), ans, [o for o in ["secante", "tangente", "esterna", "passa per il centro"] if o != ans],
             "Distanza del centro dalla retta: |%d|/%d = %s, raggio %d: <b>%s</b>." % (a * al + b * be + c, nn, fq(d_), r, ans))


def s4_tang():
    al, be = R.randint(-3, 3), R.randint(-3, 3)
    dx, dy = R.choice([(3, 4), (4, 3), (-3, 4), (3, -4), (0, 5), (5, 0), (-4, -3), (1, 2), (2, -1), (2, 1)])
    x0, y0 = al + dx, be + dy
    r2 = dx * dx + dy * dy
    # tangente: dx(x − x0) + dy(y − y0) = 0
    c = -(dx * x0 + dy * y0)
    ans = "%s = 0" % show(P([(dx, {"x": 1}), (dy, {"y": 1}), (c, {})]))
    w = ["%s = 0" % show(P([(dy, {"x": 1}), (-dx, {"y": 1}), (-(dy * x0 - dx * y0), {})])), "%s = 0" % show(P([(dx, {"x": 1}), (dy, {"y": 1}), (-c, {})])) if c else "%s = 0" % show(P([(dx, {"x": 1}), (dy, {"y": 1}), (1, {})])),
         "%s = 0" % show(P([(dx, {"x": 1}), (dy, {"y": 1}), (-(dx * al + dy * be), {})]))]
    return M("Scrivi la retta tangente alla circonferenza %s nel suo punto %s." % (std(al, be, r2), pt(x0, y0, "P")), ans, [x for x in w if x != ans],
             "La tangente è perpendicolare al raggio CP, che ha direzione (%s; %s): %s(%s) %s %s(%s) = 0 → <b>%s</b>." % (fq(dx), fq(dy), fq(dx), show(P([(1, {"x": 1}), (-x0, {})])), "+" if dy >= 0 else "−", fq(abs(dy)), show(P([(1, {"y": 1}), (-y0, {})])), ans))


def s5_assi():
    al, be = R.randint(-4, 4), R.randint(-4, 4)
    r2 = al * al + be * be
    if r2 == 0:
        return None
    # passa per l’origine: incontra gli assi in (0;0), (2α;0), (0;2β)
    q = gen(al, be, r2)
    t = R.choice(["x", "y"])
    if t == "x":
        ans = "(0; 0) e (%s; 0)" % fq(2 * al) if al else "solo (0; 0) (tangente all’asse x)"
        w = ["(0; 0) e (%s; 0)" % fq(-2 * al) if al else "(0; 0) e (1; 0)", "(0; 0) e (%s; 0)" % fq(al) if al else "nessun punto", "(%s; 0) e (%s; 0)" % (fq(al), fq(be)) if (al, be) != (0, 0) else "(1; 0)"]
        e = "Pongo y = 0: %s = 0 → <b>%s</b>." % (show(P([(1, {"x": 2}), (-2 * al, {"x": 1})])), ans)
    else:
        ans = "(0; 0) e (0; %s)" % fq(2 * be) if be else "solo (0; 0) (tangente all’asse y)"
        w = ["(0; 0) e (0; %s)" % fq(-2 * be) if be else "(0; 0) e (0; 1)", "(0; 0) e (0; %s)" % fq(be) if be else "nessun punto", "(0; %s) e (0; %s)" % (fq(al), fq(be)) if (al, be) != (0, 0) else "(0; 1)"]
        e = "Pongo x = 0: %s = 0 → <b>%s</b>." % (show(P([(1, {"y": 2}), (-2 * be, {"y": 1})])), ans)
    return M("In quali punti la circonferenza %s incontra l’asse %s?" % (q, t), ans, [x for x in w if x != ans], e)


def main():
    seen = set()
    sets = [
        ("Equazione dati centro e raggio", mix(R, seen, [(s1_eq, 14), (s2_diam, 6)])),
        ("Centro e raggio", mix(R, seen, [(s1_cr, 14), (s2_real, 6)])),
        ("Posizione di punti e rette", mix(R, seen, [(s3_punto, 8), (s3_retta, 12)])),
        ("Retta tangente", mix(R, seen, [(s4_tang, 20)])),
        ("Intersezioni e riepilogo", mix(R, seen, [(s5_assi, 10), (s2_diam, 5), (s2_real, 5)])),
    ]
    body = L(["La circonferenza è il luogo dei punti che hanno distanza r da un centro C(α; β): (x − α)² + (y − β)² = r². Sviluppando si ottiene x² + y² + ax + by + c = 0.",
              "Dalla forma x² + y² + ax + by + c = 0: centro C(−a/2; −b/2), raggio r = √(a²/4 + b²/4 − c). Se il radicando è negativo non c’è nessun punto reale.",
              "Un punto è interno, sulla circonferenza o esterno se la sua distanza dal centro è minore, uguale o maggiore di r. Una retta è secante, tangente o esterna se la distanza del centro dalla retta è minore, uguale o maggiore di r.",
              "La tangente in un punto P della circonferenza è perpendicolare al raggio CP."],
             [("x² + y² − 6x + 4y − 3 = 0", ["C(3; −2)", "r = √(9 + 4 + 3)"], "C(3; −2), r = 4"),
              ("Centro (1; 2), r = 3", ["(x − 1)² + (y − 2)² = 9"], "x² + y² − 2x − 4y − 4 = 0")],
             [["Centro (a/2; b/2)", "Il centro è (−a/2; −b/2): attenzione ai segni."],
              ["Scrivere r invece di r²", "Nell’equazione compare r²: con r = 3 si scrive 9."],
              ["Accettare 2x² + y² = 4", "I coefficienti di x² e y² devono essere uguali (e non c’è il termine xy)."]])
    faq = [("Come si riconosce l’equazione di una circonferenza?", "Deve essere di secondo grado, con x² e y² dello stesso coefficiente, senza il termine xy, e con a²/4 + b²/4 − c &gt; 0."),
           ("Come si trova la tangente da un punto esterno?", "Si scrive il fascio di rette per il punto e si impone che la distanza dal centro sia uguale al raggio (oppure Δ = 0 nel sistema): si trovano due tangenti.")]
    unit(G, R, "circonferenza-nel-piano-cartesiano", "G",
         "Le coniche nel piano cartesiano: la circonferenza come luogo geometrico, equazione, centro e raggio, posizioni di punti e rette, tangenti",
         "La circonferenza nel piano cartesiano", "Circonferenza nel piano cartesiano",
         "Schede di matematica per la terza liceo sulla circonferenza nel piano cartesiano: equazione dati centro e raggio, centro e raggio dall’equazione, diametro, posizione di punti e rette, retta tangente, intersezioni con gli assi. 100 esercizi con soluzioni.",
         "C(−a/2; −b/2), r = √(a²/4 + b²/4 − c)", "La tangente in P è perpendicolare al raggio CP.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
