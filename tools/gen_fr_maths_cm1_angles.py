# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les angles (Grandeurs et mesures)
  python3 tools/gen_fr_maths_cm1_angles.py
CM1 : vocabulaire (sommet, côtés, angle droit, aigu, obtus), notation (angle ABC), comparer des angles saillants.
CM2 : en plus, le degré (angle droit = 90°), somme et multiple d’un angle, moitié d’un angle (pliage).
Erreurs : croire qu’un angle est plus grand parce que ses côtés sont plus longs, lire la mauvaise lettre pour le sommet,
confondre aigu et obtus.
"""
import random, math
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, wrap, text, line, INK, RED, GREEN, horloge, hm

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52119 + 100 * lv)
    K = Kids(R)


def ang(deg, Lg=110, rot=0, lab=None, x0=30, y0=140):
    a0 = math.radians(rot)
    a1 = math.radians(rot + deg)
    p1 = (x0 + Lg * math.cos(-a0), y0 + Lg * math.sin(-a0))
    p2 = (x0 + Lg * math.cos(-a1), y0 + Lg * math.sin(-a1))
    s = [line(x0, y0, p1[0], p1[1], INK, 3), line(x0, y0, p2[0], p2[1], INK, 3),
         "<path d='M%.1f %.1f A26 26 0 0 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (x0 + 26 * math.cos(-a0), y0 + 26 * math.sin(-a0), x0 + 26 * math.cos(-a1), y0 + 26 * math.sin(-a1), RED)]
    if lab:
        s.append(text(x0 - 12, y0 + 16, lab[1], 15))
        s.append(text(p1[0] + 10, p1[1] + 5, lab[0], 15))
        s.append(text(p2[0] - 6, p2[1] - 8, lab[2], 15))
    return s, [x0, p1[0], p2[0]], [y0, p1[1], p2[1]]


def pic(parts, label):
    xs = sum((p[1] for p in parts), [])
    ys = sum((p[2] for p in parts), [])
    mx, my = min(xs) - 22, min(ys) - 22
    body = "".join(sum((p[0] for p in parts), []))
    return wrap(max(xs) - mx + 22, max(ys) - my + 26, "<g transform='translate(%.1f,%.1f)'>%s</g>" % (-mx, -my, body), label)


def s1():
    deg = R.choice([90, 90] + list(range(20, 85, 5)) + list(range(100, 170, 5)))
    rot = R.choice([0, 0, R.randint(10, 60)])
    right = "un angle droit" if deg == 90 else "un angle aigu" if deg < 90 else "un angle obtus"
    w = [x for x in ["un angle droit", "un angle aigu", "un angle obtus", "un angle plat"] if x != right]
    return mcq("<div class='qfig'>%s</div>Quel est ce type d’angle ?" % pic([ang(deg, rot=rot)], "un angle"), right, w,
               "On compare avec l’équerre : %s." % ("il correspond exactement : c’est <b>un angle droit</b>" if deg == 90 else
                                                     "il est plus petit qu’un angle droit : c’est <b>un angle aigu</b>" if deg < 90 else "il est plus grand qu’un angle droit : c’est <b>un angle obtus</b>"))


def s2():
    a, b, c = R.sample("ABCDEFGHKLMNRST", 3)
    k = R.choice(["sommet", "cote", "nom"])
    deg = R.choice([40, 60, 75, 110, 130])
    p = pic([ang(deg, lab=(a, b, c))], "angle %s%s%s" % (a, b, c))
    if k == "sommet":
        return mcq("<div class='qfig'>%s</div>Quel est le sommet de l’angle %s%s%s ?" % (p, a, b, c), b, [a, c, a + b],
                   "Dans le nom d’un angle, la lettre du <b>milieu</b> est le sommet : <b>%s</b>." % b)
    if k == "cote":
        return mcq("<div class='qfig'>%s</div>Quels sont les côtés de l’angle %s%s%s ?" % (p, a, b, c), "[%s%s) et [%s%s)" % (b, a, b, c), ["[%s%s) et [%s%s)" % (a, b, a, c), "[%s%s) et [%s%s)" % (c, a, c, b), "[%s%s)" % (a, c)],
                   "Les côtés partent du sommet %s : ce sont les demi-droites <b>[%s%s) et [%s%s)</b>." % (b, b, a, b, c))
    return mcq("<div class='qfig'>%s</div>Comment nomme-t-on cet angle marqué en rouge ?" % p, "l’angle %s%s%s" % (a, b, c), ["l’angle %s%s%s" % (b, a, c), "l’angle %s%s%s" % (a, c, b), "l’angle %s%s%s" % (b, c, a)],
               "Le sommet %s s’écrit au milieu : <b>l’angle %s%s%s</b> (ou %s%s%s)." % (b, a, b, c, c, b, a))


def s3():
    d1, d2 = R.sample(list(range(25, 165, 10)), 2)
    if abs(d1 - d2) < 15:
        return None
    l1, l2 = (60, 120) if (d1 > d2) == (R.random() < 0.6) else (120, 60)
    A = ang(d1, Lg=l1, x0=30)
    B = ang(d2, Lg=l2, x0=30 + 2 * max(l1, 70) + 60)
    sA = [text(30 + 10, 175, "A", 16, col=GREEN)]
    sB = [text(30 + 2 * max(l1, 70) + 70, 175, "B", 16, col=GREEN)]
    p = pic([(A[0] + sA, A[1], A[2] + [180]), (B[0] + sB, B[1], B[2])], "deux angles A et B")
    right = "l’angle A" if d1 > d2 else "l’angle B"
    return mcq("<div class='qfig'>%s</div>Quel est le plus grand angle ?" % p, right, ["l’angle B" if right == "l’angle A" else "l’angle A", "ils sont égaux", "celui qui a les côtés les plus longs"],
               "On compare l’ouverture, pas la longueur des côtés (on peut utiliser un calque) : <b>%s</b>." % right)


def s4_fig():
    import gen_fr_maths_ce2_figures_planes_et_angles_droits as FP
    FP.R = R
    it = FP.s3_count()
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def s4_cm1():
    if R.random() < 0.6:
        return s4_fig()
    k = R.choice(["tri", "carre", "rect", "aigu"])
    if k == "tri":
        return mcq("Combien d’angles droits a un triangle rectangle ?", "1", ["2", "3", "0"], "Un triangle rectangle a <b>1</b> angle droit ; les deux autres sont aigus.")
    q = R.choice([("Combien d’angles droits a un rectangle ?", "4", ["2", "1", "0"]), ("Combien d’angles droits a un carré ?", "4", ["2", "3", "0"]),
                  ("Un losange qui n’est pas un carré a-t-il des angles droits ?", "non, aucun", ["oui, 4", "oui, 2", "oui, 1"]),
                  ("Un angle plus petit qu’un angle droit s’appelle…", "un angle aigu", ["un angle obtus", "un angle plat", "un angle rond"]),
                  ("Un angle plus grand qu’un angle droit (mais pas plat) s’appelle…", "un angle obtus", ["un angle aigu", "un angle droit", "un angle nul"]),
                  ("Avec quel instrument vérifie-t-on un angle droit ?", "l’équerre", ["le compas", "la règle graduée", "la gomme"]),
                  ("Combien d’angles aigus a un triangle rectangle ?", "2", ["1", "3", "0"]),
                  ("Un triangle peut-il avoir deux angles droits ?", "non", ["oui", "seulement s’il est grand", "seulement s’il est isocèle"])])
    return mcq(q[0], q[1], q[2], "Réponse : <b>%s</b>." % q[1])


def s4_cm2():
    k = R.choice(["somme", "double", "moitie", "droit", "type"])
    if k == "somme":
        a, b = R.choice(range(10, 80, 5)), R.choice(range(10, 80, 5))
        return mcq("On construit un angle égal à la somme d’un angle de %d° et d’un angle de %d°. Combien mesure-t-il ?" % (a, b), "%d°" % (a + b), ["%d°" % abs(a - b), "%d°" % (a + b + 10), "%d°" % (90 - a - b if a + b < 90 else a + b - 90)],
                   "On place les angles côte à côte : %d° + %d° = <b>%d°</b>%s." % (a, b, a + b, " (un angle obtus)" if a + b > 90 else " (un angle droit)" if a + b == 90 else " (un angle aigu)"))
    if k == "double":
        a, m = R.choice(range(10, 60, 5)), R.choice([2, 3])
        return mcq("Combien mesure un angle %s fois plus grand qu’un angle de %d° ?" % ({2: "deux", 3: "trois"}[m], a), "%d°" % (a * m), ["%d°" % (a + m), "%d°" % (a * m + a), "%d°" % (a * m - 10)],
                   "%d %s %d = <b>%d°</b>." % (a, FOIS, m, a * m))
    if k == "moitie":
        a = R.choice(range(20, 170, 10))
        return mcq("En pliant, on partage un angle de %d° en deux angles égaux. Combien mesure chacun ?" % a, "%d°" % (a // 2), ["%d°" % (a * 2), "%d°" % (a - 2), "%d°" % (a // 2 + 10)],
                   "%d %s 2 = <b>%d°</b>." % (a, DIV, a // 2))
    if k == "droit":
        q = R.choice([("Combien mesure un angle droit ?", "90°", ["100°", "45°", "180°"]), ("Combien mesure la moitié d’un angle droit ?", "45°", ["50°", "90°", "30°"]),
                      ("Un angle de 120°, c’est…", "un angle obtus", ["un angle aigu", "un angle droit", "un angle plat"]), ("Un angle de 35°, c’est…", "un angle aigu", ["un angle obtus", "un angle droit", "un angle plat"])])
        return mcq(q[0], q[1], q[2], "Un angle droit mesure 90°. Réponse : <b>%s</b>." % q[1])
    a = R.choice(range(5, 180, 5))
    if a == 90:
        return None
    right = "aigu" if a < 90 else "obtus"
    return mcq("Un angle mesure %d°. Est-il aigu, droit ou obtus ?" % a, right, ["obtus" if right == "aigu" else "aigu", "droit", "plat"],
               "%d° est %s que 90° : il est <b>%s</b>." % (a, "plus petit" if a < 90 else "plus grand", right))


def s4():
    return s4_cm1() if L == 1 else s4_cm2()


def s5():
    h = R.randint(1, 12)
    m = R.choice([0, 0, 0, 10, 15, 20, 30, 40, 45, 50])
    deg = abs(30 * h - 5.5 * m) % 360
    deg = min(deg, 360 - deg)
    if m and (abs(deg - 90) < 12 and deg != 90 or deg > 165 or deg < 12):
        return None
    if not m and (h == 6 or h == 12):
        return None
    right = "un angle droit" if deg == 90 else "un angle aigu" if deg < 90 else "un angle obtus"
    if L == 2 and not m and R.random() < 0.7:
        return mcq("<div class='qfig'>%s</div>Il est %s. Quel angle forment les deux aiguilles ?" % (horloge(h % 12 or 12, 0), hm(h, 0)), "%d°" % deg, ["%d°" % (deg + 30), "%d°" % (h * 10) if h * 10 != deg else "%d°" % (deg + 60), "%d°" % (deg - 30 if deg > 30 else 90)],
                   "Entre deux chiffres de l’horloge, il y a 360° ÷ 12 = 30°. %d intervalles : <b>%d°</b>." % (deg // 30, deg))
    return mcq("<div class='qfig'>%s</div>Il est %s. Quel angle (le plus petit) forment les deux aiguilles ?" % (horloge(h % 12 or 12, m), hm(h, m)), right, [x for x in ["un angle droit", "un angle aigu", "un angle obtus", "un angle plat"] if x != right],
               "On compare l’angle entre les aiguilles à un angle droit : <b>%s</b>." % right)


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Droit, aigu ou obtus ?", mix(R, seen, [(s1, 20)])),
        ("Nommer un angle", mix(R, seen, [(s2, 20)])),
        ("Comparer des angles", mix(R, seen, [(s3, 20)])),
        ("Angles dans les figures" if lv == 1 else "Mesurer en degrés", mix(R, seen, [(s4, 20)])),
        ("Angles et horloge", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Un angle a un <b>sommet</b> et deux <b>côtés</b>. L’angle ABC a pour sommet B (la lettre du milieu) et pour côtés [BA) et [BC).",
         "On compare un angle à l’angle droit avec l’équerre : plus petit = <b>aigu</b>, égal = <b>droit</b>, plus grand = <b>obtus</b>.",
         "La grandeur d’un angle ne dépend pas de la longueur de ses côtés, seulement de son ouverture."] +
        (["Un angle droit mesure <b>90°</b> (degrés). Pour la somme de deux angles, on les place côte à côte."] if lv == 2 else []),
        [example("L’angle RST", ["sommet : S (la lettre du milieu)", "côtés : [SR) et [ST)"], "angle de sommet S")],
        [["Croire qu’un angle est plus grand parce que ses côtés sont plus longs", "Seule l’ouverture compte."],
         ["Prendre la première lettre pour le sommet", "Le sommet est toujours la lettre du milieu."],
         ["Confondre aigu et obtus", "Aigu = plus petit que l’angle droit (comme une pointe aiguë)."]])
    faq = [("Comment comparer deux angles sans rapporteur ?", "Avec un calque : on reproduit un angle et on le pose sur l’autre en faisant coïncider les sommets et un côté."),
           ("Combien de degrés dans un tour complet ?", "360°. Un angle droit est un quart de tour : 90°.")]
    unit(lv, R, "angles", "G",
         ("Utiliser le lexique et les notations relatives aux angles ; comparer des angles (angles saillants)" if lv == 1 else
          "Utiliser le lexique et les notations relatives aux angles ; comparer des angles ; construire un angle égal à la somme de deux angles ou multiple d’un angle ; construire la moitié d’un angle par pliage ; savoir qu’un angle droit mesure 90°"),
         "Les angles", "Angles",
         "Fiches de maths %s sur les angles : angle droit, aigu, obtus, sommet et côtés, comparer des angles%s et l’horloge. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", mesures en degrés, somme et moitié d’un angle"),
         "Aigu &lt; droit &lt; obtus.", "Le sommet est la lettre du milieu : angle ABC, sommet B.",
         body, faq, sets, 19)


if __name__ == "__main__":
    build(1)
