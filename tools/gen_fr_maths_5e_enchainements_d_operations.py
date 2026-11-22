# -*- coding: utf-8 -*-
"""
France Maths 5e : Enchaînements d’opérations, priorités, distributivité, programmes de calcul
  python3 tools/gen_fr_maths_5e_enchainements_d_operations.py
Diviser par un décimal, priorités avec parenthèses, distributivité simple (calcul mental 12 × 99), traduire un programme de calcul,
multiples et critères de divisibilité par 3 et 9.
Erreurs : calculer de gauche à droite, 7 × 99 = 7 × 100 − 1, 4,5 ÷ 0,5 = 2,25.
"""
import random
from fr_c4 import *

R = random.Random(60204)
K = Kids(R)


def s1():
    b = R.choice([Fr(1, 10), Fr(1, 2), Fr(2, 10), Fr(25, 100), Fr(5, 100), Fr(15, 10), Fr(12, 10), Fr(4, 10)])
    q = R.randint(2, 40)
    a = b * q
    if (a * 100).denominator != 1:
        return None
    k = 10 if (b * 10).denominator == 1 else 100
    return M("%s %s %s = …" % (d(a), DIV, d(b)), d(q), [d(a * b), d(Fr(q, 10)), d(q * 10)],
             "On multiplie les deux nombres par %d : %s %s %s = %s %s %s = <b>%s</b>. (Diviser par un nombre plus petit que 1 donne un résultat plus grand.)" % (k, d(a), DIV, d(b), d(a * k), DIV, d(b * k), d(q)))


def s2():
    a, b, c, e = R.randint(2, 12), R.randint(2, 9), R.randint(2, 9), R.randint(1, 20)
    k = R.choice(["1", "2", "3", "4"])
    if k == "1":
        expr_, r, w = "%d + %d × (%d − %d)" % (e, a, b + c, c), e + a * b, [(e + a) * b, e + a * (b + c) - c, e + a * b + c]
    elif k == "2":
        if (a + b) * c - e < 0:
            return None
        expr_, r, w = "(%d + %d) × %d − %d" % (a, b, c, e), (a + b) * c - e, [a + b * c - e, a * c + b - e, (a + b) * c + e]
    elif k == "3":
        expr_, r, w = "%d − %d ÷ %d + %d" % (a * c + 30, a * c, c, e), a * c + 30 - a + e, [30 // c + e, a * c + 30 - a - e, a * c + 30 - a]
    else:
        expr_, r, w = "%d × [%d + (%d − %d)]" % (c, a, b + e, e), c * (a + b), [c * a + b, c + a + b, c * (a + b + e)]
    return M("Calcule : %s" % expr_, str(r), [str(x) for x in w if x >= 0], "Parenthèses (ou crochets) d’abord, puis × et ÷, puis + et − de gauche à droite : <b>%d</b>." % r)


def s3():
    k = R.choice(["99", "101", "dev", "fact"])
    a = R.randint(3, 49)
    if k == "99":
        n = R.choice([9, 99, 999])
        return M("Calcule astucieusement : %d × %s" % (a, num(n)), num(a * n), [num(a * (n + 1) - 1), num(a * (n + 1)), num(a * n + a)],
                 "%d × %s = %d × (%s − 1) = %s − %d = <b>%s</b>." % (a, num(n), a, num(n + 1), num(a * (n + 1)), a, num(a * n)))
    if k == "101":
        n = R.choice([11, 101, 1001])
        return M("Calcule astucieusement : %d × %s" % (a, num(n)), num(a * n), [num(a * (n - 1) + 1), num(a * (n - 1)), num(a * n - a * 2)],
                 "%d × %s = %d × (%s + 1) = %s + %d = <b>%s</b>." % (a, num(n), a, num(n - 1), num(a * (n - 1)), a, num(a * n)))
    b, c = R.randint(2, 30), R.randint(2, 30)
    if k == "dev":
        return M("Quelle égalité est vraie ?", "%d × (%d + %d) = %d × %d + %d × %d" % (a, b, c, a, b, a, c),
                 ["%d × (%d + %d) = %d × %d + %d" % (a, b, c, a, b, c), "%d × (%d + %d) = %d + %d × %d" % (a, b, c, a, b, c), "%d × (%d + %d) = (%d + %d) × (%d + %d)" % (a, b, c, a, b, a, c)],
                 "On distribue %d à chacun des termes : <b>%d × (%d + %d) = %d × %d + %d × %d</b>." % (a, a, b, c, a, b, a, c))
    s_ = R.choice([10, 100])
    b = R.randint(1, s_ - 1)
    return M("Calcule astucieusement : %d × %d + %d × %d" % (a, b, a, s_ - b), num(a * s_), [num(a * s_ + b), num(a * b + s_ - b), num(2 * a * s_)],
             "On factorise : %d × (%d + %d) = %d × %d = <b>%s</b>." % (a, b, s_ - b, a, s_, num(a * s_)))


def s4():
    a = R.randint(2, 12)
    m, n = R.randint(2, 6), R.randint(1, 9)
    k = R.choice(["fwd", "expr", "phrase"])
    if k == "fwd":
        r = (a + n) * m
        return M("Programme : « Choisis un nombre ; ajoute %d ; multiplie le résultat par %d. » On choisit %d. Quel résultat obtient-on ?" % (n, m, a), str(r), [str(a + n * m), str(a * m + n), str((a + m) * n)],
                 "(%d + %d) × %d = <b>%d</b>." % (a, n, m, r))
    if k == "expr":
        return M("Programme : « Choisis un nombre ; multiplie-le par %d ; enlève %d. » Quelle expression donne le résultat pour le nombre %d ?" % (m, n, a), "%d × %d − %d" % (a, m, n),
                 ["%d × (%d − %d)" % (a, m, n), "(%d − %d) × %d" % (a, n, m), "%d − %d × %d" % (a, n, m)],
                 "On multiplie d’abord, puis on enlève : <b>%d × %d − %d</b> = %d." % (a, m, n, a * m - n))
    return M("Quelle expression traduit « le triple de la différence de %d et %d » ?" % (a + n, n), "3 × (%d − %d)" % (a + n, n), ["3 × %d − %d" % (a + n, n), "%d − 3 × %d" % (a + n, n), "(3 × %d) − (3 + %d)" % (a + n, n)],
             "On calcule d’abord la différence, puis on la triple : <b>3 × (%d − %d)</b> = %d." % (a + n, n, 3 * a))


def s5():
    p = K.next()
    k = R.choice(["div3", "div9", "achat", "multiple"])
    if k in ("div3", "div9"):
        q = 3 if k == "div3" else 9
        n = R.randint(1000, 99999)
        if R.random() < 0.5:
            n -= n % q
        ok = n % q == 0
        sd = sum(map(int, str(n)))
        return M("%s est-il divisible par %d ?" % (num(n), q), "oui" if ok else "non", ["non" if ok else "oui", "oui, car il est impair" if n % 2 else "oui, car il est pair", "on ne peut pas savoir sans poser la division"],
                 "Somme des chiffres : %s = %d, %s divisible par %d : <b>%s</b>." % (" + ".join(str(n)), sd, "qui est" if sd % q == 0 else "qui n’est pas", q, "oui" if ok else "non"))
    if k == "achat":
        n, a, b = R.randint(2, 6), Fr(R.randint(150, 900), 100), Fr(R.randint(100, 500), 100)
        return M("%s achète %d cahiers à %s € et une règle à %s €. Combien paie-t-%s ?" % (p[0], n, em(a), em(b), p[1]), euro(n * a + b), [euro(n * (a + b)), euro(n + a + b), euro(n * a)],
                 "%d × %s + %s = <b>%s</b>." % (n, em(a), em(b), euro(n * a + b)))
    a = R.randint(3, 12)
    lo = R.randint(20, 60)
    hi = lo + R.randint(10, 30)
    ms = [x for x in range(lo, hi + 1) if x % a == 0]
    return M("Combien y a-t-il de multiples de %d entre %d et %d (inclus) ?" % (a, lo, hi), str(len(ms)), [str(len(ms) + 1), str(len(ms) - 1) if len(ms) > 1 else str(len(ms) + 2), str((hi - lo) // a + 2)],
             "Ce sont %s : <b>%d</b>." % (", ".join(map(str, ms)) if ms else "aucun", len(ms)))


def main():
    seen = set()
    sets = [("Diviser par un décimal", mix(R, seen, [(s1, 20)])), ("Priorités et parenthèses", mix(R, seen, [(s2, 20)])),
            ("Distributivité et calcul astucieux", mix(R, seen, [(s3, 20)])), ("Programmes de calcul", mix(R, seen, [(s4, 20)])), ("Divisibilité et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Ordre des calculs : d’abord les parenthèses, puis les multiplications et divisions, enfin les additions et soustractions.",
              "Distributivité : k × (a + b) = k × a + k × b. Exemple : 7 × 99 = 7 × 100 − 7 × 1 = 693.",
              "Pour diviser par un décimal, on multiplie les deux nombres par 10 ou 100 pour enlever la virgule du diviseur."],
             [("4,5 ÷ 0,5", ["45 ÷ 5"], "9")],
             [["Calculer de gauche à droite : 3 + 4 × 2 = 14", "La multiplication d’abord : 3 + 8 = 11."],
              ["7 × 99 = 7 × 100 − 1", "Il faut enlever 7 × 1 : 700 − 7 = 693."],
              ["4,5 ÷ 0,5 = 2,25", "Diviser par 0,5 donne un résultat plus grand : 9."]])
    faq = [("Pourquoi multiplier dividende et diviseur par 10 ?", "Le quotient ne change pas, et le diviseur devient entier, ce qui facilite le calcul."),
           ("À quoi sert la distributivité ?", "À calculer plus vite de tête et, plus tard, à transformer des expressions littérales.")]
    unit("5e", R, "enchainements-d-operations", "N",
         "Diviser par un nombre décimal ; enchaîner des opérations en respectant les priorités ; utiliser la distributivité simple pour calculer ; traduire un programme de calcul par une expression ; utiliser les critères de divisibilité par 3 et 9",
         "Enchaînements d’opérations et priorités", "Enchaînements d’opérations",
         "Fiches de maths 5e sur les enchaînements d’opérations : diviser par un décimal, priorités, distributivité, programmes de calcul et divisibilité. 100 exercices corrigés.",
         "Parenthèses, puis × et ÷, puis + et −.", "k × (a + b) = k × a + k × b", body, faq, sets, 4)


if __name__ == "__main__":
    main()
