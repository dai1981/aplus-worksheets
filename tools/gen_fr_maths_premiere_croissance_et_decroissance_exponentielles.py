# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Croissance et décroissance exponentielles (modèles t ↦ A e^(kt), valeurs, dérivée, lien avec les suites géométriques, problèmes)
  python3 tools/gen_fr_maths_premiere_croissance_et_decroissance_exponentielles.py
Erreurs : croire que e^(−kt) augmente, f(0) = 0 au lieu de A, taux d’évolution k au lieu de e^k − 1, multiplier l’exposant par A.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60613)


def ex(t):
    return "e<sup>%s</sup>" % t


def kt(k, v="t"):
    if k == 1:
        return v
    if k == -1:
        return MINUS + v
    return "%s%s" % (d(k), v)


def r2(x, k=2):
    return dk(Fr(x), k)


def model():
    A = R.choice([20, 50, 80, 100, 200, 500, 1000, 1500, 2000])
    k = R.choice([Fr(1, 10), Fr(2, 10), Fr(5, 100), Fr(3, 10), Fr(1, 2), Fr(-1, 10), Fr(-2, 10), Fr(-5, 100), Fr(-3, 10), Fr(-1, 2)])
    return A, k


def s1():
    A, k = model()
    q = R.choice(["sens", "sens", "f0", "pos"])
    f = "%s%s" % (num(A), ex(kt(k)))
    if q == "sens":
        ans = "croissante" if k > 0 else "décroissante"
        return M("f(t) = %s pour t ⩾ 0. Le modèle décrit-il une croissance ou une décroissance ?" % f, "une " + ("croissance" if k > 0 else "décroissance") + " exponentielle",
                 ["une " + ("décroissance" if k > 0 else "croissance") + " exponentielle", "une croissance linéaire", "une décroissance linéaire"],
                 "k = %s %s 0 : f est <b>%s</b>." % (d(k), "&gt;" if k > 0 else "&lt;", ans))
    if q == "f0":
        return M("f(t) = %s. Que vaut f(0) ?" % f, num(A), ["0", num(A * k) if Fr(A * k).denominator == 1 and A * k > 0 else "1", d(k) if k > 0 else num(A + 1)],
                 "e<sup>0</sup> = 1, donc f(0) = <b>%s</b> : c’est la valeur initiale." % num(A))
    return M("f(t) = %s. Quel est le signe de f(t) ?" % f, "toujours strictement positif", ["négatif quand t est grand" if k < 0 else "négatif pour t &lt; 0", "nul pour t = 0", "du signe de k"],
             "A = %s &gt; 0 et e<sup>X</sup> &gt; 0 : f(t) est <b>toujours strictement positif</b> (il peut tendre vers 0 sans l’atteindre)." % num(A))


def s2():
    A, k = model()
    t = R.choice([1, 2, 3, 5, 10])
    e_ = round(math.exp(float(k) * t), 4)
    v = A * e_
    ans = r2(v, 1 if v >= 100 else 2)
    return M("f(t) = %s%s. Calcule f(%d) (donné : %s ≈ %s). Arrondis %s." % (num(A), ex(kt(k)), t, ex(d(k * t)), r2(e_, 4), "au dixième" if v >= 100 else "au centième"), ans,
             [r2(A * float(k) * t, 1 if v >= 100 else 2) if A * k * t > 0 else r2(A - v, 1), r2(A * e_ * (1 if k > 0 else 1) + A, 1 if v >= 100 else 2), r2(A * math.exp(float(-k) * t), 1 if v >= 100 else 2)],
             "f(%d) = %s × %s ≈ <b>%s</b>." % (t, num(A), r2(e_, 4), ans))


def s3():
    A, k = model()
    q = R.choice(["der", "der", "sign", "tangent"])
    if q == "der":
        ans = "f′(t) = %s%s" % (d(A * k) if A * k not in (1, -1) else "", ex(kt(k)))
        return M("Quelle est la dérivée de f(t) = %s%s ?" % (num(A), ex(kt(k))), ans,
                 ["f′(t) = %s%s" % (num(A), ex(kt(k))), "f′(t) = %s%s" % (d(k) if k not in (1, -1) else "", ex(kt(k))), "f′(t) = %s%s" % (d(A * k), ex(kt(k) + " − 1"))],
                 "(e<sup>kt</sup>)′ = k e<sup>kt</sup> : f′(t) = %s × %s %s = <b>%s</b>." % (num(A), d(k), ex(kt(k)), ans[8:]))
    if q == "sign":
        ans = "positif : f est croissante" if k > 0 else "négatif : f est décroissante"
        return M("f(t) = %s%s. Quel est le signe de f′(t) ?" % (num(A), ex(kt(k))), ans, ["négatif : f est décroissante" if k > 0 else "positif : f est croissante", "nul", "du signe de t"],
                 "f′(t) = %s%s a le signe de A × k = %s : <b>%s</b>." % (d(A * k), ex(kt(k)), d(A * k), ans))
    return M("f(t) = %s%s. Quel est le coefficient directeur de la tangente à la courbe en t = 0 ?" % (num(A), ex(kt(k))), d(A * k), [num(A), d(k), d(A + k)],
             "f′(0) = A × k × e<sup>0</sup> = <b>%s</b>." % d(A * k))


def s4():
    k = R.choice([Fr(1, 10), Fr(2, 10), Fr(5, 100), Fr(-1, 10), Fr(-2, 10), Fr(-5, 100), Fr(3, 100), Fr(-3, 100)])
    q = R.choice(["raison", "raison", "taux", "taux"])
    e_ = math.exp(float(k))
    if q == "raison":
        A = R.choice([100, 500, 1000, 2000])
        return M("On pose u<sub>n</sub> = %s%s (n entier). Quelle est la raison de la suite géométrique (u<sub>n</sub>) ?" % (num(A), ex(kt(k, "n"))), ex(d(k)) + " ≈ " + r2(e_, 3),
                 [d(k), d(1 + k), num(A)], "u<sub>n+1</sub> = u<sub>n</sub> × %s : raison <b>%s ≈ %s</b>." % (ex(d(k)), ex(d(k)), r2(e_, 3)))
    t = (e_ - 1) * 100
    ans = ("+" if t > 0 else MINUS) + " " + r2(abs(t), 1) + NB + "%"
    return M("Une grandeur suit le modèle f(t) = A%s (t en années). Quel est son taux d’évolution annuel, arrondi à 0,1 %% ? (%s ≈ %s)" % (ex(kt(k)), ex(d(k)), r2(e_, 4)), ans,
             [("+" if k > 0 else MINUS) + " " + d(abs(k) * 100) + NB + "%", ("+" if t > 0 else MINUS) + " " + r2(e_ * 100, 1) + NB + "%", (MINUS if t > 0 else "+") + " " + r2(abs(t), 1) + NB + "%"],
             "Chaque année, on multiplie par %s ≈ %s : taux = %s − 1 ≈ <b>%s</b> (et non %s %%)." % (ex(d(k)), r2(e_, 4), r2(e_, 4), ans, d(k * 100)))


def s5():
    q = R.choice(["radio", "temp", "medic", "pop", "seuil"])
    if q == "radio":
        A = R.choice([100, 200, 400, 800])
        k = R.choice([Fr(1, 10), Fr(5, 100), Fr(2, 10)])
        t = R.choice([5, 10, 20])
        v = A * math.exp(-float(k) * t)
        return M("Une masse de %d g d’un élément radioactif suit m(t) = %d%s (t en années). Quelle masse reste-t-il au bout de %d ans (au gramme près) ?" % (A, A, ex(kt(-k)), t), "%d g" % round(v),
                 ["%d g" % round(A * (1 - float(k) * t)) if A * (1 - k * t) > 0 else "%d g" % round(v / 2), "%d g" % round(A * math.exp(float(k) * t)), "%d g" % round(A - float(k) * t)],
                 "m(%d) = %d × %s ≈ <b>%d g</b>." % (t, A, ex(d(-k * t)), round(v)))
    if q == "temp":
        Ta, D, k = 20, R.choice([60, 70, 80]), R.choice([Fr(1, 10), Fr(5, 100), Fr(2, 10)])
        t = R.choice([5, 10, 15])
        v = Ta + D * math.exp(-float(k) * t)
        return M("Un café refroidit dans une pièce à 20 °C : T(t) = 20 + %d%s (t en minutes). Quelle est sa température au bout de %d min (au degré près) ?" % (D, ex(kt(-k)), t), "%d °C" % round(v),
                 ["%d °C" % round(D * math.exp(-float(k) * t)), "%d °C" % round(20 + D), "%d °C" % round((20 + D) * math.exp(-float(k) * t))],
                 "T(%d) = 20 + %d × %s ≈ <b>%d °C</b>." % (t, D, ex(d(-k * t)), round(v)))
    if q == "medic":
        A = R.choice([10, 20, 50])
        k = R.choice([Fr(2, 10), Fr(3, 10), Fr(5, 10)])
        return M("La concentration d’un médicament dans le sang est C(t) = %d%s (en mg/L, t en heures). La concentration…" % (A, ex(kt(-k))), "diminue et se rapproche de 0",
                 ["augmente sans limite", "diminue puis devient négative", "reste égale à %d" % A], "k = %s &lt; 0 : C est décroissante et positive, elle <b>diminue et se rapproche de 0</b>." % d(-k))
    if q == "pop":
        A = R.choice([1000, 2000, 5000])
        k = R.choice([Fr(2, 100), Fr(3, 100), Fr(5, 100)])
        n = R.choice([10, 20])
        v = A * math.exp(float(k) * n)
        return M("Une population de %s bactéries évolue selon P(t) = %s%s (t en minutes). Combien y a-t-il de bactéries au bout de %d min (à l’unité près) ?" % (num(A), num(A), ex(kt(k)), n), num(round(v)),
                 [num(round(A * (1 + float(k) * n))), num(round(A * float(k) * n)), num(round(A * (1 + float(k)) ** n))],
                 "P(%d) = %s × %s ≈ <b>%s</b> (un peu plus que %s avec (1 + %s)<sup>%d</sup>)." % (n, num(A), ex(d(k * n)), num(round(v)), num(round(A * (1 + float(k)) ** n)), d(k), n))
    A = R.choice([100, 200])
    k = R.choice([Fr(1, 10), Fr(2, 10)])
    s_ = R.choice([Fr(1, 2), Fr(1, 4), Fr(1, 10)])
    t = 0
    while math.exp(-float(k) * t) >= float(s_):
        t += 1
    tab = table(["t"] + [str(x) for x in range(t - 2, t + 2)], [["f(t)"] + [r2(A * math.exp(-float(k) * x), 1) for x in range(t - 2, t + 2)]])
    return M("f(t) = %d%s. %s À partir de quel entier t a-t-on f(t) &lt; %s ?" % (A, ex(kt(-k)), tab, d(A * s_)), "t = %d" % t, ["t = %d" % (t - 1), "t = %d" % (t + 1), "t = %d" % (t - 2)],
             "On lit dans le tableau : f(%d) ≈ %s ⩾ %s et f(%d) ≈ %s &lt; %s : <b>t = %d</b>." % (t - 1, r2(A * math.exp(-float(k) * (t - 1)), 1), d(A * s_), t, r2(A * math.exp(-float(k) * t), 1), d(A * s_), t))


def main():
    seen = set()
    sets = [("Lire un modèle exponentiel", mix(R, seen, [(s1, 20)])), ("Calculer des valeurs", mix(R, seen, [(s2, 20)])),
            ("Dérivée et sens de variation", mix(R, seen, [(s3, 20)])), ("Lien avec les suites géométriques", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un modèle f(t) = A e<sup>kt</sup> (A &gt; 0) décrit une <b>croissance exponentielle</b> si k &gt; 0 et une <b>décroissance exponentielle</b> si k &lt; 0. f(0) = A.",
              "f′(t) = A k e<sup>kt</sup> : du signe de k. Quand t augmente de 1, f(t) est multiplié par e<sup>k</sup>.",
              "Aux instants entiers, u<sub>n</sub> = A e<sup>kn</sup> est une suite géométrique de raison e<sup>k</sup> ; le taux d’évolution par unité de temps est e<sup>k</sup> − 1."],
             [("f(t) = 500e<sup>−0,2t</sup>", ["f(0) = 500", "f(5) = 500e<sup>−1</sup> ≈ 183,9", "taux : e<sup>−0,2</sup> − 1 ≈ −18,1 %"], "décroissance exponentielle")],
             [["e<sup>−0,2t</sup> augmente avec t", "k = −0,2 &lt; 0 : décroissance."], ["Le taux d’évolution est k = 0,05, soit 5 %", "C’est e<sup>0,05</sup> − 1 ≈ 5,1 %."], ["f(0) = 0", "e<sup>0</sup> = 1 : f(0) = A."]])
    faq = [("Pourquoi parle-t-on de croissance exponentielle ?", "Parce que la grandeur est multipliée par le même nombre e<sup>k</sup> à chaque unité de temps, comme une suite géométrique, au lieu d’augmenter du même nombre."),
           ("La décroissance atteint-elle 0 ?", "Non : A e<sup>kt</sup> reste strictement positif. Il se rapproche de 0 quand t devient grand.")]
    unit("premiere", R, "croissance-et-decroissance-exponentielles", "F",
         "Représenter et utiliser les fonctions t ↦ e<sup>kt</sup> et t ↦ e<sup>−kt</sup> ; modéliser une croissance ou une décroissance exponentielle ; dériver t ↦ A e<sup>kt</sup> ; lien avec les suites géométriques et les taux d’évolution",
         "Croissance et décroissance exponentielles", "Croissance exponentielle",
         "Fiches de maths première sur la croissance et la décroissance exponentielles : modèles A e^(kt), valeurs, dérivée, taux d’évolution, suites géométriques et problèmes. 100 exercices corrigés.",
         "f(t) = A e^(kt) : croissance si k > 0", "Décroissance si k < 0 ; facteur e^k par unité de temps", body, faq, sets, 13)


if __name__ == "__main__":
    main()
