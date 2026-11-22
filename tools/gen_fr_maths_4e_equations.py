# -*- coding: utf-8 -*-
"""
France Maths 4e : Équations du premier degré (ax + b = cx + d), tester une solution, mettre en équation
  python3 tools/gen_fr_maths_4e_equations.py
Erreurs : 3x = 12 → x = 9 ou x = 36, garder le signe en changeant de membre, diviser seulement un terme.
"""
import random
from fr_c4 import *

R = random.Random(60306)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def sol(x):
    return "x = %s" % fq(x)


def s1():
    k = R.choice(["test", "test", "estsol"])
    a, b = nz(-6, 6), R.randint(-10, 10)
    c, e = nz(-6, 6), R.randint(-10, 10)
    if a == c:
        return None
    x = R.randint(-5, 6)
    lhs, rhs = a * x + b, c * x + e
    eq = "%s = %s" % (E((a, "x"), (b, "")), E((c, "x"), (e, "")))
    if k == "test":
        return M("Pour x = %s, que valent les deux membres de l’équation %s ?" % (d(x), eq), "%s et %s" % (d(lhs), d(rhs)), ["%s et %s" % (d(a + x + b), d(c + x + e)), "%s et %s" % (d(-lhs), d(-rhs)), "%s et %s" % (d(rhs), d(lhs)) if lhs != rhs else "0 et 0"],
                 "Membre de gauche : %s × %s + %s = %s ; membre de droite : %s × %s + %s = %s." % (d(a), par(x), par(b), d(lhs), d(c), par(x), par(e), d(rhs)))
    xs = Fr(e - b, a - c)
    t = R.choice([xs, xs + 1, -xs if xs else 2])
    ok = t == xs
    return M("Le nombre %s est-il solution de l’équation %s ?" % (fq(t), eq), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement si x est positif"],
             "On remplace x par %s : %s et %s%s." % (fq(t), fq(a * t + b), fq(c * t + e), " : égalité, donc <b>oui</b>" if ok else " sont différents, donc <b>non</b>"))


def s2():
    a = nz(-9, 9)
    x = R.randint(-9, 12)
    b = R.randint(-15, 15)
    k = R.choice(["ax", "x+b", "ax+b", "ax+b"])
    if k == "ax":
        if a == 1:
            return None
        r = a * x
        return M("Résous : %s = %s" % (E((a, "x")), d(r)), sol(x), [sol(r - a), sol(r * a), sol(Fr(a, r)) if r else sol(1)], "On divise les deux membres par %s : x = %s ÷ %s = <b>%s</b>." % (d(a), d(r), par(a), d(x)))
    if k == "x+b":
        if not b:
            return None
        r = x + b
        return M("Résous : %s = %s" % (E((1, "x"), (b, "")), d(r)), sol(x), [sol(r + b), sol(-x) if x else sol(1), sol(b - r) if b - r != x else sol(x + 2)], "On ajoute %s aux deux membres : <b>x = %s</b>." % (par(-b), d(x)))
    r = a * x + b
    if a == 1 or not b:
        return None
    return M("Résous : %s = %s" % (E((a, "x"), (b, "")), d(r)), sol(x), [sol(Fr(r + b, a)), sol(Fr(r, a) - b), sol(r - b - a)],
             "%s = %s − %s = %s, puis x = %s ÷ %s = <b>%s</b>." % (E((a, "x")), d(r), par(b), d(r - b), d(r - b), par(a), d(x)))


def s3():
    a, c = nz(-7, 9), nz(-7, 9)
    if a == c:
        return None
    x = Fr(R.randint(-8, 9))
    if R.random() < 0.25:
        x = Fr(R.randint(-9, 9), R.choice([2, 3]))
    b = R.randint(-12, 12)
    e = (a - c) * x + b
    if e.denominator != 1:
        return None
    e = int(e)
    eq = "%s = %s" % (E((a, "x"), (b, "")), E((c, "x"), (e, "")))
    w1 = Fr(e - b, a + c) if a + c else x + 1
    w2 = Fr(e + b, a - c)
    w3 = Fr(b - e, a - c)
    return M("Résous : %s" % eq, sol(x), [sol(w1) if w1 != x else sol(x + 1), sol(w2) if w2 != x else sol(x - 1), sol(w3) if w3 != x else sol(x + 2)],
             "On regroupe les x d’un côté : %s = %s, donc x = %s ÷ %s = <b>%s</b>." % (E((a - c, "x")), d(e - b), d(e - b), par(a - c), fq(x)))


def s4():
    k = R.choice(["par", "par2", "frac"])
    x = R.randint(-6, 9)
    if k == "par":
        m, a, b = nz(2, 6), nz(-5, 5), R.randint(-9, 9)
        r = m * (x + a) + b
        q = "%d(%s) %s = %s" % (m, E((1, "x"), (a, "")), ("+ %d" % b) if b > 0 else ("%s %d" % (MINUS, -b)) if b < 0 else "", d(r)) if b else "%d(%s) = %s" % (m, E((1, "x"), (a, "")), d(r))
        q = q.replace("  ", " ")
        w = Fr(r - b - a, m)
        return M("Résous : %s" % q, sol(x), [sol(w) if w != x else sol(x + 1), sol(r - b - m * a) if r - b - m * a != x else sol(x - 1), sol(Fr(r - b, m) + a)],
                 "On développe : %s = %s, puis on résout : <b>x = %s</b>." % (E((m, "x"), (m * a + b, "")), d(r), d(x)))
    if k == "par2":
        m, a = nz(2, 5), nz(-6, 6)
        c, e = nz(-4, 4), R.randint(-9, 9)
        if m == c:
            return None
        rhs = c * x + e
        b = rhs - m * (x + a)
        q = "%d(%s) = %s" % (m, E((1, "x"), (a, "")), E((c, "x"), (e, "")))
        if b != 0:
            return None
        xs = Fr(e - m * a, m - c)
        return M("Résous : %s" % q, sol(xs), [sol(Fr(e - a, m - c)) if Fr(e - a, m - c) != xs else sol(xs + 1), sol(Fr(e - m * a, m + c)) if m + c and Fr(e - m * a, m + c) != xs else sol(xs - 1), sol(-xs) if xs else sol(2)],
                 "%s = %s, donc %s = %s et <b>x = %s</b>." % (E((m, "x"), (m * a, "")), E((c, "x"), (e, "")), E((m - c, "x")), d(e - m * a), fq(xs)))
    dd = R.choice([2, 3, 4, 5])
    n = dd * R.randint(-6, 6)
    return M("Résous : %s = %s" % (fr("x", d(dd)), d(n // dd)), sol(n), [sol(Fr(n // dd, dd)), sol(n // dd + dd), sol(n // dd)] if n else [sol(dd), sol(1), sol(-dd)],
             "On multiplie les deux membres par %d : <b>x = %s</b>." % (dd, d(n)))


def s5():
    p, q = K.two()
    k = R.choice(["age", "tarif", "consec", "perim", "partage"])
    if k == "age":
        a = R.randint(10, 15)
        f = R.randint(25, 40)
        t = Fr(f - 2 * a, 1)
        if t <= 0:
            return None
        return M("%s a %d ans et son père %d ans. Dans combien d’années le père aura-t-il le double de l’âge %s ?" % (p[0], a, f, de_n(p[0])), pl(t, "an"), [pl(f - a, "an"), pl(Fr(f, 2) - a, "an") if (Fr(f, 2) - a) > 0 and Fr(f, 2) - a != t else pl(t + 2, "an"), pl(t + 1, "an")],
                 "On résout %d + x = 2(%d + x) : %d + x = %d + 2x, donc x = <b>%s</b>." % (f, a, f, 2 * a, pl(t, "an")))
    if k == "tarif":
        a, b, c = R.randint(5, 9), R.randint(15, 40), R.randint(2, 4)
        if a <= c:
            return None
        x = Fr(b, a - c)
        if x.denominator != 1:
            return None
        return M("Tarif A : %d € par séance. Tarif B : abonnement de %d € puis %d € par séance. Pour combien de séances les deux tarifs sont-ils égaux ?" % (a, b, c), str(x), [str(Fr(b, a + c)) if Fr(b, a + c).denominator == 1 else str(x + 1), str(b // a), str(x * 2)],
                 "On résout %dx = %d + %dx : %dx = %d, donc x = <b>%d</b>." % (a, b, c, a - c, b, x))
    if k == "consec":
        n = R.randint(3, 40)
        m = R.choice([3, 4])
        s = sum(n + i for i in range(m))
        return M("La somme de %d entiers consécutifs vaut %d. Quel est le plus petit ?" % (m, s), str(n), [str(s // m), str(n - 1), str(s - m)],
                 "x + (x + 1)%s = %d, donc %dx + %d = %d et x = <b>%d</b>." % (" + (x + 2)" + (" + (x + 3)" if m == 4 else ""), s, m, m * (m - 1) // 2, s, n))
    if k == "perim":
        l = R.randint(3, 20)
        e = R.randint(1, 9)
        P = 2 * (l + l + e)
        return M("Un rectangle a une longueur égale à sa largeur + %d cm et un périmètre de %d cm. Quelle est sa largeur ?" % (e, P), "%d cm" % l, ["%s cm" % d(Fr(P - e, 4)) if Fr(P - e, 4) != l else "%d cm" % (l + 1), "%s cm" % d(Fr(P, 4)), "%d cm" % (l + e)],
                 "2(x + x + %d) = %d, donc 4x + %d = %d et x = <b>%d cm</b>." % (e, P, 2 * e, P, l))
    a = R.randint(5, 40)
    e = R.randint(2, 15)
    t = 2 * a + e
    return M("%s et %s se partagent %d €. %s reçoit %d € de plus %s. Combien reçoit %s ?" % (p[0], q[0], t, p[0], e, que(q[0]), q[0]), "%d €" % a, ["%d €" % (a + e), "%s €" % d(Fr(t, 2)), "%d €" % (t - e)],
             "x + (x + %d) = %d, donc 2x = %d et x = <b>%d €</b>." % (e, t, t - e, a))


def main():
    seen = set()
    sets = [("Tester une solution", mix(R, seen, [(s1, 20)])), ("Équations ax + b = c", mix(R, seen, [(s2, 20)])),
            ("Inconnue des deux côtés", mix(R, seen, [(s3, 20)])), ("Avec des parenthèses ou une fraction", mix(R, seen, [(s4, 20)])), ("Mettre un problème en équation", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>solution</b> d’une équation est un nombre qui rend l’égalité vraie quand on remplace l’inconnue.",
              "On peut ajouter ou soustraire le même nombre aux deux membres, et multiplier ou diviser les deux membres par le même nombre non nul.",
              "Méthode : on développe si besoin, on regroupe les x d’un côté et les nombres de l’autre, puis on divise."],
             [("5x − 3 = 2x + 9", ["5x − 2x = 9 + 3", "3x = 12", "x = 12 ÷ 3"], "x = 4")],
             [["3x = 12, donc x = 12 − 3 = 9", "3x signifie 3 × x : on divise, x = 4."], ["x + 5 = 2, donc x = 2 + 5", "On enlève 5 aux deux membres : x = −3."],
              ["Oublier de vérifier", "On remplace x par la valeur trouvée dans l’équation de départ."]])
    faq = [("Comment mettre un problème en équation ?", "On choisit l’inconnue (ce qu’on cherche), on traduit l’énoncé par une égalité, on résout, puis on répond par une phrase."),
           ("Une équation a-t-elle toujours une solution ?", "Pas toujours : x + 1 = x n’en a aucune. Les équations de 4e ont en général une seule solution.")]
    unit("4e", R, "equations", "A",
         "Tester si un nombre est solution d’une équation ; résoudre une équation du premier degré à une inconnue (ax + b = cx + d) ; mettre en équation et résoudre un problème",
         "Équations du premier degré", "Équations",
         "Fiches de maths 4e sur les équations : tester une solution, résoudre ax + b = cx + d, parenthèses et fractions, mettre un problème en équation. 100 exercices corrigés.",
         "Même opération des deux côtés du signe =", "On isole x : on regroupe, puis on divise", body, faq, sets, 6)


if __name__ == "__main__":
    main()
