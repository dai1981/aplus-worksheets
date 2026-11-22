# -*- coding: utf-8 -*-
"""
France Maths 3e : Diviseurs, diviseurs communs et fractions irréductibles
  python3 tools/gen_fr_maths_3e_fractions_irreductibles_et_diviseurs.py
Erreurs : oublier un diviseur, simplifier par un nombre qui ne divise pas les deux termes, s’arrêter avant la fraction irréductible.
"""
import random
from math import gcd
from fr_c4 import *

R = random.Random(60401)
K = Kids(R)


def divs(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def s1():
    n = R.choice([12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 72, 75, 80, 84, 90, 96, 100])
    k = R.choice(["liste", "nb", "est"])
    dv = divs(n)
    if k == "liste":
        miss = [x for x in dv if x not in (1, n)]
        w1 = ", ".join(map(str, [x for x in dv if x != R.choice(miss)]))
        w2 = ", ".join(map(str, [x for x in dv if x not in (1, n)]))
        w3 = ", ".join(map(str, sorted(set(dv) | {max(dv) // 2 + 1})))
        return M("Quelle est la liste de tous les diviseurs de %d ?" % n, ", ".join(map(str, dv)), [w1, w2, w3], "On cherche les produits égaux à %d : %s. Diviseurs : <b>%s</b>." % (n, " ; ".join("%d × %d" % (a, n // a) for a in dv if a * a <= n), ", ".join(map(str, dv))))
    if k == "nb":
        return M("Combien %d a-t-il de diviseurs ?" % n, str(len(dv)), [str(len(dv) - 2), str(len(dv) - 1), str(len(dv) + 1)], "%s : <b>%d</b> diviseurs." % (", ".join(map(str, dv)), len(dv)))
    c = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15])
    ok = n % c == 0
    return M("%d est-il un diviseur de %d ?" % (c, n), "oui" if ok else "non", ["non" if ok else "oui", "seulement si %d est pair" % n, "on ne peut pas savoir"],
             "%d ÷ %d = %s : %s." % (n, c, d(Fr(n, c)) if (Fr(n, c) * 100).denominator == 1 else "%d reste %d" % (n // c, n % c), "c’est un entier, <b>oui</b>" if ok else "ce n’est pas un entier, <b>non</b>"))


def s2():
    g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18])
    a, b = R.randint(2, 9), R.randint(2, 9)
    if gcd(a, b) != 1 or a == b:
        return None
    x, y = a * g, b * g
    k = R.choice(["pgd", "pgd", "communs"])
    if k == "pgd":
        cd = [z for z in divs(g) if z != g]
        w = [str(cd[-1]) if cd else "1", str(x * y // g), str(min(x, y)) if min(x, y) != g else str(g * 2)]
        return M("Quel est le plus grand diviseur commun à %d et %d ?" % (x, y), str(g), w, "Les diviseurs communs à %d et %d sont %s : le plus grand est <b>%d</b>." % (x, y, ", ".join(map(str, divs(g))), g))
    dc = divs(g)
    return M("Quels sont les diviseurs communs à %d et %d ?" % (x, y), ", ".join(map(str, dc)), [", ".join(map(str, dc[1:])) if len(dc) > 1 else "aucun", ", ".join(map(str, dc + [min(x, y)])) if min(x, y) not in dc else ", ".join(map(str, dc[:-1])), "1 seulement" if len(dc) > 1 else "1, %d" % x],
             "Ce sont les diviseurs de %d : <b>%s</b>." % (g, ", ".join(map(str, dc))))


def s3():
    g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15])
    a, b = R.randint(1, 12), R.randint(2, 15)
    if gcd(a, b) != 1 or a == b:
        return None
    x, y = a * g, b * g
    p = R.choice([q for q in (2, 3, 5) if g % q == 0] or [1])
    half = Fr(x // p, y // p) if p > 1 else None
    w = [fr(x // p, y // p) if p > 1 and p != g else fr(a + 1, b), fr(x - g, y - g) if x > g else fr(a, b + 1), fr(b, a)]
    return M("Écris la fraction %s sous forme irréductible." % fr(x, y), fq(Fr(x, y)), w, "%d est le plus grand diviseur commun à %d et %d : %s = <b>%s</b>." % (g, x, y, fr("%d ÷ %d" % (x, g), "%d ÷ %d" % (y, g)), fq(Fr(x, y))))


def s4():
    k = R.choice(["irr", "irr", "egal"])
    if k == "irr":
        a, b = R.randint(2, 40), R.randint(2, 40)
        if a == b:
            return None
        ok = gcd(a, b) == 1
        return M("La fraction %s est-elle irréductible ?" % fr(a, b), "oui" if ok else "non, on peut la simplifier par %d" % gcd(a, b), ["non, on peut la simplifier par %d" % (gcd(a, b) + 1) if not ok else "non, on peut la simplifier par 2", "oui" if not ok else "non, car %d est pair" % (a if a % 2 == 0 else b), "on ne peut pas savoir"],
                 "Le plus grand diviseur commun à %d et %d est %d : %s." % (a, b, gcd(a, b), "<b>elle est irréductible</b>" if ok else "<b>on peut simplifier par %d</b>" % gcd(a, b)))
    a, b = R.randint(1, 9), R.randint(2, 12)
    if gcd(a, b) != 1:
        return None
    m, n = R.randint(2, 9), R.randint(2, 9)
    ok = R.random() < 0.5
    c, e = (a * m, b * m) if ok else (a * m + 1, b * m)
    return M("Les fractions %s et %s sont-elles égales ?" % (fr(a * n, b * n), fr(c, e)), "oui" if ok else "non", ["non" if ok else "oui", "seulement si on les arrondit", "on ne peut pas comparer"],
             "Sous forme irréductible : %s et %s : <b>%s</b>." % (fq(Fr(a * n, b * n)), fq(Fr(c, e)), "oui" if ok else "non"))


def s5():
    k = R.choice(["paquets", "dalles", "bouquets", "rangs"])
    g = R.choice([4, 6, 8, 9, 12, 15, 18, 24])
    a, b = R.randint(2, 7), R.randint(2, 7)
    if gcd(a, b) != 1 or a == b:
        return None
    x, y = a * g, b * g
    if k == "paquets":
        return M("Un pâtissier a %d macarons au chocolat et %d à la framboise. Il veut faire le plus grand nombre de boîtes identiques en utilisant tous les macarons. Combien de boîtes ?" % (x, y), str(g),
                 [str(g // 2) if g % 2 == 0 else str(g + 1), str(x + y), str(gcd(x, y) * 2)], "Le nombre de boîtes divise %d et %d ; le plus grand diviseur commun est <b>%d</b> (chaque boîte : %d au chocolat et %d à la framboise)." % (x, y, g, a, b))
    if k == "dalles":
        return M("Une pièce rectangulaire mesure %d dm sur %d dm. On veut la couvrir de dalles carrées identiques, les plus grandes possible, sans les couper. Quel est le côté d’une dalle ?" % (x, y), "%d dm" % g,
                 ["%d dm" % (g // 2) if g % 2 == 0 else "%d dm" % (g // 3 if g % 3 == 0 else 1), "%d dm" % min(x, y), "%d dm" % (x * y // g)], "Le côté divise %d et %d ; le plus grand diviseur commun est <b>%d dm</b>." % (x, y, g))
    if k == "bouquets":
        return M("Avec %d roses et %d tulipes, on fait le plus de bouquets identiques possible. Combien de roses par bouquet ?" % (x, y), str(a), [str(b), str(g), str(a + b)], "%d bouquets (plus grand diviseur commun) ; %d ÷ %d = <b>%d</b> roses." % (g, x, g, a))
    return M("Une fanfare a %d tambours et %d trompettes. Elle défile en rangs identiques, le plus grand nombre de rangs possible. Combien de musiciens par rang ?" % (x, y), str(a + b), [str(g), str(a), str(x + y)],
             "%d rangs ; chaque rang : %d tambours + %d trompettes = <b>%d</b>." % (g, a, b, a + b))


def main():
    seen = set()
    sets = [("Diviseurs d’un nombre", mix(R, seen, [(s1, 20)])), ("Diviseurs communs", mix(R, seen, [(s2, 20)])),
            ("Fractions irréductibles", mix(R, seen, [(s3, 20)])), ("Irréductible ou égales ?", mix(R, seen, [(s4, 20)])), ("Problèmes de partage", mix(R, seen, [(s5, 20)]))]
    body = L(["a est un <b>diviseur</b> de b si la division de b par a tombe juste. On trouve les diviseurs par paires : 36 = 1 × 36 = 2 × 18 = 3 × 12 = 4 × 9 = 6 × 6.",
              "Pour rendre une fraction <b>irréductible</b>, on divise le numérateur et le dénominateur par leur plus grand diviseur commun.",
              "Le plus grand diviseur commun résout les problèmes de partage en parts identiques les plus grandes (ou les plus nombreuses) possible."],
             [("84/126", ["diviseurs communs à 84 et 126 : 1, 2, 3, 6, 7, 14, 21, 42", "on divise par 42"], "2/3")],
             [["Oublier un diviseur (par exemple 6 pour 36)", "On teste tous les nombres jusqu’à la racine carrée."], ["Simplifier 24/36 en 12/18 et s’arrêter", "On divise par le plus grand diviseur commun, 12 : 2/3."],
              ["Diviser un seul terme de la fraction", "On divise le numérateur et le dénominateur par le même nombre."]])
    faq = [("Comment savoir si une fraction est irréductible ?", "Le seul diviseur commun au numérateur et au dénominateur est 1."),
           ("À quoi sert le plus grand diviseur commun ?", "À simplifier une fraction en une seule étape et à résoudre des problèmes de partage équitable.")]
    unit("3e", R, "fractions-irreductibles-et-diviseurs", "N",
         "Déterminer les diviseurs d’un nombre entier ; déterminer les diviseurs communs et le plus grand diviseur commun à deux entiers ; rendre une fraction irréductible ; résoudre des problèmes de partage",
         "Diviseurs et fractions irréductibles", "Diviseurs et fractions irréductibles",
         "Fiches de maths 3e sur les diviseurs : liste des diviseurs, diviseurs communs, plus grand diviseur commun, fractions irréductibles et problèmes de partage. 100 exercices corrigés.",
         "Fraction irréductible : on divise par le plus grand diviseur commun", "84/126 = 2/3 (on divise par 42)", body, faq, sets, 1)


if __name__ == "__main__":
    main()
