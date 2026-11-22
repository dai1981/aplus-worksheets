# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Équations du second degré (discriminant, nombre de solutions, résolution, racines irrationnelles, problèmes)
  python3 tools/gen_fr_maths_premiere_equations_du_second_degre.py
Erreurs : Δ = b² − 4ac avec −b² quand b < 0, oublier le 2a au dénominateur, Δ < 0 donc « deux solutions négatives », diviser par x et perdre la solution 0.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60607)


def eq(a, b, c):
    return "%s = 0" % P2(a, b, c)


def S(v):
    v = sorted(set(v))
    return "S = ∅" if not v else "S = {%s}" % " ; ".join(fq(x) for x in v)


def s1():
    a, b, c = nz(R, -5, 5), R.randint(-9, 9), R.randint(-9, 9)
    D = b * b - 4 * a * c
    return M("Calcule le discriminant de %s." % P2(a, b, c), d(D), [d(-b * b - 4 * a * c), d(b * b + 4 * a * c), d(b - 4 * a * c), d(b * b - 2 * a * c), d(4 * a * c - b * b), d(b * b - 4 * a - c), d(b * b + a * c)],
             "Δ = b² − 4ac = %s² − 4 × %s × %s = <b>%s</b>." % (par(b), par(a), par(c), d(D)))


def s2():
    while True:
        a, b, c = nz(R, -5, 5), R.randint(-8, 8), R.randint(-9, 9)
        D = b * b - 4 * a * c
        want = R.choice(["+", "0", "-"])
        if (want == "+" and D > 0) or (want == "-" and D < 0) or (want == "0" and D == 0):
            break
    ans = {1: "deux solutions", 0: "une seule solution", -1: "aucune solution réelle"}[(D > 0) - (D < 0)]
    return M("Combien de solutions réelles l’équation %s a-t-elle ?" % eq(a, b, c), ans, [v for v in ["deux solutions", "une seule solution", "aucune solution réelle", "deux solutions négatives"] if v != ans],
             "Δ = %s² − 4 × %s × %s = %s %s 0 : <b>%s</b>." % (par(b), par(a), par(c), d(D), "&gt;" if D > 0 else "&lt;" if D < 0 else "=", ans))


def s3():
    k = R.choice(["two", "two", "two", "double", "zero", "none"])
    a = R.choice([1, 1, 2, -1, 3, -2])
    if k == "two":
        x1, x2 = R.sample(range(-9, 10), 2)
        if a in (2, 3, -2) and R.random() < 0.5:
            x1 = Fr(R.choice([1, -1, 3, -3, 5]), abs(a))
        b, c = -a * (x1 + x2), a * x1 * x2
        if Fr(b).denominator != 1 or Fr(c).denominator != 1:
            return None
        return M("Résous %s." % eq(a, b, c), S([x1, x2]), [S([-x1, -x2]), S([x1 * a, x2 * a]) if a != 1 else S([x1, -x2]), S([x1 + x2, x1 * x2]) if x1 + x2 != x1 * x2 else S([x2]), S([x1]), S([x2]), S([x1, -x2]), S([-x1, x2])],
                 "Δ = %s ; x = (−b ± √Δ) ÷ (2a) donne <b>%s</b>." % (d(b * b - 4 * a * c), S([x1, x2])))
    if k == "double":
        x0 = R.randint(-6, 6)
        b, c = -2 * a * x0, a * x0 * x0
        return M("Résous %s." % eq(a, b, c), S([x0]), [S([-x0]) if x0 else S([1]), S([x0, -x0]) if x0 else "S = ∅", "S = ∅" if x0 else S([2])],
                 "Δ = 0 : une seule solution x = −b ÷ (2a) = <b>%s</b>." % d(x0))
    if k == "zero":
        b = nz(R, -9, 9)
        return M("Résous %s." % eq(a, b, 0), S([0, Fr(-b, a)]), [S([Fr(-b, a)]), S([Fr(b, a), 0]), S([0, Fr(-a, b)]), S([0]), S([Fr(b, a)])],
                 "x(%s) = 0 : x = 0 ou x = %s. <b>%s</b> (on ne divise pas par x : on perdrait 0)." % (E((a, "x"), (b, "")), fq(Fr(-b, a)), S([0, Fr(-b, a)])))
    b = R.randint(-4, 4)
    c = R.randint(b * b // 4 + 1, 12) if a > 0 else -R.randint(b * b // 4 + 1, 12)
    if b * b - 4 * a * c >= 0:
        return None
    return M("Résous %s." % eq(a, b, c), "S = ∅", [S([b]) if b else S([1]), S([-c, c]), S([Fr(-b, 2 * a)]) if b else S([2]), S([Fr(-c, a)])],
             "Δ = %s &lt; 0 : <b>pas de solution réelle</b>." % d(b * b - 4 * a * c))


def s4():
    k = R.choice(["p", "p", "half"])
    p = R.randint(-6, 6)
    m = R.choice([2, 3, 5, 6, 7, 10, 11])
    if k == "p":
        b, c = -2 * p, p * p - m
        sp = d(p) if p else ""
        ans = "S = {%s − √%d ; %s + √%d}" % (sp, m, sp, m) if p else "S = {−√%d ; √%d}" % (m, m)
        D = b * b - 4 * c
        return M("Résous %s." % eq(1, b, c), ans,
                 ["S = {%s − √%d ; %s + √%d}" % (d(-p), m, d(-p), m) if p else "S = {%s}" % d(m), "S = {%s − √%d ; %s + √%d}" % (sp, D, sp, D) if p else "S = {−√%d ; √%d}" % (D, D), "S = {%s − %d ; %s + %d}" % (sp, m, sp, m) if p else "S = {−%d ; %d}" % (m, m), "S = ∅"],
                 "Δ = %d = 4 × %d ; x = (%s ± 2√%d) ÷ 2 = %s ± √%d : <b>%s</b>." % (D, m, d(-b), m, d(p), m, ans))
    if k == "half":
        a, b, c = 1, R.choice([1, 3, 5, -1, -3, -5]), R.randint(-6, -1)
        D = b * b - 4 * c
        if int(math.isqrt(D)) ** 2 == D:
            return None
        ans = "S = {(%s − √%d) ÷ 2 ; (%s + √%d) ÷ 2}" % (d(-b), D, d(-b), D)
        return M("Résous %s." % eq(a, b, c), ans,
                 ["S = {%s − √%d ; %s + √%d}" % (d(-b), D, d(-b), D), "S = {(%s − √%d) ÷ 2 ; (%s + √%d) ÷ 2}" % (d(b), D, d(b), D), "S = {(%s − %d) ÷ 2 ; (%s + %d) ÷ 2}" % (d(-b), D, d(-b), D)],
                 "Δ = %s² − 4 × %s = %d ; x = (−b ± √Δ) ÷ (2a) : <b>%s</b>." % (par(b), par(c), D, ans))


def s5():
    k = R.choice(["rect", "rect", "nombre", "consec", "chute", "aire_cadre"])
    if k == "rect":
        x = R.randint(3, 15)
        y = x + R.randint(2, 9)
        return M("Un rectangle a une aire de %d m² et sa longueur dépasse sa largeur de %d m. Quelle est sa largeur ?" % (x * y, y - x), "%d m" % x, ["%d m" % y, d(-y) + " m", "%s m" % d(Fr(x * y, 2))],
                 "x(x + %d) = %d ⇔ x² + %dx − %d = 0 ; la solution positive est <b>%d m</b>." % (y - x, x * y, y - x, x * y, x))
    if k == "nombre":
        x = R.randint(3, 14)
        return M("Le carré d’un nombre positif est égal à %d fois ce nombre plus %d. Quel est ce nombre ?" % (x - 1, x), str(x), [d(-1), str(x - 1), str(x * x)],
                 "x² = %dx + %d ⇔ x² − %dx − %d = 0 ⇔ (x − %d)(x + 1) = 0 ; x &gt; 0 donc <b>x = %d</b>." % (x - 1, x, x - 1, x, x, x))
    if k == "consec":
        n = R.randint(4, 30)
        return M("Le produit de deux entiers naturels consécutifs vaut %d. Quel est le plus petit ?" % (n * (n + 1)), str(n), [str(n + 1), d(-(n + 1)), str(n * (n + 1) // 2)],
                 "n(n + 1) = %d ⇔ n² + n − %d = 0 ; Δ = %d = %d² ; n = <b>%d</b>." % (n * (n + 1), n * (n + 1), (2 * n + 1) ** 2, 2 * n + 1, n))
    if k == "chute":
        t = R.randint(2, 6)
        h = 5 * t * t
        return M("Un objet lâché d’une hauteur de %d m est à la hauteur h(t) = %d − 5t² (t en s). Au bout de combien de temps touche-t-il le sol ?" % (h, h), "%d s" % t, ["%d s" % (t * t), "%s s" % d(Fr(h, 10)), "%d s" % (2 * t), "%d s" % (t + 1)],
                 "%d − 5t² = 0 ⇔ t² = %d ⇔ t = <b>%d s</b> (t &gt; 0)." % (h, t * t, t))
    L_, l_ = R.randint(8, 20), R.randint(5, 12)
    x = R.choice([1, 2, 3])
    A = (L_ + 2 * x) * (l_ + 2 * x) - L_ * l_
    return M("Autour d’une photo de %d cm sur %d cm, on met un cadre de largeur x. L’aire du cadre seul vaut %d cm². Combien vaut x ?" % (L_, l_, A), "%d cm" % x, ["%d cm" % (x + 1), "%s cm" % d(Fr(A, 2 * (L_ + l_))) if Fr(A, 2 * (L_ + l_)) != x else "%d cm" % (x + 2), "%d cm" % (2 * x)],
             "(%d + 2x)(%d + 2x) − %d = %d ⇔ 4x² + %dx − %d = 0 ; la solution positive est <b>%d cm</b>." % (L_, l_, L_ * l_, A, 2 * (L_ + l_), A, x))


def main():
    seen = set()
    sets = [("Calculer le discriminant", mix(R, seen, [(s1, 20)])), ("Nombre de solutions", mix(R, seen, [(s2, 20)])),
            ("Résoudre", mix(R, seen, [(s3, 20)])), ("Solutions avec des racines carrées", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Pour ax² + bx + c = 0 (a ≠ 0), on calcule le <b>discriminant</b> Δ = b² − 4ac.",
              "Δ &gt; 0 : deux solutions x = (−b − √Δ) ÷ (2a) et x = (−b + √Δ) ÷ (2a). Δ = 0 : une solution x = −b ÷ (2a). Δ &lt; 0 : aucune solution réelle.",
              "Raccourcis : si c = 0, on factorise par x ; si b = 0, on isole x² ; si une racine est évidente, l’autre vient du produit c ÷ a."],
             [("2x² − 3x − 2 = 0", ["Δ = 9 + 16 = 25", "x = (3 − 5) ÷ 4 = −0,5 ou x = (3 + 5) ÷ 4 = 2"], "S = {−0,5 ; 2}")],
             [["Δ = −3² − 4ac quand b = −3", "b² = (−3)² = 9 : Δ = 9 − 4ac."], ["x = −b ± √Δ ÷ 2a", "Tout le numérateur est divisé par 2a : (−b ± √Δ) ÷ (2a)."],
              ["x² = 3x, donc x = 3", "x² − 3x = 0 ⇔ x(x − 3) = 0 : S = {0 ; 3}."]])
    faq = [("Faut-il toujours calculer Δ ?", "Non. Si c = 0 ou b = 0, ou si l’équation est déjà factorisée, on résout directement. Δ sert dans le cas général."),
           ("Que faire si Δ n’est pas un carré parfait ?", "On garde la valeur exacte avec √Δ, par exemple x = 1 ± √2, et on simplifie si possible.")]
    unit("premiere", R, "equations-du-second-degre", "A",
         "Résoudre une équation du second degré : discriminant, nombre de solutions, formules des solutions ; choisir une stratégie (factorisation, racine évidente, forme canonique) ; résoudre un problème qui se ramène au second degré",
         "Équations du second degré et discriminant", "Équations du second degré",
         "Fiches de maths première sur les équations du second degré : discriminant, nombre de solutions, résolution, solutions avec racines carrées et problèmes. 100 exercices corrigés.",
         "Δ = b² − 4ac", "Δ > 0 : deux solutions ; Δ = 0 : une ; Δ < 0 : aucune", body, faq, sets, 7)


if __name__ == "__main__":
    main()
