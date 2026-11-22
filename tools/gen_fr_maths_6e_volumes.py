# -*- coding: utf-8 -*-
"""
France Maths 6e : Volumes (pavé droit et cube, unités de volume et de contenance)
  python3 tools/gen_fr_maths_6e_volumes.py
Erreurs : additionner les dimensions au lieu de les multiplier, 1 dm³ = 10 cm³, confondre aire et volume.
"""
import random
from fr_c4 import *

R = random.Random(60118)
K = Kids(R)


def iso(L_, l_, h_, u=22):
    """pavé de cubes unité en perspective cavalière"""
    dx, dy = u * 0.5, u * 0.35
    s = []
    W = L_ * u + l_ * dx + 20
    H = h_ * u + l_ * dy + 20
    ox, oy = 10, 10 + l_ * dy
    for z in range(h_):
        for x in range(L_):
            X, Y = ox + x * u, oy + (h_ - 1 - z) * u
            s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#cfe6d6' stroke='%s' stroke-width='1.2'/>" % (X, Y, u, u, GREEN))
    for y in range(l_):
        for x in range(L_):
            X, Y = ox + x * u + (y + 1) * dx, oy - (y + 1) * dy
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e6f3ea' stroke='%s' stroke-width='1.2'/>" % (X - dx, Y + dy, X - dx + u, Y + dy, X + u, Y, X, Y, GREEN))
    for y in range(l_):
        for z in range(h_):
            X, Y = ox + L_ * u + y * dx, oy + (h_ - 1 - z) * u - y * dy
            s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#b9dcc4' stroke='%s' stroke-width='1.2'/>" % (X, Y, X + dx, Y - dy, X + dx, Y - dy + u, X, Y + u, GREEN))
    return wrap(W, H, "".join(s), "un pavé formé de petits cubes", lg=True)


def s1():
    L_, l_, h_ = R.randint(2, 5), R.randint(1, 3), R.randint(1, 4)
    n = L_ * l_ * h_
    return M("<div class='qfig'>%s</div>Ce pavé est formé de petits cubes identiques (il est plein). Combien y en a-t-il ?" % iso(L_, l_, h_), str(n), [str(L_ + l_ + h_), str(L_ * h_ + l_ * h_ + L_ * l_), str(n + L_)],
             "%d cubes en longueur, %d en largeur, %s : %d × %d × %d = <b>%d</b>." % (L_, l_, pl(h_, "couche"), L_, l_, h_, n))


def s2():
    L_, l_, h_ = R.randint(3, 15), R.randint(2, 10), R.randint(2, 10)
    u = R.choice(["cm", "m", "dm"])
    if R.random() < 0.5:
        return M("Quel est le volume d’un pavé droit de %d %s × %d %s × %d %s ?" % (L_, u, l_, u, h_, u), "%s %s³" % (num(L_ * l_ * h_), u), ["%d %s³" % (L_ + l_ + h_, u), "%s %s²" % (num(L_ * l_ * h_), u), "%s %s³" % (num(2 * (L_ * l_ + l_ * h_ + L_ * h_)), u)],
                 "V = L × l × h = %d × %d × %d = <b>%s %s³</b>." % (L_, l_, h_, num(L_ * l_ * h_), u))
    V = L_ * l_ * h_
    return M("Un pavé droit a un volume de %s cm³. Sa base mesure %d cm × %d cm. Quelle est sa hauteur ?" % (num(V), L_, l_), "%d cm" % h_, ["%d cm" % (V - L_ * l_), "%d cm" % (V // L_), "%d cm" % (h_ + 1)],
             "Aire de la base : %d × %d = %d cm² ; h = %s ÷ %d = <b>%d cm</b>." % (L_, l_, L_ * l_, num(V), L_ * l_, h_))


def s3():
    c = R.randint(2, 12)
    if R.random() < 0.7:
        u = R.choice(["cm", "m", "dm", "mm"])
        return M("Quel est le volume d’un cube d’arête %d %s ?" % (c, u), "%s %s³" % (num(c ** 3), u), ["%d %s³" % (3 * c, u), "%d %s³" % (c * c, u), "%s %s³" % (num(6 * c * c), u)],
                 "V = c × c × c = %d × %d × %d = <b>%s %s³</b>." % (c, c, c, num(c ** 3), u))
    c = R.choice([2, 3, 4, 5, 10])
    return M("Un cube a un volume de %s cm³. Quelle est la longueur de son arête ?" % num(c ** 3), "%d cm" % c, ["%d cm" % (c ** 3 // 3) if c ** 3 % 3 == 0 else "%d cm" % (c * c), "%d cm" % (c * c), "%d cm" % (c + 1)],
             "%d × %d × %d = %s : l’arête mesure <b>%d cm</b>." % (c, c, c, num(c ** 3), c))


def s4():
    k = R.choice(["dm_L", "cm_mL", "dm_cm", "L_cm", "m_L"])
    a = R.randint(2, 30)
    if k == "dm_L":
        return M("%d dm³ = … L" % a, "%d L" % a, ["%d L" % (a * 10), "%s L" % num(a * 1000), "%s L" % d(Fr(a, 10))], "1 dm³ = 1 L, donc <b>%d L</b>." % a)
    if k == "cm_mL":
        a = R.randint(20, 900)
        return M("%d cm³ = … mL" % a, "%d mL" % a, ["%s mL" % num(a * 1000), "%s mL" % d(Fr(a, 10)), "%s mL" % num(a * 10)], "1 cm³ = 1 mL, donc <b>%d mL</b>." % a)
    if k == "dm_cm":
        return M("%d dm³ = … cm³" % a, "%s cm³" % num(a * 1000), ["%s cm³" % num(a * 10), "%s cm³" % num(a * 100), "%s cm³" % num(a * 10000)], "1 dm³ = 10 × 10 × 10 cm³ = 1 000 cm³, donc <b>%s cm³</b>." % num(a * 1000))
    if k == "L_cm":
        return M("%d L = … cm³" % a, "%s cm³" % num(a * 1000), ["%s cm³" % num(a * 100), "%d cm³" % a, "%s cm³" % num(a * 10)], "1 L = 1 dm³ = 1 000 cm³, donc <b>%s cm³</b>." % num(a * 1000))
    a = R.randint(1, 9)
    return M("%d m³ = … L" % a, "%s L" % num(a * 1000), ["%d L" % (a * 100), "%d L" % (a * 10), "%s L" % num(a * 1000000)], "1 m³ = 1 000 dm³ = 1 000 L, donc <b>%s L</b>." % num(a * 1000))


def s5():
    p = K.next()
    k = R.choice(["aqua", "boite", "piscine", "cubes"])
    if k == "aqua":
        L_, l_, h_ = R.choice([40, 50, 60, 80]), R.choice([20, 25, 30]), R.choice([20, 30, 40])
        V = L_ * l_ * h_
        return M("Un aquarium mesure %d cm × %d cm × %d cm. Combien de litres d’eau peut-il contenir ?" % (L_, l_, h_), "%s L" % d(Fr(V, 1000)), ["%s L" % num(V), "%s L" % d(Fr(V, 100)), "%s L" % d(Fr(V, 10000))],
                 "V = %d × %d × %d = %s cm³ ; 1 000 cm³ = 1 L, donc <b>%s L</b>." % (L_, l_, h_, num(V), d(Fr(V, 1000))))
    if k == "boite":
        a, b, c = R.randint(2, 6), R.randint(2, 5), R.randint(2, 4)
        return M("On range des cubes de 1 cm d’arête dans une boîte de %d cm × %d cm × %d cm. Combien de cubes peut-on mettre ?" % (a, b, c), str(a * b * c), [str(a + b + c), str(a * b), str(2 * (a * b + b * c + a * c))],
                 "%d × %d × %d = <b>%d cubes</b>." % (a, b, c, a * b * c))
    if k == "piscine":
        L_, l_, h_ = R.randint(5, 12), R.randint(3, 6), R.choice([1, 2])
        return M("Une petite piscine mesure %d m × %d m et a %d m de profondeur. Quel est son volume en litres ?" % (L_, l_, h_), "%s L" % num(L_ * l_ * h_ * 1000), ["%d L" % (L_ * l_ * h_), "%s L" % num(L_ * l_ * h_ * 100), "%d L" % (L_ + l_ + h_)],
                 "V = %d × %d × %d = %d m³ = <b>%s L</b>." % (L_, l_, h_, L_ * l_ * h_, num(L_ * l_ * h_ * 1000)))
    c = R.choice([2, 3, 4])
    return M("Combien de petits cubes d’arête 1 cm faut-il pour construire un cube d’arête %d cm ?" % c, str(c ** 3), [str(c * c), str(3 * c), str(6 * c * c)],
             "%d × %d × %d = <b>%d</b>." % (c, c, c, c ** 3))


def main():
    seen = set()
    sets = [("Compter des cubes", mix(R, seen, [(s1, 20)])), ("Volume du pavé droit", mix(R, seen, [(s2, 20)])),
            ("Volume du cube", mix(R, seen, [(s3, 20)])), ("Unités de volume et de contenance", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>volume</b> mesure la place qu’occupe un solide. 1 cm³ est le volume d’un cube de 1 cm d’arête.",
              "Pavé droit : V = longueur × largeur × hauteur. Cube : V = c × c × c.",
              "1 dm³ = 1 000 cm³ = 1 L ; 1 cm³ = 1 mL ; 1 m³ = 1 000 L."],
             [("Pavé de 5 cm × 4 cm × 3 cm", ["5 × 4 = 20 cubes par couche", "20 × 3 couches"], "60 cm³")],
             [["Additionner les dimensions", "Le volume se calcule en multipliant : 5 × 4 × 3."],
              ["Croire que 1 dm³ = 10 cm³", "1 dm³ = 10 × 10 × 10 = 1 000 cm³."],
              ["Confondre aire et volume", "L’aire est en cm², le volume en cm³."]])
    faq = [("Quelle est la différence entre volume et contenance ?", "Le volume est la place occupée ; la contenance est ce qu’un récipient peut contenir. On utilise 1 dm³ = 1 L pour passer de l’un à l’autre."),
           ("Pourquoi multiplier trois nombres ?", "Longueur × largeur donne le nombre de cubes d’une couche, et on multiplie par le nombre de couches.")]
    unit("6e", R, "volumes", "G",
         "Déterminer le volume d’un pavé droit par dénombrement de cubes unités ; utiliser les formules du volume du cube et du pavé droit ; relier les unités de volume et de contenance (1 dm³ = 1 L)",
         "Volumes du cube et du pavé droit", "Volumes",
         "Fiches de maths 6e sur les volumes : compter des cubes, volume du pavé droit et du cube, cm³, dm³, litres et problèmes. 100 exercices corrigés.",
         "V = L × l × h", "1 dm³ = 1 L", body, faq, sets, 18)


if __name__ == "__main__":
    main()
