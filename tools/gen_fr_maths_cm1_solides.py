# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les solides et leurs patrons (Espace et géométrie)
  python3 tools/gen_fr_maths_cm1_solides.py
Nommer et décrire cube, pavé droit, prisme droit, pyramide, cylindre, cône, boule ; faces, arêtes, sommets ; nature des faces ;
patrons du cube ; CM2 : patron du pavé (dimensions des faces) ; assemblages de cubes. Réutilise des fonctions du CE2.
Erreurs : confondre prisme et pyramide, oublier les faces cachées, patron avec deux faces superposées, faces du pavé mal appariées.
"""
import random
from fr_c3 import mcq, lesson, example, unit, mix, Kids, GN, FOIS, wrap, text, FILL, GREEN, INK, NB, table
import gen_fr_maths_ce2_solides as CE

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52123 + 100 * lv)
    K = Kids(R)
    CE.R = R
    CE.DE.R = R


def re(it):
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def prisme_svg(col):
    w, h, d = R.randint(70, 100), R.randint(50, 70), R.randint(25, 40)
    A, B, C = (10, 10 + h), (10 + w, 10 + h), (10 + w / 2.0, 10)
    A2, B2, C2 = [(x + d, y - d * 0.6) for x, y in (A, B, C)]
    pts = lambda ps: " ".join("%.1f,%.1f" % p for p in ps)
    s = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (pts([B, B2, C2, C]), col, INK) +
         "<polygon points='%s' fill='%s' fill-opacity='0.6' stroke='%s' stroke-width='2'/>" % (pts([C, C2, A2, A]), col, INK) +
         "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (pts([A, B, C]), col, INK))
    return wrap(w + d + 24, h + 24 + d, "<g transform='translate(2,%d)'>%s</g>" % (int(d * 0.6) + 2, s), "un solide")


def s1():
    if R.random() < 0.3:
        col = R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0"])
        return mcq("<div class='qfig'>%s</div>Comment s’appelle ce solide ?" % prisme_svg(col), "un prisme droit", ["une pyramide", "un pavé droit", "un cône"],
                   "Il a deux faces triangulaires identiques et parallèles, reliées par des rectangles : c’est <b>un prisme droit</b> (à base triangulaire).")
    return re(CE.s1())


SAF = {"un cube": (6, 12, 8), "un pavé droit": (6, 12, 8), "une pyramide à base carrée": (5, 8, 5), "une pyramide à base triangulaire": (4, 6, 4),
       "un prisme droit à base triangulaire": (5, 9, 6), "un prisme droit à base hexagonale": (8, 18, 12), "un prisme droit à base pentagonale": (7, 15, 10)}
NATURE = [("Quelle est la nature des faces latérales d’un prisme droit ?", "des rectangles", ["des triangles", "des disques", "des losanges"]),
          ("Quelles sont les bases d’un prisme droit à base triangulaire ?", "deux triangles identiques", ["un triangle et un carré", "deux rectangles", "un seul triangle"]),
          ("Quelle est la nature des faces latérales d’une pyramide ?", "des triangles", ["des rectangles", "des carrés", "des disques"]),
          ("Quel solide a une seule base et un sommet principal ?", "une pyramide", ["un prisme droit", "un cylindre", "un pavé droit"]),
          ("Quel solide a deux bases identiques et parallèles qui sont des polygones ?", "un prisme droit", ["une pyramide", "un cône", "une boule"]),
          ("Un pavé droit est-il un prisme droit ?", "oui, à base rectangulaire", ["non, jamais", "oui, à base triangulaire", "seulement si c’est un cube"]),
          ("Quel solide a une surface courbe et deux disques ?", "un cylindre", ["un cône", "une boule", "un prisme droit"])]


def s2():
    if R.random() < 0.35:
        q, a, w = R.choice(NATURE)
        return mcq(q, a, w, "Réponse : <b>%s</b>." % a)
    n = R.choice(list(SAF) if L == 2 else list(SAF)[:5])
    i = R.randint(0, 2)
    word = ["faces", "arêtes", "sommets"][i]
    v = SAF[n][i]
    others = [x for x in SAF[n] if x != v] + [v + 2, v - 1, v + 1]
    return mcq("Combien %s a %s ?" % ("d’" + word if word[0] in "aeiou" else "de " + word, n), str(v), [str(x) for x in others if x != v and x > 0],
               "%s a %d faces, %d arêtes et %d sommets : <b>%d</b> %s." % (n[0].upper() + n[1:], SAF[n][0], SAF[n][1], SAF[n][2], v, word))


def s3():
    return re(CE.s4())


def s4_cm2():
    a, b, c = sorted(R.sample(range(2, 10), 3), reverse=True)
    k = R.choice(["dims", "aire", "nb", "dims"])
    f = lambda x, y: "%d cm %s %d cm" % (x, FOIS, y)
    if k == "dims":
        right = "%s, %s et %s (deux fois chacune)" % (f(a, b), f(a, c), f(b, c))
        return mcq("Un pavé droit mesure %d cm de long, %d cm de large et %d cm de haut. Quelles sont les dimensions des 6 faces de son patron ?" % (a, b, c), right,
                   ["%s (six fois)" % f(a, b), "%s, %s et %s (deux fois chacune)" % (f(a, b), f(a, c), f(a, a)), "%s, %s et %s (une fois chacune)" % (f(a, b), f(a, c), f(b, c))],
                   "Les faces opposées d’un pavé sont identiques : <b>%s</b>." % right)
    if k == "aire":
        A = 2 * (a * b + a * c + b * c)
        return mcq("Quelle est l’aire totale du patron d’un pavé droit de %d cm sur %d cm sur %d cm ?" % (a, b, c), "%d%scm²" % (A, NB),
                   ["%d%scm²" % (a * b * c, NB), "%d%scm²" % (A // 2, NB), "%d%scm²" % (6 * a * b, NB)],
                   "2 %s (%d %s %d + %d %s %d + %d %s %d) = 2 %s %d = <b>%d cm²</b>." % (FOIS, a, FOIS, b, a, FOIS, c, b, FOIS, c, FOIS, a * b + a * c + b * c, A))
    q = R.choice([("Combien de faces carrées a le patron d’un pavé droit de %d cm sur %d cm sur %d cm ?" % (a, a, c), "2", ["6", "4", "0"], "Les deux faces %d × %d sont des carrés : <b>2</b>." % (a, a)),
                  ("Combien de rectangles faut-il dessiner pour le patron d’un pavé de %d cm sur %d cm sur %d cm ?" % (a, b, c), "6", ["4", "8", "12"], "Un pavé a 6 faces : <b>6</b> rectangles."),
                  ("Dans le patron d’un pavé de %d cm sur %d cm sur %d cm, combien de faces mesurent %d cm sur %d cm ?" % (a, b, c, b, c), "2", ["1", "4", "6"], "Les faces opposées sont identiques : <b>2</b>.")])
    return mcq(q[0], q[1], q[2], q[3])


def s4():
    if L == 2:
        return s4_cm2()
    return re(CE.s3_faces() if R.random() < 0.4 else CE.s5_plan())


def s5():
    return re(CE.s3_haut() if R.random() < 0.4 else CE.s5_vie() if R.random() < 0.5 else CE.s5_plan())


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Reconnaître les solides", mix(R, seen, [(s1, 20)])),
        ("Faces, arêtes, sommets", mix(R, seen, [(s2, 20)])),
        ("Les patrons du cube", mix(R, seen, [(s3, 20)])),
        ("Faces et assemblages" if lv == 1 else "Le patron du pavé droit", mix(R, seen, [(s4, 20)])),
        ("Assemblages de cubes et solides autour de nous", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un <b>prisme droit</b> a deux bases identiques et parallèles (triangles, rectangles…) reliées par des rectangles. Le pavé droit est un prisme droit.",
         "Une <b>pyramide</b> a une base (polygone) et des faces triangulaires qui se rejoignent au sommet.",
         "On compte les <b>faces</b> (surfaces planes), les <b>arêtes</b> (segments) et les <b>sommets</b> (points), sans oublier ceux qui sont cachés.",
         "Un <b>patron</b> est une figure plane qu’on plie pour fabriquer le solide." + (" Dans le patron d’un pavé, les faces vont par paires identiques." if lv == 2 else "")],
        [example("Prisme droit à base triangulaire", ["2 triangles + 3 rectangles = 5 faces", "9 arêtes, 6 sommets"], "5 faces")],
        [["Confondre prisme et pyramide", "Le prisme a deux bases ; la pyramide une base et un sommet."],
         ["Oublier les faces cachées", "Imagine le solide en vrai, ou compte face par face."],
         ["Un patron où deux faces se superposent", "En pliant, chaque face doit prendre une place différente."]],
        table(["Solide", "Faces", "Arêtes", "Sommets"], [["cube, pavé droit", "6", "12", "8"], ["prisme à base triangulaire", "5", "9", "6"], ["pyramide à base carrée", "5", "8", "5"]]))
    faq = [("Le cube est-il un pavé droit ?", "Oui : c’est un pavé droit dont toutes les faces sont des carrés."),
           ("Combien y a-t-il de patrons du cube ?", "11 patrons différents.")]
    unit(lv, R, "solides-et-patrons", "E",
         ("Nommer et décrire un cube, un pavé droit, un prisme droit, une pyramide, un cylindre, un cône, une boule ; connaître la nature des faces ; reconnaître et construire un patron de cube" if lv == 1 else
          "Nommer et décrire les solides usuels ; reconnaître et construire un patron de cube ; reconnaître un patron de pavé droit"),
         "Les solides et leurs patrons", "Solides et patrons",
         "Fiches de maths %s sur les solides : cube, pavé, prisme droit, pyramide, faces, arêtes, sommets, patrons du cube%s et assemblages de cubes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else " et du pavé"),
         "Prisme : deux bases identiques. Pyramide : une base et un sommet.", "Cube et pavé : 6 faces, 12 arêtes, 8 sommets.",
         body, faq, sets, 23)


if __name__ == "__main__":
    build(1)
