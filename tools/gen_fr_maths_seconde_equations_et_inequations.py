# -*- coding: utf-8 -*-
"""
France Maths Seconde : Équations et inéquations du premier degré, x² = a, opérations sur les inégalités
  python3 tools/gen_fr_maths_seconde_equations_et_inequations.py
Erreurs : garder le sens en multipliant par un négatif, x² = 9 → x = 3 seulement, oublier les valeurs interdites, solution notée avec le mauvais crochet.
"""
import random
from fr_c4 import *

R = random.Random(60506)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def s1():
    a, c = nz(-7, 9), nz(-7, 9)
    if a == c:
        return None
    x = Fr(R.randint(-9, 9), R.choice([1, 1, 1, 2, 3]))
    b = R.randint(-12, 12)
    e = (a - c) * x + b
    if e.denominator != 1:
        return None
    e = int(e)
    S = "S = {%s}" % fq(x)
    return M("Résous : %s = %s" % (E((a, "x"), (b, "")), E((c, "x"), (e, ""))), S,
             ["S = {%s}" % fq(Fr(e - b, a + c)) if a + c and Fr(e - b, a + c) != x else "S = {%s}" % fq(x + 1), "S = {%s}" % fq(Fr(e + b, a - c)) if Fr(e + b, a - c) != x else "S = {%s}" % fq(x - 1), "S = {%s}" % fq(-x) if x else "S = ∅"],
             "%s = %s, donc x = %s ÷ %s : <b>%s</b>." % (E((a - c, "x")), d(e - b), d(e - b), par(a - c), S))


def s2():
    k = R.choice(["x2", "x2", "x2neg", "x2b"])
    if k == "x2":
        n = R.choice([2, 3, 5, 7, 4, 9, 16, 25, 36, 10])
        r = int(n ** 0.5)
        sol = ("−%d ; %d" % (r, r)) if r * r == n else ("−√%d ; √%d" % (n, n))
        return M("Résous : x² = %d" % n, "S = {%s}" % sol, ["S = {%s}" % sol.split(" ; ")[1], "S = {%s}" % d(Fr(n, 2)), "S = ∅"], "x² = a avec a &gt; 0 a deux solutions, −√a et √a : <b>S = {%s}</b>." % sol)
    if k == "x2neg":
        n = R.randint(1, 30)
        return M("Résous : x² = −%d" % n, "S = ∅", ["S = {−√%d}" % n, "S = {−√%d ; √%d}" % (n, n), "S = {−%d}" % n], "Un carré est toujours positif ou nul : <b>S = ∅</b>.")
    a, b = R.randint(2, 5), R.randint(1, 20)
    n = R.randint(1, 8)
    rhs = a * n * n - b
    return M("Résous : %dx² − %d = %s" % (a, b, d(rhs)), "S = {−%d ; %d}" % (n, n), ["S = {%d}" % n, "S = {−%d ; %d}" % (n * n, n * n), "S = ∅"],
             "%dx² = %d, x² = %d : <b>S = {−%d ; %d}</b>." % (a, a * n * n, n * n, n, n))


OPS = {"<": "&lt;", ">": "&gt;", "<=": "⩽", ">=": "⩾"}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}


def sol_int(op, v):
    v = fq(v)
    return {"<": "]−∞ ; %s[" % v, "<=": "]−∞ ; %s]" % v, ">": "]%s ; +∞[" % v, ">=": "[%s ; +∞[" % v}[op]


def s3():
    a, c = nz(-6, 6), nz(-6, 6)
    if a == c:
        return None
    b, e = R.randint(-10, 10), R.randint(-10, 10)
    op = R.choice(list(OPS))
    v = Fr(e - b, a - c)
    rop = op if a - c > 0 else FLIP[op]
    ans = "S = " + sol_int(rop, v)
    return M("Résous : %s %s %s" % (E((a, "x"), (b, "")), OPS[op], E((c, "x"), (e, "")) if c else d(e)), ans,
             ["S = " + sol_int(FLIP[rop], v), "S = " + sol_int(rop, -v) if v else "S = " + sol_int(rop, 1), "S = " + sol_int({"<": "<=", "<=": "<", ">": ">=", ">=": ">"}[rop], v)],
             "%s %s %s, puis on divise par %s%s : <b>%s</b>." % (E((a - c, "x")), OPS[op], d(e - b), par(a - c), " (négatif : on change le sens)" if a - c < 0 else "", ans))


def s4():
    k = R.choice(["mult", "mult", "add", "inv"])
    a, b = R.randint(-9, 9), R.randint(-9, 9)
    if a == b:
        return None
    lo, hi = min(a, b), max(a, b)
    if k == "mult":
        m = nz(-5, 5)
        if m in (1, -1):
            return None
        l2, h2 = sorted([lo * m, hi * m])
        mx = E((m, "x"))
        return M("On sait que %s &lt; x &lt; %s. Encadre %s." % (d(lo), d(hi), mx), "%s &lt; %s &lt; %s" % (d(l2), mx, d(h2)), ["%s &lt; %s &lt; %s" % (d(lo * m), mx, d(hi * m)) if m < 0 else "%s &lt; %s &lt; %s" % (d(lo + m), mx, d(hi + m)), "%s &lt; %s &lt; %s" % (d(-h2), mx, d(-l2)) if (-h2, -l2) != (l2, h2) else "%s &lt; %s &lt; %s" % (d(l2 - 1), mx, d(h2 + 1)), "%s &lt; %s &lt; %s" % (d(lo), mx, d(hi))],
                 "On multiplie par %s%s : <b>%s &lt; %s &lt; %s</b>." % (par(m), " (négatif : on change le sens)" if m < 0 else "", d(l2), mx, d(h2)))
    if k == "add":
        c = nz(-8, 8)
        return M("On sait que %s ⩽ x ⩽ %s. Encadre x %s %d." % (d(lo), d(hi), "+" if c > 0 else MINUS, abs(c)), "%s ⩽ x %s %d ⩽ %s" % (d(lo + c), "+" if c > 0 else MINUS, abs(c), d(hi + c)),
                 ["%s ⩽ x %s %d ⩽ %s" % (d(lo - c), "+" if c > 0 else MINUS, abs(c), d(hi - c)), "%s ⩽ x %s %d ⩽ %s" % (d(hi + c), "+" if c > 0 else MINUS, abs(c), d(lo + c)), "%s ⩽ x %s %d ⩽ %s" % (d(lo * c), "+" if c > 0 else MINUS, abs(c), d(hi * c)) if lo * c < hi * c else "%s ⩽ x %s %d ⩽ %s" % (d(lo), "+" if c > 0 else MINUS, abs(c), d(hi))],
                 "On ajoute %s aux trois membres : <b>%s ⩽ x %s %d ⩽ %s</b>." % (par(c), d(lo + c), "+" if c > 0 else MINUS, abs(c), d(hi + c)))
    lo, hi = R.randint(1, 5), R.randint(6, 10)
    return M("On sait que %d ⩽ x ⩽ %d. Encadre %s." % (lo, hi, fr(1, "x")), "%s ⩽ %s ⩽ %s" % (fr(1, hi), fr(1, "x"), fr(1, lo)), ["%s ⩽ %s ⩽ %s" % (fr(1, lo), fr(1, "x"), fr(1, hi)), "%d ⩽ %s ⩽ %d" % (lo, fr(1, "x"), hi), "−%d ⩽ %s ⩽ −%d" % (hi, fr(1, "x"), lo)],
             "La fonction inverse est décroissante sur ]0 ; +∞[ : l’ordre change : <b>%s ⩽ %s ⩽ %s</b>." % (fr(1, hi), fr(1, "x"), fr(1, lo)))


def s5():
    p = K.next()
    k = R.choice(["forfait", "moyenne", "rect", "age", "budget"])
    if k == "forfait":
        a, b, c = R.randint(2, 6), R.randint(10, 40), R.randint(7, 12)
        if c <= a:
            return None
        n = Fr(b, c - a)
        m = int(n) + 1
        return M("Abonnement : %d € + %d € par séance. Sans abonnement : %d € par séance. À partir de combien de séances l’abonnement est-il strictement plus avantageux ?" % (b, a, c), pl(m, "séance"), [pl(int(n), "séance") if int(n) != m and int(n) > 0 else pl(m + 1, "séance"), pl(b // c if b // c not in (m, int(n)) else m + 2, "séance"), pl(b, "séance")],
                 "%d + %dx &lt; %dx ⇔ x &gt; %s : <b>%s</b>." % (b, a, c, fq(n), pl(m, "séance")))
    if k == "moyenne":
        n1, n2 = R.randint(7, 14), R.randint(7, 14)
        t = R.randint(10, 13)
        need = 3 * t - n1 - n2
        if not 0 < need <= 20:
            return None
        return M("%s a eu %d et %d. Quelle note minimale lui faut-il au troisième devoir pour avoir au moins %d de moyenne ?" % (p[0], n1, n2, t), str(need), [str(t), str(need + 1), str(need - 1)],
                 "(%d + %d + x) ÷ 3 ⩾ %d ⇔ x ⩾ %d : <b>%d</b>." % (n1, n2, t, need, need))
    if k == "rect":
        a = R.randint(2, 9)
        P = R.randint(20, 60)
        lmax = Fr(P - 2 * a, 4)
        return M("Un rectangle a une longueur égale à sa largeur ℓ + %d. Son périmètre doit être au plus %d cm. Quelles valeurs peut prendre ℓ ?" % (a, P), "0 &lt; ℓ ⩽ %s" % fq(lmax), ["0 &lt; ℓ ⩽ %s" % fq(Fr(P - a, 4)), "0 &lt; ℓ ⩽ %s" % fq(Fr(P, 4)), "ℓ ⩾ %s" % fq(lmax)],
                 "2(ℓ + ℓ + %d) ⩽ %d ⇔ 4ℓ ⩽ %d ⇔ ℓ ⩽ %s : <b>0 &lt; ℓ ⩽ %s</b>." % (a, P, P - 2 * a, fq(lmax), fq(lmax)))
    if k == "age":
        a, f = R.randint(10, 16), R.randint(36, 50)
        t = f - 3 * a
        if t <= 0 or t % 2:
            return None
        x = t // 2
        return M("%s a %d ans et sa mère %d ans. Dans combien d’années la mère aura-t-elle trois fois l’âge %s ?" % (p[0], a, f, de_n(p[0])), pl(x, "an"), [pl(t, "an"), pl(Fr(f, 3) - a, "an") if (Fr(f, 3) - a) > 0 and (Fr(f, 3) - a).denominator == 1 else pl(x + 1, "an"), pl(x + 2, "an")],
                 "%d + x = 3(%d + x) ⇔ 2x = %d ⇔ x = <b>%s</b>." % (f, a, t, pl(x, "an")))
    bud, pu = R.choice([50, 80, 100]), R.choice([3, 4, 6, 7])
    fra = R.randint(5, 12)
    n = (bud - fra) // pu
    return M("%s a %d €. Livraison : %d € ; chaque livre coûte %d €. Combien de livres peut-%s acheter au maximum ?" % (p[0], bud, fra, pu, p[1]), str(n), [str(bud // pu), str(n + 1), str((bud + fra) // pu) if (bud + fra) // pu != n + 1 else str(n - 1)],
             "%d + %dx ⩽ %d ⇔ x ⩽ %s : <b>%d</b>." % (fra, pu, bud, fq(Fr(bud - fra, pu)), n))


def main():
    seen = set()
    sets = [("Équations du premier degré", mix(R, seen, [(s1, 20)])), ("Équations x² = a", mix(R, seen, [(s2, 20)])),
            ("Inéquations du premier degré", mix(R, seen, [(s3, 20)])), ("Opérations sur les inégalités", mix(R, seen, [(s4, 20)])), ("Modéliser par une équation ou une inéquation", mix(R, seen, [(s5, 20)]))]
    body = L(["On peut ajouter ou soustraire un même nombre aux deux membres d’une égalité ou d’une inégalité.",
              "On peut multiplier ou diviser par un même nombre non nul ; dans une inégalité, <b>si ce nombre est négatif, on change le sens</b>.",
              "x² = a : deux solutions −√a et √a si a &gt; 0, une seule (0) si a = 0, aucune si a &lt; 0. Les solutions d’une inéquation s’écrivent avec un intervalle."],
             [("−3x + 5 &gt; 11", ["−3x &gt; 6", "x &lt; −2 (on divise par −3)"], "S = ]−∞ ; −2[")],
             [["−2x &lt; 6, donc x &lt; −3", "On divise par −2 : x &gt; −3."], ["x² = 9, donc x = 3", "Aussi x = −3."], ["Écrire S = [−2 ; +∞[ pour x &gt; −2", "−2 est exclu : ]−2 ; +∞[."]])
    faq = [("Comment vérifier ?", "On remplace x par la solution (ou par un nombre de l’intervalle) dans l’énoncé de départ."),
           ("Pourquoi changer le sens ?", "Multiplier par un négatif inverse l’ordre : 2 &lt; 3 mais −2 &gt; −3.")]
    unit("seconde", R, "equations-et-inequations", "N",
         "Résoudre des équations et des inéquations du premier degré ; résoudre une équation x² = a ; utiliser les règles d’addition et de multiplication des inégalités ; modéliser un problème par une équation ou une inéquation",
         "Équations et inéquations", "Équations et inéquations",
         "Fiches de maths seconde sur les équations et inéquations : premier degré, x² = a, opérations sur les inégalités et modélisation. 100 exercices corrigés.",
         "× ou ÷ par un négatif : on change le sens", "x² = a (a > 0) : x = −√a ou x = √a", body, faq, sets, 6)


if __name__ == "__main__":
    main()
