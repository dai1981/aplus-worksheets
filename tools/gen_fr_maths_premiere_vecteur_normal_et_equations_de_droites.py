# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Vecteur normal et équations cartésiennes de droites (vecteur normal, droite passant par un point, droites perpendiculaires, médiatrice, hauteur, projeté orthogonal)
  python3 tools/gen_fr_maths_premiere_vecteur_normal_et_equations_de_droites.py
Erreurs : confondre vecteur normal (a ; b) et vecteur directeur (−b ; a), oublier de calculer c avec le point, médiatrice passant par A au lieu du milieu.
"""
import random
from fr_ly1 import *

R = random.Random(60618)


def V(s):
    return "<span class='vec'>%s</span>" % s


def co(x, y):
    return "(%s ; %s)" % (fq(x), fq(y))


def eqn(a, b, c):
    return "%s = 0" % expr([(a, "x"), (b, "y"), (c, "")])


def s1():
    a, b, c = nz(R, -7, 7), nz(R, -7, 7), R.randint(-9, 9)
    k = R.choice(["n", "n", "u", "pt"])
    if k == "n":
        return M("Donne un vecteur normal à la droite d : %s." % eqn(a, b, c), "%s%s" % (V("n"), co(a, b)), ["%s%s" % (V("n"), co(-b, a)), "%s%s" % (V("n"), co(b, a)), "%s%s" % (V("n"), co(a, c)) if c not in (b, 0) else "%s%s" % (V("n"), co(a, -b))],
                 "Pour ax + by + c = 0, %s(a ; b) est normal : <b>%s%s</b>." % (V("n"), V("n"), co(a, b)))
    if k == "u":
        return M("Donne un vecteur directeur de la droite d : %s." % eqn(a, b, c), "%s%s" % (V("u"), co(-b, a)), ["%s%s" % (V("u"), co(a, b)), "%s%s" % (V("u"), co(b, a)) if (b, a) != (-b, a) else "%s%s" % (V("u"), co(a, -b)), "%s%s" % (V("u"), co(-a, b))],
                 "Pour ax + by + c = 0, %s(−b ; a) est directeur : <b>%s%s</b> (il est orthogonal au vecteur normal (a ; b))." % (V("u"), V("u"), co(-b, a)))
    x = R.randint(-5, 5)
    num_ = -c - a * x
    if num_ % b:
        return None
    y = num_ // b
    return M("Le point A(%s ; m) appartient à la droite %s. Que vaut m ?" % (d(x), eqn(a, b, c)), d(y), [d(-y) if y else "1", fq(Fr(c - a * x, b)) if Fr(c - a * x, b) != y else d(y + 1), fq(Fr(-c - a * x, -b)) if y else "2"],
             "On remplace x par %s : %s = 0 ⇔ m = <b>%s</b>." % (d(x), expr([(a * x, ""), (b, "m"), (c, "")]).replace("m", "m", 1), d(y)))


def s2():
    a, b = nz(R, -6, 6), nz(R, -6, 6)
    x0, y0 = R.randint(-6, 6), R.randint(-6, 6)
    c = -a * x0 - b * y0
    k = R.choice(["normal", "normal", "direct"])
    if k == "normal":
        return M("Quelle est une équation de la droite passant par A%s et de vecteur normal %s%s ?" % (co(x0, y0), V("n"), co(a, b)), eqn(a, b, c),
                 [eqn(a, b, a * x0 + b * y0), eqn(-b, a, b * x0 - a * y0), eqn(a, b, 0) if c else eqn(a, b, 1), eqn(b, a, -b * x0 - a * y0) if (b, a) != (a, b) else eqn(a, -b, -a * x0 + b * y0), eqn(a, b, c + 1)],
                 "%sx %s %sy + c = 0 avec A : %s × %s + %s × %s + c = 0, donc c = %s : <b>%s</b>." % (d(a) if abs(a) != 1 else MINUS if a < 0 else "", "+" if b > 0 else MINUS, d(abs(b)) if abs(b) != 1 else "", d(a), par(x0), par(b), par(y0), d(c), eqn(a, b, c)))
    # droite de vecteur directeur u(p ; q) → normal (q ; −p) → q x − p y + c = 0
    p_, q_ = nz(R, -5, 5), nz(R, -5, 5)
    A_, B_ = q_, -p_
    c = -A_ * x0 - B_ * y0
    return M("Quelle est une équation de la droite passant par A%s et de vecteur directeur %s%s ?" % (co(x0, y0), V("u"), co(p_, q_)), eqn(A_, B_, c),
             [eqn(p_, q_, -p_ * x0 - q_ * y0), eqn(A_, B_, -c) if c else eqn(A_, B_, 1), eqn(-B_, A_, B_ * x0 - A_ * y0) if (-B_, A_) != (A_, B_) else eqn(1, 1, 1)],
             "Un vecteur normal est %s%s ; on calcule c avec A : <b>%s</b>." % (V("n"), co(q_, -p_), eqn(A_, B_, c)))


def s3():
    k = R.choice(["perp", "perp", "med", "haut", "check"])
    if k == "perp":
        a, b, c = nz(R, -6, 6), nz(R, -6, 6), R.randint(-9, 9)
        x0, y0 = R.randint(-5, 5), R.randint(-5, 5)
        # perpendiculaire : normal (−b ; a) → −b x + a y + c' = 0
        cp = b * x0 - a * y0
        return M("Quelle est une équation de la droite passant par A%s et perpendiculaire à d : %s ?" % (co(x0, y0), eqn(a, b, c)), eqn(-b, a, cp),
                 [eqn(a, b, -a * x0 - b * y0), eqn(b, a, -b * x0 - a * y0) if (b, a) != (-b, a) else eqn(1, 1, 1), eqn(-b, a, c) if c != cp else eqn(-b, a, cp + 1)],
                 "Un vecteur directeur de d, (%s ; %s), est normal à la perpendiculaire : <b>%s</b>." % (d(-b), d(a), eqn(-b, a, cp)))
    if k == "check":
        a, b = nz(R, -6, 6), nz(R, -6, 6)
        kk = nz(R, -3, 3)
        perp = R.random() < 0.5
        a2, b2 = (-b * kk, a * kk) if perp else (a * kk, b * kk + R.choice([1, -1]))
        p = a * a2 + b * b2
        return M("Les droites %s et %s sont-elles perpendiculaires ?" % (eqn(a, b, R.randint(-5, 5)), eqn(a2, b2, R.randint(-5, 5))), "oui" if p == 0 else "non",
                 ["non" if p == 0 else "oui", "seulement si elles passent par l’origine", "on ne peut pas savoir"],
                 "Produit scalaire des vecteurs normaux : %s × %s + %s × %s = %s : <b>%s</b>." % (d(a), par(a2), par(b), par(b2), d(p), "perpendiculaires" if p == 0 else "pas perpendiculaires"))
    A = (R.randint(-6, 6), R.randint(-6, 6))
    B = (A[0] + 2 * nz(R, -3, 3), A[1] + 2 * R.randint(-3, 3))
    if k == "med":
        n = (B[0] - A[0], B[1] - A[1])
        I = ((A[0] + B[0]) // 2, (A[1] + B[1]) // 2)
        c = -n[0] * I[0] - n[1] * I[1]
        return M("Quelle est une équation de la médiatrice de [AB], avec A%s et B%s ?" % (co(*A), co(*B)), eqn(n[0], n[1], c),
                 [eqn(n[0], n[1], -n[0] * A[0] - n[1] * A[1]), eqn(-n[1], n[0], n[1] * I[0] - n[0] * I[1]) if n[1] else eqn(1, 1, 0), eqn(n[0], n[1], -c) if c else eqn(n[0], n[1], 1)],
                 "%s%s est normal, et la médiatrice passe par le milieu I%s de [AB] : <b>%s</b>." % (V("AB"), co(*n), co(*I), eqn(n[0], n[1], c)))
    C = (R.randint(-6, 6), R.randint(-6, 6))
    n = (B[0] - A[0], B[1] - A[1])
    c = -n[0] * C[0] - n[1] * C[1]
    return M("Dans le triangle ABC avec A%s, B%s et C%s, quelle est une équation de la hauteur issue de C ?" % (co(*A), co(*B), co(*C)), eqn(n[0], n[1], c),
             [eqn(n[0], n[1], -n[0] * A[0] - n[1] * A[1]) if (n[0] * A[0] + n[1] * A[1]) != (n[0] * C[0] + n[1] * C[1]) else eqn(n[0], n[1], c + 1), eqn(-n[1], n[0], n[1] * C[0] - n[0] * C[1]) if n[1] else eqn(1, 1, 0), eqn(n[0], n[1], -c) if c else eqn(n[0], n[1], 2)],
             "La hauteur passe par C et a pour vecteur normal %s%s : <b>%s</b>." % (V("AB"), co(*n), eqn(n[0], n[1], c)))


def s4():
    # droite d : a x + b y + c = 0 ; H sur d ; A = H + t n
    a, b = R.choice([(1, 1), (1, -1), (1, 2), (2, 1), (1, 0), (0, 1), (1, -2), (3, 1), (2, -1)])
    hx, hy = R.randint(-4, 4), R.randint(-4, 4)
    c = -a * hx - b * hy
    t = nz(R, -2, 2)
    A = (hx + t * a, hy + t * b)
    k = R.choice(["H", "H", "dist"])
    if k == "H":
        return M("Quel est le projeté orthogonal H du point A%s sur la droite d : %s ?" % (co(*A), eqn(a, b, c)), "H%s" % co(hx, hy),
                 ["H%s" % co(A[0] - t * b, A[1] + t * a) if b or a else "H(0 ; 0)", "H%s" % co(hx + a, hy + b), "H%s" % co(A[0], -(a * A[0] + c) / Fr(b) if b else 0)],
                 "H = A + k%s(%s ; %s) avec H ∈ d : on trouve k = %s et <b>H%s</b>." % (V("n"), d(a), d(b), d(-t), co(hx, hy)))
    n2 = a * a + b * b
    return M("Quelle est la distance du point A%s à la droite d : %s (longueur AH, H projeté orthogonal de A sur d) ?" % (co(*A), eqn(a, b, c)), sq(t * t * n2),
             [d(abs(a * A[0] + b * A[1] + c)), sq(n2), sq(A[0] ** 2 + A[1] ** 2) if A != (0, 0) else "1"],
             "H%s, donc AH = √(%s² + %s²) = <b>%s</b>." % (co(hx, hy), par(A[0] - hx), par(A[1] - hy), sq(t * t * n2)))


def s5():
    k = R.choice(["tangente", "tangente", "inter", "reduite"])
    if k == "tangente":
        O = (R.randint(-4, 4), R.randint(-4, 4))
        r = R.choice([(3, 4), (4, 3), (0, 5), (5, 0), (1, 2), (2, -1), (-3, 4)])
        T = (O[0] + r[0], O[1] + r[1])
        c = -r[0] * T[0] - r[1] * T[1]
        return M("Le cercle de centre Ω%s passe par T%s. Quelle est une équation de la tangente au cercle en T ?" % (co(*O), co(*T)), eqn(r[0], r[1], c),
                 [eqn(-r[1], r[0], r[1] * T[0] - r[0] * T[1]), eqn(r[0], r[1], -r[0] * O[0] - r[1] * O[1]), eqn(r[0], r[1], -c) if c else eqn(r[0], r[1], 1)],
                 "La tangente en T est perpendiculaire au rayon : %s%s est normal, et elle passe par T : <b>%s</b>." % (V("ΩT"), co(*r), eqn(r[0], r[1], c)))
    if k == "inter":
        x, y = R.randint(-5, 5), R.randint(-5, 5)
        a, b = nz(R, -4, 4), nz(R, -4, 4)
        a2, b2 = -b, a
        c1, c2 = -a * x - b * y, -a2 * x - b2 * y
        return M("Les droites d : %s et d′ : %s sont perpendiculaires. Quel est leur point d’intersection ?" % (eqn(a, b, c1), eqn(a2, b2, c2)), co(x, y), [co(y, x) if x != y else co(x, -y) if y else co(1, 1), co(-x, -y) if (x, y) != (0, 0) else co(1, 0), co(x, -y) if y else co(x + 1, y)],
                 "On résout le système : <b>%s</b>." % co(x, y))
    a, b, c = nz(R, -6, 6), nz(R, -6, 6), R.randint(-9, 9)
    m, p = Fr(-a, b), Fr(-c, b)
    ans = "y = " + expr([(m, "x"), (p, "")])
    return M("Quelle est l’équation réduite de la droite %s ?" % eqn(a, b, c), ans, ["y = " + expr([(Fr(a, b), "x"), (Fr(c, b), "")]), "y = " + expr([(-a, "x"), (-c, "")]), "y = " + expr([(Fr(-b, a), "x"), (p, "")]) if Fr(-b, a) != m else "y = " + expr([(m, "x"), (-p, "")])],
             ("On isole y : %sy = %s, puis on divise par %s : <b>%s</b>." % (d(b) if b != -1 else MINUS, expr([(-a, "x"), (-c, "")]), d(b), ans)) if b != 1 else "On isole y : <b>%s</b>." % ans)


def main():
    seen = set()
    sets = [("Vecteur normal et vecteur directeur", mix(R, seen, [(s1, 20)])), ("Équation d’une droite", mix(R, seen, [(s2, 20)])),
            ("Droites perpendiculaires, médiatrices et hauteurs", mix(R, seen, [(s3, 20)])), ("Projeté orthogonal", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    n = V("n")
    body = L(["Un vecteur %s non nul est <b>normal</b> à une droite s’il est orthogonal à ses vecteurs directeurs." % n,
              "La droite d’équation ax + by + c = 0 a pour vecteur normal %s(a ; b) et pour vecteur directeur (−b ; a)." % n,
              "Droite passant par A(x<sub>A</sub> ; y<sub>A</sub>) de vecteur normal %s(a ; b) : a(x − x<sub>A</sub>) + b(y − y<sub>A</sub>) = 0." % n,
              "Deux droites sont perpendiculaires si leurs vecteurs normaux sont orthogonaux. Le projeté orthogonal H de A sur d est le point de d tel que %s est normal à d." % V("AH")],
             [("A(1 ; 2), %s(3 ; −1)" % n, ["3x − y + c = 0", "3 × 1 − 2 + c = 0 donc c = −1"], "3x − y − 1 = 0")],
             [["2x + 3y − 1 = 0 a pour vecteur normal (−3 ; 2)", "(−3 ; 2) est directeur ; le normal est (2 ; 3)."], ["La médiatrice de [AB] passe par A", "Elle passe par le milieu de [AB]."], ["Oublier c", "On calcule c avec les coordonnées du point."]])
    faq = [("Pourquoi utiliser un vecteur normal ?", "Il donne directement les coefficients a et b de l’équation cartésienne, ce qui est pratique pour les perpendiculaires, les médiatrices, les hauteurs et les tangentes."),
           ("Une droite a-t-elle une seule équation cartésienne ?", "Non : on peut multiplier tous les coefficients par un même nombre non nul. 2x + 4y − 6 = 0 et x + 2y − 3 = 0 décrivent la même droite.")]
    unit("premiere", R, "vecteur-normal-et-equations-de-droites", "G",
         "Vecteur normal à une droite ; équation cartésienne ax + by + c = 0 ; déterminer une équation de droite passant par un point et de vecteur normal donné ; droites perpendiculaires, médiatrices, hauteurs ; projeté orthogonal d’un point sur une droite",
         "Vecteur normal et équations de droites", "Vecteur normal",
         "Fiches de maths première sur le vecteur normal et les équations cartésiennes de droites : perpendiculaires, médiatrices, hauteurs, tangentes et projeté orthogonal. 100 exercices corrigés.",
         "ax + by + c = 0 : n(a ; b) est normal", "Vecteur directeur (−b ; a)", body, faq, sets, 18)


if __name__ == "__main__":
    main()
