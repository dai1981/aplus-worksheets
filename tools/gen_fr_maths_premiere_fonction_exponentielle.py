# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Fonction exponentielle (propriétés algébriques, équations et inéquations, dérivées, signe et variations, valeurs)
  python3 tools/gen_fr_maths_premiere_fonction_exponentielle.py
Erreurs : eᵃ × eᵇ = eᵃᵇ, eᵃ + eᵇ = eᵃ⁺ᵇ, (eᵃ)ⁿ = eᵃ⁺ⁿ, (e^(ax+b))′ = e^(ax+b) sans le facteur a, croire que eˣ peut être négatif ou nul.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60612)


def ex(t):
    return "e<sup>%s</sup>" % t if t not in ("1", "") else "e"


def lin(a, b, v="x"):
    return E((a, v), (b, ""))


def s1():
    k = R.choice(["prod", "quot", "pow", "inv", "mix"])
    a, b = R.randint(-6, 9), R.randint(-6, 9)
    if k == "prod":
        p, q = lin(nz(R, -4, 4), R.randint(-5, 5)), lin(nz(R, -4, 4), R.randint(-5, 5))
        m1, c1 = R.randint(1, 4), R.randint(-5, 5)
        m2, c2 = R.randint(-3, 3), R.randint(-5, 5)
        if m1 + m2 == 0:
            return None
        ans = ex(lin(m1 + m2, c1 + c2))
        return M("Simplifie %s × %s." % (ex(lin(m1, c1)), ex(lin(m2, c2))), ans,
                 [ex("(%s)(%s)" % (lin(m1, c1), lin(m2, c2))), ex(lin(m1 - m2, c1 - c2)) if m1 != m2 else ex(lin(m1, c1 - c2)), "2" + ex(lin(m1 + m2, c1 + c2)), ex(lin(m1 * m2, c1 * c2)) if m1 * m2 else ex(lin(1, c1 + c2))],
                 "e<sup>a</sup> × e<sup>b</sup> = e<sup>a+b</sup> : <b>%s</b>." % ans)
    if k == "quot":
        if a == b:
            return None
        ans = ex(d(a - b)) if a - b != 1 else "e"
        return M("Simplifie %s ÷ %s." % (ex(d(a)) if a != 1 else "e", ex(d(b)) if b != 1 else "e"), ans,
                 [ex(d(a + b)) if a + b != 1 else "e", ex(fq(Fr(a, b))) if b else ex("1"), ex(d(b - a)) if b - a != 1 else "e", "1"],
                 "e<sup>a</sup> ÷ e<sup>b</sup> = e<sup>a−b</sup> : <b>%s</b>." % ans)
    if k == "pow":
        a, n = nz(R, -5, 5), R.randint(2, 5)
        return M("Simplifie (%s)<sup>%d</sup>." % (ex(d(a)) if a != 1 else "e", n), ex(d(a * n)), [ex(d(a + n)), ex(d(a ** n)) if a ** n != a * n else ex(d(a * n + 1)), "%d%s" % (n, ex(d(a)) if a != 1 else "e")],
                 "(e<sup>a</sup>)<sup>n</sup> = e<sup>na</sup> : <b>%s</b>." % ex(d(a * n)))
    if k == "inv":
        a = nz(R, -9, 9)
        return M("Quelle expression est égale à 1 ÷ %s ?" % (ex(d(a)) if a != 1 else "e"), ex(d(-a)) if -a != 1 else "e", [ex(d(a)) if a != 1 else "e", "−" + (ex(d(a)) if a != 1 else "e"), ex(fq(Fr(1, a))) if abs(a) != 1 else ex("0")],
                 "1 ÷ e<sup>a</sup> = e<sup>−a</sup> : <b>%s</b>." % (ex(d(-a)) if -a != 1 else "e"))
    m = R.randint(2, 4)
    c = R.randint(1, 5)
    ans = ex(lin(m - 1, c))
    return M("Simplifie (%s × %s) ÷ e<sup>x</sup>." % (ex(lin(m, 0)), ex(d(c))), ans if m - 1 != 0 else ex(d(c)),
             [ex(lin(m + 1, c)), ex(lin(m, c - 1)), ex("%dx" % (m * c)), ex(lin(m - 1, -c))], "e<sup>%dx</sup> × e<sup>%d</sup> ÷ e<sup>x</sup> = e<sup>%dx + %d − x</sup> = <b>%s</b>." % (m, c, m, c, ans))


def s2():
    k = R.choice(["eq", "eq", "eq1", "ineq", "ineq", "neg", "carre"])
    if k == "eq":
        a, b, c = nz(R, -5, 5), R.randint(-9, 9), R.randint(-9, 9)
        x = Fr(c - b, a)
        return M("Résous %s = %s." % (ex(lin(a, b)), ex(d(c)) if c != 1 else "e"), "x = %s" % fq(x), ["x = %s" % fq(Fr(c + b, a)), "x = %s" % fq(Fr(c, a) - b), "x = %s" % fq(Fr(c - b, -a)) if x else "x = 1", "x = %s" % fq(Fr(c, a)), "x = %s" % fq(Fr(c - b, 1))],
                 "e<sup>a</sup> = e<sup>b</sup> ⇔ a = b : %s = %s ⇔ <b>x = %s</b>." % (lin(a, b), d(c), fq(x)))
    if k == "eq1":
        a, b = nz(R, -5, 5), nz(R, -9, 9)
        x = Fr(-b, a)
        return M("Résous %s = 1." % ex(lin(a, b)), "x = %s" % fq(x), ["x = %s" % fq(Fr(1 - b, a)), "pas de solution", "x = %s" % fq(-x)],
                 "1 = e<sup>0</sup>, donc %s = 0 ⇔ <b>x = %s</b>." % (lin(a, b), fq(x)))
    if k == "ineq":
        a, b = R.randint(1, 4), R.randint(-6, 6)
        c, e = R.randint(-3, 3), R.randint(-6, 6)
        if a == c:
            return None
        op = R.choice(["&gt;", "&lt;", "⩾", "⩽"])
        x0 = Fr(e - b, a - c)
        pos = a - c > 0
        rev = {"&gt;": "&lt;", "&lt;": "&gt;", "⩾": "⩽", "⩽": "⩾"}
        o2 = op if pos else rev[op]
        cl = op in ("⩾", "⩽")
        if o2 in ("&gt;", "⩾"):
            ans = "S = %s%s ; +∞[" % ("[" if cl else "]", fq(x0))
            w = ["S = ]−∞ ; %s%s" % (fq(x0), "]" if cl else "["), "S = %s%s ; +∞[" % ("]" if cl else "[", fq(x0)), "S = %s%s ; +∞[" % ("[" if cl else "]", fq(-x0)) if x0 else "S = ℝ"]
        else:
            ans = "S = ]−∞ ; %s%s" % (fq(x0), "]" if cl else "[")
            w = ["S = %s%s ; +∞[" % ("[" if cl else "]", fq(x0)), "S = ]−∞ ; %s%s" % (fq(x0), "[" if cl else "]"), "S = ]−∞ ; %s%s" % (fq(-x0), "]" if cl else "[") if x0 else "S = ℝ"]
        return M("Résous %s %s %s." % (ex(lin(a, b)), op, ex(lin(c, e))), ans, w,
                 "exp est strictement croissante : %s %s %s ⇔ %s : <b>%s</b>." % (lin(a, b), op, lin(c, e), "x %s %s" % (o2, fq(x0)), ans))
    if k == "neg":
        a = R.randint(1, 9)
        f = R.choice(["e<sup>x</sup> = %s" % d(-a), "e<sup>x</sup> + %d = 0" % a, "e<sup>2x</sup> = %s" % d(-a)])
        return M("Résous %s." % f, "S = ∅", ["S = {%s}" % d(-a), "S = {0}", "S = {%s}" % d(a)], "e<sup>X</sup> &gt; 0 pour tout réel X : l’équation n’a <b>pas de solution</b>.")
    a = R.randint(1, 5)
    return M("Résous %s = %s." % (ex("x²"), ex(d(a * a))), "S = {%s ; %d}" % (d(-a), a), ["S = {%d}" % a, "S = {%d}" % (a * a), "S = ∅"],
             "x² = %d ⇔ x = %s ou x = %d : <b>S = {%s ; %d}</b>." % (a * a, d(-a), a, d(-a), a))


def s3():
    k = R.choice(["k", "lin", "lin", "xex", "sum", "kex"])
    if k == "k":
        c = nz(R, -9, 9)
        return M("Quelle est la dérivée de f(x) = %se<sup>x</sup> ?" % (d(c) if c not in (1, -1) else MINUS if c == -1 else ""), "f′(x) = %se<sup>x</sup>" % (d(c) if c not in (1, -1) else MINUS if c == -1 else ""),
                 ["f′(x) = %sxe<sup>x−1</sup>" % (d(c) if c != 1 else ""), "f′(x) = %s" % d(c), "f′(x) = e<sup>x</sup>" if c != 1 else "f′(x) = xe<sup>x−1</sup>", "f′(x) = %se<sup>x</sup>" % d(-c) if c not in (1, -1) else "f′(x) = 0"],
                 "(e<sup>x</sup>)′ = e<sup>x</sup> : <b>%se<sup>x</sup></b>." % (d(c) if c not in (1, -1) else MINUS if c == -1 else ""))
    if k in ("lin",):
        a, b = R.choice([2, 3, -1, -2, 4, Fr(1, 2), -3]), R.randint(-5, 5)
        A = fq(a) if Fr(a).denominator != 1 else d(a)
        ans = "f′(x) = %s%s" % ("" if a == 1 else MINUS if a == -1 else A, ex(lin(a, b)))
        return M("Quelle est la dérivée de f(x) = %s ?" % ex(lin(a, b)), ans, ["f′(x) = %s" % ex(lin(a, b)), "f′(x) = %s" % ex(lin(a, b - 1)) if b else "f′(x) = " + ex(lin(a, -1)), "f′(x) = (%s)%s" % (lin(a, b), ex(lin(a, b - 1)))],
                 "(e<sup>ax+b</sup>)′ = a e<sup>ax+b</sup> : <b>%s</b>." % ans[8:])
    if k == "xex":
        return M("Quelle est la dérivée de f(x) = xe<sup>x</sup> ?", "f′(x) = (x + 1)e<sup>x</sup>", ["f′(x) = e<sup>x</sup>", "f′(x) = xe<sup>x</sup>", "f′(x) = x²e<sup>x−1</sup>"],
                 "(uv)′ = u′v + uv′ = e<sup>x</sup> + xe<sup>x</sup> = <b>(x + 1)e<sup>x</sup></b>.")
    if k == "kex":
        a, b = nz(R, -4, 4), R.randint(-6, 6)
        ans = "f′(x) = (%s)e<sup>x</sup>" % lin(a, a + b)
        return M("Quelle est la dérivée de f(x) = (%s)e<sup>x</sup> ?" % lin(a, b), ans, ["f′(x) = %se<sup>x</sup>" % d(a) if a not in (1, -1) else "f′(x) = e<sup>x</sup>", "f′(x) = (%s)e<sup>x</sup>" % lin(a, b), "f′(x) = (%s)e<sup>x</sup>" % lin(a, b - a) if a else "f′(x) = 0", "f′(x) = (%s)e<sup>x</sup>" % lin(a, a)],
                 "u′v + uv′ = %se<sup>x</sup> + (%s)e<sup>x</sup> = <b>%s</b>." % (d(a), lin(a, b), ans[8:]))
    c, n = nz(R, -5, 5), R.randint(2, 4)
    ans = "f′(x) = e<sup>x</sup> %s %s" % ("+" if c > 0 else MINUS, ("%dx<sup>%d</sup>" % (abs(c) * n, n - 1)) if n > 2 else "%dx" % (abs(c) * 2))
    return M("Quelle est la dérivée de f(x) = e<sup>x</sup> %s %sx<sup>%d</sup> ?" % ("+" if c > 0 else MINUS, d(abs(c)) if abs(c) != 1 else "", n), ans,
             [ans.replace("e<sup>x</sup>", "xe<sup>x−1</sup>"), "f′(x) = e<sup>x</sup> %s %sx<sup>%d</sup>" % ("+" if c > 0 else MINUS, d(abs(c)) if abs(c) != 1 else "", n), "f′(x) = %s" % ans[8:].split(" ", 1)[1].lstrip("+ ")],
             "On dérive terme à terme : <b>%s</b>." % ans[8:])


def s4():
    k = R.choice(["sign", "sign", "var", "tan0", "decr"])
    if k == "sign":
        a, b = nz(R, -5, 5), R.randint(-9, 9)
        x0 = Fr(-b, a)
        ans = "positif pour x &gt; %s" % fq(x0) if a > 0 else "positif pour x &lt; %s" % fq(x0)
        return M("Quel est le signe de f(x) = (%s)e<sup>x</sup> ?" % lin(a, b), ans + ", négatif de l’autre côté",
                 [("positif pour x &lt; %s" % fq(x0) if a > 0 else "positif pour x &gt; %s" % fq(x0)) + ", négatif de l’autre côté", "toujours positif, car e<sup>x</sup> &gt; 0", "toujours négatif"],
                 "e<sup>x</sup> &gt; 0 : f(x) a le signe de %s, qui s’annule en %s : <b>%s</b>." % (lin(a, b), fq(x0), ans))
    if k == "var":
        a = R.randint(-5, 5)
        m = a - 1
        F = lambda t: "xe<sup>x</sup>" if t == 0 else "(%s)e<sup>x</sup>" % E((1, "x"), (-t, ""))
        return M("f(x) = %s, donc f′(x) = %s. Où f admet-elle son minimum ?" % (F(a), F(m)), "en x = %s" % d(m), ["en x = %s" % d(a), "en x = %s" % d(-m) if m else "en x = 1", "en x = 0" if m else "en x = 2"],
                 "f′(x) a le signe de %s : négatif puis positif, minimum <b>en x = %s</b>." % (E((1, "x"), (-m, "")), d(m)))
    if k == "tan0":
        c = R.choice([1, 2, 3, -1, -2])
        ans = "y = %s" % E((c, "x"), (1, ""))
        return M("Quelle est l’équation de la tangente à la courbe de f(x) = %s au point d’abscisse 0 ?" % ex(lin(c, 0)), ans, ["y = %s" % E((1, "x"), (1, "")) if c != 1 else "y = x", "y = %s" % E((c, "x")) if c != 1 else "y = ex", "y = %s" % E((c, "x"), (c, "")) if c != 1 else "y = 2x + 1", "y = %s" % E((c, "x"), (-1, ""))],
                 "f(0) = 1, f′(x) = %s donc f′(0) = %s : <b>%s</b>." % ((d(c) if c != 1 else "") + ex(lin(c, 0)), d(c), ans))
    k2 = R.randint(1, 5)
    c = R.randint(2, 9)
    return M("Quel est le sens de variation de f(x) = %d%s sur ℝ ?" % (c, ex(lin(-k2, 0))), "décroissante", ["croissante", "décroissante puis croissante", "constante"],
             "f′(x) = %s%s &lt; 0 : f est <b>décroissante</b>." % (d(-c * k2), ex(lin(-k2, 0))))


def s5():
    k = R.choice(["val", "val", "compare", "suite", "euler", "e0"])
    if k == "val":
        a = R.choice([-2, -1, Fr(1, 2), 1, 2, 3, Fr(-1, 2)])
        v = math.exp(float(a))
        ans = dk(Fr(v), 2) if v < 10 else dk(Fr(v), 1)
        return M("Donne une valeur approchée au centième de %s." % (ex(fq(a)) if a != 1 else "e"), ans,
                 [dk(Fr(float(a) * 2.718), 2), dk(Fr(2.718 + float(a)), 2), dk(Fr(v * 2), 2), dk(Fr(1 / v), 2)], "À la calculatrice : %s ≈ <b>%s</b>." % (ex(fq(a)) if a != 1 else "e", ans))
    if k == "compare":
        a, b = R.sample(range(-5, 6), 2)
        ans = "%s %s %s" % (ex(d(a)) if a != 1 else "e", "&lt;" if a < b else "&gt;", ex(d(b)) if b != 1 else "e")
        return M("Compare %s et %s." % (ex(d(a)) if a != 1 else "e", ex(d(b)) if b != 1 else "e"), ans,
                 ["%s %s %s" % (ex(d(a)) if a != 1 else "e", "&gt;" if a < b else "&lt;", ex(d(b)) if b != 1 else "e"), "%s = %s" % (ex(d(a)) if a != 1 else "e", ex(d(b)) if b != 1 else "e"), "on ne peut pas comparer"],
                 "exp est strictement croissante et %d %s %d : <b>%s</b>." % (a, "&lt;" if a < b else "&gt;", b, ans) if a >= 0 and b >= 0 else "exp est strictement croissante : <b>%s</b>." % ans)
    if k == "suite":
        a = R.choice([2, 3, -1, Fr(1, 2), -2, Fr(-1, 2)])
        return M("u<sub>n</sub> = %s. Cette suite est géométrique. Quelle est sa raison ?" % ex("%sn" % (fq(a) if a not in (1, -1) else MINUS if a == -1 else "")), ex(fq(a)) if a != 1 else "e",
                 [fq(a), "e", ex("%sn" % fq(a)) if a not in (1, -1) else "n"], "u<sub>n+1</sub> = e<sup>%s(n+1)</sup> = u<sub>n</sub> × %s : raison <b>%s</b>." % (fq(a), ex(fq(a)), ex(fq(a))))
    if k == "euler":
        h = R.choice([Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(1, 2)])
        n = R.randint(2, 3)
        v = (1 + h) ** n
        return M("Méthode d’Euler pour f′ = f, f(0) = 1, avec le pas h = %s : y<sub>k+1</sub> = (1 + h) × y<sub>k</sub>. Quelle valeur approchée de f(%s) obtient-on ?" % (d(h), d(n * h)), d(v),
                 [d(1 + n * h), d((1 + h) * n), d(h ** n + 1)], "y<sub>%d</sub> = %s<sup>%d</sup> = <b>%s</b> (valeur exacte %s ≈ %s)." % (n, d(1 + h), n, d(v), ex(d(n * h)), dk(Fr(math.exp(float(n * h))), 3)))
    v = R.choice([("e<sup>0</sup>", "1", ["0", "e", "n’existe pas"]), ("e<sup>1</sup>", "e ≈ 2,718", ["1", "0", "10"]), ("le signe de e<sup>x</sup>", "strictement positif pour tout x", ["positif seulement si x &gt; 0", "négatif si x &lt; 0", "nul en 0"]),
                  ("(e<sup>x</sup>)′", "e<sup>x</sup>", ["xe<sup>x−1</sup>", "e", "1"])])
    return M("Que vaut %s ?" % v[0], v[1], v[2], "Réponse : <b>%s</b>." % v[1])


def main():
    seen = set()
    sets = [("Propriétés algébriques", mix(R, seen, [(s1, 20)])), ("Équations et inéquations", mix(R, seen, [(s2, 20)])),
            ("Dérivées", mix(R, seen, [(s3, 20)])), ("Signe et variations", mix(R, seen, [(s4, 20)])), ("Valeurs, suites et méthode d’Euler", mix(R, seen, [(s5, 20)]))]
    body = L(["La fonction exponentielle est l’unique fonction dérivable sur ℝ telle que <b>exp′ = exp et exp(0) = 1</b>. On note exp(x) = e<sup>x</sup>, avec e ≈ 2,718.",
              "e<sup>a</sup> × e<sup>b</sup> = e<sup>a+b</sup> ; e<sup>a</sup> ÷ e<sup>b</sup> = e<sup>a−b</sup> ; e<sup>−a</sup> = 1 ÷ e<sup>a</sup> ; (e<sup>a</sup>)<sup>n</sup> = e<sup>na</sup>.",
              "e<sup>x</sup> &gt; 0 pour tout x ; exp est strictement croissante, donc e<sup>a</sup> = e<sup>b</sup> ⇔ a = b et e<sup>a</sup> &lt; e<sup>b</sup> ⇔ a &lt; b.",
              "(e<sup>ax+b</sup>)′ = a e<sup>ax+b</sup>."],
             [("e<sup>2x − 1</sup> &gt; e<sup>x + 3</sup>", ["2x − 1 &gt; x + 3", "x &gt; 4"], "S = ]4 ; +∞["), ("f(x) = (x − 2)e<sup>x</sup>", ["f′(x) = e<sup>x</sup> + (x − 2)e<sup>x</sup> = (x − 1)e<sup>x</sup>"], "minimum en x = 1")],
             [["e<sup>2</sup> × e<sup>3</sup> = e<sup>6</sup>", "On ajoute les exposants : e<sup>5</sup>."], ["e<sup>2</sup> + e<sup>3</sup> = e<sup>5</sup>", "Il n’y a pas de règle pour la somme."],
              ["(e<sup>3x</sup>)′ = e<sup>3x</sup>", "(e<sup>3x</sup>)′ = 3e<sup>3x</sup>."], ["e<sup>x</sup> = −2 a une solution", "e<sup>x</sup> &gt; 0 : aucune solution."]])
    faq = [("Pourquoi e<sup>x</sup> est-il toujours positif ?", "e<sup>x</sup> = (e<sup>x/2</sup>)² est un carré, et il n’est jamais nul car e<sup>x</sup> × e<sup>−x</sup> = 1."),
           ("Quel lien avec les suites géométriques ?", "Pour tout réel a, la suite u<sub>n</sub> = e<sup>na</sup> est géométrique de raison e<sup>a</sup> : l’exponentielle prolonge les suites géométriques aux réels.")]
    unit("premiere", R, "fonction-exponentielle", "F",
         "Fonction exponentielle : définition par exp′ = exp et exp(0) = 1, propriétés algébriques, nombre e, signe, variations et courbe ; résoudre des équations et inéquations ; dériver x ↦ e<sup>ax+b</sup> ; lien avec les suites géométriques ; méthode d’Euler",
         "Fonction exponentielle : propriétés et dérivée", "Fonction exponentielle",
         "Fiches de maths première sur la fonction exponentielle : propriétés algébriques, équations, inéquations, dérivées, signe, variations et méthode d’Euler. 100 exercices corrigés.",
         "exp′ = exp et e^0 = 1", "e^a × e^b = e^(a+b) ; e^x > 0", body, faq, sets, 12)


if __name__ == "__main__":
    main()
