# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Équations de cercles et paraboles (équation d’un cercle, centre et rayon, cercle de diamètre [AB], appartenance, parabole y = ax² + bx + c : axe, sommet, intersections)
  python3 tools/gen_fr_maths_premiere_equations_de_cercles_et_paraboles.py
Erreurs : (x + a)² pour un centre d’abscisse a, oublier la racine (rayon = r², pas r), signe du centre dans la forme développée, axe y = α au lieu de x = α.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60619)


def co(x, y):
    return "(%s ; %s)" % (fq(x), fq(y))


def sqf(v, a):
    """(v − a)²"""
    if a == 0:
        return "%s²" % v
    return "(%s %s %s)²" % (v, MINUS if a > 0 else "+", fq(abs(a)))


def ceq(a, b, r2):
    return "%s + %s = %s" % (sqf("x", a), sqf("y", b), d(r2))


def deq(a, b, r2):
    """x² + y² − 2ax − 2by + (a² + b² − r²) = 0"""
    return "%s = 0" % expr([(1, "x²"), (1, "y²"), (-2 * a, "x"), (-2 * b, "y"), (a * a + b * b - r2, "")])


def s1():
    a, b, r = R.randint(-6, 6), R.randint(-6, 6), R.randint(1, 9)
    k = R.choice(["eq", "eq", "read", "read"])
    if k == "eq":
        return M("Quelle est une équation du cercle de centre Ω%s et de rayon %d ?" % (co(a, b), r), ceq(a, b, r * r),
                 [ceq(-a, -b, r * r) if (a, b) != (0, 0) else ceq(0, 0, r), ceq(a, b, r) if r > 1 else ceq(a, b, 2), ceq(-a, -b, r) if (a, b) != (0, 0) else ceq(1, 1, r * r), ceq(b, a, r * r) if a != b else ceq(a, -b, r * r) if b else ceq(a + 1, b, r * r)],
                 "M(x ; y) est sur le cercle ⇔ ΩM² = r² : <b>%s</b>." % ceq(a, b, r * r))
    return M("Quels sont le centre et le rayon du cercle d’équation %s ?" % ceq(a, b, r * r), "centre %s, rayon %d" % (co(a, b), r),
             ["centre %s, rayon %d" % (co(-a, -b), r) if (a, b) != (0, 0) else "centre (1 ; 1), rayon %d" % r, "centre %s, rayon %d" % (co(a, b), r * r) if r > 1 else "centre %s, rayon 2" % co(a, b), "centre %s, rayon %d" % (co(-a, -b), r * r) if (a, b) != (0, 0) else "centre (0 ; 0), rayon %d" % (2 * r)],
             "(x − a)² + (y − b)² = r² : centre (a ; b), rayon r = √%d = <b>%d</b>." % (r * r, r))


def s2():
    a, b, r = nz(R, -6, 6), nz(R, -6, 6), R.randint(1, 8)
    k = R.choice(["cr", "cr", "canon"])
    E2 = deq(a, b, r * r)
    if k == "cr":
        return M("Quels sont le centre et le rayon du cercle d’équation %s ?" % E2, "centre %s, rayon %d" % (co(a, b), r),
                 ["centre %s, rayon %d" % (co(-a, -b), r), "centre %s, rayon %d" % (co(2 * a, 2 * b), r), "centre %s, rayon %s" % (co(a, b), d(abs(a * a + b * b - r * r))) if abs(a * a + b * b - r * r) != r else "centre %s, rayon %d" % (co(a, b), r * r)],
                 "On complète les carrés : %s, donc centre %s et <b>rayon %d</b>." % (ceq(a, b, r * r), co(a, b), r))
    return M("Écris %s sous la forme (x − a)² + (y − b)² = r²." % E2, ceq(a, b, r * r),
             [ceq(-a, -b, r * r), ceq(a, b, r * r - a * a - b * b) if r * r - a * a - b * b > 0 else ceq(a, b, a * a + b * b), ceq(2 * a, 2 * b, r * r)],
             "x² − 2ax = (x − a)² − a² et de même pour y : <b>%s</b>." % ceq(a, b, r * r))


def s3():
    k = R.choice(["diam", "diam", "appart", "passe"])
    if k == "diam":
        A = (R.randint(-6, 6), R.randint(-6, 6))
        B = (A[0] + 2 * R.randint(-4, 4), A[1] + 2 * R.randint(-4, 4))
        if A == B:
            return None
        I = ((A[0] + B[0]) // 2, (A[1] + B[1]) // 2)
        r2 = (B[0] - A[0]) ** 2 // 4 + (B[1] - A[1]) ** 2 // 4
        return M("Quelle est une équation du cercle de diamètre [AB], avec A%s et B%s ?" % (co(*A), co(*B)), ceq(I[0], I[1], r2),
                 [ceq(I[0], I[1], 4 * r2), ceq(A[0], A[1], 4 * r2), ceq(-I[0], -I[1], r2) if I != (0, 0) else ceq(1, 1, r2)],
                 "Centre : milieu I%s ; rayon² = (AB ÷ 2)² = %d : <b>%s</b>." % (co(*I), r2, ceq(I[0], I[1], r2)))
    a, b, r = R.randint(-4, 4), R.randint(-4, 4), R.choice([5, 5, 10, 13])
    vecs = {5: [(3, 4), (4, 3), (0, 5), (-3, 4), (5, 0), (-4, -3)], 10: [(6, 8), (8, 6), (0, 10), (-6, 8)], 13: [(5, 12), (12, 5), (-5, 12), (0, 13)]}[r]
    if k == "appart":
        on = R.random() < 0.5
        v = R.choice(vecs)
        P = (a + v[0], b + v[1] + (0 if on else R.choice([1, -1])))
        val_ = (P[0] - a) ** 2 + (P[1] - b) ** 2
        return M("Le point P%s appartient-il au cercle d’équation %s ?" % (co(*P), ceq(a, b, r * r)), "oui" if on else "non",
                 ["non" if on else "oui", "seulement si P est le centre", "on ne peut pas savoir"],
                 "%s² + %s² = %d %s %d : <b>%s</b>." % (par(P[0] - a), par(P[1] - b), val_, "=" if on else "≠", r * r, "oui" if on else "non"))
    v = R.choice(vecs)
    P = (a + v[0], b + v[1])
    return M("Le cercle de centre Ω%s passe par le point P%s. Quel est son rayon ?" % (co(a, b), co(*P)), str(r), [str(r * r), str(abs(v[0]) + abs(v[1])), sq(abs(v[0] * v[0] - v[1] * v[1])) if v[0] * v[0] != v[1] * v[1] else str(r + 1)],
             "r = ΩP = √(%s² + %s²) = √%d = <b>%d</b>." % (par(v[0]), par(v[1]), r * r, r))


def s4():
    a = R.choice([1, -1, 2, -2, 3])
    al, be = R.randint(-5, 5), R.randint(-9, 9)
    b, c = -2 * a * al, a * al * al + be
    f = P2(a, b, c)
    k = R.choice(["axe", "sommet", "sommet", "oy", "ox"])
    if k == "axe":
        return M("Quel est l’axe de symétrie de la parabole d’équation y = %s ?" % f, "la droite d’équation x = %s" % d(al),
                 ["la droite d’équation x = %s" % d(-al) if al else "la droite d’équation x = 1", "la droite d’équation y = %s" % d(be), "la droite d’équation y = %s" % d(al) if al != be else "la droite d’équation x = %s" % d(be + 1)],
                 "x = −b ÷ (2a) = %s ÷ %s = <b>%s</b>." % (d(-b), par(2 * a), d(al)))
    if k == "sommet":
        return M("Quelles sont les coordonnées du sommet de la parabole d’équation y = %s ?" % f, co(al, be),
                 [co(-al, be) if al else co(1, be), co(al, c) if c != be else co(al, be + 1), co(be, al) if be != al else co(al, -be) if be else co(1, 1)],
                 "x<sub>S</sub> = −b ÷ (2a) = %s ; y<sub>S</sub> = f(%s) = %s : <b>S%s</b>." % (d(al), d(al), d(be), co(al, be)))
    if k == "oy":
        return M("En quel point la parabole d’équation y = %s coupe-t-elle l’axe des ordonnées ?" % f, co(0, c), [co(c, 0) if c else co(1, 0), co(0, be) if be != c else co(0, a), co(0, a) if a != c else co(0, b)],
                 "Pour x = 0, y = c = %s : <b>%s</b>." % (d(c), co(0, c)))
    x1, x2 = sorted(R.sample(range(-6, 7), 2))
    a = R.choice([1, -1, 2])
    b, c = -a * (x1 + x2), a * x1 * x2
    return M("En quels points la parabole d’équation y = %s coupe-t-elle l’axe des abscisses ?" % P2(a, b, c), "%s et %s" % (co(x1, 0), co(x2, 0)),
             ["%s et %s" % (co(0, x1), co(0, x2)), "%s et %s" % (co(-x2, 0), co(-x1, 0)) if x1 != -x2 else "%s seulement" % co(x2, 0), "%s" % co(0, c)],
             "On résout %s = 0 : x = %s ou x = %s, d’où <b>%s et %s</b>." % (P2(a, b, c), d(x1), d(x2), co(x1, 0), co(x2, 0)))


def s5():
    k = R.choice(["inter", "inter", "cercle_axe", "tang"])
    if k == "inter":
        x1, x2 = sorted(R.sample(range(-4, 5), 2))
        m, p = R.randint(-3, 3), R.randint(-4, 4)
        # parabole y = x² + bx + c, droite y = mx + p ; x² + (b − m)x + (c − p) = (x − x1)(x − x2)
        b = m - (x1 + x2)
        c = p + x1 * x2
        y1, y2 = m * x1 + p, m * x2 + p
        return M("Quels sont les points d’intersection de la parabole y = %s et de la droite y = %s ?" % (P2(1, b, c), E((m, "x"), (p, ""))), "%s et %s" % (co(x1, y1), co(x2, y2)),
                 ["%s et %s" % (co(x1, 0), co(x2, 0)), "%s et %s" % (co(-x1, y1), co(-x2, y2)) if x1 != -x2 else "%s seulement" % co(x1, y1), "%s et %s" % (co(y1, x1), co(y2, x2)) if (x1, y1) != (y1, x1) or (x2, y2) != (y2, x2) else "aucun point"],
                 "%s = %s ⇔ %s = 0 ⇔ x = %s ou x = %s ; on calcule y avec la droite : <b>%s et %s</b>." % (P2(1, b, c), E((m, "x"), (p, "")), P2(1, b - m, c - p), d(x1), d(x2), co(x1, y1), co(x2, y2)))
    if k == "cercle_axe":
        a, b = R.randint(-4, 4), R.choice([3, 4, -3, -4, 0])
        r = 5
        h = math.isqrt(r * r - b * b)
        return M("Où le cercle d’équation %s coupe-t-il l’axe des abscisses ?" % ceq(a, b, 25), "%s et %s" % (co(a - h, 0), co(a + h, 0)),
                 ["%s et %s" % (co(a - 5, 0), co(a + 5, 0)) if h != 5 else "%s et %s" % (co(a - 4, 0), co(a + 4, 0)), "%s et %s" % (co(0, b - h), co(0, b + h)), "%s et %s" % (co(-a - h, 0), co(-a + h, 0)) if a else "il ne le coupe pas"],
                 "On pose y = 0 : %s + %s = 25 ⇔ %s = %d ⇔ x = %s ± %d : <b>%s et %s</b>." % (sqf("x", a), "%d" % (b * b), sqf("x", a), h * h, d(a), h, co(a - h, 0), co(a + h, 0)))
    a, b = R.randint(-3, 3), R.randint(-3, 3)
    v = R.choice([(3, 4), (4, 3), (0, 5), (5, 0), (-3, 4), (4, -3)])
    T = (a + v[0], b + v[1])
    c = -v[0] * T[0] - v[1] * T[1]
    return M("Quelle est une équation de la tangente au cercle %s au point T%s ?" % (ceq(a, b, 25), co(*T)), "%s = 0" % expr([(v[0], "x"), (v[1], "y"), (c, "")]),
             ["%s = 0" % expr([(-v[1], "x"), (v[0], "y"), (v[1] * T[0] - v[0] * T[1], "")]), "%s = 0" % expr([(v[0], "x"), (v[1], "y"), (-v[0] * a - v[1] * b, "")]), "%s = 0" % expr([(v[0], "x"), (v[1], "y"), (-c, "")]) if c else "%s = 0" % expr([(v[0], "x"), (v[1], "y"), (1, "")])],
             "Le rayon ΩT(%s ; %s) est normal à la tangente, qui passe par T : <b>%s = 0</b>." % (d(v[0]), d(v[1]), expr([(v[0], "x"), (v[1], "y"), (c, "")])))


def main():
    seen = set()
    sets = [("Équation d’un cercle", mix(R, seen, [(s1, 20)])), ("Centre et rayon à partir de la forme développée", mix(R, seen, [(s2, 20)])),
            ("Diamètre, rayon et appartenance", mix(R, seen, [(s3, 20)])), ("Parabole : axe, sommet, intersections avec les axes", mix(R, seen, [(s4, 20)])), ("Intersections et tangentes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le cercle de centre Ω(a ; b) et de rayon r a pour équation <b>(x − a)² + (y − b)² = r²</b>.",
              "Avec une forme développée x² + y² − 2ax − 2by + k = 0, on complète les carrés : x² − 2ax = (x − a)² − a².",
              "La parabole d’équation y = ax² + bx + c a pour axe de symétrie la droite x = −b ÷ (2a) ; son sommet est S(−b ÷ (2a) ; f(−b ÷ (2a)))."],
             [("x² + y² − 4x + 6y − 3 = 0", ["(x − 2)² − 4 + (y + 3)² − 9 − 3 = 0", "(x − 2)² + (y + 3)² = 16"], "centre (2 ; −3), rayon 4")],
             [["Centre (2 ; −3) : (x + 2)² + (y − 3)²", "(x − 2)² + (y + 3)² : on soustrait les coordonnées du centre."], ["(x − 1)² + y² = 9 : rayon 9", "Le rayon est √9 = 3."],
              ["L’axe de la parabole est y = −b/(2a)", "C’est une droite verticale : x = −b/(2a)."]])
    faq = [("Toute équation x² + y² + … = 0 est-elle celle d’un cercle ?", "Non : après avoir complété les carrés, si le second membre est négatif, aucun point ne convient ; s’il est nul, c’est un seul point."),
           ("Comment savoir si un point est sur un cercle ?", "On remplace x et y par ses coordonnées dans l’équation : le point est sur le cercle si l’égalité est vraie.")]
    unit("premiere", R, "equations-de-cercles-et-paraboles", "G",
         "Équation d’un cercle défini par son centre et son rayon, ou par un diamètre ; déterminer le centre et le rayon d’un cercle donné par une équation développée ; parabole représentative d’une fonction du second degré : axe de symétrie, sommet ; intersections",
         "Équations de cercles et paraboles", "Cercles et paraboles",
         "Fiches de maths première sur les équations de cercles et les paraboles : centre, rayon, cercle de diamètre [AB], appartenance, axe, sommet, intersections et tangentes. 100 exercices corrigés.",
         "Cercle : (x − a)² + (y − b)² = r²", "Parabole : axe x = −b ÷ (2a)", body, faq, sets, 19)


if __name__ == "__main__":
    main()
