# -*- coding: utf-8 -*-
"""
France Maths 4e : Racine carrée
  python3 tools/gen_fr_maths_4e_racine_carree.py
Erreurs : √49 = 24,5 (diviser par 2), √(9 + 16) = 3 + 4, √ d’un négatif, encadrer avec les mauvais entiers.
"""
import random
import math
from fr_c4 import *

R = random.Random(60304)
K = Kids(R)


def rt(x):
    return "√%s" % d(x) if Fr(x).denominator == 1 and len(d(x)) <= 3 else "√(%s)" % d(x)


def s1():
    k = R.choice(["int", "int", "dec", "frac", "carre"])
    if k == "int":
        n = R.randint(2, 20)
        return M("Calcule : %s" % rt(n * n), str(n), [d(Fr(n * n, 2)), str(n * n), str(n + 1)], "%d × %d = %d, donc %s = <b>%d</b>." % (n, n, n * n, rt(n * n), n))
    if k == "dec":
        n = Fr(R.randint(1, 12), 10)
        return M("Calcule : %s" % rt(n * n), d(n), [d(n * 10), d(n * n / 2), d(n / 10)], "%s × %s = %s, donc %s = <b>%s</b>." % (d(n), d(n), d(n * n), rt(n * n), d(n)))
    if k == "frac":
        a, b = R.randint(1, 9), R.randint(2, 10)
        if math.gcd(a, b) != 1:
            return None
        return M("Calcule : √(%s)" % fr(a * a, b * b), fr(a, b), [fr(a * a, b), fr(a, b * b), fr(a * a, 2 * b * b)], "√%d = %d et √%d = %d : <b>%s</b>." % (a * a, a, b * b, b, fr(a, b)))
    n = R.randint(2, 30)
    return M("Calcule : (√%d)²" % n, str(n), [str(n * n), str(2 * n), "√%d" % (2 * n)], "Par définition, (√a)² = a : <b>%d</b>." % n)


def s2():
    k = R.choice(["enc", "enc", "enc", "calc"])
    if k == "calc":
        n = R.choice([2, 3, 5, 7, 10, 15, 20, 50, 80, 120])
        v = Fr(round(math.sqrt(n) * 10), 10)
        return M("À la calculatrice, donne l’arrondi au dixième de √%d." % n, d(v), [d(Fr(n, 2)) if n < 30 else d(v + 1), d(v + Fr(1, 10)), d(Fr(int(math.sqrt(n) * 10), 10)) if Fr(int(math.sqrt(n) * 10), 10) != v else d(v - Fr(1, 10))],
                 "√%d ≈ %s… → <b>%s</b>." % (n, d(Fr(int(math.sqrt(n) * 1000), 1000)), d(v)))
    n = R.randint(2, 150)
    r = int(math.isqrt(n))
    if r * r == n:
        return None
    return M("Entre quels entiers consécutifs se trouve √%d ?" % n, "%d et %d" % (r, r + 1), ["%d et %d" % (r - 1, r) if r > 1 else "%d et %d" % (r + 1, r + 2), "%d et %d" % (n // 2, n // 2 + 1), "%d et %d" % (r + 1, r + 2)],
             "%d² = %d &lt; %d &lt; %d = %d², donc <b>%d &lt; √%d &lt; %d</b>." % (r, r * r, n, (r + 1) ** 2, r + 1, r, n, r + 1))


def s3():
    k = R.choice(["egal", "somme", "neg", "carre", "prod"])
    if k == "egal":
        n = R.randint(2, 15)
        return M("Quelles sont les solutions de l’équation x² = %d ?" % (n * n), "%d et −%d" % (n, n), ["%d seulement" % n, "%s" % d(Fr(n * n, 2)), "aucune"], "x = √%d = %d ou x = −√%d = −%d : <b>%d et −%d</b>." % (n * n, n, n * n, n, n, n))
    if k == "neg":
        n = R.randint(2, 30)
        return M("Que vaut √(−%d) ?" % n, "elle n’existe pas", ["−√%d" % n, "%s" % ("−" + str(int(math.isqrt(n))) if math.isqrt(n) ** 2 == n else "−%d" % n), "0"],
                 "Un carré n’est jamais négatif : la racine carrée d’un nombre négatif <b>n’existe pas</b>.")
    if k == "somme":
        a, b = R.choice([(9, 16), (36, 64), (9, 40), (25, 144), (64, 225), (16, 9), (144, 256), (81, 144)])
        r = math.isqrt(a + b)
        return M("Calcule : √(%d + %d)" % (a, b), str(r), [str(math.isqrt(a) + math.isqrt(b)) if math.isqrt(a) ** 2 == a and math.isqrt(b) ** 2 == b else str(r + 1), str(a + b), d(Fr(a + b, 2))],
                 "On calcule d’abord sous la racine : √%d = <b>%d</b>. (√(a + b) n’est pas √a + √b.)" % (a + b, r))
    if k == "carre":
        n = R.choice([-3, -5, -7, -9, 4, 6])
        return M("Calcule : √(%s²)" % par(n), d(abs(n)), [d(n) if n < 0 else d(-n), d(n * n), "elle n’existe pas"], "%s² = %d et √%d = <b>%d</b> (une racine carrée est positive)." % (par(n), n * n, n * n, abs(n)))
    a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (2, 32), (3, 27)])
    r = math.isqrt(a * b)
    return M("Calcule : √%d × √%d" % (a, b), str(r), [str(a * b), "√%d" % (a + b), str(r * 2)], "√%d × √%d = √%d = <b>%d</b>." % (a, b, a * b, r))


def s4():
    k = R.choice(["cote", "cote", "ordre", "aire"])
    if k == "cote":
        c = R.randint(2, 25)
        return M("Un carré a une aire de %d cm². Combien mesure son côté ?" % (c * c), "%d cm" % c, ["%s cm" % d(Fr(c * c, 4)), "%s cm" % d(Fr(c * c, 2)), "%d cm" % (c * c)],
                 "Côté = √aire = √%d = <b>%d cm</b>." % (c * c, c))
    if k == "aire":
        a = R.choice([2, 3, 5, 6, 7, 8, 10, 11])
        v = Fr(round(math.sqrt(a) * 100), 100)
        return M("Un carré a une aire de %d m². Quelle est la longueur de son côté, arrondie au centimètre ?" % a, "%s m" % dk(v, 2), ["%s m" % d(Fr(a, 4)) if a % 4 else "%s m" % d(Fr(a, 2)), "%s m" % dk(v + Fr(1, 100), 2), "%s m" % dk(Fr(int(math.sqrt(a) * 10), 10), 2) if Fr(int(math.sqrt(a) * 10), 10) != v else "%s m" % dk(v - Fr(1, 100), 2)],
                 "Côté = √%d ≈ %s… ≈ <b>%s m</b>." % (a, d(Fr(int(math.sqrt(a) * 10000), 10000)), dk(v, 2)))
    xs = R.sample([4, 5, 7, 10, 15, 20, 30, 50], 3)
    ys = ["√%d" % x for x in xs]
    nn = R.choice([2, 3, 4, 5, 6])
    ys.append(str(nn))
    vals = xs + [nn * nn]
    order = [y for _, y in sorted(zip(vals, ys))]
    if len(set(vals)) < 4:
        return None
    a1 = [order[1], order[0]] + order[2:]
    a2 = order[:2] + [order[3], order[2]]
    w = [" &lt; ".join(order[::-1]), " &lt; ".join(a1), " &lt; ".join(a2)]
    return M("Range dans l’ordre croissant : %s." % ", ".join(ys), " &lt; ".join(order), w, "On compare les carrés : %s. Ordre : <b>%s</b>." % (", ".join("%s² = %d" % (y, v) for y, v in zip(ys, vals)), " &lt; ".join(order)))


def s5():
    p = K.next()
    k = R.choice(["jardin", "chute", "diag", "dalles"])
    if k == "jardin":
        c = R.randint(5, 30)
        return M("%s a un jardin carré de %d m². Quelle longueur de grillage faut-il pour en faire le tour ?" % (p[0], c * c), "%d m" % (4 * c), ["%d m" % c, "%d m" % (c * c * 4), "%s m" % d(Fr(c * c, 4))],
                 "Côté : √%d = %d m ; périmètre : 4 × %d = <b>%d m</b>." % (c * c, c, c, 4 * c))
    if k == "chute":
        t = R.choice([1, 2, 3, 4])
        h = 5 * t * t
        return M("Le temps de chute t (en s) d’un objet lâché d’une hauteur h (en m) vérifie t = √(h ÷ 5). Combien de temps met un objet lâché de %d m ?" % h, "%d s" % t, ["%d s" % (h // 5), "%s s" % d(Fr(h, 10)), "%d s" % (t + 1)],
                 "t = √(%d ÷ 5) = √%d = <b>%d s</b>." % (h, t * t, t))
    if k == "diag":
        c = R.choice([3, 4, 5, 6, 8, 10])
        v = Fr(round(c * math.sqrt(2) * 10), 10)
        return M("La diagonale d’un carré de côté %d cm mesure √%d cm. Donne son arrondi au dixième." % (c, 2 * c * c), "%s cm" % d(v), ["%d cm" % (2 * c), "%d cm" % c, "%s cm" % d(Fr(2 * c * c, 2))],
                 "√%d ≈ <b>%s cm</b>." % (2 * c * c, d(v)))
    n = R.randint(4, 20)
    a = R.choice([20, 25, 30, 40, 50])
    tot = n * n
    return M("On veut carreler une pièce carrée avec %d dalles carrées de %d cm de côté, sans les couper. Combien de dalles y a-t-il sur un côté ?" % (tot, a), str(n), [d(Fr(tot, 4)), d(Fr(tot, 2)), str(n + 1)],
             "Les dalles forment un carré : √%d = <b>%d</b>." % (tot, n))


def main():
    seen = set()
    sets = [("Racines carrées exactes", mix(R, seen, [(s1, 20)])), ("Encadrer et arrondir", mix(R, seen, [(s2, 20)])),
            ("Propriétés et pièges", mix(R, seen, [(s3, 20)])), ("Côté d’un carré et comparaisons", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La <b>racine carrée</b> d’un nombre positif a est le nombre positif dont le carré est a : √49 = 7 car 7² = 49.",
              "On peut encadrer une racine carrée entre deux entiers : 6² = 36 &lt; 40 &lt; 49 = 7², donc 6 &lt; √40 &lt; 7.",
              "Si un carré a pour aire A, son côté mesure √A. La racine carrée d’un nombre négatif n’existe pas."],
             [("√81", ["9 × 9 = 81"], "9"), ("Encadrer √30", ["5² = 25 et 6² = 36"], "5 &lt; √30 &lt; 6")],
             [["√49 = 24,5", "On ne divise pas par 2 : 7 × 7 = 49, donc √49 = 7."], ["√(9 + 16) = 3 + 4 = 7", "On calcule d’abord 9 + 16 = 25, puis √25 = 5."],
              ["x² = 25 a pour seule solution 5", "−5 est aussi solution car (−5)² = 25."]])
    faq = [("Quels sont les carrés parfaits à connaître ?", "1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144… jusqu’à 400 = 20²."),
           ("À quoi sert la racine carrée en 4e ?", "Surtout à calculer une longueur avec le théorème de Pythagore.")]
    unit("4e", R, "racine-carree", "N",
         "Connaître et utiliser la racine carrée d’un nombre positif ; connaître les carrés parfaits ; encadrer une racine carrée entre deux entiers ; utiliser la calculatrice pour en donner une valeur approchée ; résoudre x² = a",
         "Racine carrée", "Racine carrée",
         "Fiches de maths 4e sur la racine carrée : carrés parfaits, encadrer et arrondir, propriétés, côté d’un carré et problèmes. 100 exercices corrigés.",
         "√a est le nombre positif dont le carré est a", "√49 = 7 car 7² = 49", body, faq, sets, 4)


if __name__ == "__main__":
    main()
