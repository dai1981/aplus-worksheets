# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Fonctions dérivées (dérivées usuelles, somme, produit par un réel, produit, quotient, inverse, x ↦ g(ax + b))
  python3 tools/gen_fr_maths_premiere_fonctions_derivees.py
Erreurs : (uv)′ = u′v′, (1/x)′ = 1/x², (√x)′ = 1/√x, (u/v)′ = (u′v + uv′)/v², oublier le facteur a dans g(ax + b), dériver la constante en 1.
"""
import random
from fr_ly1 import *

R = random.Random(60610)
X = {4: "x⁴", 3: "x³", 2: "x²", 1: "x", 0: ""}


def poly(cs):
    return expr([(c, X[e]) for c, e in cs])


def der(cs):
    return [(c * e, e - 1) for c, e in cs if e > 0]


def pmul(p, q):
    out = {}
    for c1, e1 in p:
        for c2, e2 in q:
            out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
    return sorted([(c, e) for e, c in out.items() if c], key=lambda t: -t[1])


def padd(p, q):
    out = {}
    for c, e in p + q:
        out[e] = out.get(e, 0) + c
    return sorted([(c, e) for e, c in out.items() if c], key=lambda t: -t[1])


def s1():
    k = R.choice(["pow", "pow", "inv", "sqrt", "const", "aff"])
    if k == "pow":
        n = R.randint(2, 9)
        return M("Quelle est la dérivée de f(x) = x<sup>%d</sup> ?" % n, "f′(x) = %dx<sup>%d</sup>" % (n, n - 1) if n > 2 else "f′(x) = 2x",
                 ["f′(x) = x<sup>%d</sup>" % (n - 1) if n > 2 else "f′(x) = x", "f′(x) = %dx<sup>%d</sup>" % (n, n), "f′(x) = %dx<sup>%d</sup>" % (n - 1, n) if n > 2 else "f′(x) = x²", "f′(x) = %dx" % n if n > 2 else "f′(x) = 2"],
                 "(x<sup>n</sup>)′ = nx<sup>n−1</sup> : <b>%s</b>." % ("%dx<sup>%d</sup>" % (n, n - 1) if n > 2 else "2x"))
    if k == "inv":
        a = nz(R, -9, 9)
        if a == 1:
            return M("Quelle est la dérivée de f(x) = 1/x sur ]0 ; +∞[ ?", "f′(x) = −1/x²", ["f′(x) = 1/x²", "f′(x) = ln x", "f′(x) = −1/x"], "(1/x)′ = <b>−1/x²</b>.")
        return M("Quelle est la dérivée de f(x) = %s/x sur ]0 ; +∞[ ?" % d(a), "f′(x) = %s/x²" % d(-a), ["f′(x) = %s/x²" % d(a), "f′(x) = %s" % d(a), "f′(x) = %s/x" % d(-a)],
                 "f(x) = %s × 1/x et (1/x)′ = −1/x² : <b>f′(x) = %s/x²</b>." % (d(a), d(-a)))
    if k == "sqrt":
        a = R.randint(1, 8)
        if a == 1:
            return M("Quelle est la dérivée de f(x) = √x sur ]0 ; +∞[ ?", "f′(x) = 1/(2√x)", ["f′(x) = 1/√x", "f′(x) = 2√x", "f′(x) = √x/2"], "(√x)′ = <b>1/(2√x)</b> (√x n’est pas dérivable en 0).")
        return M("Quelle est la dérivée de f(x) = %d√x sur ]0 ; +∞[ ?" % a, "f′(x) = %s/√x" % fq(Fr(a, 2)) if a % 2 == 0 else "f′(x) = %d/(2√x)" % a,
                 ["f′(x) = %d/√x" % a if a % 2 else "f′(x) = %d/√x" % a, "f′(x) = %d√x/2" % a, "f′(x) = 1/(%d√x)" % (2 * a), "f′(x) = %d/(2√x)" % (2 * a)],
                 "%d × 1/(2√x) = <b>%s</b>." % (a, "%s/√x" % fq(Fr(a, 2)) if a % 2 == 0 else "%d/(2√x)" % a))
    if k == "const":
        c = R.randint(2, 99)
        return M("Quelle est la dérivée de f(x) = %d ?" % c, "f′(x) = 0", ["f′(x) = 1", "f′(x) = %d" % c, "f′(x) = %dx" % c], "La dérivée d’une constante est <b>0</b>.")
    m, p = nz(R, -9, 9), nz(R, -9, 9)
    return M("Quelle est la dérivée de f(x) = %s ?" % E((m, "x"), (p, "")), "f′(x) = %s" % d(m), ["f′(x) = %s" % d(p), "f′(x) = %s" % E((m, "x")), "f′(x) = %s" % d(m + p), "f′(x) = %s" % d(-m)],
             "(mx + p)′ = m : <b>%s</b>." % d(m))


def s2():
    deg = R.choice([2, 3, 3, 4])
    cs = [(nz(R, -5, 5), deg)] + [(R.randint(-9, 9), e) for e in range(deg - 1, -1, -1)]
    cs = [(c, e) for c, e in cs if c]
    if len(cs) < 3:
        return None
    ans = "f′(x) = " + poly(der(cs))
    bad1 = "f′(x) = " + poly([(c, e - 1) for c, e in cs if e > 0])
    bad2 = "f′(x) = " + poly(padd(der(cs), [(c, 0) for c, e in cs if e == 0]))
    bad3 = "f′(x) = " + poly([(c * e, e) for c, e in cs if e > 0])
    bad4 = "f′(x) = " + poly([(c * (e - 1), e - 1) if e > 1 else (c, 0) for c, e in cs if e > 0])
    return M("Calcule la dérivée de f(x) = %s." % poly(cs), ans, [bad1, bad2, bad3, bad4],
             "On dérive terme à terme : (ax<sup>n</sup>)′ = anx<sup>n−1</sup>, la constante disparaît : <b>%s</b>." % ans)


def s3():
    k = R.choice(["pp", "pp", "xsqrt", "value"])
    if k == "xsqrt":
        a = R.randint(1, 5)
        return M("Calcule la dérivée de f(x) = %sx√x sur ]0 ; +∞[ (produit de %sx et de √x)." % (d(a) if a > 1 else "", d(a) if a > 1 else ""), "f′(x) = %s√x" % (fq(Fr(3 * a, 2))),
                 ["f′(x) = %s/(2√x)" % d(a), "f′(x) = %s√x" % (d(a) if a > 1 else ""), "f′(x) = %s√x" % fq(Fr(a, 2)), "f′(x) = %s√x" % d(3 * a)],
                 "(uv)′ = u′v + uv′ = %s√x + %sx × 1/(2√x) = %s√x + %s√x = <b>%s√x</b>." % (d(a) if a > 1 else "", d(a) if a > 1 else "", d(a) if a > 1 else "", fq(Fr(a, 2)), fq(Fr(3 * a, 2))))
    u = [(nz(R, -3, 3), R.choice([1, 2])), (R.randint(-5, 5), 0)]
    v = [(nz(R, -4, 4), 1), (nz(R, -6, 6), 0)]
    u = [t for t in u if t[0]]
    prod = pmul(u, v)
    dp = der(prod)
    if k == "value":
        x0 = R.randint(-3, 3)
        val_ = sum(c * x0 ** e for c, e in dp)
        wrong = sum(c * x0 ** e for c, e in der(u)) * sum(c * x0 ** e for c, e in der(v))
        return M("f(x) = (%s)(%s). Calcule f′(%s)." % (poly(u), poly(v), d(x0)), d(val_), [d(wrong), d(sum(c * x0 ** e for c, e in prod)), d(val_ + 2), d(-val_) if val_ else "1"],
                 "f′(x) = u′v + uv′ = %s ; f′(%s) = <b>%s</b>." % (poly(dp), d(x0), d(val_)))
    ans = "f′(x) = " + poly(dp)
    w1 = "f′(x) = " + poly(pmul(der(u), der(v)))
    w2 = "f′(x) = " + poly(padd(pmul(der(u), v), [(-c, e) for c, e in pmul(u, der(v))]))
    w3 = "f′(x) = " + poly(pmul(der(u), v))
    return M("Calcule la dérivée de f(x) = (%s)(%s)." % (poly(u), poly(v)), ans, [w1, w2, w3, "f′(x) = " + poly(padd(dp, [(1, 0)]))],
             "(uv)′ = u′v + uv′ = (%s)(%s) + (%s)(%s) = <b>%s</b>." % (poly(der(u)), poly(v), poly(u), poly(der(v)), poly(dp)))


def s4():
    k = R.choice(["hom", "hom", "inv", "inv2"])
    if k == "hom":
        a, b, c, e = nz(R, -5, 5), R.randint(-6, 6), nz(R, -4, 4), nz(R, -6, 6)
        n = a * e - b * c
        if n == 0:
            return None
        den = E((c, "x"), (e, ""))
        return M("Calcule la dérivée de f(x) = (%s) ÷ (%s)." % (E((a, "x"), (b, "")), den), "f′(x) = %s ÷ (%s)²" % (d(n), den),
                 ["f′(x) = %s ÷ (%s)²" % (d(a * e + b * c), den), "f′(x) = %s ÷ (%s)²" % (d(-n), den), "f′(x) = %s" % fq(Fr(a, c)), "f′(x) = %s ÷ (%s)" % (d(n), den)],
                 "(u/v)′ = (u′v − uv′) ÷ v² = (%s(%s) − %s(%s)) ÷ (%s)² = <b>%s ÷ (%s)²</b>." % (d(a), den, par(c), E((a, "x"), (b, "")), den, d(n), den))
    if k == "inv":
        a, b = nz(R, -5, 5), nz(R, -6, 6)
        v = E((a, "x"), (b, ""))
        return M("Calcule la dérivée de f(x) = 1 ÷ (%s)." % v, "f′(x) = %s ÷ (%s)²" % (d(-a), v), ["f′(x) = %s ÷ (%s)²" % (d(a), v), "f′(x) = 1 ÷ %s" % d(a), "f′(x) = −1 ÷ (%s)²" % v if a != 1 else "f′(x) = 1 ÷ (%s)²" % v],
                 "(1/v)′ = −v′ ÷ v² avec v′ = %s : <b>%s ÷ (%s)²</b>." % (d(a), d(-a), v))
    c = R.randint(1, 9)
    v = P2(1, 0, c)
    return M("Calcule la dérivée de f(x) = 1 ÷ (%s)." % v, "f′(x) = −2x ÷ (%s)²" % v, ["f′(x) = 2x ÷ (%s)²" % v, "f′(x) = 1 ÷ (2x)", "f′(x) = −1 ÷ (%s)²" % v], "(1/v)′ = −v′ ÷ v² avec v′ = 2x : <b>−2x ÷ (%s)²</b>." % v)


def s5():
    k = R.choice(["pow", "pow", "sqrt", "inv", "value"])
    a, b = nz(R, -5, 5), nz(R, -7, 7)
    inner = E((a, "x"), (b, ""))
    if a == 1:
        return None
    if k == "pow":
        n = R.randint(2, 5)
        sq = "²" if n - 1 == 2 else "" if n - 1 == 1 else "<sup>%d</sup>" % (n - 1)
        ans = "f′(x) = %s(%s)%s" % (d(n * a), inner, sq)
        return M("Calcule la dérivée de f(x) = (%s)<sup>%d</sup>." % (inner, n), ans,
                 ["f′(x) = %d(%s)%s" % (n, inner, sq), "f′(x) = %s(%s)%s" % (d(a), inner, sq), "f′(x) = %s(%s)<sup>%d</sup>" % (d(n * a), inner, n), "f′(x) = %s(%s)%s" % (d(n + a), inner, sq)],
                 "(g(ax + b))′ = a × g′(ax + b) : %s × %d(%s)%s = <b>%s</b>." % (d(a), n, inner, sq, ans[8:]))
    if k == "sqrt":
        a = abs(a)
        inner = E((a, "x"), (b, ""))
        ans = "f′(x) = %s ÷ (2√(%s))" % (d(a), inner) if a % 2 else "f′(x) = %s ÷ √(%s)" % (d(a // 2), inner) if a > 2 else "f′(x) = 1 ÷ √(%s)" % inner
        return M("Calcule la dérivée de f(x) = √(%s) (là où %s &gt; 0)." % (inner, inner), ans,
                 ["f′(x) = 1 ÷ (2√(%s))" % inner, "f′(x) = %s√(%s)" % (d(a), inner), "f′(x) = %s ÷ √(%s)" % (d(a), inner) if a != 2 else "f′(x) = 4 ÷ √(%s)" % inner, "f′(x) = %s ÷ (2√(%s))" % (d(2 * a), inner)],
                 "(√(ax + b))′ = a ÷ (2√(ax + b)) : <b>%s</b>." % ans[8:])
    if k == "inv":
        ans = "f′(x) = %s ÷ (%s)²" % (d(-a), inner)
        return M("Calcule la dérivée de f(x) = 1 ÷ (%s) avec la formule de g(ax + b)." % inner, ans, ["f′(x) = −1 ÷ (%s)²" % inner, "f′(x) = %s ÷ (%s)²" % (d(a), inner), "f′(x) = %s ÷ (%s)" % (d(-a), inner)],
                 "g(x) = 1/x, g′(x) = −1/x², donc f′(x) = %s × (−1 ÷ (%s)²) = <b>%s</b>." % (d(a), inner, ans[8:]))
    n = R.randint(2, 4)
    x0 = R.randint(-2, 2)
    v = n * a * (a * x0 + b) ** (n - 1)
    return M("f(x) = (%s)<sup>%d</sup>. Calcule f′(%s)." % (inner, n, d(x0)), d(v), [d(n * (a * x0 + b) ** (n - 1)), d((a * x0 + b) ** n), d(n * a * (a * x0 + b) ** n), d(v + a) if a else "1"],
             "f′(x) = %s(%s)%s ; f′(%s) = %s × %s%s = <b>%s</b>." % (d(n * a), inner, "²" if n == 3 else "" if n == 2 else "³", d(x0), d(n * a), par(a * x0 + b), "²" if n == 3 else "" if n == 2 else "³", d(v)))


def main():
    seen = set()
    sets = [("Dérivées usuelles", mix(R, seen, [(s1, 20)])), ("Dériver un polynôme", mix(R, seen, [(s2, 20)])),
            ("Dérivée d’un produit", mix(R, seen, [(s3, 20)])), ("Quotient et inverse", mix(R, seen, [(s4, 20)])), ("Dérivée de x ↦ g(ax + b)", mix(R, seen, [(s5, 20)]))]
    body = L(["Dérivées usuelles : (k)′ = 0 ; (mx + p)′ = m ; (x<sup>n</sup>)′ = nx<sup>n−1</sup> ; (1/x)′ = −1/x² ; (√x)′ = 1/(2√x) sur ]0 ; +∞[.",
              "Opérations : (u + v)′ = u′ + v′ ; (ku)′ = ku′ ; <b>(uv)′ = u′v + uv′</b> ; (1/v)′ = −v′/v² ; <b>(u/v)′ = (u′v − uv′)/v²</b>.",
              "Si f(x) = g(ax + b), alors <b>f′(x) = a × g′(ax + b)</b>."],
             [("f(x) = (x² + 1)(3x − 2)", ["u = x² + 1, u′ = 2x ; v = 3x − 2, v′ = 3", "f′(x) = 2x(3x − 2) + 3(x² + 1)"], "f′(x) = 9x² − 4x + 3"),
              ("f(x) = (2x − 1)⁵", ["g(X) = X⁵, a = 2"], "f′(x) = 2 × 5(2x − 1)⁴ = 10(2x − 1)⁴")],
             [["(uv)′ = u′v′", "(uv)′ = u′v + uv′."], ["(1/x)′ = 1/x²", "(1/x)′ = −1/x²."], ["((3x + 1)²)′ = 2(3x + 1)", "On multiplie par a = 3 : 6(3x + 1)."], ["La dérivée de 7 est 1", "La dérivée d’une constante est 0."]])
    faq = [("Faut-il développer avant de dériver ?", "Pour un produit de polynômes, on peut développer puis dériver terme à terme, ou utiliser (uv)′ = u′v + uv′. Les deux donnent le même résultat."),
           ("Pourquoi √x n’est-elle pas dérivable en 0 ?", "Le taux de variation (√h − 0) ÷ h = 1/√h devient de plus en plus grand quand h tend vers 0 : il n’a pas de limite finie (tangente verticale).")]
    unit("premiere", R, "fonctions-derivees", "F",
         "Fonction dérivée ; dérivées des fonctions usuelles (puissances, inverse, racine carrée) ; dérivée d’une somme, d’un produit par un réel, d’un produit, de l’inverse, d’un quotient ; dérivée de x ↦ g(ax + b)",
         "Fonctions dérivées : formules et opérations", "Fonctions dérivées",
         "Fiches de maths première sur les fonctions dérivées : dérivées usuelles, polynômes, produit, quotient, inverse et dérivée de g(ax + b). 100 exercices corrigés.",
         "(uv)′ = u′v + uv′", "(u/v)′ = (u′v − uv′)/v² ; g(ax + b)′ = a × g′(ax + b)", body, faq, sets, 10)


if __name__ == "__main__":
    main()
