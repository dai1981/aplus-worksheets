# -*- coding: utf-8 -*-
"""
France Maths Première (spécialité) : Formule d’Al-Kashi et applications du produit scalaire (longueurs, angles, développements, bilinéarité, ensemble des points M tels que MA · MB = 0)
  python3 tools/gen_fr_maths_premiere_al_kashi_et_applications_du_produit_scalaire.py
Erreurs : a² = b² + c² + 2bc cos A, oublier la racine carrée, ‖u + v‖² = ‖u‖² + ‖v‖², confondre le centre du cercle avec A ou B.
"""
import math
import random
from fr_ly1 import *

R = random.Random(60617)


def V(s):
    return "<span class='vec'>%s</span>" % s


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def tri_svg(b, c, ang_deg, show="sides"):
    import math as m_
    A = (0, 0)
    B = (c, 0)
    C = (b * m_.cos(m_.radians(ang_deg)), b * m_.sin(m_.radians(ang_deg)))
    return figure({"A": A, "B": B, "C": C}, [("A", "B"), ("B", "C"), ("C", "A")], sides=[("A", "B", "%s" % d(c)), ("A", "C", "%s" % d(b))], W=340, H=220, label="triangle ABC")


def s1():
    b, c = R.randint(2, 10), R.randint(2, 10)
    ang, cs = R.choice([(60, Fr(1, 2)), (120, Fr(-1, 2)), (90, 0), (60, Fr(1, 2))])
    a2 = b * b + c * c - 2 * b * c * cs
    a2 = int(a2)
    ans = sq(a2)
    fig = tri_svg(b, c, ang)
    return M("<div class='qfig'>%s</div>AB = %d, AC = %d et l’angle BAC mesure %d°. Calcule BC." % (fig, c, b, ang), ans,
             [sq(int(b * b + c * c + 2 * b * c * cs)) if b * b + c * c + 2 * b * c * cs > 0 and int(b * b + c * c + 2 * b * c * cs) != a2 else d(b + c), d(a2), sq(b * b + c * c) if cs else sq(b * b + c * c + b * c), d(abs(b - c)) if b != c else d(b + 1)],
             "Al-Kashi : BC² = AB² + AC² − 2 × AB × AC × cos(%d°) = %d + %d − 2 × %d × %d × %s = %d, donc <b>BC = %s</b>." % (ang, c * c, b * b, c, b, "(" + fq(cs) + ")" if cs < 0 else fq(cs), a2, ans))


def s2():
    T = [(3, 5, 7, 120), (5, 7, 8, 60), (3, 4, 5, 90), (5, 3, 7, 120), (8, 3, 7, 60), (7, 8, 13, 120), (5, 12, 13, 90), (5, 8, 7, 60), (8, 5, 7, 60), (6, 10, 14, 120), (10, 16, 14, 60), (6, 8, 10, 90)]
    b, c, a, ang = R.choice(T)
    k = R.choice([1, 2, 3]) if max(a, b, c) <= 8 else 1
    b, c, a = b * k, c * k, a * k
    cs = Fr(b * b + c * c - a * a, 2 * b * c)
    return M("Dans le triangle ABC, AB = %d, AC = %d et BC = %d. Quelle est la mesure de l’angle BAC ?" % (c, b, a), "%d°" % ang,
             ["%d°" % x for x in (30, 45, 60, 90, 120, 135, 150) if x != ang], "cos BAC = (AB² + AC² − BC²) ÷ (2 × AB × AC) = (%d + %d − %d) ÷ %d = %s, donc <b>BAC = %d°</b>." % (c * c, b * b, a * a, 2 * b * c, fq(cs), ang))


def s3():
    nu, nv = R.randint(2, 8), R.randint(2, 8)
    p = R.randint(-nu * nv + 1, nu * nv - 1)
    k = R.choice(["somme", "somme", "diff", "prod"])
    if k == "somme":
        s2 = nu * nu + nv * nv + 2 * p
        return M("‖%s‖ = %d, ‖%s‖ = %d et %s · %s = %s. Calcule ‖%s + %s‖²." % (V("u"), nu, V("v"), nv, V("u"), V("v"), d(p), V("u"), V("v")), d(s2),
                 [d(nu * nu + nv * nv), d(nu * nu + nv * nv + p), d((nu + nv) ** 2), d(nu * nu + nv * nv - 2 * p)],
                 "‖%s + %s‖² = ‖%s‖² + 2 %s · %s + ‖%s‖² = %d + %s + %d = <b>%s</b>." % (V("u"), V("v"), V("u"), V("u"), V("v"), V("v"), nu * nu, par(2 * p), nv * nv, d(s2)))
    if k == "diff":
        s2 = nu * nu + nv * nv - 2 * p
        return M("‖%s‖ = %d, ‖%s‖ = %d et ‖%s − %s‖² = %d. Calcule %s · %s." % (V("u"), nu, V("v"), nv, V("u"), V("v"), s2, V("u"), V("v")), d(p) if Fr(p).denominator == 1 else fq(p),
                 [d(-p) if p else "1", d(nu * nu + nv * nv - s2), fq(Fr(s2 - nu * nu - nv * nv, 2)) if p else "2", d(s2)],
                 "%s · %s = ½(‖%s‖² + ‖%s‖² − ‖%s − %s‖²) = ½(%d + %d − %d) = <b>%s</b>." % (V("u"), V("v"), V("u"), V("v"), V("u"), V("v"), nu * nu, nv * nv, s2, d(p)))
    a, b, c, e = R.choice([(2, 1, 1, -1), (1, 2, 1, -1), (1, 1, 1, -1), (3, 1, 1, 2), (1, -1, 2, 1), (2, -1, 1, 3)])
    # (a u + b v) · (c u + e v) = ac nu² + (ae + bc) p + be nv²
    v_ = a * c * nu * nu + (a * e + b * c) * p + b * e * nv * nv
    L1 = E((a, V("u")), (b, V("v")))
    L2 = E((c, V("u")), (e, V("v")))
    return M("‖%s‖ = %d, ‖%s‖ = %d et %s · %s = %s. Calcule (%s) · (%s)." % (V("u"), nu, V("v"), nv, V("u"), V("v"), d(p), L1, L2), d(v_),
             [d(a * c * nu * nu + b * e * nv * nv), d(a * c * nu * nu + (a * e + b * c) * p - b * e * nv * nv) if b * e else d(v_ + p), d(a * c * nu + b * e * nv + (a * e + b * c) * p) if (nu, nv) != (1, 1) else d(v_ + 1), d(v_ - 2 * p) if p else d(v_ + 3)],
             "On développe (bilinéarité) : %s‖%s‖² %s %s %s · %s %s %s‖%s‖² = <b>%s</b>." % (d(a * c) if a * c != 1 else "", V("u"), "+" if a * e + b * c >= 0 else MINUS, (d(abs(a * e + b * c)) + " ") if abs(a * e + b * c) != 1 else "", V("u"), V("v"), "+" if b * e >= 0 else MINUS, d(abs(b * e)) if abs(b * e) != 1 else "", V("v"), d(v_)))


def s4():
    k = R.choice(["cercle", "cercle", "centre", "MI"])
    A = (R.randint(-6, 6), R.randint(-6, 6))
    B = (A[0] + 2 * R.randint(-4, 4), A[1] + 2 * R.randint(-4, 4))
    if A == B:
        return None
    I = (Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2))
    AB2 = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2
    if k == "cercle":
        return M("A et B sont deux points distincts. Quel est l’ensemble des points M tels que %s · %s = 0 ?" % (V("MA"), V("MB")) if R.random() < 0.3 else
                 "A%s et B%s. Quel est l’ensemble des points M tels que %s · %s = 0 ?" % (co(*A), co(*B), V("MA"), V("MB")), "le cercle de diamètre [AB]",
                 ["la médiatrice de [AB]", "la droite (AB)", "le cercle de centre A passant par B"], "%s · %s = 0 ⇔ M = A, M = B ou l’angle AMB est droit : c’est <b>le cercle de diamètre [AB]</b>." % (V("MA"), V("MB")))
    if k == "centre":
        return M("A%s et B%s. L’ensemble des points M tels que %s · %s = 0 est un cercle. Quels sont son centre et son rayon ?" % (co(*A), co(*B), V("MA"), V("MB")),
                 "centre (%s ; %s), rayon %s" % (fq(I[0]), fq(I[1]), sq(AB2 // 4)),
                 ["centre (%s ; %s), rayon %s" % (fq(I[0]), fq(I[1]), sq(AB2)), "centre %s, rayon %s" % (co(*A), sq(AB2)), "centre (%s ; %s), rayon %s" % (fq(Fr(B[0] - A[0], 2)), fq(Fr(B[1] - A[1], 2)), sq(AB2 // 4))],
                 "Centre : milieu I de [AB] = (%s ; %s). Rayon : AB ÷ 2 = √%d ÷ 2 = <b>%s</b>." % (fq(I[0]), fq(I[1]), AB2, sq(AB2 // 4)))
    MI = R.randint(1, 10)
    AB = R.choice([2, 4, 6, 8, 10])
    v = MI * MI - Fr(AB * AB, 4)
    return M("I est le milieu de [AB], AB = %d et MI = %d. Calcule %s · %s (avec %s · %s = MI² − AB²/4)." % (AB, MI, V("MA"), V("MB"), V("MA"), V("MB")), d(v),
             [d(MI * MI - AB * AB), d(MI * MI + Fr(AB * AB, 4)), d(MI * MI - Fr(AB, 2)), d(-v) if v else "1"], "%d² − %d²/4 = %d − %s = <b>%s</b>." % (MI, AB, MI * MI, d(Fr(AB * AB, 4)), d(v)))


def s5():
    k = R.choice(["dist", "dist", "parallelo", "angle_rect"])
    if k == "dist":
        b, c = R.randint(3, 12) * 10, R.randint(3, 12) * 10
        ang, cs = R.choice([(60, 0.5), (120, -0.5)])
        a = math.sqrt(b * b + c * c - 2 * b * c * cs)
        return M("Deux bateaux partent d’un port P. L’un parcourt %d m, l’autre %d m, et les directions forment un angle de %d°. Quelle distance les sépare (au mètre près) ?" % (b, c, ang), "%d m" % round(a),
                 ["%d m" % round(math.sqrt(b * b + c * c + 2 * b * c * cs)), "%d m" % round(math.sqrt(b * b + c * c)), "%d m" % (b + c), "%d m" % abs(b - c) if b != c else "%d m" % round(a / 2)],
                 "Al-Kashi : d² = %d² + %d² − 2 × %d × %d × cos(%d°) ≈ %s, donc <b>d ≈ %d m</b>." % (b, c, b, c, ang, num(round(a * a)), round(a)))
    if k == "parallelo":
        a, b = R.randint(3, 8), R.randint(3, 8)
        ang, cs = R.choice([(60, Fr(1, 2)), (120, Fr(-1, 2))])
        d2 = a * a + b * b + 2 * a * b * cs
        return M("ABCD est un parallélogramme avec AB = %d, AD = %d et l’angle BAD de %d°. Calcule AC² (diagonale), avec %s = %s + %s." % (a, b, ang, V("AC"), V("AB"), V("AD")), d(d2),
                 [d(a * a + b * b - 2 * a * b * cs), d(a * a + b * b), d((a + b) ** 2)],
                 "AC² = AB² + 2 %s · %s + AD² = %d + 2 × %s + %d = <b>%s</b>." % (V("AB"), V("AD"), a * a, d(a * b * cs), b * b, d(d2)))
    a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (4, 5, 6), (5, 6, 8), (2, 3, 4), (7, 8, 9)])
    cs = Fr(a * a + b * b - c * c, 2 * a * b)
    ans = "rectangle" if cs == 0 else "obtusangle (un angle obtus)" if cs < 0 else "acutangle (trois angles aigus)"
    return M("Un triangle a pour côtés %d, %d et %d. Le plus grand angle est-il droit, aigu ou obtus ?" % (a, b, c), ans, [x for x in ["rectangle", "obtusangle (un angle obtus)", "acutangle (trois angles aigus)", "on ne peut pas savoir"] if x != ans],
             "Al-Kashi : cos = (%d + %d − %d) ÷ %d = %s : le triangle est <b>%s</b>." % (a * a, b * b, c * c, 2 * a * b, fq(cs) if cs == 0 else fq(cs) + (" &lt; 0" if cs < 0 else " &gt; 0"), ans))


def main():
    seen = set()
    sets = [("Al-Kashi : calculer une longueur", mix(R, seen, [(s1, 20)])), ("Al-Kashi : calculer un angle", mix(R, seen, [(s2, 20)])),
            ("Développer avec le produit scalaire", mix(R, seen, [(s3, 20)])), ("Ensemble des points M tels que MA · MB = 0", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    u, v = V("u"), V("v")
    body = L(["<b>Formule d’Al-Kashi</b> : dans un triangle ABC, BC² = AB² + AC² − 2 × AB × AC × cos(BAC). Si l’angle est droit, on retrouve Pythagore.",
              "Développements : ‖%s + %s‖² = ‖%s‖² + 2 %s · %s + ‖%s‖², donc %s · %s = ½(‖%s + %s‖² − ‖%s‖² − ‖%s‖²)." % (u, v, u, u, v, v, u, v, u, v, u, v),
              "Le produit scalaire est bilinéaire : on développe (a%s + b%s) · (c%s + d%s) comme un produit de sommes." % (u, v, u, v),
              "Si I est le milieu de [AB] : %s · %s = MI² − AB²/4. L’ensemble des points M tels que %s · %s = 0 est le <b>cercle de diamètre [AB]</b>." % (V("MA"), V("MB"), V("MA"), V("MB"))],
             [("AB = 5, AC = 8, BAC = 60°", ["BC² = 25 + 64 − 2 × 5 × 8 × ½ = 49"], "BC = 7")],
             [["BC² = AB² + AC² + 2 AB × AC cos A", "C’est « moins » : − 2 AB × AC cos A."], ["BC = 49", "49 est BC² : BC = 7."], ["‖%s + %s‖² = ‖%s‖² + ‖%s‖²" % (u, v, u, v), "Il manque le terme 2 %s · %s." % (u, v)]])
    faq = [("Quand utiliser Al-Kashi ?", "Quand on connaît deux côtés et l’angle entre eux (pour le troisième côté), ou les trois côtés (pour un angle). Il généralise Pythagore à tous les triangles."),
           ("Comment démontrer la formule d’Al-Kashi ?", "BC² = ‖%s − %s‖² = AC² − 2 %s · %s + AB² et %s · %s = AB × AC × cos A." % (V("AC"), V("AB"), V("AB"), V("AC"), V("AB"), V("AC")))]
    unit("premiere", R, "al-kashi-et-applications-du-produit-scalaire", "G",
         "Formule d’Al-Kashi ; développements de ‖u + v‖² et ‖u − v‖², bilinéarité et symétrie du produit scalaire ; ensemble des points M tels que MA · MB = 0 ; calculer des longueurs et des angles",
         "Al-Kashi et applications du produit scalaire", "Al-Kashi",
         "Fiches de maths première sur la formule d’Al-Kashi et les applications du produit scalaire : longueurs, angles, développements, bilinéarité et cercle de diamètre [AB]. 100 exercices corrigés.",
         "BC² = AB² + AC² − 2 AB × AC × cos A", "MA · MB = 0 : cercle de diamètre [AB]", body, faq, sets, 17)


if __name__ == "__main__":
    main()
