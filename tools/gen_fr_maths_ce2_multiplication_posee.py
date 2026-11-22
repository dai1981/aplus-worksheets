# -*- coding: utf-8 -*-
"""
France Maths CE2 : La multiplication posée (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_multiplication_posee.py
Multiplier un nombre de 2 ou 3 chiffres par un nombre à 1 chiffre, puis à 2 chiffres ; multiples de 10 ; problèmes.
Erreurs : oublier la retenue (47 × 3 → 121), oublier le décalage de la 2e ligne (34 × 12 → 102), multiplier seulement les unités.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, posee, Kids, FOIS

R = random.Random(51007)
K = Kids(R)


def no_carry(a, b):
    """oublier les retenues : 47 × 3 → 12 puis 1 → 121"""
    ds = [int(d) for d in str(a)]
    s = str(ds[0] * b) + "".join(str(d * b % 10) for d in ds[1:])
    return int(s)


def one(a, b):
    p = a * b
    w = [no_carry(a, b), p + 10, p - 10, a * (b + 1), a + b * 10]
    e = "On multiplie %d par chaque chiffre de %d, de droite à gauche, en ajoutant les retenues. %d %s %d = <b>%s</b>." % (b, a, a, FOIS, b, num(p))
    return mcq(posee([str(a), str(b)], op=FOIS) + "Calcule en posant l’opération : %d %s %d" % (a, FOIS, b), num(p), [num(x) for x in w if x > 0 and x != p], e)


def s1():
    a, b = R.randint(12, 49), R.randint(2, 5)
    return one(a, b)


def s2():
    a, b = R.randint(23, 99), R.randint(3, 9)
    if a % 10 * b < 10:
        return None
    return one(a, b)


def s3():
    a, b = R.randint(102, 899), R.randint(2, 9)
    if a * b > 9999:
        return None
    return one(a, b)


def s4_two():
    a, b = R.randint(13, 98), R.randint(11, 39)
    if b % 10 == 0 or a * b > 9999:
        return None
    u, d = b % 10, b // 10
    p = a * b
    w = [a * u + a * d, a * u + a, a * u * 10 + a * d, p + 100, p - 10]
    e = "%d %s %d = %s ; %d %s %d0 = %s (on décale : on écrit un 0) ; %s + %s = <b>%s</b>." % (
        a, FOIS, u, num(a * u), a, FOIS, d, num(a * d * 10), num(a * u), num(a * d * 10), num(p))
    return mcq(posee([str(a), str(b)], op=FOIS) + "Calcule en posant l’opération : %d %s %d" % (a, FOIS, b), num(p), [num(x) for x in w if x > 0 and x != p], e)


def s4_dix():
    a, b = R.randint(12, 99), R.choice([20, 30, 40, 50, 60])
    p = a * b
    return mcq("Calcule : %d %s %d" % (a, FOIS, b), num(p), [num(a * (b // 10)), num(p * 10), num(a * (b // 10) + 10)],
               "%d %s %d = %d %s %d %s 10 = %s %s 10 = <b>%s</b>." % (a, FOIS, b, a, FOIS, b // 10, FOIS, num(a * (b // 10)), FOIS, num(p)))


def s5_prob():
    p = K.next()
    k = R.choice(["car", "page", "prix", "jour", "carton"])
    if k == "car":
        a, b = R.randint(3, 9), R.randint(42, 59)
        q = "Une école réserve %d cars de %d places. Combien de places y a-t-il en tout ?" % (a, b)
        u = ""
    elif k == "page":
        a, b = R.randint(12, 28), R.randint(24, 48)
        q = "%s lit %d pages par jour pendant %d jours. Combien de pages lit-%s ?" % (p[0], b, a, p[1])
        u = ""
    elif k == "prix":
        a, b = R.randint(3, 9), R.randint(125, 489)
        q = "Une famille achète %d vélos à %d € chacun. Combien paie-t-elle ?" % (a, b)
        u = " €"
    elif k == "jour":
        a, b = R.randint(12, 31), 24
        q = "Combien d’heures y a-t-il dans %d jours ?" % a
        u = " h"
    else:
        a, b = R.randint(15, 45), R.choice([12, 18, 24, 36])
        q = "Un magasin reçoit %d cartons de %d bouteilles. Combien de bouteilles en tout ?" % (a, b)
        u = ""
    r = a * b
    w = [a + b, r + 10, no_carry(max(a, b), min(a, b)) if min(a, b) < 10 else a * (b % 10) + a * (b // 10), r - 10]
    return mcq(q, num(r) + u, [num(x) + u for x in w if x > 0 and x != r], "%d %s %d = <b>%s%s</b>." % (a, FOIS, b, num(r), u))


def main():
    seen = set()
    sets = [
        ("2 chiffres × 1 chiffre", mix(R, seen, [(s1, 20)])),
        ("Avec des retenues", mix(R, seen, [(s2, 20)])),
        ("3 chiffres × 1 chiffre", mix(R, seen, [(s3, 20)])),
        ("Multiplier par un nombre à 2 chiffres", mix(R, seen, [(s4_two, 14), (s4_dix, 6)])),
        ("Problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["On multiplie le chiffre du bas par <b>chaque chiffre du haut</b>, de droite à gauche.",
         "Si un produit fait 10 ou plus, on écrit les unités et on <b>retient</b> les dizaines pour la colonne suivante.",
         "Pour multiplier par 23, on calcule %s 3, puis %s 20 (on écrit un <b>0</b> au début de la 2e ligne), puis on additionne." % (FOIS, FOIS)],
        [example("47 %s 3" % FOIS, ["7 %s 3 = 21 : j’écris 1, je retiens 2" % FOIS, "4 %s 3 = 12, plus 2 = 14" % FOIS], "141"),
         example("34 %s 12" % FOIS, ["34 %s 2 = 68" % FOIS, "34 %s 10 = 340" % FOIS, "68 + 340 = 408"], "408")],
        [["Oublier la retenue : 47 %s 3 = 121" % FOIS, "Ajoute la retenue 2 aux dizaines : 141."],
         ["Oublier le 0 de la 2e ligne : 34 %s 12 = 68 + 34 = 102" % FOIS, "La 2e ligne vaut 34 %s 10 = 340 : 408." % FOIS],
         ["Multiplier seulement les unités", "Chaque chiffre du haut est multiplié."]])
    faq = [("Faut-il connaître les tables ?", "Oui : chaque étape de la multiplication posée utilise un résultat des tables."),
           ("Comment vérifier ?", "Avec un ordre de grandeur : 47 %s 3, c’est environ 50 %s 3 = 150." % (FOIS, FOIS))]
    make_unit(R, "multiplication-posee", "N",
              "Calculer en colonnes le produit d’un nombre de deux ou trois chiffres par un nombre à un ou deux chiffres ; multiplier par 10 et par un multiple de 10 ; résoudre des problèmes multiplicatifs (résumé du programme 2024 du cycle 2).",
              "La multiplication posée", "Multiplication posée CE2 : fiches et exercices avec corrigé", "Multiplication posée",
              "Fiches de maths CE2 sur la multiplication posée : 2 et 3 chiffres par 1 chiffre, avec retenues, par un nombre à 2 chiffres et problèmes. 100 exercices corrigés.",
              "On multiplie chaque chiffre, de droite à gauche, avec les retenues.", "Pour × 23 : × 3, puis × 20 (avec un 0), puis on additionne.",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
