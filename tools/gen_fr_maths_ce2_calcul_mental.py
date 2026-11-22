# -*- coding: utf-8 -*-
"""
France Maths CE2 : Calcul mental (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_calcul_mental.py
Doubles et moitiés, compléments à la dizaine, à 100 et à 1 000, ajouter ou soustraire 9, 19, 29…, multiplier par 10
et par 100, ajouter des dizaines et des centaines, petits problèmes.
Erreurs : + 9 compté comme + 10, moitié de 70 = 30, oublier un 0 en multipliant par 100, complément à 100 de 35 = 75.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids

R = random.Random(51003)
K = Kids(R)


def s1_double():
    k = R.choice(["d", "d", "m", "m"])
    if k == "d":
        n = R.choice([R.randint(11, 49), R.randint(5, 75) * 1 if R.random() < 0.3 else R.randint(1, 6) * 100 + R.choice([0, 50]), R.randint(2, 9) * 10 + 5])
        return mcq("Quel est le double de %s ?" % num(n), num(2 * n), [num(2 * n + 10), num(n + 2), num(2 * n - 10), num(n // 2) if n % 2 == 0 else num(2 * n + 1)],
                   "Le double, c’est 2 fois le nombre : %s + %s = <b>%s</b>." % (num(n), num(n), num(2 * n)))
    n = R.choice([R.randint(2, 40) * 2, R.randint(4, 15) * 10, R.randint(2, 12) * 100])
    h = n // 2
    return mcq("Quelle est la moitié de %s ?" % num(n), num(h), [num(h + 5) if n % 20 else num(h + 10), num(2 * n), num(h - 5) if h > 5 else num(h + 1), num(n - 2)],
               "La moitié, c’est partager en 2 parts égales : %s + %s = %s, donc la moitié est <b>%s</b>." % (num(h), num(h), num(n), num(h)))


def s2_comp():
    k = R.choice(["100", "100", "1000", "diz"])
    if k == "100":
        a = R.randint(11, 89)
        if a % 10 == 0:
            return None
        return mcq("Combien faut-il ajouter à %d pour faire 100 ?" % a, str(100 - a), [str(110 - a), str(90 - a), str(a)],
                   "%d + %d = 100. (Attention : %d + %d = %d, pas 100.)" % (a, 100 - a, a, 110 - a, 110) if False else
                   "%d pour aller à %d, puis %d pour aller à 100 : <b>%d</b>." % ((a // 10 + 1) * 10 - a, (a // 10 + 1) * 10, 100 - (a // 10 + 1) * 10, 100 - a))
    if k == "1000":
        a = R.randint(1, 19) * 50 if R.random() < 0.5 else R.randint(11, 99) * 10
        if a % 100 == 0:
            return None
        return mcq("Combien faut-il ajouter à %s pour faire 1 000 ?" % num(a), num(1000 - a), [num(1100 - a), num(900 - a), num(1000 - a + 10)],
                   "%s + %s = 1 000 : <b>%s</b>." % (num(a), num(1000 - a), num(1000 - a)))
    a = R.randint(101, 989)
    if a % 10 == 0:
        return None
    up = (a // 10 + 1) * 10
    return mcq("Quel est le complément de %s à la dizaine suivante ?" % num(a), str(up - a), [str(10 - (up - a)), str(up - a + 10), num(up)],
               "La dizaine suivante est %s : %s + %d = %s. Le complément est <b>%d</b>." % (num(up), num(a), up - a, num(up), up - a))


def s3_neuf():
    a = R.randint(120, 980)
    b = R.choice([9, 19, 29, 39, 8, 18, 28, 38])
    if R.random() < 0.5:
        r = a + b
        return mcq("Calcule : %s + %d" % (num(a), b), num(r), [num(r + 1), num(r - 1) if b % 10 == 9 else num(r + 2), num(a + b + 10)],
                   "Ajouter %d, c’est ajouter %d puis enlever %d : %s + %d − %d = <b>%s</b>." % (b, b + (10 - b % 10), 10 - b % 10, num(a), b + (10 - b % 10), 10 - b % 10, num(r)))
    r = a - b
    return mcq("Calcule : %s − %d" % (num(a), b), num(r), [num(r - 1), num(r + 1) if b % 10 == 9 else num(r - 2), num(a - b - 10)],
               "Enlever %d, c’est enlever %d puis ajouter %d : %s − %d + %d = <b>%s</b>." % (b, b + (10 - b % 10), 10 - b % 10, num(a), b + (10 - b % 10), 10 - b % 10, num(r)))


def s4_dix():
    k = R.choice(["x10", "x100", "x10", "ad"])
    if k == "x10":
        n = R.randint(12, 950)
        return mcq("Calcule : %s × 10" % num(n), num(n * 10), [num(n * 100), num(n + 10), num(n * 10 + 10)],
                   "Multiplier par 10 : chaque chiffre prend une valeur 10 fois plus grande, on écrit un 0 à droite : <b>%s</b>." % num(n * 10))
    if k == "x100":
        n = R.randint(2, 99)
        return mcq("Calcule : %s × 100" % num(n), num(n * 100), [num(n * 10), num(n * 1000), num(n + 100)],
                   "Multiplier par 100 : on écrit deux 0 à droite : <b>%s</b>." % num(n * 100))
    a = R.randint(1000, 8900)
    b = R.choice([R.randint(2, 9) * 10, R.randint(2, 9) * 100, R.randint(1, 9) * 1000])
    if a + b > 9999:
        return None
    return mcq("Calcule : %s + %s" % (num(a), num(b)), num(a + b), [num(a + b // 10), num(a + b * 10) if a + b * 10 < 10000 else num(a + b + 1), num(a + b - 10)],
               "On ajoute seulement au chiffre des %s : <b>%s</b>." % ({10: "dizaines", 100: "centaines", 1000: "milliers"}[10 ** (len(str(b)) - 1)], num(a + b)))


def s5_prob():
    k = R.choice(["double", "moitie", "comp", "fois10"])
    p = K.next()
    if k == "double":
        n = R.randint(15, 45)
        return mcq("%s a %d billes. Sa sœur en a le double. Combien de billes a sa sœur ?" % (p[0], n), str(2 * n), [str(n + 2), str(n // 2), str(2 * n + 10)],
                   "Le double de %d est %d + %d = <b>%d</b>." % (n, n, n, 2 * n))
    if k == "moitie":
        n = R.randint(5, 40) * 2
        return mcq("%s a %d images. %s en donne la moitié à son frère. Combien en donne-t-%s ?" % (p[0], n, p[1].capitalize(), p[1]), str(n // 2), [str(n * 2), str(n - 2), str(n // 2 + 5)],
                   "La moitié de %d est <b>%d</b>." % (n, n // 2))
    if k == "comp":
        a = R.randint(21, 89)
        return mcq("Un livre a 100 pages. %s en a lu %d. Combien de pages lui reste-t-il à lire ?" % (p[0], a), str(100 - a), [str(110 - a), str(a), str(90 - a)],
                   "%d + ? = 100 : il reste <b>%d</b> pages." % (a, 100 - a))
    n = R.randint(12, 60)
    return mcq("Un paquet contient 10 crayons. Combien de crayons y a-t-il dans %d paquets ?" % n, num(n * 10), [num(n + 10), num(n * 100), num(n * 10 + 10)],
               "%d × 10 = <b>%s</b> crayons." % (n, num(n * 10)))


def main():
    seen = set()
    sets = [
        ("Doubles et moitiés", mix(R, seen, [(s1_double, 20)])),
        ("Compléments", mix(R, seen, [(s2_comp, 20)])),
        ("Ajouter ou enlever 9, 19, 29…", mix(R, seen, [(s3_neuf, 20)])),
        ("Multiplier par 10 et 100", mix(R, seen, [(s4_dix, 20)])),
        ("Petits problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["Le <b>double</b> d’un nombre, c’est ce nombre ajouté à lui-même. La <b>moitié</b>, c’est partager en 2 parts égales.",
         "Pour ajouter 9, ajoute 10 puis enlève 1. Pour ajouter 19, ajoute 20 puis enlève 1.",
         "Pour trouver le complément à 100, va d’abord à la dizaine suivante, puis à 100.",
         "Multiplier par 10, c’est écrire un 0 à droite ; par 100, deux 0."],
        [example("Calcule 347 + 29.", ["347 + 30 = 377", "377 − 1 = 376"], "376"),
         example("Complément de 63 à 100.", ["63 + 7 = 70", "70 + 30 = 100", "7 + 30 = 37"], "37")],
        [["347 + 9 = 357 (on a ajouté 10)", "Après + 10, enlève 1 : 356."],
         ["Moitié de 70 = 30", "35 + 35 = 70, donc la moitié est 35."],
         ["Complément de 35 à 100 = 75", "35 + 65 = 100 : le complément est 65."]])
    faq = [("Pourquoi faire du calcul mental tous les jours ?", "Il aide à calculer vite et juste, et à vérifier les opérations posées."),
           ("Comment trouver vite la moitié d’un grand nombre ?", "Partage les centaines, les dizaines et les unités : la moitié de 860 est 400 + 30 = 430.")]
    make_unit(R, "calcul-mental", "N",
              "Mémoriser des faits numériques (doubles, moitiés, compléments, tables) et utiliser des procédures de calcul mental : ajouter ou soustraire 9, 19, 29…, multiplier par 10 et par 100, trouver la moitié d’un nombre pair en le décomposant (résumé du programme 2024 du cycle 2).",
              "Calcul mental : doubles, moitiés, compléments et × 10", "Calcul mental CE2 : fiches et exercices avec corrigé", "Calcul mental",
              "Fiches de calcul mental CE2 : doubles et moitiés, compléments à 100 et à 1 000, ajouter 9 ou 19, multiplier par 10 et 100. 100 exercices corrigés.",
              "Pour ajouter 9, ajoute 10 et enlève 1.", "Pour × 10, écris un 0 à droite.",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
