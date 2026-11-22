# -*- coding: utf-8 -*-
"""
France Maths Seconde : Fonctions de référence (carré, inverse, racine carrée, cube, valeur absolue)
  python3 tools/gen_fr_maths_seconde_fonctions_de_reference.py
Erreurs : x² ⩽ 9 ⇔ x ⩽ 3, 1/x croissante sur ℝ*, comparer des carrés de négatifs sans changer l’ordre, √ définie sur ℝ.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60509)
K = Kids(R)
REF = [("carré", "x²"), ("inverse", fr(1, "x")), ("racine carrée", "√x"), ("cube", "x³"), ("valeur absolue", "|x|")]


def s1():
    k = R.choice(["dom", "var", "graph"])
    nm, f = R.choice(REF)
    if k == "dom":
        D = {"carré": "ℝ", "inverse": "ℝ ∖ {0}", "racine carrée": "[0 ; +∞[", "cube": "ℝ", "valeur absolue": "ℝ"}
        return M("Quel est l’ensemble de définition de la fonction %s (x ↦ %s) ?" % (nm, f), D[nm], [x for x in ["ℝ", "ℝ ∖ {0}", "[0 ; +∞[", "]0 ; +∞["] if x != D[nm]][:3],
                 "<b>%s</b>." % D[nm])
    if k == "var":
        V = {"carré": "décroissante sur ]−∞ ; 0], croissante sur [0 ; +∞[", "inverse": "décroissante sur ]−∞ ; 0[ et sur ]0 ; +∞[", "racine carrée": "croissante sur [0 ; +∞[",
             "cube": "croissante sur ℝ", "valeur absolue": "décroissante sur ]−∞ ; 0], croissante sur [0 ; +∞["}
        opts = sorted(set(V.values()) - {V[nm]})
        R.shuffle(opts)
        return M("Quelles sont les variations de la fonction %s ?" % nm, V[nm], opts[:3], "La fonction %s est <b>%s</b>." % (nm, V[nm]))
    G = {"carré": "une parabole de sommet O", "inverse": "une hyperbole", "racine carrée": "une demi-parabole couchée partant de O", "cube": "une courbe symétrique par rapport à O, croissante", "valeur absolue": "un « V » de sommet O"}
    opts = [v for k_, v in G.items() if k_ != nm]
    R.shuffle(opts)
    return M("La courbe de la fonction %s est…" % nm, G[nm], opts[:3], "Réponse : <b>%s</b>." % G[nm])


def s1b():
    k = R.choice(["carré", "inverse", "racine carrée", "cube", "valeur absolue"])
    if k == "carré":
        x = R.choice([Fr(R.randint(-12, 12)), Fr(R.randint(-9, 9), 10)])
        if x in (0, 1):
            return None
        return M("Quelle est l’image de %s par la fonction carré ?" % d(x), d(x * x), [d(-x * x) if x else "1", d(2 * x) if 2 * x != x * x else d(x * x + 1), d(abs(x))] if x not in (0, 1) else [d(2 * x + 1), d(-1), d(3)],
                 "%s² = <b>%s</b>." % (par(x), d(x * x)))
    if k == "inverse":
        x = R.choice([2, 4, 5, 8, 10, -2, -4, -5, Fr(1, 2), Fr(-1, 4)])
        x = Fr(x)
        return M("Quelle est l’image de %s par la fonction inverse ?" % d(x), d(1 / x), [d(-x), d(-1 / x), d(x)], "1 ÷ %s = <b>%s</b>." % (par(x), d(1 / x)))
    if k == "racine carrée":
        n = R.randint(1, 15)
        return M("Quelle est l’image de %d par la fonction racine carrée ?" % (n * n), str(n), [d(Fr(n * n, 2)), str(n * n * n * n) if n < 6 else str(n + 1), d(-n)], "√%d = <b>%d</b>." % (n * n, n))
    if k == "cube":
        x = R.randint(-5, 5)
        if x in (0, 1, -1):
            return None
        return M("Quelle est l’image de %s par la fonction cube ?" % d(x), d(x ** 3), [d(3 * x), d(-x ** 3), d(x * x)], "%s³ = <b>%s</b>." % (par(x), d(x ** 3)))
    x = R.choice([Fr(R.randint(-20, -1)), Fr(R.randint(-99, -1), 10)])
    return M("Quelle est l’image de %s par la fonction valeur absolue ?" % d(x), d(-x), [d(x), d(x * x) if x * x != -x else "0", "0"], "|%s| = <b>%s</b>." % (d(x), d(-x)))


def s2():
    k = R.choice(["sq_neg", "sq_pos", "inv", "racine", "cube"])
    if k == "sq_neg":
        a, b = sorted(R.sample(range(-15, 0), 2))
        a, b = Fr(a, R.choice([1, 10])), Fr(b, R.choice([1, 10]))
        if a == b:
            return None
        lo, hi = min(a, b), max(a, b)
        return M("Sans calculer, compare %s² et %s²." % (par(lo), par(hi)), "%s² &gt; %s²" % (par(lo), par(hi)), ["%s² &lt; %s²" % (par(lo), par(hi)), "%s² = %s²" % (par(lo), par(hi)), "on ne peut pas comparer"],
                 "%s &lt; %s ⩽ 0 et la fonction carré est décroissante sur ]−∞ ; 0] : l’ordre change, <b>%s² &gt; %s²</b>." % (d(lo), d(hi), par(lo), par(hi)))
    if k == "sq_pos":
        a, b = sorted(R.sample(range(1, 30), 2))
        a, b = Fr(a, 10), Fr(b, 10)
        return M("Sans calculer, compare %s² et %s²." % (d(a), d(b)), "%s² &lt; %s²" % (d(a), d(b)), ["%s² &gt; %s²" % (d(a), d(b)), "%s² = %s²" % (d(a), d(b)), "on ne peut pas comparer"],
                 "0 ⩽ %s &lt; %s et la fonction carré est croissante sur [0 ; +∞[ : <b>%s² &lt; %s²</b>." % (d(a), d(b), d(a), d(b)))
    if k == "inv":
        a, b = sorted(R.sample(range(2, 40), 2))
        sg = R.choice([1, -1])
        a, b = Fr(a * sg, 10), Fr(b * sg, 10)
        lo, hi = min(a, b), max(a, b)
        return M("Sans calculer, compare %s et %s." % (fr(1, d(lo)), fr(1, d(hi))), "%s &gt; %s" % (fr(1, d(lo)), fr(1, d(hi))), ["%s &lt; %s" % (fr(1, d(lo)), fr(1, d(hi))), "%s = %s" % (fr(1, d(lo)), fr(1, d(hi))), "on ne peut pas comparer"],
                 "%s &lt; %s sont de même signe et la fonction inverse est décroissante sur cet intervalle : <b>%s &gt; %s</b>." % (d(lo), d(hi), fr(1, d(lo)), fr(1, d(hi))))
    if k == "racine":
        a, b = sorted(R.sample(range(2, 99), 2))
        return M("Sans calculer, compare √%d et √%d." % (a, b), "√%d &lt; √%d" % (a, b), ["√%d &gt; √%d" % (a, b), "√%d = √%d" % (a, b), "on ne peut pas comparer"], "La fonction racine est croissante : <b>√%d &lt; √%d</b>." % (a, b))
    a, b = sorted(R.sample(range(-20, 20), 2))
    return M("Sans calculer, compare %s³ et %s³." % (par(a), par(b)), "%s³ &lt; %s³" % (par(a), par(b)), ["%s³ &gt; %s³" % (par(a), par(b)), "%s³ = %s³" % (par(a), par(b)), "on ne peut pas comparer"],
             "La fonction cube est croissante sur ℝ : <b>%s³ &lt; %s³</b>." % (par(a), par(b)))


def s3():
    a = R.randint(1, 10)
    k = R.choice(["le", "ge", "lt_inv", "rac", "abs"])
    if k == "le":
        return M("Résous x² ⩽ %d." % (a * a), "S = [−%d ; %d]" % (a, a), ["S = ]−∞ ; %d]" % a, "S = ]−∞ ; −%d] ∪ [%d ; +∞[" % (a, a), "S = [0 ; %d]" % a], "Les x dont le carré est au plus %d sont entre −%d et %d : <b>S = [−%d ; %d]</b>." % (a * a, a, a, a, a))
    if k == "ge":
        return M("Résous x² &gt; %d." % (a * a), "S = ]−∞ ; −%d[ ∪ ]%d ; +∞[" % (a, a), ["S = ]%d ; +∞[" % a, "S = ]−%d ; %d[" % (a, a), "S = ]−∞ ; −%d] ∪ [%d ; +∞[" % (a, a)], "<b>S = ]−∞ ; −%d[ ∪ ]%d ; +∞[</b>." % (a, a))
    if k == "lt_inv":
        return M("Résous %s &lt; %s pour x &gt; 0." % (fr(1, "x"), fr(1, a)), "S = ]%d ; +∞[" % a, ["S = ]0 ; %d[" % a, "S = ]%s ; +∞[" % fr(1, a), "S = ]−∞ ; %d[" % a], "La fonction inverse est décroissante sur ]0 ; +∞[ : 1/x &lt; 1/%d ⇔ x &gt; %d : <b>S = ]%d ; +∞[</b>." % (a, a, a))
    if k == "rac":
        return M("Résous √x ⩽ %d." % a, "S = [0 ; %d]" % (a * a), ["S = ]−∞ ; %d]" % (a * a), "S = [0 ; %d]" % a, "S = [0 ; √%d]" % a], "√x ⩽ %d ⇔ 0 ⩽ x ⩽ %d : <b>S = [0 ; %d]</b>." % (a, a * a, a * a))
    return M("Résous |x| &lt; %d." % a, "S = ]−%d ; %d[" % (a, a), ["S = ]−∞ ; %d[" % a, "S = ]−∞ ; −%d[ ∪ ]%d ; +∞[" % (a, a), "S = [−%d ; %d]" % (a, a)], "Les x à moins de %d de 0 : <b>S = ]−%d ; %d[</b>." % (a, a, a))


def s4():
    k = R.choice(["enc_sq", "enc_sq", "enc_inv", "enc_rac"])
    if k == "enc_sq":
        a, b = sorted(R.sample(range(-6, 7), 2))
        if a < 0 < b:
            lo, hi = 0, max(a * a, b * b)
            expl = "x prend la valeur 0, et la plus grande valeur de x² est %d" % hi
        elif b <= 0:
            lo, hi = b * b, a * a
            expl = "la fonction carré est décroissante sur ]−∞ ; 0] : l’ordre change"
        else:
            lo, hi = a * a, b * b
            expl = "la fonction carré est croissante sur [0 ; +∞["
        return M("Si %s ⩽ x ⩽ %s, quel encadrement de x² est le plus précis ?" % (d(a), d(b)), "%d ⩽ x² ⩽ %d" % (lo, hi), ["%d ⩽ x² ⩽ %d" % (a * a, b * b) if (a * a, b * b) != (lo, hi) else "%d ⩽ x² ⩽ %d" % (lo, hi + 1), "%s ⩽ x² ⩽ %s" % (d(-a * a) if a < 0 else d(a * a - 1), d(b * b)), "%s ⩽ x² ⩽ %s" % (d(2 * a), d(2 * b))],
                 "%s : <b>%d ⩽ x² ⩽ %d</b>." % (expl[0].upper() + expl[1:], lo, hi))
    if k == "enc_inv":
        a, b = sorted(R.sample([2, 4, 5, 8, 10], 2))
        return M("Si %d ⩽ x ⩽ %d, encadre %s." % (a, b, fr(1, "x")), "%s ⩽ %s ⩽ %s" % (d(Fr(1, b)), fr(1, "x"), d(Fr(1, a))), ["%s ⩽ %s ⩽ %s" % (d(Fr(1, a)), fr(1, "x"), d(Fr(1, b))), "%d ⩽ %s ⩽ %d" % (a, fr(1, "x"), b), "−%d ⩽ %s ⩽ −%d" % (b, fr(1, "x"), a)],
                 "La fonction inverse est décroissante sur ]0 ; +∞[ : <b>%s ⩽ 1/x ⩽ %s</b>." % (d(Fr(1, b)), d(Fr(1, a))))
    a, b = sorted(R.sample([1, 4, 9, 16, 25, 36, 49], 2))
    return M("Si %d ⩽ x ⩽ %d, encadre √x." % (a, b), "%d ⩽ √x ⩽ %d" % (int(a ** 0.5), int(b ** 0.5)), ["%s ⩽ √x ⩽ %s" % (d(Fr(a, 2)), d(Fr(b, 2))), "%d ⩽ √x ⩽ %d" % (a, b), "%d ⩽ √x ⩽ %d" % (int(b ** 0.5), int(a ** 0.5))],
             "La fonction racine est croissante : <b>%d ⩽ √x ⩽ %d</b>." % (int(a ** 0.5), int(b ** 0.5)))


def s5():
    k = R.choice(["pos", "pos", "aire", "graph"])
    if k == "pos":
        V = [("Sur [0 ; 1], comment se placent les courbes de x ↦ x² et x ↦ x³ ?", "la courbe de x³ est en dessous de celle de x²", ["la courbe de x³ est au-dessus de celle de x²", "elles sont confondues", "elles ne se coupent jamais"]),
             ("Sur [1 ; +∞[, comment se placent les courbes de x ↦ x² et x ↦ x³ ?", "la courbe de x³ est au-dessus de celle de x²", ["la courbe de x³ est en dessous de celle de x²", "elles sont confondues", "elles ne se coupent jamais"]),
             ("Sur [0 ; 1], comment se placent x, x² et √x ?", "x² ⩽ x ⩽ √x", ["√x ⩽ x ⩽ x²", "x ⩽ x² ⩽ √x", "x = x² = √x"]),
             ("En quels points se coupent les courbes de x ↦ x² et x ↦ √x ?", "en (0 ; 0) et (1 ; 1)", ["seulement en (0 ; 0)", "en (1 ; 1) seulement", "elles ne se coupent pas"])]
        q, a_, w = R.choice(V)
        return M(q, a_, w, "On compare sur des exemples puis on justifie (x³ − x² = x²(x − 1)) : <b>%s</b>." % a_)
    if k == "aire":
        lo, hi = R.choice([4, 9, 16, 25]), R.choice([36, 49, 64, 81, 100])
        a, b = int(lo ** 0.5), int(hi ** 0.5)
        return M("Un carré a une aire comprise entre %d cm² et %d cm². Entre quelles valeurs est son côté c ?" % (lo, hi), "entre %d et %d cm" % (a, b), ["entre %d et %d cm" % (lo, hi), "entre %s et %s cm" % (d(Fr(lo, 2)), d(Fr(hi, 2))), "entre %s et %s cm" % (d(Fr(lo, 4)), d(Fr(hi, 4)))],
                 "c = √A et la fonction racine est croissante : <b>entre %d et %d cm</b>." % (a, b))
    nm, f, F = R.choice([("carré", "x²", lambda x: x * x), ("cube", "x³", lambda x: x ** 3), ("valeur absolue", "|x|", abs), ("inverse", "1/x", lambda x: 1 / x if x else 0)])
    x = R.choice([-2, -1, 1, 2])
    return M("Quel point appartient à la courbe de la fonction %s ?" % nm, "(%s ; %s)" % (d(x), d(Fr(F(Fr(x))))), ["(%s ; %s)" % (d(x), d(-Fr(F(Fr(x))))) if F(Fr(x)) != 0 else "(1 ; 0)", "(%s ; %s)" % (d(Fr(F(Fr(x)))), d(x)) if Fr(F(Fr(x))) != x else "(%s ; %s)" % (d(x), d(x + 3)), "(%s ; %s)" % (d(x), d(2 * x))] if F(Fr(x)) != 2 * x else ["(%s ; %s)" % (d(x), d(-Fr(F(Fr(x))))), "(%s ; %s)" % (d(x), d(x * 3)), "(%s ; %s)" % (d(x), d(x + 5))],
             "On calcule l’image de %s : <b>%s</b>." % (d(x), d(Fr(F(Fr(x))))))


def main():
    seen = set()
    sets = [("Connaître les fonctions de référence", mix(R, seen, [(s1, 10), (s1b, 10)])), ("Comparer sans calculer", mix(R, seen, [(s2, 20)])),
            ("Résoudre avec les fonctions de référence", mix(R, seen, [(s3, 20)])), ("Encadrer", mix(R, seen, [(s4, 20)])), ("Positions relatives et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Carré x² : décroissante sur ]−∞ ; 0], croissante sur [0 ; +∞[ (parabole). Inverse 1/x : décroissante sur ]−∞ ; 0[ et sur ]0 ; +∞[ (hyperbole).",
              "Racine √x : définie et croissante sur [0 ; +∞[. Cube x³ : croissante sur ℝ. Valeur absolue |x| : comme le carré, en forme de V.",
              "Une fonction <b>croissante</b> conserve l’ordre, une fonction <b>décroissante</b> l’inverse : c’est ce qui permet de comparer et d’encadrer."],
             [("−3 ⩽ x ⩽ −1 : encadrer x²", ["la fonction carré est décroissante sur ]−∞ ; 0]", "l’ordre change"], "1 ⩽ x² ⩽ 9")],
             [["x² ⩽ 9 ⇔ x ⩽ 3", "S = [−3 ; 3] : −4 n’est pas solution, −2 l’est."], ["(−5)² &lt; (−3)² car −5 &lt; −3", "Sur ]−∞ ; 0], le carré change l’ordre : 25 &gt; 9."],
              ["1/x décroissante sur ℝ", "Elle est décroissante sur chacun des intervalles ]−∞ ; 0[ et ]0 ; +∞[, mais 1/(−1) &lt; 1/1."]])
    faq = [("Pourquoi la fonction inverse n’est-elle pas décroissante sur ℝ ∖ {0} ?", "−1 &lt; 1 et 1/(−1) = −1 &lt; 1 = 1/1 : l’ordre est conservé ici, alors qu’une fonction décroissante l’inverserait."),
           ("Comment encadrer x² quand x change de signe ?", "Le minimum est 0 (atteint en x = 0) ; le maximum est le plus grand des carrés des bornes.")]
    unit("seconde", R, "fonctions-de-reference", "F",
         "Connaître les définitions, les représentations graphiques et les variations des fonctions carré, inverse, racine carrée, cube et valeur absolue ; les utiliser pour comparer, encadrer et résoudre des équations et inéquations",
         "Fonctions de référence", "Fonctions de référence",
         "Fiches de maths seconde sur les fonctions de référence : carré, inverse, racine carrée, cube, valeur absolue, comparer, encadrer et résoudre. 100 exercices corrigés.",
         "Croissante : conserve l’ordre ; décroissante : l’inverse", "x² ⩽ a² ⇔ −a ⩽ x ⩽ a (a > 0)", body, faq, sets, 9)


if __name__ == "__main__":
    main()
