# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Calcul mental
  python3 tools/gen_fr_maths_cp_calcul_mental.py
CP : + 1, + 2, − 1, − 2, ± 10, + 9, dizaines entières. CE1 : ± dizaines, ± centaines, + 9 / + 19 / + 29, − 9, × 10.
Erreurs : 45 + 10 = 46 (ajouter aux unités), 37 + 9 = 47 (oublier d’enlever 1), 34 + 20 = 36.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, FOIS
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53005 + 100 * lv)
    K = Kids(R)


def wr(v, *xs):
    return [num(x) for x in xs if x >= 0 and x != v]


def s1():
    if L == 0:
        n = R.randint(3, 97)
        d = R.choice([1, 2, -1, -2])
        v = n + d
        if not 0 <= v <= 100:
            return None
        return mcq("%d %s %d = …" % (n, "+" if d > 0 else "−", abs(d)), str(v), wr(v, n - d, v + (1 if d > 0 else -1), v + 10 * (1 if d > 0 else -1)),
                   "%s %d : <b>%d</b>." % ("J’avance de" if d > 0 else "Je recule de", abs(d), v))
    n = R.randint(12, 899)
    d = R.choice([10, 20, 30, 40, 50, -10, -20, -30])
    v = n + d
    if not 0 < v < 1000 or (n % 10 == 0):
        return None
    return mcq("%s %s %d = …" % (num(n), "+" if d > 0 else "−", abs(d)), num(v), wr(v, n + d // 10, n - d, v + 100 if d > 0 else v - 100),
               "On %s %s au chiffre des dizaines : <b>%s</b>." % ("ajoute" if d > 0 else "enlève", pl(abs(d) // 10, "dizaine"), num(v)))


def s2():
    if L == 0:
        n = R.randint(1, 89)
        d = R.choice([10, -10])
        v = n + d
        if not 0 <= v <= 99:
            return None
        if R.random() < 0.3:
            svg = pic(KP.rods_svg(n // 10, n % 10), "%s et %s" % (pl(n // 10, "barre"), pl(n % 10, "cube")))
            q = "<div class='qfig'>%s</div>Voici %d. Combien font %d %s 10 ?" % (svg, n, n, "+" if d > 0 else "−")
        else:
            q = "%d %s 10 = …" % (n, "+" if d > 0 else "−")
        return mcq(q, str(v), wr(v, n + (1 if d > 0 else -1), n - d, v + d), "On %s 1 dizaine, les unités ne changent pas : <b>%d</b>." % ("ajoute" if d > 0 else "enlève", v))
    n = R.randint(105, 899)
    d = R.choice([100, 200, 300, -100, -200])
    v = n + d
    if not 0 < v < 1000:
        return None
    return mcq("%s %s %d = …" % (num(n), "+" if d > 0 else "−", abs(d)), num(v), wr(v, n + d // 10, n + d // 100, n - d),
               "On change seulement le chiffre des centaines : <b>%s</b>." % num(v))


def s3():
    if L == 0:
        n = R.randint(3, 80)
        if n % 10 == 0:
            return None
        return mcq("%d + 9 = …" % n, str(n + 9), wr(n + 9, n + 10, n + 8, n + 19), "%d + 10 = %d, puis on enlève 1 : <b>%d</b>." % (n, n + 10, n + 9))
    k = R.choice([9, 19, 29, -9, -19])
    n = R.randint(21, 960)
    v = n + k
    if not 0 < v < 1000:
        return None
    r = (abs(k) + 1)
    return mcq("%s %s %d = …" % (num(n), "+" if k > 0 else "−", abs(k)), num(v), wr(v, n + (r if k > 0 else -r), n + (k - 2 if k > 0 else k + 2), v + (10 if k > 0 else -10)),
               "%s %s %d = %s, puis on %s 1 : <b>%s</b>." % (num(n), "+" if k > 0 else "−", r, num(n + (r if k > 0 else -r)), "enlève" if k > 0 else "ajoute", num(v)))


def s4():
    if L == 0:
        a, b = R.randint(1, 9), R.randint(1, 9)
        if R.random() < 0.6:
            if a + b > 10:
                return None
            return mcq("%d + %d = …" % (10 * a, 10 * b), str(10 * (a + b)), wr(10 * (a + b), a + b, 10 * (a + b) + 10, 10 * a + b),
                       "%s + %s = %s : <b>%d</b>." % (pl(a, "dizaine"), pl(b, "dizaine"), pl(a + b, "dizaine"), 10 * (a + b)))
        if a <= b:
            return None
        u = R.randint(0, 9)
        if R.random() < 0.5 or u == 0:
            return mcq("%d − %d = …" % (10 * a, 10 * b), str(10 * (a - b)), wr(10 * (a - b), a - b, 10 * (a + b), 10 * (a - b) + 10),
                       "%s − %s = %s : <b>%d</b>." % (pl(a, "dizaine"), pl(b, "dizaine"), pl(a - b, "dizaine"), 10 * (a - b)))
        return mcq("%d + %d = …" % (10 * a, u), str(10 * a + u), wr(10 * a + u, a + u, 10 * u + a, 10 * a + u + 10), "%d dizaines et %s : <b>%d</b>." % (a, pl(u, "unité"), 10 * a + u))
    if R.random() < 0.5:
        n = R.randint(2, 99)
        return mcq("%d %s 10 = …" % (n, FOIS), num(10 * n), wr(10 * n, n + 10, 100 * n, n * 10 + 1), "Multiplier par 10 : chaque unité devient une dizaine, on écrit un 0 à droite : <b>%s</b>." % num(10 * n))
    a, b = R.randint(11, 19), R.randint(2, 9)
    return mcq("%d %s %d = …" % (a, FOIS, b), str(a * b), wr(a * b, 10 * b + a % 10 + b, 10 * b + (a % 10), a * b + b),
               "%d %s %d = 10 %s %d + %d %s %d = %d + %d = <b>%d</b>." % (a, FOIS, b, FOIS, b, a % 10, FOIS, b, 10 * b, (a % 10) * b, a * b))


def s5():
    p = K.next()
    k = R.choice(["plus10", "moins", "plus9", "dz"])
    if L == 0:
        if k == "plus10":
            n = R.randint(5, 85)
            return mcq("%s a %d images. %s en gagne 10. Combien en a-t-%s ?" % (p[0], n, p[1].capitalize(), p[1]), str(n + 10), wr(n + 10, n + 1, n + 20, n),
                       "%d + 10 = <b>%d</b>." % (n, n + 10))
        if k == "moins":
            n = R.randint(12, 60)
            d = R.choice([1, 2, 10])
            return mcq("Il y a %d enfants dans la cour. %s rentre%s. Combien d’enfants restent dans la cour ?" % (n, "1 enfant" if d == 1 else "%d enfants" % d, "" if d == 1 else "nt"), str(n - d),
                       wr(n - d, n + d, n - d - 1, n - 10 * d if d < 10 else n - 1), "%d − %d = <b>%d</b>." % (n, d, n - d))
        if k == "plus9":
            n = R.randint(10, 60)
            return mcq("%s a %d €. Sa mamie lui donne 9 €. Combien a-t-%s ?" % (p[0], n, p[1]), "%d €" % (n + 9), ["%d €" % x for x in (n + 10, n + 8, n + 19)],
                       "%d + 10 − 1 = <b>%d €</b>." % (n, n + 9))
        a, b = R.randint(2, 6), R.randint(1, 3)
        return mcq("Le maître a %d paquets de 10 crayons. Il en achète encore %s. Combien de crayons a-t-il ?" % (a, pl(b, "paquet")), str(10 * (a + b)), wr(10 * (a + b), a + b, 10 * a + b, 10 * (a + b) + 10),
                   "%d paquets de 10 = %d crayons : <b>%d</b>." % (a + b, 10 * (a + b), 10 * (a + b)))
    if k == "plus10":
        n = R.randint(120, 780)
        d = R.choice([100, 200, 30, 40])
        return mcq("Un album a %s images. %s en colle encore %d. Combien d’images y a-t-il ?" % (num(n), p[0], d), num(n + d), wr(n + d, n + d // 10, n + 10 * d if 10 * d < 1000 else n + d + 10, n + d + 100),
                   "%s + %d = <b>%s</b>." % (num(n), d, num(n + d)))
    if k == "moins":
        n = R.randint(210, 900)
        d = R.choice([100, 200, 20, 30])
        return mcq("Un magasin a %s ballons. Il en vend %d. Combien en reste-t-il ?" % (num(n), d), num(n - d), wr(n - d, n + d, n - d // 10, n - d - 100 if n - d > 100 else n - d + 1),
                   "%s − %d = <b>%s</b>." % (num(n), d, num(n - d)))
    if k == "plus9":
        n = R.randint(30, 300)
        k2 = R.choice([9, 19, 29])
        return mcq("%s a %d €. %s gagne %d €. Combien a-t-%s ?" % (p[0], n, p[1].capitalize(), k2, p[1]), "%s €" % num(n + k2), ["%s €" % num(x) for x in (n + k2 + 1, n + k2 - 1, n + k2 + 10)],
                   "%d + %d − 1 = <b>%s €</b>." % (n, k2 + 1, num(n + k2)))
    n = R.randint(3, 60)
    return mcq("Une boîte contient 10 gâteaux. Combien de gâteaux dans %d boîtes ?" % n, num(10 * n), wr(10 * n, n + 10, 100 * n, 10 * n + 10),
               "%d %s 10 = <b>%s</b>." % (n, FOIS, num(10 * n)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Ajouter ou enlever 1 ou 2" if lv == 0 else "Ajouter ou enlever des dizaines", mix(R, seen, [(s1, 20)])),
        ("Ajouter ou enlever 10" if lv == 0 else "Ajouter ou enlever des centaines", mix(R, seen, [(s2, 20)])),
        ("Ajouter 9" if lv == 0 else "Ajouter 9, 19, 29, enlever 9", mix(R, seen, [(s3, 20)])),
        ("Calculer avec les dizaines" if lv == 0 else "Multiplier par 10, décomposer", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    if lv == 0:
        th = ["+ 1, c’est le nombre qui vient juste après ; − 1, celui juste avant.",
              "+ 10 : le chiffre des dizaines augmente de 1, les unités ne changent pas (34 + 10 = 44).",
              "+ 9, c’est + 10 puis − 1 (27 + 9 = 37 − 1 = 36)."]
        ex = example("27 + 9", ["27 + 10 = 37", "37 − 1 = 36"], "36")
    else:
        th = ["+ 30 : le chiffre des dizaines augmente de 3 (245 + 30 = 275).",
              "+ 19, c’est + 20 puis − 1 ; − 9, c’est − 10 puis + 1.",
              "× 10 : on écrit un 0 à droite (23 × 10 = 230). 13 × 7 = 10 × 7 + 3 × 7."]
        ex = example("346 + 19", ["346 + 20 = 366", "366 − 1 = 365"], "365")
    body = lesson(th, [ex], [["Ajouter 10 aux unités : 45 + 10 = 46" if lv == 0 else "Ajouter 30 aux unités : 245 + 30 = 248", "On ajoute aux dizaines : 55." if lv == 0 else "On ajoute 3 dizaines : 275."],
                             ["Oublier d’enlever 1 : 37 + 9 = 47", "37 + 10 = 47, puis 47 − 1 = 46."],
                             ["Pour − 9, enlever 1 au lieu d’ajouter 1" if lv else "Confondre + 1 et + 10", "52 − 9 = 52 − 10 + 1 = 43." if lv else "34 + 1 = 35 ; 34 + 10 = 44."]])
    faq = [("Pourquoi faire du calcul mental ?", "Pour calculer vite sans poser l’opération, et pour vérifier un résultat."),
           ("Comment ajouter 9 facilement ?", "On ajoute 10, puis on enlève 1.")]
    unit(lv, R, "calcul-mental", "N",
         ("Calculer mentalement : ajouter ou retrancher 1, 2 et 10 ; ajouter 9 ; ajouter et soustraire des dizaines entières ; compléter à la dizaine supérieure" if lv == 0 else
          "Calculer mentalement : ajouter ou soustraire des dizaines ou des centaines entières ; ajouter 9, 19, 29 ; soustraire 9 ; multiplier par 10 ; calculer des produits comme 13 × 7 en décomposant"),
         "Calcul mental", "Calcul mental",
         ("Fiches de calcul mental CP : + 1, + 2, + 10, − 10, + 9 et dizaines entières, avec des problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de calcul mental CE1 : ajouter des dizaines et des centaines, + 9, + 19, − 9, × 10 et problèmes. 100 exercices corrigés."),
         "+ 9 = + 10 − 1" if lv == 0 else "+ 19 = + 20 − 1", "27 + 9 = 37 − 1 = 36" if lv == 0 else "346 + 19 = 366 − 1 = 365",
         body, faq, sets, 5)


if __name__ == "__main__":
    build(0)
