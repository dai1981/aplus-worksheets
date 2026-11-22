# -*- coding: utf-8 -*-
"""
France Maths Seconde : Équations de droites (vecteur directeur, équation cartésienne, équation réduite, pente, parallélisme, intersection)
  python3 tools/gen_fr_maths_seconde_equations_de_droites.py
Erreurs : pente = Δx/Δy, droite verticale y = c, vecteur directeur (a ; b) pour ax + by + c = 0, confondre parallèles et sécantes.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60514)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def V(s):
    return "<span class='vec'>%s</span>" % s


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def red(m, p):
    return "y = %s" % E((m, "x"), (p, ""))


def s1():
    m, p = nz(-5, 5), R.randint(-6, 6)
    x1, x2 = R.sample(range(-5, 6), 2)
    y1, y2 = m * x1 + p, m * x2 + p
    k = R.choice(["pente", "eq", "eq"])
    if k == "pente":
        return M("Quelle est la pente de la droite passant par A%s et B%s ?" % (co(x1, y1), co(x2, y2)), d(m), [fq(Fr(x2 - x1, y2 - y1)) if Fr(x2 - x1, y2 - y1) != m else d(m + 1), d(-m), d(y2 - y1) if y2 - y1 != m else d(m - 1)],
                 "m = (y<sub>B</sub> − y<sub>A</sub>) ÷ (x<sub>B</sub> − x<sub>A</sub>) = %s ÷ %s = <b>%s</b>." % (d(y2 - y1), par(x2 - x1), d(m)))
    return M("Quelle est l’équation réduite de la droite passant par A%s et B%s ?" % (co(x1, y1), co(x2, y2)), red(m, p), [red(m, -p) if p else red(m, 1), red(-m, p), red(m, y1) if y1 != p else red(m, p + 2)],
             "m = %s ; p = y<sub>A</sub> − m × x<sub>A</sub> = %s : <b>%s</b>." % (d(m), d(p), red(m, p)))


def s2():
    k = R.choice(["vd", "vd", "pt_m", "vert"])
    if k == "vd":
        a, b, c = nz(-6, 6), nz(-6, 6), R.randint(-9, 9)
        eq = "%s = 0" % E((a, "x"), (b, "y"), (c, ""))
        return M("Quel est un vecteur directeur de la droite d’équation %s ?" % eq, "%s%s" % (V("u"), co(-b, a)), ["%s%s" % (V("u"), co(a, b)), "%s%s" % (V("u"), co(b, a)) if (b, a) != (-b, a) else "%s%s" % (V("u"), co(a, -b)), "%s%s" % (V("u"), co(-b, -a)) if a else "%s(1 ; 1)" % V("u")],
                 "Pour ax + by + c = 0, %s(−b ; a) est un vecteur directeur : <b>%s%s</b>." % (V("u"), V("u"), co(-b, a)))
    if k == "pt_m":
        m, (x0, y0) = nz(-4, 4), (R.randint(-5, 5), R.randint(-5, 5))
        p = y0 - m * x0
        return M("Quelle est l’équation réduite de la droite de pente %s passant par A%s ?" % (d(m), co(x0, y0)), red(m, p), [red(m, y0), red(x0, y0) if x0 else red(m, p + 1), red(m, y0 + m * x0) if m * x0 else red(m, p - 1)],
                 "y = %sx + p et %s = %s × %s + p, donc p = %s : <b>%s</b>." % (d(m), d(y0), d(m), par(x0), d(p), red(m, p)))
    c = R.randint(-6, 6)
    q = R.choice(["v", "h"])
    if q == "v":
        return M("Quelle est l’équation de la droite verticale passant par A%s ?" % co(c, R.randint(-5, 5)), "x = %s" % d(c), ["y = %s" % d(c), "y = %sx" % d(c) if c not in (0, 1) else "y = x + %d" % (c + 2), "x = 0"] if c else ["y = 0", "y = x", "x = 1"],
                 "Tous ses points ont la même abscisse : <b>x = %s</b> (pas d’équation réduite y = mx + p, pas de pente)." % d(c))
    y0 = R.randint(-5, 5)
    return M("Quelle est la pente de la droite d’équation y = %s ?" % d(y0), "0", [d(y0) if y0 else "1", "elle n’a pas de pente", "1"], "La droite est horizontale : <b>m = 0</b>.")


def s3():
    k = R.choice(["cart2red", "pt", "pt", "vd2eq"])
    if k == "cart2red":
        b = nz(-4, 4)
        m, p = nz(-4, 4), R.randint(-6, 6)
        a, c = -m * b, -p * b
        eq = "%s = 0" % E((a, "x"), (b, "y"), (c, ""))
        return M("Quelle est l’équation réduite de la droite d’équation %s ?" % eq, red(m, p), [red(-m, -p), red(a, c) if (a, c) != (m, p) else red(m, p + 1), red(m, -p) if p else red(-m, p)],
                 "On isole y : %sy = %s, puis on divise par %s : <b>%s</b>." % (d(b) if b not in (1, -1) else ("" if b == 1 else MINUS), E((-a, "x"), (-c, "")), par(b), red(m, p)))
    if k == "pt":
        m, p = nz(-4, 4), R.randint(-6, 6)
        x = R.randint(-5, 5)
        y = m * x + p + R.choice([0, 0, 1, -1])
        ok = y == m * x + p
        return M("Le point A%s appartient-il à la droite d’équation %s ?" % (co(x, y), red(m, p)), "oui" if ok else "non", ["non" if ok else "oui", "seulement si x &gt; 0", "on ne peut pas savoir"],
                 "%s × %s %s = %s %s %s : <b>%s</b>." % (d(m), par(x), ("+ %s" % d(p)) if p >= 0 else ("− %s" % d(-p)), d(m * x + p), "=" if ok else "≠", d(y), "oui" if ok else "non"))
    a, b = nz(-5, 5), nz(-5, 5)
    x0, y0 = R.randint(-4, 4), R.randint(-4, 4)
    # droite de vecteur directeur (a ; b) passant par A : b x − a y + c = 0
    c = -(b * x0 - a * y0)
    eq = "%s = 0" % E((b, "x"), (-a, "y"), (c, ""))
    return M("Quelle est une équation cartésienne de la droite passant par A%s, de vecteur directeur %s%s ?" % (co(x0, y0), V("u"), co(a, b)), eq,
             ["%s = 0" % E((a, "x"), (b, "y"), (-(a * x0 + b * y0), "")), "%s = 0" % E((b, "x"), (-a, "y"), (-c, "")) if c else "%s = 0" % E((b, "x"), (-a, "y"), (1, "")), "%s = 0" % E((-a, "x"), (b, "y"), (a * x0 - b * y0, "")) if (-a, b) != (b, -a) else "%s = 0" % E((b, "x"), (a, "y"), (c, ""))],
             "M(x ; y) est sur la droite ⇔ det(%s, %s) = 0 ⇔ %s(y − %s) − %s(x − %s) = 0, soit <b>%s</b> (ou une équation proportionnelle)." % (V("AM"), V("u"), d(a), par(y0), par(b), par(x0), eq))


def s4():
    m1, p1 = nz(-4, 4), R.randint(-6, 6)
    k = R.choice(["pos", "pos", "inter"])
    if k == "pos":
        same = R.random() < 0.4
        m2 = m1 if same else nz(-4, 4)
        p2 = R.randint(-6, 6)
        if same and p2 == p1:
            ans = "confondues"
        elif m1 == m2:
            ans = "parallèles (strictement)"
        else:
            ans = "sécantes"
        return M("Les droites d’équations %s et %s sont…" % (red(m1, p1), red(m2, p2)), ans, [o for o in ["sécantes", "parallèles (strictement)", "confondues", "perpendiculaires toujours"] if o != ans][:3],
                 "On compare les pentes %s et %s%s : <b>%s</b>." % (d(m1), d(m2), "" if m1 != m2 else " (égales), puis les ordonnées à l’origine", ans))
    m2 = nz(-4, 4)
    if m2 == m1:
        return None
    x = Fr(R.randint(-4, 4))
    p2 = m1 * x + p1 - m2 * x
    if p2.denominator != 1 or abs(p2) > 15:
        return None
    y = m1 * x + p1
    return M("Quelles sont les coordonnées du point d’intersection des droites %s et %s ?" % (red(m1, p1), red(m2, p2)), co(x, y), [co(y, x) if x != y else co(x + 1, y), co(x, m1 * x - p1) if p1 else co(x, y + 2), co(-x, y) if x else co(1, y)],
             "%s = %s ⇔ x = %s ; y = %s : <b>%s</b>." % (E((m1, "x"), (p1, "")), E((m2, "x"), (p2, "")), d(x), d(y), co(x, y)))


def s5():
    m = R.choice([-2, -1, Fr(-1, 2), Fr(1, 2), 1, 2, 3, Fr(-3, 2)])
    p = R.randint(-3, 3)
    svg = relabel(de_k8.kosy(lines=[(m, p, BLUE, "")], lo=-5, hi=5, u=22), "droite dans un repère")
    k = R.choice(["eq", "eq", "pente", "vd"])
    if k == "eq":
        return M("<div class='qfig'>%s</div>Quelle est l’équation réduite de cette droite ?" % svg, red(m, p), [red(-m, p), red(m, -p) if p else red(2 * m, p), red(p, m) if p and Fr(p) != Fr(m) else red(m, p + 1)],
                 "Ordonnée à l’origine %s, pente %s : <b>%s</b>." % (d(p), fq(m), red(m, p)))
    if k == "pente":
        return M("<div class='qfig'>%s</div>Quelle est la pente de cette droite ?" % svg, fq(m), [fq(-m), fq(1 / Fr(m)) if 1 / Fr(m) != m else fq(2 * m), d(p) if Fr(p) not in (Fr(m), -Fr(m)) else fq(m + 1)],
                 "Pour 1 vers la droite, on %s de %s : <b>%s</b>." % ("monte" if m > 0 else "descend", d(abs(m)), fq(m)))
    mm = Fr(m)
    a, b = mm.denominator, mm.numerator
    return M("<div class='qfig'>%s</div>Quel vecteur est un vecteur directeur de cette droite ?" % svg, "%s%s" % (V("u"), co(a, b)), ["%s%s" % (V("u"), co(b, a)), "%s%s" % (V("u"), co(a, -b)), "%s%s" % (V("u"), co(0, 1))],
             "Une droite de pente m a pour vecteur directeur (1 ; m), ou ici <b>%s%s</b>." % (V("u"), co(a, b)))


def main():
    seen = set()
    sets = [("Pente et équation réduite", mix(R, seen, [(s1, 20)])), ("Vecteur directeur et cas particuliers", mix(R, seen, [(s2, 20)])),
            ("Équations cartésiennes", mix(R, seen, [(s3, 20)])), ("Positions relatives et intersection", mix(R, seen, [(s4, 20)])), ("Lecture graphique", mix(R, seen, [(s5, 20)]))]
    body = L(["Toute droite a une <b>équation cartésienne</b> ax + by + c = 0, de vecteur directeur %s(−b ; a)." % V("u"),
              "Une droite non verticale a une <b>équation réduite</b> y = mx + p : m est la <b>pente</b> (m = Δy ÷ Δx), p l’ordonnée à l’origine. Une droite verticale a une équation x = c.",
              "Deux droites non verticales sont parallèles si et seulement si elles ont la même pente ; sinon elles sont sécantes (on résout un système pour l’intersection)."],
             [("A(1 ; 2) et B(3 ; 8)", ["m = (8 − 2) ÷ (3 − 1) = 3", "p = 2 − 3 × 1 = −1"], "y = 3x − 1")],
             [["m = Δx ÷ Δy", "La pente est Δy ÷ Δx."], ["Droite verticale : y = c", "Une droite verticale a une équation x = c."], ["Vecteur directeur (a ; b) pour ax + by + c = 0", "C’est (−b ; a)."]])
    faq = [("Une droite a-t-elle une seule équation cartésienne ?", "Non : on peut multiplier tous les coefficients par un même nombre non nul. L’équation réduite, elle, est unique."),
           ("Comment trouver l’intersection de deux droites ?", "On résout le système formé par leurs deux équations.")]
    unit("seconde", R, "equations-de-droites", "G",
         "Déterminer une équation cartésienne ou réduite d’une droite à partir de deux points, d’un point et d’un vecteur directeur ou d’un point et de la pente ; lire la pente et un vecteur directeur ; étudier la position relative de deux droites et leur intersection",
         "Équations de droites", "Équations de droites",
         "Fiches de maths seconde sur les droites : pente, équation réduite, équation cartésienne, vecteur directeur, droites parallèles et intersection. 100 exercices corrigés.",
         "y = mx + p, avec m = Δy ÷ Δx", "ax + by + c = 0 : vecteur directeur (−b ; a)", body, faq, sets, 14)


if __name__ == "__main__":
    main()
