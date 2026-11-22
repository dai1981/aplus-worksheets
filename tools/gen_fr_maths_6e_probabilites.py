# -*- coding: utf-8 -*-
"""
France Maths 6e : Probabilités (situations d’équiprobabilité)
  python3 tools/gen_fr_maths_6e_probabilites.py
Vocabulaire (certain, impossible, probable), probabilité avec un dé, une urne, une roue, des cartes ; comparer des chances.
Erreurs : écrire le nombre de cas favorables sans diviser, croire qu’un 6 est plus rare, comparer des effectifs au lieu de proportions.
"""
import random
from math import gcd
from fr_c4 import *

R = random.Random(60122)
K = Kids(R)
COUL = ["rouges", "bleues", "vertes", "jaunes", "noires"]


def P(a, b):
    return fr(a, b)


def s1():
    V = [("Obtenir 7 en lançant un dé à six faces", "impossible"), ("Obtenir un nombre entre 1 et 6 avec un dé à six faces", "certain"),
         ("Tirer une boule rouge dans un sac qui ne contient que des boules rouges", "certain"), ("Tirer une boule verte dans un sac qui ne contient que des boules bleues", "impossible"),
         ("Obtenir pile en lançant une pièce", "une chance sur deux"), ("Obtenir un nombre pair avec un dé à six faces", "une chance sur deux"),
         ("Qu’il fasse jour à midi demain", "certain"), ("Obtenir 0 avec un dé à six faces", "impossible"),
         ("Tirer un as dans un jeu de 32 cartes", "possible, mais peu probable"), ("Obtenir 6 avec un dé à six faces", "possible, mais peu probable"),
         ("Tirer une boule bleue dans un sac de 9 boules bleues et 1 rouge", "très probable"), ("Tirer la boule rouge dans un sac de 9 boules bleues et 1 rouge", "possible, mais peu probable"),
         ("Obtenir un nombre plus petit que 6 avec un dé à six faces", "très probable"), ("Obtenir face en lançant une pièce", "une chance sur deux")]
    ev, a = R.choice(V)
    return M("« %s » : cet événement est…" % ev, a, [x for x in ["certain", "impossible", "une chance sur deux", "très probable", "possible, mais peu probable"] if x != a][:3],
             "Réponse : <b>%s</b>." % a)


def s2():
    n = R.choice([6, 6, 8, 10, 12, 20])
    k = R.choice(["num", "pair", "impair", "plus", "mult3", "moins"])
    if k == "num":
        v = R.randint(1, n)
        fav, ev = [v], "obtenir %d" % v
    elif k == "pair":
        fav, ev = [x for x in range(1, n + 1) if x % 2 == 0], "obtenir un nombre pair"
    elif k == "impair":
        fav, ev = [x for x in range(1, n + 1) if x % 2], "obtenir un nombre impair"
    elif k == "plus":
        m = R.randint(2, n - 2)
        fav, ev = list(range(m + 1, n + 1)), "obtenir un nombre strictement plus grand que %d" % m
    elif k == "mult3":
        fav, ev = [x for x in range(1, n + 1) if x % 3 == 0], "obtenir un multiple de 3"
    else:
        m = R.randint(2, n - 2)
        fav, ev = list(range(1, m + 1)), "obtenir un nombre inférieur ou égal à %d" % m
    f = len(fav)
    lst = ", ".join(map(str, fav)) if f <= 10 else "%d nombres" % f
    return M("On lance un dé équilibré à %d faces numérotées de 1 à %d. Quelle est la probabilité d’%s ?" % (n, n, ev), P(f, n), [P(1, n) if f > 1 else P(1, 2), P(f, n - f) if n - f > 0 and n - f != n else P(f + 1, n), P(n - f, n) if n - f != f else P(f + 1, n)],
             "%d issues équiprobables ; issues favorables : %s. Probabilité : <b>%s</b>." % (n, lst, P(f, n)))


def s3():
    cs = R.sample(COUL, 3)
    ns = [R.randint(1, 9) for _ in cs]
    t = sum(ns)
    i = R.randrange(3)
    k = R.choice(["une", "pas"])
    desc = ", ".join("%d boule%s %s" % (n, "s" if n > 1 else "", c if n > 1 else c[:-1]) for n, c in zip(ns, cs))
    if k == "une":
        return M("Un sac contient %s. On tire une boule au hasard. Quelle est la probabilité qu’elle soit %s ?" % (desc, cs[i][:-1]), P(ns[i], t), [P(ns[i], t - ns[i]) if t - ns[i] else P(1, 2), P(1, 3), P(ns[i], 10) if t != 10 else P(ns[i] + 1, t)],
                 "%d boules en tout, dont %d %s : <b>%s</b>." % (t, ns[i], cs[i] if ns[i] > 1 else cs[i][:-1], P(ns[i], t)))
    return M("Un sac contient %s. On tire une boule au hasard. Quelle est la probabilité qu’elle ne soit pas %s ?" % (desc, cs[i][:-1]), P(t - ns[i], t), [P(ns[i], t), P(t - ns[i], ns[i]), P(2, 3)],
             "%d boules ne sont pas %s sur %d : <b>%s</b>." % (t - ns[i], cs[i], t, P(t - ns[i], t)))


def s4():
    p, q = K.two()
    a1, b1 = R.randint(1, 6), R.randint(1, 9)
    m = R.choice([2, 3])
    a2, b2 = a1 * m + R.choice([-1, 1]), b1 * m + R.choice([-1, 0, 1])
    if a2 <= 0 or b2 <= 0 or Fr(a1, a1 + b1) == Fr(a2, a2 + b2):
        return None
    win = p[0] if Fr(a1, a1 + b1) > Fr(a2, a2 + b2) else q[0]
    return M("On gagne si on tire une boule rouge. Le sac %s contient %s et %s ; celui %s, %s et %s. Qui a le plus de chances de gagner ?" % (
                 de_n(p[0]), pl(a1, "rouge"), pl(b1, "bleue"), de_n(q[0]), pl(a2, "rouge"), pl(b2, "bleue")), win,
             [q[0] if win == p[0] else p[0], "ils ont autant de chances", "on ne peut pas savoir"],
             "On compare les proportions : %s et %s. <b>%s</b> a le plus de chances." % (P(a1, a1 + b1), P(a2, a2 + b2), win))


def s5():
    k = R.choice(["roue", "cartes", "lettres", "piece"])
    if k == "roue":
        n = R.choice([4, 5, 8, 10])
        r = R.randint(1, n - 1)
        return M("Une roue est partagée en %d secteurs égaux. %s, les autres blancs. Quelle est la probabilité de tomber sur un secteur rouge ?" % (n, "1 est rouge" if r == 1 else "%d sont rouges" % r), P(r, n), [P(n - r, n) if n - r != r else P(r + 1, n), P(r, n - r) if n - r != r else P(1, n), P(1, r) if r > 1 else P(2, n)],
                 "%d secteurs égaux, %s : <b>%s</b>." % (n, pl(r, "rouge"), P(r, n)))
    if k == "cartes":
        V = [("un cœur", 8, "Il y a 8 cœurs"), ("un roi", 4, "Il y a 4 rois"), ("une carte rouge", 16, "Il y a 16 cartes rouges"), ("le roi de cœur", 1, "Il y a 1 roi de cœur"), ("une figure (valet, dame ou roi)", 12, "Il y a 12 figures")]
        ev, n, why = R.choice(V)
        return M("On tire une carte au hasard dans un jeu de 32 cartes. Quelle est la probabilité de tirer %s ?" % ev, P(n, 32), [P(1, n) if n > 1 else P(1, 4), P(n, 52), P(32 - n, 32)],
                 "%s sur 32 : <b>%s</b>." % (why, P(n, 32)))
    if k == "lettres":
        w = R.choice(["MATHEMATIQUES", "PROBABILITE", "ANANAS", "BANANE", "COLLEGE", "PARALLELE"])
        l = R.choice(sorted(set(w)))
        n = w.count(l)
        return M("On écrit chaque lettre du mot %s sur un carton et on tire un carton au hasard. Quelle est la probabilité de tirer la lettre %s ?" % (w, l), P(n, len(w)),
                 [P(1, len(set(w))), P(n, 26), P(len(w) - n, len(w))], "%d lettres, dont %d « %s » : <b>%s</b>." % (len(w), n, l, P(n, len(w))))
    return M("On lance une pièce équilibrée. Elle vient de tomber 5 fois sur pile. Quelle est la probabilité d’obtenir pile au prochain lancer ?", P(1, 2), [P(5, 6), P(1, 6), "0"],
             "La pièce n’a pas de mémoire : la probabilité reste <b>%s</b>." % P(1, 2))


def main():
    seen = set()
    sets = [("Certain, impossible, probable", mix(R, seen, [(s1, 14), (s5, 6)])), ("Lancer un dé", mix(R, seen, [(s2, 20)])),
            ("Tirer une boule", mix(R, seen, [(s3, 20)])), ("Comparer des chances", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une expérience est <b>aléatoire</b> quand on ne peut pas prévoir le résultat. Les résultats possibles s’appellent les <b>issues</b>.",
              "Quand les issues ont toutes la même chance (équiprobabilité) : probabilité = nombre d’issues favorables ÷ nombre total d’issues.",
              "Une probabilité est entre 0 (impossible) et 1 (certain)."],
             [("Dé à 6 faces : obtenir 5 ou 6", ["2 issues favorables sur 6"], "%s" % fr(2, 6))],
             [["Donner seulement le nombre de cas favorables", "On divise par le nombre total d’issues : 2 sur 6, c’est %s." % fr(2, 6)],
              ["Croire que le 6 est plus difficile à obtenir", "Avec un dé équilibré, chaque face a la même chance."],
              ["Comparer le nombre de boules rouges au lieu des proportions", "3 rouges sur 4 (%s) est mieux que 5 rouges sur 10 (%s)." % (fr(3, 4), fr(5, 10))]])
    faq = [("Une probabilité peut-elle être plus grande que 1 ?", "Non : elle est toujours comprise entre 0 et 1."),
           ("Que veut dire équiprobable ?", "Toutes les issues ont la même probabilité, comme les faces d’un dé équilibré.")]
    unit("6e", R, "probabilites", "D",
         "Reconnaître une expérience aléatoire ; utiliser le vocabulaire (issue, certain, impossible) ; calculer des probabilités dans des situations d’équiprobabilité ; comparer des chances",
         "Les probabilités", "Probabilités",
         "Fiches de maths 6e sur les probabilités : certain, impossible, dé, urne, roue, cartes et comparer des chances. 100 exercices corrigés.",
         "Probabilité = cas favorables ÷ cas possibles", "Entre 0 (impossible) et 1 (certain).", body, faq, sets, 22)


if __name__ == "__main__":
    main()
