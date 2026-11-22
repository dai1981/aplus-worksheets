# -*- coding: utf-8 -*-
"""
France Maths CP : Les longueurs ; CE1 (build(1)) : Longueurs et périmètres
  python3 tools/gen_fr_maths_cp_longueurs.py
CP : comparer, mesurer en cm avec la règle, cm et m (1 m = 100 cm). CE1 : m, cm, km (1 km = 1 000 m), mesurer, périmètre.
Erreurs : mesurer à partir de 1 au lieu de 0, croire que 80 cm &gt; 1 m car 80 &gt; 1, oublier un côté du périmètre.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, NB, FOIS
import k_pics as KP
import gen_fr_maths_ce2_longueurs_et_perimetres as LP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53010 + 100 * lv)
    K = Kids(R)
    LP.R = R
    LP.K = K


def U(v, u):
    return "%s%s%s" % (num(v), NB, u)


def s1():
    n = R.randint(3, 4)
    ls = R.sample(range(3, 11), n)
    long = R.random() < 0.6
    v = max(ls) if long else min(ls)
    i = ls.index(v)
    lab = "ABCD"[:n]
    if L == 0 and R.random() < 0.3:
        offs = [R.randint(0, 2) for _ in range(n)]
        svg = pic(KP.pencils_svg(ls, offsets=offs), "%d crayons de longueurs différentes, décalés" % n, lg=True)
        e = "Les crayons ne commencent pas au même endroit : on compare de la pointe au bout. Le plus %s est <b>%s</b>." % ("long" if long else "court", lab[i])
    else:
        svg = pic(KP.pencils_svg(ls), "%d crayons de longueurs différentes" % n, lg=True)
        e = "Les crayons sont alignés à gauche : le plus %s est <b>%s</b>." % ("long" if long else "court", lab[i])
        offs = None
    if offs:
        e = "On regarde la longueur de chaque crayon, pas où il s’arrête. Le plus %s est <b>%s</b>." % ("long" if long else "court", lab[i])
    return mcq("<div class='qfig'>%s</div>Quel crayon est le plus %s ?" % (svg, "long" if long else "court"), "le crayon %s" % lab[i], ["le crayon %s" % lab[j] for j in range(n) if j != i] + ["ils sont tous pareils"],
               e)


def s2():
    a = 0 if R.random() < 0.4 else R.choice([10, 20, 30])
    ln = R.randint(2, 11)
    b = a + 10 * ln
    if b > 140:
        return None
    right = "%d cm" % ln
    wr = ["%d cm" % (b // 10), "%d cm" % (ln + 1), "%d cm" % (ln - 1)]
    e = ("Le segment commence à 0 : il mesure <b>%d cm</b>." % ln) if a == 0 else ("Le segment va de %d à %d : %d − %d = <b>%d cm</b>." % (a // 10, b // 10, b // 10, a // 10, ln))
    return mcq("<div class='qfig'>%s</div>Combien mesure le segment rouge ?" % LP.regle(a, b), right, [w for w in wr if w != right], e)


OBJ_CP = [("Un crayon", 15, "cm"), ("Une gomme", 4, "cm"), ("La porte de la classe", 2, "m"), ("Un autobus", 12, "m"), ("Un livre", 24, "cm"),
          ("Une baguette de pain", 65, "cm"), ("Un lit", 2, "m"), ("Une règle", 20, "cm"), ("La cour de l’école", 40, "m"), ("Une cuillère", 15, "cm"),
          ("Un cahier", 30, "cm"), ("Une piscine", 25, "m"), ("Une fourchette", 18, "cm"), ("La façade de l’école", 30, "m"), ("Un pinceau", 20, "cm"),
          ("Un arbre", 10, "m"), ("Une chaussure", 20, "cm"), ("Un train", 200, "m"), ("Un doigt", 6, "cm"), ("Une voiture", 4, "m")]
OBJ_CE1 = OBJ_CP + [("Le trajet de Paris à Lyon", 465, "km"), ("Une étape du Tour de France", 160, "km"), ("Un marathon", 42, "km"), ("La Seine", 777, "km"),
                    ("Le trajet en vélo jusqu’au village voisin", 5, "km"), ("Une piste d’athlétisme", 400, "m")]


def s3():
    o, v, u = R.choice(OBJ_CP if L == 0 else OBJ_CE1)
    opts = ["cm", "m"] + (["kg", "L"] if L == 0 else ["km", "kg"])
    return mcq("%s mesure environ %s … Quelle unité convient ?" % (o, num(v)), u, [x for x in opts if x != u],
               "%s mesure environ %s <b>%s</b>." % (o, num(v), u))


def s4():
    if L == 0:
        k = R.choice(["cmp", "conv", "conv2"])
        if k == "cmp":
            c = R.choice([50, 60, 70, 80, 90, 99, 120, 150, 110, 200])
            ans = "1 m" if c < 100 else "%d cm" % c
            return mcq("Quel est le plus long : 1 m ou %d cm ?" % c, ans, ["%d cm" % c if c < 100 else "1 m", "c’est pareil", "on ne peut pas savoir"],
                       "1 m = 100 cm. %d cm %s 100 cm, donc <b>%s</b> est le plus long." % (c, "&lt;" if c < 100 else "&gt;", ans))
        if k == "conv":
            m = R.randint(1, 5)
            return mcq("%s = … cm" % pl(m, "mètre"), "%d cm" % (100 * m), ["%d cm" % (10 * m), "%d cm" % m, "%d cm" % (1000 * m)], "1 m = 100 cm, donc %d m = <b>%d cm</b>." % (m, 100 * m))
        c = R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90])
        return mcq("Combien de centimètres faut-il ajouter à %d cm pour faire 1 m ?" % c, "%d cm" % (100 - c), ["%d cm" % (10 - c // 10), "%d cm" % (100 + c), "%d cm" % c if c != 50 else "40 cm"],
                   "1 m = 100 cm : %d + <b>%d</b> = 100." % (c, 100 - c))
    k = R.choice(["m", "km", "mc", "cmp", "cmp2"])
    if k == "m":
        m = R.randint(2, 9)
        return mcq("%d m = … cm" % m, "%d cm" % (100 * m), ["%d cm" % (10 * m), "%s cm" % num(1000 * m), "%d cm" % m], "1 m = 100 cm, donc %d m = <b>%d cm</b>." % (m, 100 * m))
    if k == "km":
        km = R.randint(1, 9)
        return mcq("%d km = … m" % km, "%s m" % num(1000 * km), ["%d m" % (100 * km), "%d m" % (10 * km), "%s m" % num(10000 * km)], "1 km = 1 000 m, donc %d km = <b>%s m</b>." % (km, num(1000 * km)))
    if k == "mc":
        m, c = R.randint(1, 4), R.randint(5, 95)
        return mcq("%d m %d cm = … cm" % (m, c), "%d cm" % (100 * m + c), ["%d cm" % (10 * m + c), "%d cm" % (m + c), "%d cm" % (100 * m + c + 100)],
                   "%d m = %d cm ; %d + %d = <b>%d cm</b>." % (m, 100 * m, 100 * m, c, 100 * m + c))
    if k == "cmp":
        c = R.randint(110, 390)
        m = R.randint(1, 3)
        ans = "%d cm" % c if c > 100 * m else "%d m" % m
        return mcq("Quel est le plus long : %d m ou %d cm ?" % (m, c), ans, ["%d m" % m if ans.endswith("cm") else "%d cm" % c, "c’est pareil", "on ne peut pas savoir"],
                   "%d m = %d cm. %d cm %s %d cm : <b>%s</b>." % (m, 100 * m, c, "&gt;" if c > 100 * m else "&lt;", 100 * m, ans))
    m = R.choice([500, 800, 900, 1200, 1500, 2000, 700, 1100])
    ans = "%s m" % num(m) if m > 1000 else "1 km"
    return mcq("Quel est le plus long : 1 km ou %s m ?" % num(m), ans, ["1 km" if m > 1000 else "%s m" % num(m), "c’est pareil", "on ne peut pas savoir"],
               "1 km = 1 000 m : <b>%s</b> est le plus long." % ans)


def s5():
    p = K.next()
    if L == 1 and R.random() < 0.45:
        k = R.choice(["poly", "rect", "carre"])
        LP.U_[0] = "cm"
        if k == "poly":
            n = R.choice([3, 4, 5])
            sides = [R.randint(2, 12) for _ in range(n)]
            P = sum(sides)
            return mcq("<div class='qfig'>%s</div>Quel est le périmètre de cette figure ?" % LP.poly_svg("poly", sides), LP.unitf(P), [LP.unitf(P - sides[0]), LP.unitf(P + sides[0]), LP.unitf(P + 10)],
                       "Le périmètre, c’est la longueur du tour : %s = <b>%s</b>." % (" + ".join(map(str, sides)), LP.unitf(P)))
        if k == "rect":
            a, b = R.randint(5, 15), R.randint(2, 9)
            if a <= b:
                return None
            P = 2 * (a + b)
            return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce rectangle ?" % LP.poly_svg("rect", (a, b)), LP.unitf(P), [LP.unitf(a + b), LP.unitf(2 * a + b), LP.unitf(P + 2)],
                       "On fait le tour : %d + %d + %d + %d = <b>%s</b>." % (a, b, a, b, LP.unitf(P)))
        c = R.randint(2, 15)
        return mcq("<div class='qfig'>%s</div>Quel est le périmètre de ce carré ?" % LP.poly_svg("carre", (c, c)), LP.unitf(4 * c), [LP.unitf(2 * c), LP.unitf(3 * c), LP.unitf(4 * c + 4)],
                   "4 côtés égaux : %s = <b>%s</b>." % (" + ".join([str(c)] * 4), LP.unitf(4 * c)))
    k = R.choice(["bout", "coupe", "saut", "ruban"])
    if k == "bout":
        a, b = (R.randint(10, 40), R.randint(10, 40)) if L == 0 else (R.randint(35, 85), R.randint(35, 85))
        if a == b:
            return None
        return mcq("%s met bout à bout un ruban rouge de %d cm et un ruban bleu de %d cm. Quelle longueur obtient-%s ?" % (p[0], a, b, p[1]), "%d cm" % (a + b), ["%d cm" % abs(a - b), "%d cm" % (a + b + 10), "%d m" % (a + b)],
                   "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if k == "coupe":
        if L == 0:
            a, b = 100, R.choice([20, 30, 40, 50, 60])
            return mcq("%s a une ficelle de 1 m. %s en coupe %d cm. Quelle longueur reste-t-il ?" % (p[0], p[1].capitalize(), b), "%d cm" % (a - b), ["%d cm" % (b - 1 if b > 1 else 1), "%d cm" % (100 + b), "%d cm" % (10 - b // 10)],
                       "1 m = 100 cm ; 100 − %d = <b>%d cm</b>." % (b, a - b))
        a, b = R.randint(2, 5), R.randint(15, 85)
        return mcq("%s a une corde de %d m. %s en coupe %d cm. Quelle longueur reste-t-il ?" % (p[0], a, p[1].capitalize(), b), "%d cm" % (100 * a - b), ["%d cm" % (100 * a + b), "%d cm" % (10 * a - b) if 10 * a > b else "%d cm" % (100 * a - b + 10), "%d m" % (a - 1)],
                   "%d m = %d cm ; %d − %d = <b>%d cm</b>." % (a, 100 * a, 100 * a, b, 100 * a - b))
    if k == "saut":
        a, b = (R.randint(60, 120), R.randint(5, 30)) if L == 0 else (R.randint(150, 280), R.randint(10, 60))
        q = K.next()
        return mcq("%s saute %d cm. %s saute %d cm de plus. Combien saute %s ?" % (p[0], a, q[0], b, q[0]), "%d cm" % (a + b), ["%d cm" % (a - b), "%d cm" % b, "%d cm" % (a + b + 10)],
                   "%d + %d = <b>%d cm</b>." % (a, b, a + b))
    if L == 0:
        n, l = R.randint(2, 4), R.choice([5, 10, 20])
        return mcq("%s colle %d bandes de %d cm bout à bout. Quelle longueur obtient-%s ?" % (p[0], n, l, p[1]), "%d cm" % (n * l), ["%d cm" % (n + l), "%d cm" % (n * l + l), "%d cm" % l],
                   "%s = <b>%d cm</b>." % (" + ".join([str(l)] * n), n * l))
    km, m = R.randint(1, 3), R.choice([200, 300, 400, 500, 600, 800])
    return mcq("%s court %d km le matin et %d m le soir. Combien de mètres en tout ?" % (p[0], km, m), "%s m" % num(1000 * km + m), ["%d m" % (km + m), "%s m" % num(100 * km + m), "%s m" % num(1000 * km + m + 100)],
               "%d km = %s m ; %s + %d = <b>%s m</b>." % (km, num(1000 * km), num(1000 * km), m, num(1000 * km + m)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Comparer des longueurs", mix(R, seen, [(s1, 20)])),
        ("Mesurer avec la règle", mix(R, seen, [(s2, 20)])),
        ("Choisir la bonne unité", mix(R, seen, [(s3, 20)])),
        ("Mètres et centimètres" if lv == 0 else "Convertir et comparer", mix(R, seen, [(s4, 20)])),
        ("Problèmes" if lv == 0 else "Périmètres et problèmes", mix(R, seen, [(s5, 20)])),
    ]
    th = ["Pour comparer deux longueurs, on les aligne au même point de départ.",
          "Pour mesurer avec une règle, on place le <b>0</b> au début de l’objet.",
          "1 mètre (m) = 100 centimètres (cm)." if lv == 0 else "1 m = 100 cm ; 1 km = 1 000 m. Le <b>périmètre</b> est la longueur du tour d’une figure."]
    body = lesson(th, [example("1 m ou 80 cm ?", ["1 m = 100 cm", "100 &gt; 80"], "1 m est plus long")],
                  [["Mesurer à partir de 1", "On part du 0 de la règle."],
                   ["Croire que 80 cm &gt; 1 m car 80 &gt; 1", "On compare dans la même unité : 1 m = 100 cm."],
                   ["Oublier un côté du périmètre" if lv else "Comparer sans aligner", "On ajoute la longueur de <b>tous</b> les côtés." if lv else "On place les objets au même point de départ."]])
    faq = [("Quelle unité choisir ?", "Le centimètre pour les petits objets, le mètre pour une pièce ou un bus%s." % ("" if lv == 0 else ", le kilomètre pour un trajet")),
           ("Combien de centimètres dans un mètre ?", "100 centimètres.")]
    unit(lv, R, "longueurs" if lv == 0 else "longueurs-et-perimetres", "G",
         ("Comparer des longueurs ; mesurer des segments en centimètres avec une règle ; connaître le mètre et le centimètre et la relation 1 m = 100 cm ; résoudre des problèmes de longueurs" if lv == 0 else
          "Mesurer des longueurs avec une règle ; connaître le mètre, le centimètre et le kilomètre (1 m = 100 cm, 1 km = 1 000 m) ; calculer le périmètre d’un polygone ; résoudre des problèmes de longueurs"),
         "Les longueurs" if lv == 0 else "Longueurs et périmètres", "Longueurs" if lv == 0 else "Longueurs et périmètres",
         ("Fiches de maths CP sur les longueurs : comparer, mesurer avec la règle, choisir l’unité, mètres et centimètres et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur les longueurs : comparer, mesurer, unités m, cm, km, convertir, périmètre et problèmes. 100 exercices corrigés."),
         "1 m = 100 cm" if lv == 0 else "1 km = 1 000 m ; 1 m = 100 cm", "On mesure à partir du 0 de la règle.", body, faq, sets, 10)


if __name__ == "__main__":
    build(0)
