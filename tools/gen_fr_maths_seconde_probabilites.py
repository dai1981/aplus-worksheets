# -*- coding: utf-8 -*-
"""
France Maths Seconde : Probabilités (événements, réunion et intersection, tableaux croisés, fréquences conditionnelles, probabilités conditionnelles, arbres)
  python3 tools/gen_fr_maths_seconde_probabilites.py
Erreurs : P(A ∪ B) = P(A) + P(B) sans retirer P(A ∩ B), confondre P_A(B) et P_B(A), diviser par l’effectif total au lieu de l’effectif de A.
"""
import random
from fr_c4 import *

R = random.Random(60519)
K = Kids(R)


def s1():
    k = R.choice(["union", "union", "inter", "contr"])
    pa, pb = Fr(R.randint(2, 7), 10), Fr(R.randint(2, 7), 10)
    pab = Fr(R.randint(1, min(int(pa * 10), int(pb * 10)) - 0), 10)
    if pab >= min(pa, pb) or pa + pb - pab > 1:
        return None
    if k == "union":
        r = pa + pb - pab
        return M("P(A) = %s, P(B) = %s et P(A ∩ B) = %s. Calcule P(A ∪ B)." % (d(pa), d(pb), d(pab)), d(r), [d(pa + pb), d(pa * pb), d(pa + pb + pab) if pa + pb + pab <= 1 else d(r - Fr(1, 10))],
                 "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = <b>%s</b>." % d(r))
    if k == "inter":
        u = pa + pb - pab
        return M("P(A) = %s, P(B) = %s et P(A ∪ B) = %s. Calcule P(A ∩ B)." % (d(pa), d(pb), d(u)), d(pab), [d(pa * pb) if pa * pb != pab else d(pab + Fr(1, 10)), d(pa + pb - u + Fr(1, 10)), d(u - pa)],
                 "P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = <b>%s</b>." % d(pab))
    return M("P(A) = %s. Que vaut P(Ā) (événement contraire) ?" % d(pa), d(1 - pa), [d(pa), d(-pa), d(1 + pa)], "P(Ā) = 1 − P(A) = <b>%s</b>." % d(1 - pa))


def tab():
    a, b, c, e = [R.randint(5, 40) for _ in range(4)]
    labs = R.choice([(("Filles", "Garçons"), ("Sport", "Pas de sport")), (("Interne", "Externe"), ("Seconde", "Première")), (("Vélo", "Bus"), ("Moins de 3 km", "Plus de 3 km"))])
    (r1, r2), (c1, c2) = labs
    tb = table(["", c1, c2, "Total"], [[r1, str(a), str(b), str(a + b)], [r2, str(c), str(e), str(c + e)], ["Total", str(a + c), str(b + e), str(a + b + c + e)]])
    return tb, (a, b, c, e), (r1, r2, c1, c2)


def s2():
    tb, (a, b, c, e), (r1, r2, c1, c2) = tab()
    n = a + b + c + e
    k = R.choice(["marg", "cond", "cond", "comp"])
    if k == "marg":
        return M("%s<br>Quelle est la fréquence marginale de « %s » ?" % (tb, c1), fq(Fr(a + c, n)), [fq(Fr(a, n)), fq(Fr(a, a + c)), fq(Fr(a + c, a + b))],
                 "Effectif de « %s » ÷ effectif total = %d ÷ %d = <b>%s</b>." % (c1, a + c, n, fq(Fr(a + c, n))))
    if k == "cond":
        return M("%s<br>Parmi les « %s », quelle est la fréquence de « %s » ?" % (tb, r1, c1), fq(Fr(a, a + b)), [fq(Fr(a, n)), fq(Fr(a, a + c)) if Fr(a, a + c) != Fr(a, a + b) else fq(Fr(b, a + b)), fq(Fr(a + c, n))],
                 "Fréquence conditionnelle : %d ÷ %d = <b>%s</b> (on divise par l’effectif de « %s »)." % (a, a + b, fq(Fr(a, a + b)), r1))
    return M("%s<br>Parmi les « %s », quelle est la fréquence de « %s » ?" % (tb, c2, r2), fq(Fr(e, b + e)), [fq(Fr(e, c + e)) if Fr(e, c + e) != Fr(e, b + e) else fq(Fr(b, b + e)), fq(Fr(e, n)), fq(Fr(b + e, n))],
             "%d ÷ %d = <b>%s</b>." % (e, b + e, fq(Fr(e, b + e))))


def s3():
    tb, (a, b, c, e), (r1, r2, c1, c2) = tab()
    n = a + b + c + e
    k = R.choice(["inter", "union", "pcond"])
    if k == "inter":
        return M("%s<br>On choisit une personne au hasard. Quelle est la probabilité qu’elle soit « %s » et « %s » ?" % (tb, r1, c2), fq(Fr(b, n)), [fq(Fr(b, a + b)), fq(Fr(b, b + e)), fq(Fr(a + b, n) * Fr(b + e, n)) if Fr(a + b, n) * Fr(b + e, n) != Fr(b, n) else fq(Fr(b + 1, n))],
                 "Case « %s / %s » : %d ÷ %d = <b>%s</b>." % (r1, c2, b, n, fq(Fr(b, n))))
    if k == "union":
        u = a + b + c
        return M("%s<br>On choisit une personne au hasard. Quelle est la probabilité qu’elle soit « %s » ou « %s » ?" % (tb, r1, c1), fq(Fr(u, n)), [fq(Fr(a + b + a + c, n)) if a + b + a + c <= n else fq(Fr(a, n)), fq(Fr(a, n)), fq(Fr(u - a, n))],
                 "P(A ∪ B) = (%d + %d − %d) ÷ %d = <b>%s</b>." % (a + b, a + c, a, n, fq(Fr(u, n))))
    return M("%s<br>On choisit une personne au hasard parmi les « %s ». Quelle est la probabilité qu’elle soit « %s » ?" % (tb, c1, r2), fq(Fr(c, a + c)), [fq(Fr(c, c + e)) if Fr(c, c + e) != Fr(c, a + c) else fq(Fr(a, a + c)), fq(Fr(c, n)), fq(Fr(a + c, n))],
             "P<sub>%s</sub>(%s) = %d ÷ %d = <b>%s</b>." % (c1, r2, c, a + c, fq(Fr(c, a + c))))


def s4():
    pa = Fr(R.choice([2, 3, 4, 5, 6, 7]), 10)
    pba = Fr(R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 10)
    pbna = Fr(R.choice([1, 2, 3, 4, 5]), 10)
    k = R.choice(["chemin", "chemin", "branche", "cond"])
    if k == "chemin":
        return M("Sur un arbre pondéré : P(A) = %s et P<sub>A</sub>(B) = %s. Calcule P(A ∩ B)." % (d(pa), d(pba)), d(pa * pba), [d(pa + pba) if pa + pba <= 1 else d(pa * pba + Fr(1, 10)), d(pba), d(pa)],
                 "On multiplie le long du chemin : %s × %s = <b>%s</b>." % (d(pa), d(pba), d(pa * pba)))
    if k == "branche":
        return M("Sur un arbre pondéré, P<sub>A</sub>(B) = %s. Que vaut P<sub>A</sub>(B̄) ?" % d(pba), d(1 - pba), [d(pba), d(1 - pa), d(pa * (1 - pba))],
                 "Les branches issues d’un même nœud ont pour somme 1 : <b>%s</b>." % d(1 - pba))
    inter = pa * pba
    return M("P(A) = %s et P(A ∩ B) = %s. Calcule P<sub>A</sub>(B)." % (d(pa), d(inter)), d(pba), [d(inter * pa) if inter * pa != pba else d(pba + Fr(1, 10)), d(pa - inter) if pa - inter != pba else d(1 - pba), d(inter)],
             "P<sub>A</sub>(B) = P(A ∩ B) ÷ P(A) = %s ÷ %s = <b>%s</b>." % (d(inter), d(pa), d(pba)))


def s5():
    k = R.choice(["test", "dés", "pieces", "confusion"])
    if k == "test":
        p = Fr(R.choice([1, 2, 5]), 100)
        s = Fr(R.choice([90, 95, 99]), 100)
        return M("Une maladie touche %s %% d’une population. Un test est positif pour %s %% des malades. Quelle est la probabilité qu’une personne soit malade et testée positive ?" % (d(p * 100), d(s * 100)), d(p * s), [d(s), d(p), d(p + s - 1) if p + s - 1 > 0 and p + s - 1 != p * s else d(p * (1 - s))],
                 "P(M ∩ T) = P(M) × P<sub>M</sub>(T) = %s × %s = <b>%s</b>." % (d(p), d(s), d(p * s)))
    if k == "dés":
        ev, n_ = R.choice([("une somme égale à 7", 6), ("un double", 6), ("une somme supérieure ou égale à 10", 6), ("deux nombres pairs", 9), ("au moins un 6", 11), ("une somme égale à 4", 3)])
        return M("On lance deux dés équilibrés. Quelle est la probabilité d’obtenir %s ?" % ev, fq(Fr(n_, 36)), [fq(Fr(n_, 12)) if Fr(n_, 12) < 1 else fr(1, 2), fq(Fr(n_ + 1, 36)), fq(Fr(1, 11))], "Tableau à double entrée : %d issues favorables sur 36 : <b>%s</b>." % (n_, fq(Fr(n_, 36))))
    if k == "pieces":
        n_, ev, c = R.choice([(3, "exactement deux « pile »", 3), (3, "au moins un « pile »", 7), (3, "trois « face »", 1), (2, "au moins un « face »", 3)])
        return M("On lance %d fois une pièce équilibrée. Quelle est la probabilité d’obtenir %s ?" % (n_, ev), fq(Fr(c, 2 ** n_)), [fq(Fr(c, 2 * n_)) if Fr(c, 2 * n_) <= 1 else fr(1, 2), fq(Fr(c + 1, 2 ** n_)), fq(Fr(1, 2 ** n_)) if c != 1 else fr(1, 2)],
                 "Il y a 2<sup>%d</sup> = %d issues équiprobables, dont %s : <b>%s</b>." % (n_, 2 ** n_, pl(c, "favorable"), fq(Fr(c, 2 ** n_))))
    V = [("Dans un lycée, P<sub>F</sub>(S) désigne la probabilité…", "qu’un élève fasse du sport sachant que c’est une fille", ["qu’un élève soit une fille sachant qu’il fait du sport", "qu’un élève soit une fille et fasse du sport", "qu’un élève fasse du sport ou soit une fille"]),
         ("P<sub>A</sub>(B) et P<sub>B</sub>(A) sont-elles toujours égales ?", "non, en général elles sont différentes", ["oui, toujours", "oui, si P(A) = 0,5", "elles valent toujours P(A ∩ B)"]),
         ("Sur un arbre pondéré, pour obtenir la probabilité d’un chemin, on…", "multiplie les probabilités des branches", ["additionne les probabilités des branches", "prend la plus grande branche", "divise par le nombre de branches"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Réunion, intersection et contraire", mix(R, seen, [(s1, 20)])), ("Tableaux croisés et fréquences conditionnelles", mix(R, seen, [(s2, 20)])),
            ("Probabilités à partir d’un tableau", mix(R, seen, [(s3, 20)])), ("Arbres pondérés et probabilités conditionnelles", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["P(A ∪ B) = P(A) + P(B) − P(A ∩ B) ; P(Ā) = 1 − P(A).",
              "Dans un tableau croisé, la <b>fréquence conditionnelle</b> de B parmi A est (effectif de A ∩ B) ÷ (effectif de A).",
              "<b>Probabilité conditionnelle</b> : P<sub>A</sub>(B) = P(A ∩ B) ÷ P(A). Sur un arbre, on multiplie le long d’un chemin : P(A ∩ B) = P(A) × P<sub>A</sub>(B)."],
             [("P(A) = 0,4 et P<sub>A</sub>(B) = 0,3", ["P(A ∩ B) = 0,4 × 0,3"], "0,12")],
             [["P(A ∪ B) = P(A) + P(B)", "On retire P(A ∩ B), comptée deux fois."], ["Confondre P<sub>A</sub>(B) et P<sub>B</sub>(A)", "On divise par la probabilité de l’événement « sachant »."],
              ["Diviser par l’effectif total pour une fréquence conditionnelle", "On divise par l’effectif de la sous-population."]])
    faq = [("Que signifie « sachant que » ?", "On se restreint à une partie de la population : on ne compte plus que les individus de A."),
           ("Comment vérifier un arbre ?", "Les branches issues d’un même nœud ont pour somme 1.")]
    unit("seconde", R, "probabilites", "S",
         "Utiliser la réunion, l’intersection et le contraire d’événements ; calculer des fréquences marginales et conditionnelles dans un tableau croisé ; calculer des probabilités, y compris conditionnelles, à l’aide de tableaux et d’arbres pondérés",
         "Probabilités et probabilités conditionnelles", "Probabilités",
         "Fiches de maths seconde sur les probabilités : réunion, intersection, tableaux croisés, fréquences conditionnelles, probabilités conditionnelles et arbres. 100 exercices corrigés.",
         "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "P_A(B) = P(A ∩ B) ÷ P(A)", body, faq, sets, 19)


if __name__ == "__main__":
    main()
