# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Suites arithmétiques (raison, terme général, sens de variation, représentation, problèmes)
  python3 tools/gen_fr_maths_premiere_suites_arithmetiques.py
Erreurs : u(n) = u(0) + (n − 1)r quand la suite commence à u(0), raison = u(n) − u(n+1), diviser par le mauvais écart d’indices, confondre avec une suite géométrique.
"""
import random
from fr_ly1 import *

R = random.Random(60603)


def terms(u0, r, k=4, start=0):
    return " ; ".join("%s = %s" % (U(start + i), d(u0 + i * r)) for i in range(k))


def s1():
    k = R.choice(["raison", "raison", "est", "suivant"])
    u0, r = R.randint(-15, 20), nz(R, -9, 9)
    if k == "raison":
        return M("Une suite arithmétique vérifie %s. Quelle est sa raison ?" % terms(u0, r), d(r), [d(-r), d(u0), d(r * 2), d(u0 + r)],
                 "r = %s − %s = <b>%s</b> (terme suivant moins terme précédent)." % (U(1), U(0), d(r)))
    if k == "suivant":
        return M("Une suite arithmétique a pour premiers termes %s. Que vaut %s ?" % (terms(u0, r, 3), U(4)), d(u0 + 4 * r), [d(u0 + 3 * r), d(u0 + 5 * r), d(u0 - 4 * r), d(4 * r), d(u0 + 2 * r)],
                 "r = %s, donc %s = %s + 2 × %s = <b>%s</b>." % (d(r), U(4), d(u0 + 2 * r), par(r), d(u0 + 4 * r)))
    q = R.choice([2, 3])
    seqs = [("%s ; %s ; %s ; %s" % (d(u0), d(u0 + r), d(u0 + 2 * r), d(u0 + 3 * r)), True)]
    a = R.randint(1, 4)
    bad = R.choice(["%s ; %s ; %s ; %s" % (a, a * q, a * q * q, a * q ** 3), "%s ; %s ; %s ; %s" % (a, a + 1, a + 3, a + 6), "%s ; %s ; %s ; %s" % (1, 4, 9, 16)])
    good = seqs[0][0]
    others = ["%s ; %s ; %s ; %s" % (a, a * q, a * q * q, a * q ** 3), "%s ; %s ; %s ; %s" % (a, a + 1, a + 3, a + 6), "1 ; 4 ; 9 ; 16", "%s ; %s ; %s ; %s" % (a, a + 2, a + 5, a + 7)]
    return M("Laquelle de ces listes peut être le début d’une suite arithmétique ?", good, others,
             "On passe d’un terme au suivant en ajoutant toujours %s : <b>%s</b>." % (d(r), good))


def s2():
    k = R.choice(["u0", "u0", "u1", "up", "expr"])
    u0, r = R.randint(-20, 30), nz(R, -8, 8)
    n = R.randint(10, 60)
    if k == "u0":
        return M("(u<sub>n</sub>) est arithmétique de premier terme %s = %s et de raison %s. Calcule %s." % (U(0), d(u0), d(r), U(n)), d(u0 + n * r),
                 [d(u0 + (n - 1) * r), d(u0 * r ** 1 + n), d(u0 + (n + 1) * r), d(n * r)], "%s = %s + n × r = %s + %d × %s = <b>%s</b>." % (U("n"), U(0), d(u0), n, par(r), d(u0 + n * r)))
    if k == "u1":
        return M("(u<sub>n</sub>) est arithmétique avec %s = %s et r = %s (la suite commence à %s). Calcule %s." % (U(1), d(u0), d(r), U(1), U(n)), d(u0 + (n - 1) * r),
                 [d(u0 + n * r), d(u0 + (n + 1) * r), d(n * r)], "%s = %s + (n − 1) × r = %s + %d × %s = <b>%s</b>." % (U("n"), U(1), d(u0), n - 1, par(r), d(u0 + (n - 1) * r)))
    if k == "up":
        p = R.randint(3, 9)
        return M("(u<sub>n</sub>) est arithmétique avec %s = %s et r = %s. Calcule %s." % (U(p), d(u0), d(r), U(n)), d(u0 + (n - p) * r),
                 [d(u0 + n * r), d(u0 + (n - p - 1) * r), d(u0 + (n + p) * r)], "%s = %s + (%d − %d) × r = %s + %d × %s = <b>%s</b>." % (U(n), U(p), n, p, d(u0), n - p, par(r), d(u0 + (n - p) * r)))
    ans = "%s = %s" % (U("n"), E((r, "n"), (u0, "")))
    return M("(u<sub>n</sub>) est arithmétique de premier terme %s = %s et de raison %s. Quelle est son expression ?" % (U(0), d(u0), d(r)), ans,
             ["%s = %s" % (U("n"), E((u0, "n"), (r, ""))) if u0 else "%s = %s" % (U("n"), E((r, ""))), "%s = %s" % (U("n"), E((r, "n"), (u0 - r, ""))), "%s = %s × %s<sup>n</sup>" % (U("n"), d(u0), par(r)), "%s = %s" % (U("n"), E((r, "n"), (u0 + r, "")))],
             "%s = %s + nr : <b>%s</b>." % (U("n"), U(0), ans))


def s3():
    r = nz(R, -7, 7)
    p, q_ = sorted(R.sample(range(0, 15), 2))
    if q_ - p < 2:
        return None
    up = R.randint(-20, 30)
    uq = up + (q_ - p) * r
    k = R.choice(["r", "r", "u0"])
    if k == "r":
        return M("(u<sub>n</sub>) est arithmétique avec %s = %s et %s = %s. Quelle est sa raison ?" % (U(p), d(up), U(q_), d(uq)), d(r),
                 [d(uq - up), fq(Fr(uq - up, q_ - p + 1)), fq(Fr(up - uq, q_ - p)) if r else "1", fq(Fr(uq, q_))],
                 "%s − %s = (%d − %d) × r, donc r = %s ÷ %d = <b>%s</b>." % (U(q_), U(p), q_, p, d(uq - up), q_ - p, d(r)))
    u0 = up - p * r
    return M("(u<sub>n</sub>) est arithmétique avec %s = %s et %s = %s. Calcule %s." % (U(p), d(up), U(q_), d(uq), U(0)), d(u0),
             [d(up + p * r), d(up - (p - 1) * r), d(uq - q_ * r + r), d(up)], "r = %s ÷ %d = %s, puis %s = %s − %d × %s = <b>%s</b>." % (d(uq - up), q_ - p, d(r), U(0), d(up), p, par(r), d(u0)))


def s4():
    k = R.choice(["var", "var", "aff", "graph", "seuil"])
    u0, r = R.randint(-10, 20), nz(R, -6, 6)
    if k == "var":
        ans = "croissante" if r > 0 else "décroissante"
        return M("(u<sub>n</sub>) est arithmétique de raison %s et %s = %s. Quel est son sens de variation ?" % (d(r), U(0), d(u0)), ans,
                 ["décroissante" if r > 0 else "croissante", "%s, car %s %s 0" % ("croissante" if u0 > 0 else "décroissante", U(0), "&gt;" if u0 > 0 else "⩽") if (u0 > 0) != (r > 0) else "constante", "constante", "on ne peut pas savoir"],
                 "u<sub>n+1</sub> − u<sub>n</sub> = r = %s : la suite est <b>%s</b> (seul le signe de r compte)." % (d(r), ans))
    if k == "aff":
        a, b = nz(R, -9, 9), R.randint(-12, 12)
        return M("La suite définie par %s = %s est arithmétique. Quelle est sa raison ?" % (U("n"), E((a, "n"), (b, ""))), d(a), [d(b), d(a + b), d(-a), d(2 * a), d(b - a)],
                 "%s − %s = (%s) − (%s) = <b>%s</b> : c’est le coefficient de n." % (U("n+1"), U("n"), E((a, "n"), (a + b, "")), E((a, "n"), (b, "")), d(a)))
    if k == "graph":
        r = R.choice([-2, -1, 1, 2])
        u0 = R.randint(-3, 3)
        pts = [(i, u0 + i * r, "") for i in range(5)]
        svg = relabel(kosy(pts=pts, lo=-5, hi=5, u=22), "termes d’une suite")
        return M("<div class='qfig'>%s</div>Les points représentent u<sub>0</sub>, …, u<sub>4</sub>. Ils sont alignés. Quelle est la raison de la suite ?" % svg, d(r), [d(-r), d(u0) if u0 not in (r, -r) else d(2 * r), "0"],
                 "On passe d’un point au suivant en %s de %d : r = <b>%s</b>." % ("montant" if r > 0 else "descendant", abs(r), d(r)))
    u0, r = R.randint(1, 20), R.randint(3, 9)
    s_ = R.randint(80, 300)
    n = -(-(s_ - u0) // r)
    if u0 + n * r == s_:
        n += 1
    return M("%s = %d et %s = %s + %d. À partir de quel rang n a-t-on %s &gt; %d ?" % (U(0), u0, U("n+1"), U("n"), r, U("n"), s_), "n = %d" % n, ["n = %d" % (n - 1), "n = %d" % (n + 1), "n = %d" % (s_ // r), "n = %d" % (n + 2), "n = %d" % (s_ // r + 2)],
             "%s = %d + %dn &gt; %d ⇔ n &gt; %s ; le premier entier est <b>n = %d</b>." % (U("n"), u0, r, s_, fq(Fr(s_ - u0, r)), n))


def s5():
    k = R.choice(["sal", "theatre", "epargne", "course", "loyer"])
    if k == "sal":
        a, r, n = R.randint(18, 26) * 100, R.choice([40, 50, 60, 75, 80]), R.randint(5, 12)
        return M("Un salaire mensuel est de %s € la première année (année 1). Il augmente de %d € chaque année. Quel est le salaire de l’année %d ?" % (num(a), r, n), euro(a + (n - 1) * r),
                 [euro(a + n * r), euro(a + r), euro(a + (n + 1) * r)], "Année n : %s + (n − 1) × %d. Année %d : <b>%s</b>." % (num(a), r, n, euro(a + (n - 1) * r)))
    if k == "theatre":
        a, r, n = R.randint(12, 24), R.choice([2, 3]), R.randint(10, 25)
        return M("Dans un théâtre, la rangée 1 compte %d sièges et chaque rangée a %d sièges de plus que la précédente. Combien de sièges dans la rangée %d ?" % (a, r, n), str(a + (n - 1) * r),
                 [str(a + n * r), str(a * n), str(a + (n - 2) * r)], "%d + (%d − 1) × %d = <b>%d</b>." % (a, n, r, a + (n - 1) * r))
    if k == "epargne":
        a, r, n = R.randint(1, 8) * 50, R.choice([20, 25, 30, 40]), R.randint(6, 24)
        return M("Léa a %d € sur un compte en janvier (mois 0) et y ajoute %d € chaque mois. Combien a-t-elle au mois %d ?" % (a, r, n), euro(a + n * r), [euro(a + (n - 1) * r), euro(n * r), euro((a + r) * n)],
                 "%s = %d + %d × %d = <b>%s</b>." % (U(n), a, r, n, euro(a + n * r)))
    if k == "loyer":
        a, r = R.randint(55, 90) * 10, R.choice([15, 20, 25, 30])
        target = a + R.randint(4, 10) * r
        n = (target - a) // r
        return M("Un loyer de %d € augmente de %d € par an. Au bout de combien d’années atteindra-t-il %d € ?" % (a, r, target), pl(n, "an"), [pl(n + 1, "an"), pl(n - 1, "an"), pl(target // r, "an")],
                 "%d + %dn = %d ⇔ n = %d ÷ %d = <b>%d</b>." % (a, r, target, target - a, r, n))
    a, r, n = R.randint(2, 6), R.choice([Fr(1, 2), 1, Fr(3, 2)]), R.randint(6, 12)
    return M("Un coureur court %s km la semaine 1 et ajoute %s km chaque semaine. Combien court-il la semaine %d ?" % (d(a), d(r), n), d(a + (n - 1) * r) + NB + "km",
             [d(a + n * r) + NB + "km", d(a * n) + NB + "km", d(a + (n - 2) * r) + NB + "km"], "%s + (%d − 1) × %s = <b>%s km</b>." % (d(a), n, d(r), d(a + (n - 1) * r)))


def main():
    seen = set()
    sets = [("Reconnaître une suite arithmétique", mix(R, seen, [(s1, 20)])), ("Terme général", mix(R, seen, [(s2, 20)])),
            ("Trouver la raison et le premier terme", mix(R, seen, [(s3, 20)])), ("Variations, représentation et seuil", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Une suite est <b>arithmétique</b> quand on passe d’un terme au suivant en ajoutant toujours le même nombre r (la raison) : u<sub>n+1</sub> = u<sub>n</sub> + r.",
              "Terme général : u<sub>n</sub> = u<sub>0</sub> + nr, et plus généralement u<sub>n</sub> = u<sub>p</sub> + (n − p)r.",
              "Si r &gt; 0, la suite est croissante ; si r &lt; 0, décroissante. Ses points sont alignés : c’est la version discrète d’une fonction affine."],
             [("u<sub>3</sub> = 11 et u<sub>8</sub> = 26", ["u<sub>8</sub> − u<sub>3</sub> = 5r = 15, donc r = 3", "u<sub>0</sub> = 11 − 3 × 3 = 2"], "u<sub>n</sub> = 2 + 3n")],
             [["u<sub>n</sub> = u<sub>0</sub> + (n − 1)r", "Avec u<sub>0</sub> : u<sub>0</sub> + nr. Le « n − 1 » sert quand on part de u<sub>1</sub>."],
              ["r = (u<sub>8</sub> − u<sub>3</sub>) ÷ 8", "On divise par l’écart d’indices : 8 − 3 = 5."], ["La suite est croissante car u<sub>0</sub> &gt; 0", "Seul le signe de r compte."]])
    faq = [("Comment montrer qu’une suite est arithmétique ?", "On calcule u<sub>n+1</sub> − u<sub>n</sub> : si le résultat est un nombre qui ne dépend pas de n, la suite est arithmétique de raison ce nombre."),
           ("Quel lien avec les fonctions affines ?", "u<sub>n</sub> = u<sub>0</sub> + nr = f(n) avec f(x) = rx + u<sub>0</sub> : les points (n ; u<sub>n</sub>) sont sur une droite de coefficient directeur r.")]
    unit("premiere", R, "suites-arithmetiques", "A",
         "Suites arithmétiques : relation de récurrence, terme général, sens de variation ; lien avec les fonctions affines ; modéliser une croissance linéaire",
         "Suites arithmétiques : raison, terme général et variations", "Suites arithmétiques",
         "Fiches de maths première sur les suites arithmétiques : raison, terme général, premier terme, sens de variation, seuil et problèmes de croissance linéaire. 100 exercices corrigés.",
         "Suite arithmétique : u(n) = u(0) + nr", "On ajoute toujours la même raison r", body, faq, sets, 3)


if __name__ == "__main__":
    main()
