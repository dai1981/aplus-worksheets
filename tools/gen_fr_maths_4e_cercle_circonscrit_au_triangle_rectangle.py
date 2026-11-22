# -*- coding: utf-8 -*-
"""
France Maths 4e : Cercle circonscrit à un triangle rectangle
  python3 tools/gen_fr_maths_4e_cercle_circonscrit_au_triangle_rectangle.py
Erreurs : rayon = hypoténuse, centre au sommet de l’angle droit, médiane = hypoténuse, oublier la réciproque.
"""
import random
import math
from fr_c4 import *

R = random.Random(60315)
K = Kids(R)
LET = ["ABC", "EFG", "RST", "KLM", "DEF", "PQR", "IJK", "UVW"]
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (15, 20, 25), (10, 24, 26)]


def s1():
    L = R.choice(LET)
    V, P, Q = L
    h = R.choice([R.randint(4, 30), Fr(R.randint(31, 199), 10)])
    k = R.choice(["centre", "rayon", "diam", "rayon"])
    if k == "centre":
        return M("Le triangle %s est rectangle en %s. Où se trouve le centre de son cercle circonscrit ?" % (L, V), "au milieu de [%s%s]" % (P, Q), ["en %s" % V, "au milieu de [%s%s]" % (V, P), "à l’extérieur du triangle"],
                 "Le centre du cercle circonscrit à un triangle rectangle est <b>le milieu de l’hypoténuse [%s%s]</b>." % (P, Q))
    if k == "rayon":
        return M("Le triangle %s est rectangle en %s et %s%s = %s cm. Quel est le rayon de son cercle circonscrit ?" % (L, V, P, Q, d(h)), "%s cm" % d(Fr(h) / 2), ["%s cm" % d(h), "%s cm" % d(Fr(h) * 2), "%s cm" % d(Fr(h) / 4)],
                 "L’hypoténuse est un diamètre : rayon = %s ÷ 2 = <b>%s cm</b>." % (d(h), d(Fr(h) / 2)))
    r = h
    return M("Un triangle %s rectangle en %s est inscrit dans un cercle de rayon %s cm. Combien mesure %s%s ?" % (L, V, d(r), P, Q), "%s cm" % d(Fr(r) * 2), ["%s cm" % d(r), "%s cm" % d(Fr(r) / 2), "on ne peut pas savoir"],
             "L’hypoténuse [%s%s] est un diamètre : %s%s = 2 × %s = <b>%s cm</b>." % (P, Q, P, Q, d(r), d(Fr(r) * 2)))


def s2():
    L = R.choice(LET)
    V, P, Q = L
    O = R.choice([x for x in "OHIJ" if x not in L])
    h = R.randint(3, 20) * 2
    k = R.choice(["med", "med", "medinv"])
    if k == "med":
        return M("Le triangle %s est rectangle en %s, %s est le milieu de [%s%s] et %s%s = %d cm. Combien mesure %s%s ?" % (L, V, O, P, Q, P, Q, h, O, V), "%d cm" % (h // 2), ["%d cm" % h, "%d cm" % (h // 4) if h % 4 == 0 else "%s cm" % d(Fr(h, 4)), "on ne peut pas savoir"],
                 "%s est le centre du cercle circonscrit, qui passe par %s : %s%s = %s%s = %s%s = <b>%d cm</b>." % (O, V, O, V, O, P, O, Q, h // 2))
    return M("Le triangle %s est rectangle en %s et la médiane issue de %s mesure %d cm. Combien mesure l’hypoténuse ?" % (L, V, V, h // 2), "%d cm" % h, ["%d cm" % (h // 2), "%d cm" % (h * 2), "%d cm" % (h // 2 + 1)],
             "La médiane issue de l’angle droit mesure la moitié de l’hypoténuse : <b>%d cm</b>." % h)


def s3():
    V = [("C est un point du cercle de diamètre [AB] (C différent de A et B). Que peut-on dire du triangle ABC ?", "il est rectangle en C", ["il est rectangle en A", "il est isocèle en C", "il est équilatéral"]),
         ("Si un triangle est inscrit dans un cercle et qu’un de ses côtés est un diamètre, alors…", "il est rectangle", ["il est isocèle", "il est équilatéral", "on ne peut rien dire"]),
         ("Le triangle EFG est rectangle en E. Quel segment est un diamètre de son cercle circonscrit ?", "[FG]", ["[EF]", "[EG]", "la hauteur issue de E"]),
         ("Dans le triangle ABC, la médiane issue de A mesure la moitié de [BC]. Que peut-on en déduire ?", "ABC est rectangle en A", ["ABC est isocèle en A", "ABC est rectangle en B", "on ne peut rien déduire"]),
         ("M est le milieu de [RS] et MT = MR = MS. Quelle est la nature du triangle RST ?", "rectangle en T", ["rectangle en M", "équilatéral", "isocèle en R"]),
         ("Le centre du cercle circonscrit à un triangle rectangle est-il toujours sur un côté du triangle ?", "oui, au milieu de l’hypoténuse", ["non, il est toujours à l’intérieur", "non, il est toujours à l’extérieur", "oui, sur un sommet"]),
         ("Pour tracer le cercle circonscrit à un triangle rectangle, il suffit de…", "placer le milieu de l’hypoténuse et tracer le cercle passant par les sommets", ["tracer les trois hauteurs", "prendre le sommet de l’angle droit comme centre", "tracer un cercle de rayon égal à l’hypoténuse"]),
         ("A, B, C sont sur un cercle de centre O et O est le milieu de [AB]. L’angle ACB mesure…", "90°", ["45°", "180°", "60°"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3b():
    L = R.choice(LET)
    V, P, Q = L
    O = R.choice([x for x in "OHIJ" if x not in L])
    r = R.randint(2, 9)
    k = R.choice(["angle", "rayon"])
    if k == "angle":
        return M("[%s%s] est un diamètre d’un cercle de rayon %d cm et %s est un point du cercle. Combien mesure l’angle %s%s%s ?" % (P, Q, r, V, P, V, Q), "90°", ["45°", "180°", "%d°" % (2 * r * 10) if 2 * r * 10 not in (90, 180, 45) else "60°"],
                 "Un triangle inscrit dans un cercle dont un côté est un diamètre est rectangle : l’angle en %s mesure <b>90°</b>." % V)
    a, b, c = R.choice(TRIP)
    return M("Le triangle %s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Quel est le rayon de son cercle circonscrit ?" % (L, V, V, P, a, V, Q, b), "%s cm" % d(Fr(c, 2)),
             ["%d cm" % c, "%s cm" % d(Fr(a + b, 2)), "%s cm" % d(Fr(c, 4))], "Pythagore : %s%s = √(%d + %d) = %d cm ; rayon = %d ÷ 2 = <b>%s cm</b>." % (P, Q, a * a, b * b, c, c, d(Fr(c, 2))))


def s4():
    a, b, c = R.choice(TRIP)
    L = R.choice(LET)
    V, P, Q = L
    k = R.choice(["perim", "aire", "cote"])
    if k == "perim":
        v = Fr(round(math.pi * c * 10), 10)
        return M("Le triangle %s est rectangle en %s avec %s%s = %d cm. Quel est le périmètre de son cercle circonscrit, arrondi au dixième ?" % (L, V, P, Q, c), "%s cm" % d(v),
                 ["%s cm" % d(Fr(round(math.pi * c * 2 * 10), 10)), "%s cm" % d(Fr(round(math.pi * c * c / 4 * 10), 10)), "%s cm" % d(Fr(round(math.pi * c / 2 * 10), 10))],
                 "Diamètre %d cm ; périmètre = π × %d ≈ <b>%s cm</b>." % (c, c, d(v)))
    if k == "aire":
        v = Fr(round(math.pi * c * c / 4 * 10), 10)
        return M("Le triangle %s est rectangle en %s avec %s%s = %d cm. Quelle est l’aire du disque circonscrit, arrondie au dixième ?" % (L, V, P, Q, c), "%s cm²" % d(v),
                 ["%s cm²" % d(Fr(round(math.pi * c * c * 10), 10)), "%s cm²" % d(Fr(round(math.pi * c * 10), 10)), "%s cm²" % d(Fr(round(math.pi * c * c / 2 * 10), 10))],
                 "Rayon %s cm ; aire = π × %s² ≈ <b>%s cm²</b>." % (d(Fr(c, 2)), d(Fr(c, 2)), d(v)))
    return M("Le triangle %s, inscrit dans un cercle de diamètre [%s%s] = %d cm, a %s%s = %d cm. Combien mesure %s%s ?" % (L, P, Q, c, V, P, a, V, Q), "%d cm" % b, ["%d cm" % (c - a), "%s cm" % d(Fr(round(math.sqrt(c * c + a * a) * 10), 10)), "%d cm" % (c + a)],
             "%s est sur le cercle de diamètre [%s%s], donc le triangle est rectangle en %s : %s%s² = %d − %d = %d, %s%s = <b>%d cm</b>." % (V, P, Q, V, V, Q, c * c, a * a, b * b, V, Q, b))


def s5():
    k = R.choice(["table", "jardin", "equerre", "verif"])
    a, b, c = R.choice(TRIP)
    if k == "table":
        return M("On veut poser un plateau rectangulaire de %d cm sur %d cm sur une table ronde, ses quatre coins juste au bord. Quel diamètre doit avoir la table ?" % (a * 10, b * 10), "%d cm" % (c * 10), ["%d cm" % ((a + b) * 10), "%d cm" % (c * 5), "%d cm" % (b * 10)],
                 "Les coins sont sur le cercle : la diagonale est un diamètre, √(%s + %s) = <b>%d cm</b>." % (num((a * 10) ** 2), num((b * 10) ** 2), c * 10))
    if k == "jardin":
        return M("Un jardinier tend une corde de %d m entre deux piquets A et B, et place un piquet C à %s m du milieu de [AB]. Le triangle ABC est-il rectangle en C ?" % (2 * a, d(a)), "oui", ["non", "seulement si C est sur [AB]", "on ne peut pas savoir"],
                 "La médiane issue de C mesure la moitié de AB : C est sur le cercle de diamètre [AB], donc <b>oui</b>.")
    if k == "equerre":
        return M("Pour trouver le centre d’un disque en carton, on place le coin d’une équerre sur le bord : les côtés coupent le bord en P et Q. Que représente [PQ] ?", "un diamètre", ["un rayon", "une corde quelconque", "la moitié d’un rayon"],
                 "L’angle droit est inscrit : [PQ] est <b>un diamètre</b> ; en recommençant, le centre est l’intersection de deux diamètres.")
    m = R.randint(3, 12)
    t = m + R.choice([0, 0, 1, -1])
    ok = t == m
    return M("Dans le triangle ABC, I est le milieu de [BC], BC = %d cm et IA = %d cm. Le triangle ABC est-il rectangle en A ?" % (2 * m, t), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "il est rectangle en I"],
             "%s" % ("IA = BC ÷ 2 : A est sur le cercle de diamètre [BC], <b>oui</b>." if ok else "IA ≠ BC ÷ 2 : A n’est pas sur le cercle de diamètre [BC], <b>non</b>."))


def main():
    seen = set()
    sets = [("Centre et rayon", mix(R, seen, [(s1, 20)])), ("Médiane issue de l’angle droit", mix(R, seen, [(s2, 20)])),
            ("Propriétés et réciproque", mix(R, seen, [(s3, 8), (s3b, 12)])), ("Avec Pythagore et le cercle", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Si un triangle est rectangle, son cercle circonscrit a pour <b>diamètre l’hypoténuse</b> : son centre est le milieu de l’hypoténuse.",
              "Conséquence : la médiane issue du sommet de l’angle droit mesure la moitié de l’hypoténuse.",
              "<b>Réciproque</b> : si un point C est sur le cercle de diamètre [AB] (C ≠ A, B), alors le triangle ABC est rectangle en C."],
             [("ABC rectangle en A, BC = 10 cm", ["le centre O est le milieu de [BC]", "rayon = BC ÷ 2"], "rayon 5 cm, OA = 5 cm")],
             [["Prendre l’hypoténuse comme rayon", "L’hypoténuse est un diamètre : le rayon en est la moitié."], ["Placer le centre au sommet de l’angle droit", "Le centre est au milieu de l’hypoténuse."],
              ["Croire que tout triangle inscrit est rectangle", "Il faut qu’un côté soit un diamètre."]])
    faq = [("Pourquoi l’hypoténuse est-elle un diamètre ?", "Un rectangle a des diagonales de même longueur qui se coupent en leur milieu : le milieu de l’hypoténuse est à égale distance des trois sommets."),
           ("À quoi sert la réciproque ?", "À prouver qu’un triangle est rectangle sans connaître ses longueurs, seulement avec un cercle.")]
    unit("4e", R, "cercle-circonscrit-au-triangle-rectangle", "E",
         "Caractériser le triangle rectangle par son cercle circonscrit : l’hypoténuse est un diamètre ; utiliser la médiane issue de l’angle droit ; utiliser la réciproque pour démontrer qu’un triangle est rectangle",
         "Cercle circonscrit à un triangle rectangle", "Cercle circonscrit au triangle rectangle",
         "Fiches de maths 4e sur le cercle circonscrit au triangle rectangle : centre et rayon, médiane, réciproque, calculs avec Pythagore et problèmes. 100 exercices corrigés.",
         "L’hypoténuse est un diamètre du cercle circonscrit", "Centre = milieu de l’hypoténuse", body, faq, sets, 15)


if __name__ == "__main__":
    main()
