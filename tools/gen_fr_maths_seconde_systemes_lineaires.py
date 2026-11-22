# -*- coding: utf-8 -*-
"""
France Maths Seconde : Systèmes de deux équations linéaires à deux inconnues
  python3 tools/gen_fr_maths_seconde_systemes_lineaires.py
Erreurs : substituer sans parenthèses, soustraire les équations en oubliant un signe, inverser x et y dans la réponse, oublier le cas sans solution.
"""
import random
from fr_c4 import *

R = random.Random(60515)
K = Kids(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def E(*t):
    return expr(list(t))


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def sysh(e1, e2):
    return "<span class='sys'>%s<br>%s</span>" % (e1, e2)


def mk(small=False):
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, b, c, e = nz(-5, 5), nz(-5, 5), nz(-5, 5), nz(-5, 5)
    if small:
        b = 1
    if a * e - b * c == 0:
        return None
    return x, y, a, b, c, e


def s1():
    t = mk()
    if not t:
        return None
    x, y, a, b, c, e = t
    k = R.choice(["test", "test", "sol"])
    e1 = "%s = %s" % (E((a, "x"), (b, "y")), d(a * x + b * y))
    e2 = "%s = %s" % (E((c, "x"), (e, "y")), d(c * x + e * y))
    if k == "test":
        tx, ty = R.choice([(x, y), (y, x), (x, y + 1)]) if x != y else R.choice([(x, y), (x + 1, y)])
        ok = a * tx + b * ty == a * x + b * y and c * tx + e * ty == c * x + e * y
        return M("Le couple %s est-il solution du système %s ?" % (co(tx, ty), sysh(e1, e2)), "oui" if ok else "non", ["non" if ok else "oui", "seulement de la première équation" if ok else "oui, il vérifie au moins une équation", "on ne peut pas savoir"],
                 "On remplace dans les deux équations : %s." % ("les deux sont vérifiées, <b>oui</b>" if ok else "une équation n’est pas vérifiée, <b>non</b>"))
    return M("Quelle est la solution du système %s ?" % sysh(e1, e2), co(x, y), [co(y, x) if x != y else co(x, y + 1), co(-x, y) if x else co(1, y), co(x, -y) if y else co(x, 1)],
             "On peut vérifier : %s × %s + %s × %s = %s et %s × %s + %s × %s = %s : <b>%s</b>." % (d(a), par(x), d(b), par(y), d(a * x + b * y), d(c), par(x), d(e), par(y), d(c * x + e * y), co(x, y)))


def s2():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, c, e = nz(-4, 4), nz(-5, 5), nz(-5, 5)
    p = y - a * x
    if c + e * a == 0:
        return None
    e1 = "y = %s" % E((a, "x"), (p, ""))
    e2 = "%s = %s" % (E((c, "x"), (e, "y")), d(c * x + e * y))
    return M("Résous par substitution : %s" % sysh(e1, e2), co(x, y), [co(y, x) if x != y else co(x, y + 1), co(x, a * x - p) if p else co(x, y + 2), co(Fr(c * x + e * y - e * p, c - e * a), y) if c - e * a and Fr(c * x + e * y - e * p, c - e * a) != x else co(x + 1, y)],
             "On remplace y par %s dans la seconde : %s(%s) … = %s, d’où x = %s, puis y = %s : <b>%s</b>." % (E((a, "x"), (p, "")), d(e) if e not in (1, -1) else ("" if e == 1 else MINUS), E((a, "x"), (p, "")), d(c * x + e * y), d(x), d(y), co(x, y)))


def s3():
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    a, b = nz(-5, 5), nz(1, 5)
    c = nz(-5, 5)
    if a == c:
        return None
    s1_, s2_ = a * x + b * y, c * x - b * y
    e1 = "%s = %s" % (E((a, "x"), (b, "y")), d(s1_))
    e2 = "%s = %s" % (E((c, "x"), (-b, "y")), d(s2_))
    if a + c == 0:
        return None
    return M("Résous par combinaison : %s" % sysh(e1, e2), co(x, y), [co(y, x) if x != y else co(x, y + 1), co(Fr(s1_ - s2_, a - c), y) if Fr(s1_ - s2_, a - c) != x else co(x, -y) if y else co(x, 1), co(x, -y) if y else co(x + 2, y)],
             "On additionne les deux équations (les y s’éliminent) : %s = %s, donc x = %s, puis y = %s : <b>%s</b>." % (E((a + c, "x")), d(s1_ + s2_), d(x), d(y), co(x, y)))


def s4():
    k = R.choice(["nb", "nb", "det"])
    a, b = nz(-5, 5), nz(-5, 5)
    kk = R.choice([2, 3, -1, -2])
    c1 = R.randint(-9, 9)
    q = R.choice(["une", "aucune", "infinite"])
    if q == "une":
        c, e = nz(-5, 5), nz(-5, 5)
        if a * e - b * c == 0:
            return None
        c2 = R.randint(-9, 9)
    elif q == "aucune":
        c, e = kk * a, kk * b
        c2 = kk * c1 + R.choice([1, 2, -1])
    else:
        c, e = kk * a, kk * b
        c2 = kk * c1
    e1, e2 = "%s = %s" % (E((a, "x"), (b, "y")), d(c1)), "%s = %s" % (E((c, "x"), (e, "y")), d(c2))
    ans = {"une": "une seule solution", "aucune": "aucune solution", "infinite": "une infinité de solutions"}[q]
    if k == "det":
        D = a * e - b * c
        return M("Calcule le déterminant du système %s. Combien a-t-il de solutions ?" % sysh(e1, e2), "det = %s : %s" % (d(D), "une seule solution" if D else "pas une solution unique"),
                 ["det = %s : %s" % (d(a * e + b * c), "une seule solution" if a * e + b * c else "pas une solution unique") if a * e + b * c != D else "det = %s : une seule solution" % d(D + 1), "det = %s : %s" % (d(-D) if D else "1", "pas une solution unique" if D else "une seule solution"), "det = %s : aucune solution" % d(a * b - c * e) if a * b - c * e != D else "det = 0 : une infinité de solutions"],
                 "det = ab′ − ba′ = %s × %s − %s × %s = %s : %s." % (d(a), par(e), d(b), par(c), d(D), "<b>une seule solution</b>" if D else "<b>pas de solution unique</b> (aucune ou une infinité)"))
    return M("Combien de solutions le système %s a-t-il ?" % sysh(e1, e2), ans, [o for o in ["une seule solution", "aucune solution", "une infinité de solutions", "deux solutions"] if o != ans][:3],
             "%s" % ("Les droites sont sécantes : <b>une seule solution</b>." if q == "une" else "Les droites sont parallèles (coefficients proportionnels) %s : <b>%s</b>." % ("et distinctes" if q == "aucune" else "et confondues", ans)))


def s5():
    p = K.next()
    k = R.choice(["billets", "places", "ages", "melange", "pieces"])
    if k == "billets":
        a, b = R.randint(3, 15), R.randint(3, 15)
        pa, pb = R.choice([(8, 5), (12, 7), (10, 6), (15, 9)])
        return M("Un groupe de %d personnes paie %d € au cinéma. Le tarif adulte est %d €, le tarif enfant %d €. Combien d’adultes y a-t-il ?" % (a + b, pa * a + pb * b, pa, pb), str(a), [str(b), str((pa * a + pb * b) // pa) if (pa * a + pb * b) // pa not in (a, b) else str(a + 1), str((a + b) // 2) if (a + b) // 2 not in (a, b) else str(a + 2)],
                 "x + y = %d et %dx + %dy = %d : <b>%d adultes</b> (et %d enfants)." % (a + b, pa, pb, pa * a + pb * b, a, b))
    if k == "places":
        a, b = R.randint(10, 40), R.randint(10, 40)
        return M("Dans une salle, il y a %d chaises et tabourets. Les chaises ont 4 pieds, les tabourets 3 ; on compte %d pieds. Combien de tabourets ?" % (a + b, 4 * a + 3 * b), str(b), [str(a), str((4 * a + 3 * b) // 3 - (a + b)) if (4 * a + 3 * b) // 3 - (a + b) not in (a, b) else str(b + 1), str((a + b) // 2) if (a + b) // 2 not in (a, b) else str(b + 2)],
                 "x + y = %d et 4x + 3y = %d : <b>%d tabourets</b>." % (a + b, 4 * a + 3 * b, b))
    if k == "ages":
        a, b = R.randint(8, 16), R.randint(30, 45)
        return M("La somme des âges %s et de sa mère est %d ans ; la différence est %d ans. Quel âge a %s ?" % (de_n(p[0]), a + b, b - a, p[0]), "%d ans" % a, ["%d ans" % b, "%s ans" % d(Fr(a + b, 2)), "%d ans" % (b - a)],
                 "x + y = %d et y − x = %d : 2x = %d, <b>x = %d ans</b>." % (a + b, b - a, 2 * a, a))
    if k == "melange":
        x, y = R.randint(2, 8), R.randint(2, 8)
        pa, pb = R.choice([(3, 5), (4, 7), (2, 6)])
        return M("On achète %d kg de fruits (pommes à %d €/kg et poires à %d €/kg) pour %d €. Combien de kg de pommes ?" % (x + y, pa, pb, pa * x + pb * y), "%d kg" % x, ["%d kg" % y, "%s kg" % d(Fr(x + y, 2)) if Fr(x + y, 2) not in (x, y) else "%d kg" % (x + 1), "%d kg" % (x + 2)],
                 "x + y = %d et %dx + %dy = %d : <b>%d kg</b> de pommes." % (x + y, pa, pb, pa * x + pb * y, x))
    a, b = R.randint(3, 15), R.randint(3, 15)
    return M("Une tirelire contient %d pièces de 1 € et de 2 €, pour un total de %d €. Combien y a-t-il de pièces de 2 € ?" % (a + b, a + 2 * b), str(b), [str(a), str((a + 2 * b) // 2) if (a + 2 * b) // 2 not in (a, b) else str(b + 1), str(a + b - 1)],
             "x + y = %d et x + 2y = %d : y = %d − %d = <b>%d</b>." % (a + b, a + 2 * b, a + 2 * b, a + b, b))


def main():
    seen = set()
    sets = [("Tester et vérifier", mix(R, seen, [(s1, 20)])), ("Méthode par substitution", mix(R, seen, [(s2, 20)])),
            ("Méthode par combinaison", mix(R, seen, [(s3, 20)])), ("Nombre de solutions", mix(R, seen, [(s4, 20)])), ("Mettre en système", mix(R, seen, [(s5, 20)]))]
    body = L(["Résoudre un système de deux équations à deux inconnues, c’est trouver les couples (x ; y) qui vérifient <b>les deux</b> équations : c’est le point d’intersection des deux droites.",
              "<b>Substitution</b> : on exprime une inconnue en fonction de l’autre dans une équation et on la remplace dans l’autre. <b>Combinaison</b> : on additionne ou soustrait les équations pour éliminer une inconnue.",
              "Si le déterminant ab′ − ba′ est non nul, il y a une seule solution ; sinon les droites sont parallèles (aucune ou une infinité de solutions)."],
             [("x + y = 10 et x − y = 4", ["on additionne : 2x = 14", "x = 7, puis y = 3"], "(7 ; 3)")],
             [["Remplacer sans parenthèses", "2(3x − 1), pas 2 × 3x − 1."], ["Donner (y ; x)", "Le couple s’écrit (x ; y)."], ["Penser qu’il y a toujours une solution", "Si les droites sont parallèles, il n’y en a pas (ou une infinité)."]])
    faq = [("Quelle méthode choisir ?", "La substitution si une inconnue est déjà isolée (y = …) ; la combinaison si les coefficients s’éliminent facilement."),
           ("Comment vérifier ?", "On remplace x et y dans les deux équations de départ.")]
    unit("seconde", R, "systemes-lineaires", "G",
         "Résoudre un système de deux équations linéaires à deux inconnues par substitution ou combinaison ; interpréter graphiquement comme l’intersection de deux droites ; déterminer le nombre de solutions ; modéliser un problème par un système",
         "Systèmes de deux équations à deux inconnues", "Systèmes d’équations",
         "Fiches de maths seconde sur les systèmes linéaires : vérifier une solution, substitution, combinaison, nombre de solutions et problèmes. 100 exercices corrigés.",
         "Solution = point d’intersection des deux droites", "det ≠ 0 : une seule solution", body, faq, sets, 15)


if __name__ == "__main__":
    main()
