# -*- coding: utf-8 -*-
"""
France Maths 5e : Statistiques (effectifs, fréquences, moyenne, représentations)
  python3 tools/gen_fr_maths_5e_statistiques.py
Erreurs : confondre effectif et fréquence, oublier de diviser par l’effectif total, moyenne = valeur du milieu.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_tableaux_et_diagrammes as TD

R = random.Random(60218)
K = Kids(R)
TD.R = R


def s1():
    vals = [R.randint(5, 20) for _ in range(R.randint(10, 15))]
    v = R.choice(vals)
    n = vals.count(v)
    k = R.choice(["eff", "freq", "tot"])
    lst = ", ".join(map(str, vals))
    if k == "eff":
        return M("Notes d’un contrôle : %s. Quel est l’effectif de la note %d ?" % (lst, v), str(n), [str(v), str(len(vals)), str(n + 1)], "La note %d apparaît <b>%d</b> fois." % (v, n))
    if k == "freq":
        return M("Notes d’un contrôle : %s. Quelle est la fréquence de la note %d ?" % (lst, v), fr(n, len(vals)), [fr(v, len(vals)), str(n), fr(len(vals), n)],
                 "Fréquence = effectif ÷ effectif total = <b>%s</b>." % fr(n, len(vals)))
    return M("Notes d’un contrôle : %s. Quel est l’effectif total ?" % lst, str(len(vals)), [str(sum(vals)), str(max(vals)), str(len(vals) - 1)], "On compte toutes les notes : <b>%d</b>." % len(vals))


def s2():
    tot = R.choice([20, 25, 40, 50])
    n = R.randint(2, tot - 2)
    f = Fr(n, tot)
    k = R.choice(["dec", "pc", "frac"])
    if k == "dec":
        return M("Dans un club de %d membres, %d font du tennis. Quelle est la fréquence des joueurs de tennis, en écriture décimale ?" % (tot, n), d(f), [d(Fr(n, 100)), d(Fr(tot, n)) if Fr(tot, n).denominator in (1, 2, 4, 5, 10, 20, 25, 50) else d(f + Fr(1, 10)), d(1 - f)],
                 "%d ÷ %d = <b>%s</b>." % (n, tot, d(f)))
    if k == "pc":
        return M("Dans un club de %d membres, %d font du tennis. Quelle est la fréquence en pourcentage ?" % (tot, n), "%s %%" % d(f * 100), ["%d %%" % n, "%s %%" % d((1 - f) * 100), "%s %%" % d(f)],
                 "%d ÷ %d = %s = <b>%s %%</b>." % (n, tot, d(f), d(f * 100)))
    if (f * 100).denominator != 1 or f == Fr(1, 2):
        return None
    w = [fq(1 - f), fr(100, int(f * 100)), fr(1, int(f * 100)) if int(f * 100) > 1 else fr(1, 3)]
    return M("La fréquence d’une valeur est %s %%. Écris-la sous forme de fraction irréductible." % d(f * 100), fq(f), w,
             "%s %% = %s = <b>%s</b>." % (d(f * 100), fr(d(f * 100), 100), fq(f)))


def s3():
    vals = [R.randint(6, 18) for _ in range(R.randint(4, 7))]
    s = sum(vals)
    m = Fr(s, len(vals))
    if (m * 100).denominator != 1:
        return None
    k = R.choice(["moy", "moy", "manque"])
    if k == "moy":
        srt = sorted(vals)
        return M("Calcule la moyenne de : %s." % ", ".join(map(str, vals)), d(m), [d(srt[len(srt) // 2]) if srt[len(srt) // 2] != m else d(m + 1), str(s), d(Fr(max(vals) + min(vals), 2)) if Fr(max(vals) + min(vals), 2) != m else d(m - 1)],
                 "Moyenne = somme ÷ nombre de valeurs = %d ÷ %d = <b>%s</b>." % (s, len(vals), d(m)))
    t = R.randint(10, 16)
    n = len(vals) + 1
    need = t * n - s
    if not 0 <= need <= 20:
        return None
    return M("Un élève a eu %s. Quelle note doit-il avoir au prochain contrôle pour avoir exactement %d de moyenne ?" % (", ".join(map(str, vals)), t), str(need), [str(t), str(need + 1), str(t * n - s + len(vals)) if t * n - s + len(vals) != need else str(need - 1)],
             "Il faut un total de %d × %d = %d points ; il en a %d : il manque <b>%d</b>." % (t, n, t * n, s, need))


def s4():
    t, key, cats, vals, u = TD.data(4, 30)
    tot = sum(vals)
    i = R.randrange(len(cats))
    k = R.choice(["lire", "freq", "angle"])
    svg = barres(list(zip(cats, vals)), "nombre %s" % TD.de(u))
    if k == "lire":
        return M("<div class='qfig'>%s</div>%s. Combien %s pour « %s » ?" % (svg, t, TD.de(u), cats[i]), str(vals[i]), [str(vals[(i + 1) % len(vals)]), str(vals[i] + 1), str(tot)],
                 "On lit le haut de la barre « %s » : <b>%d</b>." % (cats[i], vals[i]))
    if k == "freq":
        return M("<div class='qfig'>%s</div>%s. Quelle est la fréquence de « %s » ?" % (svg, t, cats[i]), fr(vals[i], tot), [fr(vals[i], 100), fr(tot, vals[i]), fr(vals[i], max(vals)) if vals[i] != max(vals) else fr(1, len(cats))],
                 "Effectif total : %d. Fréquence : <b>%s</b>." % (tot, fr(vals[i], tot)))
    if 360 * vals[i] % tot:
        return None
    return M("<div class='qfig'>%s</div>%s. Dans un diagramme circulaire, quel angle faut-il pour « %s » ?" % (svg, t, cats[i]), "%d°" % (360 * vals[i] // tot), ["%d°" % vals[i], "%d°" % (180 * vals[i] // tot), "%d°" % (360 * vals[i] // tot + 10)],
             "360° × %s = <b>%d°</b>." % (fr(vals[i], tot), 360 * vals[i] // tot))


def s5():
    k = R.choice(["choix", "moyc", "compare"])
    if k == "choix":
        V = [("Pour représenter la répartition des élèves selon leur sport préféré, quel graphique convient bien ?", "un diagramme en barres ou circulaire", ["une courbe", "un nuage de points", "aucun graphique"]),
             ("Pour représenter l’évolution de la température au cours d’une journée, quel graphique convient bien ?", "un graphique cartésien (courbe)", ["un diagramme circulaire", "un tableau sans graphique", "un diagramme en barres empilées"]),
             ("Dans un diagramme circulaire, une catégorie de fréquence 25 % correspond à un angle de…", "90°", ["25°", "45°", "180°"]),
             ("Dans un diagramme circulaire, une catégorie de fréquence %s correspond à un angle de…" % fr(1, 3), "120°", ["30°", "60°", "180°"])]
        q, a, w = R.choice(V)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    if k == "moyc":
        vals = [(R.randint(8, 18), R.randint(1, 5)) for _ in range(3)]
        if len({v for v, _ in vals}) < 3:
            return None
        n = sum(c for _, c in vals)
        s = sum(v * c for v, c in vals)
        m = Fr(s, n)
        if (m * 100).denominator != 1:
            return None
        tb = table(["Note"] + [str(v) for v, _ in vals], [["Effectif"] + [str(c) for _, c in vals]])
        return M("%s<br>Quelle est la note moyenne ?" % tb, d(m), [d(Fr(sum(v for v, _ in vals), 3)) if Fr(sum(v for v, _ in vals), 3) != m and (Fr(sum(v for v, _ in vals), 3) * 100).denominator == 1 else d(m + 1), str(s), d(m - 1)],
                 "On ajoute note × effectif : %d, et on divise par l’effectif total %d : <b>%s</b>." % (s, n, d(m)))
    a = [R.randint(8, 16) for _ in range(4)]
    b = [R.randint(8, 16) for _ in range(4)]
    ma, mb = Fr(sum(a), 4), Fr(sum(b), 4)
    if ma == mb:
        return None
    p, q = K.two()
    w = p[0] if ma > mb else q[0]
    return M("Notes %s : %s. Notes %s : %s. Qui a la meilleure moyenne ?" % (de_n(p[0]), ", ".join(map(str, a)), de_n(q[0]), ", ".join(map(str, b))), w, [q[0] if w == p[0] else p[0], "les deux ont la même moyenne", "on ne peut pas savoir"],
             "%s : %s ; %s : %s. <b>%s</b>." % (p[0], d(ma), q[0], d(mb), w))


def main():
    seen = set()
    sets = [("Effectifs et fréquences", mix(R, seen, [(s1, 20)])), ("Fréquences : décimal, fraction, %", mix(R, seen, [(s2, 20)])),
            ("Calculer une moyenne", mix(R, seen, [(s3, 20)])), ("Lire et construire des diagrammes", mix(R, seen, [(s4, 20)])), ("Interpréter et comparer", mix(R, seen, [(s5, 20)]))]
    body = L(["L’<b>effectif</b> d’une valeur est le nombre de fois où elle apparaît ; la <b>fréquence</b> est effectif ÷ effectif total (fraction, décimal ou %).",
              "La <b>moyenne</b> est la somme des valeurs divisée par le nombre de valeurs.",
              "Diagramme en barres : hauteur = effectif. Diagramme circulaire : angle = 360° × fréquence."],
             [("Notes 12, 15, 9, 14", ["12 + 15 + 9 + 14 = 50", "50 ÷ 4"], "12,5")],
             [["Confondre effectif et fréquence", "La fréquence se calcule en divisant par l’effectif total."], ["Oublier de diviser par le nombre de valeurs", "Moyenne = somme ÷ nombre de valeurs."],
              ["Croire que la moyenne est la valeur du milieu", "La valeur du milieu s’appelle la médiane (étudiée en 4e)."]])
    faq = [("La somme des fréquences fait combien ?", "1, soit 100 %."), ("La moyenne est-elle forcément une des valeurs ?", "Non : la moyenne de 12 et 13 est 12,5.")]
    unit("5e", R, "statistiques", "D",
         "Recueillir et organiser des données ; calculer des effectifs et des fréquences (fraction, décimal, pourcentage) ; lire et construire des diagrammes en barres et circulaires ; calculer et interpréter une moyenne simple",
         "Statistiques", "Statistiques",
         "Fiches de maths 5e sur les statistiques : effectifs, fréquences, moyenne, diagrammes en barres et circulaires, comparer des séries. 100 exercices corrigés.",
         "Fréquence = effectif ÷ effectif total", "Moyenne = somme ÷ nombre de valeurs", body, faq, sets, 18)


if __name__ == "__main__":
    main()
