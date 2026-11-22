# -*- coding: utf-8 -*-
"""
France Maths 3e : Théorème de Thalès (configuration emboîtée et papillon), réciproque et contraposée
  python3 tools/gen_fr_maths_3e_theoreme_de_thales.py
Erreurs : mal associer les côtés (AM/MB au lieu de AM/AB), utiliser Thalès sans droites parallèles, inverser le produit en croix.
"""
import random
from fr_c4 import *

R = random.Random(60410)
K = Kids(R)
NM = [("A", "B", "C", "M", "N"), ("O", "E", "F", "R", "S"), ("S", "T", "U", "K", "L"), ("P", "Q", "R", "E", "F"), ("D", "E", "F", "G", "H")]


def thfig(n, k, labels, butterfly=False):
    A, B, C, M_, N = n
    pts = {A: (2.6, 4.2), B: (0, 0), C: (6.2, 0)}
    (ax, ay), (bx, by), (cx, cy) = pts[A], pts[B], pts[C]
    if not butterfly:
        pts[M_] = (ax + (bx - ax) * k, ay + (by - ay) * k)
        pts[N] = (ax + (cx - ax) * k, ay + (cy - ay) * k)
        segs = [(A, B), (A, C), (B, C), (M_, N)]
    else:
        pts[M_] = (ax - (bx - ax) * k, ay - (by - ay) * k)
        pts[N] = (ax - (cx - ax) * k, ay - (cy - ay) * k)
        segs = [(M_, B), (N, C), (B, C), (M_, N)]
    return figure(pts, segs, [], label="configuration de Thalès", W=320, H=260)


def tri():
    n = R.choice(NM)
    ab = R.choice([4, 5, 6, 8, 9, 10, 12, 15])
    k = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5)])
    return n, ab, k


def s1():
    n, ab, k = tri()
    A, B, C, M_, N = n
    am = ab * k
    bc = R.choice([6, 8, 9, 10, 12, 14, 15, 20])
    mn = bc * k
    if (am * 10).denominator != 1 or (mn * 10).denominator != 1:
        return None
    svg = thfig(n, float(k), [(A, M_, "%s" % d(am)), (A, B, "%s" % d(ab)), (B, C, "%s" % d(bc))])
    return M("<div class='qfig'>%s</div>(%s%s) // (%s%s), %s%s = %s cm, %s%s = %s cm, %s%s = %s cm. Calcule %s%s." % (svg, M_, N, B, C, A, M_, d(am), A, B, d(ab), B, C, d(bc), M_, N), "%s cm" % d(mn),
             ["%s cm" % d(bc * ab / am) if (bc * ab / am * 10).denominator == 1 else "%s cm" % d(mn + 1), "%s cm" % d(bc * am / (ab - am)) if (bc * am / (ab - am) * 10).denominator == 1 and bc * am / (ab - am) != mn else "%s cm" % d(mn * 2), "%s cm" % d(bc - (ab - am))],
             "D’après le théorème de Thalès : %s%s/%s%s = %s%s/%s%s, donc %s%s = %s × %s ÷ %s = <b>%s cm</b>." % (A, M_, A, B, M_, N, B, C, M_, N, d(bc), d(am), d(ab), d(mn)))


def s2():
    n, ab, k = tri()
    A, B, C, M_, N = n
    am = ab * k
    ac = R.choice([6, 8, 9, 10, 12, 14, 15, 20])
    an = ac * k
    if (am * 10).denominator != 1 or (an * 10).denominator != 1:
        return None
    q = R.choice(["AC", "AN"])
    if q == "AC":
        svg = thfig(n, float(k), [(A, M_, d(am)), (A, B, d(ab)), (A, N, d(an))])
        return M("<div class='qfig'>%s</div>(%s%s) // (%s%s), %s%s = %s, %s%s = %s, %s%s = %s (en cm). Calcule %s%s." % (svg, M_, N, B, C, A, M_, d(am), A, B, d(ab), A, N, d(an), A, C), "%s cm" % d(ac),
                 ["%s cm" % d(an * am / ab) if (an * am / ab * 10).denominator == 1 and an * am / ab != ac else "%s cm" % d(ac + 1), "%s cm" % d(an + ab - am), "%s cm" % d(an * 2) if an * 2 != ac else "%s cm" % d(ac + 2)],
                 "%s%s/%s%s = %s%s/%s%s, donc %s%s = %s × %s ÷ %s = <b>%s cm</b>." % (A, M_, A, B, A, N, A, C, A, C, d(an), d(ab), d(am), d(ac)))
    svg = thfig(n, float(k), [(A, M_, d(am)), (A, B, d(ab)), (A, C, d(ac))])
    return M("<div class='qfig'>%s</div>(%s%s) // (%s%s), %s%s = %s, %s%s = %s, %s%s = %s (en cm). Calcule %s%s." % (svg, M_, N, B, C, A, M_, d(am), A, B, d(ab), A, C, d(ac), A, N), "%s cm" % d(an),
             ["%s cm" % d(ac * ab / am) if (ac * ab / am * 10).denominator == 1 else "%s cm" % d(an + 1), "%s cm" % d(ac - (ab - am)), "%s cm" % d(ac * am / (ab - am)) if (ac * am / (ab - am) * 10).denominator == 1 and ac * am / (ab - am) != an else "%s cm" % d(an * 2)],
             "%s%s/%s%s = %s%s/%s%s, donc %s%s = %s × %s ÷ %s = <b>%s cm</b>." % (A, M_, A, B, A, N, A, C, A, N, d(ac), d(am), d(ab), d(an)))


def s3():
    n, ab, k = tri()
    A, B, C, M_, N = n
    k = R.choice([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(3, 5), Fr(1, 3)])
    am = ab * k
    bc = R.choice([6, 8, 9, 10, 12, 15])
    mn = bc * k
    if (am * 10).denominator != 1 or (mn * 10).denominator != 1:
        return None
    svg = thfig(n, float(k), [(A, M_, d(am)), (A, B, d(ab)), (M_, N, d(mn))], butterfly=True)
    return M("<div class='qfig'>%s</div>Les droites (%s%s) et (%s%s) se coupent en %s, et (%s%s) // (%s%s). %s%s = %s, %s%s = %s, %s%s = %s (en cm). Calcule %s%s." % (svg, B, M_, C, N, A, M_, N, B, C, A, M_, d(am), A, B, d(ab), M_, N, d(mn), B, C), "%s cm" % d(bc),
             ["%s cm" % d(mn * am / ab) if (mn * am / ab * 10).denominator == 1 else "%s cm" % d(bc + 1), "%s cm" % d(mn + ab - am), "%s cm" % d(mn * (ab + am) / am) if (mn * (ab + am) / am * 10).denominator == 1 and mn * (ab + am) / am != bc else "%s cm" % d(bc * 2)],
             "Configuration « papillon » : %s%s/%s%s = %s%s/%s%s, donc %s%s = %s × %s ÷ %s = <b>%s cm</b>." % (A, M_, A, B, M_, N, B, C, B, C, d(mn), d(ab), d(am), d(bc)))


def s4():
    n = R.choice(NM)
    A, B, C, M_, N = n
    am, ab = R.choice([(3, 5), (2, 6), (4, 10), (6, 9), (5, 8), (3, 7)])
    an_ok = R.random() < 0.5
    ac = R.choice([10, 12, 14, 15, 18, 20])
    an = Fr(ac * am, ab) if an_ok else Fr(ac * am, ab) + Fr(R.choice([-1, 1]), 2)
    if (an * 10).denominator != 1:
        return None
    ans = "oui, (%s%s) // (%s%s)" % (M_, N, B, C) if an_ok else "non, elles ne sont pas parallèles"
    return M("%s, %s, %s sont alignés dans cet ordre, ainsi que %s, %s, %s. %s%s = %d, %s%s = %d, %s%s = %s, %s%s = %d (en cm). Les droites (%s%s) et (%s%s) sont-elles parallèles ?" % (A, M_, B, A, N, C, A, M_, am, A, B, ab, A, N, d(an), A, C, ac, M_, N, B, C),
             ans, ["non, elles ne sont pas parallèles" if an_ok else "oui, (%s%s) // (%s%s)" % (M_, N, B, C), "on ne peut pas savoir sans mesurer les angles", "oui, car les points sont alignés"],
             "%s%s/%s%s = %s et %s%s/%s%s = %s : %s." % (A, M_, A, B, fq(Fr(am, ab)), A, N, A, C, fq(an / ac), "égaux, d’après la réciproque de Thalès <b>les droites sont parallèles</b>" if an_ok else "différents, d’après la contraposée <b>elles ne sont pas parallèles</b>"))


def s5():
    k = R.choice(["arbre", "pont", "ombre", "toit"])
    if k == "arbre":
        b, h, ob = R.choice([(1, 2, 6), (2, 3, 8), (1, Fr(3, 2), 10), (2, Fr(5, 2), 12)])
        H = h * ob / b
        return M("Un bâton vertical de %s m projette une ombre de %s m. Au même moment, un arbre projette une ombre de %s m. Quelle est la hauteur de l’arbre ?" % (d(h), d(b), d(ob)), "%s m" % d(H), ["%s m" % d(ob * b / h), "%s m" % d(h + ob - b), "%s m" % d(ob * h)],
                 "Les rayons du soleil sont parallèles : hauteur ÷ ombre = %s ÷ %s, donc H = %s × %s ÷ %s = <b>%s m</b>." % (d(h), d(b), d(h), d(ob), d(b), d(H)))
    if k == "pont":
        a, b, c = R.choice([(4, 12, 3), (5, 15, 4), (6, 18, 5), (3, 9, 2)])
        return M("Pour mesurer la largeur d’une rivière, on place des repères : avec (DE) // (BC), AD = %d m, AB = %d m et DE = %d m. Quelle est la largeur BC ?" % (a, b, c), "%d m" % (c * b // a), ["%s m" % d(Fr(c * a, b)), "%d m" % (c + b - a), "%d m" % (c * b)],
                 "AD/AB = DE/BC, donc BC = %d × %d ÷ %d = <b>%d m</b>." % (c, b, a, c * b // a))
    if k == "ombre":
        h, dd = R.choice([(Fr(16, 10), 2), (Fr(18, 10), 3), (Fr(15, 10), 4), (Fr(17, 10), 5)])
        return M("%s (%s m) se tient à %d m d’un lampadaire et son ombre mesure %d m. La lampe, l’extrémité de l’ombre et le haut de la tête sont alignés. Quelle est la hauteur du lampadaire ?" % (K.next()[0], d(h), 2 * dd, dd), "%s m" % d(h * 3), ["%s m" % d(h * 2), "%s m" % d(h + 2 * dd), "%s m" % d(h * Fr(3, 2))],
                 "Ombre totale : %d + %d = %d m ; rapport %d ÷ %d = 3 ; hauteur = %s × 3 = <b>%s m</b>." % (2 * dd, dd, 3 * dd, 3 * dd, dd, d(h), d(h * 3)))
    a, b = R.choice([(2, 6), (3, 9), (1, 4)])
    return M("Un toit triangulaire a une hauteur de %d m. Une poutre horizontale est placée à %d m du sommet, parallèle à la base de %d m. Quelle est la longueur de la poutre ?" % (b, a, b * 2), "%s m" % d(Fr(a * b * 2, b)), ["%s m" % d(Fr(b * 2 * b, a)), "%d m" % (b * 2 - a), "%s m" % d(Fr(a * 2, 1))] if Fr(a * 2, 1) != Fr(a * b * 2, b) else ["%s m" % d(Fr(b * 2 * b, a)), "%d m" % (b * 2 - a), "%d m" % (b * 2 - 2 * a)],
             "Les longueurs sont proportionnelles : %d/%d = poutre/%d, donc poutre = <b>%s m</b>." % (a, b, b * 2, d(Fr(a * b * 2, b))))


def main():
    seen = set()
    sets = [("Calculer un côté parallèle", mix(R, seen, [(s1, 20)])), ("Calculer sur les côtés", mix(R, seen, [(s2, 20)])),
            ("Configuration papillon", mix(R, seen, [(s3, 20)])), ("Réciproque et contraposée", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["<b>Théorème de Thalès</b> : si M ∈ (AB), N ∈ (AC) et (MN) // (BC), alors AM/AB = AN/AC = MN/BC.",
              "Les configurations peuvent être emboîtées (triangles l’un dans l’autre) ou en « papillon » (sommet commun entre les deux triangles).",
              "<b>Réciproque</b> : si A, M, B et A, N, C sont alignés dans le même ordre et AM/AB = AN/AC, alors (MN) // (BC). Si les rapports sont différents, les droites ne sont pas parallèles (contraposée)."],
             [("AM = 3, AB = 5, BC = 8, (MN) // (BC)", ["AM/AB = MN/BC", "3/5 = MN/8"], "MN = 4,8")],
             [["Écrire AM/MB = MN/BC", "On compare les côtés des deux triangles : AM/AB."], ["Utiliser Thalès sans parallèles", "Il faut savoir que (MN) // (BC)."],
              ["Oublier l’ordre des points pour la réciproque", "Les points doivent être alignés dans le même ordre."]])
    faq = [("Comment écrire les rapports ?", "Petit triangle en haut, grand triangle en bas : AM/AB = AN/AC = MN/BC (les sommets correspondants dans le même ordre)."),
           ("Quel lien avec les agrandissements ?", "Le triangle AMN est une réduction (ou un agrandissement) du triangle ABC de rapport AM/AB.")]
    unit("3e", R, "theoreme-de-thales", "E",
         "Connaître et utiliser le théorème de Thalès (configurations emboîtée et papillon) pour calculer des longueurs ; utiliser sa réciproque et sa contraposée pour démontrer que des droites sont ou ne sont pas parallèles ; résoudre des problèmes",
         "Théorème de Thalès", "Théorème de Thalès",
         "Fiches de maths 3e sur le théorème de Thalès : calculer des longueurs, configuration papillon, réciproque, contraposée et problèmes, avec figures. 100 exercices corrigés.",
         "(MN) // (BC) : AM/AB = AN/AC = MN/BC", "Réciproque : rapports égaux → droites parallèles", body, faq, sets, 10)


if __name__ == "__main__":
    main()
