# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Les aires (Grandeurs et mesures)
  python3 tools/gen_fr_maths_cm1_aires.py
CM1 : comparer des aires, aire en carreaux et en cm² sur quadrillage, figures composées, aire et périmètre.
CM2 : en plus, dm² et m², conversions, aire du carré et du rectangle par une formule.
Erreurs : confondre aire et périmètre, compter les traits au lieu des carreaux, 1 dm² = 10 cm², oublier l’unité au carré.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, wrap, text, line, FILL, GREEN, INK, NB

R = K = None
L = 1
Q = 22


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52118 + 100 * lv)
    K = Kids(R)


def blob(n, w=7, h=5):
    cells = {(R.randint(1, w - 2), R.randint(1, h - 2))}
    while len(cells) < n:
        x, y = R.choice(sorted(cells))
        dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        c = (x + dx, y + dy)
        if 0 <= c[0] < w and 0 <= c[1] < h:
            cells.add(c)
    return cells


def perim(cells):
    p = 0
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in cells:
                p += 1
    return p


def grid(figs, w=7, h=5, labels=None, unit_lab=None):
    s = []
    for k, cells in enumerate(figs):
        ox = 8 + k * (w * Q + 24)
        for i in range(w + 1):
            s.append(line(ox + i * Q, 8, ox + i * Q, 8 + h * Q, "#c9d6df", 0.8))
        for j in range(h + 1):
            s.append(line(ox, 8 + j * Q, ox + w * Q, 8 + j * Q, "#c9d6df", 0.8))
        for x, y in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1'/>" % (ox + x * Q, 8 + y * Q, Q, Q, FILL, GREEN))
        if labels:
            s.append(text(ox + w * Q / 2.0, 8 + h * Q + 22, labels[k], 16, col=GREEN))
    W = 16 + len(figs) * (w * Q + 24) - 24
    H = 8 + h * Q + (30 if labels else 10)
    if unit_lab:
        s.append(text(8, H + 4, unit_lab, 12, anchor="start", weight=600))
        H += 12
    return wrap(W, H, "".join(s), "figure%s sur quadrillage" % ("s" if len(figs) > 1 else ""), lg=True)


def s1():
    n = R.randint(5, 14)
    c = blob(n)
    lab = "Un carreau = 1 cm²" if R.random() < 0.5 else None
    u = " cm²" if lab else " carreaux"
    p = perim(c)
    return mcq("<div class='qfig'>%s</div>Quelle est l’aire de cette figure%s ?" % (grid([c], unit_lab=lab), " (en carreaux)" if not lab else ""), "%d%s" % (n, u.replace(" ", NB)),
               ["%d%s" % (p, u.replace(" ", NB)) if p != n else "%d%s" % (n + 2, u.replace(" ", NB)), "%d%s" % (n + 1, u.replace(" ", NB)), "%d%s" % (n - 1, u.replace(" ", NB))],
               "On compte les carreaux à l’intérieur : <b>%d%s</b>. (Le périmètre, lui, compte les côtés du tour : %d.)" % (n, u, p))


def s2():
    if R.random() < 0.35:
        n = R.randint(6, 12)
        c = blob(n)
        p = perim(c)
        if p == n:
            return None
        k = R.choice(["aire", "perimetre"])
        right = n if k == "aire" else p
        return mcq("<div class='qfig'>%s</div>Le côté d’un carreau mesure 1 cm. %s de cette figure ?" % (grid([c]), "Quelle est l’aire" if k == "aire" else "Quel est le périmètre"),
                   "%d%s%s" % (right, NB, "cm²" if k == "aire" else "cm"), ["%d%s%s" % (p if k == "aire" else n, NB, "cm²" if k == "aire" else "cm"), "%d%s%s" % (right, NB, "cm" if k == "aire" else "cm²"), "%d%s%s" % (right + 2, NB, "cm²" if k == "aire" else "cm")],
                   "L’aire compte les carreaux (%d cm²) ; le périmètre compte les côtés du tour (%d cm). Réponse : <b>%d %s</b>." % (n, p, right, "cm²" if k == "aire" else "cm"))
    a, b = R.randint(6, 13), R.randint(6, 13)
    ca, cb = blob(a), blob(b)
    right = "A" if a > b else "B" if b > a else "elles ont la même aire"
    return mcq("<div class='qfig'>%s</div>Quelle figure a la plus grande aire ?" % grid([ca, cb], labels=["A", "B"]), right, [x for x in ["A", "B", "elles ont la même aire", "on ne peut pas savoir"] if x != right],
               "A : %d carreaux, B : %d carreaux. Réponse : <b>%s</b>." % (a, b, right))


def s3():
    Lg, l = R.randint(3, 15), R.randint(2, 10)
    if Lg == l and L == 1:
        return None
    u = R.choice(["cm", "m"] if L == 2 else ["cm"])
    if L == 1 and Lg <= 7 and l <= 5:
        cells = {(x, y) for x in range(Lg) for y in range(l)}
        return mcq("<div class='qfig'>%s</div>Le côté d’un carreau mesure 1 cm. Quelle est l’aire du rectangle ?" % grid([cells], w=max(Lg, 7), h=max(l, 5)),
                   "%d%scm²" % (Lg * l, NB), ["%d%scm²" % (2 * (Lg + l), NB) if 2 * (Lg + l) != Lg * l else "%d%scm²" % (Lg * l + 1, NB), "%d%scm²" % (Lg + l, NB), "%d%scm" % (Lg * l, NB)],
                   "%d rangées de %d carreaux : %d %s %d = <b>%d cm²</b>." % (l, Lg, l, FOIS, Lg, Lg * l))
    if Lg == l:
        return mcq("Quelle est l’aire d’un carré de %d%s%s de côté ?" % (Lg, NB, u), "%d%s%s²" % (Lg * Lg, NB, u), ["%d%s%s²" % (4 * Lg, NB, u) if 4 * Lg != Lg * Lg else "%d%s%s²" % (Lg * Lg + 1, NB, u), "%d%s%s²" % (2 * Lg, NB, u), "%d%s%s" % (Lg * Lg, NB, u)],
                   "Aire du carré = côté %s côté = %d %s %d = <b>%d %s²</b>." % (FOIS, Lg, FOIS, Lg, Lg * Lg, u))
    return mcq("Quelle est l’aire d’un rectangle de %d%s%s sur %d%s%s ?" % (Lg, NB, u, l, NB, u), "%d%s%s²" % (Lg * l, NB, u), ["%d%s%s²" % (2 * (Lg + l), NB, u) if 2 * (Lg + l) != Lg * l else "%d%s%s²" % (Lg * l + 1, NB, u), "%d%s%s²" % (Lg + l, NB, u), "%d%s%s" % (Lg * l, NB, u)],
               "Aire du rectangle = longueur %s largeur = %d %s %d = <b>%d %s²</b>." % (FOIS, Lg, FOIS, l, Lg * l, u))


def s4_cm1():
    a, b, c, d = R.randint(3, 6), R.randint(2, 4), R.randint(1, 3), R.randint(1, 3)
    if c >= a:
        return None
    cells = {(x, y) for x in range(a) for y in range(b)} | {(x, y) for x in range(c) for y in range(b, b + d)}
    n = len(cells)
    return mcq("<div class='qfig'>%s</div>Le côté d’un carreau mesure 1 cm. Quelle est l’aire de cette figure ?" % grid([cells], w=max(a, 7), h=max(b + d, 5)),
               "%d%scm²" % (n, NB), ["%d%scm²" % (a * (b + d), NB), "%d%scm²" % (perim(cells), NB) if perim(cells) != n else "%d%scm²" % (n + 2, NB), "%d%scm²" % (a * b, NB)],
               "On découpe en deux rectangles : %d %s %d + %d %s %d = <b>%d cm²</b>." % (a, FOIS, b, c, FOIS, d, n))


def s4_cm2():
    k = R.choice(["dm_cm", "m_dm", "m_cm", "cm_dm", "cmp"])
    a = R.randint(2, 15)
    if k == "dm_cm":
        return mcq("Complète : %d%sdm² = … cm²" % (a, NB), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 dm² = 10 cm %s 10 cm = 100 cm² : <b>%s cm²</b>." % (FOIS, num(a * 100)))
    if k == "m_dm":
        return mcq("Complète : %d%sm² = … dm²" % (a, NB), num(a * 100), [num(a * 10), num(a * 1000), num(a + 100)], "1 m² = 10 dm %s 10 dm = 100 dm² : <b>%s dm²</b>." % (FOIS, num(a * 100)))
    if k == "m_cm":
        return mcq("Complète : %d%sm² = … cm²" % (a, NB), num(a * 10000), [num(a * 100), num(a * 1000), num(a * 100000)], "1 m² = 100 dm² = 10 000 cm² : <b>%s cm²</b>." % num(a * 10000))
    if k == "cm_dm":
        n = a * 100
        return mcq("Complète : %s%scm² = … dm²" % (num(n), NB), str(a), [num(n // 10), num(n * 100), str(a * 10)], "100 cm² = 1 dm² : %s %s 100 = <b>%d dm²</b>." % (num(n), DIV, a))
    x = a * 100 + R.choice([-50, 50, 30])
    big = "%d%sdm²" % (a, NB) if a * 100 > x else "%s%scm²" % (num(x), NB)
    return mcq("Quelle est la plus grande aire : %d%sdm² ou %s%scm² ?" % (a, NB, num(x), NB), big, ["%s%scm²" % (num(x), NB) if big.endswith("dm²") else "%d%sdm²" % (a, NB), "elles sont égales", "on ne peut pas comparer"],
               "%d dm² = %s cm². Réponse : <b>%s</b>." % (a, num(a * 100), big))


def s4():
    return s4_cm1() if L == 1 else s4_cm2()


def s5():
    p = K.next()
    k = R.choice(["carrelage", "peinture", "jardin", "tapis"])
    if k == "carrelage":
        Lg, l = R.randint(3, 8), R.randint(2, 6)
        return mcq("Une salle de bain rectangulaire mesure %d m sur %d m. Combien de carreaux de 1 m² faut-il pour couvrir le sol ?" % (Lg, l), str(Lg * l), [str(2 * (Lg + l)) if 2 * (Lg + l) != Lg * l else str(Lg * l + 1), str(Lg + l), str(Lg * l * 2)],
                   "Aire = %d %s %d = <b>%d m²</b>, donc %d carreaux." % (Lg, FOIS, l, Lg * l, Lg * l))
    if k == "peinture":
        Lg, l, c = R.randint(4, 9), R.randint(2, 3), R.choice([5, 10])
        a = Lg * l
        return mcq("Un mur mesure %d m sur %d m. Un pot de peinture couvre %d m². Combien de pots faut-il au minimum ?" % (Lg, l, c), str(-(-a // c)), [str(a // c) if a % c else str(a // c + 1), str(a), str(2 * (Lg + l) // c + 1)],
                   "Aire : %d %s %d = %d m². %d %s %d : il faut <b>%d</b> pots." % (Lg, FOIS, l, a, a, DIV, c, -(-a // c))) if a % c else None
    if k == "jardin":
        Lg, l = R.randint(8, 25), R.randint(4, 12)
        q = R.choice(["aire", "perimetre"])
        right = "%d m²" % (Lg * l) if q == "aire" else "%d m" % (2 * (Lg + l))
        return mcq(("Un jardin rectangulaire mesure %d m sur %d m. Quelle surface faut-il pour semer du gazon partout ?" if q == "aire" else
                    "Un jardin rectangulaire mesure %d m sur %d m. Quelle longueur de clôture pour en faire le tour ?") % (Lg, l), right,
                   ["%d m" % (2 * (Lg + l)) if q == "aire" else "%d m²" % (Lg * l), "%d %s" % (Lg + l, "m²" if q == "aire" else "m"), "%d %s" % (Lg * l + 2 * (Lg + l), "m²" if q == "aire" else "m")],
                   ("Semer partout : c’est une aire, %d %s %d = <b>%d m²</b>." % (Lg, FOIS, l, Lg * l)) if q == "aire" else ("Faire le tour : c’est un périmètre, (%d + %d) %s 2 = <b>%d m</b>." % (Lg, l, FOIS, 2 * (Lg + l))))
    c = R.randint(2, 6)
    return mcq("%s pose des dalles carrées de 1 m de côté sur une terrasse carrée de %d m de côté. Combien de dalles ?" % (p[0], c), str(c * c), [str(4 * c) if 4 * c != c * c else str(c * c + 1), str(2 * c), str(c)],
               "%d %s %d = <b>%d</b> dalles." % (c, FOIS, c, c * c))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Compter les carreaux", mix(R, seen, [(s1, 20)])),
        ("Comparer des aires, aire et périmètre", mix(R, seen, [(s2, 20)])),
        ("Aire du rectangle et du carré", mix(R, seen, [(s3, 20)])),
        ("Figures composées" if lv == 1 else "cm², dm² et m²", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["L’<b>aire</b> d’une figure est la mesure de sa surface. Sur un quadrillage, on compte les carreaux.",
         "Un <b>centimètre carré</b> (1 cm²) est l’aire d’un carré de 1 cm de côté.",
         "Aire du rectangle = longueur %s largeur. Aire du carré = côté %s côté." % (FOIS, FOIS),
         "Ne pas confondre : le <b>périmètre</b> mesure le tour (en cm), l’aire mesure l’intérieur (en cm²)."] +
        (["1 dm² = 100 cm² ; 1 m² = 100 dm² = 10 000 cm²."] if lv == 2 else []),
        [example("Rectangle de 6 cm sur 4 cm", ["aire : 6 %s 4 = 24 cm²" % FOIS, "périmètre : (6 + 4) %s 2 = 20 cm" % FOIS], "24 cm² et 20 cm")],
        [["Confondre aire et périmètre", "Aire = surface (cm²), périmètre = tour (cm)."],
         ["Compter les traits au lieu des carreaux", "On compte les petits carrés à l’intérieur."],
         ["1 dm² = 10 cm²", "1 dm² est un carré de 10 cm sur 10 cm : 100 cm²."]])
    faq = [("Deux figures de même périmètre ont-elles la même aire ?", "Non : un rectangle de 9 cm sur 1 cm et un carré de 5 cm de côté ont 20 cm de périmètre, mais 9 cm² et 25 cm² d’aire."),
           ("Pourquoi écrit-on cm² ?", "Parce que l’aire se mesure avec des carrés : cm %s cm = cm²." % FOIS)]
    unit(lv, R, "aires", "G",
         ("Comparer des aires de figures planes ; déterminer des aires en utilisant le centimètre carré" if lv == 1 else
          "Comparer et déterminer des aires ; utiliser le centimètre carré, le décimètre carré et le mètre carré et convertir ; déterminer l’aire d’un carré et d’un rectangle"),
         "Les aires", "Aires",
         "Fiches de maths %s sur les aires : compter les carreaux, comparer, aire et périmètre, aire du rectangle et du carré%s et problèmes. 100 exercices corrigés." % (GN(lv), ", figures composées" if lv == 1 else ", cm², dm², m²"),
         "Aire du rectangle = longueur × largeur.", "L’aire se mesure en cm², le périmètre en cm.",
         body, faq, sets, 18)


if __name__ == "__main__":
    build(1)
