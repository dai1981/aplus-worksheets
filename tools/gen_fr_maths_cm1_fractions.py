# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les fractions (Nombres, calcul et résolution de problèmes)
  python3 tools/gen_fr_maths_cm1_fractions.py
CM1 : dénominateurs jusqu’à 20. CM2 : jusqu’à 60. Lire, écrire, représenter ; écrire une fraction comme un entier plus une
fraction inférieure à 1 (et inversement) ; encadrer entre deux entiers consécutifs ; placer et repérer sur une demi-droite graduée.
Erreurs : inverser numérateur et dénominateur, 17/5 = 1 + 7/5, oublier de multiplier l’entier par le dénominateur (2 + 3/4 = 5/4).
"""
import random
from fr_c3 import mcq, lesson, example, unit, mix, Kids, GN, fr, bande, disque, droite_frac, nomfrac

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52108 + 100 * lv)
    K = Kids(R)


def dmax():
    return 20 if L == 1 else 60


def s1():
    if R.random() < 0.55:
        d = R.choice([3, 4, 5, 6, 8, 10, 12] + ([7, 9] if L == 2 else []))
        k = R.randint(1, d - 1)
        pic = bande(d, k) if R.random() < 0.5 or d > 10 else disque(d, k)
        return mcq("<div class='qfig'>%s</div>Quelle fraction de la figure est coloriée ?" % pic, fr(k, d), [fr(d, k), fr(d - k, d) if d - k != k else fr(k, d + 1), fr(k, d - k) if d - k != k else fr(k + 1, d)],
                   "%d parts égales (dénominateur), %d coloriées (numérateur) : <b>%s</b>." % (d, k, fr(k, d)))
    d = R.randint(5, dmax())
    n = R.randint(1, min(2 * d, 20))
    if n == d:
        return None
    if R.random() < 0.5:
        return mcq("Comment s’écrit « %s » ?" % nomfrac(n, d), fr(n, d), [fr(d, n), fr(n, d + 1), fr(n + 1, d)], "On lit le numérateur puis le dénominateur : <b>%s</b>." % fr(n, d))
    return mcq("Comment se lit %s ?" % fr(n, d), nomfrac(n, d), [nomfrac(d, n) if n > 1 and d <= 20 else nomfrac(n, d + 1), nomfrac(n + 1, d), nomfrac(n, d - 1) if d > 5 else nomfrac(n, d + 2)],
               "%s se lit <b>%s</b>." % (fr(n, d), nomfrac(n, d)))


def s2():
    d = R.randint(2, 12 if L == 1 else 20)
    e = R.randint(1, 5)
    r = R.randint(1, d - 1)
    n = e * d + r
    if R.random() < 0.5:
        right = "%d + %s" % (e, fr(r, d))
        return mcq("Écris %s comme un entier plus une fraction plus petite que 1." % fr(n, d), right,
                   ["1 + %s" % fr(n - d, d) if n - d >= d else "%d + %s" % (e + 1, fr(r, d)), "%d + %s" % (e, fr(d - r, d)) if d - r != r else "%d + %s" % (e - 1, fr(r + d, d)), "%d + %s" % (r, fr(e, d)) if r != e else "%d + %s" % (e + 1, fr(r, d))],
                   "%s = %d %s : %s = %d, il reste %s. <b>%s</b>." % (fr(n, d), e, "fois " + fr(d, d), fr(e * d, d), e, fr(r, d), right))
    right = fr(n, d)
    return mcq("Écris %d + %s sous la forme d’une seule fraction." % (e, fr(r, d)), right, [fr(e + r, d), fr(e * r, d) if e * r != n else fr(n + 1, d), fr(n, d * e) if e > 1 else fr(r + 1, d)],
               "%d = %s, donc %d + %s = <b>%s</b>." % (e, fr(e * d, d), e, fr(r, d), right))


def s3():
    d = R.randint(2, dmax())
    n = R.randint(d + 1, 9 * d)
    if n % d == 0:
        return None
    e = n // d
    right = "entre %d et %d" % (e, e + 1)
    return mcq("Entre quels entiers consécutifs se trouve %s ?" % fr(n, d), right, ["entre %d et %d" % (e - 1, e) if e > 0 else "entre 2 et 3", "entre %d et %d" % (e + 1, e + 2), "entre %d et %d" % (n % 10, n % 10 + 1) if n % 10 not in (e, e - 1, e + 1) else "entre %d et %d" % (e + 3, e + 4)],
               "%s = %s et %s = %s. %s est entre les deux : <b>%s</b>." % (fr(e * d, d), e, fr((e + 1) * d, d), e + 1, fr(n, d), right))


def s4():
    d = R.choice([2, 3, 4, 5, 6, 8, 10] + ([12] if L == 2 else []))
    units = 3 if d <= 6 else 2
    k = R.randint(1, units * d - 1)
    if k % d == 0:
        return None
    if R.random() < 0.7:
        pic = droite_frac(d, units, [(k, "A")], width=440)
        return mcq("<div class='qfig'>%s</div>Quelle fraction repère le point A ?" % pic, fr(k, d), [fr(k, units * d), fr(k + 1, d), fr(k - 1, d) if k > 1 else fr(k + 2, d), fr(d, k)],
                   "Chaque unité est partagée en %d. A est à %d graduations de 0 : <b>%s</b>." % (d, k, fr(k, d)))
    ks = R.sample([x for x in range(1, units * d) if x % d], 3)
    pic = droite_frac(d, units, [(x, ch) for x, ch in zip(ks, "ABC")], width=440)
    i = R.randrange(3)
    right = "ABC"[i]
    return mcq("<div class='qfig'>%s</div>Quel point est repéré par %s ?" % (pic, fr(ks[i], d)), right, [c for c in "ABC" if c != right] + ["aucun"],
               "%s : %d graduations après 0 (chaque graduation vaut %s). C’est le point <b>%s</b>." % (fr(ks[i], d), ks[i], fr(1, d), right))


def s5():
    p = K.next()
    k = R.choice(["pizza", "heure", "verres", "tablette"])
    if k == "pizza":
        d = R.choice([4, 6, 8])
        n = R.randint(d + 1, 4 * d)
        if n % d == 0:
            return None
        return mcq("Des pizzas sont coupées en %d parts égales. %s en mange %d parts avec ses amis, soit %s de pizza. Combien de pizzas entières ont été mangées ?" % (d, p[0], n, fr(n, d)),
                   str(n // d), [str(n // d + 1), str(n % d), str(n)], "%s = %d + %s : <b>%d</b> pizzas entières (et %s d’une autre)." % (fr(n, d), n // d, fr(n % d, d), n // d, fr(n % d, d)))
    if k == "heure":
        n = R.choice([5, 6, 7, 9, 10, 11])
        return mcq("Un film dure %s d’heure. Entre quelles durées se trouve-t-il ?" % fr(n, 4), "entre %d h et %d h" % (n // 4, n // 4 + 1),
                   ["entre %d h et %d h" % (n // 4 + 1, n // 4 + 2), "entre 4 h et 5 h", "entre %d h et %d h" % (n, n + 1)],
                   "%s d’heure = %d h et %s : <b>entre %d h et %d h</b>." % (fr(n, 4), n // 4, fr(n % 4, 4), n // 4, n // 4 + 1))
    if k == "verres":
        d = R.choice([3, 4, 5])
        n = R.randint(d + 1, 3 * d)
        if n % d == 0:
            return None
        return mcq("Une carafe contient 1 L. On verse %d verres de %s L chacun. Quelle quantité a-t-on versée ?" % (n, fr(1, d)), fr(n, d) + " L", [fr(1, n * d) + " L", fr(d, n) + " L", fr(n, d * n) + " L"],
                   "%d fois %s = <b>%s L</b> (c’est plus que 1 L : il faut plus d’une carafe)." % (n, fr(1, d), fr(n, d)))
    d = R.choice([6, 8, 10, 12])
    n = R.randint(1, d - 1)
    return mcq("Une tablette de chocolat a %d carrés. %s en mange %d. Quelle fraction de la tablette reste-t-il ?" % (d, p[0], n), fr(d - n, d), [fr(n, d), fr(d - n, n) if d - n != n else fr(n, d - 1), fr(d, d - n)],
               "Il reste %d carrés sur %d : <b>%s</b>." % (d - n, d, fr(d - n, d)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Lire et écrire une fraction", mix(R, seen, [(s1, 20)])),
        ("Entier + fraction", mix(R, seen, [(s2, 20)])),
        ("Encadrer entre deux entiers", mix(R, seen, [(s3, 20)])),
        ("La demi-droite graduée", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Dans %s, le <b>dénominateur</b> 5 dit en combien de parts égales on partage l’unité, le <b>numérateur</b> 17 combien de parts on prend." % fr(17, 5),
         "%s = 1 : 5 cinquièmes font une unité. Donc %s = %s + %s = <b>3 + %s</b>." % (fr(5, 5), fr(17, 5), fr(15, 5), fr(2, 5), fr(2, 5)),
         "Inversement, 2 + %s = %s + %s = %s." % (fr(3, 4), fr(8, 4), fr(3, 4), fr(11, 4)),
         "Pour encadrer %s : 15 cinquièmes = 3 et 20 cinquièmes = 4, donc 3 &lt; %s &lt; 4." % (fr(17, 5), fr(17, 5))],
        [example("Placer %s sur une demi-droite" % fr(7, 4), ["chaque unité est partagée en 4", "on compte 7 graduations depuis 0"], "entre 1 et 2")],
        [["Inverser : 3 parts sur 8 → %s" % fr(8, 3), "Le nombre de parts du partage va en bas : %s." % fr(3, 8)],
         ["%s = 1 + %s" % (fr(17, 5), fr(7, 5)), "%s est encore plus grand que 1 : on enlève 5 cinquièmes autant de fois que possible." % fr(7, 5)],
         ["2 + %s = %s" % (fr(3, 4), fr(5, 4)), "2 unités = 8 quarts : %s." % fr(11, 4)]])
    faq = [("Une fraction peut-elle être plus grande que 1 ?", "Oui, quand le numérateur est plus grand que le dénominateur : %s = 1 + %s." % (fr(7, 4), fr(3, 4))),
           ("Quels dénominateurs en %s ?" % GN(lv), "Jusqu’à %d, et aussi 100%s pour les fractions décimales." % (dmax(), "" if lv == 1 else " et 1 000"))]
    unit(lv, R, "fractions", "N",
         "Interpréter, représenter, lire et écrire des fractions (dénominateur inférieur ou égal à %d) ; écrire une fraction supérieure à 1 comme la somme d’un entier et d’une fraction inférieure à 1 et inversement ; encadrer une fraction entre deux entiers consécutifs ; placer et repérer une fraction sur une demi-droite graduée" % dmax(),
         "Les fractions : lire, décomposer et placer", "Fractions",
         "Fiches de maths %s sur les fractions : lire et écrire, écrire une fraction comme entier + fraction, encadrer entre deux entiers, demi-droite graduée et problèmes. 100 exercices corrigés." % GN(lv),
         "17/5 = 15/5 + 2/5 = 3 + 2/5.", "5/5 = 1 : le dénominateur dit combien de parts font une unité.",
         body, faq, sets, 8)


if __name__ == "__main__":
    build(1)
