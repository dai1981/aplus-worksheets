# -*- coding: utf-8 -*-
"""
France Maths 4e : Programmes de calcul (exécuter, exprimer, remonter, comparer, démontrer)
  python3 tools/gen_fr_maths_4e_programmes_de_calcul.py
Erreurs : oublier les parenthèses dans l’expression, faire les étapes dans le désordre, croire qu’un exemple suffit à démontrer.
"""
import random
from fr_c4 import *

R = random.Random(60307)
K = Kids(R)

OPS = [("ajouter", "Ajoute %d."), ("soustraire", "Soustrais %d."), ("multiplier", "Multiplie par %d."), ("carre", "Élève au carré.")]


def prog():
    """retourne (étapes texte, fonction, expression)"""
    a, b, c = R.randint(2, 9), R.randint(2, 6), R.randint(1, 9)
    k = R.choice(["A", "B", "C", "D", "E"])
    if k == "A":
        return ["Ajoute %d." % a, "Multiplie par %d." % b, "Soustrais %d." % c], (lambda x: (x + a) * b - c), "%d(x + %d) − %d" % (b, a, c), ["x + %d × %d − %d" % (a, b, c), "%d(x + %d − %d)" % (b, a, c), "%dx + %d − %d" % (b, a, c)], k
    if k == "B":
        return ["Multiplie par %d." % b, "Ajoute %d." % a, "Multiplie par %d." % c if c > 1 else "Multiplie par 2."], (lambda x: (b * x + a) * (c if c > 1 else 2)), "%d(%dx + %d)" % (c if c > 1 else 2, b, a), ["%dx + %d × %d" % (b, a, c if c > 1 else 2), "%dx + %d" % (b * (c if c > 1 else 2), a), "%d(x + %d)" % (b * (c if c > 1 else 2), a)], k
    if k == "C":
        return ["Soustrais %d." % a, "Élève au carré."], (lambda x: (x - a) ** 2), "(x − %d)²" % a, ["x − %d²" % a, "x² − %d" % a, "x² − %d²" % a], k
    if k == "D":
        return ["Élève au carré.", "Ajoute %d." % a, "Multiplie par %d." % b], (lambda x: (x * x + a) * b), "%d(x² + %d)" % (b, a), ["x² + %d × %d" % (a, b), "(%dx)² + %d" % (b, a), "%dx² + %d" % (b, a)], k
    return ["Multiplie par %d." % b, "Soustrais %d." % c, "Multiplie par −1."], (lambda x: -(b * x - c)), "−(%dx − %d)" % (b, c), ["−%dx − %d" % (b, c), "%dx − %d" % (b, c), "−%d(x − %d)" % (b, c)], k


def txt(steps):
    return "« Choisis un nombre. " + " ".join(steps) + " »"


def s1():
    st, f, ex, _, _ = prog()
    x = R.choice([R.randint(-5, 10), Fr(R.randint(1, 9), 2)])
    r = f(Fr(x))
    if r.denominator not in (1, 2, 4):
        return None
    w = [fq(r + 1), fq(-r) if r else "1", d(Fr(x) + sum(1 for _ in st))]
    if st[0].startswith("Ajoute"):
        a = int(st[0].split()[1][:-1])
        b = int(st[1].split()[-1][:-1])
        w[1] = d(Fr(x) + a * b - int(st[2].split()[1][:-1]))
    return M("Programme : %s On choisit %s. Quel résultat obtient-on ?" % (txt(st), d(x)), fq(r), w, "On applique les étapes dans l’ordre en partant de %s : <b>%s</b>." % (d(x), fq(r)))


def s2():
    st, f, ex, wrong, k = prog()
    w = wrong
    return M("Programme : %s Quelle expression donne le résultat si on choisit x ?" % txt(st), ex, w[:3], "On écrit chaque étape en gardant les parenthèses : <b>%s</b>." % ex)


def s3():
    a, b, c = R.randint(2, 9), R.randint(2, 6), R.randint(1, 9)
    x = R.randint(-4, 12)
    k = R.choice(["A", "B"])
    if k == "A":
        r = (x + a) * b - c
        return M("Programme : « Choisis un nombre. Ajoute %d. Multiplie par %d. Soustrais %d. » On obtient %s. Quel nombre avait-on choisi ?" % (a, b, c, d(r)), d(x), [d(Fr(r + c, b) + a) if Fr(r + c, b) + a != x else d(x + 1), d(Fr(r - c, b) - a) if Fr(r - c, b) - a != x and (Fr(r - c, b) - a).denominator == 1 else d(x - 1), d((r + c) * b - a)],
                 "On remonte : %d + %d = %d ; %d ÷ %d = %d ; %d − %d = <b>%s</b>. (Ou on résout %d(x + %d) − %d = %d.)" % (r, c, r + c, r + c, b, (r + c) // b, (r + c) // b, a, d(x), b, a, c, r))
    r = b * x - a
    return M("Programme : « Choisis un nombre. Multiplie-le par %d. Soustrais %d. » On obtient %s. Quel nombre avait-on choisi ?" % (b, a, d(r)), d(x), [d(Fr(r - a, b)) if Fr(r - a, b) != x and Fr(r - a, b).denominator == 1 else d(x + 2), d((r + a) * b), d(Fr(r, b) + a) if Fr(r, b).denominator == 1 and Fr(r, b) + a != x else d(x - 1)],
             "On résout %dx − %d = %d : %dx = %d, donc x = <b>%s</b>." % (b, a, r, b, r + a, d(x)))


def s4():
    a, b = R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["egal", "egal", "toujours", "contre"])
    if k == "egal":
        c = R.randint(1, 9)
        e = R.randint(2, 6)
        if e == 1:
            return None
        # A : x × e − c ; B : x + a
        xs = Fr(a + c, e - 1)
        if xs.denominator != 1:
            return None
        return M("Programme A : « Multiplie par %d, puis soustrais %d. » Programme B : « Ajoute %d. » Pour quel nombre de départ obtient-on le même résultat ?" % (e, c, a), d(xs),
                 [d(Fr(a - c, e - 1)) if Fr(a - c, e - 1).denominator == 1 and Fr(a - c, e - 1) != xs else d(xs + 1), d(Fr(a + c, e + 1)) if Fr(a + c, e + 1).denominator == 1 and Fr(a + c, e + 1) != xs else d(xs + 2), d(a + c)],
                 "On résout %dx − %d = x + %d : %dx = %d, donc x = <b>%s</b>." % (e, c, a, e - 1, a + c, d(xs)))
    if k == "toujours":
        m = R.randint(2, 5)
        return M("Programme : « Choisis un nombre. Ajoute %d. Multiplie par %d. Soustrais %d fois le nombre de départ. » Que remarque-t-on ?" % (a, m, m),
                 "on obtient toujours %d" % (a * m), ["on obtient toujours le nombre de départ", "on obtient toujours %d" % a, "le résultat dépend du nombre choisi"],
                 "%d(x + %d) − %dx = %dx + %d − %dx = <b>%d</b> : le résultat ne dépend pas de x." % (m, a, m, m, a * m, m, a * m))
    x0 = R.randint(1, 4)
    return M("Un programme donne le nombre de départ pour x = %d et x = %d. Est-ce une preuve qu’il donne toujours le nombre de départ ?" % (x0, x0 + 1),
             "non : des exemples ne suffisent pas, il faut un calcul littéral", ["oui, deux exemples suffisent", "oui, si les exemples sont des nombres entiers", "non, il faudrait tester 10 nombres"],
             "Pour démontrer qu’une propriété est toujours vraie, on utilise une lettre (calcul littéral). <b>Un seul contre-exemple</b> suffit, lui, à montrer qu’elle est fausse.")


def s5():
    a, b = R.randint(2, 9), R.randint(2, 9)
    k = R.choice(["prix", "magie", "tableur", "aire"])
    if k == "prix":
        n = R.randint(3, 12)
        return M("Prix d’une commande : on multiplie le nombre de livres n par %d €, puis on ajoute %d € de livraison. Quelle expression donne le prix ?" % (a, b), "%dn + %d" % (a, b), ["%d(n + %d)" % (a, b), "n + %d + %d" % (a, b), "%dn + %d" % (b, a)],
                 "<b>%dn + %d</b>. Par exemple pour %d livres : %d × %d + %d = %d €." % (a, b, n, a, n, b, a * n + b))
    if k == "magie":
        return M("Tour de magie : « Choisis un nombre. Ajoute %d. Multiplie par 2. Soustrais %d. Divise par 2. Soustrais le nombre choisi. » Quel est toujours le résultat ?" % (a, 2 * b), d(a - b),
                 [d(a), d(2 * a - 2 * b), d(a + b)], "(2(x + %d) − %d) ÷ 2 − x = x + %d − %d − x = <b>%s</b>." % (a, 2 * b, a, b, d(a - b)))
    if k == "tableur":
        c = R.choice(["A2", "B2", "A3"])
        return M("Dans un tableur, la cellule %s contient le nombre de départ. Quelle formule calcule « ajoute %d puis multiplie par %d » ?" % (c, a, b), "=(%s+%d)*%d" % (c, a, b), ["=%s+%d*%d" % (c, a, b), "=(%s*%d)+%d" % (c, b, a), "%s+%d*%d=" % (c, a, b)],
                 "Il faut des parenthèses pour faire l’addition d’abord : <b>=(%s+%d)*%d</b>." % (c, a, b))
    return M("Programme : « Choisis un nombre x. Élève-le au carré. Ajoute %d fois le nombre de départ. » Quelle expression factorisée donne le résultat ?" % a, "x(x + %d)" % a, ["x² + %d" % a, "(x + %d)²" % a, "%dx²" % a],
             "x² + %dx = <b>x(x + %d)</b>." % (a, a))


def main():
    seen = set()
    sets = [("Exécuter un programme", mix(R, seen, [(s1, 20)])), ("Traduire par une expression", mix(R, seen, [(s2, 20)])),
            ("Retrouver le nombre de départ", mix(R, seen, [(s3, 20)])), ("Comparer et démontrer", mix(R, seen, [(s4, 20)])), ("Problèmes et tableur", mix(R, seen, [(s5, 20)]))]
    body = L(["Un programme de calcul est une suite d’étapes. On peut l’exécuter avec un nombre, ou le traduire avec une lettre x.",
              "Pour traduire, on garde les <b>parenthèses</b> : « ajoute 3 puis multiplie par 5 » donne 5(x + 3), pas x + 3 × 5.",
              "Pour démontrer qu’un programme donne toujours le même résultat, on fait un calcul littéral ; des exemples ne suffisent pas."],
             [("« Ajoute 4, multiplie par 3, soustrais 12. »", ["3(x + 4) − 12", "= 3x + 12 − 12"], "3x")],
             [["« Ajoute 3, multiplie par 5 » donne x + 3 × 5", "L’addition est faite d’abord : 5(x + 3)."], ["Remonter un programme dans le même sens", "Pour remonter, on fait les opérations contraires dans l’ordre inverse."],
              ["« Ça marche pour 2 et 5, donc c’est toujours vrai »", "Il faut une preuve avec une lettre."]])
    faq = [("Comment trouver le nombre de départ ?", "On remonte le programme avec les opérations contraires, ou on résout une équation."),
           ("À quoi servent les programmes de calcul ?", "À découvrir le calcul littéral : la lettre remplace « n’importe quel nombre ».")]
    unit("4e", R, "programmes-de-calcul", "A",
         "Exécuter un programme de calcul ; le traduire par une expression littérale ; retrouver un nombre de départ ; comparer deux programmes et démontrer une propriété avec le calcul littéral ; utiliser une formule dans un tableur",
         "Programmes de calcul", "Programmes de calcul",
         "Fiches de maths 4e sur les programmes de calcul : exécuter, traduire par une expression, remonter, comparer, démontrer et tableur. 100 exercices corrigés.",
         "Un programme se traduit par une expression avec x", "« Ajoute 3, multiplie par 5 » → 5(x + 3)", body, faq, sets, 7)


if __name__ == "__main__":
    main()
