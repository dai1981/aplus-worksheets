# -*- coding: utf-8 -*-
"""
France Maths 4e : Théorème de la droite des milieux (et réciproque)
  python3 tools/gen_fr_maths_4e_droite_des_milieux.py
Erreurs : MN = BC au lieu de BC ÷ 2, appliquer le théorème sans deux milieux, confondre théorème et réciproque.
"""
import random
from fr_c4 import *

R = random.Random(60312)
K = Kids(R)
LET = ["ABC", "EFG", "RST", "KLM", "DEF", "PQR", "IJK", "UVW"]
MID = ["MN", "IJ", "PQ", "UV", "XY"]


def tri():
    L = R.choice(LET)
    m = R.choice([x for x in MID if not set(x) & set(L)])
    A, B, C = L
    ax, ay = R.uniform(1.5, 4.5), R.uniform(3.2, 4.5)
    pts = {A: (ax, ay), B: (0, 0), C: (6, 0)}
    return L, m, pts


def fig_mid(L, m, pts, sides, which="AB-AC", ticks=True):
    A, B, C = L
    M_, N = m
    (ax, ay), (bx, by), (cx, cy) = pts[A], pts[B], pts[C]
    P = dict(pts)
    P[M_] = ((ax + bx) / 2, (ay + by) / 2)
    P[N] = ((ax + cx) / 2, (ay + cy) / 2)
    tk = [(A, M_, 1), (M_, B, 1), (A, N, 2), (N, C, 2)] if ticks else []
    return figure(P, [(A, B), (B, C), (C, A), (M_, N)], sides, ticks=tk, label="triangle et segment des milieux")


def s1():
    L, m, pts = tri()
    A, B, C = L
    M_, N = m
    bc = R.choice([R.randint(4, 30), Fr(R.randint(41, 199), 10)])
    if R.random() < 0.5:
        svg = fig_mid(L, m, pts, [(B, C, "%s cm" % d(bc))])
        return M("<div class='qfig'>%s</div>%s est le milieu de [%s%s] et %s est le milieu de [%s%s]. Combien mesure %s ?" % (svg, M_, A, B, N, A, C, m), "%s cm" % d(Fr(bc) / 2),
                 ["%s cm" % d(bc), "%s cm" % d(Fr(bc) * 2), "%s cm" % d(Fr(bc) / 2 + 1)], "D’après le théorème de la droite des milieux, %s = %s%s ÷ 2 = <b>%s cm</b>." % (m, B, C, d(Fr(bc) / 2)))
    mn = bc
    svg = fig_mid(L, m, pts, [(M_, N, "%s cm" % d(mn))])
    return M("<div class='qfig'>%s</div>%s est le milieu de [%s%s] et %s est le milieu de [%s%s]. Combien mesure %s%s ?" % (svg, M_, A, B, N, A, C, B, C), "%s cm" % d(Fr(mn) * 2),
             ["%s cm" % d(mn), "%s cm" % d(Fr(mn) / 2), "%s cm" % d(Fr(mn) + 2)], "%s = %s%s ÷ 2, donc %s%s = 2 × %s = <b>%s cm</b>." % (m, B, C, B, C, d(mn), d(Fr(mn) * 2)))


def s2():
    L = R.choice(LET)
    A, B, C = L
    m = R.choice([x for x in MID if not set(x) & set(L)])
    M_, N = m
    V = [("Dans le triangle %s, %s est le milieu de [%s%s] et %s celui de [%s%s]. Que peut-on dire des droites (%s) et (%s%s) ?" % (L, M_, A, B, N, A, C, m, B, C), "elles sont parallèles", ["elles sont perpendiculaires", "elles se coupent en %s" % B, "on ne peut rien dire"]),
         ("Pour utiliser le théorème de la droite des milieux dans le triangle %s, il faut savoir que…" % L, "%s et %s sont les milieux de deux côtés" % (M_, N), ["%s et %s sont sur deux côtés" % (M_, N), "(%s) est parallèle à un côté" % m, "le triangle est rectangle"]),
         ("Dans le triangle %s, %s est le milieu de [%s%s] et la droite passant par %s parallèle à (%s%s) coupe [%s%s] en %s. Que peut-on dire de %s ?" % (L, M_, A, B, M_, B, C, A, C, N, N), "%s est le milieu de [%s%s]" % (N, A, C), ["%s = %s" % (N, C), "%s%s = %s%s" % (M_, N, B, C), "on ne peut rien dire"]),
         ("Quelle phrase énonce le théorème de la droite des milieux ?", "Dans un triangle, le segment qui joint les milieux de deux côtés est parallèle au troisième côté et mesure sa moitié.",
          ["Dans un triangle, une droite parallèle à un côté passe par les milieux des deux autres côtés.", "Dans un triangle, les milieux des trois côtés sont alignés.", "Dans un triangle, le segment qui joint deux milieux mesure le double du troisième côté."]),
         ("%s est le milieu de [%s%s] et %s est sur [%s%s] avec (%s) parallèle à (%s%s). Quel résultat utilise-t-on pour montrer que %s est le milieu de [%s%s] ?" % (M_, A, B, N, A, C, m, B, C, N, A, C), "la réciproque de la droite des milieux (droite parallèle passant par un milieu)",
          ["le théorème de Pythagore", "la droite des milieux (les deux milieux sont connus)", "la symétrie axiale"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3():
    L, m, pts = tri()
    A, B, C = L
    M_, N = m
    ab, ac = R.randint(4, 20), R.randint(4, 20)
    k = R.choice(["recip", "recip", "perim"])
    if k == "recip":
        P = dict(pts)
        (ax, ay), (bx, by), (cx, cy) = pts[A], pts[B], pts[C]
        P[M_] = ((ax + bx) / 2, (ay + by) / 2)
        P[N] = ((ax + cx) / 2, (ay + cy) / 2)
        svg = figure(P, [(A, B), (B, C), (C, A), (M_, N)], [(A, C, "%d cm" % ac)], ticks=[(A, M_, 1), (M_, B, 1)], label="triangle avec une parallèle")
        return M("<div class='qfig'>%s</div>%s est le milieu de [%s%s] et (%s) est parallèle à (%s%s). Combien mesure %s%s ?" % (svg, M_, A, B, m, B, C, A, N), "%s cm" % d(Fr(ac, 2)),
                 ["%d cm" % ac, "%d cm" % (2 * ac), "on ne peut pas savoir"], "D’après la réciproque, %s est le milieu de [%s%s] : %s%s = %d ÷ 2 = <b>%s cm</b>." % (N, A, C, A, N, ac, d(Fr(ac, 2))))
    bc = R.randint(4, 20)
    if not (abs(ab - ac) < bc < ab + ac):
        return None
    per = Fr(ab + ac + bc, 2)
    return M("Le triangle %s a pour côtés %s%s = %d cm, %s%s = %d cm et %s%s = %d cm. On joint les milieux des trois côtés. Quel est le périmètre du petit triangle obtenu ?" % (L, A, B, ab, A, C, ac, B, C, bc), "%s cm" % d(per),
             ["%d cm" % (ab + ac + bc), "%s cm" % d(Fr(ab + ac + bc, 4)), "%d cm" % (2 * (ab + ac + bc))], "Chaque côté du petit triangle mesure la moitié d’un côté du grand : (%d + %d + %d) ÷ 2 = <b>%s cm</b>." % (ab, ac, bc, d(per)))


def s4():
    k = R.choice(["quadri", "trap", "coord"])
    if k == "coord":
        ax, ay = 2 * R.randint(-3, 3), 2 * R.randint(-3, 3)
        bx, by = 2 * R.randint(-3, 3), 2 * R.randint(-3, 3)
        if (ax, ay) == (bx, by):
            return None
        return M("A%s et B%s. Quelles sont les coordonnées du milieu de [AB] ?" % ("(%s ; %s)" % (d(ax), d(ay)), "(%s ; %s)" % (d(bx), d(by))), "(%s ; %s)" % (d(Fr(ax + bx, 2)), d(Fr(ay + by, 2))),
                 ["(%s ; %s)" % (d(ax + bx), d(ay + by)), "(%s ; %s)" % (d(Fr(bx - ax, 2)), d(Fr(by - ay, 2))), "(%s ; %s)" % (d(Fr(ax + ay, 2)), d(Fr(bx + by, 2)))],
                 "On fait la moyenne des abscisses et des ordonnées : <b>(%s ; %s)</b>." % (d(Fr(ax + bx, 2)), d(Fr(ay + by, 2))))
    if k == "quadri":
        dg = R.randint(6, 30)
        return M("ABCD est un quadrilatère dont la diagonale [AC] mesure %d cm. I, J, K, L sont les milieux de [AB], [BC], [CD] et [DA]. Combien mesure IJ ?" % dg, "%s cm" % d(Fr(dg, 2)),
                 ["%d cm" % dg, "%s cm" % d(Fr(dg, 4)), "%d cm" % (2 * dg)], "Dans le triangle ABC, I et J sont des milieux : IJ = AC ÷ 2 = <b>%s cm</b>." % d(Fr(dg, 2)))
    h = R.randint(4, 20)
    return M("Dans le triangle ABC, I est le milieu de [AB] et J le milieu de [AC]. La hauteur issue de A mesure %d cm. À quelle distance de (BC) se trouve la droite (IJ) ?" % (2 * h), "%d cm" % h, ["%d cm" % (2 * h), "%d cm" % (4 * h), "%s cm" % d(Fr(h, 2))],
             "(IJ) est parallèle à (BC) et passe à mi-hauteur : <b>%d cm</b>." % h)


def s5():
    k = R.choice(["toit", "echelle", "reprod", "pont"])
    a = R.randint(3, 15) * 2
    if k == "toit":
        return M("La façade d’un chalet est un triangle dont la base mesure %d m. Une poutre horizontale relie les milieux des deux côtés du toit. Combien mesure-t-elle ?" % a, "%s m" % d(Fr(a, 2)),
                 ["%d m" % a, "%s m" % d(Fr(a, 4)), "%d m" % (a + 2)], "Droite des milieux : %d ÷ 2 = <b>%s m</b>." % (a, d(Fr(a, 2))))
    if k == "echelle":
        return M("Une échelle double ouverte forme un triangle avec le sol ; ses pieds sont écartés de %d dm. Une barre de sécurité relie les milieux des deux montants. Quelle est sa longueur ?" % a, "%s dm" % d(Fr(a, 2)),
                 ["%d dm" % a, "%d dm" % (2 * a), "%s dm" % d(Fr(a, 3)) if a % 3 == 0 else "%s dm" % d(Fr(a, 2) + 1)], "La barre joint deux milieux : <b>%s dm</b>." % d(Fr(a, 2)))
    if k == "reprod":
        return M("Pour mesurer la largeur BC d’un étang, on plante A, puis on mesure IJ où I et J sont les milieux de [AB] et [AC]. On trouve IJ = %d m. Quelle est la largeur BC ?" % a, "%d m" % (2 * a),
                 ["%d m" % a, "%s m" % d(Fr(a, 2)), "%d m" % (a + 2)], "BC = 2 × IJ = <b>%d m</b>." % (2 * a))
    return M("Un panneau triangulaire a une base de %d cm. On trace le segment qui joint les milieux de deux côtés, puis, dans le petit triangle du haut, encore le segment des milieux. Combien mesure ce dernier segment ?" % (2 * a), "%s cm" % d(Fr(a, 2)),
             ["%d cm" % a, "%s cm" % d(Fr(a, 4)), "%d cm" % (2 * a)], "On divise deux fois par 2 : %d ÷ 4 = <b>%s cm</b>." % (2 * a, d(Fr(a, 2))))


def main():
    seen = set()
    sets = [("Calculer une longueur", mix(R, seen, [(s1, 20)])), ("Énoncés et vocabulaire", mix(R, seen, [(s2, 20)])),
            ("Réciproque et périmètres", mix(R, seen, [(s3, 20)])), ("Milieux dans d’autres figures", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Théorème</b> : dans un triangle, le segment qui joint les milieux de deux côtés est parallèle au troisième côté et mesure la moitié de sa longueur.",
              "<b>Réciproque</b> : dans un triangle, la droite qui passe par le milieu d’un côté et qui est parallèle à un deuxième côté coupe le troisième côté en son milieu.",
              "On vérifie toujours les hypothèses : deux milieux pour le théorème, un milieu et une parallèle pour la réciproque."],
             [("ABC, M milieu de [AB], N milieu de [AC], BC = 9 cm", ["(MN) // (BC)", "MN = BC ÷ 2"], "MN = 4,5 cm")],
             [["MN = BC", "MN mesure la moitié de BC."], ["Utiliser le théorème avec un seul milieu", "Avec un seul milieu, il faut aussi une parallèle (réciproque)."],
              ["Oublier de justifier", "On cite le théorème : « Dans le triangle …, … »."]])
    faq = [("Quelle différence entre le théorème et sa réciproque ?", "Le théorème part de deux milieux et conclut au parallélisme et à la longueur ; la réciproque part d’un milieu et d’une parallèle et conclut à un milieu."),
           ("À quoi sert ce théorème ?", "À calculer des longueurs ou à prouver que deux droites sont parallèles.")]
    unit("4e", R, "droite-des-milieux", "E",
         "Connaître et utiliser le théorème de la droite des milieux et sa réciproque pour calculer une longueur, démontrer un parallélisme ou montrer qu’un point est un milieu",
         "Théorème de la droite des milieux", "Droite des milieux",
         "Fiches de maths 4e sur la droite des milieux : théorème, réciproque, calcul de longueurs, périmètres et problèmes, avec figures. 100 exercices corrigés.",
         "Le segment des milieux est parallèle au 3e côté", "Il mesure la moitié de ce côté", body, faq, sets, 12)


if __name__ == "__main__":
    main()
