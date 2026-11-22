# -*- coding: utf-8 -*-
"""
France Maths 4e : Probabilités (événement contraire, événements incompatibles, expériences à deux épreuves)
  python3 tools/gen_fr_maths_4e_probabilites.py
Erreurs : additionner des probabilités d’événements compatibles, oublier des issues dans un tableau, croire que la somme de deux dés est équiprobable.
"""
import random
from fr_c4 import *

R = random.Random(60318)
K = Kids(R)
COUL = [("rouge", "rouges"), ("bleue", "bleues"), ("verte", "vertes"), ("jaune", "jaunes"), ("noire", "noires"), ("blanche", "blanches")]


def boules(cs, ns):
    p = ["%d boule%s %s" % (n, "s" if n > 1 else "", c[1] if n > 1 else c[0]) for c, n in zip(cs, ns)]
    return ", ".join(p[:-1]) + " et " + p[-1]


def s1():
    k = R.choice(["contr", "contr", "contrfrac", "incomp"])
    if k == "contr":
        p = Fr(R.randint(1, 99), 100)
        return M("La probabilité qu’un événement A se réalise est %s. Quelle est la probabilité de l’événement contraire « non A » ?" % d(p), d(1 - p), [d(p), d(-p), d(1 + p)],
                 "P(non A) = 1 − P(A) = 1 − %s = <b>%s</b>." % (d(p), d(1 - p)))
    if k == "contrfrac":
        n = R.choice([3, 5, 6, 7, 8, 9, 12])
        m = R.randint(1, n - 1)
        p = Fr(m, n)
        return M("P(A) = %s. Quelle est P(non A) ?" % fq(p), fq(1 - p), [fq(p), fr(1, n - m) if n - m > 1 else fr(1, n), fr(n - m, m) if n - m != m else fr(2, n)],
                 "1 − %s = <b>%s</b>." % (fq(p), fq(1 - p)))
    cs = R.sample(COUL, 3)
    ns = [R.randint(1, 6) for _ in cs]
    t = sum(ns)
    p = Fr(ns[0] + ns[1], t)
    return M("Une urne contient %s. Quelle est la probabilité de tirer une boule %s ou %s ?" % (boules(cs, ns), cs[0][0], cs[1][0]), fq(p), [fq(Fr(ns[0] * ns[1], t * t)), fr(ns[0] + ns[1], t * 2), fq(Fr(ns[2], t))],
             "Les deux événements sont incompatibles : P = %s + %s = <b>%s</b>." % (fr(ns[0], t), fr(ns[1], t), fq(p)))


def s2():
    k = R.choice(["piece2", "de_piece", "deux_de", "urne2"])
    if k == "piece2":
        ev, n_, txt = R.choice([("deux « pile »", 1, "PP"), ("au moins un « pile »", 3, "PP, PF, FP"), ("un « pile » et un « face »", 2, "PF, FP"), ("aucun « pile »", 1, "FF")])
        return M("On lance deux fois une pièce équilibrée. Quelle est la probabilité d’obtenir %s ?" % ev, fq(Fr(n_, 4)), [fr(1, 3) if n_ != 1 else fr(1, 2), fr(n_, 2) if n_ < 2 else fr(1, 4), fr(n_ + 1, 4) if n_ < 3 else fr(1, 2)],
                 "Issues : PP, PF, FP, FF (4 issues équiprobables). Favorables : %s → <b>%s</b>." % (txt, fq(Fr(n_, 4))))
    if k == "de_piece":
        f = R.randint(1, 6)
        return M("On lance un dé à 6 faces puis une pièce. Combien y a-t-il d’issues ? Et quelle est la probabilité d’obtenir « %d et pile » ?" % f, "12 issues ; %s" % fr(1, 12), ["8 issues ; %s" % fr(1, 8), "12 issues ; %s" % fr(1, 6), "6 issues ; %s" % fr(1, 6)],
                 "6 × 2 = 12 issues équiprobables ; une seule est favorable : <b>%s</b>." % fr(1, 12))
    if k == "deux_de":
        s = R.randint(2, 12)
        n_ = 6 - abs(7 - s)
        return M("On lance deux dés à 6 faces et on additionne les résultats. Quelle est la probabilité d’obtenir %d ?" % s, fq(Fr(n_, 36)), [fr(1, 11), fr(1, 12) if Fr(1, 12) != Fr(n_, 36) else fr(1, 6), fq(Fr(n_, 6)) if Fr(n_, 6) != Fr(n_, 36) else fr(2, 36)],
                 "Il y a 36 issues équiprobables (tableau 6 × 6) ; %s donnent %d : <b>%s</b>." % (pl(n_, "issue"), s, fq(Fr(n_, 36))))
    cs = R.sample(COUL, 2)
    a, b = R.randint(1, 5), R.randint(1, 5)
    t = a + b
    p = Fr(a * a, t * t)
    return M("Une urne contient %s. On tire une boule, on la remet, puis on en tire une seconde. Quelle est la probabilité d’obtenir deux boules %s ?" % (boules(cs, [a, b]), cs[0][1]), fq(p),
             [fq(Fr(2 * a, t)) if 2 * a < t else fr(a, 2 * t), fq(Fr(a, t)), fq(Fr(a * a, t)) if a * a < t else fq(Fr(a, t * t))],
             "Arbre : %s × %s = <b>%s</b>." % (fr(a, t), fr(a, t), fq(p)))


def s3():
    a = R.randint(1, 4)
    b = R.randint(1, 4)
    t = a + b
    k = R.choice(["deux", "diff", "aumoins"])
    cs = R.sample(COUL, 2)
    pa, pb = Fr(a, t), Fr(b, t)
    if k == "deux":
        p = pb * pb
        ev = "deux boules %s" % cs[1][1]
    elif k == "diff":
        p = 2 * pa * pb
        ev = "deux boules de couleurs différentes"
    else:
        p = 1 - pb * pb
        ev = "au moins une boule %s" % cs[0][0]
    return M("Urne : %s. On tire une boule, on la remet, on en tire une autre. Quelle est la probabilité d’obtenir %s ?" % (boules(cs, [a, b]), ev), fq(p),
             [fq(pa * pb) if pa * pb != p else fq(p / 2), fq(pa + pb) if pa + pb != p else fr(1, 2), fq(1 - p) if 1 - p != p else fq(p * 2 / 3)],
             "Avec l’arbre : %s → <b>%s</b>." % ({"deux": "%s × %s" % (fq(pb), fq(pb)), "diff": "%s × %s + %s × %s" % (fq(pa), fq(pb), fq(pb), fq(pa)), "aumoins": "1 − %s × %s" % (fq(pb), fq(pb))}[k], fq(p)))


def s4():
    k = R.choice(["tableau", "tableau", "menu", "code"])
    if k == "tableau":
        ev, f = R.choice([("un double", lambda x, y: x == y), ("une somme égale à 7", lambda x, y: x + y == 7), ("un produit pair", lambda x, y: (x * y) % 2 == 0),
                          ("deux nombres impairs", lambda x, y: x % 2 and y % 2), ("au moins un 6", lambda x, y: x == 6 or y == 6), ("une somme supérieure à 9", lambda x, y: x + y > 9)])
        n_ = sum(1 for x in range(1, 7) for y in range(1, 7) if f(x, y))
        return M("On lance deux dés à 6 faces. Quelle est la probabilité d’obtenir %s ?" % ev, fq(Fr(n_, 36)), [fr(n_, 12) if Fr(n_, 12) < 1 else fr(1, 2), fq(Fr(n_ + 1, 36)), fr(1, 6) if Fr(n_, 36) != Fr(1, 6) else fr(1, 3)],
                 "Dans le tableau à double entrée (36 cases), %s conviennent : <b>%s</b>." % (pl(n_, "case"), fq(Fr(n_, 36))))
    if k == "menu":
        e, p_, ds = R.randint(2, 4), R.randint(2, 4), R.randint(2, 4)
        return M("Un menu propose %d entrées, %d plats et %d desserts. Combien de menus différents (entrée, plat, dessert) peut-on composer ?" % (e, p_, ds), str(e * p_ * ds), [str(e + p_ + ds), str(e * p_ + ds), str(e * p_ * ds * 2)],
                 "%d × %d × %d = <b>%d</b> menus." % (e, p_, ds, e * p_ * ds))
    n = R.choice([2, 3])
    return M("Un cadenas a %d molettes de %d chiffres chacune (0 à %d). Combien de codes possibles ? Et quelle est la probabilité de trouver le code au hasard du premier coup ?" % (n, 10, 9), "%s codes ; %s" % (num(10 ** n), fr(1, num(10 ** n))),
             ["%d codes ; %s" % (10 * n, fr(1, 10 * n)), "%s codes ; %s" % (num(10 ** n), fr(1, 10)), "%d codes ; %s" % (n ** 10 if n == 2 else 9 ** n, fr(1, 9 ** n))],
             "10 possibilités pour chaque molette : 10<sup>%d</sup> = %s codes ; <b>%s</b>." % (n, num(10 ** n), fr(1, num(10 ** n))))


def s5():
    k = R.choice(["jeu", "roue", "equit", "sondage"])
    p = K.next()
    if k == "jeu":
        return M("On lance deux dés. %s gagne si la somme vaut 7, son adversaire gagne si la somme vaut 12. Ce jeu est-il équitable ?" % p[0], "non, %s a plus de chances" % p[0], ["oui, chacun a une chance sur 11", "non, l’adversaire a plus de chances", "on ne peut pas savoir"],
                 "P(somme 7) = 6/36 et P(somme 12) = 1/36 : <b>non, %s a plus de chances</b>." % p[0])
    if k == "roue":
        n = R.choice([4, 5, 8, 10])
        g = R.randint(1, n - 1)
        p2 = Fr(g, n) ** 2
        return M("Une roue a %d secteurs égaux dont %s. On la fait tourner deux fois. Quelle est la probabilité de gagner les deux fois ?" % (n, pl(g, "secteur gagnant", "secteurs gagnants")), fq(p2),
                 [fq(Fr(2 * g, n)) if 2 * g < n else fq(Fr(g, n)), fq(Fr(g, n)), fq(Fr(g * g, n)) if g * g < n else fq(1 - p2)], "%s × %s = <b>%s</b>." % (fq(Fr(g, n)), fq(Fr(g, n)), fq(p2)))
    if k == "equit":
        return M("Pile ou face avec deux pièces : %s gagne si les deux faces sont identiques, sinon c’est son adversaire. Le jeu est-il équitable ?" % p[0], "oui : chacun a une probabilité de 1/2", ["non : %s a plus de chances" % p[0], "non : l’adversaire a 3 chances sur 4", "on ne peut pas savoir"],
                 "Identiques : PP, FF ; différentes : PF, FP. <b>Oui, 1/2 chacun</b>.")
    tot = R.choice([200, 400, 500, 1000])
    q = R.choice([Fr(1, 4), Fr(2, 5), Fr(3, 10), Fr(1, 5)])
    return M("Dans un sondage, %s des élèves viennent à vélo. Dans un collège de %d élèves, combien peut-on estimer de cyclistes ?" % (d(q * 100) + " %", tot), str(int(q * tot)), [str(int(q * 100)), str(tot - int(q * tot)), str(int(q * tot) * 2)],
             "%s %% de %d = <b>%d</b> (c’est une estimation)." % (d(q * 100), tot, int(q * tot)))


def main():
    seen = set()
    sets = [("Événement contraire et incompatibles", mix(R, seen, [(s1, 20)])), ("Deux épreuves : lister les issues", mix(R, seen, [(s2, 20)])),
            ("Arbres de probabilités", mix(R, seen, [(s3, 20)])), ("Tableaux et dénombrement", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["P(non A) = 1 − P(A). Si A et B sont <b>incompatibles</b> (ne peuvent pas se produire en même temps), P(A ou B) = P(A) + P(B).",
              "Pour une expérience à <b>deux épreuves</b>, on liste les issues avec un arbre ou un tableau à double entrée.",
              "Sur un arbre, on multiplie les probabilités le long d’un chemin et on additionne les chemins qui conviennent."],
             [("Deux lancers d’une pièce : P(deux piles)", ["issues : PP, PF, FP, FF", "1 issue favorable sur 4"], "1/4")],
             [["Croire que les sommes de deux dés (2 à 12) sont équiprobables", "7 s’obtient de 6 façons, 12 d’une seule."], ["Oublier PF ou FP", "Ce sont deux issues différentes."],
              ["Additionner sur un chemin d’arbre", "On multiplie le long d’un chemin."]])
    faq = [("Comment savoir si deux événements sont incompatibles ?", "Ils n’ont aucune issue en commun : par exemple « obtenir 2 » et « obtenir 5 » avec un dé."),
           ("Arbre ou tableau ?", "Le tableau à double entrée est pratique pour deux dés ; l’arbre convient à toutes les expériences à plusieurs épreuves.")]
    unit("4e", R, "probabilites", "D",
         "Utiliser l’événement contraire et les événements incompatibles ; représenter une expérience à deux épreuves par un arbre ou un tableau ; calculer des probabilités ; dénombrer des issues",
         "Probabilités : événements et expériences à deux épreuves", "Probabilités",
         "Fiches de maths 4e sur les probabilités : événement contraire, événements incompatibles, deux épreuves, arbres, tableaux à double entrée et problèmes. 100 exercices corrigés.",
         "P(non A) = 1 − P(A)", "Sur un arbre, on multiplie le long d’un chemin", body, faq, sets, 18)


if __name__ == "__main__":
    main()
