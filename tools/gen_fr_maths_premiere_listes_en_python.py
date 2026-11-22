# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Listes en Python (création en extension, par ajouts, en compréhension ; indices ; len ; parcours ; listes de termes d’une suite, sommes, moyenne, simulation)
  python3 tools/gen_fr_maths_premiere_listes_en_python.py
Erreurs : le premier indice est 0 (pas 1), L[len(L)] n’existe pas, range(1, n) s’arrête à n − 1, append ajoute à la fin, confondre la valeur et l’indice.
"""
import random
from fr_ly1 import *

R = random.Random(60624)


def lst(v):
    return "[%s]" % ", ".join(str(x) for x in v)


def s1():
    L_ = R.sample(range(0, 40), R.randint(4, 7))
    k = R.choice(["idx", "idx", "neg", "len", "last"])
    if k == "idx":
        i = R.randint(0, len(L_) - 1)
        return M("L = %s. Que vaut L[%d] ?" % (lst(L_), i), str(L_[i]), [str(L_[i - 1]) if i > 0 else str(L_[1]), str(L_[i + 1]) if i + 1 < len(L_) else str(L_[0]), str(i)],
                 "Les indices commencent à 0 : L[%d] est le %s élément, <b>%d</b>." % (i, "1<sup>er</sup>" if i == 0 else "%d<sup>e</sup>" % (i + 1), L_[i]))
    if k == "neg":
        return M("L = %s. Que vaut L[-1] ?" % lst(L_), str(L_[-1]), [str(L_[0]), str(L_[-2]), "une erreur"], "L[-1] est le dernier élément : <b>%d</b>." % L_[-1])
    if k == "len":
        return M("L = %s. Que vaut len(L) ?" % lst(L_), str(len(L_)), [str(len(L_) - 1), str(sum(L_)), str(max(L_))], "len(L) est le nombre d’éléments : <b>%d</b>." % len(L_))
    return M("L = %s. Quelle instruction donne le dernier élément ?" % lst(L_), "L[%d]" % (len(L_) - 1), ["L[%d]" % len(L_), "L[1]" if len(L_) > 2 else "L[0]", "L[%d]" % L_[-1] if L_[-1] not in (len(L_) - 1, len(L_), 1) else "L[0]", "L[len(L)]"],
             "Il y a %d éléments, d’indices 0 à %d : <b>L[%d]</b> (ou L[-1]). L[%d] provoque une erreur." % (len(L_), len(L_) - 1, len(L_) - 1, len(L_)))


def s2():
    k = R.choice(["comp", "comp", "comp2", "range", "cond"])
    if k == "comp":
        a, b, n = R.randint(2, 5), R.randint(1, 5), R.randint(3, 6)
        v = [a * i + b for i in range(n)]
        return M("Que contient L ?%s" % code("L = [%d * k + %d for k in range(%d)]" % (a, b, n) if b >= 0 else "L = [%d * k - %d for k in range(%d)]" % (a, -b, n)), lst(v),
                 [lst([a * i + b for i in range(1, n + 1)]), lst([a * i + b for i in range(n + 1)]), lst([a * i for i in range(n)])],
                 "k prend les valeurs 0 à %d : <b>%s</b>." % (n - 1, lst(v)))
    if k == "comp2":
        n = R.randint(3, 6)
        v = [i * i for i in range(1, n + 1)]
        return M("Que contient L ?%s" % code("L = [k ** 2 for k in range(1, %d)]" % (n + 1)), lst(v), [lst([i * i for i in range(n)]), lst([2 * i for i in range(1, n + 1)]), lst([i * i for i in range(1, n + 2)])],
                 "k va de 1 à %d (range s’arrête avant %d) : <b>%s</b>." % (n, n + 1, lst(v)))
    if k == "range":
        a, b = R.randint(0, 4), R.randint(7, 13)
        st = R.choice([1, 2, 3])
        v = list(range(a, b, st))
        return M("Que contient list(range(%d, %d%s)) ?" % (a, b, ", %d" % st if st > 1 else ""), lst(v), [lst(list(range(a, b + 1, st))), lst(list(range(a + 1, b + 1, st))), lst(list(range(a, b)) if st > 1 else list(range(1, b)))],
                 "On commence à %d, on avance de %d et on s’arrête <b>avant</b> %d : <b>%s</b>." % (a, st, b, lst(v)))
    L_ = R.sample(range(0, 25), 6)
    s_ = R.randint(3, 15)
    v = [x for x in L_ if x > s_]
    return M("L = %s. Que contient M ?%s" % (lst(L_), code("M = [x for x in L if x > %d]" % s_)), lst(v), [lst([x for x in L_ if x >= s_]) if s_ in L_ else lst([x for x in L_ if x < s_]), lst([x for x in L_ if x < s_]), lst([i for i, x in enumerate(L_) if x > s_])],
             "On garde les éléments strictement supérieurs à %d, dans l’ordre : <b>%s</b>." % (s_, lst(v)))


def s3():
    k = R.choice(["append", "append", "loop_sum", "count", "modif"])
    if k == "append":
        a = R.randint(1, 4)
        n = R.randint(3, 5)
        L_ = []
        for i in range(n):
            L_.append(a * i)
        return M("Que contient L à la fin ?%s" % code("L = []", "for i in range(%d):" % n, "    L.append(%d * i)" % a), lst(L_), [lst([a * i for i in range(1, n + 1)]), lst([a * i for i in range(n - 1)]), "[%d]" % (a * (n - 1))],
                 "À chaque tour, append ajoute %d × i à la fin : <b>%s</b>." % (a, lst(L_)))
    if k == "loop_sum":
        L_ = R.sample(range(1, 20), R.randint(4, 6))
        return M("L = %s. Que vaut s à la fin ?%s" % (lst(L_), code("s = 0", "for x in L:", "    s = s + x")), str(sum(L_)), [str(len(L_)), str(sum(L_) - L_[-1]), str(sum(range(len(L_))))],
                 "On ajoute chaque élément : s = <b>%d</b> (comme sum(L))." % sum(L_))
    if k == "count":
        L_ = [R.randint(1, 6) for _ in range(R.randint(6, 9))]
        t = R.choice(L_)
        c = L_.count(t)
        return M("L = %s. Que vaut c à la fin ?%s" % (lst(L_), code("c = 0", "for x in L:", "    if x == %d:" % t, "        c = c + 1")), str(c), [str(t), str(len(L_)), str(c + 1), str(L_.index(t))],
                 "c compte les éléments égaux à %d : <b>%d</b>." % (t, c))
    L_ = R.sample(range(1, 15), 5)
    i, v = R.randint(0, 4), R.randint(20, 40)
    L2 = list(L_)
    L2[i] = v
    return M("L = %s. Que contient L après l’instruction L[%d] = %d ?" % (lst(L_), i, v), lst(L2), [lst(L_[:i] + [v] + L_[i:]), lst(L_ + [v]), lst(L_[:i + 1] + [v] + L_[i + 2:]) if i < 4 else lst([v] + L_[1:])],
             "L’élément d’indice %d est remplacé (la liste garde 5 éléments) : <b>%s</b>." % (i, lst(L2)))


def s4():
    k = R.choice(["suite", "suite", "geo", "moy"])
    if k == "suite":
        u0, r, n = R.randint(1, 9), R.randint(2, 5), R.randint(4, 6)
        v = [u0 + r * i for i in range(n)]
        return M("Que contient L à la fin ?%s" % code("u = %d" % u0, "L = [u]", "for k in range(%d):" % (n - 1), "    u = u + %d" % r, "    L.append(u)"), lst(v), [lst(v[1:] + [v[-1] + r]), lst(v[:-1]), lst([u0 + r * i for i in range(n + 1)])],
                 "L contient u<sub>0</sub> puis les %d termes suivants : <b>%s</b>." % (n - 1, lst(v)))
    if k == "geo":
        u0, q, n = R.randint(2, 3), R.choice([2, 3]), R.randint(4, 5)
        v = [u0 * q ** i for i in range(n)]
        return M("Que contient L ?%s" % code("L = [%d * %d ** n for n in range(%d)]" % (u0, q, n)), lst(v), [lst([(u0 * q) ** i for i in range(n)]), lst([u0 * q * i for i in range(n)]), lst([u0 * q ** i for i in range(1, n + 1)]), lst([u0 * q ** i for i in range(n - 1)]), lst([u0 + q * i for i in range(n)])],
                 "Termes u<sub>0</sub> à u<sub>%d</sub> de la suite géométrique : <b>%s</b>." % (n - 1, lst(v)))
    L_ = [R.randint(5, 20) for _ in range(R.choice([4, 5]))]
    m = Fr(sum(L_), len(L_))
    return M("L = %s. Que renvoie moyenne(L) ?%s" % (lst(L_), code("def moyenne(L):", "    return sum(L) / len(L)")), d(m).replace(",", "."), [str(sum(L_)), d(Fr(sum(L_), len(L_) - 1)).replace(",", ".") if Fr(sum(L_), len(L_) - 1).denominator in (1, 2, 4, 5, 8) else str(len(L_)), str(max(L_))],
             "sum(L) = %d et len(L) = %d : %d / %d = <b>%s</b> (Python écrit le point décimal)." % (sum(L_), len(L_), sum(L_), len(L_), d(m).replace(",", ".")))


def s5():
    k = R.choice(["max", "max", "idx_max", "freq", "fib"])
    if k == "max":
        L_ = R.sample(range(0, 40), 6)
        return M("L = %s. Que renvoie f(L) ?%s" % (lst(L_), code("def f(L):", "    m = L[0]", "    for x in L:", "        if x > m:", "            m = x", "    return m")), str(max(L_)),
                 [str(min(L_)), str(L_[0]) if L_[0] != max(L_) else str(L_[-1]), str(L_.index(max(L_))), str(sorted(L_)[-2]), str(L_[-1])], "f garde le plus grand élément rencontré : <b>%d</b> (le maximum)." % max(L_))
    if k == "idx_max":
        L_ = R.sample(range(1, 50), 6)
        i = L_.index(max(L_))
        return M("L = %s. Que renvoie g(L) ?%s" % (lst(L_), code("def g(L):", "    j = 0", "    for i in range(len(L)):", "        if L[i] > L[j]:", "            j = i", "    return j")), str(i),
                 [str(max(L_)), str(i + 1), str(len(L_) - 1) if i != len(L_) - 1 else "0", str(L_.index(min(L_))), str(len(L_))], "g renvoie l’<b>indice</b> du maximum : %d est à l’indice <b>%d</b>." % (max(L_), i))
    if k == "freq":
        n = R.choice([1000, 10000])
        p = R.choice(["1/6", "1/2"])
        return M("Que renvoie approximativement ce programme ?%s" % code("from random import randint", "L = [randint(1, 6) for i in range(%d)]" % n, "print(L.count(6) / len(L))"), "une valeur proche de 0,17 (fréquence des 6)",
                 ["exactement 6", "une valeur proche de %d" % (n // 6), "une valeur proche de 0,5"], "On simule %s lancers de dé et on calcule la fréquence des 6 : elle est proche de 1/6 ≈ <b>0,17</b>." % num(n))
    n = R.randint(6, 9)
    F = [1, 1]
    while len(F) < n:
        F.append(F[-1] + F[-2])
    return M("Que contient F à la fin ?%s" % code("F = [1, 1]", "while len(F) < %d:" % n, "    F.append(F[-1] + F[-2])"), lst(F), [lst(F[:-1]), lst(F + [F[-1] + F[-2]]), lst([1] + [2 ** i for i in range(n - 1)])],
             "Chaque nouveau terme est la somme des deux derniers (suite de Fibonacci), jusqu’à %d éléments : <b>%s</b>." % (n, lst(F)))


def main():
    seen = set()
    sets = [("Indices et longueur", mix(R, seen, [(s1, 20)])), ("Listes en compréhension et range", mix(R, seen, [(s2, 20)])),
            ("Ajouter, parcourir, modifier", mix(R, seen, [(s3, 20)])), ("Listes et suites", mix(R, seen, [(s4, 20)])), ("Algorithmes sur les listes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une liste se crée <b>en extension</b> (L = [3, 5, 8]), <b>par ajouts</b> (L = [] puis L.append(x)) ou <b>en compréhension</b> (L = [k ** 2 for k in range(5)]).",
              "Les indices commencent à <b>0</b> : L[0] est le premier élément, L[len(L) − 1] (ou L[-1]) le dernier. len(L) donne le nombre d’éléments.",
              "On parcourt une liste par ses éléments (for x in L) ou par ses indices (for i in range(len(L))). range(a, b) va de a à b − 1."],
             [("L = [2 * k + 1 for k in range(4)]", ["k = 0, 1, 2, 3", "2k + 1 = 1, 3, 5, 7"], "L = [1, 3, 5, 7]")],
             [["L[1] est le premier élément", "C’est L[0] ; L[1] est le deuxième."], ["range(1, 5) va jusqu’à 5", "Il s’arrête à 4."], ["L[len(L)] est le dernier élément", "Il n’existe pas : le dernier est L[len(L) − 1]."]])
    faq = [("Pourquoi utiliser des listes en mathématiques ?", "Pour stocker les termes d’une suite, des résultats de simulation ou des données statistiques, puis calculer une somme, une moyenne, un maximum ou une fréquence."),
           ("Quelle différence entre L.append(x) et L[i] = x ?", "append ajoute x à la fin (la liste s’allonge) ; L[i] = x remplace l’élément d’indice i (même longueur).")]
    unit("premiere", R, "listes-en-python", "P",
         "Générer une liste en extension, par ajouts successifs ou en compréhension ; manipuler des éléments et des indices ; parcourir une liste ; itérer sur les éléments ; utiliser des listes pour les termes d’une suite, des simulations et des statistiques",
         "Listes en Python", "Listes en Python",
         "Fiches de maths première sur les listes en Python : indices, len, append, listes en compréhension, parcours, termes de suites, moyenne, maximum et simulations. 100 exercices corrigés.",
         "Le premier indice d’une liste est 0", "L = [f(k) for k in range(n)]", body, faq, sets, 24)


if __name__ == "__main__":
    main()
