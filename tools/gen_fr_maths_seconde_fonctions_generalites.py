# -*- coding: utf-8 -*-
"""
France Maths Seconde : Fonctions — ensemble de définition, images, antécédents, courbe, parité, résolutions graphiques
  python3 tools/gen_fr_maths_seconde_fonctions_generalites.py
Erreurs : confondre image et antécédent, oublier une valeur interdite, (−x)² ≠ x², lire f(x) = k sur le mauvais axe.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60508)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    k = R.choice(["frac", "frac", "racine", "poly"])
    a = nz(-9, 9)
    if k == "frac":
        return M("Quel est l’ensemble de définition de f(x) = %s ?" % fr(3, E((1, "x"), (a, ""))), "ℝ ∖ {%s}" % d(-a), ["ℝ ∖ {%s}" % d(a), "ℝ", "]%s ; +∞[" % d(-a)],
                 "Le dénominateur ne doit pas être nul : x %s %d ≠ 0 ⇔ x ≠ %s : <b>ℝ ∖ {%s}</b>." % ("+" if a > 0 else MINUS, abs(a), d(-a), d(-a)))
    if k == "racine":
        return M("Quel est l’ensemble de définition de f(x) = √(%s) ?" % E((1, "x"), (a, "")), "[%s ; +∞[" % d(-a), ["]%s ; +∞[" % d(-a), "[%s ; +∞[" % d(a), "ℝ"],
                 "Il faut x %s %d ⩾ 0 ⇔ x ⩾ %s : <b>[%s ; +∞[</b>." % ("+" if a > 0 else MINUS, abs(a), d(-a), d(-a)))
    return M("Quel est l’ensemble de définition de f(x) = %s ?" % E((1, "x²"), (a, "x"), (nz(-9, 9), "")), "ℝ", ["ℝ ∖ {0}", "[0 ; +∞[", "ℝ ∖ {%s}" % d(-a)],
             "Un polynôme se calcule pour tout réel : <b>ℝ</b>.")


def s2():
    a, b, c = R.choice([1, 2, -1, 3]), R.randint(-6, 6), R.randint(-9, 9)
    form = E((a, "x²"), (b, "x"), (c, ""))
    k = R.choice(["img", "img", "point"])
    x = nz(-5, 5)
    y = a * x * x + b * x + c
    if k == "img":
        return M("f(x) = %s. Calcule f(%s)." % (form, d(x)), d(y), [d(-a * x * x + b * x + c), d(a * 2 * x + b * x + c), d(a * x * x - b * x + c)] if b else [d(-a * x * x + c), d(a * 2 * x + c), d(y + 1)],
                 "f(%s) = %s × %s² %s = <b>%s</b>." % (d(x), d(a), par(x), (" + %s × %s" % (d(b), par(x)) if b else "") + (" + %s" % par(c) if c else ""), d(y)))
    yy = y + R.choice([0, 0, 1, -2])
    ok = yy == y
    return M("f(x) = %s. Le point A(%s ; %s) appartient-il à la courbe de f ?" % (form, d(x), d(yy)), "oui" if ok else "non", ["non" if ok else "oui", "seulement si %s &gt; 0" % d(x), "on ne peut pas savoir sans tracer"],
             "f(%s) = %s %s %s : <b>%s</b>." % (d(x), d(y), "=" if ok else "≠", d(yy), "oui" if ok else "non"))


def s3():
    k = R.choice(["ant1", "ant2", "ant0"])
    if k == "ant1":
        a, b = nz(-5, 5), R.randint(-9, 9)
        x = R.randint(-6, 6)
        y = a * x + b
        return M("f(x) = %s. Quel est l’antécédent de %s par f ?" % (E((a, "x"), (b, "")), d(y)), d(x), [d(a * y + b), d(x + 1), d(-x) if x else "1"],
                 "On résout %s = %s : x = <b>%s</b>." % (E((a, "x"), (b, "")), d(y), d(x)))
    if k == "ant2":
        n = R.randint(1, 8)
        c = R.randint(-5, 5)
        return M("f(x) = %s. Quels sont les antécédents de %s par f ?" % (E((1, "x²"), (c, "")), d(n * n + c)), "%s et %s" % (d(-n), d(n)), [d(n), d(n * n + 2 * c) if n * n + 2 * c != n else "aucun", "%s et %s" % (d(-n * n), d(n * n)) if n > 1 else "aucun"],
                 "x² %s = %s ⇔ x² = %d ⇔ x = <b>−%d ou %d</b>." % ((" + %d" % c) if c > 0 else (" − %d" % -c) if c else "", d(n * n + c), n * n, n, n))
    c = R.randint(0, 6)
    v = -R.randint(1, 9)
    return M("f(x) = x² + %d. Combien d’antécédents le nombre %s a-t-il par f ?" % (c, d(v)), "aucun", ["un", "deux", "une infinité"], "x² + %d ⩾ %d &gt; %s pour tout x : <b>aucun</b>." % (c, c, d(v)))


def s4():
    k = R.choice(["par", "par", "graph"])
    V = [("x²", "paire"), ("x³", "impaire"), ("|x|", "paire"), (fr(1, "x"), "impaire"), ("x² + 1", "paire"), ("2x", "impaire"), ("x + 1", "ni paire ni impaire"), ("x² + x", "ni paire ni impaire"), ("x⁴ − 3x²", "paire"), ("x³ − x", "impaire")]
    if k == "par":
        f, ans = R.choice(V)
        return M("La fonction f : x ↦ %s est…" % f, ans, [o for o in ["paire", "impaire", "ni paire ni impaire", "paire et impaire"] if o != ans],
                 "On compare f(−x) et f(x) : <b>%s</b>." % ans)
    W_ = [("La courbe d’une fonction paire est symétrique par rapport…", "à l’axe des ordonnées", ["à l’axe des abscisses", "à l’origine", "à la droite y = x"]),
          ("La courbe d’une fonction impaire est symétrique par rapport…", "à l’origine du repère", ["à l’axe des ordonnées", "à l’axe des abscisses", "à la droite y = x"]),
          ("f est paire et f(3) = 7. Que vaut f(−3) ?", "7", ["−7", "3", "on ne peut pas savoir"]),
          ("f est impaire et f(2) = 5. Que vaut f(−2) ?", "−5", ["5", "−2", "on ne peut pas savoir"])]
    q, a_, w = R.choice(W_)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s4b():
    k = R.choice(["val", "val", "form"])
    if k == "val":
        x, y = R.randint(1, 9), nz(-12, 12)
        par_ = R.choice(["paire", "impaire"])
        r = y if par_ == "paire" else -y
        return M("f est %s et f(%d) = %s. Que vaut f(−%d) ?" % (par_, x, d(y), x), d(r), [d(-r), d(x) if x not in (r, -r) else d(r + 1), "on ne peut pas savoir"],
                 "%s : f(−%d) = <b>%s</b>." % ("f(−x) = f(x)" if par_ == "paire" else "f(−x) = −f(x)", x, d(r)))
    a, b = nz(-5, 5), nz(-9, 9)
    V = [(E((a, "x²"), (b, "")), "paire"), (E((a, "x³"), (b, "x")), "impaire"), (E((a, "x²"), (b, "x")), "ni paire ni impaire"), (E((a, "x"), (b, "")), "ni paire ni impaire"), (E((a, "x⁴"), (b, "x²")), "paire")]
    f, ans = R.choice(V)
    return M("La fonction f : x ↦ %s est…" % f, ans, [o for o in ["paire", "impaire", "ni paire ni impaire", "paire et impaire"] if o != ans],
             "On calcule f(−x) et on compare avec f(x) et −f(x) : <b>%s</b>." % ans)


def s5():
    c = R.randint(-2, 2)
    svg = relabel(de_k10.kurve([(lambda x: x * x - 4 + c, BLUE, "")], (-3, 3, 1), (-5 + c, 6 + c, 1), W=340, H=320), "courbe de f")
    k = R.choice(["eq", "eq", "ineq", "zero"])
    m = R.choice([1, 2, 3])
    if k == "eq":
        y = m * m - 4 + c
        return M("<div class='qfig'>%s</div>Voici la courbe de f sur [−3 ; 3]. Résous graphiquement f(x) = %s." % (svg, d(y)), "S = {−%d ; %d}" % (m, m), ["S = {%d}" % m, "S = {%s}" % d(y), "S = {%d ; %d}" % (m, m + 1)],
                 "On cherche les abscisses des points de la courbe d’ordonnée %s : <b>S = {−%d ; %d}</b>." % (d(y), m, m))
    if k == "zero":
        if c not in (0,):
            return None
        return M("<div class='qfig'>%s</div>Voici la courbe de f sur [−3 ; 3]. Résous graphiquement f(x) = 0." % svg, "S = {−2 ; 2}", ["S = {−4}", "S = {0}", "S = ∅"], "La courbe coupe l’axe des abscisses en −2 et 2 : <b>S = {−2 ; 2}</b>.")
    m = min(m, 2)
    y = m * m - 4 + c
    return M("<div class='qfig'>%s</div>Voici la courbe de f sur [−3 ; 3]. Résous graphiquement f(x) &lt; %s." % (svg, d(y)), "S = ]−%d ; %d[" % (m, m), ["S = [−3 ; −%d[ ∪ ]%d ; 3]" % (m, m), "S = [−%d ; %d]" % (m, m), "S = ]−∞ ; %d[" % m],
             "La courbe est sous la droite y = %s entre −%d et %d : <b>S = ]−%d ; %d[</b>." % (d(y), m, m, m, m))


def main():
    seen = set()
    sets = [("Ensemble de définition", mix(R, seen, [(s1, 20)])), ("Images et points de la courbe", mix(R, seen, [(s2, 20)])),
            ("Antécédents", mix(R, seen, [(s3, 20)])), ("Parité", mix(R, seen, [(s4, 8), (s4b, 12)])), ("Résolutions graphiques", mix(R, seen, [(s5, 20)]))]
    body = L(["Une fonction f associe à chaque x de son <b>ensemble de définition</b> un unique nombre f(x), son image. On exclut les valeurs qui annulent un dénominateur ou rendent négatif ce qui est sous une racine.",
              "M(x ; y) est sur la courbe de f si et seulement si y = f(x). Un antécédent de k est une solution de f(x) = k.",
              "f est <b>paire</b> si f(−x) = f(x) (courbe symétrique par rapport à l’axe des ordonnées), <b>impaire</b> si f(−x) = −f(x) (symétrique par rapport à l’origine)."],
             [("f(x) = x² − 3x ; f(−2)", ["(−2)² − 3 × (−2)", "4 + 6"], "f(−2) = 10")],
             [["Confondre image et antécédent", "f(3) = 7 : 7 est l’image de 3, 3 est un antécédent de 7."], ["(−2)² = −4", "(−2)² = 4."], ["Oublier une valeur interdite", "On vérifie dénominateurs et racines."]])
    faq = [("Comment résoudre f(x) = k graphiquement ?", "On trace la droite horizontale y = k et on lit les abscisses des points d’intersection avec la courbe."),
           ("Une fonction peut-elle être ni paire ni impaire ?", "Oui, c’est même le cas le plus fréquent (par exemple x ↦ x + 1).")]
    unit("seconde", R, "fonctions-generalites", "F",
         "Déterminer l’ensemble de définition d’une fonction ; calculer des images et des antécédents ; tester l’appartenance d’un point à une courbe ; reconnaître une fonction paire ou impaire ; résoudre graphiquement f(x) = k et f(x) &lt; k",
         "Fonctions : définition, images, antécédents et parité", "Fonctions : généralités",
         "Fiches de maths seconde sur les fonctions : ensemble de définition, images, antécédents, courbe représentative, parité et résolutions graphiques. 100 exercices corrigés.",
         "M(x ; y) ∈ C_f ⇔ y = f(x)", "Paire : f(−x) = f(x) ; impaire : f(−x) = −f(x)", body, faq, sets, 8)


if __name__ == "__main__":
    main()
