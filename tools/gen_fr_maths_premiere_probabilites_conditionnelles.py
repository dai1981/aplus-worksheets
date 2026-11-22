# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Probabilités conditionnelles (définition, tableaux croisés, arbres pondérés, P(A ∩ B) = P(A) × P_A(B), inverser le conditionnement)
  python3 tools/gen_fr_maths_premiere_probabilites_conditionnelles.py
Erreurs : confondre P_A(B) et P_B(A), diviser par l’effectif total, additionner le long d’une branche, oublier que les branches issues d’un nœud ont pour somme 1.
"""
import random
from fr_ly1 import *

R = random.Random(60620)


def P_(a, b):
    return "P<sub>%s</sub>(%s)" % (a, b)


def s1():
    k = R.choice(["def", "def", "inter", "pa"])
    pa = Fr(R.randint(2, 8), 10)
    pba = Fr(R.randint(1, 9), 10)
    inter = pa * pba
    if k == "def":
        return M("P(A) = %s et P(A ∩ B) = %s. Calcule %s." % (d(pa), d(inter), P_("A", "B")), d(pba), [d(inter * pa) , d(pa - inter), d(inter / (1 - pa)) if inter / (1 - pa) <= 1 and (inter / (1 - pa)).denominator in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100, 1000) else d(inter + pa) if inter + pa <= 1 else "1", d(inter)],
                 "%s = P(A ∩ B) ÷ P(A) = %s ÷ %s = <b>%s</b>." % (P_("A", "B"), d(inter), d(pa), d(pba)))
    if k == "inter":
        return M("P(A) = %s et %s = %s. Calcule P(A ∩ B)." % (d(pa), P_("A", "B"), d(pba)), d(inter), [d(pa + pba) if pa + pba <= 1 else d(pa), d(pba / pa) if (pba / pa) <= 1 and (pba / pa).denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100) else d(pba), d(pa * (1 - pba))],
                 "P(A ∩ B) = P(A) × %s = %s × %s = <b>%s</b>." % (P_("A", "B"), d(pa), d(pba), d(inter)))
    return M("%s = %s et P(A ∩ B) = %s. Calcule P(A)." % (P_("A", "B"), d(pba), d(inter)), d(pa), [d(inter * pba), d(pba - inter) if pba > inter else d(1 - pba), d(1 - pa), d(pba + inter) if pba + inter <= 1 else d(inter)],
             "P(A) = P(A ∩ B) ÷ %s = %s ÷ %s = <b>%s</b>." % (P_("A", "B"), d(inter), d(pba), d(pa)))


def tab():
    a, b, c, e = [R.randint(5, 60) for _ in range(4)]
    labs = R.choice([(("Filles", "Garçons"), ("Demi-pension", "Externat")), (("Seconde", "Première"), ("Option latin", "Sans latin")), (("Vaccinés", "Non vaccinés"), ("Malades", "Non malades")),
                     (("Matin", "Soir"), ("En retard", "À l’heure")), (("Produit A", "Produit B"), ("Défectueux", "Conforme"))])
    (r1, r2), (c1, c2) = labs
    tb = table(["", c1, c2, "Total"], [[r1, str(a), str(b), str(a + b)], [r2, str(c), str(e), str(c + e)], ["Total", str(a + c), str(b + e), str(a + b + c + e)]])
    return tb, (a, b, c, e), (r1, r2, c1, c2)


def s2():
    tb, (a, b, c, e), (r1, r2, c1, c2) = tab()
    n = a + b + c + e
    k = R.choice(["l", "c", "l2", "c2"])
    if k == "l":
        return M("%s<br>On choisit une personne au hasard. Calcule P<sub>« %s »</sub>(« %s »)." % (tb, r1, c1), fq(Fr(a, a + b)), [fq(Fr(a, a + c)), fq(Fr(a, n)), fq(Fr(a + b, n))],
                 "Parmi les %d personnes « %s », %d sont « %s » : <b>%s</b>." % (a + b, r1, a, c1, fq(Fr(a, a + b))))
    if k == "c":
        return M("%s<br>On choisit une personne au hasard. Calcule P<sub>« %s »</sub>(« %s »)." % (tb, c1, r1), fq(Fr(a, a + c)), [fq(Fr(a, a + b)), fq(Fr(a, n)), fq(Fr(a + c, n))],
                 "Parmi les %d personnes « %s », %d sont « %s » : <b>%s</b>." % (a + c, c1, a, r1, fq(Fr(a, a + c))))
    if k == "l2":
        return M("%s<br>On choisit une personne au hasard. Calcule P<sub>« %s »</sub>(« %s »)." % (tb, r2, c2), fq(Fr(e, c + e)), [fq(Fr(e, b + e)), fq(Fr(e, n)), fq(Fr(c, c + e))],
                 "Parmi les %d personnes « %s », %d sont « %s » : <b>%s</b>." % (c + e, r2, e, c2, fq(Fr(e, c + e))))
    return M("%s<br>On choisit une personne au hasard. Calcule P(« %s » ∩ « %s »)." % (tb, r2, c1), fq(Fr(c, n)), [fq(Fr(c, c + e)), fq(Fr(c, a + c)), fq(Fr((c + e) * (a + c), n * n)) if Fr((c + e) * (a + c), n * n) != Fr(c, n) else fq(Fr(c + 1, n))],
             "Case « %s / %s » ÷ total : %d ÷ %d = <b>%s</b>." % (r2, c1, c, n, fq(Fr(c, n))))


def s3():
    pa = Fr(R.randint(1, 9), 10)
    pba, pbna = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    svg = arbre(pa, pba, pbna)
    k = R.choice(["chemin", "chemin2", "branche", "pbar"])
    if k == "chemin":
        return M("<div class='qfig'>%s</div>Calcule P(A ∩ B)." % svg, d(pa * pba), [d(pa + pba) if pa + pba <= 1 else d(pba), d(pba), d(pa * pbna)],
                 "On multiplie les probabilités le long du chemin A → B : %s × %s = <b>%s</b>." % (d(pa), d(pba), d(pa * pba)))
    if k == "chemin2":
        return M("<div class='qfig'>%s</div>Calcule P(Ā ∩ B̄)." % svg, d((1 - pa) * (1 - pbna)), [d((1 - pa) + (1 - pbna)) if (1 - pa) + (1 - pbna) <= 1 else d(1 - pbna), d((1 - pa) * pbna), d(1 - pa * pba)],
                 "Chemin Ā → B̄ : %s × %s = <b>%s</b>." % (d(1 - pa), d(1 - pbna), d((1 - pa) * (1 - pbna))))
    if k == "branche":
        return M("<div class='qfig'>%s</div>Lis %s sur l’arbre." % (svg, P_("Ā", "B")), d(pbna), [d(pba) if pba != pbna else d(1 - pbna), d(1 - pa), d((1 - pa) * pbna)],
                 "C’est la probabilité portée par la branche Ā → B : <b>%s</b>." % d(pbna))
    return M("Dans un arbre pondéré, %s = %s. Que vaut %s ?" % (P_("A", "B"), d(pba), P_("A", "B̄")), d(1 - pba), [d(pba), d(1 - pa) if 1 - pa != 1 - pba else d(pa), "1"],
             "Les branches issues du nœud A ont pour somme 1 : 1 − %s = <b>%s</b>." % (d(pba), d(1 - pba)))


def s4():
    pa = Fr(R.randint(1, 9), 10)
    pba, pbna = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
    pb = pa * pba + (1 - pa) * pbna
    k = R.choice(["inv", "inv", "dist"])
    if k == "inv":
        v = pa * pba / pb
        ans = fq(v) if v.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100) else d(v)
        return M("<div class='qfig'>%s</div>P(B) = %s. Calcule %s." % (arbre(pa, pba, pbna), d(pb), P_("B", "A")), ans,
                 [d(pba), d(pa * pba), fq(pa * pba / (1 - pb)) if pa * pba < 1 - pb else d(pa)],
                 "%s = P(A ∩ B) ÷ P(B) = %s ÷ %s = <b>%s</b> (différent de %s = %s)." % (P_("B", "A"), d(pa * pba), d(pb), ans, P_("A", "B"), d(pba)))
    return M("%s se lit…" % P_("B", "A"), "probabilité de A sachant B", ["probabilité de B sachant A", "probabilité de A et B", "probabilité de B ou A"],
             "%s est la probabilité de A <b>sachant que B est réalisé</b>." % P_("B", "A")) if R.random() < 0.2 else None


def s5():
    k = R.choice(["test", "test", "urne", "usine", "eleves"])
    if k == "test":
        p = R.choice([Fr(1, 100), Fr(2, 100), Fr(5, 100), Fr(1, 10)])
        se = R.choice([Fr(9, 10), Fr(95, 100), Fr(99, 100)])
        fp_ = R.choice([Fr(2, 100), Fr(5, 100), Fr(1, 100)])
        pt = p * se + (1 - p) * fp_
        v = p * se / pt
        return M("Une maladie touche %s %% de la population. Un test est positif pour %s %% des malades et pour %s %% des non-malades. Une personne a un test positif. Quelle est la probabilité qu’elle soit malade (arrondie à 0,01) ?" % (d(p * 100), d(se * 100), d(fp_ * 100)),
                 dk(v, 2), [dk(se, 2), dk(p * se, 2) if dk(p * se, 2) != dk(v, 2) else dk(1 - v, 2), dk(1 - fp_, 2)],
                 "P(T) = %s × %s + %s × %s = %s ; P<sub>T</sub>(M) = %s ÷ %s ≈ <b>%s</b>." % (d(p), d(se), d(1 - p), d(fp_), d(pt), d(p * se), d(pt), dk(v, 2)))
    if k == "urne":
        r, b = R.randint(2, 7), R.randint(2, 7)
        n = r + b
        v = Fr(r, n) * Fr(r - 1, n - 1)
        return M("Une urne contient %d boules rouges et %d bleues. On tire deux boules sans remise. Quelle est la probabilité de tirer deux rouges ?" % (r, b), fq(v), [fq(Fr(r * r, n * n)), fq(Fr(r, n) * Fr(r - 1, n)), fq(Fr(r, n) + Fr(r - 1, n - 1)) if Fr(r, n) + Fr(r - 1, n - 1) <= 1 else fq(Fr(r - 1, n - 1))],
                 "Sans remise : %s × %s = <b>%s</b> (la deuxième probabilité est conditionnelle au premier tirage)." % (fq(Fr(r, n)), fq(Fr(r - 1, n - 1)), fq(v)))
    if k == "usine":
        pa = R.choice([Fr(6, 10), Fr(7, 10), Fr(4, 10)])
        da, db = R.choice([Fr(2, 100), Fr(3, 100), Fr(1, 100)]), R.choice([Fr(4, 100), Fr(5, 100), Fr(6, 100)])
        return M("Une usine a deux machines. A fabrique %s %% des pièces, dont %s %% sont défectueuses ; B fabrique le reste, dont %s %% sont défectueuses. Quelle est la probabilité qu’une pièce soit fabriquée par A et défectueuse ?" % (d(pa * 100), d(da * 100), d(db * 100)),
                 d(pa * da), [d(da), d(pa * da + (1 - pa) * db), d(pa + da)], "P(A ∩ D) = P(A) × P<sub>A</sub>(D) = %s × %s = <b>%s</b>." % (d(pa), d(da), d(pa * da)))
    n = R.choice([20, 25, 30, 32, 35])
    f = R.randint(8, n - 8)
    fl = R.randint(2, f - 2)
    g = n - f
    gl = R.randint(1, g - 1)
    return M("Une classe de %d élèves compte %d filles. %d filles et %d garçons font du latin. On choisit un élève qui fait du latin. Quelle est la probabilité que ce soit une fille ?" % (n, f, fl, gl), fq(Fr(fl, fl + gl)),
             [fq(Fr(fl, f)), fq(Fr(fl, n)), fq(Fr(f, n))], "On se restreint aux %d latinistes : %d ÷ %d = <b>%s</b>." % (fl + gl, fl, fl + gl, fq(Fr(fl, fl + gl))))


def main():
    seen = set()
    sets = [("Définition", mix(R, seen, [(s1, 20)])), ("Tableaux croisés", mix(R, seen, [(s2, 20)])),
            ("Arbres pondérés", mix(R, seen, [(s3, 20)])), ("Inverser le conditionnement", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Si P(A) ≠ 0, la <b>probabilité de B sachant A</b> est P<sub>A</sub>(B) = P(A ∩ B) ÷ P(A). Donc P(A ∩ B) = P(A) × P<sub>A</sub>(B).",
              "Dans un tableau croisé, P<sub>A</sub>(B) = effectif de A ∩ B ÷ effectif de A (on divise par l’effectif de la condition).",
              "Dans un arbre pondéré : on <b>multiplie</b> le long d’un chemin ; les branches issues d’un même nœud ont pour somme 1.",
              "P<sub>B</sub>(A) n’est pas P<sub>A</sub>(B) : P<sub>B</sub>(A) = P(A ∩ B) ÷ P(B)."],
             [("P(A) = 0,3, P<sub>A</sub>(B) = 0,6, P<sub>Ā</sub>(B) = 0,2", ["P(A ∩ B) = 0,3 × 0,6 = 0,18", "P(B) = 0,18 + 0,7 × 0,2 = 0,32"], "P<sub>B</sub>(A) = 0,18 ÷ 0,32 = 0,5625")],
             [["P<sub>A</sub>(B) = effectif de A ∩ B ÷ effectif total", "On divise par l’effectif de A."], ["P(A ∩ B) = P(A) + P<sub>A</sub>(B)", "On multiplie le long du chemin."], ["P<sub>A</sub>(B) = P<sub>B</sub>(A)", "En général, ces deux nombres sont différents."]])
    faq = [("Quelle différence entre P(A ∩ B) et P<sub>A</sub>(B) ?", "P(A ∩ B) se calcule sur toute la population ; P<sub>A</sub>(B) seulement parmi les issues où A est réalisé."),
           ("Pourquoi un test positif ne veut-il pas dire « malade » à coup sûr ?", "Parce que P<sub>T</sub>(M) dépend aussi de la rareté de la maladie : s’il y a peu de malades, beaucoup de tests positifs viennent de non-malades.")]
    unit("premiere", R, "probabilites-conditionnelles", "S",
         "Probabilité conditionnelle d’un événement B sachant un événement A de probabilité non nulle, notée P<sub>A</sub>(B) ; P(A ∩ B) = P(A) × P<sub>A</sub>(B) ; tableaux croisés et arbres pondérés ; distinguer P<sub>A</sub>(B) et P<sub>B</sub>(A)",
         "Probabilités conditionnelles et arbres pondérés", "Probabilités conditionnelles",
         "Fiches de maths première sur les probabilités conditionnelles : définition, tableaux croisés, arbres pondérés, inverser le conditionnement et problèmes. 100 exercices corrigés.",
         "Probabilité de B sachant A = P(A ∩ B) ÷ P(A)", "Arbre : on multiplie le long d’un chemin", body, faq, sets, 20)


if __name__ == "__main__":
    main()
