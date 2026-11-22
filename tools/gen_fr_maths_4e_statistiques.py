# -*- coding: utf-8 -*-
"""
France Maths 4e : Statistiques (moyenne pondérée, médiane, étendue, comparer des séries)
  python3 tools/gen_fr_maths_4e_statistiques.py
Erreurs : médiane sans ranger les valeurs, moyenne pondérée sans les effectifs, étendue = plus grande valeur, confondre moyenne et médiane.
"""
import random
from fr_c4 import *

R = random.Random(60317)
K = Kids(R)


def med(v):
    s = sorted(v)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def s1():
    n = R.choice([5, 7, 9, 6, 8, 10])
    v = [R.randint(2, 20) for _ in range(n)]
    m = med(v)
    raw = Fr(v[n // 2]) if n % 2 else Fr(v[n // 2 - 1] + v[n // 2], 2)
    mean = Fr(sum(v), n)
    w = [d(raw) if raw != m else d(m + 1), d(mean) if (mean * 100).denominator == 1 and mean != m else d(m - 1), d(Fr(max(v) + min(v), 2)) if Fr(max(v) + min(v), 2) != m else d(m + 2)]
    return M("Quelle est la médiane de la série : %s ?" % " ; ".join(map(str, v)), d(m), w,
             "On range : %s. %s : <b>%s</b>." % (" ; ".join(map(str, sorted(v))), "Valeur du milieu (%de)" % (n // 2 + 1) if n % 2 else "Moyenne des %de et %de valeurs" % (n // 2, n // 2 + 1), d(m)))


def s2():
    k = R.choice(["etendue", "etendue", "moy"])
    v = [R.randint(-5, 25) if R.random() < 0.3 else R.randint(5, 25) for _ in range(R.randint(5, 9))]
    if k == "etendue":
        e = max(v) - min(v)
        return M("Quelle est l’étendue de la série : %s ?" % " ; ".join(d(x) for x in v), d(e), [d(max(v)), d(max(v) + min(v)), d(abs(v[-1] - v[0])) if abs(v[-1] - v[0]) != e else d(e + 1)],
                 "Étendue = plus grande − plus petite = %s − %s = <b>%s</b>." % (d(max(v)), par(min(v)), d(e)))
    s = sum(v)
    m = Fr(s, len(v))
    if (m * 100).denominator != 1:
        return None
    return M("Quelle est la moyenne de la série : %s ?" % " ; ".join(d(x) for x in v), d(m), [d(s), d(med(v)) if med(v) != m else d(m + 1), d(Fr(s, len(v) - 1)) if (Fr(s, len(v) - 1) * 100).denominator == 1 else d(m - 1)],
             "Somme : %s ; %s ÷ %d = <b>%s</b>." % (d(s), d(s), len(v), d(m)))


def s3():
    vals = sorted(R.sample(range(5, 20), R.choice([3, 4])))
    eff = [R.randint(1, 8) for _ in vals]
    n = sum(eff)
    s = sum(a * b for a, b in zip(vals, eff))
    m = Fr(s, n)
    if (m * 100).denominator != 1:
        return None
    k = R.choice(["moy", "moy", "med"])
    tb = table(["Note"] + [str(x) for x in vals], [["Effectif"] + [str(e) for e in eff]])
    if k == "moy":
        naive = Fr(sum(vals), len(vals))
        return M("%s<br>Quelle est la moyenne de ces notes ?" % tb, d(m), [d(naive) if (naive * 100).denominator == 1 and naive != m else d(m + 1), d(s), d(Fr(s, len(vals))) if (Fr(s, len(vals)) * 100).denominator == 1 else d(m - 1)],
                 "Moyenne pondérée : (%s) ÷ %d = %d ÷ %d = <b>%s</b>." % (" + ".join("%d × %d" % (a, b) for a, b in zip(vals, eff)), n, s, n, d(m)))
    full = [a for a, b in zip(vals, eff) for _ in range(b)]
    md = med(full)
    return M("%s<br>Quelle est la médiane de ces notes ?" % tb, d(md), [d(med(vals)) if med(vals) != md else d(md + 1), d(m) if m != md else d(md - 1), d(Fr(n + 1, 2)) if Fr(n + 1, 2) != md else d(md + 2)],
             "Il y a %d notes. %s <b>%s</b>." % (n, "La médiane est la %de note : " % (n // 2 + 1) if n % 2 else "La médiane est la moyenne des %de et %de notes : " % (n // 2, n // 2 + 1), d(md)))


def s4():
    k = R.choice(["coef", "coef", "compare", "def"])
    if k == "coef":
        notes = [R.randint(6, 18) for _ in range(3)]
        co = R.choice([[1, 2, 3], [1, 1, 2], [2, 3, 5], [1, 2, 2]])
        s = sum(a * b for a, b in zip(notes, co))
        m = Fr(s, sum(co))
        if (m * 100).denominator != 1:
            return None
        naive = Fr(sum(notes), 3)
        return M("%s a eu %d (coefficient %d), %d (coefficient %d) et %d (coefficient %d). Quelle est sa moyenne ?" % (K.next()[0], notes[0], co[0], notes[1], co[1], notes[2], co[2]), d(m),
                 [d(naive) if (naive * 100).denominator == 1 and naive != m else d(m + 1), d(Fr(s, 3)) if (Fr(s, 3) * 100).denominator == 1 and Fr(s, 3) != m else d(m - 1), d(s)],
                 "(%d × %d + %d × %d + %d × %d) ÷ %d = %d ÷ %d = <b>%s</b>." % (notes[0], co[0], notes[1], co[1], notes[2], co[2], sum(co), s, sum(co), d(m)))
    if k == "compare":
        a = [R.randint(8, 14) for _ in range(5)]
        b = [R.randint(2, 20) for _ in range(5)]
        ea, eb = max(a) - min(a), max(b) - min(b)
        if ea == eb:
            return None
        ans = "la série A" if ea < eb else "la série B"
        return M("Série A : %s. Série B : %s. Quelle série est la plus regroupée (plus petite étendue) ?" % (" ; ".join(map(str, a)), " ; ".join(map(str, b))), ans, ["la série B" if ans == "la série A" else "la série A", "elles ont la même étendue", "on ne peut pas savoir"],
                 "Étendue de A : %d ; étendue de B : %d. <b>%s</b>." % (ea, eb, ans[0].upper() + ans[1:]))
    V = [("La médiane d’une série partage les valeurs rangées en…", "deux groupes de même effectif", ["deux groupes de même somme", "quatre groupes", "trois groupes"]),
         ("Dans une série, on remplace la plus grande valeur 18 par 80. Qu’est-ce qui ne change pas ?", "la médiane", ["la moyenne", "l’étendue", "la somme des valeurs"]),
         ("L’étendue mesure…", "la dispersion des valeurs", ["la valeur la plus fréquente", "la valeur du milieu", "la moyenne"]),
         ("La moyenne d’une série est 12. On ajoute 3 à chaque valeur. Quelle est la nouvelle moyenne ?", "15", ["12", "36", "on ne peut pas savoir"]),
         ("Une série a une médiane de 10. Cela signifie que…", "au moins la moitié des valeurs sont inférieures ou égales à 10", ["la moyenne vaut 10", "10 est la valeur la plus fréquente", "toutes les valeurs sont proches de 10"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s5():
    k = R.choice(["salaires", "manque", "temps", "classe"])
    if k == "salaires":
        base = [R.choice([1500, 1600, 1700, 1800, 1900]) for _ in range(4)]
        boss = R.choice([6000, 8000, 10000])
        v = sorted(base + [boss])
        m = Fr(sum(v), 5)
        return M("Les salaires d’une petite entreprise sont (en €) : %s. Quel indicateur représente le mieux le salaire « typique » ?" % " ; ".join(num(x) for x in v), "la médiane (%s €)" % num(v[2]),
                 ["la moyenne (%s €)" % num(m), "l’étendue (%s €)" % num(v[-1] - v[0]), "la plus grande valeur (%s €)" % num(v[-1])],
                 "La moyenne est tirée vers le haut par le salaire de %s € ; <b>la médiane</b> n’est pas influencée par cette valeur extrême." % num(boss))
    if k == "manque":
        notes = [R.randint(8, 16) for _ in range(3)]
        t = R.randint(11, 14)
        need = 4 * t - sum(notes)
        if not 0 <= need <= 20:
            return None
        return M("Un élève a eu %s à ses trois premiers contrôles. Quelle note lui faut-il au quatrième pour obtenir %d de moyenne ?" % (", ".join(map(str, notes)), t), str(need), [str(t), str(need + 1), str(3 * t - sum(notes)) if 3 * t - sum(notes) != need else str(need - 1)],
                 "Il faut un total de 4 × %d = %d ; il a %d : <b>%d</b>." % (t, 4 * t, sum(notes), need))
    if k == "temps":
        v = sorted(R.sample(range(40, 80), 7))
        return M("Temps (en s) de 7 nageurs : %s. Combien de nageurs ont un temps inférieur ou égal à la médiane ?" % " ; ".join(map(str, v)), "4", ["3", "7", "5"],
                 "La médiane est la 4e valeur (%d s) : <b>4</b> nageurs." % v[3])
    n1, n2 = R.randint(10, 15), R.randint(10, 15)
    m1, m2 = R.randint(9, 14), R.randint(9, 14)
    m = Fr(n1 * m1 + n2 * m2, n1 + n2)
    if (m * 100).denominator != 1 or m1 == m2:
        return None
    return M("Une classe de %d élèves a %d de moyenne, une autre de %d élèves a %d de moyenne. Quelle est la moyenne de l’ensemble des élèves ?" % (n1, m1, n2, m2), d(m),
             [d(Fr(m1 + m2, 2)) if Fr(m1 + m2, 2) != m else d(m + 1), d(n1 * m1 + n2 * m2), d(m + Fr(1, 2))],
             "(%d × %d + %d × %d) ÷ %d = %d ÷ %d = <b>%s</b>." % (n1, m1, n2, m2, n1 + n2, n1 * m1 + n2 * m2, n1 + n2, d(m)))


def main():
    seen = set()
    sets = [("Médiane", mix(R, seen, [(s1, 20)])), ("Étendue et moyenne", mix(R, seen, [(s2, 20)])),
            ("Tableaux d’effectifs", mix(R, seen, [(s3, 20)])), ("Coefficients et comparaisons", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La <b>moyenne pondérée</b> : on multiplie chaque valeur par son effectif (ou coefficient), on additionne, puis on divise par l’effectif total.",
              "La <b>médiane</b> partage la série <b>rangée</b> en deux groupes de même effectif.",
              "L’<b>étendue</b> = plus grande valeur − plus petite valeur : elle mesure la dispersion."],
             [("Série 4 ; 9 ; 7 ; 12 ; 5 ; 8", ["rangée : 4 ; 5 ; 7 ; 8 ; 9 ; 12", "médiane : (7 + 8) ÷ 2", "étendue : 12 − 4"], "médiane 7,5 ; étendue 8")],
             [["Chercher la médiane sans ranger", "On range d’abord les valeurs dans l’ordre croissant."], ["Moyenne des valeurs sans les effectifs", "Chaque valeur compte autant de fois que son effectif."],
              ["Étendue = plus grande valeur", "C’est l’écart entre la plus grande et la plus petite."]])
    faq = [("Moyenne ou médiane ?", "La médiane résiste aux valeurs extrêmes ; la moyenne tient compte de toutes les valeurs."),
           ("Comment trouver la médiane d’un nombre pair de valeurs ?", "On prend la moyenne des deux valeurs du milieu.")]
    unit("4e", R, "statistiques", "D",
         "Calculer et interpréter une moyenne pondérée, une médiane et une étendue ; lire un tableau d’effectifs ; comparer des séries statistiques",
         "Statistiques : moyenne, médiane et étendue", "Statistiques",
         "Fiches de maths 4e sur les statistiques : médiane, étendue, moyenne pondérée, tableaux d’effectifs, comparer des séries et problèmes. 100 exercices corrigés.",
         "Médiane : la valeur du milieu de la série rangée", "Étendue = max − min", body, faq, sets, 17)


if __name__ == "__main__":
    main()
