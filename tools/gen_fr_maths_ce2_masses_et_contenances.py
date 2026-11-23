# -*- coding: utf-8 -*-
"""
France Maths CE2 : Masses et contenances (Grandeurs et mesures)
  python3 tools/gen_fr_maths_ce2_masses_et_contenances.py
Choisir l’unité (g, kg, t ; L, dL, cL), convertir, comparer, lire une balance en équilibre et un verre doseur, problèmes.
Erreurs : 1 kg = 100 g, comparer sans convertir (800 g &gt; 2 kg), confondre masse et contenance, lire une graduation sur deux.
"""
import random
from fr_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, text, line, INK, FILL, GREEN, BLUE, NB, FOIS

R = random.Random(51013)
K = Kids(R)


def U(v, u):
    return "%s%s%s" % (num(v), NB, u)


MASS = [("Un éléphant pèse environ", 5, "t"), ("Un sac de pommes de terre pèse", 10, "kg"), ("Une gomme pèse environ", 20, "g"), ("Un chat pèse environ", 4, "kg"),
        ("Une plume pèse environ", 1, "g"), ("Une voiture pèse environ", 1, "t"), ("Un paquet de beurre pèse", 250, "g"), ("Un enfant de 8 ans pèse environ", 25, "kg"),
        ("Un camion chargé pèse environ", 20, "t"), ("Une pomme pèse environ", 150, "g"), ("Un melon pèse environ", 1, "kg"), ("Une lettre pèse environ", 20, "g"),
        ("Une baleine bleue pèse environ", 150, "t"), ("Un vélo pèse environ", 12, "kg")]
CAP = [("Une baignoire contient environ", 150, "L"), ("Une cuillère à soupe contient environ", 1, "cL"), ("Un verre d’eau contient environ", 20, "cL"),
       ("Un seau contient environ", 10, "L"), ("Une canette contient", 33, "cL"), ("Une bouteille d’eau contient", 1, "L"), ("Un bol contient environ", 3, "dL"),
       ("Un aquarium contient environ", 60, "L"), ("Une tasse de café contient environ", 10, "cL"), ("Un arrosoir contient environ", 8, "L"),
       ("Une brique de lait contient", 1, "L"), ("Une petite bouteille de jus contient", 25, "cL")]


def s1_mass():
    o, v, u = R.choice(MASS)
    return mcq("Quelle unité convient ? %s %s …" % (o, num(v)), u, [x for x in ["g", "kg", "t", "L"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))


def s1_cap():
    o, v, u = R.choice(CAP)
    return mcq("Quelle unité convient ? %s %s …" % (o, num(v)), u, [x for x in ["L", "dL", "cL", "kg"] if x != u], "%s %s <b>%s</b>." % (o, num(v), u))


def s2():
    k = R.choice(["kg_g", "t_kg", "kgg", "g_kgg", "L_cL", "L_dL", "dL_cL", "LcL"])
    a = R.randint(2, 9)
    if k == "kg_g":
        return mcq("Complète : %s = … g" % U(a, "kg"), num(a * 1000), [num(a * 100), num(a * 10), num(a + 1000)], "1 kg = 1 000 g, donc %d kg = <b>%s g</b>." % (a, num(a * 1000)))
    if k == "t_kg":
        return mcq("Complète : %s = … kg" % U(a, "t"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 t = 1 000 kg, donc %d t = <b>%s kg</b>." % (a, num(a * 1000)))
    if k == "kgg":
        b = R.choice([50, 100, 200, 250, 300, 400, 500, 600, 750, 800, 900])
        return mcq("Complète : %s %s = … g" % (U(a, "kg"), U(b, "g")), num(a * 1000 + b), [num(a * 100 + b), num(a + b), num(a * 1000 + b * 10)],
                   "%d kg = %s g ; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "g_kgg":
        b = R.choice([50, 150, 200, 250, 300, 450, 500, 750, 800])
        n = a * 1000 + b
        return mcq("Complète : %s = … kg … g" % U(n, "g"), "%s %s" % (U(a, "kg"), U(b, "g")), ["%s %s" % (U(a * 10 + b // 100, "kg"), U(b % 100, "g")), "%s %s" % (U(n // 100, "kg"), U(n % 100, "g")), "%s %s" % (U(a + 1, "kg"), U(b, "g"))],
                   "1 000 g = 1 kg. %s g = %s g + %d g = <b>%d kg %d g</b>." % (num(n), num(a * 1000), b, a, b))
    if k == "L_cL":
        return mcq("Complète : %s = … cL" % U(a, "L"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 L = 100 cL, donc %d L = <b>%s cL</b>." % (a, num(a * 100)))
    if k == "L_dL":
        return mcq("Complète : %s = … dL" % U(a, "L"), num(a * 10), [num(a * 100), num(a), num(a * 1000)], "1 L = 10 dL, donc %d L = <b>%s dL</b>." % (a, num(a * 10)))
    if k == "dL_cL":
        a = R.randint(2, 20)
        return mcq("Complète : %s = … cL" % U(a, "dL"), num(a * 10), [num(a * 100), num(a), num(a + 10)], "1 dL = 10 cL, donc %d dL = <b>%s cL</b>." % (a, num(a * 10)))
    b = R.choice([25, 33, 50, 75, 20, 10, 40])
    return mcq("Complète : %s %s = … cL" % (U(a, "L"), U(b, "cL")), num(a * 100 + b), [num(a * 10 + b), num(a + b), num(a * 1000 + b)],
               "%d L = %d cL ; %d + %d = <b>%s cL</b>." % (a, a * 100, a * 100, b, num(a * 100 + b)))


def s3():
    k = R.choice(["kg", "kg", "L", "t"])
    if k == "kg":
        a = R.randint(1, 4)
        x = a * 1000
        y = R.choice([a * 100, x + R.choice([-200, 250, 500, -500]), a * 900, 800 * a])
        A, B = U(a, "kg"), U(y, "g")
    elif k == "t":
        a = R.randint(1, 5)
        x = a * 1000
        y = R.choice([a * 100, x + R.choice([-300, 400]), a * 800])
        A, B = U(a, "t"), U(y, "kg")
    else:
        a = R.randint(1, 3)
        x = a * 100
        y = R.choice([a * 10, x + R.choice([-25, 50, -50, 75]), a * 90])
        A, B = U(a, "L"), U(y, "cL")
    if y == x or y <= 0:
        return None
    big = A if x > y else B
    small = B if big == A else A
    return mcq("Lequel est le plus grand : %s ou %s ?" % (A, B), big, [small, "ils sont égaux", "on ne peut pas comparer"],
               "On convertit avant de comparer : %s = %s %s. Le plus grand est <b>%s</b>." % (A, num(x), B.split(NB)[-1], big))


def balance_svg(obj, weights):
    s = [line(150, 40, 150, 150, INK, 4), "<path d='M120 160 h60 l-10 -10 h-40 Z' fill='%s'/>" % INK, line(40, 40, 260, 40, INK, 4),
         line(40, 40, 40, 80, INK, 1.5), line(260, 40, 260, 80, INK, 1.5),
         "<path d='M0 80 h80 l-10 14 h-60 Z' fill='#dddddd' stroke='%s'/>" % INK, "<path d='M220 80 h80 l-10 14 h-60 Z' fill='#dddddd' stroke='%s'/>" % INK,
         "<rect x='14' y='44' width='52' height='36' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>" % (FILL, GREEN), text(40, 67, obj, 12)]
    x = 222
    for i, w in enumerate(weights):
        ww = 18 if w < 100 else 22 if w < 1000 else 28
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#b9b9b9' stroke='%s'/>" % (x, 80 - ww, ww, ww, INK))
        # étiquettes alternées au-dessus et au-dessous du plateau pour qu'elles ne se chevauchent pas
        s.append(text(x + ww / 2.0, 80 - ww - 4 if i % 2 == 0 else 108, ("%d kg" % (w // 1000) if w >= 1000 else "%d g" % w).replace(" ", NB), 10))
        x += ww + 3
    return wrap(max(304, x + 6), 168, "".join(s), "balance en équilibre", lg=True)


def s4_balance():
    obj = R.choice(["paquet", "colis", "melon", "sac", "potiron"])
    pool = [1000, 500, 200, 100, 50, 20, 10]
    ws = sorted(R.sample(pool, R.randint(2, 3)) + ([R.choice([500, 200, 100])] if R.random() < 0.3 else []), reverse=True)
    t = sum(ws)
    if len(ws) * 30 > 90:
        ws = ws[:3]
        t = sum(ws)
    right = U(t, "g") if t < 1000 else "%s" % U(t, "g")
    return mcq("<div class='qfig'>%s</div>La balance est en équilibre. Quelle est la masse du %s ?" % (balance_svg(obj, ws), obj), right,
               [U(len(ws), "g"), U(t - ws[-1], "g"), U(t + ws[-1], "g"), U(max(ws), "g")],
               "On additionne les masses marquées : %s = <b>%s</b>." % (" + ".join("%s g" % num(w) for w in ws), right))


def verre(level, top, step):
    """verre doseur gradué en cL"""
    H = 170
    s = ["<path d='M60 20 L60 190 Q60 200 70 200 L150 200 Q160 200 160 190 L160 20' fill='none' stroke='%s' stroke-width='2.5'/>" % INK]
    y = lambda v: 200 - v / float(top) * H
    s.append("<rect x='62' y='%.1f' width='96' height='%.1f' fill='#bcdcf5'/>" % (y(level), 198 - y(level)))
    for v in range(0, top + 1, step):
        big = v % (step * 2) == 0
        s.append(line(160, y(v), 160 - (18 if big else 10), y(v), INK, 1.6))
        if big:
            s.append(text(168, y(v) + 4, "%d cL" % v if v else "0", 12, anchor="start"))
    return wrap(230, 210, "".join(s), "verre doseur gradué en centilitres", lg=True)


def s4_verre():
    top, step = R.choice([(50, 5), (100, 10), (40, 5), (60, 10)])
    lv = step * R.randint(1, top // step - 1)
    return mcq("<div class='qfig'>%s</div>Quelle quantité d’eau y a-t-il dans le verre doseur ?" % verre(lv, top, step), "%d cL" % lv,
               ["%d cL" % (lv + step), "%d cL" % (lv - step) if lv > step else "%d cL" % (lv + 2 * step), "%d cL" % (lv // step), "%d L" % lv],
               "Chaque petite graduation vaut %d cL. L’eau arrive à <b>%d cL</b>." % (step, lv))


def s5():
    p = K.next()
    k = R.choice(["sac", "bouteilles", "panier", "camion", "verres", "confiture"])
    if k == "sac":
        a, b = R.randint(2, 6), R.choice([250, 300, 400, 500, 750])
        return mcq("%s porte un sac de %d kg et un paquet de %d g. Quelle masse porte-t-%s en tout ?" % (p[0], a, b, p[1]), "%s g" % num(a * 1000 + b), ["%s g" % num(a + b), "%s g" % num(a * 100 + b), "%s kg" % num(a + b)],
                   "%d kg = %s g ; %s + %d = <b>%s g</b>." % (a, num(a * 1000), num(a * 1000), b, num(a * 1000 + b)))
    if k == "bouteilles":
        n, c = R.randint(3, 8), R.choice([25, 33, 50, 75])
        return mcq("On remplit %d bouteilles de %d cL. Combien de centilitres faut-il ?" % (n, c), "%d cL" % (n * c), ["%d cL" % (n + c), "%d L" % (n * c), "%d cL" % (n * c + c)],
                   "%d %s %d = <b>%d cL</b>." % (n, FOIS, c, n * c))
    if k == "panier":
        a, b, c = R.choice([150, 200, 250]), R.choice([300, 400, 500]), R.choice([100, 120, 180])
        return mcq("Dans un panier, il y a une pomme de %d g, un melon de %d g et une poire de %d g. Quelle est la masse des fruits ?" % (a, b, c), "%d g" % (a + b + c), ["%d g" % (a + b), "%d kg" % (a + b + c), "%d g" % (a + b + c + 100)],
                   "%d + %d + %d = <b>%d g</b>." % (a, b, c, a + b + c))
    if k == "camion":
        t, l = R.randint(3, 9), R.randint(2, 6)
        return mcq("Un camion pèse %d t vide. On le charge avec %d t de sable. Combien pèse-t-il, en kilogrammes ?" % (t, l), "%s kg" % num((t + l) * 1000), ["%s kg" % num(t + l), "%s kg" % num((t + l) * 100), "%s kg" % num(t * 1000)],
                   "%d + %d = %d t = <b>%s kg</b>." % (t, l, t + l, num((t + l) * 1000)))
    if k == "verres":
        L_, v = R.choice([1, 2]), R.choice([20, 25])
        return mcq("Avec une bouteille de %d L, combien de verres de %d cL peut-on remplir ?" % (L_, v), (L_ * 100) // v, [L_ * 100 - v, v // L_ if v // L_ != (L_ * 100) // v else 3, (L_ * 10) // v if (L_ * 10) // v else 10],
                   "%d L = %d cL ; %d %s %d = <b>%d</b> verres." % (L_, L_ * 100, L_ * 100, "÷", v, (L_ * 100) // v))
    n, m = R.randint(3, 8), R.choice([250, 500, 400])
    return mcq("%s achète %d pots de confiture de %d g. Quelle masse de confiture achète-t-%s ?" % (p[0], n, m, p[1]), "%s g" % num(n * m), ["%s g" % num(n + m), "%s kg" % num(n * m), "%s g" % num(n * m + m)],
               "%d %s %d = <b>%s g</b>." % (n, FOIS, m, num(n * m)))


def main():
    seen = set()
    sets = [
        ("Choisir la bonne unité", mix(R, seen, [(s1_mass, 10), (s1_cap, 10)])),
        ("Convertir", mix(R, seen, [(s2, 20)])),
        ("Comparer", mix(R, seen, [(s3, 20)])),
        ("Lire une balance et un verre doseur", mix(R, seen, [(s4_balance, 10), (s4_verre, 10)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["La <b>masse</b> dit combien un objet est lourd : <b>1 t = 1 000 kg</b>, <b>1 kg = 1 000 g</b>.",
         "La <b>contenance</b> dit combien de liquide un récipient peut contenir : <b>1 L = 10 dL = 100 cL</b>, <b>1 dL = 10 cL</b>.",
         "Pour comparer ou calculer, on met les mesures <b>dans la même unité</b>.",
         "Sur une balance en équilibre, la masse de l’objet est égale à la somme des masses marquées."],
        [example("2 kg 300 g = … g", ["2 kg = 2 000 g", "2 000 + 300 = 2 300"], "2 300 g"),
         example("1 L = … verres de 25 cL", ["1 L = 100 cL", "100 ÷ 25 = 4"], "4 verres")],
        [["1 kg = 100 g", "1 kg = 1 000 g (kilo veut dire mille)."],
         ["Comparer 800 g et 2 kg : 800 &gt; 2", "2 kg = 2 000 g, donc 2 kg est plus lourd."],
         ["Lire une graduation sur deux", "Regarde combien vaut chaque petit trait avant de lire."]])
    faq = [("Quelle est la différence entre masse et contenance ?", "La masse se mesure en g, kg, t (avec une balance). La contenance se mesure en L, dL, cL (avec un verre doseur)."),
           ("Que veut dire « kilo » ?", "Kilo veut dire mille : 1 kilogramme = 1 000 grammes, 1 kilomètre = 1 000 mètres.")]
    make_unit(R, "masses-et-contenances", "G",
              "Comparer, estimer et mesurer des masses (g, kg, t) et des contenances (L, dL, cL) ; connaître les relations entre ces unités ; lire une balance et un récipient gradué ; résoudre des problèmes (résumé du programme 2024 du cycle 2).",
              "Masses et contenances", "Masses et contenances CE2 : fiches et exercices avec corrigé", "Masses et contenances",
              "Fiches de maths CE2 sur les masses (g, kg, t) et les contenances (L, dL, cL) : unités, conversions, comparaisons, balance, verre doseur et problèmes. 100 exercices corrigés.",
              "1 kg = 1 000 g ; 1 t = 1 000 kg.", "1 L = 10 dL = 100 cL.",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
