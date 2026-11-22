# -*- coding: utf-8 -*-
"""
France Maths 6e : Triangles et quadrilatères particuliers
  python3 tools/gen_fr_maths_6e_triangles_et_quadrilateres.py
Triangles (isocèle, équilatéral, rectangle, isocèle rectangle) par les côtés ou les angles ; quadrilatères (carré, rectangle, losange,
parallélogramme, trapèze, trapèze rectangle) par leurs propriétés ; reconnaître une figure ; problèmes.
Erreurs : croire qu’un carré n’est pas un rectangle, confondre losange et parallélogramme, oublier qu’un triangle équilatéral est isocèle.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FP

R = random.Random(60116)
K = Kids(R)
FP.R = R


def s1():
    A, B, C = R.sample("ABCDEFGHIJKLMNPRST", 3)
    k = R.choice(["equi", "iso", "quel", "rect", "isorect"])
    if k == "equi":
        a = Fr(R.randint(20, 90), 10)
        sides, ans = (a, a, a), "équilatéral"
    elif k == "iso":
        a = Fr(R.randint(30, 90), 10)
        b = a + Fr(R.choice([-15, -10, 10, 20]), 10)
        sides, ans = (a, a, b), "isocèle"
    elif k == "quel":
        a, b = Fr(R.randint(30, 60), 10), Fr(R.randint(30, 60), 10)
        c = a + b - Fr(R.randint(5, 15), 10)
        if len({a, b, c}) < 3 or (a * a + b * b == c * c):
            return None
        sides, ans = (a, b, c), "quelconque"
    elif k == "rect":
        m = R.choice([1, Fr(3, 2), 2])
        sides, ans = (3 * m, 4 * m, 5 * m), "rectangle"
    else:
        return M("Le triangle %s%s%s a deux côtés égaux qui forment un angle droit. Quelle est sa nature ?" % (A, B, C), "isocèle rectangle", ["équilatéral", "isocèle, mais pas rectangle", "quelconque"],
                 "Deux côtés égaux : isocèle ; un angle droit : rectangle. C’est un triangle <b>isocèle rectangle</b>.")
    pr = R.sample(list(sides), 3)
    extra = " Il a un angle droit en %s." % C if ans == "rectangle" else ""
    return M("Dans le triangle %s%s%s : %s%s = %s cm, %s%s = %s cm, %s%s = %s cm.%s Quelle est sa nature ?" % (A, B, C, A, B, d(pr[0]), B, C, d(pr[1]), A, C, d(pr[2]), extra), ans,
             [x for x in ["équilatéral", "isocèle", "rectangle", "quelconque"] if x != ans],
             {"équilatéral": "Les trois côtés ont la même longueur : <b>équilatéral</b>.", "isocèle": "Deux côtés ont la même longueur : <b>isocèle</b>.",
              "quelconque": "Les trois côtés sont différents et il n’y a pas d’angle droit : <b>quelconque</b>.", "rectangle": "Il a un angle droit : <b>rectangle</b>."}[ans])


def s2():
    k = R.choice(["rect", "iso", "equi", "quel"])
    if k == "rect":
        a = R.randint(15, 75)
        ang, ans = (90, a, 90 - a), "rectangle"
    elif k == "iso":
        t = R.choice(range(20, 161, 10))
        if t == 60 or t == 90:
            return None
        b = Fr(180 - t, 2)
        ang, ans = (t, b, b), "isocèle"
    elif k == "equi":
        ang, ans = (60, 60, 60), "équilatéral"
    else:
        a, b = R.randint(30, 80), R.randint(30, 80)
        c = 180 - a - b
        if len({a, b, c}) < 3 or 90 in (a, b, c) or c <= 0:
            return None
        ang, ans = (a, b, c), "quelconque"
    pr = R.sample(list(ang), 3)
    return M("Un triangle a des angles de %s°, %s° et %s°. Quelle est sa nature ?" % tuple(d(x) for x in pr), ans, [x for x in ["équilatéral", "isocèle", "rectangle", "quelconque"] if x != ans],
             {"rectangle": "Un angle mesure 90° : <b>rectangle</b>.", "isocèle": "Deux angles égaux : le triangle est <b>isocèle</b>.", "équilatéral": "Trois angles de 60° : <b>équilatéral</b>.",
              "quelconque": "Trois angles différents, aucun droit : <b>quelconque</b>."}[ans])


QD = [("Je suis un quadrilatère qui a 4 angles droits et 4 côtés de même longueur. Qui suis-je ?", "un carré", ["un losange", "un rectangle", "un trapèze"]),
      ("Je suis un quadrilatère qui a 4 angles droits, mais pas 4 côtés égaux. Qui suis-je ?", "un rectangle", ["un carré", "un losange", "un parallélogramme quelconque"]),
      ("Je suis un quadrilatère qui a 4 côtés de même longueur, mais pas d’angle droit. Qui suis-je ?", "un losange", ["un carré", "un rectangle", "un trapèze"]),
      ("Je suis un quadrilatère dont les côtés opposés sont parallèles deux à deux. Qui suis-je ?", "un parallélogramme", ["un trapèze quelconque", "un cerf-volant", "un triangle"]),
      ("Je suis un quadrilatère qui a seulement deux côtés parallèles. Qui suis-je ?", "un trapèze", ["un parallélogramme", "un rectangle", "un losange"]),
      ("Je suis un trapèze qui a un angle droit. Qui suis-je ?", "un trapèze rectangle", ["un rectangle", "un carré", "un losange"]),
      ("Un carré est-il un rectangle ?", "oui, car il a 4 angles droits", ["non, jamais", "seulement s’il est grand", "non, car ses côtés sont égaux"]),
      ("Un carré est-il un losange ?", "oui, car il a 4 côtés égaux", ["non, jamais", "seulement s’il est tourné", "non, car il a des angles droits"]),
      ("Un losange est-il toujours un carré ?", "non, il faut en plus un angle droit", ["oui, toujours", "oui, s’il est tourné", "non, jamais"]),
      ("Un rectangle est-il un parallélogramme ?", "oui, ses côtés opposés sont parallèles", ["non, jamais", "seulement si c’est un carré", "non, il a des angles droits"]),
      ("Combien d’angles droits a un trapèze rectangle ?", "2", ["1", "4", "0"]),
      ("Dans un parallélogramme, les côtés opposés…", "sont parallèles et de même longueur", ["sont perpendiculaires", "sont de longueurs différentes", "se coupent"]),
      ("Les diagonales d’un rectangle…", "ont la même longueur", ["sont toujours perpendiculaires", "ne se coupent pas", "ont des longueurs différentes"]),
      ("Les diagonales d’un losange…", "sont perpendiculaires", ["ont toujours la même longueur", "sont parallèles", "ne se coupent pas"])]


def s3():
    if R.random() < 0.5:
        q, a, w = R.choice(QD)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    A, B, C, D_ = R.sample("ABCDEFGHIJKLMNPRST", 4)
    fig_ = R.choice(["losange", "carré", "rectangle", "parallélogramme"])
    v = Fr(R.randint(20, 90), 10)
    if fig_ in ("losange", "carré"):
        return M("%s%s%s%s est un %s et %s%s = %s cm. Combien mesure %s%s ?" % (A, B, C, D_, fig_, A, B, d(v), B, C), "%s cm" % d(v), ["%s cm" % d(2 * v), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                 "Les 4 côtés d’un %s ont la même longueur : <b>%s cm</b>." % (fig_, d(v)))
    if R.random() < 0.5:
        return M("%s%s%s%s est un %s et %s%s = %s cm. Combien mesure %s%s ?" % (A, B, C, D_, fig_, A, B, d(v), C, D_), "%s cm" % d(v), ["%s cm" % d(2 * v), "%s cm" % d(v / 2), "on ne peut pas savoir"],
                     "Dans un %s, les côtés opposés ont la même longueur : %s%s = %s%s = <b>%s cm</b>." % (fig_, C, D_, A, B, d(v)))
    return M("%s%s%s%s est un %s et %s%s = %s cm. Peut-on connaître %s%s ?" % (A, B, C, D_, fig_, A, B, d(v), B, C), "non, il manque une information", ["oui, %s cm" % d(v), "oui, %s cm" % d(2 * v), "oui, %s cm" % d(v / 2)],
             "[%s%s] est un côté consécutif à [%s%s] : dans un %s, il n’a pas forcément la même longueur. <b>On ne peut pas le savoir</b>." % (B, C, A, B, fig_))


def poly(pts, label):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = min(xs) - 14, min(ys) - 14
    pts = [(x - mx, y - my) for x, y in pts]
    return wrap(max(xs) - min(xs) + 28, max(ys) - min(ys) + 28, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN), label, lg=True)


def s4():
    k = R.choice(["carré", "rectangle", "losange", "parallélogramme", "trapèze", "trapèze rectangle"])
    if k in ("carré", "rectangle", "losange"):
        pic = FP.shape(k)
    elif k == "parallélogramme":
        w, h, t = R.randint(110, 160), R.randint(60, 90), R.randint(30, 55)
        pic = poly([(t, 0), (t + w, 0), (w, h), (0, h)], "une figure")
    elif k == "trapèze":
        w, h, t1, t2 = R.randint(140, 190), R.randint(60, 90), R.randint(20, 40), R.randint(30, 50)
        pic = poly([(t1, 0), (w - t2, 0), (w, h), (0, h)], "une figure")
    else:
        w, h, t = R.randint(130, 180), R.randint(60, 95), R.randint(40, 70)
        pic = poly([(0, 0), (w - t, 0), (w, h), (0, h)], "une figure")
    ans = ("un " if k != "losange" else "un ") + k
    w = [("un " + x) for x in ["carré", "rectangle", "losange", "parallélogramme", "trapèze", "trapèze rectangle"] if x != k]
    R.shuffle(w)
    return M("<div class='qfig'>%s</div>Quel est le nom le plus précis de ce quadrilatère ?" % pic, ans, w[:3], "On regarde les côtés parallèles, les longueurs et les angles droits : c’est <b>%s</b>." % ans)


def s5():
    k = R.choice(["iso", "equi", "losange", "rect", "trap"])
    if k == "iso":
        a, b = R.randint(4, 12), R.randint(3, 10)
        if a == b:
            return None
        return M("Un triangle isocèle a deux côtés de %d cm et un troisième côté de %d cm. Quel est son périmètre ?" % (a, b), "%d cm" % (2 * a + b), ["%d cm" % (a + b), "%d cm" % (a + 2 * b), "%d cm" % (3 * a)],
                 "%d + %d + %d = <b>%d cm</b>." % (a, a, b, 2 * a + b))
    if k == "equi":
        p = 3 * R.randint(3, 20)
        return M("Un triangle équilatéral a un périmètre de %d cm. Combien mesure un côté ?" % p, "%d cm" % (p // 3), ["%d cm" % (p // 2) if p % 2 == 0 else "%d cm" % (p - 3), "%d cm" % p, "%d cm" % (p // 4) if p % 4 == 0 else "%d cm" % (p // 3 + 1)],
                 "Les 3 côtés sont égaux : %d ÷ 3 = <b>%d cm</b>." % (p, p // 3))
    if k == "losange":
        c = R.randint(3, 15)
        return M("Un losange a un côté de %d cm. Quel est son périmètre ?" % c, "%d cm" % (4 * c), ["%d cm" % (2 * c), "%d cm" % (c * c), "%d cm" % (3 * c)],
                 "Un losange a 4 côtés égaux : 4 × %d = <b>%d cm</b>." % (c, 4 * c))
    if k == "rect":
        a, b = R.randint(4, 15), R.randint(2, 10)
        if a == b:
            return None
        return M("Un rectangle mesure %d cm sur %d cm. Combien mesure chacune de ses diagonales si l’une mesure %s cm ?" % (a, b, d(Fr(round((a * a + b * b) ** 0.5 * 10), 10))),
                 "%s cm" % d(Fr(round((a * a + b * b) ** 0.5 * 10), 10)), ["%d cm" % (a + b), "%s cm" % d(Fr(round((a * a + b * b) ** 0.5 * 10), 20)), "%d cm" % a],
                 "Les diagonales d’un rectangle ont la même longueur : <b>%s cm</b>." % d(Fr(round((a * a + b * b) ** 0.5 * 10), 10)))
    a = R.randint(80, 140)
    return M("Dans un parallélogramme, un angle mesure %d°. Combien mesure l’angle opposé ?" % a, "%d°" % a, ["%d°" % (180 - a), "%d°" % (360 - a), "%d°" % (90 - a % 90)],
             "Dans un parallélogramme, les angles opposés ont la même mesure : <b>%d°</b>." % a)


def main():
    seen = set()
    sets = [("Triangles : les côtés", mix(R, seen, [(s1, 20)])), ("Triangles : les angles", mix(R, seen, [(s2, 20)])),
            ("Quadrilatères : propriétés", mix(R, seen, [(s3, 20)])), ("Reconnaître un quadrilatère", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Triangle <b>isocèle</b> : deux côtés égaux ; <b>équilatéral</b> : trois côtés égaux ; <b>rectangle</b> : un angle droit.",
              "Parallélogramme : côtés opposés parallèles. Rectangle : 4 angles droits. Losange : 4 côtés égaux. Carré : les deux à la fois.",
              "Trapèze : deux côtés parallèles (les bases)."],
             [("Un quadrilatère a 4 côtés égaux et un angle droit", ["losange + angle droit"], "un carré")],
             [["Croire qu’un carré n’est pas un rectangle", "Le carré a 4 angles droits : c’est un rectangle particulier."],
              ["Confondre losange et parallélogramme", "Le losange a en plus 4 côtés égaux."],
              ["Oublier qu’un triangle équilatéral est aussi isocèle", "Il a même trois côtés égaux."]])
    faq = [("Quelle est la différence entre un losange et un carré ?", "Les deux ont 4 côtés égaux ; le carré a en plus 4 angles droits."),
           ("Comment reconnaître un trapèze ?", "Il a au moins deux côtés parallèles.")]
    unit("6e", R, "triangles-et-quadrilateres", "E",
         "Reconnaître, nommer et décrire les triangles particuliers (isocèle, équilatéral, rectangle) et les quadrilatères particuliers (carré, rectangle, losange, parallélogramme, trapèze, trapèze rectangle) à partir de leurs propriétés",
         "Triangles et quadrilatères particuliers", "Triangles et quadrilatères",
         "Fiches de maths 6e sur les triangles et quadrilatères : triangles isocèles, équilatéraux, rectangles, carré, rectangle, losange, parallélogramme, trapèze et problèmes. 100 exercices corrigés.",
         "Un carré est un rectangle et un losange.", "Isocèle : 2 côtés égaux.", body, faq, sets, 16)


if __name__ == "__main__":
    main()
