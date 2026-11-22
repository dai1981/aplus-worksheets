# -*- coding: utf-8 -*-
"""
France Maths Seconde : Vecteurs et coordonnées (coordonnées d’un vecteur, norme, distance, milieu, déterminant et colinéarité)
  python3 tools/gen_fr_maths_seconde_coordonnees_et_colinearite.py
Erreurs : x_A − x_B, milieu = différence ÷ 2, norme sans racine, det = xy′ + x′y.
"""
import random
import math
from fr_c4 import *
import de_k8

R = random.Random(60513)
K = Kids(R)


def V(s):
    return "<span class='vec'>%s</span>" % s


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def P():
    return R.randint(-6, 6), R.randint(-6, 6)


def s1():
    (ax, ay), (bx, by) = P(), P()
    if (ax, ay) == (bx, by):
        return None
    k = R.choice(["vec", "vec", "som", "kv"])
    if k == "vec":
        return M("A%s et B%s. Quelles sont les coordonnées de %s ?" % (co(ax, ay), co(bx, by), V("AB")), co(bx - ax, by - ay), [co(ax - bx, ay - by), co(ax + bx, ay + by), co(by - ay, bx - ax) if (by - ay, bx - ax) != (bx - ax, by - ay) else co(bx - ax + 1, by - ay)],
                 "%s(x<sub>B</sub> − x<sub>A</sub> ; y<sub>B</sub> − y<sub>A</sub>) = <b>%s</b>." % (V("AB"), co(bx - ax, by - ay)))
    if k == "som":
        return M("%s%s et %s%s. Quelles sont les coordonnées de %s + %s ?" % (V("u"), co(ax, ay), V("v"), co(bx, by), V("u"), V("v")), co(ax + bx, ay + by), [co(ax - bx, ay - by), co(ax * bx, ay * by), co(ax + ay, bx + by)],
                 "On additionne les coordonnées : <b>%s</b>." % co(ax + bx, ay + by))
    kk = R.choice([2, 3, -2, -1, Fr(1, 2)])
    return M("%s%s. Quelles sont les coordonnées de %s%s ?" % (V("u"), co(ax, ay), fq(kk) if kk != -1 else MINUS, V("u")), co(kk * ax, kk * ay), [co(kk * ax, ay), co(ax + kk, ay + kk), co(-kk * ax, -kk * ay) if (ax, ay) != (0, 0) else co(1, 1)],
             "On multiplie chaque coordonnée par %s : <b>%s</b>." % (fq(kk), co(kk * ax, kk * ay)))


def s2():
    (ax, ay), (bx, by) = P(), P()
    if (ax, ay) == (bx, by):
        return None
    k = R.choice(["mil", "mil", "dist", "norme"])
    if k == "mil":
        mx, my = Fr(ax + bx, 2), Fr(ay + by, 2)
        return M("A%s et B%s. Quelles sont les coordonnées du milieu de [AB] ?" % (co(ax, ay), co(bx, by)), co(mx, my), [co(Fr(bx - ax, 2), Fr(by - ay, 2)), co(ax + bx, ay + by), co(Fr(ax + ay, 2), Fr(bx + by, 2)) if (Fr(ax + ay, 2), Fr(bx + by, 2)) != (mx, my) else co(mx + 1, my)],
                 "Milieu : ((x<sub>A</sub> + x<sub>B</sub>) ÷ 2 ; (y<sub>A</sub> + y<sub>B</sub>) ÷ 2) = <b>%s</b>." % co(mx, my))
    dx, dy = bx - ax, by - ay
    s_ = dx * dx + dy * dy
    r = math.isqrt(s_)
    exact = "%d" % r if r * r == s_ else "√%d" % s_
    if k == "dist":
        return M("A%s et B%s. Calcule la distance AB (valeur exacte)." % (co(ax, ay), co(bx, by)), exact, ["%d" % (abs(dx) + abs(dy)), "%d" % s_, "√%d" % (abs(dx * dx - dy * dy)) if dx * dx != dy * dy else "%d" % (abs(dx) * 2)],
                 "AB = √((%s)² + (%s)²) = √%d = <b>%s</b>." % (d(dx), d(dy), s_, exact))
    return M("Calcule la norme du vecteur %s%s (valeur exacte)." % (V("u"), co(dx, dy)), exact, ["%d" % (abs(dx) + abs(dy)), "%d" % s_, "√%d" % (abs(dx) + abs(dy)) if abs(dx) + abs(dy) != s_ else "%d" % (s_ + 1)],
             "‖%s‖ = √(x² + y²) = √%d = <b>%s</b>." % (V("u"), s_, exact))


def s3():
    a, b = R.randint(-6, 6), R.randint(-6, 6)
    c, e = R.randint(-6, 6), R.randint(-6, 6)
    k = R.choice(["det", "det", "col", "find"])
    if k == "det":
        D = a * e - b * c
        return M("Calcule det(%s, %s) avec %s%s et %s%s." % (V("u"), V("v"), V("u"), co(a, b), V("v"), co(c, e)), d(D), [d(a * e + b * c), d(a * c - b * e), d(-D) if D else "1"],
                 "det = xy′ − yx′ = %s × %s − %s × %s = <b>%s</b>." % (d(a), par(e), d(b), par(c), d(D)))
    if k == "col":
        kk = R.choice([2, 3, -2, Fr(1, 2), -1])
        ok = R.random() < 0.5
        if (a, b) == (0, 0):
            return None
        c2, e2 = kk * a, kk * b + (0 if ok else R.choice([1, -1]))
        D = a * e2 - b * c2
        return M("%s%s et %s%s sont-ils colinéaires ?" % (V("u"), co(a, b), V("v"), co(c2, e2)), "oui" if D == 0 else "non", ["non" if D == 0 else "oui", "seulement s’ils ont la même norme", "on ne peut pas savoir"],
                 "det = %s × %s − %s × %s = %s : <b>%s</b>." % (d(a), par(e2), d(b), par(c2), d(D), "colinéaires" if D == 0 else "non colinéaires"))
    if a == 0 or b == 0:
        return None
    kk = R.choice([2, 3, -2, -3, Fr(1, 2)])
    y = kk * b
    return M("Pour quelle valeur de y les vecteurs %s%s et %s(%s ; y) sont-ils colinéaires ?" % (V("u"), co(a, b), V("v"), d(kk * a)), "y = %s" % d(y), ["y = %s" % d(Fr(b, kk)) if Fr(b, kk) != y else "y = %s" % d(y + 1), "y = %s" % d(-y) if y else "y = 1", "y = %s" % d(kk * a)] if kk * a != y else ["y = %s" % d(Fr(b, kk)), "y = %s" % d(-y), "y = %s" % d(y + 2)],
             "det = %s × y − %s × %s = 0 ⇔ y = <b>%s</b>." % (d(a), par(b), par(kk * a), d(y)))


def s4():
    (ax, ay) = P()
    ux, uy = R.choice([(1, 2), (2, 1), (1, -1), (2, -3), (3, 1), (1, 3)])
    t1, t2 = R.sample([-2, -1, 1, 2, 3], 2)
    bx, by = ax + t1 * ux, ay + t1 * uy
    cx, cy = ax + t2 * ux, ay + t2 * uy
    ok = R.random() < 0.5
    if not ok:
        cy += R.choice([1, -1])
    k = R.choice(["align", "para"])
    if k == "align":
        D = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        return M("A%s, B%s et C%s sont-ils alignés ?" % (co(ax, ay), co(bx, by), co(cx, cy)), "oui" if D == 0 else "non", ["non" if D == 0 else "oui", "seulement si AB = AC", "on ne peut pas savoir"],
                 "%s%s et %s%s : det = %s, %s." % (V("AB"), co(bx - ax, by - ay), V("AC"), co(cx - ax, cy - ay), d(D), "<b>alignés</b>" if D == 0 else "<b>non alignés</b>"))
    dx, dy = P()
    ex, ey = dx + t2 * ux, dy + t2 * uy + (0 if ok else R.choice([1, -1]))
    D = (bx - ax) * (ey - dy) - (by - ay) * (ex - dx)
    return M("A%s, B%s, C%s, D%s. Les droites (AB) et (CD) sont-elles parallèles ?" % (co(ax, ay), co(bx, by), co(dx, dy), co(ex, ey)), "oui" if D == 0 else "non", ["non" if D == 0 else "oui", "seulement si AB = CD", "on ne peut pas savoir"],
             "%s%s et %s%s : det = %s, %s." % (V("AB"), co(bx - ax, by - ay), V("CD"), co(ex - dx, ey - dy), d(D), "<b>parallèles</b>" if D == 0 else "<b>non parallèles</b>"))


def s5():
    k = R.choice(["para", "para", "sym", "graph"])
    if k == "para":
        (ax, ay), (bx, by), (cx, cy) = P(), P(), P()
        if len({(ax, ay), (bx, by), (cx, cy)}) < 3 or (bx - ax) * (cy - ay) == (by - ay) * (cx - ax):
            return None
        return M("A%s, B%s, C%s. Quelles sont les coordonnées de D pour que ABCD soit un parallélogramme ?" % (co(ax, ay), co(bx, by), co(cx, cy)), co(ax + cx - bx, ay + cy - by),
                 [co(cx + bx - ax, cy + by - ay), co(bx + cx, by + cy), co(Fr(ax + cx, 2), Fr(ay + cy, 2))],
                 "ABCD parallélogramme ⇔ %s = %s : D = A + %s = <b>%s</b>." % (V("AD"), V("BC"), V("BC"), co(ax + cx - bx, ay + cy - by)))
    if k == "sym":
        (ax, ay), (ix, iy) = P(), P()
        if (ax, ay) == (ix, iy):
            return None
        return M("Quelles sont les coordonnées du symétrique de A%s par rapport à I%s ?" % (co(ax, ay), co(ix, iy)), co(2 * ix - ax, 2 * iy - ay), [co(Fr(ax + ix, 2), Fr(ay + iy, 2)), co(ix - ax, iy - ay), co(2 * ax - ix, 2 * ay - iy)],
                 "I est le milieu de [AA’] : A’ = (2x<sub>I</sub> − x<sub>A</sub> ; 2y<sub>I</sub> − y<sub>A</sub>) = <b>%s</b>." % co(2 * ix - ax, 2 * iy - ay))
    (ax, ay) = (R.randint(-4, 1), R.randint(-4, 1))
    ux, uy = R.randint(1, 4), R.randint(-3, 3)
    bx, by = ax + ux, ay + uy
    if not (-5 <= by <= 5):
        return None
    svg = relabel(de_k8.kosy(pts=[(ax, ay, "A"), (bx, by, "B")], lo=-5, hi=5, u=22), "points A et B")
    return M("<div class='qfig'>%s</div>Lis les coordonnées du vecteur %s." % (svg, V("AB")), co(ux, uy), [co(-ux, -uy), co(bx, by) if (bx, by) != (ux, uy) else co(ax, ay), co(uy, ux) if uy != ux else co(ux + 1, uy)],
             "De A à B : %s en abscisse, %s en ordonnée : <b>%s</b>." % (d(ux), d(uy), co(ux, uy)))


def main():
    seen = set()
    sets = [("Coordonnées de vecteurs", mix(R, seen, [(s1, 20)])), ("Milieu, distance et norme", mix(R, seen, [(s2, 20)])),
            ("Déterminant et colinéarité", mix(R, seen, [(s3, 20)])), ("Alignement et parallélisme", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un repère orthonormé : %s(x<sub>B</sub> − x<sub>A</sub> ; y<sub>B</sub> − y<sub>A</sub>), ‖%s(x ; y)‖ = √(x² + y²), et le milieu de [AB] a pour coordonnées les moyennes." % (V("AB"), V("u")),
              "det(%s, %s) = xy′ − yx′. Deux vecteurs sont <b>colinéaires</b> si et seulement si leur déterminant est nul." % (V("u"), V("v")),
              "A, B, C alignés ⇔ %s et %s colinéaires ; (AB) // (CD) ⇔ %s et %s colinéaires." % (V("AB"), V("AC"), V("AB"), V("CD"))],
             [("%s(2 ; −3) et %s(−4 ; 6)" % (V("u"), V("v")), ["det = 2 × 6 − (−3) × (−4)", "= 12 − 12 = 0"], "colinéaires")],
             [["Calculer x<sub>A</sub> − x<sub>B</sub>", "On fait « arrivée − départ »."], ["Oublier la racine dans la norme", "‖u‖ = √(x² + y²)."], ["det = xy′ + x′y", "C’est une différence : xy′ − yx′."]])
    faq = [("Pourquoi un repère orthonormé ?", "Les formules de distance et de norme utilisent le théorème de Pythagore : il faut des axes perpendiculaires et la même unité."),
           ("Que signifie un déterminant nul ?", "Les vecteurs ont la même direction : l’un est un multiple de l’autre.")]
    unit("seconde", R, "coordonnees-et-colinearite", "G",
         "Calculer les coordonnées d’un vecteur, d’une somme et d’un produit par un réel ; calculer une distance, une norme et les coordonnées d’un milieu ; utiliser le déterminant pour étudier la colinéarité, l’alignement et le parallélisme",
         "Vecteurs et coordonnées", "Coordonnées et colinéarité",
         "Fiches de maths seconde sur les vecteurs dans un repère : coordonnées, norme, distance, milieu, déterminant, colinéarité, alignement et parallélisme. 100 exercices corrigés.",
         "det(u→, v→) = xy′ − yx′ = 0 ⇔ colinéaires", "AB = √((x_B − x_A)² + (y_B − y_A)²)", body, faq, sets, 13)


if __name__ == "__main__":
    main()
