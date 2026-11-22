# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Fonctions polynômes du second degré — formes développée, canonique et factorisée, sommet, variations, somme et produit des racines
  python3 tools/gen_fr_maths_premiere_forme_canonique_et_sommet.py
Erreurs : sommet (−α ; β) au lieu de (α ; β) pour a(x − α)² + β, α = b/(2a) sans le signe moins, oublier de multiplier par a en développant, minimum quand a < 0.
"""
import random
from fr_ly1 import *

R = random.Random(60606)


def canon(a, al, be):
    """a(x − α)² + β"""
    inner = E((1, "x"), (-al, ""))
    A = "" if a == 1 else MINUS if a == -1 else fq(a) if Fr(a).denominator != 1 else d(a)
    s = "%s(%s)²" % (A, inner) if al else "%sx²" % A
    if be:
        s += " %s %s" % ("+" if be > 0 else MINUS, fq(abs(be)))
    return s


def dev(a, al, be):
    return P2(a, -2 * a * al, a * al * al + be)


def s1():
    k = R.choice(["dev", "dev", "fact", "image"])
    a, al, be = nz(R, -3, 3), R.randint(-5, 5), R.randint(-9, 9)
    if k == "dev":
        return M("Développe f(x) = %s." % canon(a, al, be), "f(x) = " + dev(a, al, be),
                 ["f(x) = " + P2(a, -2 * a * al, al * al + be), "f(x) = " + P2(a, 2 * a * al, a * al * al + be), "f(x) = " + P2(a, 0, a * al * al + be), "f(x) = " + P2(a, -a * al, a * al * al + be)],
                 "%s(x² %s %dx + %d) %s = <b>%s</b>." % ("" if a == 1 else d(a), MINUS if al > 0 else "+", abs(2 * al), al * al, ("+ %d" % be) if be >= 0 else "− %d" % -be, dev(a, al, be)))
    if k == "fact":
        x1, x2 = sorted(R.sample(range(-6, 7), 2))
        return M("Développe f(x) = %s(%s)(%s)." % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (-x1, "")), E((1, "x"), (-x2, ""))), "f(x) = " + P2(a, -a * (x1 + x2), a * x1 * x2),
                 ["f(x) = " + P2(a, a * (x1 + x2), a * x1 * x2), "f(x) = " + P2(a, -(x1 + x2), x1 * x2) if a != 1 else "f(x) = " + P2(1, -(x1 + x2), -x1 * x2), "f(x) = " + P2(a, -a * (x1 + x2), -a * x1 * x2), "f(x) = " + P2(a, -a * x1 * x2, a * (x1 + x2))],
                 "On développe le produit puis on multiplie par a : <b>%s</b>." % P2(a, -a * (x1 + x2), a * x1 * x2))
    x = R.randint(-4, 4)
    if x == al:
        return None
    v = a * (x - al) ** 2 + be
    return M("f(x) = %s. Calcule f(%s)." % (canon(a, al, be), d(x)), d(v), [d(a * (x + al) ** 2 + be), d((a * (x - al)) ** 2 + be), d(a * (x - al) + be), d(v + 2 * be) if be else d(v + 1), d(-v), d(a * (x - al) ** 2 - be)],
             "f(%s) = %s × %s²%s = <b>%s</b>." % (d(x), d(a), par(x - al), (" + %d" % be) if be > 0 else (" − %d" % -be) if be else "", d(v)))


def s2():
    k = R.choice(["a1", "a1", "a"])
    al, be = R.randint(-6, 6), R.randint(-9, 9)
    if al == 0:
        return None
    a = 1 if k == "a1" else R.choice([2, 3, -1, -2])
    f = dev(a, al, be)
    ans = canon(a, al, be)
    return M("Quelle est la forme canonique de f(x) = %s ?" % f, ans,
             [canon(a, -al, be), canon(a, al, a * al * al + be) if a * al * al + be != be else canon(a, al, be + 1), canon(a, al, be + al * al) if a != 1 else canon(1, al, -be) if be else canon(1, al, 1), canon(1, al, be) if a != 1 else canon(1, 2 * al, be)],
             "α = −b ÷ (2a) = %s ; β = f(α) = %s : <b>f(x) = %s</b>." % (d(al), d(be), ans))


def s3():
    k = R.choice(["S_can", "S_dev", "ext", "var", "axe"])
    a, al, be = nz(R, -3, 3), R.randint(-6, 6), R.randint(-9, 9)
    if k == "S_can":
        return M("Quelles sont les coordonnées du sommet de la parabole d’équation y = %s ?" % canon(a, al, be), "S(%s ; %s)" % (d(al), d(be)),
                 ["S(%s ; %s)" % (d(-al), d(be)), "S(%s ; %s)" % (d(be), d(al)), "S(%s ; %s)" % (d(-al), d(-be)), "S(%s ; %s)" % (d(al), d(-be))],
                 "Pour a(x − α)² + β, le sommet est <b>S(%s ; %s)</b> (attention au signe dans la parenthèse)." % (d(al), d(be)))
    if k == "S_dev":
        f = dev(a, al, be)
        return M("Quelles sont les coordonnées du sommet de la parabole d’équation y = %s ?" % f, "S(%s ; %s)" % (d(al), d(be)),
                 ["S(%s ; %s)" % (d(-al), d(3 * a * al * al + be)), "S(%s ; %s)" % (d(al), d(a * al * al + be)), "S(%s ; %s)" % (d(-al), d(be)), "S(%s ; %s)" % (d(-2 * a * al), d(be)), "S(%s ; %s)" % (d(be), d(al)), "S(%s ; %s)" % (d(al), d(-be))],
                 "α = −b ÷ (2a) = %s ÷ %s = %s ; β = f(%s) = %s : <b>S(%s ; %s)</b>." % (d(2 * a * al), par(2 * a), d(al), d(al), d(be), d(al), d(be)))
    if k == "ext":
        f = dev(a, al, be)
        ans = "%s %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(be), d(al))
        return M("f(x) = %s. Quel est l’extremum de f sur ℝ ?" % f, ans,
                 ["%s %s, atteint en x = %s" % ("maximum" if a > 0 else "minimum", d(be), d(al)), "%s %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(al), d(be)), "%s %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(be), d(-al)), "%s %s, atteint en x = %s" % ("maximum" if a > 0 else "minimum", d(al), d(be)), "%s %s, atteint en x = 0" % ("minimum" if a > 0 else "maximum", d(a * al * al + be))],
                 "a = %s %s 0 : f admet un <b>%s</b>. Sommet : (%s ; %s)." % (d(a), "&gt;" if a > 0 else "&lt;", ans, d(al), d(be)))
    if k == "var":
        xs = ["−∞", d(al), "+∞"]
        ys = ["", be, ""]
        ans = "décroissante sur ]−∞ ; %s] et croissante sur [%s ; +∞[" % (d(al), d(al)) if a > 0 else "croissante sur ]−∞ ; %s] et décroissante sur [%s ; +∞[" % (d(al), d(al))
        return M("Quelles sont les variations de f(x) = %s ?" % canon(a, al, be), ans,
                 ["croissante sur ]−∞ ; %s] et décroissante sur [%s ; +∞[" % (d(al), d(al)) if a > 0 else "décroissante sur ]−∞ ; %s] et croissante sur [%s ; +∞[" % (d(al), d(al)),
                  ans.replace(d(al), d(-al)) if al else ans.replace(d(al) + "]", "1]").replace("[" + d(al), "[1"), ans.replace(d(al), d(be)) if be != al else ans.replace(d(al), d(al + 1))],
                 "a %s 0 : la parabole est tournée vers le %s ; le changement de sens a lieu en α = %s : <b>%s</b>." % ("&gt;" if a > 0 else "&lt;", "haut" if a > 0 else "bas", d(al), ans))
    f = dev(a, al, be)
    return M("Quel est l’axe de symétrie de la parabole d’équation y = %s ?" % f, "la droite x = %s" % d(al), ["la droite x = %s" % d(-al) if al else "la droite x = 1", "la droite y = %s" % d(be), "la droite x = %s" % d(be) if be != al else "la droite y = %s" % d(al)],
             "L’axe passe par le sommet : <b>x = α = %s</b>." % d(al))


def s4():
    k = R.choice(["rac", "rac", "SP", "autre", "fact"])
    a = nz(R, -3, 3)
    x1, x2 = sorted(R.sample(range(-7, 8), 2))
    if k == "rac":
        f = "%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (-x1, "")), E((1, "x"), (-x2, "")))
        return M("Quelles sont les racines de f(x) = %s ?" % f, "%s et %s" % (d(x1), d(x2)), ["%s et %s" % (d(-x2), d(-x1)), "%s, %s et %s" % (d(a), d(x1), d(x2)), "%s et %s" % (d(x1 * a), d(x2 * a)) if a != 1 else "%s et %s" % (d(-x1), d(x2))],
                 "Un produit est nul si un facteur est nul : x = <b>%s</b> ou x = <b>%s</b>." % (d(x1), d(x2)))
    if k == "SP":
        b, c = -a * (x1 + x2), a * x1 * x2
        which = R.choice(["S", "P"])
        if which == "S":
            return M("f(x) = %s a deux racines. Que vaut leur somme ?" % P2(a, b, c), fq(Fr(-b, a)), [fq(Fr(b, a)), fq(Fr(c, a)), d(-b), fq(Fr(-c, a)), fq(Fr(-b, 2 * a))],
                     "Somme des racines = −b ÷ a = %s ÷ %s = <b>%s</b>." % (d(-b), par(a), fq(Fr(-b, a))))
        return M("f(x) = %s a deux racines. Que vaut leur produit ?" % P2(a, b, c), fq(Fr(c, a)), [fq(Fr(-c, a)), fq(Fr(-b, a)), d(c) if a != 1 else fq(Fr(b, a))],
                 "Produit des racines = c ÷ a = %s ÷ %s = <b>%s</b>." % (d(c), par(a), fq(Fr(c, a))))
    if k == "autre":
        b, c = -a * (x1 + x2), a * x1 * x2
        if x1 == 0:
            return None
        return M("%s est une racine de f(x) = %s. Quelle est l’autre racine ?" % (d(x1), P2(a, b, c)), d(x2), [d(-x2), fq(Fr(c, a * x2)) if Fr(c, a * x2) != x2 else d(x2 + 1), d(-x1), d(x1 + x2)],
                 "Produit des racines = c ÷ a = %s, donc l’autre racine vaut %s ÷ %s = <b>%s</b>." % (fq(Fr(c, a)), fq(Fr(c, a)), par(x1), d(x2)))
    b, c = -a * (x1 + x2), a * x1 * x2
    ans = "%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (-x1, "")), E((1, "x"), (-x2, "")))
    return M("f(x) = %s s’annule en %s et en %s. Quelle est sa forme factorisée ?" % (P2(a, b, c), d(x1), d(x2)), ans,
             ["%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (x1, "")), E((1, "x"), (x2, ""))), "(%s)(%s)" % (E((1, "x"), (-x1, "")), E((1, "x"), (-x2, ""))) if a != 1 else "%s(%s)(%s)" % ("2", E((1, "x"), (-x1, "")), E((1, "x"), (-x2, ""))),
              "%s(%s)(%s)" % (MINUS if a == 1 else "", E((1, "x"), (-x1, "")), E((1, "x"), (-x2, ""))), "%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (-x1, "")), E((1, "x"), (x2, ""))), "%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (x1, "")), E((1, "x"), (-x2, "")))],
             "f(x) = a(x − x₁)(x − x₂) avec a = %s : <b>%s</b>." % (d(a), ans))


def s5():
    k = R.choice(["graph", "graph", "enclos", "profit", "lancer"])
    if k == "graph":
        a = R.choice([1, -1, Fr(1, 2), Fr(-1, 2)])
        al, be = R.randint(-3, 3), R.randint(-3, 3)
        svg = kurve([(lambda x, a=a, al=al, be=be: float(a) * (x - al) ** 2 + be, BLUE, "")], (-5, 5, 1), (-5, 5, 1), label="parabole")
        sub = R.choice(["S", "a"])
        if sub == "S":
            return M("<div class='qfig'>%s</div>Quel est le sommet de la parabole ?" % svg, "S(%s ; %s)" % (d(al), d(be)), ["S(%s ; %s)" % (d(be), d(al)) if al != be else "S(%s ; %s)" % (d(al + 1), d(be)), "S(%s ; %s)" % (d(-al), d(be)) if al else "S(%s ; %s)" % (d(al), d(-be) if be else "1"), "S(0 ; %s)" % d(a * al * al + be) if al else "S(1 ; %s)" % d(be)],
                     "On lit le point le plus %s : <b>S(%s ; %s)</b>." % ("bas" if a > 0 else "haut", d(al), d(be)))
        return M("<div class='qfig'>%s</div>La parabole représente f(x) = a(x − α)² + β. Quel est le signe de a ?" % svg, "a %s 0" % ("&gt;" if a > 0 else "&lt;"), ["a %s 0" % ("&lt;" if a > 0 else "&gt;"), "a = 0", "on ne peut pas savoir"],
                 "La parabole est tournée vers le %s : <b>a %s 0</b>." % ("haut" if a > 0 else "bas", "&gt;" if a > 0 else "&lt;"))
    if k == "enclos":
        P = R.choice([20, 24, 28, 32, 36, 40, 60, 80])
        x = Fr(P, 4)
        return M("Avec %d m de clôture, on délimite un rectangle de côtés x et %d − x (en m). Pour quelle valeur de x l’aire x(%d − x) est-elle maximale ?" % (P, P // 2, P // 2), d(x) + NB + "m",
                 [d(P // 2) + NB + "m", d(x * x) + NB + "m", d(Fr(P, 8)) + NB + "m"], "A(x) = −x² + %dx : α = −%d ÷ (−2) = <b>%s m</b> (un carré)." % (P // 2, P // 2, d(x)))
    if k == "profit":
        al, be = R.randint(10, 60), R.randint(2, 20) * 100
        a = R.choice([-1, -2, -3])
        return M("Le bénéfice (en €) pour x objets vendus est B(x) = %s. Quel est le bénéfice maximal ?" % canon(a, al, be), euro(be), [euro(al), euro(be + a * al * al) if be + a * al * al > 0 else euro(be * 2), euro(-a * al * al)],
                 "a &lt; 0 : le maximum est β = <b>%s</b>, atteint pour %d objets." % (euro(be), al))
    t = R.choice([1, 2, 3])
    h0 = R.randint(1, 3)
    v = 10 * t
    return M("La hauteur (en m) d’une balle à l’instant t (en s) est h(t) = −5t² + %dt + %d. Quelle hauteur maximale atteint-elle ?" % (v, h0), d(5 * t * t + h0) + NB + "m",
             [d(h0) + NB + "m", d(10 * t * t + h0) + NB + "m", d(5 * t * t) + NB + "m"], "α = −%d ÷ (−10) = %d ; h(%d) = −5 × %d + %d + %d = <b>%s m</b>." % (v, t, t, t * t, v * t, h0, d(5 * t * t + h0)))


def main():
    seen = set()
    sets = [("Développer et calculer", mix(R, seen, [(s1, 20)])), ("Forme canonique", mix(R, seen, [(s2, 20)])),
            ("Sommet, extremum et variations", mix(R, seen, [(s3, 20)])), ("Racines, somme et produit", mix(R, seen, [(s4, 20)])), ("Lecture graphique et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Trois écritures de f(x) (a ≠ 0) : <b>développée</b> ax² + bx + c, <b>canonique</b> a(x − α)² + β, <b>factorisée</b> a(x − x₁)(x − x₂) (quand f a deux racines).",
              "α = −b ÷ (2a) et β = f(α). Le sommet de la parabole est S(α ; β), l’axe de symétrie est la droite x = α.",
              "Si a &gt; 0, f est décroissante puis croissante : minimum β en α. Si a &lt; 0, croissante puis décroissante : maximum β.",
              "Racines x₁ et x₂ : x₁ + x₂ = −b ÷ a et x₁ × x₂ = c ÷ a."],
             [("f(x) = 2x² − 12x + 13", ["α = 12 ÷ 4 = 3", "β = f(3) = 18 − 36 + 13 = −5"], "f(x) = 2(x − 3)² − 5, minimum −5 en x = 3")],
             [["a(x + 3)² + 1 : sommet (3 ; 1)", "x + 3 = x − (−3) : sommet (−3 ; 1)."], ["α = b ÷ (2a)", "α = −b ÷ (2a)."], ["2(x − 1)² = 2x² − 2x + 2", "2(x² − 2x + 1) = 2x² − 4x + 2."]])
    faq = [("Quelle forme choisir ?", "La forme canonique donne le sommet et les variations, la forme factorisée les racines et le signe, la forme développée l’image de 0 (c) et les calculs de Δ."),
           ("Comment obtenir la forme canonique ?", "On calcule α = −b ÷ (2a) puis β = f(α), et on écrit a(x − α)² + β. On peut vérifier en développant.")]
    unit("premiere", R, "forme-canonique-et-sommet", "A",
         "Fonctions polynômes du second degré : formes développée, canonique et factorisée ; sommet et axe de symétrie de la parabole ; variations et extremum ; somme et produit des racines ; choisir la forme adaptée à un problème",
         "Second degré : forme canonique, sommet et variations", "Forme canonique et sommet",
         "Fiches de maths première sur le second degré : forme canonique, sommet de la parabole, variations, extremum, forme factorisée, somme et produit des racines. 100 exercices corrigés.",
         "f(x) = a(x − α)² + β : sommet S(α ; β)", "α = −b ÷ (2a) et β = f(α)", body, faq, sets, 6)


if __name__ == "__main__":
    main()
