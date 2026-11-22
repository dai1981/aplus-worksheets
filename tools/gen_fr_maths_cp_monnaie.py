# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : La monnaie
  python3 tools/gen_fr_maths_cp_monnaie.py
CP : pièces de 1 € et 2 €, billets de 5 €, 10 €, 20 €, 50 € ; compter, comparer, faire une somme, acheter.
CE1 : euros et centimes, écriture à virgule, rendre la monnaie (exercices du générateur CE2 avec un autre tirage).
Erreurs : compter les pièces au lieu de leur valeur, croire que plus de pièces = plus d’argent, 1 € = 10 c.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, eur, argent_svg, NB
import gen_fr_maths_ce2_monnaie as MO

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53012 + 100 * lv)
    K = Kids(R)
    MO.R = R
    MO.K = K


VAL = [100, 200, 500, 1000, 2000, 5000]


def E(c):
    return eur(c)


def nm(v):
    return ("un billet de %s" % E(v)) if v >= 500 else ("une pièce de %s" % (E(v) if v >= 100 else eur(v, c=True)))


def s1():
    if R.random() < 0.6:
        pool = VAL if L == 0 else VAL + [10, 20, 50]
        a, b = R.sample(pool, 2)
        more = R.random() < 0.6
        ans = nm(max(a, b) if more else min(a, b))
        return mcq("Qu’est-ce qui vaut le %s : %s ou %s ?" % ("plus" if more else "moins", nm(a), nm(b)), ans, [nm(min(a, b) if more else max(a, b)), "les deux valent autant", "on ne peut pas savoir"],
                   "%s %s %s : c’est <b>%s</b>." % (E(max(a, b)) if max(a, b) >= 100 else eur(max(a, b), c=True), "&gt;", E(min(a, b)) if min(a, b) >= 100 else eur(min(a, b), c=True), ans))
    v = R.choice(VAL if L == 0 else VAL + [10, 20, 50, 5, 2, 1])
    others = [x for x in (VAL if L == 0 else VAL + [10, 20, 50]) if x != v]
    R.shuffle(others)
    kind = "ce billet" if v >= 500 else "cette pièce"
    return mcq("<div class='qfig'>%s</div>Combien vaut %s ?" % (argent_svg([v]), kind), E(v) if v >= 100 else eur(v, c=True), [E(x) if x >= 100 else eur(x, c=True) for x in others[:3]],
               "C’est %s de <b>%s</b>." % ("un billet" if v >= 500 else "une pièce", E(v) if v >= 100 else eur(v, c=True)))


def s2():
    n = R.randint(2, 5)
    items = [R.choice(VAL[:5] if R.random() < 0.6 else VAL[:3]) for _ in range(n)]
    t = sum(items)
    if t > 10000:
        return None
    return mcq("<div class='qfig'>%s</div>Combien d’argent y a-t-il ?" % argent_svg(items), E(t), ["%d%s€" % (n, NB), E(t + 100), E(t - min(items)) if t - min(items) > 0 else E(t + 200)],
               "On ajoute les valeurs : %s = <b>%s</b>." % (" + ".join(E(x) for x in sorted(items, reverse=True)), E(t)))


def s3():
    p, q = K.two()
    k = R.choice(["qui", "combien"])
    if k == "qui":
        a = sorted([R.choice([100, 200]) for _ in range(R.randint(3, 6))], reverse=True)
        b = [R.choice([500, 1000, 200]) for _ in range(R.randint(1, 2))]
        ta, tb = sum(a), sum(b)
        if ta == tb:
            return None
        win = p[0] if ta > tb else q[0]
        return mcq("%s a %s. %s a %s. Qui a le plus d’argent ?" % (p[0], " + ".join(E(x) for x in a), q[0], " + ".join(E(x) for x in b)), win,
                   [q[0] if win == p[0] else p[0], "les deux ont autant", "celui qui a le plus de pièces"],
                   "%s a %s et %s a %s : <b>%s</b> a le plus d’argent (le nombre de pièces ne compte pas)." % (p[0], E(ta), q[0], E(tb), win))
    piece, tot = R.choice([(100, 500), (200, 1000), (500, 1000), (500, 2000), (1000, 2000), (1000, 5000), (200, 600), (200, 800), (100, 700), (500, 1500), (1000, 3000), (2000, 4000)])
    n = tot // piece
    return mcq("Combien de %s de %s faut-il pour faire %s ?" % ("billets" if piece >= 500 else "pièces", E(piece), E(tot)), str(n), [str(n + 1), str(tot // 100), str(n * 2)],
               "%s = %s : il en faut <b>%d</b>." % (" + ".join([E(piece)] * n), E(tot), n))


def decomp(t):
    out, r = [], t
    for v in [5000, 2000, 1000, 500, 200, 100]:
        while r >= v:
            out.append(v)
            r -= v
    return out


def s4():
    t = R.randint(3, 40) * 100 if L == 0 else R.randint(3, 60) * 100
    good = decomp(t)
    fmt = lambda xs: " + ".join(E(x) for x in xs)
    bad1 = good[:-1] if len(good) > 1 else [good[0] // 2]
    bad2 = good + [100]
    bad3 = [x for x in good] + [200] if good[-1] != 200 else good[:-1] + [100]
    return mcq("Quelle somme fait exactement %s ?" % E(t), fmt(good), [fmt(bad1), fmt(bad2), fmt(sorted(bad3, reverse=True))],
               "%s = <b>%s</b>." % (fmt(good), E(t)))


def s5():
    p = K.next()
    k = R.choice(["reste", "deux", "assez", "manque"])
    items = [("un ballon", 8), ("un livre", 6), ("une petite voiture", 3), ("un jeu", 15), ("une poupée", 12), ("un puzzle", 9), ("une trousse", 5), ("des crayons", 4), ("un yoyo", 2)]
    (a, pa), (b, pb) = R.sample(items, 2)
    if k == "reste":
        have = R.choice([10, 20, 20, 50])
        if pa >= have:
            return None
        return mcq("%s a un billet de %d €. %s achète %s à %d €. Combien d’argent lui reste-t-il ?" % (p[0], have, p[1].capitalize(), a, pa), E(100 * (have - pa)), [E(100 * (have + pa)), E(100 * pa), E(100 * (have - pa + 1))],
                   "%d − %d = <b>%d €</b>." % (have, pa, have - pa))
    if k == "deux":
        return mcq("%s achète %s à %d € et %s à %d €. Combien paie-t-%s ?" % (p[0], a, pa, b, pb, p[1]), E(100 * (pa + pb)), [E(100 * abs(pa - pb)), E(100 * (pa + pb + 1)), E(100 * max(pa, pb))],
                   "%d + %d = <b>%d €</b>." % (pa, pb, pa + pb))
    if k == "assez":
        have = pa + R.choice([-3, -2, -1, 1, 2, 4])
        if have <= 0:
            return None
        ok = have >= pa
        return mcq("%s a %d €. Peut-%s acheter %s à %d € ?" % (p[0], have, p[1], a, pa), "oui" if ok else "non", ["non" if ok else "oui", "seulement avec des pièces de 2 €", "on ne peut pas savoir"],
                   "%d %s %d : <b>%s</b>." % (have, "&gt;" if have > pa else "&lt;", pa, "oui" if ok else "non"))
    have = R.randint(1, pa - 1) if pa > 1 else 1
    return mcq("%s veut acheter %s à %d €. %s a %d €. Combien lui manque-t-il ?" % (p[0], a, pa, p[1].capitalize(), have), E(100 * (pa - have)), [E(100 * (pa + have)), E(100 * have), E(100 * (pa - have + 1))],
               "%d + … = %d : il manque <b>%d €</b>." % (have, pa, pa - have))


def e5():
    it = MO.s5()
    if it is None or "Combien coûtent" in it["q"]:
        return None
    return it


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Reconnaître les pièces et les billets", mix(R, seen, [(s1, 20)])), ("Compter l’argent", mix(R, seen, [(s2, 20)])),
                ("Comparer des sommes", mix(R, seen, [(s3, 20)])), ("Faire une somme", mix(R, seen, [(s4, 20)])), ("Acheter", mix(R, seen, [(s5, 20)]))]
        th = ["Les pièces de 1 € et de 2 € ; les billets de 5 €, 10 €, 20 €, 50 €.",
              "Pour compter l’argent, on ajoute la <b>valeur</b> de chaque pièce et de chaque billet.",
              "Beaucoup de pièces, ce n’est pas toujours beaucoup d’argent : un billet de 10 € vaut plus que 4 pièces de 2 €."]
        ex = example("10 € + 5 € + 2 €", ["10 + 5 = 15", "15 + 2 = 17"], "17 €")
    else:
        sets = [("Reconnaître les pièces et les billets", mix(R, seen, [(s1, 20)])), ("Compter l’argent", mix(R, seen, [(MO.s1, 20)])),
                ("Euros et centimes", mix(R, seen, [(MO.s2, 20)])), ("Rendre la monnaie", mix(R, seen, [(MO.s4, 20)])), ("Problèmes d’achat", mix(R, seen, [(e5, 20)]))]
        th = ["1 euro = 100 centimes : 1 € = 100 c.",
              "3,50 € se lit « 3 euros 50 » : avant la virgule les euros, après les centimes.",
              "Pour rendre la monnaie, on complète du prix jusqu’à la somme donnée."]
        ex = example("On paie 7,50 € avec un billet de 10 €", ["7,50 € + 0,50 € = 8 €", "8 € + 2 € = 10 €"], "on rend 2,50 €")
    body = lesson(th, [ex], [["Compter les pièces au lieu de leur valeur", "3 pièces de 2 € font 6 €, pas 3 €."],
                             ["Croire que plus de pièces = plus d’argent", "On compare les sommes, pas le nombre de pièces."],
                             ["1 € = 10 c" if lv else "Oublier un billet", "1 € = 100 c." if lv else "On barre chaque pièce quand on l’a comptée."]])
    faq = [("Quelles pièces et quels billets existent ?", "Pièces : 1 c, 2 c, 5 c, 10 c, 20 c, 50 c, 1 €, 2 €. Billets : 5 €, 10 €, 20 €, 50 €, 100 €, 200 €."),
           ("Comment rendre la monnaie ?", "On part du prix et on ajoute jusqu’à la somme donnée par le client.")]
    unit(lv, R, "monnaie", "G",
         ("Connaître les pièces et les billets en euros ; comparer des sommes ; réaliser une somme d’argent ; résoudre des problèmes d’achat en euros" if lv == 0 else
          "Connaître les pièces et les billets ; utiliser les euros et les centimes (1 € = 100 c) et l’écriture à virgule ; rendre la monnaie ; résoudre des problèmes d’achat"),
         "La monnaie", "Monnaie",
         ("Fiches de maths CP sur la monnaie : pièces et billets en euros, compter, comparer, faire une somme et acheter. 100 exercices corrigés." if lv == 0 else
          "Fiches de maths CE1 sur la monnaie : pièces et billets, compter, euros et centimes, rendre la monnaie et problèmes d’achat. 100 exercices corrigés."),
         "On compte la valeur des pièces et des billets." if lv == 0 else "1 € = 100 centimes", "10 € + 5 € + 2 € = 17 €" if lv == 0 else "3,50 € = 3 euros et 50 centimes",
         body, faq, sets, 12)


if __name__ == "__main__":
    build(0)
