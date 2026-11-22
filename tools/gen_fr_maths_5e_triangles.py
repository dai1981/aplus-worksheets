# -*- coding: utf-8 -*-
"""
France Maths 5e : Triangles (inégalité triangulaire, angles, constructions, droites remarquables)
  python3 tools/gen_fr_maths_5e_triangles.py
Construire un triangle (existence), somme des angles, triangles particuliers, médiatrices et cercle circonscrit, hauteurs, médianes.
Erreurs : croire qu’on peut toujours construire un triangle avec trois longueurs, confondre hauteur et médiane, oublier que les hauteurs peuvent sortir du triangle.
"""
import random
from fr_c4 import *

R = random.Random(60214)
K = Kids(R)


def s1():
    a, b = R.randint(2, 12), R.randint(2, 12)
    k = R.choice(["oui", "non", "plat"])
    if k == "oui":
        c = R.randint(abs(a - b) + 1, a + b - 1)
    elif k == "non":
        c = a + b + R.randint(1, 5)
    else:
        c = a + b
    xs = R.sample([a, b, c], 3)
    ans = {"oui": "oui", "non": "non, c’est impossible", "plat": "non : les trois points sont alignés"}[k]
    return M("Peut-on construire un triangle dont les côtés mesurent %d cm, %d cm et %d cm ?" % tuple(xs), ans, [x for x in ["oui", "non, c’est impossible", "non : les trois points sont alignés", "oui, s’il est rectangle"] if x != ans],
             "On compare le plus grand côté (%d cm) à la somme des deux autres (%d cm) : %s." % (max(xs), sum(xs) - max(xs),
             "%d &lt; %d, donc <b>oui</b>" % (max(xs), sum(xs) - max(xs)) if k == "oui" else "%d &gt; %d, donc <b>c’est impossible</b>" % (max(xs), sum(xs) - max(xs)) if k == "non" else "il y a égalité : le triangle est « aplati », <b>les points sont alignés</b>"))


def s2():
    k = R.choice(["third", "iso_base", "iso_top", "rect", "equi"])
    if k == "third":
        a, b = R.randint(20, 100), R.randint(20, 100)
        c = 180 - a - b
        if c <= 5:
            return None
        return M("Dans le triangle ABC, Â = %d° et B̂ = %d°. Combien mesure Ĉ ?" % (a, b), "%d°" % c, ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (90 - c if c < 90 else c - 10)], "180 − %d − %d = <b>%d°</b>." % (a, b, c))
    if k == "iso_base":
        t = R.choice(range(20, 161, 10))
        return M("ABC est isocèle en A et Â = %d°. Combien mesure B̂ ?" % t, "%s°" % d(Fr(180 - t, 2)), ["%d°" % (180 - t), "%d°" % t, "%s°" % d(Fr(180 + t, 2)) if t < 180 else "1°"],
                 "Les angles à la base sont égaux : (180 − %d) ÷ 2 = <b>%s°</b>." % (t, d(Fr(180 - t, 2))))
    if k == "iso_top":
        b = R.choice(range(20, 86, 5))
        return M("ABC est isocèle en A et B̂ = %d°. Combien mesure Â ?" % b, "%d°" % (180 - 2 * b), ["%d°" % (180 - b), "%d°" % b, "%s°" % d(Fr(180 - b, 2))], "Ĉ = B̂ = %d° ; Â = 180 − 2 × %d = <b>%d°</b>." % (b, b, 180 - 2 * b))
    if k == "rect":
        a = R.randint(15, 75)
        return M("ABC est rectangle en C et Â = %d°. Combien mesure B̂ ?" % a, "%d°" % (90 - a), ["%d°" % (180 - a), "%d°" % a if a != 45 else "55°", "%d°" % (90 + a)], "90 − %d = <b>%d°</b>." % (a, 90 - a))
    return M("Un triangle a deux angles de 60°. Quelle est sa nature ?", "équilatéral", ["isocèle seulement", "rectangle", "quelconque"], "Le troisième angle vaut 180 − 120 = 60° : les trois angles sont égaux, il est <b>équilatéral</b>.")


DR = [("La médiatrice d’un côté d’un triangle est…", "la perpendiculaire à ce côté passant par son milieu", ["la droite passant par un sommet et le milieu du côté opposé", "la perpendiculaire à un côté passant par le sommet opposé", "la droite qui partage un angle en deux"]),
      ("Une hauteur d’un triangle est…", "la droite passant par un sommet et perpendiculaire au côté opposé", ["la droite passant par un sommet et le milieu du côté opposé", "la médiatrice d’un côté", "le plus grand côté"]),
      ("Une médiane d’un triangle est…", "la droite passant par un sommet et le milieu du côté opposé", ["la perpendiculaire à un côté passant par son milieu", "la droite passant par un sommet et perpendiculaire au côté opposé", "un côté du triangle"]),
      ("Le point de concours des médiatrices d’un triangle est…", "le centre du cercle circonscrit", ["le milieu du plus grand côté", "toujours à l’intérieur du triangle", "un sommet du triangle"]),
      ("Dans un triangle, les trois hauteurs…", "sont concourantes (elles se coupent en un même point)", ["sont parallèles", "ne se coupent jamais", "ont la même longueur"]),
      ("Une médiane partage le triangle en deux triangles…", "de même aire", ["de même périmètre", "isocèles", "rectangles"]),
      ("Dans un triangle obtus, l’orthocentre (point de concours des hauteurs) est…", "à l’extérieur du triangle", ["toujours à l’intérieur", "au milieu d’un côté", "sur un sommet"]),
      ("Dans un triangle rectangle, les hauteurs se coupent…", "au sommet de l’angle droit", ["au milieu de l’hypoténuse", "à l’extérieur du triangle", "elles ne se coupent pas"])]


def s3():
    q, a, w = R.choice(DR)
    if R.random() < 0.4:
        O, A, B, C = R.sample("OABCDEFIJ", 4)
        v = Fr(R.randint(20, 90), 10)
        return M("%s est le point de concours des médiatrices du triangle %s%s%s et %s%s = %s cm. Combien mesure %s%s ?" % (O, A, B, C, O, A, d(v), O, B), "%s cm" % d(v), ["%s cm" % d(2 * v), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                 "%s est le centre du cercle circonscrit : %s%s = %s%s = %s%s = <b>%s cm</b>." % (O, O, A, O, B, O, C, d(v)))
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s4():
    k = R.choice(["aire", "aire2", "med"])
    b, h = R.randint(3, 15), R.randint(2, 12)
    if k == "aire":
        return M("Un triangle a une base de %d cm et une hauteur relative à cette base de %d cm. Quelle est son aire ?" % (b, h), "%s cm²" % d(Fr(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(Fr(b * h, 4)) if (b * h) % 4 == 0 else "%s cm²" % d(Fr(b * h, 2) + 1)],
                 "A = base × hauteur ÷ 2 = %d × %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(Fr(b * h, 2))))
    if k == "aire2":
        A = Fr(b * h, 2)
        return M("Un triangle a une aire de %s cm² et une base de %d cm. Quelle est la hauteur relative à cette base ?" % (d(A), b), "%d cm" % h, ["%s cm" % d(A / b), "%s cm" % d(A - b), "%d cm" % (2 * h)],
                 "h = 2 × A ÷ base = 2 × %s ÷ %d = <b>%d cm</b>." % (d(A), b, h))
    A = Fr(b * h, 2)
    return M("Une médiane partage un triangle d’aire %s cm² en deux triangles. Quelle est l’aire de chacun ?" % d(A), "%s cm²" % d(A / 2), ["%s cm²" % d(A), "%s cm²" % d(A * 2), "%s cm²" % d(A / 3)],
             "Une médiane partage le triangle en deux triangles de même aire : <b>%s cm²</b>." % d(A / 2))


def s5():
    k = R.choice(["peri", "constr", "iso"])
    if k == "peri":
        a, b = R.randint(3, 9), R.randint(3, 9)
        if b >= 2 * a:
            return None
        return M("Un triangle isocèle a deux côtés de %d cm et une base de %d cm. Quel est son périmètre ?" % (a, b), "%d cm" % (2 * a + b), ["%d cm" % (a + b), "%d cm" % (a + 2 * b), "%d cm" % (3 * a)], "%d + %d + %d = <b>%d cm</b>." % (a, a, b, 2 * a + b))
    if k == "iso":
        p = R.randint(12, 40)
        b = R.randint(2, p // 2 - 1)
        if (p - b) % 2:
            return None
        a = (p - b) // 2
        if b >= 2 * a:
            return None
        return M("Un triangle isocèle a un périmètre de %d cm et une base de %d cm. Combien mesure chacun des deux côtés égaux ?" % (p, b), "%d cm" % a, ["%d cm" % (p - b), "%s cm" % d(Fr(p, 3)), "%d cm" % (a + 1)],
                 "(%d − %d) ÷ 2 = <b>%d cm</b>." % (p, b, a))
    V = [("Pour construire un triangle connaissant ses trois côtés, on utilise…", "la règle et le compas", ["le rapporteur seulement", "l’équerre seulement", "aucun instrument"]),
         ("Pour construire un triangle connaissant un côté et les deux angles adjacents, on utilise…", "la règle et le rapporteur", ["le compas seulement", "l’équerre seulement", "la règle seulement"]),
         ("On connaît deux côtés et l’angle compris entre eux. Combien de triangles différents peut-on construire ?", "un seul (à un déplacement près)", ["deux", "une infinité", "aucun"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def main():
    seen = set()
    sets = [("Peut-on construire le triangle ?", mix(R, seen, [(s1, 20)])), ("Angles d’un triangle", mix(R, seen, [(s2, 20)])),
            ("Droites remarquables", mix(R, seen, [(s3, 20)])), ("Aire du triangle et médiane", mix(R, seen, [(s4, 20)])), ("Problèmes et constructions", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Inégalité triangulaire</b> : un triangle existe si le plus grand côté est plus petit que la somme des deux autres.",
              "La somme des angles d’un triangle vaut 180° (on le démontre avec une parallèle et les angles alternes-internes).",
              "Médiatrices → centre du cercle circonscrit ; hauteurs (perpendiculaires issues d’un sommet) → orthocentre ; médianes (sommet–milieu du côté opposé)."],
             [("Côtés 4 cm, 5 cm, 10 cm ?", ["4 + 5 = 9", "10 &gt; 9"], "impossible")],
             [["Croire qu’on peut toujours construire un triangle", "Avec 4 cm, 5 cm et 10 cm, les deux petits côtés ne se rejoignent pas."],
              ["Confondre hauteur et médiane", "La hauteur est perpendiculaire au côté ; la médiane passe par son milieu."],
              ["Croire que les hauteurs restent dans le triangle", "Dans un triangle obtus, elles se coupent à l’extérieur."]])
    faq = [("Pourquoi la somme des angles vaut-elle 180° ?", "En traçant la parallèle à un côté passant par le sommet opposé, les trois angles se retrouvent côte à côte et forment un angle plat."),
           ("Que se passe-t-il si le plus grand côté est égal à la somme des deux autres ?", "Le triangle est aplati : les trois sommets sont alignés.")]
    unit("5e", R, "triangles", "E",
         "Démontrer et utiliser la somme des angles d’un triangle ; construire des triangles (inégalité triangulaire) ; connaître les médiatrices et le cercle circonscrit, les hauteurs, les médianes ; calculer l’aire d’un triangle",
         "Les triangles", "Triangles",
         "Fiches de maths 5e sur les triangles : inégalité triangulaire, somme des angles, triangles isocèles et rectangles, médiatrices, hauteurs, médianes et aire. 100 exercices corrigés.",
         "Somme des angles = 180°", "Plus grand côté &lt; somme des deux autres.", body, faq, sets, 14)


if __name__ == "__main__":
    main()
