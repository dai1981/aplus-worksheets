# -*- coding: utf-8 -*-
"""
France Maths Seconde : Arithmétique (multiples, diviseurs, parité, nombres premiers, fractions irréductibles)
  python3 tools/gen_fr_maths_seconde_arithmetique.py
Erreurs : 1 est premier, un nombre impair est premier, 2n + 1 n’est pas toujours impair, simplifier sans aller jusqu’au bout.
"""
import random
from math import gcd
from fr_c4 import *

R = random.Random(60501)
K = Kids(R)


def prime(n):
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def factor(n):
    f, k = [], 2
    while n > 1:
        while n % k == 0:
            f.append(k)
            n //= k
        k += 1
    return f


def fstr(f):
    out = []
    for p in sorted(set(f)):
        c = f.count(p)
        out.append("%d%s" % (p, "<sup>%d</sup>" % c if c > 1 else ""))
    return " × ".join(out)


def s1():
    k = R.choice(["mult", "mult", "def", "pair"])
    if k == "mult":
        a = R.choice([3, 4, 6, 7, 9, 11, 12, 13, 15, 17])
        n = a * R.randint(5, 60) + R.choice([0, 0, R.randint(1, a - 1)])
        ok = n % a == 0
        return M("%s est-il un multiple de %d ?" % (num(n), a), "oui" if ok else "non", ["non" if ok else "oui", "seulement si %s est pair" % num(n), "on ne peut pas savoir"],
                 "%s = %d × %d%s : <b>%s</b>." % (num(n), a, n // a, "" if ok else " + %d" % (n % a), "oui" if ok else "non"))
    if k == "def":
        a, kk = R.randint(3, 15), R.randint(2, 20)
        return M("On a %d = %d × %d. Quelle phrase est vraie ?" % (a * kk, a, kk), "%d est un multiple de %d et %d est un diviseur de %d" % (a * kk, a, a, a * kk),
                 ["%d est un multiple de %d" % (a, a * kk), "%d est un diviseur de %d" % (a * kk, a), "%d et %d n’ont aucun lien" % (a, a * kk)],
                 "a est un multiple de b s’il existe un entier k tel que a = kb : <b>%d est un multiple de %d</b>, et %d en est un diviseur." % (a * kk, a, a))
    V = [("Si n est un entier, le nombre 2n est…", "pair", ["impair", "premier", "on ne peut pas savoir"]),
         ("Si n est un entier, le nombre 2n + 1 est…", "impair", ["pair", "premier", "on ne peut pas savoir"]),
         ("La somme de deux nombres impairs est…", "paire", ["impaire", "première", "on ne peut pas savoir"]),
         ("Le produit de deux nombres impairs est…", "impair", ["pair", "premier", "on ne peut pas savoir"]),
         ("Le carré d’un nombre impair est…", "impair", ["pair", "premier", "multiple de 4"]),
         ("Le produit de deux entiers consécutifs n(n + 1) est…", "pair", ["impair", "premier", "un carré"]),
         ("Si a et b sont des multiples de 7, alors a + b est…", "un multiple de 7", ["un multiple de 14", "impair", "premier"]),
         ("La somme de trois entiers consécutifs est toujours un multiple de…", "3", ["2", "6", "9"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s2():
    k = R.choice(["prem", "prem", "liste", "plus"])
    if k == "prem":
        n = R.randint(2, 120)
        ok = prime(n)
        if not ok and R.random() < 0.4:
            return None
        d_ = next((k for k in range(2, n) if n % k == 0), None)
        return M("%d est-il un nombre premier ?" % n, "oui" if ok else "non", ["non" if ok else "oui", "oui, car il est impair" if n % 2 else "non, car il est pair" if ok else "oui, car il est pair", "on ne peut pas savoir"],
                 "%s" % ("%d n’a que deux diviseurs, 1 et lui-même : <b>oui</b>." % n if ok else "%d est divisible par %d : <b>non</b>." % (n, d_)))
    if k == "liste":
        lo = R.choice([10, 20, 30, 40, 50, 60, 70, 80, 90])
        ps = [x for x in range(lo, lo + 10) if prime(x)]
        ans = ", ".join(map(str, ps)) if ps else "aucun"
        imp = [x for x in range(lo, lo + 10) if x % 2]
        return M("Quels sont les nombres premiers entre %d et %d ?" % (lo, lo + 9), ans, [", ".join(map(str, imp)), ", ".join(map(str, ps + [x for x in imp if x % 5 and not prime(x)][:1])) if [x for x in imp if x % 5 and not prime(x)] else "%d" % (lo + 1), ", ".join(map(str, ps[:-1])) if len(ps) > 1 else "%d" % (lo + 3)],
                 "On teste les nombres impairs : <b>%s</b>." % ans)
    V = [("Le nombre 1 est-il premier ?", "non, il n’a qu’un seul diviseur", ["oui", "oui, car il ne se divise que par lui-même", "on ne peut pas savoir"]),
         ("Quel est le seul nombre premier pair ?", "2", ["0", "4", "il n’y en a pas"]),
         ("Pour savoir si 97 est premier, jusqu’à quel nombre suffit-il de tester les diviseurs ?", "9 (car 10² &gt; 97)", ["48", "97", "50"]),
         ("Un nombre premier a exactement…", "deux diviseurs", ["un diviseur", "trois diviseurs", "un nombre impair de diviseurs"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s3():
    n = R.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 72, 75, 84, 90, 96, 98, 100, 108, 120, 126, 140, 150, 168, 180, 196, 210, 225, 252, 300, 360])
    f = factor(n)
    ans = fstr(f)
    w = [fstr(f[:-1] + [f[-1] * 2]) if len(f) > 1 and f[-1] * 2 != f[-1] else "2 × %d" % (n // 2), " × ".join(map(str, sorted(set(f)))) if len(set(f)) != len(f) else fstr(f + [2]), "%d × %d" % (f[0] * f[1] if len(f) > 2 else f[0], n // (f[0] * f[1] if len(f) > 2 else f[0]))]
    return M("Quelle est la décomposition de %d en produit de facteurs premiers ?" % n, ans, w, "On divise par 2, 3, 5, 7… : %d = <b>%s</b>." % (n, ans))


def s4():
    a, b = R.randint(2, 30), R.randint(2, 30)
    g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15])
    if gcd(a, b) != 1 or a == b:
        return None
    x, y = a * g, b * g
    k = R.choice(["irr", "irr", "dec"])
    if k == "irr":
        return M("Écris %s sous forme irréductible." % fr(x, y), fq(Fr(x, y)), [fr(x // 2, y // 2) if g % 2 == 0 and g != 2 else fr(b, a), fr(a + 1, b), fr(a, b + 1)],
                 "%s = %s et %s : <b>%s</b>." % (fr(x, y), fr("%s × %d" % (fstr(factor(a)) if a > 1 else "1", g), "%s × %d" % (fstr(factor(b)), g)), "on simplifie par %d" % g, fq(Fr(x, y))))
    n = R.choice([3, 6, 7, 9, 11, 12, 15, 8, 20, 25, 40, 16])
    m = R.randint(1, n - 1)
    if gcd(m, n) != 1:
        return None
    dec = all(p in (2, 5) for p in factor(n))
    return M("Le nombre %s est-il un nombre décimal ?" % fr(m, n), "non" if not dec else "oui", ["oui" if not dec else "non", "oui, la calculatrice affiche un résultat", "on ne peut pas savoir"],
             ("Sous forme irréductible, le dénominateur %d a un facteur premier autre que 2 et 5 : <b>non</b>, son écriture décimale est illimitée." % n) if not dec else
             "Le dénominateur %d = %s n’a que 2 et 5 comme facteurs premiers : <b>oui</b>, %s = %s." % (n, fstr(factor(n)), fr(m, n), d(Fr(m, n))))


def s5():
    k = R.choice(["paquets", "engrenage", "demo", "carre"])
    if k == "paquets":
        g = R.choice([6, 8, 9, 12, 14, 15, 18])
        a, b = R.randint(2, 9), R.randint(2, 9)
        if gcd(a, b) != 1 or a == b:
            return None
        return M("On veut répartir %d billes rouges et %d billes bleues en paquets identiques, le plus grand nombre de paquets possible. Combien de paquets ?" % (a * g, b * g), str(g), [str(a * b * g), str(a + b), str(g // 2) if g % 2 == 0 else str(g * 2)],
                 "Le nombre de paquets divise %d et %d ; le plus grand diviseur commun est <b>%d</b>." % (a * g, b * g, g))
    if k == "engrenage":
        a, b = R.choice([(12, 18), (8, 12), (10, 15), (14, 21), (6, 15), (20, 30), (9, 12)])
        l = a * b // gcd(a, b)
        return M("Deux roues dentées ont %d et %d dents. Au bout de combien de dents passées se retrouvent-elles pour la première fois dans la même position ?" % (a, b), str(l), [str(a * b), str(gcd(a, b)), str(a + b)],
                 "C’est le plus petit multiple commun à %d et %d : <b>%d</b>." % (a, b, l))
    if k == "carre":
        n = R.choice([12, 18, 20, 24, 45, 50, 72, 98, 75])
        f = factor(n)
        m = 1
        for p in set(f):
            if f.count(p) % 2:
                m *= p
        return M("Par quel plus petit entier faut-il multiplier %d pour obtenir un carré parfait ?" % n, str(m), [str(n), str(m * 2) if m * 2 != n else str(m + 1), "2" if m != 2 else "3"],
                 "%d = %s : il faut des exposants pairs, on multiplie par <b>%d</b> (%d × %d = %d = %d²)." % (n, fstr(f), m, n, m, n * m, int((n * m) ** 0.5)))
    V = [("Pour démontrer que la somme de deux multiples de 5 est un multiple de 5, on écrit…", "5k + 5k’ = 5(k + k’)", ["5 + 5 = 10", "5k + 5k = 10k", "on vérifie sur deux exemples"]),
         ("Pour démontrer que le carré d’un nombre impair est impair, on part de…", "n = 2k + 1, donc n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1", ["n = 2k, donc n² = 4k²", "3² = 9 est impair", "n² = 2k + 1"]),
         ("n est un entier. (n + 1)² − n² est toujours…", "impair", ["pair", "premier", "égal à 1"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Multiples, diviseurs et parité", mix(R, seen, [(s1, 20)])), ("Nombres premiers", mix(R, seen, [(s2, 20)])),
            ("Décomposition en facteurs premiers", mix(R, seen, [(s3, 20)])), ("Fractions irréductibles et décimaux", mix(R, seen, [(s4, 20)])), ("Problèmes et démonstrations", mix(R, seen, [(s5, 20)]))]
    body = L(["a est un <b>multiple</b> de b (et b un <b>diviseur</b> de a) s’il existe un entier k tel que a = kb. Un nombre pair s’écrit 2k, un nombre impair 2k + 1.",
              "Un nombre <b>premier</b> a exactement deux diviseurs : 1 et lui-même (1 n’est pas premier). Tout entier ≥ 2 se décompose en produit de facteurs premiers.",
              "Une fraction est irréductible quand numérateur et dénominateur n’ont pas de facteur premier commun."],
             [("Décomposer 180", ["180 = 2 × 90 = 2 × 2 × 45", "45 = 3 × 3 × 5"], "2² × 3² × 5")],
             [["Dire que 1 est premier", "1 n’a qu’un diviseur : il n’est pas premier."], ["Dire qu’un nombre impair est premier (9, 15, 21…)", "Il faut tester ses diviseurs."],
              ["Démontrer avec des exemples", "On utilise une écriture littérale : 2k, 2k + 1, 5k…"]])
    faq = [("Jusqu’où tester pour savoir si n est premier ?", "Il suffit de tester les nombres premiers dont le carré est inférieur ou égal à n."),
           ("À quoi sert la décomposition en facteurs premiers ?", "À simplifier des fractions, trouver des diviseurs communs ou reconnaître un carré.")]
    unit("seconde", R, "arithmetique", "N",
         "Utiliser les notions de multiple, diviseur, nombre pair, nombre impair et nombre premier pour modéliser et résoudre des problèmes ; décomposer en facteurs premiers ; rendre une fraction irréductible ; démontrer des propriétés simples",
         "Arithmétique : multiples, diviseurs et nombres premiers", "Arithmétique",
         "Fiches de maths seconde sur l’arithmétique : multiples, diviseurs, parité, nombres premiers, décomposition, fractions irréductibles et démonstrations. 100 exercices corrigés.",
         "a = kb : a est un multiple de b", "Un nombre premier a exactement deux diviseurs", body, faq, sets, 1)


if __name__ == "__main__":
    main()
