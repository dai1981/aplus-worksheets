# -*- coding: utf-8 -*-
"""
France Maths CE2 : Les nombres jusqu’à 10 000 (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_nombres_jusqu_a_10000.py
Milliers, centaines, dizaines, unités ; tableau de numération ; écrire en chiffres et en lettres ; décomposer ;
chiffre des centaines et nombre de centaines ; suivant et précédent.
Erreurs : oublier le zéro (3 milliers 5 dizaines → 350), confondre chiffre et nombre de centaines, inverser deux chiffres.
"""
import random
from fr_c2 import pl
from fr_common import (mcq, num, lesson, example, make_unit, mix, blocs, numeration, lettres, Kids)

R = random.Random(51001)


def four():
    return R.randint(1001, 9999)


def parts(n):
    return n // 1000, n // 100 % 10, n // 10 % 10, n % 10


def wrong_place(n):
    m, c, d, u = parts(n)
    out = []
    if c == 0 or d == 0:
        out.append(int("".join(str(x) for x in (m, c, d, u) if x)) if any((m, c, d, u)) else None)
    out += [m * 1000 + d * 100 + c * 10 + u if c != d else None, n + 1000 if n + 1000 < 10000 else n - 1000, n + 100, n - 10]
    return [num(x) for x in out if x and 0 < x < 10000 and x != n]


def s1_blocs():
    m, c, d, u = R.randint(1, 3), R.randint(0, 6), R.randint(0, 9), R.randint(0, 9)
    n = 1000 * m + 100 * c + 10 * d + u
    return mcq(blocs(m, c, d, u) + "Quel nombre est représenté ?", num(n), wrong_place(n),
               "%s, %s, %s et %s : <b>%s</b>." % (pl(m, "millier"), pl(c, "centaine"), pl(d, "dizaine"), pl(u, "unité"), num(n)))


def s1_tableau():
    n = four()
    if R.random() < 0.4:
        n = n // 10 * 10 if R.random() < 0.5 else (n // 1000) * 1000 + n % 100
    return mcq(numeration(n) + "Quel nombre est écrit dans le tableau de numération ?", num(n), wrong_place(n),
               "On lit les chiffres de gauche à droite : m, c, d, u. Le nombre est <b>%s</b>." % num(n))


def s1_unites():
    m, c, d, u = R.randint(1, 9), R.choice([0, R.randint(1, 9)]), R.choice([0, R.randint(1, 9)]), R.randint(0, 9)
    n = 1000 * m + 100 * c + 10 * d + u
    words = []
    for v, w in ((m, "millier"), (c, "centaine"), (d, "dizaine"), (u, "unité")):
        if v:
            words.append("%d %s%s" % (v, w, "s" if v > 1 else ""))
    if len(words) < 2 or words == ["%d millier%s" % (m, "s" if m > 1 else "")]:
        return None
    R.shuffle(words)
    return mcq("Quel nombre a " + ", ".join(words[:-1]) + " et " + words[-1] + " ?", num(n), wrong_place(n),
               "Range chaque quantité à sa place (m, c, d, u) et mets 0 dans les colonnes vides : <b>%s</b>." % num(n))


def s2_lettres_vers():
    n = four()
    if R.random() < 0.5:
        n = n // 10 * 10
    return mcq("Écris en chiffres : <b>%s</b>." % lettres(n), num(n), wrong_place(n),
               "« %s » s’écrit <b>%s</b>." % (lettres(n), num(n)))


def s2_vers_lettres():
    n = four()
    w = [n + 10 if (n // 10) % 10 != 9 else n - 10, n + 100 if (n // 100) % 10 != 9 else n - 100, n + 1000 if n < 9000 else n - 1000, n + 1]
    return mcq("Comment s’écrit %s en lettres ?" % num(n), lettres(n), [lettres(x) for x in w if 0 < x < 10000],
               "%s s’écrit <b>%s</b>." % (num(n), lettres(n)))


def s3_decomp():
    n = four()
    m, c, d, u = parts(n)
    terms = [str(v) for v in (1000 * m, 100 * c, 10 * d, u) if v]
    if len(terms) < 3:
        return None
    sh = " + ".join(num(int(t)) for t in terms)
    if R.random() < 0.5:
        return mcq("Quel nombre est égal à %s ?" % sh, num(n), wrong_place(n), "%s = <b>%s</b>." % (sh, num(n)))
    right = sh
    w1 = " + ".join(num(int(t)) for t in [str(1000 * m), str(10 * c), str(d), str(u)] if int(t))
    w2 = " + ".join(num(int(t)) for t in [str(100 * m), str(100 * c), str(10 * d), str(u)] if int(t))
    w3 = " + ".join(num(int(t)) for t in [str(1000 * m), str(100 * d), str(10 * c), str(u)] if int(t))
    return mcq("Quelle décomposition est celle de %s ?" % num(n), right, [w1, w2, w3],
               "%s = %s + %s + %s + %s = <b>%s</b>." % (num(n), pl(m, "millier"), pl(c, "centaine"), pl(d, "dizaine"), pl(u, "unité"), right))


def s3_chiffre():
    n = four()
    m, c, d, u = parts(n)
    k = R.choice(["cchiffre", "dchiffre", "cnombre", "dnombre", "mchiffre"])
    if k == "cchiffre":
        return mcq("Quel est le chiffre des centaines de %s ?" % num(n), str(c), [str(d), str(m), str(n // 100), str(u)],
                   "Dans %s, le chiffre des centaines est le 2<sup>e</sup> en partant de la gauche : <b>%d</b>." % (num(n), c))
    if k == "dchiffre":
        return mcq("Quel est le chiffre des dizaines de %s ?" % num(n), str(d), [str(c), str(u), str(n // 10), str(m)],
                   "Le chiffre des dizaines est juste avant celui des unités : <b>%d</b>." % d)
    if k == "mchiffre":
        return mcq("Quel est le chiffre des milliers de %s ?" % num(n), str(m), [str(c), str(u), str(d), str(m + 1)],
                   "Le chiffre des milliers est le premier à gauche : <b>%d</b>." % m)
    if k == "cnombre":
        return mcq("Combien y a-t-il de centaines en tout dans %s ?" % num(n), num(n // 100), [str(c), num(n // 10), str(m), num(n // 100 + 1)],
                   "%s = %s centaines et %d unités, donc le nombre de centaines est <b>%s</b> (le chiffre des centaines est seulement %d)." % (num(n), num(n // 100), n % 100, num(n // 100), c))
    return mcq("Combien y a-t-il de dizaines en tout dans %s ?" % num(n), num(n // 10), [str(d), num(n // 100), num(n // 10 + 1), str(c)],
               "%s = %s dizaines et %d unités, donc il y a <b>%s</b> dizaines en tout." % (num(n), num(n // 10), u, num(n // 10)))


def s4_voisins():
    n = four()
    k = R.choice(["suiv", "prec", "plus10", "plus100", "moins100", "plus1000"])
    if k == "suiv":
        if n % 10 != 9 and R.random() < 0.6:
            n = n // 10 * 10 + 9
        return mcq("Quel est le nombre qui suit %s ?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n // 10 * 10 + 10 + 0) if n % 10 != 9 else num(n + 11)],
                   "Le suivant, c’est %s + 1 = <b>%s</b>." % (num(n), num(n + 1)))
    if k == "prec":
        if R.random() < 0.6:
            n = n // 100 * 100
        if n < 1001:
            return None
        return mcq("Quel est le nombre qui précède %s ?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 101) if n > 1101 else num(n - 2)],
                   "Le précédent, c’est %s − 1 = <b>%s</b>." % (num(n), num(n - 1)))
    if k == "plus10":
        n = n // 100 * 100 + 90 + R.randint(0, 9)
        if n + 10 >= 10000:
            return None
        return mcq("Ajoute 1 dizaine à %s." % num(n), num(n + 10), [num(n + 1), num(n + 100), num(n - 90)],
                   "%s + 10 = <b>%s</b> : on change de centaine." % (num(n), num(n + 10)))
    if k == "plus100":
        n = n // 1000 * 1000 + 900 + R.randint(0, 99)
        if n + 100 >= 10000:
            return None
        return mcq("Ajoute 1 centaine à %s." % num(n), num(n + 100), [num(n + 10), num(n + 1000) if n + 1000 < 10000 else num(n - 100), num(n - 900)],
                   "%s + 100 = <b>%s</b> : on change de millier." % (num(n), num(n + 100)))
    if k == "moins100":
        if n < 1100:
            return None
        return mcq("Enlève 100 à %s." % num(n), num(n - 100), [num(n - 10), num(n - 1000), num(n + 100)],
                   "%s − 100 = <b>%s</b>." % (num(n), num(n - 100)))
    if n > 8999:
        return None
    return mcq("Ajoute 1 000 à %s." % num(n), num(n + 1000), [num(n + 100), num(n + 10), num(n - 1000) if n > 1999 else num(n + 1)],
               "%s + 1 000 = <b>%s</b> : seul le chiffre des milliers change." % (num(n), num(n + 1000)))


def s5_devinette():
    m, c, d, u = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9), R.randint(0, 9)
    if len({m, c, d, u}) < 4:
        return None
    n = 1000 * m + 100 * c + 10 * d + u
    clues = ["mon chiffre des milliers est %d" % m, "mon chiffre des centaines est %d" % c, "mon chiffre des dizaines est %d" % d, "mon chiffre des unités est %d" % u]
    R.shuffle(clues)
    return mcq("Devinette : %s. Qui suis-je ?" % "; ".join(clues).replace("; ", " ; "), num(n),
               [num(1000 * m + 100 * d + 10 * c + u), num(1000 * u + 100 * d + 10 * c + m), num(1000 * c + 100 * m + 10 * d + u)],
               "On place chaque chiffre dans sa colonne : m = %d, c = %d, d = %d, u = %d. Le nombre est <b>%s</b>." % (m, c, d, u, num(n)))


def s5_probleme():
    k = R.choice(["billets", "carnets", "boites"])
    m, c, d = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
    if k == "billets":
        tot = 1000 * m + 100 * c + 10 * d
        return mcq("Une caisse contient %d billets de 1 000 €, %d billets de 100 € et %d billets de 10 €. Quelle somme y a-t-il ?" % (m, c, d), num(tot) + " €",
                   [num(m + c + d) + " €", num(1000 * m + 10 * c + d) + " €", num(100 * m + 10 * c + d) + " €"],
                   "%s + %s + %s = <b>%s €</b>." % (num(1000 * m), num(100 * c), num(10 * d), num(tot)))
    if k == "carnets":
        n = R.randint(1200, 9800)
        return mcq("Une imprimerie range %s tickets en carnets de 100. Combien de carnets complets obtient-elle ?" % num(n), num(n // 100),
                   [str(n // 100 % 10), num(n // 10), num(n // 1000)],
                   "Il y a %s centaines dans %s, donc <b>%s</b> carnets complets." % (num(n // 100), num(n), num(n // 100)))
    n = R.randint(1100, 9900)
    return mcq("On range %s perles dans des boîtes de 10. Combien de boîtes pleines peut-on remplir ?" % num(n), num(n // 10),
               [str(n // 10 % 10), num(n // 100), num(n // 10 + 1)],
               "Le nombre de dizaines de %s est %s : <b>%s</b> boîtes pleines." % (num(n), num(n // 10), num(n // 10)))


def main():
    seen = set()
    sets = [
        ("Milliers, centaines, dizaines, unités", mix(R, seen, [(s1_blocs, 8), (s1_tableau, 6), (s1_unites, 6)])),
        ("Lire et écrire les nombres", mix(R, seen, [(s2_lettres_vers, 10), (s2_vers_lettres, 10)])),
        ("Décomposer un nombre", mix(R, seen, [(s3_decomp, 10), (s3_chiffre, 10)])),
        ("Suivant, précédent, + 10, + 100, + 1 000", mix(R, seen, [(s4_voisins, 20)])),
        ("Devinettes et problèmes", mix(R, seen, [(s5_devinette, 8), (s5_probleme, 12)])),
    ]
    body = lesson(
        ["Un nombre jusqu’à 9 999 a au plus <b>4 chiffres</b> : milliers (m), centaines (c), dizaines (d), unités (u).",
         "1 millier = 10 centaines = 100 dizaines = 1 000 unités.",
         "Quand une colonne est vide, on écrit un <b>0</b> : 3 milliers et 5 dizaines, c’est 3 050.",
         "Le <b>chiffre</b> des centaines de 4 725 est 7, mais le <b>nombre</b> de centaines est 47."],
        [example("Écris le nombre : 6 milliers, 2 dizaines et 9 unités.", ["m = 6, c = 0, d = 2, u = 9"], "6 029"),
         example("Combien de dizaines en tout dans 3 480 ?", ["3 480 = 348 dizaines"], "348 dizaines")],
        [["Oublier le 0 : 3 milliers 5 dizaines → 350", "Mets un 0 dans chaque colonne vide : 3 050."],
         ["Confondre chiffre et nombre de centaines", "Le chiffre est 1 seul chiffre ; le nombre compte tous les milliers en plus."],
         ["Inverser deux chiffres : 4 725 → 4 752", "Lis les colonnes dans l’ordre m, c, d, u."]],
        numeration(4725))
    faq = [("Jusqu’à quel nombre va-t-on en CE2 ?", "Jusqu’à 9 999 : on lit, écrit et décompose les nombres de 4 chiffres, et on compte jusqu’à 10 000."),
           ("Pourquoi écrit-on 4 536 avec un espace ?", "On sépare les chiffres par groupes de trois en partant de la droite pour lire plus facilement les milliers.")]
    make_unit(R, "nombres-jusqu-a-10-000", "N",
              "Connaître les unités de numération (unités, dizaines, centaines, milliers) et leurs relations ; lire et écrire les nombres jusqu’à 9 999 en chiffres et en lettres ; passer d’une représentation à une autre (matériel, écriture en chiffres, en lettres, décompositions) (résumé du programme 2024 du cycle 2).",
              "Les nombres jusqu’à 10 000 : milliers, centaines, dizaines et unités", "Les nombres jusqu’à 10 000 CE2 : fiches et exercices avec corrigé",
              "Nombres jusqu’à 10 000",
              "Fiches de maths CE2 sur les nombres jusqu’à 10 000 : tableau de numération, écrire en chiffres et en lettres, décomposer, chiffre et nombre de centaines. 100 exercices corrigés.",
              "Chaque chiffre a une valeur selon sa place : m, c, d, u.", "Dans une colonne vide, on écrit 0.",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
