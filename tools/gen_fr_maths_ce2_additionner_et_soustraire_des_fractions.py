# -*- coding: utf-8 -*-
"""
France Maths CE2 : Additionner et soustraire des fractions (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_additionner_et_soustraire_des_fractions.py
Même dénominateur (2, 3, 4, 5, 6, 8, 10), résultat plus grand que 1, complément à 1, dénominateurs multiples
(1/2 + 1/4, 1/5 + 3/10), problèmes.
Erreurs : additionner les dénominateurs (1/4 + 2/4 → 3/8), oublier que 4/4 = 1, additionner 1/2 + 1/4 en 2/6.
"""
import random
from fractions import Fraction as F
from fr_c2 import pl
from fr_common import mcq, lesson, example, make_unit, mix, Kids, fr

R = random.Random(51010)
K = Kids(R)
DEN = [3, 4, 5, 6, 8, 10]


def fv(v, d):
    """valeur F écrite avec le dénominateur d"""
    return fr(int(v * d), d)


def s1_add():
    d = R.choice(DEN)
    a, b = R.randint(1, d - 2), R.randint(1, d - 2)
    if a + b >= d:
        return None
    return mcq("Calcule : %s + %s" % (fr(a, d), fr(b, d)), fr(a + b, d), [fr(a + b, 2 * d), fr(a * b, d) if a * b != a + b else fr(a + b + 1, d), fr(a + b, d + d // 2), fr(a + b - 1, d) if a + b > 1 else None],
               "Même dénominateur : on additionne les parts. %d + %d = %d %s, donc <b>%s</b>." % (a, b, a + b, "parts", fr(a + b, d)))


def s1_sub():
    d = R.choice(DEN)
    a = R.randint(2, d)
    b = R.randint(1, a - 1)
    return mcq("Calcule : %s − %s" % (fr(a, d), fr(b, d)), fr(a - b, d), [fr(a + b, d), fr(a - b + 1, d), fr(b, d) if b != a - b else fr(a, d)],
               "On enlève %s à %s : %d − %d = %d, donc <b>%s</b>." % (pl(b, "part"), pl(a, "part"), a, b, a - b, fr(a - b, d)))


def s2_plus_un():
    d = R.choice(DEN)
    a, b = R.randint(2, d - 1), R.randint(2, d - 1)
    s = a + b
    if s <= d:
        return None
    right = "1 + %s" % fr(s - d, d)
    return mcq("Calcule %s + %s et écris le résultat avec 1 + …" % (fr(a, d), fr(b, d)), right,
               ["1 + %s" % fr(s - d + 1, d) if s - d + 1 < d else "2 + %s" % fr(s - d, d), fr(s, 2 * d), "1 + %s" % fr(s, d)],
               "%s + %s = %s = %s + %s = <b>1 + %s</b>." % (fr(a, d), fr(b, d), fr(s, d), fr(d, d), fr(s - d, d), fr(s - d, d)))


def s2_egal1():
    d = R.choice(DEN + [2])
    a = R.randint(1, d - 1)
    b = d - a
    c = R.choice(["1", fr(a + b, 2 * d), fr(d - 1, d) if d - 1 != a else fr(1, d)])
    return mcq("Calcule : %s + %s" % (fr(a, d), fr(b, d)), "1", [fr(d, 2 * d), fr(d - 1, d), fr(1, d), fr(a, b) if a != b else fr(2, d)],
               "%s + %s = %s : toutes les parts, donc <b>1</b>." % (fr(a, d), fr(b, d), fr(d, d)))


def s3_compl():
    d = R.choice(DEN + [2])
    a = R.randint(1, d - 1)
    return mcq("Complète : %s + … = 1" % fr(a, d), fr(d - a, d), [fr(a, d) if a != d - a else fr(a + 1, d), fr(d - a, 2 * d), fr(d - a + 1, d) if d - a + 1 < d else fr(1, d + 1), fr(1, a) if a > 1 else None],
               "1 = %s. Il manque %d − %d = %s : <b>%s</b>." % (fr(d, d), d, a, pl(d - a, "part"), fr(d - a, d)))


def s3_moins():
    d = R.choice(DEN + [2])
    a = R.randint(1, d - 1)
    return mcq("Calcule : 1 − %s" % fr(a, d), fr(d - a, d), [fr(a, d) if a != d - a else fr(a + 1, d), fr(1 - 0, d) if d - a != 1 else fr(2, d), fr(d - a, d + 1)],
               "1 = %s ; %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), fr(d - a, d)))


PAIRS = [(2, 4), (2, 6), (2, 8), (2, 10), (4, 8), (3, 6), (5, 10)]


def s4_mult():
    a_d, b_d = R.choice(PAIRS)
    a = R.randint(1, a_d - 1)
    b = R.randint(1, b_d - 1)
    if F(a, a_d) == F(b, b_d) and R.random() < 0.5:
        return None
    k = b_d // a_d
    op = R.choice(["+", "−"])
    v = F(a, a_d) + F(b, b_d) if op == "+" else F(a, a_d) - F(b, b_d)
    if v <= 0 or v > 1:
        return None
    right = fv(v, b_d)
    nn = a + b if op == "+" else abs(a - b)
    wr = [fr(nn, a_d + b_d) if nn else None, fr(nn, b_d) if nn else None, fv(v + F(1, b_d), b_d) if v + F(1, b_d) <= 1 else fv(v - F(1, b_d), b_d)]
    return mcq("Calcule : %s %s %s" % (fr(a, a_d), op, fr(b, b_d)), right, [w for w in wr if w != right],
               "%s = %s (chaque part est coupée en %d). %s %s %s = <b>%s</b>." % (fr(a, a_d), fr(a * k, b_d), k, fr(a * k, b_d), op, fr(b, b_d), right))


def s5_prob():
    p = K.next()
    k = R.choice(["ruban", "gateau", "trajet", "bouteille", "livre"])
    d = R.choice([4, 5, 6, 8, 10])
    a, b = R.randint(1, d - 2), R.randint(1, d - 2)
    if a + b >= d:
        return None
    if k == "ruban":
        q = "%s utilise %s d’un ruban le matin et %s l’après-midi. Quelle fraction du ruban a-t-%s utilisée ?" % (p[0], fr(a, d), fr(b, d), p[1])
        r_, wr = fr(a + b, d), [fr(a + b, 2 * d), fr(d - a - b, d), fr(abs(a - b), d) if a != b else fr(a + b + 1, d)]
    elif k == "gateau":
        q = "%s mange %s d’un gâteau. Quelle fraction du gâteau reste-t-il ?" % (p[0], fr(a, d))
        r_, wr = fr(d - a, d), [fr(a, d) if a != d - a else fr(a + 1, d), fr(d - a, 2 * d), fr(d + a, d)]
    elif k == "trajet":
        q = "%s a parcouru %s du chemin de l’école. Quelle fraction du chemin lui reste-t-il à faire ?" % (p[0], fr(a + b, d))
        r_, wr = fr(d - a - b, d), [fr(a + b, d), fr(d - a - b, 2 * d), fr(d - a - b + 1, d)]
    elif k == "bouteille":
        q = "Une bouteille est pleine aux %s. On boit %s de la bouteille. Quelle fraction reste-t-il ?" % (fr(a + b, d), fr(b, d))
        r_, wr = fr(a, d), [fr(a + 2 * b, d) if a + 2 * b <= d else fr(a + 1, d), fr(a, 2 * d), fr(b, d) if b != a else fr(a + 1, d)]
    else:
        q = "%s lit %s d’un livre lundi et %s mardi. Quelle fraction du livre a-t-%s lue en deux jours ?" % (p[0], fr(a, d), fr(b, d), p[1])
        r_, wr = fr(a + b, d), [fr(a + b, 2 * d), fr(d - a - b, d) if d - a - b != a + b else fr(a + b + 1, d), fr(a * b, d) if a * b != a + b and a * b < d else fr(a + b - 1, d) if a + b > 1 else None]
    return mcq(q, r_, wr, "Même dénominateur : on compte les parts. Réponse : <b>%s</b>." % r_)


def main():
    seen = set()
    sets = [
        ("Même dénominateur", mix(R, seen, [(s1_add, 12), (s1_sub, 8)])),
        ("Faire 1 ou plus que 1", mix(R, seen, [(s2_plus_un, 12), (s2_egal1, 8)])),
        ("Compléter à 1", mix(R, seen, [(s3_compl, 12), (s3_moins, 8)])),
        ("Avec 1/2 et 1/4, 1/5 et 1/10", mix(R, seen, [(s4_mult, 20)])),
        ("Problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["Avec le <b>même dénominateur</b>, les parts ont la même taille : on additionne ou on soustrait les <b>numérateurs</b>. Le dénominateur ne change pas.",
         "%s + %s = %s (2 quarts + 1 quart = 3 quarts)." % (fr(2, 4), fr(1, 4), fr(3, 4)),
         "Quand on a toutes les parts, on a 1 : %s = 1. Donc %s = 1 + %s." % (fr(5, 5), fr(7, 5), fr(2, 5)),
         "Pour %s + %s, on coupe chaque moitié en 2 : %s = %s, puis %s + %s = %s." % (fr(1, 2), fr(1, 4), fr(1, 2), fr(2, 4), fr(2, 4), fr(1, 4), fr(3, 4))],
        [example("%s + %s" % (fr(3, 8), fr(4, 8)), ["3 huitièmes + 4 huitièmes = 7 huitièmes"], fr(7, 8)),
         example("1 − %s" % fr(2, 5), ["1 = %s" % fr(5, 5), "5 − 2 = 3"], fr(3, 5))],
        [["Additionner les dénominateurs : %s + %s = %s" % (fr(1, 4), fr(2, 4), fr(3, 8)), "Les parts restent des quarts : %s." % fr(3, 4)],
         ["Oublier que %s = 1" % fr(4, 4), "%s + %s = %s = 1." % (fr(3, 4), fr(1, 4), fr(4, 4))],
         ["%s + %s = %s" % (fr(1, 2), fr(1, 4), fr(2, 6)), "On écrit d’abord %s = %s : le résultat est %s." % (fr(1, 2), fr(2, 4), fr(3, 4))]])
    faq = [("Pourquoi le dénominateur ne change-t-il pas ?", "Parce qu’il dit la taille des parts. Des quarts plus des quarts, ce sont encore des quarts."),
           ("Peut-on additionner des tiers et des quarts au CE2 ?", "Non : au CE2, on additionne des fractions de même dénominateur, ou dont un dénominateur est un multiple de l’autre (demis et quarts).")]
    make_unit(R, "additionner-et-soustraire-des-fractions", "N",
              "Additionner et soustraire des fractions de même dénominateur, ou dont un dénominateur est multiple de l’autre ; décomposer une fraction en 1 + une fraction ; trouver le complément à 1 ; résoudre des problèmes (résumé du programme 2024 du cycle 2).",
              "Additionner et soustraire des fractions", "Additionner des fractions CE2 : fiches et exercices avec corrigé", "Additionner des fractions",
              "Fiches de maths CE2 pour additionner et soustraire des fractions : même dénominateur, complément à 1, résultat plus grand que 1, demis et quarts, problèmes. 100 exercices corrigés.",
              "Même dénominateur : on additionne les numérateurs.", "Le dénominateur ne change pas : 2/4 + 1/4 = 3/4.",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
