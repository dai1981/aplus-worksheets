# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Tableaux, diagrammes et courbes (Organisation et gestion de données)
  python3 tools/gen_fr_maths_cm1_tableaux_et_graphiques.py
Lire et interpréter un tableau (à double entrée), un diagramme en barres, une courbe ; CM2 : un diagramme circulaire ;
résoudre des problèmes en une ou plusieurs étapes. Réutilise des fonctions du CE2 (autres tirages).
Erreurs : lire la mauvaise ligne, lire entre deux graduations, confondre la plus grande valeur et le plus grand écart.
"""
import random, math
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, wrap, text, line, INK, RED, GREEN, FILL, BLUE, fr, dz
import gen_fr_maths_ce2_tableaux_et_diagrammes as CE

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52124 + 100 * lv)
    K = Kids(R)
    CE.R = R


def re(it):
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def s1():
    return re(CE.s3() if R.random() < 0.6 else CE.s1())


def s2():
    return re(CE.s2() if R.random() < 0.6 else CE.s4())


def courbe(xs, ys, ylab, xlab, step):
    top = int(math.ceil(max(ys) / float(step)) * step)
    lo = 0
    W, H, x0, y0 = 420, 200, 46, 30
    X = lambda i: x0 + i * (W - x0 - 16) / float(len(xs) - 1)
    Y = lambda v: y0 + H - (v - lo) / float(top - lo) * H
    s = []
    for v in range(lo, top + 1, step):
        s.append(line(x0, Y(v), W - 10, Y(v), "#d6d6d6", 1))
        s.append(text(x0 - 6, Y(v) + 4, num(v), 11, anchor="end", weight=400))
    for i, x in enumerate(xs):
        s.append(line(X(i), y0, X(i), y0 + H, "#eeeeee", 1))
        s.append(text(X(i), y0 + H + 16, x, 11, weight=500))
    s.append(line(x0, y0, x0, y0 + H, INK, 2))
    s.append(line(x0, y0 + H, W - 10, y0 + H, INK, 2))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(ys)), BLUE))
    for i, v in enumerate(ys):
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (X(i), Y(v), BLUE))
    s.append(text(6, y0 - 16, ylab, 11, anchor="start", weight=600))
    s.append(text(W - 10, y0 + H + 32, xlab, 11, anchor="end", weight=600))
    return wrap(W, y0 + H + 38, "".join(s), "courbe", lg=True)


def s3():
    k = R.choice(["temp", "taille", "eau"])
    if k == "temp":
        xs = ["%d h" % h for h in range(6, 21, 2)]
        base = R.randint(4, 12)
        ys = [base + int(round(R.randint(8, 14) * math.sin(math.pi * i / (len(xs) - 1)))) + R.randint(0, 2) for i in range(len(xs))]
        ylab, xlab, step, u = "température (°C)", "heure", 2, "°C"
    elif k == "taille":
        xs = ["%d an%s" % (a, "s" if a > 1 else "") for a in range(1, 11)]
        ys = [75 + 9 * i + R.randint(0, 3) for i in range(10)]
        ylab, xlab, step, u = "taille (cm)", "âge", 10, "cm"
    else:
        xs = ["jan", "fév", "mar", "avr", "mai", "juin", "juil"]
        ys = [R.randint(2, 15) * 10 for _ in xs]
        ylab, xlab, step, u = "pluie (mm)", "mois", 20, "mm"
    if len(set(ys)) < len(ys) - 1:
        return None
    if k == "taille":
        ys = [v // 2 * 2 for v in ys]
    q = R.choice(["val", "max", "ecart"])
    pic = courbe(xs, ys, ylab, xlab, step)
    if q == "val":
        i = R.randrange(len(xs))
        if k == "taille" and ys[i] % 10 and ys[i] % 5:
            return None
        if k == "temp" and ys[i] % 2:
            return None
        return mcq("<div class='qfig'>%s</div>Quelle est la valeur pour « %s » ?" % (pic, xs[i]), "%d %s" % (ys[i], u), ["%d %s" % (ys[i] + step, u), "%d %s" % (ys[i] - step // 2 if step > 2 else ys[i] - 1, u), "%d %s" % (ys[(i + 1) % len(ys)], u) if ys[(i + 1) % len(ys)] != ys[i] else "%d %s" % (ys[i] + 2 * step, u)],
                   "On part de « %s », on monte jusqu’à la courbe, puis on lit sur l’axe vertical : <b>%d %s</b>." % (xs[i], ys[i], u))
    if q == "max":
        if k == "taille":
            return None
        m = ys.index(max(ys))
        if ys.count(max(ys)) > 1:
            return None
        return mcq("<div class='qfig'>%s</div>Pour quelle valeur de l’axe horizontal la courbe est-elle la plus haute ?" % pic, xs[m], [xs[j] for j in R.sample([j for j in range(len(xs)) if j != m], 3)],
                   "Le point le plus haut correspond à <b>%s</b> (%d %s)." % (xs[m], ys[m], u))
    if k != "eau":
        return None
    i, j = sorted(R.sample(range(len(xs)), 2))
    d = abs(ys[j] - ys[i])
    if d == 0:
        return None
    return mcq("<div class='qfig'>%s</div>Quel est l’écart de pluie entre « %s » et « %s » ?" % (pic, xs[i], xs[j]), "%d %s" % (d, u), ["%d %s" % (ys[i] + ys[j], u), "%d %s" % (d + step, u), "%d %s" % (max(ys[i], ys[j]), u)],
               "%d − %d = <b>%d %s</b>." % (max(ys[i], ys[j]), min(ys[i], ys[j]), d, u))


def camembert(parts, labels):
    cx, cy, r = 110, 110, 90
    cols = ["#9fc3e8", "#f0c27a", "#9fd39f", "#e8a0a0", "#c9a0e8"]
    s, a0 = [], -math.pi / 2
    tot = float(sum(parts))
    for i, v in enumerate(parts):
        a1 = a0 + 2 * math.pi * v / tot
        big = 1 if a1 - a0 > math.pi else 0
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, big, cx + r * math.cos(a1), cy + r * math.sin(a1), cols[i], INK))
        am = (a0 + a1) / 2
        s.append(text(cx + r * 0.58 * math.cos(am), cy + r * 0.58 * math.sin(am) + 4, labels[i], 12))
        a0 = a1
    return wrap(220, 220, "".join(s), "diagramme circulaire", lg=True)


SPLITS = [(1, 2, 1, 4, 1, 4), (1, 2, 1, 4, 1, 8, 1, 8), (1, 4, 1, 4, 1, 4, 1, 4), (1, 3, 1, 3, 1, 3), (1, 2, 1, 3, 1, 6), (3, 4, 1, 8, 1, 8), (1, 2, 1, 2)]
ACT = ["foot", "danse", "judo", "tennis", "natation"]


def s4_cm2():
    sp = R.choice(SPLITS)
    fr_ = [(sp[i], sp[i + 1]) for i in range(0, len(sp), 2)]
    den = 24
    parts = [n * den // d for n, d in fr_]
    labs = R.sample(ACT, len(parts))
    tot = R.choice([24, 48, 72, 96, 120])
    i = R.randrange(len(parts))
    n, d = fr_[i]
    k = R.choice(["frac", "nb"])
    pic = camembert(parts, labs)
    if k == "frac":
        return mcq("<div class='qfig'>%s</div>Quelle fraction des élèves pratique « %s » ?" % (pic, labs[i]), fr(n, d), [fr(n, d + 1) if d < 8 else fr(n, d // 2), fr(d - n, d) if d - n != n else fr(n, d * 2), fr(1, len(parts)) if fr(1, len(parts)) != fr(n, d) else fr(2, d + 1)],
                   "La part « %s » occupe %s du disque : <b>%s</b>." % (labs[i], fr(n, d), fr(n, d)))
    return mcq("<div class='qfig'>%s</div>%d élèves ont répondu. Combien pratiquent « %s » ?" % (pic, tot, labs[i]), str(tot * n // d), [str(tot // len(parts)) if tot // len(parts) != tot * n // d else str(tot * n // d + 2), str(tot - tot * n // d), str(tot * n // d * 2)],
               "La part « %s » représente %s du disque : %s de %d = <b>%d</b>." % (labs[i], fr(n, d), fr(n, d), tot, tot * n // d))


def s4():
    return s4_cm2() if L == 2 else re(CE.s5())


def s5():
    p = K.next()
    k = R.choice(["tab", "bar"])
    if k == "tab":
        jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]
        v = [R.randint(120, 480) for _ in jours]
        prix = R.choice([2, 3, 5])
        tb = CE.table(["Jour"] + jours, [["Entrées vendues"] + [str(x) for x in v]])
        q = R.choice(["recette", "moyenne", "ecart"])
        if q == "recette":
            i = R.randrange(5)
            return mcq("Une piscine vend des entrées à %d €.<br>%s<br>Quelle est la recette du %s ?" % (prix, tb, jours[i]), "%s €" % num(v[i] * prix), ["%s €" % num(v[i] + prix), "%s €" % num(sum(v) * prix), "%s €" % num(v[i])],
                       "%d entrées %s %d € = <b>%s €</b>." % (v[i], FOIS, prix, num(v[i] * prix)))
        if q == "ecart":
            i, j = v.index(max(v)), v.index(min(v))
            return mcq("%s<br>Combien d’entrées de plus le jour le plus fréquenté que le jour le moins fréquenté ?" % tb, num(v[i] - v[j]), [num(v[i] + v[j]), num(v[i]), num(v[i] - v[j] + 10)],
                       "Le plus : %s (%d). Le moins : %s (%d). Écart : <b>%d</b>." % (jours[i], v[i], jours[j], v[j], v[i] - v[j]))
        tot = sum(v)
        return mcq("%s<br>Combien d’entrées ont été vendues sur la semaine ?" % tb, num(tot), [num(tot - v[-1]), num(tot + 100), num(max(v) * 5)], "%s = <b>%s</b>." % (" + ".join(map(str, v)), num(tot)))
    it = CE.s4()
    return re(it)


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Lire un tableau", mix(R, seen, [(s1, 20)])),
        ("Lire un diagramme en barres", mix(R, seen, [(s2, 20)])),
        ("Lire une courbe", mix(R, seen, [(s3, 20)])),
        ("Compter et compléter" if lv == 1 else "Le diagramme circulaire", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Avant de répondre, on lit le <b>titre</b> et ce que représente chaque axe, ligne ou colonne.",
         "Dans un <b>tableau à double entrée</b>, une case est au croisement d’une ligne et d’une colonne.",
         "Sur un <b>diagramme en barres</b> ou une <b>courbe</b>, on part de l’axe horizontal, on monte jusqu’à la barre ou la courbe, puis on lit la valeur sur l’axe vertical."] +
        (["Dans un <b>diagramme circulaire</b>, chaque part du disque représente une fraction du total : un quart du disque = %s." % fr(1, 4)] if lv == 2 else []),
        [example("Courbe de température : 10 h → 14 °C, 14 h → 22 °C", ["écart : 22 − 14"], "8 °C de plus")],
        [["Lire la mauvaise ligne", "Suis la ligne et la colonne avec ton doigt."],
         ["Lire entre deux graduations au hasard", "Regarde combien vaut chaque graduation avant de lire."],
         ["Additionner pour « combien de plus »", "« Combien de plus » demande une soustraction."]])
    faq = [("Quand utilise-t-on une courbe ?", "Pour montrer comment une grandeur change avec le temps : température, taille…"),
           ("À quoi sert un diagramme circulaire ?", "À voir quelle part du total représente chaque catégorie.")]
    unit(lv, R, "tableaux-et-graphiques", "D",
         "Recueillir des données et les présenter dans un tableau ou un diagramme en barres ; lire et interpréter les données d’un tableau, d’un diagramme en barres%s ou d’une courbe ; résoudre des problèmes en une ou plusieurs étapes" % ("" if lv == 1 else ", d’un diagramme circulaire"),
         "Tableaux, diagrammes et courbes", "Tableaux et graphiques",
         "Fiches de maths %s sur la lecture de données : tableaux à double entrée, diagrammes en barres, courbes%s et problèmes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", diagrammes circulaires"),
         "Je lis le titre et les axes avant de répondre.", "Pour « combien de plus », je fais une soustraction.",
         body, faq, sets, 24)


if __name__ == "__main__":
    build(1)
