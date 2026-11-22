# -*- coding: utf-8 -*-
"""
France Maths CE2 : Figures planes et angles droits (Espace et géométrie)
  python3 tools/gen_fr_maths_ce2_figures_planes_et_angles_droits.py
Reconnaître carré, rectangle, losange, triangle, triangle rectangle, cercle, polygones ; côtés et sommets ;
angles droits, angles plus petits ou plus grands qu’un angle droit ; cercle : centre, rayon, diamètre ; devinettes.
Erreurs : un carré tourné n’est plus un carré, le losange a des angles droits, confondre rayon et diamètre.
"""
import random, math
from fr_common import mcq, lesson, example, make_unit, mix, wrap, text, line, INK, FILL, GREEN, RED, NB

R = random.Random(51017)
COLS = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"]


def rot(pts, a, cx=0, cy=0):
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def poly(pts, label, col=None):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = min(xs) - 14, min(ys) - 14
    pts = [(x - mx, y - my) for x, y in pts]
    W, H = max(xs) - min(xs) + 28, max(ys) - min(ys) + 28
    return wrap(W, H, "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % p for p in pts), col or R.choice(COLS), GREEN), label, lg=True)


def shape(kind):
    a = R.choice([0, 0, R.uniform(-0.5, 0.5)])
    if kind == "carré":
        c = R.randint(70, 120)
        p = [(0, 0), (c, 0), (c, c), (0, c)]
    elif kind == "rectangle":
        w, h = R.randint(120, 180), R.randint(50, 95)
        p = [(0, 0), (w, 0), (w, h), (0, h)]
    elif kind == "losange":
        w, h = R.randint(70, 110), R.randint(110, 160)
        p = [(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)]
    elif kind == "triangle rectangle":
        w, h = R.randint(80, 150), R.randint(60, 120)
        p = [(0, 0), (0, h), (w, h)]
    elif kind == "triangle":
        w, h = R.randint(100, 150), R.randint(70, 120)
        x = R.randint(25, w - 25)
        if abs(h * h - x * (w - x)) < 0.25 * h * h:
            raise ValueError("presque droit")
        p = [(0, h), (w, h), (x, 0)]
    elif kind == "pentagone":
        r = R.randint(55, 75)
        p = [(r * math.cos(2 * math.pi * i / 5 - math.pi / 2), r * math.sin(2 * math.pi * i / 5 - math.pi / 2)) for i in range(5)]
    else:
        r = R.randint(55, 75)
        p = [(r * math.cos(2 * math.pi * i / 6), r * math.sin(2 * math.pi * i / 6)) for i in range(6)]
    return poly(rot(p, a), "une figure plane")


NAMES = ["carré", "rectangle", "losange", "triangle rectangle", "triangle", "pentagone", "hexagone"]
ART = {"carré": "un carré", "rectangle": "un rectangle", "losange": "un losange", "triangle rectangle": "un triangle rectangle", "triangle": "un triangle",
       "pentagone": "un pentagone", "hexagone": "un hexagone", "cercle": "un cercle"}
CONF = {"carré": ["un losange", "un rectangle"], "rectangle": ["un carré", "un losange"], "losange": ["un carré", "un rectangle"],
        "triangle rectangle": ["un triangle", "un rectangle"], "triangle": ["un triangle rectangle", "un losange"], "pentagone": ["un hexagone", "un carré"],
        "hexagone": ["un pentagone", "un losange"]}
WHY = {"carré": "4 côtés égaux et 4 angles droits.", "rectangle": "4 angles droits ; les côtés opposés sont égaux.", "losange": "4 côtés égaux mais pas d’angle droit.",
       "triangle rectangle": "3 côtés et un angle droit.", "triangle": "3 côtés, sans angle droit.", "pentagone": "5 côtés.", "hexagone": "6 côtés."}


def s1():
    k = R.choice(NAMES)
    w = CONF[k] + [ART[n] for n in NAMES if ART[n] not in CONF[k] and n != k]
    return mcq("<div class='qfig'>%s</div>Comment s’appelle cette figure ?" % shape(k), ART[k], w, "Cette figure a %s C’est <b>%s</b>." % (WHY[k], ART[k]))


PROP = [("Combien de côtés a un pentagone ?", "5", ["6", "4", "8"]), ("Combien de côtés a un hexagone ?", "6", ["5", "8", "4"]),
        ("Combien de sommets a un triangle ?", "3", ["4", "2", "6"]), ("Combien de sommets a un rectangle ?", "4", ["2", "8", "6"]),
        ("Combien d’angles droits a un carré ?", "4", ["2", "0", "1"]), ("Combien d’angles droits a un rectangle ?", "4", ["2", "0", "1"]),
        ("Combien d’angles droits a un triangle rectangle ?", "1", ["2", "3", "0"]), ("Combien d’angles droits a un losange qui n’est pas un carré ?", "0", ["4", "2", "1"]),
        ("Quelle figure a 4 côtés égaux et 4 angles droits ?", "un carré", ["un losange", "un rectangle", "un hexagone"]),
        ("Quelle figure a 4 côtés égaux mais pas d’angle droit ?", "un losange", ["un carré", "un rectangle", "un triangle"]),
        ("Quelle figure a 4 angles droits et des côtés de deux longueurs différentes ?", "un rectangle", ["un carré", "un losange", "un pentagone"]),
        ("Quelle figure a 3 côtés et un angle droit ?", "un triangle rectangle", ["un rectangle", "un triangle", "un carré"]),
        ("Comment s’appelle une figure fermée faite de segments ?", "un polygone", ["un cercle", "une droite", "un solide"]),
        ("Un carré est-il aussi un rectangle ?", "oui, il a 4 angles droits", ["non, jamais", "seulement s’il est grand", "oui, car il a 3 côtés"]),
        ("Un carré est-il aussi un losange ?", "oui, il a 4 côtés égaux", ["non, jamais", "seulement s’il est tourné", "non, car il a des angles droits"]),
        ("Dans un rectangle, combien de côtés ont la même longueur que le plus long côté ?", "2", ["4", "1", "3"]),
        ("Quel instrument utilise-t-on pour vérifier un angle droit ?", "l’équerre", ["le compas", "la règle graduée", "la gomme"]),
        ("Quel instrument utilise-t-on pour tracer un cercle ?", "le compas", ["l’équerre", "la règle", "le crayon seul"]),
        ("Combien de côtés a un octogone ?", "8", ["6", "10", "7"]), ("Combien de côtés a un quadrilatère ?", "4", ["3", "5", "8"]),
        ("Combien de sommets a un hexagone ?", "6", ["5", "12", "8"]), ("Combien de côtés a un panneau « Stop » ?", "8", ["6", "5", "4"])]


def s2():
    q, a, w = R.choice(PROP)
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


def angle_svg(deg):
    L = 110
    x0, y0 = 30, 140
    a = math.radians(deg)
    x1, y1 = x0 + L * math.cos(-a), y0 + L * math.sin(-a)
    s = [line(x0, y0, x0 + L, y0, INK, 3), line(x0, y0, x1, y1, INK, 3),
         "<path d='M%.1f %.1f A28 28 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0 + 28, y0, x0 + 28 * math.cos(-a), y0 + 28 * math.sin(-a), RED)]
    xs = [x0, x0 + L, x1]
    mx = min(xs) - 12
    W = max(xs) - mx + 12
    return wrap(W, 160, "<g transform='translate(%.1f,0)'>%s</g>" % (-mx, "".join(s)), "un angle")


def s3_angle():
    deg = R.choice([90, 90, 90] + list(range(25, 80, 5)) + list(range(105, 165, 5)))
    right = "un angle droit" if deg == 90 else "plus petit qu’un angle droit" if deg < 90 else "plus grand qu’un angle droit"
    w = [x for x in ["un angle droit", "plus petit qu’un angle droit", "plus grand qu’un angle droit", "on ne peut pas savoir"] if x != right]
    if deg == 90 and R.random() < 0.6:
        return None
    return mcq("<div class='qfig'>%s</div>Avec ton équerre, compare cet angle à un angle droit." % angle_svg(deg), right, w,
               "On pose l’équerre sur l’angle. Cet angle est <b>%s</b>%s." % (right, "" if deg == 90 else " (il est %s)" % ("aigu" if deg < 90 else "obtus")))


SHAPES_RA = [("carré", 4), ("rectangle", 4), ("triangle rectangle", 1), ("losange", 0), ("triangle", 0)]


def trapeze():
    w, h, t = R.randint(120, 170), R.randint(60, 100), R.randint(30, 60)
    return poly([(0, 0), (w - t, 0), (w, h), (0, h)], "une figure plane"), 2


def maison():
    w, h, r = R.randint(90, 130), R.randint(60, 90), R.randint(35, 60)
    return poly([(0, r), (w / 2, 0), (w, r), (w, r + h), (0, r + h)], "une figure plane"), 2


def s3_count():
    k = R.choice(["sh", "sh", "trap", "maison"])
    if k == "sh":
        n, v = R.choice(SHAPES_RA)
        pic = shape(n)
    elif k == "trap":
        pic, v = trapeze()
    else:
        pic, v = maison()
    return mcq("<div class='qfig'>%s</div>Combien d’angles droits a cette figure ?" % pic, str(v), [str(x) for x in (0, 1, 2, 3, 4) if x != v],
               "On vérifie chaque angle avec l’équerre : <b>%d</b> angle%s droit%s." % (v, "s" if v > 1 else "", "s" if v > 1 else ""))


def cercle_svg(r, seg):
    cx = cy = 90
    s = ["<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.2'/>" % (cx, cy, r, FILL, GREEN),
         "<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, INK), text(cx - 10, cy - 6, "O", 14)]
    a = R.uniform(0, 2 * math.pi)
    x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
    if seg == "rayon":
        s.append(line(cx, cy, x1, y1, RED, 3))
    else:
        s.append(line(cx - r * math.cos(a), cy - r * math.sin(a), x1, y1, RED, 3))
    return wrap(180, 180, "".join(s), "un cercle de centre O et un segment rouge")


def s4():
    k = R.choice(["r2d", "d2r", "seg", "seg", "cmp"])
    if k == "r2d":
        r = R.randint(2, 15)
        return mcq("Le rayon d’un cercle mesure %d%scm. Combien mesure son diamètre ?" % (r, NB), "%d%scm" % (2 * r, NB), ["%d%scm" % (r, NB), "%d%scm" % (r + 2, NB), "%d%scm" % (4 * r, NB)],
                   "Le diamètre est le double du rayon : 2 × %d = <b>%d cm</b>." % (r, 2 * r))
    if k == "d2r":
        d = 2 * R.randint(2, 15)
        return mcq("Le diamètre d’un cercle mesure %d%scm. Combien mesure son rayon ?" % (d, NB), "%d%scm" % (d // 2, NB), ["%d%scm" % (d, NB), "%d%scm" % (2 * d, NB), "%d%scm" % (d - 2, NB)],
                   "Le rayon est la moitié du diamètre : %d ÷ 2 = <b>%d cm</b>." % (d, d // 2))
    if k == "seg":
        seg = R.choice(["rayon", "diamètre"])
        r = R.randint(45, 80)
        return mcq("<div class='qfig'>%s</div>Comment s’appelle le segment rouge ?" % cercle_svg(r, seg), "un " + seg, ["un diamètre" if seg == "rayon" else "un rayon", "le centre", "un côté"],
                   ("Il relie le centre O à un point du cercle : c’est <b>un rayon</b>." if seg == "rayon" else "Il passe par le centre O et relie deux points du cercle : c’est <b>un diamètre</b>."))
    r = R.randint(3, 12)
    return mcq("Pour tracer un cercle de %d%scm de diamètre, quel écartement donnes-tu au compas ?" % (2 * r, NB), "%d%scm" % (r, NB), ["%d%scm" % (2 * r, NB), "%d%scm" % (r + 1, NB), "%d%scm" % (4 * r, NB)],
               "L’écartement du compas est le rayon : %d ÷ 2 = <b>%d cm</b>." % (2 * r, r))


RIDDLE = [("Je suis un quadrilatère. J’ai 4 angles droits et mes 4 côtés ont la même longueur. Qui suis-je ?", "un carré", ["un rectangle", "un losange", "un triangle"]),
          ("Je suis un quadrilatère. J’ai 4 angles droits, mais mes côtés n’ont pas tous la même longueur. Qui suis-je ?", "un rectangle", ["un carré", "un losange", "un pentagone"]),
          ("Je suis un quadrilatère. Mes 4 côtés ont la même longueur, mais je n’ai pas d’angle droit. Qui suis-je ?", "un losange", ["un carré", "un rectangle", "un hexagone"]),
          ("J’ai 3 côtés et un de mes angles est droit. Qui suis-je ?", "un triangle rectangle", ["un rectangle", "un carré", "un losange"]),
          ("Je n’ai ni côté ni sommet. Tous mes points sont à la même distance du centre. Qui suis-je ?", "un cercle", ["un carré", "un losange", "une boule"]),
          ("J’ai 5 côtés et 5 sommets. Qui suis-je ?", "un pentagone", ["un hexagone", "un octogone", "un carré"]),
          ("J’ai 6 côtés. Les alvéoles des abeilles ont ma forme. Qui suis-je ?", "un hexagone", ["un pentagone", "un carré", "un octogone"]),
          ("J’ai 3 côtés de la même longueur. Qui suis-je ?", "un triangle", ["un carré", "un losange", "un cercle"])]


def s5():
    if R.random() < 0.45:
        q, a, w = R.choice(RIDDLE)
        return mcq(q, a, w, "Réponse : <b>%s</b>." % a)
    k = R.choice(NAMES[:5] + ["pentagone", "hexagone"])
    n = {"carré": 4, "rectangle": 4, "losange": 4, "triangle rectangle": 3, "triangle": 3, "pentagone": 5, "hexagone": 6}[k]
    word = R.choice(["côtés", "sommets"])
    return mcq("<div class='qfig'>%s</div>Combien de %s a cette figure ?" % (shape(k), word), str(n), [str(x) for x in (n - 1, n + 1, n + 2, 2 * n) if x != n and x > 0],
               "On compte les %s : <b>%d</b>. Une figure a autant de côtés que de sommets." % (word, n))


def main():
    seen = set()
    sets = [
        ("Reconnaître les figures", mix(R, seen, [(s1, 20)])),
        ("Côtés, sommets et propriétés", mix(R, seen, [(s2, 20)])),
        ("Les angles droits", mix(R, seen, [(s3_angle, 10), (s3_count, 10)])),
        ("Le cercle", mix(R, seen, [(s4, 20)])),
        ("Devinettes et figures", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un <b>polygone</b> est une figure fermée faite de segments : ce sont ses <b>côtés</b>. Les coins sont les <b>sommets</b>.",
         "On vérifie un <b>angle droit</b> avec l’équerre. Un angle peut être droit, plus petit ou plus grand qu’un angle droit.",
         "Le <b>carré</b> : 4 côtés égaux et 4 angles droits. Le <b>rectangle</b> : 4 angles droits. Le <b>losange</b> : 4 côtés égaux. Le <b>triangle rectangle</b> : un angle droit.",
         "Le <b>cercle</b> a un centre. Le <b>rayon</b> va du centre au cercle ; le <b>diamètre</b> traverse le cercle en passant par le centre : diamètre = 2 × rayon."],
        [example("Un carré tourné sur sa pointe", ["4 côtés égaux", "4 angles droits"], "c’est toujours un carré"),
         example("Rayon 5 cm", ["diamètre = 2 × 5"], "10 cm")],
        [["Croire qu’un carré tourné est un losange", "Il garde ses 4 angles droits : c’est un carré (et aussi un losange particulier)."],
         ["Dire qu’un losange a des angles droits", "Un losange n’a pas d’angle droit, sauf s’il est un carré."],
         ["Confondre rayon et diamètre", "Le diamètre est deux fois plus long que le rayon."]])
    faq = [("Un carré est-il un rectangle ?", "Oui. Il a 4 angles droits, comme le rectangle, et en plus ses 4 côtés sont égaux."),
           ("Comment vérifier un angle droit sans équerre ?", "On peut plier une feuille deux fois pour fabriquer un gabarit d’angle droit.")]
    make_unit(R, "figures-planes-et-angles-droits", "E",
              "Reconnaître, nommer et décrire des figures planes (carré, rectangle, losange, triangle, triangle rectangle, polygones, cercle) ; utiliser le vocabulaire côté, sommet, angle droit, centre, rayon, diamètre ; repérer des angles droits avec l’équerre (résumé du programme 2024 du cycle 2).",
              "Figures planes et angles droits", "Figures planes CE2 : fiches et exercices avec corrigé", "Figures planes et angles droits",
              "Fiches de maths CE2 sur les figures planes : carré, rectangle, losange, triangle rectangle, polygones, angles droits avec l’équerre, cercle, rayon et diamètre. 100 exercices corrigés.",
              "Carré : 4 côtés égaux et 4 angles droits.", "Le diamètre d’un cercle est le double du rayon.",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
