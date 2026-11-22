# -*- coding: utf-8 -*-
"""
France Maths 6e : Périmètres et aires
  python3 tools/gen_fr_maths_6e_perimetres_et_aires.py
Périmètre d’un polygone, aire du rectangle et du carré, aire du triangle, périmètre et aire du disque (π ≈ 3,14), unités d’aire, figures composées.
Erreurs : confondre périmètre et aire, oublier de diviser par 2 pour le triangle, prendre le diamètre pour le rayon, 1 m² = 100 cm².
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_longueurs_et_perimetres as LP

R = random.Random(60117)
K = Kids(R)
LP.R = R
PI = Fr(314, 100)


def s1():
    k = R.choice(["poly", "rect", "carre", "cote"])
    LP.U_[0] = R.choice(["cm", "m"])
    u = LP.U_[0]
    if k == "poly":
        n = R.choice([3, 4, 5, 6])
        sides = [R.randint(3, 15) for _ in range(n)]
        P = sum(sides)
        return M("<div class='qfig'>%s</div>Quel est le périmètre de ce polygone ?" % LP.poly_svg("poly", sides), "%d %s" % (P, u), ["%d %s" % (P - sides[0], u), "%d %s" % (P + sides[1], u), "%d %s²" % (P, u)],
                 "On additionne les longueurs de tous les côtés : %s = <b>%d %s</b>." % (" + ".join(map(str, sides)), P, u))
    if k == "rect":
        a, b = R.randint(5, 20), R.randint(2, 12)
        if a <= b:
            return None
        return M("Quel est le périmètre d’un rectangle de %d %s sur %d %s ?" % (a, u, b, u), "%d %s" % (2 * (a + b), u), ["%d %s" % (a + b, u), "%d %s" % (a * b, u), "%d %s" % (2 * a + b, u)],
                 "P = 2 × (L + l) = 2 × (%d + %d) = <b>%d %s</b>." % (a, b, 2 * (a + b), u))
    if k == "carre":
        c = R.randint(3, 25)
        return M("Quel est le périmètre d’un carré de côté %d %s ?" % (c, u), "%d %s" % (4 * c, u), ["%d %s" % (2 * c, u), "%d %s" % (c * c, u) if c != 4 else "%d %s" % (3 * c, u), "%d %s" % (4 * c + 4, u)],
                 "P = 4 × c = 4 × %d = <b>%d %s</b>." % (c, 4 * c, u))
    P = 2 * R.randint(10, 40)
    a = R.randint(3, P // 2 - 2)
    return M("Un rectangle a un périmètre de %d %s et une longueur de %d %s. Quelle est sa largeur ?" % (P, u, P // 2 - a, u), "%d %s" % (a, u), ["%d %s" % (P - (P // 2 - a), u), "%d %s" % (P // 2, u), "%d %s" % (P - 2 * (P // 2 - a), u)],
             "La moitié du périmètre est L + l = %d. Donc l = %d − %d = <b>%d %s</b>." % (P // 2, P // 2, P // 2 - a, a, u))


def tri_svg(b, h, x):
    sc = min(220.0 / max(b, x if x > b else b), 150.0 / h)
    B = b * sc
    H = h * sc
    X = x * sc
    ox, oy = 30, 20
    pts = [(ox, oy + H), (ox + B, oy + H), (ox + X, oy)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN),
         line(ox + X, oy, ox + X, oy + H, RED, 1.8),
         text(ox + B / 2, oy + H + 22, "%s cm" % d(b), 14), text(ox + X + 8, oy + H / 2, "%s cm" % d(h), 14, anchor="start", col=RED)]
    if 0 <= X <= B:
        s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='1.4'/>" % (ox + X, oy + H - 10, ox + X + 10, oy + H - 10, ox + X + 10, oy + H, RED))
    return wrap(max(B, X) + 110, H + 50, "".join(s), "un triangle avec une hauteur", lg=True)


def s2():
    a, b = R.randint(3, 25), R.randint(2, 15)
    u = R.choice(["cm", "m"])
    k = R.choice(["rect", "carre", "inv"])
    if k == "rect":
        return M("Quelle est l’aire d’un rectangle de %d %s sur %d %s ?" % (a, u, b, u), "%d %s²" % (a * b, u), ["%d %s²" % (2 * (a + b), u), "%d %s²" % (a + b, u), "%d %s" % (a * b, u)],
                 "A = L × l = %d × %d = <b>%d %s²</b>." % (a, b, a * b, u))
    if k == "carre":
        return M("Quelle est l’aire d’un carré de côté %d %s ?" % (a, u), "%d %s²" % (a * a, u), ["%d %s²" % (4 * a, u) if a != 4 else "%d %s²" % (2 * a, u), "%d %s²" % (2 * a, u) if a != 2 else "%d %s²" % (a + 2, u), "%d %s" % (a * a, u)],
                 "A = c × c = %d × %d = <b>%d %s²</b>." % (a, a, a * a, u))
    return M("Un rectangle a une aire de %d %s² et une longueur de %d %s. Quelle est sa largeur ?" % (a * b, u, a, u), "%d %s" % (b, u), ["%d %s" % (a * b - a, u), "%d %s" % (a * b // 2, u) if a * b % 2 == 0 else "%d %s" % (b + 1, u), "%d %s" % (a, u) if a != b else "%d %s" % (b + 2, u)],
             "l = A ÷ L = %d ÷ %d = <b>%d %s</b>." % (a * b, a, b, u))


def s3():
    b, h = R.randint(3, 14), R.randint(2, 10)
    x = R.choice([R.randint(1, b - 1), R.randint(1, b - 1), b + R.randint(1, 3)])
    A = Fr(b * h, 2)
    svg = tri_svg(b, h, x)
    return M("<div class='qfig'>%s</div>Quelle est l’aire de ce triangle ? (la hauteur est en rouge)" % svg, "%s cm²" % d(A), ["%d cm²" % (b * h), "%s cm²" % d(b + h), "%s cm²" % d(Fr(b * h, 4)) if (b * h) % 4 == 0 else "%s cm²" % d(A + 1)],
             "A = base × hauteur ÷ 2 = %d × %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(A)))


def s4():
    r = R.randint(1, 12)
    k = R.choice(["perim", "aire", "diam"])
    if k == "perim":
        P = 2 * PI * r
        return M("Quel est le périmètre d’un cercle de rayon %d cm ? (prends π ≈ 3,14)" % r, "%s cm" % d(P), ["%s cm" % d(PI * r), "%s cm" % d(PI * r * r), "%s cm" % d(4 * PI * r)],
                 "P = 2 × π × r ≈ 2 × 3,14 × %d = <b>%s cm</b>." % (r, d(P)))
    if k == "diam":
        D = 2 * r
        return M("Quel est le périmètre d’un cercle de diamètre %d cm ? (prends π ≈ 3,14)" % D, "%s cm" % d(PI * D), ["%s cm" % d(2 * PI * D), "%s cm" % d(PI * D * D / 4), "%s cm" % d(PI * r)],
                 "P = π × d ≈ 3,14 × %d = <b>%s cm</b>." % (D, d(PI * D)))
    A = PI * r * r
    return M("Quelle est l’aire d’un disque de rayon %d cm ? (prends π ≈ 3,14)" % r, "%s cm²" % d(A), ["%s cm²" % d(2 * PI * r), "%s cm²" % d(PI * 4 * r * r), "%s cm²" % d(PI * r * 2) if r != 2 else "%s cm²" % d(PI * r)],
             "A = π × r × r ≈ 3,14 × %d × %d = <b>%s cm²</b>." % (r, r, d(A)))


def s5():
    k = R.choice(["conv", "conv2", "compo", "carrelage", "jardin"])
    if k == "conv":
        a = R.randint(2, 9)
        return M("%d m² = … cm²" % a, "%s cm²" % num(a * 10000), ["%s cm²" % num(a * 100), "%s cm²" % num(a * 1000), "%s cm²" % num(a * 10)],
                 "1 m² = 100 cm × 100 cm = 10 000 cm², donc <b>%s cm²</b>." % num(a * 10000))
    if k == "conv2":
        a = R.randint(2, 9)
        return M("%d cm² = … mm²" % a, "%d mm²" % (a * 100), ["%d mm²" % (a * 10), "%s mm²" % num(a * 1000), "%d mm²" % a],
                 "1 cm² = 10 mm × 10 mm = 100 mm², donc <b>%d mm²</b>." % (a * 100))
    if k == "compo":
        a, b, c, e = R.randint(6, 12), R.randint(4, 8), R.randint(2, 5), R.randint(2, 4)
        if c >= a or e >= b:
            return None
        return M("Une figure en L est un rectangle de %d m sur %d m auquel on a retiré, dans un coin, un carré de %d m sur %d m. Quelle est son aire ?" % (a, b, c, c), "%d m²" % (a * b - c * c),
                 ["%d m²" % (a * b), "%d m²" % (a * b + c * c), "%d m²" % (2 * (a + b))], "%d × %d − %d × %d = <b>%d m²</b>." % (a, b, c, c, a * b - c * c))
    if k == "carrelage":
        a, b = R.randint(3, 8), R.randint(2, 6)
        return M("Une pièce rectangulaire mesure %d m sur %d m. Un carreau couvre 1 m². Combien de carreaux faut-il ?" % (a, b), str(a * b), [str(2 * (a + b)), str(a + b), str(a * b + a)],
                 "Aire = %d × %d = %d m², donc <b>%d carreaux</b>." % (a, b, a * b, a * b))
    a, b = R.randint(8, 25), R.randint(5, 15)
    return M("Un jardin rectangulaire mesure %d m sur %d m. Quelle longueur de grillage faut-il pour en faire le tour ?" % (a, b), "%d m" % (2 * (a + b)), ["%d m²" % (a * b), "%d m" % (a + b), "%d m" % (a * b)],
             "C’est un périmètre : 2 × (%d + %d) = <b>%d m</b>." % (a, b, 2 * (a + b)))


def main():
    seen = set()
    sets = [("Périmètres", mix(R, seen, [(s1, 20)])), ("Aire du rectangle et du carré", mix(R, seen, [(s2, 20)])),
            ("Aire du triangle", mix(R, seen, [(s3, 20)])), ("Le cercle et le disque", mix(R, seen, [(s4, 20)])), ("Unités et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>périmètre</b> est la longueur du tour d’une figure (en cm, m…). L’<b>aire</b> est la mesure de sa surface (en cm², m²…).",
              "Rectangle : P = 2 × (L + l), A = L × l. Triangle : A = base × hauteur ÷ 2.",
              "Cercle : P = 2 × π × r ; disque : A = π × r × r, avec π ≈ 3,14."],
             [("Disque de rayon 5 cm", ["3,14 × 5 × 5"], "78,5 cm²")],
             [["Confondre périmètre et aire", "Périmètre : on fait le tour (cm). Aire : on couvre la surface (cm²)."],
              ["Oublier de diviser par 2 pour le triangle", "Un triangle est la moitié d’un rectangle de même base et même hauteur."],
              ["Croire que 1 m² = 100 cm²", "1 m² = 100 cm × 100 cm = 10 000 cm²."]])
    faq = [("Pourquoi π ?", "Dans tout cercle, le périmètre est environ 3,14 fois le diamètre : ce nombre s’appelle π."),
           ("Qu’est-ce qu’une hauteur d’un triangle ?", "Le segment qui part d’un sommet et arrive perpendiculairement sur le côté opposé (ou son prolongement).")]
    unit("6e", R, "perimetres-et-aires", "G",
         "Calculer le périmètre d’un polygone et d’un cercle ; calculer l’aire d’un rectangle, d’un carré, d’un triangle et d’un disque ; utiliser les unités d’aire ; résoudre des problèmes",
         "Périmètres et aires", "Périmètres et aires",
         "Fiches de maths 6e sur les périmètres et les aires : polygones, rectangle, carré, triangle, cercle et disque, unités d’aire et problèmes. 100 exercices corrigés.",
         "Aire du triangle = base × hauteur ÷ 2", "Disque : A = π × r × r", body, faq, sets, 17)


if __name__ == "__main__":
    main()
