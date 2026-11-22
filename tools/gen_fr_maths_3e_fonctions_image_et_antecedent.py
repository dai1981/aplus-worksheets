# -*- coding: utf-8 -*-
"""
France Maths 3e : Notion de fonction — image, antécédent, tableau de valeurs, représentation graphique
  python3 tools/gen_fr_maths_3e_fonctions_image_et_antecedent.py
Erreurs : confondre image et antécédent, lire sur le mauvais axe, croire qu’un nombre a un seul antécédent, (−3)² = −9.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60408)
K = Kids(R)
FN = ["f", "g", "h"]


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    f = R.choice(FN)
    x = nz(-6, 7)
    k = R.choice(["aff", "carre", "carre", "prod"])
    if k == "aff":
        a, b = nz(-5, 5), R.randint(-9, 9)
        y, form, w = a * x + b, E((a, "x"), (b, "")), [a + x + b, a * (x + b), -a * x + b]
    elif k == "carre":
        a, b = R.choice([1, 2, -1]), R.randint(-6, 6)
        c = R.randint(-9, 9)
        y, form = a * x * x + b * x + c, E((a, "x²"), (b, "x"), (c, ""))
        w = [-a * x * x + b * x + c, a * 2 * x + b * x + c, a * x * x - b * x + c]
    else:
        a = nz(-4, 4)
        y, form = (x + a) * (x - a), "(x %s %d)(x %s %d)" % ("+" if a > 0 else MINUS, abs(a), MINUS if a > 0 else "+", abs(a))
        w = [x * x + a * a, (x + a) + (x - a), x * x - a]
    w = [d(v) for v in w if v != y]
    return M("On considère la fonction %s : x ↦ %s. Quelle est l’image de %s par %s ?" % (f, form.replace(" ", NB), d(x), f), d(y), w,
             "%s(%s) = <b>%s</b>." % (f, d(x), d(y)))


def s2():
    f = R.choice(FN)
    a, b = nz(-5, 5), R.randint(-9, 9)
    x = R.randint(-6, 8)
    y = a * x + b
    if (a, b) == (1, 0):
        return None
    k = R.choice(["ant", "ant", "voc"])
    if k == "ant":
        return M("Soit %s(x) = %s. Quel est l’antécédent de %s par %s ?" % (f, E((a, "x"), (b, "")), d(y), f), d(x), [d(a * y + b), d(Fr(y + b, a)) if (Fr(y + b, a)).denominator == 1 and Fr(y + b, a) != x else d(x + 1), d(Fr(y, a) - b) if Fr(y, a).denominator == 1 and Fr(y, a) - b != x else d(x - 1)],
                 "On résout %s = %s : %s = %s, donc x = <b>%s</b>." % (E((a, "x"), (b, "")), d(y), E((a, "x")), d(y - b), d(x)))
    V = [("%s(3) = 7. Que peut-on dire ?" % f, "7 est l’image de 3", ["3 est l’image de 7", "7 est un antécédent de 3", "%s vaut 7 partout" % f]),
         ("%s(−2) = 5. Quel nombre est un antécédent de 5 ?" % f, "−2", ["5", "−5", "2"]),
         ("Un nombre peut-il avoir plusieurs antécédents par une fonction ?", "oui", ["non, jamais", "seulement 0", "seulement s’il est négatif"]),
         ("Un nombre peut-il avoir plusieurs images par une fonction ?", "non, une seule", ["oui, toujours deux", "oui, parfois", "aucune"]),
         ("Quelle phrase est équivalente à « %s(4) = 0 » ?" % f, "4 a pour image 0 par %s" % f, ["0 a pour image 4 par %s" % f, "%s est nulle" % f, "4 n’a pas d’image"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s3():
    f = R.choice(FN)
    xs = [-3, -2, -1, 0, 1, 2, 3]
    k = R.choice(["sq", "aff", "cube"])
    if k == "sq":
        c = R.randint(-4, 4)
        F = lambda x: x * x + c
    elif k == "aff":
        a, b = nz(-3, 3), R.randint(-4, 4)
        F = lambda x: a * x + b
    else:
        F = lambda x: x * x * x - 3 * x
    ys = [F(x) for x in xs]
    tb = table(["x"] + [d(x) for x in xs], [["%s(x)" % f] + [d(y) for y in ys]])
    i = R.randrange(len(xs))
    q = R.choice(["img", "ant"])
    if q == "img":
        return M("%s<br>D’après ce tableau, quelle est l’image de %s par %s ?" % (tb, d(xs[i]), f), d(ys[i]), [d(xs[ys.index(xs[i])]) if xs[i] in ys and xs[ys.index(xs[i])] != ys[i] else d(ys[i] + 1), d(-ys[i]) if ys[i] else "1", d(ys[(i + 1) % 7])] if ys[(i + 1) % 7] != ys[i] else [d(ys[i] + 1), d(-ys[i]) if ys[i] else "1", d(xs[i] + 5)],
                 "On lit dans la colonne x = %s : <b>%s(%s) = %s</b>." % (d(xs[i]), f, d(xs[i]), d(ys[i])))
    y = ys[i]
    ants = [xs[j] for j in range(7) if ys[j] == y]
    ans = " et ".join(d(v) for v in ants)
    w = [d(y) if y not in ants else d(y + 10), d(ants[0]) if len(ants) > 1 else d(-ants[0]) if ants[0] else "1", " et ".join(d(v) for v in ants + [ants[-1] + 1])]
    return M("%s<br>D’après ce tableau, quel(s) antécédent(s) de %s par %s lit-on ?" % (tb, d(y), f), ans, w,
             "On cherche %s dans la ligne %s(x) : <b>%s</b>." % (d(y), f, ans))


def s4():
    f = R.choice(FN)
    c = R.choice([-4, -3, -2, -1, 0, 1, 2])
    a = R.choice([1, -1])
    F = lambda x: a * (x * x) + c if a == 1 else -(x * x) + c + 9
    xs = list(range(-3, 4))
    pts = [(x, F(x)) for x in xs]
    ys = [y for _, y in pts]
    lo, hi = min(ys) - 1, max(ys) + 1
    lo -= lo % 2
    hi += hi % 2
    svg = relabel(de_k10.kurve([(lambda x: float(F(x)), BLUE, "")], (-3, 3, 1), (lo, hi, 1 if hi - lo <= 12 else 2), W=340, H=300), "courbe d’une fonction")
    k = R.choice(["img", "ant", "ant"])
    x = R.choice(xs)
    y = F(x)
    if k == "img":
        return M("<div class='qfig'>%s</div>Voici la courbe de %s. Lis l’image de %s par %s." % (svg, f, d(x), f), d(y), [d(x) if x != y else d(y + 2), d(y + 1), d(F(-x) + 1) if F(-x) + 1 != y else d(y - 1)],
                 "On part de x = %s sur l’axe des abscisses, on lit l’ordonnée du point de la courbe : <b>%s</b>." % (d(x), d(y)))
    ants = sorted({xx for xx in xs if F(xx) == y})
    ans = " et ".join(d(v) for v in ants)
    w = [d(ants[0]) if len(ants) > 1 else d(-ants[0]) if ants[0] else "1", d(y) if y not in ants else d(y + 5), " et ".join(d(v) for v in ants + [ants[-1] + 1]) if ants[-1] + 1 <= 3 else d(ants[0] - 1)]
    return M("<div class='qfig'>%s</div>Voici la courbe de %s. Quel(s) antécédent(s) de %s lit-on ?" % (svg, f, d(y)), ans, w,
             "On part de %s sur l’axe des ordonnées, on cherche les points de la courbe à cette hauteur et on lit leurs abscisses : <b>%s</b>." % (d(y), ans))


def s5():
    k = R.choice(["aire", "prix", "chute", "tableur"])
    if k == "aire":
        x = R.randint(1, 10)
        return M("Pour un carré de côté x cm, on note A(x) son aire. Combien vaut A(%d) ?" % x, "%d cm²" % (x * x), ["%d cm²" % (4 * x), "%d cm²" % (2 * x), "%d cm²" % (x + 4)], "A(x) = x², donc A(%d) = <b>%d cm²</b>." % (x, x * x))
    if k == "prix":
        a, b = R.randint(2, 6), R.randint(5, 20)
        y = a * R.randint(2, 15) + b
        return M("Le prix d’une course de taxi est P(x) = %dx + %d (x en km). Pour quelle distance paie-t-on %d € ?" % (a, b, y), "%s km" % d(Fr(y - b, a)), ["%s km" % d(a * y + b), "%s km" % d(Fr(y, a)) if (Fr(y, a) * 100).denominator == 1 else "%s km" % d(Fr(y - b, a) + 1), "%s km" % d(Fr(y + b, a)) if (Fr(y + b, a) * 100).denominator == 1 else "%s km" % d(Fr(y - b, a) - 1)],
                 "On cherche l’antécédent de %d : %dx + %d = %d, donc x = <b>%s km</b>." % (y, a, b, y, d(Fr(y - b, a))))
    if k == "chute":
        t = R.randint(1, 4)
        return M("La hauteur d’une balle (en m) en fonction du temps t (en s) est h(t) = 20 − 5t². Que vaut h(%d) ?" % t, "%s m" % d(20 - 5 * t * t), ["%s m" % d(20 - 5 * t), "%s m" % d((20 - 5 * t) ** 2) if t < 4 else "%s m" % d(20 + 5 * t * t), "%s m" % d(20 - 10 * t)],
                 "h(%d) = 20 − 5 × %d² = 20 − %d = <b>%s m</b>." % (t, t, 5 * t * t, d(20 - 5 * t * t)))
    a, b = R.randint(2, 9), R.randint(1, 9)
    return M("Dans un tableur, A2 contient x. On veut calculer f(x) = %dx² − %d en B2. Quelle formule écrire ?" % (a, b), "=%d*A2^2-%d" % (a, b), ["=%dA2^2-%d" % (a, b), "=(%d*A2)^2-%d" % (a, b), "=%d*A2*2-%d" % (a, b)],
             "On commence par =, * pour multiplier, ^2 pour le carré : <b>=%d*A2^2-%d</b>." % (a, b))


def main():
    seen = set()
    sets = [("Calculer une image", mix(R, seen, [(s1, 20)])), ("Antécédents et vocabulaire", mix(R, seen, [(s2, 20)])),
            ("Tableaux de valeurs", mix(R, seen, [(s3, 20)])), ("Lire une courbe", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une <b>fonction</b> f associe à chaque nombre x un unique nombre f(x), appelé l’<b>image</b> de x. On note f : x ↦ f(x).",
              "Si f(a) = b, alors b est l’image de a et a est <b>un antécédent</b> de b. Un nombre peut avoir plusieurs antécédents, ou aucun.",
              "Sur la courbe de f, l’image se lit sur l’axe des ordonnées, l’antécédent sur l’axe des abscisses."],
             [("f(x) = x² − 3x ; image de −2", ["f(−2) = (−2)² − 3 × (−2)", "= 4 + 6"], "10")],
             [["Confondre image et antécédent", "f(3) = 7 : 7 est l’image, 3 est l’antécédent."], ["(−2)² = −4", "(−2)² = 4."],
              ["Ne donner qu’un antécédent", "On cherche tous les points de la courbe à la bonne hauteur."]])
    faq = [("Comment calculer un antécédent ?", "On résout l’équation f(x) = b."),
           ("Tous les nombres ont-ils un antécédent ?", "Non : avec f(x) = x², le nombre −4 n’a aucun antécédent.")]
    unit("3e", R, "fonctions-image-et-antecedent", "F",
         "Comprendre la notion de fonction ; utiliser les notations f(x) et x ↦ f(x) ; calculer une image ; déterminer un antécédent par le calcul, avec un tableau de valeurs ou une représentation graphique",
         "Fonctions : image et antécédent", "Fonctions : image et antécédent",
         "Fiches de maths 3e sur les fonctions : notation f(x), calcul d’images, antécédents, tableaux de valeurs, lecture graphique et problèmes. 100 exercices corrigés.",
         "f(a) = b : b est l’image de a, a est un antécédent de b", "Image : axe des ordonnées ; antécédent : axe des abscisses", body, faq, sets, 8)


if __name__ == "__main__":
    main()
