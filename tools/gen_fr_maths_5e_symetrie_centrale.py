# -*- coding: utf-8 -*-
"""
France Maths 5e : La symétrie centrale (demi-tour)
  python3 tools/gen_fr_maths_5e_symetrie_centrale.py
Image d’un point par la symétrie de centre O (le centre est le milieu de [AA’]), propriétés (conservation des longueurs, des angles,
image d’une droite parallèle), figures ayant un centre de symétrie, retrouver le centre.
Erreurs : confondre avec la symétrie axiale, ne changer qu’une coordonnée, croire que l’image d’une droite la coupe.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60212)
K = Kids(R)


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def s1():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == 0 or y == 0 or abs(x) == abs(y):
        return None
    svg = relabel(de_k8.kosy(pts=[(x, y, "A"), (0, 0, "O")], lo=-6, hi=6, u=20), "le point A et le centre O")
    return M("<div class='qfig'>%s</div>Quelles sont les coordonnées de A’, symétrique de A par rapport à O ?" % svg, co(-x, -y), [co(-x, y), co(x, -y), co(y, x)],
             "O est le milieu de [AA’] : on prend les opposés des deux coordonnées, A’<b>%s</b>." % co(-x, -y))


def s2():
    cx, cy = R.randint(-3, 3), R.randint(-3, 3)
    x, y = cx + R.randint(-3, 3), cy + R.randint(-3, 3)
    if (x, y) == (cx, cy) or (cx, cy) == (0, 0):
        return None
    ix, iy = 2 * cx - x, 2 * cy - y
    if max(abs(ix), abs(iy), abs(x), abs(y)) > 6:
        return None
    svg = relabel(de_k8.kosy(pts=[(x, y, "A"), (cx, cy, "C")], lo=-6, hi=6, u=20), "le point A et le centre C")
    return M("<div class='qfig'>%s</div>Quelles sont les coordonnées de A’, symétrique de A par rapport au point C ?" % svg, co(ix, iy), [co(-x, -y), co(2 * cx + x, 2 * cy + y) if (2 * cx + x, 2 * cy + y) != (ix, iy) else co(ix + 1, iy), co(cx - (y - cy), cy + (x - cx))],
             "De A à C : %s horizontalement, %s verticalement. On refait le même trajet après C : A’<b>%s</b>." % (d(cx - x), d(cy - y), co(ix, iy)))


PROP = [("Par une symétrie centrale, un segment de 5 cm a pour image…", "un segment de 5 cm", ["un segment de 10 cm", "un segment de 2,5 cm", "un point"]),
        ("Par une symétrie centrale, un angle de 40° a pour image…", "un angle de 40°", ["un angle de 140°", "un angle de 80°", "un angle de 320°"]),
        ("Par une symétrie centrale, l’image d’une droite qui ne passe pas par le centre est…", "une droite parallèle", ["une droite perpendiculaire", "la même droite", "un cercle"]),
        ("Par une symétrie centrale, l’image d’une droite qui passe par le centre est…", "elle-même", ["une droite perpendiculaire", "une droite parallèle distincte", "un point"]),
        ("Le symétrique du centre O par la symétrie de centre O est…", "le point O lui-même", ["un point à 1 cm de O", "il n’existe pas", "l’infini"]),
        ("La symétrie centrale de centre O correspond à…", "un demi-tour autour de O", ["un pliage le long d’une droite", "un quart de tour", "un glissement"]),
        ("Par une symétrie centrale, un cercle de rayon 3 cm a pour image…", "un cercle de rayon 3 cm", ["un cercle de rayon 6 cm", "une droite", "un disque de rayon 1,5 cm"]),
        ("Par une symétrie centrale, l’aire d’une figure…", "est conservée", ["double", "est divisée par 2", "devient nulle"])]


def s3():
    q, a, w = R.choice(PROP)
    if R.random() < 0.4:
        l = Fr(R.randint(20, 90), 10)
        return M("[AB] mesure %s cm. A’ et B’ sont les symétriques de A et B par rapport à O. Combien mesure [A’B’] ?" % d(l), "%s cm" % d(l), ["%s cm" % d(2 * l), "%s cm" % d(l / 2), "on ne peut pas savoir"],
                 "La symétrie centrale conserve les longueurs : <b>%s cm</b>." % d(l))
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


FIG = [("la lettre N", True), ("la lettre S", True), ("la lettre Z", True), ("la lettre H", True), ("la lettre X", True), ("la lettre O", True), ("la lettre I", True),
       ("la lettre A", False), ("la lettre E", False), ("la lettre T", False), ("la lettre K", False), ("la lettre L", False), ("la lettre M", False), ("la lettre V", False),
       ("un parallélogramme", True), ("un rectangle", True), ("un losange", True), ("un cercle", True), ("un triangle équilatéral", False), ("un trapèze qui n’est pas un parallélogramme", False),
       ("un carré", True), ("un triangle isocèle", False)]


def s4():
    f, ok = R.choice(FIG)
    return M("%s a-t-%s un centre de symétrie ?" % (f[0].upper() + f[1:], "elle" if f.startswith("la") or f.startswith("une") else "il"), "oui" if ok else "non",
             ["non" if ok else "oui", "oui, elle en a deux" if f.startswith("la") or f.startswith("une") else "oui, il en a deux", "on ne peut pas savoir"],
             ("<b>Oui</b> : après un demi-tour autour de son centre, la figure se superpose à elle-même." if ok else "<b>Non</b> : après un demi-tour, la figure ne se superpose à elle-même autour d’aucun point."))


def s5():
    k = R.choice(["centre", "dist", "coord"])
    if k == "centre":
        x, y = R.randint(-5, 5), R.randint(-5, 5)
        x2, y2 = x + 2 * R.randint(-3, 3), y + 2 * R.randint(-3, 3)
        if (x, y) == (x2, y2):
            return None
        return M("A%s et A’%s sont symétriques par rapport à un point O. Quelles sont les coordonnées de O ?" % (co(x, y), co(x2, y2)), co(Fr(x + x2, 2), Fr(y + y2, 2)),
                 [co(Fr(x2 - x, 2), Fr(y2 - y, 2)), co(x + x2, y + y2), co(Fr(x + x2, 2), Fr(y - y2, 2)) if y != y2 else co(0, 0)],
                 "O est le milieu de [AA’] : <b>%s</b>." % co(Fr(x + x2, 2), Fr(y + y2, 2)))
    if k == "dist":
        l = Fr(R.randint(15, 80), 10)
        return M("A’ est le symétrique de A par rapport à O et OA = %s cm. Combien mesure AA’ ?" % d(l), "%s cm" % d(2 * l), ["%s cm" % d(l), "%s cm" % d(l / 2), "on ne peut pas savoir"],
                 "O est le milieu de [AA’] : AA’ = 2 × OA = <b>%s cm</b>." % d(2 * l))
    l = Fr(R.randint(15, 80), 10)
    return M("A’ est le symétrique de A par rapport à O et AA’ = %s cm. Combien mesure OA’ ?" % d(l), "%s cm" % d(l / 2), ["%s cm" % d(l), "%s cm" % d(2 * l), "on ne peut pas savoir"],
             "O est le milieu de [AA’] : OA’ = AA’ ÷ 2 = <b>%s cm</b>." % d(l / 2))


def main():
    seen = set()
    sets = [("Symétrique par rapport à l’origine", mix(R, seen, [(s1, 20)])), ("Symétrique par rapport à un point", mix(R, seen, [(s2, 20)])),
            ("Propriétés", mix(R, seen, [(s3, 20)])), ("Centre de symétrie d’une figure", mix(R, seen, [(s4, 20)])), ("Le centre, milieu de [AA’]", mix(R, seen, [(s5, 20)]))]
    body = L(["Le symétrique A’ du point A par rapport à O est tel que <b>O est le milieu de [AA’]</b> : c’est un demi-tour autour de O.",
              "La symétrie centrale conserve les longueurs, les angles, les aires ; l’image d’une droite est une droite parallèle.",
              "Une figure a un <b>centre de symétrie</b> si elle est inchangée par un demi-tour autour de ce point (parallélogramme, cercle, lettre S…)."],
             [("A(2 ; −3), centre O(0 ; 0)", ["opposés des coordonnées"], "A’(−2 ; 3)")],
             [["Confondre avec la symétrie axiale", "Symétrie centrale : un demi-tour autour d’un point, pas un pliage."],
              ["Ne changer qu’une coordonnée", "Par rapport à l’origine, on change les deux signes."],
              ["Croire que l’image d’une droite la coupe", "L’image est une droite parallèle (ou la même si elle passe par O)."]])
    faq = [("Quelle différence avec la symétrie axiale ?", "La symétrie axiale est un pliage le long d’une droite ; la symétrie centrale est un demi-tour autour d’un point."),
           ("Pourquoi le parallélogramme a-t-il un centre de symétrie ?", "Ses diagonales se coupent en leur milieu : ce point est le centre de symétrie.")]
    unit("5e", R, "symetrie-centrale", "E",
         "Définir le demi-tour (symétrie centrale) et construire l’image d’un point ; connaître ses propriétés de conservation ; reconnaître les figures ayant un centre de symétrie",
         "La symétrie centrale", "Symétrie centrale",
         "Fiches de maths 5e sur la symétrie centrale : symétrique d’un point, propriétés, centre de symétrie d’une figure et milieu. 100 exercices corrigés.",
         "O est le milieu de [AA’].", "Demi-tour autour de O.", body, faq, sets, 12)


if __name__ == "__main__":
    main()
