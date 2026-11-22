# -*- coding: utf-8 -*-
"""
France Maths 5e : Carrés et cubes (puissances d’exposant 2 et 3)
  python3 tools/gen_fr_maths_5e_carres_et_cubes.py
Notation a² et a³, carrés de 0 à 12, cube de 10, écrire un nombre comme un carré ou un cube, expressions avec puissances, aires et volumes.
Erreurs : 5² = 10, 2³ = 6, (−3)² = −9, 3 × 4² = 144.
"""
import random
from fr_c4 import *

R = random.Random(60205)
K = Kids(R)


def s1():
    a = R.randint(0, 12)
    if R.random() < 0.25:
        x = R.choice([Fr(1, 10), Fr(2, 10), Fr(3, 10), Fr(5, 10), Fr(12, 10), Fr(15, 10), Fr(11, 10), Fr(4, 10)])
        return M("%s² = …" % d(x), d(x * x), [d(2 * x), d(x * x * 10), d(x + 2)], "%s² = %s × %s = <b>%s</b>." % (d(x), d(x), d(x), d(x * x)))
    if R.random() < 0.5:
        return M("%d² = …" % a, str(a * a), [str(2 * a), str(a + 2), str(a * a + a)], "%d² = %d × %d = <b>%d</b> (et non %d × 2)." % (a, a, a, a * a, a))
    b = R.choice([1, 2, 3, 4, 5, 10])
    return M("%d³ = …" % b, num(b ** 3), [str(3 * b), num(b * b), num(b ** 3 + b)], "%d³ = %d × %d × %d = <b>%s</b>." % (b, b, b, b, num(b ** 3)))


def s2():
    k = R.choice(["carre", "carre", "cube", "lequel"])
    if k == "carre":
        a = R.randint(2, 12)
        return M("%d est le carré de quel nombre ?" % (a * a), str(a), [str(a * a // 2) if a * a % 2 == 0 else str(a + 1), str(a * a), str(a - 1)],
                 "%d × %d = %d : %d = <b>%d</b>²." % (a, a, a * a, a * a, a))
    if k == "cube":
        a = R.choice([2, 3, 4, 5, 10])
        return M("Quel nombre a pour cube %s ?" % num(a ** 3), str(a), [str(a ** 3 // 3) if a ** 3 % 3 == 0 else str(a * a), str(a + 1), num(a ** 3)],
                 "%d × %d × %d = %s, donc %s = <b>%d</b>³." % (a, a, a, num(a ** 3), num(a ** 3), a))
    sq = [x * x for x in range(2, 13)]
    good = R.choice(sq)
    bad = R.sample([x for x in range(10, 150) if x not in sq], 3)
    allv = sorted(bad + [good])
    return M("Lequel de ces nombres est un carré parfait : %s ?" % ", ".join(map(str, allv)), str(good), [str(x) for x in bad],
             "%d = %d², les autres ne sont pas des carrés d’entiers : <b>%d</b>." % (good, int(good ** 0.5), good))


def s3():
    a, b, c = R.randint(2, 6), R.randint(2, 9), R.randint(1, 9)
    k = R.choice(["k*a2", "a2+b", "(a+b)2", "a2-b2", "neg"])
    if k == "k*a2":
        return M("Calcule : %d × %d²" % (b, a), str(b * a * a), [str((b * a) ** 2), str(b * 2 * a), str(b * a + a)], "La puissance d’abord : %d² = %d ; %d × %d = <b>%d</b>." % (a, a * a, b, a * a, b * a * a))
    if k == "a2+b":
        return M("Calcule : %d² + %d" % (b, c), str(b * b + c), [str((b + c) ** 2), str(2 * b + c), str(b * b + c * c)], "%d² = %d ; %d + %d = <b>%d</b>." % (b, b * b, b * b, c, b * b + c))
    if k == "(a+b)2":
        return M("Calcule : (%d + %d)²" % (a, b), str((a + b) ** 2), [str(a * a + b * b), str(2 * (a + b)), str(a + b * b)], "Les parenthèses d’abord : %d + %d = %d ; %d² = <b>%d</b>." % (a, b, a + b, a + b, (a + b) ** 2))
    if k == "a2-b2":
        if b <= a:
            a, b = b, a + 1
        return M("Calcule : %d² − %d²" % (b, a), str(b * b - a * a), [str((b - a) ** 2), str(2 * (b - a)), str(b * b - a)], "%d − %d = <b>%d</b>." % (b * b, a * a, b * b - a * a))
    return M("Calcule : (−%d)²" % b, str(b * b), ["−%d" % (b * b), "−%d" % (2 * b), str(2 * b)], "(−%d)² = (−%d) × (−%d) = <b>%d</b> (le produit de deux négatifs est positif)." % (b, b, b, b * b)) if False else \
        M("Calcule : 10³ − %d²" % b, num(1000 - b * b), [num(30 - 2 * b) if 30 - 2 * b > 0 else num(1000 - 2 * b), num(100 - b * b), num((10 - b) ** 3) if b < 10 else num(999)],
          "10³ = 1 000 et %d² = %d : 1 000 − %d = <b>%s</b>." % (b, b * b, b * b, num(1000 - b * b)))


def s4():
    k = R.choice(["aire", "vol", "cote", "arete"])
    a = R.randint(2, 12)
    u = R.choice(["cm", "m"])
    if k == "aire":
        return M("Quelle est l’aire d’un carré de côté %d %s ?" % (a, u), "%d %s²" % (a * a, u), ["%d %s²" % (4 * a, u) if a != 4 else "%d %s²" % (2 * a, u), "%d %s²" % (2 * a, u) if a != 2 else "%d %s²" % (a + 2, u), "%d %s" % (a * a, u)],
                 "A = %d² = <b>%d %s²</b>." % (a, a * a, u))
    if k == "vol":
        a = R.randint(2, 10)
        return M("Quel est le volume d’un cube d’arête %d %s ?" % (a, u), "%s %s³" % (num(a ** 3), u), ["%d %s³" % (3 * a, u), "%d %s³" % (a * a, u), "%s %s³" % (num(6 * a * a), u)],
                 "V = %d³ = <b>%s %s³</b>." % (a, num(a ** 3), u))
    if k == "cote":
        return M("Un carré a une aire de %d %s². Quelle est la longueur de son côté ?" % (a * a, u), "%d %s" % (a, u), ["%d %s" % (a * a // 2, u) if a * a % 2 == 0 and a * a // 2 != a else "%d %s" % (a + 1, u), "%d %s" % (a * a // 4, u) if a * a % 4 == 0 and a * a // 4 != a else "%d %s" % (a + 2, u), "%d %s" % (a * a, u)],
                     "On cherche le nombre dont le carré vaut %d : %d² = %d, donc <b>%d %s</b>." % (a * a, a, a * a, a, u))
    a = R.choice([2, 3, 4, 5, 10])
    return M("Un cube a un volume de %s %s³. Quelle est la longueur de son arête ?" % (num(a ** 3), u), "%d %s" % (a, u), ["%d %s" % (a * a, u), "%d %s" % (a + 1, u), "%s %s" % (num(a ** 3 // 3) if a ** 3 % 3 == 0 else num(a ** 3 // 2), u)],
             "%d³ = %s : l’arête mesure <b>%d %s</b>." % (a, num(a ** 3), a, u))


def s5():
    k = R.choice(["vrai", "compare", "unite", "suite"])
    if k == "vrai":
        a = R.randint(2, 9)
        V = [("%d² = %d × 2" % (a, a), False), ("%d² = %d × %d" % (a, a, a), True), ("%d³ = %d × 3" % (a, a), False), ("%d³ = %d × %d × %d" % (a, a, a, a), True)]
        good = [t for t, v in V if v]
        bad = [t for t, v in V if not v]
        g = R.choice(good)
        return M("Avec le nombre %d, quelle égalité est vraie ?" % a, g, bad + ["%d² = %d" % (a, 2 * a)], "Un carré est le produit d’un nombre par lui-même ; un cube, de trois facteurs égaux : <b>%s</b>." % g)
    if k == "compare":
        a, b = R.choice([(2, 3), (3, 2), (4, 3), (2, 5), (5, 2), (3, 4)])
        x, y = a ** b, b ** a
        if x == y:
            return None
        return M("Quel est le plus grand : %d<sup>%d</sup> ou %d<sup>%d</sup> ?" % (a, b, b, a), "%d<sup>%d</sup>" % ((a, b) if x > y else (b, a)), ["%d<sup>%d</sup>" % ((b, a) if x > y else (a, b)), "ils sont égaux", "on ne peut pas savoir"],
                 "%d<sup>%d</sup> = %d et %d<sup>%d</sup> = %d." % (a, b, x, b, a, y))
    if k == "unite":
        return M("Combien de cm² y a-t-il dans 1 m² ?", "10 000 cm²", ["100 cm²", "1 000 cm²", "200 cm²"], "1 m² = 100 cm × 100 cm = 100² cm² = <b>10 000 cm²</b>.") if R.random() < 0.5 else \
            M("Combien de cm³ y a-t-il dans 1 dm³ ?", "1 000 cm³", ["100 cm³", "10 cm³", "300 cm³"], "1 dm³ = 10³ cm³ = <b>1 000 cm³</b>.")
    n = R.randint(4, 9)
    sq = [i * i for i in range(1, n + 1)]
    return M("Quel nombre vient ensuite dans la suite %s, … ?" % ", ".join(map(str, sq)), str((n + 1) ** 2), [str(sq[-1] + n), str(sq[-1] + 2 * n), str(sq[-1] * 2)],
             "Ce sont les carrés : %d² = <b>%d</b>." % (n + 1, (n + 1) ** 2))


def main():
    seen = set()
    sets = [("Calculer un carré ou un cube", mix(R, seen, [(s1, 20)])), ("Reconnaître un carré ou un cube", mix(R, seen, [(s2, 20)])),
            ("Expressions avec des puissances", mix(R, seen, [(s3, 20)])), ("Aires et volumes", mix(R, seen, [(s4, 20)])), ("Comparer et raisonner", mix(R, seen, [(s5, 20)]))]
    body = L(["a² (« a au carré ») = a × a. a³ (« a au cube ») = a × a × a.",
              "À connaître : les carrés de 0 à 12 (0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144) et 10³ = 1 000.",
              "Dans un calcul, la puissance passe avant la multiplication : 3 × 4² = 3 × 16 = 48."],
             [("2 × 5² + 1", ["5² = 25", "2 × 25 = 50", "50 + 1"], "51")],
             [["5² = 10", "5² = 5 × 5 = 25."], ["2³ = 6", "2³ = 2 × 2 × 2 = 8."], ["3 × 4² = 12² = 144", "La puissance d’abord : 3 × 16 = 48."]])
    faq = [("Pourquoi dit-on « au carré » ?", "Parce que a² est l’aire d’un carré de côté a."), ("Et « au cube » ?", "a³ est le volume d’un cube d’arête a.")]
    unit("5e", R, "carres-et-cubes", "N",
         "Utiliser la notation des carrés et des cubes ; connaître les carrés des entiers de 0 à 12 et le cube de 10 ; écrire un nombre comme un carré ou un cube ; calculer des expressions simples contenant des puissances",
         "Carrés et cubes", "Carrés et cubes",
         "Fiches de maths 5e sur les carrés et les cubes : calculer a² et a³, carrés parfaits, expressions avec puissances, aires, volumes et problèmes. 100 exercices corrigés.",
         "a² = a × a ; a³ = a × a × a", "3 × 4² = 3 × 16 = 48", body, faq, sets, 5)


if __name__ == "__main__":
    main()
