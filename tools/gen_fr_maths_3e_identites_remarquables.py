# -*- coding: utf-8 -*-
"""
France Maths 3e : Identités remarquables
  python3 tools/gen_fr_maths_3e_identites_remarquables.py
Erreurs : (a + b)² = a² + b², oublier le double produit, (a − b)² = a² − b², (2x)² = 2x².
"""
import random
from fr_c4 import *

R = random.Random(60405)
K = Kids(R)


def E(*t):
    return expr(list(t))


def s1():
    a, b = R.randint(1, 6), R.randint(1, 12)
    k = R.choice(["plus", "moins", "diff"])
    ax = E((a, "x"))
    if k == "plus":
        r = E((a * a, "x²"), (2 * a * b, "x"), (b * b, ""))
        return M("Développe : (%s + %d)²" % (ax, b), r, [E((a * a, "x²"), (b * b, "")), E((a * a, "x²"), (a * b, "x"), (b * b, "")), E((a, "x²"), (2 * a * b, "x"), (b * b, "")) if a > 1 else E((1, "x²"), (2 * b, "x"), (2 * b, ""))],
                 "(a + b)² = a² + 2ab + b² : %s² + 2 × %s × %d + %d² = <b>%s</b>." % ("(%s)" % ax if a > 1 else ax, ax, b, b, r))
    if k == "moins":
        r = E((a * a, "x²"), (-2 * a * b, "x"), (b * b, ""))
        return M("Développe : (%s − %d)²" % (ax, b), r, [E((a * a, "x²"), (-b * b, "")), E((a * a, "x²"), (2 * a * b, "x"), (b * b, "")), E((a * a, "x²"), (-2 * a * b, "x"), (-b * b, ""))],
                 "(a − b)² = a² − 2ab + b² : <b>%s</b>." % r)
    r = E((a * a, "x²"), (-b * b, ""))
    return M("Développe : (%s + %d)(%s − %d)" % (ax, b, ax, b), r, [E((a * a, "x²"), (b * b, "")), E((a * a, "x²"), (-2 * a * b, "x"), (-b * b, "")), E((a, "x²"), (-b * b, "")) if a > 1 else E((1, "x²"), (-2 * b, ""))],
             "(a + b)(a − b) = a² − b² : <b>%s</b>." % r)


def s2():
    a, b = R.randint(1, 6), R.randint(1, 12)
    k = R.choice(["diff", "diff", "plus", "moins"])
    ax = E((a, "x"))
    if k == "diff":
        q = E((a * a, "x²"), (-b * b, ""))
        r = "(%s + %d)(%s − %d)" % (ax, b, ax, b)
        return M("Factorise : %s" % q, r, ["(%s − %d)²" % (ax, b), "(%s + %d)²" % (ax, b), "(%s − %d)(%s + %d)" % (E((a * a, "x")), b, ax, b) if a > 1 else "(x + %d)(x − %d)" % (b * b, b * b)],
                 "a² − b² = (a + b)(a − b) avec a = %s et b = %d : <b>%s</b>." % (ax, b, r))
    if k == "plus":
        q = E((a * a, "x²"), (2 * a * b, "x"), (b * b, ""))
        return M("Factorise : %s" % q, "(%s + %d)²" % (ax, b), ["(%s + %d)(%s − %d)" % (ax, b, ax, b), "(%s − %d)²" % (ax, b), "(%s + %d)²" % (ax, b * b)],
                 "On reconnaît a² + 2ab + b² avec a = %s et b = %d : <b>(%s + %d)²</b>." % (ax, b, ax, b))
    q = E((a * a, "x²"), (-2 * a * b, "x"), (b * b, ""))
    return M("Factorise : %s" % q, "(%s − %d)²" % (ax, b), ["(%s + %d)²" % (ax, b), "(%s + %d)(%s − %d)" % (ax, b, ax, b), "(%s − %d)²" % (ax, b * b)],
             "On reconnaît a² − 2ab + b² : <b>(%s − %d)²</b>." % (ax, b))


def s3():
    k = R.choice(["carre", "carre", "diff", "moins"])
    if k == "carre":
        n = R.choice([101, 102, 103, 1001, 51, 21, 31, 41, 201])
        b = n % 10 if n < 100 else n - (n // 100) * 100
        a = n - b
        return M("Calcule mentalement %s² avec une identité remarquable." % num(n), num(n * n), [num(a * a + b * b), num(a * a + a * b + b * b), num(n * n + 1)],
                 "(%s + %d)² = %s + 2 × %s × %d + %d = <b>%s</b>." % (num(a), b, num(a * a), num(a), b, b * b, num(n * n)))
    if k == "moins":
        n = R.choice([99, 98, 49, 39, 29, 999, 199])
        a = (n // 10 + 1) * 10 if n < 100 else (n // 100 + 1) * 100
        b = a - n
        return M("Calcule mentalement %s² avec une identité remarquable." % num(n), num(n * n), [num(a * a - b * b), num(a * a - a * b + b * b), num(n * n - 1)],
                 "(%s − %d)² = %s − 2 × %s × %d + %d = <b>%s</b>." % (num(a), b, num(a * a), num(a), b, b * b, num(n * n)))
    a = R.choice([100, 50, 30, 40, 1000, 20])
    b = R.randint(1, 5)
    return M("Calcule mentalement %s × %s." % (num(a + b), num(a - b)), num(a * a - b * b), [num(a * a + b * b), num(a * a), num(a * a - 2 * b)],
             "(%s + %d)(%s − %d) = %s − %d = <b>%s</b>." % (num(a), b, num(a), b, num(a * a), b * b, num(a * a - b * b)))


def s4():
    k = R.choice(["diffex", "diffex", "facto", "eq"])
    a, b = R.randint(1, 9), R.randint(1, 9)
    if k == "diffex":
        r = E((4 * a, "x"))
        return M("Développe et réduis : (x + %d)² − (x − %d)²" % (a, a), r, ["0", E((2 * a * a, "")), E((2, "x²"), (2 * a * a, ""))],
                 "(x² + %dx + %d) − (x² − %dx + %d) = <b>%s</b>." % (2 * a, a * a, 2 * a, a * a, r))
    if k == "facto":
        return M("Factorise : (x + %d)² − %d" % (a, b * b), "(x + %d)(x + %d)" % (a + b, a - b) if a != b else "x(x + %d)" % (2 * a), ["(x + %d)²" % (a - b) if a != b else "(x + %d)²" % a, "(x + %d − %d)²" % (a, b), "(x + %d)(x + %d)" % (a + b, a + b)],
                 "a² − b² avec a = x + %d et b = %d : (x + %d + %d)(x + %d − %d) = <b>%s</b>." % (a, b, a, b, a, b, "(x + %d)(x + %d)" % (a + b, a - b) if a != b else "x(x + %d)" % (2 * a))) if a > b else None
    a = R.randint(2, 12)
    return M("Résous x² − %d = 0 en factorisant." % (a * a), "x = %d ou x = −%d" % (a, a), ["x = %d" % a, "x = %d ou x = −%d" % (a * a, a * a), "pas de solution"],
             "x² − %d = (x − %d)(x + %d) = 0 : un produit est nul si l’un des facteurs est nul : <b>x = %d ou x = −%d</b>." % (a * a, a, a, a, a))


def s5():
    k = R.choice(["aire", "aire", "nombres", "demo"])
    a = R.randint(1, 9)
    if k == "aire":
        return M("On agrandit chaque côté d’un carré de côté x de %d cm. De combien l’aire augmente-t-elle ?" % a, E((2 * a, "x"), (a * a, "")) + " cm²", [str(a * a) + " cm²", E((2 * a, "x")) + " cm²", E((a, "x"), (a * a, "")) + " cm²"],
                 "(x + %d)² − x² = x² + %dx + %d − x² = <b>%s cm²</b>." % (a, 2 * a, a * a, E((2 * a, "x"), (a * a, ""))))
    if k == "nombres":
        n = R.randint(3, 40)
        return M("Calcule (%d + 1)² − %d² sans calculatrice." % (n, n), str(2 * n + 1), ["1", str(2 * n), str(n + 1)],
                 "(n + 1)² − n² = 2n + 1 = 2 × %d + 1 = <b>%d</b>." % (n, 2 * n + 1))
    V = [("Pour tout entier n, (n + 1)² − n² est…", "toujours impair", ["toujours pair", "toujours égal à 1", "toujours un carré"]),
         ("Pour tout nombre n, (n − 1)(n + 1) + 1 est égal à…", "n²", ["n² − 1", "2n", "n² + 2"]),
         ("Quelle égalité est fausse pour certains nombres ?", "(a + b)² = a² + b²", ["(a + b)² = a² + 2ab + b²", "(a − b)(a + b) = a² − b²", "(a − b)² = a² − 2ab + b²"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Développer avec les identités", mix(R, seen, [(s1, 20)])), ("Factoriser avec les identités", mix(R, seen, [(s2, 20)])),
            ("Calcul mental", mix(R, seen, [(s3, 20)])), ("Calculs plus complexes", mix(R, seen, [(s4, 20)])), ("Problèmes et démonstrations", mix(R, seen, [(s5, 20)]))]
    body = L(["(a + b)² = a² + 2ab + b²",
              "(a − b)² = a² − 2ab + b²",
              "(a + b)(a − b) = a² − b². Lues de droite à gauche, ces égalités servent à <b>factoriser</b>."],
             [("(3x − 5)²", ["a = 3x, b = 5", "(3x)² − 2 × 3x × 5 + 5²"], "9x² − 30x + 25"), ("49 − x²", ["7² − x²"], "(7 + x)(7 − x)")],
             [["(a + b)² = a² + b²", "Il manque le double produit 2ab."], ["(3x)² = 3x²", "(3x)² = 9x²."], ["(a − b)² = a² − b²", "(a − b)² = a² − 2ab + b²."]])
    faq = [("Comment reconnaître a² − b² ?", "Deux carrés séparés par un signe − : x² − 25, 4x² − 9, (x + 1)² − 16."),
           ("À quoi servent les identités remarquables ?", "À développer et factoriser plus vite, à calculer mentalement (99² = (100 − 1)²) et à résoudre des équations.")]
    unit("3e", R, "identites-remarquables", "A",
         "Connaître et utiliser les identités remarquables (a + b)², (a − b)² et (a + b)(a − b) pour développer, factoriser, calculer mentalement et démontrer",
         "Identités remarquables", "Identités remarquables",
         "Fiches de maths 3e sur les identités remarquables : développer (a + b)², (a − b)², (a + b)(a − b), factoriser, calcul mental et démonstrations. 100 exercices corrigés.",
         "(a + b)² = a² + 2ab + b²", "a² − b² = (a + b)(a − b)", body, faq, sets, 5)


if __name__ == "__main__":
    main()
