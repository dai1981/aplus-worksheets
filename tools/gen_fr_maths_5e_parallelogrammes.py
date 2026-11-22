# -*- coding: utf-8 -*-
"""
France Maths 5e : Les parallélogrammes (et rectangle, losange, carré)
  python3 tools/gen_fr_maths_5e_parallelogrammes.py
Définition, propriétés (côtés opposés, diagonales, angles), propriétés caractéristiques, parallélogrammes particuliers, calculs.
Erreurs : croire que les diagonales d’un parallélogramme sont égales ou perpendiculaires, confondre propriété et réciproque.
"""
import random
from fr_c4 import *

R = random.Random(60215)
K = Kids(R)


def nm():
    return "".join(R.sample("ABCDEFGHIJKLMNPRSTUV", 4))


def s1():
    A, B, C, D_ = nm()
    k = R.choice(["cote", "diag", "angle_opp", "angle_cons"])
    v = Fr(R.randint(20, 90), 10)
    if k == "cote":
        return M("%s%s%s%s est un parallélogramme et %s%s = %s cm. Combien mesure %s%s ?" % (A, B, C, D_, A, B, d(v), D_, C), "%s cm" % d(v), ["%s cm" % d(2 * v), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                 "Les côtés opposés d’un parallélogramme ont la même longueur : %s%s = %s%s = <b>%s cm</b>." % (D_, C, A, B, d(v)))
    if k == "diag":
        O = "O"
        return M("%s%s%s%s est un parallélogramme de centre O et %s%s = %s cm. Combien mesure O%s ?" % (A, B, C, D_, A, C, d(v), A), "%s cm" % d(v / 2), ["%s cm" % d(v), "%s cm" % d(2 * v), "on ne peut pas savoir"],
                 "Les diagonales se coupent en leur milieu O : O%s = %s%s ÷ 2 = <b>%s cm</b>." % (A, A, C, d(v / 2)))
    a = R.choice(range(40, 141, 5))
    if a == 90:
        return None
    if k == "angle_opp":
        return M("%s%s%s%s est un parallélogramme et l’angle en %s mesure %d°. Combien mesure l’angle en %s ?" % (A, B, C, D_, A, a, C), "%d°" % a, ["%d°" % (180 - a), "%d°" % (360 - a), "%d°" % (90 - a % 90)],
                 "Les angles opposés d’un parallélogramme sont égaux : <b>%d°</b>." % a)
    return M("%s%s%s%s est un parallélogramme et l’angle en %s mesure %d°. Combien mesure l’angle en %s ?" % (A, B, C, D_, A, a, B), "%d°" % (180 - a), ["%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a % 90)],
             "Deux angles consécutifs d’un parallélogramme sont supplémentaires : 180 − %d = <b>%d°</b>." % (a, 180 - a))


CAR = [("Si un quadrilatère a ses diagonales qui se coupent en leur milieu, alors c’est…", "un parallélogramme", ["un rectangle", "un losange", "un trapèze"]),
       ("Si un quadrilatère a ses côtés opposés parallèles deux à deux, alors c’est…", "un parallélogramme", ["un carré", "un trapèze rectangle", "un cerf-volant"]),
       ("Si un quadrilatère non croisé a deux côtés opposés parallèles et de même longueur, alors c’est…", "un parallélogramme", ["un trapèze", "un losange", "un rectangle"]),
       ("Si un parallélogramme a un angle droit, alors c’est…", "un rectangle", ["un losange", "un carré", "un trapèze"]),
       ("Si un parallélogramme a deux côtés consécutifs de même longueur, alors c’est…", "un losange", ["un rectangle", "un carré", "un trapèze"]),
       ("Si un parallélogramme a ses diagonales de même longueur, alors c’est…", "un rectangle", ["un losange", "un trapèze", "un carré, toujours"]),
       ("Si un parallélogramme a ses diagonales perpendiculaires, alors c’est…", "un losange", ["un rectangle", "un trapèze", "un carré, toujours"]),
       ("Un parallélogramme qui est à la fois un rectangle et un losange est…", "un carré", ["un trapèze", "un cerf-volant", "impossible"]),
       ("Les diagonales d’un rectangle…", "ont la même longueur et se coupent en leur milieu", ["sont perpendiculaires", "ne se coupent pas", "ont des longueurs différentes"]),
       ("Les diagonales d’un losange…", "sont perpendiculaires et se coupent en leur milieu", ["ont toujours la même longueur", "sont parallèles", "ne se coupent pas"])]


def s2():
    q, a, w = R.choice(CAR)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3():
    A, B, C, D_ = nm()
    k = R.choice(["rect", "los", "carre", "rien"])
    if k == "rect":
        return M("%s%s%s%s est un parallélogramme dont les diagonales [%s%s] et [%s%s] mesurent toutes les deux %d cm. Quelle est sa nature ?" % (A, B, C, D_, A, C, B, D_, R.randint(4, 12)), "un rectangle", ["un losange", "un carré", "on ne peut pas savoir"],
                 "Un parallélogramme dont les diagonales ont la même longueur est <b>un rectangle</b>.")
    if k == "los":
        return M("%s%s%s%s est un parallélogramme et %s%s = %s%s = %d cm. Quelle est sa nature ?" % (A, B, C, D_, A, B, B, C, R.randint(3, 9)), "un losange", ["un rectangle", "un carré", "on ne peut pas savoir"],
                 "Deux côtés consécutifs égaux : c’est <b>un losange</b>.")
    if k == "carre":
        return M("%s%s%s%s est un parallélogramme dont les diagonales sont perpendiculaires et de même longueur. Quelle est sa nature ?" % (A, B, C, D_), "un carré", ["un rectangle", "un losange seulement", "on ne peut pas savoir"],
                 "Diagonales de même longueur : rectangle ; perpendiculaires : losange ; les deux : <b>un carré</b>.")
    return M("%s%s%s%s est un parallélogramme et %s%s = %d cm, %s%s = %d cm. Est-ce forcément un rectangle ?" % (A, B, C, D_, A, B, R.randint(5, 9), B, C, R.randint(2, 4)), "non, on ne peut pas savoir", ["oui", "non, c’est un losange", "oui, c’est un carré"],
             "Deux longueurs de côtés ne disent rien sur les angles : <b>on ne peut pas savoir</b>.")


def s4():
    k = R.choice(["peri", "peri2", "aire"])
    a, b = R.randint(3, 15), R.randint(2, 10)
    if k == "peri":
        return M("Un parallélogramme a des côtés de %d cm et %d cm. Quel est son périmètre ?" % (a, b), "%d cm" % (2 * (a + b)), ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (2 * a + b)],
                 "Côtés opposés égaux : 2 × (%d + %d) = <b>%d cm</b>." % (a, b, 2 * (a + b)))
    if k == "peri2":
        return M("Un losange a un côté de %d cm. Quel est son périmètre ?" % a, "%d cm" % (4 * a), ["%d cm" % (2 * a), "%d cm" % (a * a), "%d cm" % (3 * a)], "4 côtés égaux : <b>%d cm</b>." % (4 * a))
    h = R.randint(2, 9)
    return M("Un parallélogramme a une base de %d cm et une hauteur de %d cm. Quelle est son aire ?" % (a, h), "%d cm²" % (a * h), ["%s cm²" % d(Fr(a * h, 2)), "%d cm²" % (2 * (a + h)), "%d cm²" % (a + h)],
             "A = base × hauteur = %d × %d = <b>%d cm²</b>." % (a, h, a * h))


def s5():
    A, B, C, D_ = nm()
    k = R.choice(["quatrieme", "milieu", "demo"])
    if k == "quatrieme":
        ax, ay, bx, by, cx, cy = [R.randint(-4, 4) for _ in range(6)]
        dx, dy = ax + cx - bx, ay + cy - by
        if len({(ax, ay), (bx, by), (cx, cy), (dx, dy)}) < 4 or (bx - ax) * (cy - ay) == (by - ay) * (cx - ax):
            return None
        co = lambda x, y: "(%s ; %s)" % (d(x), d(y))
        return M("Dans un repère, %s%s, %s%s et %s%s. Quelles sont les coordonnées de %s pour que %s%s%s%s soit un parallélogramme ?" % (A, co(ax, ay), B, co(bx, by), C, co(cx, cy), D_, A, B, C, D_),
                 co(dx, dy), [co(bx + cx - ax, by + cy - ay), co(ax + bx - cx, ay + by - cy), co(-dx, -dy) if (dx, dy) != (0, 0) else co(1, 1)],
                 "Dans %s%s%s%s, les diagonales [%s%s] et [%s%s] ont le même milieu : on passe de %s à %s comme de %s à %s. %s<b>%s</b>." % (A, B, C, D_, A, C, B, D_, B, A, C, D_, D_, co(dx, dy)))
    if k == "milieu":
        v = R.randint(2, 9)
        return M("%s%s%s%s est un parallélogramme de centre O et O%s = %d cm. Combien mesure %s%s ?" % (A, B, C, D_, B, v, B, D_), "%d cm" % (2 * v), ["%d cm" % v, "%s cm" % d(Fr(v, 2)), "on ne peut pas savoir"],
                 "O est le milieu de [%s%s] : %s%s = 2 × %d = <b>%d cm</b>." % (B, D_, B, D_, v, 2 * v))
    return M("Pour démontrer que %s%s%s%s est un parallélogramme, quelle information suffit ?" % (A, B, C, D_), "ses diagonales [%s%s] et [%s%s] ont le même milieu" % (A, C, B, D_),
             ["%s%s = %s%s" % (A, B, B, C), "il a quatre côtés", "l’angle en %s est aigu" % A], "Propriété caractéristique : <b>si les diagonales ont le même milieu, c’est un parallélogramme</b>.")


def main():
    seen = set()
    sets = [("Propriétés du parallélogramme", mix(R, seen, [(s1, 20)])), ("Reconnaître un quadrilatère", mix(R, seen, [(s2, 10), (s3, 10)])),
            ("Parallélogrammes particuliers", mix(R, seen, [(s3, 20)])), ("Périmètre et aire", mix(R, seen, [(s4, 20)])), ("Démontrer et construire", mix(R, seen, [(s5, 20)]))]
    body = L(["Un <b>parallélogramme</b> est un quadrilatère dont les côtés opposés sont parallèles deux à deux.",
              "Propriétés : côtés opposés de même longueur, angles opposés égaux, diagonales qui se coupent en leur milieu (centre de symétrie).",
              "Rectangle : parallélogramme avec un angle droit (diagonales égales). Losange : deux côtés consécutifs égaux (diagonales perpendiculaires). Carré : les deux."],
             [("Diagonales qui se coupent en leur milieu et sont perpendiculaires", ["parallélogramme", "+ diagonales perpendiculaires"], "un losange")],
             [["Croire que les diagonales d’un parallélogramme sont égales", "C’est vrai seulement pour le rectangle (et le carré)."],
              ["Croire qu’elles sont perpendiculaires", "C’est vrai seulement pour le losange (et le carré)."],
              ["Confondre une propriété et sa réciproque", "« Si c’est un parallélogramme, alors… » n’est pas la même phrase que « Si…, alors c’est un parallélogramme »."]])
    faq = [("Un carré est-il un parallélogramme ?", "Oui : c’est un parallélogramme qui est à la fois un rectangle et un losange."),
           ("Comment construire un parallélogramme ?", "Avec des parallèles, ou avec le compas en reportant les longueurs des côtés opposés, ou avec le milieu des diagonales.")]
    unit("5e", R, "parallelogrammes", "E",
         "Connaître la définition du parallélogramme, ses propriétés et ses propriétés caractéristiques (côtés, diagonales) ; connaître les cas du rectangle, du losange et du carré ; calculer l’aire d’un parallélogramme",
         "Les parallélogrammes", "Parallélogrammes",
         "Fiches de maths 5e sur les parallélogrammes : propriétés, diagonales, rectangle, losange, carré, périmètre, aire et démonstrations. 100 exercices corrigés.",
         "Diagonales qui se coupent en leur milieu.", "Côtés opposés parallèles et égaux.", body, faq, sets, 15)


if __name__ == "__main__":
    main()
