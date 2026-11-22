# -*- coding: utf-8 -*-
"""
France Maths 6e : Médiatrice et cercle
  python3 tools/gen_fr_maths_6e_mediatrice_et_cercle.py
Médiatrice d’un segment (définition, propriété d’équidistance), cercle (centre, rayon, diamètre, corde), cercle circonscrit
à un triangle (point de concours des médiatrices), régionnement du plan.
Erreurs : croire que la médiatrice est n’importe quelle perpendiculaire, confondre rayon et diamètre, disque et cercle.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FP

R = random.Random(60115)
K = Kids(R)
FP.R = R


def s1():
    A, B, M_ = R.sample("ABCDEFGHIJKLMNP", 3)
    v = Fr(R.randint(20, 90), 10)
    k = R.choice(["dist", "def", "def2"])
    if k == "dist":
        return M("%s est sur la médiatrice du segment [%s%s]. %s%s = %s cm. Combien mesure %s%s ?" % (M_, A, B, M_, A, d(v), M_, B), "%s cm" % d(v), ["%s cm" % d(v * 2), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                 "Tout point de la médiatrice est à égale distance des extrémités : %s%s = %s%s = <b>%s cm</b>." % (M_, B, M_, A, d(v)))
    if k == "def":
        return M("La médiatrice d’un segment [%s%s] est…" % (A, B), "la droite perpendiculaire à [%s%s] qui passe par son milieu" % (A, B),
                 ["n’importe quelle droite perpendiculaire à [%s%s]" % (A, B), "la droite qui passe par %s et %s" % (A, B), "le cercle de diamètre [%s%s]" % (A, B)],
                 "La médiatrice est <b>la perpendiculaire à [%s%s] passant par son milieu</b>." % (A, B))
    return M("Quels points sont à égale distance de %s et de %s ?" % (A, B), "les points de la médiatrice de [%s%s]" % (A, B), ["seulement le milieu de [%s%s]" % (A, B), "les points de la droite (%s%s)" % (A, B), "les points du cercle de centre %s" % A],
             "L’ensemble des points équidistants de %s et %s est <b>la médiatrice de [%s%s]</b>." % (A, B, A, B))


def s2():
    A, B, M_ = R.sample("ABCDEFGHIJKLMNP", 3)
    a = Fr(R.randint(20, 90), 10)
    eq = R.random() < 0.5
    b = a if eq else a + Fr(R.choice([-3, -2, -1, 1, 2, 3]), 10)
    return M("%s%s = %s cm et %s%s = %s cm. Le point %s est-il sur la médiatrice de [%s%s] ?" % (M_, A, d(a), M_, B, d(b), M_, A, B), "oui" if eq else "non",
             ["non" if eq else "oui", "seulement s’il est le milieu de [%s%s]" % (A, B), "on ne peut pas savoir"],
             "%s est sur la médiatrice si et seulement si %s%s = %s%s. Ici, %s : <b>%s</b>." % (M_, M_, A, M_, B, "c’est le cas" if eq else "%s ≠ %s" % (d(a), d(b)), "oui" if eq else "non"))


def s3():
    k = R.choice(["seg", "r2d", "d2r", "corde", "comp"])
    if k == "seg":
        return FP.s4() if False else _seg()
    if k == "r2d":
        r = Fr(R.randint(10, 90), 10)
        return M("Le rayon d’un cercle mesure %s cm. Combien mesure son diamètre ?" % d(r), "%s cm" % d(2 * r), ["%s cm" % d(r / 2), "%s cm" % d(r), "%s cm" % d(r + 2)],
                 "Le diamètre est le double du rayon : <b>%s cm</b>." % d(2 * r))
    if k == "d2r":
        dd = Fr(R.randint(20, 180), 10)
        return M("Le diamètre d’un cercle mesure %s cm. Combien mesure son rayon ?" % d(dd), "%s cm" % d(dd / 2), ["%s cm" % d(dd * 2), "%s cm" % d(dd), "%s cm" % d(dd - 2) if dd > 2 else "%s cm" % d(dd + 1)],
                 "Le rayon est la moitié du diamètre : <b>%s cm</b>." % d(dd / 2))
    if k == "corde":
        V = [("Un segment qui relie deux points d’un cercle s’appelle…", "une corde", ["un rayon", "un centre", "un arc"]),
             ("Un diamètre est…", "une corde qui passe par le centre", ["la moitié d’un rayon", "un point du cercle", "un arc de cercle"]),
             ("Quelle est la plus longue corde d’un cercle ?", "un diamètre", ["un rayon", "n’importe quelle corde", "elles ont toutes la même longueur"]),
             ("La différence entre un cercle et un disque est…", "le cercle est la ligne, le disque est la surface", ["il n’y a aucune différence", "le disque est plus petit", "le cercle n’a pas de centre"]),
             ("Tous les points d’un cercle de centre O et de rayon 3 cm sont…", "à 3 cm de O", ["à moins de 3 cm de O", "à 6 cm de O", "à plus de 3 cm de O"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    r = R.randint(2, 9)
    return M("Pour tracer un cercle de %d cm de diamètre, quel écartement faut-il donner au compas ?" % (2 * r), "%d cm" % r, ["%d cm" % (2 * r), "%d cm" % (4 * r), "%d cm" % (r + 1)],
             "L’écartement du compas est le rayon : <b>%d cm</b>." % r)


def _seg():
    seg = R.choice(["rayon", "diamètre", "corde"])
    import math
    r = R.randint(50, 75)
    cx = cy = 90
    s = ["<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (cx, cy, r, FILL, GREEN), "<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, INK), text(cx - 10, cy - 6, "O", 14)]
    a = R.uniform(0, 2 * math.pi)
    x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
    if seg == "rayon":
        s.append(line(cx, cy, x1, y1, RED, 3))
    elif seg == "diamètre":
        s.append(line(cx - r * math.cos(a), cy - r * math.sin(a), x1, y1, RED, 3))
    else:
        b = a + R.uniform(1.2, 2.4)
        s.append(line(cx + r * math.cos(b), cy + r * math.sin(b), x1, y1, RED, 3))
    svg = wrap(180, 180, "".join(s), "un cercle de centre O et un segment rouge")
    art = {"rayon": "un rayon", "diamètre": "un diamètre", "corde": "une corde (qui n’est pas un diamètre)"}
    return M("<div class='qfig'>%s</div>Comment s’appelle le segment rouge ?" % svg, art[seg], [v for k, v in art.items() if k != seg] + ["un arc"],
             {"rayon": "Il relie le centre O à un point du cercle : c’est <b>un rayon</b>.", "diamètre": "Il relie deux points du cercle en passant par O : <b>un diamètre</b>.",
              "corde": "Il relie deux points du cercle sans passer par O : <b>une corde</b>."}[seg])


def s4():
    A, B, C, O = R.sample("ABCDEFGHIJKLMNPRS", 4)
    k = R.choice(["centre", "dist", "dist", "rect"])
    if k == "centre":
        return M("Le centre du cercle circonscrit au triangle %s%s%s est…" % (A, B, C), "le point de concours des médiatrices des côtés", ["le milieu du plus grand côté", "le point de concours des bissectrices", "le sommet %s" % A],
                 "Le centre est à égale distance des trois sommets : c’est <b>le point de concours des médiatrices</b>.")
    if k == "dist":
        v = Fr(R.randint(20, 80), 10)
        return M("%s est le centre du cercle circonscrit au triangle %s%s%s et %s%s = %s cm. Combien mesure %s%s ?" % (O, A, B, C, O, A, d(v), O, C), "%s cm" % d(v), ["%s cm" % d(2 * v), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                 "%s est à égale distance des trois sommets : %s%s = %s%s = <b>%s cm</b>." % (O, O, C, O, A, d(v)))
    return M("Combien de médiatrices faut-il tracer, au minimum, pour trouver le centre du cercle circonscrit à un triangle ?", "2", ["3", "1", "4"],
             "Les trois médiatrices se coupent en un même point : deux suffisent pour le trouver, la troisième sert à vérifier. Réponse : <b>2</b>.")


def s5():
    A, B = R.sample("ABCDEFGH", 2)
    r = R.randint(2, 6)
    k = R.choice(["disque", "cercle", "plus", "proche"])
    if k == "disque":
        return M("Où sont les points situés à moins de %d cm du point %s ?" % (r, A), "à l’intérieur du cercle de centre %s et de rayon %d cm" % (A, r),
                 ["sur le cercle de centre %s et de rayon %d cm" % (A, r), "à l’extérieur du cercle de centre %s et de rayon %d cm" % (A, r), "sur une droite passant par %s" % A],
                 "Ils forment le disque : <b>à l’intérieur du cercle de centre %s et de rayon %d cm</b>." % (A, r))
    if k == "cercle":
        return M("Où sont les points situés à exactement %d cm du point %s ?" % (r, A), "sur le cercle de centre %s et de rayon %d cm" % (A, r),
                 ["à l’intérieur du cercle de centre %s et de rayon %d cm" % (A, r), "sur le cercle de centre %s et de rayon %d cm" % (A, 2 * r), "sur la médiatrice d’un segment" ],
                 "Exactement %d cm de %s : <b>sur le cercle de centre %s et de rayon %d cm</b>." % (r, A, A, r))
    if k == "plus":
        return M("Où sont les points situés à plus de %d cm du point %s ?" % (r, A), "à l’extérieur du cercle de centre %s et de rayon %d cm" % (A, r),
                 ["à l’intérieur du cercle de centre %s et de rayon %d cm" % (A, r), "sur le cercle de centre %s et de rayon %d cm" % (A, r), "sur la droite (%s%s)" % (A, B)],
                 "<b>À l’extérieur du cercle de centre %s et de rayon %d cm</b>." % (A, r))
    return M("Deux écoles sont placées en %s et %s. Où sont les maisons plus proches de l’école %s que de l’école %s ?" % (A, B, A, B), "du côté de %s par rapport à la médiatrice de [%s%s]" % (A, A, B),
             ["sur la médiatrice de [%s%s]" % (A, B), "du côté de %s par rapport à la médiatrice de [%s%s]" % (B, A, B), "à l’intérieur du cercle de diamètre [%s%s]" % (A, B)],
             "La médiatrice partage le plan : <b>du côté de %s</b>, on est plus près de %s que de %s." % (A, A, B))


def main():
    seen = set()
    sets = [("La médiatrice", mix(R, seen, [(s1, 20)])), ("Sur la médiatrice ou non ?", mix(R, seen, [(s2, 20)])),
            ("Le cercle", mix(R, seen, [(s3, 20)])), ("Cercle circonscrit", mix(R, seen, [(s4, 20)])), ("Régions du plan", mix(R, seen, [(s5, 20)]))]
    body = L(["La <b>médiatrice</b> d’un segment est la droite perpendiculaire à ce segment passant par son milieu.",
              "Tout point de la médiatrice de [AB] est à égale distance de A et de B ; et tout point à égale distance de A et B est sur la médiatrice.",
              "Le cercle <b>circonscrit</b> à un triangle passe par ses trois sommets ; son centre est le point de concours des trois médiatrices."],
             [("M sur la médiatrice de [AB], MA = 4 cm", ["MA = MB"], "MB = 4 cm")],
             [["Tracer n’importe quelle perpendiculaire", "La médiatrice passe par le milieu du segment."],
              ["Confondre rayon et diamètre", "Le diamètre est le double du rayon."],
              ["Confondre cercle et disque", "Le cercle est le contour ; le disque est toute la surface."]])
    faq = [("Comment tracer une médiatrice au compas ?", "On trace deux arcs de même rayon centrés en A et en B ; la droite qui passe par leurs deux points d’intersection est la médiatrice."),
           ("Pourquoi le cercle circonscrit passe-t-il par les trois sommets ?", "Son centre est sur les trois médiatrices, donc à la même distance des trois sommets.")]
    unit("6e", R, "mediatrice-et-cercle", "E",
         "Connaître la médiatrice d’un segment et sa propriété caractéristique (équidistance) ; connaître le vocabulaire du cercle ; construire le cercle circonscrit à un triangle ; décrire des régions du plan avec un cercle ou une médiatrice",
         "Médiatrice et cercle", "Médiatrice et cercle",
         "Fiches de maths 6e sur la médiatrice et le cercle : définition, équidistance, rayon, diamètre, corde, cercle circonscrit et régions du plan. 100 exercices corrigés.",
         "Sur la médiatrice de [AB] : MA = MB.", "Centre du cercle circonscrit = point de concours des médiatrices.", body, faq, sets, 15)


if __name__ == "__main__":
    main()
