# -*- coding: utf-8 -*-
"""
France Maths CE2 : Longueurs et périmètres (Grandeurs et mesures)
  python3 tools/gen_fr_maths_ce2_longueurs_et_perimetres.py
Choisir l’unité (km, m, dm, cm, mm), convertir, comparer, mesurer avec une règle, calculer des longueurs, périmètre
d’un polygone, d’un carré et d’un rectangle.
Erreurs : 1 m = 10 cm, oublier de convertir avant de comparer, lire la règle à partir de 1, oublier des côtés du périmètre.
"""
import random, math
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, text, line, INK, RED, FILL, GREEN, NB

R = random.Random(51012)
K = Kids(R)

OBJ = [("Un crayon mesure", 15, "cm"), ("Une gomme mesure", 4, "cm"), ("Une fourmi mesure", 5, "mm"), ("Une coccinelle mesure", 7, "mm"),
       ("La classe mesure", 9, "m"), ("Le trajet en voiture de Paris à Lyon fait", 465, "km"), ("Un timbre mesure", 25, "mm"),
       ("La hauteur d’une porte est", 2, "m"), ("Un autobus mesure", 12, "m"), ("Une piscine olympique mesure", 50, "m"), ("Un livre mesure", 24, "cm"),
       ("La largeur d’un ongle est", 1, "cm"), ("Une baguette de pain mesure", 65, "cm"), ("Le tour d’une piste d’athlétisme fait", 400, "m"),
       ("Une étape du Tour de France fait", 160, "km"), ("Un grain de riz mesure", 6, "mm"), ("Un lit mesure", 2, "m"),
       ("Une règle d’écolier mesure", 30, "cm"), ("Une rue du village mesure", 300, "m"), ("La Loire mesure", 1006, "km"), ("Une pièce de 1 € mesure", 23, "mm"),
       ("La hauteur d’une table est", 75, "cm"), ("Un marathon fait", 42, "km"), ("Un terrain de football mesure", 105, "m")]
UNITS = ["mm", "cm", "m", "km"]
TO_MM = {"mm": 1, "cm": 10, "dm": 100, "m": 1000, "km": 1000000}


def s1_unite():
    o, v, u = R.choice(OBJ)
    return mcq("Quelle unité convient ? %s environ %s …" % (o, num(v)), u, [x for x in UNITS if x != u],
               "%s environ %s <b>%s</b>." % (o, num(v), u))


def L(v, u):
    return "%s%s%s" % (num(v), NB, u)


def s2_conv():
    k = R.choice(["m_cm", "km_m", "cm_mm", "m_dm", "dm_cm", "mcm", "cm_mcm", "kmm"])
    if k == "m_cm":
        a = R.randint(2, 9)
        return mcq("Complète : %s = … cm" % L(a, "m"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 m = 100 cm, donc %d m = <b>%s cm</b>." % (a, num(a * 100)))
    if k == "km_m":
        a = R.randint(2, 9)
        return mcq("Complète : %s = … m" % L(a, "km"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 km = 1 000 m, donc %d km = <b>%s m</b>." % (a, num(a * 1000)))
    if k == "cm_mm":
        a = R.randint(2, 30)
        return mcq("Complète : %s = … mm" % L(a, "cm"), num(a * 10), [num(a * 100), num(a + 10), str(a)], "1 cm = 10 mm, donc %d cm = <b>%s mm</b>." % (a, num(a * 10)))
    if k == "m_dm":
        a = R.randint(2, 9)
        return mcq("Complète : %s = … dm" % L(a, "m"), num(a * 10), [num(a * 100), str(a), num(a * 1000)], "1 m = 10 dm, donc %d m = <b>%s dm</b>." % (a, num(a * 10)))
    if k == "dm_cm":
        a = R.randint(2, 15)
        return mcq("Complète : %s = … cm" % L(a, "dm"), num(a * 10), [num(a * 100), str(a), num(a + 10)], "1 dm = 10 cm, donc %d dm = <b>%s cm</b>." % (a, num(a * 10)))
    if k == "mcm":
        a, b = R.randint(1, 8), R.randint(5, 95)
        return mcq("Complète : %s %s = … cm" % (L(a, "m"), L(b, "cm")), num(a * 100 + b), [num(a + b), num(a * 10 + b), "%d%02d" % (a, b) if b >= 10 else "%d%d" % (a, b)],
                   "%d m = %d cm, et %d + %d = <b>%s cm</b>." % (a, a * 100, a * 100, b, num(a * 100 + b)))
    if k == "cm_mcm":
        a, b = R.randint(1, 8), R.randint(5, 95)
        n = a * 100 + b
        return mcq("Complète : %s = … m … cm" % L(n, "cm"), "%s %s" % (L(a, "m"), L(b, "cm")), ["%s %s" % (L(n // 10, "m"), L(n % 10, "cm")), "%s %s" % (L(a * 10 + b // 10, "m"), L(b % 10, "cm")), "%s %s" % (L(a + 1, "m"), L(b, "cm"))],
                   "100 cm = 1 m. %d cm = %d cm + %d cm = <b>%d m %d cm</b>." % (n, a * 100, b, a, b))
    a, b = R.randint(1, 6), R.choice([50, 100, 200, 250, 500, 750, 800, 300])
    return mcq("Complète : %s %s = … m" % (L(a, "km"), L(b, "m")), num(a * 1000 + b), [num(a * 100 + b), num(a + b), num(a * 1000 + b * 10)],
               "%d km = %s m, et %s + %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))


def s3_cmp():
    k = R.choice(["mcm", "kmm", "cmmm"])
    if k == "mcm":
        a, b = R.randint(1, 5), R.randint(5, 95)
        x = a * 100 + b
        y = x + R.choice([-30, -9, 9, 30, 45, -45])
        if y <= 0 or y == x:
            return None
        A, B = "%s %s" % (L(a, "m"), L(b, "cm")), L(y, "cm")
        big = A if x > y else B
    elif k == "kmm":
        a = R.randint(1, 6)
        x = a * 1000
        y = R.choice([a * 100, a * 1000 + R.choice([-150, 150, 900]), a * 1000 - 900])
        if y == x or y <= 0:
            return None
        A, B = L(a, "km"), L(y, "m")
        big = A if x > y else B
    else:
        a = R.randint(3, 40)
        x = a * 10
        y = x + R.choice([-6, -15, 7, 15, 40])
        if y <= 0 or y == x:
            return None
        A, B = L(a, "cm"), L(y, "mm")
        big = A if x > y else B
    small = B if big == A else A
    return mcq("Quelle est la plus grande longueur : %s ou %s ?" % (A, B), big, [small, "elles sont égales", "on ne peut pas comparer"],
               "On convertit dans la même unité avant de comparer. La plus grande est <b>%s</b>." % big)


def regle(a, b):
    """règle en cm, segment de a à b (en mm)"""
    W = 14 * 34 + 20
    s = ["<rect x='6' y='40' width='%d' height='46' fill='#f6efd6' stroke='%s' stroke-width='1.5'/>" % (W - 12, INK)]
    for mm in range(0, 141):
        x = 14 + mm * 3.4
        h = 16 if mm % 10 == 0 else 10 if mm % 5 == 0 else 6
        s.append(line(x, 40, x, 40 + h, INK, 1.2 if mm % 10 else 1.6))
        if mm % 10 == 0:
            s.append(text(x, 76, str(mm // 10), 12, weight=600))
    s.append(line(14 + a * 3.4, 26, 14 + b * 3.4, 26, RED, 4))
    for v in (a, b):
        s.append(line(14 + v * 3.4, 20, 14 + v * 3.4, 32, RED, 2))
    return wrap(W, 92, "".join(s), "règle graduée en centimètres et un segment rouge", lg=True)


def s4_regle():
    a = R.choice([0, 0, 10, 20, 30])
    b = a + R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90]) + R.choice([0, 0, 5])
    if b > 140:
        return None
    ln = b - a
    right = "%d cm" % (ln // 10) if ln % 10 == 0 else "%d cm %d mm" % (ln // 10, ln % 10)
    wr = ["%d cm" % (b // 10) if b % 10 == 0 else "%d cm %d mm" % (b // 10, b % 10), "%d cm" % (ln // 10 + 1), "%d mm" % (ln // 10)]
    return mcq("<div class='qfig'>%s</div>Quelle est la longueur du segment rouge ?" % regle(a, b), right, [w for w in wr if w != right],
               "Le segment va de %s à %s : %s − %s = <b>%s</b>." % (("%g" % (a / 10.0)).replace(".", ","), ("%g" % (b / 10.0)).replace(".", ","), ("%g" % (b / 10.0)).replace(".", ","), ("%g" % (a / 10.0)).replace(".", ","), right))


def s4_calc():
    p = K.next()
    k = R.choice(["corde", "course", "planche"])
    if k == "corde":
        a, b = R.randint(2, 5), R.randint(15, 85)
        return mcq("%s a une corde de %d m. %s en coupe %d cm. Quelle longueur reste-t-il ?" % (p[0], a, p[1].capitalize(), b), "%d cm" % (a * 100 - b), ["%d cm" % (a * 100 + b), "%d m" % (a - 1), "%d cm" % (a * 10 - b) if a * 10 > b else "%d cm" % (a * 100 - b + 10)],
                   "%d m = %d cm, puis %d − %d = <b>%d cm</b> (soit %d m %d cm)." % (a, a * 100, a * 100, b, a * 100 - b, (a * 100 - b) // 100, (a * 100 - b) % 100))
    if k == "course":
        a, b = R.randint(1, 4), R.choice([200, 300, 400, 500, 600, 800])
        return mcq("%s court %d km le matin et %d m le soir. Quelle distance parcourt-%s en tout, en mètres ?" % (p[0], a, b, p[1]), "%s m" % num(a * 1000 + b), ["%s m" % num(a + b), "%s m" % num(a * 100 + b), "%s m" % num(a * 1000 + b + 100)],
                   "%d km = %s m ; %s + %d = <b>%s m</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    n, l = R.randint(3, 6), R.randint(25, 80)
    return mcq("On met %d planches de %d cm bout à bout. Quelle longueur obtient-on ?" % (n, l), "%s cm" % num(n * l), ["%s cm" % num(n + l), "%s cm" % num(n * l + l), "%s m" % num(n * l)],
               "%d %s %d = <b>%s cm</b>." % (n, "×", l, num(n * l)))


def poly_svg(kind, sides):
    if kind in ("rect", "carre"):
        L_, l_ = sides
        sc = 150.0 / max(L_, l_)
        w, h = max(L_ * sc, 40), max(l_ * sc, 40)
        x0, y0 = 50, 30
        s = ["<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, w, h, FILL, GREEN),
             text(x0 + w / 2, y0 - 8, unitf(L_), 14), text(x0 - 8, y0 + h / 2 + 5, unitf(l_), 14, anchor="end")]
        return wrap(x0 + w + 30, y0 + h + 20, "".join(s), "rectangle" if kind == "rect" else "carré", lg=True)
    n = len(sides)
    pts = [(130 + 90 * math.cos(2 * math.pi * i / n - math.pi / 2), 110 + 90 * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN)]
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = mx - 130, my - 110
        d = math.hypot(dx, dy) or 1
        s.append(text(mx + dx / d * 22, my + dy / d * 22 + 5, unitf(sides[i]), 13))
    return wrap(260, 225, "".join(s), "polygone à %d côtés" % n, lg=True)


U_ = ["cm"]


def unitf(v):
    return "%d%s%s" % (v, NB, U_[0])


def s5():
    k = R.choice(["poly", "poly", "rect", "carre", "cloture", "carre_txt"])
    U_[0] = R.choice(["cm", "m"])
    if k == "poly":
        n = R.choice([3, 4, 5, 6])
        sides = [R.randint(3, 15) for _ in range(n)]
        P = sum(sides)
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce polygone ?" % poly_svg("poly", sides), unitf(P), [unitf(P - sides[0]), unitf(P + sides[0]), unitf(max(sides) * n) if max(sides) * n != P else unitf(P + 1)],
                   "Le périmètre est le tour de la figure : %s = <b>%s</b>." % (" + ".join(map(str, sides)), unitf(P)))
    if k == "rect":
        L_, l_ = R.randint(5, 20), R.randint(2, 12)
        if L_ <= l_:
            return None
        P = 2 * (L_ + l_)
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce rectangle ?" % poly_svg("rect", (L_, l_)), unitf(P), [unitf(L_ + l_), unitf(L_ * l_) if L_ * l_ != P else unitf(P + 2), unitf(2 * L_ + l_)],
                   "Un rectangle a 2 longueurs et 2 largeurs : %d + %d + %d + %d = <b>%s</b>." % (L_, l_, L_, l_, unitf(P)))
    if k == "carre":
        c = R.randint(3, 25)
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce carré ?" % poly_svg("carre", (c, c)), unitf(4 * c), [unitf(2 * c), unitf(c * c) if c != 4 else unitf(3 * c), unitf(4 * c + 4)],
                   "Le carré a 4 côtés égaux : 4 %s %d = <b>%s</b>." % ("×", c, unitf(4 * c)))
    if k == "carre_txt":
        P = 4 * R.randint(3, 25)
        return mcq("Le périmètre d’un carré est %s. Quelle est la longueur de son côté ?" % unitf(P), unitf(P // 4), [unitf(P // 2), unitf(P - 4), unitf(P * 4)],
                   "4 côtés égaux : %d %s 4 = <b>%s</b>." % (P, "÷", unitf(P // 4)))
    U_[0] = "m"
    L_, l_ = R.randint(12, 40), R.randint(6, 25)
    if L_ <= l_:
        return None
    return mcq("Un jardin rectangulaire mesure %d m de long et %d m de large. Quelle longueur de clôture faut-il pour en faire le tour ?" % (L_, l_), unitf(2 * (L_ + l_)), [unitf(L_ + l_), unitf(L_ * l_), unitf(2 * L_ + l_)],
               "Le tour du jardin : %d + %d + %d + %d = <b>%d m</b>." % (L_, l_, L_, l_, 2 * (L_ + l_)))


def main():
    seen = set()
    sets = [
        ("Choisir la bonne unité", mix(R, seen, [(s1_unite, 20)])),
        ("Convertir des longueurs", mix(R, seen, [(s2_conv, 20)])),
        ("Comparer des longueurs", mix(R, seen, [(s3_cmp, 20)])),
        ("Mesurer et calculer", mix(R, seen, [(s4_regle, 12), (s4_calc, 8)])),
        ("Le périmètre", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Les unités de longueur : <b>1 km = 1 000 m</b>, <b>1 m = 10 dm = 100 cm</b>, <b>1 dm = 10 cm</b>, <b>1 cm = 10 mm</b>.",
         "Pour comparer ou calculer, on écrit les longueurs <b>dans la même unité</b>.",
         "Avec une règle, on place le 0 au début du segment. Si on part d’un autre nombre, on fait une soustraction.",
         "Le <b>périmètre</b> est la longueur du tour d’une figure : on additionne tous les côtés."],
        [example("3 m 25 cm = … cm", ["3 m = 300 cm", "300 + 25 = 325"], "325 cm"),
         example("Périmètre d’un rectangle de 8 cm sur 3 cm", ["8 + 3 + 8 + 3"], "22 cm")],
        [["1 m = 10 cm", "1 m = 100 cm (et 1 dm = 10 cm)."],
         ["Comparer 2 m et 150 cm sans convertir : 150 &gt; 2", "2 m = 200 cm, donc 2 m &gt; 150 cm."],
         ["Oublier deux côtés du rectangle : 8 + 3 = 11 cm", "Le tour a 4 côtés : 22 cm."]])
    faq = [("Qu’est-ce que le décimètre ?", "Un décimètre (dm) vaut 10 cm. Il y a 10 dm dans 1 m."),
           ("Le périmètre a-t-il une unité ?", "Oui, c’est une longueur : on écrit toujours l’unité (cm, m…).")]
    make_unit(R, "longueurs-et-perimetres", "G",
              "Comparer, mesurer et estimer des longueurs ; connaître les unités km, m, dm, cm, mm et leurs relations ; calculer des longueurs ; calculer le périmètre d’un polygone (résumé du programme 2024 du cycle 2).",
              "Longueurs et périmètres", "Longueurs et périmètres CE2 : fiches et exercices avec corrigé", "Longueurs et périmètres",
              "Fiches de maths CE2 sur les longueurs : km, m, dm, cm, mm, conversions, comparaisons, mesurer avec une règle et calculer des périmètres. 100 exercices corrigés.",
              "1 m = 100 cm ; 1 km = 1 000 m ; 1 cm = 10 mm.", "Le périmètre est la longueur du tour de la figure.",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
