# -*- coding: utf-8 -*-
"""
France Maths Seconde : Puissances et racines carrées
  python3 tools/gen_fr_maths_seconde_puissances_et_racines_carrees.py
Erreurs : (a²)³ = a⁵, 2³ × 3³ = 6⁹, √(a + b) = √a + √b, √((−3)²) = −3, √50 = 25√2.
"""
import random
import math
from fr_c4 import *

R = random.Random(60504)
K = Kids(R)


def sup(n):
    return "<sup>%s</sup>" % d(n)


def P(a, n):
    return "%s%s" % (a, sup(n)) if n != 1 else a


def s1():
    a = R.choice(["a", "x", "b", "y"])
    m, n = R.randint(-5, 6), R.randint(-5, 6)
    p = R.randint(2, 4)
    k = R.choice(["prod", "quot", "pow", "mix"])
    if k == "prod":
        return M("Simplifie : %s × %s" % (P(a, m), P(a, n)), P(a, m + n), [P(a, m * n), P(a, m - n) if m - n != m + n else P(a, m + n + 1), "%s%s" % (a, sup(m + n + 2))],
                 "On additionne les exposants : <b>%s</b>." % P(a, m + n))
    if k == "quot":
        if m == n:
            return None
        return M("Simplifie : %s" % fr(P(a, m), P(a, n)), P(a, m - n), [P(a, m + n) if m + n != m - n else P(a, m - n + 1), P(a, n - m), P(a, m * n) if m * n not in (m - n, m + n, n - m) else P(a, m - n + 2)],
                 "On soustrait les exposants : %s − %s = %s : <b>%s</b>." % (d(m), par(n), d(m - n), P(a, m - n)))
    if k == "pow":
        if m in (0, 1):
            return None
        return M("Simplifie : (%s)%s" % (P(a, m), sup(p)), P(a, m * p), [P(a, m + p), P(a, m ** p) if m ** p != m * p else P(a, m * p + 1), P(a, m * p - 1)],
                 "On multiplie les exposants : <b>%s</b>." % P(a, m * p))
    c = R.randint(2, 5)
    e = c ** p
    return M("Simplifie : (%d%s)%s" % (c, a, sup(p)), "%d%s" % (e, P(a, p)), ["%d%s" % (c, P(a, p)), "%d%s" % (c * p, P(a, p)), "%d%s" % (e, a)],
             "(ka)<sup>n</sup> = k<sup>n</sup>a<sup>n</sup> : %d%s = %d, donc <b>%d%s</b>." % (c, sup(p), e, e, P(a, p)))


def s2():
    k = R.choice(["num", "num", "neg", "frac"])
    if k == "num":
        a, b = R.choice([(2, 3), (2, 5), (3, 5), (2, 7)])
        m, n = R.randint(1, 4), R.randint(1, 4)
        e = R.randint(1, 3)
        v = Fr(a ** m * b ** n * (a * b) ** e)
        return M("Écris sous la forme %d<sup>p</sup> × %d<sup>q</sup> : %s × %s × %s" % (a, b, P(str(a), m), P(str(b), n), P(str(a * b), e)), "%s × %s" % (P(str(a), m + e), P(str(b), n + e)),
                 ["%s × %s" % (P(str(a), m), P(str(b), n + e)), "%s × %s" % (P(str(a), m * e), P(str(b), n * e)) if m * e != m + e or n * e != n + e else "%s × %s" % (P(str(a), m + e + 1), P(str(b), n + e)), "%s" % P(str(a * b), m + n + e)],
                 "%s = %s × %s, puis on additionne les exposants : <b>%s × %s</b>." % (P(str(a * b), e), P(str(a), e), P(str(b), e), P(str(a), m + e), P(str(b), n + e)))
    if k == "neg":
        a, n = R.randint(2, 5), R.randint(1, 3)
        return M("Écris sous forme de fraction : %s" % P(str(a), -n), fq(Fr(1, a ** n)), [d(-a ** n), fq(Fr(-1, a * n)), fq(Fr(1, a * n)) if a * n != a ** n else d(-a * n)],
                 "a<sup>−n</sup> = 1 ÷ a<sup>n</sup> : <b>%s</b>." % fq(Fr(1, a ** n)))
    a, b, n = R.randint(2, 5), R.randint(2, 7), R.randint(2, 3)
    if math.gcd(a, b) != 1:
        return None
    return M("Calcule : (%s)%s" % (fr(a, b), sup(n)), fq(Fr(a ** n, b ** n)), [fq(Fr(a ** n, b)), fq(Fr(a * n, b * n)) if Fr(a * n, b * n) != Fr(a ** n, b ** n) else fq(Fr(a, b ** n)), fq(Fr(b ** n, a ** n))],
             "On élève numérateur et dénominateur : <b>%s</b>." % fq(Fr(a ** n, b ** n)))


def s3():
    k = R.choice(["simpl", "simpl", "simpl", "abs"])
    if k == "simpl":
        c = R.choice([2, 3, 4, 5, 6, 7, 10])
        r = R.choice([2, 3, 5, 6, 7])
        n = c * c * r
        return M("Écris √%d sous la forme a√b avec b entier le plus petit possible." % n, "%d√%d" % (c, r), ["%d√%d" % (c * c, r), "%d√%d" % (r, c * c) if r != c * c else "%d√%d" % (c, r * 2), "%d√%d" % (c * r, c)],
                 "√%d = √(%d × %d) = √%d × √%d = <b>%d√%d</b>." % (n, c * c, r, c * c, r, c, r))
    x = R.choice([-2, -3, -5, -7, -11])
    return M("Calcule √((%s)²)." % d(x), d(-x), [d(x), d(x * x), "elle n’existe pas"], "√(a²) = |a| : |%s| = <b>%s</b>." % (d(x), d(-x)))


def s4():
    k = R.choice(["somme", "prod", "dev", "cmp"])
    if k == "somme":
        r = R.choice([2, 3, 5])
        a, b = R.randint(1, 4), R.randint(1, 4)
        x, y = a * a * r, b * b * r
        return M("Simplifie : √%d + √%d" % (x, y), "%d√%d" % (a + b, r), ["√%d" % (x + y), "%d√%d" % (a * b, r), "%d√%d" % (a + b, 2 * r)],
                 "√%d = %s√%d et √%d = %s√%d : <b>%d√%d</b>." % (x, a if a > 1 else "", r, y, b if b > 1 else "", r, a + b, r))
    if k == "prod":
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (6, 24), (2, 50)])
        return M("Calcule : √%d × √%d" % (a, b), str(math.isqrt(a * b)), ["√%d" % (a + b), str(a * b), "%d√2" % math.isqrt(a * b)], "√a × √b = √(ab) = √%d = <b>%d</b>." % (a * b, math.isqrt(a * b)))
    if k == "dev":
        a = R.choice([2, 3, 5, 7])
        b = R.randint(1, 5)
        return M("Développe et réduis : (√%d + %d)(√%d − %d)" % (a, b, a, b), d(a - b * b), [d(a + b * b), d(a - b), "%d − %d√%d" % (a, b, a)],
                 "(x + y)(x − y) = x² − y² : %d − %d = <b>%s</b>." % (a, b * b, d(a - b * b)))
    a, b = R.randint(2, 30), R.randint(2, 30)
    if a == b:
        return None
    return M("Compare √%d + √%d et √%d." % (a, b, a + b), "√%d + √%d &gt; √%d" % (a, b, a + b), ["√%d + √%d = √%d" % (a, b, a + b), "√%d + √%d &lt; √%d" % (a, b, a + b), "on ne peut pas comparer"],
             "Pour a, b &gt; 0, √(a + b) &lt; √a + √b (on compare les carrés : a + b &lt; a + b + 2√(ab)).")


def s5():
    k = R.choice(["carre", "bact", "diag", "sci"])
    if k == "carre":
        c = R.choice([2, 3, 4, 5])
        r = R.choice([2, 3, 5])
        return M("Un carré a une aire de %d cm². Donne la valeur exacte de son côté sous la forme a√b." % (c * c * r), "%d√%d cm" % (c, r), ["%d√%d cm" % (c * c, r), "%s cm" % d(Fr(c * c * r, 4)), "%d√%d cm" % (r, c)],
                 "Côté = √%d = <b>%d√%d cm</b>." % (c * c * r, c, r))
    if k == "bact":
        n = R.randint(3, 10)
        return M("Une population de bactéries double toutes les heures. Au départ, il y en a 1 000. Combien y en a-t-il après %d heures ?" % n, num(1000 * 2 ** n), [num(1000 * 2 * n), num(1000 + 2 ** n), num(1000 * 2 ** (n - 1))],
                 "1 000 × 2<sup>%d</sup> = <b>%s</b>." % (n, num(1000 * 2 ** n)))
    if k == "diag":
        c = R.randint(2, 9)
        return M("Quelle est la valeur exacte de la diagonale d’un carré de côté %d cm ?" % c, "%d√2 cm" % c, ["%d cm" % (2 * c), "√%d cm" % (2 * c), "%d√2 cm" % (2 * c)],
                 "d² = %d² + %d² = %d, donc d = √%d = <b>%d√2 cm</b>." % (c, c, 2 * c * c, 2 * c * c, c))
    a = R.choice([2, 3, 4, 5])
    e = R.randint(2, 8)
    return M("Calcule (%d × 10%s)² et écris le résultat en notation scientifique." % (a, sup(e)), "%s × 10%s" % (d(a * a if a * a < 10 else Fr(a * a, 10)), sup(2 * e if a * a < 10 else 2 * e + 1)),
             ["%d × 10%s" % (a * a, sup(e * e)) if a * a < 10 else "%d × 10%s" % (a * a, sup(2 * e)), "%d × 10%s" % (2 * a, sup(2 * e)) if 2 * a < 10 else "%s × 10%s" % (d(Fr(2 * a, 10)), sup(2 * e + 1)), "%s × 10%s" % (d(a * a if a * a < 10 else Fr(a * a, 10)), sup(e + 2))],
             "%d² = %d et (10%s)² = 10%s : <b>%s × 10%s</b>." % (a, a * a, sup(e), sup(2 * e), d(a * a if a * a < 10 else Fr(a * a, 10)), sup(2 * e if a * a < 10 else 2 * e + 1)))


def main():
    seen = set()
    sets = [("Règles de calcul", mix(R, seen, [(s1, 20)])), ("Puissances de nombres", mix(R, seen, [(s2, 20)])),
            ("Simplifier une racine carrée", mix(R, seen, [(s3, 20)])), ("Calculs avec des racines", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["aᵐ × aⁿ = aᵐ⁺ⁿ ; aᵐ ÷ aⁿ = aᵐ⁻ⁿ ; (aᵐ)ⁿ = aᵐˣⁿ ; (ab)ⁿ = aⁿbⁿ ; a⁻ⁿ = 1/aⁿ.",
              "Pour a, b ⩾ 0 : √(ab) = √a × √b et √(a²) = a ; pour tout réel a, √(a²) = |a|. Mais √(a + b) ≠ √a + √b.",
              "Simplifier √n : on cherche le plus grand carré qui divise n (√72 = √(36 × 2) = 6√2)."],
             [("√45 + √20", ["√45 = 3√5", "√20 = 2√5"], "5√5")],
             [["(a²)³ = a⁵", "On multiplie les exposants : a⁶."], ["√(9 + 16) = 3 + 4", "√25 = 5."], ["√((−3)²) = −3", "√((−3)²) = √9 = 3 = |−3|."]])
    faq = [("Pourquoi √(a²) = |a| ?", "Une racine carrée est toujours positive ; si a est négatif, √(a²) vaut −a."),
           ("Comment savoir quel carré chercher ?", "On teste 4, 9, 16, 25, 36, 49… en partant du plus grand possible.")]
    unit("seconde", R, "puissances-et-racines-carrees", "N",
         "Utiliser les règles de calcul sur les puissances entières et les racines carrées ; simplifier une racine carrée ; connaître √(a²) = |a| et √(ab) = √a × √b ; comparer √(a + b) et √a + √b",
         "Puissances et racines carrées", "Puissances et racines carrées",
         "Fiches de maths seconde sur les puissances et les racines carrées : règles de calcul, exposants négatifs, simplifier √n, calculs et problèmes. 100 exercices corrigés.",
         "aᵐ × aⁿ = aᵐ⁺ⁿ ; √(ab) = √a × √b", "√(a²) = |a| ; √(a + b) ≠ √a + √b", body, faq, sets, 4)


if __name__ == "__main__":
    main()
