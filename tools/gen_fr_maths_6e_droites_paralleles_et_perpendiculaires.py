# -*- coding: utf-8 -*-
"""
France Maths 6e : Droites parallèles et perpendiculaires, distance d’un point à une droite
  python3 tools/gen_fr_maths_6e_droites_paralleles_et_perpendiculaires.py
Erreurs : croire que deux droites qui ne se coupent pas sur le dessin sont parallèles, confondre ⊥ et //,
prendre n’importe quel segment pour la distance à une droite.
"""
import random, math
from fr_c4 import *

R = random.Random(60113)
K = Kids(R)
NAMES = ["(d)", "(d’)", "(Δ)", "(e)", "(f)", "(g)"]


def ln(x1, y1, x2, y2, col=INK, w=2.4):
    return line(x1, y1, x2, y2, col, w)


def two_lines(kind):
    cx, cy, L_ = 160, 100, 140
    a = math.radians(R.choice([0, 15, 30, -20, 60, 75, 100, 120]))
    s = []
    if kind == "par":
        off = R.randint(28, 45)
        nx, ny = -math.sin(a) * off, math.cos(a) * off
        for sgn in (-1, 1):
            x0, y0 = cx + sgn * nx, cy + sgn * ny
            s.append(ln(x0 - L_ * math.cos(a), y0 - L_ * math.sin(a), x0 + L_ * math.cos(a), y0 + L_ * math.sin(a), [GREEN, BLUE][sgn > 0]))
    else:
        b = a + math.radians(90 if kind == "perp" else R.choice([55, 65, 115, 125]))
        s.append(ln(cx - L_ * math.cos(a), cy - L_ * math.sin(a), cx + L_ * math.cos(a), cy + L_ * math.sin(a), GREEN))
        s.append(ln(cx - L_ * 0.7 * math.cos(b), cy - L_ * 0.7 * math.sin(b), cx + L_ * 0.7 * math.cos(b), cy + L_ * 0.7 * math.sin(b), BLUE))
    body = "<g>%s</g>" % "".join(s)
    return "<svg xmlns='http://www.w3.org/2000/svg' data-pf='lg' viewBox='0 -10 320 220' width='320' height='230' role='img' aria-label='deux droites'><clipPath id='c'><rect x='0' y='-10' width='320' height='220'/></clipPath><g clip-path='url(#c)'>%s</g></svg>" % body


def s1():
    kind = R.choice(["par", "perp", "sec"])
    ans = {"par": "parallèles", "perp": "perpendiculaires", "sec": "sécantes, mais pas perpendiculaires"}[kind]
    svg = "<div class='qfig'>%s</div>" % two_lines(kind)
    return M(svg + "Avec ta règle et ton équerre, dis comment sont ces deux droites.", ans, [x for x in ["parallèles", "perpendiculaires", "sécantes, mais pas perpendiculaires", "confondues"] if x != ans],
             {"par": "Elles ne se coupent pas et restent toujours à la même distance : elles sont <b>parallèles</b>.",
              "perp": "Elles se coupent en formant un angle droit (vérifié avec l’équerre) : elles sont <b>perpendiculaires</b>.",
              "sec": "Elles se coupent, mais l’angle n’est pas droit : elles sont <b>sécantes, mais pas perpendiculaires</b>."}[kind])


def s2():
    a, b, c = R.sample(NAMES, 3)
    k = R.choice(["pp", "perpperp", "parperp", "nota", "notb"])
    if k == "pp":
        return M("%s // %s et %s // %s. Que peut-on dire de %s et %s ?" % (a, b, b, c, a, c), "%s // %s" % (a, c), ["%s ⊥ %s" % (a, c), "elles sont sécantes", "on ne peut rien dire"],
                 "Si deux droites sont parallèles à une même droite, alors elles sont parallèles entre elles : <b>%s // %s</b>." % (a, c))
    if k == "perpperp":
        return M("%s ⊥ %s et %s ⊥ %s. Que peut-on dire de %s et %s ?" % (a, c, b, c, a, b), "%s // %s" % (a, b), ["%s ⊥ %s" % (a, b), "elles sont sécantes", "on ne peut rien dire"],
                 "Si deux droites sont perpendiculaires à une même droite, alors elles sont parallèles entre elles : <b>%s // %s</b>." % (a, b))
    if k == "parperp":
        return M("%s // %s et %s ⊥ %s. Que peut-on dire de %s et %s ?" % (a, b, c, a, c, b), "%s ⊥ %s" % (c, b), ["%s // %s" % (c, b), "elles ne se coupent pas", "on ne peut rien dire"],
                 "Si deux droites sont parallèles, toute droite perpendiculaire à l’une est perpendiculaire à l’autre : <b>%s ⊥ %s</b>." % (c, b))
    if k == "nota":
        return M("Que signifie « %s ⊥ %s » ?" % (a, b), "%s et %s sont perpendiculaires" % (a, b), ["%s et %s sont parallèles" % (a, b), "%s et %s sont confondues" % (a, b), "%s et %s ne se coupent pas" % (a, b)],
                 "Le symbole ⊥ veut dire <b>perpendiculaires</b>.")
    return M("Que signifie « %s // %s » ?" % (a, b), "%s et %s sont parallèles" % (a, b), ["%s et %s sont perpendiculaires" % (a, b), "%s et %s se coupent" % (a, b), "%s et %s forment un angle droit" % (a, b)],
             "Le symbole // veut dire <b>parallèles</b>.")


def s3():
    P = R.choice("ABCMNP")
    h = R.randint(2, 6)
    xs = R.sample([-4, -3, -2, 2, 3, 4], 2)
    lens = [Fr(round(math.hypot(h, x) * 10), 10) for x in xs]
    sc = 26
    X0, Y0 = 200, 40
    s = [ln(20, Y0 + h * sc, 380, Y0 + h * sc, INK, 2.4), text(372, Y0 + h * sc - 8, "(d)", 15, anchor="end")]
    s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (X0, Y0, RED) + text(X0 + 10, Y0 - 6, P, 16, anchor="start"))
    segs = [(0, Fr(h), "H")] + [(x, l, nm) for x, l, nm in zip(xs, lens, ["K", "L"])]
    R.shuffle(segs)
    for x, l, nm in segs:
        x1 = X0 + x * sc
        s.append(ln(X0, Y0, x1, Y0 + h * sc, BLUE, 2))
        s.append(text(x1, Y0 + h * sc + 20, nm, 15))
        s.append(text((X0 + x1) / 2 + (12 if x >= 0 else -12), Y0 + h * sc / 2, "%s cm" % d(l), 13, anchor="start" if x >= 0 else "end"))
    s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (X0, Y0 + h * sc - 10, X0 + 10, Y0 + h * sc - 10, X0 + 10, Y0 + h * sc, INK))
    svg = wrap(400, Y0 + h * sc + 30, "".join(s), "un point et une droite", lg=True)
    return M("<div class='qfig'>%s</div>Quelle est la distance du point %s à la droite (d) ?" % (svg, P), "%d cm" % h, ["%s cm" % d(l) for l in lens] + ["on ne peut pas savoir"],
             "La distance d’un point à une droite se mesure sur la <b>perpendiculaire</b> : c’est %sH = <b>%d cm</b>, la plus courte." % (P, h))


Q4 = [("Quel instrument permet de tracer une droite perpendiculaire à une autre ?", "l’équerre", ["le compas", "le rapporteur seul", "la gomme"]),
      ("Deux droites perpendiculaires forment…", "quatre angles droits", ["un seul angle aigu", "deux angles obtus", "aucun angle"]),
      ("Deux droites parallèles…", "ne se coupent jamais", ["se coupent en un point", "forment un angle droit", "ont toujours la même longueur"]),
      ("Par un point A extérieur à une droite (d), combien de droites parallèles à (d) peut-on tracer ?", "une seule", ["deux", "aucune", "une infinité"]),
      ("Par un point A, combien de droites perpendiculaires à (d) peut-on tracer ?", "une seule", ["deux", "aucune", "une infinité"]),
      ("Deux droites sécantes ont…", "un seul point commun", ["aucun point commun", "deux points communs", "tous leurs points communs"]),
      ("Dans un rectangle ABCD, les côtés [AB] et [BC] sont…", "perpendiculaires", ["parallèles", "de même longueur", "sécantes non perpendiculaires"]),
      ("Dans un rectangle ABCD, les droites (AB) et (CD) sont…", "parallèles", ["perpendiculaires", "sécantes", "confondues"]),
      ("Pour tracer la parallèle à (d) passant par A, on peut tracer…", "deux perpendiculaires successives avec l’équerre", ["un cercle de centre A", "une seule perpendiculaire", "la médiatrice de [AB]"]),
      ("La distance d’un point à une droite est…", "la longueur du plus court chemin, sur la perpendiculaire", ["la longueur de n’importe quel segment", "toujours 1 cm", "la longueur de la droite"])]


def s4():
    if R.random() < 0.5:
        q, a, w = R.choice(Q4)
        return M(q, a, w, "Réponse : <b>%s</b>." % a)
    L4 = "ABCDEFGH"
    a, b, c, dd = R.sample(L4, 4)
    fig_ = R.choice(["rectangle", "carré"])
    side = R.choice([("(%s%s)" % (a, b), "(%s%s)" % (c, dd), "parallèles"), ("(%s%s)" % (a, b), "(%s%s)" % (b, c), "perpendiculaires"), ("(%s%s)" % (b, c), "(%s%s)" % (dd, a), "parallèles"), ("(%s%s)" % (c, dd), "(%s%s)" % (dd, a), "perpendiculaires")])
    return M("%s%s%s%s est un %s. Les droites %s et %s sont…" % (a, b, c, dd, fig_, side[0], side[1]), side[2], [x for x in ["parallèles", "perpendiculaires", "confondues", "sécantes, mais pas perpendiculaires"] if x != side[2]],
             "Dans un %s, les côtés opposés sont parallèles et les côtés consécutifs sont perpendiculaires : <b>%s</b>." % (fig_, side[2]))


def s5():
    a, b, c, e = R.sample(NAMES, 4)
    k = R.choice(["trois", "quatre", "faux"])
    if k == "trois":
        return M("%s ⊥ %s, %s ⊥ %s et %s // %s. Que peut-on dire de %s et %s ?" % (a, b, c, b, c, e, a, e), "%s // %s" % (a, e), ["%s ⊥ %s" % (a, e), "on ne peut rien dire", "elles sont sécantes"],
                 "%s et %s sont perpendiculaires à %s, donc parallèles ; et %s // %s, donc <b>%s // %s</b>." % (a, c, b, c, e, a, e))
    if k == "quatre":
        return M("%s // %s, %s ⊥ %s et %s ⊥ %s. Que peut-on dire de %s et %s ?" % (a, b, c, a, e, b, c, e), "%s // %s" % (c, e), ["%s ⊥ %s" % (c, e), "on ne peut rien dire", "elles sont sécantes"],
                 "%s ⊥ %s et %s // %s, donc %s ⊥ %s. %s et %s sont perpendiculaires à %s : <b>%s // %s</b>." % (c, a, a, b, c, b, c, e, b, c, e))
    return M("%s ⊥ %s et %s ⊥ %s. Peut-on dire que %s ⊥ %s ?" % (a, b, b, c, a, c), "non : %s // %s" % (a, c), ["oui", "on ne peut rien dire", "non : %s et %s sont sécantes" % (a, c)],
             "%s et %s sont perpendiculaires à la même droite %s : elles sont parallèles, donc <b>%s // %s</b>." % (a, c, b, a, c))


def main():
    seen = set()
    sets = [("Reconnaître des droites", mix(R, seen, [(s1, 20)])), ("Propriétés des droites", mix(R, seen, [(s2, 20)])),
            ("Distance d’un point à une droite", mix(R, seen, [(s3, 20)])), ("Instruments et figures", mix(R, seen, [(s4, 20)])), ("Raisonner en plusieurs étapes", mix(R, seen, [(s5, 20)]))]
    body = L(["Deux droites <b>perpendiculaires</b> (⊥) se coupent en formant un angle droit. Deux droites <b>parallèles</b> (//) ne se coupent jamais.",
              "Si deux droites sont perpendiculaires à une même droite, elles sont parallèles. Si deux droites sont parallèles, toute perpendiculaire à l’une est perpendiculaire à l’autre.",
              "La <b>distance</b> d’un point A à une droite (d) est la longueur AH, où H est le pied de la perpendiculaire à (d) passant par A."],
             [("(d) ⊥ (Δ) et (d’) ⊥ (Δ)", ["deux perpendiculaires à la même droite"], "(d) // (d’)")],
             [["Croire que deux droites sont parallèles parce qu’on ne voit pas où elles se coupent", "Des droites sont infinies : on vérifie l’écart avec l’équerre et la règle."],
              ["Confondre ⊥ et //", "⊥ : perpendiculaires ; // : parallèles."],
              ["Prendre n’importe quel segment pour la distance", "La distance se mesure sur la perpendiculaire : c’est le chemin le plus court."]])
    faq = [("Comment vérifier que deux droites sont perpendiculaires ?", "On place l’angle droit de l’équerre sur le point d’intersection, un côté le long d’une droite."),
           ("Deux droites qui ne se coupent pas sur le dessin sont-elles parallèles ?", "Pas forcément : il faut vérifier, car les droites se prolongent.")]
    unit("6e", R, "droites-paralleles-et-perpendiculaires", "E",
         "Connaître les positions relatives de deux droites ; tracer des perpendiculaires et des parallèles ; raisonner avec les propriétés des droites parallèles et perpendiculaires ; déterminer la distance d’un point à une droite",
         "Droites parallèles et perpendiculaires", "Parallèles et perpendiculaires",
         "Fiches de maths 6e sur les droites parallèles et perpendiculaires : reconnaître, propriétés, distance d’un point à une droite et raisonnement. 100 exercices corrigés.",
         "⊥ : angle droit. // : ne se coupent jamais.", "Deux perpendiculaires à une même droite sont parallèles.", body, faq, sets, 13)


if __name__ == "__main__":
    main()
