# -*- coding: utf-8 -*-
"""
France Maths 5e : Comparer, additionner et soustraire des fractions (dénominateurs quelconques)
  python3 tools/gen_fr_maths_5e_comparer_additionner_et_soustraire_des_fractions.py
Égalité de fractions, simplifier, comparer, additionner et soustraire avec des dénominateurs quelconques, problèmes.
Erreurs : additionner numérateurs et dénominateurs (1/2 + 1/3 = 2/5), multiplier seulement le dénominateur, comparer 2/3 et 3/4 avec 2 &lt; 3.
"""
import random
from math import gcd
from fr_c4 import *

R = random.Random(60203)
K = Kids(R)


def F(a, b):
    return fr(a, b)


def s1():
    a, b = R.randint(1, 9), R.randint(2, 12)
    if gcd(a, b) > 1 or a == b:
        return None
    k = R.randint(2, 7)
    t = R.choice(["num", "den", "simpl"])
    if t == "num":
        return M("Complète : %s = %s" % (F(a, b), F("…", b * k)), str(a * k), [str(a + b * k - b), str(a), str(a * k + 1)],
                 "%d × %d = %d, donc on multiplie aussi le numérateur par %d : <b>%d</b>." % (b, k, b * k, k, a * k))
    if t == "den":
        return M("Complète : %s = %s" % (F(a, b), F(a * k, "…")), str(b * k), [str(b + a * k - a), str(b), str(b * k + k)],
                 "%d × %d = %d, donc le dénominateur est %d × %d = <b>%d</b>." % (a, k, a * k, b, k, b * k))
    return M("Simplifie %s au maximum." % F(a * k, b * k), F(a, b), [F(a * k // gcd(a * k, 2) if (a * k) % 2 == 0 and (b * k) % 2 == 0 and gcd(a * k // 2, b * k // 2) > 1 else a * k - 1, b * k // 2 if (a * k) % 2 == 0 and (b * k) % 2 == 0 and gcd(a * k // 2, b * k // 2) > 1 else b * k - 1), F(a + 1, b + 1), F(b, a)],
             "On divise numérateur et dénominateur par %d : <b>%s</b>." % (k * gcd(a, b), F(a, b)))


def s2():
    a, b, c, e = R.randint(1, 9), R.randint(2, 10), R.randint(1, 9), R.randint(2, 10)
    x, y = Fr(a, b), Fr(c, e)
    if x == y or gcd(a, b) > 1 or gcd(c, e) > 1 or b == e:
        return None
    big = max(x, y)
    A, B = F(a, b), F(c, e)
    l = b * e // gcd(b, e)
    return M("Quelle est la plus grande fraction : %s ou %s ?" % (A, B), A if x > y else B, [B if x > y else A, "elles sont égales", "on ne peut pas savoir"],
             "Même dénominateur %d : %s et %s. La plus grande est <b>%s</b>." % (l, F(int(x * l), l), F(int(y * l), l), A if x > y else B))


def s3():
    b = R.choice([2, 3, 4, 5, 6])
    m = R.choice([2, 3, 4])
    e = b * m
    a, c = R.randint(1, 2 * b), R.randint(1, 2 * e)
    if gcd(a, b) > 1 or gcd(c, e) > 1:
        return None
    plus = R.random() < 0.55
    r = Fr(a, b) + Fr(c, e) if plus else Fr(a, b) - Fr(c, e)
    if r <= 0:
        return None
    return M("%s %s %s = …" % (F(a, b), "+" if plus else "−", F(c, e)), F(a * m + c if plus else a * m - c, e),
             [F(a + c if plus else abs(a - c), b + e), F(a + c if plus else abs(a - c), e), F(a * m + c + 1 if plus else a * m - c + 1, e)],
             "%s = %s, puis %s %s %s = <b>%s</b>." % (F(a, b), F(a * m, e), F(a * m, e), "+" if plus else "−", F(c, e), F(a * m + c if plus else a * m - c, e)))


def s4():
    b, e = R.sample([2, 3, 4, 5, 6, 7, 8, 9, 10], 2)
    if gcd(b, e) == min(b, e):
        return None
    a, c = R.randint(1, b - 1), R.randint(1, e - 1)
    if gcd(a, b) > 1 or gcd(c, e) > 1:
        return None
    l = b * e // gcd(b, e)
    plus = R.random() < 0.6
    r = Fr(a, b) + Fr(c, e) if plus else Fr(a, b) - Fr(c, e)
    if r <= 0:
        return None
    N = int(r * l)
    return M("%s %s %s = …" % (F(a, b), "+" if plus else "−", F(c, e)), F(N, l) if Fr(N, l) == r else F(N, l),
             [F(a + c if plus else abs(a - c) or 1, b + e), F(a * c, b * e) if not plus else F(a + c, b * e), F(N + 1, l)],
             "Dénominateur commun %d : %s %s %s = <b>%s</b>%s." % (l, F(a * l // b, l), "+" if plus else "−", F(c * l // e, l), F(N, l), "" if gcd(N, l) == 1 else " = %s" % fq(r)))


def s5():
    p = K.next()
    k = R.choice(["reste", "deux", "trajet", "compare"])
    if k == "reste":
        b, e = R.sample([3, 4, 5, 6, 8], 2)
        a, c = 1, 1
        r = 1 - Fr(a, b) - Fr(c, e)
        if r <= 0:
            return None
        l = b * e // gcd(b, e)
        return M("%s dépense %s de son argent de poche en livres et %s en jeux. Quelle fraction lui reste-t-il ?" % (p[0], F(a, b), F(c, e)), fq(r),
                 [F(b + e - 2, b + e) if (b + e - 2) else F(1, 2), F(int((Fr(a, b) + Fr(c, e)) * l), l), F(1, l)],
                 "%s + %s = %s ; 1 − %s = <b>%s</b>." % (F(a, b), F(c, e), fq(Fr(a, b) + Fr(c, e)), fq(Fr(a, b) + Fr(c, e)), fq(r)))
    if k == "deux":
        b, e = R.sample([2, 3, 4, 5, 6], 2)
        r = Fr(1, b) + Fr(1, e)
        if r >= 1:
            return None
        return M("Un réservoir est rempli au %s le matin, puis on ajoute %s du réservoir l’après-midi. Quelle fraction est remplie ?" % (F(1, b), F(1, e)), fq(r), [F(2, b + e), F(1, b * e), fq(1 - r)],
                 "%s + %s = <b>%s</b>." % (F(1, b), F(1, e), fq(r)))
    if k == "trajet":
        b = R.choice([3, 4, 5, 6])
        e = b * 2
        a = R.randint(1, b - 1)
        c = R.randint(1, e - 2 * a - 1) if e - 2 * a - 1 >= 1 else None
        if not c or gcd(a, b) > 1:
            return None
        r = 1 - Fr(a, b) - Fr(c, e)
        return M("%s fait %s du trajet à vélo, %s en bus et le reste à pied. Quelle fraction du trajet fait-%s à pied ?" % (p[0], F(a, b), F(c, e), p[1]), fq(r), [fq(Fr(a, b) + Fr(c, e)), F(1, e), F(e - a - c, e + b)],
                 "1 − %s − %s = %s − %s − %s = <b>%s</b>." % (F(a, b), F(c, e), F(e, e), F(2 * a, e), F(c, e), fq(r)))
    q = K.next()
    a, b, c, e = 2, 3, 3, 4
    x = R.choice([(2, 3, 3, 4), (3, 5, 4, 7), (5, 6, 7, 9), (3, 8, 2, 5), (4, 9, 1, 2)])
    a, b, c, e = x
    w = p[0] if Fr(a, b) > Fr(c, e) else q[0]
    return M("%s a lu %s de son livre et %s %s du sien (même nombre de pages). Qui a lu le plus ?" % (p[0], F(a, b), q[0], F(c, e)), w, [q[0] if w == p[0] else p[0], "ils ont lu autant", "on ne peut pas savoir"],
             "On compare %s et %s avec le dénominateur %d : <b>%s</b>." % (F(a, b), F(c, e), b * e, w))


def main():
    seen = set()
    sets = [("Fractions égales et simplification", mix(R, seen, [(s1, 20)])), ("Comparer des fractions", mix(R, seen, [(s2, 20)])),
            ("Un dénominateur multiple de l’autre", mix(R, seen, [(s3, 20)])), ("Dénominateurs quelconques", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["On ne change pas une fraction en multipliant (ou en divisant) le numérateur et le dénominateur par le même nombre : %s = %s." % (fr(2, 3), fr(8, 12)),
              "Pour comparer, additionner ou soustraire, on écrit les fractions avec le <b>même dénominateur</b>.",
              "Ensuite, on additionne ou on soustrait les numérateurs et on garde le dénominateur."],
             [("%s + %s" % (fr(2, 3), fr(1, 4)), ["%s + %s" % (fr(8, 12), fr(3, 12))], fr(11, 12))],
             [["%s + %s = %s" % (fr(1, 2), fr(1, 3), fr(2, 5)), "On met au même dénominateur : %s + %s = %s." % (fr(3, 6), fr(2, 6), fr(5, 6))],
              ["Multiplier seulement le dénominateur", "%s = %s, et pas %s." % (fr(2, 3), fr(4, 6), fr(2, 6))],
              ["Comparer seulement les numérateurs", "%s &lt; %s car %s &lt; %s." % (fr(2, 3), fr(3, 4), fr(8, 12), fr(9, 12))]])
    faq = [("Comment trouver un dénominateur commun ?", "On cherche un multiple commun aux deux dénominateurs, par exemple leur produit, ou mieux le plus petit."),
           ("Faut-il simplifier le résultat ?", "Oui, quand c’est possible : %s = %s." % (fr(6, 8), fr(3, 4)))]
    unit("5e", R, "comparer-additionner-et-soustraire-des-fractions", "N",
         "Utiliser l’égalité de fractions ; comparer des fractions ; additionner et soustraire des fractions de dénominateurs quelconques ; résoudre des problèmes",
         "Comparer, additionner et soustraire des fractions", "Fractions : comparer et additionner",
         "Fiches de maths 5e sur les fractions : fractions égales, simplifier, comparer, additionner et soustraire avec des dénominateurs différents, problèmes. 100 exercices corrigés.",
         "Même dénominateur d’abord.", "%s + %s = %s + %s = %s" % (fr(2, 3), fr(1, 4), fr(8, 12), fr(3, 12), fr(11, 12)), body, faq, sets, 3)


if __name__ == "__main__":
    main()
