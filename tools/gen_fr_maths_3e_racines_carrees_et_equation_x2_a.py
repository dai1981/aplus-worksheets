# -*- coding: utf-8 -*-
"""
France Maths 3e : Racines carrées et équations x² = a
  python3 tools/gen_fr_maths_3e_racines_carrees_et_equation_x2_a.py
Erreurs : x² = 25 → x = 5 seulement, x² = −4 → x = −2, √(9 + 16) = 7, x² = 10 → x = 5.
"""
import random
import math
from fr_c4 import *

R = random.Random(60403)
K = Kids(R)


def S2(a):
    return "x = %s ou x = %s" % (a, ("−" + a) if not a.startswith("−") else a[1:])


def s1():
    n = R.randint(1, 15)
    k = R.choice(["carre", "carre", "zero", "neg", "dec"])
    if k == "carre":
        return M("Résous l’équation x² = %d." % (n * n), "x = %d ou x = −%d" % (n, n), ["x = %d" % n, "x = %s" % d(Fr(n * n, 2)), "pas de solution"],
                 "Les nombres dont le carré vaut %d sont %d et −%d : <b>x = %d ou x = −%d</b>." % (n * n, n, n, n, n))
    if k == "zero":
        return M("Résous l’équation x² = 0.", "x = 0", ["x = 0 ou x = 1", "pas de solution", "x = 1 ou x = −1"], "Seul 0 a pour carré 0 : <b>x = 0</b>.")
    if k == "neg":
        return M("Résous l’équation x² = −%d." % (n * n), "pas de solution", ["x = −%d" % n, "x = %d ou x = −%d" % (n, n), "x = %d" % n], "Un carré est toujours positif ou nul : <b>pas de solution</b>.")
    v = Fr(n, 10)
    return M("Résous l’équation x² = %s." % d(v * v), "x = %s ou x = −%s" % (d(v), d(v)), ["x = %s" % d(v), "x = %s ou x = −%s" % (d(v * 10), d(v * 10)), "x = %s ou x = −%s" % (d(v * v / 2), d(v * v / 2))],
             "%s² = %s : <b>x = %s ou x = −%s</b>." % (d(v), d(v * v), d(v), d(v)))


def s2():
    a = R.choice([2, 3, 5, 6, 7, 10, 11, 13, 15, 17, 20, 30])
    k = R.choice(["exact", "approx", "approx"])
    if k == "exact":
        return M("Donne les solutions exactes de l’équation x² = %d." % a, "x = √%d ou x = −√%d" % (a, a), ["x = √%d" % a, "x = %s ou x = −%s" % (d(Fr(a, 2)), d(Fr(a, 2))), "pas de solution"],
                 "%d est positif : <b>x = √%d ou x = −√%d</b>." % (a, a, a))
    v = Fr(round(math.sqrt(a) * 100), 100)
    return M("Donne les solutions de x² = %d, arrondies au centième." % a, "x ≈ %s ou x ≈ −%s" % (dk(v, 2), dk(v, 2)), ["x ≈ %s" % dk(v, 2), "x ≈ %s ou x ≈ −%s" % (d(Fr(a, 2)), d(Fr(a, 2))), "x ≈ %s ou x ≈ −%s" % (dk(v + Fr(1, 100), 2), dk(v + Fr(1, 100), 2))],
             "√%d ≈ %s… → <b>x ≈ %s ou x ≈ −%s</b>." % (a, d(Fr(int(math.sqrt(a) * 10000), 10000)), dk(v, 2), dk(v, 2)))


def s3():
    k = R.choice(["ax2", "ax2", "x2b", "carreplus"])
    n = R.randint(1, 10)
    if k == "ax2":
        a = R.choice([2, 3, 4, 5])
        return M("Résous l’équation %dx² = %d." % (a, a * n * n), "x = %d ou x = −%d" % (n, n), ["x = %s ou x = −%s" % (d(Fr(a * n * n, 2)), d(Fr(a * n * n, 2))) if a != 2 else "x = %d ou x = −%d" % (n * n, n * n), "x = %d" % n, "x = %s ou x = −%s" % (d(Fr(n * n * a, a + 1)), d(Fr(n * n * a, a + 1))) if (Fr(n * n * a, a + 1) * 10).denominator == 1 else "pas de solution"],
                 "x² = %d ÷ %d = %d, donc <b>x = %d ou x = −%d</b>." % (a * n * n, a, n * n, n, n))
    if k == "x2b":
        b = R.randint(1, 30)
        return M("Résous l’équation x² + %d = %d." % (b, n * n + b), "x = %d ou x = −%d" % (n, n), ["x = %d ou x = −%d" % (math.isqrt(n * n + 2 * b) if math.isqrt(n * n + 2 * b) ** 2 == n * n + 2 * b else n + 1, math.isqrt(n * n + 2 * b) if math.isqrt(n * n + 2 * b) ** 2 == n * n + 2 * b else n + 1), "x = %d" % n, "x = %d ou x = −%d" % (n * n, n * n) if n > 1 else "pas de solution"],
                 "x² = %d − %d = %d, donc <b>x = %d ou x = −%d</b>." % (n * n + b, b, n * n, n, n))
    a = R.randint(1, 8)
    return M("Résous l’équation (x − %d)² = %d." % (a, n * n), "x = %s ou x = %s" % (d(a + n), d(a - n)), ["x = %s" % d(a + n), "x = %s ou x = %s" % (d(n - a), d(-n - a)), "x = %s ou x = %s" % (d(n * n + a), d(a - n * n)) if n > 1 else "x = %s ou x = %s" % (d(a + 2), d(a - 2))],
             "x − %d = %d ou x − %d = −%d, donc <b>x = %s ou x = %s</b>." % (a, n, a, n, d(a + n), d(a - n)))


def s4():
    k = R.choice(["prod", "quot", "somme", "carre"])
    if k == "prod":
        a, b = R.choice([(4, 9), (4, 25), (9, 16), (16, 25), (4, 49), (9, 36), (25, 4), (36, 4)])
        return M("Calcule : √%d" % (a * b), str(math.isqrt(a * b)), [str(math.isqrt(a) + math.isqrt(b)), d(Fr(a * b, 2)), str(math.isqrt(a * b) + 1)], "√%d = √%d × √%d = %d × %d = <b>%d</b>." % (a * b, a, b, math.isqrt(a), math.isqrt(b), math.isqrt(a * b)))
    if k == "quot":
        a, b = R.choice([(9, 4), (25, 16), (49, 9), (1, 4), (16, 81), (36, 25)])
        return M("Calcule : √(%s)" % fr(a, b), fq(Fr(math.isqrt(a), math.isqrt(b))), [fq(Fr(a, math.isqrt(b))) if math.isqrt(b) != b else fq(Fr(a, 2)), fq(Fr(math.isqrt(a), b)), fq(Fr(b, a))],
                 "√%d ÷ √%d = %d ÷ %d = <b>%s</b>." % (a, b, math.isqrt(a), math.isqrt(b), fq(Fr(math.isqrt(a), math.isqrt(b)))))
    if k == "somme":
        a, b = R.choice([(9, 16), (36, 64), (25, 144), (64, 225), (144, 256), (81, 144)])
        return M("Calcule : √(%d + %d)" % (a, b), str(math.isqrt(a + b)), [str(math.isqrt(a) + math.isqrt(b)), str(a + b), str(math.isqrt(a + b) + 1)],
                 "√%d = <b>%d</b> (et non √%d + √%d = %d)." % (a + b, math.isqrt(a + b), a, b, math.isqrt(a) + math.isqrt(b)))
    n = R.randint(2, 12)
    return M("Calcule : (√%d)² + √(%d²)" % (n, n), str(2 * n), [str(n), str(n * n + n), str(2 * n * n)], "(√%d)² = %d et √(%d²) = %d : <b>%d</b>." % (n, n, n, n, 2 * n))


def s5():
    k = R.choice(["carre", "disque", "cube", "chute", "pyth"])
    if k == "carre":
        a = R.randint(2, 30)
        return M("Un carré a une aire de %d m². Combien mesure son côté ?" % (a * a), "%d m" % a, ["%s m" % d(Fr(a * a, 4)), "%s m" % d(Fr(a * a, 2)), "%d m et −%d m" % (a, a)],
                 "c² = %d avec c &gt; 0 (une longueur est positive) : <b>c = %d m</b>." % (a * a, a))
    if k == "disque":
        r = R.randint(2, 15)
        return M("Un disque a une aire de %dπ cm². Quel est son rayon ?" % (r * r), "%d cm" % r, ["%d cm" % (r * r), "%s cm" % d(Fr(r * r, 2)), "%d cm" % (2 * r)],
                 "πr² = %dπ, donc r² = %d et <b>r = %d cm</b>." % (r * r, r * r, r))
    if k == "cube":
        return M("Pour quelles valeurs de x a-t-on x² = 2x² − 49 ?", "x = 7 ou x = −7", ["x = 7", "x = 49", "pas de solution"], "On obtient x² = 49 : <b>x = 7 ou x = −7</b>.")
    if k == "chute":
        h = R.choice([20, 45, 80, 125, 180])
        t = math.isqrt(h // 5)
        return M("Un objet lâché sans vitesse parcourt d = 5t² mètres en t secondes. Combien de temps met-il pour tomber de %d m ?" % h, "%d s" % t, ["%d s" % (h // 5), "%d s" % (h // 10), "%d s ou −%d s" % (t, t)],
                 "5t² = %d, t² = %d et t &gt; 0 : <b>t = %d s</b>." % (h, h // 5, t))
    a = R.randint(2, 9)
    return M("Un triangle rectangle isocèle a une hypoténuse de longueur √%d cm. Combien mesurent les deux autres côtés ?" % (2 * a * a), "%d cm" % a, ["%d cm" % (a * a), "%s cm" % d(Fr(2 * a * a, 2)), "√%d cm" % a],
             "x² + x² = %d, donc x² = %d et <b>x = %d cm</b>." % (2 * a * a, a * a, a))


def main():
    seen = set()
    sets = [("Résoudre x² = a", mix(R, seen, [(s1, 20)])), ("Solutions exactes et approchées", mix(R, seen, [(s2, 20)])),
            ("Se ramener à x² = a", mix(R, seen, [(s3, 20)])), ("Calculs avec des racines carrées", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Si a &gt; 0, l’équation x² = a a <b>deux solutions</b> : √a et −√a. Si a = 0, une seule : 0. Si a &lt; 0, aucune.",
              "√(a × b) = √a × √b et √(a ÷ b) = √a ÷ √b pour a, b positifs. Mais √(a + b) n’est pas √a + √b.",
              "Dans un problème de longueur ou de durée, on ne garde que la solution positive."],
             [("3x² = 75", ["x² = 25", "x = 5 ou x = −5"], "deux solutions"), ("x² = 7", ["x = √7 ou x = −√7"], "x ≈ 2,65 ou x ≈ −2,65")],
             [["x² = 25 donne seulement x = 5", "(−5)² = 25 aussi : x = 5 ou x = −5."], ["x² = −4 donne x = −2", "(−2)² = 4 : un carré n’est jamais négatif, pas de solution."],
              ["x² = 10 donne x = 5", "On ne divise pas par 2 : x = √10 ou x = −√10."]])
    faq = [("Pourquoi deux solutions ?", "Parce qu’un nombre et son opposé ont le même carré."),
           ("Faut-il garder la solution négative ?", "En calcul, oui ; dans un problème de longueur, de temps ou d’aire, on ne garde que la solution positive.")]
    unit("3e", R, "racines-carrees-et-equation-x2-a", "N",
         "Résoudre une équation de la forme x² = a ; donner des solutions exactes ou approchées ; utiliser les propriétés de la racine carrée ; résoudre des problèmes de géométrie et de physique",
         "Racines carrées et équations x² = a", "Racines carrées et x² = a",
         "Fiches de maths 3e sur les racines carrées : résoudre x² = a, solutions exactes et approchées, calculs avec √ et problèmes. 100 exercices corrigés.",
         "x² = a (a > 0) : x = √a ou x = −√a", "x² = a (a < 0) : pas de solution", body, faq, sets, 3)


if __name__ == "__main__":
    main()
