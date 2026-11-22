# -*- coding: utf-8 -*-
"""
France Maths Seconde : Signe d’une expression — produit nul, tableaux de signes de produits et de quotients, inéquations
  python3 tools/gen_fr_maths_seconde_tableaux_de_signes.py
Erreurs : signe de ax + b sans regarder a, valeur interdite incluse, (x − 3)(x + 2) = 0 → x = −3 ou 2, oublier qu’un carré est positif.
"""
import random
from fr_c4 import *

R = random.Random(60507)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def S2(a, b):
    a, b = sorted([a, b])
    return "S = {%s ; %s}" % (fq(a), fq(b)) if a != b else "S = {%s}" % fq(a)


def s1():
    a, b = nz(-6, 6), nz(-9, 9)
    c, e = nz(-6, 6), nz(-9, 9)
    x1, x2 = Fr(-b, a), Fr(-e, c)
    if x1 == x2:
        return None
    if R.random() < 0.5:
        a, c = 1, 1
        x1, x2 = Fr(-b), Fr(-e)
    q = "(%s)(%s) = 0" % (E((a, "x"), (b, "")), E((c, "x"), (e, "")))
    return M("Résous : %s" % q, S2(x1, x2), [S2(-x1, -x2), "S = {%s}" % fq(x1), S2(Fr(b, a), x2) if Fr(b, a) != x1 else S2(x1, x2 + 1)],
             "Un produit est nul si et seulement si l’un des facteurs est nul : <b>%s</b>." % S2(x1, x2))


def s2():
    a, b = nz(-6, 6), nz(-9, 9)
    x0 = Fr(-b, a)
    k = R.choice(["pos", "neg"])
    ok = (a > 0) == (k == "pos")
    side = "x &gt; %s" % fq(x0) if ok else "x &lt; %s" % fq(x0)
    other = "x &lt; %s" % fq(x0) if ok else "x &gt; %s" % fq(x0)
    return M("Pour quelles valeurs de x l’expression %s est-elle strictement %s ?" % (E((a, "x"), (b, "")), "positive" if k == "pos" else "négative"), side, [other, "x &gt; %s" % fq(-x0) if x0 and side != "x &gt; %s" % fq(-x0) else "x &lt; %s" % fq(-x0 - 1), "pour tout x"],
             "%s s’annule en %s ; a = %s est %s, donc elle est %s %s : <b>%s</b>." % (E((a, "x"), (b, "")), fq(x0), d(a), "positif" if a > 0 else "négatif", "du signe de a", "à droite de " + fq(x0), side))


def table_svg(x1, x2, f1, f2, quot=False):
    """tableau de signes de (f1)(f2) ou (f1)/(f2) ; x1 < x2 racines"""
    W, H = 470, 168
    cols = [70, 170, 250, 330, 420]
    s = []
    s.append("<rect x='2' y='2' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 4, H - 4, INK))
    for y in (40, 82, 124):
        s.append(line(2, y, W - 2, y, INK, 1.2))
    s.append(line(130, 2, 130, H - 2, INK, 1.2))
    s.append(text(66, 27, "x", 15, weight=700))
    s.append(text(150, 27, "−∞", 14) + text(210, 27, x1, 14) + text(330, 27, x2, 14) + text(445, 27, "+∞", 14))
    labs = [f1[0], f2[0], ("(%s)/(%s)" if quot else "(%s)(%s)") % (f1[0], f2[0])]
    sig = [f1[1], f2[1], [f1[1][i] * f2[1][i] for i in range(3)]]
    for r_, (lab, sg) in enumerate(zip(labs, sig)):
        y = 66 + 42 * r_
        s.append(text(66, y, lab, 13 if r_ < 2 else 12))
        for i, xc in enumerate((170, 270, 390)):
            s.append(text(xc, y, "+" if sg[i] > 0 else MINUS, 16, weight=700))
        for xb in (210, 330):
            s.append(line(xb, 40 + 42 * r_, xb, 82 + 42 * r_, INK, 1))
    return wrap(W, H, "".join(s), "tableau de signes", lg=True)


def s3():
    a, b = nz(-8, 8), nz(-8, 8)
    if a == b:
        return None
    r1, r2 = sorted([-a, -b])
    k = R.choice(["pos", "neg", "pos0", "neg0"])
    q = "(%s)(%s)" % (E((1, "x"), (a, "")), E((1, "x"), (b, "")))
    op = {"pos": "&gt; 0", "neg": "&lt; 0", "pos0": "⩾ 0", "neg0": "⩽ 0"}[k]
    cl = k.endswith("0")
    if k.startswith("pos"):
        ans = "S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(r1), "]" if cl else "[", "[" if cl else "]", d(r2))
        w = ["S = %s%s ; %s%s" % ("[" if cl else "]", d(r1), d(r2), "]" if cl else "["), "S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(-r2), "]" if cl else "[", "[" if cl else "]", d(-r1)) if (-r2, -r1) != (r1, r2) else "S = ]%s ; +∞[" % d(r2),
             "S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(r1), "[" if cl else "]", "]" if cl else "[", d(r2))]
    else:
        ans = "S = %s%s ; %s%s" % ("[" if cl else "]", d(r1), d(r2), "]" if cl else "[")
        w = ["S = ]−∞ ; %s%s ∪ %s%s ; +∞[" % (d(r1), "]" if cl else "[", "[" if cl else "]", d(r2)), "S = %s%s ; %s%s" % ("[" if cl else "]", d(-r2), d(-r1), "]" if cl else "[") if (-r2, -r1) != (r1, r2) else "S = ]−∞ ; %s[" % d(r1),
             "S = %s%s ; %s%s" % ("]" if cl else "[", d(r1), d(r2), "[" if cl else "]")]
    return M("Résous l’inéquation %s %s." % (q, op), ans, w, "Racines %s et %s ; le produit est positif à l’extérieur des racines, négatif entre elles : <b>%s</b>." % (d(r1), d(r2), ans))


def s4():
    a, b = nz(-8, 8), nz(-8, 8)
    if a == b:
        return None
    k = R.choice(["vi", "vi", "sign", "tab"])
    num_, den = E((1, "x"), (a, "")), E((1, "x"), (b, ""))
    if k == "vi":
        return M("Quelle est la valeur interdite de l’expression %s ?" % fr(num_, den), "x = %s" % d(-b), ["x = %s" % d(-a), "x = %s" % d(b), "il n’y en a pas"],
                 "Le dénominateur %s s’annule pour <b>x = %s</b>." % (den, d(-b)))
    if k == "tab":
        r1, r2 = sorted([-a, -b])
        f1 = (E((1, "x"), (-r1, "")), [-1, 1, 1])
        f2 = (E((1, "x"), (-r2, "")), [-1, -1, 1])
        svg = table_svg(d(r1), d(r2), f1, f2)
        return M("<div class='qfig'>%s</div>D’après ce tableau, sur quel intervalle (%s)(%s) est-il négatif ?" % (svg, f1[0], f2[0]), "]%s ; %s[" % (d(r1), d(r2)), ["]−∞ ; %s[" % d(r1), "]%s ; +∞[" % d(r2), "]−∞ ; %s[ ∪ ]%s ; +∞[" % (d(r1), d(r2))],
                 "On lit le signe « − » dans la dernière ligne : <b>]%s ; %s[</b>." % (d(r1), d(r2)))
    r1, r2 = -a, -b
    op = R.choice(["&gt; 0", "⩽ 0"])
    lo, hi = sorted([r1, r2])
    if op == "&gt; 0":
        ans = "S = ]−∞ ; %s[ ∪ ]%s ; +∞[" % (d(lo), d(hi))
    else:
        ans = "S = %s%s ; %s%s" % ("[" if lo == r1 else "]", d(lo), d(hi), "]" if hi == r1 else "[")
    w = ["S = [%s ; %s]" % (d(lo), d(hi)), "S = ]%s ; %s[" % (d(lo), d(hi)) if ans != "S = ]%s ; %s[" % (d(lo), d(hi)) else "S = ]−∞ ; %s]" % d(lo), "S = ]−∞ ; %s] ∪ [%s ; +∞[" % (d(lo), d(hi))]
    return M("Résous %s %s." % (fr(num_, den), op), ans, w, "Même signe qu’un produit, mais %s est une valeur interdite (crochet ouvert) : <b>%s</b>." % (d(r2), ans))


def s5():
    k = R.choice(["carre", "carre", "fact", "benef"])
    if k == "carre":
        a = R.randint(1, 9)
        V = [("(x − %d)² ⩾ 0" % a, "ℝ (pour tout réel x)", ["S = [%d ; +∞[" % a, "S = {%d}" % a, "S = ∅"]),
             ("(x + %d)² &lt; 0" % a, "S = ∅", ["S = ]−∞ ; −%d[" % a, "S = {−%d}" % a, "ℝ (pour tout réel x)"]),
             ("x² + %d &gt; 0" % (a * a), "ℝ (pour tout réel x)", ["S = ]%d ; +∞[" % a, "S = ]−%d ; %d[" % (a, a), "S = ∅"]),
             ("(x − %d)² ⩽ 0" % a, "S = {%d}" % a, ["S = ∅", "S = ]−∞ ; %d]" % a, "ℝ (pour tout réel x)"])]
        q, ans, w = R.choice(V)
        return M("Résous : %s" % q, ans, w, "Un carré est toujours positif ou nul : <b>%s</b>." % ans)
    if k == "fact":
        a = R.randint(1, 9)
        return M("Pour résoudre x² − %d &lt; 0, on factorise. Quelle est la solution ?" % (a * a), "S = ]−%d ; %d[" % (a, a), ["S = ]−∞ ; %d[" % a, "S = ]−∞ ; −%d[ ∪ ]%d ; +∞[" % (a, a), "S = ]−%d ; %d[" % (a * a, a * a)],
                 "x² − %d = (x − %d)(x + %d) : négatif entre les racines : <b>S = ]−%d ; %d[</b>." % (a * a, a, a, a, a))
    a = R.choice([10, 20, 30])
    b = R.choice([2, 3, 4])
    return M("Le bénéfice d’une entreprise est B(x) = (x − %d)(%d − x) (x en centaines d’objets). Pour quelles valeurs de x est-il positif ?" % (b, a), "x ∈ [%d ; %d]" % (b, a), ["x ∈ ]−∞ ; %d] ∪ [%d ; +∞[" % (b, a), "x ⩾ %d" % b, "x ⩽ %d" % a],
             "(x − %d) et (%d − x) sont positifs ensemble entre %d et %d : <b>x ∈ [%d ; %d]</b>." % (b, a, b, a, b, a))


def main():
    seen = set()
    sets = [("Équations produit nul", mix(R, seen, [(s1, 20)])), ("Signe de ax + b", mix(R, seen, [(s2, 20)])),
            ("Inéquations produit", mix(R, seen, [(s3, 20)])), ("Quotients et tableaux de signes", mix(R, seen, [(s4, 20)])), ("Carrés et problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Un produit est nul si et seulement si l’un de ses facteurs est nul. ax + b s’annule en −b/a et a le <b>signe de a à droite</b> de cette valeur.",
              "Pour étudier le signe d’un produit ou d’un quotient, on fait un <b>tableau de signes</b> : une ligne par facteur, puis la règle des signes.",
              "Pour un quotient, la valeur qui annule le dénominateur est <b>interdite</b> (double barre dans le tableau, crochet ouvert)."],
             [("(x − 1)(x + 3) &lt; 0", ["racines −3 et 1", "négatif entre les racines"], "S = ]−3 ; 1[")],
             [["(x − 3)(x + 5) = 0 donne x = −3 ou x = 5", "x − 3 = 0 donne x = 3 ; x + 5 = 0 donne x = −5."], ["−2x + 4 est positif pour x &gt; 2", "a = −2 est négatif : positif pour x &lt; 2."],
              ["Inclure la valeur interdite", "Le dénominateur ne doit jamais être nul : crochet ouvert."]])
    faq = [("Comment trouver le signe de ax + b sans tableau ?", "Il est du signe de a à droite de −b/a, et du signe contraire à gauche."),
           ("Pourquoi ne pas multiplier par le dénominateur ?", "Son signe change selon x : on ne saurait pas s’il faut changer le sens de l’inégalité.")]
    unit("seconde", R, "tableaux-de-signes", "N",
         "Résoudre une équation produit nul ; déterminer le signe d’une expression ax + b ; étudier le signe d’un produit ou d’un quotient de facteurs du premier degré à l’aide d’un tableau de signes ; résoudre des inéquations",
         "Équations produit nul et tableaux de signes", "Tableaux de signes",
         "Fiches de maths seconde sur les tableaux de signes : équation produit nul, signe de ax + b, inéquations produit et quotient, valeurs interdites. 100 exercices corrigés.",
         "Produit nul ⇔ un facteur nul", "ax + b a le signe de a à droite de −b/a", body, faq, sets, 7)


if __name__ == "__main__":
    main()
