# -*- coding: utf-8 -*-
"""
France Maths 6e : Les angles
  python3 tools/gen_fr_maths_6e_angles.py
Nature d’un angle, mesure au rapporteur, angles adjacents, opposés par le sommet, supplémentaires, somme des angles d’un triangle, bissectrice.
Erreurs : lire la mauvaise graduation du rapporteur (180° − a), croire que des angles opposés sont supplémentaires, somme des angles = 360°.
"""
import random
from fr_c4 import *
import gen_de_mathe_k5_winkel as W

R = random.Random(60114)
K = Kids(R)
W.R = R
NAT = ["aigu", "droit", "obtus", "plat"]


def nat(a):
    return "aigu" if a < 90 else "droit" if a == 90 else "obtus" if a < 180 else "plat"


def pic(a, rot=0, scale=False, lab=("A", "O", "B")):
    return relabel(W.winkel_svg(a, rot, scale, lab), "un angle de sommet %s" % lab[1])


def s1():
    if R.random() < 0.5:
        a = R.choice(list(range(20, 90, 5)) + [90, 90] + list(range(100, 180, 5)) + [180])
        ans = nat(a)
        return M("%sQuelle est la nature de cet angle ?" % pic(a, R.choice([0, 15, 30, 200 if a < 150 else 0])), "un angle " + ans, ["un angle " + x for x in NAT if x != ans],
                 "Cet angle est %s : c’est <b>un angle %s</b>." % ({"aigu": "plus petit qu’un angle droit", "droit": "un quart de tour (90°)", "obtus": "entre 90° et 180°", "plat": "égal à 180°"}[ans], ans))
    a = R.choice([x for x in range(5, 181, 5)])
    ans = nat(a)
    return M("Un angle mesure %d°. Quelle est sa nature ?" % a, "aigu" if ans == "aigu" else ans, [x for x in NAT if x != ans],
             "%d° : %s, donc <b>%s</b>." % (a, {"aigu": "moins de 90°", "droit": "exactement 90°", "obtus": "entre 90° et 180°", "plat": "exactement 180°"}[ans], ans))


def s2():
    a = R.choice([x for x in range(20, 171, 5) if x != 90])
    q = pic(a, 0, scale=True)
    return M(q + "Lis la mesure de l’angle AOB sur le rapporteur.", "%d°" % a, ["%d°" % (180 - a), "%d°" % (a + 10), "%d°" % (a - 5)],
             "Le côté [OA] est sur le zéro de la graduation extérieure : on lit sur la même graduation, <b>%d°</b> (et non %d°)." % (a, 180 - a))


def s3():
    a = R.randint(20, 160)
    if a == 90:
        return None
    k = R.choice(["supp", "opp", "adj", "comp", "voc"])
    if k == "supp":
        return M("Deux angles sont supplémentaires. L’un mesure %d°. Combien mesure l’autre ?" % a, "%d°" % (180 - a), ["%d°" % (360 - a), "%d°" % abs(90 - a), "%d°" % a],
                 "Deux angles supplémentaires ont une somme de 180° : 180 − %d = <b>%d°</b>." % (a, 180 - a))
    if k == "opp":
        return M("Deux droites se coupent en O. Un des angles mesure %d°. Combien mesure l’angle opposé par le sommet ?" % a, "%d°" % a, ["%d°" % (180 - a), "%d°" % (360 - a), "%d°" % abs(90 - a)],
                 "Deux angles opposés par le sommet ont la même mesure : <b>%d°</b>." % a)
    if k == "adj":
        b = R.randint(10, 160 - a) if a < 150 else 10
        return M("Les angles AOB et BOC sont adjacents. AOB = %d° et BOC = %d°. Combien mesure l’angle AOC ?" % (a, b), "%d°" % (a + b), ["%d°" % abs(a - b), "%d°" % (180 - a - b) if 180 - a - b > 0 else "%d°" % (a + b + 10), "%d°" % (a + b + 10)],
                 "Les angles adjacents s’ajoutent : %d + %d = <b>%d°</b>." % (a, b, a + b))
    if k == "comp":
        a = R.randint(10, 80)
        return M("Un angle droit est partagé en deux angles. L’un mesure %d°. Combien mesure l’autre ?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % a if a != 45 else "%d°" % (a + 5), "%d°" % (90 + a)],
                 "90 − %d = <b>%d°</b>." % (a, 90 - a))
    V = [("Deux angles adjacents…", "ont le même sommet, un côté commun et sont de part et d’autre de ce côté", ["ont la même mesure", "ont une somme de 180°", "sont toujours droits"]),
         ("Deux angles opposés par le sommet…", "ont la même mesure", ["ont une somme de 180°", "ont une somme de 90°", "sont toujours aigus"]),
         ("Deux angles supplémentaires…", "ont une somme de 180°", ["ont la même mesure", "ont une somme de 90°", "ont une somme de 360°"]),
         ("Un angle plat mesure…", "180°", ["90°", "360°", "100°"]), ("Un angle droit mesure…", "90°", ["180°", "100°", "45°"])]
    q, an, w = R.choice(V)
    return M(q, an, w, "Réponse : <b>%s</b>." % an)


def s4():
    a, b = R.randint(20, 110), R.randint(20, 110)
    c = 180 - a - b
    if c < 10:
        return None
    k = R.choice(["third", "eq", "iso", "rect"])
    if k == "third":
        return M("Dans un triangle ABC, l’angle A mesure %d° et l’angle B mesure %d°. Combien mesure l’angle C ?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (90 - a + b if 0 < 90 - a + b < 180 and 90 - a + b != c else c + 10)],
                 "La somme des angles d’un triangle vaut 180° : 180 − %d − %d = <b>%d°</b>." % (a, b, c))
    if k == "eq":
        return M("Combien mesure chaque angle d’un triangle équilatéral ?", "60°", ["90°", "180°", "45°"], "Les 3 angles sont égaux : 180 ÷ 3 = <b>60°</b>.")
    if k == "iso":
        t = R.choice(range(20, 161, 10))
        return M("Un triangle isocèle a un angle au sommet principal de %d°. Combien mesure chacun des deux autres angles ?" % t, "%s°" % d(Fr(180 - t, 2)), ["%d°" % (180 - t), "%d°" % t, "%s°" % d(Fr(360 - t, 2))],
                 "Les deux angles à la base sont égaux : (180 − %d) ÷ 2 = <b>%s°</b>." % (t, d(Fr(180 - t, 2))))
    a = R.randint(15, 75)
    return M("Un triangle est rectangle. Un de ses angles aigus mesure %d°. Combien mesure l’autre angle aigu ?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % (90 + a), "%d°" % (180 - 90 - a + 10)],
             "180 − 90 − %d = <b>%d°</b>." % (a, 90 - a))


def s5():
    k = R.choice(["biss", "biss2", "plat", "tour"])
    if k == "biss":
        a = R.choice(range(20, 180, 2))
        return M("La bissectrice d’un angle de %d° le partage en deux angles. Combien mesure chacun d’eux ?" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (180 - a), "%d°" % (a // 2 + 10)],
                 "La bissectrice partage l’angle en deux angles égaux : %d ÷ 2 = <b>%d°</b>." % (a, a // 2))
    if k == "biss2":
        a = R.randint(10, 85)
        return M("[OC) est la bissectrice de l’angle AOB. AOC = %d°. Combien mesure AOB ?" % a, "%d°" % (2 * a), ["%d°" % a, "%d°" % (180 - a), "%d°" % (90 - a) if 90 - a != a else "%d°" % (a + 10)],
                 "AOB = 2 × AOC = <b>%d°</b>." % (2 * a))
    if k == "plat":
        a, b = R.randint(20, 80), R.randint(20, 80)
        return M("Sur une droite, au point O, on trace deux demi-droites. On obtient trois angles adjacents : %d°, %d° et un troisième. Combien mesure-t-il ?" % (a, b), "%d°" % (180 - a - b), ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (90 - a + b if 0 < 90 - a + b and 90 - a + b != 180 - a - b else 180 - a - b + 10)],
                 "Les trois angles forment un angle plat : 180 − %d − %d = <b>%d°</b>." % (a, b, 180 - a - b))
    h = R.choice([1, 2, 3, 4, 5])
    return M("De combien de degrés tourne la grande aiguille d’une horloge en %d quart%s d’heure ?" % (h, "s" if h > 1 else ""), "%d°" % (90 * h), ["%d°" % (15 * h), "%d°" % (60 * h), "%d°" % (45 * h)],
             "Un tour complet fait 360° en 1 h : un quart d’heure, c’est 90°. %d × 90 = <b>%d°</b>." % (h, 90 * h))


def main():
    seen = set()
    sets = [("Nature d’un angle", mix(R, seen, [(s1, 20)])), ("Mesurer au rapporteur", mix(R, seen, [(s2, 20)])),
            ("Angles adjacents, opposés, supplémentaires", mix(R, seen, [(s3, 20)])), ("Angles d’un triangle", mix(R, seen, [(s4, 20)])), ("Bissectrice et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un angle est <b>aigu</b> (moins de 90°), <b>droit</b> (90°), <b>obtus</b> (entre 90° et 180°) ou <b>plat</b> (180°).",
              "Deux angles <b>opposés par le sommet</b> ont la même mesure ; deux angles <b>supplémentaires</b> ont une somme de 180°.",
              "La somme des angles d’un triangle vaut <b>180°</b>. La <b>bissectrice</b> partage un angle en deux angles égaux."],
             [("Triangle : 50° et 70°", ["180 − 50 − 70"], "60°")],
             [["Lire la mauvaise graduation du rapporteur", "On part du zéro qui est sur un côté de l’angle et on lit la même graduation."],
              ["Croire que des angles opposés par le sommet sont supplémentaires", "Ils sont égaux ; ce sont les angles adjacents sur une droite qui sont supplémentaires."],
              ["Penser que la somme des angles d’un triangle vaut 360°", "C’est 180° (360° pour un quadrilatère)."]])
    faq = [("Comment utiliser un rapporteur ?", "On place le centre sur le sommet, le zéro sur un côté, puis on lit sur la graduation qui part de ce zéro."),
           ("Qu’est-ce qu’une bissectrice ?", "La demi-droite qui partage un angle en deux angles de même mesure.")]
    unit("6e", R, "angles", "E",
         "Reconnaître et nommer des angles (aigu, droit, obtus, plat) ; mesurer un angle avec un rapporteur ; connaître le vocabulaire des angles (adjacents, opposés par le sommet, supplémentaires) ; utiliser la somme des angles d’un triangle ; connaître la bissectrice",
         "Les angles", "Angles",
         "Fiches de maths 6e sur les angles : nature, mesure au rapporteur, angles adjacents, opposés et supplémentaires, angles du triangle et bissectrice. 100 exercices corrigés.",
         "Somme des angles d’un triangle = 180°", "Angles opposés par le sommet : égaux.", body, faq, sets, 14)


if __name__ == "__main__":
    main()
