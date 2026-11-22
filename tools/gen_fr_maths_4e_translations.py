# -*- coding: utf-8 -*-
"""
France Maths 4e : Translations
  python3 tools/gen_fr_maths_4e_translations.py
Erreurs : déplacer dans le mauvais sens (de B vers A), confondre translation et symétrie, croire qu’une translation change les longueurs.
"""
import random
from fr_c4 import *
import de_k8

R = random.Random(60311)
K = Kids(R)


def co(x, y):
    return "(%s ; %s)" % (d(x), d(y))


def s1():
    ax, ay = R.randint(-4, 2), R.randint(-4, 2)
    dx, dy = R.randint(-3, 4), R.randint(-3, 4)
    if (dx, dy) == (0, 0):
        return None
    bx, by = ax + dx, ay + dy
    mx, my = R.randint(-4, 4), R.randint(-4, 4)
    nx, ny = mx + dx, my + dy
    if not all(-5 <= v <= 5 for v in (bx, by, nx, ny)) or (mx, my) in ((ax, ay), (bx, by)):
        return None
    svg = relabel(de_k8.kosy(pts=[(ax, ay, "A"), (bx, by, "B"), (mx, my, "M")], lo=-5, hi=5, u=22), "points dans un repère")
    return M("<div class='qfig'>%s</div>Quelles sont les coordonnées de l’image de M par la translation qui transforme A en B ?" % svg, co(nx, ny),
             [co(mx - dx, my - dy), co(mx + dy, my + dx) if dx != dy else co(nx + 1, ny), co(2 * ax - mx, 2 * ay - my) if (2 * ax - mx, 2 * ay - my) != (nx, ny) else co(nx, ny + 1)],
             "Pour aller de A à B, on se déplace de %s horizontalement et de %s verticalement. On fait le même déplacement à partir de M : <b>%s</b>." % (d(dx), d(dy), co(nx, ny)))


def s2():
    ax, ay = R.randint(-6, 6), R.randint(-6, 6)
    bx, by = R.randint(-6, 6), R.randint(-6, 6)
    if (ax, ay) == (bx, by):
        return None
    dx, dy = bx - ax, by - ay
    k = R.choice(["img", "img", "ant"])
    mx, my = R.randint(-6, 6), R.randint(-6, 6)
    if k == "img":
        return M("A%s et B%s. Quelle est l’image du point M%s par la translation qui transforme A en B ?" % (co(ax, ay), co(bx, by), co(mx, my)), co(mx + dx, my + dy),
                 [co(mx - dx, my - dy), co(mx + bx, my + by), co(mx + dy, my + dx) if dx != dy else co(mx + dx + 1, my + dy)],
                 "Déplacement de A à B : %s en abscisse, %s en ordonnée. M’ = (%s + %s ; %s + %s) = <b>%s</b>." % (d(dx), d(dy), d(mx), par(dx), d(my), par(dy), co(mx + dx, my + dy)))
    return M("A%s et B%s. Le point N est l’image d’un point P par la translation qui transforme A en B, et N%s. Quelles sont les coordonnées de P ?" % (co(ax, ay), co(bx, by), co(mx, my)), co(mx - dx, my - dy),
             [co(mx + dx, my + dy), co(mx - bx, my - by), co(ax + mx, ay + my) if (ax + mx, ay + my) != (mx - dx, my - dy) else co(mx - dx, my - dy + 1)],
             "On fait le déplacement inverse (de B vers A) : <b>%s</b>." % co(mx - dx, my - dy))


def s3():
    V = [("Une translation conserve…", "les longueurs, les angles, les aires et le parallélisme", ["seulement les longueurs", "seulement l’orientation des points", "rien : la figure est déformée"]),
         ("La translation qui transforme A en B transforme C en D (A, B, C non alignés). Quelle est la nature de ABDC ?", "un parallélogramme", ["un rectangle", "un trapèze quelconque", "un triangle"]),
         ("Une translation est définie par…", "une direction, un sens et une longueur", ["un centre et un angle", "une droite (l’axe)", "un seul point"]),
         ("Par une translation, l’image d’une droite est…", "une droite parallèle", ["une droite perpendiculaire", "un point", "une droite qui la coupe toujours"]),
         ("La translation qui transforme A en B et celle qui transforme B en A sont…", "réciproques (l’une annule l’autre)", ["identiques", "des symétries", "impossibles à comparer"]),
         ("Dans un pavage de carreaux identiques, on passe d’un carreau à un carreau voisin de même orientation par…", "une translation", ["une symétrie axiale", "une rotation de 90°", "un agrandissement"]),
         ("Un triangle a une aire de 12 cm². Quelle est l’aire de son image par une translation ?", "12 cm²", ["24 cm²", "6 cm²", "cela dépend de la translation"]),
         ("Une figure et son image par une translation sont…", "superposables, sans retourner le calque", ["superposables en retournant le calque", "jamais superposables", "toujours confondues"]),
         ("La translation qui transforme A en B transforme M en M’. Que peut-on dire des segments [AB] et [MM’] ?", "ils sont parallèles et de même longueur", ["ils sont perpendiculaires", "ils ont le même milieu", "[MM’] est deux fois plus long"]),
         ("Quelle transformation n’est PAS une translation ?", "le retournement d’une figure (symétrie axiale)", ["le glissement d’un tiroir", "le déplacement d’une cabine de téléphérique", "le glissement d’une pièce d’échecs en ligne droite"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def s3b():
    k = R.choice(["mm", "angle", "perim"])
    a = R.randint(3, 15)
    if k == "mm":
        return M("La translation qui transforme A en B transforme M en M’. AB = %d cm. Combien mesure MM’ ?" % a, "%d cm" % a, ["%d cm" % (2 * a), "%s cm" % d(Fr(a, 2)), "on ne peut pas savoir"],
                 "Chaque point se déplace de la même longueur que de A à B : MM’ = AB = <b>%d cm</b>." % a)
    if k == "angle":
        t = R.randint(20, 160)
        return M("Dans le triangle EFG, l’angle en F mesure %d°. E’F’G’ est son image par une translation. Combien mesure l’angle en F’ ?" % t, "%d°" % t, ["%d°" % (180 - t), "%d°" % (2 * t) if 2 * t < 360 else "%d°" % (t + 10), "on ne peut pas savoir"],
                 "Une translation conserve les angles : <b>%d°</b>." % t)
    b, c = R.randint(3, 15), R.randint(3, 15)
    return M("Un rectangle mesure %d cm sur %d cm. Quel est le périmètre de son image par une translation de %d cm ?" % (b, c, a), "%d cm" % (2 * (b + c)), ["%d cm" % (2 * (b + c) + a), "%d cm" % (b * c), "%d cm" % (2 * (b + c) + 4 * a)],
             "L’image est un rectangle identique : 2 × (%d + %d) = <b>%d cm</b>." % (b, c, 2 * (b + c)))


def s4():
    k = R.choice(["comp", "comp", "par"])
    if k == "comp":
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        c, e = R.randint(-5, 5), R.randint(-5, 5)
        if (a, b) == (0, 0) or (c, e) == (0, 0):
            return None
        mx, my = R.randint(-5, 5), R.randint(-5, 5)
        return M("On déplace le point M%s de %s en abscisse et %s en ordonnée, puis de %s en abscisse et %s en ordonnée. Où arrive-t-il ?" % (co(mx, my), d(a), d(b), d(c), d(e)),
                 co(mx + a + c, my + b + e), [co(mx + a - c, my + b - e), co(mx + a * c, my + b * e), co(mx + a + c, my - b - e) if b + e else co(mx + a + c + 1, my)],
                 "Deux translations successives donnent une translation : (%s + %s + %s ; %s + %s + %s) = <b>%s</b>." % (d(mx), par(a), par(c), d(my), par(b), par(e), co(mx + a + c, my + b + e)))
    pts = R.sample(["A", "B", "C", "D", "E", "F"], 4)
    ax, ay = R.randint(-5, 0), R.randint(-5, 0)
    bx, by = ax + R.randint(2, 5), ay + R.randint(-1, 2)
    cx, cy = ax + R.randint(-1, 2), ay + R.randint(2, 4)
    dx_, dy_ = cx + bx - ax, cy + by - ay
    if max(abs(v) for v in (bx, by, cx, cy, dx_, dy_)) > 5:
        return None
    A, B, C, D = pts
    return M("La translation qui transforme %s%s en %s%s transforme %s%s en %s. Quelles sont les coordonnées de %s ?" % (A, co(ax, ay), B, co(bx, by), C, co(cx, cy), D, D), co(dx_, dy_),
             [co(cx - bx + ax, cy - by + ay), co(ax + bx - cx, ay + by - cy), co(bx + cx, by + cy)],
             "%s%s%s%s est un parallélogramme : %s = %s + (%s ; %s) = <b>%s</b>." % (A, B, D, C, D, C, d(bx - ax), d(by - ay), co(dx_, dy_)))


def s5():
    k = R.choice(["frise", "frise", "dist", "mixte"])
    if k == "frise":
        n = R.randint(2, 6)
        u = R.choice([3, 4, 5, 6])
        return M("Une frise est obtenue en répétant un motif par une translation de %d cm vers la droite. De combien est décalé le %de motif par rapport au 1er ?" % (u, n + 1), "%d cm" % (n * u), ["%d cm" % ((n + 1) * u), "%d cm" % u, "%d cm" % (n + u)],
                 "Du 1er au %de motif, il y a %s : %d × %d = <b>%d cm</b>." % (n + 1, pl(n, "décalage"), n, u, n * u))
    if k == "dist":
        a = R.randint(3, 12)
        b = R.randint(3, 12)
        return M("ABC est un triangle avec AB = %d cm et AC = %d cm. A’B’C’ est son image par une translation. Combien mesure A’C’ ?" % (a, b), "%d cm" % b, ["%d cm" % a, "%d cm" % (a + b), "on ne peut pas savoir"],
                 "Une translation conserve les longueurs : A’C’ = AC = <b>%d cm</b>." % b)
    V = [("On fait glisser une figure sans la tourner ni la retourner. Quelle transformation utilise-t-on ?", "une translation", ["une symétrie axiale", "une symétrie centrale", "un agrandissement"]),
         ("Un ascenseur monte de 12 m. Quelle transformation décrit le mouvement d’un point de la cabine ?", "une translation verticale de 12 m", ["une symétrie d’axe horizontal", "une rotation", "une réduction"]),
         ("La symétrie de centre O transforme A en A’. Est-ce une translation ?", "non, c’est une symétrie centrale (demi-tour)", ["oui, toujours", "oui, si A est près de O", "non, c’est une symétrie axiale"])]
    q, a, w = R.choice(V)
    return M(q, a, w, "Réponse : <b>%s</b>." % a)


def main():
    seen = set()
    sets = [("Construire une image sur un quadrillage", mix(R, seen, [(s1, 20)])), ("Translations et coordonnées", mix(R, seen, [(s2, 20)])),
            ("Propriétés", mix(R, seen, [(s3, 10), (s3b, 10)])), ("Enchaîner des translations et parallélogrammes", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["La translation qui transforme A en B fait <b>glisser</b> toute la figure dans la même direction, le même sens et de la même longueur que de A vers B.",
              "Si elle transforme C en D, alors ABDC est un parallélogramme (éventuellement aplati).",
              "Une translation conserve les longueurs, les angles, les aires et le parallélisme : la figure et son image sont superposables."],
             [("A(1 ; 2), B(4 ; 1), M(0 ; −3)", ["de A à B : +3 en abscisse, −1 en ordonnée", "M’ = (0 + 3 ; −3 − 1)"], "M’(3 ; −4)")],
             [["Faire le déplacement de B vers A", "On va dans le sens de A vers B."], ["Confondre avec une symétrie", "Une translation ne retourne pas et ne fait pas tourner la figure."],
              ["Penser que l’image est plus grande", "Une translation conserve toutes les longueurs."]])
    faq = [("Quelle différence entre translation et symétrie ?", "La translation fait glisser la figure ; la symétrie axiale la retourne et la symétrie centrale lui fait faire un demi-tour."),
           ("Où rencontre-t-on des translations ?", "Dans les frises, les pavages, les escalators, les ascenseurs ou les tapis roulants.")]
    unit("4e", R, "translations", "E",
         "Construire l’image d’un point ou d’une figure par une translation ; utiliser le lien entre translation et parallélogramme ; connaître les propriétés de conservation ; utiliser les translations dans des frises, des pavages et un repère",
         "Translations", "Translations",
         "Fiches de maths 4e sur les translations : image sur un quadrillage et dans un repère, propriétés, parallélogramme, enchaîner des translations, frises. 100 exercices corrigés.",
         "Une translation fait glisser la figure", "A → B et C → D : ABDC est un parallélogramme", body, faq, sets, 11)


if __name__ == "__main__":
    main()
