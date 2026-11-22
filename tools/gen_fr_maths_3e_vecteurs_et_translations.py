# -*- coding: utf-8 -*-
"""
France Maths 3e : Vecteurs et translations
  python3 tools/gen_fr_maths_3e_vecteurs_et_translations.py
Erreurs : coordonnées xA − xB au lieu de xB − xA, ABCD au lieu de ABDC pour le parallélogramme, ajouter les vecteurs bout à bout dans le mauvais ordre.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60412)
K = Kids(R)


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def VEC(s):
    return "<span class='vec'>%s</span>" % s


def s1():
    ax, ay, bx, by = [R.randint(-6, 6) for _ in range(4)]
    if (ax, ay) == (bx, by):
        return None
    return M("A%s et B%s. Quelles sont les coordonnées du vecteur %s ?" % (co(ax, ay), co(bx, by), VEC("AB")), co(bx - ax, by - ay),
             [co(ax - bx, ay - by), co(ax + bx, ay + by), co(by - ay, bx - ax) if (by - ay, bx - ax) != (bx - ax, by - ay) else co(bx - ax + 1, by - ay)],
             "%s(x<sub>B</sub> − x<sub>A</sub> ; y<sub>B</sub> − y<sub>A</sub>) = (%s − %s ; %s − %s) = <b>%s</b>." % (VEC("AB"), d(bx), par(ax), d(by), par(ay), co(bx - ax, by - ay)))


def s2():
    ax, ay = R.randint(-5, 5), R.randint(-5, 5)
    ux, uy = R.randint(-4, 4), R.randint(-4, 4)
    if (ux, uy) == (0, 0):
        return None
    k = R.choice(["img", "img", "ant"])
    if k == "img":
        return M("Le point M%s a pour image M’ par la translation de vecteur %s%s. Quelles sont les coordonnées de M’ ?" % (co(ax, ay), VEC("u"), co(ux, uy)), co(ax + ux, ay + uy),
                 [co(ax - ux, ay - uy), co(ux - ax, uy - ay), co(ax + uy, ay + ux) if ux != uy else co(ax + ux, ay - uy) if uy else co(ax + ux + 1, ay)],
                 "M’ = (%s + %s ; %s + %s) = <b>%s</b>." % (d(ax), par(ux), d(ay), par(uy), co(ax + ux, ay + uy)))
    return M("Par la translation de vecteur %s%s, le point P a pour image Q%s. Quelles sont les coordonnées de P ?" % (VEC("u"), co(ux, uy), co(ax, ay)), co(ax - ux, ay - uy),
             [co(ax + ux, ay + uy), co(ux - ax, uy - ay), co(ax - uy, ay - ux) if ux != uy else co(ax - ux, ay + uy) if uy else co(ax - ux - 1, ay)],
             "P + %s = Q, donc P = (%s − %s ; %s − %s) = <b>%s</b>." % (VEC("u"), d(ax), par(ux), d(ay), par(uy), co(ax - ux, ay - uy)))


def s3():
    V_ = [("%s = %s. Quelle est la nature du quadrilatère ABDC (A, B, C non alignés) ?" % (VEC("AB"), VEC("CD")), "un parallélogramme", ["un rectangle", "un trapèze quelconque", "un losange"]),
          ("ABCD est un parallélogramme. Quel vecteur est égal à %s ?" % VEC("AB"), VEC("DC"), [VEC("CD"), VEC("BC"), VEC("AD")]),
          ("ABCD est un parallélogramme. Quel vecteur est égal à %s ?" % VEC("AD"), VEC("BC"), [VEC("CB"), VEC("DC"), VEC("AB")]),
          ("D’après la relation de Chasles, %s + %s = …" % (VEC("AB"), VEC("BC")), VEC("AC"), [VEC("CA"), VEC("BB"), VEC("AB") + " + " + VEC("CB")]),
          ("%s + %s = …" % (VEC("AB"), VEC("BA")), "le vecteur nul", [VEC("AB"), "2" + VEC("AB"), VEC("BB") + " + " + VEC("AA") + " + 1"]),
          ("Deux vecteurs égaux ont…", "la même direction, le même sens et la même longueur", ["seulement la même longueur", "la même origine", "des directions perpendiculaires"]),
          ("I est le milieu de [AB]. Quelle égalité est vraie ?", "%s = %s" % (VEC("AI"), VEC("IB")), ["%s = %s" % (VEC("AI"), VEC("BI")), "%s = %s" % (VEC("IA"), VEC("IB")), "%s = 2%s" % (VEC("AI"), VEC("AB"))]),
          ("Le vecteur %s est l’opposé de…" % VEC("AB"), VEC("BA"), [VEC("AB"), "−" + VEC("BA"), VEC("BB")])]
    q, a, w = R.choice(V_)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3b():
    ax, ay, bx, by, cx, cy = [R.randint(-5, 5) for _ in range(6)]
    if len({(ax, ay), (bx, by), (cx, cy)}) < 3 or (bx - ax) * (cy - ay) == (by - ay) * (cx - ax):
        return None
    k = R.choice(["para", "chasles"])
    if k == "para":
        dx, dy = cx + bx - ax, cy + by - ay
        return M("A%s, B%s, C%s. Quelles sont les coordonnées de D pour que ABDC soit un parallélogramme (%s = %s) ?" % (co(ax, ay), co(bx, by), co(cx, cy), VEC("AB"), VEC("CD")), co(dx, dy),
                 [co(ax + cx - bx, ay + cy - by), co(bx + cx, by + cy), co(cx - bx + ax, cy - by + ay) if (cx - bx + ax, cy - by + ay) != (ax + cx - bx, ay + cy - by) else co(dx + 1, dy)],
                 "%s = %s, donc D = C + %s = (%s + %s ; %s + %s) = <b>%s</b>." % (VEC("CD"), VEC("AB"), VEC("AB"), d(cx), par(bx - ax), d(cy), par(by - ay), co(dx, dy)))
    ux, uy = bx - ax, by - ay
    vx, vy = cx - bx, cy - by
    return M("%s%s et %s%s. Quelles sont les coordonnées de %s + %s ?" % (VEC("AB"), co(ux, uy), VEC("BC"), co(vx, vy), VEC("AB"), VEC("BC")), co(ux + vx, uy + vy),
             [co(ux - vx, uy - vy), co(ux * vx, uy * vy), co(ux + vy, uy + vx) if (vx, vy) != (vy, vx) else co(ux + vx + 1, uy + vy)],
             "On additionne les coordonnées : (%s + %s ; %s + %s) = <b>%s</b>, c’est %s." % (d(ux), par(vx), d(uy), par(vy), co(ux + vx, uy + vy), VEC("AC")))


def s4():
    ax, ay = R.randint(-4, 2), R.randint(-4, 2)
    ux, uy = R.randint(-3, 3), R.randint(-3, 3)
    if (ux, uy) == (0, 0):
        return None
    bx, by = ax + ux, ay + uy
    mx, my = R.randint(-4, 4), R.randint(-4, 4)
    nx, ny = mx + ux, my + uy
    if not all(-5 <= v <= 5 for v in (bx, by, nx, ny)) or (mx, my) in ((ax, ay), (bx, by)):
        return None
    svg = relabel(de_k8.kosy(pts=[(ax, ay, "A"), (bx, by, "B"), (mx, my, "M")], lo=-5, hi=5, u=22), "points dans un repère")
    k = R.choice(["img", "vec"])
    if k == "vec":
        return M("<div class='qfig'>%s</div>Lis les coordonnées du vecteur %s." % (svg, VEC("AB")), co(ux, uy), [co(-ux, -uy), co(uy, ux) if ux != uy else co(ux, uy + 1), co(bx, by) if (bx, by) != (ux, uy) else co(ax, ay)],
                 "De A à B : %s en abscisse et %s en ordonnée : <b>%s</b>." % (d(ux), d(uy), co(ux, uy)))
    return M("<div class='qfig'>%s</div>Quelles sont les coordonnées de l’image de M par la translation de vecteur %s ?" % (svg, VEC("AB")), co(nx, ny),
             [co(mx - ux, my - uy), co(mx + uy, my + ux) if ux != uy else co(nx, ny + 1), co(bx + mx, by + my)],
             "%s(%s ; %s), donc M’ = <b>%s</b>." % (VEC("AB"), d(ux), d(uy), co(nx, ny)))


def s5():
    k = R.choice(["deplacement", "deplacement", "bateau", "robot"])
    if k == "deplacement":
        a, b, c, e = R.randint(-6, 6), R.randint(-6, 6), R.randint(-6, 6), R.randint(-6, 6)
        return M("Un drone se déplace selon le vecteur (%s ; %s), puis selon le vecteur (%s ; %s). Quel vecteur aurait donné le même déplacement en une fois ?" % (d(a), d(b), d(c), d(e)), co(a + c, b + e), [co(a - c, b - e), co(a * c, b * e), co(c - a, e - b)],
                 "On additionne les vecteurs : <b>%s</b>." % co(a + c, b + e))
    if k == "bateau":
        x, y = R.randint(1, 8), R.randint(1, 8)
        return M("Un bateau part du port O(0 ; 0) et suit le vecteur (%d ; %d), puis revient en ligne droite au port. Quelles sont les coordonnées du vecteur du retour ?" % (x, y), co(-x, -y), [co(x, y), co(-y, -x) if x != y else co(-x, y), co(0, 0)],
                 "Le retour est l’opposé de l’aller : <b>%s</b>." % co(-x, -y))
    n = R.randint(2, 5)
    a, b = R.randint(-3, 3), R.randint(-3, 3)
    if (a, b) == (0, 0):
        return None
    return M("Un robot part de (0 ; 0) et répète %d fois le déplacement de vecteur (%s ; %s). Où arrive-t-il ?" % (n, d(a), d(b)), co(n * a, n * b), [co(a + n, b + n), co(a, b), co(n * a, b) if b else co(a, n * b + 1)],
             "%d × (%s ; %s) = <b>%s</b>." % (n, d(a), d(b), co(n * a, n * b)))


def main():
    seen = set()
    sets = [("Coordonnées d’un vecteur", mix(R, seen, [(s1, 20)])), ("Image par une translation", mix(R, seen, [(s2, 20)])),
            ("Égalité de vecteurs et Chasles", mix(R, seen, [(s3, 8), (s3b, 12)])), ("Lecture dans un repère", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Le <b>vecteur</b> %s décrit la translation qui transforme A en B : une direction, un sens et une longueur." % VEC("AB"),
              "Dans un repère : %s(x<sub>B</sub> − x<sub>A</sub> ; y<sub>B</sub> − y<sub>A</sub>). L’image de M par la translation de vecteur %s(a ; b) est M’(x + a ; y + b)." % (VEC("AB"), VEC("u")),
              "%s = %s ⇔ ABDC est un parallélogramme. <b>Relation de Chasles</b> : %s + %s = %s." % (VEC("AB"), VEC("CD"), VEC("AB"), VEC("BC"), VEC("AC"))],
             [("A(1 ; 3), B(4 ; −1)", ["%s(4 − 1 ; −1 − 3)" % VEC("AB")], "%s(3 ; −4)" % VEC("AB"))],
             [["Calculer x<sub>A</sub> − x<sub>B</sub>", "On fait « arrivée − départ » : x<sub>B</sub> − x<sub>A</sub>."], ["%s = %s ⇒ ABCD parallélogramme" % (VEC("AB"), VEC("CD")), "C’est ABDC (attention à l’ordre des lettres)."],
              ["%s + %s = %s" % (VEC("AB"), VEC("BC"), VEC("CA")), "On va de A à B puis de B à C : on arrive en C, c’est %s." % VEC("AC")]])
    faq = [("Quelle est la différence entre vecteur et segment ?", "Un segment a une longueur ; un vecteur a en plus une direction et un sens."),
           ("À quoi servent les vecteurs ?", "À décrire des déplacements (physique, jeux vidéo, navigation) et à démontrer des propriétés de figures.")]
    unit("3e", R, "vecteurs-et-translations", "E",
         "Associer un vecteur à une translation ; calculer les coordonnées d’un vecteur et l’image d’un point ; utiliser l’égalité de vecteurs et le lien avec le parallélogramme ; additionner des vecteurs (relation de Chasles)",
         "Vecteurs et translations", "Vecteurs et translations",
         "Fiches de maths 3e sur les vecteurs : coordonnées, translations, égalité de vecteurs et parallélogramme, relation de Chasles, lecture dans un repère et problèmes. 100 exercices corrigés.",
         "AB→(xB − xA ; yB − yA)", "AB→ + BC→ = AC→ (Chasles)", body, faq, sets, 12)


if __name__ == "__main__":
    main()
