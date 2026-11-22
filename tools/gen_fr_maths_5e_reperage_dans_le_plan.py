# -*- coding: utf-8 -*-
"""
France Maths 5e : Se repérer sur une droite graduée et dans le plan
  python3 tools/gen_fr_maths_5e_reperage_dans_le_plan.py
Abscisses (avec des relatifs et des décimaux), coordonnées d’un point (abscisse ; ordonnée), placer un point, signes des coordonnées.
Erreurs : inverser abscisse et ordonnée, oublier le signe −, compter les carreaux à partir du mauvais axe.
"""
import random
from fr_c4 import *
import de_k8
from fr_c3 import droite_dec

R = random.Random(60211)
K = Kids(R)


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def s1():
    lo = R.choice([-3, -2, -1]) * 10
    v = lo + R.randint(1, 19)
    if v % 10 == 0:
        return None
    svg = droite_dec(lo, lo + 20, 1, [(v, "A")], k=1, every=10)
    return M("<div class='qfig'>%s</div>Quelle est l’abscisse du point A ?" % svg, d(Fr(v, 10)), [d(Fr(-v, 10)), d(Fr(v + 1, 10)), d(Fr(v, 1)) if abs(v) < 30 else d(Fr(v - 1, 10))],
             "Chaque graduation vaut 0,1 : A a pour abscisse <b>%s</b>." % d(Fr(v, 10)))


def s2():
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    if x == y or x == 0 or y == 0:
        return None
    nm = R.choice("ABCDEMN")
    svg = relabel(de_k8.kosy(pts=[(x, y, nm)], lo=-5, hi=5, u=22), "un point dans un repère")
    return M("<div class='qfig'>%s</div>Quelles sont les coordonnées du point %s ?" % (svg, nm), co(x, y), [co(y, x), co(-x, y), co(x, -y)],
             "On lit d’abord l’abscisse (axe horizontal) : %s, puis l’ordonnée (axe vertical) : %s. %s<b>%s</b>." % (d(x), d(y), nm, co(x, y)))


def s3():
    names = R.sample("ABCDEFGH", 4)
    pts = []
    used = set()
    while len(pts) < 4:
        x, y = R.randint(-5, 5), R.randint(-5, 5)
        if (x, y) in used or x == 0 or y == 0:
            continue
        used.add((x, y))
        pts.append((x, y, names[len(pts)]))
    tx, ty, tn = R.choice(pts)
    if (ty, tx) in used and (ty, tx) != (tx, ty):
        return None
    svg = relabel(de_k8.kosy(pts=pts, lo=-5, hi=5, u=22), "quatre points dans un repère")
    return M("<div class='qfig'>%s</div>Quel point a pour coordonnées %s ?" % (svg, co(tx, ty)), "le point " + tn, ["le point " + p[2] for p in pts if p[2] != tn],
             "Abscisse %s, ordonnée %s : c’est <b>le point %s</b>." % (d(tx), d(ty), tn))


def s4():
    x, y = R.choice([-1, 1]) * R.randint(1, 9), R.choice([-1, 1]) * R.randint(1, 9)
    k = R.choice(["quad", "axe", "sym"])
    if k == "quad":
        pos = {(1, 1): "en haut à droite de l’origine", (-1, 1): "en haut à gauche de l’origine", (-1, -1): "en bas à gauche de l’origine", (1, -1): "en bas à droite de l’origine"}
        ans = pos[(1 if x > 0 else -1, 1 if y > 0 else -1)]
        return M("Où se trouve le point %s dans le repère ?" % co(x, y), ans, [v for v in pos.values() if v != ans],
                 "Abscisse %s : %s ; ordonnée %s : %s. Le point est <b>%s</b>." % (d(x), "à droite" if x > 0 else "à gauche", d(y), "en haut" if y > 0 else "en bas", ans))
    if k == "axe":
        z = R.choice(["abs", "ord"])
        P = (x, 0) if z == "abs" else (0, y)
        ans = "sur l’axe des abscisses" if z == "abs" else "sur l’axe des ordonnées"
        return M("Où se trouve le point %s ?" % co(*P), ans, ["sur l’axe des ordonnées" if z == "abs" else "sur l’axe des abscisses", "à l’origine", "en haut à droite de l’origine"],
                 "%s : <b>%s</b>." % ("Son ordonnée est 0" if z == "abs" else "Son abscisse est 0", ans))
    return M("Le point A a pour coordonnées %s. Quelles sont les coordonnées du point B, symétrique de A par rapport à l’origine ?" % co(x, y), co(-x, -y), [co(-x, y), co(x, -y), co(y, x)],
             "On prend les opposés des deux coordonnées : <b>%s</b>." % co(-x, -y))


def s5():
    k = R.choice(["dist", "milieu", "deplace"])
    if k == "dist":
        a, b = R.randint(-9, 0), R.randint(1, 9)
        return M("Sur une droite graduée, A a pour abscisse %s et B a pour abscisse %s. Quelle est la distance AB ?" % (d(a), d(b)), d(b - a), [d(b + a) if b + a > 0 else d(b - a + 2), d(abs(a)), d(b - a - 1)],
                 "AB = %s − %s = %s + %d = <b>%s</b>." % (d(b), par(a), d(b), -a, d(b - a)))
    if k == "milieu":
        a = R.randint(-10, 2)
        b = a + 2 * R.randint(1, 6)
        return M("A a pour abscisse %s et B pour abscisse %s. Quelle est l’abscisse du milieu de [AB] ?" % (d(a), d(b)), d(Fr(a + b, 2)), [d(Fr(b - a, 2)), d(a + b), d(Fr(a + b, 2) + 1)],
                 "Le milieu est à mi-chemin : (%s + %s) ÷ 2 = <b>%s</b>." % (d(a), par(b), d(Fr(a + b, 2))))
    x, y = R.randint(-5, 5), R.randint(-5, 5)
    dx, dy = R.randint(-4, 4), R.randint(-4, 4)
    if dx == 0 or dy == 0:
        return None
    return M("Un robot est au point %s. Il se déplace de %d %s vers la %s, puis de %d %s vers le %s. Où arrive-t-il ?" % (co(x, y), abs(dx), "unité" if abs(dx) == 1 else "unités", "droite" if dx > 0 else "gauche", abs(dy), "unité" if abs(dy) == 1 else "unités", "haut" if dy > 0 else "bas"),
             co(x + dx, y + dy), [co(x + dy, y + dx), co(x - dx, y + dy), co(x + dx, y - dy)],
             "Abscisse : %s %s %d ; ordonnée : %s %s %d. Arrivée : <b>%s</b>." % (d(x), "+" if dx > 0 else "−", abs(dx), d(y), "+" if dy > 0 else "−", abs(dy), co(x + dx, y + dy)))


def main():
    seen = set()
    sets = [("Abscisses sur une droite graduée", mix(R, seen, [(s1, 20)])), ("Lire des coordonnées", mix(R, seen, [(s2, 20)])),
            ("Retrouver un point", mix(R, seen, [(s3, 20)])), ("Signes et axes", mix(R, seen, [(s4, 20)])), ("Distances et déplacements", mix(R, seen, [(s5, 20)]))]
    body = L(["Sur une droite graduée, chaque point a une <b>abscisse</b>, positive à droite de l’origine, négative à gauche.",
              "Dans un repère, un point a deux coordonnées : (<b>abscisse</b> ; <b>ordonnée</b>). On lit d’abord sur l’axe horizontal, puis sur l’axe vertical.",
              "L’origine O a pour coordonnées (0 ; 0)."],
             [("A(−3 ; 2)", ["3 unités à gauche", "2 unités en haut"], "A est en haut à gauche de O")],
             [["Inverser abscisse et ordonnée", "On écrit toujours (horizontal ; vertical)."], ["Oublier le signe −", "À gauche de O ou en bas, la coordonnée est négative."],
              ["Compter les carreaux depuis le bord", "On compte toujours depuis les axes."]])
    faq = [("Comment retenir l’ordre des coordonnées ?", "On « marche » d’abord sur l’axe horizontal, puis on « monte » ou on « descend »."),
           ("Quelles sont les coordonnées d’un point sur l’axe des abscisses ?", "Son ordonnée est 0 : (x ; 0).")]
    unit("5e", R, "reperage-dans-le-plan", "E",
         "Lire et placer des abscisses (nombres relatifs) sur une droite graduée ; lire et placer des points de coordonnées données dans un repère orthogonal",
         "Se repérer sur une droite et dans le plan", "Repérage dans le plan",
         "Fiches de maths 5e sur le repérage : abscisses, coordonnées d’un point, retrouver un point, signes, distances et déplacements. 100 exercices corrigés.",
         "Coordonnées : (abscisse ; ordonnée)", "On lit d’abord l’horizontal.", body, faq, sets, 11)


if __name__ == "__main__":
    main()
