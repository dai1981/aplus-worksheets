# -*- coding: utf-8 -*-
"""
France Maths 4e : Théorème de Pythagore (calculer une longueur)
  python3 tools/gen_fr_maths_4e_theoreme_de_pythagore.py
Erreurs : additionner les longueurs sans les carrés, ajouter au lieu de soustraire pour un côté de l’angle droit, oublier la racine, se tromper d’hypoténuse.
"""
import random
import math
from fr_c4 import *

R = random.Random(60313)
K = Kids(R)
LET = ["ABC", "EFG", "RST", "KLM", "DEF", "PQR", "IJK", "UVW", "MNO"]
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29), (9, 40, 41), (15, 20, 25), (10, 24, 26), (12, 35, 37)]


def rfig(L, a, b, labs):
    """L = (sommet de l’angle droit, autre, autre) ; a, b : longueurs des côtés de l’angle droit ; labs : {côté: texte}"""
    V, P, Q = L
    pts = {V: (0, 0), P: (a, 0), Q: (0, b)} if R.random() < 0.5 else {V: (0, 0), P: (-a, 0), Q: (0, b)}
    sides = [(x[0], x[1], t) for x, t in labs.items()]
    return figure(pts, [(V, P), (P, Q), (Q, V)], sides, right=[(V, P, Q)], label="triangle rectangle")


def s1():
    a, b, c = R.choice(TRIP)
    if R.random() < 0.5:
        a, b = b, a
    k = R.choice([1, 1, 2, Fr(1, 2), Fr(1, 10)]) if c <= 25 else 1
    a, b, c = a * k, b * k, c * k
    L = R.choice(LET)
    V, P, Q = L
    svg = rfig(L, float(a), float(b), {(V, P): "%s cm" % d(a), (V, Q): "%s cm" % d(b)})
    return M("<div class='qfig'>%s</div>Le triangle %s est rectangle en %s. Calcule %s%s." % (svg, L, V, P, Q), "%s cm" % d(c),
             ["%s cm" % d(a + b), "%s cm" % d(c * c), "%s cm" % d(abs(b - a)) if a != b else "%s cm" % d(c + 1)],
             "%s%s² = %s%s² + %s%s² = %s + %s = %s, donc %s%s = √%s = <b>%s cm</b>." % (P, Q, V, P, V, Q, d(a * a), d(b * b), d(c * c), P, Q, d(c * c), d(c)))


def s2():
    a, b, c = R.choice(TRIP)
    k = R.choice([1, 1, 2, Fr(1, 2)]) if c <= 25 else 1
    a, b, c = a * k, b * k, c * k
    L = R.choice(LET)
    V, P, Q = L
    svg = rfig(L, float(a), float(b), {(V, P): "%s cm" % d(a), (P, Q): "%s cm" % d(c)})
    s_ = c * c + a * a
    w2 = Fr(round(math.sqrt(s_) * 10), 10)
    return M("<div class='qfig'>%s</div>Le triangle %s est rectangle en %s. Calcule %s%s." % (svg, L, V, V, Q), "%s cm" % d(b),
             ["%s cm" % d(w2), "%s cm" % d(c - a), "%s cm" % d(c + a)],
             "L’hypoténuse est [%s%s] : %s%s² = %s%s² − %s%s² = %s − %s = %s, donc %s%s = <b>%s cm</b>." % (P, Q, V, Q, P, Q, V, P, d(c * c), d(a * a), d(b * b), V, Q, d(b)))


def s3():
    a, b = R.randint(2, 12), R.randint(2, 12)
    k = R.choice(["hyp", "hyp", "cote"])
    L = R.choice(LET)
    V, P, Q = L
    if k == "hyp":
        s_ = a * a + b * b
        if math.isqrt(s_) ** 2 == s_:
            return None
        v = Fr(round(math.sqrt(s_) * 10), 10)
        return M("Le triangle %s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Donne %s%s arrondi au dixième." % (L, V, V, P, a, V, Q, b, P, Q), "%s cm" % d(v),
                 ["%d cm" % (a + b), "%s cm" % d(Fr(round(math.sqrt(abs(a * a - b * b)) * 10), 10)) if a != b else "%s cm" % d(v + 1), "%d cm" % s_],
                 "%s%s² = %d + %d = %d ; %s%s = √%d ≈ <b>%s cm</b>." % (P, Q, a * a, b * b, s_, P, Q, s_, d(v)))
    c = max(a, b) + R.randint(1, 6)
    s_ = c * c - a * a
    if math.isqrt(s_) ** 2 == s_:
        return None
    v = Fr(round(math.sqrt(s_) * 10), 10)
    return M("Le triangle %s est rectangle en %s avec %s%s = %d cm et %s%s = %d cm. Donne %s%s arrondi au dixième." % (L, V, P, Q, c, V, P, a, V, Q), "%s cm" % d(v),
             ["%s cm" % d(Fr(round(math.sqrt(c * c + a * a) * 10), 10)), "%d cm" % (c - a), "%d cm" % s_],
             "%s%s² = %d − %d = %d ; %s%s = √%d ≈ <b>%s cm</b>." % (V, Q, c * c, a * a, s_, V, Q, s_, d(v)))


def s4():
    k = R.choice(["hypname", "egalite", "diag", "iso"])
    L = R.choice(LET)
    V, P, Q = L
    if k == "hypname":
        return M("Le triangle %s est rectangle en %s. Quelle est son hypoténuse ?" % (L, V), "[%s%s]" % (P, Q), ["[%s%s]" % (V, P), "[%s%s]" % (V, Q), "le sommet %s" % V],
                 "L’hypoténuse est le côté opposé à l’angle droit : <b>[%s%s]</b>." % (P, Q))
    if k == "egalite":
        return M("Le triangle %s est rectangle en %s. Quelle égalité est vraie ?" % (L, V), "%s%s² = %s%s² + %s%s²" % (P, Q, V, P, V, Q),
                 ["%s%s² = %s%s² + %s%s²" % (V, P, P, Q, V, Q), "%s%s = %s%s + %s%s" % (P, Q, V, P, V, Q), "%s%s² = %s%s² − %s%s²" % (P, Q, V, P, V, Q)],
                 "Le carré de l’hypoténuse est égal à la somme des carrés des deux autres côtés : <b>%s%s² = %s%s² + %s%s²</b>." % (P, Q, V, P, V, Q))
    if k == "diag":
        a, b, c = R.choice(TRIP[:9])
        return M("Un rectangle mesure %d cm sur %d cm. Combien mesure sa diagonale ?" % (a, b), "%d cm" % c, ["%d cm" % (a + b), "%d cm" % (c * c), "%d cm" % (2 * (a + b))],
                 "La diagonale est l’hypoténuse : √(%d + %d) = √%d = <b>%d cm</b>." % (a * a, b * b, c * c, c))
    c = R.choice([2, 3, 4, 5, 6, 10])
    v = Fr(round(c * math.sqrt(2) * 10), 10)
    return M("Un carré a pour côté %d cm. Donne la longueur de sa diagonale, arrondie au dixième." % c, "%s cm" % d(v), ["%d cm" % (2 * c), "%d cm" % (c * c), "%s cm" % d(Fr(round(c * math.sqrt(3) * 10), 10))],
             "d² = %d + %d = %d ; d = √%d ≈ <b>%s cm</b>." % (c * c, c * c, 2 * c * c, 2 * c * c, d(v)))


def s5():
    k = R.choice(["echelle", "tv", "rampe", "ecran", "chemin", "cerf"])
    if k == "echelle":
        a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (1.2, 1.6, 2), (1.5, 2, 2.5), (0.9, 1.2, 1.5)])
        a, b, c = Fr(a).limit_denominator(10), Fr(b).limit_denominator(10), Fr(c).limit_denominator(10)
        return M("Une échelle de %s m est posée contre un mur vertical. Son pied est à %s m du mur. À quelle hauteur arrive-t-elle ?" % (d(c), d(a)), "%s m" % d(b), ["%s m" % d(c - a), "%s m" % d(Fr(round(math.sqrt(float(c * c + a * a)) * 10), 10)), "%s m" % d(c + a)],
                 "h² = %s² − %s² = %s − %s = %s, donc h = <b>%s m</b>." % (d(c), d(a), d(c * c), d(a * a), d(b * b), d(b)))
    if k == "tv":
        a, b = R.choice([(80, 45), (120, 68), (100, 56), (64, 36)])
        v = Fr(round(math.sqrt(a * a + b * b)), 1)
        return M("L’écran d’une télévision mesure %d cm de large et %d cm de haut. Quelle est sa diagonale, arrondie au centimètre ?" % (a, b), "%d cm" % v, ["%d cm" % (a + b), "%d cm" % round(math.sqrt(a * a - b * b)), "%d cm" % (2 * (a + b))],
                 "√(%s + %s) = √%s ≈ <b>%d cm</b>." % (num(a * a), num(b * b), num(a * a + b * b), v))
    if k == "rampe":
        l, h = R.choice([(4, 0.3), (5, 0.4), (6, 0.5), (3, 0.2)])
        L_ = Fr(l).limit_denominator(10)
        hh = Fr(h).limit_denominator(10)
        v = Fr(round(math.sqrt(float(L_ * L_ + hh * hh)) * 100), 100)
        return M("Une rampe d’accès monte de %s m sur une distance horizontale de %s m. Quelle est sa longueur, arrondie au centimètre ?" % (d(hh), d(L_)), "%s m" % dk(v, 2), ["%s m" % d(L_ + hh), "%s m" % dk(Fr(round(math.sqrt(float(L_ * L_ - hh * hh)) * 100), 100), 2), "%s m" % d(L_)],
                 "√(%s² + %s²) ≈ <b>%s m</b>." % (d(L_), d(hh), dk(v, 2)))
    if k == "ecran":
        a, b, c = R.choice(TRIP[:8])
        return M("Un terrain rectangulaire mesure %d m sur %d m. Combien de mètres économise-t-on en le traversant en diagonale plutôt qu’en longeant deux côtés ?" % (a * 5, b * 5), "%d m" % ((a + b - c) * 5), ["%d m" % (c * 5), "%d m" % ((a + b) * 5), "%d m" % ((a + b + c) * 5)],
                 "Diagonale : √(%d² + %d²) = %d m ; %d − %d = <b>%d m</b>." % (a * 5, b * 5, c * 5, (a + b) * 5, c * 5, (a + b - c) * 5))
    if k == "chemin":
        n, e = R.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15)])
        return M("Un randonneur marche %d km vers le nord, puis %d km vers l’est. À quelle distance (à vol d’oiseau) est-il de son point de départ ?" % (n, e), "%d km" % round(math.sqrt(n * n + e * e)), ["%d km" % (n + e), "%d km" % (e - n), "%d km" % (n * n + e * e)],
                 "Les deux trajets sont perpendiculaires : √(%d + %d) = <b>%d km</b>." % (n * n, e * e, round(math.sqrt(n * n + e * e))))
    h = R.choice([6, 8, 12, 15])
    a, b, c = [t for t in TRIP if t[1] == h or t[0] == h][0]
    base = a if b == h else b
    return M("Un cerf-volant est retenu par une ficelle tendue de %d m. Il se trouve à la verticale d’un point situé à %d m de l’enfant. À quelle hauteur est-il (hauteur de la main négligée) ?" % (c, base), "%d m" % h, ["%d m" % (c - base), "%d m" % (c + base), "%d m" % round(math.sqrt(c * c + base * base))],
             "h² = %d − %d = %d ; h = <b>%d m</b>." % (c * c, base * base, h * h, h))


def main():
    seen = set()
    sets = [("Calculer l’hypoténuse", mix(R, seen, [(s1, 20)])), ("Calculer un côté de l’angle droit", mix(R, seen, [(s2, 20)])),
            ("Valeurs arrondies", mix(R, seen, [(s3, 20)])), ("Hypoténuse, égalité, diagonales", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Dans un triangle rectangle, l’<b>hypoténuse</b> est le côté opposé à l’angle droit ; c’est le plus long côté.",
              "<b>Théorème de Pythagore</b> : si ABC est rectangle en A, alors BC² = AB² + AC².",
              "Pour un côté de l’angle droit, on soustrait : AB² = BC² − AC². On termine par la racine carrée."],
             [("ABC rectangle en A, AB = 6 cm, AC = 8 cm", ["BC² = 6² + 8² = 36 + 64 = 100", "BC = √100"], "BC = 10 cm"), ("EFG rectangle en E, FG = 13, EF = 5", ["EG² = 169 − 25 = 144"], "EG = 12")],
             [["BC = AB + AC", "Ce sont les carrés qui s’ajoutent, pas les longueurs."], ["Ajouter quand on cherche un côté de l’angle droit", "On soustrait du carré de l’hypoténuse."],
              ["Oublier la racine carrée", "BC² = 100 donne BC = 10, pas 100."]])
    faq = [("Le théorème marche-t-il pour tous les triangles ?", "Non, seulement pour les triangles rectangles."),
           ("Comment repérer l’hypoténuse ?", "C’est le côté en face de l’angle droit, toujours le plus long.")]
    unit("4e", R, "theoreme-de-pythagore", "E",
         "Connaître et utiliser le théorème de Pythagore pour calculer une longueur dans un triangle rectangle (hypoténuse ou côté de l’angle droit), en valeur exacte ou arrondie ; résoudre des problèmes",
         "Théorème de Pythagore", "Théorème de Pythagore",
         "Fiches de maths 4e sur le théorème de Pythagore : calculer l’hypoténuse ou un côté de l’angle droit, valeurs arrondies, diagonales et problèmes. 100 exercices corrigés.",
         "Rectangle en A : BC² = AB² + AC²", "L’hypoténuse est en face de l’angle droit", body, faq, sets, 13)


if __name__ == "__main__":
    main()
