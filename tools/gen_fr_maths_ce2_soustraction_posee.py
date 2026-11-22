# -*- coding: utf-8 -*-
"""
France Maths CE2 : La soustraction posée (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_soustraction_posee.py
Soustractions posées jusqu’à 4 chiffres, sans et avec retenues, avec des zéros, vérifier par l’addition, problèmes
(reste, écart, combien de plus).
Erreurs : soustraire le petit chiffre du grand dans chaque colonne (523 − 278 → 355), oublier la retenue, problème
d’écart résolu par une addition.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, posee, Kids

R = random.Random(51005)
K = Kids(R)


def digits(n, k=4):
    return [int(d) for d in str(n).rjust(k, "0")][::-1]


def borrows(a, b):
    da, db = digits(a), digits(b)
    c, n = 0, 0
    for k in range(4):
        if da[k] - db[k] - c < 0:
            n += 1
            c = 1
        else:
            c = 0
    return n


def flip(a, b):
    """petit du grand dans chaque colonne"""
    da, db = digits(a), digits(b)
    return int("".join(str(abs(da[k] - db[k])) for k in (3, 2, 1, 0)))


def no_borrow(a, b):
    da, db = digits(a), digits(b)
    return int("".join(str((da[k] - db[k]) % 10) for k in (3, 2, 1, 0)))


def task(a, b, need=None):
    if b >= a:
        return None
    n = borrows(a, b)
    if need is not None and (n != need if need < 2 else n < 2):
        return None
    r = a - b
    w = [flip(a, b) if n else None, no_borrow(a, b) if n else None, r + 10, r - 10, r + 100, a + b if a + b < 10000 else None]
    e = "On aligne les unités et on calcule de droite à gauche."
    if n:
        e += " Quand le chiffre du haut est trop petit, on ajoute 10 en haut et 1 au chiffre du bas de la colonne suivante (retenue)."
    e += " %s − %s = <b>%s</b>. Vérification : %s + %s = %s." % (num(a), num(b), num(r), num(r), num(b), num(a))
    return mcq(posee([str(a), str(b)], op="−") + "Calcule en posant l’opération : %s − %s" % (num(a), num(b)), num(r),
               [num(x) for x in w if x and 0 < x < 10000 and x != r], e)


def s1():
    return task(R.randint(2000, 9999), R.randint(100, 1999), 0)


def s2():
    return task(R.randint(2000, 9999), R.randint(100, 4999), 1)


def s3():
    return task(R.randint(3000, 9999), R.randint(1000, 5999), 2)


def s4_zero():
    a = R.choice([R.randint(2, 9) * 1000, R.randint(2, 9) * 1000 + R.randint(1, 9) * 100, R.randint(1, 9) * 1000 + R.randint(1, 9) * 10])
    return task(a, R.randint(101, a - 100))


def s4_verif():
    a, b = R.randint(1500, 9000), R.randint(200, 1400)
    r = a - b
    return mcq("%s − %s = %s. Quelle addition permet de vérifier ce calcul ?" % (num(a), num(b), num(r)), "%s + %s = %s" % (num(r), num(b), num(a)),
               ["%s + %s = %s" % (num(a), num(b), num(a + b)), "%s − %s = %s" % (num(a), num(r), num(b)), "%s + %s = %s" % (num(r), num(a), num(r + a))],
               "La différence plus le nombre enlevé redonne le premier nombre : <b>%s + %s = %s</b>." % (num(r), num(b), num(a)))


def s5_prob():
    p = K.next()
    a, b = R.randint(1500, 9800), R.randint(250, 1490)
    r = a - b
    k = R.choice(["reste", "ecart", "plus", "manque"])
    wr = [num(a + b) if a + b < 10000 else num(r + 100), num(flip(a, b)) if borrows(a, b) else num(r + 10), num(r - 10)]
    if k == "reste":
        return mcq("Un camion transporte %s kg de sable. Il en décharge %s kg. Combien de kilogrammes reste-t-il ?" % (num(a), num(b)), num(r) + " kg", [w + " kg" for w in wr],
                   "%s − %s = <b>%s kg</b>." % (num(a), num(b), num(r)))
    if k == "ecart":
        a, b = R.randint(1200, 2025), R.randint(1100, 1950)
        if a <= b:
            return None
        return mcq("Le pont A a été construit en %d et le pont B en %d. Combien d’années les séparent ?" % (b, a), str(a - b), [str(a + b), str(a - b + 10), str(a - b - 1)],
                   "On cherche l’écart : %d − %d = <b>%d</b> ans." % (a, b, a - b))
    if k == "plus":
        return mcq("Une ville A a %s habitants et une ville B en a %s. Combien d’habitants la ville A a-t-elle de plus ?" % (num(a), num(b)), num(r), wr,
                   "Pour trouver « de plus », on calcule l’écart : %s − %s = <b>%s</b>." % (num(a), num(b), num(r)))
    return mcq("Un club veut récolter %s € pour un voyage. Il a déjà %s €. Combien lui manque-t-il ?" % (num(a), num(b)), num(r) + " €", [w + " €" for w in wr],
               "%s − %s = <b>%s €</b>." % (num(a), num(b), num(r)))


def main():
    seen = set()
    sets = [
        ("Sans retenue", mix(R, seen, [(s1, 20)])),
        ("Avec une retenue", mix(R, seen, [(s2, 20)])),
        ("Avec plusieurs retenues", mix(R, seen, [(s3, 20)])),
        ("Avec des zéros et vérification", mix(R, seen, [(s4_zero, 12), (s4_verif, 8)])),
        ("Problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["On pose le plus grand nombre en haut et on <b>aligne les unités</b>.",
         "On calcule de droite à gauche. Si le chiffre du haut est plus petit, on <b>ajoute 10</b> en haut et on ajoute 1 au chiffre du bas de la colonne suivante : c’est la retenue.",
         "On vérifie avec une addition : différence + nombre enlevé = premier nombre."],
        [example("5 324 − 1 687", ["u : 4 − 7 impossible → 14 − 7 = 7, retenue", "d : 2 − (8 + 1) impossible → 12 − 9 = 3, retenue", "c : 3 − (6 + 1) impossible → 13 − 7 = 6, retenue ; m : 5 − (1 + 1) = 3"], "3 637")],
        [["Enlever le petit du grand dans chaque colonne : 523 − 278 = 355", "On enlève toujours le chiffre du bas : 523 − 278 = 245."],
         ["Oublier d’ajouter la retenue en bas", "Écris la retenue sous le chiffre de la colonne suivante."],
         ["Additionner pour trouver un écart", "« Combien de plus ? » se calcule avec une soustraction."]])
    faq = [("Quelle technique de soustraction utilise-t-on ?", "Ici, la technique par compensation (on ajoute 10 en haut et 1 en bas). Si ta classe emprunte à la colonne voisine, le résultat est le même."),
           ("Comment savoir si on doit soustraire dans un problème ?", "Quand on cherche ce qui reste, ce qui manque ou un écart entre deux nombres.")]
    make_unit(R, "soustraction-posee", "N",
              "Calculer en colonnes des soustractions de nombres entiers ayant jusqu’à 4 chiffres avec une technique usuelle ; contrôler le résultat par une addition ; résoudre des problèmes de recherche d’un reste, d’un manque ou d’un écart (résumé du programme 2024 du cycle 2).",
              "La soustraction posée avec retenues", "Soustraction posée CE2 : fiches et exercices avec corrigé", "Soustraction posée",
              "Fiches de maths CE2 sur la soustraction posée : sans et avec retenues, avec des zéros, vérification par l’addition et problèmes d’écart. 100 exercices corrigés.",
              "On aligne les unités et on calcule de droite à gauche.", "On vérifie : différence + nombre enlevé = premier nombre.",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
