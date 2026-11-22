# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Produit scalaire (définition avec le cosinus, projection orthogonale, expression en repère orthonormé, orthogonalité, calcul d’angles)
  python3 tools/gen_fr_maths_premiere_produit_scalaire.py
Erreurs : u · v = ‖u‖ × ‖v‖ sans le cosinus, xx′ − yy′, oublier le signe quand le projeté est du « mauvais côté », u · v = 0 ⇔ u = 0.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60616)


def V(s):
    return "<span class='vec'>%s</span>" % s


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def s1():
    a, b = R.randint(2, 9), R.randint(2, 9)
    t, cs, lab = R.choice([(Fr(1, 3), Fr(1, 2), "60°"), (Fr(2, 3), Fr(-1, 2), "120°"), (Fr(1, 2), 0, "90°"), (0, 1, "0°"), (1, -1, "180°"), (Fr(1, 4), None, "45°"), (Fr(3, 4), None, "135°")])
    useR = R.random() < 0.5
    ang = pif(t) if useR else lab
    if cs is None:
        k = a * b
        ans = (MINUS if t == Fr(3, 4) else "") + ("%s√2" % fq(Fr(k, 2)) if Fr(k, 2) != 1 else "√2")
        return M("‖%s‖ = %d, ‖%s‖ = %d et l’angle entre %s et %s mesure %s. Calcule %s · %s." % (V("u"), a, V("v"), b, V("u"), V("v"), ang, V("u"), V("v")), ans,
                 [d(k), d(k * (-1 if t == Fr(1, 4) else 1)) if t == Fr(3, 4) else MINUS + ans, "%s√3" % fq(Fr(k, 2)), fq(Fr(k, 2))],
                 "%s · %s = ‖%s‖ × ‖%s‖ × cos(%s) = %d × %d × %s = <b>%s</b>." % (V("u"), V("v"), V("u"), V("v"), ang, a, b, "(−√2/2)" if t == Fr(3, 4) else "√2/2", ans))
    val_ = a * b * Fr(cs)
    return M("‖%s‖ = %d, ‖%s‖ = %d et l’angle entre %s et %s mesure %s. Calcule %s · %s." % (V("u"), a, V("v"), b, V("u"), V("v"), ang, V("u"), V("v")), fq(val_),
             [d(a * b) if a * b != val_ else d(-a * b), fq(-val_) if val_ else d(a + b), "%s√3" % fq(Fr(a * b, 2)), d(a * a + b * b) if val_ != a * a + b * b else d(a + b)],
             "%s · %s = ‖%s‖ × ‖%s‖ × cos(%s) = %d × %d × %s = <b>%s</b>." % (V("u"), V("v"), V("u"), V("v"), ang, a, b, "(" + fq(cs) + ")" if cs < 0 else fq(cs), fq(val_)))


def s2():
    AB = R.randint(3, 10)
    AH = R.randint(1, 12)
    side = R.choice(["meme", "meme", "oppose", "perp"])
    if side == "perp":
        return M("Dans le triangle ABC, le projeté orthogonal de C sur la droite (AB) est le point A lui-même. Que vaut %s · %s ?" % (V("AB"), V("AC")), "0",
                 [d(AB), d(AB * AB), "on ne peut pas savoir"], "Le projeté de C est A, donc %s ⊥ %s : <b>%s · %s = 0</b>." % (V("AB"), V("AC"), V("AB"), V("AC")))
    s = 1 if side == "meme" else -1
    pos = "sur la demi-droite [AB)" if s > 0 else "sur la droite (AB), du côté opposé à B par rapport à A"
    return M("AB = %d. H, projeté orthogonal de C sur (AB), est %s, avec AH = %d. Calcule %s · %s." % (AB, pos, AH, V("AB"), V("AC")), d(s * AB * AH),
             [d(-s * AB * AH), d(AB * AB), d(AB + AH), d(AB * (AB - AH)) if AB != AH else d(2 * AB)],
             "%s · %s = %s · %s = %sAB × AH = %s%d × %d = <b>%s</b>." % (V("AB"), V("AC"), V("AB"), V("AH"), "" if s > 0 else "−", "" if s > 0 else "−", AB, AH, d(s * AB * AH)))


def s3():
    k = R.choice(["dot", "dot", "norm", "pts"])
    x, y, x2, y2 = [R.randint(-6, 6) for _ in range(4)]
    if k == "dot":
        return M("Dans un repère orthonormé, %s%s et %s%s. Calcule %s · %s." % (V("u"), co(x, y), V("v"), co(x2, y2), V("u"), V("v")), d(x * x2 + y * y2),
                 [d(x * x2 - y * y2), d(x * y2 + y * x2), d((x + x2) * (y + y2)), d(x * x2 + y * y2 + 1)], "x x′ + y y′ = %s × %s + %s × %s = <b>%s</b>." % (d(x), par(x2), par(y), par(y2), d(x * x2 + y * y2)))
    if k == "norm":
        n2 = x * x + y * y
        if n2 == 0:
            return None
        ans = sq(n2)
        return M("Dans un repère orthonormé, %s%s. Calcule ‖%s‖." % (V("u"), co(x, y), V("u")), ans, [d(abs(x) + abs(y)), d(n2), sq(abs(x * x - y * y)) if x * x != y * y else d(abs(x) * 2)],
                 ("‖%s‖ = √(x² + y²) = √%d = <b>%s</b>." % (V("u"), n2, ans)) if ans != "√%d" % n2 else "‖%s‖ = √(x² + y²) = <b>√%d</b>." % (V("u"), n2))
    A, B, C = (x, y), (x2, y2), (R.randint(-6, 6), R.randint(-6, 6))
    u = (B[0] - A[0], B[1] - A[1])
    v = (C[0] - A[0], C[1] - A[1])
    return M("A%s, B%s et C%s. Calcule %s · %s." % (co(*A), co(*B), co(*C), V("AB"), V("AC")), d(u[0] * v[0] + u[1] * v[1]),
             [d(B[0] * C[0] + B[1] * C[1]), d(u[0] * v[0] - u[1] * v[1]), d(u[0] * v[1] + u[1] * v[0])],
             "%s%s et %s%s : %s · %s = <b>%s</b>." % (V("AB"), co(*u), V("AC"), co(*v), V("AB"), V("AC"), d(u[0] * v[0] + u[1] * v[1])))


def s4():
    k = R.choice(["m", "m", "check", "rect"])
    if k == "m":
        a, b, c = nz(R, -6, 6), nz(R, -6, 6), R.randint(-6, 6)
        # u(m ; a), v(b ; c) : mb + ac = 0
        m = Fr(-a * c, b)
        return M("Pour quelle valeur de m les vecteurs %s(m ; %s) et %s%s sont-ils orthogonaux ?" % (V("u"), d(a), V("v"), co(b, c), ), "m = %s" % fq(m),
                 ["m = %s" % fq(-m), "m = %s" % fq(Fr(-b * c, a)), "m = %s" % fq(Fr(-a, b)), "m = %s" % fq(Fr(c, b)), "m = %s" % fq(Fr(-a * b, c)) if c else "m = 1", "m = %s" % d(a)],
                 "%s · %s = %s + %s × %s = 0 ⇔ <b>m = %s</b>." % (V("u"), V("v"), E((b, "m")), par(a), par(c), fq(m)))
    if k == "check":
        x, y = nz(R, -6, 6), nz(R, -6, 6)
        kk = R.choice([1, 2, -1, 3])
        orth = R.random() < 0.5
        u2 = (-y * kk, x * kk) if orth else (-y * kk + R.choice([1, -1]), x * kk)
        p = x * u2[0] + y * u2[1]
        return M("Les vecteurs %s%s et %s%s sont-ils orthogonaux ?" % (V("u"), co(x, y), V("v"), co(*u2)), "oui, car %s · %s = 0" % (V("u"), V("v")) if p == 0 else "non, car %s · %s = %s" % (V("u"), V("v"), d(p)),
                 ["non, car %s · %s = %s" % (V("u"), V("v"), d(x * u2[0] - y * u2[1])) if p == 0 else "oui, car %s · %s = 0" % (V("u"), V("v")), "oui, car ils ont la même norme", "non, car ils ne sont pas colinéaires"],
                 "%s × %s + %s × %s = %s : %s." % (d(x), par(u2[0]), par(y), par(u2[1]), d(p), "<b>orthogonaux</b>" if p == 0 else "<b>pas orthogonaux</b>"))
    while True:
        A = (R.randint(-4, 4), R.randint(-4, 4))
        u = (nz(R, -4, 4), nz(R, -4, 4))
        kk = nz(R, -2, 2)
        B = (A[0] + u[0], A[1] + u[1])
        C = (A[0] - u[1] * kk, A[1] + u[0] * kk)
        if B != C:
            break
    return M("A%s, B%s et C%s. Le triangle ABC est-il rectangle en A ?" % (co(*A), co(*B), co(*C)), "oui, car %s · %s = 0" % (V("AB"), V("AC")),
             ["non, car %s · %s ≠ 0" % (V("AB"), V("AC")), "oui, car AB = AC", "on ne peut pas savoir sans figure"],
             "%s%s, %s%s : %s × %s + %s × %s = 0. <b>Rectangle en A</b>." % (V("AB"), co(*u), V("AC"), co(-u[1] * kk, u[0] * kk), d(u[0]), par(-u[1] * kk), d(u[1]), par(u[0] * kk)))


def s5():
    for _ in range(200):
        u = (R.randint(-4, 4), R.randint(-4, 4))
        v = (R.randint(-4, 4), R.randint(-4, 4))
        nu, nv = u[0] ** 2 + u[1] ** 2, v[0] ** 2 + v[1] ** 2
        if not nu or not nv:
            continue
        p = u[0] * v[0] + u[1] * v[1]
        c2 = Fr(p * p, nu * nv)
        if c2 in (0, Fr(1, 2)) and (u[0] * v[1] - u[1] * v[0]) != 0:
            break
    else:
        return None
    ang = 90 if p == 0 else 45 if p > 0 else 135
    return M("Dans un repère orthonormé, %s%s et %s%s. Quelle est la mesure de l’angle entre %s et %s ?" % (V("u"), co(*u), V("v"), co(*v), V("u"), V("v")), "%d°" % ang,
             ["%d°" % a for a in (30, 45, 60, 90, 120, 135, 150) if a != ang][:3] if ang != 45 else ["135°", "60°", "30°"],
             "cos θ = (%s · %s) ÷ (‖%s‖ × ‖%s‖) = %s ÷ (√%d × √%d) = %s : <b>θ = %d°</b>." % (V("u"), V("v"), V("u"), V("v"), d(p), nu, nv, "0" if p == 0 else ("√2/2" if p > 0 else "−√2/2"), ang))


def main():
    seen = set()
    sets = [("Définition avec le cosinus", mix(R, seen, [(s1, 20)])), ("Projection orthogonale", mix(R, seen, [(s2, 20)])),
            ("Calcul avec des coordonnées", mix(R, seen, [(s3, 20)])), ("Orthogonalité", mix(R, seen, [(s4, 20)])), ("Calculer un angle", mix(R, seen, [(s5, 20)]))]
    u, v = V("u"), V("v")
    body = L(["%s · %s = ‖%s‖ × ‖%s‖ × cos θ, où θ est l’angle entre les deux vecteurs. Si θ est aigu, le produit est positif ; obtus, négatif ; droit, nul." % (u, v, u, v),
              "Avec le projeté orthogonal H de C sur (AB) : %s · %s = AB × AH si H est du côté de B, −AB × AH sinon." % (V("AB"), V("AC")),
              "En repère orthonormé : %s(x ; y) · %s(x′ ; y′) = xx′ + yy′ et ‖%s‖ = √(x² + y²)." % (u, v, u),
              "%s et %s sont <b>orthogonaux</b> si et seulement si %s · %s = 0." % (u, v, u, v)],
             [("%s(2 ; 1), %s(−1 ; 3)" % (u, v), ["%s · %s = 2 × (−1) + 1 × 3 = 1" % (u, v), "‖%s‖ = √5, ‖%s‖ = √10, cos θ = 1/√50" % (u, v)], "θ ≈ 81,9°")],
             [["%s · %s = ‖%s‖ × ‖%s‖" % (u, v, u, v), "Il manque cos θ (c’est vrai seulement si θ = 0)."], ["xx′ − yy′", "On ajoute : xx′ + yy′."], ["H du côté opposé : %s · %s = AB × AH" % (V("AB"), V("AC")), "Le produit est alors négatif : −AB × AH."]])
    faq = [("Le produit scalaire est-il un vecteur ?", "Non, c’est un nombre réel (positif, négatif ou nul)."),
           ("Quelle formule choisir ?", "Avec des longueurs et un angle : le cosinus ; avec une figure et un projeté : la projection ; avec des coordonnées : xx′ + yy′.")]
    unit("premiere", R, "produit-scalaire", "G",
         "Produit scalaire de deux vecteurs : définition à l’aide du cosinus, par projection orthogonale ; expression en base orthonormée ; orthogonalité de deux vecteurs ; calcul d’angles et de longueurs",
         "Produit scalaire : définitions, coordonnées et orthogonalité", "Produit scalaire",
         "Fiches de maths première sur le produit scalaire : définition avec le cosinus, projection orthogonale, coordonnées, orthogonalité et calcul d’angles. 100 exercices corrigés.",
         "u · v = ‖u‖ × ‖v‖ × cos θ = xx′ + yy′", "Orthogonaux ⇔ u · v = 0", body, faq, sets, 16)


if __name__ == "__main__":
    main()
