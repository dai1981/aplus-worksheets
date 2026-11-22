# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Comparer, additionner et soustraire des fractions
  python3 tools/gen_fr_maths_cm1_calculer_avec_des_fractions.py
Comparer à 1, même dénominateur, même numérateur, dénominateurs multiples ; additionner et soustraire (même dénominateur,
puis un dénominateur multiple de l’autre) ; écrire le résultat comme entier + fraction ; problèmes.
Erreurs : additionner les dénominateurs, croire 1/8 &gt; 1/4, comparer 2/3 et 5/6 sans les mettre au même dénominateur.
"""
import random
from fractions import Fraction as F
from fr_c3 import mcq, lesson, example, unit, mix, Kids, GN, fr

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52109 + 100 * lv)
    K = Kids(R)


def dmax():
    return 20 if L == 1 else 60


def opts_cmp(a, b):
    return [a, b, "elles sont égales", "on ne peut pas savoir"]


def s1():
    k = R.choice(["un", "den", "den"])
    d = R.randint(3, dmax())
    if k == "un":
        n = R.choice([x for x in range(1, 2 * d) if x != d])
        right = "plus petite que 1" if n < d else "plus grande que 1"
        return mcq("%s est-elle plus petite ou plus grande que 1 ?" % fr(n, d), right, ["plus grande que 1" if n < d else "plus petite que 1", "égale à 1", "on ne peut pas savoir"],
                   "1 = %s. Le numérateur %d est %s que le dénominateur : <b>%s</b>." % (fr(d, d), n, "plus petit" if n < d else "plus grand", right))
    a, b = R.sample(range(1, 2 * d), 2)
    g, s = (a, b) if a > b else (b, a)
    return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(a, d), fr(b, d)), fr(g, d), [fr(s, d), "elles sont égales", "on ne peut pas savoir"],
               "Même dénominateur : les parts ont la même taille. %d parts &gt; %d parts : <b>%s</b>." % (g, s, fr(g, d)))


def s2():
    if R.random() < 0.5:
        a, b = R.sample(range(2, dmax() + 1), 2)
        n = R.randint(1, min(a, b) - 1) if min(a, b) > 2 else 1
        big = fr(n, min(a, b))
        return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(n, a), fr(n, b)), big, [fr(n, max(a, b)), "elles sont égales", "on ne peut pas savoir"],
                   "Même numérateur : plus le dénominateur est grand, plus les parts sont petites. <b>%s</b> est la plus grande." % big)
    d1 = R.randint(2, 10 if L == 1 else 15)
    m = R.choice([2, 3, 4])
    d2 = d1 * m
    if d2 > dmax():
        return None
    a = R.randint(1, 2 * d1 - 1)
    b = R.randint(1, 2 * d2 - 1)
    if F(a, d1) == F(b, d2):
        return None
    g = fr(a, d1) if F(a, d1) > F(b, d2) else fr(b, d2)
    s = fr(b, d2) if g == fr(a, d1) else fr(a, d1)
    return mcq("Quelle est la plus grande fraction : %s ou %s ?" % (fr(a, d1), fr(b, d2)), g, [s, "elles sont égales", "on ne peut pas savoir"],
               "On écrit %s = %s (on multiplie en haut et en bas par %d). On compare %d et %d %s : <b>%s</b>." % (fr(a, d1), fr(a * m, d2), m, a * m, b, "" if True else "", g))


def mixed(v, d):
    """F → « 2 + 3/8 » ou « 3/8 » ou « 2 »"""
    e = v.numerator * (d // v.denominator) // d
    r = v.numerator * (d // v.denominator) - e * d
    if e and r:
        return "%d + %s" % (e, fr(r, d))
    if e:
        return str(e)
    return fr(r, d)


def s3():
    d = R.randint(3, 12 if L == 1 else 30)
    a, b = R.randint(1, 2 * d), R.randint(1, d)
    s = a + b
    if R.random() < 0.5 or s <= d:
        return mcq("Calcule : %s + %s" % (fr(a, d), fr(b, d)), fr(s, d), [fr(s, 2 * d), fr(a * b, d) if a * b != s else fr(s + 1, d), fr(s, d + d // 2) if d > 2 else fr(s - 1, d)],
                   "Même dénominateur : on additionne les numérateurs, le dénominateur ne change pas : <b>%s</b>." % fr(s, d))
    if s % d == 0:
        return None
    right = mixed(F(s, d), d)
    return mcq("Calcule %s + %s et écris le résultat sous la forme entier + fraction." % (fr(a, d), fr(b, d)), right,
               [mixed(F(s - d, d), d) if s - d > d else "1 + %s" % fr(s, d), "%d + %s" % (s // d + 1, fr(s % d, d)), "%d + %s" % (s // d, fr(d - s % d, d)) if d - s % d != s % d else "%d + %s" % (s // d, fr(s % d, 2 * d))],
               "%s + %s = %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(s, d), right))


def s4():
    d1 = R.randint(2, 10 if L == 1 else 15)
    m = R.choice([2, 3, 4, 5])
    d2 = d1 * m
    if d2 > dmax():
        return None
    a, b = R.randint(1, 2 * d1 - 1), R.randint(1, 2 * d2 - 1)
    op = R.choice(["+", "−"])
    v = F(a, d1) + F(b, d2) if op == "+" else F(a, d1) - F(b, d2)
    if v <= 0:
        return None
    n = v * d2
    right = fr(n.numerator, d2) if n.denominator == 1 else None
    if not right:
        return None
    w = [fr(a + b if op == "+" else abs(a - b), d1 + d2) if (a != b or op == "+") else None, fr(a + b if op == "+" else abs(a - b), d2) if (a != b or op == "+") else None, fr(n.numerator + 1, d2), fr(n.numerator, d1) if d1 != d2 and n.numerator else None]
    return mcq("Calcule : %s %s %s" % (fr(a, d1), op, fr(b, d2)), right, [x for x in w if x and x != right],
               "%s = %s. Puis %s %s %s = <b>%s</b>." % (fr(a, d1), fr(a * m, d2), fr(a * m, d2), op, fr(b, d2), right))


def s4b():
    d = R.randint(3, 12 if L == 1 else 25)
    a, b = R.randint(2, 3 * d), R.randint(1, 2 * d)
    if a <= b:
        a, b = b, a
    if a == b:
        return None
    if R.random() < 0.4:
        e = R.randint(1, 3)
        b = R.randint(1, d - 1)
        right = fr(e * d - b, d)
        return mcq("Calcule : %d − %s" % (e, fr(b, d)), right, [fr(e - b if e > b else b - e, d), fr(e * d + b, d), fr(d - b, d) if e > 1 else fr(b, d)],
                   "%d = %s. %s − %s = <b>%s</b>." % (e, fr(e * d, d), fr(e * d, d), fr(b, d), right))
    return mcq("Calcule : %s − %s" % (fr(a, d), fr(b, d)), fr(a - b, d), [fr(a - b, 0) if False else fr(a + b, d), fr(a - b + 1, d), fr(a - b, d * 2)],
               "On soustrait les numérateurs : %d − %d = %d. Réponse : <b>%s</b>." % (a, b, a - b, fr(a - b, d)))


def s5():
    p, o = K.two()
    k = R.choice(["course", "gateau", "plus", "bouteille"])
    if k == "course":
        d1, m = R.choice([(2, 2), (2, 4), (3, 2), (4, 2), (5, 2)] + ([(3, 3), (4, 3), (6, 2)] if L == 2 else []))
        d2 = d1 * m
        a, b = R.randint(1, d1 - 1), R.randint(1, d2 - 1)
        v = F(a, d1) + F(b, d2)
        n = v * d2
        return mcq("%s court %s de km puis %s de km. Quelle distance a-t-%s parcourue ?" % (p[0], fr(a, d1), fr(b, d2), p[1]), fr(n.numerator, d2) + " km",
                   [fr(a + b, d1 + d2) + " km", fr(a + b, d2) + " km" if a + b != n.numerator else fr(n.numerator + 1, d2) + " km", fr(a * b, d2) + " km" if a * b != n.numerator else fr(n.numerator - 1, d2) + " km"],
                   "%s = %s ; %s + %s = <b>%s km</b>." % (fr(a, d1), fr(a * m, d2), fr(a * m, d2), fr(b, d2), fr(n.numerator, d2)))
    if k == "gateau":
        d = R.choice([6, 8, 10, 12])
        a, b = R.randint(1, d // 2), R.randint(1, d // 2)
        if a + b >= d:
            return None
        return mcq("%s mange %s d’un gâteau et %s en mange %s. Quelle fraction du gâteau reste-t-il ?" % (p[0], fr(a, d), o[0], fr(b, d)), fr(d - a - b, d),
                   [fr(a + b, d), fr(d - a - b, 2 * d), fr(d - a - b + 1, d)], "Mangé : %s. Reste : %s − %s = <b>%s</b>." % (fr(a + b, d), fr(d, d), fr(a + b, d), fr(d - a - b, d)))
    if k == "plus":
        d = R.randint(4, 12)
        a, b = R.sample(range(1, d), 2)
        big, sm = max(a, b), min(a, b)
        who = p[0] if a > b else o[0]
        return mcq("%s a lu %s d’un livre, %s en a lu %s. Qui en a lu le plus, et de combien ?" % (p[0], fr(a, d), o[0], fr(b, d)), "%s, de %s" % (who, fr(big - sm, d)),
                   ["%s, de %s" % (o[0] if who == p[0] else p[0], fr(big - sm, d)), "%s, de %s" % (who, fr(big + sm, d)), "%s, de %s" % (who, fr(big - sm, 2 * d))],
                   "%s &gt; %s ; écart : %s − %s = <b>%s</b>." % (fr(big, d), fr(sm, d), fr(big, d), fr(sm, d), fr(big - sm, d)))
    d = R.choice([4, 5, 10])
    a = R.randint(d + 1, 3 * d)
    b = R.randint(1, d - 1)
    if a - b <= 0:
        return None
    return mcq("Un bidon contient %s L d’eau. On en utilise %s L. Combien de litres restent ?" % (fr(a, d), fr(b, d)), fr(a - b, d) + " L", [fr(a + b, d) + " L", fr(a - b, 2 * d) + " L", fr(a - b - 1, d) + " L"],
               "%s − %s = <b>%s L</b>." % (fr(a, d), fr(b, d), fr(a - b, d)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Comparer à 1 et avec le même dénominateur", mix(R, seen, [(s1, 20)])),
        ("Même numérateur, dénominateurs multiples", mix(R, seen, [(s2, 20)])),
        ("Additionner des fractions", mix(R, seen, [(s3, 20)])),
        ("Soustraire et dénominateurs différents", mix(R, seen, [(s4, 12), (s4b, 8)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Même dénominateur : la plus grande fraction a le plus grand numérateur. Même numérateur : c’est celle qui a le <b>plus petit</b> dénominateur.",
         "Si un dénominateur est un multiple de l’autre, on change une fraction : %s = %s (on multiplie en haut et en bas par 2)." % (fr(2, 3), fr(4, 6)),
         "Pour additionner ou soustraire, il faut le <b>même dénominateur</b> : on additionne les numérateurs, le dénominateur ne change pas."],
        [example("%s + %s" % (fr(2, 3), fr(5, 6)), ["%s = %s" % (fr(2, 3), fr(4, 6)), "%s + %s = %s" % (fr(4, 6), fr(5, 6), fr(9, 6))], "%s = 1 + %s" % (fr(9, 6), fr(3, 6)))],
        [["Additionner les dénominateurs : %s + %s = %s" % (fr(1, 4), fr(2, 4), fr(3, 8)), "Des quarts plus des quarts font des quarts : %s." % fr(3, 4)],
         ["Croire que %s &gt; %s car 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Plus on partage, plus les parts sont petites."],
         ["Comparer %s et %s en regardant seulement les numérateurs" % (fr(2, 3), fr(5, 6)), "On écrit %s = %s, puis %s &lt; %s." % (fr(2, 3), fr(4, 6), fr(4, 6), fr(5, 6))]])
    faq = [("Comment trouver une fraction égale ?", "On multiplie (ou divise) le numérateur et le dénominateur par le même nombre : %s = %s = %s." % (fr(1, 2), fr(2, 4), fr(5, 10))),
           ("Doit-on simplifier le résultat ?", "Ce n’est pas obligatoire en %s, mais on peut écrire le résultat sous la forme entier + fraction." % GN(lv))]
    unit(lv, R, "comparer-additionner-et-soustraire-des-fractions", "N",
         "Comparer des fractions (dénominateur inférieur ou égal à %d) ; additionner et soustraire des fractions de même dénominateur ou dont un dénominateur est multiple de l’autre" % dmax(),
         "Comparer, additionner et soustraire des fractions", "Calculer avec des fractions",
         "Fiches de maths %s pour comparer des fractions, les additionner et les soustraire (même dénominateur ou multiple), avec problèmes. 100 exercices corrigés." % GN(lv),
         "Même dénominateur : on additionne les numérateurs.", "2/3 = 4/6 : on multiplie en haut et en bas par le même nombre.",
         body, faq, sets, 9)


if __name__ == "__main__":
    build(1)
