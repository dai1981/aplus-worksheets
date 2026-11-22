# -*- coding: utf-8 -*-
"""
France Maths 5e : Angles et parallélisme (alternes-internes, correspondants)
  python3 tools/gen_fr_maths_5e_angles_et_parallelisme.py
Reconnaître des angles alternes-internes, correspondants, opposés par le sommet ; calculer un angle quand les droites sont parallèles ;
démontrer que deux droites sont parallèles (ou non) avec les angles.
Erreurs : croire que des alternes-internes sont toujours égaux (il faut des droites parallèles), confondre avec supplémentaires.
"""
import random, math
from fr_c4 import *

R = random.Random(60213)
K = Kids(R)
POS = ["rb", "bl", "la", "ar"]   # droite-bas, bas-gauche, gauche-haut, haut-droite


def val(pos, t):
    return t if pos in ("rb", "la") else 180 - t


def fig(marks, t=60, par=True):
    """marks : [(intersection 0/1, pos, texte, couleur)]"""
    y1, y2 = 70, 170
    a = math.radians(t)
    dx = math.cos(a) / math.sin(a)
    x1 = 170
    x2 = x1 + (y2 - y1) * dx
    s = [line(20, y1, 380, y1 if par else y1 - 18, INK, 2.4), line(20, y2, 380, y2, INK, 2.4)]
    s.append(text(372, (y1 if par else y1 - 18) - 8, "(d)", 15, anchor="end") + text(372, y2 - 8, "(d’)", 15, anchor="end"))
    tx0, ty0 = x1 - 60 * dx, y1 - 60
    tx1, ty1 = x2 + 50 * dx, y2 + 50
    s.append(line(tx0, ty0, tx1, ty1, BLUE, 2.4))
    ang = {"rb": (0, t), "bl": (t, 180), "la": (180, 180 + t), "ar": (180 + t, 360)}
    for i, pos, lab, col in marks:
        cx, cy = (x1, y1) if i == 0 else (x2, y2)
        if not par and i == 0:
            pass
        a0, a1 = ang[pos]
        r = 26
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='1.6'/>" % (cx, cy, p0[0], p0[1], r, r, p1[0], p1[1], col, col))
        am = math.radians((a0 + a1) / 2)
        s.append(text(cx + 46 * math.cos(am), cy + 46 * math.sin(am) + 5, lab, 15, col=col))
    return wrap(400, 240, "".join(s), "deux droites coupées par une sécante", lg=True)


def s1():
    k = R.choice(["ai", "co", "op", "sup"])
    if k == "ai":
        p0 = R.choice(["rb", "bl"])
        p1 = {"rb": "la", "bl": "ar"}[p0]
        ans = "alternes-internes"
        m = [(0, p0, "a", RED), (1, p1, "b", GREEN)]
    elif k == "co":
        p0 = R.choice(POS)
        p1 = p0
        ans = "correspondants"
        m = [(0, p0, "a", RED), (1, p1, "b", GREEN)]
    elif k == "op":
        p0 = R.choice(POS)
        p1 = POS[(POS.index(p0) + 2) % 4]
        i = R.randint(0, 1)
        ans = "opposés par le sommet"
        m = [(i, p0, "a", RED), (i, p1, "b", GREEN)]
    else:
        p0 = R.choice(POS)
        p1 = POS[(POS.index(p0) + 1) % 4]
        i = R.randint(0, 1)
        ans = "adjacents et supplémentaires"
        m = [(i, p0, "a", RED), (i, p1, "b", GREEN)]
    svg = fig(m, R.choice([50, 60, 65, 70, 115, 120, 125]))
    return M("<div class='qfig'>%s</div>Comment appelle-t-on les angles a et b ?" % svg, ans, [x for x in ["alternes-internes", "correspondants", "opposés par le sommet", "adjacents et supplémentaires"] if x != ans],
             {"alternes-internes": "Ils sont de part et d’autre de la sécante, entre les deux droites : <b>alternes-internes</b>.",
              "correspondants": "Ils sont du même côté de la sécante, à la même place à chaque intersection : <b>correspondants</b>.",
              "opposés par le sommet": "Même sommet, côtés dans le prolongement l’un de l’autre : <b>opposés par le sommet</b>.",
              "adjacents et supplémentaires": "Même sommet, un côté commun, et ensemble ils forment un angle plat : <b>adjacents et supplémentaires</b>."}[ans])


def s2():
    t = R.choice(range(35, 146, 5))
    if t == 90:
        return None
    p0 = R.choice(POS)
    k = R.choice(["ai", "co", "sup"])
    if k == "ai" and p0 not in ("rb", "bl"):
        p0 = R.choice(["rb", "bl"])
    p1 = {"ai": {"rb": "la", "bl": "ar"}.get(p0, p0), "co": p0, "sup": POS[(POS.index(p0) + 1) % 4]}[k]
    a = val(p0, t)
    b = val(p1, t)
    svg = fig([(0, p0, "%d°" % a, RED), (1, p1, "?", GREEN)], t)
    why = {"ai": "Les droites sont parallèles, donc les angles alternes-internes sont égaux", "co": "Les droites sont parallèles, donc les angles correspondants sont égaux",
           "sup": "L’angle ? est égal à l’angle correspondant à côté du %d° : ensemble ils forment un angle plat" % a}[k]
    return M("<div class='qfig'>%s</div>Les droites (d) et (d’) sont parallèles. Combien mesure l’angle « ? » ?" % svg, "%d°" % b, ["%d°" % (180 - b), "%d°" % (90 - min(a, 180 - a)), "%d°" % (360 - b)],
             "%s : <b>%d°</b>." % (why, b))


def s3():
    t = R.choice(range(40, 141, 5))
    if t == 90:
        return None
    k = R.choice(["ai", "co"])
    p0 = R.choice(["rb", "bl"]) if k == "ai" else R.choice(POS)
    p1 = {"rb": "la", "bl": "ar"}[p0] if k == "ai" else p0
    a = val(p0, t)
    eq = R.random() < 0.5
    b = a if eq else a + R.choice([-3, -2, 2, 3])
    nm = "alternes-internes" if k == "ai" else "correspondants"
    return M("Deux droites (d) et (d’) sont coupées par une sécante. Deux angles %s mesurent %d° et %d°. Les droites (d) et (d’) sont-elles parallèles ?" % (nm, a, b), "oui" if eq else "non",
             ["non" if eq else "oui", "on ne peut pas savoir", "oui, si les angles sont aigus"],
             ("Si deux angles %s sont égaux, alors les droites sont parallèles : <b>oui</b>." if eq else "Si les droites étaient parallèles, ces angles %s seraient égaux. Ils ne le sont pas : <b>non</b>.") % nm)


def s4():
    k = R.choice(["opp", "sup", "triangle", "quad"])
    a = R.choice(range(25, 156, 5))
    if k == "opp":
        return M("Deux droites se coupent. Un angle mesure %d°. Combien mesure l’angle opposé par le sommet ?" % a, "%d°" % a, ["%d°" % (180 - a), "%d°" % (360 - a), "%d°" % abs(90 - a)], "Angles opposés par le sommet : égaux, <b>%d°</b>." % a)
    if k == "sup":
        return M("Deux angles adjacents forment un angle plat. L’un mesure %d°. Combien mesure l’autre ?" % a, "%d°" % (180 - a), ["%d°" % a, "%d°" % (360 - a), "%d°" % abs(90 - a)], "180 − %d = <b>%d°</b>." % (a, 180 - a))
    if k == "triangle":
        b = R.choice(range(20, 160 - a + 1, 5)) if a < 140 else 10
        return M("Dans un triangle, deux angles mesurent %d° et %d°. Combien mesure le troisième ?" % (a, b), "%d°" % (180 - a - b), ["%d°" % (360 - a - b), "%d°" % (a + b), "%d°" % (180 - a - b + 10)],
                 "La somme des angles d’un triangle vaut 180° : <b>%d°</b>." % (180 - a - b)) if 180 - a - b > 0 else None
    b, c = R.randint(60, 120), R.randint(60, 120)
    return M("Dans un quadrilatère, trois angles mesurent %d°, %d° et %d°. Combien mesure le quatrième ?" % (a, b, c), "%d°" % (360 - a - b - c), ["%d°" % (180 - a - b - c + 180), "%d°" % (180 - (a + b + c) % 180), "%d°" % (360 - a - b)],
             "Un quadrilatère se partage en 2 triangles : la somme vaut 360°, donc <b>%d°</b>." % (360 - a - b - c)) if 0 < 360 - a - b - c < 180 else None


def s5():
    t = R.choice(range(35, 146, 5))
    if t == 90:
        return None
    p0 = R.choice(POS)
    p1 = POS[(POS.index(p0) + 2) % 4]
    a = val(p0, t)
    b = val(p1, t)
    svg = fig([(0, p0, "%d°" % a, RED), (1, p1, "?", GREEN)], t)
    return M("<div class='qfig'>%s</div>Les droites (d) et (d’) sont parallèles. Combien mesure l’angle « ? » ?" % svg, "%d°" % b, ["%d°" % (180 - b), "%d°" % (360 - b), "%d°" % abs(90 - b) if b != 45 else "50°"],
             "On combine : l’angle correspondant au %d° est égal à %d°, puis l’angle opposé par le sommet lui est égal : <b>%d°</b>." % (a, a, b))


def main():
    seen = set()
    sets = [("Nommer des paires d’angles", mix(R, seen, [(s1, 20)])), ("Calculer avec des parallèles", mix(R, seen, [(s2, 20)])),
            ("Les droites sont-elles parallèles ?", mix(R, seen, [(s3, 20)])), ("Angles opposés, supplémentaires, somme", mix(R, seen, [(s4, 20)])), ("Raisonner en deux étapes", mix(R, seen, [(s5, 20)]))]
    body = L(["Quand deux droites sont coupées par une sécante, on parle d’angles <b>alternes-internes</b> (de part et d’autre de la sécante, entre les droites) et <b>correspondants</b> (même position aux deux intersections).",
              "Si les deux droites sont <b>parallèles</b>, les angles alternes-internes sont égaux, et les angles correspondants aussi.",
              "Réciproquement, si deux angles alternes-internes (ou correspondants) sont égaux, alors les droites sont parallèles."],
             [("(d) // (d’), angle correspondant de 70°", ["les correspondants sont égaux"], "70°")],
             [["Croire que les alternes-internes sont toujours égaux", "Ils sont égaux seulement si les droites sont parallèles."],
              ["Confondre égaux et supplémentaires", "Deux angles adjacents sur une droite font 180° ; les alternes-internes sont égaux."],
              ["Conclure au parallélisme avec des angles presque égaux", "Il faut qu’ils soient exactement égaux."]])
    faq = [("Comment démontrer que deux droites sont parallèles ?", "On montre que deux angles alternes-internes (ou correspondants) formés avec une sécante sont égaux."),
           ("Comment se souvenir de « alternes-internes » ?", "« Alternes » : de part et d’autre de la sécante ; « internes » : entre les deux droites.")]
    unit("5e", R, "angles-et-parallelisme", "E",
         "Reconnaître les angles usuels ; connaître et utiliser les angles alternes-internes et correspondants pour caractériser le parallélisme de deux droites",
         "Angles et parallélisme", "Angles et parallélisme",
         "Fiches de maths 5e sur les angles et le parallélisme : alternes-internes, correspondants, opposés par le sommet, calculer un angle et démontrer un parallélisme. 100 exercices corrigés.",
         "Droites parallèles ⇔ angles alternes-internes égaux.", "Correspondants : même position.", body, faq, sets, 13)


if __name__ == "__main__":
    main()
