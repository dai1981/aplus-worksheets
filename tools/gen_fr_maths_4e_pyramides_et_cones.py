# -*- coding: utf-8 -*-
"""
France Maths 4e : Pyramides et cônes de révolution (description, volume)
  python3 tools/gen_fr_maths_4e_pyramides_et_cones.py
Erreurs : oublier ÷ 3, prendre le diamètre pour le rayon, confondre hauteur et arête latérale, mal convertir cm³ en L.
"""
import random
import math
from fr_c4 import *

R = random.Random(60316)
K = Kids(R)


def s1():
    V = [("Combien de faces a une pyramide à base carrée ?", "5", ["4", "6", "8"]),
         ("Combien d’arêtes a une pyramide à base triangulaire ?", "6", ["3", "4", "9"]),
         ("Combien de sommets a une pyramide à base hexagonale ?", "7", ["6", "12", "8"]),
         ("Combien de faces latérales a une pyramide à base pentagonale ?", "5", ["6", "4", "10"]),
         ("Quelle est la forme des faces latérales d’une pyramide ?", "des triangles", ["des rectangles", "des carrés", "des disques"]),
         ("La hauteur d’une pyramide est…", "le segment issu du sommet, perpendiculaire à la base", ["une arête latérale", "le côté de la base", "la hauteur d’une face latérale"]),
         ("Un cône de révolution est obtenu en faisant tourner…", "un triangle rectangle autour d’un côté de l’angle droit", ["un rectangle autour d’un côté", "un demi-disque autour de son diamètre", "un triangle isocèle autour de sa base"]),
         ("La base d’un cône de révolution est…", "un disque", ["un triangle", "un carré", "un rectangle"]),
         ("Combien d’arêtes a une pyramide à base carrée ?", "8", ["4", "5", "12"]),
         ("Combien de sommets a une pyramide à base triangulaire ?", "4", ["3", "6", "5"]),
         ("Une pyramide régulière a pour base…", "un polygone régulier", ["un rectangle quelconque", "un disque", "un triangle quelconque"]),
         ("Un tétraèdre est…", "une pyramide à base triangulaire", ["une pyramide à base carrée", "un prisme", "un cône"]),
         ("Le patron d’un cône de révolution est formé…", "d’un disque et d’une portion de disque", ["de deux disques et d’un rectangle", "d’un disque et d’un triangle", "de triangles seulement"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s1b():
    n = R.randint(3, 12)
    NOM = {3: "triangulaire", 4: "carrée", 5: "pentagonale", 6: "hexagonale", 8: "octogonale", 10: "décagonale"}
    if n not in NOM:
        return None
    k = R.choice(["faces", "aretes", "sommets"])
    v = {"faces": n + 1, "aretes": 2 * n, "sommets": n + 1}[k]
    nm = {"faces": "faces", "aretes": "arêtes", "sommets": "sommets"}[k]
    return M("Une pyramide a une base %s (%d côtés). Combien a-t-elle %s ?" % (NOM[n], n, ("d’" if nm[0] in "aeéiou" else "de ") + nm), str(v), [str(n), str(3 * n) if 3 * n != v else str(v + 2), str(v + 1) if v + 1 != 3 * n else str(v - 1)],
             "%s" % {"faces": "1 base + %d faces latérales = <b>%d</b>." % (n, v), "aretes": "%d arêtes pour la base + %d arêtes latérales = <b>%d</b>." % (n, n, v), "sommets": "%d sommets pour la base + 1 sommet principal = <b>%d</b>." % (n, v)}[k])


def s2():
    k = R.choice(["carre", "rect", "tri", "Bh"])
    h = R.choice([3, 6, 9, 12, 15, 4, 5, 10])
    if k == "carre":
        c = R.randint(2, 12)
        v = Fr(c * c * h, 3)
        if v.denominator != 1:
            return None
        return M("Une pyramide a une base carrée de côté %d cm et une hauteur de %d cm. Quel est son volume ?" % (c, h), "%s cm³" % num(v), ["%s cm³" % num(c * c * h), "%s cm³" % num(Fr(c * h, 3)) if Fr(c * h, 3).denominator == 1 else "%s cm³" % num(c * h), "%s cm³" % num(Fr(c * c * h, 2)) if Fr(c * c * h, 2).denominator == 1 else "%s cm³" % num(v + c)],
                     "V = aire de la base × hauteur ÷ 3 = %d × %d × %d ÷ 3 = <b>%s cm³</b>." % (c, c, h, num(v)))
    if k == "rect":
        a, b = R.randint(2, 10), R.randint(2, 10)
        v = Fr(a * b * h, 3)
        if v.denominator != 1 or a == b:
            return None
        return M("Une pyramide a pour base un rectangle de %d cm sur %d cm et une hauteur de %d cm. Quel est son volume ?" % (a, b, h), "%s cm³" % num(v), ["%s cm³" % num(a * b * h), "%s cm³" % num(Fr(2 * (a + b) * h, 3)) if Fr(2 * (a + b) * h, 3).denominator == 1 else "%s cm³" % num(v * 2), "%s cm³" % num(a + b + h)],
                     "V = %d × %d × %d ÷ 3 = <b>%s cm³</b>." % (a, b, h, num(v)))
    if k == "tri":
        b, hb = R.randint(2, 10), R.randint(2, 10)
        B = Fr(b * hb, 2)
        v = B * h / 3
        if v.denominator != 1:
            return None
        return M("Une pyramide a pour base un triangle de base %d cm et de hauteur %d cm. La hauteur de la pyramide est %d cm. Quel est son volume ?" % (b, hb, h), "%s cm³" % num(v), ["%s cm³" % num(b * hb * h / Fr(3)) if (Fr(b * hb * h, 3)).denominator == 1 else "%s cm³" % num(v * 2), "%s cm³" % num(B * h), "%s cm³" % num(Fr(b * hb * h, 2))],
                     "Aire de la base : %d × %d ÷ 2 = %s cm² ; V = %s × %d ÷ 3 = <b>%s cm³</b>." % (b, hb, num(B), num(B), h, num(v)))
    B = R.randint(5, 60)
    v = Fr(B * h, 3)
    if v.denominator != 1:
        return None
    return M("Une pyramide a une base d’aire %d cm² et une hauteur de %d cm. Quel est son volume ?" % (B, h), "%s cm³" % num(v), ["%s cm³" % num(B * h), "%s cm³" % num(Fr(B * h, 2)) if Fr(B * h, 2).denominator == 1 else "%s cm³" % num(v + B), "%s cm³" % num(B + h)],
             "V = %d × %d ÷ 3 = <b>%s cm³</b>." % (B, h, num(v)))


def s3():
    r = R.randint(1, 10)
    h = R.choice([3, 6, 9, 12, 4, 5, 10])
    k = R.choice(["exact", "arr", "arr", "diam"])
    if k == "exact":
        v = Fr(r * r * h, 3)
        if v.denominator != 1:
            return None
        return M("Un cône de révolution a un rayon de %d cm et une hauteur de %d cm. Quel est son volume exact ?" % (r, h), "%sπ cm³" % num(v), ["%sπ cm³" % num(r * r * h), "%sπ cm³" % num(Fr(2 * r * h, 3)) if Fr(2 * r * h, 3).denominator == 1 else "%sπ cm³" % num(v * 2), "%sπ cm³" % num(Fr(r * h, 3)) if Fr(r * h, 3).denominator == 1 else "%sπ cm³" % num(v + 1)],
                     "V = π × r² × h ÷ 3 = π × %d × %d ÷ 3 = <b>%sπ cm³</b>." % (r * r, h, num(v)))
    if k == "arr":
        v = Fr(round(math.pi * r * r * h / 3 * 10), 10)
        return M("Un cône de révolution a un rayon de %d cm et une hauteur de %d cm. Donne son volume arrondi au dixième." % (r, h), "%s cm³" % d(v), ["%s cm³" % d(Fr(round(math.pi * r * r * h * 10), 10)), "%s cm³" % d(Fr(round(math.pi * 2 * r * h / 3 * 10), 10)), "%s cm³" % d(Fr(round(math.pi * r * h / 3 * 10), 10))],
                     "V = π × %d² × %d ÷ 3 ≈ <b>%s cm³</b>." % (r, h, d(v)))
    dm = 2 * r
    v = Fr(round(math.pi * r * r * h / 3 * 10), 10)
    return M("Un cône a un diamètre de %d cm et une hauteur de %d cm. Donne son volume arrondi au dixième." % (dm, h), "%s cm³" % d(v), ["%s cm³" % d(Fr(round(math.pi * dm * dm * h / 3 * 10), 10)), "%s cm³" % d(Fr(round(math.pi * r * r * h * 10), 10)), "%s cm³" % d(Fr(round(math.pi * dm * h / 3 * 10), 10))],
             "Rayon = %d ÷ 2 = %d cm ; V = π × %d² × %d ÷ 3 ≈ <b>%s cm³</b>." % (dm, r, r, h, d(v)))


def s4():
    k = R.choice(["conv", "conv", "compare", "hauteur"])
    if k == "conv":
        v = R.choice([500, 1000, 1500, 2500, 250, 750, 3000, 200])
        return M("Convertis %s cm³ en litres." % num(v), "%s L" % d(Fr(v, 1000)), ["%s L" % d(Fr(v, 100)), "%s L" % num(v * 1000), "%s L" % d(Fr(v, 10))],
                 "1 L = 1 dm³ = 1 000 cm³, donc %s cm³ = <b>%s L</b>." % (num(v), d(Fr(v, 1000))))
    if k == "compare":
        c = R.randint(2, 9)
        return M("Un cube et une pyramide ont la même base carrée de côté %d cm et la même hauteur %d cm. Combien de fois la pyramide est-elle contenue dans le cube ?" % (c, c), "3 fois", ["2 fois", "4 fois", "1 fois (même volume)"],
                 "V(pyramide) = V(cube) ÷ 3 : <b>3 fois</b>.")
    B = R.choice([12, 15, 18, 24, 30, 36, 40])
    h = R.randint(2, 12)
    v = B * h
    return M("Une pyramide de volume %d cm³ a une base d’aire %d cm². Quelle est sa hauteur ?" % (v, B), "%d cm" % (3 * v // B), ["%d cm" % (v // B), "%s cm" % d(Fr(v, 3 * B)) if (Fr(v, 3 * B) * 10).denominator == 1 else "%d cm" % (v // B + 1), "%d cm" % (3 * v - B)],
             "V = B × h ÷ 3, donc h = 3 × V ÷ B = 3 × %d ÷ %d = <b>%d cm</b>." % (v, B, 3 * v // B))


def s5():
    p = K.next()
    k = R.choice(["louvre", "glace", "entonnoir", "tas", "tente"])
    if k == "louvre":
        return M("La pyramide du Louvre a une base carrée d’environ 35 m de côté et une hauteur d’environ 21 m. Quel est son volume approximatif ?", "8 575 m³", ["25 725 m³", "245 m³", "12 862,5 m³"],
                 "35 × 35 × 21 ÷ 3 = <b>8 575 m³</b>.")
    if k == "glace":
        r, h = R.choice([(3, 10), (2, 9), (3, 12), (2, 12)])
        v = Fr(round(math.pi * r * r * h / 3), 1)
        return M("Un cornet de glace a la forme d’un cône de rayon %d cm et de hauteur %d cm. Quel volume de glace contient-il, arrondi au cm³ ?" % (r, h), "%d cm³" % v, ["%d cm³" % round(math.pi * r * r * h), "%d cm³" % round(math.pi * 2 * r * h / 3), "%d cm³" % round(math.pi * r * h / 3)],
                 "π × %d² × %d ÷ 3 ≈ <b>%d cm³</b>." % (r, h, v))
    if k == "entonnoir":
        r, h = R.choice([(6, 10), (5, 12), (9, 10), (10, 15)])
        v = math.pi * r * r * h / 3
        L_ = Fr(round(v / 100), 10)
        return M("Un entonnoir conique a un rayon de %d cm et une hauteur de %d cm. Quelle est sa contenance en litres, arrondie au dixième ?" % (r, h), "%s L" % d(L_), ["%s L" % d(Fr(round(v * 3 / 100), 10)), "%s L" % d(Fr(round(v), 1)), "%s L" % d(Fr(round(v / 10), 10))],
                 "V ≈ %s cm³ = <b>%s L</b> (1 L = 1 000 cm³)." % (num(round(v)), d(L_)))
    if k == "tas":
        r, h = R.choice([(3, 2), (6, 2), (3, 4), (2, 3)])
        v = Fr(round(math.pi * r * r * h / 3 * 10), 10)
        return M("Un tas de sable a la forme d’un cône de %d m de rayon et %d m de haut. Quel est son volume, arrondi au dixième ?" % (r, h), "%s m³" % d(v), ["%s m³" % d(Fr(round(math.pi * r * r * h * 10), 10)), "%s m³" % d(Fr(round(math.pi * r * h / 3 * 10), 10)), "%s m³" % d(Fr(round(math.pi * 4 * r * r * h / 3 * 10), 10))],
                 "π × %d² × %d ÷ 3 ≈ <b>%s m³</b>." % (r, h, d(v)))
    c, h = R.choice([(2, 3), (3, 2), (4, 3), (3, 3)])
    v = Fr(c * c * h, 3)
    return M("La tente %s a la forme d’une pyramide à base carrée de %d m de côté et de %d m de haut. Quel est le volume d’air à l’intérieur ?" % (de_n(p[0]), c, h), "%s m³" % d(v), ["%d m³" % (c * c * h), "%s m³" % d(Fr(c * h, 3)) if Fr(c * h, 3) != v else "%d m³" % (c * h), "%s m³" % d(Fr(c * c * h, 2))],
             "%d × %d × %d ÷ 3 = <b>%s m³</b>." % (c, c, h, d(v)))


def main():
    seen = set()
    sets = [("Décrire une pyramide ou un cône", mix(R, seen, [(s1, 10), (s1b, 10)])), ("Volume d’une pyramide", mix(R, seen, [(s2, 20)])),
            ("Volume d’un cône", mix(R, seen, [(s3, 20)])), ("Unités et calculs inverses", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>pyramide</b> a une base polygonale et des faces latérales triangulaires qui se rejoignent au sommet. Un <b>cône de révolution</b> a une base en forme de disque.",
              "Volume d’une pyramide ou d’un cône : <b>V = aire de la base × hauteur ÷ 3</b>. Pour le cône : V = π × r² × h ÷ 3.",
              "1 L = 1 dm³ = 1 000 cm³."],
             [("Pyramide : base carrée de 6 cm, hauteur 10 cm", ["aire de la base : 36 cm²", "36 × 10 ÷ 3"], "120 cm³")],
             [["Oublier de diviser par 3", "Une pyramide occupe le tiers du prisme de même base et même hauteur."], ["Prendre le diamètre comme rayon", "r = diamètre ÷ 2."],
              ["Utiliser l’arête latérale comme hauteur", "La hauteur est perpendiculaire à la base."]])
    faq = [("Pourquoi diviser par 3 ?", "Trois pyramides identiques peuvent remplir un prisme de même base et de même hauteur : chacune en occupe le tiers."),
           ("Comment trouver la hauteur à partir du volume ?", "h = 3 × V ÷ aire de la base.")]
    unit("4e", R, "pyramides-et-cones", "E",
         "Décrire une pyramide et un cône de révolution ; calculer le volume d’une pyramide et d’un cône (aire de la base × hauteur ÷ 3) ; convertir des unités de volume et de contenance ; résoudre des problèmes",
         "Pyramides et cônes", "Pyramides et cônes",
         "Fiches de maths 4e sur les pyramides et les cônes : vocabulaire, faces, arêtes, sommets, volume d’une pyramide et d’un cône, conversions et problèmes. 100 exercices corrigés.",
         "V = aire de la base × hauteur ÷ 3", "Cône : V = πr²h ÷ 3", body, faq, sets, 16)


if __name__ == "__main__":
    main()
