# -*- coding: utf-8 -*-
"""
France Maths 6e : Multiplier des nombres décimaux
  python3 tools/gen_fr_maths_6e_multiplication_de_decimaux.py
× 10, 100, 1 000 et × 0,1 ; décimal × entier ; décimal × décimal ; ordre de grandeur ; problèmes.
Erreurs : 3,5 × 10 = 3,50, mal placer la virgule (2,5 × 1,2 = 30 ou 0,3), croire qu’un produit est toujours plus grand.
"""
import random
from fr_c4 import *

R = random.Random(60104)
K = Kids(R)


def rv(lo, hi, k):
    return Fr(R.randint(lo * 10 ** k, hi * 10 ** k), 10 ** k)


def s1():
    a = rv(0, 99, R.choice([1, 2, 3]))
    if a.denominator == 1 or a == 0:
        return None
    m = R.choice([10, 100, 1000])
    r = a * m
    return M("%s %s %s = …" % (d(a), FOIS, num(m)), d(r), [d(a * m * 10), d(a * m / 10), d(a) + "0" if "," in d(a) else d(a * 10)],
             "Multiplier par %s, c’est rendre chaque chiffre %s fois plus grand : la virgule se déplace de %d rang%s vers la droite. <b>%s</b>." % (num(m), num(m), len(str(m)) - 1, "s" if m > 10 else "", d(r)))


def s2():
    a = rv(1, 60, R.choice([1, 2]))
    n = R.randint(2, 9)
    if a.denominator == 1:
        return None
    r = a * n
    k = len(d(a).split(",")[1])
    wrong = Fr(int(a * 10 ** k) * n, 10 ** (k + 1))
    return M("%s %s %d = …" % (d(a), FOIS, n), d(r), [d(wrong), d(r * 10), d(r + n)],
             "On calcule %s %s %d = %s, puis on place la virgule : %d chiffre%s après la virgule. <b>%s</b>." % (num(int(a * 10 ** k)), FOIS, n, num(int(a * 10 ** k) * n), k, "s" if k > 1 else "", d(r)))


def s3():
    a = rv(0, 30, 1)
    b = rv(0, 20, R.choice([1, 2]))
    if a.denominator == 1 or b.denominator == 1 or a < 1 and b < 1 and R.random() < 0.5:
        return None
    r = a * b
    ka, kb = len(d(a).split(",")[1]), len(d(b).split(",")[1])
    A, B = int(a * 10 ** ka), int(b * 10 ** kb)
    return M("%s %s %s = …" % (d(a), FOIS, d(b)), d(r), [d(Fr(A * B, 10 ** max(ka, kb))), d(Fr(A * B, 10 ** (ka + kb + 1))), d(Fr(int(a) * int(b)) + (a - int(a)) * (b - int(b)))],
             "%s %s %s = %s ; il faut %d chiffres après la virgule (%d + %d) : <b>%s</b>." % (num(A), FOIS, num(B), num(A * B), ka + kb, ka, kb, d(r)))


def s4():
    k = R.choice(["ordre", "plus", "dixieme"])
    if k == "ordre":
        a = rv(10, 99, 1)
        b = rv(2, 9, 1)
        if a.denominator == 1 or b.denominator == 1:
            return None
        est = round(a) * round(b)
        return M("Quel est le meilleur ordre de grandeur de %s %s %s ?" % (d(a), FOIS, d(b)), num(int(est)), [num(int(est * 10)), num(int(round(a) + round(b))), num(int(est / 10)) if est >= 100 else num(int(est * 100))],
                 "On arrondit : %d %s %d = <b>%s</b> (le résultat exact est %s)." % (round(a), FOIS, round(b), num(int(est)), d(a * b)))
    if k == "dixieme":
        a = rv(1, 999, 0)
        m = R.choice([Fr(1, 10), Fr(1, 100)])
        return M("%s %s %s = …" % (d(a), FOIS, d(m)), d(a * m), [d(a / m), d(a * m * 10) if m == Fr(1, 100) else d(a * m / 10), d(a + m)],
                 "Multiplier par %s, c’est diviser par %d : <b>%s</b>." % (d(m), int(1 / m), d(a * m)))
    a = rv(2, 50, 0)
    b = Fr(R.randint(1, 9), 10)
    return M("%s %s %s : le résultat est-il plus grand ou plus petit que %s ?" % (d(a), FOIS, d(b), d(a)), "plus petit", ["plus grand", "égal à %s" % d(a), "on ne peut pas savoir"],
             "%s est plus petit que 1, donc le produit est plus petit que %s : %s %s %s = <b>%s</b>." % (d(b), d(a), d(a), FOIS, d(b), d(a * b)))


def s5():
    p = K.next()
    k = R.choice(["prix", "essence", "tissu", "pas", "grand"])
    if k == "prix":
        a, n = Fr(R.randint(120, 990), 100), R.randint(3, 12)
        return M("Un cahier coûte %s €. %s en achète %d. Combien paie-t-%s ?" % (d(a), p[0], n, p[1]), euro(a * n), [euro(a + n), euro(a * n + a), euro(a * n / 10)],
                 "%s %s %d = <b>%s €</b>." % (d(a), FOIS, n, em(a * n)))
    if k == "essence":
        a, l = Fr(R.randint(165, 199), 100), Fr(R.randint(20, 45) * 10 + R.choice([0, 5]), 10)
        r = a * l
        return M("Le litre d’essence coûte %s €. On met %s L dans le réservoir. Combien paie-t-on, au centime près ?" % (d(a), d(l)), euro(Fr(round(r * 100), 100)),
                 [euro(Fr(round(r * 10), 100)), euro(a + l), euro(Fr(round(r * 100), 100) + 1)],
                 "%s %s %s = %s, soit <b>%s €</b>." % (d(a), FOIS, d(l), d(r), em(Fr(round(r * 100), 100))))
    if k == "tissu":
        a, l = Fr(R.randint(4, 15), 1), Fr(R.randint(5, 35), 10)
        if l.denominator == 1:
            return None
        return M("Un mètre de tissu coûte %s €. Combien coûtent %s m ?" % (d(a), d(l)), euro(a * l), [euro(a * l * 10), euro(a + l), euro(a * int(l))],
                 "%s %s %s = <b>%s €</b>." % (d(a), FOIS, d(l), em(a * l)))
    if k == "pas":
        a, n = Fr(R.randint(55, 85), 100), R.choice([10, 100, 1000])
        return M("Un pas de %s mesure %s m. Quelle distance parcourt-%s en %s pas ?" % (p[0], d(a), p[1], num(n)), "%s m" % d(a * n), ["%s m" % d(a * n * 10), "%s m" % d(a * n / 10), "%s m" % d(a + n)],
                 "%s %s %s = <b>%s m</b>." % (d(a), FOIS, num(n), d(a * n)))
    a = Fr(R.randint(11, 40), 10)
    b = Fr(R.randint(11, 30), 10)
    if a.denominator == 1 or b.denominator == 1:
        return None
    return M("Un rectangle mesure %s cm sur %s cm. Quelle est son aire ?" % (d(a), d(b)), "%s cm²" % d(a * b), ["%s cm²" % d(2 * (a + b)), "%s cm²" % d(a * b * 10), "%s cm²" % d(a + b)],
             "Aire = longueur %s largeur = %s %s %s = <b>%s cm²</b>." % (FOIS, d(a), FOIS, d(b), d(a * b)))


def main():
    seen = set()
    sets = [("× 10, × 100, × 1 000", mix(R, seen, [(s1, 20)])), ("Décimal × entier", mix(R, seen, [(s2, 20)])),
            ("Décimal × décimal", mix(R, seen, [(s3, 20)])), ("Ordre de grandeur et × 0,1", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["× 10, × 100, × 1 000 : chaque chiffre devient 10, 100, 1 000 fois plus grand ; la virgule « se déplace » de 1, 2, 3 rangs vers la droite.",
              "Pour 2,5 × 1,2 : on calcule 25 × 12 = 300 sans virgule, puis on met autant de chiffres après la virgule que dans les deux facteurs (1 + 1 = 2) : 3,00 = 3.",
              "Multiplier par un nombre plus petit que 1 donne un résultat plus petit."],
             [("4,25 × 3", ["425 × 3 = 1 275", "2 chiffres après la virgule"], "12,75")],
             [["3,5 × 10 = 3,50", "3,50 = 3,5 ! En fait 3,5 × 10 = 35."],
              ["2,5 × 1,2 = 30", "Il faut 2 chiffres après la virgule : 3,00 = 3."],
              ["Croire qu’un produit est toujours plus grand", "12 × 0,5 = 6 : multiplier par 0,5, c’est prendre la moitié."]])
    faq = [("Comment placer la virgule dans un produit ?", "On compte les chiffres après la virgule dans les deux facteurs et on en met autant dans le résultat."),
           ("À quoi sert l’ordre de grandeur ?", "À vérifier rapidement qu’un résultat est plausible.")]
    unit("6e", R, "multiplication-de-decimaux", "N",
         "Multiplier un nombre décimal par 10, 100, 1 000 ; multiplier un décimal par un entier ou par un décimal ; estimer un ordre de grandeur ; résoudre des problèmes",
         "Multiplier des nombres décimaux", "Multiplication de décimaux",
         "Fiches de maths 6e sur la multiplication des nombres décimaux : × 10, × 100, décimal × entier, décimal × décimal, ordre de grandeur et problèmes. 100 exercices corrigés.",
         "On calcule sans virgule, puis on la place.", "2,5 × 1,2 = 3", body, faq, sets, 4)


if __name__ == "__main__":
    main()
