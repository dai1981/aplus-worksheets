# -*- coding: utf-8 -*-
"""
France Maths 4e : Réciproque et contraposée du théorème de Pythagore
  python3 tools/gen_fr_maths_4e_reciproque_et_contraposee_de_pythagore.py
Erreurs : ne pas prendre le plus grand côté, conclure « rectangle » parce que c’est presque égal, confondre théorème, réciproque et contraposée.
"""
import random
from fr_c4 import *

R = random.Random(60314)
K = Kids(R)
LET = ["ABC", "EFG", "RST", "KLM", "DEF", "PQR", "IJK", "UVW", "MNO"]
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29), (15, 20, 25), (10, 24, 26), (12, 35, 37), (9, 40, 41)]


def sides():
    """(a, b, c, rectangle?)"""
    a, b, c = R.choice(TRIP)
    k = R.choice([1, 1, Fr(1, 10), 2, Fr(1, 2)]) if c < 30 else 1
    a, b, c = a * k, b * k, c * k
    ok = R.random() < 0.5
    if not ok:
        c = c + (k if k < 1 else 1)
    return a, b, c, ok


def s1():
    a, b, c, ok = sides()
    L = R.choice(LET)
    A, B, C = L
    v = [a, b, c]
    nm = R.sample([A + B, B + C, A + C], 3)
    hyp = nm[2]
    rv = [x for x in L if x not in hyp][0]
    lst = ", ".join("%s = %s cm" % (n_, d(x)) for n_, x in zip(nm, v))
    ans = "oui, il est rectangle en %s" % rv if ok else "non, il n’est pas rectangle"
    w = [x for x in ["oui, il est rectangle en %s" % rv, "non, il n’est pas rectangle", "oui, il est rectangle en %s" % hyp[0], "on ne peut pas savoir sans le dessiner"] if x != ans]
    return M("Le triangle %s est tel que %s. Est-il rectangle ?" % (L, lst), ans, w,
             "Le plus grand côté est [%s] : %s² = %s et %s² + %s² = %s + %s = %s. %s" % (hyp, hyp, d(c * c), nm[0], nm[1], d(a * a), d(b * b), d(a * a + b * b),
                                                                                         "Égalité : d’après la réciproque du théorème de Pythagore, <b>il est rectangle en %s</b>." % rv if ok else "Pas d’égalité : d’après la contraposée, <b>il n’est pas rectangle</b>."))


def s2():
    a, b, c, _ = sides()
    a, b, c = R.choice(TRIP)
    L = R.choice(LET)
    A, B, C = L
    nm = R.sample([A + B, B + C, A + C], 3)
    rv = [x for x in L if x not in nm[2]][0]
    v = [a, b, c]
    order = list(zip(nm, v))
    R.shuffle(order)
    lst = ", ".join("%s = %d" % (n_, x) for n_, x in order)
    others = [x for x in L if x != rv]
    return M("Le triangle %s est tel que %s (en cm). Il est rectangle : en quel sommet ?" % (L, lst), rv, others + ["il n’est pas rectangle"],
             "L’angle droit est en face du plus grand côté [%s] : %d² = %d² + %d². Rectangle en <b>%s</b>." % (nm[2], c, a, b, rv))


def s3():
    V = [("On sait que ABC est rectangle en A et on veut calculer BC. Quel résultat utilise-t-on ?", "le théorème de Pythagore", ["la réciproque du théorème de Pythagore", "la contraposée du théorème de Pythagore", "la droite des milieux"]),
         ("On connaît les trois longueurs d’un triangle et on veut prouver qu’il est rectangle. Quel résultat utilise-t-on ?", "la réciproque du théorème de Pythagore", ["le théorème de Pythagore", "la contraposée du théorème de Pythagore", "la somme des angles"]),
         ("On connaît les trois longueurs et BC² ≠ AB² + AC², avec [BC] le plus grand côté. Quel résultat permet de conclure ?", "la contraposée du théorème de Pythagore", ["la réciproque du théorème de Pythagore", "le théorème de Pythagore", "on ne peut rien conclure"]),
         ("Énoncé : « Si BC² = AB² + AC², alors le triangle ABC est rectangle en A. » C’est…", "la réciproque du théorème de Pythagore", ["le théorème de Pythagore", "la contraposée", "une définition"]),
         ("Énoncé : « Si BC² ≠ AB² + AC² (BC étant le plus grand côté), alors ABC n’est pas rectangle. » C’est…", "la contraposée du théorème de Pythagore", ["la réciproque", "le théorème de Pythagore", "une propriété fausse"]),
         ("Pour tester si un triangle est rectangle avec la réciproque, quel côté met-on au carré seul ?", "le plus grand côté", ["le plus petit côté", "n’importe quel côté", "la hauteur"]),
         ("BC² = 50,41 et AB² + AC² = 50,4. Le triangle est-il rectangle ?", "non : l’égalité doit être exacte", ["oui : c’est presque égal", "oui, à 0,01 près", "on ne peut pas savoir"]),
         ("Un triangle a des côtés de 3 cm, 4 cm et 5 cm. Un autre a des côtés de 30 cm, 40 cm et 50 cm. Sont-ils rectangles ?", "oui, les deux", ["seulement le premier", "seulement le second", "aucun des deux"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3b():
    a, b, c, ok = sides()
    k = R.choice(["calc", "compare"])
    if k == "calc":
        return M("Dans un triangle, les deux plus petits côtés mesurent %s cm et %s cm. Combien vaut la somme de leurs carrés ?" % (d(a), d(b)), d(a * a + b * b), [d((a + b) ** 2), d(a + b), d(a * a * b * b) if a * a * b * b < 10000 else d(a * a + b * b + 1)],
                 "%s² + %s² = %s + %s = <b>%s</b>." % (d(a), d(b), d(a * a), d(b * b), d(a * a + b * b)))
    s_ = a * a + b * b
    sign = "=" if c * c == s_ else "&gt;" if c * c > s_ else "&lt;"
    return M("Triangle de côtés %s cm, %s cm et %s cm. Compare le carré du plus grand côté et la somme des carrés des deux autres." % (d(a), d(b), d(c)), "%s %s %s" % (d(c * c), sign, d(s_)),
             ["%s %s %s" % (d(c * c), s, d(s_)) for s in ["=", "&gt;", "&lt;"] if s != sign] + ["%s = %s" % (d(c), d(a + b))],
             "%s² = %s et %s² + %s² = %s : <b>%s %s %s</b>." % (d(c), d(c * c), d(a), d(b), d(s_), d(c * c), sign, d(s_)))


def s4():
    k = R.choice(["rect", "losange", "carre"])
    if k == "rect":
        a, b, c = R.choice(TRIP[:8])
        dg = c if R.random() < 0.5 else c + 1
        ok = dg == c
        ans = "oui" if ok else "non"
        return M("Un quadrilatère ABCD a ses côtés opposés égaux deux à deux : AB = CD = %d cm, BC = DA = %d cm. Sa diagonale AC mesure %d cm. Est-ce un rectangle ?" % (a, b, dg), ans, ["non" if ok else "oui", "on ne peut pas savoir", "seulement si AC = BD"],
                 "%d² = %d et %d² + %d² = %d : %s ABC %s rectangle en B. C’est un parallélogramme %s : <b>%s</b>." % (dg, dg * dg, a, b, a * a + b * b, "égalité, donc" if ok else "pas d’égalité, donc", "est" if ok else "n’est pas", "avec un angle droit" if ok else "sans angle droit", ans))
    if k == "losange":
        a, b, c = R.choice(TRIP[:8])
        return M("Les diagonales d’un parallélogramme mesurent %d cm et %d cm et ses côtés %d cm. Ses diagonales sont-elles perpendiculaires ?" % (2 * a, 2 * b, c), "oui, c’est un losange",
                 ["non", "on ne peut pas savoir", "oui, c’est un rectangle"], "Les diagonales se coupent en leur milieu : demi-diagonales %d et %d. %d² + %d² = %d = %d² : le triangle est rectangle, <b>c’est un losange</b>." % (a, b, a, b, c * c, c))
    a = R.randint(3, 9)
    return M("Un triangle isocèle a deux côtés de %d cm et un troisième de %d cm. Est-il rectangle ?" % (a, a + 1), "non", ["oui", "on ne peut pas savoir", "oui, en son sommet principal"],
             "%d² = %d et %d² + %d² = %d : pas d’égalité, <b>non</b>." % (a + 1, (a + 1) ** 2, a, a, 2 * a * a))


def s5():
    k = R.choice(["mur", "corde", "cadre", "terrain"])
    if k == "mur":
        a, b, c = R.choice([(60, 80, 100), (30, 40, 50), (90, 120, 150), (45, 60, 75)])
        dd = c if R.random() < 0.5 else c + R.choice([-2, 2, 3])
        ok = dd == c
        return M("Un maçon vérifie qu’un mur est bien perpendiculaire au sol : il mesure %d cm sur le sol, %d cm sur le mur et %d cm entre les deux points. Le mur est-il perpendiculaire au sol ?" % (a, b, dd),
                 "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement si le mur est haut"],
                 "%d² = %s et %d² + %d² = %s : %s." % (dd, num(dd * dd), a, b, num(a * a + b * b), "égalité, le mur est <b>perpendiculaire</b>" if ok else "pas d’égalité, il <b>n’est pas perpendiculaire</b>"))
    if k == "corde":
        return M("Les Égyptiens utilisaient une corde à 13 nœuds (12 intervalles égaux) pour former un triangle de côtés 3, 4 et 5 intervalles. Pourquoi ?", "pour obtenir un angle droit", ["pour obtenir un triangle équilatéral", "pour mesurer une aire", "pour tracer un cercle"],
                 "3² + 4² = 25 = 5² : d’après la réciproque, le triangle est <b>rectangle</b>.")
    if k == "cadre":
        a, b, c = R.choice(TRIP[:6])
        f = R.choice([5, 10])
        dd = c * f + R.choice([0, 0, 1, -1])
        ok = dd == c * f
        return M("Un cadre de tableau mesure %d cm sur %d cm, et sa diagonale %d cm. Les coins sont-ils des angles droits ?" % (a * f, b * f, dd), "oui" if ok else "non", ["non" if ok else "oui", "on ne peut pas savoir", "seulement deux coins"],
                 "%s et %s + %s = %s : <b>%s</b>." % (num(dd * dd), num((a * f) ** 2), num((b * f) ** 2), num((a * f) ** 2 + (b * f) ** 2), "oui" if ok else "non"))
    a, b, c = R.choice(TRIP)
    return M("Un terrain triangulaire a des côtés de %d m, %d m et %d m. Quelle est son aire ?" % (a, b, c), "%s m²" % d(Fr(a * b, 2)), ["%d m²" % (a * b), "%s m²" % d(Fr(a * c, 2)), "%d m²" % (a + b + c)],
             "%d² + %d² = %d² : il est rectangle, l’aire vaut %d × %d ÷ 2 = <b>%s m²</b>." % (a, b, c, a, b, d(Fr(a * b, 2))))


def main():
    seen = set()
    sets = [("Le triangle est-il rectangle ?", mix(R, seen, [(s1, 20)])), ("Trouver l’angle droit", mix(R, seen, [(s2, 20)])),
            ("Théorème, réciproque ou contraposée", mix(R, seen, [(s3, 8), (s3b, 12)])), ("Dans les quadrilatères", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["On repère le <b>plus grand côté</b>. On calcule séparément son carré et la somme des carrés des deux autres côtés.",
              "S’il y a égalité, d’après la <b>réciproque</b> du théorème de Pythagore, le triangle est rectangle (l’angle droit est en face du plus grand côté).",
              "S’il n’y a pas égalité, d’après la <b>contraposée</b>, le triangle n’est pas rectangle."],
             [("AB = 7,5 ; AC = 10 ; BC = 12,5", ["BC² = 156,25", "AB² + AC² = 56,25 + 100 = 156,25"], "rectangle en A")],
             [["Ne pas prendre le plus grand côté", "L’hypoténuse éventuelle est toujours le plus grand côté."], ["« C’est presque égal, donc rectangle »", "Il faut une égalité exacte."],
              ["Utiliser le théorème au lieu de la réciproque", "Le théorème suppose déjà le triangle rectangle."]])
    faq = [("Quelle différence entre réciproque et contraposée ?", "La réciproque prouve qu’un triangle est rectangle (égalité) ; la contraposée prouve qu’il ne l’est pas (pas d’égalité)."),
           ("Comment rédiger ?", "« Dans le triangle ABC, [BC] est le plus grand côté. BC² = … et AB² + AC² = … Donc BC² = AB² + AC². D’après la réciproque du théorème de Pythagore, ABC est rectangle en A. »")]
    unit("4e", R, "reciproque-et-contraposee-de-pythagore", "E",
         "Utiliser la réciproque du théorème de Pythagore pour démontrer qu’un triangle est rectangle et sa contraposée pour démontrer qu’il ne l’est pas ; choisir le bon résultat selon la situation",
         "Réciproque et contraposée du théorème de Pythagore", "Réciproque de Pythagore",
         "Fiches de maths 4e sur la réciproque et la contraposée du théorème de Pythagore : prouver qu’un triangle est rectangle ou non, angle droit, quadrilatères et problèmes. 100 exercices corrigés.",
         "Égalité → rectangle (réciproque)", "Pas d’égalité → pas rectangle (contraposée)", body, faq, sets, 14)


if __name__ == "__main__":
    main()
