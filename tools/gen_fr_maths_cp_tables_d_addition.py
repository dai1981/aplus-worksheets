# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Tables d’addition et compléments (CE1 : compléments à la dizaine et à 100)
  python3 tools/gen_fr_maths_cp_tables_d_addition.py
Erreurs : compter le premier nombre deux fois (8 + 5 = 12), donner la somme au lieu du complément,
complément à 100 de 65 = 45 (oublier la retenue).
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, ch, KINDS, nom, de
import k_pics as KP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53004 + 100 * lv)
    K = Kids(R)


def wr(v, *xs):
    return [str(x) for x in xs if x >= 0 and x != v]


def s1():
    """CP : sommes jusqu’à 10 avec images ; CE1 : tables jusqu’à 20"""
    if L == 0:
        a, b = R.randint(1, 6), R.randint(1, 6)
        if a + b > 10:
            return None
        k = R.choice(["des", "grp"])
        if k == "des":
            svg = pic(KP.dice_svg([a, b]), "deux dés : %d et %d" % (a, b))
            q = "<div class='qfig'>%s</div>Combien de points en tout ?" % svg
        else:
            kind = R.choice(KINDS)
            svg = pic(KP.two_groups_svg(a, kind, b, kind, word="+"), "%s et %s" % (ch(kind, a), ch(kind, b)))
            q = "<div class='qfig'>%s</div>%d + %d = …" % (svg, a, b)
        return mcq(q, str(a + b), wr(a + b, a + b - 1, a + b + 1, abs(a - b) if a != b else a + b + 2),
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    a, b = R.randint(2, 9), R.randint(2, 9)
    if R.random() < 0.3:
        a = R.randint(10, 11)
    return mcq("%d + %d = …" % (a, b), str(a + b), wr(a + b, a + b - 1, a + b + 1, a + b - 10 if a + b > 10 else a + b + 10),
               "%d + %d = <b>%d</b>." % (a, b, a + b))


def s2():
    """compléments à 10 (CP) / à la dizaine supérieure (CE1)"""
    if L == 0:
        n = R.randint(1, 9)
        r = R.random()
        if r < 0.4:
            svg = pic(KP.tenframe_svg(n, 1, kind="dot"), "une boîte de 10 avec %d jetons" % n)
            q = "<div class='qfig'>%s</div>Combien manque-t-il pour faire 10 ?" % svg
        else:
            q = R.choice(["%d + … = 10" % n, "… + %d = 10" % n, "10 = %d + …" % n, "Combien faut-il ajouter à %d pour avoir 10 ?" % n])
        return mcq(q, str(10 - n), wr(10 - n, n, 10 + n, 10 - n + 1 if 10 - n < 9 else 10 - n - 1),
                   "%d + <b>%d</b> = 10." % (n, 10 - n))
    n = R.randint(11, 98)
    if n % 10 == 0:
        return None
    t = n // 10 * 10 + 10
    return mcq("%d + … = %d" % (n, t), str(t - n), wr(t - n, n % 10, 10 - n % 10 + 1, t - n + 10),
               "Pour aller de %d à %d, il faut <b>%d</b> (%d + %d = 10)." % (n, t, t - n, n % 10, t - n))


def s3():
    """CP : sommes avec passage de la dizaine ; CE1 : compléments à 100"""
    if L == 0:
        a, b = R.randint(5, 9), R.randint(3, 9)
        if a + b <= 10:
            return None
        k = 10 - a
        q = "%d + %d = …" % (a, b)
        if R.random() < 0.4:
            svg = pic(KP.tenframe_svg(a + b, 2, kind="dot"), "deux boîtes de 10 avec %d jetons" % (a + b))
            q = "<div class='qfig'>%s</div>%s" % (svg, q)
        return mcq(q, str(a + b), wr(a + b, a + b - 1, a + b + 1, a + b - 10),
                   "On complète à 10 : %d + %d = 10, puis 10 + %d = <b>%d</b>." % (a, k, b - k, a + b))
    if R.random() < 0.4:
        d = R.randint(1, 9) * 10
        return mcq("%d + … = 100" % d, str(100 - d), wr(100 - d, d, 100 - d + 10, (10 - d // 10)),
                   "%s + %s = 10 dizaines : %d + <b>%d</b> = 100." % (pl(d // 10, "dizaine"), pl(10 - d // 10, "dizaine"), d, 100 - d))
    n = R.randint(11, 89)
    if n % 10 == 0:
        return None
    c = 100 - n
    return mcq("%d + … = 100" % n, str(c), wr(c, c + 10, (10 - n // 10) * 10 + (10 - n % 10), c - 1),
               "%d + %d = %d, puis %d + %d = 100. En tout : <b>%d</b>." % (n, 10 - n % 10, n + 10 - n % 10, n + 10 - n % 10, 100 - (n + 10 - n % 10), c))


def s4():
    """compléter et décomposer"""
    if L == 0:
        s = R.randint(6, 20)
        a = R.randint(1, s - 1)
        if s - a > 10 or a > 10:
            return None
        if R.random() < 0.5:
            return mcq("%d + … = %d" % (a, s), str(s - a), wr(s - a, s + a, s - a + 1, s), "%d + <b>%d</b> = %d. On peut vérifier en comptant à partir de %d." % (a, s - a, s, a))
        if R.random() < 0.5:
            svg = pic(KP.bond_svg(s, a, "?"), "%d se décompose en %d et ?" % (s, a))
            return mcq("<div class='qfig'>%s</div>Quel nombre manque ?" % svg, str(s - a), wr(s - a, s + a, s - a - 1, s), "%d = %d + <b>%d</b>." % (s, a, s - a))
        return mcq("%d = %d + …" % (s, a), str(s - a), wr(s - a, s + a, s - a + 1, a), "%d = %d + <b>%d</b>." % (s, a, s - a))
    a, b, c = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
    if R.random() < 0.5:
        return mcq("%d + %d + %d = …" % (a, b, c), str(a + b + c), wr(a + b + c, a + b + c - 1, a + b + c + 1, a + b + c + 10, a + b),
                   "On cherche d’abord une paire facile : %d + %d + %d = <b>%d</b>." % (a, b, c, a + b + c))
    s = R.randint(11, 20)
    a = R.randint(2, 9)
    if s - a > 9:
        return None
    return mcq("%d = %d + …" % (s, a), str(s - a), wr(s - a, s + a, s - a + 1, s - 10), "%d − %d = %d, donc %d = %d + <b>%d</b>." % (s, a, s - a, s, a, s - a))


def s5():
    p = K.next()
    k = R.choice(["tot", "manque", "boite", "deux"])
    if L == 0:
        if k == "tot":
            a, b = R.randint(3, 9), R.randint(2, 9)
            th = R.choice(["billes", "images", "bonbons", "voitures"])
            return mcq("%s a %d %s. On lui en donne %d. Combien en a-t-%s maintenant ?" % (p[0], a, th, b, p[1]), str(a + b), wr(a + b, a + b - 1, a - b if a > b else a + b + 1, a + b + 10),
                       "%d + %d = <b>%d</b> %s." % (a, b, a + b, th))
        if k in ("manque", "boite"):
            n = R.randint(2, 8)
            return mcq("Une boîte contient 10 œufs. %s en a déjà mis %d. Combien doit-%s encore en mettre ?" % (p[0], n, p[1]), str(10 - n), wr(10 - n, n, 10 + n, 10 - n - 1),
                       "%d + <b>%d</b> = 10." % (n, 10 - n))
        a, b = R.randint(5, 9), R.randint(5, 9)
        q, r = K.next(), p
        return mcq("%s a %d cartes et %s en a %d. Combien de cartes y a-t-il en tout ?" % (p[0], a, q[0], b), str(a + b), wr(a + b, a + b - 1, a + b + 1, a + b - 10),
                   "%d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "tot":
        n = R.randint(21, 89)
        if n % 10 == 0:
            return None
        t = n // 10 * 10 + 10
        return mcq("Le car a %d places. %d élèves sont assis. Combien manque-t-il d’élèves pour qu’il soit plein ? (le car a %d places)" % (t, n, t) if False else
                   "Le car a %d places. %d élèves sont assis. Combien de places sont libres ?" % (t, n), str(t - n), wr(t - n, t + n, 10 - (t - n) if t - n != 5 else t - n + 1, t - n + 10),
                   "%d + <b>%d</b> = %d." % (n, t - n, t))
    if k in ("manque", "boite"):
        n = R.randint(21, 89)
        if n % 10 == 0:
            return None
        return mcq("%s a %d €. Il lui faut 100 € pour acheter un vélo. Combien lui manque-t-il ?" % (p[0], n) if p[1] == "il" else
                   "%s a %d €. Il lui faut 100 € pour acheter un vélo. Combien lui manque-t-il ?" % (p[0], n), "%d €" % (100 - n), ["%d €" % x for x in (100 - n + 10, (10 - n // 10) * 10 + 10 - n % 10, 100 + n) if x != 100 - n],
                   "%d + %d = %d, puis + %d = 100 : il manque <b>%d €</b>." % (n, 10 - n % 10, n + 10 - n % 10, 100 - n - 10 + n % 10, 100 - n))
    a, b, c = R.randint(3, 9), R.randint(3, 9), R.randint(3, 9)
    return mcq("%s gagne %d points, puis %d points, puis %d points. Combien de points en tout ?" % (p[0], a, b, c), str(a + b + c), wr(a + b + c, a + b, a + b + c + 1, a + b + c - 1),
               "%d + %d + %d = <b>%d</b>." % (a, b, c, a + b + c))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Additions jusqu’à 10" if lv == 0 else "Tables d’addition", mix(R, seen, [(s1, 20)])),
        ("Compléments à 10" if lv == 0 else "Compléter à la dizaine", mix(R, seen, [(s2, 20)])),
        ("Passer la dizaine" if lv == 0 else "Compléter à 100", mix(R, seen, [(s3, 20)])),
        ("Compléter et décomposer" if lv == 0 else "Trois nombres et décompositions", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    if lv == 0:
        th = ["Les compléments à 10 sont à savoir par cœur : 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5.",
              "Pour 8 + 5, on complète à 10 : 8 + 2 = 10, puis 10 + 3 = 13.",
              "8 + 5 = 5 + 8 : on peut commencer par le plus grand nombre."]
        ex = example("9 + 6", ["9 + 1 = 10", "10 + 5 = 15"], "15")
    else:
        th = ["Compléter à la dizaine : 47 + 3 = 50 (7 + 3 = 10).",
              "Compléter à 100 : 65 + 5 = 70, puis 70 + 30 = 100, donc 65 + 35 = 100.",
              "Pour ajouter trois nombres, on cherche une paire qui fait 10."]
        ex = example("65 + … = 100", ["65 + 5 = 70", "70 + 30 = 100"], "35")
    body = lesson(th, [ex], [["Compter le premier nombre deux fois : 8 + 5 = 12", "On compte à partir du nombre suivant : 9, 10, 11, 12, 13."],
                             ["Donner le total au lieu du complément", "« Combien manque-t-il ? » : on cherche ce qu’il faut ajouter."],
                             ["Complément à 100 de 65 = 45" if lv else "Croire que 10 − 3 = 6", "65 + 45 = 110. Le bon complément est 35." if lv else "3 + 7 = 10, donc il manque 7."]])
    faq = [("Comment apprendre les tables d’addition ?", "D’abord les compléments à 10 et les doubles, puis les autres en passant par 10."),
           ("Qu’est-ce qu’un complément ?", "C’est ce qu’il faut ajouter pour arriver à un nombre : le complément de 7 à 10 est 3.")]
    unit(lv, R, "tables-d-addition" if lv == 0 else "complements-a-la-dizaine-et-a-100", "N",
         ("Connaître les compléments à 10 ; connaître les tables d’addition (de 0 à 10) et les utiliser pour une addition ou une soustraction ; décomposer les nombres jusqu’à 20" if lv == 0 else
          "Connaître les tables d’addition ; calculer des compléments à la dizaine supérieure et à 100 ; ajouter plusieurs nombres en regroupant ceux qui font 10"),
         "Tables d’addition et compléments à 10" if lv == 0 else "Compléments à la dizaine et à 100", "Tables d’addition" if lv == 0 else "Compléments à 100",
         ("Fiches de maths CP sur les tables d’addition : additions jusqu’à 10, compléments à 10, passer la dizaine, décomposer et problèmes. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur les compléments : tables d’addition, compléter à la dizaine, compléter à 100, trois nombres et problèmes. 100 exercices corrigés."),
         "7 + 3 = 10" if lv == 0 else "65 + 35 = 100", "Les compléments à 10 aident à calculer." if lv == 0 else "On passe par la dizaine : 65 → 70 → 100.",
         body, faq, sets, 4)


if __name__ == "__main__":
    build(0)
