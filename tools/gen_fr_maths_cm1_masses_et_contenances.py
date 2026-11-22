# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Masses et contenances (Grandeurs et mesures)
  python3 tools/gen_fr_maths_cm1_masses_et_contenances.py
Masses du milligramme à la tonne (mg, cg, dg, g, dag, hg, kg, t), contenances du millilitre à l’hectolitre (mL, cL, dL, L, daL, hL) ;
choisir l’unité, convertir (CM2 : avec des décimaux), comparer, lire une balance, problèmes.
Erreurs : 1 kg = 100 g, 1 t = 100 kg, 1 L = 100 mL, comparer sans convertir.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, dz, table, NB
import gen_fr_maths_ce2_masses_et_contenances as CE

R = K = None
L = 1
UM = ["kg", "hg", "dag", "g", "dg", "cg", "mg"]
UC = ["hL", "daL", "L", "dL", "cL", "mL"]


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52117 + 100 * lv)
    K = Kids(R)
    CE.R = R


def M(v, u):
    return "%s%s%s" % (v, NB, u)


MASS = [("Un comprimé pèse environ", 500, "mg"), ("Un éléphant pèse environ", 5, "t"), ("Une fourmi pèse environ", 5, "mg"), ("Un camion pèse environ", 12, "t"),
        ("Un paquet de sucre pèse", 1, "kg"), ("Une pomme pèse environ", 150, "g"), ("Une plume pèse environ", 50, "mg"), ("Un cartable pèse environ", 4, "kg")]
CAP = [("Une piscine de jardin contient environ", 50, "hL"), ("Une cuillère à café contient environ", 5, "mL"), ("Une bouteille contient", 75, "cL"),
       ("Un seau contient environ", 10, "L"), ("Un flacon de sirop contient environ", 125, "mL"), ("Une citerne contient environ", 30, "hL")]


def s1():
    k = R.random()
    if k < 0.4:
        o, v, u = R.choice(MASS + CAP)
        pool = ["mg", "g", "kg", "t"] if (o, v, u) in MASS else ["mL", "cL", "L", "hL"]
        return mcq("Quelle unité convient ? %s %s …" % (o, num(v)), u, [x for x in pool if x != u], "%s %s <b>%s</b>." % (o, num(v), u))
    U_ = UM if R.random() < 0.6 else UC
    i, j = sorted(R.sample(range(len(U_)), 2))
    if j - i > 3:
        return None
    n = R.randint(2, 60)
    r = n * 10 ** (j - i)
    return mcq("Complète : %s = … %s" % (M(num(n), U_[i]), U_[j]), num(r), [num(n * 10 ** (j - i - 1)) if j - i > 1 else num(n * 100), num(r * 10), num(n + 10 ** (j - i))],
               "%s : chaque unité vaut 10 fois la suivante. On multiplie par %s : <b>%s %s</b>." % (" ; ".join(U_), num(10 ** (j - i)), num(r), U_[j]))


def s2():
    k = R.choice(["t_kg", "kg_g", "g_mg", "L_mL", "hL_L", "kgg"] + (["dec_kg", "dec_L", "g_kg"] if L == 2 else []))
    a = R.randint(2, 9)
    if k == "t_kg":
        return mcq("Complète : %s = … kg" % M(a, "t"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 t = 1 000 kg : <b>%s kg</b>." % num(a * 1000))
    if k == "kg_g":
        b = R.randint(1, 9) * 100 + R.choice([0, 50])
        return mcq("Complète : %s %s = … g" % (M(a, "kg"), M(b, "g")), num(a * 1000 + b), [num(a * 100 + b), num(a + b), num(a * 10000 + b)], "%d kg = %s g ; + %d = <b>%s g</b>." % (a, num(a * 1000), b, num(a * 1000 + b)))
    if k == "g_mg":
        return mcq("Complète : %s = … mg" % M(a, "g"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 g = 1 000 mg : <b>%s mg</b>." % num(a * 1000))
    if k == "L_mL":
        return mcq("Complète : %s = … mL" % M(a, "L"), num(a * 1000), [num(a * 100), num(a * 10), num(a * 10000)], "1 L = 1 000 mL : <b>%s mL</b>." % num(a * 1000))
    if k == "hL_L":
        return mcq("Complète : %s = … L" % M(a, "hL"), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 hL = 100 L : <b>%s L</b>." % num(a * 100))
    if k == "kgg":
        n = R.randint(1050, 9950)
        if n % 1000 == 0:
            return None
        return mcq("Complète : %s = … kg … g" % M(num(n), "g"), "%s %s" % (M(n // 1000, "kg"), M(n % 1000, "g")), ["%s %s" % (M(n // 100, "kg"), M(n % 100, "g")), "%s %s" % (M(n // 10, "kg"), M(n % 10, "g")), "%s %s" % (M(n // 1000 + 1, "kg"), M(n % 1000, "g"))],
                   "1 000 g = 1 kg : <b>%d kg %d g</b>." % (n // 1000, n % 1000))
    if k == "dec_kg":
        n = R.randint(1005, 9995)
        return mcq("Complète : %s = … g" % M(dz(n, 3), "kg"), num(n), [num(n // 10) if n % 10 == 0 else dz(n, 1), num(n * 10), num(n // 100)], "1 kg = 1 000 g : %s kg = <b>%s g</b>." % (dz(n, 3), num(n)))
    if k == "dec_L":
        n = R.randint(105, 995)
        return mcq("Complète : %s = … cL" % M(dz(n, 2), "L"), num(n), [num(n * 10), dz(n, 1), num(n // 10)], "1 L = 100 cL : %s L = <b>%s cL</b>." % (dz(n, 2), num(n)))
    n = R.randint(105, 9950)
    return mcq("Complète : %s = … kg" % M(num(n), "g"), M(dz(n, 3), "kg"), [M(dz(n, 2), "kg"), M(num(n * 1000), "kg"), M(dz(n, 1), "kg")], "1 000 g = 1 kg : <b>%s kg</b>." % dz(n, 3))


def s3():
    k = R.choice(["kg", "L", "t"])
    if k == "kg":
        a = R.randint(1, 4)
        y = R.choice([a * 100, a * 1000 + R.choice([-200, 250, 500]), a * 900])
        A, B, x = M(a, "kg"), M(num(y), "g"), a * 1000
    elif k == "t":
        a = R.randint(1, 5)
        y = R.choice([a * 100, a * 1000 + R.choice([-300, 400]), a * 800])
        A, B, x = M(a, "t"), M(num(y), "kg"), a * 1000
    else:
        a = R.randint(1, 3)
        y = R.choice([a * 100, a * 1000 + R.choice([-250, 500]), a * 900])
        A, B, x = M(a, "L"), M(num(y), "mL"), a * 1000
    if y == x:
        return None
    big = A if x > y else B
    return mcq("Lequel est le plus grand : %s ou %s ?" % (A, B), big, [B if big == A else A, "ils sont égaux", "on ne peut pas comparer"],
               "%s = %s. Le plus grand est <b>%s</b>." % (A, M(num(x), B.split(NB)[-1]), big))


def s4():
    it = CE.s4_balance() if R.random() < 0.6 else CE.s4_verre()
    if not it:
        return None
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])


def s5():
    p = K.next()
    k = R.choice(["med", "camion", "bouteilles", "recette", "aquarium"])
    if k == "med":
        n, d = R.randint(2, 3), R.choice([250, 500])
        j = R.randint(5, 10)
        return mcq("%s prend %d comprimés de %d mg par jour pendant %d jours. Quelle masse de médicament en tout, en grammes ?" % (p[0], n, d, j), M(dz(n * d * j, 3), "g"), [M(num(n * d * j), "g"), M(dz(n * d * j, 2), "g"), M(dz(n * d, 3), "g")],
                   "%d %s %d %s %d = %s mg = <b>%s g</b>." % (n, FOIS, d, FOIS, j, num(n * d * j), dz(n * d * j, 3)))
    if k == "camion":
        c, s = R.randint(8, 20), R.randint(25, 60)
        return mcq("Un camion peut porter %d t. Combien de sacs de %d kg peut-il porter au plus ?" % (c, s), num(c * 1000 // s), [num(c * 100 // s), num(c * 1000 // s + 1), num(c * 1000 - s)],
                   "%d t = %s kg ; %s %s %d = %d reste %d : <b>%s sacs</b>." % (c, num(c * 1000), num(c * 1000), DIV, s, c * 1000 // s, c * 1000 % s, num(c * 1000 // s)))
    if k == "bouteilles":
        n, c = R.randint(4, 12), R.choice([25, 33, 50, 75])
        return mcq("On remplit %d bouteilles de %d cL. Combien de litres faut-il ?" % (n, c), M(dz(n * c, 2), "L"), [M(num(n * c), "L"), M(dz(n * c, 1), "L"), M(dz(n * c, 3), "L")],
                   "%d %s %d = %d cL = <b>%s L</b>." % (n, FOIS, c, n * c, dz(n * c, 2)))
    if k == "recette":
        a, b, c = R.choice([250, 300, 125]), R.choice([150, 200, 100]), R.choice([4, 6])
        return mcq("Une recette demande %d g de farine, %d g de sucre et %d œufs de 50 g. Quelle est la masse totale, en kilogrammes ?" % (a, b, c), M(dz(a + b + 50 * c, 3), "kg"), [M(num(a + b + 50 * c), "kg"), M(dz(a + b + c, 3), "kg"), M(dz(a + b, 3), "kg")],
                   "%d + %d + %d %s 50 = %d g = <b>%s kg</b>." % (a, b, c, FOIS, a + b + 50 * c, dz(a + b + 50 * c, 3)))
    a = R.randint(2, 9)
    return mcq("Un aquarium contient %s. On le vide avec un seau de 10 L. Combien de seaux faut-il ?" % M(a, "hL"), num(a * 10), [num(a), num(a * 100), num(a * 10 + 1)],
               "%d hL = %d L ; %d %s 10 = <b>%d</b> seaux." % (a, a * 100, a * 100, DIV, a * 10))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Unités de masse et de contenance", mix(R, seen, [(s1, 20)])),
        ("Convertir" + ("" if lv == 1 else " avec des décimaux"), mix(R, seen, [(s2, 20)])),
        ("Comparer", mix(R, seen, [(s3, 20)])),
        ("Balance et verre doseur", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Masses : <b>t, kg, hg, dag, g, dg, cg, mg</b>. 1 t = 1 000 kg ; 1 kg = 1 000 g ; 1 g = 1 000 mg.",
         "Contenances : <b>hL, daL, L, dL, cL, mL</b>. 1 hL = 100 L ; 1 L = 100 cL = 1 000 mL.",
         "Comme pour les longueurs, chaque unité vaut 10 fois l’unité à sa droite.",
         "Pour comparer ou calculer, on convertit dans la même unité."],
        [example("2,5 kg en g", ["1 kg = 1 000 g", "2,5 %s 1 000" % FOIS], "2 500 g")],
        [["1 kg = 100 g", "Kilo veut dire mille : 1 kg = 1 000 g."],
         ["1 L = 100 mL", "1 L = 100 cL = 1 000 mL."],
         ["Comparer 800 g et 2 kg : 800 &gt; 2", "2 kg = 2 000 g : c’est plus lourd."]],
        table(["kg", "hg", "dag", "g", "dg", "cg", "mg"], [["2", "5", "0", "0", "", "", ""]]))
    faq = [("Pourquoi le milligramme ?", "Pour les très petites masses : médicaments, insectes. 1 g = 1 000 mg."),
           ("Qu’est-ce que l’hectolitre ?", "1 hL = 100 L. On l’utilise pour les grandes quantités : citernes, piscines, récoltes de vin.")]
    unit(lv, R, "masses-et-contenances", "G",
         "Connaître et utiliser les unités de masse du milligramme au kilogramme et à la tonne, et les unités de contenance du millilitre à l’hectolitre ; choisir une unité adaptée ; comparer et estimer ; résoudre des problèmes",
         "Masses et contenances", "Masses et contenances",
         "Fiches de maths %s sur les masses (mg, g, kg, t) et les contenances (mL, cL, L, hL) : unités, conversions, comparaisons, balance et problèmes. 100 exercices corrigés." % GN(lv),
         "1 kg = 1 000 g ; 1 g = 1 000 mg ; 1 t = 1 000 kg.", "1 L = 100 cL = 1 000 mL ; 1 hL = 100 L.",
         body, faq, sets, 17)


if __name__ == "__main__":
    build(1)
