# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Taux de variation, nombre dérivé et tangente (sécantes, limite du taux, lecture graphique, équation de tangente, approximation affine)
  python3 tools/gen_fr_maths_premiere_nombre_derive_et_tangente.py
Erreurs : diviser par f(b) − f(a) au lieu de b − a, f′(a) confondu avec f(a), tangente y = f′(a)(x + a) + f(a), lire l’ordonnée du point au lieu de la pente de la tangente.
"""
import random
from fr_ly1 import *

R = random.Random(60609)


def poly(cs):
    """cs = [(coef, exposant)] → texte"""
    return expr([(c, {3: "x³", 2: "x²", 1: "x", 0: ""}[e]) for c, e in cs])


def ev(cs, x):
    return sum(Fr(c) * Fr(x) ** e for c, e in cs)


def der(cs):
    return [(c * e, e - 1) for c, e in cs if e > 0]


def rnd_poly(deg=2):
    cs = [(nz(R, -3, 3), 2), (R.randint(-6, 6), 1), (R.randint(-9, 9), 0)]
    if deg == 3:
        cs = [(nz(R, -2, 2), 3)] + cs[1:]
    return cs


def s1():
    cs = rnd_poly()
    a, b = sorted(R.sample(range(-4, 6), 2))
    fa, fb = ev(cs, a), ev(cs, b)
    t = Fr(fb - fa, b - a)
    k = R.choice(["taux", "taux", "secante"])
    q = ("Calcule le taux de variation de f(x) = %s entre %s et %s." if k == "taux" else "Quel est le coefficient directeur de la sécante à la courbe de f(x) = %s aux points d’abscisses %s et %s ?") % (poly(cs), d(a), d(b))
    return M(q, fq(t), [fq(Fr(b - a, fb - fa)) if fb != fa else fq(t + 1), fq(fb - fa), fq(Fr(fb + fa, b - a)), fq(Fr(fb - fa, b + a)) if a + b else fq(-t)],
             "(f(%s) − f(%s)) ÷ (%s − %s) = (%s − %s) ÷ %s = <b>%s</b>." % (d(b), d(a), d(b), par(a), d(fb), par(fa), d(b - a), fq(t)))


def s2():
    k = R.choice(["simp", "simp", "lim", "lim_x2"])
    a = R.randint(-5, 5)
    c1, c0 = R.randint(-6, 6), R.randint(-9, 9)
    m = nz(R, -3, 3)
    f = poly([(m, 2), (c1, 1), (c0, 0)])
    if k == "simp":
        ans = E((2 * m * a + c1, ""), (m, "h"))
        return M("f(x) = %s. Pour h ≠ 0, simplifie (f(%s + h) − f(%s)) ÷ h." % (f, d(a), d(a)) if a >= 0 else "f(x) = %s. Pour h ≠ 0, simplifie (f(%s + h) − f(%s)) ÷ h." % (f, d(a), d(a)), ans,
                 [E((2 * m * a + c1, ""), (m, "h²")), E((m * a + c1, ""), (m, "h")), E((2 * m * a, ""), (m, "h")), E((2 * m * a + c1 + c0, ""), (m, "h"))],
                 "f(%s + h) − f(%s) = %s ; on divise par h : <b>%s</b>." % (d(a), d(a), expr([(m, "h²"), (2 * m * a + c1, "h")]), ans))
    if k == "lim":
        v = 2 * m * a + c1
        return M("f(x) = %s. On a (f(%s + h) − f(%s)) ÷ h = %s pour h ≠ 0. Que vaut f′(%s) ?" % (f, d(a), d(a), E((v, ""), (m, "h")), d(a)), d(v),
                 [d(v + m), d(m * a * a + c1 * a + c0), d(m), d(-v) if v else "1"], "Quand h tend vers 0, %s tend vers <b>%s</b> : c’est f′(%s)." % (E((v, ""), (m, "h")), d(v), d(a)))
    return M("Pour f(x) = x², quelle est la limite de (f(%s + h) − f(%s)) ÷ h quand h tend vers 0 ?" % (d(a), d(a)), d(2 * a), [d(a * a), d(a), "0", d(2 * a + 1)],
             "(%s + h)² − %s² = %sh + h², divisé par h : %s + h → <b>%s</b>." % (par(a), par(a), d(2 * a) if a else "0", E((2 * a, ""), (1, "h")), d(2 * a)))


def s3():
    m = R.choice([Fr(1, 2), 1, Fr(-1, 2), -1, 2, -2, 0])
    a = R.randint(-2, 2)
    fa = R.randint(-2, 2)
    A2 = R.choice([Fr(1, 2), Fr(-1, 2), 1, -1])
    f = lambda x, m=m, a=a, fa=fa, A2=A2: float(A2) * (x - a) ** 2 + float(m) * (x - a) + fa
    t = lambda x, m=m, a=a, fa=fa: float(m) * (x - a) + fa
    svg = kurve([(f, BLUE, "C"), (t, RED, "T")], (-5, 5, 1), (-5, 5, 1), pts=[(a, fa, "A")], label="courbe et tangente en A")
    k = R.choice(["fp", "fp", "fa"])
    if k == "fp":
        return M("<div class='qfig'>%s</div>La droite T est tangente à la courbe de f au point A. Que vaut f′(%s) ?" % (svg, d(a)), fq(m),
                 [d(fa) if Fr(fa) != m else fq(m + 1), fq(-m) if m else "1", fq(1 / Fr(m)) if m and 1 / Fr(m) != m else "2", d(a) if Fr(a) not in (m, -m) else "3"],
                 "f′(%s) est le coefficient directeur de la tangente T : <b>%s</b>%s." % (d(a), fq(m), " (tangente horizontale)" if m == 0 else ""))
    return M("<div class='qfig'>%s</div>Que vaut f(%s) ?" % (svg, d(a)), d(fa), [fq(m) if Fr(m) != fa else d(fa + 1), d(a) if a != fa else d(fa - 1), d(-fa) if fa else "1"],
             "f(%s) est l’ordonnée du point A : <b>%s</b> (f′(%s) serait la pente de T)." % (d(a), d(fa), d(a)))


def s4():
    k = R.choice(["given", "given", "poly", "poly"])
    a = R.randint(-4, 4)
    if k == "given":
        fa, fpa = R.randint(-9, 9), nz(R, -6, 6)
        ans = "y = " + E((fpa, "x"), (fa - fpa * a, ""))
        return M("f(%s) = %s et f′(%s) = %s. Quelle est l’équation de la tangente à la courbe de f au point d’abscisse %s ?" % (d(a), d(fa), d(a), d(fpa), d(a)), ans,
                 ["y = " + E((fpa, "x"), (fa + fpa * a, "")), "y = " + E((fa, "x"), (fpa - fa * a, "")), "y = " + E((fpa, "x"), (fa, "")), "y = " + E((fpa, "x"), (-fa - fpa * a, "")), "y = " + E((fa, "x"), (fpa, "")), "y = " + E((-fpa, "x"), (fa, ""))],
                 "y = f′(a)(x − a) + f(a) = %s(x − %s) + %s = <b>%s</b>." % (d(fpa), par(a), par(fa), ans[4:]))
    cs = rnd_poly()
    fa, fpa = ev(cs, a), ev(der(cs), a)
    ans = "y = " + E((fpa, "x"), (fa - fpa * a, ""))
    return M("Quelle est l’équation de la tangente à la courbe de f(x) = %s au point d’abscisse %s ?" % (poly(cs), d(a)), ans,
             ["y = " + E((fpa, "x"), (fa + fpa * a, "")), "y = " + E((fpa, "x"), (fa, "")), "y = " + E((fa, "x"), (fpa - fa * a, "")), "y = " + E((fpa, "x"), (fa - fpa * a + 1, "")), "y = " + E((fa, "x"), (fpa, "")), "y = " + E((1, "x"), (fa - a, ""))],
             "f(%s) = %s ; f′(x) = %s donc f′(%s) = %s ; y = %s(x − %s) + %s : <b>%s</b>." % (d(a), d(fa), poly(der(cs)), d(a), d(fpa), d(fpa), par(a), par(fa), ans))


def s5():
    k = R.choice(["approx", "vitesse", "vitesse", "marginal", "approx"])
    if k == "approx":
        a = R.randint(1, 9)
        fa, fpa = R.randint(-9, 20), nz(R, -8, 8)
        h = R.choice([Fr(1, 10), Fr(2, 10), Fr(-1, 10), Fr(5, 100), Fr(-2, 100), Fr(1, 100)])
        return M("f(%d) = %s et f′(%d) = %s. Donne une valeur approchée de f(%s) (approximation affine)." % (a, d(fa), a, d(fpa), d(a + h)), d(fa + fpa * h),
                 [d(fa + h), d(fpa * (a + h)), d(fa - fpa * h), d(fpa + fa * h)], "f(a + h) ≈ f(a) + f′(a) × h = %s + %s × %s = <b>%s</b>." % (d(fa), par(fpa), d(h), d(fa + fpa * h)))
    if k == "vitesse":
        c = R.choice([2, 3, 4, 5])
        t = R.randint(1, 8)
        b = R.randint(0, 6)
        dist = "%dt²%s" % (c, (" + %dt" % b if b > 1 else " + t") if b else "")
        return M("Un objet parcourt d(t) = %s mètres en t secondes. Quelle est sa vitesse instantanée à t = %d s ?" % (dist, t), "%d m/s" % (2 * c * t + b),
                 ["%d m/s" % (c * t * t + b * t), "%s m/s" % d(Fr(c * t * t + b * t, t)) if Fr(c * t * t + b * t, t) != 2 * c * t + b else "%d m/s" % (c * t + b), "%d m/s" % (2 * c + b), "%d m/s" % (2 * c * t)],
                 "v(t) = d′(t) = %s ; v(%d) = <b>%d m/s</b> (la vitesse moyenne d(t) ÷ t ne convient pas)." % (expr([(2 * c, "t"), (b, "")]), t, 2 * c * t + b))
    q0 = R.randint(10, 60)
    a = R.choice([Fr(1, 2), 1, 2])
    b = R.randint(2, 20)
    return M("Le coût de production de q objets est C(q) = %sq² + %dq (en €). Que vaut C′(%d) (coût marginal) ?" % (fq(a) if a != 1 else "", b, q0), euro(2 * a * q0 + b),
             [euro(a * q0 * q0 + b * q0), euro(a * q0 + b), euro(2 * a * q0)], "C′(q) = %sq + %d ; C′(%d) = <b>%s</b>." % (d(2 * a) if 2 * a != 1 else "", b, q0, euro(2 * a * q0 + b)))


def main():
    seen = set()
    sets = [("Taux de variation et sécante", mix(R, seen, [(s1, 20)])), ("Du taux de variation au nombre dérivé", mix(R, seen, [(s2, 20)])),
            ("Lecture graphique", mix(R, seen, [(s3, 20)])), ("Équation de la tangente", mix(R, seen, [(s4, 20)])), ("Approximation affine et vitesse", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>taux de variation</b> de f entre a et a + h est (f(a + h) − f(a)) ÷ h : c’est le coefficient directeur de la sécante.",
              "Quand h tend vers 0, si ce taux tend vers un nombre, c’est le <b>nombre dérivé</b> f′(a) : la pente de la tangente au point d’abscisse a.",
              "Tangente en a : <b>y = f′(a)(x − a) + f(a)</b>. Près de a : f(a + h) ≈ f(a) + f′(a) × h."],
             [("f(x) = x² en a = 3", ["(f(3 + h) − f(3)) ÷ h = (6h + h²) ÷ h = 6 + h", "f′(3) = 6, f(3) = 9"], "tangente y = 6(x − 3) + 9 = 6x − 9")],
             [["y = f′(a)(x + a) + f(a)", "C’est x − a."], ["f′(a) = f(a) lu sur le graphique", "f(a) est l’ordonnée du point ; f′(a) est la pente de la tangente."],
              ["Taux = (b − a) ÷ (f(b) − f(a))", "On divise la variation de f par la variation de x."]])
    faq = [("Que représente f′(a) ?", "La pente de la tangente à la courbe au point d’abscisse a, et la vitesse de variation instantanée de f en a."),
           ("Comment lire f′(a) sur un graphique ?", "On repère deux points de la tangente et on calcule (différence des ordonnées) ÷ (différence des abscisses).")]
    unit("premiere", R, "nombre-derive-et-tangente", "F",
         "Taux de variation, sécantes ; nombre dérivé comme limite du taux de variation ; tangente à une courbe, équation de la tangente ; approximation affine ; interpréter le nombre dérivé en contexte (vitesse instantanée, coût marginal)",
         "Nombre dérivé et tangente", "Nombre dérivé et tangente",
         "Fiches de maths première sur le nombre dérivé : taux de variation, sécante, limite, lecture graphique, équation de tangente et approximation affine. 100 exercices corrigés.",
         "Tangente : y = f′(a)(x − a) + f(a)", "f′(a) est la pente de la tangente en a", body, faq, sets, 9)


if __name__ == "__main__":
    main()
