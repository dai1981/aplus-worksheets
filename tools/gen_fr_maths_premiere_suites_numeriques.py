# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Suites numériques (forme explicite, récurrence, motifs, algorithme, sens de variation)
  python3 tools/gen_fr_maths_premiere_suites_numeriques.py
Erreurs : confondre u(n+1) et u(n) + 1, décaler l’indice (u₀ est le premier terme), appliquer la formule de récurrence comme une formule explicite, conclure sur le sens de variation à partir de deux termes.
"""
import random
from fr_ly1 import *

R = random.Random(60602)


def s1():
    k = R.choice(["poly", "poly", "frac", "pow", "plus1"])
    n = R.randint(2, 9)
    if k == "poly":
        a, b, c = nz(R, -3, 3), R.randint(-6, 6), R.randint(-9, 9)
        f = lambda t: a * t * t + b * t + c
        ex = E((a, "n²"), (b, "n"), (c, ""))
        return M("La suite (u<sub>n</sub>) est définie par %s = %s. Calcule %s." % (U("n"), ex, U(n)), d(f(n)), [d(f(n - 1)), d(f(n + 1)), d(a * 2 * n + b * n + c), d((a * n) ** 2 + b * n + c), d(a * n * n - b * n + c), d(-a * n * n + b * n + c)],
                 "On remplace n par %d : %s = <b>%s</b>." % (n, U(n), d(f(n))))
    if k == "frac":
        a, b = R.randint(1, 6), R.randint(1, 5)
        f = lambda t: Fr(a * t + 1, t + b)
        return M("%s = (%dn + 1) ÷ (n + %d). Calcule %s." % (U("n"), a, b, U(n)), fq(f(n)), [fq(f(n + 1)), fq(Fr(a * n + 1, n) + b), fq(f(n - 1))],
                 "%s = (%d × %d + 1) ÷ (%d + %d) = <b>%s</b>." % (U(n), a, n, n, b, fq(f(n))))
    if k == "pow":
        a, q = R.randint(1, 5), R.choice([2, 3])
        n = R.randint(2, 5)
        return M("%s = %d × %d<sup>n</sup>. Calcule %s." % (U("n"), a, q, U(n)), d(a * q ** n), [d((a * q) ** n), d(a * q * n), d(a * q ** (n - 1))],
                 "%s = %d × %d<sup>%d</sup> = %d × %d = <b>%d</b> (la puissance d’abord)." % (U(n), a, q, n, a, q ** n, a * q ** n))
    a, b = nz(R, -4, 5), R.randint(-6, 8)
    f = lambda t: a * t * t + b
    return M("%s = %s. Exprime %s en fonction de n." % (U("n"), E((a, "n²"), (b, "")), U("n+1")), E((a, "n²"), (2 * a, "n"), (a + b, "")),
             [E((a, "n²"), (b + 1, "")), E((a, "n²"), (a + b, "")), E((a, "n²"), (2 * a, "n"), (b, "")), E((a, "n²"), (a, "n"), (a + b, "")), E((a, "n²"), (1, "n"), (b + 1, ""))],
             "%s = %s(n + 1)² %s = <b>%s</b> (on remplace n par n + 1, on ne rajoute pas 1)." % (U("n+1"), "" if a == 1 else MINUS if a == -1 else d(a), ("+ " + d(b)) if b >= 0 else (MINUS + " " + d(-b)), E((a, "n²"), (2 * a, "n"), (a + b, ""))))


def s2():
    k = R.choice(["aff", "aff", "carre", "inv"])
    u0 = R.randint(-4, 6)
    n = R.randint(2, 3)
    if k == "aff":
        p, q = R.choice([2, 3, -1, -2, Fr(1, 2)]), R.randint(-5, 5)
        if Fr(p) == Fr(1, 2) and u0 % 2:
            u0 += 1
        t = [Fr(u0)]
        for _ in range(n):
            t.append(p * t[-1] + q)
        rhs = E((p, U("n")), (q, ""))
        return M("%s = %s et %s = %s. Calcule %s." % (U(0), d(u0), U("n+1"), rhs, U(n)), fq(t[n]), [fq(t[n - 1]), fq(p * n + q), fq(p * t[n] + q), fq(t[n] + q), fq(p * (t[n - 1] + q))],
                 "%s ; %s = <b>%s</b>." % (" ; ".join("%s = %s" % (U(i), fq(t[i])) for i in range(1, n)), U(n), fq(t[n])))
    if k == "carre":
        c = nz(R, -3, 3)
        u0 = R.randint(-2, 3)
        t = [u0]
        for _ in range(2):
            t.append(t[-1] ** 2 + c)
        return M("%s = %s et %s = %s. Calcule %s." % (U(0), d(u0), U("n+1"), E((1, U("n") + "²"), (c, "")), U(2)), d(t[2]), [d(t[1]), d(4 + c), d(2 * t[1] + c), d(t[1] ** 2 - c), d(t[2] + 1), d(-(t[1] ** 2) + c)],
                 "%s = %s ; %s = %s² %s = <b>%s</b>." % (U(1), d(t[1]), U(2), par(t[1]), ("+ " + d(c)) if c >= 0 else (MINUS + " " + d(-c)), d(t[2])))
    p = R.randint(2, 5)
    u1 = R.randint(1, 9)
    t = [u1]
    for i in range(1, 3):
        t.append(t[-1] + p * i)
    return M("%s = %d et, pour tout n ⩾ 1, %s = %s + %dn. Calcule %s." % (U(1), u1, U("n+1"), U("n"), p, U(3)), d(t[2]), [d(t[1]), d(u1 + 2 * p), d(u1 + 3 * p * 2)],
             "%s = %d + %d × 1 = %d ; %s = %d + %d × 2 = <b>%d</b>." % (U(2), u1, p, t[1], U(3), t[1], p, t[2]))


def s3():
    k = R.choice(["aff", "diff", "diff", "rec", "frac", "graph"])
    if k == "aff":
        a, b = nz(R, -7, 7), R.randint(-9, 9)
        ans = "croissante" if a > 0 else "décroissante"
        return M("Quel est le sens de variation de la suite définie par %s = %s ?" % (U("n"), E((a, "n"), (b, ""))), ans, ["décroissante" if a > 0 else "croissante", "constante", "ni croissante ni décroissante"],
                 "%s − %s = %s, %s : la suite est <b>%s</b>." % (U("n+1"), U("n"), d(a), "positif" if a > 0 else "négatif", ans))
    if k == "diff":
        a, b, c = R.randint(1, 4), R.randint(-6, 6), R.randint(-9, 9)
        return M("%s = %s. Calcule %s − %s." % (U("n"), E((a, "n²"), (b, "n"), (c, "")), U("n+1"), U("n")), E((2 * a, "n"), (a + b, "")),
                 [E((2 * a, "n"), (b, "")), E((a, "n"), (a + b, "")), E((2 * a, "n"), (a + b + c, "")), E((a, "")), E((2 * a, "n"), (a - b, ""))],
                 "%s(n + 1)² − %sn² %s = <b>%s</b>." % (d(a) if a > 1 else "", d(a) if a > 1 else "", ("+ %s" % E((b, ""))) if b > 0 else ("" if not b else "− %s" % d(-b)), E((2 * a, "n"), (a + b, ""))))
    if k == "rec":
        c = R.randint(1, 9)
        sgn = R.choice([1, -1])
        rhs = "%s %s %s" % (U("n"), "+" if sgn > 0 else MINUS, R.choice(["%d" % c, "n² + %d" % c, ("%dn + 1" % c) if c > 1 else "n + 1"]))
        ans = "croissante" if sgn > 0 else "décroissante"
        return M("Pour tout n, %s = %s. Quel est le sens de variation de (u<sub>n</sub>) ?" % (U("n+1"), rhs), ans, ["décroissante" if sgn > 0 else "croissante", "on ne peut pas savoir sans %s" % U(0), "constante"],
                 "%s − %s = %s%s, %s pour tout n : la suite est <b>%s</b>." % (U("n+1"), U("n"), "" if sgn > 0 else MINUS + "(", rhs.split(" ", 2)[2] + ("" if sgn > 0 else ")"), "positif" if sgn > 0 else "négatif", ans))
    if k == "frac":
        c = R.randint(1, 9)
        b = R.randint(1, 4)
        return M("%s = %d ÷ (n + %d) pour n ⩾ 0. Quel est le sens de variation de la suite ?" % (U("n"), c, b), "décroissante", ["croissante", "constante", "croissante puis décroissante"],
                 "Quand n augmente, n + %d augmente, donc %d ÷ (n + %d) diminue : la suite est <b>décroissante</b>." % (b, c, b))
    a, b = R.randint(1, 3), R.randint(4, 9)
    m = Fr(b, 2 * a)
    return M("%s = %s. La suite est-elle monotone ?" % (U("n"), E((a, "n²"), (-b, "n"))),
             "elle décroît d’abord, puis croît",
             ["oui, elle est croissante", "oui, elle est décroissante", "oui, elle est constante"],
             "%s − %s = %s : négatif pour les petits n, positif ensuite. La suite <b>décroît d’abord, puis croît</b>." % (U("n+1"), U("n"), E((2 * a, "n"), (a - b, ""))))


def s4():
    k = R.choice(["motif", "motif", "algo", "algo2", "rang"])
    if k == "motif":
        a, b = R.randint(2, 6), R.randint(1, 5)
        obj = R.choice(["allumettes", "jetons", "carreaux", "points"])
        n = R.randint(8, 30)
        return M("Un motif de rang 1 utilise %d %s, celui de rang 2 en utilise %d, celui de rang 3 en utilise %d, et ainsi de suite (on ajoute %d à chaque fois). Combien de %s pour le rang %d ?" % (a + b, obj, 2 * a + b, 3 * a + b, a, obj, n),
                 str(a * n + b), [str(a * n), str(a * (n - 1) + b + a * 2), str((a + b) * n)], "Rang n : %dn + %d. Rang %d : %d × %d + %d = <b>%d</b>." % (a, b, n, a, n, b, a * n + b))
    if k == "algo":
        u0, p, q, n = R.randint(1, 5), R.choice([2, 3]), R.randint(-3, 3), R.randint(2, 4)
        t = [u0]
        for _ in range(n):
            t.append(p * t[-1] + q)
        if t[1] == t[0]:
            return None
        return M("Que vaut u à la fin de ce programme ?%s" % code("u = %d" % u0, "for i in range(%d):" % n, "    u = %d * u %s %d" % (p, "+" if q >= 0 else "-", abs(q))), d(t[n]),
                 [d(t[n - 1]), d(t[n] * p + q), d(u0 + n * (p + q)), d(u0 * p ** n), d(t[n] + 1)], "La boucle fait %d tours : u prend les valeurs %s. À la fin, u = <b>%s</b> = u<sub>%d</sub>." % (n, ", ".join(d(x) for x in t[1:]), d(t[n]), n))
    if k == "algo2":
        a, b, n = R.randint(1, 4), R.randint(1, 6), R.randint(3, 6)
        return M("Que renvoie suite(%d) ?%s" % (n, code("def suite(n):", "    return %d * n ** 2 + %d" % (a, b))), str(a * n * n + b), [str((a * n) ** 2 + b), str(a * 2 * n + b), str(a * n * n)],
                 "%d × %d² + %d = <b>%d</b> (forme explicite)." % (a, n, b, a * n * n + b))
    u0 = R.randint(1, 5)
    return M("Une suite commence par %s = %d. Quel est son 10<sup>e</sup> terme ?" % (U(0), u0), U(9), [U(10), U(11), U(8)], "%s est le 1<sup>er</sup> terme, donc le 10<sup>e</sup> est <b>%s</b>." % (U(0), U(9)))


def s5():
    k = R.choice(["abo", "pop", "eau", "stock"])
    if k == "abo":
        u0 = R.randint(4, 12) * 100
        r = R.choice([Fr(8, 10), Fr(9, 10), Fr(85, 100)])
        a = R.randint(2, 8) * 50
        u1 = r * u0 + a
        u2 = r * u1 + a
        return M("Un club compte %d abonnés en 2025. Chaque année, %s %% des abonnés restent et %d nouveaux s’inscrivent. On note %s le nombre d’abonnés en 2025 + n. Combien y aura-t-il d’abonnés en 2027 ?" % (u0, d(r * 100), a, U("n")),
                 d(u2), [d(u1), d(u0 + 2 * a), d(r * r * u0)], "%s = %s × %s + %d = %s ; %s = %s × %s + %d = <b>%s</b>." % (U(1), d(r), d(u0), a, d(u1), U(2), d(r), d(u1), a, d(u2)))
    if k == "pop":
        u0 = R.randint(2, 9) * 1000
        t = R.choice([2, 4, 5, 10])
        u2 = u0 * (1 + Fr(t, 100)) ** 2
        return M("Une ville compte %s habitants. Sa population augmente de %d %% par an. Quelle relation de récurrence vérifie la population %s après n années ?" % (num(u0), t, U("n")),
                 "%s = %s × %s" % (U("n+1"), d(1 + Fr(t, 100)), U("n")), ["%s = %s + %d" % (U("n+1"), U("n"), t), "%s = %s × %s" % (U("n+1"), d(Fr(t, 100)), U("n")), "%s = %s + %s" % (U("n+1"), U("n"), d(1 + Fr(t, 100)))],
                 "Augmenter de %d %% revient à multiplier par 1 + %s = <b>%s</b>." % (t, d(Fr(t, 100)), d(1 + Fr(t, 100))))
    if k == "eau":
        u0 = R.randint(10, 30) * 10
        p = R.choice([10, 20, 25])
        a = R.randint(2, 6) * 10
        u1 = u0 * (100 - p) / Fr(100) + a
        return M("Une cuve contient %d L. Chaque semaine, on retire %d %% de l’eau puis on ajoute %d L. Combien de litres après une semaine ?" % (u0, p, a), d(u1), [d(u0 - p + a), d((u0 + a) * (100 - p) / Fr(100)), d(u0 * p / Fr(100) + a)],
                 "%d × %s + %d = <b>%s</b> L (on retire d’abord, on ajoute ensuite)." % (u0, d(1 - Fr(p, 100)), a, d(u1)))
    u0, a = R.randint(50, 120), R.randint(3, 9)
    n = R.randint(5, 12)
    return M("Un stock de %d pièces diminue de %d pièces par jour. On note %s le stock après n jours. Exprime %s en fonction de n." % (u0, a, U("n"), U("n")), "%s = %d %s %dn" % (U("n"), u0, MINUS, a),
             ["%s = %d %s %d" % (U("n"), u0, MINUS, a), "%s = %d %s %d<sup>n</sup>" % (U("n"), u0, MINUS, a), "%s = %dn %s %d" % (U("n"), u0, MINUS, a)],
             "On retire %d chaque jour, n fois : <b>%s = %d − %dn</b>." % (a, U("n"), u0, a))


def main():
    seen = set()
    sets = [("Forme explicite", mix(R, seen, [(s1, 20)])), ("Relation de récurrence", mix(R, seen, [(s2, 20)])),
            ("Sens de variation", mix(R, seen, [(s3, 20)])), ("Motifs et algorithmes", mix(R, seen, [(s4, 20)])), ("Modéliser par une suite", mix(R, seen, [(s5, 20)]))]
    body = L(["Une suite (u<sub>n</sub>) associe un nombre u<sub>n</sub> à chaque entier n. Le premier terme est souvent u<sub>0</sub>.",
              "<b>Forme explicite</b> : u<sub>n</sub> = f(n), on calcule directement n’importe quel terme. <b>Récurrence</b> : u<sub>n+1</sub> = f(u<sub>n</sub>), on calcule les termes un par un.",
              "Sens de variation : on étudie le signe de u<sub>n+1</sub> − u<sub>n</sub>. Positif pour tout n : croissante ; négatif : décroissante."],
             [("u<sub>0</sub> = 2 et u<sub>n+1</sub> = 3u<sub>n</sub> − 1", ["u<sub>1</sub> = 3 × 2 − 1 = 5", "u<sub>2</sub> = 3 × 5 − 1 = 14"], "u<sub>2</sub> = 14"),
              ("u<sub>n</sub> = n² + 1", ["u<sub>n+1</sub> − u<sub>n</sub> = (n + 1)² + 1 − n² − 1 = 2n + 1 &gt; 0"], "la suite est croissante")],
             [["u<sub>n+1</sub> = u<sub>n</sub> + 1", "u<sub>n+1</sub> s’obtient en remplaçant n par n + 1 dans la formule."], ["Le 5<sup>e</sup> terme est u<sub>5</sub>", "Si la suite commence à u<sub>0</sub>, le 5<sup>e</sup> terme est u<sub>4</sub>."],
              ["u<sub>1</sub> &lt; u<sub>2</sub> donc la suite est croissante", "Il faut comparer u<sub>n+1</sub> et u<sub>n</sub> pour tout n."]])
    faq = [("Quelle différence entre forme explicite et récurrence ?", "Avec la forme explicite, on calcule u<sub>100</sub> directement. Avec une récurrence, il faut d’abord u<sub>99</sub>, donc tous les termes précédents (ou un algorithme)."),
           ("Comment étudier le sens de variation d’une suite ?", "On calcule u<sub>n+1</sub> − u<sub>n</sub> et on étudie son signe. Si les termes sont positifs, on peut aussi comparer u<sub>n+1</sub> ÷ u<sub>n</sub> à 1.")]
    unit("premiere", R, "suites-numeriques", "A",
         "Modes de génération d’une suite : explicite, par récurrence, par un algorithme, par des motifs ; calculer des termes ; sens de variation d’une suite ; modéliser une situation discrète par une suite",
         "Suites numériques : forme explicite, récurrence et variations", "Suites numériques",
         "Fiches de maths première sur les suites numériques : forme explicite, relation de récurrence, motifs, algorithmes en Python et sens de variation. 100 exercices corrigés.",
         "Pour u(n + 1), on remplace n par n + 1", "Sens de variation : signe de u(n + 1) − u(n)", body, faq, sets, 2)


if __name__ == "__main__":
    main()
