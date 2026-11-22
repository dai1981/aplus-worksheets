# -*- coding: utf-8 -*-
"""
France Maths Seconde : Fonctions affines (coefficient directeur, ordonnée à l’origine, variations, signe, expression)
  python3 tools/gen_fr_maths_seconde_fonctions_affines.py
Erreurs : m = (x₂ − x₁)/(y₂ − y₁), confondre m et p, croissante si p > 0, résoudre mx + p = 0 en x = p/m.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60511)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    m, p = nz(-6, 6), nz(-9, 9)
    k = R.choice(["m", "p", "var", "taux"])
    f = E((m, "x"), (p, ""))
    if k == "m":
        return M("f(x) = %s. Quel est le coefficient directeur de f ?" % f, d(m), [d(p), d(-m), d(m + p)], "f(x) = mx + p avec m = <b>%s</b>." % d(m))
    if k == "p":
        return M("f(x) = %s. Quelle est l’ordonnée à l’origine de f ?" % f, d(p), [d(m), d(-p), "0"], "p = f(0) = <b>%s</b>." % d(p))
    if k == "var":
        ans = "croissante sur ℝ" if m > 0 else "décroissante sur ℝ"
        return M("Quel est le sens de variation de f(x) = %s ?" % f, ans, ["décroissante sur ℝ" if m > 0 else "croissante sur ℝ", "croissante puis décroissante", "constante sur ℝ"],
                 "m = %s est %s : f est <b>%s</b>." % (d(m), "positif" if m > 0 else "négatif", ans))
    dx = R.randint(1, 5)
    return M("f(x) = %s. De combien f(x) varie-t-il quand x augmente de %d ?" % (f, dx), d(m * dx), [d(m), d(m * dx + p), d(dx)], "f(x + h) − f(x) = mh = %s × %d = <b>%s</b>." % (d(m), dx, d(m * dx)))


def s2():
    m = nz(-5, 5)
    p = R.randint(-9, 9)
    x1, x2 = R.sample(range(-6, 7), 2)
    y1, y2 = m * x1 + p, m * x2 + p
    k = R.choice(["m", "m", "f"])
    if k == "m":
        w = [fq(Fr(x2 - x1, y2 - y1)) if Fr(x2 - x1, y2 - y1) != m else d(m + 1), d(y2 - y1) if y2 - y1 != m else d(m - 1), fq(Fr(y2 + y1, x2 + x1)) if x2 + x1 and Fr(y2 + y1, x2 + x1) != m else d(-m)]
        return M("f est affine avec f(%s) = %s et f(%s) = %s. Quel est son coefficient directeur ?" % (d(x1), d(y1), d(x2), d(y2)), d(m), w,
                 "m = (%s − %s) ÷ (%s − %s) = %s ÷ %s = <b>%s</b>." % (d(y2), par(y1), d(x2), par(x1), d(y2 - y1), par(x2 - x1), d(m)))
    ans = "f(x) = %s" % E((m, "x"), (p, ""))
    return M("f est affine avec f(%s) = %s et f(%s) = %s. Quelle est son expression ?" % (d(x1), d(y1), d(x2), d(y2)), ans,
             ["f(x) = %s" % E((m, "x"), (-p, "")) if p else "f(x) = %s" % E((m, "x"), (1, "")), "f(x) = %s" % E((-m, "x"), (p, "")), "f(x) = %s" % E((p, "x"), (m, "")) if p and p != m else "f(x) = %s" % E((m, "x"), (p + 2, ""))],
             "m = %s ; p = f(%s) − m × %s = %s : <b>%s</b>." % (d(m), d(x1), par(x1), d(p), ans))


def s3():
    m = R.choice([-3, -2, -1, Fr(-1, 2), Fr(1, 2), 1, 2, 3, Fr(3, 2), Fr(-3, 2)])
    p = R.randint(-3, 3)
    svg = relabel(de_k8.kosy(lines=[(m, p, BLUE, "")], lo=-5, hi=5, u=22), "droite représentant f")
    k = R.choice(["m", "p", "f"])
    if k == "p":
        return M("<div class='qfig'>%s</div>Quelle est l’ordonnée à l’origine de f ?" % svg, d(p), [d(-p) if p else "1", fq(m) if Fr(m) != p else d(p + 2), d(p + 1)], "La droite coupe l’axe des ordonnées en <b>%s</b>." % d(p))
    if k == "m":
        return M("<div class='qfig'>%s</div>Quel est le coefficient directeur de f ?" % svg, fq(m), [fq(-m), fq(1 / Fr(m)) if 1 / Fr(m) != m else fq(2 * m), d(p) if Fr(p) not in (Fr(m), -Fr(m)) else fq(m + 1)],
                 "On avance de %s vers la droite, on %s de %s : m = <b>%s</b>." % ("1" if Fr(m).denominator == 1 else "2", "monte" if m > 0 else "descend", d(abs(m)) if Fr(m).denominator == 1 else d(abs(2 * m)), fq(m)))
    ans = "f(x) = %s" % E((m, "x"), (p, ""))
    return M("<div class='qfig'>%s</div>Quelle est l’expression de f ?" % svg, ans, ["f(x) = %s" % E((-m, "x"), (p, "")), "f(x) = %s" % E((p, "x"), (m, "")) if p and Fr(p) != Fr(m) else "f(x) = %s" % E((m, "x"), (p + 1, "")), "f(x) = %s" % E((m, "x"), (-p, "")) if p else "f(x) = %s" % E((2 * m, "x"))],
             "Ordonnée à l’origine %s, coefficient directeur %s : <b>%s</b>." % (d(p), fq(m), ans))


def s4():
    m, p = nz(-6, 6), nz(-9, 9)
    x0 = Fr(-p, m)
    k = R.choice(["zero", "sign", "sign", "ineq"])
    f = E((m, "x"), (p, ""))
    if k == "zero":
        return M("Pour quelle valeur f(x) = %s s’annule-t-elle ?" % f, "x = %s" % fq(x0), ["x = %s" % fq(Fr(p, m)) if p else "x = 1", "x = %s" % fq(Fr(m, -p)) if Fr(m, -p) != x0 else "x = %s" % fq(x0 + 1), "x = %s" % d(-p)] if Fr(-p) != x0 else ["x = %s" % fq(Fr(p, m)), "x = %s" % fq(Fr(m, -p)), "x = %s" % fq(x0 + 1)],
                 "%s = 0 ⇔ x = %s ÷ %s = <b>%s</b>." % (f, d(-p), par(m), fq(x0)))
    if k == "sign":
        ans = "négatif puis positif" if m > 0 else "positif puis négatif"
        return M("Quel est le signe de f(x) = %s quand x parcourt ℝ (de gauche à droite) ?" % f, ans + " (il change en %s)" % fq(x0), [("positif puis négatif" if m > 0 else "négatif puis positif") + " (il change en %s)" % fq(x0), "toujours positif", ans + " (il change en %s)" % fq(-x0) if x0 else "toujours négatif"],
                 "m = %s est %s : f(x) est du signe de m à droite de %s : <b>%s</b>." % (d(m), "positif" if m > 0 else "négatif", fq(x0), ans))
    ans = "S = ]%s ; +∞[" % fq(x0) if m > 0 else "S = ]−∞ ; %s[" % fq(x0)
    return M("Résous f(x) &gt; 0 avec f(x) = %s." % f, ans, ["S = ]−∞ ; %s[" % fq(x0) if m > 0 else "S = ]%s ; +∞[" % fq(x0), ans.replace("]%s" % fq(x0), "[%s" % fq(x0)).replace("%s[" % fq(x0), "%s]" % fq(x0)), "S = ]%s ; +∞[" % fq(-x0) if m > 0 and x0 else "S = ℝ"],
             "%s &gt; 0 ⇔ x %s %s : <b>%s</b>." % (f, "&gt;" if m > 0 else "&lt;", fq(x0), ans))


def s5():
    k = R.choice(["taxi", "temp", "location", "compare"])
    if k == "taxi":
        p, m = R.randint(3, 8), R.choice([Fr(3, 2), 2, Fr(5, 2), 3])
        x = R.randint(5, 25)
        return M("Un taxi coûte %d € de prise en charge et %s € par km. Le prix est une fonction affine de la distance x. Combien coûte une course de %d km ?" % (p, d(m), x), euro(m * x + p), [euro((m + p) * x), euro(m * x), euro(m + p + x)],
                 "P(x) = %sx + %d ; P(%d) = <b>%s</b>." % (d(m), p, x, euro(m * x + p)))
    if k == "temp":
        return M("Une fonction affine f vérifie f(0) = 32 et f(100) = 212 (conversion °C → °F). Quel est son coefficient directeur ?", "1,8", ["2,12", "0,56", "180"], "m = (212 − 32) ÷ (100 − 0) = <b>1,8</b>.")
    if k == "location":
        a1, b1 = R.randint(2, 5), R.randint(20, 50)
        a2 = a1 + R.randint(2, 6)
        n = Fr(b1, a2 - a1)
        if n.denominator != 1:
            return None
        return M("Formule A : f(x) = %dx + %d. Formule B : g(x) = %dx. Pour quelle valeur de x les deux formules coûtent-elles la même chose ?" % (a1, b1, a2), str(n), [str(Fr(b1, a1 + a2)) if Fr(b1, a1 + a2).denominator == 1 else str(n + 1), str(b1), str(n * 2)],
                 "%dx + %d = %dx ⇔ x = <b>%s</b> (abscisse du point d’intersection des droites)." % (a1, b1, a2, n))
    m = R.choice([2, 3, 4])
    return M("Une fonction linéaire f vérifie f(5) = %d. Que vaut f(15) ?" % (5 * m), str(15 * m), [str(5 * m + 10), str(5 * m * 2), str(m)],
             "f(x) = %dx, donc f(15) = <b>%d</b> (proportionnalité)." % (m, 15 * m))


def main():
    seen = set()
    sets = [("Coefficient directeur et ordonnée à l’origine", mix(R, seen, [(s1, 20)])), ("Déterminer une fonction affine", mix(R, seen, [(s2, 20)])),
            ("Lecture graphique", mix(R, seen, [(s3, 20)])), ("Signe et inéquations", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["f(x) = mx + p : m est le <b>coefficient directeur</b> (taux de variation : f augmente de m quand x augmente de 1), p l’<b>ordonnée à l’origine</b> (p = f(0)).",
              "Si m &gt; 0, f est croissante ; si m &lt; 0, décroissante ; si m = 0, constante. La courbe est une droite.",
              "Avec deux points : m = (f(x₂) − f(x₁)) ÷ (x₂ − x₁). mx + p est du signe de m à droite de −p/m."],
             [("f(1) = 5 et f(4) = 14", ["m = (14 − 5) ÷ (4 − 1) = 3", "p = 5 − 3 × 1 = 2"], "f(x) = 3x + 2")],
             [["m = (x₂ − x₁) ÷ (y₂ − y₁)", "C’est (y₂ − y₁) ÷ (x₂ − x₁)."], ["f croissante car p &gt; 0", "Le sens de variation dépend de m, pas de p."], ["3x + 6 = 0 donne x = 2", "x = −6 ÷ 3 = −2."]])
    faq = [("Quelle différence entre affine et linéaire ?", "Une fonction linéaire est une fonction affine avec p = 0 : elle modélise la proportionnalité."),
           ("Comment tracer la droite ?", "On place deux points, par exemple (0 ; p) et (1 ; m + p).")]
    unit("seconde", R, "fonctions-affines", "F",
         "Interpréter le coefficient directeur comme taux de variation et l’ordonnée à l’origine ; relier le sens de variation, le signe et la droite représentative d’une fonction affine ; déterminer une fonction affine à partir de deux valeurs ou d’un graphique",
         "Fonctions affines", "Fonctions affines",
         "Fiches de maths seconde sur les fonctions affines : coefficient directeur, ordonnée à l’origine, variations, signe, lecture graphique et problèmes. 100 exercices corrigés.",
         "f(x) = mx + p : m taux de variation, p = f(0)", "m > 0 : croissante ; m < 0 : décroissante", body, faq, sets, 11)


if __name__ == "__main__":
    main()
