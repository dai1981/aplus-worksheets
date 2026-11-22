# -*- coding: utf-8 -*-
"""
France Maths 6e : Priorités opératoires
  python3 tools/gen_fr_maths_6e_priorites_operatoires.py
Erreurs : calculer de gauche à droite (2 + 3 × 4 = 20), oublier les parenthèses, traduire « le double de la somme » en 2 × a + b.
"""
import random
from fr_c4 import *

R = random.Random(60107)
K = Kids(R)


def s1():
    a, b, c = R.randint(2, 20), R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["a+bc", "bc+a", "a-bc", "ab+c"])
    if k == "a+bc":
        return M("%d + %d %s %d = …" % (a, b, FOIS, c), str(a + b * c), [str((a + b) * c), str(a + b + c), str(a * b + c)], "La multiplication d’abord : %d %s %d = %d ; puis %d + %d = <b>%d</b>." % (b, FOIS, c, b * c, a, b * c, a + b * c))
    if k == "bc+a":
        return M("%d %s %d + %d = …" % (b, FOIS, c, a), str(b * c + a), [str(b * (c + a)), str(b + c + a), str(b * c * a)], "%d %s %d = %d ; %d + %d = <b>%d</b>." % (b, FOIS, c, b * c, b * c, a, b * c + a))
    if k == "a-bc":
        a = b * c + R.randint(1, 30)
        return M("%d − %d %s %d = …" % (a, b, FOIS, c), str(a - b * c), [str((a - b) * c), str(a - b - c), str(a - b * c + 1)], "%d %s %d = %d ; %d − %d = <b>%d</b>." % (b, FOIS, c, b * c, a, b * c, a - b * c))
    return M("%d %s %d + %d %s %d = …" % (a, FOIS, b, c, FOIS, 2), str(a * b + c * 2), [str((a * b + c) * 2), str(a * (b + c) * 2), str(a * b + c + 2)], "Les deux multiplications d’abord : %d + %d = <b>%d</b>." % (a * b, c * 2, a * b + c * 2))


def s2():
    b, q = R.randint(2, 9), R.randint(2, 12)
    a = R.randint(2, 30)
    k = R.choice(["a+div", "div-a", "mixte"])
    if k == "a+div":
        return M("%d + %d %s %d = …" % (a, b * q, DIV, b), str(a + q), [str((a + b * q) // b) if (a + b * q) % b == 0 else str(a + q + 1), str(a + b * q - b), str(a + q * b)], "La division d’abord : %d %s %d = %d ; %d + %d = <b>%d</b>." % (b * q, DIV, b, q, a, q, a + q))
    if k == "div-a":
        if q <= a % q and False:
            return None
        a = R.randint(1, q - 1) if q > 1 else 0
        return M("%d %s %d − %d = …" % (b * q, DIV, b, a), str(q - a), [str(b * q // (b - a)) if b - a > 0 and (b * q) % (b - a) == 0 and b * q // (b - a) != q - a else str(q - a + 1), str(b * q - a), str(q + a)], "%d %s %d = %d ; %d − %d = <b>%d</b>." % (b * q, DIV, b, q, q, a, q - a))
    c = R.randint(2, 6)
    return M("%d %s %d + %d %s %d = …" % (b * q, DIV, b, c, FOIS, a), str(q + c * a), [str((q + c) * a), str(q + c + a), str(b * q + c * a)], "%d %s %d = %d et %d %s %d = %d ; %d + %d = <b>%d</b>." % (b * q, DIV, b, q, c, FOIS, a, c * a, q, c * a, q + c * a))


def s3():
    a, b, c = R.randint(2, 15), R.randint(2, 15), R.randint(2, 9)
    k = R.choice(["(a+b)c", "c(a-b)", "a-(b+c)", "(a+b)/c"])
    if k == "(a+b)c":
        return M("(%d + %d) %s %d = …" % (a, b, FOIS, c), str((a + b) * c), [str(a + b * c), str(a * c + b), str(a + b + c)], "Les parenthèses d’abord : %d + %d = %d ; %d %s %d = <b>%d</b>." % (a, b, a + b, a + b, FOIS, c, (a + b) * c))
    if k == "c(a-b)":
        if a <= b:
            a, b = b + 1, a
        return M("%d %s (%d − %d) = …" % (c, FOIS, a, b), str(c * (a - b)), [str(c * a - b), str(c * (a + b)), str(c * a - c - b)], "%d − %d = %d ; %d %s %d = <b>%d</b>." % (a, b, a - b, c, FOIS, a - b, c * (a - b)))
    if k == "a-(b+c)":
        a = b + c + R.randint(1, 20)
        return M("%d − (%d + %d) = …" % (a, b, c), str(a - b - c), [str(a - b + c), str(a + b + c), str(a - b - c + 1)], "%d + %d = %d ; %d − %d = <b>%d</b>." % (b, c, b + c, a, b + c, a - b - c))
    s = c * R.randint(2, 9)
    a = R.randint(1, s - 1)
    b = s - a
    return M("(%d + %d) %s %d = …" % (a, b, DIV, c), str(s // c), [str(a + b // c) if b % c == 0 else str(s // c + 1), str(s * c), str(s - c)], "%d + %d = %d ; %d %s %d = <b>%d</b>." % (a, b, s, s, DIV, c, s // c))


def s4():
    a, b = R.sample(range(3, 21), 2)
    k = R.choice(["double_somme", "somme_double", "produit_somme", "diff_triple"])
    if k == "double_somme":
        return M("Quelle expression traduit « le double de la somme de %d et %d » ?" % (a, b), "2 %s (%d + %d)" % (FOIS, a, b), ["2 %s %d + %d" % (FOIS, a, b), "%d + %d %s 2" % (a, b, FOIS), "(2 + %d) %s %d" % (a, FOIS, b)],
                 "On fait d’abord la somme, puis on la double : <b>2 × (%d + %d)</b> = %d." % (a, b, 2 * (a + b)))
    if k == "somme_double":
        return M("Quelle expression traduit « la somme de %d et du double de %d » ?" % (a, b), "%d + 2 %s %d" % (a, FOIS, b), ["2 %s (%d + %d)" % (FOIS, a, b), "(%d + 2) %s %d" % (a, FOIS, b), "%d %s 2 + %d" % (a, FOIS, b)],
                 "C’est une somme : %d plus le double de %d : <b>%d + 2 × %d</b> = %d." % (a, b, a, b, a + 2 * b))
    if k == "produit_somme":
        c = R.randint(2, 9)
        return M("Quelle expression traduit « le produit de %d par la somme de %d et %d » ?" % (c, a, b), "%d %s (%d + %d)" % (c, FOIS, a, b), ["%d %s %d + %d" % (c, FOIS, a, b), "%d + %d %s %d" % (c, a, FOIS, b), "(%d + %d) + %d" % (a, b, c)],
                 "Il faut des parenthèses pour calculer la somme d’abord : <b>%d × (%d + %d)</b> = %d." % (c, a, b, c * (a + b)))
    if a < 3 * b:
        a = 3 * b + R.randint(1, 20)
    return M("Quelle expression traduit « la différence entre %d et le triple de %d » ?" % (a, b), "%d − 3 %s %d" % (a, FOIS, b), ["(%d − 3) %s %d" % (a, FOIS, b), "3 %s (%d − %d)" % (FOIS, a, b), "%d − %d %s 3 + 1" % (a, b, FOIS)],
             "On enlève le triple de %d : <b>%d − 3 × %d</b> = %d." % (b, a, b, a - 3 * b))


def s5():
    p = K.next()
    k = R.choice(["achats", "cinema", "points", "partage"])
    if k == "achats":
        n, a, b = R.randint(2, 6), R.randint(2, 9), R.randint(3, 15)
        return M("%s achète %d cahiers à %d € et une trousse à %d €. Quel calcul donne le prix total ?" % (p[0], n, a, b), "%d %s %d + %d" % (n, FOIS, a, b), ["%d %s (%d + %d)" % (n, FOIS, a, b), "%d + %d + %d" % (n, a, b), "(%d + %d) %s %d" % (n, b, FOIS, a)],
                 "%d cahiers à %d €, puis la trousse : %d × %d + %d = <b>%d €</b>." % (n, a, n, a, b, n * a + b))
    if k == "cinema":
        n, a, b = R.randint(2, 5), R.randint(6, 12), R.randint(2, 5)
        return M("%d amis vont au cinéma : chacun paie une place à %d € et du pop-corn à %d €. Combien paient-ils en tout ?" % (n, a, b), "%d €" % (n * (a + b)), ["%d €" % (n * a + b), "%d €" % (n + a + b), "%d €" % (a + b)],
                 "Chaque ami paie %d + %d = %d €, donc %d × (%d + %d) = <b>%d €</b>." % (a, b, a + b, n, a, b, n * (a + b)))
    if k == "points":
        a, b, c = R.randint(2, 6), R.randint(2, 6), R.randint(1, 5)
        return M("Au jeu, une victoire rapporte 3 points et un nul 1 point. Une équipe a %d victoires et %d nuls. Combien a-t-elle de points ?" % (a, b), str(3 * a + b), [str(3 * (a + b)), str(a + b), str(3 * a * b)],
                 "3 × %d + 1 × %d = <b>%d points</b>." % (a, b, 3 * a + b))
    n = R.randint(2, 6)
    a, b = R.randint(10, 40), R.randint(10, 40)
    s = a + b
    s -= s % n
    b = s - a
    if b <= 0:
        return None
    return M("%s et ses amis (%d personnes en tout) se partagent %d bonbons et %d caramels. Combien de friandises chacun reçoit-il ?" % (p[0], n, a, b), str(s // n), [str(a + b // n) if b % n == 0 else str(s // n + 1), str(s * n), str(s - n)],
             "(%d + %d) ÷ %d = %d ÷ %d = <b>%d</b>." % (a, b, n, s, n, s // n))


def main():
    seen = set()
    sets = [("Multiplication avant addition", mix(R, seen, [(s1, 20)])), ("Avec des divisions", mix(R, seen, [(s2, 20)])),
            ("Avec des parenthèses", mix(R, seen, [(s3, 20)])), ("Traduire une phrase", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un calcul sans parenthèses, on effectue d’abord les <b>multiplications et divisions</b>, puis les additions et soustractions.",
              "Les calculs entre <b>parenthèses</b> se font en premier.",
              "« Le double de la somme de 3 et 5 » s’écrit 2 × (3 + 5)."],
             [("2 + 3 × 4", ["3 × 4 = 12", "2 + 12"], "14")],
             [["Calculer de gauche à droite : 2 + 3 × 4 = 20", "La multiplication d’abord : 2 + 12 = 14."],
              ["Oublier les parenthèses", "(2 + 3) × 4 = 20 n’est pas égal à 2 + 3 × 4 = 14."],
              ["Écrire 2 × 3 + 5 pour « le double de la somme de 3 et 5 »", "On met la somme entre parenthèses : 2 × (3 + 5)."]])
    faq = [("Pourquoi des priorités ?", "Pour qu’un calcul écrit en ligne ait un seul résultat, le même pour tout le monde."),
           ("Et s’il n’y a que des additions et des soustractions ?", "On calcule de gauche à droite.")]
    unit("6e", R, "priorites-operatoires", "N",
         "Connaître et utiliser la priorité de la multiplication et de la division sur l’addition et la soustraction ; utiliser les parenthèses ; traduire un calcul en une expression",
         "Priorités opératoires", "Priorités opératoires",
         "Fiches de maths 6e sur les priorités opératoires : multiplication avant addition, divisions, parenthèses, traduire une phrase et problèmes. 100 exercices corrigés.",
         "× et ÷ avant + et −.", "Parenthèses d’abord.", body, faq, sets, 7)


if __name__ == "__main__":
    main()
