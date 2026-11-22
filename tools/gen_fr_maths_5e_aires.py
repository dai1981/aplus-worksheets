# -*- coding: utf-8 -*-
"""
France Maths 5e : Aires (triangle, parallélogramme, disque, figures composées) et conversions
  python3 tools/gen_fr_maths_5e_aires.py
Erreurs : prendre le côté oblique au lieu de la hauteur, oublier ÷ 2 pour le triangle, utiliser le diamètre à la place du rayon, 1 m² = 100 cm².
"""
import random
from fr_c4 import *

R = random.Random(60216)
K = Kids(R)
PI = Fr(314, 100)


def para_svg(b, h, s_, side_lab):
    sc = min(200.0 / (b + s_), 120.0 / h)
    B, H, S = b * sc, h * sc, s_ * sc
    ox, oy = 30, 20
    pts = [(ox + S, oy), (ox + S + B, oy), (ox + B, oy + H), (ox, oy + H)]
    sv = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN),
          line(ox + S, oy, ox + S, oy + H, RED, 1.6), text(ox + B / 2, oy + H + 22, "%d cm" % b, 14), text(ox + S + 6, oy + H / 2 + 5, "%d cm" % h, 14, anchor="start", col=RED),
          text(ox + S / 2 - 8, oy + H / 2 - 4, side_lab, 13, anchor="end")]
    return wrap(B + S + 70, H + 50, "".join(sv), "un parallélogramme et une hauteur", lg=True)


def s1():
    b, h = R.randint(4, 14), R.randint(2, 9)
    s_ = R.randint(1, 4)
    side = round(((s_ ** 2 + h ** 2) ** 0.5) * 10) / 10.0
    svg = para_svg(b, h, s_, "%s cm" % d(Fr(int(side * 10), 10)))
    return M("<div class='qfig'>%s</div>Quelle est l’aire de ce parallélogramme ?" % svg, "%d cm²" % (b * h), ["%s cm²" % d(b * Fr(int(side * 10), 10)), "%s cm²" % d(Fr(b * h, 2)), "%d cm²" % (2 * (b + h))],
             "A = base × hauteur = %d × %d = <b>%d cm²</b> (on n’utilise pas le côté oblique)." % (b, h, b * h))


def s2():
    b, h = R.randint(3, 16), R.randint(2, 12)
    k = R.choice(["tri", "tri_inv", "trap"])
    if k == "tri":
        return M("Un triangle a une base de %d cm et une hauteur de %d cm. Quelle est son aire ?" % (b, h), "%s cm²" % d(Fr(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(Fr(b + h, 2))],
                 "A = %d × %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(Fr(b * h, 2))))
    if k == "tri_inv":
        return M("Un triangle rectangle a des côtés de l’angle droit de %d cm et %d cm. Quelle est son aire ?" % (b, h), "%s cm²" % d(Fr(b * h, 2)), ["%d cm²" % (b * h), "%d cm²" % (b + h), "%s cm²" % d(Fr(b * h, 4))],
                 "Un côté de l’angle droit sert de base, l’autre de hauteur : %d × %d ÷ 2 = <b>%s cm²</b>." % (b, h, d(Fr(b * h, 2))))
    c = R.randint(2, b)
    return M("Un trapèze rectangle a des bases de %d cm et %d cm et une hauteur de %d cm. On le découpe en un rectangle et un triangle. Quelle est son aire ?" % (b + c, b, h), "%s cm²" % d(b * h + Fr(c * h, 2)),
             ["%d cm²" % ((b + c) * h), "%d cm²" % (b * h), "%s cm²" % d(b * h + c * h)],
             "Rectangle : %d × %d = %d ; triangle : %d × %d ÷ 2 = %s ; total : <b>%s cm²</b>." % (b, h, b * h, c, h, d(Fr(c * h, 2)), d(b * h + Fr(c * h, 2))))


def s3():
    r = R.randint(1, 10)
    k = R.choice(["r", "d", "demi"])
    if k == "r":
        return M("Quelle est l’aire d’un disque de rayon %d cm ? (π ≈ 3,14)" % r, "%s cm²" % d(PI * r * r), ["%s cm²" % d(2 * PI * r), "%s cm²" % d(PI * 4 * r * r), "%s cm²" % d(PI * r)],
                 "A = π × r² ≈ 3,14 × %d² = <b>%s cm²</b>." % (r, d(PI * r * r)))
    if k == "d":
        return M("Quelle est l’aire d’un disque de diamètre %d cm ? (π ≈ 3,14)" % (2 * r), "%s cm²" % d(PI * r * r), ["%s cm²" % d(PI * 4 * r * r), "%s cm²" % d(2 * PI * r), "%s cm²" % d(PI * 2 * r)],
                 "Le rayon est %d cm : A ≈ 3,14 × %d² = <b>%s cm²</b>." % (r, r, d(PI * r * r)))
    return M("Quelle est l’aire d’un demi-disque de rayon %d cm ? (π ≈ 3,14)" % r, "%s cm²" % d(PI * r * r / 2), ["%s cm²" % d(PI * r * r), "%s cm²" % d(PI * r), "%s cm²" % d(PI * r * r * 2)],
             "La moitié de π × %d² : <b>%s cm²</b>." % (r, d(PI * r * r / 2)))


def s4():
    k = R.choice(["m2cm2", "cm2m2", "dm2", "ha", "km"])
    a = R.randint(2, 50)
    if k == "m2cm2":
        return M("%d m² = … cm²" % a, "%s cm²" % num(a * 10000), ["%s cm²" % num(a * 100), "%s cm²" % num(a * 1000), "%s cm²" % num(a * 100000)], "1 m² = 10 000 cm² : <b>%s cm²</b>." % num(a * 10000))
    if k == "cm2m2":
        a = R.choice([500, 2500, 7500, 12000, 30000, 450])
        return M("%s cm² = … m²" % num(a), "%s m²" % d(Fr(a, 10000)), ["%s m²" % d(Fr(a, 100)), "%s m²" % d(Fr(a, 1000)), "%s m²" % d(Fr(a, 100000))], "On divise par 10 000 : <b>%s m²</b>." % d(Fr(a, 10000)))
    if k == "dm2":
        return M("%d dm² = … cm²" % a, "%s cm²" % num(a * 100), ["%s cm²" % num(a * 10), "%s cm²" % num(a * 1000), "%d cm²" % a], "1 dm² = 10 cm × 10 cm = 100 cm² : <b>%s cm²</b>." % num(a * 100))
    if k == "ha":
        a = R.randint(2, 30)
        return M("%d ha = … m² (1 ha = 1 hm²)" % a, "%s m²" % num(a * 10000), ["%s m²" % num(a * 100), "%s m²" % num(a * 1000), "%s m²" % num(a * 1000000)], "1 ha = 100 m × 100 m = 10 000 m² : <b>%s m²</b>." % num(a * 10000))
    a = R.randint(2, 9)
    return M("%d km² = … m²" % a, "%s m²" % num(a * 1000000), ["%s m²" % num(a * 1000), "%s m²" % num(a * 10000), "%s m²" % num(a * 100000)], "1 km² = 1 000 m × 1 000 m = 1 000 000 m² : <b>%s m²</b>." % num(a * 1000000))


def s5():
    k = R.choice(["piscine", "jardin", "fenetre", "peinture"])
    if k == "piscine":
        L_, l_, r = R.randint(8, 15), R.randint(4, 6), 0
        return M("Une terrasse est formée d’un rectangle de %d m sur %d m et d’un demi-disque de diamètre %d m collé sur la largeur. Quelle est son aire ? (π ≈ 3,14)" % (L_, l_, l_), "%s m²" % d(L_ * l_ + PI * Fr(l_, 2) ** 2 / 2),
                 ["%s m²" % d(L_ * l_ + PI * l_ * l_ / 2), "%s m²" % d(L_ * l_ + PI * Fr(l_, 2) ** 2), "%d m²" % (L_ * l_)],
                 "%d × %d + 3,14 × %s² ÷ 2 = <b>%s m²</b>." % (L_, l_, d(Fr(l_, 2)), d(L_ * l_ + PI * Fr(l_, 2) ** 2 / 2)))
    if k == "jardin":
        a, b, c = R.randint(10, 20), R.randint(6, 12), R.randint(2, 5)
        return M("Un jardin rectangulaire de %d m sur %d m contient un bassin carré de %d m de côté. Quelle est l’aire de la pelouse autour ?" % (a, b, c), "%d m²" % (a * b - c * c), ["%d m²" % (a * b), "%d m²" % (a * b - 4 * c), "%d m²" % (a * b + c * c)],
                 "%d × %d − %d × %d = <b>%d m²</b>." % (a, b, c, c, a * b - c * c))
    if k == "fenetre":
        b, h = R.randint(4, 10), R.randint(3, 8)
        return M("Un panneau triangulaire a une base de %d dm et une hauteur de %d dm. Combien de cm² de peinture faut-il couvrir ?" % (b, h), "%s cm²" % num(b * h * 50), ["%s cm²" % num(b * h * 100), "%s cm²" % d(Fr(b * h, 2)), "%s cm²" % num(b * h * 5)],
                 "Aire : %d × %d ÷ 2 = %s dm² = <b>%s cm²</b>." % (b, h, d(Fr(b * h, 2)), num(b * h * 50)))
    a, b = R.randint(3, 8), R.randint(2, 5)
    l = R.choice([5, 10])
    return M("Un pot de peinture couvre %d m². Combien de pots faut-il pour peindre un mur de %d m sur %d m ?" % (l, a, b), str(-(-a * b // l)), [str(a * b // l) if a * b % l else str(a * b // l + 1), str(a * b), str(-(-a * b // l) + 1)],
             "Aire : %d m² ; %d ÷ %d = %s, on arrondit au-dessus : <b>%d pots</b>." % (a * b, a * b, l, d(Fr(a * b, l)), -(-a * b // l)))


def main():
    seen = set()
    sets = [("Aire du parallélogramme", mix(R, seen, [(s1, 20)])), ("Triangle et trapèze", mix(R, seen, [(s2, 20)])),
            ("Aire du disque", mix(R, seen, [(s3, 20)])), ("Unités d’aire", mix(R, seen, [(s4, 20)])), ("Figures composées et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Parallélogramme : A = base × hauteur. Triangle : A = base × hauteur ÷ 2. La hauteur est perpendiculaire à la base.",
              "Disque : A = π × r² (π ≈ 3,14).",
              "Pour une figure composée, on la découpe en figures simples, puis on ajoute ou on retranche les aires. 1 m² = 10 000 cm²."],
             [("Disque de diamètre 10 cm", ["r = 5 cm", "3,14 × 5²"], "78,5 cm²")],
             [["Prendre le côté oblique comme hauteur", "La hauteur est perpendiculaire à la base."], ["Oublier ÷ 2 pour le triangle", "Un triangle est la moitié d’un parallélogramme."],
              ["Utiliser le diamètre à la place du rayon", "r = diamètre ÷ 2."]])
    faq = [("Pourquoi l’aire du parallélogramme est-elle base × hauteur ?", "On découpe un triangle d’un côté et on le recolle de l’autre : on obtient un rectangle de même base et même hauteur."),
           ("Que vaut 1 hectare ?", "1 ha = 10 000 m² (un carré de 100 m de côté).")]
    unit("5e", R, "aires", "E",
         "Calculer l’aire d’un triangle, d’un parallélogramme, d’un disque et de figures complexes ; effectuer des conversions d’unités d’aire",
         "Aires : triangle, parallélogramme, disque", "Aires",
         "Fiches de maths 5e sur les aires : parallélogramme, triangle, trapèze, disque, unités d’aire et figures composées. 100 exercices corrigés.",
         "Parallélogramme : base × hauteur", "Disque : π × r²", body, faq, sets, 16)


if __name__ == "__main__":
    main()
