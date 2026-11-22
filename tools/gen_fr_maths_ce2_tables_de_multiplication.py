# -*- coding: utf-8 -*-
"""
France Maths CE2 : Les tables de multiplication (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_tables_de_multiplication.py
Tables de 2 à 9, facteur manquant, multiples, × 10 et × 100, commutativité, petits problèmes.
Erreurs : confondre avec l’addition (6 × 7 → 13), se tromper de ligne (7 × 8 → 48 ou 63), oublier le 0 (× 10).
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, FOIS, table

R = random.Random(51006)
K = Kids(R)


def wrongs(a, b):
    p = a * b
    return [a * (b + 1), a * (b - 1), a + b, (a + 1) * b, (a - 1) * b, p + 1, p - 2]


def fact(tabs):
    a, b = R.choice(tabs), R.randint(2, 10)
    if R.random() < 0.4:
        a, b = b, a
    return mcq("Combien font %d %s %d ?" % (a, FOIS, b), a * b, [x for x in wrongs(a, b) if x > 0 and x != a * b],
               "Dans la table de %d : %d %s %d = <b>%d</b>." % (max(a, b) if min(a, b) == 10 else a if a in tabs else b, a, FOIS, b, a * b))


def s1():
    return fact([2, 3, 4, 5])


def s2():
    return fact([6, 7, 8, 9])


def s3_manq():
    a, b = R.randint(2, 9), R.randint(2, 10)
    p = a * b
    if R.random() < 0.5:
        q = "Complète : %d %s … = %d" % (a, FOIS, p)
    else:
        q = "Complète : … %s %d = %d" % (FOIS, a, p)
    return mcq(q, b, [b + 1, b - 1, p - a, a, p // 2 if p % 2 == 0 and p // 2 != b else None],
               "On cherche combien de fois %d dans %d : %d %s <b>%d</b> = %d." % (a, p, a, FOIS, b, p))


def s4_multiple():
    t = R.randint(3, 9)
    good = t * R.randint(3, 9)
    bad = set()
    while len(bad) < 3:
        x = good + R.choice([-3, -2, -1, 1, 2, 3]) + R.choice([0, t])
        if x > 0 and x % t:
            bad.add(x)
    allv = sorted(bad | {good})
    return mcq("Parmi %s, quel nombre est dans la table de %d ?" % (", ".join(map(str, allv[:-1])) + " et " + str(allv[-1]), t), good, sorted(bad),
               "%d = %d %s %d, donc %d est dans la table de %d." % (good, t, FOIS, good // t, good, t))


def s4_10():
    a = R.randint(2, 99)
    k = R.choice([10, 100]) if a < 100 else 10
    p = a * k
    return mcq("Combien font %d %s %s ?" % (a, FOIS, num(k)), num(p), [num(a * (110 - k) // 1 if k == 10 else a * 10), num(a + k), num(p * 10) if p * 10 < 100000 else None, num(a * 1000) if k == 10 else None],
               "Multiplier par %s, c’est écrire %s à droite du nombre : <b>%s</b>." % (num(k), "un 0" if k == 10 else "deux 0", num(p)))


def s4_comm():
    a, b = R.randint(3, 9), R.randint(3, 9)
    if a == b:
        return None
    return mcq("Je sais que %d %s %d = %d. Combien font %d %s %d ?" % (a, FOIS, b, a * b, b, FOIS, a), a * b, [a * b + a, a * b - b, a + b],
               "On peut changer l’ordre des facteurs : %d %s %d = %d %s %d = <b>%d</b>." % (b, FOIS, a, a, FOIS, b, a * b))


def s4_double():
    a = R.randint(3, 9)
    return mcq("Je sais que 4 %s %d = %d. Combien font 8 %s %d ?" % (FOIS, a, 4 * a, FOIS, a), 8 * a, [4 * a + 4, 4 * a + a, 8 + a],
               "8, c’est le double de 4 : 8 %s %d = 2 %s %d = <b>%d</b>." % (FOIS, a, FOIS, 4 * a, 8 * a))


SCENES = [("Il y a %d boîtes de %d œufs. Combien d’œufs en tout ?", "œufs"),
          ("Une classe forme %d équipes de %d élèves. Combien d’élèves en tout ?", "élèves"),
          ("Un fleuriste fait %d bouquets de %d roses. Combien de roses utilise-t-il ?", "roses"),
          ("Il y a %d rangées de %d chaises dans la salle. Combien de chaises en tout ?", "chaises"),
          ("Un paquet contient %d sachets de %d bonbons. Combien de bonbons en tout ?", "bonbons"),
          ("Une voiture a 4 roues. Combien de roues ont %d voitures ? (%d)", None)]


def s5_prob():
    k = R.randint(0, 5)
    if k == 5:
        n = R.randint(3, 9)
        return mcq("Une voiture a 4 roues. Combien de roues ont %d voitures ?" % n, 4 * n, [4 + n, 4 * (n + 1), 4 * n - 1],
                   "%d %s 4 = <b>%d</b> roues." % (n, FOIS, 4 * n))
    if k == 4:
        p = K.next()
        a, b = R.randint(3, 9), R.randint(3, 9)
        return mcq("%s achète %d cahiers à %d € chacun. Combien paie-t-%s ?" % (p[0], a, b, p[1]), "%d €" % (a * b), ["%d €" % x for x in wrongs(a, b) if x != a * b],
                   "%d %s %d = <b>%d €</b>." % (a, FOIS, b, a * b))
    t, _ = SCENES[k]
    a, b = R.randint(3, 9), R.randint(3, 9)
    if k == 0:
        b = R.choice([6, 10, 12]) if R.random() < 0.3 else 6
        if b == 12:
            b = 6
    return mcq(t % (a, b), a * b, [x for x in wrongs(a, b) if x != a * b],
               "%d groupes de %d : %d %s %d = <b>%d</b>." % (a, b, a, FOIS, b, a * b))


def main():
    seen = set()
    sets = [
        ("Tables de 2, 3, 4 et 5", mix(R, seen, [(s1, 20)])),
        ("Tables de 6, 7, 8 et 9", mix(R, seen, [(s2, 20)])),
        ("Le facteur manquant", mix(R, seen, [(s3_manq, 20)])),
        ("Multiples, × 10 et × 100", mix(R, seen, [(s4_multiple, 8), (s4_10, 6), (s4_comm, 3), (s4_double, 3)])),
        ("Problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["%d %s %d, c’est <b>%d fois %d</b> : 4 + 4 + 4 + 4 + 4 + 4 = 24." % (6, FOIS, 4, 6, 4),
         "On peut <b>changer l’ordre</b> : 6 %s 4 = 4 %s 6. Il reste moins de résultats à apprendre." % (FOIS, FOIS),
         "Pour retrouver un résultat oublié, on part d’un résultat connu : 7 %s 8 = 7 %s 10 − 7 %s 2 = 70 − 14 = 56." % (FOIS, FOIS, FOIS),
         "Pour multiplier par 10, on écrit un 0 à droite : 23 %s 10 = 230." % FOIS],
        [example("Combien font 7 %s 6 ?" % FOIS, ["7 %s 5 = 35" % FOIS, "on ajoute encore 7 : 35 + 7 = 42"], "42")],
        [["Additionner : 6 %s 7 = 13" % FOIS, "6 %s 7, c’est 6 fois 7 : 42." % FOIS],
         ["Se tromper de ligne : 7 %s 8 = 63" % FOIS, "63, c’est 7 %s 9. Vérifie : 7 %s 8 = 56." % (FOIS, FOIS)],
         ["Oublier le 0 : 34 %s 10 = 34" % FOIS, "34 %s 10 = 340." % FOIS]],
        table(["%s" % FOIS] + [str(j) for j in range(1, 11)], [[str(i)] + [str(i * j) for j in range(1, 11)] for i in range(2, 10)]))
    faq = [("Quelles tables connaître au CE2 ?", "Toutes les tables de 2 à 9, à connaître par cœur à la fin de l’année."),
           ("Comment apprendre la table de 9 ?", "9 %s n = 10 %s n − n. Par exemple 9 %s 7 = 70 − 7 = 63." % (FOIS, FOIS, FOIS))]
    make_unit(R, "tables-de-multiplication", "N",
              "Connaître les tables de multiplication de 2 à 9 ; les utiliser pour trouver un produit ou un facteur manquant ; multiplier par 10 et par 100 ; utiliser la commutativité (résumé du programme 2024 du cycle 2).",
              "Les tables de multiplication de 2 à 9", "Tables de multiplication CE2 : fiches et exercices avec corrigé", "Tables de multiplication",
              "Fiches de maths CE2 sur les tables de multiplication de 2 à 9 : résultats, facteur manquant, multiples, × 10, × 100 et problèmes. 100 exercices corrigés.",
              "6 × 4, c’est 6 fois 4.", "On peut changer l’ordre : 6 × 4 = 4 × 6.",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
