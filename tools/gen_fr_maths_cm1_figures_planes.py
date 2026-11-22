# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Figures planes, droites perpendiculaires et parallèles (Espace et géométrie)
  python3 tools/gen_fr_maths_cm1_figures_planes.py
Triangles (rectangle, isocèle, équilatéral), quadrilatères (carré, rectangle, losange ; CM2 : trapèze, trapèze rectangle,
pentagone, hexagone), codages, droites perpendiculaires et parallèles, cercle et disque, propriétés et programmes de construction.
Erreurs : un carré tourné « n’est plus un carré », croire que deux droites qui ne se coupent pas sur le dessin sont parallèles,
confondre rayon et diamètre, cercle et disque.
"""
import random, math
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, wrap, text, line, INK, RED, GREEN, FILL, BLUE
import gen_fr_maths_ce2_figures_planes_et_angles_droits as CE

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52121 + 100 * lv)
    K = Kids(R)
    CE.R = R


def tick(p, q, n=1):
    mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dy)
    nx, ny = -dy / d * 6, dx / d * 6
    s = []
    for i in range(n):
        o = (i - (n - 1) / 2.0) * 5
        cx, cy = mx + dx / d * o, my + dy / d * o
        s.append(line(cx - nx, cy - ny, cx + nx, cy + ny, RED, 2))
    return "".join(s)


def rmark(c, a, b, sz=12):
    ua = ((a[0] - c[0]), (a[1] - c[1]))
    ub = ((b[0] - c[0]), (b[1] - c[1]))
    la, lb = math.hypot(*ua), math.hypot(*ub)
    p1 = (c[0] + ua[0] / la * sz, c[1] + ua[1] / la * sz)
    p2 = (c[0] + ub[0] / lb * sz, c[1] + ub[1] / lb * sz)
    p3 = (p1[0] + ub[0] / lb * sz, p1[1] + ub[1] / lb * sz)
    return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (p1[0], p1[1], p3[0], p3[1], p2[0], p2[1], RED)


def tri(kind):
    if kind == "équilatéral":
        a = R.randint(90, 130)
        p = [(0, a * math.sqrt(3) / 2), (a, a * math.sqrt(3) / 2), (a / 2, 0)]
        extra = tick(p[0], p[1]) + tick(p[1], p[2]) + tick(p[2], p[0])
    elif kind == "isocèle":
        b, h = R.randint(70, 110), R.randint(110, 150)
        p = [(0, h), (b, h), (b / 2, 0)]
        extra = tick(p[1], p[2]) + tick(p[2], p[0])
    elif kind == "rectangle":
        a, b = R.randint(80, 140), R.randint(60, 110)
        if abs(a - b) < 15:
            raise ValueError
        p = [(0, 0), (0, b), (a, b)]
        extra = rmark(p[1], p[0], p[2])
    elif kind == "rectangle isocèle":
        a = R.randint(80, 120)
        p = [(0, 0), (0, a), (a, a)]
        extra = rmark(p[1], p[0], p[2]) + tick(p[0], p[1]) + tick(p[1], p[2])
    else:
        a, h = R.randint(110, 150), R.randint(70, 110)
        x = R.randint(20, 50)
        if abs(h * h - x * (a - x)) < 0.3 * h * h:
            raise ValueError
        p = [(0, h), (a, h), (x, 0)]
        extra = ""
    s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (" ".join("%.1f,%.1f" % q for q in p), FILL, GREEN) + extra
    xs, ys = [q[0] for q in p], [q[1] for q in p]
    return wrap(max(xs) + 30, max(ys) + 30, "<g transform='translate(15,15)'>%s</g>" % s, "un triangle avec des codages")


TRI = ["équilatéral", "isocèle", "rectangle", "rectangle isocèle", "quelconque"]


def s1():
    k = R.choice(TRI)
    right = "un triangle " + k
    w = ["un triangle " + x for x in TRI if x != k]
    why = {"équilatéral": "ses 3 côtés sont codés égaux", "isocèle": "2 côtés sont codés égaux", "rectangle": "il a un angle droit (codé)",
           "rectangle isocèle": "il a un angle droit et 2 côtés égaux", "quelconque": "il n’a ni côtés égaux ni angle droit"}[k]
    return mcq("<div class='qfig'>%s</div>Regarde les codages. Quel est ce triangle ?" % tri(k), right, w, "Les codages indiquent que %s : c’est <b>%s</b>." % (why, right))


def quad(kind):
    a = R.choice([0, 0, R.uniform(-0.4, 0.4)])
    if kind == "trapèze":
        w, h, t1, t2 = R.randint(130, 170), R.randint(60, 90), R.randint(20, 40), R.randint(20, 50)
        p = [(t1, 0), (w - t2, 0), (w, h), (0, h)]
    elif kind == "trapèze rectangle":
        w, h, t = R.randint(130, 170), R.randint(60, 90), R.randint(30, 60)
        p = [(0, 0), (w - t, 0), (w, h), (0, h)]
    elif kind == "parallélogramme":
        w, h, t = R.randint(110, 150), R.randint(60, 90), R.randint(30, 50)
        p = [(t, 0), (w + t, 0), (w, h), (0, h)]
    else:
        return CE.shape(kind)
    return CE.poly(CE.rot(p, a), "une figure plane")


QUADS = ["carré", "rectangle", "losange"]
QUADS2 = ["carré", "rectangle", "losange", "trapèze", "trapèze rectangle", "pentagone", "hexagone"]


def s2():
    pool = QUADS + ["pentagone", "hexagone", "triangle"] if L == 1 else QUADS2
    k = R.choice(pool)
    art = {"carré": "un carré", "rectangle": "un rectangle", "losange": "un losange", "trapèze": "un trapèze", "trapèze rectangle": "un trapèze rectangle",
           "pentagone": "un pentagone", "hexagone": "un hexagone", "triangle": "un triangle"}
    conf = {"carré": ["un losange", "un rectangle"], "rectangle": ["un carré", "un parallélogramme"] if L == 2 else ["un carré", "un losange"], "losange": ["un carré", "un rectangle"],
            "trapèze": ["un trapèze rectangle", "un parallélogramme"], "trapèze rectangle": ["un trapèze", "un rectangle"], "pentagone": ["un hexagone", "un carré"],
            "hexagone": ["un pentagone", "un losange"], "triangle": ["un rectangle", "un losange"]}[k]
    pic = quad(k) if k in ("trapèze", "trapèze rectangle") else CE.shape(k)
    why = {"carré": "4 côtés égaux et 4 angles droits", "rectangle": "4 angles droits", "losange": "4 côtés égaux sans angle droit", "trapèze": "2 côtés parallèles (et seulement 2)",
           "trapèze rectangle": "2 côtés parallèles et 2 angles droits", "pentagone": "5 côtés", "hexagone": "6 côtés", "triangle": "3 côtés"}[k]
    rest = [art[x] for x in pool if art[x] not in conf and x != k]
    R.shuffle(rest)
    return mcq("<div class='qfig'>%s</div>Comment s’appelle cette figure ?" % pic, art[k], conf + rest, "Elle a %s : c’est <b>%s</b>." % (why, art[k]))


def lines_svg(angles, labels):
    W, H = 300, 200
    s = ["<rect x='0' y='0' width='%d' height='%d' fill='#ffffff'/>" % (W, H)]
    cols = [GREEN, BLUE, RED, INK]
    for i, (a, off) in enumerate(angles):
        r = math.radians(a)
        cx, cy = W / 2 + off * math.sin(r), H / 2 - off * math.cos(r)
        dx, dy = math.cos(r) * 170, -math.sin(r) * 170
        s.append(line(cx - dx, cy - dy, cx + dx, cy + dy, cols[i], 2.4))
        f = [0.8, -0.6, 0.45][i]
        lx, ly = cx + dx * f, cy + dy * f
        s.append(text(min(max(lx + 10, 12), W - 14), min(max(ly - 6, 14), H - 6), labels[i], 14, col=cols[i]))
    return wrap(W, H, "<clipPath id='cl'><rect x='0' y='0' width='%d' height='%d'/></clipPath><g clip-path='url(#cl)'>%s</g>" % (W, H, "".join(s)), "des droites", lg=True)


def s3():
    base = R.choice([0, 20, 35, 60, 110, 150])
    k = R.choice(["par", "perp"])
    a1 = base
    a2 = base if k == "par" else base + 90
    a3 = base + R.choice([40, 55, 130, 25])
    lab = ["(d₁)", "(d₂)", "(d₃)"]
    R.shuffle(lab)
    offs = [-40, 45, R.randint(-20, 20)] if k == "par" else [0, 0, 60]
    if k == "perp":
        offs = [R.randint(-30, 30), R.randint(-40, 40), 70]
    pic = lines_svg([(a1, offs[0]), (a2, offs[1]), (a3, offs[2])], lab)
    q = "Quelles droites sont %s ?" % ("parallèles" if k == "par" else "perpendiculaires")
    pair = lambda x, y: "%s et %s" % tuple(sorted([x, y]))
    right = pair(lab[0], lab[1])
    return mcq("<div class='qfig'>%s</div>%s" % (pic, q), right, [pair(lab[0], lab[2]), pair(lab[1], lab[2]), "aucune"],
               ("%s ne se coupent jamais, même si on les prolonge : elles sont <b>parallèles</b>." % right if k == "par" else
                "%s se coupent en formant un angle droit (vérifie avec l’équerre) : elles sont <b>perpendiculaires</b>." % right))


def s3b():
    q = R.choice([("Deux droites perpendiculaires se coupent en formant…", "un angle droit", ["un angle aigu", "un angle obtus", "elles ne se coupent pas"]),
                  ("Deux droites parallèles…", "ne se coupent jamais", ["se coupent en formant un angle droit", "se coupent toujours", "ont la même longueur"]),
                  ("Quel instrument permet de tracer une droite perpendiculaire à une autre ?", "l’équerre", ["le compas", "la règle graduée seule", "la gomme"]),
                  ("Dans un rectangle, deux côtés opposés sont…", "parallèles", ["perpendiculaires", "de longueurs différentes", "sécants"]),
                  ("Dans un rectangle, deux côtés consécutifs sont…", "perpendiculaires", ["parallèles", "égaux", "sécants sans angle droit"]),
                  ("Si (d₁) est perpendiculaire à (d₃) et (d₂) est perpendiculaire à (d₃), alors (d₁) et (d₂) sont…", "parallèles", ["perpendiculaires", "sécantes", "on ne peut pas savoir"])])
    return mcq(q[0], q[1], q[2], "Réponse : <b>%s</b>." % q[1])


def s4():
    k = R.random()
    if k < 0.55:
        it = CE.s4()
        return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None
    r = R.randint(2, 9)
    d = R.choice([r - 1, r + 1, r, r + 2, 2 * r])
    if d == r and R.random() < 0.5:
        d = r - 1 if r > 2 else r + 1
    where = "sur le cercle" if d == r else "à l’intérieur du disque" if d < r else "à l’extérieur du disque"
    return mcq("Un cercle de centre O a un rayon de %d cm. Le point A est à %d cm de O. Où est le point A ?" % (r, d), where,
               [x for x in ["sur le cercle", "à l’intérieur du disque", "à l’extérieur du disque", "au centre"] if x != where],
               "Tous les points du cercle sont à %d cm de O. A est à %d cm : il est <b>%s</b>." % (r, d, where))


def s5():
    if L == 2 and R.random() < 0.5:
        q = R.choice([
            ("Programme : trace un segment [AB] de 5 cm ; trace la perpendiculaire à (AB) en A et en B ; place C et D à 5 cm de B et de A, du même côté. Quelle figure ABCD obtiens-tu ?", "un carré", ["un rectangle", "un losange", "un trapèze"]),
            ("Programme : trace un segment [AB] de 6 cm ; trace la perpendiculaire en A et en B ; place D et C à 3 cm de A et de B, du même côté. Quelle figure ABCD obtiens-tu ?", "un rectangle", ["un carré", "un losange", "un trapèze"]),
            ("Programme : trace un cercle de centre O ; trace deux diamètres [AC] et [BD] perpendiculaires. Quelle figure ABCD obtiens-tu ?", "un carré", ["un rectangle", "un trapèze", "un pentagone"]),
            ("Programme : trace [AB] de 4 cm ; avec le compas, trouve C à 4 cm de A et de B. Quelle figure ABC obtiens-tu ?", "un triangle équilatéral", ["un triangle rectangle", "un triangle isocèle seulement", "un carré"]),
            ("Programme : trace deux droites parallèles ; place A et B sur la première, C et D sur la seconde, avec AB ≠ DC. Quelle figure ABCD obtiens-tu ?", "un trapèze", ["un rectangle", "un losange", "un carré"]),
            ("Programme : trace un angle droit de sommet A ; place B sur un côté à 4 cm de A et C sur l’autre à 4 cm de A. Quelle figure ABC obtiens-tu ?", "un triangle rectangle isocèle", ["un triangle équilatéral", "un carré", "un triangle quelconque"])])
        return mcq(q[0], q[1], q[2], "On suit le programme étape par étape et on vérifie avec les outils : <b>%s</b>." % q[1])
    if R.random() < 0.45:
        it = CE.s5()
        if it and "Qui suis-je" not in it["q"]:
            return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])
        return None
    q = R.choice([
        ("Je suis un quadrilatère avec 4 côtés égaux et 4 angles droits. Qui suis-je ?", "un carré", ["un losange", "un rectangle", "un trapèze"]),
        ("Je suis un quadrilatère avec 4 angles droits ; mes côtés opposés sont égaux. Qui suis-je ?", "un rectangle", ["un losange", "un trapèze", "un pentagone"]),
        ("Je suis un quadrilatère avec 4 côtés égaux, sans angle droit. Qui suis-je ?", "un losange", ["un carré", "un rectangle", "un hexagone"]),
        ("Je suis un triangle qui a 2 côtés de même longueur. Qui suis-je ?", "un triangle isocèle", ["un triangle équilatéral", "un triangle rectangle", "un carré"]),
        ("Je suis un triangle qui a 3 côtés de même longueur. Qui suis-je ?", "un triangle équilatéral", ["un triangle isocèle seulement", "un triangle rectangle", "un losange"]),
        ("Je suis un triangle qui a un angle droit. Qui suis-je ?", "un triangle rectangle", ["un triangle équilatéral", "un rectangle", "un losange"]),
        ("Le segment qui va du centre à un point du cercle s’appelle…", "un rayon", ["un diamètre", "une corde", "un côté"]),
        ("La surface à l’intérieur d’un cercle s’appelle…", "un disque", ["un rayon", "un cercle", "une boule"]),
        ("Un carré est-il un losange ?", "oui, il a 4 côtés égaux", ["non, jamais", "seulement s’il est tourné", "non, il a des angles droits"]),
        ("Un carré est-il un rectangle ?", "oui, il a 4 angles droits", ["non, jamais", "seulement s’il est grand", "oui, il a 3 côtés"]),
        ("Que signifient deux petits traits identiques sur deux côtés ?", "ces côtés ont la même longueur", ["ces côtés sont parallèles", "l’angle est droit", "les côtés sont perpendiculaires"]),
        ("Que signifie un petit carré dessiné dans un angle ?", "l’angle est droit", ["les côtés sont égaux", "l’angle est aigu", "les droites sont parallèles"])])
    return mcq(q[0], q[1], q[2], "Réponse : <b>%s</b>." % q[1])


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Les triangles et leurs codages", mix(R, seen, [(s1, 20)])),
        ("Quadrilatères et polygones", mix(R, seen, [(s2, 20)])),
        ("Perpendiculaires et parallèles", mix(R, seen, [(s3, 14), (s3b, 6)])),
        ("Cercle et disque", mix(R, seen, [(s4, 20)])),
        ("Propriétés et devinettes" if lv == 1 else "Programmes de construction et propriétés", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Les <b>codages</b> donnent des informations : traits identiques = côtés de même longueur ; petit carré = angle droit.",
         "Triangle <b>isocèle</b> : 2 côtés égaux. <b>Équilatéral</b> : 3 côtés égaux. <b>Rectangle</b> : un angle droit.",
         "Carré : 4 côtés égaux et 4 angles droits. Rectangle : 4 angles droits. Losange : 4 côtés égaux." + (" Trapèze : 2 côtés parallèles." if lv == 2 else ""),
         "Deux droites <b>perpendiculaires</b> se coupent en formant un angle droit. Deux droites <b>parallèles</b> ne se coupent jamais.",
         "Le <b>cercle</b> est la ligne ; le <b>disque</b> est la surface. Diamètre = 2 %s rayon." % FOIS],
        [example("Un triangle avec deux côtés codés et un angle droit", ["2 côtés égaux : isocèle", "un angle droit : rectangle"], "triangle rectangle isocèle")],
        [["Croire qu’un carré tourné n’est plus un carré", "Il garde ses 4 côtés égaux et ses 4 angles droits."],
         ["Dire que deux droites sont parallèles parce qu’elles ne se coupent pas sur le dessin", "On les prolonge : si elles finissent par se couper, elles ne sont pas parallèles."],
         ["Confondre cercle et disque", "Le cercle est le bord ; le disque est l’intérieur."]])
    faq = [("Un triangle équilatéral est-il isocèle ?", "Oui : il a même 3 côtés égaux, donc au moins 2."),
           ("Comment vérifier que deux droites sont parallèles ?", "On trace une perpendiculaire à l’une : elle doit être aussi perpendiculaire à l’autre. On peut aussi mesurer l’écart en deux endroits.")]
    unit(lv, R, "figures-planes", "E",
         ("Utiliser le vocabulaire géométrique et les instruments ; connaître les codages ; décrire le cercle et le disque ; reconnaître la perpendicularité et le parallélisme ; nommer et reconnaître triangle, triangle rectangle, isocèle, équilatéral, carré, rectangle, losange et leurs propriétés" if lv == 1 else
          "Reconnaître la perpendicularité et le parallélisme ; nommer et reconnaître les triangles particuliers, le carré, le rectangle, le losange, le trapèze, le trapèze rectangle, le pentagone et l’hexagone et leurs propriétés ; élaborer et suivre un programme de construction"),
         "Figures planes : triangles, quadrilatères, perpendiculaires et parallèles", "Figures planes",
         "Fiches de maths %s sur les figures planes : triangles et codages, carré, rectangle, losange%s, droites perpendiculaires et parallèles, cercle et disque. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", trapèze, programmes de construction"),
         "Traits identiques = côtés égaux ; petit carré = angle droit.", "Perpendiculaires : angle droit. Parallèles : ne se coupent jamais.",
         body, faq, sets, 21)


if __name__ == "__main__":
    build(1)
