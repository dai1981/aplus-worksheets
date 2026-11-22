# -*- coding: utf-8 -*-
"""
France Maths 6e : Comparer et calculer avec des fractions
  python3 tools/gen_fr_maths_6e_calculer_avec_des_fractions.py
Comparer (même dénominateur, même numérateur, à 1), encadrer entre deux entiers, additionner et soustraire (même dénominateur
ou dénominateur multiple), multiplier une fraction par un entier, problèmes.
Erreurs : 1/8 &gt; 1/4 car 8 &gt; 4, 1/2 + 1/4 = 2/6, 3 × 2/5 = 6/15.
"""
import random
from math import gcd
from fr_c4 import *

R = random.Random(60109)
K = Kids(R)


def s1():
    k = R.choice(["den", "num", "un"])
    den = R.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    if k == "den":
        a, b = R.sample(range(1, 2 * den), 2)
        big = max(a, b)
        return M("Quelle est la plus grande fraction : %s ou %s ?" % (fr(a, den), fr(b, den)), fr(big, den), [fr(min(a, b), den), "elles sont égales", "on ne peut pas savoir"],
                 "Même dénominateur : on compare les numérateurs. <b>%s</b>." % fr(big, den))
    if k == "num":
        n = R.randint(1, 5)
        a, b = R.sample([3, 4, 5, 6, 7, 8, 9, 10, 12], 2)
        g = min(a, b)
        return M("Quelle est la plus grande fraction : %s ou %s ?" % (fr(n, a), fr(n, b)), fr(n, g), [fr(n, max(a, b)), "elles sont égales", "on ne peut pas savoir"],
                 "Même numérateur : plus on partage, plus les parts sont petites. La plus grande est <b>%s</b>." % fr(n, g))
    n = R.randint(1, 2 * den)
    if n == den:
        return None
    r = "plus petite que 1" if n < den else "plus grande que 1"
    return M("%s est-elle plus petite ou plus grande que 1 ?" % fr(n, den), r, ["plus grande que 1" if n < den else "plus petite que 1", "égale à 1", "on ne peut pas savoir"],
             "1 = %s. Le numérateur %d est %s que le dénominateur %d : %s est <b>%s</b>." % (fr(den, den), n, "plus petit" if n < den else "plus grand", den, fr(n, den), r))


def s2():
    den = R.choice([2, 3, 4, 5, 6, 8, 10])
    n = R.randint(den + 1, 6 * den)
    if n % den == 0:
        return None
    e = n // den
    if R.random() < 0.6:
        return M("Entre quels entiers consécutifs se trouve %s ?" % fr(n, den), "%d et %d" % (e, e + 1), ["%d et %d" % (e - 1, e) if e > 0 else "%d et %d" % (e + 1, e + 2), "%d et %d" % (e + 1, e + 2), "%d et %d" % (den, n) if n < 30 else "%d et %d" % (e + 2, e + 3)],
                 "%s = %s + %s, donc <b>%d &lt; %s &lt; %d</b>." % (fr(n, den), fr(e * den, den), fr(n - e * den, den), e, fr(n, den), e + 1))
    xs = sorted(R.sample([x for x in range(1, 3 * den) if x % den], 3))
    up = [fr(x, den) for x in xs]
    sh = list(up)
    R.shuffle(sh)
    return M("Range dans l’ordre croissant : %s" % " ; ".join(sh), " &lt; ".join(up), [" &lt; ".join(up[::-1]), " &lt; ".join([up[1], up[0], up[2]]), " &lt; ".join([up[0], up[2], up[1]])],
             "Même dénominateur : on range les numérateurs. <b>%s</b>." % " &lt; ".join(up))


def s3():
    den = R.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    a, b = R.randint(1, 2 * den), R.randint(1, 2 * den)
    if gcd(a, den) > 1 or gcd(b, den) > 1:
        return None
    if R.random() < 0.5:
        return M("%s + %s = …" % (fr(a, den), fr(b, den)), fr(a + b, den), [fr(a + b, 2 * den), fr(a * b, den) if a * b != a + b else fr(a + b + 1, den), fr(a + b, den * den)],
                 "Même dénominateur : on additionne les numérateurs et on garde le dénominateur : <b>%s</b>." % fr(a + b, den))
    if a <= b:
        a, b = b + 1, a
    return M("%s − %s = …" % (fr(a, den), fr(b, den)), fr(a - b, den), [fr(a - b, 0) if False else fr(a + b, den), fr(a - b + 1, den), fr(a - b, 2 * den) if True else ""],
             "On soustrait les numérateurs : %d − %d = %d, donc <b>%s</b>." % (a, b, a - b, fr(a - b, den)))


def s4():
    d1 = R.choice([2, 3, 4, 5])
    m = R.choice([2, 3, 4])
    d2 = d1 * m
    if d2 > 20:
        return None
    a, b = R.randint(1, 2 * d1), R.randint(1, 2 * d2)
    if gcd(a, d1) > 1 or gcd(b, d2) > 1:
        return None
    plus = R.random() < 0.6
    A = a * m
    if not plus and A <= b:
        return None
    r = A + b if plus else A - b
    return M("%s %s %s = …" % (fr(a, d1), "+" if plus else "−", fr(b, d2)), fr(r, d2),
             [fr(a + b if plus else abs(a - b), d1 + d2), fr(a + b if plus else abs(a - b) or 1, d2), fr(r, d1 * d2) if d1 * d2 != d2 else fr(r + 1, d2)],
             "On écrit %s avec le dénominateur %d : %s = %s. Puis %s %s %s = <b>%s</b>." % (fr(a, d1), d2, fr(a, d1), fr(A, d2), fr(A, d2), "+" if plus else "−", fr(b, d2), fr(r, d2)))


def s5():
    p = K.next()
    k = R.choice(["mult", "mult", "pizza", "jus", "chemin"])
    if k == "mult":
        n, den = R.randint(2, 9), R.choice([3, 4, 5, 7, 9, 10])
        a = R.randint(1, den - 1)
        return M("%d %s %s = …" % (n, FOIS, fr(a, den)), fr(n * a, den), [fr(n * a, n * den), fr(a, n * den), fr(n + a, den)],
                 "On multiplie le numérateur par %d : %d %s %d = %d, donc <b>%s</b>." % (n, n, FOIS, a, n * a, fr(n * a, den)))
    if k == "pizza":
        den = R.choice([6, 8, 12])
        a, b = R.randint(1, den // 2), R.randint(1, den // 2 - 1)
        if gcd(a, den) > 1 or gcd(b, den) > 1:
            return None
        q = K.next()
        return M("%s mange %s d’une pizza et %s en mange %s. Quelle fraction de la pizza ont-ils mangée ?" % (p[0], fr(a, den), q[0], fr(b, den)), fr(a + b, den), [fr(a + b, 2 * den), fr(den - a - b, den), fr(a * b, den) if a * b != a + b else fr(a + b + 1, den)],
                 "%s + %s = <b>%s</b>." % (fr(a, den), fr(b, den), fr(a + b, den)))
    if k == "jus":
        n = R.randint(3, 8)
        return M("Chaque verre contient %s de litre. Combien de litres faut-il pour %d verres ?" % (fr(1, 4), n), fq(Fr(n, 4)) if False else fr(n, 4), [fr(1, 4 * n), fr(n, 4 * n), fr(n + 1, 4)],
                 "%d %s %s = <b>%s</b> L (= %s L)." % (n, FOIS, fr(1, 4), fr(n, 4), d(Fr(n, 4))))
    den = R.choice([4, 5, 6, 8])
    a = R.randint(1, den - 2)
    return M("%s a parcouru %s du chemin. Quelle fraction lui reste-t-il à faire ?" % (p[0], fr(a, den)), fr(den - a, den), [fr(a, den) if a != den - a else fr(a + 1, den), fr(1, den - a) if den - a > 1 else fr(1, 2), fr(den - a, 2 * den)],
             "Le chemin entier, c’est %s = 1. %s − %s = <b>%s</b>." % (fr(den, den), fr(den, den), fr(a, den), fr(den - a, den)))


def main():
    seen = set()
    sets = [("Comparer des fractions", mix(R, seen, [(s1, 20)])), ("Encadrer et ranger", mix(R, seen, [(s2, 20)])),
            ("Même dénominateur", mix(R, seen, [(s3, 20)])), ("Dénominateurs multiples", mix(R, seen, [(s4, 20)])), ("Fraction × entier et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Avec le même dénominateur, on compare, on additionne ou on soustrait les <b>numérateurs</b> ; le dénominateur ne change pas.",
              "Pour %s + %s, on écrit %s = %s, puis %s + %s = %s." % (fr(1, 2), fr(1, 4), fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4), fr(3, 4)),
              "3 × %s = %s : on multiplie seulement le numérateur." % (fr(2, 5), fr(6, 5))],
             [("%s + %s" % (fr(2, 3), fr(5, 6)), ["%s = %s" % (fr(2, 3), fr(4, 6)), "%s + %s" % (fr(4, 6), fr(5, 6))], fr(9, 6))],
             [["Croire que %s &gt; %s car 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Partager en 8 donne des parts plus petites qu’en 4."],
              ["%s + %s = %s" % (fr(1, 2), fr(1, 4), fr(2, 6)), "On ne additionne pas les dénominateurs : %s + %s = %s." % (fr(2, 4), fr(1, 4), fr(3, 4))],
              ["3 × %s = %s" % (fr(2, 5), fr(6, 15)), "On multiplie seulement le numérateur : %s." % fr(6, 5)]])
    faq = [("Pourquoi ne pas additionner les dénominateurs ?", "Le dénominateur dit la taille des parts : des quarts plus des quarts restent des quarts."),
           ("Comment comparer %s et %s ?" % (fr(2, 3), fr(5, 6)), "On écrit %s = %s : %s &lt; %s." % (fr(2, 3), fr(4, 6), fr(4, 6), fr(5, 6)))]
    unit("6e", R, "calculer-avec-des-fractions", "N",
         "Comparer, encadrer et ordonner des fractions ou des nombres mixtes ; additionner et soustraire deux fractions dans des cas simples ; multiplier une fraction par un entier",
         "Comparer et calculer avec des fractions", "Calculer avec des fractions",
         "Fiches de maths 6e pour comparer et calculer avec des fractions : comparer, encadrer, additionner, soustraire, multiplier par un entier et problèmes. 100 exercices corrigés.",
         "%s + %s = %s" % (fr(2, 4), fr(1, 4), fr(3, 4)), "On garde le dénominateur.", body, faq, sets, 9)


if __name__ == "__main__":
    main()
