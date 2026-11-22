# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : La multiplication posée (entiers et décimaux)
  python3 tools/gen_fr_maths_cm1_multiplication.py
CM1 : entier × entier (jusqu’à 4 chiffres × 2 chiffres), décimal × entier à un chiffre, ordre de grandeur.
CM2 : entier × entier à 3 chiffres, décimal × entier (1 ou 2 chiffres).
Erreurs : oublier le décalage (0) de la deuxième ligne, oublier la retenue, mal placer la virgule du produit.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, dz, posee, FOIS

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52106 + 100 * lv)
    K = Kids(R)


def noshift(a, b):
    """additionner les lignes sans le décalage"""
    return sum(a * int(d) for d in str(b))


def nocarry1(a, d):
    ds = [int(c) for c in str(a)]
    return int(str(ds[0] * d) + "".join(str(x * d % 10) for x in ds[1:]))


def ent(a, b):
    r = a * b
    w = [noshift(a, b) if b >= 10 else nocarry1(a, b), r + 10 ** (len(str(r)) - 2), r - 100, a * (b // 10 * 10) if b % 10 else r * 10]
    if b >= 10:
        lines = []
        for i, d in enumerate(str(b)[::-1]):
            lines.append("%s %s %s = %s" % (num(a), FOIS, num(int(d) * 10 ** i), num(a * int(d) * 10 ** i)))
        e = "%s, puis on additionne les lignes : <b>%s</b>." % (" ; ".join(lines), num(r))
    else:
        e = "On multiplie chaque chiffre par %d, de droite à gauche, avec les retenues : <b>%s</b>." % (b, num(r))
    return mcq(posee([str(a), str(b)], op=FOIS) + "Calcule en posant l’opération : %s %s %s" % (num(a), FOIS, num(b)), num(r), [num(x) for x in w if x > 0 and x != r], e)


def s1():
    a, b = R.randint(102, 989), R.randint(12, 98)
    if b % 10 == 0:
        return None
    return ent(a, b)


def s2():
    if L == 1:
        a, b = R.randint(1012, 9989), R.randint(12, 79)
    else:
        a, b = R.randint(112, 989), R.randint(102, 789)
    if b % 10 == 0 or a % 10 == 0:
        return None
    return ent(a, b)


def dec(a, ka, b):
    r = a * b
    w = [dz(r, ka - 1) if ka > 1 else num(r), dz(r, ka + 1), dz(a * b // 10 * 10 + (a % 10) * b % 10, ka) if (a % 10) * b >= 10 else dz(r + 10 ** ka, ka), dz(noshift(a, b), ka) if b >= 10 else dz(nocarry1(a, b), ka)]
    return mcq(posee([dz(a, ka).replace(" ", ""), str(b)], op=FOIS) + "Calcule en posant l’opération : %s %s %d" % (dz(a, ka), FOIS, b), dz(r, ka), w,
               "On calcule %s %s %d = %s sans s’occuper de la virgule, puis on met %d chiffre%s après la virgule, comme dans %s : <b>%s</b>." % (
                   num(a), FOIS, b, num(r), ka, "s" if ka > 1 else "", dz(a, ka), dz(r, ka)))


def s3():
    ka = R.choice([1, 2])
    a = R.randint(10 ** ka + 1, 10 ** (ka + 2) - 1)
    if a % 10 == 0:
        return None
    return dec(a, ka, R.randint(2, 9))


def s4():
    if L == 2:
        ka = R.choice([1, 2, 1])
        a = R.randint(10 ** ka + 1, 10 ** (ka + 2) - 1)
        b = R.randint(12, 48)
        if a % 10 == 0 or b % 10 == 0:
            return None
        return dec(a, ka, b)
    k = R.choice(["estim", "dix"])
    if k == "estim":
        a, b = R.randint(21, 98) * 10 + R.randint(1, 9), R.randint(2, 9) * 10 + R.randint(1, 4)
        e = round(a, -2) * round(b, -1)
        return mcq("Quel est le meilleur ordre de grandeur de %s %s %d ?" % (num(a), FOIS, b), num(e), [num(e * 10), num(e // 10), num(round(a, -2) + round(b, -1))],
                   "On arrondit : %s %s %d = <b>%s</b> (le produit exact est %s)." % (num(round(a, -2)), FOIS, round(b, -1), num(e), num(a * b)))
    a, b = R.randint(12, 999), R.choice([20, 30, 40, 50, 60, 200, 300, 400, 500])
    r = a * b
    return mcq("Calcule : %s %s %s" % (num(a), FOIS, num(b)), num(r), [num(a * (b // 10 if b < 100 else b // 100)), num(r * 10), num(r // 10)],
               "%s %s %s = %s %s %d %s %d = <b>%s</b>." % (num(a), FOIS, num(b), num(a), FOIS, b // (10 if b < 100 else 100), FOIS, 10 if b < 100 else 100, num(r)))


def s5():
    p = K.next()
    k = R.choice(["car", "prix", "ruban", "salle", "litres"])
    if k == "car":
        a, b = R.randint(12, 48), R.randint(35, 63)
        return mcq("Une école loue %d cars de %d places. Combien de places en tout ?" % (a, b), num(a * b), [num(noshift(b, a)), num(a + b), num(a * b + 100)], "%d %s %d = <b>%s</b>." % (a, FOIS, b, num(a * b)))
    if k == "prix":
        n = R.randint(2, 9) if L == 1 else R.randint(12, 36)
        pr = R.randint(105, 1999)
        if pr % 10 == 0:
            return None
        r = n * pr
        return mcq("%s achète %d places de cinéma à %s € l’une. Combien paie-t-%s ?" % (p[0], n, dz(pr, 2, True), p[1]) if pr < 1500 else
                   "Un club achète %d ballons à %s € l’un. Combien paie-t-il ?" % (n, dz(pr, 2, True)), dz(r, 2, True) + " €", [dz(r, 1) + " €", dz(r * 10, 2, True) + " €", dz(r + 100, 2, True) + " €"],
                   "%d %s %s = <b>%s €</b>." % (n, FOIS, dz(pr, 2, True), dz(r, 2, True)))
    if k == "ruban":
        n, l = R.randint(3, 9), R.randint(11, 99)
        return mcq("On coupe %d morceaux de ruban de %s m. Quelle longueur de ruban faut-il ?" % (n, dz(l, 1)), dz(n * l, 1) + " m", [dz(n * l, 2) + " m", num(n * l) + " m", dz(n * l + 10, 1) + " m"],
                   "%d %s %s = <b>%s m</b>." % (n, FOIS, dz(l, 1), dz(n * l, 1)))
    if k == "salle":
        a, b = R.randint(18, 45), R.randint(24, 52)
        return mcq("Une salle de spectacle a %d rangées de %d fauteuils. Combien de fauteuils ?" % (a, b), num(a * b), [num(noshift(a, b)), num(a * b - 10), num(a + b)], "%d %s %d = <b>%s</b>." % (a, FOIS, b, num(a * b)))
    n, v = R.randint(3, 9), R.randint(105, 875)
    if v % 10 == 0:
        return None
    return mcq("Une bouteille contient %s L. Combien de litres dans %d bouteilles ?" % (dz(v, 2), n), dz(n * v, 2) + " L", [dz(n * v, 1) + " L", dz(n * v, 3) + " L", dz(n * v + 100, 2) + " L"],
               "%d %s %s = <b>%s L</b>." % (n, FOIS, dz(v, 2), dz(n * v, 2)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("3 chiffres × 2 chiffres", mix(R, seen, [(s1, 20)])),
        ("4 chiffres × 2 chiffres" if lv == 1 else "3 chiffres × 3 chiffres", mix(R, seen, [(s2, 20)])),
        ("Un décimal × un entier à 1 chiffre", mix(R, seen, [(s3, 20)])),
        ("Ordre de grandeur et multiples de 10" if lv == 1 else "Un décimal × un entier à 2 chiffres", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Pour 347 %s 26 : on calcule 347 %s 6, puis 347 %s 20 (on écrit d’abord un <b>0</b>), puis on additionne." % (FOIS, FOIS, FOIS),
         "Pour un décimal : on multiplie sans la virgule, puis on met dans le produit <b>autant de chiffres après la virgule</b> que dans le facteur décimal.",
         "On vérifie avec un ordre de grandeur : 347 %s 26 ≈ 300 %s 30 = 9 000." % (FOIS, FOIS)],
        [example("347 %s 26" % FOIS, ["347 %s 6 = 2 082" % FOIS, "347 %s 20 = 6 940" % FOIS, "2 082 + 6 940"], "9 022"),
         example("4,35 %s 6" % FOIS, ["435 %s 6 = 2 610" % FOIS, "2 chiffres après la virgule"], "26,10 = 26,1")],
        [["Oublier le 0 de la 2e ligne : 347 %s 26 = 2 082 + 694" % FOIS, "La 2e ligne vaut 347 %s 20 = 6 940." % FOIS],
         ["Oublier une retenue", "Ajoute la retenue après avoir multiplié le chiffre suivant."],
         ["Mal placer la virgule : 4,35 %s 6 = 261" % FOIS, "Un seul facteur a 2 chiffres après la virgule : 26,10."]])
    faq = [("Pourquoi écrit-on un 0 au début de la deuxième ligne ?", "Parce qu’on multiplie par des dizaines : %s 20 au lieu de %s 2." % (FOIS, FOIS)),
           ("Faut-il aligner les virgules dans une multiplication ?", "Non. On aligne les chiffres à droite, et on place la virgule du résultat à la fin.")]
    unit(lv, R, "multiplication-posee", "N",
         ("Estimer le résultat d’une opération ; poser et effectuer la multiplication de deux nombres entiers ; poser et effectuer la multiplication d’un nombre décimal par un nombre entier inférieur à 10" if lv == 1 else
          "Estimer le résultat d’une opération ; poser et effectuer la multiplication de deux entiers et d’un nombre décimal par un nombre entier"),
         "La multiplication posée : entiers et décimaux", "Multiplication posée",
         "Fiches de maths %s sur la multiplication posée : 3 et 4 chiffres par 2 chiffres, décimal par entier, ordre de grandeur et problèmes. 100 exercices corrigés." % GN(lv),
         "× 26 : on calcule × 6, puis × 20 (avec un 0), puis on additionne.", "Autant de chiffres après la virgule que dans le facteur décimal.",
         body, faq, sets, 6)


if __name__ == "__main__":
    build(1)
