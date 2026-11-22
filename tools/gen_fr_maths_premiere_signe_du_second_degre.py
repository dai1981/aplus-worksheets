# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Signe d’un polynôme du second degré, factorisation et inéquations
  python3 tools/gen_fr_maths_premiere_signe_du_second_degre.py
Erreurs : « du signe de a entre les racines », oublier le coefficient a en factorisant, crochets ouverts/fermés inversés avec ⩽, Δ < 0 donc « jamais positif ».
"""
import random
from fr_ly1 import *

R = random.Random(60608)


def iv(a, b, ca, cb):
    return "%s%s ; %s%s" % (ca, a, b, cb)


def roots():
    a = R.choice([1, 1, 2, -1, -2, 3])
    x1, x2 = sorted(R.sample(range(-8, 9), 2))
    return a, x1, x2, -a * (x1 + x2), a * x1 * x2


def s1():
    a, x1, x2, b, c = roots()
    k = R.choice(["out", "in", "x"])
    if k in ("out", "in"):
        ans = ("positif" if a > 0 else "négatif") if k == "out" else ("négatif" if a > 0 else "positif")
        where = "à l’extérieur des racines (x &lt; %s ou x &gt; %s)" % (d(x1), d(x2)) if k == "out" else "entre les racines (%s &lt; x &lt; %s)" % (d(x1), d(x2))
        return M("f(x) = %s a pour racines %s et %s. Quel est le signe de f(x) %s ?" % (P2(a, b, c), d(x1), d(x2), where), ans,
                 ["négatif" if ans == "positif" else "positif", "nul", "positif puis négatif"],
                 "f(x) est du signe de a = %s à l’extérieur des racines et du signe contraire entre elles : <b>%s</b>." % (d(a), ans))
    x = R.choice([v for v in range(-9, 10) if v not in (x1, x2)])
    v = a * (x - x1) * (x - x2)
    ans = "positif" if v > 0 else "négatif"
    return M("f(x) = %s. Quel est le signe de f(%s) ?" % ("%s(%s)(%s)" % ("" if a == 1 else MINUS if a == -1 else d(a), E((1, "x"), (-x1, "")), E((1, "x"), (-x2, ""))), d(x)), ans,
             ["négatif" if v > 0 else "positif", "nul", "on ne peut pas savoir"], "f(%s) = %s × %s × %s = %s : <b>%s</b>." % (d(x), d(a), par(x - x1), par(x - x2), d(v), ans))


def s2():
    a, x1, x2, b, c = roots()
    op = R.choice(["&gt; 0", "&lt; 0", "⩾ 0", "⩽ 0"])
    cl = "⩾" in op or "⩽" in op
    pos = ">" in op.replace("&gt;", ">") or "⩾" in op
    want_out = (a > 0) == pos
    if want_out:
        ans = "S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(x1), "]" if cl else "[", "[" if cl else "]", d(x2))
        alt = iv(d(x1), d(x2), "[" if cl else "]", "]" if cl else "[")
        bad = "S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(x1), "[" if cl else "]", "]" if cl else "[", d(x2))
    else:
        ans = "S = " + iv(d(x1), d(x2), "[" if cl else "]", "]" if cl else "[")
        alt = "]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(x1), "]" if cl else "[", "[" if cl else "]", d(x2))
        bad = "S = " + iv(d(x1), d(x2), "]" if cl else "[", "[" if cl else "]")
    w = ["S = " + alt, bad, ans.replace(d(x1), "#").replace(d(x2), d(-x1)).replace("#", d(-x2)) if (-x2, -x1) != (x1, x2) else "S = ℝ", "S = ℝ"]
    return M("Résous %s %s (racines %s et %s)." % (P2(a, b, c), op, d(x1), d(x2)), ans, w,
             "a = %s : f(x) est %s à l’extérieur des racines, %s entre elles. <b>%s</b>." % (d(a), "positif" if a > 0 else "négatif", "négatif" if a > 0 else "positif", ans))


def s3():
    k = R.choice(["fact", "fact", "fact_a", "nofact"])
    if k == "nofact":
        a = R.choice([1, 2, -1])
        b = R.randint(-4, 4)
        c = (b * b // (4 * abs(a)) + R.randint(1, 6)) * (1 if a > 0 else -1)
        return M("Peut-on factoriser %s sous la forme a(x − x₁)(x − x₂) ?" % P2(a, b, c), "non, car Δ = %s &lt; 0" % d(b * b - 4 * a * c),
                 ["oui, car Δ = %s" % d(b * b - 4 * a * c), "oui, car a ≠ 0", "non, car c %s 0" % ("&gt;" if c > 0 else "&lt;")],
                 "Δ = %s &lt; 0 : pas de racine réelle, <b>pas de factorisation</b> de cette forme." % d(b * b - 4 * a * c))
    a, x1, x2, b, c = roots()
    if x1 == -x2:
        return None
    if k == "fact":
        a = 1
        b, c = -(x1 + x2), x1 * x2
    F = lambda A, p, q: ("%s(%s)(%s)" % ("" if A == 1 else MINUS if A == -1 else d(A), E((1, "x"), (-p, "")), E((1, "x"), (-q, "")))).replace("(x)", "x")
    ans = F(a, x1, x2)
    return M("Factorise %s." % P2(a, b, c), ans, [F(a, -x1, -x2), F(1, x1, x2) if a != 1 else F(1, -x1, x2), F(a, x1, -x2), F(-a, x1, x2), F(a, -x1, x2), F(a, x2, x2), F(a, x1 - x2, x2)],
             "Δ = %s ; racines %s et %s ; <b>%s</b>." % (d(b * b - 4 * a * c), d(x1), d(x2), ans))


def s4():
    k = R.choice(["neg", "neg", "zero", "zero_ineq"])
    a = R.choice([1, 2, -1, -3])
    if k == "neg":
        b = R.randint(-4, 4)
        c = (b * b // (4 * abs(a)) + R.randint(1, 5)) * (1 if a > 0 else -1)
        if b * b - 4 * a * c >= 0:
            return None
        op = R.choice(["&gt; 0", "&lt; 0"])
        ans = "S = ℝ" if (a > 0) == (op == "&gt; 0") else "S = ∅"
        return M("Résous %s %s." % (P2(a, b, c), op), ans, ["S = ∅" if ans == "S = ℝ" else "S = ℝ", "S = ]0 ; +∞[", "S = ]−∞ ; 0["],
                 "Δ = %s &lt; 0 : f(x) est toujours du signe de a = %s. <b>%s</b>." % (d(b * b - 4 * a * c), d(a), ans))
    x0 = R.randint(-6, 6)
    b, c = -2 * a * x0, a * x0 * x0
    if k == "zero":
        ans = "positif ou nul, nul seulement en x = %s" % d(x0) if a > 0 else "négatif ou nul, nul seulement en x = %s" % d(x0)
        return M("Quel est le signe de %s sur ℝ ?" % P2(a, b, c), ans, ["négatif ou nul, nul seulement en x = %s" % d(x0) if a > 0 else "positif ou nul, nul seulement en x = %s" % d(x0), "positif puis négatif", "positif ou nul, nul seulement en x = %s" % d(-x0) if x0 else "toujours strictement positif"],
                 "Δ = 0 : f(x) = %s(x %s %d)², du signe de a, nul en x = %s : <b>%s</b>." % ("" if a == 1 else MINUS if a == -1 else d(a), MINUS if x0 > 0 else "+", abs(x0), d(x0), ans))
    op = "&gt; 0" if a > 0 else "&lt; 0"
    ans = "S = ℝ ∖ {%s}" % d(x0)
    return M("Résous %s %s." % (P2(a, b, c), op), ans, ["S = ℝ", "S = ∅", "S = {%s}" % d(x0)],
             "Δ = 0 : f(x) = a(x − %s)² est du signe de a partout, et nul en %s. <b>%s</b>." % (par(x0), d(x0), ans))


def s5():
    k = R.choice(["benef", "benef", "compare", "aire", "graph"])
    if k == "benef":
        x1, x2 = sorted(R.sample(range(5, 80, 5), 2))
        a = -R.choice([1, 2])
        return M("Le bénéfice d’une entreprise pour x centaines d’objets est B(x) = %s(x − %d)(x − %d). Pour quelles valeurs de x l’entreprise est-elle rentable (B(x) &gt; 0) ?" % (MINUS if a == -1 else MINUS + "2", x1, x2),
                 "x ∈ ]%d ; %d[" % (x1, x2), ["x ∈ [0 ; %d[ ∪ ]%d ; +∞[" % (x1, x2), "x ∈ ]%d ; +∞[" % x2, "x ∈ ]0 ; %d[" % x1],
                 "a &lt; 0 : B(x) est positif entre les racines : <b>x ∈ ]%d ; %d[</b>." % (x1, x2))
    if k == "compare":
        m, p = R.randint(-3, 3), R.randint(-4, 4)
        x1, x2 = sorted(R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2))
        b, c = -(x1 + x2) + m, x1 * x2 + p
        return M("Pour quelles valeurs de x la parabole y = %s est-elle au-dessus de la droite y = %s ?" % (P2(1, b, c), E((m, "x"), (p, ""))),
                 "x &lt; %s ou x &gt; %s" % (d(x1), d(x2)), ["%s &lt; x &lt; %s" % (d(x1), d(x2)), "x &lt; %s ou x &gt; %s" % (d(-x2), d(-x1)) if (x1, x2) != (-x2, -x1) else "x &gt; %s" % d(x2), "pour tout réel x"],
                 "%s &gt; %s ⇔ %s &gt; 0 ⇔ (%s)(%s) &gt; 0 ; a = 1 &gt; 0, racines %s et %s : <b>x &lt; %s ou x &gt; %s</b>." % (P2(1, b, c), E((m, "x"), (p, "")), P2(1, -(x1 + x2), x1 * x2), E((1, "x"), (-x1, "")), E((1, "x"), (-x2, "")), d(x1), d(x2), d(x1), d(x2)))
    if k == "aire":
        L_ = R.randint(8, 16)
        A = R.randint(L_ * 2, L_ * L_ // 4 - 1)
        disc = L_ * L_ - 4 * A
        import math
        r = math.isqrt(disc)
        if r * r != disc or (L_ - r) % 2:
            return None
        x1, x2 = (L_ - r) // 2, (L_ + r) // 2
        return M("Un rectangle a un périmètre de %d cm et un côté x (en cm). Son aire est x(%d − x). Pour quelles valeurs de x l’aire dépasse-t-elle %d cm² ?" % (2 * L_, L_, A),
                 "%d &lt; x &lt; %d" % (x1, x2), ["x &lt; %d ou x &gt; %d" % (x1, x2), "0 &lt; x &lt; %d" % x1, "%d &lt; x &lt; %d" % (x1, L_)],
                 "x(%d − x) &gt; %d ⇔ −x² + %dx − %d &gt; 0 ; racines %d et %d, a &lt; 0 : <b>%d &lt; x &lt; %d</b>." % (L_, A, L_, A, x1, x2, x1, x2))
    a = R.choice([1, -1])
    x1, x2 = sorted(R.sample(range(-4, 5), 2))
    svg = kurve([(lambda x, a=a, x1=x1, x2=x2: a * (x - x1) * (x - x2) * 0.5, BLUE, "")], (-5, 5, 1), (-5, 5, 1), label="parabole")
    ans = ("x &lt; %s ou x &gt; %s" if a > 0 else "%s &lt; x &lt; %s") % (d(x1), d(x2))
    return M("<div class='qfig'>%s</div>Pour quelles valeurs de x a-t-on f(x) &gt; 0 ?" % svg, ans,
             [("%s &lt; x &lt; %s" if a > 0 else "x &lt; %s ou x &gt; %s") % (d(x1), d(x2)), "x &gt; %s" % d(x2), "x &lt; %s" % d(x1)],
             "On lit où la courbe est au-dessus de l’axe des abscisses : <b>%s</b>." % ans)


def main():
    seen = set()
    sets = [("Signe d’un trinôme", mix(R, seen, [(s1, 20)])), ("Inéquations du second degré", mix(R, seen, [(s2, 20)])),
            ("Factoriser", mix(R, seen, [(s3, 20)])), ("Cas Δ = 0 et Δ < 0", mix(R, seen, [(s4, 20)])), ("Problèmes et lecture graphique", mix(R, seen, [(s5, 20)]))]
    body = L(["Si Δ &gt; 0, f(x) = a(x − x₁)(x − x₂) est <b>du signe de a à l’extérieur des racines</b> et du signe contraire entre elles.",
              "Si Δ = 0, f(x) = a(x − x₀)² est du signe de a et s’annule en x₀. Si Δ &lt; 0, f(x) est toujours du signe de a.",
              "Pour résoudre f(x) &gt; 0 : racines, signe de a, tableau de signes, puis on lit l’ensemble des solutions (crochets fermés avec ⩾ ou ⩽)."],
             [("x² − x − 6 ⩽ 0", ["Δ = 25, racines −2 et 3", "a = 1 &gt; 0 : négatif entre les racines"], "S = [−2 ; 3]")],
             [["Du signe de a entre les racines", "C’est à l’extérieur des racines qu’il est du signe de a."], ["2x² − 2x − 4 = (x + 1)(x − 2)", "On garde a : 2(x + 1)(x − 2)."],
              ["Δ &lt; 0 donc x² + x + 1 &gt; 0 n’a pas de solution", "Δ &lt; 0 et a &gt; 0 : c’est toujours positif, S = ℝ."]])
    faq = [("Comment retenir la règle du signe ?", "Pense à la parabole : si a &gt; 0, elle est tournée vers le haut, donc au-dessus de l’axe à l’extérieur des racines et en dessous entre elles."),
           ("Faut-il toujours factoriser pour étudier le signe ?", "Non : il suffit de connaître les racines (avec Δ) et le signe de a. La factorisation aide à justifier avec un tableau de signes.")]
    unit("premiere", R, "signe-du-second-degre", "A",
         "Étudier le signe d’une fonction polynôme du second degré ; factoriser quand c’est possible ; résoudre une inéquation du second degré ; interpréter graphiquement",
         "Signe du second degré et inéquations", "Signe du second degré",
         "Fiches de maths première sur le signe d’un trinôme du second degré : règle du signe de a, factorisation, inéquations, cas Δ = 0 et Δ < 0, problèmes. 100 exercices corrigés.",
         "Du signe de a à l’extérieur des racines", "Du signe contraire entre les racines", body, faq, sets, 8)


if __name__ == "__main__":
    main()
