# -*- coding: utf-8 -*-
"""
France Maths 3e : Développer et factoriser (double distributivité, facteur commun, démontrer)
  python3 tools/gen_fr_maths_3e_developper_et_factoriser.py
Erreurs : oublier un produit, erreur de signe devant une parenthèse, factoriser sans le même facteur, « vérifier sur un exemple » au lieu de démontrer.
"""
import random
from fr_c4 import *

R = random.Random(60404)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def B(a, b, v="x"):
    return "(%s)" % E((a, v), (b, ""))


def s1():
    a, b, c, e = nz(-6, 6), nz(-9, 9), nz(-6, 6), nz(-9, 9)
    r = E((a * c, "x²"), (a * e + b * c, "x"), (b * e, ""))
    w1 = E((a * c, "x²"), (b * e, ""))
    w2 = E((a * c, "x²"), (a * e + b * c, "x"), (-b * e, ""))
    w3 = E((a * c, "x²"), (a * e - b * c, "x"), (b * e, "")) if a * e - b * c != a * e + b * c else E((a * c, "x"), (a * e + b * c, "x"), (b * e, ""))
    return M("Développe et réduis : %s%s" % (B(a, b), B(c, e)), r, [w1, w2, w3],
             "%s × %s + %s × %s + %s × %s + %s × %s, puis on réduit : <b>%s</b>." % (E((a, "x")), E((c, "x")), E((a, "x")), par(e), par(b), E((c, "x")), par(b), par(e), r))


def s2():
    a, b, c, e = nz(-5, 5), nz(-9, 9), nz(-5, 5), nz(-9, 9)
    f, g = nz(-5, 5), nz(-9, 9)
    k = R.choice(["moins", "plus"])
    A = (a * c, a * e + b * c, b * e)
    if k == "moins":
        r = (A[0], A[1] - f, A[2] - g)
        q = "%s%s − %s" % (B(a, b), B(c, e), B(f, g))
        w = [(A[0], A[1] - f, A[2] + g), (A[0], A[1] + f, A[2] + g), (A[0], A[1] - f, A[2])]
    else:
        m = nz(-4, 4)
        r = (A[0], A[1] + m * f, A[2] + m * g)
        q = "%s%s + %s%s" % (B(a, b), B(c, e), d(m) if m != -1 else MINUS, B(f, g)) if m != 1 else "%s%s + %s" % (B(a, b), B(c, e), B(f, g))
        q = q.replace("+ −", "− ") if m < 0 else q
        w = [(A[0], A[1] + f, A[2] + m * g), (A[0], A[1] + m * f, A[2] + g), (A[0] + m, A[1], A[2] + m * g)]
    rs = E((r[0], "x²"), (r[1], "x"), (r[2], ""))
    return M("Développe et réduis : %s" % q, rs, [E((x[0], "x²"), (x[1], "x"), (x[2], "")) for x in w],
             "On développe chaque partie, en changeant les signes après un « − » devant une parenthèse : <b>%s</b>." % rs)


def s3():
    a, b = nz(-5, 5), nz(-9, 9)
    c, e = nz(-5, 5), nz(-9, 9)
    f, g = nz(-5, 5), nz(-9, 9)
    if (c, e) == (f, g) or (a, b) == (c, e):
        return None
    k = R.choice(["plus", "moins", "carre"])
    F = B(a, b)
    if k == "plus":
        q = "%s%s + %s%s" % (F, B(c, e), F, B(f, g))
        r = "%s%s" % (F, B(c + f, e + g)) if (c + f, e + g) != (0, 0) else None
        w = ["%s%s" % (F, B(c * f, e * g)) if c * f else "%s²%s" % (F, B(c + f, e + g)), "%s²%s" % (F, B(c + f, e + g)), "%s%s" % (F, B(c + f, e - g)) if g else "%s%s" % (F, B(c - f, e))]
    elif k == "moins":
        q = "%s%s − %s%s" % (F, B(c, e), F, B(f, g))
        r = "%s%s" % (F, B(c - f, e - g)) if c - f or e - g else None
        w = ["%s%s" % (F, B(c - f, e + g)), "%s%s" % (F, B(c + f, e + g)) if (c + f) or (e + g) else "%s" % F, "%s²%s" % (F, B(c - f, e - g)) if c - f or e - g else F]
    else:
        q = "%s² + %s%s" % (F, F, B(c, e))
        r = "%s%s" % (F, B(a + c, b + e)) if (a + c, b + e) != (0, 0) else None
        w = ["%s%s" % (F, B(c, e)), "%s²%s" % (F, B(c, e)), "%s%s" % (F, B(a + c + 1, b + e))]
    if r is None or "(0)" in r or any("(0)" in x for x in w):
        return None
    return M("Factorise : %s" % q, r, w, "%s est un facteur commun : on le met devant, et on regroupe le reste : <b>%s</b>." % (F, r))


def s4():
    k = R.choice(["demo", "demo", "test", "contre"])
    if k == "demo":
        a, b = nz(1, 9), nz(1, 9)
        lhs = "(x + %d)(x + %d) − x²" % (a, b)
        rhs = E((a + b, "x"), (a * b, ""))
        return M("Pour démontrer que, pour tout nombre x, %s = %s, que faut-il faire ?" % (lhs, rhs), "développer et réduire le membre de gauche pour obtenir %s" % rhs,
                 ["vérifier l’égalité pour x = 1 et x = 2", "remplacer x par 0", "c’est impossible à démontrer"], "Un calcul littéral valable pour tout x est une <b>démonstration</b> ; des exemples ne suffisent pas.")
    if k == "test":
        a, b = nz(-5, 5), nz(-5, 5)
        x = R.randint(-3, 4)
        A = (x + a) * (x + b)
        return M("Pour x = %s, que vaut (x %s %d)(x %s %d) ?" % (d(x), "+" if a > 0 else MINUS, abs(a), "+" if b > 0 else MINUS, abs(b)), d(A), [d(x * x + a * b), d((x + a) + (x + b)), d(x * x + (a + b) * x - a * b) if a * b else d(A + 1)],
                 "(%s %s %d) × (%s %s %d) = %s × %s = <b>%s</b>." % (par(x), "+" if a > 0 else MINUS, abs(a), par(x), "+" if b > 0 else MINUS, abs(b), par(x + a), par(x + b), d(A)))
    a = R.randint(1, 6)
    return M("Léa affirme : « (x + %d)² = x² + %d pour tout x ». Avec x = 1, que trouve-t-on ?" % (a, a * a), "%d ≠ %d : l’affirmation est fausse" % ((1 + a) ** 2, 1 + a * a),
             ["%d = %d : l’affirmation est vraie" % ((1 + a) ** 2, (1 + a) ** 2), "on ne peut pas conclure avec un exemple", "%d ≠ %d : l’affirmation est vraie" % ((1 + a) ** 2, 1 + a * a)],
             "(1 + %d)² = %d et 1 + %d = %d : un seul <b>contre-exemple</b> suffit à montrer que c’est faux." % (a, (1 + a) ** 2, a * a, 1 + a * a))


def s5():
    k = R.choice(["aire", "aire", "cadre", "prog"])
    a, b = R.randint(1, 9), R.randint(1, 9)
    if k == "aire":
        return M("Un rectangle a pour dimensions 2x + %d et x + %d. Quelle est son aire, développée et réduite ?" % (a, b), E((2, "x²"), (2 * b + a, "x"), (a * b, "")), [E((2, "x²"), (a * b, "")), E((3, "x"), (a + b, "")), E((2, "x²"), (a + b, "x"), (a * b, ""))],
                 "(2x + %d)(x + %d) = 2x² + %dx + %dx + %d = <b>%s</b>." % (a, b, 2 * b, a, a * b, E((2, "x²"), (2 * b + a, "x"), (a * b, ""))))
    if k == "cadre":
        c = R.randint(10, 30)
        return M("Un carré de côté x + %d contient un carré de côté x. Quelle expression réduite donne l’aire de la bande entre les deux ?" % a, E((2 * a, "x"), (a * a, "")), [E((a * a, "")), E((2 * a, "x")), E((1, "x²"), (a * a, ""))],
                 "(x + %d)² − x² = x² + %dx + %d − x² = <b>%s</b>." % (a, 2 * a, a * a, E((2 * a, "x"), (a * a, ""))))
    return M("Programme : « Choisis x. Calcule (x + %d)(x − %d). Ajoute %d. » Quelle expression simplifiée obtient-on ?" % (a, a, a * a), "x²", [E((1, "x²"), (2 * a * a, "")), E((1, "x²"), (-2 * a * a, "")), E((1, "x²"), (2 * a, "x"))],
             "(x + %d)(x − %d) = x² − %d ; + %d donne <b>x²</b> : le programme donne toujours le carré du nombre choisi." % (a, a, a * a, a * a))


def main():
    seen = set()
    sets = [("Double distributivité", mix(R, seen, [(s1, 20)])), ("Sommes et différences de produits", mix(R, seen, [(s2, 20)])),
            ("Factoriser par un facteur commun", mix(R, seen, [(s3, 20)])), ("Démontrer ou tester", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["(a + b)(c + d) = ac + ad + bc + bd : chaque terme de la première parenthèse multiplie chaque terme de la seconde.",
              "Un signe « − » devant un produit change tous les signes du développement de ce produit.",
              "Factoriser : on repère un <b>facteur commun</b> (souvent une parenthèse) : k × A + k × B = k(A + B)."],
             [("(x + 3)(2x − 1) + (x + 3)(x + 5)", ["facteur commun : (x + 3)", "(x + 3)[(2x − 1) + (x + 5)]"], "(x + 3)(3x + 4)")],
             [["(x + 2)(x − 5) = x² − 10", "Il manque −5x + 2x : x² − 3x − 10."], ["A − (x + 1)(x − 2) = A − x² − x − 2", "Tous les signes changent : A − x² + x + 2."],
              ["Démontrer avec un exemple", "Un exemple peut seulement montrer qu’une égalité est fausse (contre-exemple)."]])
    faq = [("Comment vérifier une factorisation ?", "On redéveloppe le résultat : on doit retrouver l’expression de départ."),
           ("Quand factoriser plutôt que développer ?", "Pour résoudre une équation produit nul ou simplifier un calcul, on factorise ; pour réduire ou comparer, on développe.")]
    unit("3e", R, "developper-et-factoriser", "A",
         "Développer et réduire des expressions avec la double distributivité, y compris des sommes et différences de produits ; factoriser par un facteur commun ; démontrer une égalité ou utiliser un contre-exemple",
         "Développer et factoriser", "Développer et factoriser",
         "Fiches de maths 3e sur le calcul littéral : double distributivité, différences de produits, factoriser par un facteur commun, démontrer et contre-exemple. 100 exercices corrigés.",
         "(a + b)(c + d) = ac + ad + bc + bd", "kA + kB = k(A + B)", body, faq, sets, 4)


if __name__ == "__main__":
    main()
