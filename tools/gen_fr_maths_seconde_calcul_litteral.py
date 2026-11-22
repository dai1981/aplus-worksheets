# -*- coding: utf-8 -*-
"""
France Maths Seconde : Calcul littéral (identités remarquables, factorisation, expressions fractionnaires, formules, comparaison)
  python3 tools/gen_fr_maths_seconde_calcul_litteral.py
Erreurs : (a + b)² = a² + b², 1/a + 1/b = 2/(a + b), isoler une variable en ajoutant au lieu de diviser, comparer sans étudier le signe de la différence.
"""
import random
from fr_c4 import *

R = random.Random(60505)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    a, b = R.randint(1, 7), R.randint(1, 9)
    k = R.choice(["p", "m", "d", "fp", "fm", "fd"])
    ax = E((a, "x"))
    if k == "p":
        r = E((a * a, "x²"), (2 * a * b, "x"), (b * b, ""))
        return M("Développe : (%s + %d)²" % (ax, b), r, [E((a * a, "x²"), (b * b, "")), E((a * a, "x²"), (a * b, "x"), (b * b, "")), E((a, "x²"), (2 * a * b, "x"), (b * b, "")) if a > 1 else E((1, "x²"), (2 * b, "x"), (2 * b, ""))],
                 "(a + b)² = a² + 2ab + b² : <b>%s</b>." % r)
    if k == "m":
        r = E((a * a, "x²"), (-2 * a * b, "x"), (b * b, ""))
        return M("Développe : (%s − %d)²" % (ax, b), r, [E((a * a, "x²"), (-b * b, "")), E((a * a, "x²"), (-2 * a * b, "x"), (-b * b, "")), E((a * a, "x²"), (2 * a * b, "x"), (b * b, ""))],
                 "(a − b)² = a² − 2ab + b² : <b>%s</b>." % r)
    if k == "d":
        r = E((a * a, "x²"), (-b * b, ""))
        return M("Développe : (%s − %d)(%s + %d)" % (ax, b, ax, b), r, [E((a * a, "x²"), (b * b, "")), E((a * a, "x²"), (-2 * a * b, "x"), (-b * b, "")), E((a, "x²"), (-b * b, "")) if a > 1 else E((1, "x²"), (-b, ""))],
                 "(a − b)(a + b) = a² − b² : <b>%s</b>." % r)
    if k == "fp":
        return M("Factorise : %s" % E((a * a, "x²"), (2 * a * b, "x"), (b * b, "")), "(%s + %d)²" % (ax, b), ["(%s − %d)²" % (ax, b), "(%s + %d)(%s − %d)" % (ax, b, ax, b), "(%s + %d)²" % (ax, b * b)],
                 "On reconnaît a² + 2ab + b² : <b>(%s + %d)²</b>." % (ax, b))
    if k == "fm":
        return M("Factorise : %s" % E((a * a, "x²"), (-2 * a * b, "x"), (b * b, "")), "(%s − %d)²" % (ax, b), ["(%s + %d)²" % (ax, b), "(%s + %d)(%s − %d)" % (ax, b, ax, b), "(%s − %d)²" % (ax, b * b)],
                 "On reconnaît a² − 2ab + b² : <b>(%s − %d)²</b>." % (ax, b))
    return M("Factorise : %s" % E((a * a, "x²"), (-b * b, "")), "(%s − %d)(%s + %d)" % (ax, b, ax, b), ["(%s − %d)²" % (ax, b), "(%s + %d)²" % (ax, b), "(%s − %d)(%s + %d)" % (E((a * a, "x")), b, ax, b) if a > 1 else "(x − %d)(x + %d)" % (b * b, b * b)],
             "a² − b² = (a − b)(a + b) : <b>(%s − %d)(%s + %d)</b>." % (ax, b, ax, b))


def s2():
    k = R.choice(["fc", "fc", "diff2"])
    a, b = nz(-5, 5), nz(-9, 9)
    c, e = nz(-5, 5), nz(-9, 9)
    F = "(%s)" % E((1, "x"), (b, ""))
    if k == "fc":
        G1, G2 = "(%s)" % E((c, "x"), (e, "")), "(%s)" % E((a, "x"), (1, ""))
        q = "%s%s + %s%s" % (F, G1, F, G2)
        s_ = (c + a, e + 1)
        if s_ == (0, 0) or s_[0] == 0:
            return None
        r = "%s(%s)" % (F, E((s_[0], "x"), (s_[1], "")))
        return M("Factorise : %s" % q, r, ["%s(%s)" % (F, E((c * a, "x²"), (e + 1, ""))), "%s²(%s)" % (F, E((s_[0], "x"), (s_[1], ""))), "%s(%s)" % (F, E((c - a, "x"), (e - 1, ""))) if c != a else "%s(%s)" % (F, E((s_[0] + 1, "x"), (s_[1], "")))],
                 "%s est en facteur : %s[%s + %s] = <b>%s</b>." % (F, F, G1, G2, r))
    m = R.randint(1, 6)
    q = "%s² − %d" % (F, m * m)
    r = "(%s)(%s)" % (E((1, "x"), (b - m, "")), E((1, "x"), (b + m, "")))
    return M("Factorise : %s" % q, r, ["(%s)²" % E((1, "x"), (b - m, "")), "(%s)(%s)" % (E((1, "x"), (b - m * m, "")), E((1, "x"), (b + m * m, ""))), "(%s)(%s)" % (E((1, "x"), (-b - m, "")), E((1, "x"), (b + m, ""))) if b else "(x − %d)²" % m],
             "A² − B² = (A − B)(A + B) avec A = %s et B = %d : <b>%s</b>." % (F, m, r))


def s3():
    k = R.choice(["somme", "somme", "unx"])
    a, b = R.randint(1, 7), R.randint(2, 9)
    if k == "somme":
        c = R.randint(1, 7)
        return M("Écris sous une seule fraction (x ≠ 0) : %s + %d" % (fr(a, "x"), c), fr("%dx + %d" % (c, a) if c > 1 else "x + %d" % a, "x"),
                 [fr(a + c, "x"), fr(a + c, "x + 1"), fr("%d + %d" % (a, c), "x")],
                 "%d = %s, donc la somme vaut <b>%s</b>." % (c, fr("%sx" % (c if c > 1 else ""), "x"), fr("%dx + %d" % (c, a) if c > 1 else "x + %d" % a, "x")))
    return M("Écris sous une seule fraction (x ≠ 0, x ≠ −%d) : %s − %s" % (b, fr(1, "x"), fr(1, "x + %d" % b)), fr(b, "x(x + %d)" % b), [MINUS + fr(b, "x(x + %d)" % b), fr(1, "x(x + %d)" % b), fr(b, "2x + %d" % b)],
             "Dénominateur commun x(x + %d) : %s = <b>%s</b>." % (b, fr("(x + %d) − x" % b, "x(x + %d)" % b), fr(b, "x(x + %d)" % b)))


def s4():
    V = [("U = RI. Exprime I en fonction de U et R (R ≠ 0).", "I = " + fr("U", "R"), ["I = U − R", "I = UR", "I = " + fr("R", "U")]),
         ("d = vt. Exprime t en fonction de d et v (v ≠ 0).", "t = " + fr("d", "v"), ["t = d − v", "t = dv", "t = " + fr("v", "d")]),
         ("S = πr² (r &gt; 0). Exprime r en fonction de S.", "r = √(" + fr("S", "π") + ")", ["r = " + fr("S", "π"), "r = √S − π", "r = " + fr("S", "2π")]),
         ("V = πr²h. Exprime h en fonction de V et r.", "h = " + fr("V", "πr²"), ["h = V − πr²", "h = Vπr²", "h = " + fr("πr²", "V")]),
         ("P = 2(L + ℓ). Exprime L en fonction de P et ℓ.", "L = " + fr("P", "2") + " − ℓ", ["L = P − 2ℓ", "L = " + fr("P − ℓ", "2"), "L = 2P − ℓ"]),
         ("F = 1,8C + 32. Exprime C en fonction de F.", "C = " + fr("F − 32", "1,8"), ["C = 1,8F − 32", "C = " + fr("F", "1,8") + " − 32", "C = F − 33,8"]),
         ("E = " + fr(1, 2) + "mv² (m &gt; 0, v &gt; 0). Exprime v en fonction de E et m.", "v = √(" + fr("2E", "m") + ")", ["v = " + fr("2E", "m"), "v = √(2Em)", "v = √(" + fr("E", "2m") + ")"]),
         ("A = " + fr("(B + b)h", "2") + ". Exprime h en fonction de A, B et b.", "h = " + fr("2A", "B + b"), ["h = 2A − B − b", "h = " + fr("A", "2(B + b)"), "h = " + fr("B + b", "2A")])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "On isole la lettre en faisant les mêmes opérations des deux côtés : <b>%s</b>." % a_)


def s4b():
    k = R.choice(["diff", "ratio", "carre"])
    if k == "diff":
        a = R.randint(1, 9)
        return M("Pour tout réel x, on compare A = (x + %d)² et B = x² + %d. Que vaut A − B ?" % (a, a * a), E((2 * a, "x")), ["0", E((a * a, "")), E((2 * a, "x"), (2 * a * a, ""))],
                 "A − B = x² + %dx + %d − x² − %d = <b>%s</b> : A ⩾ B quand x ⩾ 0." % (2 * a, a * a, a * a, E((2 * a, "x"))))
    if k == "ratio":
        a, b = R.choice([(12, 15), (24, 30), (40, 50), (9, 12)])
        return M("Pour comparer deux nombres positifs a = %d et b = %d par quotient, on calcule a ÷ b = %s. Que conclut-on ?" % (a, b, d(Fr(a, b))), "a &lt; b, car a ÷ b &lt; 1", ["a &gt; b, car a ÷ b &gt; 0", "a = b", "on ne peut rien conclure"],
                 "Pour des positifs, a ÷ b &lt; 1 ⇔ a &lt; b : <b>a &lt; b</b> (a vaut %s %% de b)." % d(Fr(a * 100, b)))
    a = R.choice([Fr(1, 2), Fr(3, 10), Fr(1, 4), Fr(7, 10)])
    return M("Si 0 &lt; x &lt; 1, comment se rangent x, x² et √x ? (exemple : x = %s)" % d(a), "x² &lt; x &lt; √x", ["√x &lt; x &lt; x²", "x &lt; x² &lt; √x", "x = x² = √x"],
             "Pour x = %s : x² = %s et √x ≈ %s : <b>x² &lt; x &lt; √x</b>." % (d(a), d(a * a), d(Fr(round(float(a) ** 0.5 * 100), 100))))


def s5():
    k = R.choice(["aire", "aire", "bande", "nombre"])
    a = R.randint(1, 9)
    if k == "aire":
        return M("Un carré a pour côté x + %d. Quelle expression développée donne son aire ?" % a, E((1, "x²"), (2 * a, "x"), (a * a, "")), [E((1, "x²"), (a * a, "")), E((4, "x"), (4 * a, "")), E((1, "x²"), (a, "x"), (a * a, ""))],
                 "(x + %d)² = <b>%s</b>." % (a, E((1, "x²"), (2 * a, "x"), (a * a, ""))))
    if k == "bande":
        return M("Une allée de %d m de large entoure une pelouse carrée de côté x. Quelle est l’aire de l’allée, factorisée ?" % a, "(x + %d)² − x² = %d(x + %d)" % (2 * a, 4 * a, a),
                 ["%d" % (4 * a * a), "(x + %d)² − x² = %dx" % (a, 2 * a), "(x + %d)²" % (2 * a)],
                 "Grand carré de côté x + %d : (x + %d)² − x² = %dx + %d = <b>%d(x + %d)</b>." % (2 * a, 2 * a, 4 * a, 4 * a * a, 4 * a, a))
    n = R.randint(11, 99)
    return M("Calcule %d² − %d² sans calculatrice." % (n + 1, n - 1), str(4 * n), [str(2), str(2 * n), str((n + 1) ** 2 - n * n)],
             "(a − b)(a + b) = (%d − %d)(%d + %d) = 2 × %d = <b>%d</b>." % (n + 1, n - 1, n + 1, n - 1, 2 * n, 4 * n))


def main():
    seen = set()
    sets = [("Identités remarquables", mix(R, seen, [(s1, 20)])), ("Factoriser", mix(R, seen, [(s2, 20)])),
            ("Expressions fractionnaires", mix(R, seen, [(s3, 20)])), ("Formules et comparaisons", mix(R, seen, [(s4, 8), (s4b, 12)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["(a + b)² = a² + 2ab + b² ; (a − b)² = a² − 2ab + b² ; (a − b)(a + b) = a² − b², à utiliser dans les deux sens.",
              "Pour additionner des fractions avec des lettres, on met au même dénominateur (en précisant les valeurs interdites).",
              "Pour isoler une lettre dans une formule, on fait la même opération des deux côtés. Pour comparer A et B, on étudie le signe de A − B."],
             [("Isoler t dans d = vt", ["on divise par v (v ≠ 0)"], "t = d/v")],
             [["(a + b)² = a² + b²", "Il manque le double produit 2ab."], ["1/x + 1/y = 2/(x + y)", "On met au même dénominateur : (x + y)/(xy)."],
              ["Dans d = vt, écrire t = d − v", "v multiplie t : on divise, t = d/v."]])
    faq = [("Quand choisir la forme développée ou factorisée ?", "La forme factorisée sert à résoudre une équation produit nul ou étudier un signe ; la forme développée sert à réduire ou calculer une image."),
           ("Pourquoi préciser x ≠ 0 ?", "Un dénominateur ne peut pas être nul.")]
    unit("seconde", R, "calcul-litteral", "N",
         "Utiliser les identités remarquables dans les deux sens ; factoriser par un facteur commun ; transformer des expressions fractionnaires simples ; isoler une variable dans une formule ; comparer deux quantités par différence ou par quotient",
         "Calcul littéral", "Calcul littéral",
         "Fiches de maths seconde sur le calcul littéral : identités remarquables, factorisation, expressions fractionnaires, formules et comparaisons. 100 exercices corrigés.",
         "(a − b)(a + b) = a² − b²", "Choisir la forme la plus adaptée : développée ou factorisée", body, faq, sets, 5)


if __name__ == "__main__":
    main()
