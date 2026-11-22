# -*- coding: utf-8 -*-
"""
France Maths 6e : Comparer, ranger, encadrer et arrondir des décimaux
  python3 tools/gen_fr_maths_6e_comparer_ranger_et_arrondir.py
Erreurs : 3,45 &gt; 3,5 car 45 &gt; 5, 2,80 &gt; 2,8, arrondir 4,67 au dixième en 4,6.
"""
import random
from fr_c4 import *

R = random.Random(60102)
K = Kids(R)


def pair():
    a = Fr(R.randint(10, 999), 100)
    k = R.choice(["long", "zero", "near"])
    if k == "long":
        b = Fr(int(a * 10), 10) + Fr(R.randint(1, 9), 10) if R.random() < 0.5 else a + Fr(R.randint(1, 9), 1000)
        b = Fr(int(b * 1000), 1000)
    elif k == "zero":
        b = Fr(int(a * 10) + R.choice([-1, 1, 0]), 10)
    else:
        b = a + Fr(R.choice([-12, -3, 3, 12, 50]), 100)
    if b <= 0:
        return None
    return a, b


def s1():
    p = pair()
    if not p:
        return None
    a, b = p
    if a == b:
        return None
    big = R.random() < 0.6
    ans = d(max(a, b) if big else min(a, b))
    return M("Quel est le plus %s : %s ou %s ?" % ("grand" if big else "petit", d(a), d(b)), ans, [d(min(a, b) if big else max(a, b)), "ils sont égaux", "on ne peut pas savoir"],
             "On compare chiffre par chiffre à partir de la gauche (unités, dixièmes, centièmes…) : <b>%s</b>." % ans)


def s2():
    a = Fr(R.randint(10, 99), 10)
    xs = {a, a + Fr(R.randint(1, 9), 100), a - Fr(1, 10) + Fr(R.randint(1, 9), 100), Fr(int(a), 1) + Fr(R.randint(1, 9), 1000) * 10}
    xs = sorted(x for x in xs if x > 0)
    if len(xs) < 4:
        return None
    xs = xs[:4]
    up = R.random() < 0.5
    good = xs if up else xs[::-1]
    sh = list(xs)
    R.shuffle(sh)
    by_len = sorted(xs, key=lambda x: (len(d(x)), x))
    sep = " &lt; " if up else " &gt; "
    f = lambda l: sep.join(d(x) for x in l)
    bads = [xs[::-1] if up else xs, by_len if up else by_len[::-1], [good[1], good[0], good[2], good[3]]]
    return M("Range dans l’ordre %s : %s" % ("croissant" if up else "décroissant", " ; ".join(d(x) for x in sh)), f(good), [f(b) for b in bads if b != good],
             "On compare les parties entières, puis les dixièmes, puis les centièmes : <b>%s</b>." % f(good))


def s3():
    v = Fr(R.randint(101, 9999), 100)
    if v.denominator == 1:
        return None
    if R.random() < 0.5:
        lo = int(v)
        return M("Entre quels entiers consécutifs se trouve %s ?" % d(v), "%d et %d" % (lo, lo + 1), ["%d et %d" % (lo - 1, lo), "%s et %s" % (d(v - Fr(1, 100)), d(v + Fr(1, 100))), "%d et %d" % (lo + 1, lo + 2)],
                 "La partie entière de %s est %d : <b>%d &lt; %s &lt; %d</b>." % (d(v), lo, lo, d(v), lo + 1))
    lo = Fr(int(v * 10), 10)
    if lo == v:
        return None
    return M("Encadre %s entre deux nombres qui ont un seul chiffre après la virgule et qui se suivent." % d(v), "%s et %s" % (d(lo), d(lo + Fr(1, 10))),
             ["%d et %d" % (int(v), int(v) + 1), "%s et %s" % (d(lo - Fr(1, 10)), d(lo)), "%s et %s" % (d(lo + Fr(1, 10)), d(lo + Fr(2, 10)))],
             "On regarde le chiffre des dixièmes : <b>%s &lt; %s &lt; %s</b>." % (d(lo), d(v), d(lo + Fr(1, 10))))


def rnd(v, k):
    q = v * 10 ** k
    n = int(q)
    if q - n >= Fr(1, 2):
        n += 1
    return Fr(n, 10 ** k)


def s4():
    v = Fr(R.randint(1001, 99999), 1000)
    k = R.choice([0, 1, 2])
    if (v * 10 ** k).denominator == 1:
        return None
    r = rnd(v, k)
    trunc = Fr(int(v * 10 ** k), 10 ** k)
    up = trunc + Fr(1, 10 ** k)
    cand = [(up if r == trunc else trunc, k), (rnd(v, k + 1), k + 1) if k < 2 else (r + Fr(2, 100) * (1 if r == trunc else -1), k), (rnd(v, k - 1), k - 1) if k else (r + 1, 0),
            (r + Fr(1, 10 ** k) * (1 if r == trunc else -1) * 2, k)]
    w = [dk(x, kk) for x, kk in cand if x != r][:3]
    lab = ["à l’unité", "au dixième", "au centième"][k]
    return M("Arrondis %s %s." % (d(v), lab), dk(r, k), w,
             "On regarde le chiffre juste après : s’il vaut 5 ou plus, on arrondit au-dessus. %s arrondi %s : <b>%s</b>." % (d(v), lab, dk(r, k)))


def s5():
    p, q = K.two()
    k = R.choice(["course", "saut", "prix", "taille"])
    if k == "course":
        a = Fr(R.randint(1150, 1499), 100)
        b = a + Fr(R.choice([-9, -1, 1, 9, 10, -10]), 100)
        win = p[0] if a < b else q[0]
        return M("Au 100 m, %s court en %s s et %s en %s s. Qui est le plus rapide ?" % (p[0], d(a), q[0], d(b)), win, [q[0] if win == p[0] else p[0], "ils sont aussi rapides", "on ne peut pas savoir"],
                 "Le plus rapide met le moins de temps : %s &lt; %s, c’est <b>%s</b>." % (d(min(a, b)), d(max(a, b)), win))
    if k == "saut":
        a = Fr(R.randint(250, 450), 100)
        b = Fr(int(a * 10) + R.choice([-1, 1]), 10)
        if a == b:
            return None
        win = p[0] if a > b else q[0]
        return M("Au saut en longueur, %s saute %s m et %s saute %s m. Qui saute le plus loin ?" % (p[0], d(a), q[0], d(b)), win, [q[0] if win == p[0] else p[0], "ils sautent pareil", "on ne peut pas savoir"],
                 "%s %s %s : <b>%s</b>." % (d(max(a, b)), "&gt;", d(min(a, b)), win))
    if k == "prix":
        v = Fr(R.randint(1001, 9999), 100)
        r = rnd(v, 0)
        return M("Un jeu coûte %s €. Quel est son prix arrondi à l’euro près ?" % d(v), "%s €" % d(r), ["%s €" % d(r + 1 if r <= v else r - 1), "%s €" % d(rnd(v, 1)), "%s €" % d(r + 10)],
                 "Arrondi à l’unité : <b>%s €</b>." % d(r))
    a = Fr(R.randint(120, 175), 100)
    xs = sorted({a, a + Fr(R.randint(1, 9), 100), a - Fr(R.randint(1, 9), 100)})
    if len(xs) < 3:
        return None
    nm = [p[0], q[0], K.next()[0]]
    if len(set(nm)) < 3:
        return None
    sh = list(zip(nm, R.sample(xs, 3)))
    tall = max(sh, key=lambda t: t[1])[0]
    return M("%s mesure %s m, %s mesure %s m et %s mesure %s m. Qui est le plus grand ?" % (sh[0][0], d(sh[0][1]), sh[1][0], d(sh[1][1]), sh[2][0], d(sh[2][1])), tall,
             [t[0] for t in sh if t[0] != tall] + ["ils ont la même taille"], "On compare les centièmes : <b>%s</b> est le plus grand." % tall)


def main():
    seen = set()
    sets = [("Comparer deux décimaux", mix(R, seen, [(s1, 20)])), ("Ranger des décimaux", mix(R, seen, [(s2, 20)])),
            ("Encadrer", mix(R, seen, [(s3, 20)])), ("Arrondir", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Pour comparer deux décimaux, on compare d’abord les <b>parties entières</b>, puis les dixièmes, puis les centièmes.",
              "On peut ajouter des zéros à la fin : 3,5 = 3,50. Alors 3,50 &gt; 3,45.",
              "Pour <b>arrondir</b> au dixième, on regarde le chiffre des centièmes : 0 à 4 on garde, 5 à 9 on augmente."],
             [("Compare 3,5 et 3,45", ["3,5 = 3,50", "50 centièmes &gt; 45 centièmes"], "3,5 &gt; 3,45")],
             [["Croire que 3,45 &gt; 3,5 car 45 &gt; 5", "On compare les dixièmes : 4 &lt; 5, donc 3,45 &lt; 3,5."],
              ["Croire que 2,80 &gt; 2,8", "Un zéro à la fin ne change pas le nombre : 2,80 = 2,8."],
              ["Arrondir 4,67 au dixième en 4,6", "Le chiffre des centièmes est 7 : on arrondit à 4,7."]])
    faq = [("Arrondir et tronquer, c’est pareil ?", "Non : tronquer, c’est couper ; arrondir, c’est prendre la valeur la plus proche."),
           ("Comment ranger des décimaux ?", "On écrit tous les nombres avec le même nombre de chiffres après la virgule, puis on compare.")]
    unit("6e", R, "comparer-ranger-et-arrondir", "N",
         "Comparer, ranger, encadrer des nombres décimaux ; donner une valeur approchée (arrondi à l’unité, au dixième, au centième)",
         "Comparer, ranger, encadrer et arrondir", "Comparer et arrondir des décimaux",
         "Fiches de maths 6e pour comparer, ranger, encadrer et arrondir des nombres décimaux, avec des problèmes. 100 exercices corrigés.",
         "3,5 &gt; 3,45 : on compare les dixièmes.", "On peut écrire 3,5 = 3,50.", body, faq, sets, 2)


if __name__ == "__main__":
    main()
