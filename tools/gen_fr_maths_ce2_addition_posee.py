# -*- coding: utf-8 -*-
"""
France Maths CE2 : L’addition posée (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_ce2_addition_posee.py
Additions posées de 2 ou 3 nombres jusqu’à 4 chiffres, avec ou sans retenues, chiffres manquants, estimation,
problèmes.
Erreurs : oublier la retenue (345 + 238 → 573), mal aligner les chiffres (345 + 42 → 765), écrire 13 dans une colonne.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, posee, Kids

R = random.Random(51004)
K = Kids(R)


def digits(n, k=4):
    return [int(d) for d in str(n).rjust(k, "0")][::-1]


def carries(nums):
    out, c = {}, 0
    for k in range(4):
        s = sum(digits(x)[k] for x in nums) + c
        c = s // 10
        if c and k < 3:
            out[k + 1] = c
    return out


def no_carry(nums):
    return int("".join(str(sum(digits(x)[k] for x in nums) % 10) for k in (3, 2, 1, 0)))


def misaligned(nums):
    big = max(nums)
    out = 0
    for x in nums:
        out += x * (10 ** (len(str(big)) - len(str(x))))
    return out


def task(nums, need=None):
    r = sum(nums)
    if r > 9999 or (need is not None and len(carries(nums)) != need):
        return None
    w = [no_carry(nums) if carries(nums) else None, r + 10, r - 10, r + 100, r + 1]
    if len({len(str(x)) for x in nums}) > 1:
        w.insert(0, misaligned(nums))
    cs = carries(nums)
    e = "On pose les nombres en alignant les unités, puis on calcule de droite à gauche."
    if cs:
        e += " Retenues : %s." % ", ".join("1 %s" % {1: "dizaine", 2: "centaine", 3: "millier"}[k] if v == 1 else "%d %ss" % (v, {1: "dizaine", 2: "centaine", 3: "millier"}[k]) for k, v in sorted(cs.items()))
    e += " Résultat : <b>%s</b>." % num(r)
    return mcq(posee([str(x) for x in nums]) + "Calcule en posant l’opération : %s" % " + ".join(num(x) for x in nums), num(r),
               [num(x) for x in w if x and 0 < x < 10000 and x != r], e)


def s1():
    return task([R.randint(1011, 6888), R.randint(101, 2111)], 0)


def s2():
    return task([R.randint(1105, 6889), R.randint(105, 2489)], 1)


def s3():
    return task([R.randint(1156, 6589), R.randint(156, 2489)], R.choice([2, 3]))


def s3b():
    b = R.randint(12, 98)
    return task([R.randint(1205, 8889), b])


def s4_trois():
    nums = [R.randint(101, 3999), R.randint(101, 2999), R.randint(12, 999)]
    if not carries(nums):
        return None
    return task(nums)


def s4_manquant():
    a, b = R.randint(1105, 6889), R.randint(105, 2489)
    r = a + b
    if r > 9999:
        return None
    pos = R.randint(0, 3)
    sa = str(a)
    i = len(sa) - 1 - pos
    d = sa[i]
    shown = sa[:i] + "?" + sa[i + 1:]
    shown = shown[:-3] + "\u00a0" + shown[-3:]
    return mcq("Quel chiffre remplace le « ? » : %s + %s = %s ?" % (shown, num(b), num(r)), d, [str((int(d) + 1) % 10), str((int(d) + 9) % 10), str((int(d) + 2) % 10)],
               "%s + %s = %s, donc le chiffre caché est <b>%s</b>." % (num(a), num(b), num(r), d))


def s5_prob():
    p = K.next()
    k = R.choice(["km", "livres", "argent", "vel", "estim"])
    a, b = R.randint(1200, 5800), R.randint(350, 3900)
    if a + b > 9999:
        return None
    r = a + b
    wr = [num(no_carry([a, b])) if carries([a, b]) else num(r + 100), num(r + 10), num(abs(a - b))]
    if k == "km":
        return mcq("Une famille roule %s km en été et %s km en hiver. Combien de kilomètres en tout ?" % (num(a), num(b)), num(r) + " km", [w + " km" for w in wr],
                   "%s + %s = <b>%s km</b>." % (num(a), num(b), num(r)))
    if k == "livres":
        return mcq("Une bibliothèque a %s livres. Elle en achète %s. Combien de livres a-t-elle maintenant ?" % (num(a), num(b)), num(r), wr,
                   "%s + %s = <b>%s</b> livres." % (num(a), num(b), num(r)))
    if k == "argent":
        return mcq("Une école dépense %s € pour un voyage et %s € pour des livres. Combien dépense-t-elle en tout ?" % (num(a), num(b)), num(r) + " €", [w + " €" for w in wr],
                   "%s + %s = <b>%s €</b>." % (num(a), num(b), num(r)))
    if k == "vel":
        return mcq("Samedi, %s personnes visitent un musée ; dimanche, %s personnes. Combien de visiteurs en tout ?" % (num(a), num(b)), num(r), wr,
                   "%s + %s = <b>%s</b> visiteurs." % (num(a), num(b), num(r)))
    a, b = R.randint(12, 68) * 100 + R.randint(1, 99), R.randint(5, 30) * 100 + R.randint(1, 99)
    if a + b > 9999:
        return None
    est = round(a, -2) + round(b, -2)
    return mcq("Quel est le meilleur ordre de grandeur de %s + %s ?" % (num(a), num(b)), num(est), [num(est + 1000), num(est // 10), num(round(a, -3) + 0)],
               "On arrondit à la centaine : %s + %s = <b>%s</b> (le résultat exact est %s)." % (num(round(a, -2)), num(round(b, -2)), num(est), num(a + b)))


def main():
    seen = set()
    sets = [
        ("Sans retenue", mix(R, seen, [(s1, 20)])),
        ("Avec une retenue", mix(R, seen, [(s2, 20)])),
        ("Avec plusieurs retenues", mix(R, seen, [(s3, 14), (s3b, 6)])),
        ("Trois nombres et chiffres manquants", mix(R, seen, [(s4_trois, 12), (s4_manquant, 8)])),
        ("Problèmes", mix(R, seen, [(s5_prob, 20)])),
    ]
    body = lesson(
        ["On <b>aligne les unités</b> : unités sous unités, dizaines sous dizaines, etc.",
         "On calcule colonne par colonne, <b>de droite à gauche</b>.",
         "Si une colonne fait 10 ou plus, on écrit les unités et on <b>retient</b> 1 dans la colonne suivante.",
         "Avant de calculer, on cherche un <b>ordre de grandeur</b> pour vérifier le résultat."],
        [example("2 457 + 1 386", ["u : 7 + 6 = 13, j’écris 3, je retiens 1", "d : 1 + 5 + 8 = 14, j’écris 4, je retiens 1", "c : 1 + 4 + 3 = 8 ; m : 2 + 1 = 3"], "3 843")],
        [["Oublier la retenue : 345 + 238 = 573", "Écris la retenue en haut de la colonne suivante : 583."],
         ["Aligner à gauche : 345 + 42 = 765", "Aligne les unités à droite : 387."],
         ["Écrire 13 dans une colonne", "On n’écrit qu’un chiffre par colonne ; la dizaine part en retenue."]])
    faq = [("Pourquoi aligner les unités ?", "Pour additionner des chiffres qui ont la même valeur : unités avec unités, dizaines avec dizaines."),
           ("Comment vérifier une addition ?", "Avec un ordre de grandeur, ou en recommençant le calcul dans un autre ordre.")]
    make_unit(R, "addition-posee", "N",
              "Calculer en colonnes des additions de deux ou trois nombres entiers ayant jusqu’à 4 chiffres ; utiliser un ordre de grandeur pour contrôler un résultat ; résoudre des problèmes additifs (résumé du programme 2024 du cycle 2).",
              "L’addition posée avec retenues", "Addition posée CE2 : fiches et exercices avec corrigé", "Addition posée",
              "Fiches de maths CE2 sur l’addition posée : sans retenue, avec retenues, trois nombres, chiffres manquants, ordre de grandeur et problèmes. 100 exercices corrigés.",
              "On aligne les unités et on calcule de droite à gauche.", "Quand une colonne fait 10 ou plus, on retient 1.",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
