# -*- coding: utf-8 -*-
"""
France Maths 5e : Calcul littéral (formules, substitution, tester une égalité, distributivité, réduire)
  python3 tools/gen_fr_maths_5e_calcul_litteral.py
Erreurs : 3x avec x = 4 donne 34, x² = 2x, 3(x + 2) = 3x + 2, 2x + 3x = 5x², 4x + 3 = 7x.
"""
import random
from fr_c4 import *

R = random.Random(60206)
K = Kids(R)
V = ["x", "a", "n", "y", "t"]


def s1():
    x = R.randint(2, 9)
    v = R.choice(V)
    a, b = R.randint(2, 9), R.randint(1, 15)
    k = R.choice(["ax+b", "ax-b", "x2", "a(x+b)", "x2+ax"])
    if k == "ax+b":
        e, r, w = "%d%s + %d" % (a, v, b), a * x + b, [int("%d%d" % (a, x)) + b, a + x + b, a * (x + b)]
    elif k == "ax-b":
        e, r, w = "%d%s − %d" % (a, v, b), a * x - b, [int("%d%d" % (a, x)) - b, a * (x - b), a - x + b]
    elif k == "x2":
        e, r, w = "%s² + %d" % (v, b), x * x + b, [2 * x + b, (x + b) ** 2, x + 2 + b]
    elif k == "a(x+b)":
        e, r, w = "%d(%s + %d)" % (a, v, b), a * (x + b), [a * x + b, a + x + b, int("%d%d" % (a, x)) + b]
    else:
        e, r, w = "%s² + %d%s" % (v, a, v), x * x + a * x, [2 * x + a * x, (x + a) * 2, x * x + a + x]
    return M("Calcule %s pour %s = %d." % (e, v, x), str(r), [str(t) for t in w if t != r],
             "On remplace %s par %d : %s = <b>%d</b>." % (v, x, e.replace(v, "×%d" % x).replace("(×", "(").replace(" ×", " ").replace("²", "²"), r) if False else
             "On remplace %s par %d (attention : %d%s veut dire %d × %s) : <b>%d</b>." % (v, x, a, v, a, v, r))


def s2():
    k = R.choice(["perim", "aire", "double", "carre", "prix"])
    if k == "perim":
        return M("Quelle formule donne le périmètre P d’un carré de côté c ?", "P = 4c", ["P = c²", "P = c + 4", "P = 2c"], "Un carré a 4 côtés de longueur c : <b>P = 4c</b>.") if R.random() < 0.5 else \
            M("Quelle formule donne le périmètre P d’un rectangle de longueur L et de largeur ℓ ?", "P = 2(L + ℓ)", ["P = L × ℓ", "P = 2L + ℓ", "P = L + ℓ"], "<b>P = 2(L + ℓ)</b> = 2L + 2ℓ.")
    if k == "aire":
        return M("Quelle formule donne l’aire A d’un carré de côté c ?", "A = c²", ["A = 4c", "A = 2c", "A = c + c"], "<b>A = c × c = c²</b>.")
    n = R.randint(2, 9)
    if k == "double":
        return M("On choisit un nombre n. Quelle expression traduit « le double de n, augmenté de %d » ?" % n, "2n + %d" % n, ["2(n + %d)" % n, "n² + %d" % n, "n + 2 + %d" % n],
                 "Le double de n est 2n, puis on ajoute %d : <b>2n + %d</b>." % (n, n))
    if k == "carre":
        return M("On choisit un nombre x. Quelle expression traduit « le carré de x, diminué de %d » ?" % n, "x² − %d" % n, ["2x − %d" % n, "(x − %d)²" % n, "x − %d²" % n],
                 "Le carré de x est x², puis on enlève %d : <b>x² − %d</b>." % (n, n))
    p = Fr(R.randint(10, 60), 10)
    return M("Un ticket coûte %s €. Quelle expression donne le prix de n tickets ?" % em(p), "%s × n" % em(p), ["%s + n" % em(p), "n + %s" % em(p * 2), "%s ÷ n" % em(p)],
             "n tickets à %s € : <b>%s × n</b> (on écrit aussi %sn)." % (em(p), em(p), em(p)))


def s3():
    a, b, x = R.randint(2, 6), R.randint(1, 9), R.randint(1, 6)
    v = R.choice(V)
    lhs = a * x + b
    c = R.choice([lhs, lhs + R.choice([-2, -1, 1, 2])])
    ok = c == lhs
    return M("L’égalité %d%s + %d = %d est-elle vraie pour %s = %d ?" % (a, v, b, c, v, x), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement si %s est pair" % v],
             "Pour %s = %d : %d × %d + %d = %d, %s %d : <b>%s</b>." % (v, x, a, x, b, lhs, "égal à" if ok else "différent de", c, "oui" if ok else "non"))


def s4():
    k = R.choice(["dev", "dev2", "fact", "red", "red2"])
    a, b, c = R.randint(2, 9), R.randint(1, 9), R.randint(2, 9)
    v = R.choice(V)
    if k == "dev":
        return M("Développe : %d(%s + %d)" % (a, v, b), "%d%s + %d" % (a, v, a * b), ["%d%s + %d" % (a, v, b), "%d%s" % (a + b, v), "%s + %d" % (v, a * b)],
                 "On distribue %d : %d × %s + %d × %d = <b>%d%s + %d</b>." % (a, a, v, a, b, a, v, a * b))
    if k == "dev2":
        return M("Développe : %d(%d%s − %d)" % (a, c, v, b), "%d%s − %d" % (a * c, v, a * b), ["%d%s − %d" % (a * c, v, b), "%d%s − %d" % (a + c, v, a * b), "%d%s − %d" % (a * c, v, a + b)],
                 "%d × %d%s − %d × %d = <b>%d%s − %d</b>." % (a, c, v, a, b, a * c, v, a * b))
    if k == "fact":
        return M("Factorise : %d%s + %d" % (a, v, a * b), "%d(%s + %d)" % (a, v, b), ["%d(%s + %d)" % (a, v, a * b), "%s(%d + %d)" % (v, a, a * b), "%d%s(1 + %d)" % (a, v, b)],
                 "%d%s + %d = %d × %s + %d × %d = <b>%d(%s + %d)</b>." % (a, v, a * b, a, v, a, b, a, v, b))
    if k == "red":
        return M("Réduis : %d%s + %d%s" % (a, v, c, v), "%d%s" % (a + c, v), ["%d%s²" % (a + c, v), "%d%s" % (a * c, v), "%d" % (a + c)],
                 "%d%s + %d%s = (%d + %d)%s = <b>%d%s</b>." % (a, v, c, v, a, c, v, a + c, v))
    e = R.randint(1, 9)
    return M("Réduis : %d%s + %d + %d%s − %d" % (a, v, b + e, c, v, e), "%d%s + %d" % (a + c, v, b), ["%d%s" % (a + c + b, v), "%d%s + %d" % (a + c, v, b + 2 * e), "%d%s²" % (a + c, v)],
             "On regroupe les %s et les nombres : (%d + %d)%s + (%d − %d) = <b>%d%s + %d</b>." % (v, a, c, v, b + e, e, a + c, v, b))


def s5():
    k = R.choice(["contre", "demo", "pairs", "equiv", "equiv"])
    if k == "equiv":
        a, b, c = R.randint(2, 6), R.randint(1, 9), R.randint(1, 5)
        return M("Quelle expression est égale à %d(x + %d) + %dx pour tout nombre x ?" % (a, b, c), "%dx + %d" % (a + c, a * b), ["%dx + %d" % (a + c, b), "%dx + %d" % (a * c, a * b), "%dx" % (a + c + a * b)],
                 "%d(x + %d) + %dx = %dx + %d + %dx = <b>%dx + %d</b>." % (a, b, c, a, a * b, c, a + c, a * b))
    if k == "contre":
        V2 = [("« Pour tout nombre x, x² est plus grand que x. »", "faux : pour x = 0,5, x² = 0,25"), ("« Pour tout nombre n, 2n est plus grand que n. »", "faux : pour n = 0, 2n = n"),
              ("« Pour tout nombre a, a + a = a². »", "faux : pour a = 3, a + a = 6 et a² = 9"), ("« Pour tout nombre x, 3(x + 1) = 3x + 1. »", "faux : pour x = 0, on obtient 3 et 1")]
        q, a = R.choice(V2)
        return M("%s Cette affirmation est-elle vraie ?" % q, a, ["vrai, on l’a vérifié pour x = 2", "vrai pour tous les nombres", "on ne peut pas savoir"],
                 "Un seul contre-exemple suffit pour montrer qu’une affirmation est fausse : <b>%s</b>." % a)
    if k == "demo":
        n = R.randint(2, 9)
        return M("Programme : « Choisis un nombre, ajoute %d, multiplie par 2, enlève le double du nombre choisi. » Que trouve-t-on toujours ?" % n, str(2 * n), [str(n), "le nombre choisi", str(2 * n + 2)],
                 "Avec x : 2(x + %d) − 2x = 2x + %d − 2x = <b>%d</b>, quel que soit x." % (n, 2 * n, 2 * n))
    return M("Si n est un nombre entier, comment s’écrit toujours un nombre pair ?", "2n", ["n + 2", "n²", "2n + 1"], "Un nombre pair est un multiple de 2 : <b>2n</b>. (2n + 1 est impair.)")


def main():
    seen = set()
    sets = [("Remplacer une lettre par un nombre", mix(R, seen, [(s1, 20)])), ("Écrire une formule", mix(R, seen, [(s2, 20)])),
            ("Tester une égalité", mix(R, seen, [(s3, 20)])), ("Développer, factoriser, réduire", mix(R, seen, [(s4, 20)])), ("Démontrer et contre-exemples", mix(R, seen, [(s5, 20)]))]
    body = L(["Une lettre peut représenter n’importe quel nombre. 3x veut dire 3 × x ; x² veut dire x × x.",
              "<b>Développer</b> : k(a + b) = ka + kb. <b>Factoriser</b> : ka + kb = k(a + b).",
              "<b>Réduire</b> : on regroupe les termes en x et les nombres : 4x + 2 + 3x = 7x + 2."],
             [("Calcule 2x² + 3 pour x = 4", ["x² = 16", "2 × 16 + 3"], "35")],
             [["3x pour x = 4 donne 34", "3x = 3 × 4 = 12."], ["3(x + 2) = 3x + 2", "On multiplie aussi le 2 : 3x + 6."], ["2x + 3x = 5x² ou 4x + 3 = 7x", "2x + 3x = 5x ; 4x + 3 ne se réduit pas."]])
    faq = [("Pourquoi écrire 3x au lieu de 3 × x ?", "C’est plus court : on peut supprimer le signe × devant une lettre ou une parenthèse."),
           ("Un exemple suffit-il pour prouver une propriété ?", "Non. Un exemple peut montrer qu’elle est fausse (contre-exemple), mais pour prouver qu’elle est vraie, il faut un calcul avec une lettre.")]
    unit("5e", R, "calcul-litteral", "A",
         "Produire des formules ; calculer la valeur d’une expression par substitution ; tester si une égalité est vraie ; développer et factoriser avec k(a + b) = ka + kb ; réduire une expression ; utiliser un contre-exemple",
         "Le calcul littéral", "Calcul littéral",
         "Fiches de maths 5e sur le calcul littéral : substitution, formules, tester une égalité, développer, factoriser, réduire et contre-exemples. 100 exercices corrigés.",
         "k(a + b) = ka + kb", "3x = 3 × x", body, faq, sets, 6)


if __name__ == "__main__":
    main()
