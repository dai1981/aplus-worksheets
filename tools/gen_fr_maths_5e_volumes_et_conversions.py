# -*- coding: utf-8 -*-
"""
France Maths 5e : Volumes (pavé droit, prisme droit, cylindre) et conversions
  python3 tools/gen_fr_maths_5e_volumes_et_conversions.py
Erreurs : V = base + hauteur, oublier de calculer l’aire de la base, prendre le diamètre comme rayon, 1 dm³ = 10 cm³, 1 L = 100 cm³.
"""
import random
from fr_c4 import *

R = random.Random(60217)
K = Kids(R)
PI = Fr(314, 100)


def s1():
    a, b, c = R.randint(2, 12), R.randint(2, 10), R.randint(2, 15)
    k = R.choice(["pave", "cube", "inv"])
    if k == "pave":
        return M("Quel est le volume d’un pavé droit de %d cm × %d cm × %d cm ?" % (a, b, c), "%s cm³" % num(a * b * c), ["%d cm³" % (a + b + c), "%s cm³" % num(2 * (a * b + b * c + a * c)), "%d cm²" % (a * b * c)],
                 "V = L × l × h = <b>%s cm³</b>." % num(a * b * c))
    if k == "cube":
        return M("Quel est le volume d’un cube d’arête %d cm ?" % a, "%s cm³" % num(a ** 3), ["%d cm³" % (3 * a), "%d cm³" % (a * a), "%s cm³" % num(6 * a * a)], "V = %d³ = <b>%s cm³</b>." % (a, num(a ** 3)))
    return M("Un pavé droit a un volume de %s cm³ et une base de %d cm × %d cm. Quelle est sa hauteur ?" % (num(a * b * c), a, b), "%d cm" % c, ["%s cm" % num(a * b * c - a * b), "%d cm" % (c + 1), "%s cm" % num(a * b * c // a)],
             "h = V ÷ (aire de la base) = %s ÷ %d = <b>%d cm</b>." % (num(a * b * c), a * b, c))


def s2():
    b, h, H = R.randint(2, 10), R.randint(2, 8), R.randint(3, 15)
    k = R.choice(["tri", "base", "rect"])
    if k == "tri":
        B = Fr(b * h, 2)
        return M("Un prisme droit a pour base un triangle de base %d cm et de hauteur %d cm. La hauteur du prisme est %d cm. Quel est son volume ?" % (b, h, H), "%s cm³" % d(B * H),
                 ["%s cm³" % d(b * h * H), "%d cm³" % (b + h + H), "%s cm³" % d(B + H)], "Aire de la base : %d × %d ÷ 2 = %s cm² ; V = %s × %d = <b>%s cm³</b>." % (b, h, d(B), d(B), H, d(B * H)))
    if k == "base":
        B = R.randint(5, 60)
        return M("Un prisme droit a une base d’aire %d cm² et une hauteur de %d cm. Quel est son volume ?" % (B, H), "%s cm³" % num(B * H), ["%d cm³" % (B + H), "%s cm³" % d(Fr(B * H, 2)), "%s cm³" % num(B * H * 2)],
                 "V = aire de la base × hauteur = %d × %d = <b>%s cm³</b>." % (B, H, num(B * H)))
    V = b * h * H
    return M("Un prisme droit a un volume de %s cm³ et une hauteur de %d cm. Quelle est l’aire de sa base ?" % (num(V), H), "%d cm²" % (b * h), ["%s cm²" % num(V - H), "%d cm²" % (b * h * 2), "%d cm²" % (b + h)],
             "Aire de la base = V ÷ h = %s ÷ %d = <b>%d cm²</b>." % (num(V), H, b * h))


def s3():
    r, h = R.randint(1, 10), R.randint(2, 20)
    k = R.choice(["r", "d"])
    V = PI * r * r * h
    if k == "r":
        return M("Quel est le volume d’un cylindre de rayon %d cm et de hauteur %d cm ? (π ≈ 3,14)" % (r, h), "%s cm³" % d(V), ["%s cm³" % d(2 * PI * r * h), "%s cm³" % d(PI * r * h), "%s cm³" % d(PI * 4 * r * r * h)],
                 "V = π × r² × h ≈ 3,14 × %d² × %d = <b>%s cm³</b>." % (r, h, d(V)))
    return M("Quel est le volume d’un cylindre de diamètre %d cm et de hauteur %d cm ? (π ≈ 3,14)" % (2 * r, h), "%s cm³" % d(V), ["%s cm³" % d(PI * 4 * r * r * h), "%s cm³" % d(2 * PI * r * h), "%s cm³" % d(PI * 2 * r * h)],
             "Rayon : %d cm ; V ≈ 3,14 × %d² × %d = <b>%s cm³</b>." % (r, r, h, d(V)))


def s4():
    k = R.choice(["dm_cm", "L_cm", "mL", "m_L", "cL", "cm_L"])
    a = R.randint(2, 40)
    if k == "dm_cm":
        return M("%d dm³ = … cm³" % a, "%s cm³" % num(a * 1000), ["%s cm³" % num(a * 10), "%s cm³" % num(a * 100), "%s cm³" % num(a * 10000)], "1 dm³ = 1 000 cm³ : <b>%s cm³</b>." % num(a * 1000))
    if k == "L_cm":
        return M("%d L = … cm³" % a, "%s cm³" % num(a * 1000), ["%s cm³" % num(a * 100), "%s cm³" % num(a * 10), "%d cm³" % a], "1 L = 1 dm³ = 1 000 cm³ : <b>%s cm³</b>." % num(a * 1000))
    if k == "mL":
        a = R.randint(50, 900)
        return M("%d cm³ = … mL" % a, "%d mL" % a, ["%s mL" % num(a * 10), "%s mL" % d(Fr(a, 10)), "%s mL" % num(a * 1000)], "1 cm³ = 1 mL : <b>%d mL</b>." % a)
    if k == "m_L":
        a = R.randint(1, 12)
        return M("%d m³ = … L" % a, "%s L" % num(a * 1000), ["%s L" % num(a * 100), "%s L" % num(a * 1000000), "%s L" % num(a * 10)], "1 m³ = 1 000 dm³ = 1 000 L : <b>%s L</b>." % num(a * 1000))
    if k == "cL":
        a = R.randint(10, 99)
        return M("%d cL = … L" % a, "%s L" % d(Fr(a, 100)), ["%s L" % d(Fr(a, 10)), "%s L" % d(Fr(a, 1000)), "%d L" % a], "1 L = 100 cL : <b>%s L</b>." % d(Fr(a, 100)))
    a = R.choice([250, 500, 750, 1500, 2000, 3500])
    return M("%s cm³ = … L" % num(a), "%s L" % d(Fr(a, 1000)), ["%s L" % d(Fr(a, 100)), "%s L" % d(Fr(a, 10)), "%s L" % num(a)], "1 000 cm³ = 1 L : <b>%s L</b>." % d(Fr(a, 1000)))


def s5():
    k = R.choice(["aqua", "boite", "verre", "piscine"])
    if k == "aqua":
        L_, l_, h_ = R.choice([50, 60, 80, 100]), R.choice([25, 30, 40]), R.choice([30, 40, 50])
        V = L_ * l_ * h_
        return M("Un aquarium mesure %d cm × %d cm × %d cm. Combien de litres d’eau contient-il quand il est plein ?" % (L_, l_, h_), "%s L" % d(Fr(V, 1000)), ["%s L" % num(V), "%s L" % d(Fr(V, 100)), "%s L" % d(Fr(V, 10000))],
                 "V = %s cm³ = <b>%s L</b> (1 000 cm³ = 1 L)." % (num(V), d(Fr(V, 1000))))
    if k == "boite":
        r, h = R.choice([(3, 10), (4, 10), (5, 20), (2, 25), (10, 10)])
        V = PI * r * r * h
        return M("Une boîte de conserve cylindrique a un rayon de %d cm et une hauteur de %d cm. Quel est son volume, en mL ? (π ≈ 3,14)" % (r, h), "%s mL" % d(V), ["%s mL" % d(V / 10), "%s mL" % d(2 * PI * r * h), "%s mL" % d(V * 10)],
                 "V ≈ 3,14 × %d² × %d = %s cm³ = <b>%s mL</b>." % (r, h, d(V), d(V)))
    if k == "verre":
        n = R.choice([4, 5, 8, 10])
        return M("Une bouteille de 1,5 L remplit exactement %d verres identiques. Quel est le volume d’un verre, en cL ?" % n, "%s cL" % d(Fr(150, n)), ["%s cL" % d(Fr(15, n)), "%s cL" % d(Fr(1500, n)), "%s cL" % d(Fr(150, n) + 5)],
                 "1,5 L = 150 cL ; 150 ÷ %d = <b>%s cL</b>." % (n, d(Fr(150, n))))
    L_, l_, h_ = R.randint(5, 12), R.randint(3, 6), R.choice([1, 2])
    return M("Une piscine de %d m × %d m est remplie sur %d m de profondeur. Combien de litres d’eau contient-elle ?" % (L_, l_, h_), "%s L" % num(L_ * l_ * h_ * 1000), ["%d L" % (L_ * l_ * h_), "%s L" % num(L_ * l_ * h_ * 100), "%s L" % num(L_ * l_ * h_ * 10000)],
             "V = %d m³ = <b>%s L</b>." % (L_ * l_ * h_, num(L_ * l_ * h_ * 1000)))


def main():
    seen = set()
    sets = [("Pavé droit et cube", mix(R, seen, [(s1, 20)])), ("Prisme droit", mix(R, seen, [(s2, 20)])),
            ("Cylindre", mix(R, seen, [(s3, 20)])), ("Unités de volume et de contenance", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Prisme droit et cylindre : V = <b>aire de la base × hauteur</b>.",
              "Pavé droit : V = L × l × h. Cylindre : V = π × r² × h.",
              "1 dm³ = 1 L = 1 000 cm³ ; 1 cm³ = 1 mL ; 1 m³ = 1 000 L."],
             [("Cylindre r = 3 cm, h = 10 cm", ["base : 3,14 × 9 = 28,26 cm²", "× 10"], "282,6 cm³")],
             [["V = base + hauteur", "On multiplie l’aire de la base par la hauteur."], ["Prendre le diamètre comme rayon", "r = d ÷ 2."], ["1 L = 100 cm³", "1 L = 1 000 cm³."]])
    faq = [("Qu’est-ce que la base d’un prisme ?", "L’une des deux faces parallèles et identiques ; les autres faces sont des rectangles."),
           ("Comment passer des cm³ aux litres ?", "On divise par 1 000.")]
    unit("5e", R, "volumes-et-conversions", "E",
         "Calculer le volume d’un cube, d’un pavé droit, d’un prisme droit et d’un cylindre de révolution ; effectuer des conversions d’unités de volume et de contenance",
         "Volumes : prisme droit et cylindre", "Volumes et conversions",
         "Fiches de maths 5e sur les volumes : pavé droit, prisme droit, cylindre, conversions cm³, dm³, L, mL et problèmes. 100 exercices corrigés.",
         "V = aire de la base × hauteur", "1 dm³ = 1 L = 1 000 cm³", body, faq, sets, 17)


if __name__ == "__main__":
    main()
