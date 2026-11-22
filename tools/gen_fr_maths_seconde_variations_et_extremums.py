# -*- coding: utf-8 -*-
"""
France Maths Seconde : Variations et extremums (tableaux de variations, maximum, minimum, comparer des images, optimisation)
  python3 tools/gen_fr_maths_seconde_variations_et_extremums.py
Erreurs : confondre maximum (valeur) et l’endroit où il est atteint, comparer f(a) et f(b) sur un intervalle où f n’est pas monotone, lire le tableau à l’envers.
"""
import random
from fr_c4 import *
import de_k10

R = random.Random(60510)
K = Kids(R)


def vtab(xs, ys):
    """tableau de variations : xs, ys de même longueur ; flèches entre les valeurs"""
    n = len(xs)
    W, H = 120 + 100 * (n - 1) + 40, 130
    X = lambda i: 110 + 100 * i
    s = ["<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, INK), line(2, 38, W - 2, 38, INK, 1.2), line(70, 2, 70, H - 2, INK, 1.2),
         text(36, 26, "x", 15, weight=700), text(36, 90, "f(x)", 14, weight=700)]
    for i, (x, y) in enumerate(zip(xs, ys)):
        s.append(text(X(i), 26, x, 14))
    for i in range(n):
        hi = (i > 0 and ys[i] > ys[i - 1]) or (i < n - 1 and ys[i] > ys[i + 1])
        yy = 58 if hi else 118
        s.append(text(X(i), yy, d(ys[i]), 14, weight=600))
    for i in range(n - 1):
        up = ys[i + 1] > ys[i]
        x1, x2 = X(i) + 20, X(i + 1) - 20
        y1, y2 = (110, 56) if up else (56, 110)
        s.append(line(x1, y1, x2, y2, BLUE, 1.8))
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (x2, y2, BLUE))
    return wrap(W, H, "".join(s), "tableau de variations", lg=True)


def mk():
    n = R.choice([3, 3, 4])
    xs = sorted(R.sample(range(-6, 9), n))
    ys = []
    up = R.choice([True, False])
    y = R.randint(-5, 5)
    for i in range(n):
        ys.append(y)
        y = y + (R.randint(2, 7) if up else -R.randint(2, 7))
        up = not up
    return xs, ys


def s1():
    xs, ys = mk()
    svg = vtab([d(x) for x in xs], ys)
    k = R.choice(["max", "min", "where", "var"])
    if k == "max":
        m = max(ys)
        return M("<div class='qfig'>%s</div>Quel est le maximum de f sur [%s ; %s] ?" % (svg, d(xs[0]), d(xs[-1])), d(m), [d(xs[ys.index(m)]) if xs[ys.index(m)] != m else d(m + 1), d(min(ys)), d(xs[-1]) if xs[-1] != m else d(m - 1)],
                 "La plus grande valeur de la ligne f(x) est <b>%s</b>, atteinte en x = %s." % (d(m), d(xs[ys.index(m)])))
    if k == "min":
        m = min(ys)
        return M("<div class='qfig'>%s</div>Quel est le minimum de f sur [%s ; %s] ?" % (svg, d(xs[0]), d(xs[-1])), d(m), [d(xs[ys.index(m)]) if xs[ys.index(m)] != m else d(m - 1), d(max(ys)), d(xs[0]) if xs[0] != m else d(m + 1)],
                 "La plus petite valeur est <b>%s</b>, atteinte en x = %s." % (d(m), d(xs[ys.index(m)])))
    if k == "where":
        m = max(ys)
        x = xs[ys.index(m)]
        return M("<div class='qfig'>%s</div>En quelle valeur de x le maximum de f est-il atteint ?" % svg, "x = %s" % d(x), ["x = %s" % d(m) if m != x else "x = %s" % d(x + 1), "x = %s" % d(xs[ys.index(min(ys))]), "x = %s" % d(xs[-1]) if xs[-1] != x else "x = %s" % d(xs[0])],
                 "Le maximum %s est atteint pour <b>x = %s</b>." % (d(m), d(x)))
    i = R.randrange(len(xs) - 1)
    up = ys[i + 1] > ys[i]
    ans = "croissante" if up else "décroissante"
    return M("<div class='qfig'>%s</div>Quel est le sens de variation de f sur [%s ; %s] ?" % (svg, d(xs[i]), d(xs[i + 1])), ans, ["décroissante" if up else "croissante", "constante", "on ne peut pas savoir"],
             "La flèche %s : f est <b>%s</b>." % ("monte" if up else "descend", ans))


def s2():
    xs, ys = mk()
    svg = vtab([d(x) for x in xs], ys)
    i = R.randrange(len(xs) - 1)
    a, b = sorted(R.sample(range(xs[i] * 10 + 1, xs[i + 1] * 10), 2))
    a, b = Fr(a, 10), Fr(b, 10)
    up = ys[i + 1] > ys[i]
    ans = "f(%s) &lt; f(%s)" % (d(a), d(b)) if up else "f(%s) &gt; f(%s)" % (d(a), d(b))
    return M("<div class='qfig'>%s</div>Compare f(%s) et f(%s)." % (svg, d(a), d(b)), ans, ["f(%s) &gt; f(%s)" % (d(a), d(b)) if up else "f(%s) &lt; f(%s)" % (d(a), d(b)), "f(%s) = f(%s)" % (d(a), d(b)), "on ne peut pas comparer"],
             "%s et %s sont dans [%s ; %s] où f est %s : <b>%s</b>." % (d(a), d(b), d(xs[i]), d(xs[i + 1]), "croissante (l’ordre est conservé)" if up else "décroissante (l’ordre change)", ans))


def s3():
    a = R.choice([1, -1, 2, -2])
    h, k_ = R.randint(-3, 3), R.randint(-4, 4)
    f = lambda x: a * (x - h) ** 2 + k_
    form = expr([(a, "x²"), (-2 * a * h, "x"), (a * h * h + k_, "")])
    q = R.choice(["ext", "type", "val"])
    if q == "ext":
        return M("f(x) = %s = %s(x %s %d)² %s %d. Quel est l’extremum de f sur ℝ ?" % (form, d(a) if a not in (1, -1) else ("" if a == 1 else MINUS), "−" if h >= 0 else "+", abs(h), "+" if k_ >= 0 else "−", abs(k_)),
                 "un %s égal à %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(k_), d(h)),
                 ["un %s égal à %s, atteint en x = %s" % ("maximum" if a > 0 else "minimum", d(k_), d(h)), "un %s égal à %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(h), d(k_)) if h != k_ else "un %s égal à %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(k_ + 1), d(h)),
                  "un %s égal à %s, atteint en x = %s" % ("minimum" if a > 0 else "maximum", d(k_), d(-h)) if h else "un %s égal à %s, atteint en x = 1" % ("minimum" if a > 0 else "maximum", d(k_))],
                 "%s(x − %s)² est %s 0 et vaut 0 en x = %s : <b>%s %s en x = %s</b>." % (d(a) if a not in (1, -1) else ("" if a == 1 else MINUS), d(h), "⩾" if a > 0 else "⩽", d(h), "minimum" if a > 0 else "maximum", d(k_), d(h)))
    if q == "type":
        return M("Pour démontrer que %s ⩾ %s pour tout x, on remarque que %s − (%s) = %s(x %s %d)². Pourquoi est-ce suffisant ?" % (form, d(k_), form, d(k_), d(a) if a > 1 else "", "−" if h >= 0 else "+", abs(h)) if a > 0 else
                 "Pour démontrer que %s ⩽ %s pour tout x, on remarque que %s − (%s) = −%s(x %s %d)². Pourquoi est-ce suffisant ?" % (form, d(k_), form, d(k_), d(-a) if a < -1 else "", "−" if h >= 0 else "+", abs(h)),
                 "un carré est toujours positif ou nul", ["un carré est toujours strictement positif", "il suffit de tester x = 0", "il suffit de tester x = %s" % d(h)],
                 "Le signe de la différence est connu pour tout x car <b>un carré est toujours positif ou nul</b>.")
    x1, x2 = sorted(R.sample(range(-5, 6), 2))
    ys = [f(x) for x in range(x1, x2 + 1)]
    m = (max if a < 0 else min)(ys)
    return M("f(x) = %s. Quel est le %s de f sur [%s ; %s] ?" % (form, "maximum" if a < 0 else "minimum", d(x1), d(x2)), d(m), [d(k_) if k_ != m else d(m + 1), d((min if a < 0 else max)(ys)), d(f(x1)) if f(x1) != m else d(m - 1)],
             "Le sommet est en x = %s ; sur [%s ; %s], le %s vaut <b>%s</b>." % (d(h), d(x1), d(x2), "maximum" if a < 0 else "minimum", d(m)))


def s4():
    c = R.randint(-2, 2)
    G = R.choice([(lambda x: (x - 1) ** 2 - 3 + c, (-2, 4, 1), (-4 + c, 7 + c, 1), "parabole"), (lambda x: -(x + 1) ** 2 + 4 + c, (-4, 2, 1), (-6 + c, 5 + c, 1), "parabole2")])
    F, xr, yr, nm = G
    svg = relabel(de_k10.kurve([(F, BLUE, "")], xr, yr, W=340, H=320), "courbe de f")
    xs = list(range(xr[0], xr[1] + 1))
    ys = [F(x) for x in xs]
    k = R.choice(["max", "where", "var"])
    if k == "max":
        mx, mn = max(ys), min(ys)
        q = R.choice(["maximum", "minimum"])
        v = mx if q == "maximum" else mn
        return M("<div class='qfig'>%s</div>Lis le %s de f sur [%s ; %s]." % (svg, q, d(xr[0]), d(xr[1])), d(v), [d(xs[ys.index(v)]) if xs[ys.index(v)] != v else d(v + 1), d(mn if q == "maximum" else mx), d(v + 2)],
                 "Le point le plus %s de la courbe a pour ordonnée <b>%s</b>." % ("haut" if q == "maximum" else "bas", d(v)))
    if k == "where":
        v = max(ys) if nm == "parabole2" else min(ys)
        x = xs[ys.index(v)]
        return M("<div class='qfig'>%s</div>En quelle valeur de x f atteint-elle son %s ?" % (svg, "maximum" if nm == "parabole2" else "minimum"), "x = %s" % d(x), ["x = %s" % d(v) if v != x else "x = %s" % d(x + 2), "x = %s" % d(xr[0]), "x = %s" % d(xr[1])],
                 "On lit l’abscisse du sommet : <b>x = %s</b>." % d(x))
    x = 1 if nm == "parabole" else -1
    D = lambda v: d(v)
    ans = "décroissante sur [%s ; %s], croissante sur [%s ; %s]" % (D(xr[0]), D(x), D(x), D(xr[1])) if nm == "parabole" else "croissante sur [%s ; %s], décroissante sur [%s ; %s]" % (D(xr[0]), D(x), D(x), D(xr[1]))
    other = "croissante sur [%s ; %s], décroissante sur [%s ; %s]" % (D(xr[0]), D(x), D(x), D(xr[1])) if nm == "parabole" else "décroissante sur [%s ; %s], croissante sur [%s ; %s]" % (D(xr[0]), D(x), D(x), D(xr[1]))
    return M("<div class='qfig'>%s</div>Décris les variations de f." % svg, ans, [other, "croissante sur [%s ; %s]" % (D(xr[0]), D(xr[1])), "décroissante sur [%s ; %s]" % (D(xr[0]), D(xr[1]))], "On suit la courbe de gauche à droite : <b>%s</b>." % ans)


def s5():
    k = R.choice(["enclos", "enclos", "boite", "prix", "somme", "somme"])
    if k == "somme":
        S_ = R.choice([10, 12, 14, 16, 18, 20, 24, 30, 40, 50, 60])
        h = S_ // 2
        return M("Deux nombres positifs ont pour somme %d. Quel est le plus grand produit possible ?" % S_, str(h * h), [str(S_), str(h * (h - 1)) if h > 1 else "0", str(S_ * S_)],
                 "P(x) = x(%d − x) = −(x − %d)² + %d : maximum <b>%d</b> pour x = %d." % (S_, h, h * h, h * h, h))
    if k == "enclos":
        L_ = R.choice([20, 24, 32, 40, 60])
        c = L_ // 4
        return M("Avec %d m de grillage, on veut un enclos rectangulaire d’aire maximale. L’aire vaut A(x) = x(%d − x) où x est la largeur. Quelle largeur choisir ?" % (L_, L_ // 2), "%d m" % c, ["%d m" % (L_ // 2), "%d m" % (L_ // 3) if L_ % 3 == 0 else "%d m" % (c + 2), "%d m" % (c * c)],
                 "A(x) = −(x − %d)² + %d : maximum en <b>x = %d m</b> (un carré de %d m², d’aire %d m²)." % (c, c * c, c, c * c, c * c))
    if k == "boite":
        return M("Une fonction est croissante sur [0 ; 4] puis décroissante sur [4 ; 10]. Que représente f(4) ?", "le maximum de f sur [0 ; 10]", ["le minimum de f sur [0 ; 10]", "une valeur où f s’annule", "on ne peut pas savoir"],
                 "Elle monte puis descend : <b>f(4) est le maximum</b>.")
    a = R.choice([2, 4, 5])
    p0 = R.choice([10, 20, 30])
    return M("Le bénéfice (en €) est B(x) = −%d(x − %d)² + %s, où x est le prix de vente. Pour quel prix le bénéfice est-il maximal ?" % (a, p0, num(p0 * 50)), "%d €" % p0, ["%s €" % num(p0 * 50), "%d €" % a, "0 €"],
             "−%d(x − %d)² ⩽ 0 et vaut 0 pour x = %d : <b>%d €</b> (bénéfice %s €)." % (a, p0, p0, p0, num(p0 * 50)))


def main():
    seen = set()
    sets = [("Lire un tableau de variations", mix(R, seen, [(s1, 20)])), ("Comparer des images", mix(R, seen, [(s2, 20)])),
            ("Extremums par le calcul", mix(R, seen, [(s3, 20)])), ("Lire une courbe", mix(R, seen, [(s4, 20)])), ("Optimisation", mix(R, seen, [(s5, 20)]))]
    body = L(["f est <b>croissante</b> sur I si, pour a &lt; b dans I, f(a) ⩽ f(b) (elle conserve l’ordre) ; <b>décroissante</b> si f(a) ⩾ f(b) (elle inverse l’ordre).",
              "Le <b>maximum</b> de f sur I est la plus grande valeur f(x) ; on précise où il est atteint. Le tableau de variations résume tout cela avec des flèches.",
              "Pour démontrer un extremum, on peut écrire f(x) − m sous la forme d’un carré : (x − h)² ⩾ 0."],
             [("f(x) = (x − 2)² + 3", ["(x − 2)² ⩾ 0", "donc f(x) ⩾ 3, avec égalité en x = 2"], "minimum 3 atteint en 2")],
             [["Donner « x = 2 » comme maximum", "Le maximum est une valeur de f(x) ; 2 est l’endroit où il est atteint."], ["Comparer f(a) et f(b) sur un intervalle où f change de sens", "Il faut a et b dans un même intervalle de monotonie."],
              ["Lire le tableau à l’envers", "La ligne du haut donne x, la ligne du bas les valeurs de f(x)."]])
    faq = [("Quelle différence entre maximum et maximum local ?", "En seconde, on cherche le maximum sur un intervalle donné : la plus grande valeur de f sur cet intervalle."),
           ("Comment trouver un maximum à la calculatrice ?", "On trace la courbe ou on fait un tableau de valeurs avec un pas de plus en plus petit autour du sommet.")]
    unit("seconde", R, "variations-et-extremums", "F",
         "Relier la courbe et le tableau de variations d’une fonction ; déterminer graphiquement ou par le calcul un maximum ou un minimum ; comparer des images à l’aide des variations ; résoudre des problèmes d’optimisation",
         "Variations et extremums d’une fonction", "Variations et extremums",
         "Fiches de maths seconde sur les variations : tableaux de variations, maximum, minimum, comparer des images, lecture de courbes et optimisation. 100 exercices corrigés.",
         "Croissante : l’ordre est conservé", "Le maximum est une valeur de f(x), atteinte en un x", body, faq, sets, 10)


if __name__ == "__main__":
    main()
