# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Longueurs et périmètres (Grandeurs et mesures)
  python3 tools/gen_fr_maths_cm1_longueurs_et_perimetres.py
Unités du millimètre au kilomètre (km, hm, dam, m, dm, cm, mm), conversions (CM2 : avec des décimaux), comparer,
calculer des longueurs, périmètre d’un polygone, d’un rectangle, d’un carré, côté manquant, problèmes.
Erreurs : multiplier par 10 à chaque rang mais oublier un rang (hm, dam), 3,5 m = 3 m 5 cm, oublier des côtés du périmètre.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, dz, table, NB
import gen_fr_maths_ce2_longueurs_et_perimetres as CE

R = K = None
L = 1
U = ["km", "hm", "dam", "m", "dm", "cm", "mm"]


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52116 + 100 * lv)
    K = Kids(R)
    CE.R = R


def M(v, u):
    return "%s%s%s" % (v, NB, u)


def s1():
    if R.random() < 0.3:
        it = CE.s1_unite()
        return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])
    i, j = sorted(R.sample(range(7), 2))
    if j - i > 3:
        return None
    n = R.randint(2, 99)
    r = n * 10 ** (j - i)
    return mcq("Complète : %s = … %s" % (M(num(n), U[i]), U[j]), num(r), [num(n * 10 ** (j - i - 1)) if j - i > 1 else num(n * 100), num(r * 10), num(n + 10 ** (j - i))],
               "Chaque unité vaut 10 fois l’unité à sa droite (%s). De %s à %s : %d rang%s, on multiplie par %s : <b>%s %s</b>." % (" ; ".join(U), U[i], U[j], j - i, "s" if j - i > 1 else "", num(10 ** (j - i)), num(r), U[j]))


def s2():
    k = R.choice(["mcm", "cm_m", "kmm", "m_km"] + (["mm_m", "dec"] if L == 2 else []))
    if k == "mcm":
        a, b = R.randint(1, 9), R.randint(1, 99)
        r = dz(a * 100 + b, 2)
        return mcq("Écris en mètres : %s %s" % (M(a, "m"), M(b, "cm")), M(r, "m"), [M("%d,%d" % (a, b), "m") if b < 10 else M(dz(a * 1000 + b, 3), "m"), M(num(a * 100 + b), "m"), M(dz(a * 10 + b, 1), "m") if b < 10 else M(dz(a * 100 + b, 3), "m")],
                   "%d cm = %s m : %s m + %s m = <b>%s m</b>." % (b, dz(b, 2), num(a), dz(b, 2), r))
    if k == "cm_m":
        n = R.randint(105, 999)
        if n % 100 == 0:
            return None
        return mcq("Complète : %s = … m" % M(num(n), "cm"), M(dz(n, 2), "m"), [M(dz(n, 1), "m"), M(dz(n, 3), "m"), M(num(n * 100), "m")],
                   "1 m = 100 cm : %d cm = <b>%s m</b>." % (n, dz(n, 2)))
    if k == "kmm":
        a, b = R.randint(1, 9), R.randint(5, 995)
        return mcq("Écris en mètres : %s %s" % (M(a, "km"), M(b, "m")), M(num(a * 1000 + b), "m"), [M(num(a * 100 + b), "m"), M(num(a + b), "m"), M(num(a * 10000 + b), "m")],
                   "%d km = %s m ; %s + %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "m_km":
        n = R.randint(1050, 9950)
        return mcq("Complète : %s = … km" % M(num(n), "m"), M(dz(n, 3), "km"), [M(dz(n, 2), "km"), M(num(n * 1000), "km"), M(dz(n, 1), "km")],
                   "1 km = 1 000 m : %s m = <b>%s km</b>." % (num(n), dz(n, 3)))
    if k == "mm_m":
        n = R.randint(1005, 9999)
        return mcq("Complète : %s = … m" % M(num(n), "mm"), M(dz(n, 3), "m"), [M(dz(n, 2), "m"), M(dz(n, 1), "m"), M(num(n * 1000), "m")],
                   "1 m = 1 000 mm : %s mm = <b>%s m</b>." % (num(n), dz(n, 3)))
    a = R.randint(11, 99)
    i, j = R.choice([(3, 5), (0, 3), (3, 6), (4, 6), (1, 3)])
    r = a * 10 ** (j - i)
    return mcq("Complète : %s = … %s" % (M(dz(a, 1), U[i]), U[j]), num(r // 10) if r % 10 == 0 else dz(r, 1), [dz(a * 10 ** (j - i - 1), 1) if j - i > 1 else dz(a, 2), num(r) , dz(a * 10 ** (j - i + 1), 1)],
                   "De %s à %s, on multiplie par %s : <b>%s %s</b>." % (U[i], U[j], num(10 ** (j - i)), num(r // 10) if r % 10 == 0 else dz(r, 1), U[j]))


def s3():
    k = R.choice(["cmp", "cmp", "calc"])
    if k == "cmp":
        a = R.randint(101, 999)
        b = a + R.choice([-35, -8, 8, 35, 60])
        A, B = M(dz(a, 2), "m"), M(num(b), "cm")
        big = A if a > b else B
        return mcq("Quelle est la plus grande longueur : %s ou %s ?" % (A, B), big, [B if big == A else A, "elles sont égales", "on ne peut pas comparer"],
                   "%s = %s cm. On compare %d cm et %d cm : <b>%s</b>." % (A, num(a), a, b, big))
    a, b = R.randint(105, 480), R.randint(25, 95)
    return mcq("Une planche mesure %s. On en coupe %s. Quelle longueur reste-t-il ?" % (M(dz(a, 2), "m"), M(b, "cm")), M(dz(a - b, 2), "m"), [M(dz(a, 2) if False else dz(a - b * 10, 2) if a > b * 10 else dz(a + b, 2), "m"), M(num(a - b), "m"), M(dz(a - b + 10, 2), "m")],
               "%s = %d cm ; %d − %d = %d cm = <b>%s m</b>." % (M(dz(a, 2), "m"), a, a, b, a - b, dz(a - b, 2)))


def s4():
    k = R.choice(["poly", "rect", "carre", "rect_formule", "cote"])
    CE.U_[0] = R.choice(["cm", "m"])
    u = CE.U_[0]
    if k == "poly":
        n = R.choice([4, 5, 6])
        sides = [R.randint(3, 25) for _ in range(n)]
        P = sum(sides)
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce polygone ?" % CE.poly_svg("poly", sides), M(P, u), [M(P - sides[0], u), M(P + sides[1], u), M(max(sides) * n, u) if max(sides) * n != P else M(P + 1, u)],
                   "On additionne tous les côtés : %s = <b>%d %s</b>." % (" + ".join(map(str, sides)), P, u))
    if k == "rect":
        Lg, l = R.randint(8, 30), R.randint(3, 15)
        if Lg <= l:
            return None
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce rectangle ?" % CE.poly_svg("rect", (Lg, l)), M(2 * (Lg + l), u), [M(Lg + l, u), M(Lg * l, u), M(2 * Lg + l, u)],
                   "(%d + %d) %s 2 = <b>%d %s</b>." % (Lg, l, FOIS, 2 * (Lg + l), u))
    if k == "carre":
        c = R.randint(4, 40)
        return mcq("Quel est le périmètre d’un carré de %s de côté ?" % M(c, u), M(4 * c, u), [M(2 * c, u), M(c * c, u) if c != 4 else M(3 * c, u), M(4 * c + 4, u)],
                   "4 côtés égaux : 4 %s %d = <b>%d %s</b>." % (FOIS, c, 4 * c, u))
    if k == "rect_formule":
        Lg, l = R.randint(105, 480), R.randint(45, 99)
        if L == 1:
            Lg, l = R.randint(12, 60), R.randint(5, 11)
            return mcq("Un rectangle mesure %s sur %s. Quel est son périmètre ?" % (M(Lg, "m"), M(l, "m")), M(2 * (Lg + l), "m"), [M(Lg + l, "m"), M(2 * Lg + l, "m"), M(Lg * l, "m")],
                       "(%d + %d) %s 2 = <b>%d m</b>." % (Lg, l, FOIS, 2 * (Lg + l)))
        return mcq("Un rectangle mesure %s sur %s. Quel est son périmètre ?" % (M(dz(Lg, 2), "m"), M(l, "cm")), M(dz(2 * (Lg + l), 2), "m"), [M(dz(Lg + l, 2), "m"), M(dz(2 * Lg + 2 * l * 10, 2), "m"), M(num(2 * (Lg + l)), "m")],
                   "%d cm = %s m ; (%s + %s) %s 2 = <b>%s m</b>." % (l, dz(l, 2), dz(Lg, 2), dz(l, 2), FOIS, dz(2 * (Lg + l), 2)))
    Lg = R.randint(10, 40)
    l = R.randint(3, Lg - 1)
    P = 2 * (Lg + l)
    return mcq("Un rectangle a un périmètre de %s et une longueur de %s. Quelle est sa largeur ?" % (M(P, u), M(Lg, u)), M(l, u), [M(P - Lg, u), M(P // 2, u), M(P // 2 - Lg + 1, u)],
               "Longueur + largeur = %d %s 2 = %d ; largeur = %d − %d = <b>%d %s</b>." % (P, DIV, P // 2, P // 2, Lg, l, u))


def s5():
    p = K.next()
    k = R.choice(["cloture", "tour", "course", "ruban", "marche"])
    if k == "cloture":
        Lg, l, pr = R.randint(15, 40), R.randint(8, 20), R.randint(4, 12)
        P = 2 * (Lg + l)
        return mcq("Un jardin rectangulaire mesure %d m sur %d m. Le grillage coûte %d € le mètre. Combien coûte le grillage pour faire le tour ?" % (Lg, l, pr), "%s €" % num(P * pr), ["%s €" % num((Lg + l) * pr), "%s €" % num(Lg * l * pr), "%s €" % num(P + pr)],
                   "Périmètre : (%d + %d) %s 2 = %d m ; %d %s %d = <b>%s €</b>." % (Lg, l, FOIS, P, P, FOIS, pr, num(P * pr)))
    if k == "tour":
        t, n = R.choice([250, 400, 500, 800]), R.randint(3, 12)
        return mcq("Une piste fait %d m. %s fait %d tours. Quelle distance parcourt-%s, en kilomètres ?" % (t, p[0], n, p[1]), M(dz(t * n, 3), "km"), [M(num(t * n), "km"), M(dz(t * n, 2), "km"), M(dz(t * (n + 1), 3), "km")],
                   "%d %s %d = %s m = <b>%s km</b>." % (t, FOIS, n, num(t * n), dz(t * n, 3)))
    if k == "course":
        a, b = R.randint(1, 9), R.randint(100, 900)
        return mcq("Une course fait %s. %s a déjà couru %s m. Combien de mètres lui reste-t-il ?" % (M(a + 1, "km"), p[0], num(b * 10 if b * 10 < (a + 1) * 1000 else b)), None or M(num((a + 1) * 1000 - (b * 10 if b * 10 < (a + 1) * 1000 else b)), "m"),
                   [M(num(a + 1 + (b * 10 if b * 10 < (a + 1) * 1000 else b)), "m"), M(num((a + 1) * 100 - (b if b < (a + 1) * 100 else 0)), "m"), M(num((a + 1) * 1000), "m")],
                   "%d km = %s m ; on soustrait : <b>%s m</b>." % (a + 1, num((a + 1) * 1000), num((a + 1) * 1000 - (b * 10 if b * 10 < (a + 1) * 1000 else b))))
    if k == "ruban":
        n, c = R.randint(4, 9), R.randint(15, 45)
        return mcq("On coupe %d morceaux de %d cm dans un ruban de 5 m. Quelle longueur de ruban reste-t-il ?" % (n, c), M(num(500 - n * c), "cm"), [M(num(5 - n * c) if 5 > n * c else num(n * c - 5), "cm"), M(num(n * c), "cm"), M(num(500 - c), "cm")],
                   "%d %s %d = %d cm ; 5 m = 500 cm ; 500 − %d = <b>%d cm</b>." % (n, FOIS, c, n * c, n * c, 500 - n * c)) if n * c < 500 else None
    a, b = R.randint(450, 980), R.randint(1200, 2800)
    return mcq("%s marche %s m pour aller à l’école et %s m pour aller au stade. Quelle distance en tout, en kilomètres ?" % (p[0], num(a), num(b)), M(dz(a + b, 3), "km"), [M(num(a + b), "km"), M(dz(a + b, 2), "km"), M(dz(a + b + 1000, 3), "km")],
               "%s + %s = %s m = <b>%s km</b>." % (num(a), num(b), num(a + b), dz(a + b, 3)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Unités de longueur", mix(R, seen, [(s1, 20)])),
        ("Convertir" + ("" if lv == 1 else " avec des décimaux"), mix(R, seen, [(s2, 20)])),
        ("Comparer et calculer", mix(R, seen, [(s3, 20)])),
        ("Le périmètre", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Unités de longueur : <b>km, hm, dam, m, dm, cm, mm</b>. Chaque unité vaut 10 fois celle qui est à sa droite.",
         "1 km = 1 000 m ; 1 m = 100 cm = 1 000 mm. Un tableau de conversion aide à placer les chiffres.",
         "3 m 45 cm = 3,45 m : le chiffre des unités est au rang du mètre.",
         "Le <b>périmètre</b> est la longueur du tour : on additionne les côtés. Rectangle : (L + l) %s 2. Carré : 4 %s c." % (FOIS, FOIS)],
        [example("2 km 350 m en m", ["2 km = 2 000 m", "2 000 + 350"], "2 350 m")],
        table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["", "", "", "3", "4", "5", ""]]) and [
            ["3,5 m = 3 m 5 cm", "3,5 m = 3 m 50 cm (5 dixièmes de mètre = 50 cm)."],
            ["Oublier hm et dam : 1 km = 100 m", "km → hm → dam → m : 3 rangs, 1 km = 1 000 m."],
            ["Additionner seulement deux côtés du rectangle", "Le tour a 4 côtés : (L + l) %s 2." % FOIS]],
        table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["", "", "", "3", "4", "5", ""]]))
    faq = [("À quoi sert le tableau de conversion ?", "On y place un chiffre par colonne, le chiffre des unités dans la colonne de l’unité donnée ; on lit ensuite dans la nouvelle unité."),
           ("Le périmètre a-t-il une unité ?", "Oui, c’est une longueur : cm, m, km…")]
    unit(lv, R, "longueurs-et-perimetres", "G",
         "Connaître et utiliser les unités de longueur du millimètre au kilomètre et leurs relations ; choisir une unité adaptée ; comparer, estimer et calculer des longueurs ; déterminer le périmètre d’un polygone et résoudre des problèmes",
         "Longueurs et périmètres", "Longueurs et périmètres",
         "Fiches de maths %s sur les longueurs : unités du mm au km, conversions%s, comparaisons, périmètre du rectangle et du carré et problèmes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else " avec des décimaux"),
         "1 km = 1 000 m ; 1 m = 100 cm.", "Périmètre du rectangle : (L + l) × 2.",
         body, faq, sets, 16)


if __name__ == "__main__":
    build(1)
