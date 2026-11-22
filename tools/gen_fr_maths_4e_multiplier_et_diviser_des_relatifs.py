# -*- coding: utf-8 -*-
"""
France Maths 4e : Multiplier et diviser des nombres relatifs
  python3 tools/gen_fr_maths_4e_multiplier_et_diviser_des_relatifs.py
Erreurs : (−3) × (−4) = −12, appliquer la règle des signes de l’addition, oublier les priorités.
"""
import random
from fr_c4 import *

R = random.Random(60301)
K = Kids(R)


def nz(lo, hi):
    while True:
        x = R.randint(lo, hi)
        if x:
            return x


def s1():
    a, b = nz(-12, 12), nz(-12, 12)
    if a > 0 and b > 0:
        a = -a
    if R.random() < 0.25:
        a, b = Fr(nz(-50, 50), 10), nz(-9, 9)
    p = a * b
    return M("Calcule : %s × %s" % (par(a), par(b)), d(p), [d(-p), d(a + b), d(-(abs(a) + abs(b))) if a + b != -(abs(a) + abs(b)) else d(p + 1)],
             "%s : le produit est %s. %s × %s = <b>%s</b>." % ("Signes contraires" if (a < 0) != (b < 0) else "Mêmes signes", "négatif" if p < 0 else "positif", d(abs(a)), d(abs(b)), d(p)))


def s2():
    b, q = nz(-12, 12), nz(-12, 12)
    a = b * q
    if R.random() < 0.3:
        a, b = Fr(b * q, 10), b
        q = a / b
    if a > 0 and b > 0:
        a, q = -a, -q
    k = R.choice(["div", "frac"])
    if k == "frac":
        return M("Calcule : %s" % fr(d(a), d(b)), d(q), [d(-q), d(a - b), d(Fr(b, a)) if Fr(b, a).denominator in (1, 2, 4, 5, 10) else d(q + 1)],
                 "Un quotient se calcule comme un produit pour le signe : %s ÷ %s = <b>%s</b>." % (par(a), par(b), d(q)))
    return M("Calcule : %s ÷ %s" % (par(a), par(b)), d(q), [d(-q), d(a - b), d(a * b) if abs(a * b) < 200 else d(q + 1)],
             "%s : le quotient est %s. <b>%s</b>." % ("Signes contraires" if (a < 0) != (b < 0) else "Mêmes signes", "négatif" if q < 0 else "positif", d(q)))


def s3():
    k = R.choice(["signe", "calc", "puis"])
    if k == "puis":
        a = nz(-5, -1)
        n = R.randint(2, 5)
        r = a ** n
        return M("Calcule : %s<sup>%d</sup>" % (par(a), n), d(r), [d(-r), d(a * n), d(-abs(a) ** n) if r > 0 else d(abs(a) ** n + 1)],
                 "%d facteurs %s : %s → <b>%s</b>." % (n, par(a), "nombre pair de signes −, résultat positif" if n % 2 == 0 else "nombre impair de signes −, résultat négatif", d(r)))
    fs = [nz(-9, 9) for _ in range(R.randint(3, 5))]
    p = 1
    for f in fs:
        p *= f
    neg = sum(1 for f in fs if f < 0)
    if k == "signe":
        return M("Quel est le signe du produit %s ?" % " × ".join(par(f) for f in fs), "positif" if p > 0 else "négatif", ["négatif" if p > 0 else "positif", "on ne peut pas savoir sans calculer", "nul"],
                 "Il y a %s : le produit est <b>%s</b>." % (pl(neg, "facteur négatif", "facteurs négatifs"), "positif" if p > 0 else "négatif"))
    if abs(p) > 2000:
        return None
    return M("Calcule : %s" % " × ".join(par(f) for f in fs), d(p), [d(-p), d(sum(fs)), d(p + fs[0])],
             "%s, donc le signe est %s ; %s = <b>%s</b>." % (pl(neg, "facteur négatif", "facteurs négatifs"), "+" if p > 0 else "−", " × ".join(d(abs(f)) for f in fs), d(p)))


def s4():
    a, b, c = nz(-9, 9), nz(-9, 9), nz(-9, 9)
    k = R.choice(["1", "2", "3", "4"])
    if k == "1":
        e, r, w = "%s + %s × %s" % (d(a), par(b), par(c)), a + b * c, [(a + b) * c, a - b * c, a + b + c]
    elif k == "2":
        e, r, w = "%s × %s − %s" % (par(a), par(b), par(c)), a * b - c, [a * (b - c), a * b + c, -a * b - c]
    elif k == "3":
        e, r, w = "(%s − %s) × %s" % (d(a), par(b), par(c)), (a - b) * c, [a - b * c, (a + b) * c, -(a - b) * c]
    else:
        q = nz(-6, 6)
        e, r, w = "%s − %s ÷ %s" % (d(a), par(b * q), par(b)), a - q, [Fr(a - b * q, b), a + q, -a - q]
    w = [x for x in w if x != r]
    return M("Calcule : %s" % e, d(r), [d(x) for x in w], "On applique les priorités et la règle des signes : <b>%s</b>." % d(r))


def s5():
    p = K.next()
    k = R.choice(["temp", "dette", "plongee", "moy", "jeu"])
    if k == "temp":
        n, t = R.randint(3, 8), R.randint(2, 4)
        t0 = R.randint(-3, 6)
        r = t0 - n * t
        return M("À minuit, il fait %s °C. La température baisse de %d °C par heure pendant %d heures. Quelle température fait-il ensuite ?" % (d(t0), t, n), "%s °C" % d(r),
                 ["%s °C" % d(t0 + n * t), "%s °C" % d(-n * t), "%s °C" % d(t0 - n - t)], "%s + %d × (−%d) = %s − %d = <b>%s °C</b>." % (d(t0), n, t, d(t0), n * t, d(r)))
    if k == "dette":
        n, m = R.randint(3, 12), R.randint(5, 40)
        return M("%s retire %d € chaque semaine pendant %d semaines. De combien son solde a-t-il varié ?" % (p[0], m, n), "%s €" % d(-n * m), ["%s €" % d(n * m), "%s €" % d(-n - m), "%s €" % d(-m)],
                 "%d × (−%d) = <b>%s €</b>." % (n, m, d(-n * m)))
    if k == "plongee":
        a, n = R.randint(2, 6), R.randint(3, 10)
        return M("Un plongeur descend de %d m par minute. Quelle est sa variation d’altitude au bout de %d minutes ?" % (a, n), "%s m" % d(-a * n), ["%s m" % d(a * n), "%s m" % d(-a - n), "%s m" % d(-a)],
                 "%d × (−%d) = <b>%s m</b>." % (n, a, d(-a * n)))
    if k == "moy":
        ts = [R.randint(-8, 4) for _ in range(4)]
        s = sum(ts)
        if s % 4:
            return None
        return M("Températures relevées : %s °C. Quelle est la température moyenne ?" % " ; ".join(d(x) for x in ts), "%s °C" % d(Fr(s, 4)), ["%s °C" % d(Fr(-s, 4)) if s else "1 °C", "%s °C" % d(s), "%s °C" % d(Fr(sum(abs(x) for x in ts), 4)) if Fr(sum(abs(x) for x in ts), 4).denominator in (1, 2, 4) and sum(abs(x) for x in ts) != s else "%s °C" % d(Fr(s, 4) + 1)],
                 "Somme : %s ; %s ÷ 4 = <b>%s °C</b>." % (d(s), par(s), d(Fr(s, 4))))
    g, b_ = R.randint(3, 10), R.randint(3, 10)
    r = g * 3 + b_ * (-2)
    return M("À un quiz, une bonne réponse rapporte +3 points et une mauvaise −2 points. %s a %d bonnes et %d mauvaises réponses. Quel est son score ?" % (p[0], g, b_), d(r),
             [d(g * 3 + b_ * 2), d(g - b_), d((g + b_) * 1)], "%d × 3 + %d × (−2) = %d − %d = <b>%s</b>." % (g, b_, 3 * g, 2 * b_, d(r)))


def main():
    seen = set()
    sets = [("Multiplier deux relatifs", mix(R, seen, [(s1, 20)])), ("Diviser des relatifs", mix(R, seen, [(s2, 20)])),
            ("Produits de plusieurs facteurs et puissances", mix(R, seen, [(s3, 20)])), ("Priorités avec des relatifs", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Pour multiplier ou diviser deux relatifs : on multiplie (ou divise) les distances à zéro, puis on cherche le signe.",
              "<b>Mêmes signes → résultat positif ; signes contraires → résultat négatif.</b>",
              "Pour un produit de plusieurs facteurs : nombre pair de facteurs négatifs → positif ; nombre impair → négatif."],
             [("(−3) × (−4)", ["mêmes signes : positif", "3 × 4 = 12"], "12"), ("(−20) ÷ 5", ["signes contraires : négatif", "20 ÷ 5 = 4"], "−4")],
             [["(−3) × (−4) = −12", "Deux facteurs négatifs donnent un produit positif : 12."], ["Utiliser la règle de l’addition : (−3) × (−4) = −7", "On multiplie les distances à zéro : 12."],
              ["−3 + 4 × (−2) = −2", "La multiplication d’abord : −3 + (−8) = −11."]])
    faq = [("Pourquoi « moins par moins donne plus » ?", "Parce que la multiplication doit rester distributive : (−3) × (−4) + (−3) × 4 = (−3) × 0 = 0, donc (−3) × (−4) = 12."),
           ("Peut-on diviser par un nombre négatif ?", "Oui, avec la même règle des signes. On ne peut jamais diviser par 0.")]
    unit("4e", R, "multiplier-et-diviser-des-relatifs", "N",
         "Multiplier et diviser des nombres relatifs ; connaître et utiliser la règle des signes ; déterminer le signe d’un produit de plusieurs facteurs ; enchaîner des opérations avec des relatifs",
         "Multiplier et diviser des nombres relatifs", "Multiplier et diviser des relatifs",
         "Fiches de maths 4e : multiplier et diviser des nombres relatifs, règle des signes, produits de plusieurs facteurs, priorités, problèmes. 100 exercices corrigés.",
         "Mêmes signes → +, signes contraires → −", "(−3) × (−4) = 12 ; (−20) ÷ 5 = −4", body, faq, sets, 1)


if __name__ == "__main__":
    main()
