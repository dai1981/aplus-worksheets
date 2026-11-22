# -*- coding: utf-8 -*-
"""
France Maths 4e : Développer, réduire et factoriser
  python3 tools/gen_fr_maths_4e_developper_et_factoriser.py
Distributivité simple k(a + b), suppression de parenthèses, double distributivité (a + b)(c + d), factorisation par un facteur commun.
Erreurs : 3(x + 2) = 3x + 2, −(x − 4) = −x − 4, (x + 2)(x + 3) = x² + 6, 2x × 3x = 6x.
"""
import random
from fr_c4 import *

R = random.Random(60305)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    k = nz(-9, 9)
    a, b = nz(-9, 9), nz(-9, 9)
    v = R.choice(["x", "y", "a"])
    if R.random() < 0.5:
        q = "%s(%s)" % (d(k) if k != -1 else MINUS, E((a, v), (b, "")))
        if k == 1:
            return None
    else:
        q = "%s × (%s)" % (par(k), E((a, v), (b, "")))
    r = E((k * a, v), (k * b, ""))
    return M("Développe : %s" % q, r, [E((k * a, v), (b, "")), E((k * a, v), (-k * b, "")), E((k + a, v), (k + b, ""))],
             "On distribue %s à chaque terme : %s × %s + %s × %s = <b>%s</b>." % (d(k), par(k), E((a, v)), par(k), par(b), r))


def s2():
    k = R.choice(["moins", "plus", "reduire", "reduire"])
    a, b = nz(-9, 9), nz(-9, 9)
    if k == "moins":
        c = R.randint(1, 9)
        inner = E((a, "x"), (b, ""))
        base = R.randint(2, 9)
        res = E((base - a, "x"), (-b, "")) if base != a else E((-b, ""))
        return M("Supprime les parenthèses et réduis : %dx − (%s)" % (base, inner), res, [E((base - a, "x"), (b, "")), E((base + a, "x"), (b, "")), E((base - a, "x"))],
                 "Un signe − devant des parenthèses change le signe de chaque terme : %s = <b>%s</b>." % (E((base, "x"), (-a, "x"), (-b, "")), res))
    if k == "plus":
        base = R.randint(1, 9)
        return M("Supprime les parenthèses et réduis : %d + (%s)" % (base, E((a, "x"), (b, ""))), E((a, "x"), (base + b, "")), [E((a, "x"), (base - b, "")), E((a + base, "x"), (b, "")) if True else "", E((a, "x"), (base * b, ""))],
                 "Un signe + devant des parenthèses ne change rien : <b>%s</b>." % E((a, "x"), (base + b, "")))
    c, e = nz(-9, 9), nz(-9, 9)
    q = "%s %s" % (E((a, "x²"), (b, "x"), (c, "")), "+ " + E((e, "x"), (b, "x²")) if e > 0 else MINUS + " " + E((-e, "x"), (-b, "x²")))
    r = E((a + b, "x²"), (b + e, "x"), (c, ""))
    if a + b == 0 or b + e == 0:
        return None
    return M("Réduis : %s" % q, r, [E((a + b + b + e, "x²"), (c, "")), E((a + b, "x²"), (b - e, "x"), (c, "")) if b - e != b + e else E((a + b, "x⁴"), (b + e, "x"), (c, "")), E((a + 2 * b + e + c, "x"))],
             "On regroupe les termes de même nature (x² avec x², x avec x) : <b>%s</b>." % r)


def s3():
    a, b, c, e = nz(-7, 9), nz(-9, 9), nz(-7, 9), nz(-9, 9)
    if R.random() < 0.6:
        a, c = 1, 1
    r = E((a * c, "x²"), (a * e + b * c, "x"), (b * e, ""))
    f1, f2 = E((a, "x"), (b, "")), E((c, "x"), (e, ""))
    return M("Développe et réduis : (%s)(%s)" % (f1, f2), r, [E((a * c, "x²"), (b * e, "")), E((a * c, "x²"), (a * e - b * c, "x"), (b * e, "")) if a * e - b * c != a * e + b * c else E((a * c, "x²"), (a * e + b * c, "x"), (-b * e, "")), E((a + c, "x"), (b + e, ""))],
             "Chaque terme de la première parenthèse multiplie chaque terme de la seconde : %s %s %s %s, puis on réduit : <b>%s</b>." % (E((a * c, "x²")), "+ " + E((a * e, "x")) if a * e > 0 else MINUS + " " + E((-a * e, "x")), "+ " + E((b * c, "x")) if b * c > 0 else MINUS + " " + E((-b * c, "x")), "+ " + d(b * e) if b * e > 0 else MINUS + " " + d(-b * e), r))


def s4():
    k = nz(2, 9)
    a, b = nz(-9, 9), nz(-9, 9)
    from math import gcd
    a = abs(a)
    if gcd(abs(a), abs(b)) != 1:
        return None
    kind = R.choice(["num", "num", "x", "xpart"])
    if kind == "num":
        q = E((k * a, "x"), (k * b, ""))
        r = "%d(%s)" % (k, E((a, "x"), (b, "")))
        return M("Factorise : %s" % q, r, ["%d(%s)" % (k, E((k * a, "x"), (b, ""))), "%d(%s)" % (k, E((a, "x"), (b, ""))) + "x", "%dx(%s)" % (k, E((a, ""), (b, "")))],
                 "%d est un facteur commun : %s = %d × %s + %d × %s = <b>%s</b>." % (k, q, k, E((a, "x")), k, par(b), r))
    if kind == "x":
        q = E((a, "x²"), (b, "x"))
        r = "x(%s)" % E((a, "x"), (b, ""))
        return M("Factorise : %s" % q, r, ["x(%s)" % E((a, "x²"), (b, "")), "x²(%s)" % E((a, ""), (b, "")), "%s(x + 1)" % E((a + b, "x"))],
                 "x est un facteur commun : <b>%s</b>." % r)
    v = R.choice(["(x + 1)", "(x − 2)", "(2x + 3)", "(x + 5)"])
    c = nz(2, 9)
    q = "%d%s + %dx%s" % (c, v, k, v)
    r = "%s(%s)" % (v, E((k, "x"), (c, "")))
    return M("Factorise : %s" % q, r, ["%s(%s)" % (v, E((k * c, "x"))), "%s²(%s)" % (v, E((k, "x"), (c, ""))), "%d%s" % (c + k, v)],
             "%s est un facteur commun : <b>%s</b>." % (v, r))


def s5():
    k = R.choice(["aire", "aire2", "verif", "perim", "astuce"])
    a, b = R.randint(1, 9), R.randint(1, 9)
    if k == "aire":
        return M("Un rectangle a pour longueur x + %d et pour largeur %d. Quelle expression développée donne son aire ?" % (a, b), E((b, "x"), (a * b, "")), [E((b, "x"), (a, "")), E((1, "x"), (a + b, "")), E((2, "x"), (2 * a + 2 * b, ""))],
                 "Aire = %d(x + %d) = <b>%s</b>." % (b, a, E((b, "x"), (a * b, ""))))
    if k == "aire2":
        return M("Un rectangle a pour dimensions x + %d et x + %d. Quelle est son aire, développée et réduite ?" % (a, b), E((1, "x²"), (a + b, "x"), (a * b, "")), [E((1, "x²"), (a * b, "")), E((2, "x"), (a + b, "")), E((1, "x²"), (a * b, "x"), (a + b, ""))],
                 "(x + %d)(x + %d) = x² + %dx + %dx + %d = <b>%s</b>." % (a, b, b, a, a * b, E((1, "x²"), (a + b, "x"), (a * b, ""))))
    if k == "verif":
        x = R.randint(2, 6)
        c = R.randint(2, 5)
        return M("Pour vérifier que %d(x + %d) = %dx + %d, on teste x = %d. Que vaut chaque membre ?" % (c, a, c, c * a, x), "%d et %d : l’égalité est vérifiée" % (c * (x + a), c * x + c * a),
                 ["%d et %d : l’égalité est fausse" % (c * x + a, c * x + c * a), "%d et %d" % (c * (x + a), c * x + a), "on ne peut pas tester avec un nombre"],
                 "%d × (%d + %d) = %d et %d × %d + %d = %d : <b>l’égalité est vérifiée</b>." % (c, x, a, c * (x + a), c, x, c * a, c * x + c * a))
    if k == "perim":
        return M("Un rectangle a pour dimensions 2x + %d et x − 1 (x &gt; 1). Quelle expression réduite donne son périmètre ?" % a, E((6, "x"), (2 * a - 2, "")), [E((3, "x"), (a - 1, "")), E((6, "x"), (2 * a + 2, "")), E((2, "x²"), (a - 2, "x"), (-a, ""))],
                 "Périmètre = 2 × (2x + %d + x − 1) = 2 × (%s) = <b>%s</b>." % (a, E((3, "x"), (a - 1, "")), E((6, "x"), (2 * a - 2, ""))))
    n = R.randint(21, 99)
    m = R.choice([99, 101, 98, 102])
    return M("En utilisant (a + b)(c + d) ou k(a + b), calcule astucieusement %d × %d." % (n, m), num(n * m), [num(n * 100 + (m - 100)), num(n * (m - 100) + 100), num(n * 100)],
             "%d × (100 %s %d) = %s %s %d = <b>%s</b>." % (n, "+" if m > 100 else MINUS, abs(m - 100), num(n * 100), "+" if m > 100 else MINUS, n * abs(m - 100), num(n * m)))


def main():
    seen = set()
    sets = [("Développer k(a + b)", mix(R, seen, [(s1, 20)])), ("Supprimer les parenthèses et réduire", mix(R, seen, [(s2, 20)])),
            ("Double distributivité", mix(R, seen, [(s3, 20)])), ("Factoriser", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Développer</b>, c’est transformer un produit en somme : k(a + b) = ka + kb et (a + b)(c + d) = ac + ad + bc + bd.",
              "<b>Réduire</b>, c’est regrouper les termes de même nature : 3x + 5x = 8x, mais 3x + 5x² ne se réduit pas.",
              "<b>Factoriser</b>, c’est l’inverse : on repère un facteur commun. 6x + 9 = 3(2x + 3)."],
             [("(x + 2)(x − 5)", ["x × x + x × (−5) + 2 × x + 2 × (−5)", "x² − 5x + 2x − 10"], "x² − 3x − 10")],
             [["3(x + 2) = 3x + 2", "On multiplie chaque terme : 3x + 6."], ["−(x − 4) = −x − 4", "Le signe − change tous les signes : −x + 4."],
              ["(x + 2)(x + 3) = x² + 6", "Il manque les termes du milieu : x² + 3x + 2x + 6 = x² + 5x + 6."]])
    faq = [("Comment vérifier un développement ?", "On remplace x par un nombre (par exemple 2) dans les deux expressions : elles doivent donner le même résultat."),
           ("Quelle est la différence entre 2x et x² ?", "2x = x + x, alors que x² = x × x. Pour x = 3 : 2x = 6 et x² = 9.")]
    unit("4e", R, "developper-et-factoriser", "A",
         "Développer une expression avec la distributivité simple et la double distributivité ; supprimer des parenthèses précédées d’un signe + ou − ; réduire une expression ; factoriser par un facteur commun",
         "Développer, réduire et factoriser", "Développer et factoriser",
         "Fiches de maths 4e sur le calcul littéral : développer k(a + b), double distributivité, réduire, supprimer des parenthèses et factoriser. 100 exercices corrigés.",
         "Développer : k(a + b) = ka + kb", "Factoriser : ka + kb = k(a + b)", body, faq, sets, 5)


if __name__ == "__main__":
    main()
