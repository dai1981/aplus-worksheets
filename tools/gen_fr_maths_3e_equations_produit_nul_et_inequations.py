# -*- coding: utf-8 -*-
"""
France Maths 3e : Équations produit nul et inéquations du premier degré
  python3 tools/gen_fr_maths_3e_equations_produit_nul_et_inequations.py
Erreurs : (x − 3)(x + 5) = 0 → x = −3 et x = 5 (signes), ne garder qu’une solution, garder le sens de l’inégalité en divisant par un négatif.
"""
import random
from fr_c4 import *

R = random.Random(60406)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def sol2(a, b):
    a, b = sorted([a, b])
    return "x = %s ou x = %s" % (fq(a), fq(b)) if a != b else "x = %s" % fq(a)


def s1():
    a, b = nz(-9, 9), nz(-9, 9)
    if a == b:
        return None
    q = "(%s)(%s) = 0" % (E((1, "x"), (-a, "")), E((1, "x"), (-b, "")))
    return M("Résous : %s" % q, sol2(a, b), [sol2(-a, -b), "x = %s" % d(a), sol2(a, -b) if a != -b else sol2(a, b + 1)],
             "Un produit est nul si et seulement si l’un de ses facteurs est nul : x %s = 0 ou x %s = 0, donc <b>%s</b>." % (("− %d" % a if a > 0 else "+ %d" % -a), ("− %d" % b if b > 0 else "+ %d" % -b), sol2(a, b)))


def s2():
    a, b = nz(1, 5), nz(-9, 9)
    c, e = nz(1, 5), nz(-9, 9)
    x1, x2 = Fr(-b, a), Fr(-e, c)
    if x1 == x2:
        return None
    k = R.choice(["prod", "prod", "xfois"])
    if k == "xfois":
        q = "x(%s) = 0" % E((c, "x"), (e, ""))
        return M("Résous : %s" % q, sol2(0, x2), ["x = %s" % fq(x2), sol2(0, -x2), sol2(0, Fr(-c, e)) if e else "x = 0"],
                 "x = 0 ou %s = 0 : <b>%s</b>." % (E((c, "x"), (e, "")), sol2(0, x2)))
    q = "(%s)(%s) = 0" % (E((a, "x"), (b, "")), E((c, "x"), (e, "")))
    return M("Résous : %s" % q, sol2(x1, x2), [sol2(-x1, -x2), sol2(Fr(-a, b), Fr(-c, e)) if b and e and Fr(-a, b) != Fr(-c, e) else sol2(x1, -x2), sol2(-b, -e) if (Fr(-b), Fr(-e)) != (x1, x2) and a * c != 1 and -b != -e else sol2(x1 + 1, x2)],
             "%s = 0 donne x = %s ; %s = 0 donne x = %s : <b>%s</b>." % (E((a, "x"), (b, "")), fq(x1), E((c, "x"), (e, "")), fq(x2), sol2(x1, x2)))


def s3():
    k = R.choice(["diff", "fact", "x2x"])
    a = R.randint(2, 12)
    if k == "diff":
        return M("Résous : x² − %d = 0 (on pourra factoriser)." % (a * a), sol2(-a, a), ["x = %d" % a, sol2(-a * a, a * a), "pas de solution"],
                 "x² − %d = (x − %d)(x + %d) = 0 : <b>%s</b>." % (a * a, a, a, sol2(-a, a)))
    if k == "x2x":
        return M("Résous : x² = %dx." % a, sol2(0, a), ["x = %d" % a, sol2(-a, a), "x = 0"], "x² − %dx = 0, donc x(x − %d) = 0 : <b>%s</b>. (On ne divise pas par x, qui peut être nul.)" % (a, a, sol2(0, a)))
    b, c = nz(-6, 6), nz(-6, 6)
    m = nz(-5, 6)
    if m == b or m + c == 0:
        return None
    q = "(x %s %d)(x %s %d) + (x %s %d)(%s) = 0" % ("+" if b > 0 else MINUS, abs(b), "+" if m > 0 else MINUS, abs(m), "+" if b > 0 else MINUS, abs(b), E((1, "x"), (c, "")))
    f2 = Fr(-(m + c), 2)
    return M("Résous en factorisant : %s" % q, sol2(-b, f2), [sol2(-b, -m), sol2(b, -f2), "x = %s" % d(-b)],
             "(x %s %d)[(x %s %d) + (%s)] = (x %s %d)(%s) = 0 : <b>%s</b>." % ("+" if b > 0 else MINUS, abs(b), "+" if m > 0 else MINUS, abs(m), E((1, "x"), (c, "")), "+" if b > 0 else MINUS, abs(b), E((2, "x"), (m + c, "")), sol2(-b, f2)))


def ineq_str(op):
    return {"<": "&lt;", ">": "&gt;", "<=": "⩽", ">=": "⩾"}[op]


FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}


def s4():
    a = nz(-6, 6)
    b, c = R.randint(-10, 10), R.randint(-10, 10)
    op = R.choice(["<", ">", "<=", ">="])
    if a in (1,) and R.random() < 0.5:
        return None
    x = Fr(c - b, a)
    rop = op if a > 0 else FLIP[op]
    ans = "x %s %s" % (ineq_str(rop), fq(x))
    return M("Résous l’inéquation %s %s %s." % (E((a, "x"), (b, "")), ineq_str(op), d(c)), ans,
             ["x %s %s" % (ineq_str(FLIP[rop]), fq(x)), "x %s %s" % (ineq_str(rop), fq(Fr(c + b, a))) if Fr(c + b, a) != x else "x %s %s" % (ineq_str(rop), fq(x + 1)), "x %s %s" % (ineq_str(op), fq(x)) if op != rop else "x %s %s" % (ineq_str(rop), fq(-x)) if x else "x %s 1" % ineq_str(rop)],
             "%s %s %s, puis on divise par %s%s : <b>%s</b>." % (E((a, "x")), ineq_str(op), d(c - b), par(a), " (négatif : on change le sens)" if a < 0 else "", ans))


def s4b():
    a = R.choice([2, 3, 4, 5])
    b = R.randint(-6, 8)
    k = R.choice(["test", "droite"])
    t = R.randint(-4, 6)
    if k == "test":
        ok = a * t + b < 3 * a
        return M("Le nombre %s est-il solution de l’inéquation %s &lt; %d ?" % (d(t), E((a, "x"), (b, "")), 3 * a), "oui" if ok else "non", ["non" if ok else "oui", "seulement s’il est positif", "on ne peut pas savoir"],
                 "%d × %s %s %d = %s, %s %d : <b>%s</b>." % (a, par(t), "+" if b >= 0 else MINUS, abs(b), d(a * t + b), "&lt;" if ok else "⩾", 3 * a, "oui" if ok else "non"))
    v = R.randint(-5, 5)
    op = R.choice(["<", ">", "<=", ">="])
    sens = {"<": "strictement inférieurs à", ">": "strictement supérieurs à", "<=": "inférieurs ou égaux à", ">=": "supérieurs ou égaux à"}[op]
    brack = "crochet ouvert (point exclu)" if op in ("<", ">") else "crochet fermé (point inclus)"
    return M("On représente les solutions de x %s %s sur une droite graduée. Comment ?" % (ineq_str(op), d(v)), "les nombres %s %s, avec un %s en %s" % (sens, d(v), brack, d(v)),
             ["les nombres %s %s, avec un %s en %s" % ({"<": "strictement supérieurs à", ">": "strictement inférieurs à", "<=": "supérieurs ou égaux à", ">=": "inférieurs ou égaux à"}[op], d(v), brack, d(v)),
              "les nombres %s %s, avec un %s en %s" % (sens, d(v), "crochet fermé (point inclus)" if op in ("<", ">") else "crochet ouvert (point exclu)", d(v)), "seulement le point %s" % d(v)],
             "x %s %s : <b>les nombres %s %s</b>, %s." % (ineq_str(op), d(v), sens, d(v), brack))


def s5():
    p = K.next()
    k = R.choice(["forfait", "notes", "rect", "budget"])
    if k == "forfait":
        a, b, c = R.randint(15, 30), R.randint(2, 5), R.randint(5, 9)
        if c <= b:
            return None
        n = Fr(a, c - b)
        mn = int(n) + 1
        return M("Forfait A : %d € par mois + %d € par place de cinéma. Forfait B : %d € par place. À partir de combien de places le forfait A est-il strictement moins cher ?" % (a, b, c), pl(mn, "place"), [pl(int(n), "place") if int(n) != mn and int(n) > 0 else pl(mn + 1, "place"), pl(a // c, "place") if a // c not in (mn, int(n)) else pl(mn + 2, "place"), pl(a, "place")],
                 "%d + %dx &lt; %dx ⇔ %d &lt; %dx ⇔ x &gt; %s : <b>%s</b>." % (a, b, c, a, c - b, fq(n), pl(mn, "place")))
    if k == "notes":
        n1, n2 = R.randint(8, 14), R.randint(8, 14)
        t = R.randint(11, 13)
        need = 3 * t - n1 - n2
        if not 0 < need <= 20:
            return None
        return M("%s a eu %d et %d. Quelle note minimale lui faut-il au troisième contrôle pour avoir au moins %d de moyenne ?" % (p[0], n1, n2, t), str(need), [str(t), str(need + 1), str(2 * t - n1 - n2) if 2 * t - n1 - n2 > 0 and 2 * t - n1 - n2 != need else str(need - 1)],
                 "(%d + %d + x) ÷ 3 ⩾ %d ⇔ x ⩾ %d : <b>%d</b>." % (n1, n2, t, need, need))
    if k == "rect":
        a = R.randint(2, 9)
        return M("Résous x(x + %d) = 0. Quelle solution convient pour une longueur x ?" % a, "aucune : x = 0 ou x = −%d, et une longueur est strictement positive" % a,
                 ["x = %d" % a, "x = 0", "x = −%d" % a], "Les solutions sont 0 et −%d : <b>aucune ne convient</b> pour une longueur." % a)
    b = R.choice([50, 60, 80, 100])
    pu = R.choice([3, 4, 6, 7, 9])
    fr_ = R.randint(5, 15)
    n = (b - fr_) // pu
    return M("%s a %d €. Les frais de livraison sont %d € et chaque livre coûte %d €. Combien de livres peut-%s acheter au maximum ?" % (p[0], b, fr_, pu, p[1]), str(n), [str(b // pu), str(n + 1), str((b + fr_) // pu) if (b + fr_) // pu != n + 1 else str(n - 1)],
             "%d + %dx ⩽ %d ⇔ x ⩽ %s : <b>%d</b> livres au maximum." % (fr_, pu, b, fq(Fr(b - fr_, pu)), n))


def main():
    seen = set()
    sets = [("Équation produit nul", mix(R, seen, [(s1, 20)])), ("Produits de facteurs du premier degré", mix(R, seen, [(s2, 20)])),
            ("Factoriser pour résoudre", mix(R, seen, [(s3, 20)])), ("Inéquations", mix(R, seen, [(s4, 12), (s4b, 8)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Un produit est nul si et seulement si l’un de ses facteurs est nul</b> : (x − 3)(x + 5) = 0 ⇔ x = 3 ou x = −5.",
              "Pour une équation de degré 2, on se ramène à « … = 0 », on factorise, puis on utilise la propriété du produit nul.",
              "Inéquation : on ajoute ou on soustrait comme pour une équation ; si on <b>multiplie ou divise par un nombre négatif, on change le sens</b> de l’inégalité."],
             [("(2x − 6)(x + 4) = 0", ["2x − 6 = 0 ou x + 4 = 0"], "x = 3 ou x = −4"), ("−3x + 2 &lt; 11", ["−3x &lt; 9", "x &gt; −3 (on divise par −3)"], "x &gt; −3")],
             [["(x − 3)(x + 5) = 0 donne x = −3 ou x = 5", "x − 3 = 0 donne x = 3, x + 5 = 0 donne x = −5."], ["x² = 4x, donc x = 4", "On ne divise pas par x : x(x − 4) = 0, x = 0 ou x = 4."],
              ["−2x &lt; 6, donc x &lt; −3", "On divise par −2 : x &gt; −3."]])
    faq = [("Pourquoi « ou » et pas « et » ?", "Il suffit qu’un seul facteur soit nul pour que le produit soit nul : les deux valeurs sont solutions, chacune séparément."),
           ("Comment écrire les solutions d’une inéquation ?", "Par une inégalité (x &gt; −3) et sur une droite graduée, avec un crochet tourné vers l’intérieur si la borne est incluse.")]
    unit("3e", R, "equations-produit-nul-et-inequations", "A",
         "Résoudre une équation produit nul ; se ramener à une équation produit nul par factorisation ; résoudre une inéquation du premier degré et représenter ses solutions ; modéliser un problème par une équation ou une inéquation",
         "Équations produit nul et inéquations", "Équation produit nul et inéquations",
         "Fiches de maths 3e sur les équations produit nul et les inéquations : (ax + b)(cx + d) = 0, factoriser pour résoudre, inéquations et problèmes. 100 exercices corrigés.",
         "Produit nul ⇔ un des facteurs est nul", "× ou ÷ par un négatif : on change le sens", body, faq, sets, 6)


if __name__ == "__main__":
    main()
