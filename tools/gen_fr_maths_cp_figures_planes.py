# -*- coding: utf-8 -*-
"""
France Maths CP : Les figures planes ; CE1 (build(1)) : Figures planes et angles droits
  python3 tools/gen_fr_maths_cp_figures_planes.py
CP : carré, rectangle, triangle, disque ; côtés et sommets ; compter des figures. CE1 : polygones, angle droit (équerre),
aigu et obtus, milieu d’un segment (exercices du générateur CE2 avec un autre tirage).
Erreurs : croire qu’un carré tourné n’est plus un carré, confondre carré et rectangle, compter un sommet deux fois.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, NB, wrap, text, line, INK, RED, GREEN
import k_pics as KP
import gen_fr_maths_ce2_figures_planes_et_angles_droits as FP
import gen_fr_maths_ce2_longueurs_et_perimetres as LP

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53014 + 100 * lv)
    K = Kids(R)
    FP.R = R
    LP.R = R
    if lv == 1:
        FP.NAMES = [n for n in FP.NAMES if n != "losange"]
        FP.SHAPES_RA = [t for t in FP.SHAPES_RA if t[0] != "losange"]
        FP.RIDDLE = [t for t in FP.RIDDLE if "losange" not in t[1] and "losange" not in " ".join(t[2])]


FRN = {"circle": "un disque", "square": "un carré", "rectangle": "un rectangle", "triangle": "un triangle", "hexagon": "un hexagone"}
FRP = {"circle": "disques", "square": "carrés", "rectangle": "rectangles", "triangle": "triangles", "hexagon": "hexagones"}
COLS = ["red", "blue", "yellow", "green"]


def s1():
    k = R.choice(["carré", "rectangle", "triangle", "triangle rectangle", "disque", "carré", "rectangle"])
    if k == "disque":
        svg = pic(KP.one_shape_svg("circle", R.choice(COLS)), "une figure plane", lg=True)
    else:
        svg = FP.shape(k)
    ans = "un triangle" if k.startswith("triangle") else "un " + k
    w = [x for x in ["un carré", "un rectangle", "un triangle", "un disque"] if x != ans]
    why = {"carré": "4 côtés de même longueur", "rectangle": "4 côtés : 2 longs et 2 courts", "triangle": "3 côtés", "triangle rectangle": "3 côtés", "disque": "un bord tout rond, sans côté"}[k]
    return mcq("<div class='qfig'>%s</div>Comment s’appelle cette figure ?" % svg, ans, w, "Cette figure a %s : c’est <b>%s</b>." % (why, ans))


def s2():
    k = R.choice(["carré", "rectangle", "triangle", "triangle rectangle", "pentagone", "hexagone"])
    n = {"carré": 4, "rectangle": 4, "triangle": 3, "triangle rectangle": 3, "pentagone": 5, "hexagone": 6}[k]
    word = R.choice(["côtés", "sommets"])
    return mcq("<div class='qfig'>%s</div>Combien de %s a cette figure ?" % (FP.shape(k), word), str(n), [str(x) for x in (n - 1, n + 1, n + 2, 2 * n) if x != n and x > 0],
               "On compte les %s un par un : <b>%d</b>." % (word, n))


def s3():
    kinds = ["circle", "square", "rectangle", "triangle"]
    cnt = {k: R.randint(1, 4) for k in kinds}
    items = [(k, R.choice(COLS)) for k in kinds for _ in range(cnt[k])]
    R.shuffle(items)
    t = R.choice(kinds)
    seed = R.randint(1, 10 ** 6)
    svg = pic(KP.shapes_mix_svg(items, seed, cols=5, rows=4), "des figures mélangées", lg=True)
    v = cnt[t]
    return mcq("<div class='qfig'>%s</div>Combien y a-t-il de %s ?" % (svg, FRP[t]), str(v), [str(v + 1), str(v - 1) if v > 1 else str(v + 2), str(len(items))],
               "On compte seulement les %s : <b>%d</b>." % (FRP[t], v))


OBJETS = [("Une fenêtre carrée", "un carré"), ("Une porte", "un rectangle"), ("Une roue de vélo", "un disque"), ("Un panneau « Attention »", "un triangle"),
          ("Une assiette", "un disque"), ("Une feuille de cahier", "un rectangle"), ("Une part de pizza", "un triangle"), ("Une case d’un damier", "un carré"),
          ("Une pièce de 1 €", "un disque"), ("Un tableau de la classe", "un rectangle"), ("Une face d’un dé", "un carré"), ("Une horloge ronde", "un disque"),
          ("Un timbre", "un rectangle"), ("Une tranche de fromage coupée en deux par la diagonale", "un triangle")]
DEV = [("J’ai 3 côtés et 3 sommets. Qui suis-je ?", "un triangle", ["un carré", "un rectangle", "un disque"]),
       ("J’ai 4 côtés de la même longueur. Qui suis-je ?", "un carré", ["un rectangle", "un triangle", "un disque"]),
       ("J’ai 4 côtés : 2 longs et 2 courts. Qui suis-je ?", "un rectangle", ["un carré", "un triangle", "un disque"]),
       ("Je n’ai pas de côté et je suis tout rond. Qui suis-je ?", "un disque", ["un carré", "un triangle", "un rectangle"]),
       ("Combien de côtés a un triangle ?", "3", ["4", "2", "5"]), ("Combien de sommets a un carré ?", "4", ["3", "5", "8"]),
       ("Combien de côtés a un rectangle ?", "4", ["2", "3", "6"]), ("Combien de sommets a un disque ?", "0", ["1", "4", "3"])]


def s4():
    if R.random() < 0.6:
        o, a = R.choice(OBJETS)
        return mcq("%s a la forme de quelle figure ?" % o, a, [x for x in ["un carré", "un rectangle", "un triangle", "un disque"] if x != a], "%s a la forme d’<b>%s</b>." % (o, a[3:] if False else a) if False else
                   "%s a la forme %s." % (o, "d’<b>%s</b>" % a))
    q, a, w = R.choice(DEV)
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


def s5():
    """assembler des figures : combien de carrés / triangles dans une figure"""
    k = R.choice(["deux_tri", "carres", "quatre_tri", "rect2"])
    if k == "deux_tri":
        return mcq("On coupe un carré en deux en suivant une diagonale (d’un sommet à l’autre). Quelles figures obtient-on ?", "2 triangles", ["2 carrés", "2 rectangles", "4 triangles"],
                   "La diagonale coupe le carré en <b>2 triangles</b>.")
    if k == "rect2":
        return mcq("On met deux carrés pareils côte à côte. Quelle figure obtient-on ?", "un rectangle", ["un grand carré", "un triangle", "un disque"],
                   "Deux carrés côte à côte font une figure longue avec 4 angles droits : <b>un rectangle</b>.")
    if k == "carres" or R.random() < 0.7:
        n, m = R.randint(1, 4), R.randint(2, 6)
        s = []
        u = 40
        for i in range(n):
            for j in range(m):
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#cfe6d6' stroke='%s' stroke-width='2'/>" % (10 + j * u, 10 + i * u, u, u, GREEN))
        svg = wrap(20 + m * u, 20 + n * u, "".join(s), "une figure faite de petits carrés", lg=True)
        v = n * m
        big = "ce grand carré" if n == m else "ce rectangle"
        return mcq("<div class='qfig'>%s</div>Combien de petits carrés forment %s ?" % (svg, big), str(v), [str(n + m), str(v + 1), str(v - 1) if v > 2 else str(v + 2)],
                   "%s de %d petits carrés : %s = <b>%d</b>." % (pl(n, "rangée"), m, " + ".join([str(m)] * n), v))
    return mcq("On coupe un carré en suivant ses deux diagonales. Combien de triangles obtient-on ?", "4", ["2", "3", "8"], "Les deux diagonales font <b>4 triangles</b>.")


# ------------------------------------------------ CE1
def e1():
    k = R.choice(["carré", "rectangle", "triangle rectangle", "triangle", "pentagone", "hexagone"])
    w = [FP.ART[n] for n in ["carré", "rectangle", "triangle rectangle", "triangle", "pentagone", "hexagone"] if n != k]
    R.shuffle(w)
    if k in FP.CONF:
        w = [c for c in FP.CONF[k] if c != "un losange"] + w
    return mcq("<div class='qfig'>%s</div>Comment s’appelle cette figure ?" % FP.shape(k), FP.ART[k], w, "Cette figure a %s C’est <b>%s</b>." % (FP.WHY[k], FP.ART[k]))


PROP1 = [("Combien de sommets a un pentagone ?", "5", ["4", "6", "10"]), ("Combien d’angles droits a un triangle qui n’est pas rectangle ?", "0", ["1", "2", "3"]),
         ("Un triangle rectangle a combien de côtés ?", "3", ["4", "2", "1"]), ("Avec quel instrument trace-t-on un segment bien droit ?", "la règle", ["le compas", "la gomme", "le taille-crayon"])]


def e2():
    q, a, w = R.choice([t for t in FP.PROP if "losange" not in t[0] + t[1]] + PROP1)
    alt = [x for x in ["un triangle", "un pentagone", "un hexagone", "un cercle"] if x != a and x not in w]
    w = [alt.pop(0) if x == "un losange" else x for x in w]
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


def regle_pts(a, b):
    svg = LP.regle(a * 10, b * 10)
    return svg


def e5():
    k = R.choice(["mes", "regle", "plie", "regle"])
    if k == "mes":
        n = 2 * R.randint(2, 9)
        return mcq("Un segment mesure %d cm. À quelle distance de chaque extrémité est son milieu ?" % n, "%d cm" % (n // 2), ["%d cm" % n, "%d cm" % (n // 2 + 1), "%d cm" % (2 * n)],
                   "Le milieu partage le segment en deux parties égales : %d ÷ 2 = <b>%d cm</b>." % (n, n // 2) if False else
                   "Le milieu partage le segment en deux parties égales : la moitié de %d est <b>%d cm</b>." % (n, n // 2))
    if k == "regle":
        a = R.randint(0, 4)
        b = a + 2 * R.randint(2, 5)
        if b > 14:
            return None
        m = (a + b) // 2
        return mcq("<div class='qfig'>%s</div>Le segment rouge va de %d à %d sur la règle. Sur quel nombre est son milieu ?" % (regle_pts(a, b), a, b), str(m), [str((b - a) // 2), str(m + 1), str(b - 1)],
                   "Le segment mesure %d cm ; la moitié, c’est %d cm. %d + %d = <b>%d</b>." % (b - a, (b - a) // 2, a, (b - a) // 2, m))
    return mcq("Comment trouver le milieu d’un segment sans règle graduée ?", "en pliant pour que les deux extrémités se touchent",
               ["en pliant n’importe où", "en mesurant seulement un côté", "avec une équerre seulement"], "On plie la feuille pour superposer les deux extrémités : le pli passe par <b>le milieu</b>.")


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Reconnaître les figures", mix(R, seen, [(s1, 20)])), ("Côtés et sommets", mix(R, seen, [(s2, 20)])),
                ("Compter des figures", mix(R, seen, [(s3, 20)])), ("Figures autour de nous", mix(R, seen, [(s4, 20)])),
                ("Assembler et découper", mix(R, seen, [(s5, 20)]))]
        th = ["Un <b>carré</b> a 4 côtés de même longueur. Un <b>rectangle</b> a 4 côtés : 2 longs et 2 courts.",
              "Un <b>triangle</b> a 3 côtés et 3 sommets. Un <b>disque</b> est tout rond.",
              "Un carré reste un carré même s’il est tourné."]
        ex = example("Une figure a 3 côtés", ["3 côtés, 3 sommets"], "un triangle")
        mist = [["Croire qu’un carré tourné n’est plus un carré", "On regarde les côtés, pas la position."],
                ["Confondre carré et rectangle", "Le carré a 4 côtés égaux ; le rectangle a 2 longueurs différentes."],
                ["Compter un sommet deux fois", "On fait une marque sur chaque sommet compté."]]
        faq = [("Qu’est-ce qu’un sommet ?", "C’est un « coin » de la figure, là où deux côtés se rencontrent."),
               ("Un disque a-t-il des côtés ?", "Non : il n’a ni côté ni sommet.")]
        unit(lv, R, "figures-planes", "E",
             "Reconnaître et nommer le carré, le rectangle, le triangle et le disque ; utiliser les mots côté et sommet ; reconnaître des figures dans un assemblage",
             "Les figures planes", "Figures planes",
             "Fiches de maths CP sur les figures planes : carré, rectangle, triangle, disque, côtés et sommets, compter des figures et formes autour de nous. 100 exercices corrigés.",
             "Carré : 4 côtés égaux. Triangle : 3 côtés.", "Un carré tourné reste un carré.", lesson(th, [ex], mist), faq, sets, 14)
        return
    sets = [("Reconnaître les figures", mix(R, seen, [(e1, 20)])), ("Côtés, sommets et propriétés", mix(R, seen, [(e2, 20)])),
            ("Les angles droits", mix(R, seen, [(FP.s3_angle, 10), (FP.s3_count, 10)])), ("Devinettes et figures", mix(R, seen, [(FP.s5, 20)])),
            ("Le milieu d’un segment", mix(R, seen, [(e5, 20)]))]
    th = ["Un <b>polygone</b> est une figure fermée faite de segments : triangle, carré, rectangle, pentagone, hexagone…",
          "L’<b>équerre</b> sert à vérifier un angle droit. Un angle plus petit est <b>aigu</b>, plus grand <b>obtus</b>.",
          "Le <b>milieu</b> d’un segment le partage en deux parties de même longueur."]
    ex = example("Un rectangle", ["4 côtés, 4 angles droits"], "les côtés opposés ont la même longueur")
    mist = [["Croire qu’un carré tourné n’est plus un carré", "On vérifie les côtés et les angles, pas la position."],
            ["Vérifier un angle droit à l’œil", "On utilise l’équerre."],
            ["Mettre le milieu n’importe où", "On mesure, puis on prend la moitié de la longueur."]]
    faq = [("Un carré est-il un rectangle ?", "Oui : il a 4 angles droits. C’est un rectangle dont les 4 côtés sont égaux."),
           ("Comment vérifier un angle droit ?", "On pose le coin de l’équerre sur le sommet de l’angle, un bord sur un côté.")]
    unit(lv, R, "figures-planes-et-angles-droits", "E",
         "Reconnaître et nommer des polygones (triangle, carré, rectangle, pentagone, hexagone) ; repérer des angles droits avec l’équerre, des angles aigus et obtus ; trouver le milieu d’un segment",
         "Figures planes et angles droits", "Figures planes et angles droits",
         "Fiches de maths CE1 sur les figures planes : polygones, côtés et sommets, angles droits, aigus et obtus, devinettes et milieu d’un segment. 100 exercices corrigés.",
         "L’équerre vérifie les angles droits.", "Rectangle : 4 angles droits.", lesson(th, [ex], mist), faq, sets, 14)


if __name__ == "__main__":
    build(0)
