# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Variance et écart type d’une variable aléatoire (définition, formule de König-Huygens, écart type, V(aX + b), comparer des risques)
  python3 tools/gen_fr_maths_premiere_variance_et_ecart_type.py
Erreurs : V(X) = E(X²) − E(X) (oublier le carré), V(aX + b) = aV(X) + b, écart type = V(X) sans racine, variance négative.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60623)


def law(n=None):
    n = n or R.choice([2, 3, 3, 4])
    xs = sorted(R.sample(range(-4, 9), n))
    cuts = sorted(R.sample(range(1, 10), n - 1))
    ps = [Fr(b - a, 10) for a, b in zip([0] + cuts, cuts + [10])]
    return xs, ps


def E_(xs, ps, f=lambda x: x):
    return sum(f(x) * p for x, p in zip(xs, ps))


def s1():
    xs, ps = law()
    e = E_(xs, ps)
    v = E_(xs, ps, lambda x: (x - e) ** 2)
    return M("Voici la loi de X :%s E(X) = %s. Calcule la variance V(X) avec V(X) = Σ p<sub>i</sub>(x<sub>i</sub> − E(X))²." % (loi(xs, ps), d(e)), d(v),
             [d(E_(xs, ps, lambda x: x * x)), d(E_(xs, ps, lambda x: abs(x - e))), d(v * v) if v * v != v else d(v + 1), d(E_(xs, ps, lambda x: x * x) - e)],
             "V(X) = %s = <b>%s</b>." % (" + ".join("%s × %s²" % (d(p), par(x - e)) for x, p in zip(xs, ps)), d(v)))


def s2():
    xs, ps = law()
    e = E_(xs, ps)
    e2 = E_(xs, ps, lambda x: x * x)
    v = e2 - e * e
    k = R.choice(["kh", "kh", "e2"])
    if k == "kh":
        return M("E(X) = %s et E(X²) = %s. Calcule V(X) (formule de König-Huygens)." % (d(e), d(e2)), d(v), [d(e2 - e), d(e2 + e * e), d((e2 - e) ** 2), d(e * e - e2) if e * e != e2 else d(e2)],
                 "V(X) = E(X²) − E(X)² = %s − %s² = %s − %s = <b>%s</b>." % (d(e2), par(e), d(e2), d(e * e), d(v)))
    return M("Voici la loi de X :%s Calcule E(X²)." % loi(xs, ps), d(e2), [d(e * e), d(E_(xs, ps, lambda x: 2 * x)), d(sum(x * x for x in xs))],
             "E(X²) = Σ x<sub>i</sub>² × p<sub>i</sub> = %s = <b>%s</b> (différent de E(X)² = %s)." % (" + ".join("%s × %s" % (d(x * x), d(p)) for x, p in zip(xs, ps)), d(e2), d(e * e)))


def s3():
    k = R.choice(["sigma", "sigma", "sigma_approx", "from_sigma"])
    if k == "sigma":
        s_ = R.choice([Fr(1, 2), 1, Fr(3, 2), 2, 3, Fr(5, 2), 4, Fr(3, 10), Fr(7, 10), 5, Fr(12, 10)])
        v = s_ * s_
        return M("V(X) = %s. Calcule l’écart type σ(X)." % d(v), d(s_), [d(v / 2), d(v * v), d(v)], "σ(X) = √V(X) = √%s = <b>%s</b>." % (d(v), d(s_)))
    if k == "sigma_approx":
        v = R.choice([2, 3, 5, 6, 7, 8, 10, 12, Fr(15, 10), Fr(25, 10)])
        s_ = math.sqrt(float(v))
        return M("V(X) = %s. Donne σ(X) arrondi au centième." % d(v), dk(Fr(s_), 2), [dk(Fr(float(v) / 2), 2), dk(Fr(float(v) ** 2), 2), d(v)], "σ(X) = √%s ≈ <b>%s</b>." % (d(v), dk(Fr(s_), 2)))
    s_ = R.choice([2, 3, 4, Fr(1, 2), Fr(3, 2), 5])
    return M("σ(X) = %s. Que vaut V(X) ?" % d(s_), d(s_ * s_), [d(s_ / 2) if s_ / 2 != s_ * s_ else d(s_ * 2), d(s_), d(2 * s_) if 2 * s_ != s_ * s_ else d(s_ + 1)], "V(X) = σ(X)² = <b>%s</b>." % d(s_ * s_))


def s4():
    a, b = nz(R, -5, 5), R.randint(-9, 9)
    v = R.choice([Fr(1, 2), 1, 2, 3, 4, Fr(5, 2), 9])
    e = R.randint(-5, 8)
    k = R.choice(["V", "V", "sig", "E"])
    Y = E((a, "X"), (b, ""))
    if k == "V":
        return M("V(X) = %s. Calcule V(%s)." % (d(v), Y), d(a * a * v), [d(a * v + b), d(a * v), d(a * a * v + b) if b else d(-a * a * v)],
                 "V(aX + b) = a² V(X) = %s × %s = <b>%s</b> (b ne change pas la dispersion)." % (d(a * a), d(v), d(a * a * v)))
    if k == "sig":
        s_ = R.choice([1, 2, 3, Fr(1, 2), 4])
        return M("σ(X) = %s. Calcule σ(%s)." % (d(s_), Y), d(abs(a) * s_), [d(a * a * s_), d(a * s_ + b) if a * s_ + b != abs(a) * s_ else d(a * a * s_ + 1), d(a * s_) if a < 0 else d(s_)],
                 "σ(aX + b) = |a| × σ(X) = %d × %s = <b>%s</b>." % (abs(a), d(s_), d(abs(a) * s_)))
    return M("E(X) = %s et V(X) = %s. Calcule E(%s)." % (d(e), d(v), Y), d(a * e + b), [d(a * v + b), d(a * e), d(a * a * e + b)], "E(aX + b) = aE(X) + b = <b>%s</b>." % d(a * e + b))


def s5():
    k = R.choice(["compare", "compare", "salaire", "jeu"])
    if k == "compare":
        e = R.randint(2, 6)
        sA, sB = R.sample([Fr(1, 2), 1, 2, 3, 4], 2)
        return M("Deux placements ont le même gain moyen (%d %%) ; l’écart type vaut %s pour A et %s pour B. Lequel est le moins risqué ?" % (e, d(sA), d(sB)), "A" if sA < sB else "B",
                 ["B" if sA < sB else "A", "les deux sont aussi risqués", "on ne peut pas comparer"], "Le risque se mesure par la dispersion : le plus petit écart type est celui de <b>%s</b>." % ("A" if sA < sB else "B"))
    if k == "salaire":
        e, s_ = R.randint(15, 30) * 100, R.randint(1, 5) * 50
        a = R.choice([Fr(11, 10), Fr(105, 100), Fr(12, 10)])
        b = R.choice([50, 100, 0])
        return M("Les primes X d’une entreprise ont pour espérance %s € et pour écart type %d €. Elles deviennent Y = %sX%s. Que vaut l’écart type de Y ?" % (num(e), s_, d(a), " + %d" % b if b else ""), euro(a * s_),
                 [euro(a * s_ + b) if b else euro(a * a * s_), euro(s_), euro(a * a * s_) if b else euro(s_ + 10)], "σ(Y) = %s × %d = <b>%s</b> (le bonus %s ne change pas l’écart type)." % (d(a), s_, euro(a * s_), "%d €" % b if b else "nul"))
    xs = [R.randint(-5, -1), R.randint(1, 10)]
    p = Fr(R.randint(1, 9), 10)
    ps = [1 - p, p]
    e = E_(xs, ps)
    v = E_(xs, ps, lambda x: x * x) - e * e
    return M("Un jeu fait perdre %d € avec la probabilité %s et gagner %d € avec la probabilité %s. Calcule V(X)." % (-xs[0], d(1 - p), xs[1], d(p)), d(v),
             [d(E_(xs, ps, lambda x: x * x)), d(v + e * e - e) if v + e * e - e != v else d(v * 2), d(E_(xs, ps, lambda x: x * x) - e)],
             "E(X) = %s ; E(X²) = %s ; V(X) = %s − %s² = <b>%s</b>." % (d(e), d(E_(xs, ps, lambda x: x * x)), d(E_(xs, ps, lambda x: x * x)), par(e), d(v)))


def main():
    seen = set()
    sets = [("Variance par la définition", mix(R, seen, [(s1, 20)])), ("Formule de König-Huygens", mix(R, seen, [(s2, 20)])),
            ("Écart type", mix(R, seen, [(s3, 20)])), ("Transformation affine aX + b", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La <b>variance</b> mesure la dispersion de X autour de son espérance : V(X) = Σ p<sub>i</sub>(x<sub>i</sub> − E(X))². Elle est toujours positive ou nulle.",
              "Formule de König-Huygens : <b>V(X) = E(X²) − E(X)²</b>. L’<b>écart type</b> est σ(X) = √V(X), dans la même unité que X.",
              "Pour a, b réels : E(aX + b) = aE(X) + b ; V(aX + b) = a²V(X) ; σ(aX + b) = |a| σ(X)."],
             [("X prend 0 et 10 avec les probabilités 0,5 et 0,5", ["E(X) = 5 ; E(X²) = 50", "V(X) = 50 − 25 = 25"], "σ(X) = 5")],
             [["V(X) = E(X²) − E(X)", "C’est E(X)², au carré."], ["V(2X + 3) = 2V(X) + 3", "V(2X + 3) = 4V(X)."], ["σ(X) = V(X)", "σ(X) = √V(X)."]])
    faq = [("À quoi sert l’écart type ?", "À mesurer la dispersion ou le risque : deux jeux de même espérance peuvent avoir des écarts types très différents."),
           ("Pourquoi b disparaît-il dans V(aX + b) ?", "Ajouter b décale toutes les valeurs et l’espérance du même nombre : les écarts x − E(X) ne changent pas.")]
    unit("premiere", R, "variance-et-ecart-type", "S",
         "Variance et écart type d’une variable aléatoire ; formule de König-Huygens V(X) = E(X²) − E(X)² ; effet d’une transformation affine aX + b ; interpréter l’écart type comme mesure de dispersion ou de risque",
         "Variance et écart type d’une variable aléatoire", "Variance et écart type",
         "Fiches de maths première sur la variance et l’écart type : définition, formule de König-Huygens, écart type, V(aX + b) et comparaison des risques. 100 exercices corrigés.",
         "V(X) = E(X²) − E(X)² ; σ = √V", "V(aX + b) = a² V(X)", body, faq, sets, 23)


if __name__ == "__main__":
    main()
