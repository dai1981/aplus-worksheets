# -*- coding: utf-8 -*-
"""
France Maths Seconde : Statistique descriptive (moyenne et linéarité, écart type, données regroupées en classes, comparer des séries)
  python3 tools/gen_fr_maths_seconde_statistiques.py
Erreurs : la moyenne ne change pas quand on ajoute 2 à toutes les valeurs, écart type multiplié par a + b, centre de classe = borne, confondre classe médiane et classe modale.
"""
import random
import math
from fr_c4 import *

R = random.Random(60518)
K = Kids(R)


def mean(v):
    return Fr(sum(v), len(v))


def s1():
    k = R.choice(["add", "mult", "aff", "ajout"])
    m = Fr(R.randint(80, 160), 10)
    if k == "add":
        a = R.randint(1, 5)
        return M("La moyenne d’une série est %s. On ajoute %d à chaque valeur. Quelle est la nouvelle moyenne ?" % (d(m), a), d(m + a), [d(m), d(m * a), d(m + a * 2)], "La moyenne augmente aussi de %d : <b>%s</b>." % (a, d(m + a)))
    if k == "mult":
        a = R.choice([2, 3, Fr(1, 2), 10])
        return M("La moyenne d’une série est %s. On multiplie chaque valeur par %s. Quelle est la nouvelle moyenne ?" % (d(m), d(a)), d(m * a), [d(m), d(m + a), d(m * a * a)], "La moyenne est multipliée par %s : <b>%s</b>." % (d(a), d(m * a)))
    if k == "aff":
        a, b = R.choice([Fr(6, 5), Fr(3, 2), 2]), R.randint(1, 4)
        r = a * m + b
        return M("Les notes d’une classe ont pour moyenne %s. Le professeur transforme chaque note x en %sx + %d. Quelle est la nouvelle moyenne ?" % (d(m), d(a), b), d(r), [d(a * m), d(m + b), d(a * (m + b))], "Linéarité de la moyenne : %s × %s + %d = <b>%s</b>." % (d(a), d(m), b, d(r)))
    n = R.randint(5, 12)
    x = R.randint(0, 20)
    nm = (m * n + x) / (n + 1)
    if (nm * 100).denominator != 1:
        return None
    return M("Une série de %d valeurs a pour moyenne %s. On ajoute la valeur %d. Quelle est la nouvelle moyenne ?" % (n, d(m), x), d(nm), [d((m + x) / 2) if ((m + x) / 2 * 100).denominator == 1 and (m + x) / 2 != nm else d(nm + 1), d((m * n + x) / n) if ((m * n + x) / n * 100).denominator == 1 else d(nm - 1), d(m)],
             "Somme : %s × %d + %d = %s ; ÷ %d = <b>%s</b>." % (d(m), n, x, d(m * n + x), n + 1, d(nm)))


def s2():
    k = R.choice(["calc", "calc", "lin", "interp"])
    if k == "calc":
        c = R.randint(5, 15)
        e = R.choice([1, 2, 3, 4])
        v = [c - e, c + e] * 2 if R.random() < 0.5 else [c - e, c, c + e, c, c - e, c + e, c, c]
        m = mean(v)
        var = sum((x - m) ** 2 for x in v) / len(v)
        sd = Fr(round(math.sqrt(var) * 100), 100)
        if (Fr(round(math.sqrt(var) * 100), 100) ** 2 != var) and len(v) == 4:
            pass
        return M("Calcule l’écart type de la série : %s (arrondi au centième)." % " ; ".join(map(str, v)), dk(sd, 2) if sd.denominator != 1 else d(sd), [d(var) if var != sd else d(var + 1), dk(Fr(round(math.sqrt(var * len(v) / (len(v) - 1)) * 100), 100), 2), d(e * 2)],
                 "Moyenne %s ; variance = moyenne des carrés des écarts = %s ; σ = √%s ≈ <b>%s</b>." % (d(m), d(var), d(var), dk(sd, 2) if sd.denominator != 1 else d(sd)))
    s = Fr(R.randint(10, 50), 10)
    if k == "lin":
        a, b = R.choice([(2, 3), (3, 1), (Fr(1, 2), 4), (-2, 5), (10, 0)])
        return M("L’écart type d’une série est %s. On transforme chaque valeur x en %s. Quel est le nouvel écart type ?" % (d(s), expr([(a, "x"), (b, "")])), d(abs(a) * s), [d(a * s + b), d(s + b) if b else d(s * a * a), d(s)],
                 "Ajouter une constante ne change pas la dispersion ; multiplier par a multiplie σ par |a| : <b>%s</b>." % d(abs(a) * s))
    V = [("Que mesure l’écart type ?", "la dispersion des valeurs autour de la moyenne", ["la valeur la plus fréquente", "la valeur du milieu", "l’écart entre la plus grande et la plus petite valeur"]),
         ("Une série a un écart type nul. Que peut-on dire ?", "toutes les valeurs sont égales", ["la moyenne est nulle", "toutes les valeurs sont nulles", "la série est vide"]),
         ("Deux séries ont la même moyenne ; la série A a un écart type plus petit. Que peut-on dire ?", "les valeurs de A sont plus regroupées autour de la moyenne", ["A a plus de valeurs", "A a une médiane plus grande", "les deux séries sont identiques"]),
         ("Quel indicateur de dispersion associe-t-on à la médiane ?", "l’écart interquartile", ["l’écart type", "la moyenne", "le mode"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def s3():
    w_ = R.choice([5, 10, 20])
    lo = R.choice([0, 10, 20, 100, 150])
    eff = [R.randint(2, 12) for _ in range(4)]
    classes = [(lo + i * w_, lo + (i + 1) * w_) for i in range(4)]
    tb = table(["Classe"] + ["[%d ; %d[" % c for c in classes], [["Effectif"] + [str(e) for e in eff]])
    n = sum(eff)
    k = R.choice(["moy", "moy", "med", "centre"])
    if k == "centre":
        i = R.randrange(4)
        return M("%s<br>Quel est le centre de la classe [%d ; %d[ ?" % (tb, *classes[i]), d(Fr(sum(classes[i]), 2)), [str(classes[i][0]), str(classes[i][1]), str(w_)], "(%d + %d) ÷ 2 = <b>%s</b>." % (*classes[i], d(Fr(sum(classes[i]), 2))))
    if k == "moy":
        cs = [Fr(a + b, 2) for a, b in classes]
        m = sum(c * e for c, e in zip(cs, eff)) / n
        if (m * 100).denominator != 1:
            return None
        naive = sum(cs) / 4
        return M("%s<br>Estime la moyenne en utilisant les centres des classes." % tb, d(m), [d(naive) if naive != m and (naive * 100).denominator == 1 else d(m + 1), d(sum(a * e for (a, b), e in zip(classes, eff)) / Fr(n)) if ((sum(a * e for (a, b), e in zip(classes, eff)) / Fr(n)) * 100).denominator == 1 else d(m - 1), d(Fr(n, 4))],
                 "(%s) ÷ %d = <b>%s</b>." % (" + ".join("%s × %d" % (d(c), e) for c, e in zip(cs, eff)), n, d(m)))
    cum = 0
    for i, e in enumerate(eff):
        cum += e
        if cum >= Fr(n, 2):
            break
    modal = eff.index(max(eff))
    return M("%s<br>Quelle est la classe médiane ?" % tb, "[%d ; %d[" % classes[i], ["[%d ; %d[" % classes[modal] if modal != i else "[%d ; %d[" % classes[(i + 1) % 4], "[%d ; %d[" % classes[(i + 2) % 4], "[%d ; %d[" % (classes[0][0], classes[-1][1])],
             "Effectif total %d ; on cumule jusqu’à atteindre %s : <b>[%d ; %d[</b>." % (n, d(Fr(n, 2)), *classes[i]))


def s4():
    m1, m2 = R.randint(10, 14), R.randint(10, 14)
    s1_, s2_ = Fr(R.randint(5, 40), 10), Fr(R.randint(5, 40), 10)
    if s1_ == s2_:
        return None
    k = R.choice(["homog", "homog", "pc"])
    if k == "homog":
        if m1 != m2:
            m2 = m1
        ans = "la classe A" if s1_ < s2_ else "la classe B"
        return M("Classe A : moyenne %d, écart type %s. Classe B : moyenne %d, écart type %s. Quelle classe a les résultats les plus homogènes ?" % (m1, d(s1_), m2, d(s2_)), ans, ["la classe B" if ans == "la classe A" else "la classe A", "elles sont aussi homogènes", "on ne peut pas savoir"],
                 "Même moyenne ; le plus petit écart type indique des valeurs plus regroupées : <b>%s</b>." % ans)
    m = R.randint(10, 14)
    s = R.choice([1, 2, Fr(3, 2)])
    return M("Une série a pour moyenne %d et écart type %s. Quel intervalle [m − 2s ; m + 2s] contient en général la plupart des valeurs ?" % (m, d(s)), "[%s ; %s]" % (d(m - 2 * s), d(m + 2 * s)), ["[%s ; %s]" % (d(m - s), d(m + s)), "[%s ; %s]" % (d(m - 3 * s), d(m + 3 * s)), "[%s ; %s]" % (d(2 * m - s), d(2 * m + s))],
             "m − 2s = %s et m + 2s = %s : <b>[%s ; %s]</b>." % (d(m - 2 * s), d(m + 2 * s), d(m - 2 * s), d(m + 2 * s)))


def s5():
    k = R.choice(["salaire", "salaire", "notes", "python"])
    if k == "salaire":
        base = sorted(R.choice([1600, 1700, 1800, 1900, 2000]) for _ in range(5))
        top = R.choice([8000, 10000, 12000])
        v = base + [top]
        m = mean(v)
        med = Fr(v[2] + v[3], 2)
        return M("Salaires (€) : %s. On remplace %s par %s. Quel indicateur ne change pas ?" % (" ; ".join(num(x) for x in v), num(top), num(top * 2)), "la médiane", ["la moyenne", "l’écart type", "l’étendue"],
                 "Seule la plus grande valeur change : la médiane (%s €) reste la même, mais la moyenne et la dispersion augmentent." % num(med) if med.denominator == 1 else "Seule la plus grande valeur change : <b>la médiane</b> reste la même.")
    if k == "notes":
        v = [R.randint(6, 18) for _ in range(5)]
        m = mean(v)
        if (m * 100).denominator != 1:
            return None
        x = R.randint(0, 20)
        nm = (sum(v) + x) / Fr(6)
        if (nm * 100).denominator != 1:
            return None
        return M("Notes : %s. On ajoute une note de %d. La moyenne passe de %s à…" % (" ; ".join(map(str, v)), x, d(m)), d(nm), [d((m + x) / 2) if ((m + x) / 2 * 100).denominator == 1 and (m + x) / 2 != nm else d(nm + 1), d((sum(v) + x) / Fr(5)) if ((sum(v) + x) / Fr(5) * 100).denominator == 1 else d(nm - 1), d(m)],
                 "(%d + %d) ÷ 6 = <b>%s</b>." % (sum(v), x, d(nm)))
    V = [("Une fonction Python renvoie sum(L) / len(L) pour une liste L de nombres. Que renvoie-t-elle ?", "la moyenne des valeurs", ["la médiane", "l’écart type", "le nombre de valeurs"]),
         ("Dans une fonction qui calcule l’écart type, on trouve « return sqrt(v) ». Que représente v ?", "la variance", ["la moyenne", "la médiane", "l’étendue"])]
    q, a_, w = R.choice(V)
    return M(q, a_, w, "Réponse : <b>%s</b>." % a_)


def main():
    seen = set()
    sets = [("Moyenne et linéarité", mix(R, seen, [(s1, 20)])), ("Écart type", mix(R, seen, [(s2, 20)])),
            ("Données regroupées en classes", mix(R, seen, [(s3, 20)])), ("Comparer des séries", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Linéarité de la moyenne</b> : si chaque valeur x devient ax + b, la moyenne devient a × m + b.",
              "L’<b>écart type</b> s mesure la dispersion autour de la moyenne : s = √(moyenne des carrés des écarts à la moyenne). Ajouter b ne le change pas ; multiplier par a le multiplie par |a|.",
              "Pour des données regroupées en classes, on estime la moyenne avec les centres des classes. On compare deux séries avec (moyenne ; écart type) ou (médiane ; écart interquartile)."],
             [("Série 8 ; 10 ; 12 ; 10", ["moyenne 10", "écarts : −2 ; 0 ; 2 ; 0", "variance (4 + 0 + 4 + 0) ÷ 4 = 2"], "s = √2 ≈ 1,41")],
             [["Ajouter 2 à toutes les valeurs ne change pas la moyenne", "La moyenne augmente de 2 (l’écart type, lui, ne change pas)."], ["Écart type de 3x + 1 : 3s + 1", "C’est 3s."], ["Prendre une borne au lieu du centre de la classe", "Le centre de [10 ; 20[ est 15."]])
    faq = [("Pourquoi utiliser l’écart type ?", "Il résume en un nombre l’écart « moyen » des valeurs à la moyenne : plus il est petit, plus la série est homogène."),
           ("Moyenne ou médiane ?", "La médiane résiste aux valeurs extrêmes ; la moyenne en tient compte.")]
    unit("seconde", R, "statistiques", "S",
         "Utiliser la linéarité de la moyenne ; calculer et interpréter un écart type ; étudier l’effet d’une valeur ajoutée ; estimer une moyenne et une classe médiane pour des données regroupées en classes ; comparer deux séries",
         "Statistique descriptive", "Statistiques",
         "Fiches de maths seconde sur les statistiques : linéarité de la moyenne, écart type, données en classes, classe médiane et comparaison de séries. 100 exercices corrigés.",
         "Moyenne de ax + b : a × m + b", "Écart type : dispersion autour de la moyenne", body, faq, sets, 18)


if __name__ == "__main__":
    main()
