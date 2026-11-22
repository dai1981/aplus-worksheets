# -*- coding: utf-8 -*-
"""
France Maths 3e : Volumes (bilan : prisme, cylindre, pyramide, cône, boule ; solides composés ; unités)
  python3 tools/gen_fr_maths_3e_volumes.py
Erreurs : oublier ÷ 3 pour pyramide et cône, oublier 4/3 pour la boule, mauvaise conversion (1 dm³ = 1 L, 1 m³ = 1 000 L), volume × k au lieu de × k³.
"""
import random
import math
from fr_c4 import *

R = random.Random(60414)
K = Kids(R)


def rd(x, k=1):
    return Fr(round(x * 10 ** k), 10 ** k)


def s1():
    k = R.choice(["cyl", "cone", "boule", "prisme", "pyr"])
    if k == "cyl":
        r, h = R.randint(2, 10), R.randint(3, 20)
        v = rd(math.pi * r * r * h)
        return M("Quel est le volume d’un cylindre de rayon %d cm et de hauteur %d cm, arrondi au dixième ?" % (r, h), "%s cm³" % d(v), ["%s cm³" % d(rd(math.pi * r * r * h / 3)), "%s cm³" % d(rd(2 * math.pi * r * h)), "%s cm³" % d(rd(math.pi * (2 * r) ** 2 * h))],
                 "V = π × r² × h = π × %d² × %d ≈ <b>%s cm³</b>." % (r, h, d(v)))
    if k == "cone":
        r, h = R.randint(2, 10), R.randint(3, 20)
        v = rd(math.pi * r * r * h / 3)
        return M("Quel est le volume d’un cône de rayon %d cm et de hauteur %d cm, arrondi au dixième ?" % (r, h), "%s cm³" % d(v), ["%s cm³" % d(rd(math.pi * r * r * h)), "%s cm³" % d(rd(math.pi * r * h / 3)), "%s cm³" % d(rd(math.pi * r * r * h / 2))],
                 "V = π × r² × h ÷ 3 ≈ <b>%s cm³</b>." % d(v))
    if k == "boule":
        r = R.randint(2, 15)
        v = rd(4 / 3 * math.pi * r ** 3)
        return M("Quel est le volume d’une boule de rayon %d cm, arrondi au dixième ?" % r, "%s cm³" % d(v), ["%s cm³" % d(rd(math.pi * r ** 3)), "%s cm³" % d(rd(4 * math.pi * r * r)), "%s cm³" % d(rd(4 / 3 * math.pi * r * r))],
                 "V = 4/3 × π × r³ ≈ <b>%s cm³</b>." % d(v))
    if k == "prisme":
        b, hb, h = R.randint(2, 12), R.randint(2, 12), R.randint(3, 15)
        v = Fr(b * hb, 2) * h
        return M("Un prisme droit a pour base un triangle de base %d cm et de hauteur %d cm ; sa hauteur est %d cm. Quel est son volume ?" % (b, hb, h), "%s cm³" % d(v), ["%d cm³" % (b * hb * h), "%s cm³" % d(v / 3), "%d cm³" % (b + hb + h)],
                 "Aire de la base : %d × %d ÷ 2 = %s cm² ; V = %s × %d = <b>%s cm³</b>." % (b, hb, d(Fr(b * hb, 2)), d(Fr(b * hb, 2)), h, d(v)))
    c, h = R.randint(2, 12), R.choice([3, 6, 9, 12, 15])
    v = Fr(c * c * h, 3)
    return M("Une pyramide a une base carrée de %d cm de côté et une hauteur de %d cm. Quel est son volume ?" % (c, h), "%s cm³" % num(v), ["%s cm³" % num(c * c * h), "%s cm³" % num(Fr(c * c * h, 2)) if Fr(c * c * h, 2).denominator == 1 else "%s cm³" % num(v * 2), "%s cm³" % num(Fr(c * h, 3)) if Fr(c * h, 3).denominator == 1 else "%s cm³" % num(c * h)],
             "V = %d² × %d ÷ 3 = <b>%s cm³</b>." % (c, h, num(v)))


def s2():
    k = R.choice(["cm3L", "m3L", "Lcm3", "dm3"])
    if k == "cm3L":
        v = R.choice([250, 500, 750, 1500, 2000, 3500, 330, 1250])
        return M("Convertis %s cm³ en L." % num(v), "%s L" % d(Fr(v, 1000)), ["%s L" % d(Fr(v, 100)), "%s L" % d(Fr(v, 10)), "%s L" % num(v * 1000)], "1 L = 1 000 cm³ : <b>%s L</b>." % d(Fr(v, 1000)))
    if k == "m3L":
        v = R.choice([Fr(1, 2), 2, 3, Fr(5, 2), Fr(3, 10), 12])
        return M("Convertis %s m³ en L." % d(v), "%s L" % num(v * 1000), ["%s L" % num(v * 100), "%s L" % num(v * 1000000), "%s L" % d(v * 10)], "1 m³ = 1 000 dm³ = 1 000 L : <b>%s L</b>." % num(v * 1000))
    if k == "Lcm3":
        v = R.choice([Fr(3, 2), Fr(1, 4), 2, Fr(33, 100), 5])
        return M("Convertis %s L en cm³." % d(v), "%s cm³" % num(v * 1000), ["%s cm³" % d(v * 100), "%s cm³" % d(v * 10), "%s cm³" % num(v * 1000000)], "1 L = 1 000 cm³ : <b>%s cm³</b>." % num(v * 1000))
    v = R.choice([3, 25, 150, 1200])
    return M("Convertis %s dm³ en m³." % num(v), "%s m³" % d(Fr(v, 1000)), ["%s m³" % d(Fr(v, 10)), "%s m³" % d(Fr(v, 100)), "%s m³" % num(v * 1000)], "1 m³ = 1 000 dm³ : <b>%s m³</b>." % d(Fr(v, 1000)))


def s3():
    k = R.choice(["silo", "maison", "glace", "trou"])
    if k == "silo":
        r, h, hc = R.randint(2, 5), R.randint(5, 12), R.randint(2, 6)
        v = rd(math.pi * r * r * h + math.pi * r * r * hc / 3)
        return M("Un silo est formé d’un cylindre (rayon %d m, hauteur %d m) surmonté d’un cône (même rayon, hauteur %d m). Quel est son volume, arrondi au dixième ?" % (r, h, hc), "%s m³" % d(v), ["%s m³" % d(rd(math.pi * r * r * (h + hc))), "%s m³" % d(rd(math.pi * r * r * h)), "%s m³" % d(rd(math.pi * r * r * h + math.pi * r * r * hc))],
                 "π × %d² × %d + π × %d² × %d ÷ 3 ≈ <b>%s m³</b>." % (r, h, r, hc, d(v)))
    if k == "maison":
        a, b, h, t = R.randint(6, 12), R.randint(5, 10), R.randint(3, 6), R.randint(2, 4)
        v = a * b * h + Fr(b * t, 2) * a
        return M("Une maison est un pavé de %d m × %d m × %d m surmonté d’un toit en prisme de base triangulaire (base %d m, hauteur %d m, longueur %d m). Quel est son volume total ?" % (a, b, h, b, t, a), "%s m³" % d(v), ["%s m³" % d(a * b * h + b * t * a), "%d m³" % (a * b * (h + t)), "%d m³" % (a * b * h)],
                 "%d × %d × %d + %d × %d ÷ 2 × %d = <b>%s m³</b>." % (a, b, h, b, t, a, d(v)))
    if k == "glace":
        r, h = R.choice([(2, 10), (3, 12), (2, 9)])
        v = rd(math.pi * r * r * h / 3 + 2 / 3 * math.pi * r ** 3)
        return M("Un cornet de glace est un cône (rayon %d cm, hauteur %d cm) surmonté d’une demi-boule de même rayon. Quel est son volume total, arrondi au dixième ?" % (r, h), "%s cm³" % d(v), ["%s cm³" % d(rd(math.pi * r * r * h / 3 + 4 / 3 * math.pi * r ** 3)), "%s cm³" % d(rd(math.pi * r * r * h + 2 / 3 * math.pi * r ** 3)), "%s cm³" % d(rd(math.pi * r * r * h / 3))],
                 "Cône : π × %d² × %d ÷ 3 ; demi-boule : 2/3 × π × %d³ ; total ≈ <b>%s cm³</b>." % (r, h, r, d(v)))
    c, r = R.randint(6, 12), R.randint(1, 2)
    v = rd(c ** 3 - math.pi * r * r * c)
    return M("Un cube de %d cm d’arête est percé d’un trou cylindrique de rayon %d cm qui le traverse. Quel volume reste-t-il, arrondi au dixième ?" % (c, r), "%s cm³" % d(v), ["%s cm³" % d(rd(math.pi * r * r * c)), "%s cm³" % num(c ** 3), "%s cm³" % d(rd(c ** 3 - 2 * math.pi * r * c))],
             "%d³ − π × %d² × %d ≈ <b>%s cm³</b>." % (c, r, c, d(v)))


def s4():
    k = R.choice(["k3", "k3", "rk", "inv"])
    if k == "k3":
        kk = R.choice([2, 3, Fr(1, 2), Fr(1, 3), 4])
        V = R.choice([24, 54, 108, 216, 81])
        if (kk ** 3 * V).denominator != 1:
            return None
        return M("On %s un solide de volume %d cm³ avec un rapport %s. Quel est le nouveau volume ?" % ("agrandit" if kk > 1 else "réduit", V, fq(kk)), "%s cm³" % num(kk ** 3 * V), ["%s cm³" % fq(kk * V), "%s cm³" % fq(kk * kk * V), "%s cm³" % fq(3 * kk * V) if 3 * kk != kk * kk else "%s cm³" % fq(2 * kk * V)],
                 "Volume × k³ = %s : <b>%s cm³</b>." % (fq(kk ** 3), num(kk ** 3 * V)))
    if k == "rk":
        kk = R.choice([2, 3, 4, 5])
        return M("Le volume d’un solide est multiplié par %d. Par combien ses longueurs ont-elles été multipliées ?" % kk ** 3, str(kk), [str(kk ** 3 // 3) if kk ** 3 % 3 == 0 else str(kk * kk), str(kk ** 3), str(kk + 1)],
                 "k³ = %d, donc <b>k = %d</b>." % (kk ** 3, kk))
    V = R.choice([150, 200, 300, 450])
    r = R.choice([3, 4, 5])
    h = V / (math.pi * r * r)
    return M("Un cylindre de rayon %d cm a un volume de %d cm³. Quelle est sa hauteur, arrondie au dixième ?" % (r, V), "%s cm" % d(rd(h)), ["%s cm" % d(rd(V / (math.pi * r))), "%s cm" % d(rd(V / (2 * math.pi * r * r))), "%s cm" % d(rd(3 * h))],
             "h = V ÷ (π × r²) = %d ÷ (π × %d) ≈ <b>%s cm</b>." % (V, r * r, d(rd(h))))


def s5():
    k = R.choice(["piscine", "verres", "canette", "boules", "sable"])
    if k == "piscine":
        a, b, p = R.randint(8, 15), R.randint(4, 8), Fr(R.choice([12, 15, 18, 20]), 10)
        v = a * b * p
        return M("Une piscine de %d m × %d m a une profondeur de %s m. Combien de litres d’eau contient-elle ?" % (a, b, d(p)), "%s L" % num(v * 1000), ["%s L" % d(v), "%s L" % num(v * 100), "%s L" % num(v * 1000000)],
                 "%d × %d × %s = %s m³ = <b>%s L</b>." % (a, b, d(p), d(v), num(v * 1000)))
    if k == "verres":
        r, h = R.choice([(3, 8), (4, 10), (3, 10)])
        L_ = R.choice([1, Fr(3, 2), 2])
        n = int(L_ * 1000 / (math.pi * r * r * h))
        return M("Combien de verres cylindriques (rayon %d cm, hauteur %d cm) peut-on remplir entièrement avec %s L de jus ?" % (r, h, d(L_)), str(n), [str(n + 1), str(int(L_ * 1000 / (math.pi * r * h))), str(int(L_ * 1000 / (math.pi * r * r * h / 3)))],
                 "Un verre : π × %d² × %d ≈ %s cm³ ; %s cm³ ÷ %s ≈ %s : <b>%d verres</b>." % (r, h, d(rd(math.pi * r * r * h)), num(L_ * 1000), d(rd(math.pi * r * r * h)), d(rd(L_ * 1000 / (math.pi * r * r * h), 2)), n))
    if k == "canette":
        r, h = R.choice([(3, 11), (Fr(33, 10), 12), (Fr(29, 10), 15)])
        cl = round(math.pi * float(r) ** 2 * h / 10)
        return M("Une canette cylindrique a un rayon de %s cm et une hauteur de %d cm. Quelle est sa contenance en cL, arrondie à l’unité ?" % (d(r), h), "%d cL" % cl, ["%d cL" % round(math.pi * float(r) ** 2 * h), "%d cL" % round(math.pi * float(r) * h / 10), "%d cL" % round(math.pi * float(r) ** 2 * h / 100)],
                 "V = π × %s² × %d ≈ %d cm³ ; 1 cL = 10 cm³ : <b>%d cL</b>." % (d(r), h, round(math.pi * float(r) ** 2 * h), cl))
    if k == "boules":
        r = R.choice([1, 2])
        R_ = R.choice([4, 6])
        n = (R_ // r) ** 3
        return M("On fait fondre une boule de métal de rayon %d cm pour fabriquer des petites boules de rayon %d cm. Combien de petites boules obtient-on ?" % (R_, r), str(n), [str(R_ // r), str((R_ // r) ** 2), str(R_ // r * 3)],
                 "Rapport des rayons : %d ; les volumes sont dans le rapport %d³ = <b>%d</b>." % (R_ // r, R_ // r, n))
    r, h = R.choice([(2, 3), (3, 2), (1, 3), (2, 2)])
    v = rd(math.pi * r * r * h / 3)
    return M("Un tas de sable conique a un rayon de %d m et une hauteur de %d m. Quel est son volume, arrondi au dixième ?" % (r, h), "%s m³" % d(v), ["%s m³" % d(rd(math.pi * r * r * h)), "%s m³" % d(rd(math.pi * r * h / 3)), "%s m³" % d(rd(r * r * h / 3))],
             "π × %d² × %d ÷ 3 ≈ <b>%s m³</b>." % (r, h, d(v)))


def main():
    seen = set()
    sets = [("Formules de volume", mix(R, seen, [(s1, 20)])), ("Unités de volume et de contenance", mix(R, seen, [(s2, 20)])),
            ("Solides composés", mix(R, seen, [(s3, 20)])), ("Agrandissements et calculs inverses", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Prisme et cylindre : <b>V = aire de la base × hauteur</b>. Pyramide et cône : <b>V = aire de la base × hauteur ÷ 3</b>. Boule : <b>V = 4/3 × π × r³</b>.",
              "1 dm³ = 1 L ; 1 cm³ = 1 mL ; 1 m³ = 1 000 L.",
              "Pour un solide composé, on additionne (ou on soustrait) les volumes des solides simples. Agrandir de rapport k multiplie le volume par k³."],
             [("Cylindre r = 3 cm, h = 10 cm, en L", ["π × 9 × 10 ≈ 282,7 cm³"], "≈ 0,28 L")],
             [["Oublier ÷ 3 pour un cône", "Un cône occupe le tiers du cylindre de même base et même hauteur."], ["1 m³ = 100 L", "1 m³ = 1 000 L."],
              ["Volume × k", "Le volume est multiplié par k³."]])
    faq = [("Comment retenir les formules ?", "« Base × hauteur » pour les solides droits, « ÷ 3 » pour les solides pointus, et 4/3 πr³ pour la boule."),
           ("Comment trouver une hauteur à partir d’un volume ?", "On divise le volume par l’aire de la base (et on multiplie par 3 pour un cône ou une pyramide).")]
    unit("3e", R, "volumes", "E",
         "Calculer le volume d’un prisme, d’un cylindre, d’une pyramide, d’un cône et d’une boule ; convertir des unités de volume et de contenance ; calculer le volume d’un solide composé ; utiliser l’effet d’un agrandissement ou d’une réduction",
         "Volumes : bilan des solides", "Volumes",
         "Fiches de maths 3e sur les volumes : prisme, cylindre, pyramide, cône, boule, unités, solides composés, agrandissements et problèmes. 100 exercices corrigés.",
         "Solides droits : base × hauteur ; solides pointus : ÷ 3", "Boule : 4/3 πr³ ; 1 dm³ = 1 L", body, faq, sets, 14)


if __name__ == "__main__":
    main()
